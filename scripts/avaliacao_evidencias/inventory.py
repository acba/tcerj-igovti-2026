"""Inventario de analises candidatas e resolucao de arquivos de evidencia.

Le a planilha de respostas, identifica colunas de evidencia e localiza os
arquivos fisicos correspondentes. A leitura da planilha e feita uma unica vez
e exposta tambem como ``rows_by_id`` (dict por id), evitando a releitura O(n^2)
que existia no pipeline original.
"""
from __future__ import annotations

import difflib
import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import unquote

from openpyxl import load_workbook

from .questionnaire import base_coluna_evidencia
from .utils import caminho_is_file_safe, decode_nome_evidencia, normalizar_nome


@dataclass(frozen=True)
class AnaliseCandidata:
    auditado: str
    coluna_evidencia: str
    nome_original_evidencia: str
    upload: dict[str, Any]
    resposta_id: Any = None
    evidence_index: int | None = None
    erro: str = ""
    evidencia_ausente: bool = False


@dataclass(frozen=True)
class ResolucaoEvidencia:
    caminho: Path | None
    nome_decodificado: str
    erro: str = ""


def coluna_evidencia(nome: str) -> bool:
    return "evi" in nome and not nome.endswith("[filecount]")


def _parse_upload(valor: Any) -> tuple[dict[str, Any] | None, str]:
    if valor in (None, ""):
        return None, ""
    if isinstance(valor, str):
        try:
            parsed = json.loads(valor)
        except json.JSONDecodeError as exc:
            return None, f"metadados de upload invalidos: {exc.msg}"
    else:
        parsed = valor
    if not isinstance(parsed, list):
        return None, "metadados de upload devem ser uma lista"
    if len(parsed) != 1:
        return None, "coluna de evidencia deve conter exatamente um arquivo"
    upload = parsed[0]
    if not isinstance(upload, dict):
        return None, "metadado de upload deve ser um objeto"
    name = upload.get("name")
    if not isinstance(name, str) or not name:
        return None, "metadado de upload sem atributo name"
    return upload, ""


def rows_from_xlsx(caminho_xlsx: str | Path) -> Iterable[dict[str, Any]]:
    workbook = load_workbook(caminho_xlsx, read_only=True, data_only=True)
    try:
        sheet = workbook.active
        rows = sheet.iter_rows(values_only=True)
        headers = [str(value) if value is not None else "" for value in next(rows)]
        for values in rows:
            yield dict(zip(headers, values))
    finally:
        workbook.close()


def rows_by_id(caminho_xlsx: str | Path) -> dict[Any, dict[str, Any]]:
    """Indexa as linhas da planilha por ``id`` em um dict.

    Substitui a releitura O(n) da planilha a cada analise que existia no
    pipeline original (funcao ``_linha_por_id``). Construido uma unica vez
    e reutilizado para todas as analises.
    """
    indice: dict[Any, dict[str, Any]] = {}
    for linha in rows_from_xlsx(Path(caminho_xlsx)):
        indice[linha.get("id")] = linha
    return indice


def inventariar_analises(
    caminho_xlsx: str | Path,
    raiz_evidencias: str | Path,
    caminho_questionario: str | Path,
    *,
    include_unsubmitted: bool = False,
    colunas_evidencia_permitidas: set[str] | None = None,
    include_missing_evidence: bool = False,
) -> list[AnaliseCandidata]:
    del raiz_evidencias, caminho_questionario
    linhas = list(rows_from_xlsx(Path(caminho_xlsx)))
    if not linhas:
        return []
    colunas = list(linhas[0].keys())
    colunas_evidencia = [
        (evidence_index, col)
        for evidence_index, col in enumerate((col for col in colunas if coluna_evidencia(col)), start=1)
        if colunas_evidencia_permitidas is None or col in colunas_evidencia_permitidas
    ]
    analises: list[AnaliseCandidata] = []
    for linha in linhas:
        if not include_unsubmitted and not linha.get("submitdate"):
            continue
        auditado = str(linha.get("firstname") or "").strip()
        for evidence_index, coluna in colunas_evidencia:
            upload, erro = _parse_upload(linha.get(coluna))
            if upload is None and not erro:
                if include_missing_evidence:
                    analises.append(
                        AnaliseCandidata(
                            auditado=auditado,
                            coluna_evidencia=coluna,
                            nome_original_evidencia="",
                            upload={},
                            resposta_id=linha.get("id"),
                            evidence_index=evidence_index,
                            evidencia_ausente=True,
                        )
                    )
                continue
            analises.append(
                AnaliseCandidata(
                    auditado=auditado,
                    coluna_evidencia=coluna,
                    nome_original_evidencia=upload.get("name", "") if upload else "",
                    upload=upload or {},
                    resposta_id=linha.get("id"),
                    evidence_index=evidence_index,
                    erro=erro,
                )
            )
    return analises


def resolver_evidencia(
    auditado: str,
    raiz_evidencias: str | Path,
    upload: dict[str, Any],
    *,
    resposta_id: Any = None,
    evidence_index: int | None = None,
) -> ResolucaoEvidencia:
    nome_original = upload.get("name")
    if not isinstance(nome_original, str) or not nome_original:
        return ResolucaoEvidencia(caminho=None, nome_decodificado="", erro="metadado de upload sem atributo name")
    nome_decodificado = decode_nome_evidencia(nome_original)
    auditado_dir = Path(raiz_evidencias) / auditado
    caminho = auditado_dir / nome_decodificado
    if not caminho_is_file_safe(caminho):
        exportado = _resolver_evidencia_exportada_limesurvey(
            auditado_dir,
            nome_decodificado,
            resposta_id=resposta_id,
            evidence_index=evidence_index,
        )
        if exportado:
            return ResolucaoEvidencia(caminho=exportado.resolve(), nome_decodificado=nome_decodificado)
        return ResolucaoEvidencia(
            caminho=None,
            nome_decodificado=nome_decodificado,
            erro=f"arquivo de evidencia nao encontrado: {caminho}",
        )
    return ResolucaoEvidencia(caminho=caminho.resolve(), nome_decodificado=nome_decodificado)


def _resolver_evidencia_exportada_limesurvey(
    auditado_dir: Path,
    nome_decodificado: str,
    *,
    resposta_id: Any = None,
    evidence_index: int | None = None,
) -> Path | None:
    if not auditado_dir.is_dir():
        return None
    try:
        candidatos = [path for path in auditado_dir.iterdir() if caminho_is_file_safe(path)]
    except OSError:
        return None
    if not candidatos:
        return None
    if resposta_id is not None and evidence_index is not None:
        prefixo = _prefixo_exportacao_limesurvey(resposta_id, evidence_index)
        if prefixo:
            candidatos_prefixo = [path for path in candidatos if path.name.startswith(prefixo)]
            match = _melhor_match_nome_exportado(nome_decodificado, candidatos_prefixo)
            if match:
                return match
    return _melhor_match_nome_exportado(nome_decodificado, candidatos)


def _prefixo_exportacao_limesurvey(resposta_id: Any, evidence_index: int) -> str:
    try:
        return f"{int(resposta_id):05d}_{int(evidence_index):02d}_"
    except (TypeError, ValueError):
        return ""


def _melhor_match_nome_exportado(nome_decodificado: str, candidatos: list[Path]) -> Path | None:
    nome_key, suffix = _nome_exportado_key(nome_decodificado)
    matches: list[tuple[float, str, Path]] = []
    for candidato in candidatos:
        candidato_sem_prefixo = _remover_prefixo_exportacao_limesurvey(candidato.name)
        candidato_key, candidato_suffix = _nome_exportado_key(candidato_sem_prefixo)
        if candidato_suffix != suffix:
            continue
        if candidato_key == nome_key:
            score = 1.0
        else:
            score = difflib.SequenceMatcher(None, nome_key, candidato_key).ratio()
        if score >= 0.92:
            matches.append((score, candidato.name, candidato))
    if not matches:
        return None
    matches.sort(key=lambda item: (-item[0], item[1]))
    return matches[0][2]


def _remover_prefixo_exportacao_limesurvey(nome: str) -> str:
    return re.sub(r"^\d+_\d+_", "", nome)


def _nome_exportado_key(nome: str) -> tuple[str, str]:
    path = Path(nome)
    stem = unicodedata.normalize("NFKD", path.stem.casefold())
    stem = "".join(char for char in stem if not unicodedata.combining(char))
    stem = re.sub(r"[^a-z0-9]+", "-", stem)
    stem = re.sub(r"-+", "-", stem).strip("-")
    return stem, path.suffix.casefold()


__all__ = [
    "AnaliseCandidata",
    "ResolucaoEvidencia",
    "coluna_evidencia",
    "rows_from_xlsx",
    "rows_by_id",
    "inventariar_analises",
    "resolver_evidencia",
]
