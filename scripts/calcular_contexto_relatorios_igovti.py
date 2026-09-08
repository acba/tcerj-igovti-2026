#!/usr/bin/env python3
"""Calcula as estatisticas e o contexto por auditado usados nos relatorios iGovTI 2026."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "resources"))

from igovti_dados_utils import (
    COMPARAVEL_2023_MUNICIPIOS,
    COMPARAVEL_2023_SETIC,
    COMPARAVEL_2026,
    NIVEIS,
    RESULTADOS_2026,
    ROOT,
    carregar_resultados_2026,
    consolidar_pareamentos,
    direcao_variacao,
    estatisticas_serie,
    formatar_lista_variacoes,
    to_relative,
)
from xlsx_utils import dataframe_to_xlsx_se_diferente


DIMENSOES = {
    "PlanejamentoTI": "planejamento",
    "ServicosTI": "servicos",
    "RiscosTISegInfo": "riscos_seguranca",
    "EstruturaSegInfo": "estrutura_seguranca",
    "ProcessoSegInfo": "processos_seguranca",
    "GerirSoluçõesTI": "gestao_solucoes",
}
ROTULOS_DIMENSOES = {
    "PlanejamentoTI": "Planejamento de TIC",
    "ServicosTI": "Gestão de serviços de TIC",
    "RiscosTISegInfo": "Riscos de TI e de segurança da informação",
    "EstruturaSegInfo": "Estrutura de segurança da informação",
    "ProcessoSegInfo": "Processos de segurança da informação",
    "GerirSoluçõesTI": "Gestão de soluções de TIC",
}
INDICADORES = {
    "iGovTI": "igovti_geral",
    "GovernancaTI": "governanca_geral",
    "iGestTI": "igest_geral",
}

SAIDA_CONTEXTO = ROOT / "02-Execucao/01-Questionario/04-Resultados_iGovTI/20260621-contexto-relatorios-igovti-2026.xlsx"
SAIDA_JSON = ROOT / "02-Execucao/01-Questionario/04-Resultados_iGovTI/20260621-estatisticas-relatorios-igovti-2026.json"
METODOLOGIA_2026 = ROOT / "01-Planejamento/02-Metodologia_iGovTI/estrutura-igovti-2026.yaml"


def percentual(quantidade: int, total: int) -> float:
    return 100.0 * quantidade / total if total else 0.0


def carregar_praticas_governanca(metodologia_path: Path = METODOLOGIA_2026) -> dict[str, dict[str, object]]:
    """Carrega rótulos, prefixos e pesos das práticas que formam Governança de TIC."""
    config = yaml.safe_load(metodologia_path.read_text(encoding="utf-8"))
    contexto = config.get("contexto_relatorios", {}).get("praticas_governanca", {})
    componentes = {
        item["id"]: float(item["peso"])
        for item in config["agregados"]["GovernancaTI"]["componentes"]
    }
    if set(contexto) != set(componentes):
        raise ValueError(
            "As práticas de Governança do contexto não coincidem com os componentes de GovernancaTI."
        )
    return {
        pratica_id: {
            "prefixo": str(dados["prefixo"]),
            "rotulo": str(dados["rotulo"]),
            "peso": componentes[pratica_id],
        }
        for pratica_id, dados in contexto.items()
    }


def carregar_dimensoes_gestao(metodologia_path: Path = METODOLOGIA_2026) -> dict[str, dict[str, object]]:
    """Carrega rótulos, prefixos e pesos das dimensões que formam Gestão de TIC."""
    config = yaml.safe_load(metodologia_path.read_text(encoding="utf-8"))
    contexto = config.get("contexto_relatorios", {}).get("dimensoes", {})
    componentes = {
        item["id"]: float(item["peso"])
        for item in config["agregados"]["iGestTI"]["componentes"]
    }
    if set(contexto) != set(componentes):
        raise ValueError(
            "As dimensões de Gestão de TIC do contexto não coincidem com os componentes de iGestTI."
        )
    return {
        dimensao_id: {
            "prefixo": str(dados["prefixo"]),
            "rotulo": str(dados["rotulo"]),
            "peso": componentes[dimensao_id],
        }
        for dimensao_id, dados in contexto.items()
    }


def calcular_estatisticas_globais(
    resultados: pd.DataFrame,
    praticas_governanca: dict[str, dict[str, object]] | None = None,
    dimensoes_gestao: dict[str, dict[str, object]] | None = None,
) -> dict[str, object]:
    praticas_governanca = praticas_governanca or carregar_praticas_governanca()
    dimensoes_gestao = dimensoes_gestao or carregar_dimensoes_gestao()
    total = len(resultados)
    estatisticas: dict[str, object] = {"universo_2026_n": total}

    contagem_niveis = resultados["iGovTI_maturidade"].value_counts().reindex(NIVEIS, fill_value=0)
    for nivel in NIVEIS:
        prefixo = {
            "Inexpressivo": "maturidade_inexpressivo",
            "Iniciando": "maturidade_iniciando",
            "Intermediário": "maturidade_intermediario",
            "Aprimorado": "maturidade_aprimorado",
        }[nivel]
        quantidade = int(contagem_niveis[nivel])
        estatisticas[f"{prefixo}_n"] = quantidade
        estatisticas[f"{prefixo}_pct"] = percentual(quantidade, total)

    abaixo = int((resultados["iGovTI"] < 0.40).sum())
    estatisticas["igovti_abaixo_040_n"] = abaixo
    estatisticas["igovti_abaixo_040_pct"] = percentual(abaixo, total)

    for coluna, prefixo in INDICADORES.items():
        resumo = estatisticas_serie(resultados[coluna])
        for nome, valor in resumo.items():
            estatisticas[f"{prefixo}_{nome}"] = valor
        estatisticas[f"{prefixo}_zeros_pct"] = percentual(int(resumo["zeros_n"]), total)
        estatisticas[f"{prefixo}_abaixo_040_pct"] = percentual(int(resumo["abaixo_040_n"]), total)
        estatisticas[f"{prefixo}_a_partir_040_pct"] = percentual(int(resumo["a_partir_040_n"]), total)

    for coluna, dados in praticas_governanca.items():
        if coluna not in resultados:
            raise ValueError(f"Prática de Governança ausente dos resultados: {coluna}")
        prefixo = f"governanca_{dados['prefixo']}"
        resumo = estatisticas_serie(resultados[coluna])
        estatisticas[f"{prefixo}_rotulo"] = dados["rotulo"]
        estatisticas[f"{prefixo}_peso"] = dados["peso"]
        for nome, valor in resumo.items():
            estatisticas[f"{prefixo}_geral_{nome}"] = valor
        estatisticas[f"{prefixo}_geral_zeros_pct"] = percentual(int(resumo["zeros_n"]), total)
        estatisticas[f"{prefixo}_geral_abaixo_040_pct"] = percentual(int(resumo["abaixo_040_n"]), total)

    medias_governanca = resultados[list(praticas_governanca)].mean().sort_values(ascending=False)
    maior_pratica = medias_governanca.index[0]
    menor_pratica = medias_governanca.index[-1]
    estatisticas["governanca_pratica_maior_media_nome"] = praticas_governanca[maior_pratica]["rotulo"]
    estatisticas["governanca_pratica_maior_media_valor"] = float(medias_governanca.iloc[0])
    estatisticas["governanca_pratica_menor_media_nome"] = praticas_governanca[menor_pratica]["rotulo"]
    estatisticas["governanca_pratica_menor_media_valor"] = float(medias_governanca.iloc[-1])

    diferenca_componentes = resultados["iGestTI"] - resultados["GovernancaTI"]
    maior_gestao = int((diferenca_componentes > 1e-12).sum())
    maior_governanca = int((diferenca_componentes < -1e-12).sum())
    iguais = int(diferenca_componentes.abs().le(1e-12).sum())
    for nome, quantidade in {
        "gestao_maior_governanca": maior_gestao,
        "governanca_maior_gestao": maior_governanca,
        "governanca_gestao_iguais": iguais,
    }.items():
        estatisticas[f"{nome}_n"] = quantidade
        estatisticas[f"{nome}_pct"] = percentual(quantidade, total)

    colunas_dimensoes = list(DIMENSOES)
    maximos = resultados[colunas_dimensoes].max(axis=1)
    minimos = resultados[colunas_dimensoes].min(axis=1)
    for coluna, prefixo in DIMENSOES.items():
        estatisticas[f"{prefixo}_peso"] = dimensoes_gestao[coluna]["peso"]
        resumo = estatisticas_serie(resultados[coluna])
        for nome, valor in resumo.items():
            estatisticas[f"{prefixo}_geral_{nome}"] = valor
        estatisticas[f"{prefixo}_geral_zeros_pct"] = percentual(int(resumo["zeros_n"]), total)
        estatisticas[f"{prefixo}_geral_abaixo_040_pct"] = percentual(int(resumo["abaixo_040_n"]), total)
        maiores = int(np.isclose(resultados[coluna], maximos, rtol=0.0, atol=1e-12).sum())
        menores = int(np.isclose(resultados[coluna], minimos, rtol=0.0, atol=1e-12).sum())
        estatisticas[f"{prefixo}_maior_resultado_n"] = maiores
        estatisticas[f"{prefixo}_maior_resultado_pct"] = percentual(maiores, total)
        estatisticas[f"{prefixo}_menor_resultado_n"] = menores
        estatisticas[f"{prefixo}_menor_resultado_pct"] = percentual(menores, total)

    medias = resultados[colunas_dimensoes].mean().sort_values(ascending=False)
    medianas = resultados[colunas_dimensoes].median().sort_values(ascending=False)
    maior_media = medias.index[0]
    maior_mediana = medianas.index[0]
    estatisticas["dimensao_maior_media_nome"] = ROTULOS_DIMENSOES[maior_media]
    estatisticas["dimensao_maior_media_valor"] = float(medias.iloc[0])
    estatisticas["dimensao_maior_media_mediana"] = float(resultados[maior_media].median())
    estatisticas["dimensao_maior_media_maior_resultado_n"] = estatisticas[
        f"{DIMENSOES[maior_media]}_maior_resultado_n"
    ]
    estatisticas["dimensao_maior_media_maior_resultado_pct"] = estatisticas[
        f"{DIMENSOES[maior_media]}_maior_resultado_pct"
    ]
    estatisticas["dimensao_maior_mediana_nome"] = ROTULOS_DIMENSOES[maior_mediana]
    estatisticas["dimensao_maior_mediana_valor"] = float(medianas.iloc[0])
    for indice, coluna in enumerate(medias.index[-2:][::-1], start=1):
        prefixo = DIMENSOES[coluna]
        estatisticas[f"dimensao_fragil_{indice}_nome"] = ROTULOS_DIMENSOES[coluna]
        estatisticas[f"dimensao_fragil_{indice}_media"] = float(resultados[coluna].mean())
        estatisticas[f"dimensao_fragil_{indice}_abaixo_040_n"] = estatisticas[f"{prefixo}_geral_abaixo_040_n"]
        estatisticas[f"dimensao_fragil_{indice}_abaixo_040_pct"] = estatisticas[f"{prefixo}_geral_abaixo_040_pct"]
        estatisticas[f"dimensao_fragil_{indice}_menor_resultado_n"] = estatisticas[f"{prefixo}_menor_resultado_n"]
        estatisticas[f"dimensao_fragil_{indice}_menor_resultado_pct"] = estatisticas[f"{prefixo}_menor_resultado_pct"]
    return estatisticas


def adicionar_comparacao(contexto: pd.DataFrame, pareados: pd.DataFrame) -> pd.DataFrame:
    contexto = contexto.copy()
    contexto["tem_comparacao_2023"] = False
    por_sigla = contexto.set_index("_key").index
    for _, par in pareados.iterrows():
        chave = str(par["chave_2026"])
        if chave not in por_sigla:
            continue
        mascara = contexto["_key"].eq(chave)
        valores = {
            "tem_comparacao_2023": True,
            "comparacao_sigla_2023": par["sigla_2023"],
            "comparacao_tipo_pareamento": par["tipo_pareamento"],
            "comparacao_grupo": par["grupo"],
            "comparacao_nivel_2023": par["nivel_maturidade_2023"],
            "comparacao_nivel_2026": par["nivel_maturidade_2026"],
            "comparacao_igovti_2023": par["iGovTI_2023"],
            "comparacao_igovti_2026": par["iGovTI_2026"],
            "comparacao_delta_igovti": par["delta_iGovTI"],
            "comparacao_direcao_igovti": direcao_variacao(float(par["delta_iGovTI"])),
            "comparacao_governanca_2023": par["GovernancaTI_2023"],
            "comparacao_governanca_2026": par["GovernancaTI_2026"],
            "comparacao_delta_governanca": par["delta_GovernancaTI"],
            "comparacao_igest_2023": par["iGestTI_2023"],
            "comparacao_igest_2026": par["iGestTI_2026"],
            "comparacao_delta_igest": par["delta_iGestTI"],
            "comparacao_principais_avancos": formatar_lista_variacoes(par, positivas=True),
            "comparacao_principais_regressoes": formatar_lista_variacoes(par, positivas=False),
        }
        for coluna, valor in valores.items():
            contexto.loc[mascara, coluna] = valor
    return contexto


def gerar_contexto(
    resultados_path: Path,
    comparavel_2026: Path,
    setic_2023: Path,
    municipios_2023: Path,
    metodologia: Path = METODOLOGIA_2026,
) -> tuple[pd.DataFrame, dict[str, object], pd.DataFrame]:
    resultados = carregar_resultados_2026(resultados_path)
    estatisticas = calcular_estatisticas_globais(
        resultados,
        carregar_praticas_governanca(metodologia),
        carregar_dimensoes_gestao(metodologia),
    )
    _, pareados, _ = consolidar_pareamentos(comparavel_2026, setic_2023, municipios_2023)
    estatisticas["comparacao_pareados_n"] = len(pareados)
    estatisticas["comparacao_cobertura_2026_pct"] = percentual(len(pareados), len(resultados))
    colunas_globais = {
        nome: json.dumps(valor, ensure_ascii=False) if isinstance(valor, list) else valor
        for nome, valor in estatisticas.items()
    }
    repetidos = pd.DataFrame(
        {nome: [valor] * len(resultados) for nome, valor in colunas_globais.items()},
        index=resultados.index,
    )
    contexto = pd.concat([resultados.copy(), repetidos], axis=1)
    contexto = adicionar_comparacao(contexto, pareados)
    contexto = contexto.drop(columns=["_key"])
    return contexto, estatisticas, pareados


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resultados-2026", type=Path, default=RESULTADOS_2026)
    parser.add_argument("--comparavel-2026", type=Path, default=COMPARAVEL_2026)
    parser.add_argument("--setic-2023", type=Path, default=COMPARAVEL_2023_SETIC)
    parser.add_argument("--municipios-2023", type=Path, default=COMPARAVEL_2023_MUNICIPIOS)
    parser.add_argument("--metodologia", type=Path, default=METODOLOGIA_2026)
    parser.add_argument("--saida-contexto", type=Path, default=SAIDA_CONTEXTO)
    parser.add_argument("--saida-estatisticas", type=Path, default=SAIDA_JSON)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    contexto, estatisticas, pareados = gerar_contexto(
        args.resultados_2026, args.comparavel_2026, args.setic_2023, args.municipios_2023, args.metodologia
    )
    dataframe_to_xlsx_se_diferente(contexto, args.saida_contexto, index=False)
    payload = {
        "fontes": {
            "resultados_2026": to_relative(args.resultados_2026),
            "comparavel_2026": to_relative(args.comparavel_2026),
            "setic_2023": to_relative(args.setic_2023),
            "municipios_2023": to_relative(args.municipios_2023),
        },
        "estatisticas_2026": estatisticas,
        "organizacoes_pareadas": len(pareados),
    }
    args.saida_estatisticas.parent.mkdir(parents=True, exist_ok=True)
    args.saida_estatisticas.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Contexto dos relatórios: {to_relative(args.saida_contexto)}")
    print(f"Memória de cálculo: {to_relative(args.saida_estatisticas)}")
    print(f"Organizações em 2026: {len(contexto)}; pareadas com 2023: {len(pareados)}")


if __name__ == "__main__":
    main()
