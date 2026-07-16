"""Provider OpencodeGo: chat completions OpenAI-compatible, texto + imagens.

Nao envia PDFs: o conteudo textual do PDF ja vem extraido pelo pipeline
(``normalizar_evidencia``) dentro de ``pacote_evidencia.documentos``. Imagens
extraidas por ``--pdf2md``/``--docx2html`` sao anexadas como ``image_url``.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from .base import GenericProvider, ProviderContext, conteudo_provider_textual, imagem_para_data_url
from .http_utils import arquivos_imagem_do_pacote, executar_com_retry_transiente, status_from_exception
from .response import json_schema_response_format


class OpencodeGoProvider(GenericProvider):
    name = "opencodego"
    supports_images = True
    needs_api_key = True
    env_key = "OPENCODEGO_API_KEY"
    rotate_comma_separated_keys = True

    def _build_content(self, ctx: ProviderContext) -> str | list[dict[str, Any]]:
        pacote_textual = ctx.pacote_textual
        prompt_textual = conteudo_provider_textual(
            prompt=ctx.prompt,
            auditado=ctx.auditado,
            questao_base=ctx.questao_base,
            coluna_evidencia=ctx.coluna_evidencia,
            itens_afirmados=ctx.itens_afirmados,
            pacote=pacote_textual,
            response_profile=ctx.response_profile,
        )
        arquivos_imagem = arquivos_imagem_do_pacote(ctx.pacote)
        if not arquivos_imagem:
            return prompt_textual
        message_content: list[dict[str, Any]] = [{"type": "text", "text": prompt_textual}]
        for path in arquivos_imagem:
            message_content.append({"type": "text", "text": f"Imagem extraida da evidencia: {path.name}"})
            message_content.append(imagem_para_data_url(path, format_openai=False))
        return message_content

    def _call(self, ctx: ProviderContext, content: str | list[dict[str, Any]]) -> Any:
        body = {
            "model": self.model,
            "messages": [{"role": "user", "content": content}],
            "response_format": json_schema_response_format(response_profile=ctx.response_profile),
        }
        request = urllib.request.Request(
            "https://opencode.ai/zen/go/v1/chat/completions",
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {ctx.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            },
            method="POST",
        )
        raw_content = ""
        try:
            def call_opencodego() -> dict[str, Any]:
                with urllib.request.urlopen(request, timeout=120) as response:
                    return json.loads(response.read().decode("utf-8"))

            payload = executar_com_retry_transiente(call_opencodego, exclude_429=True)
            raw_content = payload["choices"][0]["message"]["content"]
            return raw_content
        except (urllib.error.URLError, TimeoutError, KeyError, IndexError, TypeError, json.JSONDecodeError, ValueError) as exc:
            result = {
                "status": "error",
                "error": f"erro ao chamar OpencodeGo: {exc}",
                "http_status": status_from_exception(exc),
            }
            if raw_content:
                result["raw_response_excerpt"] = raw_content[:2000]
            return result
