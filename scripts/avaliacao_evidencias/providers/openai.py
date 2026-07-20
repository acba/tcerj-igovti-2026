"""Provider OpenAI: usa a API Responses em modo streaming, com upload de PDF
como ``input_file`` em base64 e imagens como ``input_image``.

Endpoint e chave configuraveis via ambiente (OPENAI_BASE_URL, OPENAI_API_KEY).
Por padrao aponta para o proxy local ``openai-oauth`` em 127.0.0.1:10531.
"""
from __future__ import annotations

import json
import os
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
    status_from_exception,
)
from .response import json_schema_responses_format


DEFAULT_OPENAI_BASE_URL = "http://127.0.0.1:10531/v1"


class _OpenAIContextWindowExceeded(ValueError):
    """Sinaliza rejeicao de contexto mascarada por um status HTTP transiente."""


def _mensagem_indica_contexto_excedido(message: str) -> bool:
    normalizada = message.casefold()
    return any(
        trecho in normalizada
        for trecho in (
            "exceeds the context window",
            "context window exceeded",
            "maximum context length",
            "context_length_exceeded",
        )
    )


class OpenAIProvider(GenericProvider):
    name = "openai"
    supports_pdf_file_upload = True
    supports_images = True
    needs_api_key = False
    env_key = "OPENAI_API_KEY"
    rotate_comma_separated_keys = True

    def _build_content(self, ctx: ProviderContext) -> list[dict[str, Any]]:
        # PDFs e imagens sao enviados nativamente; remove-los dos documentos
        # do prompt evita duplicacao de informacao e economiza tokens.
        pacote_textual = pacote_textual_sem_documentos_de_arquivos_nativos(
            ctx.pacote,
            {".pdf", ".png", ".jpg", ".jpeg"},
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
        prompt_textual = (
            "Os arquivos PDF e imagens anexados nesta mesma mensagem sao parte integrante da evidencia. "
            "Analise diretamente o conteudo visual e textual desses anexos. "
            "Nao limite a avaliacao ao texto extraido em pacote_evidencia.documentos, pois ele pode estar incompleto em PDFs estruturados como imagem ou organograma.\n\n"
            f"{prompt_textual}"
        )
        content: list[dict[str, Any]] = []
        for path in arquivos_pdf_do_pacote(ctx.pacote):
            content.append(
                {
                    "type": "input_file",
                    "filename": path.name,
                    "file_data": pdf_para_data_url(path),
                    "detail": ctx.pdf_detail,
                }
            )
        for path in arquivos_imagem_do_pacote(ctx.pacote):
            content.append({"type": "input_text", "text": f"Imagem extraida da evidencia: {path.name}"})
            content.append(imagem_para_data_url(path, format_openai=True))
        content.append({"type": "input_text", "text": prompt_textual})
        return content

    def _build_content_pdf_text_fallback(self, ctx: ProviderContext) -> list[dict[str, Any]]:
        """Monta alternativa textual quando o proxy rejeita o PDF inline.

        O pacote preparado pelo pipeline ja contem o texto extraido do PDF.
        Este caminho perde informacao visual e, por isso, so e usado depois de
        uma resposta HTTP 413 ao envio nativo.
        """
        prompt_textual = conteudo_provider_textual(
            prompt=ctx.prompt,
            auditado=ctx.auditado,
            questao_base=ctx.questao_base,
            coluna_evidencia=ctx.coluna_evidencia,
            itens_afirmados=ctx.itens_afirmados,
            pacote=ctx.pacote_textual,
            response_profile=ctx.response_profile,
        )
        aviso = (
            "AVISO DE PROCESSAMENTO: o transporte do PDF nativo excedeu o limite HTTP do proxy. "
            "Avalie o texto extraido localmente presente em pacote_evidencia.documentos. "
            "Considere como lacuna qualquer elemento que dependa exclusivamente de layout, imagem, "
            "assinatura visual, grafico ou outra caracteristica nao preservada na extracao textual.\n\n"
        )
        return [{"type": "input_text", "text": aviso + prompt_textual}]

    def _call(self, ctx: ProviderContext, content: list[dict[str, Any]]) -> Any:
        base_url = os.environ.get("OPENAI_BASE_URL", DEFAULT_OPENAI_BASE_URL).rstrip("/")
        raw_content = ""

        def request_content(request_content: list[dict[str, Any]]) -> str:
            body: dict[str, Any] = {
                "model": self.model,
                "input": [{"role": "user", "content": request_content}],
                "stream": True,
                "text": json_schema_responses_format(response_profile=ctx.response_profile),
            }
            if ctx.reasoning_effort:
                body["reasoning"] = {"effort": ctx.reasoning_effort}

            def call_openai() -> dict[str, Any]:
                try:
                    return _request_openai_responses_stream(
                        url=f"{base_url}/responses",
                        api_key=ctx.api_key,
                        body=body,
                        timeout=120,
                    )
                except urllib.error.HTTPError as exc:
                    # Alguns proxies devolvem excesso da janela de contexto como
                    # 500/502. Converta-o em erro nao transiente para evitar
                    # retries inuteis e permitir o fallback textual do PDF.
                    detalhe = formatar_erro_http(exc)
                    if _mensagem_indica_contexto_excedido(detalhe):
                        raise _OpenAIContextWindowExceeded(detalhe) from exc
                    raise

            payload = executar_com_retry_transiente(
                call_openai,
                exclude_429=True,
                provider=self.name,
                model=self.model,
            )
            return _extrair_texto_openai_responses(payload)

        try:
            raw_content = request_content(content)
            return raw_content
        except (urllib.error.URLError, TimeoutError, KeyError, IndexError, TypeError, json.JSONDecodeError, ValueError) as exc:
            contexto_excedido = isinstance(exc, _OpenAIContextWindowExceeded)
            if (status_from_exception(exc) == 413 or contexto_excedido) and arquivos_pdf_do_pacote(ctx.pacote):
                fallback_reason = "context_window_exceeded" if contexto_excedido else "http_413_payload_too_large"
                if ctx.on_event is not None:
                    try:
                        ctx.on_event(
                            "openai_pdf_text_fallback",
                            {
                                "provider": self.name,
                                "model": self.model,
                                "reason": fallback_reason,
                            },
                        )
                    except Exception:
                        pass
                try:
                    raw_content = request_content(self._build_content_pdf_text_fallback(ctx))
                    return raw_content
                except (
                    urllib.error.URLError,
                    TimeoutError,
                    KeyError,
                    IndexError,
                    TypeError,
                    json.JSONDecodeError,
                    ValueError,
                ) as fallback_exc:
                    exc = fallback_exc
            result = {
                "status": "error",
                "error": f"erro ao chamar OpenAI: {formatar_erro_http(exc)}",
                "http_status": status_from_exception(exc),
            }
            if raw_content:
                result["raw_response_excerpt"] = raw_content[:2000]
            return result


def _request_openai_responses_stream(
    *,
    url: str,
    api_key: str,
    body: dict[str, Any],
    timeout: int,
) -> dict[str, Any]:
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "tcerj-igovti-2026-openai-provider/1.0",
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    request = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    events: list[dict[str, Any]] = []
    text_parts: list[str] = []
    final_response: dict[str, Any] | None = None
    with urllib.request.urlopen(request, timeout=timeout) as response:
        for raw_line in response:
            line = raw_line.decode("utf-8", errors="replace").strip()
            if not line.startswith("data:"):
                continue
            data_line = line.removeprefix("data:").strip()
            if not data_line or data_line == "[DONE]":
                continue
            try:
                event = json.loads(data_line)
            except json.JSONDecodeError:
                events.append({"raw": data_line})
                continue
            events.append(event)
            event_type = event.get("type")
            if event_type == "response.output_text.delta" and isinstance(event.get("delta"), str):
                text_parts.append(event["delta"])
            elif event_type == "response.completed" and isinstance(event.get("response"), dict):
                final_response = event["response"]
            elif isinstance(event.get("delta"), str):
                text_parts.append(event["delta"])
    return {"output_text": "".join(text_parts), "response": final_response, "events": events}


def _extrair_texto_openai_responses(payload: dict[str, Any]) -> str:
    output_text = payload.get("output_text")
    if isinstance(output_text, str) and output_text:
        return output_text
    response = payload.get("response")
    if isinstance(response, dict):
        output_text = response.get("output_text")
        if isinstance(output_text, str) and output_text:
            return output_text
        partes: list[str] = []
        output = response.get("output")
        if isinstance(output, list):
            for item in output:
                if not isinstance(item, dict):
                    continue
                content = item.get("content")
                if not isinstance(content, list):
                    continue
                for part in content:
                    if isinstance(part, dict) and isinstance(part.get("text"), str):
                        partes.append(part["text"])
        if partes:
            return "\n".join(partes)
    return ""
