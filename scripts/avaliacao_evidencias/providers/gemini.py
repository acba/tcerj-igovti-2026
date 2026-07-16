"""Provider Gemini via google-genai: upload de arquivos por File API,
contagem exata de tokens e rotacao automatica de chaves em caso de 429.

Quando ha arquivos para upload (PDFs/imagens), suprime do prompt apenas os
documentos que correspondem a esses anexos. Comentarios, justificativas e
outros documentos contextuais permanecem no pacote textual.
"""
from __future__ import annotations

import re
import shutil
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Callable

from .base import (
    GenericProvider,
    ProviderContext,
    conteudo_provider_textual,
    pacote_textual_sem_documentos_de_arquivos_nativos,
)
from .http_utils import executar_com_retry_transiente, retry_after_from_exception
from .response import json_schema_response_format
from ..utils import nome_upload_seguro


_GEMINI_MAX_TOKENS = 1_048_576
GEMINI_ALL_KEYS_429_WAIT_SECONDS = 180.0


class GeminiKeyRotationManager:
    """Gerencia ciclos de rotação imediata das chaves Gemini.

    Cada chave que retorna 429 fica indisponível apenas no ciclo corrente. A
    próxima chave é tentada imediatamente. Depois que todas retornarem 429, o
    chamador espera três minutos, inicia um novo ciclo e volta à primeira chave.
    """

    def __init__(self, keys: list[str]):
        self.keys = keys
        self.exhausted_in_cycle: set[str] = set()
        self.reported_retry_after: dict[str, float] = {}

    def next_available_key(self) -> tuple[str | None, float]:
        for key in self.keys:
            if key not in self.exhausted_in_cycle:
                return key, 0.0
        return None, GEMINI_ALL_KEYS_429_WAIT_SECONDS

    def mark_exhausted(self, key: str, retry_after_seconds: float) -> None:
        self.exhausted_in_cycle.add(key)
        self.reported_retry_after[key] = retry_after_seconds

    def reset_key(self, key: str) -> None:
        self.exhausted_in_cycle.discard(key)
        self.reported_retry_after.pop(key, None)

    def start_new_cycle(self) -> None:
        self.exhausted_in_cycle.clear()
        self.reported_retry_after.clear()

    def all_exhausted(self) -> bool:
        return all(k in self.exhausted_in_cycle for k in self.keys) if self.keys else True

    def available_count(self) -> int:
        return sum(1 for k in self.keys if k not in self.exhausted_in_cycle)


def wait_and_restart_key_cycle(
    manager: GeminiKeyRotationManager,
    *,
    emit: Callable[..., None],
    sleeper: Callable[[float], None] = time.sleep,
    stream: Any = None,
) -> float:
    """Informa indisponibilidade total, espera no máximo 180s e reinicia."""
    wait = GEMINI_ALL_KEYS_429_WAIT_SECONDS
    message = (
        "Todas as chaves Gemini estão indisponíveis por erro 429. "
        f"Aguardando {wait:.0f}s antes de iniciar um novo ciclo de rotação."
    )
    output = stream or sys.stderr
    output.write(f"\n[AVISO] {message}\n")
    output.flush()
    emit(
        "gemini_all_keys_429_wait",
        message=message,
        retry_after_seconds=wait,
        available_keys=0,
    )
    sleeper(wait)
    manager.start_new_cycle()
    return wait


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
                extensoes_anexadas = {Path(arquivo).suffix.lower() for arquivo in arquivos_upload}
                pacote_prompt = pacote_textual_sem_documentos_de_arquivos_nativos(
                    ctx.pacote,
                    extensoes_anexadas,
                )
                pacote_prompt["_observacao"] = (
                    "Os arquivos de evidencia foram enviados como anexos via File API. "
                    "Analise diretamente os anexos e preserve o restante do contexto textual."
                )

            contents_base = [
                conteudo_provider_textual(
                    prompt=ctx.prompt,
                    auditado=ctx.auditado,
                    questao_base=ctx.questao_base,
                    coluna_evidencia=ctx.coluna_evidencia,
                    itens_afirmados=ctx.itens_afirmados,
                    pacote=pacote_prompt,
                    response_profile=ctx.response_profile,
                )
            ]
            response_schema = json_schema_response_format(
                response_profile=ctx.response_profile
            )["json_schema"]["schema"]
            config = types.GenerateContentConfig(
                response_mime_type="application/json",
                response_json_schema=response_schema,
            )
            if ctx.reasoning_effort:
                config.thinking_config = types.ThinkingConfig(thinking_level=ctx.reasoning_effort)

            while True:
                key, wait = manager.next_available_key()
                if key is None:
                    wait_and_restart_key_cycle(manager, emit=emit)
                    continue

                client = get_client(key)

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
                except Exception as exc:
                    if _is_gemini_429(exc):
                        delay = _extract_retry_delay_from_gemini_error(exc)
                        manager.mark_exhausted(key, delay)
                        rotation = {
                            "from_key": key_label(key),
                            "reason": "429_no_count_tokens",
                            "retry_after_seconds": delay,
                            "available_keys": manager.available_count(),
                        }
                        key_rotations.append(rotation)
                        emit(
                            "gemini_key_rotation",
                            from_key=rotation["from_key"],
                            reason="429_no_count_tokens",
                            retry_after_seconds=delay,
                            available_keys=manager.available_count(),
                        )
                        continue

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
                    result = self._interpretar_resposta(
                        raw_text,
                        response_profile=ctx.response_profile,
                    )
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
                        continue
                    result = {"status": "error", "error": f"erro ao chamar Gemini: {exc}"}
                    if key_rotations:
                        result["key_rotations"] = key_rotations
                    return result
