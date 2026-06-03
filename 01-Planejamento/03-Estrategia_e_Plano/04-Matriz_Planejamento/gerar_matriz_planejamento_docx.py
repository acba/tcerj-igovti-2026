#!/usr/bin/env python3
"""Gera matriz de planejamento DOCX a partir de Markdown estruturado.

O script usa um DOCX existente como template OpenXML e substitui o corpo do
documento por tabelas preenchidas com os dados da matriz Markdown.
"""

from __future__ import annotations

import argparse
import copy
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_TEMPLATE = BASE_DIR / "02-Matriz de Planejamento Pós Revisão da Sub.docx"
DEFAULT_OUTPUT = BASE_DIR / "matriz_planejamento_gerada.docx"
MISSING_MARKDOWN_PLACEHOLDER = "[NÃO LOCALIZADO NO MARKDOWN]"

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
XML_NS = "http://www.w3.org/XML/1998/namespace"
W = f"{{{W_NS}}}"
R = f"{{{R_NS}}}"
XML = f"{{{XML_NS}}}"

ET.register_namespace("w", W_NS)
ET.register_namespace("r", R_NS)
ET.register_namespace("xml", XML_NS)


FIELDS = [
    "natureza",
    "gera_achado",
    "questao",
    "subquestoes",
    "riscos",
    "fontes_de_informacao",
    "informacoes_requeridas",
    "criterios",
    "criterios_de_comparabilidade",
    "procedimentos",
    "evidencias",
    "possiveis_achados",
    "o_que_a_analise_permite_dizer",
    "limitacoes_e_cautelas",
]


@dataclass
class ListItem:
    id: str
    text: str
    raw: str
    refs: list[str] = field(default_factory=list)


@dataclass
class CellParagraph:
    text: str
    bold: bool | None = None
    left_indent: int = 0
    spacing_after: int = 120


@dataclass
class Situation:
    id: str
    descricao: str = ""
    severidade: str = ""
    itens: list[str] = field(default_factory=list)
    regra: list[str] = field(default_factory=list)
    referencias: list[str] = field(default_factory=list)
    criterios: list[str] = field(default_factory=list)
    encaminhamento: str = ""


@dataclass
class Finding:
    id: str
    title: str
    situacoes: list[Situation] = field(default_factory=list)


@dataclass
class Question:
    id: str
    title: str
    question: str
    natureza: str = ""
    gera_achado: bool = True
    subquestoes: list[ListItem] = field(default_factory=list)
    riscos: list[ListItem] = field(default_factory=list)
    fontes: list[ListItem] = field(default_factory=list)
    informacoes: list[ListItem] = field(default_factory=list)
    criterios: list[ListItem] = field(default_factory=list)
    criterios_comparabilidade: list[ListItem] = field(default_factory=list)
    procedimentos: list[ListItem] = field(default_factory=list)
    evidencias: list[ListItem] = field(default_factory=list)
    achados: list[Finding] = field(default_factory=list)
    analise_permite_dizer: list[ListItem] = field(default_factory=list)
    limitacoes: list[ListItem] = field(default_factory=list)


@dataclass
class Matrix:
    title: str
    questao_geral: str
    questions: list[Question]


def normalize_text(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def split_csv_list(value: str) -> list[str]:
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]
    return [part.strip() for part in value.split(",") if part.strip()]


def get_single_line(content: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", content, flags=re.M)
    return match.group(1).strip() if match else ""


def get_section_block(content: str, field_name: str) -> str:
    match = re.search(rf"^{re.escape(field_name)}:\s*$", content, flags=re.M)
    if not match:
        return ""
    start = match.end()
    rest = content[start:]
    next_match = re.search(
        r"\n(?:" + "|".join(re.escape(field) for field in FIELDS) + r"):\s*$|\n---\s*$",
        rest,
        flags=re.M,
    )
    return (rest[: next_match.start()] if next_match else rest).strip()


def parse_bool(value: str, default: bool = True) -> bool:
    if not value:
        return default
    return value.strip().lower() in {"true", "sim", "yes", "1"}


def parse_item(text: str) -> ListItem:
    raw = text.strip()
    item_id = ""
    item_text = raw
    match = re.match(r"^([A-Z]{1,4}\d+(?:\.\d+)?|CT\d+):\s*(.+)$", raw)
    if match:
        item_id = match.group(1)
        item_text = match.group(2).strip()
    refs_match = re.search(r"\[([^\]]+)\]\s*$", raw)
    refs = split_csv_list(refs_match.group(1)) if refs_match else []
    return ListItem(item_id, item_text, raw, refs)


def parse_list(block: str) -> list[ListItem]:
    items: list[ListItem] = []
    current: str | None = None
    for line in normalize_text(block).split("\n"):
        if not line.strip():
            continue
        bullet = re.match(r"^\s*-\s+(.+)$", line)
        if bullet:
            if current:
                items.append(parse_item(current))
            current = bullet.group(1).strip()
        elif current:
            current += " " + line.strip()
    if current:
        items.append(parse_item(current))
    return items


def parse_findings(block: str) -> list[Finding]:
    findings: list[Finding] = []
    current_finding: Finding | None = None
    current_situation: Situation | None = None
    current_prop = ""

    def finish_situation() -> None:
        nonlocal current_situation, current_prop
        if current_finding and current_situation:
            current_finding.situacoes.append(current_situation)
        current_situation = None
        current_prop = ""

    def finish_finding() -> None:
        nonlocal current_finding
        finish_situation()
        if current_finding:
            findings.append(current_finding)
        current_finding = None

    for line in normalize_text(block).split("\n"):
        finding_match = re.match(r"^\s*-\s+(A\d+):\s*(.+)$", line)
        if finding_match:
            finish_finding()
            current_finding = Finding(finding_match.group(1), finding_match.group(2).strip())
            continue

        situation_match = re.match(r"^\s*-\s+(S\d+\.\d+):\s*$", line)
        if situation_match:
            finish_situation()
            current_situation = Situation(situation_match.group(1))
            continue

        if not current_situation:
            continue

        prop_match = re.match(r"^\s{4,}([a-zA-Z_]+):\s*(.*)$", line)
        if prop_match:
            current_prop = prop_match.group(1)
            value = prop_match.group(2).strip()
            assign_situation_prop(current_situation, current_prop, value)
            continue

        list_item = re.match(r"^\s{4,}-\s+(.+)$", line)
        if list_item and current_prop == "regra_de_identificacao":
            current_situation.regra.append(list_item.group(1).strip())
            continue

        if line.strip() and current_prop == "encaminhamento":
            current_situation.encaminhamento = (current_situation.encaminhamento + " " + line.strip()).strip()

    finish_finding()
    return findings


def assign_situation_prop(situation: Situation, prop: str, value: str) -> None:
    if prop == "descricao":
        situation.descricao = value
    elif prop == "severidade":
        situation.severidade = value
    elif prop in {"itens_questionario", "fontes_de_verificacao"}:
        situation.itens = split_csv_list(value)
    elif prop == "referencias_matriz":
        situation.referencias = split_csv_list(value)
    elif prop == "criterios":
        situation.criterios = split_csv_list(value)
    elif prop == "encaminhamento":
        situation.encaminhamento = value
    elif prop == "regra_de_identificacao":
        situation.regra = []


def parse_matrix(markdown: str) -> Matrix:
    text = normalize_text(markdown)
    title_match = re.search(r'^title:\s*"([^"]+)"', text, flags=re.M)
    title = title_match.group(1) if title_match else "Matriz de Planejamento"
    questao_geral = get_single_line(text, "questao_geral") or "[QUESTÃO GERAL DE AUDITORIA]"

    matches = list(re.finditer(r"^## Questão(?:\s+(\d+)|\s+Transversal)\s*-\s*(.+)$", text, flags=re.M))
    questions: list[Question] = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        content = text[start:end]
        raw_number = match.group(1) or ""
        q_id = f"Q{int(raw_number)}" if raw_number else "QT"
        natureza = get_single_line(content, "natureza")
        gera_achado = parse_bool(get_single_line(content, "gera_achado"), default=True)
        q = Question(
            id=q_id,
            title=match.group(2).strip(),
            question=get_single_line(content, "questao") or f"{q_id}. [QUESTÃO DE AUDITORIA]",
            natureza=natureza,
            gera_achado=gera_achado,
            subquestoes=parse_list(get_section_block(content, "subquestoes")),
            riscos=parse_list(get_section_block(content, "riscos")),
            fontes=parse_list(get_section_block(content, "fontes_de_informacao")),
            informacoes=parse_list(get_section_block(content, "informacoes_requeridas")),
            criterios=parse_list(get_section_block(content, "criterios")),
            criterios_comparabilidade=parse_list(get_section_block(content, "criterios_de_comparabilidade")),
            procedimentos=parse_list(get_section_block(content, "procedimentos")),
            evidencias=parse_list(get_section_block(content, "evidencias")),
            achados=parse_findings(get_section_block(content, "possiveis_achados")) if gera_achado else [],
            analise_permite_dizer=parse_list(get_section_block(content, "o_que_a_analise_permite_dizer")),
            limitacoes=parse_list(get_section_block(content, "limitacoes_e_cautelas")),
        )
        questions.append(q)

    return Matrix(title, questao_geral, questions)


def local_name(element: ET.Element) -> str:
    return element.tag.rsplit("}", 1)[-1]


def text_of(element: ET.Element) -> str:
    return "".join(t.text or "" for t in element.findall(f".//{W}t"))


def ensure_child(element: ET.Element, tag: str) -> ET.Element:
    child = element.find(tag)
    if child is None:
        child = ET.Element(tag)
        element.insert(0, child)
    return child


def set_paragraph_layout(paragraph: ET.Element, *, left_indent: int = 0, spacing_after: int | None = None) -> None:
    ppr = ensure_child(paragraph, f"{W}pPr")
    if left_indent:
        ind = ppr.find(f"{W}ind")
        if ind is None:
            ind = ET.SubElement(ppr, f"{W}ind")
        ind.set(f"{W}left", str(left_indent))
    if spacing_after is not None:
        spacing = ppr.find(f"{W}spacing")
        if spacing is None:
            spacing = ET.SubElement(ppr, f"{W}spacing")
        spacing.set(f"{W}after", str(spacing_after))


def set_paragraph_text(paragraph: ET.Element, text: str, *, bold: bool | None = None) -> None:
    first_run = paragraph.find(f"{W}r")
    base_rpr = copy.deepcopy(first_run.find(f"{W}rPr")) if first_run is not None and first_run.find(f"{W}rPr") is not None else ET.Element(f"{W}rPr")
    if bold is not None:
        for tag in ("b", "bCs"):
            existing = base_rpr.find(f"{W}{tag}")
            if bold and existing is None:
                ET.SubElement(base_rpr, f"{W}{tag}")
            elif not bold and existing is not None:
                base_rpr.remove(existing)

    for child in list(paragraph):
        if local_name(child) != "pPr":
            paragraph.remove(child)

    run = ET.SubElement(paragraph, f"{W}r")
    if len(base_rpr):
        run.append(base_rpr)
    text_el = ET.SubElement(run, f"{W}t")
    if text[:1].isspace() or text[-1:].isspace():
        text_el.set(f"{XML}space", "preserve")
    text_el.text = text


def clone_paragraph(
    template: ET.Element,
    text: str,
    *,
    bold: bool | None = None,
    left_indent: int = 0,
    spacing_after: int | None = None,
) -> ET.Element:
    paragraph = copy.deepcopy(template)
    set_paragraph_text(paragraph, text, bold=bold)
    set_paragraph_layout(paragraph, left_indent=left_indent, spacing_after=spacing_after)
    return paragraph


def clear_cell(cell: ET.Element) -> None:
    for child in list(cell):
        if local_name(child) != "tcPr":
            cell.remove(child)


def normalize_cell_paragraph(value: str | CellParagraph, *, bold: bool | None, spacing_after: int) -> CellParagraph:
    if isinstance(value, CellParagraph):
        paragraph = copy.copy(value)
        if paragraph.bold is None:
            paragraph.bold = bold
        return paragraph
    return CellParagraph(str(value), bold=bold, spacing_after=spacing_after)


def fill_cell(
    cell: ET.Element,
    texts: Iterable[str | CellParagraph],
    paragraph_template: ET.Element,
    *,
    bold: bool | None = None,
    spacing_after: int = 120,
) -> None:
    clear_cell(cell)
    values: list[CellParagraph] = []
    for value in texts:
        if isinstance(value, CellParagraph):
            if value.text.strip():
                values.append(normalize_cell_paragraph(value, bold=bold, spacing_after=spacing_after))
        elif value and str(value).strip():
            values.append(normalize_cell_paragraph(value, bold=bold, spacing_after=spacing_after))
    if not values:
        values = [CellParagraph(MISSING_MARKDOWN_PLACEHOLDER, bold=bold, spacing_after=spacing_after)]
    for value in values:
        cell.append(
            clone_paragraph(
                paragraph_template,
                value.text,
                bold=value.bold,
                left_indent=value.left_indent,
                spacing_after=value.spacing_after,
            )
        )


def first_paragraph(cell: ET.Element) -> ET.Element:
    paragraph = cell.find(f"{W}p")
    if paragraph is None:
        paragraph = ET.Element(f"{W}p")
    return paragraph


def move_leading_markdown_link_to_end(text: str) -> str:
    match = re.match(r"^(\[[^\]]+\]\([^)]+\)|https?://\S+)\s+(.+)$", text.strip())
    if not match:
        return text
    return f"{match.group(2).strip()} {match.group(1).strip()}"


def format_items(items: Iterable[ListItem]) -> list[str]:
    return [item.raw for item in items] or [MISSING_MARKDOWN_PLACEHOLDER]


def format_question_text(question: Question) -> str:
    text = re.sub(r"^Q[T\d]+\.\s*", "", question.question).strip()
    prefix = question.id
    if question.natureza:
        return f"{prefix}: {text} ({question.natureza})"
    return f"{prefix}: {text}"


def format_risk_or_comparability(question: Question) -> list[str]:
    if question.riscos:
        return format_items(question.riscos)
    if question.criterios_comparabilidade:
        return ["Critérios de comparabilidade:"] + format_items(question.criterios_comparabilidade)
    return [MISSING_MARKDOWN_PLACEHOLDER]


def format_criteria(question: Question) -> list[str]:
    criteria = list(question.criterios)
    if question.criterios_comparabilidade:
        criteria.extend(question.criterios_comparabilidade)
    return [move_leading_markdown_link_to_end(item) for item in format_items(criteria)]


def format_findings_or_analysis(question: Question) -> list[str | CellParagraph]:
    lines: list[str | CellParagraph] = []
    for finding in question.achados:
        if finding.title:
            lines.append(CellParagraph(f"{finding.id}: {finding.title}", bold=True, left_indent=0, spacing_after=80))
        for situation in finding.situacoes:
            parts = [f"{situation.id}: {situation.descricao}"]
            if situation.severidade:
                parts.append(f"Severidade: {situation.severidade}")
            if situation.referencias:
                parts.append(f"Referências: {', '.join(situation.referencias)}")
            if situation.encaminhamento:
                parts.append(f"Encaminhamento: {situation.encaminhamento}")
            lines.append(CellParagraph("- " + "; ".join(parts), left_indent=360, spacing_after=120))

    if lines:
        return lines

    if not question.gera_achado or question.natureza:
        lines.append("Não se aplica: questão de levantamento, sem geração de achado individual.")
        if question.analise_permite_dizer:
            lines.append("O que a análise permite dizer:")
            lines.extend(format_items(question.analise_permite_dizer))
        if question.limitacoes:
            lines.append("Limitações e cautelas:")
            lines.extend(format_items(question.limitacoes))
        return lines

    return [MISSING_MARKDOWN_PLACEHOLDER]


def build_question_table(template_table: ET.Element, question: Question) -> ET.Element:
    table = copy.deepcopy(template_table)
    rows = table.findall(f"{W}tr")
    if len(rows) < 4:
        raise ValueError("A tabela modelo deve possuir pelo menos 4 linhas.")

    row0_cell = rows[0].find(f"{W}tc")
    row1_cell = rows[1].find(f"{W}tc")
    header_cells = rows[2].findall(f"{W}tc")
    data_cells = rows[3].findall(f"{W}tc")
    if row0_cell is None or row1_cell is None or len(header_cells) < 6 or len(data_cells) < 6:
        raise ValueError("A tabela modelo deve possuir a estrutura 6-colunas esperada.")

    row0_templates = row0_cell.findall(f"{W}p")
    question_p = row0_templates[0] if row0_templates else ET.Element(f"{W}p")
    subquestion_p = row0_templates[1] if len(row0_templates) > 1 else question_p
    risk_p = first_paragraph(row1_cell)

    clear_cell(row0_cell)
    row0_cell.append(clone_paragraph(question_p, format_question_text(question)))
    for subquestion in question.subquestoes:
        row0_cell.append(clone_paragraph(subquestion_p, subquestion.text))

    fill_cell(row1_cell, format_risk_or_comparability(question), risk_p)

    headers = [
        "FONTES DE INFORMAÇÃO",
        "INFORMAÇÕES REQUERIDAS",
        "CRITÉRIOS",
        "PROCEDIMENTO DE AUDITORIA",
        "POSSÍVEIS EVIDÊNCIAS",
        "POSSÍVEIS ACHADOS" if question.gera_achado else "ANÁLISE / RESULTADOS",
    ]
    for cell, header in zip(header_cells, headers):
        fill_cell(cell, [header], first_paragraph(cell), bold=True, spacing_after=0)

    cell_payloads = [
        format_items(question.fontes),
        format_items(question.informacoes),
        format_criteria(question),
        format_items(question.procedimentos),
        format_items(question.evidencias),
        format_findings_or_analysis(question),
    ]
    for cell, payload in zip(data_cells, cell_payloads):
        fill_cell(cell, payload, first_paragraph(cell))

    return table


def find_template_parts(body: ET.Element) -> tuple[list[ET.Element], ET.Element, list[ET.Element], ET.Element]:
    children = list(body)
    tables = [child for child in children if local_name(child) == "tbl"]
    if not tables:
        raise ValueError("Template sem tabela de matriz.")
    matrix_table = tables[0]
    signature_table = tables[-1] if len(tables[-1].findall(f"{W}tr")) <= 6 else None
    sect_pr = children[-1] if children and local_name(children[-1]) == "sectPr" else ET.Element(f"{W}sectPr")
    intro = children[:5] if len(children) >= 5 else children[:]
    separator = [child for child in children[6:8] if local_name(child) == "p"] or [ET.Element(f"{W}p")]
    return intro, matrix_table, ([signature_table] if signature_table is not None and signature_table is not matrix_table else []), sect_pr


def replace_intro_text(intro: list[ET.Element], matrix: Matrix, jurisdicionados: str) -> list[ET.Element]:
    result = [copy.deepcopy(element) for element in intro]
    text_paragraphs = [element for element in result if local_name(element) == "p"]
    non_empty = [p for p in text_paragraphs if text_of(p).strip()]
    if non_empty:
        set_paragraph_text(non_empty[0], "MATRIZ DE PLANEJAMENTO", bold=True)
    if len(non_empty) > 1:
        set_paragraph_text(non_empty[1], f"QUESTÃO GERAL DE AUDITORIA: {matrix.questao_geral}")

    if jurisdicionados:
        template = non_empty[1] if len(non_empty) > 1 else (text_paragraphs[-1] if text_paragraphs else ET.Element(f"{W}p"))
        result.append(clone_paragraph(template, f"JURISDICIONADOS: {jurisdicionados}"))
    return result


def generate_docx(template_path: Path, markdown_path: Path, output_path: Path, jurisdicionados: str) -> None:
    matrix = parse_matrix(markdown_path.read_text(encoding="utf-8"))
    if not matrix.questions:
        raise ValueError("Nenhuma questão foi encontrada no Markdown.")

    with ZipFile(template_path, "r") as zin:
        document_xml = zin.read("word/document.xml")
        root = ET.fromstring(document_xml)
        body = root.find(f"{W}body")
        if body is None:
            raise ValueError("Template DOCX sem word/body.")
        intro, table_template, signature_parts, sect_pr = find_template_parts(body)

        for child in list(body):
            body.remove(child)

        for element in replace_intro_text(intro, matrix, jurisdicionados):
            body.append(element)

        blank_paragraph = ET.Element(f"{W}p")
        for question in matrix.questions:
            body.append(build_question_table(table_template, question))
            body.append(copy.deepcopy(blank_paragraph))

        for part in signature_parts:
            body.append(copy.deepcopy(blank_paragraph))
            body.append(copy.deepcopy(part))

        body.append(copy.deepcopy(sect_pr))
        new_document = ET.tostring(root, encoding="utf-8", xml_declaration=True)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with ZipFile(output_path, "w", ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = new_document if item.filename == "word/document.xml" else zin.read(item.filename)
                zout.writestr(item, data)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Gera DOCX da matriz de planejamento a partir de Markdown estruturado.")
    parser.add_argument("markdown", type=Path, help="Markdown da matriz de planejamento.")
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE, help="DOCX usado como template.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="DOCX de saída.")
    parser.add_argument("--jurisdicionados", default="[JURISDICIONADOS]", help="Texto para o campo de jurisdicionados.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        generate_docx(args.template, args.markdown, args.output, args.jurisdicionados)
    except Exception as exc:  # noqa: BLE001 - mensagem amigável para CLI
        print(f"Erro ao gerar DOCX: {exc}", file=sys.stderr)
        return 1
    print(f"DOCX gerado: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
