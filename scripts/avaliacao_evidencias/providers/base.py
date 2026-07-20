"""Provider generico (ABC) especializado pelos provedores concretos.

O GenericProvider define o template method ``executar`` e expõe flags de
capacidade que cada especialista ajusta:

- ``supports_pdf_file_upload``: envia arquivo PDF nativo via upload do provider
  (File API no Gemini, ``input_file`` em OpenAI Responses). Apenas gemini e openai.
- ``supports_inline_pdf``: envia PDF como base64 inline (OpenRouter, para modelos
  que suportam).
- ``supports_images``: envia imagens (.png/.jpg/.jpeg) como anexos.
- ``needs_api_key``: exige chave de API configurada.

Os metodos ``_build_content`` e ``_call`` sao abstratos; cada especialista
implementa de acordo com o SDK/endpoint do provider.
"""
from __future__ import annotations

import base64
import json
import sys
import time
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Callable

from .http_utils import (
    MAX_TRANSIENT_RETRY_DELAY_SECONDS,
    arquivos_imagem_do_pacote,
    arquivos_pdf_do_pacote,
)
from .response import item_para_dict, validar_resultado_ia


@dataclass
class ProviderContext:
    provider: str
    model: str
    api_key: str
    prompt: str
    auditado: str
    questao_base: str
    coluna_evidencia: str
    itens_afirmados: list[Any]
    pacote: dict[str, Any]
    reasoning_effort: str = ""
    on_event: Callable[[str, dict[str, Any]], None] | None = None
    response_profile: str = "evidence"
    pdf_detail: str = "auto"

    @property
    def arquivos_upload(self) -> list[str]:
        return self.pacote.get("arquivos_upload", []) if isinstance(self.pacote, dict) else []

    @property
    def pacote_textual(self) -> dict[str, Any]:
        return {k: v for k, v in self.pacote.items() if k != "arquivos_upload"} if isinstance(self.pacote, dict) else {}


def conteudo_provider_textual(
    *,
    prompt: str,
    auditado: str,
    questao_base: str,
    coluna_evidencia: str,
    itens_afirmados: list[Any],
    pacote: dict[str, Any],
    response_profile: str = "evidence",
) -> str:
    """Serializa o payload textual enviado ao provider em JSON formatado."""
    conclusao_saida = {
        "item_codigo": "...",
        "item_texto": "...",
        "afirmacao_auditado": "...",
        "estado": "conforme|nao_conforme|erro",
        "justificativa": "...",
        "lacunas": [],
        "arquivos_referenciados": [],
        "trechos_ou_elementos": [],
        "paginas_ou_localizacao": [],
    }
    if response_profile == "manager_comments_temporal":
        conclusao_saida.update(
            {
                "estado_temporal": "mantida|afastada_na_data_base|corrigida_posteriormente",
                "conclusoes_motivos": [
                    {
                        "id_motivo": "...",
                        "estado_motivo": "mantido|afastado",
                        "justificativa": "...",
                    }
                ],
                "providencias_informadas": [],
                "comentarios_encaminhamento": "",
                "consequencias_praticas": [],
                "alternativas_propostas": [],
            }
        )
    payload = {
        "formato_requerido": "JSON",
        "prompt_de_analise": prompt,
        "auditado": auditado,
        "questao_base": questao_base,
        "coluna_evidencia": coluna_evidencia,
        "itens_afirmados": [item_para_dict(item) for item in itens_afirmados],
        "pacote_evidencia": pacote,
        "saida_obrigatoria": {
            "status": "completed",
            "conclusoes": [conclusao_saida],
            "error": "",
        },
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def imagem_para_data_url(path: Path, *, format_openai: bool = False) -> dict[str, Any]:
    suffix = path.suffix.casefold()
    mime = "image/png" if suffix == ".png" else "image/jpeg"
    data_url = f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")
    if format_openai:
        return {"type": "input_image", "image_url": data_url}
    return {"type": "image_url", "image_url": {"url": data_url}}


def pdf_para_data_url(path: Path) -> str:
    return "data:application/pdf;base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def pacote_textual_sem_documentos_de_arquivos_nativos(
    pacote: dict[str, Any],
    extensoes_nativas: set[str],
) -> dict[str, Any]:
    """Remove do pacote textual documentos cujo nome corresponde a arquivos
    que serao enviados nativamente ao provider (ex.: PDF via File API).

    Evita duplicacao de informacao e desperdicio de tokens quando o conteudo
    do arquivo ja sera processado pelo modelo a partir do anexo.
    """
    if not isinstance(pacote, dict):
        return {}
    arquivos_upload = pacote.get("arquivos_upload", [])
    nomes_nativos = {
        Path(str(arquivo)).name
        for arquivo in arquivos_upload
        if Path(str(arquivo)).suffix.lower() in extensoes_nativas
    }
    pacote_textual = {k: v for k, v in pacote.items() if k != "arquivos_upload"}
    documentos = pacote_textual.get("documentos", [])
    pacote_textual["documentos"] = [
        doc
        for doc in documentos
        if not (isinstance(doc, dict) and str(doc.get("nome", "")) in nomes_nativos)
    ]
    return pacote_textual


class GenericProvider:
    """Base para todos os providers de IA do pipeline/consolidacao."""

    name: str = ""
    supports_pdf_file_upload: bool = False
    supports_inline_pdf: bool = False
    supports_images: bool = True
    needs_api_key: bool = True
    env_key: str = ""
    rotate_comma_separated_keys: bool = False

    def __init__(self, model: str):
        self.model = model

    def executar(self, ctx: ProviderContext) -> dict[str, Any]:
        self._validar_chave(ctx)
        content = self._build_content(ctx)
        if self.rotate_comma_separated_keys:
            return self._executar_com_rotacao_429(ctx, content)
        return self._finalizar_resposta(self._call(ctx, content), ctx)

    def _finalizar_resposta(self, raw: Any, ctx: ProviderContext) -> dict[str, Any]:
        # Providers podem retornar diretamente um dict de resultado ja validado
        # (ex.: FakeProvider) ou um dict de erro; nesses casos nao ha texto a
        # interpretar. Strings sao tratadas como resposta textual do modelo.
        if isinstance(raw, dict):
            return raw
        return self._interpretar_resposta(raw, response_profile=ctx.response_profile)

    def _executar_com_rotacao_429(self, ctx: ProviderContext, content: Any) -> dict[str, Any]:
        keys = [key.strip() for key in ctx.api_key.split(",") if key.strip()] or [""]
        while True:
            for index, key in enumerate(keys, start=1):
                attempt_ctx = replace(ctx, api_key=key)
                raw = self._call(attempt_ctx, content)
                if not (isinstance(raw, dict) and raw.get("http_status") == 429):
                    return self._finalizar_resposta(raw, attempt_ctx)
                label = (key[:6] + "..." + key[-4:]) if len(key) > 12 else f"chave-{index}"
                message = (
                    f"Chave {label} do provider {self.name} retornou 429. "
                    "Rotacionando imediatamente para a próxima chave."
                )
                sys.stderr.write(f"\n[AVISO] {message}\n")
                sys.stderr.flush()
                if ctx.on_event is not None:
                    try:
                        ctx.on_event("provider_key_rotation", {
                            "provider": self.name,
                            "from_key": label,
                            "reason": "429",
                            "available_keys": len(keys) - index,
                        })
                    except Exception:
                        pass

            wait = MAX_TRANSIENT_RETRY_DELAY_SECONDS
            message = (
                f"Todas as chaves do provider {self.name} estão indisponíveis por erro 429. "
                f"Aguardando {wait:.0f}s antes de iniciar um novo ciclo de rotação."
            )
            sys.stderr.write(f"\n[AVISO] {message}\n")
            sys.stderr.flush()
            if ctx.on_event is not None:
                try:
                    ctx.on_event("provider_all_keys_429_wait", {
                        "provider": self.name,
                        "retry_after_seconds": wait,
                        "available_keys": 0,
                    })
                except Exception:
                    pass
            time.sleep(wait)

    def _validar_chave(self, ctx: ProviderContext) -> None:
        if self.needs_api_key and not ctx.api_key:
            raise RuntimeError(f"{self.env_key or 'API_KEY'} nao configurada para provider {self.name}")

    def _build_prompt_textual(self, ctx: ProviderContext) -> str:
        """Prompt JSON a partir do pacote textual; especialistas podem sobrescrever."""
        return conteudo_provider_textual(
            prompt=ctx.prompt,
            auditado=ctx.auditado,
            questao_base=ctx.questao_base,
            coluna_evidencia=ctx.coluna_evidencia,
            itens_afirmados=ctx.itens_afirmados,
            pacote=ctx.pacote_textual,
            response_profile=ctx.response_profile,
        )

    def _interpretar_resposta(self, raw: Any, *, response_profile: str = "evidence") -> dict[str, Any]:
        from .response import carregar_json_modelo
        try:
            return validar_resultado_ia(carregar_json_modelo(raw), response_profile=response_profile)
        except (TypeError, ValueError) as exc:
            # A resposta inválida é evidência diagnóstica importante. Retorná-la
            # junto do erro evita que os orquestradores a descartem ao capturar a
            # exceção e permite distinguir desvio estrutural de falha do provider.
            raw_serializavel = raw if isinstance(raw, str) else repr(raw)
            return {
                "status": "error",
                "error": f"resposta do modelo invalida: {exc}",
                "raw_response": raw_serializavel,
                "raw_response_excerpt": raw_serializavel[:2000],
            }

    def _build_content(self, ctx: ProviderContext) -> Any:
        raise NotImplementedError

    def _call(self, ctx: ProviderContext, content: Any) -> Any:
        raise NotImplementedError
