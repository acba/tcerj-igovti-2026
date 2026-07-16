"""Provider OpenRouter: chat completions com response_format JSON schema.

Para modelos que suportam PDF nativo (Gemini/GPT/ChatGPT/O-series), anexa o
PDF como ``file`` com ``file_data`` base64 e ativa o plugin ``file-parser``
(engine ``native``). Para os demais, o PDF segue apenas como texto extraido
no pacote. Imagens seguem como ``image_url`` em data URI base64.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any

from .base import (
    GenericProvider,
    ProviderContext,
    conteudo_provider_textual,
    imagem_para_data_url,
    pacote_textual_sem_documentos_de_arquivos_nativos,
    pdf_para_data_url,
)
from .http_utils import (
    arquivos_imagem_do_pacote,
    arquivos_pdf_do_pacote,
    executar_com_retry_transiente,
    formatar_erro_http,
    modelo_openrouter_suporta_pdf_nativo,
    status_from_exception,
)
from .response import json_schema_response_format


class OpenRouterProvider(GenericProvider):
    name = "openrouter"
    supports_inline_pdf = True
    supports_images = True
    needs_api_key = True
    env_key = "OPENROUTER_API_KEY"
    rotate_comma_separated_keys = True

    def _build_content(self, ctx: ProviderContext) -> list[dict[str, Any]]:
        arquivos_pdf = arquivos_pdf_do_pacote(ctx.pacote)
        arquivos_imagem = arquivos_imagem_do_pacote(ctx.pacote)
        usar_pdf_nativo = bool(arquivos_pdf) and modelo_openrouter_suporta_pdf_nativo(self.model)

        # PDFs e imagens sao enviados nativamente; remove-los dos documentos
        # do prompt evita duplicacao de informacao e economiza tokens.
        extensoes_nativas: set[str] = {".png", ".jpg", ".jpeg"}
        if usar_pdf_nativo:
            extensoes_nativas.add(".pdf")
        pacote_textual = pacote_textual_sem_documentos_de_arquivos_nativos(
            ctx.pacote,
            extensoes_nativas,
        )
        prompt_textual = conteudo_provider_textual(
            prompt=ctx.prompt,
            auditado=ctx.auditado,
            questao_base=ctx.questao_base,
            coluna_evidencia=ctx.coluna_evidencia,
            itens_afirmados=ctx.itens_afirmados,
            pacote=pacote_textual,
            response_profile=ctx.response_profile,
        )

        message_content: list[dict[str, Any]] = [{"type": "text", "text": prompt_textual}]
        if usar_pdf_nativo:
            for path in arquivos_pdf:
                message_content.append(
                    {
                        "type": "file",
                        "file": {
                            "filename": path.name,
                            "file_data": pdf_para_data_url(path),
                        },
                    }
                )
        for path in arquivos_imagem:
            message_content.append({"type": "text", "text": f"Imagem extraida da evidencia: {path.name}"})
            message_content.append(imagem_para_data_url(path, format_openai=False))
        return message_content

    def _call(self, ctx: ProviderContext, content: list[dict[str, Any]]) -> Any:
        arquivos_pdf = arquivos_pdf_do_pacote(ctx.pacote)
        usar_pdf_nativo = bool(arquivos_pdf) and modelo_openrouter_suporta_pdf_nativo(self.model)
        body: dict[str, Any] = {
            "model": self.model,
            "messages": [{"role": "user", "content": content}],
            "response_format": json_schema_response_format(response_profile=ctx.response_profile),
        }
        if ctx.reasoning_effort:
            body["reasoning"] = {"effort": ctx.reasoning_effort}
        if usar_pdf_nativo:
            body["plugins"] = [{"id": "file-parser", "pdf": {"engine": "native"}}]

        request = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions",
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {ctx.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            },
            method="POST",
        )
        raw_content = ""
        raw_response = ""
        try:
            def call_openrouter() -> dict[str, Any]:
                with urllib.request.urlopen(request, timeout=120) as response:
                    return json.loads(response.read().decode("utf-8"))

            payload = executar_com_retry_transiente(call_openrouter, exclude_429=True)
            raw_response = json.dumps(payload, ensure_ascii=False)[:2000]
            content_field = payload["choices"][0]["message"]["content"]
            if content_field is None:
                raise ValueError(f"OpenRouter retornou content=null — resposta: {raw_response[:500]}")
            raw_content = content_field
            return raw_content
        except (urllib.error.URLError, TimeoutError, KeyError, IndexError, TypeError, json.JSONDecodeError, ValueError) as exc:
            result = {
                "status": "error",
                "error": f"erro ao chamar OpenRouter: {formatar_erro_http(exc)}",
                "http_status": status_from_exception(exc),
            }
            if raw_content:
                result["raw_response_excerpt"] = raw_content[:2000]
            elif raw_response:
                result["raw_response_excerpt"] = raw_response
            return result
