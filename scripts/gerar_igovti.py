#!/usr/bin/env python3
"""Gera as planilhas de resultados iGovTI 2026 a partir das respostas.

Equivalente em linha de comando à calculadora web ``scripts/calcula-igovti.html``.
Produz os arquivos:

* ``20260621-iGovTI-2026.xlsx`` (estrutura oficial)
* ``20260621-iGovTI-2026-Ajustado-Comparavel.xlsx`` (estrutura comparável)

Exemplo::

    scripts/.venv/bin/python scripts/gerar_igovti.py \
      --respostas 02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario.xlsx \
      --mapeamento-id 02-Execucao/01-Questionario/01-Coleta_LimeSurvey/urls_anexos_limesurvey_consolidado.xlsx
"""

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent / "resources"))

from igovti_calculadora import calcular_igovti


ROOT = Path(__file__).resolve().parents[1]

DEFAULT_RESPOSTAS = ROOT / "02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario.xlsx"
DEFAULT_YAML_OFICIAL = ROOT / "01-Planejamento/02-Metodologia_iGovTI/estrutura-igovti-2026.yaml"
DEFAULT_YAML_COMPARAVEL = (
    ROOT / "01-Planejamento/02-Metodologia_iGovTI/estrutura-igovti-2026-ajustado-comparavel.yaml"
)
DEFAULT_MAPEAMENTO = (
    ROOT / "02-Execucao/01-Questionario/01-Coleta_LimeSurvey/urls_anexos_limesurvey_consolidado.xlsx"
)
DEFAULT_SAIDA_OFICIAL = ROOT / "02-Execucao/01-Questionario/04-Resultados_iGovTI/20260621-iGovTI-2026.xlsx"
DEFAULT_SAIDA_COMPARAVEL = (
    ROOT / "02-Execucao/01-Questionario/04-Resultados_iGovTI/20260621-iGovTI-2026-Ajustado-Comparavel.xlsx"
)


def carregar_mapeamento_id(caminho: Path, coluna_id: str = "id", coluna_orgao: str = "orgao") -> dict[str, str]:
    """Carrega mapeamento de id numérico para sigla do órgão."""
    df = pd.read_excel(caminho)
    faltantes = {coluna_id, coluna_orgao} - set(df.columns)
    if faltantes:
        raise ValueError(f"Colunas ausentes no mapeamento: {sorted(faltantes)}")
    return {
        str(k).strip(): str(v).strip()
        for k, v in zip(df[coluna_id].astype(str), df[coluna_orgao])
        if pd.notna(v) and str(v).strip()
    }


def deduplicar_respostas(df: pd.DataFrame, mapeamento: dict[str, str] | None) -> pd.DataFrame:
    """Mantém apenas o envio mais recente de cada órgão.

    Quando o LimeSurvey possui múltiplos envios do mesmo órgão, o script de
    coleta de anexos já desconsidera os envios antigos. Para manter a
    coerência, os resultados do índice também devem usar apenas o envio mais
    recente de cada órgão.
    """
    df = df.copy()
    if mapeamento is not None:
        df["__orgao_temp"] = df["id"].astype(str).map(mapeamento)
    else:
        df["__orgao_temp"] = df["id"].astype(str)

    if df["__orgao_temp"].duplicated().any():
        coluna_data = next((c for c in ["submitdate", "datestamp", "startdate"] if c in df.columns), None)
        if coluna_data:
            df[coluna_data] = pd.to_datetime(df[coluna_data], errors="coerce")
            df = df.sort_values(coluna_data, ascending=False)
        df = df.drop_duplicates(subset=["__orgao_temp"], keep="first")
        df = df.sort_index()

    df = df.drop(columns=["__orgao_temp"])
    return df


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--respostas",
        type=Path,
        default=DEFAULT_RESPOSTAS,
        help="Planilha XLSX com as respostas do questionário.",
    )
    parser.add_argument(
        "--yaml-oficial",
        type=Path,
        default=DEFAULT_YAML_OFICIAL,
        help="YAML da estrutura iGovTI oficial.",
    )
    parser.add_argument(
        "--yaml-comparavel",
        type=Path,
        default=DEFAULT_YAML_COMPARAVEL,
        help="YAML da estrutura iGovTI ajustado comparável.",
    )
    parser.add_argument(
        "--saida-oficial",
        type=Path,
        default=DEFAULT_SAIDA_OFICIAL,
        help="Caminho de saída do XLSX oficial.",
    )
    parser.add_argument(
        "--saida-comparavel",
        type=Path,
        default=DEFAULT_SAIDA_COMPARAVEL,
        help="Caminho de saída do XLSX comparável.",
    )
    parser.add_argument(
        "--mapeamento-id",
        type=Path,
        default=DEFAULT_MAPEAMENTO,
        help="Planilha XLSX com colunas 'id' e 'orgao' para renomear registros.",
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
        help="Coluna identificadora na planilha de respostas (padrão: automático).",
    )
    return parser.parse_args()


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

    print(f"Respostas: {args.respostas}")
    df_respostas = pd.read_excel(args.respostas)
    df_dedup = deduplicar_respostas(df_respostas, mapeamento)
    removidos = len(df_respostas) - len(df_dedup)
    if removidos:
        print(f"Deduplicação: {removidos} envio(s) antigo(s) removido(s); {len(df_dedup)} órgão(s) restante(s).")

    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        caminho_temp = Path(tmp.name)
    df_dedup.to_excel(caminho_temp, index=False)

    try:
        df_oficial = calcular_igovti(
            caminho_temp,
            args.yaml_oficial,
            args.saida_oficial,
            coluna_id=coluna_id,
            mapeamento_id=mapeamento,
        )
        print(f"Oficial gerado: {args.saida_oficial} ({len(df_oficial)} registros)")

        df_comparavel = calcular_igovti(
            caminho_temp,
            args.yaml_comparavel,
            args.saida_comparavel,
            coluna_id=coluna_id,
            mapeamento_id=mapeamento,
        )
        print(f"Comparável gerado: {args.saida_comparavel} ({len(df_comparavel)} registros)")
    finally:
        caminho_temp.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
