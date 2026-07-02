#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Gera fonte larga de auditoria a partir dos ajustes pós-avaliação de evidências."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts/resources"))

from xlsx_utils import dataframe_to_xlsx_se_diferente

DEFAULT_AJUSTES = ROOT / "02-Execucao/01-Questionario/02-Ajustes_Respostas/ajustes_respostas_questionario_pos_avaliacao_evidencias.xlsx"
DEFAULT_MAPA = ROOT / "02-Execucao/03-Execucao_Procedimentos/01-Insumos/mapa-verificacao-achados.xlsx"
DEFAULT_OUTPUT = ROOT / "02-Execucao/03-Execucao_Procedimentos/99-Avaliacao_Evidencias/painel-avaliacao-evidencias.xlsx"


NAO_PARECER_REVISOR = {"", "nan", "none", "sem_parecer", "sem parecer", "não revisado", "nao revisado"}


def normalizar_texto(valor) -> str:
    if pd.isna(valor):
        return ""
    return str(valor).strip()


def normalizar_resultado(valor) -> str:
    texto = normalizar_texto(valor)
    if not texto:
        return ""
    texto = re.sub(r"\s+", " ", texto)
    texto_lower = texto.lower().replace("nao", "não")
    if texto_lower == "não conforme":
        return "Não conforme"
    if texto_lower == "conforme":
        return "Conforme"
    if texto_lower == "inconclusivo":
        return "Inconclusivo"
    return texto


def resultado_final(row: pd.Series) -> tuple[str, str]:
    avaliacao_revisor = normalizar_texto(row.get("Avaliação do auditor revisor"))
    if avaliacao_revisor.lower() not in NAO_PARECER_REVISOR:
        return normalizar_resultado(avaliacao_revisor), normalizar_texto(row.get("Justificativa do auditor revisor"))
    return (
        normalizar_resultado(row.get("Resultado da avaliação do juiz")),
        normalizar_texto(row.get("Justificativa do juiz")),
    )


def itens_do_mapa(mapa: Path) -> set[str]:
    acoes = pd.read_excel(mapa, sheet_name="Ações de Verificação", header=2)
    itens: set[str] = set()
    for valor in acoes["informacao_requerida"].dropna():
        item = str(valor).strip()
        if re.fullmatch(r"q\d{4}(?:ext)?(?:\[[^\]]+\])?", item):
            itens.add(item)
    return itens


def praticas_do_mapa(mapa: Path) -> dict[str, str]:
    acoes = pd.read_excel(mapa, sheet_name="Ações de Verificação", header=2)
    praticas: dict[str, str] = {}
    for _, row in acoes.iterrows():
        item = normalizar_texto(row.get("informacao_requerida"))
        if not re.fullmatch(r"q\d{4}(?:ext)?(?:\[[^\]]+\])?", item):
            continue
        if item in praticas:
            continue

        descricao = normalizar_texto(row.get("descricao_evidencia"))
        match = re.search(r"para verificar se\s+(.+)$", descricao, flags=re.IGNORECASE | re.DOTALL)
        if match:
            pratica = match.group(1).strip()
            pratica = re.sub(r"^a organização\s+", "", pratica, flags=re.IGNORECASE)
            praticas[item] = pratica[:1].lower() + pratica[1:]
        else:
            praticas[item] = f"a prática declarada no item {item}"
    return praticas


def gerar_fonte(ajustes: Path, output: Path, mapa: Path | None = None, itens: set[str] | None = None) -> pd.DataFrame:
    df = pd.read_excel(ajustes)

    required = {"Auditado", "Código do item avaliado", "Resposta afirmada", "Resultado da avaliação do juiz", "Justificativa do juiz"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Colunas ausentes na planilha de ajustes: {', '.join(sorted(missing))}")

    if itens is None and mapa:
        itens = itens_do_mapa(mapa)
    praticas = praticas_do_mapa(mapa) if mapa else {}

    registros: dict[str, dict[str, str]] = {}
    for _, row in df.iterrows():
        auditado = normalizar_texto(row.get("Auditado")).upper()
        item = normalizar_texto(row.get("Código do item avaliado"))
        if not auditado or not item:
            continue
        if itens is not None and item not in itens:
            continue

        resultado, justificativa = resultado_final(row)
        if resultado != "Não conforme":
            continue

        registro = registros.setdefault(auditado, {"Auditado": auditado})
        registro[item] = resultado
        registro[f"{item}__resposta_afirmada"] = normalizar_texto(row.get("Resposta afirmada"))
        registro[f"{item}__justificativa"] = justificativa
        registro[f"{item}__pratica"] = praticas.get(item, f"a prática declarada no item {item}")

    if not registros:
        result = pd.DataFrame(columns=["Auditado"])
    else:
        result = pd.DataFrame(sorted(registros.values(), key=lambda item: item["Auditado"]))

    dataframe_to_xlsx_se_diferente(
        result,
        output,
        index=False,
        sheet_name="Ajustes Evidencias Auditoria",
    )

    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Gera fonte larga para ações de auditoria baseadas em ajustes pós-avaliação de evidências."
    )
    parser.add_argument("--ajustes", type=Path, default=DEFAULT_AJUSTES, help="Planilha de ajustes pós-avaliação de evidências.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Arquivo XLSX de saída.")
    parser.add_argument("--mapa", type=Path, default=DEFAULT_MAPA, help="Mapa de verificação usado para filtrar itens e inferir práticas.")
    parser.add_argument(
        "--todos-itens",
        action="store_true",
        help="Exporta todos os itens não conformes, sem restringir aos itens já usados no mapa.",
    )
    args = parser.parse_args()

    itens = None if args.todos_itens else itens_do_mapa(args.mapa)
    result = gerar_fonte(args.ajustes, args.output, mapa=args.mapa, itens=itens)

    itens_exportados = sorted(
        col for col in result.columns
        if re.fullmatch(r"q\d{4}(?:ext)?(?:\[[^\]]+\])?", str(col))
    )
    print(f"Fonte gerada: {args.output}")
    print(f"Auditados com ajustes exportados: {len(result)}")
    print(f"Itens exportados: {len(itens_exportados)}")


if __name__ == "__main__":
    main()
