#!/usr/bin/env python3
"""Converte pareceres consolidados em minuta de ajustes compatível com o aplicador."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


COLUNAS = [
    "Auditado",
    "Código do item avaliado",
    "Achado",
    "Resposta afirmada",
    "Avaliações dos modelos",
    "Resultado da avaliação do juiz",
    "Justificativa do juiz",
    "Avaliação do auditor revisor",
    "Justificativa do auditor revisor",
]


def gerar(input_path: Path, output_path: Path) -> None:
    frame = pd.read_excel(input_path)
    required = {"auditado", "item", "estado", "justificativa"}
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"Parecer consolidado sem colunas obrigatórias: {', '.join(missing)}")
    afirmacoes_elegiveis = {
        "y", "sim", "adota parcialmente.", "adota parcialmente",
        "adota em maior parte ou totalmente.", "adota em maior parte ou totalmente",
    }
    frame = frame.loc[
        frame["estado"].astype(str).str.casefold().eq("nao_conforme")
        & frame["afirmacao_auditado"].fillna("").astype(str).str.strip().str.casefold().isin(afirmacoes_elegiveis)
    ].copy()
    frame["afirmacao_auditado"] = frame["afirmacao_auditado"].replace({"Y": "Sim", "y": "Sim"})
    result = pd.DataFrame(
        {
            "Auditado": frame["auditado"].astype(str).str.strip().str.upper(),
            "Código do item avaliado": frame["item"].astype(str).str.strip(),
            "Achado": frame.get("gera_achado", ""),
            "Resposta afirmada": frame.get("afirmacao_auditado", ""),
            "Avaliações dos modelos": frame.get("opinioes_modelos", ""),
            "Resultado da avaliação do juiz": "Não conforme",
            "Justificativa do juiz": frame["justificativa"],
            "Avaliação do auditor revisor": "",
            "Justificativa do auditor revisor": "",
        }
    )
    result = result.loc[result["Código do item avaliado"].ne("")].drop_duplicates(
        ["Auditado", "Código do item avaliado"], keep="last"
    ).sort_values(
        ["Auditado", "Código do item avaliado"], kind="stable"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        result[COLUNAS].to_excel(writer, sheet_name="Ajustes Respostas iGovTI", index=False)
        pendencias = result.loc[
            ~result["Resultado da avaliação do juiz"].isin(["Conforme", "Não conforme"])
        ]
        pendencias[COLUNAS].to_excel(writer, sheet_name="Pendências", index=False)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pareceres", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    gerar(args.pareceres, args.output)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
