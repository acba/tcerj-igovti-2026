#!/usr/bin/env python3
"""Gera gráficos para os relatórios consolidado e individuais do iGovTI 2026."""

from __future__ import annotations

import argparse
import concurrent.futures
import math
import os
import re
import shutil
import tempfile
import unicodedata
from collections import Counter
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-igovti")

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, to_rgba
from matplotlib.patches import Patch, Rectangle
import numpy as np
import pandas as pd
import yaml

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "resources"))

from igovti_dados_utils import (
    COMPARAVEL_2023_MUNICIPIOS,
    COMPARAVEL_2023_SETIC,
    COMPARAVEL_2026,
    RESULTADOS_2026,
    RESPOSTAS_2026,
    carregar_resultados_2026,
    consolidar_pareamentos,
)


ROOT = Path(__file__).resolve().parents[1]
RESULTS_FILE = RESULTADOS_2026
RAW_FILE = RESPOSTAS_2026
METHODOLOGY_FILE = ROOT / "01-Planejamento/02-Metodologia_iGovTI/estrutura-igovti-2026.yaml"
PROCEDURES_FILE = ROOT / "02-Execucao/03-Execucao_Procedimentos/01-Insumos/mapa-verificacao-achados.xlsx"
DEFAULT_OUTPUT_ROOT = Path(tempfile.gettempdir()) / "tcerj-igovti-2026"
CONSOLIDATED_IMG = DEFAULT_OUTPUT_ROOT / "relatorio-consolidado/img"
INDIVIDUAL_IMG = DEFAULT_OUTPUT_ROOT / "relatorios-individuais/img"

DPI = 300
SKIP_EXISTING = False
WORKER_RESULTS: pd.DataFrame | None = None
WORKER_RAW_BY_KEY: pd.DataFrame | None = None
WORKER_PAIRS_BY_KEY: dict[str, dict[str, object]] | None = None
LEVELS = ["Inexpressivo", "Iniciando", "Intermediário", "Aprimorado"]
LEVEL_COLORS = {
    "Inexpressivo": "#B22222",  # firebrick
    "Iniciando": "#FFA500",     # orange
    "Intermediário": "#9ACD32", # yellowgreen
    "Aprimorado": "#228B22",    # forestgreen
}
LEVEL_BOUNDS = [0.0, 0.15, 0.40, 0.70, 1.0]

COMPONENTS = {
    "iGovTI": "iGovTI",
    "GovernancaTI": "Governança de TIC",
    "iGestTI": "Gestão de TIC",
}
DIMENSIONS = {
    "PlanejamentoTI": "Planejamento de TI",
    "ServicosTI": "Gestão de Serviços",
    "RiscosTISegInfo": "Riscos e segurança",
    "EstruturaSegInfo": "Estrutura de segurança",
    "ProcessoSegInfo": "Processos de segurança",
    "GerirSoluçõesTI": "Gestão de soluções",
}
QUESTION_LABELS = {
    "PA01": "Q1 - Estrutura de TIC",
    "PA02": "Q2 - Governança e comitê",
    "PA03": "Q3 - Planejamento de TIC",
    "PA04": "Q4 - Capacidade institucional",
    "PA05": "Q5 - Gestão de serviços",
    "PA06": "Q6 - Contratações de TIC",
}
BASE_QUESTIONS = [
    "q1001", "q1002", "q1003", "q1004",
    "q2101", "q2102",
    "q2201", "q2202", "q2203", "q2204",
    "q2301", "q2302", "q2303",
    "q2401", "q2402", "q2403",
    "q2501", "q2502", "q2503", "q2504",
    "q2601", "q2602",
]
QUESTION_GROUPS = {
    "Q1": ["q0101", "q0102", "q0103[D]", "q0103[G]"],
    "Q2": ["q1001", "q1002"],
    "Q3": ["q2101", "q2102"],
    "Q4": ["q2701", "q2702", "q2703", "q2704", "q2705", "q2706", "q2708[A]", "q2708[B]", "q2708[C]", "q2708[D]"],
    "Q5": ["q2201", "q2202", "q2203", "q2204"],
    "Q6": ["q2801", "q2802", "q2804[A]", "q2804[B]", "q2804[C]"],
}
WORKFORCE_LINKS = ["efetivos", "comissionados", "terceirizados", "cedidos", "temporarios", "estagiarios"]
WORKFORCE_LABELS = ["Efetivos", "Comissionados", "Terceirizados", "Cedidos", "Temporários", "Estagiários"]
WORKFORCE_COLORS = ["#3B6EA8", "#7556A5", "#D59A2F", "#167D8D", "#B64B5A", "#6B7280"]

RESPONSE_ORDER = [
    "Não adota",
    "Há decisão formal",
    "Adota em menor parte",
    "Adota parcialmente",
    "Adota em maior parte ou totalmente",
    "Não se aplica",
]
RESPONSE_COLORS = {
    "Não adota": LEVEL_COLORS["Inexpressivo"],
    "Há decisão formal": "#D2691E",
    "Adota em menor parte": LEVEL_COLORS["Iniciando"],
    "Adota parcialmente": LEVEL_COLORS["Intermediário"],
    "Adota em maior parte ou totalmente": LEVEL_COLORS["Aprimorado"],
    "Não se aplica": "#9CA3AF",
}
def configure_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "axes.labelcolor": "#1F2937",
            "axes.titlecolor": "#111827",
            "axes.edgecolor": "#9CA3AF",
            "xtick.color": "#374151",
            "ytick.color": "#374151",
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.dpi": DPI,
        }
    )


def normalize_id(value: object) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = text.encode("ascii", "ignore").decode().upper()
    text = re.sub(r"^PREFEITURA MUNICIPAL DE ", "", text)
    return re.sub(r"[^A-Z0-9]", "", text)


def clean_response(value: object) -> str:
    text = str(value or "").strip()
    return text[:-1] if text.endswith(".") else text


def response_category(value: object) -> str | None:
    text = clean_response(value)
    if text == "Não adota":
        return "Não adota"
    if text.startswith("Há decisão formal"):
        return "Há decisão formal"
    if text == "Adota em menor parte":
        return text
    if text == "Adota parcialmente":
        return text
    if text == "Adota em maior parte ou totalmente":
        return text
    if text == "Não se aplica":
        return text
    return None


def maturity(value: float) -> str:
    if value < 0.15:
        return "Inexpressivo"
    if value < 0.40:
        return "Iniciando"
    if value < 0.70:
        return "Intermediário"
    return "Aprimorado"


def safe_float(value: object, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def load_data(results_file: Path = RESULTS_FILE, raw_file: Path = RAW_FILE) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, float]]:
    results = carregar_resultados_2026(results_file)
    raw = pd.read_excel(raw_file)
    if "firstname" not in raw.columns:
        raise ValueError(f"A planilha de respostas nao possui a coluna firstname: {raw_file}")
    if raw["firstname"].isna().any() or raw["firstname"].duplicated().any():
        repetidas = raw.loc[raw["firstname"].duplicated(False), "firstname"].astype(str).tolist()
        raise ValueError(f"A base de respostas deve conter uma linha unica por organizacao. Duplicadas: {repetidas}")
    with METHODOLOGY_FILE.open(encoding="utf-8") as stream:
        methodology = yaml.safe_load(stream)
    category_scores = {str(key): float(value) for key, value in methodology["categorias"].items()}

    raw = pd.concat(
        [raw, raw["firstname"].map(normalize_id).rename("_key")],
        axis=1,
    )
    chaves_resultados = set(results["_key"])
    chaves_respostas = set(raw["_key"])
    if chaves_resultados != chaves_respostas:
        sem_resposta = sorted(chaves_resultados - chaves_respostas)
        sem_resultado = sorted(chaves_respostas - chaves_resultados)
        raise ValueError(
            "As bases de resultados e respostas nao possuem as mesmas organizacoes. "
            f"Sem resposta: {sem_resposta}; sem resultado: {sem_resultado}"
        )
    return results, raw, category_scores


def load_procedure_profiles(raw: pd.DataFrame) -> pd.DataFrame:
    actions = pd.read_excel(PROCEDURES_FILE, sheet_name="Ações de Verificação", header=2)
    procedures = pd.read_excel(PROCEDURES_FILE, sheet_name="Procedimentos de Auditoria", header=2)
    variables = pd.read_excel(PROCEDURES_FILE, sheet_name="Variáveis Temporárias", header=2)
    action_by_id = actions.set_index("id").to_dict("index")
    procedure_actions = {
        row["id"]: list(dict.fromkeys(re.findall(r"\bAV\d+\b", str(row["logica_achado"]))))
        for _, row in procedures.iterrows()
        if str(row.get("id", "")).startswith("PA")
    }

    rows = []
    for _, source in raw.iterrows():
        context = source.to_dict()
        for _, variable in variables.iterrows():
            name = str(variable.get("nome", "")).strip()
            expression = str(variable.get("expressao", "")).strip()
            if not name or name == "nan" or not expression or expression == "nan":
                continue
            context[name] = evaluate_temporary(expression, context)

        output = {"_key": source["_key"]}
        for procedure_id, action_ids in procedure_actions.items():
            evaluations = []
            for action_id in action_ids:
                action = action_by_id[action_id]
                field = str(action["informacao_requerida"])
                actual = context.get(field)
                if actual is None or (isinstance(actual, float) and math.isnan(actual)):
                    continue
                nonconforming = evaluate_condition(str(action["situacao_inconforme"]), actual)
                evaluations.append(0.0 if nonconforming else 1.0)
            output[procedure_id] = float(np.mean(evaluations)) if evaluations else np.nan
        rows.append(output)
    return pd.DataFrame(rows)


def evaluate_temporary(expression: str, context: dict[str, object]) -> object:
    prepared = expression
    references = re.findall(r"q\d{4}(?:\[[^]]+\])?", expression)
    for reference in sorted(set(references), key=len, reverse=True):
        prepared = prepared.replace(reference, repr(safe_float(context.get(reference))))
    variable_names = re.findall(r"\b[A-Za-z_]\w*\b", prepared)
    for name in sorted(set(variable_names), key=len, reverse=True):
        if name in context and name not in {"True", "False"}:
            prepared = re.sub(rf"\b{re.escape(name)}\b", repr(context[name]), prepared)
    try:
        return eval(prepared, {"__builtins__": {}}, {})
    except Exception:
        return np.nan


def evaluate_condition(expression: str, actual: object) -> bool:
    expression = str(expression).strip()
    actual_text = str(actual).strip()
    if expression.startswith("~(") and expression.endswith(")"):
        return actual_text != expression[2:-1]
    if expression.startswith("(") and expression.endswith(")") and " | " in expression:
        return any(evaluate_condition(item, actual) for item in expression[1:-1].split(" | "))
    if expression.startswith("~"):
        return not evaluate_condition(expression[1:], actual)
    if expression in {"True", "False"}:
        return bool(actual) is (expression == "True")
    for operator in (">=", "<=", ">", "<"):
        if expression.startswith(operator):
            target = safe_float(expression[len(operator):])
            value = safe_float(actual)
            return {">=": value >= target, "<=": value <= target, ">": value > target, "<": value < target}[operator]
    try:
        return float(actual) == float(expression)
    except (TypeError, ValueError):
        return actual_text == expression


def load_pairs(
    comparable_2026: Path = COMPARAVEL_2026,
    setic_2023: Path = COMPARAVEL_2023_SETIC,
    municipios_2023: Path = COMPARAVEL_2023_MUNICIPIOS,
) -> list[dict[str, object]]:
    _, pareados, _ = consolidar_pareamentos(comparable_2026, setic_2023, municipios_2023)
    pairs = []
    for _, row in pareados.iterrows():
        old = {"id": row["sigla_2023"], "nivel_maturidade": row["nivel_maturidade_2023"]}
        new = {"id": row["sigla_2026"], "nivel_maturidade": row["nivel_maturidade_2026"]}
        for column in row.index:
            if column.endswith("_2023"):
                old[column[:-5]] = row[column]
            elif column.endswith("_2026") and column not in {"sigla_2026", "chave_2026", "nivel_maturidade_2026"}:
                new[column[:-5]] = row[column]
        pairs.append({"grupo": row["grupo"], "key": row["chave_2026"], "old": old, "new": new})
    return pairs


def clean_axis(ax: plt.Axes, grid_axis: str = "y") -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis=grid_axis, color="#D1D5DB", linewidth=0.7, alpha=0.7)
    ax.set_axisbelow(True)


def add_maturity_background(ax: plt.Axes, orientation: str = "vertical", alpha: float = 0.08) -> None:
    for index, level in enumerate(LEVELS):
        start, end = LEVEL_BOUNDS[index], LEVEL_BOUNDS[index + 1]
        if orientation == "vertical":
            ax.axvspan(start, end, color=LEVEL_COLORS[level], alpha=alpha, linewidth=0)
        else:
            ax.axhspan(start, end, color=LEVEL_COLORS[level], alpha=alpha, linewidth=0)


def save(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if SKIP_EXISTING and path.exists():
        plt.close(fig)
        return
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor="white", metadata={"Software": "TCE-RJ iGovTI 2026"})
    plt.close(fig)


def save_shared(fig: plt.Figure, filename: str) -> None:
    target = CONSOLIDATED_IMG / filename
    save(fig, target)
    INDIVIDUAL_IMG.mkdir(parents=True, exist_ok=True)
    individual_target = INDIVIDUAL_IMG / filename
    if not (SKIP_EXISTING and individual_target.exists()):
        shutil.copy2(target, individual_target)


def individual_output(sigla: object, filename: str) -> Path:
    return INDIVIDUAL_IMG / str(sigla) / filename


def maturity_legend(ax: plt.Axes, location: str = "upper center", extra_handles: list | None = None) -> None:
    handles = [Patch(facecolor=LEVEL_COLORS[level], label=level) for level in LEVELS]
    if extra_handles:
        handles.extend(extra_handles)
    ax.legend(handles=handles, ncol=min(len(handles), 4), loc=location, bbox_to_anchor=(0.5, 1.12), frameon=False)


def plot_maturity_distribution(results: pd.DataFrame) -> None:
    counts = results["iGovTI_maturidade"].value_counts().reindex(LEVELS, fill_value=0)
    fig, ax = plt.subplots(figsize=(9.2, 3.4))
    bars = ax.bar(LEVELS, counts.values, color=[LEVEL_COLORS[level] for level in LEVELS], width=0.68)
    labels = [f"{value}\n({value / counts.sum():.1%})" for value in counts.values]
    ax.bar_label(bars, labels=labels, padding=5, fontweight="bold")
    ax.set_ylabel("Número de organizações")
    ax.set_ylim(0, max(counts.values) * 1.23)
    clean_axis(ax)
    save_shared(fig, "igovti_2026_distribuicao_maturidade.png")


def plot_continuous_distribution(results: pd.DataFrame) -> None:
    values = results["iGovTI"].astype(float).to_numpy()
    bins = np.arange(0, 1.0001, 0.05)
    counts, edges = np.histogram(values, bins=bins)
    fig, ax = plt.subplots(figsize=(9, 5))
    for count, left, right in zip(counts, edges[:-1], edges[1:]):
        center = (left + right) / 2
        color = LEVEL_COLORS[maturity(center)]
        ax.bar(center, count, width=(right - left) * 0.92, color=color, edgecolor="white")
        if count:
            ax.text(center, count + 0.35, f"{count}", ha="center", va="bottom", fontsize=8)
    ax.axvline(values.mean(), color="#111827", linestyle="--", linewidth=1.2, label=f"Média: {values.mean():.3f}")
    ax.axvline(np.median(values), color="#3B6EA8", linestyle=":", linewidth=1.5, label=f"Mediana: {np.median(values):.3f}")
    ax.set_xlim(0, 1)
    ax.set_xlabel("iGovTI 2026")
    ax.set_ylabel("Número de organizações")
    statistic_handles, _ = ax.get_legend_handles_labels()
    maturity_legend(ax, extra_handles=statistic_handles)
    clean_axis(ax)
    save_shared(fig, "igovti_2026_distribuicao_continua.png")


def plot_component_distribution(results: pd.DataFrame) -> None:
    series = [results[key].astype(float).to_numpy() for key in COMPONENTS]
    positions = np.arange(1, len(series) + 1)
    colors = ["#3B6EA8", "#D59A2F", "#167D8D"]
    fig, ax = plt.subplots(figsize=(9.2, 6.2))
    box = ax.boxplot(series, positions=positions, widths=0.48, patch_artist=True, showfliers=False,
                     medianprops={"color": "#111827", "linewidth": 1.8})
    for patch, color in zip(box["boxes"], colors):
        patch.set_facecolor(color); patch.set_alpha(0.75)
    rng = np.random.default_rng(2026)
    for position, values, color in zip(positions, series, colors):
        ax.scatter(position + rng.normal(0, 0.055, len(values)), values, s=15, color=color, alpha=0.33, linewidth=0)
        ax.scatter(position, np.mean(values), marker="D", s=46, color="white", edgecolor="#111827", zorder=5)
    add_maturity_background(ax, orientation="horizontal", alpha=0.055)
    ax.set_xticks(positions, COMPONENTS.values())
    ax.set_ylim(0, 1)
    ax.set_ylabel("Resultado")
    maturity_legend(ax)
    clean_axis(ax)
    save_shared(fig, "igovti_2026_distribuicao_componentes.png")


def plot_governance_management(results: pd.DataFrame) -> None:
    x = results["GovernancaTI"].astype(float).to_numpy()
    y = results["iGestTI"].astype(float).to_numpy()
    colors = [LEVEL_COLORS[maturity(value)] for value in results["iGovTI"].astype(float)]
    fig, ax = plt.subplots(figsize=(8.2, 7.2))
    ax.scatter(x, y, c=colors, s=42, alpha=0.72, edgecolor="white", linewidth=0.45)
    ax.plot([0, 1], [0, 1], color="#4B5563", linestyle="--", linewidth=1, label="Governança = gestão")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("Governança de TIC"); ax.set_ylabel("Gestão de TIC")
    comparison_handles, _ = ax.get_legend_handles_labels()
    maturity_legend(ax, extra_handles=comparison_handles)
    clean_axis(ax, grid_axis="both")
    save_shared(fig, "igovti_2026_governanca_vs_gestao.png")


def plot_dimension_distribution(results: pd.DataFrame) -> None:
    keys = list(DIMENSIONS)
    values = [results[key].astype(float).to_numpy() for key in keys]
    positions = np.arange(1, len(values) + 1)
    fig, ax = plt.subplots(figsize=(10.5, 6.6))
    box = ax.boxplot(values, positions=positions, vert=False, widths=0.55, patch_artist=True, showfliers=False,
                     medianprops={"color": "#111827", "linewidth": 1.7})
    for patch, key in zip(box["boxes"], keys):
        color = LEVEL_COLORS[maturity(float(results[key].mean()))]
        patch.set_facecolor(color); patch.set_alpha(0.72)
    for position, key, series in zip(positions, keys, values):
        mean = float(np.mean(series))
        ax.scatter(mean, position, marker="D", s=45, color="white", edgecolor="#111827", zorder=5)
        ax.text(mean + 0.018, position + 0.19, f"média {mean:.3f}", fontsize=8)
    add_maturity_background(ax, alpha=0.055)
    ax.set_yticks(positions, DIMENSIONS.values()); ax.set_xlim(0, 1)
    ax.set_xlabel("Resultado")
    maturity_legend(ax)
    clean_axis(ax, grid_axis="x")
    save_shared(fig, "igovti_2026_distribuicao_dimensoes_gestao.png")


def plot_dimension_maturity(results: pd.DataFrame) -> None:
    counts = []
    for key in DIMENSIONS:
        classified = results[key].astype(float).map(maturity)
        counts.append([100 * (classified == level).mean() for level in LEVELS])
    fig, ax = plt.subplots(figsize=(11.2, 6.8))
    left = np.zeros(len(DIMENSIONS))
    y = np.arange(len(DIMENSIONS))
    for index, level in enumerate(LEVELS):
        values = np.array([row[index] for row in counts])
        bars = ax.barh(y, values, left=left, color=LEVEL_COLORS[level], label=level)
        for bar, value in zip(bars, values):
            if value >= 5:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height() / 2,
                        f"{value:.1f}%", ha="center", va="center", fontsize=8)
        left += values
    ax.set_yticks(y, DIMENSIONS.values()); ax.set_xlim(0, 100)
    ax.set_xlabel("Percentual de organizações")
    ax.legend(ncol=4, loc="upper center", bbox_to_anchor=(0.5, 1.12), frameon=False)
    clean_axis(ax, grid_axis="x")
    save_shared(fig, "igovti_2026_maturidade_dimensoes.png")


def plot_dimension_success(results: pd.DataFrame) -> None:
    values = []
    for key, label in DIMENSIONS.items():
        percentage = 100 * (results[key].astype(float) >= 0.40).mean()
        values.append((percentage, label))
    values.sort()
    fig, ax = plt.subplots(figsize=(9.6, 5.8))
    y = np.arange(len(values))
    percentages = [item[0] for item in values]
    colors = [LEVEL_COLORS[maturity(value / 100)] for value in percentages]
    ax.hlines(y, 0, percentages, color="#9CA3AF", linewidth=1.4)
    ax.scatter(percentages, y, s=120, color=colors, zorder=3)
    for pos, value in zip(y, percentages):
        ax.text(value + 1.5, pos, f"{value:.1f}%", va="center", fontweight="bold")
    ax.set_yticks(y, [item[1] for item in values]); ax.set_xlim(0, 100)
    ax.set_xlabel("Organizações nos níveis Intermediário ou Aprimorado")
    clean_axis(ax, grid_axis="x")
    save_shared(fig, "igovti_2026_dimensoes_intermediario_aprimorado.png")


def plot_dimension_heatmap(results: pd.DataFrame) -> None:
    keys = sorted(DIMENSIONS, key=lambda key: results[key].mean(), reverse=True)
    ordered = results.sort_values("iGovTI", ascending=False)
    matrix = ordered[keys].astype(float).to_numpy()
    cmap = LinearSegmentedColormap.from_list("maturity", [LEVEL_COLORS[level] for level in LEVELS], N=256)
    fig, ax = plt.subplots(figsize=(10.5, 8.2))
    image = ax.imshow(matrix, aspect="auto", cmap=cmap, vmin=0, vmax=1, interpolation="nearest")
    ax.set_xticks(range(len(keys)), [DIMENSIONS[key] for key in keys], rotation=30, ha="right")
    ax.set_yticks([]); ax.set_ylabel("Organizações ordenadas pelo iGovTI")
    colorbar = fig.colorbar(image, ax=ax, shrink=0.84)
    colorbar.set_ticks([0.075, 0.275, 0.55, 0.85], labels=LEVELS)
    colorbar.set_label("Nível de maturidade")
    save_shared(fig, "igovti_2026_mapa_calor_organizacoes_dimensoes.png")


def plot_correlation(results: pd.DataFrame) -> None:
    keys = list(DIMENSIONS)
    matrix = results[keys].astype(float).corr().to_numpy()
    fig, ax = plt.subplots(figsize=(9.2, 7.2))
    image = ax.imshow(matrix, cmap="RdYlGn", vmin=0.4, vmax=1.0)
    for row in range(len(keys)):
        for column in range(len(keys)):
            value = matrix[row, column]
            ax.text(column, row, f"{value:.2f}", ha="center", va="center",
                    color="white" if value >= 0.78 else "#111827", fontweight="bold")
    labels = list(DIMENSIONS.values())
    ax.set_xticks(range(len(keys)), labels, rotation=35, ha="right"); ax.set_yticks(range(len(keys)), labels)
    fig.colorbar(image, ax=ax, label="Correlação de Pearson", shrink=0.82)
    save_shared(fig, "igovti_2026_correlacao_dimensoes_gestao.png")


def plot_response_distribution(raw: pd.DataFrame) -> None:
    rows = []
    for question in BASE_QUESTIONS:
        counts = Counter(response_category(value) for value in raw[question] if response_category(value))
        total = sum(counts.values())
        rows.append([100 * counts.get(category, 0) / total if total else 0 for category in RESPONSE_ORDER])
    fig, ax = plt.subplots(figsize=(12.5, 9.2))
    left = np.zeros(len(BASE_QUESTIONS)); y = np.arange(len(BASE_QUESTIONS))
    for index, category in enumerate(RESPONSE_ORDER):
        values = np.array([row[index] for row in rows])
        ax.barh(y, values, left=left, color=RESPONSE_COLORS[category], label=category)
        left += values
    ax.set_yticks(y, BASE_QUESTIONS); ax.invert_yaxis(); ax.set_xlim(0, 100)
    ax.set_xlabel("Percentual de respostas")
    ax.legend(ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.10), frameon=False, fontsize=9)
    clean_axis(ax, grid_axis="x")
    save_shared(fig, "igovti_2026_distribuicao_respostas_questoes.png")


def plot_question_profile(profiles: pd.DataFrame) -> None:
    values = [profiles[key].mean() for key in QUESTION_LABELS]
    labels = list(QUESTION_LABELS.values())
    colors = [LEVEL_COLORS[maturity(float(value))] for value in values]
    fig, ax = plt.subplots(figsize=(10.5, 6.2))
    bars = ax.barh(labels, values, color=colors)
    ax.bar_label(bars, labels=[f"{value:.1%}" for value in values], padding=5, fontweight="bold")
    add_maturity_background(ax, alpha=0.05)
    ax.set_xlim(0, 1); ax.set_xlabel("Proporção média de verificações conformes")
    maturity_legend(ax)
    clean_axis(ax, grid_axis="x")
    save_shared(fig, "igovti_2026_perfil_questoes_auditoria.png")


def plot_comparable_distribution(pairs: list[dict[str, object]]) -> None:
    old = np.array([safe_float(pair["old"]["iGovTI"]) for pair in pairs])
    new = np.array([safe_float(pair["new"]["iGovTI"]) for pair in pairs])
    fig, ax = plt.subplots(figsize=(8.8, 5.8))
    for before, after in zip(old, new):
        ax.plot([1, 2], [before, after], color="#228B22" if after >= before else "#B22222", alpha=0.18, linewidth=0.9)
    box = ax.boxplot([old, new], positions=[1, 2], widths=0.42, patch_artist=True, showfliers=False,
                     medianprops={"color": "#111827", "linewidth": 1.8})
    box["boxes"][0].set(facecolor="#D59A2F", alpha=0.75); box["boxes"][1].set(facecolor="#167D8D", alpha=0.75)
    ax.set_xticks([1, 2], ["2023", "2026"]); ax.set_ylim(0, 1); ax.set_ylabel("iGovTI comparável")
    clean_axis(ax)
    save_shared(fig, "igovti_comparavel_distribuicao_2023_2026.png")


def plot_transition(pairs: list[dict[str, object]]) -> None:
    matrix = np.zeros((4, 4), dtype=int); index = {level: idx for idx, level in enumerate(LEVELS)}
    for pair in pairs:
        matrix[index[str(pair["old"]["nivel_maturidade"])]][index[str(pair["new"]["nivel_maturidade"])]] += 1
    fig, ax = plt.subplots(figsize=(9.2, 6.2))
    max_value = max(matrix.max(), 1)
    for row in range(4):
        for column in range(4):
            alpha = 0.12 + 0.78 * matrix[row, column] / max_value
            ax.add_patch(Rectangle((column - 0.5, row - 0.5), 1, 1,
                                   color=to_rgba(LEVEL_COLORS[LEVELS[column]], alpha)))
            ax.text(column, row, str(matrix[row, column]), ha="center", va="center", fontsize=14, fontweight="bold")
    ax.set_xlim(-0.5, 3.5); ax.set_ylim(3.5, -0.5)
    ax.set_xticks(range(4), LEVELS); ax.set_yticks(range(4), LEVELS)
    ax.set_xlabel("Nível em 2026"); ax.set_ylabel("Nível em 2023")
    save_shared(fig, "igovti_comparavel_transicao_maturidade_2023_2026.png")


def plot_aggregate_changes(pairs: list[dict[str, object]]) -> None:
    practices = {
        "ModeloTI": "Modelo de gestão", "MonitorAvaliaTI": "Monitoramento e avaliação",
        "ResultadoTI": "Resultados e simplificação", "PlanejamentoTI": "Planejamento",
        "PessoasTI": "Pessoas", "iGestServicosTI": "Serviços",
        "iGestNiveisServicoTI": "Níveis de serviço", "iGestRiscosTI": "Riscos",
        "EstruturaSegInfo": "Estrutura de segurança", "ProcessoSegInfo": "Processos de segurança",
        "ProcessoSoftware": "Processo de software", "iGestProjetosTI": "Projetos",
    }
    changes = []
    for key, label in practices.items():
        delta = np.mean([safe_float(pair["new"].get(key)) - safe_float(pair["old"].get(key)) for pair in pairs])
        changes.append((delta, label))
    changes.sort()
    fig, ax = plt.subplots(figsize=(10.2, 6.8))
    bars = ax.barh([label for _, label in changes], [value for value, _ in changes],
                   color=["#228B22" if value >= 0 else "#B22222" for value, _ in changes])
    ax.axvline(0, color="#111827", linewidth=0.9)
    ax.bar_label(bars, labels=[f"{value:+.3f}" for value, _ in changes], padding=4)
    ax.set_xlabel("Variação média (2026 - 2023)")
    clean_axis(ax, grid_axis="x")
    save_shared(fig, "igovti_comparavel_variacao_agregados_2023_2026.png")


def plot_largest_changes(pairs: list[dict[str, object]]) -> None:
    changes = sorted((safe_float(pair["new"]["iGovTI"]) - safe_float(pair["old"]["iGovTI"]), str(pair["new"]["id"])) for pair in pairs)
    selected = changes[:10] + changes[-10:]
    fig, ax = plt.subplots(figsize=(10.2, 8.6))
    bars = ax.barh([label for _, label in selected], [value for value, _ in selected],
                   color=["#228B22" if value >= 0 else "#B22222" for value, _ in selected])
    ax.axvline(0, color="#111827", linewidth=0.9)
    ax.bar_label(bars, labels=[f"{value:+.3f}" for value, _ in selected], padding=4)
    ax.set_xlabel("Variação do iGovTI comparável")
    clean_axis(ax, grid_axis="x")
    save_shared(fig, "igovti_comparavel_maiores_variacoes_2023_2026.png")


def plot_all_evolution(pairs: list[dict[str, object]]) -> None:
    ordered = sorted(pairs, key=lambda pair: safe_float(pair["new"]["iGovTI"]) - safe_float(pair["old"]["iGovTI"]))
    fig, ax = plt.subplots(figsize=(10.8, 7.4))
    for pair in ordered:
        old = safe_float(pair["old"]["iGovTI"]); new = safe_float(pair["new"]["iGovTI"])
        ax.plot([0, 1], [old, new], color="#228B22" if new >= old else "#B22222", alpha=0.38, linewidth=1.1)
    ax.scatter(np.zeros(len(ordered)), [safe_float(pair["old"]["iGovTI"]) for pair in ordered], color="#D59A2F", s=20)
    ax.scatter(np.ones(len(ordered)), [safe_float(pair["new"]["iGovTI"]) for pair in ordered], color="#167D8D", s=20)
    ax.set_xticks([0, 1], ["2023", "2026"]); ax.set_xlim(-0.15, 1.15); ax.set_ylim(0, 1)
    ax.set_ylabel("iGovTI comparável")
    clean_axis(ax)
    save_shared(fig, "igovti_comparavel_evolucao_organizacoes_2023_2026.png")


def plot_group_comparison(pairs: list[dict[str, object]]) -> None:
    groups = ["Estaduais", "Municípios"]
    deltas = [[safe_float(pair["new"]["iGovTI"]) - safe_float(pair["old"]["iGovTI"]) for pair in pairs if pair["grupo"] == group] for group in groups]
    fig, ax = plt.subplots(figsize=(8.8, 5.8))
    try:
        box = ax.boxplot(deltas, tick_labels=[f"{group}\n(n={len(values)})" for group, values in zip(groups, deltas)],
                         patch_artist=True, showfliers=False, medianprops={"color": "#111827", "linewidth": 1.7})
    except TypeError:
        box = ax.boxplot(deltas, labels=[f"{group}\n(n={len(values)})" for group, values in zip(groups, deltas)],
                         patch_artist=True, showfliers=False, medianprops={"color": "#111827", "linewidth": 1.7})
    for patch, color in zip(box["boxes"], ["#167D8D", "#D59A2F"]):
        patch.set_facecolor(color); patch.set_alpha(0.72)
    rng = np.random.default_rng(2026)
    for position, values, color in zip([1, 2], deltas, ["#167D8D", "#D59A2F"]):
        ax.scatter(position + rng.normal(0, 0.035, len(values)), values, color=color, alpha=0.68, s=28)
        ax.text(position, max(values) + 0.025, f"média {np.mean(values):+.3f}", ha="center", fontweight="bold")
    ax.axhline(0, color="#111827", linewidth=0.9)
    ax.set_ylabel("Variação do iGovTI comparável")
    clean_axis(ax)
    save_shared(fig, "igovti_comparavel_estaduais_municipios_2023_2026.png")


def plot_position_histogram(results: pd.DataFrame, record: pd.Series, key: str, filename: str, label: str) -> None:
    values = results[key].astype(float).to_numpy(); bins = np.arange(0, 1.0001, 0.05)
    counts, edges = np.histogram(values, bins=bins)
    fig, ax = plt.subplots(figsize=(9.6, 4.8))
    for count, left, right in zip(counts, edges[:-1], edges[1:]):
        center = (left + right) / 2
        ax.bar(center, count, width=(right - left) * 0.92, color=LEVEL_COLORS[maturity(center)], edgecolor="white")
    value = safe_float(record[key]); index = min(max(np.digitize(max(value - 1e-9, 0), bins) - 1, 0), len(counts) - 1)
    center = (edges[index] + edges[index + 1]) / 2
    ax.scatter(center, counts[index] + 0.5, color="#C1121F", marker="X", s=125, zorder=5, label=f"{record['sigla']}: {value:.3f}")
    ax.set_xlim(0, 1); ax.set_xlabel(label); ax.set_ylabel("Número de organizações")
    auditado_handles, _ = ax.get_legend_handles_labels()
    maturity_legend(ax, extra_handles=auditado_handles)
    clean_axis(ax)
    save(fig, individual_output(record["sigla"], filename))


def plot_individual_components(record: pd.Series) -> None:
    keys = list(COMPONENTS); values = [safe_float(record[key]) for key in keys]
    fig, ax = plt.subplots(figsize=(8.8, 5.2))
    bars = ax.bar(COMPONENTS.values(), values, color=[LEVEL_COLORS[maturity(value)] for value in values], width=0.62)
    ax.bar_label(bars, labels=[f"{value:.3f}" for value in values], padding=5, fontweight="bold")
    add_maturity_background(ax, orientation="horizontal", alpha=0.055)
    ax.set_ylim(0, 1); ax.set_ylabel("Resultado")
    maturity_legend(ax)
    clean_axis(ax)
    save(fig, individual_output(record["sigla"], f"{record['sigla']}_componentes_iGovTI.png"))


def plot_individual_radar(results: pd.DataFrame, record: pd.Series) -> None:
    keys = list(DIMENSIONS); labels = list(DIMENSIONS.values()); n = len(keys)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist(); angles += angles[:1]
    values = [safe_float(record[key]) for key in keys]; values += values[:1]
    medians = [float(results[key].median()) for key in keys]; medians += medians[:1]
    means = [float(results[key].mean()) for key in keys]; means += means[:1]
    fig, ax = plt.subplots(figsize=(8.4, 7.4), subplot_kw={"polar": True})
    ax.plot(angles, values, color="#167D8D", linewidth=2.2, label=str(record["sigla"])); ax.fill(angles, values, color="#167D8D", alpha=0.16)
    ax.plot(angles, medians, color="#B64B5A", linewidth=1.4, linestyle="--", label="Mediana geral")
    ax.plot(angles, means, color="#D59A2F", linewidth=1.4, linestyle=":", label="Média geral")
    ax.set_xticks(angles[:-1], labels); ax.set_ylim(0, 1); ax.set_yticks([0.15, 0.40, 0.70, 1.0])
    ax.set_yticklabels(["0,15", "0,40", "0,70", "1,00"], fontsize=8)
    ax.legend(loc="upper right", bbox_to_anchor=(1.28, 1.14), frameon=False)
    save(fig, individual_output(record["sigla"], f"{record['sigla']}_perfil_dimensoes_iGestTI.png"))


def plot_individual_bullets(results: pd.DataFrame, record: pd.Series) -> None:
    keys = list(DIMENSIONS); y = np.arange(len(keys)); values = [safe_float(record[key]) for key in keys]
    medians = [float(results[key].median()) for key in keys]
    fig, ax = plt.subplots(figsize=(10.2, 6.2))
    add_maturity_background(ax, alpha=0.10)
    ax.hlines(y, 0, values, color="#6B7280", linewidth=2)
    ax.scatter(values, y, color=[LEVEL_COLORS[maturity(value)] for value in values], s=115, label=str(record["sigla"]), zorder=4)
    ax.scatter(medians, y, color="#111827", marker="|", s=260, linewidths=2.2, label="Mediana geral", zorder=5)
    for position, value in zip(y, values): ax.text(value + 0.018, position, f"{value:.3f}", va="center", fontsize=9)
    ax.set_yticks(y, DIMENSIONS.values()); ax.set_xlim(0, 1); ax.set_xlabel("Resultado")
    ax.legend(ncol=2, loc="upper center", bbox_to_anchor=(0.5, 1.10), frameon=False)
    clean_axis(ax, grid_axis="x")
    save(fig, individual_output(record["sigla"], f"{record['sigla']}_comparacao_dimensoes_iGestTI.png"))


def plot_individual_percentiles(results: pd.DataFrame, record: pd.Series) -> None:
    keys = list(COMPONENTS) + list(DIMENSIONS); labels = list(COMPONENTS.values()) + list(DIMENSIONS.values())
    percentiles = [100 * (results[key].astype(float) <= safe_float(record[key])).mean() for key in keys]
    fig, ax = plt.subplots(figsize=(10.5, 6.8))
    bars = ax.barh(labels, percentiles, color=[LEVEL_COLORS[maturity(value / 100)] for value in percentiles])
    ax.bar_label(bars, labels=[f"P{value:.0f}" for value in percentiles], padding=4, fontweight="bold")
    ax.set_xlim(0, 100); ax.set_xlabel("Percentil no conjunto avaliado")
    clean_axis(ax, grid_axis="x")
    save(fig, individual_output(record["sigla"], f"{record['sigla']}_percentis_indicadores.png"))


def plot_individual_evolution(record: pd.Series, pair: dict[str, object] | None) -> None:
    if not pair:
        return
    fig, ax = plt.subplots(figsize=(8.8, 5.2))
    metrics = [("iGovTI", "iGovTI"), ("GovernancaTI", "Governança"), ("iGestTI", "Gestão")]
    for key, label in metrics:
        old = safe_float(pair["old"].get(key)); new = safe_float(pair["new"].get(key))
        ax.plot([0, 1], [old, new], marker="o", linewidth=2, label=f"{label}: {new-old:+.3f}")
    ax.set_xticks([0, 1], ["2023", "2026"]); ax.set_xlim(-0.12, 1.12); ax.set_ylim(0, 1)
    ax.set_ylabel("Resultado comparável"); ax.legend(frameon=False)
    clean_axis(ax)
    save(fig, individual_output(record["sigla"], f"{record['sigla']}_evolucao_igovti_2023_2026.png"))


def plot_workforce(raw_record: pd.Series, sigla: str) -> None:
    matrix = []
    for area in ["TI", "SI"]:
        matrix.append([safe_float(raw_record.get(f"q0105[{area}_{link}]")) for link in WORKFORCE_LINKS])
    fig, ax = plt.subplots(figsize=(9.6, 4.8))
    left = np.zeros(2); y = np.arange(2)
    for index, (label, color) in enumerate(zip(WORKFORCE_LABELS, WORKFORCE_COLORS)):
        values = np.array([matrix[0][index], matrix[1][index]])
        bars = ax.barh(y, values, left=left, color=color, label=label)
        for bar, value in zip(bars, values):
            if value > 0: ax.text(bar.get_x() + bar.get_width()/2, bar.get_y()+bar.get_height()/2, f"{int(value)}", ha="center", va="center", fontsize=8)
        left += values
    ax.set_yticks(y, ["Tecnologia da informação", "Segurança da informação"])
    ax.set_xlabel("Número de profissionais")
    ax.legend(ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.18), frameon=False, fontsize=8)
    clean_axis(ax, grid_axis="x")
    save(fig, individual_output(sigla, f"{sigla}_forca_trabalho_tic_si.png"))


def base_question_score(value: object, category_scores: dict[str, float]) -> float:
    text = clean_response(value)
    return category_scores.get(text, category_scores.get(str(value), np.nan))


def generate_consolidated(results: pd.DataFrame, raw: pd.DataFrame, profiles: pd.DataFrame, pairs: list[dict[str, object]]) -> None:
    plot_maturity_distribution(results)
    plot_continuous_distribution(results)
    plot_component_distribution(results)
    plot_governance_management(results)
    plot_dimension_distribution(results)
    plot_dimension_maturity(results)
    plot_dimension_success(results)
    plot_dimension_heatmap(results)
    plot_correlation(results)
    plot_response_distribution(raw)
    plot_question_profile(profiles)
    plot_comparable_distribution(pairs)
    plot_transition(pairs)
    plot_aggregate_changes(pairs)
    plot_largest_changes(pairs)
    plot_all_evolution(pairs)
    plot_group_comparison(pairs)


def select_audited(results: pd.DataFrame, requested: list[str] | None) -> pd.DataFrame:
    if not requested:
        return results

    by_key = {normalize_id(sigla): index for index, sigla in results["sigla"].items()}
    unknown = [value for value in requested if normalize_id(value) not in by_key]
    if unknown:
        available = ", ".join(results["sigla"].astype(str).sort_values())
        raise ValueError(f"Auditado(s) não encontrado(s): {', '.join(unknown)}. Disponíveis: {available}")

    selected_indices = list(dict.fromkeys(by_key[normalize_id(value)] for value in requested))
    return results.loc[selected_indices]


def _generate_one_individual(results: pd.DataFrame, raw_by_key: pd.DataFrame,
                             pairs_by_key: dict[str, dict[str, object]],
                             record: pd.Series) -> tuple[str, int]:
    sigla = str(record["sigla"])
    key = str(record["_key"])
    raw_record = raw_by_key.loc[key]
    plot_position_histogram(results, record, "iGovTI", f"{sigla}_comparativo_distribuicao_iGovTI.png", "iGovTI 2026")
    plot_position_histogram(results, record, "GovernancaTI", f"{sigla}_comparativo_distribuicao_GovernancaTI.png", "Governança de TIC")
    plot_position_histogram(results, record, "iGestTI", f"{sigla}_comparativo_distribuicao_iGestTI.png", "Gestão de TIC")
    plot_individual_components(record)
    plot_individual_radar(results, record)
    plot_individual_bullets(results, record)
    plot_individual_percentiles(results, record)
    pair = pairs_by_key.get(key)
    plot_individual_evolution(record, pair)
    plot_workforce(raw_record, sigla)
    quantidade = 9 if pair else 8
    return sigla, quantidade


def _init_individual_worker(results: pd.DataFrame, raw_by_key: pd.DataFrame,
                            pairs_by_key: dict[str, dict[str, object]],
                            individual_img: Path, dpi: int, skip_existing: bool) -> None:
    global WORKER_RESULTS, WORKER_RAW_BY_KEY, WORKER_PAIRS_BY_KEY, INDIVIDUAL_IMG, DPI, SKIP_EXISTING
    WORKER_RESULTS = results
    WORKER_RAW_BY_KEY = raw_by_key
    WORKER_PAIRS_BY_KEY = pairs_by_key
    INDIVIDUAL_IMG = individual_img
    DPI = dpi
    SKIP_EXISTING = skip_existing
    configure_style()


def _generate_one_individual_worker(record_dict: dict[str, object]) -> tuple[str, int]:
    if WORKER_RESULTS is None or WORKER_RAW_BY_KEY is None or WORKER_PAIRS_BY_KEY is None:
        raise RuntimeError("Worker de gráficos individuais não foi inicializado.")
    return _generate_one_individual(
        WORKER_RESULTS,
        WORKER_RAW_BY_KEY,
        WORKER_PAIRS_BY_KEY,
        pd.Series(record_dict),
    )


def generate_individual(results: pd.DataFrame, raw: pd.DataFrame, profiles: pd.DataFrame,
                        pairs: list[dict[str, object]], category_scores: dict[str, float],
                        requested: list[str] | None = None, jobs: int = 1) -> int:
    raw_by_key = raw.set_index("_key")
    pairs_by_key = {str(pair["key"]): pair for pair in pairs}
    records = select_audited(results, requested)
    total = len(records)
    if total == 0:
        return 0

    jobs = max(1, min(jobs, total))
    if jobs == 1:
        for index, (_, record) in enumerate(records.iterrows(), start=1):
            sigla, quantidade = _generate_one_individual(results, raw_by_key, pairs_by_key, record)
            print(f"[{index}/{total}] {sigla}: {quantidade} gráficos individuais")
        return total

    record_dicts = [record.to_dict() for _, record in records.iterrows()]
    with concurrent.futures.ProcessPoolExecutor(
        max_workers=jobs,
        initializer=_init_individual_worker,
        initargs=(results, raw_by_key, pairs_by_key, INDIVIDUAL_IMG, DPI, SKIP_EXISTING),
    ) as executor:
        futures = [executor.submit(_generate_one_individual_worker, record) for record in record_dicts]
        for index, future in enumerate(concurrent.futures.as_completed(futures), start=1):
            sigla, quantidade = future.result()
            print(f"[{index}/{total}] {sigla}: {quantidade} gráficos individuais")
    return len(records)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--somente-consolidados", action="store_true", help="Não gera gráficos por auditado")
    parser.add_argument("--somente-individuais", action="store_true", help="Não gera gráficos consolidados")
    parser.add_argument("--skip-existing", action="store_true", help="Pula PNG já existentes no diretório de saída")
    parser.add_argument(
        "--jobs",
        type=int,
        default=max(1, min(4, (os.cpu_count() or 2) - 1)),
        help="Quantidade de processos paralelos para gráficos individuais (padrão: até 4). Use 1 para execução sequencial.",
    )
    parser.add_argument("--dpi", type=int, default=DPI, help=f"Resolução dos PNG gerados (padrão: {DPI}).")
    parser.add_argument(
        "--auditados",
        nargs="+",
        metavar="SIGLA",
        help="Gera gráficos somente para os auditados informados. Se omitido, gera para todos.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
        help=f"Raiz dos artefatos gerados (padrão: {DEFAULT_OUTPUT_ROOT}).",
    )
    parser.add_argument("--resultados-2026", type=Path, default=RESULTS_FILE)
    parser.add_argument("--respostas-2026", type=Path, default=RAW_FILE)
    parser.add_argument("--comparavel-2026", type=Path, default=COMPARAVEL_2026)
    parser.add_argument("--setic-2023", type=Path, default=COMPARAVEL_2023_SETIC)
    parser.add_argument("--municipios-2023", type=Path, default=COMPARAVEL_2023_MUNICIPIOS)
    return parser.parse_args()


def main() -> None:
    global CONSOLIDATED_IMG, INDIVIDUAL_IMG, DPI, SKIP_EXISTING
    args = parse_args()
    if args.somente_consolidados and args.somente_individuais:
        raise ValueError("Use apenas uma das opções: --somente-consolidados ou --somente-individuais.")
    output_root = args.output_root.expanduser().resolve()
    CONSOLIDATED_IMG = output_root / "relatorio-consolidado/img"
    INDIVIDUAL_IMG = output_root / "relatorios-individuais/img"
    DPI = args.dpi
    SKIP_EXISTING = args.skip_existing
    configure_style()
    CONSOLIDATED_IMG.mkdir(parents=True, exist_ok=True)
    INDIVIDUAL_IMG.mkdir(parents=True, exist_ok=True)
    results, raw, category_scores = load_data(args.resultados_2026, args.respostas_2026)
    profiles = load_procedure_profiles(raw)
    pairs = load_pairs(args.comparavel_2026, args.setic_2023, args.municipios_2023)
    consolidated_count = 0
    if not args.somente_individuais:
        generate_consolidated(results, raw, profiles, pairs)
        consolidated_count = 17
    individual_count = 0
    if not args.somente_consolidados:
        individual_count = generate_individual(results, raw, profiles, pairs, category_scores, args.auditados, args.jobs)
    print(f"OK: {consolidated_count} gráficos consolidados e gráficos para {individual_count} organizações gerados em {DPI} dpi.")
    print(f"Gráficos consolidados: {CONSOLIDATED_IMG}")
    print(f"Gráficos individuais: {INDIVIDUAL_IMG}")


if __name__ == "__main__":
    main()
