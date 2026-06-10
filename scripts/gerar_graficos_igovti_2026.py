#!/usr/bin/env python3
"""Gera os graficos consolidados da apresentacao dos resultados do iGovTI 2026."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import openpyxl


ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT / "02-Execucao" / "01-Questionario" / "iGovTI-2026.xlsx"
OUTPUT_DIR = ROOT / "03-Relatorios" / "02-Relatorios_Individuais_Preliminares"

LEVELS = ["Inexpressivo", "Iniciando", "Intermediário", "Aprimorado"]
LEVEL_COLORS = ["#B64B5A", "#D59A2F", "#167D8D", "#2F7D5B"]

COMPONENTS = {
    "iGovTI": "iGovTI",
    "GovernancaTI": "Governança",
    "iGestTI": "Gestão",
}

DIMENSIONS = {
    "PlanejamentoTI": "Planejamento",
    "ServicosTI": "Serviços",
    "RiscosTISegInfo": "Riscos e segurança",
    "EstruturaSegInfo": "Estrutura de segurança",
    "ProcessoSegInfo": "Processos de segurança",
    "GerirSoluçõesTI": "Gestão de soluções",
}

COMPONENT_COLORS = ["#3B6EA8", "#D59A2F", "#167D8D"]
DIMENSION_COLORS = ["#3B6EA8", "#167D8D", "#B64B5A", "#7556A5", "#2F7D5B", "#D59A2F"]


def load_unique_rows() -> list[dict[str, object]]:
    workbook = openpyxl.load_workbook(INPUT_FILE, read_only=True, data_only=True)
    rows = list(workbook["resultados"].iter_rows(values_only=True))
    headers = rows[0]
    records = [dict(zip(headers, row)) for row in rows[1:] if row[0] is not None]

    unique: dict[str, dict[str, object]] = {}
    for record in records:
        key = str(record["id"]).strip()
        if key not in unique or completeness(record) > completeness(unique[key]):
            unique[key] = record

    result = list(unique.values())
    if len(result) != 114:
        raise RuntimeError(f"Esperadas 114 organizacoes unicas; encontradas {len(result)}")
    return result


def completeness(record: dict[str, object]) -> int:
    return sum(
        value not in {None, "", 0, 0.0}
        for key, value in record.items()
        if key not in {"id", "nivel_maturidade"}
    )


def configure_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "axes.labelcolor": "#1F2937",
            "axes.titlecolor": "#111827",
            "xtick.color": "#374151",
            "ytick.color": "#374151",
        }
    )


def clean_axis(ax: plt.Axes, grid_axis: str = "y") -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis=grid_axis, color="#D1D5DB", linewidth=0.7, alpha=0.7)
    ax.set_axisbelow(True)


def save(fig: plt.Figure, filename: str) -> None:
    fig.savefig(OUTPUT_DIR / filename, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def plot_maturity(records: list[dict[str, object]]) -> None:
    counts = Counter(str(record["nivel_maturidade"]) for record in records)
    values = [counts[level] for level in LEVELS]
    percentages = [100 * value / len(records) for value in values]

    fig, ax = plt.subplots(figsize=(8.8, 5.4))
    bars = ax.bar(LEVELS, values, color=LEVEL_COLORS, width=0.66)
    ax.bar_label(
        bars,
        labels=[f"{value}\n({percentage:.1f}%)" for value, percentage in zip(values, percentages)],
        padding=5,
        fontsize=10,
        fontweight="bold",
    )
    ax.set_ylabel("Número de organizações")
    ax.set_ylim(0, max(values) * 1.22)
    ax.set_title("Distribuição por nível de maturidade do iGovTI 2026", loc="left", fontweight="bold")
    clean_axis(ax)
    save(fig, "igovti_2026_distribuicao_maturidade.png")


def plot_components(records: list[dict[str, object]]) -> None:
    values = [[float(record[key]) for record in records] for key in COMPONENTS]
    positions = np.arange(1, len(values) + 1)

    fig, ax = plt.subplots(figsize=(8.8, 5.8))
    violin = ax.violinplot(values, positions=positions, widths=0.72, showmeans=False, showmedians=False, showextrema=False)
    for body, color in zip(violin["bodies"], COMPONENT_COLORS):
        body.set_facecolor(color)
        body.set_edgecolor(color)
        body.set_alpha(0.25)

    box = ax.boxplot(
        values,
        positions=positions,
        widths=0.30,
        patch_artist=True,
        showfliers=False,
        medianprops={"color": "#111827", "linewidth": 1.8},
        whiskerprops={"color": "#6B7280"},
        capprops={"color": "#6B7280"},
    )
    for patch, color in zip(box["boxes"], COMPONENT_COLORS):
        patch.set_facecolor(color)
        patch.set_edgecolor(color)
        patch.set_alpha(0.78)

    rng = np.random.default_rng(2026)
    for position, series, color in zip(positions, values, COMPONENT_COLORS):
        jitter = rng.normal(0, 0.045, len(series))
        ax.scatter(position + jitter, series, s=11, color=color, alpha=0.34, linewidth=0)
        ax.scatter(position, np.mean(series), marker="D", s=42, color="white", edgecolor="#111827", zorder=5)

    ax.axhline(0.15, color="#B64B5A", linewidth=0.8, linestyle="--", alpha=0.75)
    ax.axhline(0.40, color="#D59A2F", linewidth=0.8, linestyle="--", alpha=0.75)
    ax.axhline(0.70, color="#2F7D5B", linewidth=0.8, linestyle="--", alpha=0.75)
    ax.set_xticks(positions, COMPONENTS.values())
    ax.set_ylabel("Resultado")
    ax.set_ylim(-0.03, 1.03)
    ax.set_title("Distribuição do índice e de seus componentes principais", loc="left", fontweight="bold")
    ax.text(3.43, 0.15, "0,15", va="center", fontsize=8, color="#8E3744")
    ax.text(3.43, 0.40, "0,40", va="center", fontsize=8, color="#8A641E")
    ax.text(3.43, 0.70, "0,70", va="center", fontsize=8, color="#245F46")
    clean_axis(ax)
    save(fig, "igovti_2026_distribuicao_componentes.png")


def plot_dimensions(records: list[dict[str, object]]) -> None:
    keys = list(DIMENSIONS)
    labels = list(DIMENSIONS.values())
    values = [[float(record[key]) for record in records] for key in keys]
    positions = np.arange(1, len(values) + 1)

    fig, ax = plt.subplots(figsize=(9.4, 6.4))
    box = ax.boxplot(
        values,
        positions=positions,
        vert=False,
        widths=0.55,
        patch_artist=True,
        showfliers=False,
        medianprops={"color": "#111827", "linewidth": 1.7},
        whiskerprops={"color": "#6B7280"},
        capprops={"color": "#6B7280"},
    )
    for patch, color in zip(box["boxes"], DIMENSION_COLORS):
        patch.set_facecolor(color)
        patch.set_edgecolor(color)
        patch.set_alpha(0.78)

    for position, series, color in zip(positions, values, DIMENSION_COLORS):
        mean = float(np.mean(series))
        ax.scatter(mean, position, marker="D", s=48, color="white", edgecolor="#111827", zorder=5)
        ax.text(mean + 0.025, position + 0.23, f"média {mean:.3f}", fontsize=8, color="#374151")

    ax.axvline(0.15, color="#B64B5A", linewidth=0.8, linestyle="--", alpha=0.75)
    ax.axvline(0.40, color="#D59A2F", linewidth=0.8, linestyle="--", alpha=0.75)
    ax.axvline(0.70, color="#2F7D5B", linewidth=0.8, linestyle="--", alpha=0.75)
    ax.set_yticks(positions, labels)
    ax.set_xlabel("Resultado")
    ax.set_xlim(-0.02, 1.03)
    ax.set_title("Distribuição das dimensões que compõem o iGestTI", loc="left", fontweight="bold")
    clean_axis(ax, grid_axis="x")
    save(fig, "igovti_2026_distribuicao_dimensoes_gestao.png")


def plot_correlation(records: list[dict[str, object]]) -> None:
    keys = list(DIMENSIONS)
    labels = list(DIMENSIONS.values())
    matrix = np.array([[float(record[key]) for key in keys] for record in records])
    correlation = np.corrcoef(matrix, rowvar=False)

    fig, ax = plt.subplots(figsize=(9.2, 7.2))
    image = ax.imshow(correlation, cmap="RdYlGn", vmin=0.5, vmax=1.0)
    for row in range(len(keys)):
        for column in range(len(keys)):
            value = correlation[row, column]
            ax.text(
                column,
                row,
                f"{value:.2f}",
                ha="center",
                va="center",
                color="white" if value >= 0.78 else "#111827",
                fontweight="bold" if row == column else "normal",
            )

    ax.set_xticks(range(len(labels)), labels, rotation=35, ha="right")
    ax.set_yticks(range(len(labels)), labels)
    ax.set_title("Correlação entre as dimensões do iGestTI", loc="left", fontweight="bold")
    fig.colorbar(image, ax=ax, label="Correlação de Pearson", shrink=0.82)
    save(fig, "igovti_2026_correlacao_dimensoes_gestao.png")


def main() -> None:
    configure_style()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    records = load_unique_rows()
    plot_maturity(records)
    plot_components(records)
    plot_dimensions(records)
    plot_correlation(records)
    print(f"Graficos do iGovTI 2026 gerados para {len(records)} organizacoes unicas.")


if __name__ == "__main__":
    main()
