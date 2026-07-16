"""Factory e metadados de providers de IA.

Publica:
- ``REMOTE_PROVIDERS``: conjunto de providers remotos.
- ``get_provider(name, model)``: retorna instancia de GenericProvider.
- ``limite_tokens_provider(provider, model)``: limite aproximado de tokens.
- ``estimar_tokens_payload(...)``: estimativa de tokens do payload.
- ``conteudo_provider_textual(...)``: serializacao textual do payload.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .base import (
    GenericProvider,
    ProviderContext,
    conteudo_provider_textual,
    pacote_textual_sem_documentos_de_arquivos_nativos,
)
from .fake import FakeProvider
from .gemini import GeminiProvider
from .http_utils import arquivos_imagem_do_pacote, arquivos_pdf_do_pacote
from .opencodego import OpencodeGoProvider
from .openai import OpenAIProvider
from .openrouter import OpenRouterProvider


REMOTE_PROVIDERS = {"gemini", "openrouter", "opencodego", "openai"}


_PROVIDER_CLASSES = {
    "fake": FakeProvider,
    "gemini": GeminiProvider,
    "openrouter": OpenRouterProvider,
    "opencodego": OpencodeGoProvider,
    "openai": OpenAIProvider,
}


def get_provider(name: str, model: str) -> GenericProvider:
    cls = _PROVIDER_CLASSES.get(name)
    if cls is None:
        raise ValueError(f"provider nao suportado: {name}")
    return cls(model)


def limite_tokens_provider(provider: str, model: str) -> int:
    """Retorna o limite aproximado de tokens de entrada por provider/model.

    Fontes: documentacao oficial de cada provider (valores conservadores).
    Retorna 0 se desconhecido (nao bloqueia).
    """
    provider = provider.lower()
    model = model.lower()
    if provider == "gemini":
        return 1_048_576
    if provider == "openrouter":
        if "gpt-5.4" in model or "gpt-4" in model:
            return 400_000
        if "minimax" in model:
            return 1_000_000
        return 400_000
    if provider == "openai":
        return 400_000
    if provider == "opencodego":
        return 1_000_000
    return 0


def estimar_tokens_payload(
    *,
    prompt: str,
    auditado: str,
    questao_base: str,
    coluna_evidencia: str,
    itens_afirmados: list[Any],
    pacote: dict[str, Any],
    provider: str = "",
    response_profile: str = "evidence",
) -> dict[str, int]:
    """Estima tokens do payload enviado ao provider.

    Retorna dict com chars_texto, tokens_texto, n_imagens, tokens_imagens,
    n_pdfs, tokens_pdfs e tokens_total.

    - Texto: ~1 token / 3.5 chars.
    - Imagens PNG/JPG: ~258 tokens por imagem (independente do tamanho).
    - PDFs:
        * Gemini: File API (upload separado), estimado por conteudo.
        * OpenRouter / OpenAI: PDF como base64 inline (~1 token / 3.5 chars
          do base64, que e ~1.33x o tamanho do PDF).
        * OpencodeGo: PDFs nao sao enviados; contribuicao zero.
    """
    arquivos_upload = pacote.get("arquivos_upload", []) if isinstance(pacote, dict) else []
    pacote_estimado = {k: v for k, v in pacote.items() if k != "arquivos_upload"}
    if arquivos_upload and provider.lower() == "gemini":
        extensoes_anexadas = {Path(str(a)).suffix.lower() for a in arquivos_upload}
        pacote_estimado = pacote_textual_sem_documentos_de_arquivos_nativos(
            pacote,
            extensoes_anexadas,
        )

    texto = conteudo_provider_textual(
        prompt=prompt,
        auditado=auditado,
        questao_base=questao_base,
        coluna_evidencia=coluna_evidencia,
        itens_afirmados=itens_afirmados,
        pacote=pacote_estimado,
        response_profile=response_profile,
    )
    chars_texto = len(texto)
    tokens_texto = int(chars_texto / 3.5)

    n_imagens = sum(1 for a in arquivos_upload if Path(str(a)).suffix.lower() in {".png", ".jpg", ".jpeg"})
    tokens_imagens = n_imagens * 258

    n_pdfs = sum(1 for a in arquivos_upload if Path(str(a)).suffix.lower() == ".pdf")
    tokens_pdfs = 0
    provider_lower = provider.lower()
    is_gemini = provider_lower == "gemini"
    is_opencodego = provider_lower == "opencodego"
    for a in arquivos_upload:
        if Path(str(a)).suffix.lower() == ".pdf":
            try:
                if is_gemini:
                    size = Path(str(a)).stat().st_size
                    chars_estimados = size // 1024 * 1500
                    tokens_pdfs += int(chars_estimados / 3.5)
                elif is_opencodego:
                    pass
                else:
                    size = Path(str(a)).stat().st_size
                    tokens_pdfs += int((size * 1.33) / 3.5)
            except OSError:
                pass

    return {
        "chars_texto": chars_texto,
        "tokens_texto": tokens_texto,
        "n_imagens": n_imagens,
        "tokens_imagens": tokens_imagens,
        "n_pdfs": n_pdfs,
        "tokens_pdfs": tokens_pdfs,
        "tokens_total": tokens_texto + tokens_imagens + tokens_pdfs,
    }


def executar_provider(
    *,
    provider: str,
    model: str,
    api_key: str,
    prompt: str,
    auditado: str,
    questao_base: str,
    coluna_evidencia: str,
    itens_afirmados: list[Any],
    pacote: dict[str, Any],
    reasoning_effort: str = "",
    on_event: Any = None,
    response_profile: str = "evidence",
) -> dict[str, Any]:
    """Ponto de entrada compativel com a API antiga do ``executar_provider``.

    Decidido pela factory: constroi o provider, monta o contexto e invoca
    ``executar``. Provider fake e providers remotos seguem o mesmo fluxo.
    """
    ctx = ProviderContext(
        provider=provider,
        model=model,
        api_key=api_key,
        prompt=prompt,
        auditado=auditado,
        questao_base=questao_base,
        coluna_evidencia=coluna_evidencia,
        itens_afirmados=itens_afirmados,
        pacote=pacote,
        reasoning_effort=reasoning_effort,
        on_event=on_event,
        response_profile=response_profile,
    )
    try:
        instance = get_provider(provider, model)
    except ValueError as exc:
        return {"status": "error", "error": str(exc)}
    if instance.needs_api_key and not api_key:
        return {
            "status": "error",
            "error": f"{instance.env_key} nao configurada para provider {provider}",
        }
    return instance.executar(ctx)


__all__ = [
    "REMOTE_PROVIDERS",
    "GenericProvider",
    "ProviderContext",
    "get_provider",
    "limite_tokens_provider",
    "estimar_tokens_payload",
    "executar_provider",
    "conteudo_provider_textual",
]
