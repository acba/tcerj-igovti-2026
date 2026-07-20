#!/usr/bin/env python3
"""Compara os cenários pós-evidências e pós-comentários do gestor."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

try:
    from impactos_utils import indices_igovti, situacoes_auditoria
except ModuleNotFoundError:
    from scripts.impactos_utils import indices_igovti, situacoes_auditoria


def calcular(
    auditoria_anterior: Path,
    auditoria_atual: Path,
    contexto_anterior: Path,
    contexto_atual: Path,
) -> dict[str, dict[str, object]]:
    anterior = situacoes_auditoria(auditoria_anterior)
    atual = situacoes_auditoria(auditoria_atual)
    indices_antes = indices_igovti(contexto_anterior)
    indices_depois = indices_igovti(contexto_atual)
    universo = sorted(set(anterior) | set(atual) | set(indices_antes) | set(indices_depois))
    resultado: dict[str, dict[str, object]] = {}
    for sigla in universo:
        antes = anterior.get(sigla, {"achados": set(), "situacoes": set()})
        depois = atual.get(sigla, {"achados": set(), "situacoes": set()})
        ia, idp = indices_antes.get(sigla), indices_depois.get(sigla)
        resultado[sigla] = {
            "situacoes_antes": len(antes["situacoes"]),
            "situacoes_atuais": len(depois["situacoes"]),
            "situacoes_removidas": len(antes["situacoes"] - depois["situacoes"]),
            "achados_antes": len(antes["achados"]),
            "achados_atuais": len(depois["achados"]),
            "achados_removidos": len(antes["achados"] - depois["achados"]),
            "igovti_anterior": ia,
            "igovti_atual": idp,
            "variacao_igovti": idp - ia if ia is not None and idp is not None else None,
        }
    return resultado


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--auditoria-anterior", type=Path, required=True)
    parser.add_argument("--auditoria-atual", type=Path, required=True)
    parser.add_argument("--contexto-igovti-anterior", type=Path, required=True)
    parser.add_argument("--contexto-igovti-atual", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-xlsx", type=Path, required=True)
    args = parser.parse_args()
    resultado = calcular(
        args.auditoria_anterior,
        args.auditoria_atual,
        args.contexto_igovti_anterior,
        args.contexto_igovti_atual,
    )
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_xlsx.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    rows = [{"Auditado": sigla, **values} for sigla, values in resultado.items()]
    pd.DataFrame(rows).to_excel(args.output_xlsx, sheet_name="Impactos", index=False)
    print(args.output_json)
    print(args.output_xlsx)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
