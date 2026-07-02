#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Analisa a relação entre resultados iGovTI 2026 e achados de auditoria.

Gera, a partir dos artefatos atuais da execução:

* base cruzada e abas analíticas em XLSX;
* gráficos usados no relatório técnico;
* relatório Markdown em português com os principais achados estatísticos.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from textwrap import shorten

os.environ.setdefault("MPLCONFIGDIR", str(Path("/tmp") / "matplotlib"))

import matplotlib
import numpy as np
import pandas as pd
from scipy.stats import pearsonr, pointbiserialr, spearmanr

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

try:
    from scripts.resources.xlsx_utils import escrever_xlsx_se_diferente
except ImportError:  # execução direta do arquivo em scripts/
    from resources.xlsx_utils import escrever_xlsx_se_diferente


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IGOVTI = Path("/tmp/tcerj-igovti-2026/02-Execucao/01-Questionario/04-Resultados_iGovTI/20260621-iGovTI-2026.xlsx")
DEFAULT_RESULTADO = Path("/tmp/tcerj-igovti-2026/02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/resultado_auditoria.json")
DEFAULT_TABELAS = Path("/tmp/tcerj-igovti-2026/02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/tabelas_consolidadas_auditoria.xlsx")
DEFAULT_OUTPUT_DIR = ROOT / "03-Relatorios/99-Avaliacao_IgovTi_Achados"


INDICADORES_PADRAO = [
    "iGovTI",
    "iGestTI",
    "GovernancaTI",
    "PlanejamentoTI",
    "ServicosTI",
    "RiscosTISegInfo",
    "EstruturaSegInfo",
    "ProcessoSegInfo",
    "GerirSoluçõesTI",
    "_q4251ext[A](TCU)",
    "_q4251(TCU)",
]


def normalizar_auditado(valor: object) -> str:
    return str(valor or "").strip().upper()


def ler_tabela_marcada(path: Path, sheet_name: str) -> tuple[pd.DataFrame, list[str]]:
    df = pd.read_excel(path, sheet_name=sheet_name, keep_default_na=False)
    if "Auditado" not in df.columns:
        raise ValueError(f"A aba {sheet_name!r} não contém a coluna 'Auditado'.")
    df["Auditado"] = df["Auditado"].map(normalizar_auditado)
    colunas = [c for c in df.columns if c != "Auditado"]
    for coluna in colunas:
        df[coluna] = df[coluna].astype(str).str.strip().str.upper().eq("X").astype(int)
    return df, colunas


def nome_achado(coluna: str) -> str:
    match = re.match(r"^(\d+)\.\s*(.*)", coluna)
    if not match:
        return coluna
    return f"Achado {match.group(1)} - {match.group(2)}"


def numero_achado(coluna: str) -> str:
    match = re.match(r"^(\d+)\.", coluna)
    return match.group(1) if match else ""


def nome_situacao(coluna: str) -> tuple[str, str]:
    match = re.search(r"\[ACHADO\s*(\d+)\]\s*(.*)", coluna)
    if not match:
        return "", coluna
    return f"Achado {match.group(1)}", match.group(2)


def fmt_num(valor: object, casas: int = 3) -> str:
    if valor is None:
        return ""
    try:
        if pd.isna(valor):
            return ""
    except TypeError:
        pass
    return f"{float(valor):.{casas}f}"


def fmt_p(valor: object) -> str:
    if valor is None:
        return ""
    try:
        if pd.isna(valor):
            return ""
    except TypeError:
        pass
    p_valor = float(valor)
    if p_valor < 0.0001:
        return "< 0.0001"
    return f"{p_valor:.4f}"


def fmt_pct(valor: object, casas: int = 1) -> str:
    if valor is None:
        return ""
    try:
        if pd.isna(valor):
            return ""
    except TypeError:
        pass
    return f"{float(valor) * 100:.{casas}f}%"


def markdown_table(df: pd.DataFrame, columns: list[str], headers: list[str] | None = None, formats: dict[str, str] | None = None) -> str:
    formats = formats or {}
    headers = headers or columns
    linhas = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for _, row in df.iterrows():
        valores = []
        for coluna in columns:
            valor = row[coluna]
            formato = formats.get(coluna)
            if formato == "num3":
                valores.append(fmt_num(valor, 3))
            elif formato == "num2":
                valores.append(fmt_num(valor, 2))
            elif formato == "p":
                valores.append(fmt_p(valor))
            elif formato == "pct":
                valores.append(fmt_pct(valor))
            else:
                valores.append(str(valor))
        linhas.append("| " + " | ".join(valores) + " |")
    return "\n".join(linhas)


def carregar_base(igovti_xlsx: Path, tabelas_xlsx: Path, resultado_json: Path) -> dict[str, object]:
    igovti = pd.read_excel(igovti_xlsx, sheet_name="resultados")
    igovti["Auditado"] = igovti["id"].map(normalizar_auditado)

    achados, achado_cols = ler_tabela_marcada(tabelas_xlsx, "Achados por Auditado")
    situacoes, situacao_cols = ler_tabela_marcada(tabelas_xlsx, "Situações Inconformes")
    encaminhamentos, encaminhamento_cols = ler_tabela_marcada(tabelas_xlsx, "Encaminhamentos por Auditado")

    achados["qtd_achados"] = achados[achado_cols].sum(axis=1)
    situacoes["qtd_situacoes"] = situacoes[situacao_cols].sum(axis=1)
    encaminhamentos["qtd_encaminhamentos"] = encaminhamentos[encaminhamento_cols].sum(axis=1)

    base = igovti.merge(achados[["Auditado", "qtd_achados", *achado_cols]], on="Auditado", how="inner")
    base = base.merge(situacoes[["Auditado", "qtd_situacoes", *situacao_cols]], on="Auditado", how="inner")
    base = base.merge(encaminhamentos[["Auditado", "qtd_encaminhamentos"]], on="Auditado", how="left")

    with resultado_json.open(encoding="utf-8") as file:
        resultado = json.load(file)
    json_counts = []
    for sigla, registro in resultado.items():
        procedimentos = registro.get("procedimentos_executados", [])
        json_counts.append(
            {
                "Auditado": normalizar_auditado(sigla),
                "qtd_achados_json": sum(1 for proc in procedimentos if proc.get("achado_ocorreu") or proc.get("achado")),
            }
        )
    json_counts_df = pd.DataFrame(json_counts)
    base = base.merge(json_counts_df, on="Auditado", how="left")

    return {
        "base": base,
        "achado_cols": achado_cols,
        "situacao_cols": situacao_cols,
        "encaminhamento_cols": encaminhamento_cols,
    }


def calcular_analises(base: pd.DataFrame, achado_cols: list[str], situacao_cols: list[str]) -> dict[str, pd.DataFrame | dict[str, object]]:
    indicadores = [col for col in INDICADORES_PADRAO if col in base.columns]

    correlacoes = []
    for alvo in ["qtd_achados", "qtd_situacoes"]:
        for indicador in indicadores:
            x = pd.to_numeric(base[indicador], errors="coerce")
            y = pd.to_numeric(base[alvo], errors="coerce")
            mask = x.notna() & y.notna()
            if mask.sum() < 3:
                continue
            spearman = spearmanr(x[mask], y[mask])
            pearson = pearsonr(x[mask], y[mask])
            correlacoes.append(
                {
                    "alvo": alvo,
                    "indicador": indicador,
                    "spearman_r": spearman.statistic,
                    "spearman_p": spearman.pvalue,
                    "pearson_r": pearson.statistic,
                    "pearson_p": pearson.pvalue,
                    "n": int(mask.sum()),
                }
            )
    correlacoes_df = pd.DataFrame(correlacoes)

    recortes = [
        ("Todos", base),
        ("iGovTI > 0", base[base["iGovTI"] > 0]),
        ("iGovTI >= 0,10", base[base["iGovTI"] >= 0.10]),
        ("Sem Q1 de iGovTI", base[base["iGovTI"] > base["iGovTI"].quantile(0.25)]),
        ("iGovTI >= mediana", base[base["iGovTI"] >= base["iGovTI"].median()]),
    ]
    sensibilidade = []
    for nome, dados in recortes:
        linha = {"recorte": nome, "n": len(dados)}
        for alvo in ["qtd_achados", "qtd_situacoes"]:
            if len(dados) < 3:
                linha[f"spearman_{alvo}"] = np.nan
                linha[f"p_{alvo}"] = np.nan
            else:
                resultado = spearmanr(dados["iGovTI"], dados[alvo])
                linha[f"spearman_{alvo}"] = resultado.statistic
                linha[f"p_{alvo}"] = resultado.pvalue
        sensibilidade.append(linha)
    sensibilidade_df = pd.DataFrame(sensibilidade)

    quartis_base = base.copy()
    quartis_base["quartil"] = pd.qcut(
        quartis_base["iGovTI"],
        4,
        labels=["Q1 menor iGovTI", "Q2", "Q3", "Q4 maior iGovTI"],
        duplicates="drop",
    )
    quartis = (
        quartis_base.groupby("quartil", observed=True)
        .agg(
            organizacoes=("Auditado", "count"),
            min_igov=("iGovTI", "min"),
            max_igov=("iGovTI", "max"),
            media_igov=("iGovTI", "mean"),
            media_achados=("qtd_achados", "mean"),
            media_situacoes=("qtd_situacoes", "mean"),
            mediana_situacoes=("qtd_situacoes", "median"),
            pct_5_6=("qtd_achados", lambda s: (s >= 5).mean()),
            pct_ate_3=("qtd_achados", lambda s: (s <= 3).mean()),
        )
        .reset_index()
    )

    maturidade = (
        base.groupby("nivel_maturidade")
        .agg(
            organizacoes=("Auditado", "count"),
            media_igov=("iGovTI", "mean"),
            min_igov=("iGovTI", "min"),
            max_igov=("iGovTI", "max"),
            media_achados=("qtd_achados", "mean"),
            media_situacoes=("qtd_situacoes", "mean"),
            pct_6_achados=("qtd_achados", lambda s: (s == 6).mean()),
            pct_5_6=("qtd_achados", lambda s: (s >= 5).mean()),
        )
        .reset_index()
        .sort_values("media_igov")
    )

    achados = []
    for coluna in achado_cols:
        flag = base[coluna]
        n_com = int(flag.sum())
        n_sem = int((1 - flag).sum())
        if flag.nunique() > 1:
            pb = pointbiserialr(flag, base["iGovTI"])
            r_pb, p_val = pb.statistic, pb.pvalue
        else:
            r_pb, p_val = np.nan, np.nan
        achados.append(
            {
                "achado": nome_achado(coluna),
                "coluna": coluna,
                "n_com": n_com,
                "n_sem": n_sem,
                "pct": n_com / len(base),
                "media_igov_com": base.loc[flag == 1, "iGovTI"].mean(),
                "media_igov_sem": base.loc[flag == 0, "iGovTI"].mean(),
                "diferenca_sem_menos_com": base.loc[flag == 0, "iGovTI"].mean() - base.loc[flag == 1, "iGovTI"].mean(),
                "r_ponto_bisserial": r_pb,
                "p_valor": p_val,
            }
        )
    achados_df = pd.DataFrame(achados)

    situacoes = []
    for coluna in situacao_cols:
        achado, situacao = nome_situacao(coluna)
        n = int(base[coluna].sum())
        situacoes.append({"achado": achado, "situacao": situacao, "n": n, "pct": n / len(base), "coluna": coluna})
    situacoes_df = pd.DataFrame(situacoes).sort_values(["n", "situacao"], ascending=[False, True])

    coocorrencias = []
    for indice, col_a in enumerate(achado_cols):
        for col_b in achado_cols[indice + 1 :]:
            total = int(((base[col_a] == 1) & (base[col_b] == 1)).sum())
            coocorrencias.append(
                {
                    "par": f"Achados {numero_achado(col_a)} + {numero_achado(col_b)}",
                    "n": total,
                    "pct": total / len(base),
                    "achado_a": nome_achado(col_a),
                    "achado_b": nome_achado(col_b),
                }
            )
    coocorrencias_df = pd.DataFrame(coocorrencias).sort_values("n", ascending=False)

    coef = np.polyfit(base["iGovTI"], base["qtd_achados"], 1)
    base = base.copy()
    base["achados_esperados"] = coef[0] * base["iGovTI"] + coef[1]
    base["diferenca_achados"] = base["qtd_achados"] - base["achados_esperados"]
    mais_que_esperado = base.sort_values("diferenca_achados", ascending=False).head(12)
    menos_que_esperado = base.sort_values("diferenca_achados", ascending=True).head(12)

    resumo = {
        "n": len(base),
        "igov_media": base["iGovTI"].mean(),
        "igov_mediana": base["iGovTI"].median(),
        "igov_min": base["iGovTI"].min(),
        "igov_max": base["iGovTI"].max(),
        "achados_media": base["qtd_achados"].mean(),
        "achados_mediana": base["qtd_achados"].median(),
        "situacoes_media": base["qtd_situacoes"].mean(),
        "situacoes_mediana": base["qtd_situacoes"].median(),
        "situacoes_total": int(base["qtd_situacoes"].sum()),
        "marcacoes_achados_total": int(base["qtd_achados"].sum()),
        "encaminhamentos_total": int(base["qtd_encaminhamentos"].sum()),
        "n_4_mais": int((base["qtd_achados"] >= 4).sum()),
        "pct_4_mais": (base["qtd_achados"] >= 4).mean(),
        "n_5_6": int((base["qtd_achados"] >= 5).sum()),
        "pct_5_6": (base["qtd_achados"] >= 5).mean(),
        "n_6": int((base["qtd_achados"] == 6).sum()),
        "pct_6": (base["qtd_achados"] == 6).mean(),
        "json_mismatches": int((base["qtd_achados"] != base["qtd_achados_json"]).sum()) if "qtd_achados_json" in base.columns else 0,
    }

    return {
        "base": base,
        "correlacoes": correlacoes_df,
        "sensibilidade": sensibilidade_df,
        "quartis": quartis,
        "maturidade": maturidade,
        "achados": achados_df,
        "situacoes": situacoes_df,
        "coocorrencias": coocorrencias_df,
        "mais_que_esperado": mais_que_esperado,
        "menos_que_esperado": menos_que_esperado,
        "resumo": resumo,
        "indicadores": indicadores,
    }


def gerar_planilha(analises: dict[str, object], destino: Path) -> None:
    abas = {
        "base_cruzada": analises["base"],
        "correlacoes": analises["correlacoes"],
        "sensibilidade": analises["sensibilidade"],
        "quartis_igovti": analises["quartis"],
        "maturidade": analises["maturidade"],
        "achados": analises["achados"],
        "situacoes": analises["situacoes"],
        "coocorrencias": analises["coocorrencias"],
        "mais_achados_esperado": analises["mais_que_esperado"],
        "menos_achados_esperado": analises["menos_que_esperado"],
    }

    def _writer(temp_path: Path) -> None:
        with pd.ExcelWriter(temp_path, engine="openpyxl") as writer:
            for nome, df in abas.items():
                df.to_excel(writer, index=False, sheet_name=nome)

    escrever_xlsx_se_diferente(destino, _writer)


def gerar_graficos(analises: dict[str, object], img_dir: Path) -> None:
    img_dir.mkdir(parents=True, exist_ok=True)
    base: pd.DataFrame = analises["base"]  # type: ignore[assignment]
    quartis: pd.DataFrame = analises["quartis"]  # type: ignore[assignment]
    situacoes: pd.DataFrame = analises["situacoes"]  # type: ignore[assignment]
    indicadores: list[str] = analises["indicadores"]  # type: ignore[assignment]

    plt.style.use("seaborn-v0_8-whitegrid")

    fig, ax = plt.subplots(figsize=(8, 5), dpi=180)
    scatter = ax.scatter(
        base["iGovTI"],
        base["qtd_situacoes"],
        c=base["qtd_achados"],
        cmap="viridis",
        s=44,
        alpha=0.85,
        edgecolors="white",
        linewidth=0.4,
    )
    ax.set_xlabel("iGovTI 2026")
    ax.set_ylabel("Quantidade de situações inconformes")
    ax.set_title("Relação entre iGovTI, situações inconformes e achados")
    colorbar = fig.colorbar(scatter, ax=ax)
    colorbar.set_label("Achados distintos")
    fig.tight_layout()
    fig.savefig(img_dir / "achados_vs_igovti_2026.png")
    plt.close(fig)

    cols = ["qtd_achados", "qtd_situacoes", *indicadores]
    corr = base[cols].corr(method="spearman")
    fig, ax = plt.subplots(figsize=(9, 7), dpi=180)
    image = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(cols)))
    ax.set_yticks(range(len(cols)))
    ax.set_xticklabels(cols, rotation=45, ha="right", fontsize=7)
    ax.set_yticklabels(cols, fontsize=7)
    for i in range(len(cols)):
        for j in range(len(cols)):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=6)
    ax.set_title("Matriz de correlação Spearman")
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(img_dir / "correlacao_achados_notas_igovti_2026.png")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5), dpi=180)
    x = np.arange(len(quartis))
    width = 0.35
    ax.bar(x - width / 2, quartis["media_achados"], width, label="Achados distintos médios", color="#4C78A8")
    ax.bar(x + width / 2, quartis["media_situacoes"], width, label="Situações inconformes médias", color="#F58518")
    ax.set_xticks(x)
    ax.set_xticklabels(quartis["quartil"], rotation=15, ha="right")
    ax.set_ylabel("Média")
    ax.set_title("Achados e situações inconformes por quartil de iGovTI")
    ax.legend()
    fig.tight_layout()
    fig.savefig(img_dir / "achados_por_quartil_igovti_2026.png")
    plt.close(fig)

    top = situacoes.head(12).iloc[::-1]
    fig, ax = plt.subplots(figsize=(8.5, 6.5), dpi=180)
    ax.barh(top["situacao"].map(lambda texto: "\n".join(re.findall(r".{1,62}(?:\s+|$)", texto))), top["n"], color="#54A24B")
    ax.set_xlabel("Organizações com a situação")
    ax.set_title("Situações inconformes mais frequentes")
    fig.tight_layout()
    fig.savefig(img_dir / "situacoes_mais_frequentes_igovti_2026.png")
    plt.close(fig)


def tabela_correlacoes(correlacoes: pd.DataFrame, alvo: str, top: int = 6) -> str:
    dados = (
        correlacoes[correlacoes["alvo"] == alvo]
        .assign(abs_spearman=lambda df: df["spearman_r"].abs())
        .sort_values("abs_spearman", ascending=False)
        .head(top)
    )
    return markdown_table(
        dados,
        ["indicador", "spearman_r", "spearman_p", "pearson_r", "pearson_p", "n"],
        ["Indicador", "Spearman r", "p Spearman", "Pearson r", "p Pearson", "n"],
        {"spearman_r": "num3", "spearman_p": "p", "pearson_r": "num3", "pearson_p": "p"},
    )


def tabela_sensibilidade(sensibilidade: pd.DataFrame) -> str:
    dados = sensibilidade.rename(
        columns={
            "spearman_qtd_achados": "rho_achados",
            "p_qtd_achados": "p_achados",
            "spearman_qtd_situacoes": "rho_situacoes",
            "p_qtd_situacoes": "p_situacoes",
        }
    )
    return markdown_table(
        dados,
        ["recorte", "n", "rho_achados", "p_achados", "rho_situacoes", "p_situacoes"],
        ["Recorte", "n", "Spearman iGovTI x achados", "p achados", "Spearman iGovTI x situações", "p situações"],
        {"rho_achados": "num3", "p_achados": "p", "rho_situacoes": "num3", "p_situacoes": "p"},
    )


def tabela_quartis(quartis: pd.DataFrame) -> str:
    return markdown_table(
        quartis,
        ["quartil", "organizacoes", "min_igov", "max_igov", "media_igov", "media_achados", "media_situacoes", "pct_5_6", "pct_ate_3"],
        ["Quartil iGovTI", "Organizações", "Mín. iGovTI", "Máx. iGovTI", "Média iGovTI", "Média de achados", "Média de situações", "% com 5 ou 6 achados", "% com até 3 achados"],
        {
            "min_igov": "num3",
            "max_igov": "num3",
            "media_igov": "num3",
            "media_achados": "num3",
            "media_situacoes": "num3",
            "pct_5_6": "pct",
            "pct_ate_3": "pct",
        },
    )


def tabela_maturidade(maturidade: pd.DataFrame) -> str:
    return markdown_table(
        maturidade,
        ["nivel_maturidade", "organizacoes", "media_igov", "media_achados", "media_situacoes", "pct_6_achados", "pct_5_6"],
        ["Nível de maturidade", "Organizações", "Média iGovTI", "Média de achados", "Média de situações", "% com 6 achados", "% com 5 ou 6 achados"],
        {
            "media_igov": "num3",
            "media_achados": "num3",
            "media_situacoes": "num3",
            "pct_6_achados": "pct",
            "pct_5_6": "pct",
        },
    )


def tabela_achados(achados: pd.DataFrame) -> str:
    dados = achados.copy()
    dados["achado"] = dados["achado"].map(lambda texto: shorten(texto, width=92, placeholder="..."))
    return markdown_table(
        dados,
        ["achado", "n_com", "n_sem", "pct", "media_igov_com", "media_igov_sem", "diferenca_sem_menos_com", "r_ponto_bisserial", "p_valor"],
        ["Achado", "n com achado", "n sem achado", "%", "Média iGovTI com", "Média iGovTI sem", "Diferença sem - com", "r ponto-bisserial", "p-valor"],
        {
            "pct": "pct",
            "media_igov_com": "num3",
            "media_igov_sem": "num3",
            "diferenca_sem_menos_com": "num3",
            "r_ponto_bisserial": "num3",
            "p_valor": "p",
        },
    )


def tabela_situacoes(situacoes: pd.DataFrame, top: int = 12) -> str:
    dados = situacoes.head(top).copy()
    dados["situacao"] = dados["situacao"].map(lambda texto: shorten(texto, width=110, placeholder="..."))
    return markdown_table(
        dados,
        ["achado", "situacao", "n", "pct"],
        ["Achado", "Situação inconforme", "n", "%"],
        {"pct": "pct"},
    )


def tabela_casos(casos: pd.DataFrame) -> str:
    dados = casos[["Auditado", "iGovTI", "nivel_maturidade", "qtd_achados", "qtd_situacoes", "achados_esperados", "diferenca_achados"]].copy()
    return markdown_table(
        dados,
        ["Auditado", "iGovTI", "nivel_maturidade", "qtd_achados", "qtd_situacoes", "achados_esperados", "diferenca_achados"],
        ["Auditado", "iGovTI", "Maturidade", "Achados", "Situações", "Achados esperados", "Diferença"],
        {"iGovTI": "num3", "achados_esperados": "num2", "diferenca_achados": "num2"},
    )


def gerar_markdown(analises: dict[str, object], caminhos: dict[str, Path], destino: Path) -> None:
    base: pd.DataFrame = analises["base"]  # type: ignore[assignment]
    correlacoes: pd.DataFrame = analises["correlacoes"]  # type: ignore[assignment]
    sensibilidade: pd.DataFrame = analises["sensibilidade"]  # type: ignore[assignment]
    quartis: pd.DataFrame = analises["quartis"]  # type: ignore[assignment]
    maturidade: pd.DataFrame = analises["maturidade"]  # type: ignore[assignment]
    achados: pd.DataFrame = analises["achados"]  # type: ignore[assignment]
    situacoes: pd.DataFrame = analises["situacoes"]  # type: ignore[assignment]
    coocorrencias: pd.DataFrame = analises["coocorrencias"]  # type: ignore[assignment]
    mais: pd.DataFrame = analises["mais_que_esperado"]  # type: ignore[assignment]
    menos: pd.DataFrame = analises["menos_que_esperado"]  # type: ignore[assignment]
    resumo: dict[str, object] = analises["resumo"]  # type: ignore[assignment]

    corr_igov_achados = correlacoes[(correlacoes["alvo"] == "qtd_achados") & (correlacoes["indicador"] == "iGovTI")].iloc[0]
    corr_igov_situacoes = correlacoes[(correlacoes["alvo"] == "qtd_situacoes") & (correlacoes["indicador"] == "iGovTI")].iloc[0]
    corr_gest_situacoes = correlacoes[(correlacoes["alvo"] == "qtd_situacoes") & (correlacoes["indicador"] == "iGestTI")].iloc[0]
    top_sit = situacoes.iloc[0]
    top_co = coocorrencias.head(3)
    achado_mais = achados.sort_values("pct", ascending=False).iloc[0]
    achado_menos = achados.sort_values("pct", ascending=True).iloc[0]

    texto = f"""# Relatório técnico - relação entre achados de auditoria e notas do iGovTI 2026

## 1. Objetivo

Este relatório examina a relação entre os achados de auditoria registrados na execução dos procedimentos e as notas do iGovTI 2026 das organizações avaliadas. A análise foi atualizada com os artefatos mais recentes gerados em `/tmp/tcerj-igovti-2026`, contemplando resultados do índice, resultado estruturado da auditoria e tabelas consolidadas de achados, situações inconformes e encaminhamentos.

## 2. Fontes e método

Foram cruzadas três fontes: `{caminhos['igovti']}`, aba `resultados`; `{caminhos['resultado']}`; e `{caminhos['tabelas']}`, abas `Achados por Auditado`, `Situações Inconformes`, `Encaminhamentos por Auditado` e `Ranking de Auditados`.

A unidade de análise foi a organização auditada. Entraram no cruzamento **{resumo['n']} organizações** presentes simultaneamente nas bases. Para cada organização foram calculados a quantidade de achados distintos, a quantidade de situações inconformes, a quantidade de encaminhamentos associados, o iGovTI, o iGestTI, a nota de governança e os componentes do índice. Foram aplicadas correlações de Spearman e Pearson, comparação de médias por achado, análise de sensibilidade por recortes de iGovTI, prevalência das situações inconformes e identificação de casos divergentes em relação à tendência geral.

A correlação de Spearman foi priorizada porque a quantidade de achados é discreta e limitada a seis categorias. Essa limitação cria efeito de teto e exige cautela na interpretação. O arquivo JSON estruturado foi usado como conferência cruzada da contagem de achados; foram identificadas **{resumo['json_mismatches']} divergências** entre a contagem derivada das tabelas consolidadas e a contagem dos procedimentos no JSON.

## 3. Resultado executivo

O resultado central da análise é que **na base atualizada a correlação entre iGovTI e a carga de achados é negativa**. Considerando todas as organizações, a correlação de Spearman entre `iGovTI` e `qtd_achados` foi **{fmt_num(corr_igov_achados['spearman_r'])}** (p = **{fmt_p(corr_igov_achados['spearman_p'])}**) e entre `iGovTI` e `qtd_situacoes` foi **{fmt_num(corr_igov_situacoes['spearman_r'])}** (p = **{fmt_p(corr_igov_situacoes['spearman_p'])}**).

Essa evidência é coerente com a expectativa de auditoria: organizações com maior maturidade relativa tendem a apresentar menos achados e, principalmente, menos situações inconformes. A relação é mais forte quando se usa a quantidade de situações inconformes, porque a contagem de achados está quase saturada na amostra.

Em termos de controle externo, o principal insight é que **o iGovTI se relaciona com a carga de fragilidades, mas a quantidade de achados distintos perdeu poder discriminatório por efeito de teto**. A quantidade de situações inconformes é mais granular e informativa, pois diferencia organizações que materializam os mesmos achados em poucas ou muitas fragilidades concretas.

## 4. Visão geral da base

- iGovTI médio: **{fmt_num(resumo['igov_media'])}**; mediana: **{fmt_num(resumo['igov_mediana'])}**.
- Média de achados distintos: **{fmt_num(resumo['achados_media'])}**; mediana: **{fmt_num(resumo['achados_mediana'], 1)}**.
- Média de situações inconformes: **{fmt_num(resumo['situacoes_media'])}**; mediana: **{fmt_num(resumo['situacoes_mediana'], 1)}**.
- Marcações de achados por auditado: **{resumo['marcacoes_achados_total']}**.
- Situações inconformes registradas: **{resumo['situacoes_total']}**.
- Encaminhamentos associados nas tabelas consolidadas: **{resumo['encaminhamentos_total']}**.
- Organizações com 4 ou mais achados: **{resumo['n_4_mais']} de {resumo['n']}**, ou **{fmt_pct(resumo['pct_4_mais'])}**.
- Organizações com 5 ou 6 achados: **{resumo['n_5_6']} de {resumo['n']}**, ou **{fmt_pct(resumo['pct_5_6'])}**.
- Organizações com todos os 6 achados: **{resumo['n_6']} de {resumo['n']}**, ou **{fmt_pct(resumo['pct_6'])}**.

A alta concentração em 5 a 6 achados mostra forte efeito de teto. Nessa configuração, a simples contagem de achados distingue mal as organizações em situação crítica. A quantidade de situações inconformes recupera parte da granularidade, pois diferencia organizações que materializam os mesmos achados em poucas ou muitas fragilidades concretas.

## 5. Correlações principais

### 5.1. Quantidade de achados

{tabela_correlacoes(correlacoes, 'qtd_achados')}

### 5.2. Quantidade de situações inconformes

{tabela_correlacoes(correlacoes, 'qtd_situacoes')}

As correlações mais fortes com situações inconformes aparecem em `PlanejamentoTI`, `iGestTI` e `iGovTI`. Para situações inconformes, a associação com `iGestTI` chegou a **{fmt_num(corr_gest_situacoes['spearman_r'])}**. Esse resultado indica que a carga de fragilidades acompanha fortemente os componentes de gestão, planejamento e operação, e não apenas a governança formal. Na prática, organizações com melhor pontuação nesses componentes tendem a apresentar menos situações inconformes.

![Relação entre iGovTI 2026 e achados de auditoria](img/achados_vs_igovti_2026.png){{#fig:achados_vs_igovti_2026#}}
<div custom-style="FonteImagem">(Fonte: elaboração própria, com base nos artefatos de execução do iGovTI 2026)</div>

![Matriz de correlação entre achados e notas](img/correlacao_achados_notas_igovti_2026.png){{#fig:correlacao_achados_notas_igovti_2026#}}
<div custom-style="FonteImagem">(Fonte: elaboração própria, com base nos artefatos de execução do iGovTI 2026)</div>

## 6. Análise de sensibilidade

{tabela_sensibilidade(sensibilidade)}

A sensibilidade confirma a robustez da relação negativa. A associação permanece estatisticamente relevante na base completa, quando se excluem organizações com iGovTI igual a zero, quando se restringe a análise a iGovTI igual ou superior a 0,10 e quando se observa apenas a metade superior da distribuição. Ainda assim, a magnitude é maior e mais estável para situações inconformes do que para achados distintos, reforçando que **a quantidade de situações deve ser usada como medida principal de intensidade das fragilidades**.

## 7. Quartis e níveis de maturidade

### 7.1. Quartis de iGovTI

{tabela_quartis(quartis)}

![Achados e situações por quartil de iGovTI](img/achados_por_quartil_igovti_2026.png){{#fig:achados_por_quartil_igovti_2026#}}
<div custom-style="FonteImagem">(Fonte: elaboração própria, com base nos artefatos de execução do iGovTI 2026)</div>

O primeiro quartil concentra a maior média de situações inconformes e praticamente todos os auditados dos três primeiros quartis têm 5 ou 6 achados. O quarto quartil apresenta redução da média de achados e, sobretudo, da média de situações. Isso sugere que a maturidade medida pelo iGovTI está associada a menor intensidade de fragilidades, mas a saturação dos achados faz com que a melhora apareça de forma mais clara nas situações inconformes.

### 7.2. Níveis de maturidade declarados pelo iGovTI

{tabela_maturidade(maturidade)}

O recorte por nível de maturidade reforça que a distribuição de achados não segue uma relação linear simples. Mesmo nos níveis superiores da amostra, a média de achados permanece elevada, o que recomenda separar a comunicação do índice da comunicação dos achados. O índice informa maturidade relativa; os achados indicam descumprimentos, fragilidades ou lacunas verificadas nos critérios da fiscalização.

## 8. Achados e situações mais informativos

### 8.1. Prevalência dos achados

{tabela_achados(achados)}

O achado mais disseminado foi **{achado_mais['achado']}**, presente em **{int(achado_mais['n_com'])} organizações** (**{fmt_pct(achado_mais['pct'])}**). Mesmo o achado menos frequente, **{achado_menos['achado']}**, alcançou **{int(achado_menos['n_com'])} organizações** (**{fmt_pct(achado_menos['pct'])}**), o que demonstra amplitude sistêmica das fragilidades encontradas.

### 8.2. Situações inconformes mais frequentes

{tabela_situacoes(situacoes)}

![Situações inconformes mais frequentes](img/situacoes_mais_frequentes_igovti_2026.png){{#fig:situacoes_mais_frequentes_igovti_2026#}}
<div custom-style="FonteImagem">(Fonte: elaboração própria, com base nos artefatos de execução do iGovTI 2026)</div>

A situação inconforme mais frequente foi **\"{top_sit['situacao']}\"**, registrada em **{int(top_sit['n'])} organizações** (**{fmt_pct(top_sit['pct'])}**). Esse tipo de leitura é especialmente útil para o corpo deliberativo porque indica problemas transversais, cuja resposta pode exigir orientação normativa, indução de boas práticas, priorização de capacitação ou monitoramento em bloco, e não apenas recomendações atomizadas por jurisdicionado.

### 8.3. Coocorrência de achados

Os pares de achados com maior coocorrência foram:

{markdown_table(top_co, ['par', 'n', 'pct'], ['Par de achados', 'n', '%'], {'pct': 'pct'})}

A coocorrência elevada mostra que as fragilidades não aparecem isoladamente. Em especial, deficiências de capacidade institucional, gestão de serviços e contratações tendem a compor o mesmo quadro de baixa capacidade de sustentação da TIC. Para a fiscalização, isso sugere que recomendações pontuais podem ter menor efetividade se não forem acompanhadas de medidas estruturantes de governança, força de trabalho, planejamento e responsabilização.

## 9. Casos divergentes

### 9.1. Mais achados do que o esperado pela nota iGovTI

{tabela_casos(mais)}

### 9.2. Menos achados do que o esperado pela nota iGovTI

{tabela_casos(menos)}

Esses casos são úteis para revisão qualitativa. Organizações com muitos achados acima do esperado podem ter pontuação global que mascara fragilidades procedimentais relevantes. Organizações com poucos achados abaixo do esperado podem ter iGovTI muito baixo por ausência de práticas, mas menor número de categorias distintas de achados geradas pelas regras de execução. Nesses casos, a ausência relativa de achados não deve ser confundida com suficiência de controles.

## 10. Insights para controle externo

1. **O iGovTI é um sinalizador relevante de maturidade, mas não substitui a execução dos procedimentos.** A relação encontrada é negativa e estatisticamente relevante, sobretudo quando se observa a quantidade de situações inconformes.
2. **Há forte efeito de teto na quantidade de achados.** Como {fmt_pct(resumo['pct_4_mais'])} das organizações têm 4 ou mais achados e {fmt_pct(resumo['pct_5_6'])} têm 5 ou 6, a contagem de achados perde poder discriminatório. A quantidade de situações inconformes deve ser usada como medida complementar.
3. **O primeiro quartil de iGovTI deve ser tratado como grupo prioritário.** Ele concentra maturidade muito baixa e a maior média de situações inconformes.
4. **A melhoria de maturidade aparece mais claramente na redução de situações do que na redução de achados.** Como alguns achados atingem praticamente toda a amostra, a contagem de situações é mais adequada para priorização e monitoramento.
5. **As situações inconformes mais frequentes indicam problemas sistêmicos.** Quando uma mesma situação aparece em grande parte da amostra, a resposta de controle externo pode combinar recomendações individuais com orientação transversal aos jurisdicionados.
6. **Para seleção de fiscalizações futuras, recomenda-se combinar quatro variáveis:** iGovTI, quantidade de situações inconformes, natureza dos achados e divergência entre nota e achados esperados. Usar apenas a nota pode deixar de priorizar casos relevantes.
7. **Para comunicação do resultado, convém evitar reduzir a análise à nota do índice.** A evidência desta base aponta uma dinâmica mais completa: maior iGovTI está associado a menos fragilidades, mas a saturação dos achados exige olhar a quantidade e a natureza das situações inconformes.

## 11. Limitações

- A análise é transversal e não demonstra causalidade.
- A quantidade de achados é limitada a seis categorias, o que cria efeito de teto.
- Os achados derivam das regras e do escopo dos procedimentos desta fiscalização; portanto, a ausência de determinado achado não deve ser lida como ausência de risco fora do escopo.
- As avaliações de evidências e os artefatos de execução automatizada devem ser tratados como insumos sujeitos à revisão humana da equipe de auditoria.
- As correlações foram calculadas sobre os dados consolidados disponíveis; alterações posteriores nos ajustes de resposta, comentários do gestor ou reavaliações de evidência podem modificar os resultados.

## 12. Artefatos gerados

- Script reexecutável: `scripts/analisar_achados_igovti_2026.py`.
- Planilha de apoio: `03-Relatorios/99-Avaliacao_IgovTi_Achados/analise_achados_igovti_2026.xlsx`.
- Gráficos: `03-Relatorios/99-Avaliacao_IgovTi_Achados/img/achados_vs_igovti_2026.png`, `correlacao_achados_notas_igovti_2026.png`, `achados_por_quartil_igovti_2026.png` e `situacoes_mais_frequentes_igovti_2026.png`.
"""
    destino.write_text(texto, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--igovti-xlsx", type=Path, default=DEFAULT_IGOVTI, help="Planilha de resultados iGovTI 2026.")
    parser.add_argument("--resultado-auditoria-json", type=Path, default=DEFAULT_RESULTADO, help="Resultado estruturado da auditoria.")
    parser.add_argument("--tabelas-auditoria-xlsx", type=Path, default=DEFAULT_TABELAS, help="Tabelas consolidadas da auditoria.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Diretório de saída do relatório e artefatos.")
    parser.add_argument("--no-markdown", action="store_true", help="Não reescreve o relatório Markdown.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    for path in [args.igovti_xlsx, args.resultado_auditoria_json, args.tabelas_auditoria_xlsx]:
        if not path.exists():
            raise FileNotFoundError(path)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    dados = carregar_base(args.igovti_xlsx, args.tabelas_auditoria_xlsx, args.resultado_auditoria_json)
    analises = calcular_analises(dados["base"], dados["achado_cols"], dados["situacao_cols"])  # type: ignore[arg-type]

    xlsx_path = args.output_dir / "analise_achados_igovti_2026.xlsx"
    md_path = args.output_dir / "analise_achados_igovti_2026.md"
    img_dir = args.output_dir / "img"
    gerar_planilha(analises, xlsx_path)
    gerar_graficos(analises, img_dir)
    if not args.no_markdown:
        gerar_markdown(
            analises,
            {
                "igovti": args.igovti_xlsx,
                "resultado": args.resultado_auditoria_json,
                "tabelas": args.tabelas_auditoria_xlsx,
            },
            md_path,
        )

    resumo = analises["resumo"]
    print(f"OK: {resumo['n']} organizações analisadas.")
    print(f"Planilha: {xlsx_path}")
    print(f"Gráficos: {img_dir}")
    if not args.no_markdown:
        print(f"Relatório: {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
