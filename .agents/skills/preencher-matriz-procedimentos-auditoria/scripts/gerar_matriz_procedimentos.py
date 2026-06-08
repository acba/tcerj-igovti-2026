#!/usr/bin/env python3
"""Gera matriz de procedimentos de auditoria a partir de matriz Markdown."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter


FONTES_HEADERS = ["id", "descricao", "filepath", "chave_jurisdicionado"]
PROCEDIMENTOS_HEADERS = ["id", "descricao", "logica_achado", "numero_achado", "nome_achado"]
ACOES_HEADERS = [
    "id",
    "id_fonte_informacao",
    "acao_exclusiva_auditados",
    "auditado_inexistente_e_achado",
    "descricao_auditado_inexistente",
    "informacao_requerida",
    "criterio",
    "descricao_evidencia",
    "complemento_evidencia",
    "descricao_situacao_inconforme",
    "situacao_inconforme",
    "situacao_encontrada_nan_e_achado",
    "decodifica_sit_encontrada",
    "tipo_encaminhamento",
    "pre_encaminhamento",
    "encaminhamento",
]


@dataclass
class Situacao:
    codigo: str
    descricao: str = ""
    regras: list[str] = field(default_factory=list)
    criterios: list[str] = field(default_factory=list)
    encaminhamento: str = ""


@dataclass
class Achado:
    codigo: str
    nome: str
    questao_codigo: str
    questao_texto: str
    criterios: dict[str, str]
    situacoes: list[Situacao] = field(default_factory=list)


@dataclass
class Action:
    id: str
    source_id: str
    informacao_requerida: str
    criterio: str
    descricao_evidencia: str
    descricao_situacao_inconforme: str
    situacao_inconforme: str
    tipo_encaminhamento: str
    encaminhamento: str


def split_sections(text: str) -> list[str]:
    matches = list(re.finditer(r"^## Questão \d+.*$", text, flags=re.MULTILINE))
    sections = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append(text[match.start() : end])
    return sections


def parse_keyed_list(section: str, key: str) -> dict[str, str]:
    block = extract_named_block(section, key)
    result: dict[str, str] = {}
    for line in block.splitlines():
        match = re.match(r"\s*-\s*([A-Z]+\d+(?:\.\d+)?):\s*(.+)", line)
        if match:
            result[match.group(1)] = match.group(2).strip()
    return result


def extract_named_block(section: str, name: str) -> str:
    pattern = rf"^{re.escape(name)}:\s*$"
    match = re.search(pattern, section, flags=re.MULTILINE)
    if not match:
        return ""
    start = match.end()
    next_match = re.search(
        r"^(subquestoes|riscos|fontes_de_informacao|informacoes_requeridas|criterios|procedimentos|evidencias|possiveis_achados|natureza|gera_achado):\s*$",
        section[start:],
        flags=re.MULTILINE,
    )
    end = start + next_match.start() if next_match else len(section)
    return section[start:end]


def parse_inline_list(value: str) -> list[str]:
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]
    return [item.strip().strip("'\"") for item in value.split(",") if item.strip()]


def field_value(block: str, field_name: str) -> str:
    match = re.search(rf"^\s*{re.escape(field_name)}:\s*(.+?)\s*$", block, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def list_field(block: str, field_name: str) -> list[str]:
    value = field_value(block, field_name)
    return parse_inline_list(value) if value else []


def rule_lines(block: str) -> list[str]:
    lines = block.splitlines()
    rules: list[str] = []
    collecting = False
    for line in lines:
        if re.match(r"^\s*regra_de_identificacao:\s*$", line):
            collecting = True
            continue
        if not collecting:
            continue
        if re.match(r"^\s*[a-zA-Z_]+:\s*", line):
            break
        match = re.match(r"^\s*-\s*(.+)", line)
        if match:
            rules.append(match.group(1).strip())
    return rules


def parse_situacoes(achado_block: str) -> list[Situacao]:
    matches = list(re.finditer(r"^\s*-\s*(S\d+\.\d+):\s*$", achado_block, flags=re.MULTILINE))
    situacoes: list[Situacao] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(achado_block)
        block = achado_block[match.end() : end]
        situacoes.append(
            Situacao(
                codigo=match.group(1),
                descricao=field_value(block, "descricao"),
                regras=rule_lines(block),
                criterios=list_field(block, "criterios"),
                encaminhamento=field_value(block, "encaminhamento"),
            )
        )
    return situacoes


def parse_achados(section: str) -> list[Achado]:
    questao_match = re.search(r"questao:\s*(Q\d+)\.\s*(.+)", section)
    questao_codigo = questao_match.group(1) if questao_match else ""
    questao_texto = questao_match.group(2).strip() if questao_match else ""
    criterios = parse_keyed_list(section, "criterios")
    block = extract_named_block(section, "possiveis_achados")
    matches = list(re.finditer(r"^\s*-\s*(A\d+):\s*(.+)$", block, flags=re.MULTILINE))
    achados: list[Achado] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(block)
        achado_block = block[match.end() : end]
        achado = Achado(
            codigo=match.group(1),
            nome=match.group(2).strip(),
            questao_codigo=questao_codigo,
            questao_texto=questao_texto,
            criterios=criterios,
            situacoes=parse_situacoes(achado_block),
        )
        achados.append(achado)
    return achados


def parse_matrix(path: Path) -> list[Achado]:
    text = path.read_text(encoding="utf-8")
    achados: list[Achado] = []
    for section in split_sections(text):
        achados.extend(parse_achados(section))
    return achados


def refs_from_rule(rule: str) -> tuple[list[str], list[str]]:
    avaliacao_refs = re.findall(r"avaliacao\[([^\]]+)\]", rule)
    rule_without_avaliacao = re.sub(r"avaliacao\[[^\]]+\]", "", rule)
    q_refs = re.findall(
        r"\b(q\d{4}(?:ext\[[A-Za-z0-9_]+\]|\[[A-Za-z0-9_]+\]|evi[A-Za-z0-9_]*)?)\b",
        rule_without_avaliacao,
    )
    return q_refs, avaliacao_refs


def source_for_rule(rule: str) -> str:
    q_refs, avaliacao_refs = refs_from_rule(rule)
    if q_refs and avaliacao_refs:
        return "questionario_e_avaliacao_evidencias"
    if avaliacao_refs:
        return "avaliacao_evidencias"
    return "questionario"


def info_for_rule(rule: str) -> str:
    q_refs, avaliacao_refs = refs_from_rule(rule)
    refs = [*q_refs, *avaliacao_refs]
    return "; ".join(dict.fromkeys(refs)) if refs else rule


def criterion_text(achado: Achado, situacao: Situacao) -> str:
    refs = situacao.criterios or list(achado.criterios)
    texts = []
    for ref in refs:
        texts.append(achado.criterios.get(ref, ref))
    return "\n".join(dict.fromkeys(texts))


def encaminhamento_tipo(text: str) -> str:
    low = text.strip().casefold()
    if low.startswith("determinar"):
        return "Determinação"
    if low.startswith("recomendar"):
        return "Recomendação"
    return "Recomendação"


def normalize_rule(rule: str) -> str:
    rule = re.sub(r"^\s*ou\s+", "", rule.strip(), flags=re.IGNORECASE)
    return rule


def build_actions(achados: list[Achado], start: int = 1) -> tuple[dict[str, list[str]], list[Action]]:
    actions_by_achado: dict[str, list[str]] = {}
    actions: list[Action] = []
    counter = start
    for achado in achados:
        action_ids = []
        for situacao in achado.situacoes:
            regras = situacao.regras or [situacao.descricao]
            for rule in regras:
                action_id = f"AV{counter:02d}"
                counter += 1
                normalized = normalize_rule(rule)
                action_ids.append(action_id)
                actions.append(
                    Action(
                        id=action_id,
                        source_id=source_for_rule(normalized),
                        informacao_requerida=info_for_rule(normalized),
                        criterio=criterion_text(achado, situacao),
                        descricao_evidencia=(
                            f"Aplicação da regra {normalized} para verificar a situação {situacao.codigo}: "
                            f"{situacao.descricao}"
                        ),
                        descricao_situacao_inconforme=situacao.descricao,
                        situacao_inconforme=normalized,
                        tipo_encaminhamento=encaminhamento_tipo(situacao.encaminhamento),
                        encaminhamento=situacao.encaminhamento,
                    )
                )
        actions_by_achado[achado.codigo] = action_ids
    return actions_by_achado, actions


def procedure_description(achado: Achado) -> str:
    if achado.questao_texto:
        return f"Procedimento para verificar a questão {achado.questao_codigo}: {achado.questao_texto}"
    return f"Procedimento para verificar o possível achado {achado.codigo}: {achado.nome}"


def logic_expression(action_ids: list[str]) -> str:
    if not action_ids:
        return ""
    return "(" + " | ".join(action_ids) + ")"


def create_workbook(
    achados: list[Achado],
    actions_by_achado: dict[str, list[str]],
    actions: list[Action],
    *,
    questionario_filepath: str,
    avaliacao_filepath: str,
    chave_questionario: str,
    chave_avaliacao: str,
) -> Workbook:
    workbook = Workbook()
    ws_fontes = workbook.active
    ws_fontes.title = "Fontes de Informação"
    ws_proc = workbook.create_sheet("Procedimentos de Auditoria")
    ws_acoes = workbook.create_sheet("Ações de Verificação")

    write_header(ws_fontes, FONTES_HEADERS)
    source_ids = {action.source_id for action in actions}
    source_rows = []
    if any("questionario" in source for source in source_ids):
        source_rows.append(["questionario", "Questionário eletrônico iGovTI", questionario_filepath, chave_questionario])
    if any("avaliacao_evidencias" in source for source in source_ids):
        source_rows.append(
            ["avaliacao_evidencias", "Resultados de avaliação das evidências por prompt", avaliacao_filepath, chave_avaliacao]
        )
    if "questionario_e_avaliacao_evidencias" in source_ids:
        source_rows.append(
            [
                "questionario_e_avaliacao_evidencias",
                "Questionário eletrônico iGovTI combinado com resultados de avaliação das evidências",
                f"{questionario_filepath}; {avaliacao_filepath}",
                f"{chave_questionario}; {chave_avaliacao}",
            ]
        )
    for row in source_rows:
        ws_fontes.append(row)

    write_header(ws_proc, PROCEDIMENTOS_HEADERS)
    for index, achado in enumerate(achados, start=1):
        ws_proc.append(
            [
                f"PA{index:02d}",
                procedure_description(achado),
                logic_expression(actions_by_achado.get(achado.codigo, [])),
                index,
                achado.nome,
            ]
        )

    write_actions_intro(ws_acoes)
    write_header(ws_acoes, ACOES_HEADERS)
    for action in actions:
        ws_acoes.append(
            [
                action.id,
                action.source_id,
                None,
                None,
                None,
                action.informacao_requerida,
                action.criterio,
                action.descricao_evidencia,
                None,
                action.descricao_situacao_inconforme,
                action.situacao_inconforme,
                None,
                None,
                action.tipo_encaminhamento,
                None,
                action.encaminhamento,
            ]
        )

    style_workbook(workbook)
    return workbook


def write_header(ws: Any, headers: list[str]) -> None:
    for index, header in enumerate(headers, start=1):
        ws.cell(row=3, column=index, value=header)


def write_actions_intro(ws: Any) -> None:
    notes = [
        "Identificador da ação de verificação",
        "Fonte de informação usada na ação",
        "Lista opcional de auditados aos quais a ação se aplica",
        "TRUE se inexistência do auditado na fonte configura achado",
        "Texto da evidência se o auditado não constar da fonte",
        "Coluna, campo ou target avaliado",
        "Critério aplicável",
        "Descrição da evidência",
        "Complemento opcional",
        "Descrição da situação inconforme",
        "Valor ou expressão de inconformidade",
        "TRUE se dado vazio configura achado",
    ]
    for index, note in enumerate(notes, start=1):
        ws.cell(row=2, column=index, value=note)


def style_workbook(workbook: Workbook) -> None:
    widths = {
        "A": 14,
        "B": 28,
        "C": 36,
        "D": 24,
        "E": 38,
        "F": 28,
        "G": 54,
        "H": 72,
        "I": 18,
        "J": 56,
        "K": 42,
        "L": 24,
        "M": 24,
        "N": 22,
        "O": 28,
        "P": 72,
    }
    header_fill = PatternFill("solid", fgColor="D9EAF7")
    for ws in workbook.worksheets:
        for col, width in widths.items():
            ws.column_dimensions[col].width = width
        for cell in ws[3]:
            if cell.value:
                cell.font = Font(bold=True)
                cell.fill = header_fill
                cell.alignment = Alignment(wrap_text=True, vertical="top")
        for row in ws.iter_rows():
            for cell in row:
                cell.alignment = Alignment(wrap_text=True, vertical="top")
        ws.freeze_panes = "A4"
        if ws.max_row >= 3 and ws.max_column >= 1:
            ws.auto_filter.ref = f"A3:{get_column_letter(ws.max_column)}{ws.max_row}"


def check_workbook(path: Path) -> int:
    workbook = load_workbook(path, read_only=True, data_only=True)
    errors: list[str] = []
    try:
        required = {
            "Fontes de Informação": FONTES_HEADERS,
            "Procedimentos de Auditoria": PROCEDIMENTOS_HEADERS,
            "Ações de Verificação": ACOES_HEADERS,
        }
        for sheet_name, headers in required.items():
            if sheet_name not in workbook.sheetnames:
                errors.append(f"aba ausente: {sheet_name}")
                continue
            ws = workbook[sheet_name]
            actual = [ws.cell(3, index).value for index in range(1, len(headers) + 1)]
            if actual != headers:
                errors.append(f"cabecalho invalido em {sheet_name}: {actual}")
    finally:
        workbook.close()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("OK")
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("matriz", nargs="?", help="Arquivo matriz_planejamento.md")
    parser.add_argument("saida", nargs="?", help="Planilha .xlsx de saida")
    parser.add_argument("--check", action="store_true", help="Valida contrato basico da planilha indicada em SAIDA")
    parser.add_argument("--questionario-filepath", default="01-Coleta_Dados/20260607-respostas-questionario.xlsx")
    parser.add_argument(
        "--avaliacao-filepath",
        default="02-Testes_Auditoria/avaliacao_evidencias/resultados_avaliacao_evidencias.xlsx",
    )
    parser.add_argument("--chave-questionario", default="firstname")
    parser.add_argument("--chave-avaliacao", default="auditado")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.check:
        target = Path(args.saida or args.matriz or "")
        if not target:
            raise SystemExit("--check requer caminho da planilha")
        return check_workbook(target)
    if not args.matriz or not args.saida:
        raise SystemExit("uso: gerar_matriz_procedimentos.py MATRIZ_MD SAIDA_XLSX")
    matriz = Path(args.matriz)
    saida = Path(args.saida)
    achados = parse_matrix(matriz)
    actions_by_achado, actions = build_actions(achados)
    workbook = create_workbook(
        achados,
        actions_by_achado,
        actions,
        questionario_filepath=args.questionario_filepath,
        avaliacao_filepath=args.avaliacao_filepath,
        chave_questionario=args.chave_questionario,
        chave_avaliacao=args.chave_avaliacao,
    )
    saida.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(saida)
    print(f"OK: {len(achados)} procedimentos, {len(actions)} ações -> {saida}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
