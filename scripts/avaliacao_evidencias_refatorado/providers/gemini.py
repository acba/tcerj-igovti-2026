"""Provider Gemini via google-genai: upload de arquivos por File API,
contagem exata de tokens e rotacao automatica de chaves em caso de 429.

Quando ha arquivos para upload (PDFs/imagens), suprime os documentos de texto
do pacote no prompt — o modelo processa os arquivos diretamente via File API,
evitando duplicacao redundante.
"""
from __future__ import annotations

import re
import shutil
import tempfile
import time
from pathlib import Path
from typing import Any, Callable

from .base import GenericProvider, ProviderContext, conteudo_provider_textual
from .http_utils import executar_com_retry_transiente, retry_after_from_exception
from ..utils import nome_upload_seguro


_GEMINI_MAX_TOKENS = 1_048_576


class GeminiKeyRotationManager:
    """Gerencia rotacao de chaves de API Gemini com backoff por chave.

    Quando uma chave recebe 429 (RESOURCE_EXHAUSTED), ela e marcada como
    exaurida por um tempo. A proxima chamada usa outra chave disponivel
    imediatamente, sem esperar. Se todas as chaves estao exauridas, retorna
    o menor tempo de espera entre todas.
    """

    def __init__(self, keys: list[str]):
        self.keys = keys
        self.exhausted_until: dict[str, float] = {}
        self.consecutive_429: dict[str, int] = {}

    def next_available_key(self) -> tuple[str | None, float]:
        now = time.monotonic()
        for key in self.keys:
            until = self.exhausted_until.get(key, 0.0)
            if now >= until:
                return key, 0.0
        waits = [self.exhausted_until[k] - now for k in self.keys if k in self.exhausted_until]
        min_wait = min(waits) if waits else 60.0
        return None, max(0.0, min_wait)

    def mark_exhausted(self, key: str, retry_after_seconds: float) -> None:
        self.exhausted_until[key] = time.monotonic() + max(5.0, retry_after_seconds)
        self.consecutive_429[key] = self.consecutive_429.get(key, 0) + 1

    def reset_key(self, key: str) -> None:
        self.exhausted_until.pop(key, None)
        self.consecutive_429[key] = 0

    def should_abandon_key(self, key: str, *, threshold: int = 5) -> bool:
        return self.consecutive_429.get(key, 0) >= threshold

    def all_exhausted(self) -> bool:
        now = time.monotonic()
        return all(now < self.exhausted_until.get(k, 0.0) for k in self.keys) if self.keys else True

    def available_count(self) -> int:
        now = time.monotonic()
        return sum(1 for k in self.keys if now >= self.exhausted_until.get(k, 0.0))


def _extract_retry_delay_from_gemini_error(exc: BaseException) -> float:
    """Extrai retryDelay (segundos) de uma APIError do Gemini."""
    details = getattr(exc, "details", None)
    if details is None:
        response = getattr(exc, "response", None)
        if response is not None:
            details = getattr(response, "json", lambda: None)()
    if isinstance(details, dict):
        details = [details]
    if isinstance(details, list):
        for detail in details:
            if isinstance(detail, dict) and detail.get("@type") == "type.googleapis.com/google.rpc.RetryInfo":
                delay_str = detail.get("retryDelay", "")
                match = re.match(r"([\d.]+)\s*s", delay_str)
                if match:
                    return float(match.group(1))
    retry_after = retry_after_from_exception(exc)
    if retry_after is not None:
        return retry_after
    return 60.0


def _is_gemini_429(exc: BaseException) -> bool:
    code = getattr(exc, "code", None)
    if code is None:
        response = getattr(exc, "response", None)
        if response is not None:
            code = getattr(response, "status_code", None)
    status = getattr(exc, "status", None) or ""
    return code == 429 or "RESOURCE_EXHAUSTED" in str(status).upper()


class GeminiProvider(GenericProvider):
    name = "gemini"
    supports_pdf_file_upload = True
    supports_images = True
    needs_api_key = True
    env_key = "GEMINI_API_KEY"

    def _build_content(self, ctx: ProviderContext) -> Any:
        # Gemini usa genai.Client; o "content" e montado dentro do _call.
        return None

    def _call(self, ctx: ProviderContext, content: Any) -> Any:
        def emit(event: str, **fields: Any) -> None:
            if ctx.on_event is not None:
                try:
                    ctx.on_event(event, {**fields})
                except Exception:
                    pass

        try:
            from google import genai
            from google.genai import types
        except Exception as exc:
            return {"status": "error", "error": f"google-genai nao disponivel: {exc}"}

        keys = [k.strip() for k in ctx.api_key.split(",") if k.strip()]
        if not keys:
            return {"status": "error", "error": "GEMINI_API_KEY nao contem chaves validas"}

        # Diretorio temporario para copiar arquivos com nomes seguros (ASCII).
        # A File API do Gemini falha com caracteres nao-ASCII no nome do arquivo.
        with tempfile.TemporaryDirectory(prefix="gemini_upload_") as upload_tmp_dir:
            upload_tmp_path = Path(upload_tmp_dir)

            manager = GeminiKeyRotationManager(keys)
            clients: dict[str, Any] = {}
            abandoned: set[str] = set()
            key_rotations: list[dict[str, Any]] = []

            def get_client(key: str) -> Any:
                if key not in clients:
                    clients[key] = genai.Client(api_key=key)
                return clients[key]

            def key_label(key: str) -> str:
                return key[:6] + "..." + key[-4:]

            arquivos_upload = ctx.arquivos_upload
            pacote_prompt = ctx.pacote_textual
            if arquivos_upload:
                pacote_prompt = dict(pacote_prompt)
                pacote_prompt["documentos"] = []
                pacote_prompt["_observacao"] = (
                    "O conteudo da evidencia foi enviado como arquivo anexado via File API. "
                    "Analise diretamente o conteudo dos arquivos anexados."
                )

            contents_base = [
                conteudo_provider_textual(
                    prompt=ctx.prompt,
                    auditado=ctx.auditado,
                    questao_base=ctx.questao_base,
                    coluna_evidencia=ctx.coluna_evidencia,
                    itens_afirmados=ctx.itens_afirmados,
                    pacote=pacote_prompt,
                )
            ]
            config = types.GenerateContentConfig(response_mime_type="application/json")
            if ctx.reasoning_effort:
                config.thinking_config = types.ThinkingConfig(thinking_level=ctx.reasoning_effort)

            max_pausas = 10
            pausas_consecutivas = 0

            while True:
                available_keys = [k for k in keys if k not in abandoned]
                if not available_keys:
                    return {
                        "status": "error",
                        "error": "todas as chaves Gemini foram abandonadas apos 429 excessivo",
                        "key_rotations": key_rotations,
                    }
                manager.keys = available_keys

                key, wait = manager.next_available_key()
                if key is None:
                    pausas_consecutivas += 1
                    if pausas_consecutivas > max_pausas:
                        return {
                            "status": "error",
                            "error": f"todas as chaves Gemini exauridas apos {max_pausas} pausas consecutivas",
                            "all_keys_exhausted": True,
                            "retry_after_seconds": wait,
                            "key_rotations": key_rotations,
                        }
                    return {
                        "status": "error",
                        "error": f"todas as chaves Gemini exauridas — pausando por {wait:.0f}s",
                        "all_keys_exhausted": True,
                        "retry_after_seconds": wait,
                        "key_rotations": key_rotations,
                    }

                client = get_client(key)
                pausas_consecutivas = 0

                uploaded = []
                upload_ok = True
                for arquivo in arquivos_upload:
                    path = Path(arquivo)
                    nome_seguro = nome_upload_seguro(path.name, path.suffix)
                    caminho_seguro = upload_tmp_path / nome_seguro
                    try:
                        shutil.copy2(path, caminho_seguro)
                    except Exception as exc:
                        return {
                            "status": "error",
                            "error": f"erro ao copiar arquivo para upload seguro {arquivo}: {exc}",
                            "key_rotations": key_rotations,
                        }
                    try:
                        uploaded.append(
                            executar_com_retry_transiente(
                                lambda caminho=caminho_seguro: client.files.upload(file=str(caminho)),
                                exclude_429=True,
                            )
                        )
                    except Exception as exc:
                        if _is_gemini_429(exc):
                            delay = _extract_retry_delay_from_gemini_error(exc)
                            manager.mark_exhausted(key, delay)
                            rotation = {
                                "from_key": key_label(key),
                                "reason": "429_no_upload",
                                "retry_after_seconds": delay,
                                "available_keys": manager.available_count(),
                            }
                            key_rotations.append(rotation)
                            emit("gemini_key_rotation", from_key=rotation["from_key"], reason="429_no_upload",
                                 retry_after_seconds=delay, available_keys=manager.available_count())
                            if manager.should_abandon_key(key):
                                abandoned.add(key)
                                emit("gemini_key_abandoned", key=key_label(key), reason="consecutive_429_exceeded")
                            upload_ok = False
                            break
                        return {
                            "status": "error",
                            "error": f"erro ao fazer upload Gemini de {arquivo}: {exc}",
                            "key_rotations": key_rotations,
                        }
                if not upload_ok:
                    continue

                contents = list(contents_base)
                contents.extend(uploaded)

                try:
                    count_resp = client.models.count_tokens(model=self.model, contents=contents)
                    total_tokens_gemini = getattr(count_resp, "total_tokens", 0)
                    if total_tokens_gemini > _GEMINI_MAX_TOKENS:
                        return {
                            "status": "error",
                            "error": (
                                f"payload excede limite de tokens do Gemini: "
                                f"{total_tokens_gemini:,} > {_GEMINI_MAX_TOKENS:,}"
                            ),
                            "tokens_counted": total_tokens_gemini,
                            "key_rotations": key_rotations,
                        }
                except Exception:
                    pass

                try:
                    response = executar_com_retry_transiente(
                        lambda: client.models.generate_content(
                            model=self.model,
                            contents=contents,
                            config=config,
                        ),
                        exclude_429=True,
                    )
                    raw_text = response.text
                    manager.reset_key(key)
                    result = self._interpretar_resposta(raw_text)
                    if key_rotations:
                        result["key_rotations"] = key_rotations
                    return result
                except Exception as exc:
                    if _is_gemini_429(exc):
                        delay = _extract_retry_delay_from_gemini_error(exc)
                        manager.mark_exhausted(key, delay)
                        rotation = {
                            "from_key": key_label(key),
                            "reason": "429_no_generate",
                            "retry_after_seconds": delay,
                            "available_keys": manager.available_count(),
                        }
                        key_rotations.append(rotation)
                        emit("gemini_key_rotation", from_key=rotation["from_key"], reason="429_no_generate",
                             retry_after_seconds=delay, available_keys=manager.available_count())
                        if manager.should_abandon_key(key):
                            abandoned.add(key)
                            emit("gemini_key_abandoned", key=key_label(key), reason="consecutive_429_exceeded")
                        continue
                    result = {"status": "error", "error": f"erro ao chamar Gemini: {exc}"}
                    if key_rotations:
                        result["key_rotations"] = key_rotations
                    return result