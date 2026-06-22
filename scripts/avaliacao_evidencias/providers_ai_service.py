from __future__ import annotations

import base64
import dataclasses
import datetime as dt
import json
import os
import re
import time
import urllib.error
import urllib.request
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any, Callable, Mapping


ESTADOS_CONFORMIDADE = {"conforme", "nao_conforme", "erro"}
CONCLUSAO_CAMPOS_OBRIGATORIOS = {
    "item_codigo",
    "item_texto",
    "afirmacao_auditado",
    "estado",
    "justificativa",
    "lacunas",
    "arquivos_referenciados",
    "trechos_ou_elementos",
    "paginas_ou_localizacao",
}
RETRYABLE_PROVIDER_STATUSES = {429, 500, 502, 503, 504}
DEFAULT_TRANSIENT_RETRY_DELAYS = (30.0, 60.0, 120.0)
_GEMINI_MAX_TOKENS = 1_048_576
DEFAULT_OPENAI_BASE_URL = "http://127.0.0.1:10531/v1"


def parse_retry_after(value: str | None, *, now: Callable[[], float] = time.time) -> float | None:
    if not value:
        return None
    raw = value.strip()
    if not raw:
        return None
    try:
        return max(0.0, float(raw))
    except ValueError:
        pass
    try:
        retry_at = parsedate_to_datetime(raw)
    except (TypeError, ValueError, IndexError, OverflowError):
        return None
    if retry_at.tzinfo is None:
        retry_at = retry_at.replace(tzinfo=dt.timezone.utc)
    return max(0.0, retry_at.timestamp() - now())


def _item_para_dict(item: Any) -> dict[str, Any]:
    if dataclasses.is_dataclass(item):
        return dataclasses.asdict(item)
    if isinstance(item, Mapping):
        return dict(item)
    if hasattr(item, "__dict__"):
        return dict(item.__dict__)
    raise TypeError(f"item afirmado nao serializavel: {type(item).__name__}")


def _valor_item(item: Any, campo: str) -> Any:
    if isinstance(item, Mapping):
        return item.get(campo)
    return getattr(item, campo)


def executar_julgamento_fake(
    *,
    auditado: str,
    questao_base: str,
    coluna_evidencia: str,
    itens_afirmados: list[Any],
    checklist: str,
    pacote: dict[str, Any],
) -> dict[str, Any]:
    del auditado, questao_base, checklist
    documentos = pacote.get("documentos", []) if isinstance(pacote, dict) else []
    referencias = [
        documento.get("nome")
        for documento in documentos
        if isinstance(documento, dict) and documento.get("nome")
    ]
    conclusoes = []
    for item in itens_afirmados:
        conclusoes.append(
            {
                "item_codigo": _valor_item(item, "codigo"),
                "item_texto": _valor_item(item, "texto"),
                "afirmacao_auditado": _valor_item(item, "afirmacao"),
                "estado": "nao_conforme",
                "justificativa": "Provider fake nao emite conclusao substantiva.",
                "lacunas": ["Analise real de IA nao executada."],
                "arquivos_referenciados": referencias,
                "trechos_ou_elementos": [],
                "paginas_ou_localizacao": [],
                "coluna_evidencia": coluna_evidencia,
            }
        )
    return {"status": "completed", "conclusoes": conclusoes}


def _extrair_bloco_json(texto: str | None) -> str:
    if not isinstance(texto, str) or not texto.strip():
        return ""
    match = re.search(r"```(?:json)?\s*(.*?)```", texto, flags=re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return texto.strip()


def carregar_json_modelo(texto: str | None) -> dict[str, Any]:
    if not isinstance(texto, str) or not texto.strip():
        raise ValueError("resposta do modelo vazia ou nula")
    try:
        from json_repair import repair_json
    except ModuleNotFoundError as exc:
        raise ValueError("json-repair nao instalado para reparar respostas JSON") from exc

    bruto = _extrair_bloco_json(texto)
    reparado = repair_json(bruto)
    if not isinstance(reparado, str) or not reparado.strip():
        raise ValueError("resposta do modelo nao contem JSON reparavel")
    try:
        resultado = json.loads(reparado)
    except json.JSONDecodeError as exc:
        raise ValueError(f"resposta do modelo nao contem JSON reparavel: {exc.msg}") from exc
    if not isinstance(resultado, dict):
        raise ValueError("resposta do modelo precisa ser objeto JSON")
    return resultado


def validar_resultado_ia(resultado: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(resultado, dict):
        raise ValueError("resultado de IA deve ser objeto JSON")
    status = resultado.get("status", "completed")
    if status not in {"completed", "error"}:
        raise ValueError(f"status invalido: {status}")
    if status == "error":
        if not resultado.get("error"):
            raise ValueError("resultado error precisa de campo error")
        return resultado
    conclusoes = resultado.get("conclusoes")
    if not isinstance(conclusoes, list):
        raise ValueError("resultado completed precisa de lista conclusoes")
    for idx, conclusao in enumerate(conclusoes):
        if not isinstance(conclusao, dict):
            raise ValueError(f"conclusao {idx} deve ser objeto")
        faltantes = CONCLUSAO_CAMPOS_OBRIGATORIOS.difference(conclusao)
        if faltantes:
            raise ValueError(f"conclusao {idx} sem campos: {', '.join(sorted(faltantes))}")
        if conclusao["estado"] not in ESTADOS_CONFORMIDADE:
            raise ValueError(f"estado invalido: {conclusao['estado']}")
        for campo in ["lacunas", "arquivos_referenciados", "trechos_ou_elementos", "paginas_ou_localizacao"]:
            if not isinstance(conclusao[campo], list):
                raise ValueError(f"campo {campo} deve ser lista")
    resultado["status"] = status
    return resultado


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
    on_event: Callable[[str, dict[str, Any]], None] | None = None,
) -> dict[str, Any]:
    if provider == "fake":
        return validar_resultado_ia(
            executar_julgamento_fake(
                auditado=auditado,
                questao_base=questao_base,
                coluna_evidencia=coluna_evidencia,
                itens_afirmados=itens_afirmados,
                checklist=prompt,
                pacote=pacote,
            )
        )
    if provider == "openrouter" and not api_key:
        return {"status": "error", "error": "OPENROUTER_API_KEY nao configurada para provider openrouter"}
    if provider == "gemini" and not api_key:
        return {"status": "error", "error": "GEMINI_API_KEY nao configurada para provider gemini"}
    if provider == "opencodego" and not api_key:
        return {"status": "error", "error": "OPENCODEGO_API_KEY nao configurada para provider opencodego"}
    if provider == "openai":
        return executar_julgamento_openai_responses(
            api_key=api_key,
            model=model,
            prompt=prompt,
            auditado=auditado,
            questao_base=questao_base,
            coluna_evidencia=coluna_evidencia,
            itens_afirmados=itens_afirmados,
            pacote=pacote,
            reasoning_effort=reasoning_effort,
        )
    if provider == "openrouter":
        return executar_julgamento_openrouter(
            api_key=api_key,
            model=model,
            prompt=prompt,
            auditado=auditado,
            questao_base=questao_base,
            coluna_evidencia=coluna_evidencia,
            itens_afirmados=itens_afirmados,
            pacote=pacote,
            reasoning_effort=reasoning_effort,
        )
    if provider == "gemini":
        return executar_julgamento_gemini_genai(
            api_key=api_key,
            model=model,
            prompt=prompt,
            auditado=auditado,
            questao_base=questao_base,
            coluna_evidencia=coluna_evidencia,
            itens_afirmados=itens_afirmados,
            pacote=pacote,
            reasoning_effort=reasoning_effort,
            on_event=on_event,
        )
    if provider == "opencodego":
        return executar_julgamento_opencodego(
            api_key=api_key,
            model=model,
            prompt=prompt,
            auditado=auditado,
            questao_base=questao_base,
            coluna_evidencia=coluna_evidencia,
            itens_afirmados=itens_afirmados,
            pacote=pacote,
        )
    return {"status": "error", "error": f"provider nao suportado: {provider}/{model}"}


def _conteudo_provider_textual(
    *,
    prompt: str,
    auditado: str,
    questao_base: str,
    coluna_evidencia: str,
    itens_afirmados: list[Any],
    pacote: dict[str, Any],
) -> str:
    payload = {
        "formato_requerido": "JSON",
        "prompt_de_analise": prompt,
        "auditado": auditado,
        "questao_base": questao_base,
        "coluna_evidencia": coluna_evidencia,
        "itens_afirmados": [_item_para_dict(item) for item in itens_afirmados],
        "pacote_evidencia": pacote,
        "saida_obrigatoria": {
            "status": "completed",
            "conclusoes": [
                {
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
            ],
            "error": "",
        },
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def estimar_tokens_payload(
    *,
    prompt: str,
    auditado: str,
    questao_base: str,
    coluna_evidencia: str,
    itens_afirmados: list[Any],
    pacote: dict[str, Any],
    provider: str = "",
) -> dict[str, int]:
    """Estima tokens do payload enviado ao provider.

    Retorna dict com chars_total, tokens_estimados_texto, tokens_estimados_imagens
    e tokens_total. Para texto usa a aproximacao 1 token ~= 3.5 chars (portugues).
    Para imagens PNG/JPG usa a aproximacao do Gemini: ~258 tokens por imagem
    (independente do tamanho, para imagens processadas pelo modelo).

    Para PDFs:
    - Gemini: usa File API (upload separado), tokens estimados por conteudo
      (~1 token por 3.5 chars do texto extraido, sem overhead de base64)
    - OpenRouter/OpenAI: PDF enviado como base64 inline no payload
      (~1 token por 3.5 chars do base64, que e ~1.33x o tamanho do PDF)
    - OpencodeGo: PDFs NAO sao enviados (so texto e imagens); estimativa
      de PDFs e zero para esse provider.
    """
    arquivos_upload = pacote.get("arquivos_upload", []) if isinstance(pacote, dict) else []
    # Espelhar o runtime: quando ha arquivos para upload, o Gemini suprime
    # os documentos de texto do prompt (o modelo processa os arquivos
    # diretamente via File API). Para outros providers, o texto e mantido.
    pacote_estimado = {k: v for k, v in pacote.items() if k != "arquivos_upload"}
    has_pdfs = any(Path(str(a)).suffix.lower() == ".pdf" for a in arquivos_upload)
    if has_pdfs and provider.lower() == "gemini":
        pacote_estimado = dict(pacote_estimado)
        pacote_estimado["documentos"] = []
    texto = _conteudo_provider_textual(
        prompt=prompt,
        auditado=auditado,
        questao_base=questao_base,
        coluna_evidencia=coluna_evidencia,
        itens_afirmados=itens_afirmados,
        pacote=pacote_estimado,
    )
    chars_texto = len(texto)
    tokens_texto = int(chars_texto / 3.5)

    # Contar imagens nos arquivos_upload
    n_imagens = sum(
        1
        for a in arquivos_upload
        if Path(str(a)).suffix.lower() in {".png", ".jpg", ".jpeg"}
    )
    tokens_imagens = n_imagens * 258

    # Contar PDFs nos arquivos_upload
    n_pdfs = sum(
        1
        for a in arquivos_upload
        if Path(str(a)).suffix.lower() == ".pdf"
    )
    tokens_pdfs = 0
    provider_lower = provider.lower()
    is_gemini = provider_lower == "gemini"
    is_opencodego = provider_lower == "opencodego"
    for a in arquivos_upload:
        if Path(str(a)).suffix.lower() == ".pdf":
            try:
                if is_gemini:
                    # Gemini usa File API: tokens baseados no conteudo do PDF,
                    # nao no base64. Estima extraindo texto (~3.5 chars/token).
                    # Sem --pdf2md, o PDF inteiro e enviado; estima pelo tamanho
                    # do arquivo: ~1500 chars por KB de PDF (media para PDFs com texto)
                    size = Path(str(a)).stat().st_size
                    chars_estimados = size // 1024 * 1500
                    tokens_pdfs += int(chars_estimados / 3.5)
                elif is_opencodego:
                    # OpencodeGo nao envia PDFs como base64 (so texto e imagens).
                    # PDFs em arquivos_upload sao ignorados no runtime, entao nao
                    # contribuem para o total de tokens.
                    pass
                else:
                    # OpenRouter/OpenAI: PDF como base64 inline
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


def _json_schema_response_format() -> dict[str, Any]:
    properties = {
        "item_codigo": {"type": "string"},
        "item_texto": {"type": "string"},
        "afirmacao_auditado": {"type": "string"},
        "estado": {"type": "string", "enum": sorted(ESTADOS_CONFORMIDADE)},
        "justificativa": {"type": "string"},
        "lacunas": {"type": "array", "items": {"type": "string"}},
        "arquivos_referenciados": {"type": "array", "items": {"type": "string"}},
        "trechos_ou_elementos": {"type": "array", "items": {"type": "string"}},
        "paginas_ou_localizacao": {"type": "array", "items": {"type": "string"}},
    }
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "resultado_avaliacao_evidencia",
            "strict": True,
            "schema": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "status": {"type": "string", "enum": ["completed", "error"]},
                    "conclusoes": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "properties": properties,
                            "required": sorted(CONCLUSAO_CAMPOS_OBRIGATORIOS),
                        },
                    },
                    "error": {"type": "string"},
                },
                "required": ["status", "conclusoes", "error"],
            },
        },
    }


def _json_schema_responses_format() -> dict[str, Any]:
    chat_format = _json_schema_response_format()["json_schema"]
    return {
        "format": {
            "type": "json_schema",
            "name": chat_format["name"],
            "strict": chat_format["strict"],
            "schema": chat_format["schema"],
        }
    }


def _header_retry_after(headers: Any) -> str | None:
    if not headers:
        return None
    getter = getattr(headers, "get", None)
    if callable(getter):
        return getter("Retry-After") or getter("retry-after")
    if isinstance(headers, dict):
        return headers.get("Retry-After") or headers.get("retry-after")
    return None


def _status_from_exception(exc: BaseException) -> Any:
    status = getattr(exc, "code", None) or getattr(exc, "status", None) or getattr(exc, "status_code", None)
    response = getattr(exc, "response", None)
    if status is None and response is not None:
        status = getattr(response, "status_code", None) or getattr(response, "status", None)
    return status


def _retry_after_from_exception(exc: BaseException) -> float | None:
    response = getattr(exc, "response", None)
    retry_after = _header_retry_after(getattr(exc, "headers", None))
    if retry_after is None and response is not None:
        retry_after = _header_retry_after(getattr(response, "headers", None))
    return parse_retry_after(retry_after)


def _is_retryable_provider_error(exc: BaseException, *, exclude_429: bool = False) -> bool:
    status = _status_from_exception(exc)
    if exclude_429 and status == 429:
        return False
    return status in RETRYABLE_PROVIDER_STATUSES


def executar_com_retry_transiente(
    func: Callable[[], Any],
    *,
    max_retries: int = 3,
    fallback_delays: tuple[float, ...] = DEFAULT_TRANSIENT_RETRY_DELAYS,
    sleeper: Callable[[float], None] | None = None,
    exclude_429: bool = False,
) -> Any:
    import os
    import sys

    # Obter configuracoes por variaveis de ambiente
    env_max = os.environ.get("AI_MAX_RETRIES")
    if env_max is not None:
        try:
            actual_max = int(env_max)
        except ValueError:
            actual_max = max_retries
    else:
        actual_max = max_retries

    env_delays = os.environ.get("AI_RETRY_DELAYS")
    if env_delays is not None:
        try:
            actual_delays = tuple(float(d.strip()) for d in env_delays.split(","))
        except ValueError:
            actual_delays = fallback_delays
    else:
        actual_delays = fallback_delays

    sleep = sleeper or time.sleep
    tentativa = 0
    while True:
        try:
            return func()
        except Exception as exc:
            if not _is_retryable_provider_error(exc, exclude_429=exclude_429) or tentativa >= actual_max:
                raise
            retry_after = _retry_after_from_exception(exc)
            delay = retry_after if retry_after is not None else actual_delays[min(tentativa, len(actual_delays) - 1)]

            status_code = _status_from_exception(exc)
            sys.stderr.write(
                f"\n[AVISO] Provedor retornou erro temporario {status_code}. "
                f"Aguardando {delay:.1f}s antes da tentativa {tentativa + 1}/{actual_max}...\n"
            )
            sys.stderr.flush()

            sleep(delay)
            tentativa += 1


def executar_julgamento_opencodego(
    *,
    api_key: str,
    model: str,
    prompt: str,
    auditado: str,
    questao_base: str,
    coluna_evidencia: str,
    itens_afirmados: list[Any],
    pacote: dict[str, Any],
) -> dict[str, Any]:
    pacote_textual = {k: v for k, v in pacote.items() if k != "arquivos_upload"}
    prompt_textual = _conteudo_provider_textual(
        prompt=prompt,
        auditado=auditado,
        questao_base=questao_base,
        coluna_evidencia=coluna_evidencia,
        itens_afirmados=itens_afirmados,
        pacote=pacote_textual,
    )
    arquivos_imagem = _arquivos_imagem_openrouter(pacote)
    message_content: str | list[dict[str, Any]]
    if arquivos_imagem:
        message_content = [{"type": "text", "text": prompt_textual}]
        for path in arquivos_imagem:
            message_content.append({"type": "text", "text": f"Imagem extraida da evidencia: {path.name}"})
            message_content.append(_imagem_para_openrouter(path))
    else:
        message_content = prompt_textual
    body = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": message_content,
            }
        ],
        "response_format": _json_schema_response_format(),
    }
    request = urllib.request.Request(
        "https://opencode.ai/zen/go/v1/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        },
        method="POST",
    )
    content = ""
    try:
        def call_opencodego() -> dict[str, Any]:
            with urllib.request.urlopen(request, timeout=120) as response:
                return json.loads(response.read().decode("utf-8"))

        payload = executar_com_retry_transiente(call_opencodego)
        content = payload["choices"][0]["message"]["content"]
        return validar_resultado_ia(carregar_json_modelo(content))
    except (urllib.error.URLError, TimeoutError, KeyError, IndexError, TypeError, json.JSONDecodeError, ValueError) as exc:
        result = {"status": "error", "error": f"erro ao chamar OpencodeGo: {exc}"}
        if content:
            result["raw_response_excerpt"] = content[:2000]
        return result


def executar_julgamento_openrouter(
    *,
    api_key: str,
    model: str,
    prompt: str,
    auditado: str,
    questao_base: str,
    coluna_evidencia: str,
    itens_afirmados: list[Any],
    pacote: dict[str, Any],
    reasoning_effort: str = "",
) -> dict[str, Any]:
    pacote_textual = {k: v for k, v in pacote.items() if k != "arquivos_upload"}
    prompt_textual = _conteudo_provider_textual(
        prompt=prompt,
        auditado=auditado,
        questao_base=questao_base,
        coluna_evidencia=coluna_evidencia,
        itens_afirmados=itens_afirmados,
        pacote=pacote_textual,
    )
    arquivos_pdf = _arquivos_pdf_openrouter(pacote)
    arquivos_imagem = _arquivos_imagem_openrouter(pacote)
    usar_pdf_nativo = bool(arquivos_pdf) and _modelo_openrouter_suporta_pdf_nativo(model)
    message_content: str | list[dict[str, Any]]
    if usar_pdf_nativo or arquivos_imagem:
        message_content = [{"type": "text", "text": prompt_textual}]
        if usar_pdf_nativo:
            message_content.extend(_arquivo_pdf_para_openrouter(path) for path in arquivos_pdf)
        for path in arquivos_imagem:
            message_content.append({"type": "text", "text": f"Imagem extraida da evidencia: {path.name}"})
            message_content.append(_imagem_para_openrouter(path))
    else:
        message_content = prompt_textual
    body = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": message_content,
            }
        ],
        "response_format": _json_schema_response_format(),
    }
    if reasoning_effort:
        body["reasoning"] = {"effort": reasoning_effort}
    if usar_pdf_nativo:
        body["plugins"] = [{"id": "file-parser", "pdf": {"engine": "native"}}]
    request = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        },
        method="POST",
    )
    raw_content = ""
    raw_response = ""
    try:
        def call_openrouter() -> dict[str, Any]:
            with urllib.request.urlopen(request, timeout=120) as response:
                return json.loads(response.read().decode("utf-8"))

        payload = executar_com_retry_transiente(call_openrouter)
        raw_response = json.dumps(payload, ensure_ascii=False)[:2000]
        content_field = payload["choices"][0]["message"]["content"]
        if content_field is None:
            raise ValueError(f"OpenRouter retornou content=null — resposta: {raw_response[:500]}")
        raw_content = content_field
        return validar_resultado_ia(carregar_json_modelo(raw_content))
    except (urllib.error.URLError, TimeoutError, KeyError, IndexError, TypeError, json.JSONDecodeError, ValueError) as exc:
        result = {"status": "error", "error": f"erro ao chamar OpenRouter: {_formatar_erro_http(exc)}"}
        if raw_content:
            result["raw_response_excerpt"] = raw_content[:2000]
        elif raw_response:
            result["raw_response_excerpt"] = raw_response
        return result


def executar_julgamento_openai_responses(
    *,
    api_key: str,
    model: str,
    prompt: str,
    auditado: str,
    questao_base: str,
    coluna_evidencia: str,
    itens_afirmados: list[Any],
    pacote: dict[str, Any],
    reasoning_effort: str = "",
) -> dict[str, Any]:
    pacote_textual = {k: v for k, v in pacote.items() if k != "arquivos_upload"}
    prompt_textual = _conteudo_provider_textual(
        prompt=prompt,
        auditado=auditado,
        questao_base=questao_base,
        coluna_evidencia=coluna_evidencia,
        itens_afirmados=itens_afirmados,
        pacote=pacote_textual,
    )
    prompt_textual = (
        "Os arquivos PDF e imagens anexados nesta mesma mensagem sao parte integrante da evidencia. "
        "Analise diretamente o conteudo visual e textual desses anexos. "
        "Nao limite a avaliacao ao texto extraido em pacote_evidencia.documentos, pois ele pode estar incompleto em PDFs estruturados como imagem ou organograma.\n\n"
        f"{prompt_textual}"
    )
    content: list[dict[str, Any]] = []
    for path in _arquivos_pdf_openrouter(pacote):
        content.append(_arquivo_pdf_para_openai_responses(path))
    for path in _arquivos_imagem_openrouter(pacote):
        content.append({"type": "input_text", "text": f"Imagem extraida da evidencia: {path.name}"})
        content.append(_imagem_para_openai_responses(path))
    content.append({"type": "input_text", "text": prompt_textual})

    body: dict[str, Any] = {
        "model": model,
        "input": [
            {
                "role": "user",
                "content": content,
            }
        ],
        "stream": True,
        "text": _json_schema_responses_format(),
    }
    if reasoning_effort:
        body["reasoning"] = {"effort": reasoning_effort}

    base_url = os.environ.get("OPENAI_BASE_URL", DEFAULT_OPENAI_BASE_URL).rstrip("/")
    raw_content = ""
    try:
        def call_openai() -> dict[str, Any]:
            return _request_openai_responses_stream(
                url=f"{base_url}/responses",
                api_key=api_key,
                body=body,
                timeout=120,
            )

        payload = executar_com_retry_transiente(call_openai)
        raw_content = _extrair_texto_openai_responses(payload)
        return validar_resultado_ia(carregar_json_modelo(raw_content))
    except (urllib.error.URLError, TimeoutError, KeyError, IndexError, TypeError, json.JSONDecodeError, ValueError) as exc:
        result = {"status": "error", "error": f"erro ao chamar OpenAI: {_formatar_erro_http(exc)}"}
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
    return {
        "output_text": "".join(text_parts),
        "response": final_response,
        "events": events,
    }


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


def _formatar_erro_http(exc: BaseException) -> str:
    if isinstance(exc, urllib.error.HTTPError):
        detalhe = ""
        try:
            detalhe = exc.read().decode("utf-8", errors="replace").strip()
        except Exception:
            detalhe = ""
        if detalhe:
            return f"HTTP Error {exc.code}: {exc.reason}; body: {detalhe[:2000]}"
    return str(exc)


def _modelo_openrouter_suporta_pdf_nativo(model: str) -> bool:
    normalizado = model.strip().casefold()
    return (
        normalizado.startswith("google/")
        or "gemini" in normalizado
        or normalizado.startswith("openai/")
        or "chatgpt" in normalizado
        or "/gpt-" in normalizado
        or normalizado.startswith("gpt-")
        or re.search(r"(^|/|:)o[134](?:-|$)", normalizado) is not None
    )


def _arquivos_pdf_openrouter(pacote: dict[str, Any]) -> list[Path]:
    arquivos = []
    for valor in pacote.get("arquivos_upload", []) if isinstance(pacote, dict) else []:
        path = Path(str(valor))
        if path.suffix.casefold() == ".pdf" and path.is_file():
            arquivos.append(path)
    return arquivos


def _arquivos_imagem_openrouter(pacote: dict[str, Any]) -> list[Path]:
    arquivos = []
    for valor in pacote.get("arquivos_upload", []) if isinstance(pacote, dict) else []:
        path = Path(str(valor))
        if path.suffix.casefold() in {".png", ".jpg", ".jpeg"} and path.is_file():
            arquivos.append(path)
    return arquivos


def _arquivo_pdf_para_openrouter(path: Path) -> dict[str, Any]:
    data_url = "data:application/pdf;base64," + base64.b64encode(path.read_bytes()).decode("ascii")
    return {
        "type": "file",
        "file": {
            "filename": path.name,
            "file_data": data_url,
        },
    }


def _arquivo_pdf_para_openai_responses(path: Path) -> dict[str, Any]:
    data_url = "data:application/pdf;base64," + base64.b64encode(path.read_bytes()).decode("ascii")
    return {
        "type": "input_file",
        "filename": path.name,
        "file_data": data_url,
    }


def _imagem_para_openrouter(path: Path) -> dict[str, Any]:
    suffix = path.suffix.casefold()
    mime = "image/png" if suffix == ".png" else "image/jpeg"
    data_url = f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")
    return {
        "type": "image_url",
        "image_url": {
            "url": data_url,
        },
    }


def _imagem_para_openai_responses(path: Path) -> dict[str, Any]:
    suffix = path.suffix.casefold()
    mime = "image/png" if suffix == ".png" else "image/jpeg"
    data_url = f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")
    return {
        "type": "input_image",
        "image_url": data_url,
    }


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
        """Retorna (chave_disponivel_agora, wait_seconds).

        Se uma chave esta disponivel, retorna (key, 0.0).
        Se todas exauridas, retorna (None, menor_wait_entre_todas).
        """
        now = time.monotonic()
        for key in self.keys:
            until = self.exhausted_until.get(key, 0.0)
            if now >= until:
                return key, 0.0
        # Todas exauridas - menor tempo de espera
        waits = [self.exhausted_until[k] - now for k in self.keys if k in self.exhausted_until]
        min_wait = min(waits) if waits else 60.0
        return None, max(0.0, min_wait)

    def mark_exhausted(self, key: str, retry_after_seconds: float) -> None:
        """Marca uma chave como exaurida por retry_after_seconds."""
        self.exhausted_until[key] = time.monotonic() + max(5.0, retry_after_seconds)
        self.consecutive_429[key] = self.consecutive_429.get(key, 0) + 1

    def reset_key(self, key: str) -> None:
        """Limpa o estado de exaustao de uma chave (apos sucesso)."""
        self.exhausted_until.pop(key, None)
        self.consecutive_429[key] = 0

    def should_abandon_key(self, key: str, *, threshold: int = 5) -> bool:
        """True se uma chave recebeu 429 demais vezes consecutivas."""
        return self.consecutive_429.get(key, 0) >= threshold

    def all_exhausted(self) -> bool:
        now = time.monotonic()
        return all(now < self.exhausted_until.get(k, 0.0) for k in self.keys) if self.keys else True

    def available_count(self) -> int:
        now = time.monotonic()
        return sum(1 for k in self.keys if now >= self.exhausted_until.get(k, 0.0))


def _extract_retry_delay_from_gemini_error(exc: BaseException) -> float:
    """Extrai retryDelay (segundos) de uma APIError do Gemini.

    O erro 429 do Gemini contem details com @type RetryInfo e retryDelay "48s".
    Fall back para Retry-After header ou 60s default.
    """
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
    retry_after = _retry_after_from_exception(exc)
    if retry_after is not None:
        return retry_after
    return 60.0


def _is_gemini_429(exc: BaseException) -> bool:
    """Verifica se a excecao e um 429 RESOURCE_EXHAUSTED do Gemini."""
    code = getattr(exc, "code", None)
    if code is None:
        response = getattr(exc, "response", None)
        if response is not None:
            code = getattr(response, "status_code", None)
    status = getattr(exc, "status", None) or ""
    return code == 429 or "RESOURCE_EXHAUSTED" in str(status).upper()


def executar_julgamento_gemini_genai(
    *,
    api_key: str,
    model: str,
    prompt: str,
    auditado: str,
    questao_base: str,
    coluna_evidencia: str,
    itens_afirmados: list[Any],
    pacote: dict[str, Any],
    reasoning_effort: str = "",
    on_event: Callable[[str, dict[str, Any]], None] | None = None,
) -> dict[str, Any]:
    def emit(event: str, **fields: Any) -> None:
        if on_event is not None:
            try:
                on_event(event, {**fields})
            except Exception:
                pass

    try:
        from google import genai
        from google.genai import types
    except Exception as exc:
        return {"status": "error", "error": f"google-genai nao disponivel: {exc}"}
    keys = [k.strip() for k in api_key.split(",") if k.strip()]
    if not keys:
        return {"status": "error", "error": "GEMINI_API_KEY nao contem chaves validas"}

    manager = GeminiKeyRotationManager(keys)
    clients: dict[str, Any] = {}
    abandoned: set[str] = set()
    key_rotations: list[dict[str, Any]] = []

    def get_client(key: str) -> Any:
        if key not in clients:
            clients[key] = genai.Client(api_key=key)
        return clients[key]

    def key_label(key: str) -> str:
        return key[:6] + "…" + key[-4:]

    # Quando ha arquivos para upload (PDFs/imagens via File API), suprimir os
    # documentos de texto do pacote no prompt — o modelo processa os arquivos
    # diretamente via File API, e o texto extraido seria duplicacao redundante.
    arquivos_upload = pacote.get("arquivos_upload", []) if isinstance(pacote, dict) else []
    pacote_prompt = {k: v for k, v in pacote.items() if k != "arquivos_upload"}
    if arquivos_upload:
        pacote_prompt = dict(pacote_prompt)
        pacote_prompt["documentos"] = []
        pacote_prompt["_observacao"] = (
            "O conteudo da evidencia foi enviado como arquivo anexado via File API. "
            "Analise diretamente o conteudo dos arquivos anexados."
        )

    contents_base = [
        _conteudo_provider_textual(
            prompt=prompt,
            auditado=auditado,
            questao_base=questao_base,
            coluna_evidencia=coluna_evidencia,
            itens_afirmados=itens_afirmados,
            pacote=pacote_prompt,
        )
    ]
    config = types.GenerateContentConfig(response_mime_type="application/json")
    if reasoning_effort:
        config.thinking_config = types.ThinkingConfig(thinking_level=reasoning_effort)

    max_pausas = 10
    pausas_consecutivas = 0

    while True:
        # Filtrar chaves nao abandonadas
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
            # Todas as chaves exauridas - pausar
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
        pausas_consecutivas = 0  # reset: temos uma chave disponivel

        # Upload dos arquivos (a cada tentativa, pois podem expirar)
        uploaded = []
        upload_ok = True
        for arquivo in pacote.get("arquivos_upload", []):
            try:
                uploaded.append(
                    executar_com_retry_transiente(
                        lambda arquivo=arquivo: client.files.upload(file=arquivo),
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
                    emit("gemini_key_rotation", **rotation)
                    if manager.should_abandon_key(key):
                        abandoned.add(key)
                        emit(
                            "gemini_key_abandoned",
                            key=key_label(key),
                            reason="consecutive_429_exceeded",
                        )
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

        # Contar tokens exatos via API do Gemini antes de chamar generate_content
        try:
            count_resp = client.models.count_tokens(model=model, contents=contents)
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
            pass  # Se count_tokens falhar, seguir para generate_content

        # generate_content: 429 propaga imediatamente para rotacao (sem retry legacy)
        try:
            response = executar_com_retry_transiente(
                lambda: client.models.generate_content(
                    model=model,
                    contents=contents,
                    config=config,
                ),
                exclude_429=True,
            )
            raw_text = response.text
            manager.reset_key(key)
            result = validar_resultado_ia(carregar_json_modelo(raw_text))
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
                emit("gemini_key_rotation", **rotation)
                if manager.should_abandon_key(key):
                    abandoned.add(key)
                    emit(
                        "gemini_key_abandoned",
                        key=key_label(key),
                        reason="consecutive_429_exceeded",
                    )
                continue  # rota para proxima chave imediatamente
            # Erro nao-429: retornar
            result = {"status": "error", "error": f"erro ao chamar Gemini: {exc}"}
            if key_rotations:
                result["key_rotations"] = key_rotations
            return result


def executar_julgamento_gemini(
    *,
    api_key: str,
    model: str,
    auditado: str,
    questao_base: str,
    coluna_evidencia: str,
    itens_afirmados: list[Any],
    checklist: str,
    pacote: dict[str, Any],
) -> dict[str, Any]:
    prompt = {
        "auditado": auditado,
        "questao_base": questao_base,
        "coluna_evidencia": coluna_evidencia,
        "itens_afirmados": [_item_para_dict(item) for item in itens_afirmados],
        "checklist": checklist,
        "pacote_evidencia": pacote,
        "instrucoes": [
            "Avalie somente os criterios do checklist.",
            "Nao use conhecimento externo para suprir lacunas.",
            "Retorne somente JSON com status e conclusoes.",
            "Use estados: conforme, nao_conforme, inconclusivo, erro.",
        ],
    }
    body = {
        "contents": [
            {
                "parts": [
                    {
                        "text": json.dumps(prompt, ensure_ascii=False),
                    }
                ]
            }
        ],
        "generationConfig": {"responseMimeType": "application/json"},
    }
    import random
    keys = [k.strip() for k in api_key.split(",") if k.strip()]
    chosen_key = random.choice(keys) if keys else api_key
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={chosen_key}"
    request = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        def call_gemini() -> dict[str, Any]:
            with urllib.request.urlopen(request, timeout=120) as response:
                return json.loads(response.read().decode("utf-8"))

        payload = executar_com_retry_transiente(call_gemini)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return {"status": "error", "error": f"erro ao chamar Gemini: {exc}"}
    text = ""
    try:
        text = payload["candidates"][0]["content"]["parts"][0]["text"]
        result = carregar_json_modelo(text)
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        response = {"status": "error", "error": f"resposta Gemini invalida: {exc}", "raw": payload}
        if text:
            response["raw_response_excerpt"] = text[:2000]
        return response
    if result.get("status") not in {"completed", "error"}:
        result["status"] = "completed"
    return result
