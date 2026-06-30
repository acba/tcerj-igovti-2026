#!/usr/bin/env python3
"""Gera os graficos da comparacao harmonizada do iGovTI 2023 e 2026."""

from __future__ import annotations

import re
import os
import tempfile
import unicodedata
from collections import Counter
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-igovti")

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import openpyxl


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "02-Execucao" / "02-Questionario iGovTI 2023"
OUTPUT_DIR = Path(tempfile.gettempdir()) / "tcerj-igovti-2026/relatorio-consolidado/img"

FILES = {
    "setic_2023": DATA_DIR / "iGovTI-2023-SETIC-Ajustado-Comparavel.xlsx",
    "municipios_2023": DATA_DIR / "iGovTI-2023-Municipios-Ajustado-Comparavel.xlsx",
    "igovti_2026": ROOT / "02-Execucao/01-Questionario/04-Resultados_iGovTI/20260621-iGovTI-2026-Ajustado-Comparavel.xlsx",
}

ALIASES = {
    "FIARJ": "FIA",
    "FTMRJ": "FTM",
    "IO": "IOERJ",
    "IPEMRJ": "IPEM",
    "RIOPREVI": "RIOPREVIDENCIA",
    "RIOTRILH": "RIOTRILHOS",
    "SEDSODH": "SEDSDH",
}

LEVELS = ["Inexpressivo", "Iniciando", "Intermediário", "Aprimorado"]

PRACTICES = {
    "ModeloTI": "Modelo de gestão",
    "MonitorAvaliaTI": "Monitoramento e avaliação",
    "ResultadoTI": "Resultados e simplificação",
    "PlanejamentoTI": "Planejamento de TI",
    "PessoasTI": "Pessoas",
    "iGestServicosTI": "Gestão de Serviços",
    "iGestNiveisServicoTI": "Níveis de serviço",
    "iGestRiscosTI": "Riscos de TI",
    "EstruturaSegInfo": "Estrutura de segurança",
    "ProcessoSegInfo": "Processos de segurança",
    "ProcessoSoftware": "Processo de software",
    "iGestProjetosTI": "Projetos de TI",
}

GREEN = "#2F7D5B"
RED = "#B64B5A"
TEAL = "#167D8D"
GOLD = "#D59A2F"
GRAY = "#6B7280"


def load_rows(path: Path) -> list[dict[str, object]]:
    workbook = openpyxl.load_workbook(path, read_only=True, data_only=True)
    sheet = workbook["resultados"]
    rows = list(sheet.iter_rows(values_only=True))
    headers = rows[0]
    return [dict(zip(headers, row)) for row in rows[1:] if row[0] is not None]


def normalize_id(value: object) -> str:
    text = unicodedata.normalize("NFKD", str(value))
    text = text.encode("ascii", "ignore").decode().upper()
    text = re.sub(r"^PREFEITURA MUNICIPAL DE ", "", text)
    return re.sub(r"[^A-Z0-9]", "", text)


def completeness(row: dict[str, object]) -> int:
    return sum(
        value not in {None, "", 0, 0.0}
        for key, value in row.items()
        if key not in {"id", "nivel_maturidade"}
    )


def paired_rows() -> list[tuple[dict[str, object], dict[str, object]]]:
    rows_2023 = load_rows(FILES["setic_2023"]) + load_rows(FILES["municipios_2023"])
    rows_2026 = load_rows(FILES["igovti_2026"])

    by_id_2026: dict[str, dict[str, object]] = {}
    for row in rows_2026:
        key = normalize_id(row["id"])
        if key not in by_id_2026 or completeness(row) > completeness(by_id_2026[key]):
            by_id_2026[key] = row

    pairs: list[tuple[dict[str, object], dict[str, object]]] = []
    for row_2023 in rows_2023:
        key_2023 = normalize_id(row_2023["id"])
        key_2026 = key_2023 if key_2023 in by_id_2026 else ALIASES.get(key_2023)
        if key_2026 in by_id_2026:
            pairs.append((row_2023, by_id_2026[key_2026]))

    return pairs


def style_axis(ax: plt.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", color="#D1D5DB", linewidth=0.7, alpha=0.7)
    ax.set_axisbelow(True)


def save(fig: plt.Figure, filename: str) -> None:
    fig.savefig(OUTPUT_DIR / filename, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def plot_distribution(pairs: list[tuple[dict[str, object], dict[str, object]]]) -> None:
    values_2023 = np.array([float(old["iGovTI"]) for old, _ in pairs])
    values_2026 = np.array([float(new["iGovTI"]) for _, new in pairs])

    fig, ax = plt.subplots(figsize=(8.2, 5.4))
    for old, new in zip(values_2023, values_2026):
        color = GREEN if new >= old else RED
        ax.plot([1, 2], [old, new], color=color, alpha=0.17, linewidth=0.8, zorder=1)

    box = ax.boxplot(
        [values_2023, values_2026],
        positions=[1, 2],
        widths=0.42,
        patch_artist=True,
        showfliers=False,
        medianprops={"color": "#111827", "linewidth": 1.8},
        whiskerprops={"color": GRAY},
        capprops={"color": GRAY},
    )
    box["boxes"][0].set(facecolor=GOLD, alpha=0.72, edgecolor="#8A641E")
    box["boxes"][1].set(facecolor=TEAL, alpha=0.72, edgecolor="#0E5964")

    rng = np.random.default_rng(2026)
    ax.scatter(1 + rng.normal(0, 0.035, len(values_2023)), values_2023, s=16, color=GOLD, alpha=0.65, zorder=3)
    ax.scatter(2 + rng.normal(0, 0.035, len(values_2026)), values_2026, s=16, color=TEAL, alpha=0.65, zorder=3)
    ax.set_xticks([1, 2], ["2023", "2026"])
    ax.set_ylabel("iGovTI comparável")
    ax.set_ylim(-0.03, 0.78)
    ax.text(1, values_2023.mean() + 0.025, f"média {values_2023.mean():.3f}", ha="center", color="#6B4D17")
    ax.text(2, values_2026.mean() + 0.025, f"média {values_2026.mean():.3f}", ha="center", color="#0E5964")
    style_axis(ax)
    save(fig, "igovti_comparavel_distribuicao_2023_2026.png")


def plot_transition(pairs: list[tuple[dict[str, object], dict[str, object]]]) -> None:
    matrix = np.zeros((4, 4), dtype=int)
    level_index = {level: index for index, level in enumerate(LEVELS)}
    for old, new in pairs:
        matrix[level_index[str(old["nivel_maturidade"])]][level_index[str(new["nivel_maturidade"])]] += 1

    fig, ax = plt.subplots(figsize=(8.6, 5.8))
    image = ax.imshow(matrix, cmap="YlGnBu", vmin=0, vmax=matrix.max())
    for row in range(4):
        for column in range(4):
            value = matrix[row, column]
            color = "white" if value >= matrix.max() * 0.55 else "#111827"
            ax.text(column, row, str(value), ha="center", va="center", fontsize=13, fontweight="bold", color=color)
    ax.set_xticks(range(4), LEVELS)
    ax.set_yticks(range(4), LEVELS)
    ax.set_xlabel("Nível em 2026")
    ax.set_ylabel("Nível em 2023")
    fig.colorbar(image, ax=ax, label="Número de organizações", shrink=0.82)
    save(fig, "igovti_comparavel_transicao_maturidade_2023_2026.png")


def plot_aggregate_changes(pairs: list[tuple[dict[str, object], dict[str, object]]]) -> None:
    changes = []
    for key, label in PRACTICES.items():
        delta = np.mean([float(new[key]) - float(old[key]) for old, new in pairs])
        changes.append((delta, label))
    changes.sort()

    values = [item[0] for item in changes]
    labels = [item[1] for item in changes]
    colors = [GREEN if value >= 0 else RED for value in values]

    fig, ax = plt.subplots(figsize=(9.2, 6.6))
    bars = ax.barh(labels, values, color=colors, alpha=0.9)
    ax.axvline(0, color="#111827", linewidth=0.9)
    ax.bar_label(bars, labels=[f"{value:+.3f}" for value in values], padding=4, fontsize=9)
    ax.set_xlim(min(values) - 0.04, max(values) + 0.055)
    ax.set_xlabel("Variação média (2026 - 2023)")
    ax.grid(axis="x", color="#D1D5DB", linewidth=0.7, alpha=0.7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    save(fig, "igovti_comparavel_variacao_agregados_2023_2026.png")


def plot_largest_changes(pairs: list[tuple[dict[str, object], dict[str, object]]]) -> None:
    changes = sorted(
        ((float(new["iGovTI"]) - float(old["iGovTI"]), str(new["id"])) for old, new in pairs),
        key=lambda item: item[0],
    )
    selected = changes[:10] + changes[-10:]
    values = [item[0] for item in selected]
    labels = [item[1] for item in selected]
    colors = [GREEN if value >= 0 else RED for value in values]

    fig, ax = plt.subplots(figsize=(9.5, 8.2))
    bars = ax.barh(labels, values, color=colors, alpha=0.9)
    ax.axvline(0, color="#111827", linewidth=0.9)
    ax.bar_label(bars, labels=[f"{value:+.3f}" for value in values], padding=4, fontsize=9)
    ax.set_xlim(min(values) - 0.06, max(values) + 0.09)
    ax.set_xlabel("Variação do iGovTI comparável (2026 - 2023)")
    ax.grid(axis="x", color="#D1D5DB", linewidth=0.7, alpha=0.7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    save(fig, "igovti_comparavel_maiores_variacoes_2023_2026.png")


def main() -> None:
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
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pairs = paired_rows()
    plot_distribution(pairs)
    plot_transition(pairs)
    plot_aggregate_changes(pairs)
    plot_largest_changes(pairs)

    transitions = Counter((old["nivel_maturidade"], new["nivel_maturidade"]) for old, new in pairs)
    print(f"Graficos gerados para {len(pairs)} organizacoes e {len(transitions)} transicoes observadas.")


if __name__ == "__main__":
    main()
