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


REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.gerar_matriz_planejamento import parse_matrix as parse_planning_matrix  # noqa: E402


FONTES_HEADERS = ["id", "descricao", "filepath", "chave_jurisdicionado"]
PROCEDIMENTOS_HEADERS = ["id", "descricao", "logica_achado", "numero_achado", "nome_achado"]
VARIAVEIS_HEADERS = ["id", "id_fonte_informacao", "nome", "expressao", "descricao"]
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
    "id_situacao",
    "situacao_inconforme",
    "situacao_encontrada_nan_e_achado",
    "decodifica_sit_encontrada",
    "tipo_encaminhamento",
    "pre_encaminhamento",
    "encaminhamento",
]
TIPOS_ENCAMINHAMENTO = {"Determinação", "Recomendação"}


@dataclass
class Situacao:
    codigo: str
    descricao: str = ""
    regras: list[str] = field(default_factory=list)
    criterios: list[str] = field(default_factory=list)
    tipo_encaminhamento: str = ""
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
    id_situacao: str
    situacao_inconforme: str
    tipo_encaminhamento: str
    encaminhamento: str


@dataclass
class TemporaryVariable:
    id: str
    source_id: str
    nome: str
    expressao: str
    descricao: str


@dataclass
class QuestionDefinition:
    question: str = ""
    question_type: str = ""
    scale: str = ""
    details: dict[str, str] = field(default_factory=dict)
    subquestions: dict[str, str] = field(default_factory=dict)
    options: dict[str, str] = field(default_factory=dict)


def parse_matrix(path: Path) -> list[Achado]:
    matrix = parse_planning_matrix(path.read_text(encoding="utf-8"))
    achados: list[Achado] = []
    for question in matrix.questions:
        criteria = {criterion.id: criterion.descricao for criterion in question.criterios}
        question_text = re.sub(rf"^{re.escape(question.id)}\.\s*", "", question.question)
        for finding in question.achados:
            achados.append(
                Achado(
                    codigo=finding.id,
                    nome=finding.title,
                    questao_codigo=question.id,
                    questao_texto=question_text,
                    criterios=criteria,
                    situacoes=[
                        Situacao(
                            codigo=situation.id,
                            descricao=situation.descricao,
                            regras=list(situation.regra),
                            criterios=list(situation.criterios),
                            tipo_encaminhamento=situation.tipo_encaminhamento,
                            encaminhamento=situation.encaminhamento,
                        )
                        for situation in finding.situacoes
                    ],
                )
            )
    return achados


def parse_question_definitions(path: Path | None) -> dict[str, QuestionDefinition]:
    if not path or not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    matches = list(
        re.finditer(r"^### q(\d{4})\s+\[([^]]+)\].*$", text, flags=re.MULTILINE)
    )
    definitions: dict[str, QuestionDefinition] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[match.end() : end]
        question_match = re.search(r"^question:\s*\*\*(.+?)\*\*\s*$", block, flags=re.MULTILINE)
        scale_match = re.search(r"^scale:\s*(.+?)\s*$", block, flags=re.MULTILINE)
        definition = QuestionDefinition(
            question=question_match.group(1).strip() if question_match else "",
            question_type=match.group(2).strip(),
            scale=scale_match.group(1).strip() if scale_match else "",
        )
        current: dict[str, str] | None = None
        for line in block.splitlines():
            if line.strip() == "detail_options:":
                current = definition.details
                continue
            if line.strip() == "subquestions:":
                current = definition.subquestions
                continue
            if line.strip() == "options:":
                current = definition.options
                continue
            if re.match(r"^[a-z_]+:", line.strip()):
                current = None
                continue
            option_match = re.match(r"^-\s*([^|]+?)\s*\|\s*(.+)$", line.strip())
            if current is not None and option_match:
                current[option_match.group(1).strip()] = option_match.group(2).strip()
        definitions[match.group(1)] = definition
    return definitions


def refs_from_rule(rule: str) -> tuple[list[str], list[str]]:
    avaliacao_refs = re.findall(r"avaliacao\[([^\]]+)\]", rule)
    rule_without_avaliacao = re.sub(r"avaliacao\[[^\]]+\]", "", rule)
    q_refs = re.findall(
        r"\b(q\d{4}(?:ext\[[A-Za-z0-9_]+\]|\[[A-Za-z0-9_]+\]|evi[A-Za-z0-9_]*)?)(?![A-Za-z0-9_])",
        rule_without_avaliacao,
    )
    return q_refs, avaliacao_refs


def assignment_from_rule(rule: str) -> tuple[str, str] | None:
    match = re.fullmatch(r"\s*([A-Za-z_]\w*)\s*=(?!=)\s*(.+?)\s*", rule)
    return (match.group(1), match.group(2)) if match else None


def temporary_description(name: str) -> str:
    descriptions = {
        "total_TI": "Total de profissionais que atuam regularmente em tecnologia da informação.",
        "total_SI": "Total de profissionais que atuam regularmente em segurança da informação.",
        "total_TI_interno": "Total de profissionais internos de tecnologia da informação, excluídos terceirizados e estagiários.",
        "total_TI_terceiros": "Total de profissionais terceirizados que atuam em tecnologia da informação.",
        "predominio_terceiros": "Indica se o quantitativo de profissionais terceirizados de TI supera o quantitativo de profissionais internos de TI.",
    }
    return descriptions.get(name, f"Valor temporário calculado para {name}.")


def field_parts(field_name: str) -> tuple[str, str, str]:
    match = re.fullmatch(r"q(\d{4})(?:ext\[([^]]+)\]|\[([^]]+)\])?", field_name)
    if not match:
        return "", "", ""
    return match.group(1), match.group(2) or "", match.group(3) or ""


def purpose_text(text: str) -> str:
    text = re.sub(r"^[a-z]\)\s*", "", text.strip(), flags=re.IGNORECASE)
    text = re.sub(r"^\d{4}\.\s*", "", text).strip().rstrip("?").rstrip(".")
    if not text:
        return "o conteúdo declarado pela organização"
    if text.lower().startswith(("qual ", "como ", "quantos ", "quais ")):
        return text[0].lower() + text[1:]
    return "se " + text[0].lower() + text[1:]


def evidence_description(
    field_name: str,
    condition: str,
    definitions: dict[str, QuestionDefinition],
    temporary_variables: dict[str, TemporaryVariable],
) -> str:
    if field_name in temporary_variables:
        description = temporary_variables[field_name].descricao.rstrip(".")
        lowered = description[0].lower() + description[1:]
        if lowered.startswith("total "):
            lowered = "o " + lowered
        elif lowered.startswith("indica se "):
            lowered = lowered.removeprefix("indica ")
        return f'Valor calculado "@" da variável temporária {field_name}, para verificar {lowered}'

    number, detail, subitem = field_parts(field_name)
    definition = definitions.get(number, QuestionDefinition())
    normalized_condition = condition.strip()
    if normalized_condition in {"Não", "(Não | N/A)", "~Sim"}:
        prefix = "Resposta negativa"
    elif normalized_condition == "Sim":
        prefix = "Resposta positiva"
    else:
        prefix = 'Resposta "@"'

    if detail:
        text = definition.details.get(detail, "")
        return (
            f"{prefix} ao detalhamento {detail.lower()}) do item {number} do Questionário, "
            f"para verificar {purpose_text(text)}"
        )
    if subitem:
        if "_" in subitem:
            dimension, option = subitem.split("_", 1)
            dimension_text = definition.subquestions.get(dimension, dimension)
            option_text = definition.options.get(option, option)
            return (
                f'{prefix} ao campo {option_text.lower()} da dimensão {dimension_text} do item {number} do Questionário, '
                f"para verificar o quantitativo informado pela organização"
            )
        text = definition.subquestions.get(subitem) or definition.options.get(subitem, "")
        return (
            f"{prefix} ao subitem {subitem.lower()}) do item {number} do Questionário, "
            f"para verificar {purpose_text(text)}"
        )
    return (
        f"{prefix} ao item {number} do Questionário, "
        f"para verificar {purpose_text(definition.question)}"
    )


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


def encaminhamento_tipo(tipo_explicito: str, text: str) -> str:
    if tipo_explicito:
        for tipo_permitido in TIPOS_ENCAMINHAMENTO:
            if tipo_explicito.strip().casefold() == tipo_permitido.casefold():
                return tipo_permitido
        permitidos = ", ".join(sorted(TIPOS_ENCAMINHAMENTO))
        raise ValueError(
            f"tipo_encaminhamento inválido: {tipo_explicito!r}; use {permitidos}"
        )

    # Compatibilidade com matrizes antigas que trazem o tipo no próprio texto.
    low = text.strip().casefold()
    if low.startswith("determinar"):
        return "Determinação"
    if low.startswith("recomendar"):
        return "Recomendação"
    return "Recomendação"


def normalize_rule(rule: str) -> str:
    rule = re.sub(r"^\s*ou\s+", "", rule.strip(), flags=re.IGNORECASE)
    return rule


def tokenize_boolean(expression: str) -> list[str]:
    tokens: list[str] = []
    current: list[str] = []
    for char in expression:
        if char in "&|()":
            atom = "".join(current).strip()
            if atom:
                tokens.append(atom)
            tokens.append(char)
            current = []
        else:
            current.append(char)
    atom = "".join(current).strip()
    if atom:
        tokens.append(atom)
    return tokens


class BooleanParser:
    def __init__(self, expression: str):
        self.tokens = tokenize_boolean(expression)
        self.position = 0

    def parse(self) -> Any:
        node = self.parse_or()
        if self.position != len(self.tokens):
            raise ValueError(f"expressão lógica inválida: {' '.join(self.tokens[self.position:])}")
        return node

    def parse_or(self) -> Any:
        nodes = [self.parse_and()]
        while self.peek() == "|":
            self.position += 1
            nodes.append(self.parse_and())
        return ("|", nodes) if len(nodes) > 1 else nodes[0]

    def parse_and(self) -> Any:
        nodes = [self.parse_factor()]
        while self.peek() == "&":
            self.position += 1
            nodes.append(self.parse_factor())
        return ("&", nodes) if len(nodes) > 1 else nodes[0]

    def parse_factor(self) -> Any:
        if self.peek() == "(":
            self.position += 1
            node = self.parse_or()
            if self.peek() != ")":
                raise ValueError("parêntese não fechado na regra de identificação")
            self.position += 1
            return node
        if self.position >= len(self.tokens):
            raise ValueError("regra de identificação incompleta")
        token = self.tokens[self.position]
        self.position += 1
        return token

    def peek(self) -> str | None:
        return self.tokens[self.position] if self.position < len(self.tokens) else None


def inconformity_value(
    field_name: str,
    operator: str,
    right_side: str,
    definitions: dict[str, QuestionDefinition],
) -> str:
    value = right_side.strip().strip("'\"")
    number, detail, subitem = field_parts(field_name)
    definition = definitions.get(number, QuestionDefinition())
    option_text = ""
    if number and not detail and not subitem:
        option_text = definition.options.get(value, "")

    if operator == "==":
        return option_text or value
    if operator != "!=":
        return f"{operator} {value}"

    if option_text:
        return f"~({option_text})"
    if value == "Sim":
        if detail and definition.question_type == "adoption":
            return "(Não | N/A)"
        if subitem and definition.scale == "sim_nao":
            return "Não"
        return "~Sim"
    return f"~{value}"


def comparison_parts(
    atom: str,
    temporary_names: set[str],
    definitions: dict[str, QuestionDefinition],
) -> tuple[str, str]:
    match = re.fullmatch(
        r"\s*([A-Za-z_]\w*|q\d{4}(?:ext\[[^]]+\]|\[[^]]+\]|evi\w*)?)\s*(==|!=|>=|<=|>|<)\s*(.+?)\s*",
        atom,
    )
    if not match:
        raise ValueError(f"condição atômica inválida: {atom}")
    field_name = match.group(1)
    right_side = match.group(3).strip()
    if right_side in temporary_names:
        raise ValueError(
            f"a condição {atom!r} compara duas colunas; crie uma variável temporária booleana para essa comparação"
        )
    return field_name, inconformity_value(
        field_name,
        match.group(2),
        right_side,
        definitions,
    )


def collect_atoms(node: Any) -> list[str]:
    if isinstance(node, str):
        return [node]
    atoms: list[str] = []
    for child in node[1]:
        atoms.extend(collect_atoms(child))
    return atoms


def render_logic(node: Any, atom_actions: dict[str, str]) -> str:
    if isinstance(node, str):
        return atom_actions[node]
    operator, children = node
    rendered: list[str] = []
    for child in children:
        value = render_logic(child, atom_actions)
        if value not in rendered:
            rendered.append(value)
    if len(rendered) == 1:
        return rendered[0]
    return "(" + f" {operator} ".join(rendered) + ")"


def build_actions(
    achados: list[Achado],
    definitions: dict[str, QuestionDefinition],
    start: int = 1,
) -> tuple[dict[str, str], list[Action], list[TemporaryVariable]]:
    logic_by_achado: dict[str, str] = {}
    actions: list[Action] = []
    temporary_variables: dict[str, TemporaryVariable] = {}
    counter = start
    for achado in achados:
        situation_logics: list[str] = []
        for situacao in achado.situacoes:
            condition_rules: list[str] = []
            for rule in situacao.regras:
                assignment = assignment_from_rule(rule)
                if assignment:
                    name, expression = assignment
                    variable = TemporaryVariable(
                        id="",
                        source_id="questionario",
                        nome=name,
                        expressao=expression,
                        descricao=temporary_description(name),
                    )
                    existing = temporary_variables.get(name)
                    if existing and existing.expressao != expression:
                        raise ValueError(f"variável temporária {name} definida com expressões diferentes")
                    temporary_variables[name] = variable
                else:
                    condition_rules.append(normalize_rule(rule))

            if not condition_rules:
                raise ValueError(f"situação {situacao.codigo} sem condição de identificação")
            expression = " | ".join(f"({rule})" for rule in condition_rules)
            tree = BooleanParser(expression).parse()
            atoms = collect_atoms(tree)
            fields: dict[str, list[tuple[str, str]]] = {}
            for atom in atoms:
                field_name, condition = comparison_parts(
                    atom,
                    set(temporary_variables),
                    definitions,
                )
                fields.setdefault(field_name, [])
                if (atom, condition) not in fields[field_name]:
                    fields[field_name].append((atom, condition))

            atom_actions: dict[str, str] = {}
            for field_name, atom_conditions in fields.items():
                action_id = f"AV{counter:02d}"
                counter += 1
                conditions = list(dict.fromkeys(condition for _, condition in atom_conditions))
                action_condition = conditions[0] if len(conditions) == 1 else "(" + " | ".join(conditions) + ")"
                for atom, _ in atom_conditions:
                    atom_actions[atom] = action_id
                actions.append(
                    Action(
                        id=action_id,
                        source_id="questionario",
                        informacao_requerida=field_name,
                        criterio=criterion_text(achado, situacao),
                        descricao_evidencia=evidence_description(
                            field_name,
                            action_condition,
                            definitions,
                            temporary_variables,
                        ),
                        descricao_situacao_inconforme=situacao.descricao,
                        id_situacao=situacao.codigo,
                        situacao_inconforme=action_condition,
                        tipo_encaminhamento=encaminhamento_tipo(
                            situacao.tipo_encaminhamento,
                            situacao.encaminhamento,
                        ),
                        encaminhamento=situacao.encaminhamento,
                    )
                )
            situation_logics.append(render_logic(tree, atom_actions))
        logic_by_achado[achado.codigo] = logic_expression(situation_logics)

    variables = list(temporary_variables.values())
    for index, variable in enumerate(variables, start=1):
        variable.id = f"VT{index:02d}"
    return logic_by_achado, actions, variables


def procedure_description(achado: Achado) -> str:
    if achado.questao_texto:
        return f"Procedimento para verificar a questão {achado.questao_codigo}: {achado.questao_texto}"
    return f"Procedimento para verificar o possível achado {achado.codigo}: {achado.nome}"


def logic_expression(expressions: list[str]) -> str:
    if not expressions:
        return ""
    unique = list(dict.fromkeys(expressions))
    return unique[0] if len(unique) == 1 else "(" + " | ".join(unique) + ")"


def create_workbook(
    achados: list[Achado],
    logic_by_achado: dict[str, str],
    actions: list[Action],
    temporary_variables: list[TemporaryVariable],
    *,
    questionario_filepath: str,
    avaliacao_filepath: str,
    chave_questionario: str,
    chave_avaliacao: str,
) -> Workbook:
    workbook = Workbook()
    ws_fontes = workbook.active
    ws_fontes.title = "Fontes de Informação"
    ws_variaveis = workbook.create_sheet("Variáveis Temporárias")
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

    write_header(ws_variaveis, VARIAVEIS_HEADERS)
    for variable in temporary_variables:
        ws_variaveis.append(
            [variable.id, variable.source_id, variable.nome, variable.expressao, variable.descricao]
        )

    write_header(ws_proc, PROCEDIMENTOS_HEADERS)
    for index, achado in enumerate(achados, start=1):
        ws_proc.append(
            [
                f"PA{index:02d}",
                procedure_description(achado),
                logic_by_achado.get(achado.codigo, ""),
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
                action.id_situacao,
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

        if "Variáveis Temporárias" in workbook.sheetnames:
            ws = workbook["Variáveis Temporárias"]
            actual = [ws.cell(3, index).value for index in range(1, len(VARIAVEIS_HEADERS) + 1)]
            if actual != VARIAVEIS_HEADERS:
                errors.append(f"cabecalho invalido em Variáveis Temporárias: {actual}")

        if "Ações de Verificação" in workbook.sheetnames:
            ws = workbook["Ações de Verificação"]
            for row in range(4, ws.max_row + 1):
                action_id = ws.cell(row, 1).value
                if not action_id:
                    continue
                headers = {
                    str(ws.cell(3, column).value): column
                    for column in range(1, ws.max_column + 1)
                    if ws.cell(3, column).value
                }
                tipo = ws.cell(row, headers["tipo_encaminhamento"]).value
                if tipo and tipo not in TIPOS_ENCAMINHAMENTO:
                    errors.append(
                        f"tipo_encaminhamento inválido na ação {action_id}: {tipo!r}"
                    )
                has_situation = bool(ws.cell(row, headers["descricao_situacao_inconforme"]).value)
                if (
                    "Critérios de Auditoria" in workbook.sheetnames
                    and has_situation
                    and not ws.cell(row, headers["id_situacao"]).value
                ):
                    errors.append(f"id_situacao ausente na ação {action_id}")
                information = str(ws.cell(row, 6).value or "")
                if ";" in information or "|" in information:
                    errors.append(
                        f"ação {action_id} deve referenciar uma única coluna: {information!r}"
                    )

        if "Procedimentos de Auditoria" in workbook.sheetnames and "Ações de Verificação" in workbook.sheetnames:
            action_ids = {
                str(workbook["Ações de Verificação"].cell(row, 1).value)
                for row in range(4, workbook["Ações de Verificação"].max_row + 1)
                if workbook["Ações de Verificação"].cell(row, 1).value
            }
            ws = workbook["Procedimentos de Auditoria"]
            for row in range(4, ws.max_row + 1):
                procedure_id = ws.cell(row, 1).value
                logic = str(ws.cell(row, 3).value or "")
                for action_id in re.findall(r"\bAV\d+\b", logic):
                    if action_id not in action_ids:
                        errors.append(
                            f"procedimento {procedure_id} referencia ação inexistente: {action_id}"
                        )
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
    parser.add_argument(
        "--questionario-definicao",
        default="01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md",
        help="Arquivo Markdown com os textos dos itens e detalhamentos do questionário",
    )
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
    definitions = parse_question_definitions(Path(args.questionario_definicao))
    logic_by_achado, actions, temporary_variables = build_actions(achados, definitions)
    workbook = create_workbook(
        achados,
        logic_by_achado,
        actions,
        temporary_variables,
        questionario_filepath=args.questionario_filepath,
        avaliacao_filepath=args.avaliacao_filepath,
        chave_questionario=args.chave_questionario,
        chave_avaliacao=args.chave_avaliacao,
    )
    saida.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(saida)
    print(
        f"OK: {len(achados)} procedimentos, {len(actions)} ações e "
        f"{len(temporary_variables)} variáveis temporárias -> {saida}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
