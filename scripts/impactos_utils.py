"""Leitores compartilhados para comparações de auditoria e iGovTI."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def texto(value: object) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    return str(value).strip()


def situacoes_auditoria(path: Path | None) -> dict[str, dict[str, set[str]]]:
    if not path or not path.is_file():
        return {}
    dados = json.loads(path.read_text(encoding="utf-8"))
    result: dict[str, dict[str, set[str]]] = {}
    for sigla, orgao in dados.items():
        achados: set[str] = set()
        situacoes: set[str] = set()
        for proc in orgao.get("procedimentos_executados") or []:
            achado = proc.get("achado") or {}
            if not proc.get("achado_ocorreu") and not achado:
                continue
            numero = texto(achado.get("numero") or proc.get("numero_achado"))
            if numero:
                achados.add(numero)
            situacoes.update(texto(item) for item in achado.get("situacoes_encontradas") or [] if texto(item))
        result[str(sigla).upper()] = {"achados": achados, "situacoes": situacoes}
    return result


def indices_igovti(path: Path | None) -> dict[str, float]:
    if not path or not path.is_file():
        return {}
    frame = pd.read_excel(path)
    sigla = next((column for column in frame.columns if str(column).casefold() == "sigla"), None)
    indice = next((column for column in frame.columns if str(column).casefold() == "igovti"), None)
    if sigla is None or indice is None:
        return {}
    return {
        texto(row[sigla]).upper(): float(row[indice])
        for _, row in frame.iterrows() if texto(row[sigla]) and pd.notna(row[indice])
    }
