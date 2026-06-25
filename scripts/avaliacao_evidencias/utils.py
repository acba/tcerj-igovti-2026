"""Utilidades reutilizaveis pelo pipeline e pela consolidacao.

Funcoes de log estruturado, controle de taxa (RPM), hashing, slugs seguros,
manipulacao de ZIP e silenciamento de stderr.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import sys
import time
import unicodedata
import zipfile
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable
from urllib.parse import unquote


def log_event(
    event: str,
    message: str,
    *,
    quiet: bool = False,
    level: str = "info",
    **fields: Any,
) -> None:
    if quiet:
        return
    payload = {
        "ts": dt.datetime.now(dt.timezone.utc).isoformat(),
        "level": level,
        "event": event,
        "message": message,
        **fields,
    }
    print(json.dumps(payload, ensure_ascii=False, default=str), file=sys.stdout, flush=True)


def validar_rpm(valor: str) -> int:
    try:
        rpm = int(valor)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("--rpm deve ser um numero inteiro maior ou igual a zero") from exc
    if rpm < 0:
        raise argparse.ArgumentTypeError("--rpm deve ser maior ou igual a zero")
    return rpm


@dataclass
class RequestsPerMinuteLimiter:
    rpm: int
    clock: Callable[[], float] = time.monotonic
    sleeper: Callable[[float], None] = time.sleep
    last_started_at: float | None = None

    def wait_seconds(self) -> float:
        if self.rpm <= 0 or self.last_started_at is None:
            return 0.0
        elapsed = self.clock() - self.last_started_at
        return max(0.0, (60.0 / self.rpm) - elapsed)

    def wait_and_mark(self, wait_seconds: float | None = None) -> float:
        if wait_seconds is None:
            wait_seconds = self.wait_seconds()
        if wait_seconds > 0:
            self.sleeper(wait_seconds)
        self.last_started_at = self.clock()
        return wait_seconds


def hash_arquivo(caminho: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(caminho).open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def slug_ascii(valor: str, *, fallback: str = "evidencia", max_len: int = 30) -> str:
    normalizado = unicodedata.normalize("NFKD", valor)
    ascii_text = normalizado.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", ascii_text).strip("._-").lower()
    slug = re.sub(r"-{2,}", "-", slug)
    if not slug:
        slug = fallback
    return slug[:max_len].strip("._-") or fallback


def nome_upload_seguro(nome_original: str, sufixo: str) -> str:
    suffix = sufixo.lower()
    stem = Path(nome_original).stem or "evidencia"
    slug = slug_ascii(stem)
    digest = hashlib.sha256(nome_original.encode("utf-8", errors="ignore")).hexdigest()[:10]
    return f"{slug}-{digest}{suffix}"


def caminho_unico(destino: Path, nome: str) -> Path:
    candidato = destino / nome
    if not candidato.exists():
        return candidato
    stem = candidato.stem
    suffix = candidato.suffix
    contador = 2
    while True:
        proximo = destino / f"{stem}-{contador}{suffix}"
        if not proximo.exists():
            return proximo
        contador += 1


def copiar_upload_seguro(origem: Path, destino: Path, nome_original: str | None = None) -> Path:
    destino.mkdir(parents=True, exist_ok=True)
    nome = nome_upload_seguro(nome_original or origem.name, origem.suffix)
    target = caminho_unico(destino, nome)
    shutil.copyfile(origem, target)
    return target


def gravar_upload_texto(destino: Path, nome_original: str, texto: str) -> Path:
    destino.mkdir(parents=True, exist_ok=True)
    nome = nome_upload_seguro(nome_original, ".txt")
    target = caminho_unico(destino, nome)
    target.write_text(texto, encoding="utf-8")
    return target


def componente_nome_arquivo(valor: str) -> str:
    normalizado = unicodedata.normalize("NFKD", str(valor or "")).encode("ascii", "ignore").decode("ascii")
    seguro = re.sub(r"[^A-Za-z0-9._-]+", "_", normalizado).strip("._-")
    return seguro or "nao_informado"


def zip_member_safe(name: str) -> bool:
    path = Path(name)
    return not path.is_absolute() and ".." not in path.parts


def normalizar_nome(valor: str) -> str:
    sem_acentos = unicodedata.normalize("NFKD", valor).encode("ascii", "ignore").decode("ascii")
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in sem_acentos).strip("-")


def normalizar_texto_resposta(valor: Any) -> str:
    if valor is None:
        return ""
    texto = unicodedata.normalize("NFKD", str(valor).strip().casefold())
    texto = "".join(char for char in texto if not unicodedata.combining(char))
    texto = re.sub(r"\s+", " ", texto)
    return texto


def join_value(value: Any) -> str:
    if isinstance(value, list):
        return "; ".join(str(item) for item in value)
    if value is None:
        return ""
    return str(value)


def decode_nome_evidencia(nome: str) -> str:
    return unquote(nome)


@contextmanager
def suprimir_stderr():
    """Silencia warnings de bibliotecas (ex.: pypdf 'Multiple definitions in dictionary')."""
    saved_fd = os.dup(2)
    devnull = os.open(os.devnull, os.O_WRONLY)
    try:
        os.dup2(devnull, 2)
        yield
    finally:
        os.dup2(saved_fd, 2)
        os.close(devnull)
        os.close(saved_fd)


def eh_zip_valido(caminho: Path) -> bool:
    try:
        with zipfile.ZipFile(caminho) as _:
            return True
    except zipfile.BadZipFile:
        return False


def caminho_is_file_safe(caminho: Path) -> bool:
    """``is_file`` que tolera OSError (ex.: nome de arquivo too long).

    Nomes de evidencia decodificados de URL-encoding podem exceder o limite
    de 255 bytes por componente do filesystem (NAME_MAX), gerando
    ``OSError: [Errno 36] File name too long`` em ``pathlib.is_file()``.
    Tratado como "arquivo nao encontrado" para que o fluxo siga para os
    proximos candidatos (LimeSurvey export, fuzzy match). Usada por
    ``consolidation_core.localizar_evidencia`` e
    ``inventory.resolver_evidencia``.
    """
    try:
        return caminho.is_file()
    except OSError:
        return False