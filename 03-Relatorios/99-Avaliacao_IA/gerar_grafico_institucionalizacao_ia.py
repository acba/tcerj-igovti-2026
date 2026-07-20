#!/usr/bin/env python3
"""Gera o gráfico-síntese do estágio de institucionalização da IA."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-igovti-ia")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import PercentFormatter


RELATORIOS_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DADOS = RELATORIOS_ROOT / "99-Avaliacao_IA" / "dados_avaliacao_ia.xlsx"
DEFAULT_OUTPUT = RELATORIOS_ROOT / "99-Avaliacao_IA" / "img" / "cenario_institucionalizacao_ia.png"
DEFAULT_RESULTADO_AUDITORIA = (
    RELATORIOS_ROOT.parent
    / "02-Execucao"
    / "03-Execucao_Procedimentos"
    / "02-Resultados_Auditoria"
    / "resultado_auditoria.json"
)

QUESTOES = {
    "q3001": "Uso institucional\nde IA",
    "q3002": "Diretrizes para\nuso de IA",
    "q3005": "Controles de\nIA generativa",
}

CATEGORIAS = (
    "Não adota",
    "Planejamento ou adoção incipiente",
    "Adoção parcial ou superior",
    "Não se aplica",
)

CORES = {
    "Não adota": "#A6A6A6",
    "Planejamento ou adoção incipiente": "#F4B183",
    "Adoção parcial ou superior": "#70AD47",
    "Não se aplica": "#D9E1F2",
}


def classificar_resposta(resposta: str) -> str:
    resposta = str(resposta).strip().rstrip(".")
    if resposta == "Não adota":
        return "Não adota"
    if resposta in {
        "Há decisão formal ou plano aprovado para adotá-lo",
        "Adota em menor parte",
    }:
        return "Planejamento ou adoção incipiente"
    if resposta in {
        "Adota parcialmente",
        "Adota em maior parte ou totalmente",
    }:
        return "Adoção parcial ou superior"
    if resposta == "Não se aplica":
        return "Não se aplica"
    raise ValueError(f"Resposta não reconhecida na distribuição de IA: {resposta!r}")


def carregar_distribuicoes(path: Path, resultado_auditoria: Path) -> pd.DataFrame:
    dados = pd.read_excel(path, sheet_name="categorias_q3006_detalhe")
    resultado = json.loads(resultado_auditoria.read_text(encoding="utf-8"))
    auditados_validos = {
        sigla for sigla, registro in resultado.items() if registro.get("foi_auditado")
    }
    dados = dados[dados["auditado"].isin(auditados_validos)].copy()

    registros: list[dict[str, object]] = []
    for questao in QUESTOES:
        distribuicao = dados[questao].value_counts(dropna=False)
        for resposta, quantidade in distribuicao.items():
            registros.append(
                {
                    "questao": questao,
                    "categoria": classificar_resposta(resposta),
                    "quantidade": quantidade,
                }
            )
    consolidado = (
        pd.DataFrame(registros)
        .groupby(["questao", "categoria"], as_index=False)["quantidade"]
        .sum()
        .pivot(index="questao", columns="categoria", values="quantidade")
        .fillna(0)
        .reindex(index=QUESTOES, columns=CATEGORIAS, fill_value=0)
    )
    totais = consolidado.sum(axis=1)
    if not (totais == 113).all():
        raise ValueError(f"Totais inesperados nas questões de IA: {totais.to_dict()}")
    return consolidado.div(totais, axis=0) * 100


def gerar_grafico(distribuicoes: pd.DataFrame, output: Path) -> None:
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    fig, ax = plt.subplots(figsize=(11, 4.8))
    esquerda = pd.Series(0.0, index=distribuicoes.index)

    for categoria in CATEGORIAS:
        valores = distribuicoes[categoria]
        barras = ax.barh(
            [QUESTOES[q] for q in distribuicoes.index],
            valores,
            left=esquerda,
            color=CORES[categoria],
            edgecolor="white",
            linewidth=0.8,
            height=0.58,
            label=categoria,
        )
        for barra, valor in zip(barras, valores):
            if valor >= 4:
                ax.text(
                    barra.get_x() + barra.get_width() / 2,
                    barra.get_y() + barra.get_height() / 2,
                    f"{valor:.1f}%".replace(".", ","),
                    ha="center",
                    va="center",
                    fontsize=9,
                    color="#222222",
                    fontweight="bold",
                )
        esquerda = esquerda + valores

    ax.set_xlim(0, 100)
    ax.xaxis.set_major_formatter(PercentFormatter(100, decimals=0))
    ax.set_xlabel("Percentual das organizações avaliadas (n=113)")
    ax.grid(axis="x", color="#D9D9D9", linewidth=0.7, alpha=0.8)
    ax.set_axisbelow(True)
    ax.invert_yaxis()
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.22),
        ncol=2,
        frameon=False,
    )
    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dados", type=Path, default=DEFAULT_DADOS)
    parser.add_argument(
        "--resultado-auditoria",
        type=Path,
        default=DEFAULT_RESULTADO_AUDITORIA,
        help="Resultado da auditoria usado para restringir o universo às organizações avaliadas.",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    gerar_grafico(
        carregar_distribuicoes(args.dados, args.resultado_auditoria),
        args.output,
    )
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
