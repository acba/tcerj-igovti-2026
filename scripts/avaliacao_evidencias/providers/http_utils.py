"""Utilidades HTTP e retry transiente compartilhadas pelos providers remotos."""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.request
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any, Callable


RETRYABLE_PROVIDER_STATUSES = {429, 500, 502, 503, 504}
DEFAULT_TRANSIENT_RETRY_DELAYS = (30.0, 60.0, 120.0)


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


def _header_retry_after(headers: Any) -> str | None:
    if not headers:
        return None
    getter = getattr(headers, "get", None)
    if callable(getter):
        return getter("Retry-After") or getter("retry-after")
    if isinstance(headers, dict):
        return headers.get("Retry-After") or headers.get("retry-after")
    return None


def status_from_exception(exc: BaseException) -> Any:
    status = getattr(exc, "code", None) or getattr(exc, "status", None) or getattr(exc, "status_code", None)
    response = getattr(exc, "response", None)
    if status is None and response is not None:
        status = getattr(response, "status_code", None) or getattr(response, "status", None)
    return status


def retry_after_from_exception(exc: BaseException) -> float | None:
    response = getattr(exc, "response", None)
    retry_after = _header_retry_after(getattr(exc, "headers", None))
    if retry_after is None and response is not None:
        retry_after = _header_retry_after(getattr(response, "headers", None))
    return parse_retry_after(retry_after)


def is_retryable_provider_error(exc: BaseException, *, exclude_429: bool = False) -> bool:
    status = status_from_exception(exc)
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
            if not is_retryable_provider_error(exc, exclude_429=exclude_429) or tentativa >= actual_max:
                raise
            retry_after = retry_after_from_exception(exc)
            delay = retry_after if retry_after is not None else actual_delays[min(tentativa, len(actual_delays) - 1)]
            status_code = status_from_exception(exc)
            sys.stderr.write(
                f"\n[AVISO] Provedor retornou erro temporario {status_code}. "
                f"Aguardando {delay:.1f}s antes da tentativa {tentativa + 1}/{actual_max}...\n"
            )
            sys.stderr.flush()
            sleep(delay)
            tentativa += 1


def formatar_erro_http(exc: BaseException) -> str:
    if isinstance(exc, urllib.error.HTTPError):
        detalhe = ""
        try:
            detalhe = exc.read().decode("utf-8", errors="replace").strip()
        except Exception:
            detalhe = ""
        if detalhe:
            return f"HTTP Error {exc.code}: {exc.reason}; body: {detalhe[:2000]}"
    return str(exc)


def arquivos_pdf_do_pacote(pacote: dict[str, Any]) -> list[Path]:
    arquivos = []
    for valor in pacote.get("arquivos_upload", []) if isinstance(pacote, dict) else []:
        path = Path(str(valor))
        if path.suffix.casefold() == ".pdf" and path.is_file():
            arquivos.append(path)
    return arquivos


def arquivos_imagem_do_pacote(pacote: dict[str, Any]) -> list[Path]:
    arquivos = []
    for valor in pacote.get("arquivos_upload", []) if isinstance(pacote, dict) else []:
        path = Path(str(valor))
        if path.suffix.casefold() in {".png", ".jpg", ".jpeg"} and path.is_file():
            arquivos.append(path)
    return arquivos


def modelo_openrouter_suporta_pdf_nativo(model: str) -> bool:
    normalizado = model.strip().casefold()
    import re
    return (
        normalizado.startswith("google/")
        or "gemini" in normalizado
        or normalizado.startswith("openai/")
        or "chatgpt" in normalizado
        or "/gpt-" in normalizado
        or normalizado.startswith("gpt-")
        or re.search(r"(^|/|:)o[134](?:-|$)", normalizado) is not None
    )