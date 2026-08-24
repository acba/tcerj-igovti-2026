#!/usr/bin/env python3
"""Reconstrói a memória de cálculo do impacto da avaliação de evidências."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

import pandas as pd
from openpyxl.styles import Alignment, Font, PatternFill


ROOT = Path(__file__).resolve().parents[2]
INDICADORES = [
    "iGovTI", "GovernancaTI", "iGestTI", "PlanejamentoTI", "ServicosTI",
    "RiscosTISegInfo", "EstruturaSegInfo", "ProcessoSegInfo", "GerirSoluçõesTI",
]
NIVEIS = ["Inexpressivo", "Iniciando", "Intermediário", "Aprimorado"]


def normalizar(valor: object) -> str:
    texto = "" if pd.isna(valor) else str(valor)
    texto = "".join(
        c for c in unicodedata.normalize("NFKD", texto)
        if not unicodedata.combining(c)
    )
    return re.sub(r"\s+", "_", texto.casefold().strip())


def carregar_ajustes(path: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    df = pd.read_excel(path, sheet_name=0)
    revisor = df["Avaliação do auditor revisor"]
    usa_revisor = (
        revisor.notna() & revisor.astype(str).str.strip().ne("")
        & revisor.map(normalizar).ne("sem_parecer")
    )
    df["usa_revisor"] = usa_revisor
    df["resultado_final"] = df["Resultado da avaliação do juiz"]
    df.loc[usa_revisor, "resultado_final"] = revisor[usa_revisor]
    df["nao_conforme"] = df["resultado_final"].map(normalizar).eq("nao_conforme")
    df["item_base"] = df["Código do item avaliado"].astype(str).str.extract(r"^(q\d{4})", expand=False)
    df = df[df["nao_conforme"]].copy()

    por_auditado = (
        df.groupby("Auditado")
        .agg(
            registros_pos_evidencia=("Código do item avaliado", "size"),
            itens_distintos=("Código do item avaliado", "nunique"),
            registros_achado=("Achado", lambda s: s.astype(str).str.casefold().eq("sim").sum()),
        )
        .reset_index()
        .sort_values(["registros_pos_evidencia", "Auditado"], ascending=[False, True])
    )
    por_item = (
        df.groupby(["Código do item avaliado", "Achado"], dropna=False)
        .size().rename("registros").reset_index()
        .sort_values(["registros", "Código do item avaliado"], ascending=[False, True])
    )
    por_base = (
        df.groupby(["item_base", "Achado"], dropna=False)
        .size().rename("registros").reset_index()
        .sort_values(["registros", "item_base"], ascending=[False, True])
    )
    return df, por_auditado, por_item, por_base


def carregar_indices(pre_path: Path, final_path: Path, por_auditado: pd.DataFrame) -> dict[str, pd.DataFrame]:
    pre = pd.read_excel(pre_path, sheet_name="resultados")
    final = pd.read_excel(final_path, sheet_name="resultados")
    cols = ["id", "nivel_maturidade", *INDICADORES]
    comp = pre[cols].merge(final[cols], on="id", suffixes=("_pre", "_final"), validate="one_to_one")
    if len(comp) != 113:
        raise ValueError(f"Esperadas 113 organizações no comparativo; encontradas {len(comp)}.")
    for indicador in INDICADORES:
        comp[f"delta_{indicador}"] = comp[f"{indicador}_final"] - comp[f"{indicador}_pre"]
    comp["mudanca_maturidade"] = comp["nivel_maturidade_pre"] + " -> " + comp["nivel_maturidade_final"]
    ordem = {nivel: i for i, nivel in enumerate(NIVEIS)}
    comp["delta_nivel_ordem"] = comp["nivel_maturidade_final"].map(ordem) - comp["nivel_maturidade_pre"].map(ordem)
    comp["houve_queda_maturidade"] = comp["delta_nivel_ordem"] < 0
    comp = comp.merge(por_auditado, left_on="id", right_on="Auditado", how="left")
    for coluna in ["registros_pos_evidencia", "itens_distintos", "registros_achado"]:
        comp[coluna] = comp[coluna].fillna(0).astype(int)
    comp = comp.sort_values(["delta_iGovTI", "id"])

    resumo = []
    for indicador in INDICADORES:
        antes, depois, delta = comp[f"{indicador}_pre"], comp[f"{indicador}_final"], comp[f"delta_{indicador}"]
        resumo.append({
            "indicador": indicador,
            "media_pre": antes.mean(), "media_final": depois.mean(), "delta_media": delta.mean(),
            "mediana_pre": antes.median(), "mediana_final": depois.median(), "delta_mediana": depois.median() - antes.median(),
            "min_delta": delta.min(), "max_delta": delta.max(),
            "qtd_reducao": int((delta < -1e-12).sum()),
            "qtd_sem_variacao": int((delta.abs() <= 1e-12).sum()),
            "qtd_aumento": int((delta > 1e-12).sum()),
        })
    resumo_df = pd.DataFrame(resumo)

    maturidade = pd.DataFrame({
        "nivel_maturidade": NIVEIS,
        "pre": [int((comp["nivel_maturidade_pre"] == n).sum()) for n in NIVEIS],
        "final": [int((comp["nivel_maturidade_final"] == n).sum()) for n in NIVEIS],
    })
    maturidade["delta"] = maturidade["final"] - maturidade["pre"]
    transicoes = (
        comp.groupby(["nivel_maturidade_pre", "nivel_maturidade_final"])
        .size().rename("qtd").reset_index()
    )
    quedas = (
        comp[["id", *[f"{i}_pre" for i in INDICADORES], *[f"{i}_final" for i in INDICADORES]]]
        .set_index("id")
    )
    linhas = []
    for auditado, row in quedas.iterrows():
        for indicador in INDICADORES:
            linhas.append({"id": auditado, "indicador": indicador, "pre": row[f"{indicador}_pre"], "final": row[f"{indicador}_final"], "delta": row[f"{indicador}_final"] - row[f"{indicador}_pre"]})
    maiores_quedas = pd.DataFrame(linhas).sort_values(["delta", "id", "indicador"]).head(50)
    return {"comparativo_por_auditado": comp, "resumo_indicadores": resumo_df, "maturidade_resumo": maturidade, "maturidade_transicoes": transicoes, "maiores_quedas_dimensao": maiores_quedas}


def carregar_conformidade(path: Path) -> dict[str, pd.DataFrame]:
    df = pd.read_excel(path, sheet_name=0)
    grupos = []
    for auditado, g in df.groupby("auditado"):
        estados = g["estado"].map(normalizar)
        conformes = int((estados == "conforme").sum())
        nao_conformes = int((estados == "nao_conforme").sum())
        total = len(g)
        grupos.append({
            "auditado": auditado, "itens_avaliados": total, "itens_distintos": g["item"].nunique(),
            "evidencias_distintas": g["evidencia"].nunique(), "conformes": conformes,
            "nao_conformes": nao_conformes, "inconclusivos": int((estados == "inconclusivo").sum()),
            "outros": total - conformes - nao_conformes - int((estados == "inconclusivo").sum()),
            "taxa_conformidade": conformes / total if total else 0,
            "todas_conformes": conformes == total,
        })
    conf = pd.DataFrame(grupos).sort_values(["taxa_conformidade", "itens_avaliados", "auditado"], ascending=[False, False, True])
    return {
        "conformidade_por_auditado": conf,
        "auditados_100pct_conformes": conf[conf["todas_conformes"]].copy(),
        "maior_conformidade": pd.concat([conf[conf["todas_conformes"]], conf[(~conf["todas_conformes"]) & (conf["itens_avaliados"] >= 10)]], ignore_index=True).head(20),
    }


def resumir_bases(
    respostas_pre: Path,
    respostas_final: Path,
    ajustes: pd.DataFrame,
    comparativo: pd.DataFrame,
) -> pd.DataFrame:
    pre = pd.read_excel(respostas_pre).set_index("firstname")
    final = pd.read_excel(respostas_final).set_index("firstname")
    colunas = pre.columns.intersection(final.columns)
    pre = pre.loc[final.index, colunas]
    iguais = pre.eq(final[colunas]) | (pre.isna() & final[colunas].isna())
    alteradas = ~iguais
    delta = comparativo["delta_iGovTI"]
    return pd.DataFrame(
        [
            ("Organizações no cenário com ajuste inicial", len(pre)),
            ("Organizações no cenário final", len(final)),
            ("Registros de não conformidade no arquivo pós-evidência", len(ajustes)),
            ("Células efetivamente alteradas pelo ajuste pós-evidência", int(alteradas.to_numpy().sum())),
            ("Organizações com pelo menos uma célula alterada", int((alteradas.sum(axis=1) > 0).sum())),
            ("Organizações com redução no iGovTI", int((delta < -1e-12).sum())),
            ("Organizações sem variação no iGovTI", int((delta.abs() <= 1e-12).sum())),
            ("Organizações com aumento no iGovTI", int((delta > 1e-12).sum())),
        ],
        columns=["elemento_analisado", "resultado"],
    )


def extrair_auditoria(path: Path, validos: set[str]) -> dict[str, dict[str, set[str]]]:
    bruto = json.loads(path.read_text(encoding="utf-8"))
    saida = {}
    for auditado in sorted(validos):
        registro = bruto.get(auditado, {})
        achados, situacoes, encaminhamentos = set(), set(), set()
        for proc in registro.get("procedimentos_executados", []):
            if not proc.get("achado_ocorreu") or not proc.get("achado"):
                continue
            achado = proc["achado"]
            numero = achado.get("numero", proc.get("numero_achado"))
            nome = achado.get("nome", proc.get("nome_achado"))
            achados.add(f"{numero}. {nome}")
            situacoes.update(f"[ACHADO {numero}] {s}" for s in achado.get("situacoes_encontradas", []))
            encaminhamentos.update(f"[{e.get('tipo')}] {e.get('encaminhamento')}" for e in achado.get("encaminhamentos", []))
        saida[auditado] = {"achados": achados, "situacoes": situacoes, "encaminhamentos": encaminhamentos}
    return saida


def comparar_conjuntos(pre: dict, final: dict, chave: str, rotulo: str) -> pd.DataFrame:
    itens = sorted(set().union(*(v[chave] for v in pre.values()), *(v[chave] for v in final.values())))
    linhas = []
    for item in itens:
        antes = {a for a, v in pre.items() if item in v[chave]}
        depois = {a for a, v in final.items() if item in v[chave]}
        linhas.append({
            rotulo: item, "ajuste_inicial_respostas": len(antes), "final_pos_evidencias": len(depois),
            "delta": len(depois) - len(antes), "adicionados": len(depois - antes), "removidos": len(antes - depois),
            "auditados_adicionados": "; ".join(sorted(depois - antes)) or None,
            "auditados_removidos": "; ".join(sorted(antes - depois)) or None,
        })
    return pd.DataFrame(linhas).sort_values(["delta", rotulo], ascending=[False, True])


def carregar_impacto_auditoria(pre_path: Path, final_path: Path, universo_path: Path) -> dict[str, pd.DataFrame]:
    if universo_path.suffix.lower() == ".xlsx":
        # O cadastro delimita o universo da fiscalização, mas a condição de
        # respondente válido está registrada no resultado da auditoria.
        cadastro = set(pd.read_excel(universo_path)["sigla"].dropna().astype(str))
        universo = json.loads(pre_path.read_text(encoding="utf-8"))
        validos = {a for a, r in universo.items() if a in cadastro and r.get("foi_auditado")}
    else:
        universo = json.loads(universo_path.read_text(encoding="utf-8"))
        validos = {a for a, r in universo.items() if r.get("foi_auditado")}
    if len(validos) != 113:
        raise ValueError(f"Esperadas 113 organizações avaliadas; encontradas {len(validos)}.")
    pre, final = extrair_auditoria(pre_path, validos), extrair_auditoria(final_path, validos)
    linhas = []
    for auditado in sorted(validos):
        linha = {"Auditado": auditado}
        for chave, prefixo in [("achados", "achados"), ("situacoes", "situacoes"), ("encaminhamentos", "encaminhamentos")]:
            a, f = len(pre[auditado][chave]), len(final[auditado][chave])
            linha[f"{prefixo}_ajuste_inicial_respostas"] = a
            linha[f"{prefixo}_final_pos_evidencias"] = f
            linha[f"delta_{prefixo}"] = f - a
        linhas.append(linha)
    por_auditado = pd.DataFrame(linhas)

    medidas = []
    for chave, nome in [("achados", "Marcações de achados por auditado"), ("situacoes", "Situações inconformes"), ("encaminhamentos", "Encaminhamentos associados")]:
        a, f, d = por_auditado[f"{chave}_ajuste_inicial_respostas"], por_auditado[f"{chave}_final_pos_evidencias"], por_auditado[f"delta_{chave}"]
        medidas.append({
            "medida": nome, "total_ajuste_inicial_respostas": int(a.sum()), "total_final_pos_evidencias": int(f.sum()), "delta_total": int(d.sum()),
            "marcacoes_adicionadas": int(d.clip(lower=0).sum()), "marcacoes_removidas": int((-d.clip(upper=0)).sum()),
            "auditados_com_aumento": int((d > 0).sum()), "auditados_sem_variacao": int((d == 0).sum()), "auditados_com_reducao": int((d < 0).sum()),
            "media_ajuste_inicial_respostas": a.mean(), "media_final_pos_evidencias": f.mean(), "delta_media": d.mean(),
            "mediana_ajuste_inicial_respostas": a.median(), "mediana_final_pos_evidencias": f.median(), "delta_mediana": f.median() - a.median(),
            "min_ajuste_inicial_respostas": int(a.min()), "min_final_pos_evidencias": int(f.min()), "max_ajuste_inicial_respostas": int(a.max()), "max_final_pos_evidencias": int(f.max()),
        })
    resumo = pd.DataFrame(medidas)
    distribuicao = pd.DataFrame({
        "qtd_achados": sorted(set(por_auditado["achados_ajuste_inicial_respostas"]) | set(por_auditado["achados_final_pos_evidencias"]))
    })
    distribuicao["ajuste_inicial_respostas"] = distribuicao["qtd_achados"].map(Counter(por_auditado["achados_ajuste_inicial_respostas"]))
    distribuicao["final_pos_evidencias"] = distribuicao["qtd_achados"].map(Counter(por_auditado["achados_final_pos_evidencias"]))
    distribuicao["delta"] = distribuicao["final_pos_evidencias"] - distribuicao["ajuste_inicial_respostas"]
    s1, s2 = por_auditado["situacoes_ajuste_inicial_respostas"], por_auditado["situacoes_final_pos_evidencias"]
    estatisticas = pd.DataFrame([
        {"estatistica": "média", "situacoes_ajuste_inicial_respostas": s1.mean(), "situacoes_final_pos_evidencias": s2.mean(), "delta": s2.mean() - s1.mean()},
        {"estatistica": "mediana", "situacoes_ajuste_inicial_respostas": s1.median(), "situacoes_final_pos_evidencias": s2.median(), "delta": s2.median() - s1.median()},
        {"estatistica": "mínimo", "situacoes_ajuste_inicial_respostas": s1.min(), "situacoes_final_pos_evidencias": s2.min(), "delta": s2.min() - s1.min()},
        {"estatistica": "máximo", "situacoes_ajuste_inicial_respostas": s1.max(), "situacoes_final_pos_evidencias": s2.max(), "delta": s2.max() - s1.max()},
    ])
    return {
        "impacto_auditoria_resumo": resumo,
        "impacto_auditoria_auditado": por_auditado,
        "top_aumento_situacoes": por_auditado.sort_values(["delta_situacoes", "Auditado"], ascending=[False, True]).head(25),
        "impacto_por_achado": comparar_conjuntos(pre, final, "achados", "achado"),
        "impacto_por_situacao": comparar_conjuntos(pre, final, "situacoes", "situacao_inconforme"),
        "impacto_por_encaminhamento": comparar_conjuntos(pre, final, "encaminhamentos", "encaminhamento"),
        "distribuicao_qtd_achados": distribuicao,
        "estatisticas_qtd_situacoes": estatisticas,
    }


def formatar_workbook(writer: pd.ExcelWriter) -> None:
    for ws in writer.book.worksheets:
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions
        for cell in ws[1]:
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill("solid", fgColor="4472C4")
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        for col in ws.columns:
            largura = min(max(len(str(c.value or "")) for c in list(col)[:200]) + 2, 60)
            ws.column_dimensions[col[0].column_letter].width = max(largura, 12)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--igovti-pre", type=Path, required=True)
    parser.add_argument("--igovti-final", type=Path, default=ROOT / "02-Execucao/01-Questionario/04-Resultados_iGovTI/20260621-iGovTI-2026.xlsx")
    parser.add_argument("--respostas-pre", type=Path, default=ROOT / "02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario-01-pos-ajuste-inicial.xlsx")
    parser.add_argument("--respostas-final", type=Path, default=ROOT / "02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario-02-pos-avaliacao-evidencias.xlsx")
    parser.add_argument("--ajustes", type=Path, default=ROOT / "02-Execucao/01-Questionario/02-Ajustes_Respostas/ajustes_respostas_questionario_pos_avaliacao_evidencias.xlsx")
    parser.add_argument("--pareceres", type=Path, default=ROOT / "02-Execucao/03-Execucao_Procedimentos/99-Avaliacao_Evidencias/consolidado/pareceres_consolidados.xlsx")
    parser.add_argument("--auditoria-pre", type=Path, required=True)
    parser.add_argument("--auditoria-final", type=Path, required=True)
    parser.add_argument("--universo-auditoria", type=Path, default=ROOT / "02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/resultado_auditoria.json")
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("dados_impacto_avaliacao_evidencias.xlsx"))
    args = parser.parse_args()

    ajustes, por_auditado, por_item, por_base = carregar_ajustes(args.ajustes)
    abas = carregar_indices(args.igovti_pre, args.igovti_final, por_auditado)
    abas["resumo_base"] = resumir_bases(
        args.respostas_pre,
        args.respostas_final,
        ajustes,
        abas["comparativo_por_auditado"],
    )
    abas.update({"ajustes_pos_evidencia": ajustes, "ajustes_por_auditado": por_auditado, "ajustes_por_item": por_item, "ajustes_por_item_base": por_base})
    abas.update(carregar_conformidade(args.pareceres))
    abas.update(carregar_impacto_auditoria(args.auditoria_pre, args.auditoria_final, args.universo_auditoria))
    abas["fontes_execucao_auditoria"] = pd.DataFrame([
        {"cenario": "ajuste_inicial_somente_respostas", "respostas": str(args.igovti_pre), "resultado_auditoria": str(args.auditoria_pre), "observacao": "Cenário anterior à aplicação dos ajustes decorrentes da avaliação de evidências."},
        {"cenario": "final_pos_evidencias", "respostas": str(args.igovti_final), "resultado_auditoria": str(args.auditoria_final), "observacao": "Cenário final, após a aplicação dos ajustes decorrentes da avaliação de evidências."},
    ])

    ordem = [
        "comparativo_por_auditado", "resumo_base", "resumo_indicadores", "maturidade_resumo", "maturidade_transicoes",
        "ajustes_pos_evidencia", "ajustes_por_auditado", "ajustes_por_item", "ajustes_por_item_base",
        "maiores_quedas_dimensao", "conformidade_por_auditado", "auditados_100pct_conformes", "maior_conformidade",
        "fontes_execucao_auditoria", "impacto_auditoria_resumo", "impacto_auditoria_auditado", "top_aumento_situacoes",
        "impacto_por_achado", "impacto_por_situacao", "impacto_por_encaminhamento", "distribuicao_qtd_achados", "estatisticas_qtd_situacoes",
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(args.output, engine="openpyxl") as writer:
        for nome in ordem:
            abas[nome].to_excel(writer, sheet_name=nome, index=False)
        formatar_workbook(writer)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
