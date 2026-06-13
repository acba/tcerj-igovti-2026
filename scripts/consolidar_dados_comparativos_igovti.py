#!/usr/bin/env python3
"""Consolida o painel comparavel do iGovTI 2023 e 2026 em uma planilha auditavel."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from igovti_dados import (
    AGREGADOS_COMPARAVEIS,
    COMPARAVEL_2023_MUNICIPIOS,
    COMPARAVEL_2023_SETIC,
    COMPARAVEL_2026,
    INDICADORES_COMPARAVEIS,
    ORDEM_NIVEIS,
    ROOT,
    consolidar_pareamentos,
    direcao_variacao,
)


SAIDA_PADRAO = ROOT / "02-Execucao/02-Questionario iGovTI 2023/20260611-comparacao-iGovTI-2023-2026.xlsx"


def gerar_estatisticas(pareados: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    resumo = []
    for indicador, rotulo in INDICADORES_COMPARAVEIS.items():
        antigo = pareados[f"{indicador}_2023"]
        atual = pareados[f"{indicador}_2026"]
        delta = pareados[f"delta_{indicador}"]
        resumo.append(
            {
                "indicador": indicador,
                "descricao": rotulo,
                "media_2023": antigo.mean(),
                "mediana_2023": antigo.median(),
                "media_2026": atual.mean(),
                "mediana_2026": atual.median(),
                "variacao_media": delta.mean(),
                "variacao_mediana": delta.median(),
                "organizacoes_com_avanco": int((delta > 1e-12).sum()),
                "organizacoes_com_regressao": int((delta < -1e-12).sum()),
                "organizacoes_estaveis": int(delta.abs().le(1e-12).sum()),
            }
        )

    transicoes = pd.crosstab(
        pareados["nivel_maturidade_2023"],
        pareados["nivel_maturidade_2026"],
        dropna=False,
    ).reindex(index=ORDEM_NIVEIS, columns=ORDEM_NIVEIS, fill_value=0)
    transicoes.index.name = "nivel_2023"

    delta_nivel = pareados.apply(
        lambda linha: ORDEM_NIVEIS[linha["nivel_maturidade_2026"]]
        - ORDEM_NIVEIS[linha["nivel_maturidade_2023"]],
        axis=1,
    )
    geral = pd.DataFrame(
        [
            {
                "organizacoes_pareadas": len(pareados),
                "avanco_igovti": int((pareados["delta_iGovTI"] > 1e-12).sum()),
                "regressao_igovti": int((pareados["delta_iGovTI"] < -1e-12).sum()),
                "estabilidade_igovti": int(pareados["delta_iGovTI"].abs().le(1e-12).sum()),
                "avanco_nivel_maturidade": int((delta_nivel > 0).sum()),
                "regressao_nivel_maturidade": int((delta_nivel < 0).sum()),
                "mesmo_nivel_maturidade": int((delta_nivel == 0).sum()),
            }
        ]
    )
    return geral, pd.DataFrame(resumo), transicoes.reset_index()


def preparar_resultados_individuais(pareados: pd.DataFrame) -> pd.DataFrame:
    colunas = [
        "grupo", "sigla_2023", "sigla_2026", "tipo_pareamento",
        "nivel_maturidade_2023", "nivel_maturidade_2026",
    ]
    for indicador in INDICADORES_COMPARAVEIS:
        colunas.extend([f"{indicador}_2023", f"{indicador}_2026", f"delta_{indicador}"])
    saida = pareados[colunas].copy()
    saida["direcao_iGovTI"] = saida["delta_iGovTI"].map(direcao_variacao)
    saida["principais_avancos"] = saida.apply(
        lambda linha: _formatar_variacoes(linha, positivas=True), axis=1
    )
    saida["principais_regressoes"] = saida.apply(
        lambda linha: _formatar_variacoes(linha, positivas=False), axis=1
    )
    return saida


def _formatar_variacoes(linha: pd.Series, positivas: bool) -> str:
    valores = [(float(linha[f"delta_{campo}"]), rotulo) for campo, rotulo in AGREGADOS_COMPARAVEIS.items()]
    if positivas:
        valores = sorted((item for item in valores if item[0] > 1e-12), reverse=True)[:3]
    else:
        valores = sorted(item for item in valores if item[0] < -1e-12)[:3]
    return "; ".join(f"{rotulo} ({delta:+.4f})" for delta, rotulo in valores)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--comparavel-2026", type=Path, default=COMPARAVEL_2026)
    parser.add_argument("--setic-2023", type=Path, default=COMPARAVEL_2023_SETIC)
    parser.add_argument("--municipios-2023", type=Path, default=COMPARAVEL_2023_MUNICIPIOS)
    parser.add_argument("--saida", type=Path, default=SAIDA_PADRAO)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    pareamentos, pareados, nao_pareados_2026 = consolidar_pareamentos(
        args.comparavel_2026, args.setic_2023, args.municipios_2023
    )
    geral, agregados, transicoes = gerar_estatisticas(pareados)
    individuais = preparar_resultados_individuais(pareados)
    args.saida.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(args.saida, engine="openpyxl") as writer:
        individuais.to_excel(writer, sheet_name="Resultados pareados", index=False)
        geral.to_excel(writer, sheet_name="Estatísticas gerais", index=False)
        agregados.to_excel(writer, sheet_name="Estatísticas agregados", index=False)
        transicoes.to_excel(writer, sheet_name="Transições maturidade", index=False)
        pareamentos.to_excel(writer, sheet_name="Pareamentos", index=False)
        pareamentos.loc[~pareamentos["pareado"]].to_excel(writer, sheet_name="Sem par em 2026", index=False)
        nao_pareados_2026.to_excel(writer, sheet_name="Sem histórico em 2023", index=False)
    print(f"Consolidação gerada: {args.saida}")
    print(f"Organizações pareadas: {len(pareados)}")


if __name__ == "__main__":
    main()
