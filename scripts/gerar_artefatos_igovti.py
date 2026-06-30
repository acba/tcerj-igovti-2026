#!/usr/bin/env python3
"""Gera os artefatos derivados do iGovTI 2026 a partir das respostas.

Gera, em sequência:

1. ``02-Execucao/01-Questionario/04-Resultados_iGovTI/<prefixo>-iGovTI-2026.xlsx``
2. ``02-Execucao/01-Questionario/04-Resultados_iGovTI/<prefixo>-iGovTI-2026-Ajustado-Comparavel.xlsx``
3. ``02-Execucao/02-Questionario iGovTI 2023/<prefixo>-comparacao-iGovTI-2023-2026.xlsx``
4. ``02-Execucao/01-Questionario/04-Resultados_iGovTI/<prefixo>-contexto-relatorios-igovti-2026.xlsx``
5. ``02-Execucao/01-Questionario/04-Resultados_iGovTI/<prefixo>-estatisticas-relatorios-igovti-2026.json``

Exemplo::

    scripts/.venv/bin/python scripts/gerar_artefatos_igovti.py \
      --respostas 02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario.xlsx
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RESOURCES = Path(__file__).resolve().parent / "resources"

sys.path.insert(0, str(RESOURCES))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from gerar_igovti import carregar_mapeamento_id, deduplicar_respostas
from igovti_calculadora import calcular_igovti

from calcular_contexto_relatorios_igovti import (
    DIMENSOES,
    INDICADORES,
    ROTULOS_DIMENSOES,
    calcular_estatisticas_globais,
    percentual,
)
from consolidar_dados_comparativos_igovti import (
    gerar_estatisticas,
    preparar_resultados_individuais,
)
from igovti_dados_utils import (
    COMPARAVEL_2023_MUNICIPIOS,
    COMPARAVEL_2023_SETIC,
    NIVEIS,
    ROOT as IGOVTI_ROOT,
    carregar_comparavel,
    carregar_resultados_2026,
    classificar_maturidade,
    consolidar_pareamentos,
    direcao_variacao,
    estatisticas_serie,
    formatar_lista_variacoes,
    normalizar_sigla,
    to_relative,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--respostas",
        type=Path,
        default=ROOT / "02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario.xlsx",
        help="Planilha XLSX com as respostas do questionário.",
    )
    parser.add_argument(
        "--prefixo",
        type=str,
        default="20260621",
        help="Prefixo dos arquivos de saída (padrão: 20260621)."
    )
    parser.add_argument(
        "--yaml-oficial",
        type=Path,
        default=ROOT / "01-Planejamento/02-Metodologia_iGovTI/estrutura-igovti-2026.yaml",
        help="YAML da estrutura iGovTI oficial.",
    )
    parser.add_argument(
        "--yaml-comparavel",
        type=Path,
        default=ROOT / "01-Planejamento/02-Metodologia_iGovTI/estrutura-igovti-2026-ajustado-comparavel.yaml",
        help="YAML da estrutura iGovTI ajustado comparável.",
    )
    parser.add_argument(
        "--mapeamento-id",
        type=Path,
        default=ROOT / "02-Execucao/01-Questionario/01-Coleta_LimeSurvey/urls_anexos_limesurvey_consolidado.xlsx",
        help="Planilha com colunas 'id' e 'orgao'.",
    )
    parser.add_argument(
        "--sem-mapeamento",
        action="store_true",
        help="Usa o identificador original da planilha de respostas.",
    )
    parser.add_argument(
        "--coluna-id",
        type=str,
        default="",
        help="Coluna identificadora na planilha de respostas.",
    )
    parser.add_argument(
        "--setic-2023",
        type=Path,
        default=COMPARAVEL_2023_SETIC,
        help="XLSX comparável do SETIC 2023.",
    )
    parser.add_argument(
        "--municipios-2023",
        type=Path,
        default=COMPARAVEL_2023_MUNICIPIOS,
        help="XLSX comparável dos municípios 2023.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "02-Execucao",
        help="Diretório base para os arquivos de saída.",
    )
    return parser.parse_args()


def gerar_comparacao(
    caminho_comparavel_2026: Path,
    caminho_setic_2023: Path,
    caminho_municipios_2023: Path,
    caminho_saida: Path,
) -> None:
    """Gera a planilha comparativa 2023-2026."""
    pareamentos, pareados, nao_pareados_2026 = consolidar_pareamentos(
        caminho_comparavel_2026, caminho_setic_2023, caminho_municipios_2023
    )
    geral, agregados, transicoes = gerar_estatisticas(pareados)
    individuais = preparar_resultados_individuais(pareados)

    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(caminho_saida, engine="openpyxl") as writer:
        individuais.to_excel(writer, sheet_name="Resultados pareados", index=False)
        geral.to_excel(writer, sheet_name="Estatísticas gerais", index=False)
        agregados.to_excel(writer, sheet_name="Estatísticas agregados", index=False)
        transicoes.to_excel(writer, sheet_name="Transições maturidade", index=False)
        pareamentos.to_excel(writer, sheet_name="Pareamentos", index=False)
        pareamentos.loc[~pareamentos["pareado"]].to_excel(writer, sheet_name="Sem par em 2026", index=False)
        nao_pareados_2026.to_excel(writer, sheet_name="Sem histórico em 2023", index=False)

    print(f"Comparação gerada: {to_relative(caminho_saida)}")
    print(f"  Organizações pareadas: {len(pareados)}")


def _adicionar_comparacao(contexto: pd.DataFrame, pareados: pd.DataFrame) -> pd.DataFrame:
    """Incorpora dados do pareamento 2023-2026 ao contexto por órgão."""
    contexto = contexto.copy()
    contexto["tem_comparacao_2023"] = False
    por_sigla = set(contexto.set_index("_key").index)
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
    caminho_resultados_2026: Path,
    caminho_comparavel_2026: Path,
    caminho_setic_2023: Path,
    caminho_municipios_2023: Path,
    caminho_contexto: Path,
    caminho_estatisticas: Path,
) -> None:
    """Gera o contexto e a memória de cálculo dos relatórios."""
    resultados = carregar_resultados_2026(caminho_resultados_2026)
    estatisticas = calcular_estatisticas_globais(resultados)
    _, pareados, _ = consolidar_pareamentos(caminho_comparavel_2026, caminho_setic_2023, caminho_municipios_2023)
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
    contexto = _adicionar_comparacao(contexto, pareados)
    contexto = contexto.drop(columns=["_key"])

    caminho_contexto.parent.mkdir(parents=True, exist_ok=True)
    contexto.to_excel(caminho_contexto, index=False)

    payload = {
        "fontes": {
            "resultados_2026": to_relative(caminho_resultados_2026),
            "comparavel_2026": to_relative(caminho_comparavel_2026),
            "setic_2023": to_relative(caminho_setic_2023),
            "municipios_2023": to_relative(caminho_municipios_2023),
        },
        "estatisticas_2026": estatisticas,
        "organizacoes_pareadas": len(pareados),
    }
    caminho_estatisticas.parent.mkdir(parents=True, exist_ok=True)
    caminho_estatisticas.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Contexto gerado: {to_relative(caminho_contexto)}")
    print(f"Memória de cálculo: {to_relative(caminho_estatisticas)}")
    print(f"  Organizações em 2026: {len(contexto)}; pareadas com 2023: {len(pareados)}")


def main() -> None:
    args = parse_args()

    mapeamento: dict[str, str] | None = None
    if not args.sem_mapeamento:
        if args.mapeamento_id.exists():
            mapeamento = carregar_mapeamento_id(args.mapeamento_id)
            print(f"Mapeamento carregado: {len(mapeamento)} órgãos.")
        else:
            print(f"Aviso: mapeamento não encontrado em {args.mapeamento_id}; usando ids originais.")

    coluna_id = args.coluna_id or None
    prefixo = args.prefixo

    dir_q1 = args.output_dir / "01-Questionario"
    dir_resultados = dir_q1 / "04-Resultados_iGovTI"
    dir_q2 = args.output_dir / "02-Questionario iGovTI 2023"

    saida_oficial = dir_resultados / f"{prefixo}-iGovTI-2026.xlsx"
    saida_comparavel = dir_resultados / f"{prefixo}-iGovTI-2026-Ajustado-Comparavel.xlsx"
    saida_comparacao = dir_q2 / f"{prefixo}-comparacao-iGovTI-2023-2026.xlsx"
    saida_contexto = dir_resultados / f"{prefixo}-contexto-relatorios-igovti-2026.xlsx"
    saida_estatisticas = dir_resultados / f"{prefixo}-estatisticas-relatorios-igovti-2026.json"

    print(f"Respostas: {args.respostas}")
    print(f"Prefixo: {prefixo}")

    df_respostas = pd.read_excel(args.respostas)
    df_dedup = deduplicar_respostas(df_respostas, mapeamento)
    removidos = len(df_respostas) - len(df_dedup)
    if removidos:
        print(f"Deduplicação: {removidos} envio(s) antigo(s) removido(s); {len(df_dedup)} órgão(s) restante(s).")
    print()

    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        caminho_temp = Path(tmp.name)
    df_dedup.to_excel(caminho_temp, index=False)

    try:
        calcular_igovti(
            caminho_temp,
            args.yaml_oficial,
            saida_oficial,
            coluna_id=coluna_id,
            mapeamento_id=mapeamento,
        )
        print(f"Oficial gerado: {to_relative(saida_oficial)}")

        calcular_igovti(
            caminho_temp,
            args.yaml_comparavel,
            saida_comparavel,
            coluna_id=coluna_id,
            mapeamento_id=mapeamento,
        )
        print(f"Comparável gerado: {to_relative(saida_comparavel)}")
    finally:
        caminho_temp.unlink(missing_ok=True)

    gerar_comparacao(saida_comparavel, args.setic_2023, args.municipios_2023, saida_comparacao)
    gerar_contexto(
        saida_oficial,
        saida_comparavel,
        args.setic_2023,
        args.municipios_2023,
        saida_contexto,
        saida_estatisticas,
    )

    print("\nConjunto iGovTI atualizado com sucesso.")


if __name__ == "__main__":
    main()
