#!/usr/bin/env python3
"""Gera a matriz de achados iGovTI 2026 preservando o OOXML do modelo."""

from __future__ import annotations

import argparse
import copy
import importlib.util
import re
import sys
import zipfile
from pathlib import Path

from lxml import etree
from openpyxl import load_workbook

sys.path.insert(0, str(Path(__file__).resolve().parent / "resources"))
from matriz_aplicabilidade import carregar_catalogo_matriz

try:
    from scripts.gerar_matriz_planejamento import (
        AUDITED_ENTITIES_HEADER,
        AUDIT_OBJECTIVE_HEADER,
        compact_display_identifiers,
        display_identifier,
        parse_matrix as parse_planning_matrix,
    )
except ImportError:
    from gerar_matriz_planejamento import (  # type: ignore
        AUDITED_ENTITIES_HEADER,
        AUDIT_OBJECTIVE_HEADER,
        compact_display_identifiers,
        display_identifier,
        parse_matrix as parse_planning_matrix,
    )


NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "xml": "http://www.w3.org/XML/1998/namespace",
}
W = f"{{{NS['w']}}}"


EFEITOS = {
    "A1": [
        ("Fragilidade na responsabilização", "Ausência de unidade ou função institucionalmente reconhecida para coordenar o uso da tecnologia da informação e responder por seus resultados."),
        ("Atuação reativa e fragmentada", "Falta de clareza sobre as responsabilidades de planejamento, coordenação, gestão, execução, monitoramento e controle da TIC."),
        ("Baixa influência institucional", "Participação insuficiente da TIC em decisões estratégicas, orçamentárias, contratuais e de gestão de riscos."),
    ],
    "A2": [
        ("Direcionamento insuficiente da TIC", "Baixa clareza sobre papéis, responsabilidades, objetivos, indicadores, metas e acompanhamento do desempenho da TIC."),
        ("Priorização deficiente", "Ausência de instância colegiada para deliberar sobre prioridades, projetos, riscos, serviços, orçamento e contratações de TIC."),
        ("Governança meramente formal", "Inexistência de reuniões, deliberações e acompanhamento efetivo das decisões relacionadas à TIC."),
    ],
    "A3": [
        ("Atuação reativa", "Planejamento de TIC sem processo formal e sem participação adequada das áreas demandantes."),
        ("Baixa legitimidade institucional", "Plano de TIC sem aprovação formal suficiente para orientar projetos, orçamento e contratações."),
        ("Desalinhamento institucional", "Execução de ações de TIC com baixo valor para os objetivos e resultados da organização."),
        ("Ineficiência na alocação de recursos", "Aquisições reativas, não priorizadas ou desconectadas do orçamento e do plano de contratações."),
        ("Desatualização das prioridades", "Manutenção de metas e iniciativas incompatíveis com mudanças institucionais, orçamentárias ou tecnológicas."),
    ],
    "A4": [
        ("Subdimensionamento da força de trabalho", "Ausência de base estruturada para estimar, alocar e acompanhar a capacidade necessária de pessoal de TIC e segurança da informação."),
        ("Baixa clareza de responsabilidades", "Ausência de cargos ou funções formalmente atribuídos à TIC ou à segurança da informação."),
        ("Execução insuficiente de funções críticas", "Risco de incapacidade para planejar, gerir, proteger, contratar, fiscalizar e sustentar serviços e ativos de TIC."),
        ("Dependência excessiva de terceiros", "Perda de conhecimento, redução da governabilidade e risco de descontinuidade dos serviços quando não houver capacidade interna mínima de coordenação e fiscalização."),
    ],
    "A5": [
        ("Prestação reativa de serviços", "Falta de definição clara, padronizada e transparente dos serviços de TIC oferecidos aos usuários e às áreas demandantes."),
        ("Ausência de parâmetros de desempenho", "Impossibilidade de avaliar objetivamente a qualidade, a disponibilidade e o atendimento dos principais serviços de TIC."),
        ("Controle inadequado dos ativos", "Informações insuficientes sobre ativos, itens de configuração e seus relacionamentos com sistemas, infraestrutura e serviços."),
        ("Tratamento deficiente de incidentes", "Resposta não padronizada, intempestiva ou sem rastreabilidade, com maior impacto sobre a continuidade e a qualidade dos serviços."),
    ],
    "A6": [
        ("Instrução processual frágil", "Falta de clareza sobre etapas, responsabilidades, instâncias decisórias, modelos e critérios de aprovação das contratações de TIC."),
        ("Soluções incompatíveis", "Contratação de soluções desalinhadas aos padrões tecnológicos, aos requisitos institucionais ou às prioridades aprovadas."),
        ("Participação técnica insuficiente", "Planejamento da contratação sem equipe formalmente designada ou sem participação técnica da área de TIC."),
    ],
}


def carregar_modulo_matriz(repo: Path):
    path = repo / ".agents/skills/preencher-matriz-procedimentos-auditoria/scripts/gerar_matriz_procedimentos.py"
    spec = importlib.util.spec_from_file_location("gerar_matriz_procedimentos", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Não foi possível carregar {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def carregar_achados(repo: Path):
    module = carregar_modulo_matriz(repo)
    matriz = repo / "01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/matriz_planejamento-pos-comentarios-gestor.md"
    planning_matrix = parse_planning_matrix(matriz.read_text(encoding="utf-8"))
    questions = {question.id: question for question in planning_matrix.questions}
    return [
        (
            finding,
            {risk.id: risk.text for risk in questions[finding.questao_codigo].riscos},
            questions[finding.questao_codigo],
        )
        for finding in module.parse_matrix(matriz)
    ]


def carregar_acoes(repo: Path):
    path = repo / "02-Execucao/03-Execucao_Procedimentos/01-Insumos/mapa-verificacao-achados-pos-comentarios-gestor.xlsx"
    workbook = load_workbook(path, read_only=False, data_only=False)
    try:
        ws_acoes = workbook["Ações de Verificação"]
        headers = {ws_acoes.cell(3, col).value: col for col in range(1, ws_acoes.max_column + 1)}
        acoes = {}
        for row in range(4, ws_acoes.max_row + 1):
            action_id = ws_acoes.cell(row, headers["id"]).value
            if not action_id:
                continue
            acoes[str(action_id)] = {
                name: ws_acoes.cell(row, col).value for name, col in headers.items()
            }

        ws_proc = workbook["Procedimentos de Auditoria"]
        proc_headers = {ws_proc.cell(3, col).value: col for col in range(1, ws_proc.max_column + 1)}
        por_achado = {}
        for row in range(4, ws_proc.max_row + 1):
            numero = ws_proc.cell(row, proc_headers["numero_achado"]).value
            logica = str(ws_proc.cell(row, proc_headers["logica_achado"]).value or "")
            if numero:
                por_achado[f"A{int(numero)}"] = re.findall(r"\bAV\d+\b", logica)
        return acoes, por_achado
    finally:
        workbook.close()


def contar_auditados(repo: Path) -> int:
    respostas_dir = repo / "02-Execucao/01-Questionario/03-Respostas_Processadas"
    candidatos = [
        respostas_dir / "20260716-respostas-questionario-pos-comentarios-gestor.xlsx",
        respostas_dir / "20260621-respostas-questionario-02-pos-avaliacao-evidencias.xlsx",
        respostas_dir / "20260621-respostas-questionario-01-pos-ajuste-inicial.xlsx",
    ]
    path = next((candidato for candidato in candidatos if candidato.exists()), None)
    if path is None:
        raise FileNotFoundError(
            "Nenhuma base processada do questionário foi encontrada para contar os auditados."
        )
    workbook = load_workbook(path, read_only=False, data_only=True)
    try:
        ws = workbook.active
        headers = [ws.cell(1, col).value for col in range(1, ws.max_column + 1)]
        column = headers.index("firstname") + 1
        return sum(1 for row in range(2, ws.max_row + 1) if ws.cell(row, column).value)
    finally:
        workbook.close()


def formatar_condicao(value) -> str:
    value = str(value or "").strip()
    fixed = {
        "(Não | N/A)": 'resposta "Não" ou "N/A"',
        "Não": 'resposta "Não"',
        "Sim": 'resposta "Sim"',
        "0": "valor igual a zero",
        "True": "resultado verdadeiro",
    }
    if value in fixed:
        return fixed[value]
    if value.startswith("~(") and value.endswith(")"):
        marker = re.match(r"([a-z])\)", value[2:], flags=re.IGNORECASE)
        return f"resposta distinta da alternativa {marker.group(1).lower()})" if marker else "resposta distinta da alternativa indicada"
    if value.startswith("(") and value.endswith(")") and " | " in value:
        options = [item.strip() for item in value[1:-1].split(" | ")]
        markers = [re.match(r"([a-z])\)", item, flags=re.IGNORECASE) for item in options]
        if all(markers):
            return "uma das alternativas " + ", ".join(f"{match.group(1).lower()})" for match in markers)
        return "um dos valores " + ", ".join(f'"{item}"' for item in options)
    marker = re.match(r"([a-z])\)", value, flags=re.IGNORECASE)
    if marker:
        return f"alternativa {marker.group(1).lower()})"
    if value.startswith((">", "<")):
        return f"condição {value}"
    return f'resposta "{value}"'


def listar_campos(fields) -> str:
    fields = list(dict.fromkeys(str(field) for field in fields))
    if len(fields) == 1:
        return fields[0]
    return ", ".join(fields[:-1]) + " e " + fields[-1]


def evidencias_do_achado(achado, action_ids, acoes):
    por_descricao = {}
    for action_id in action_ids:
        action = acoes[action_id]
        por_descricao.setdefault(action["descricao_situacao_inconforme"], []).append(action)

    evidencias = []
    for situacao in achado.situacoes:
        actions = por_descricao.get(situacao.descricao, [])
        conditions = {}
        for action in actions:
            field = action["informacao_requerida"]
            condition = formatar_condicao(action["situacao_inconforme"])
            conditions.setdefault(condition, []).append(field)
        items = [
            f"{condition} em {listar_campos(fields)}"
            for condition, fields in conditions.items()
        ] or ["Condição prevista na Matriz de Procedimentos de Auditoria"]
        evidencias.append({
            "situacao": f"{situacao.codigo} - {situacao.descricao.rstrip('.')}",
            "itens": items,
        })
    return evidencias


def _id_local_criterio(criterion_id: str) -> str:
    return criterion_id.rsplit(".", 1)[-1]


def criterios_do_achado(question, achado, variantes_especificas):
    """Materializa a visão sequencial dos critérios usados pelo achado."""
    display_mapping = compact_display_identifiers(question)
    usados = {
        reference
        for situacao in achado.situacoes
        for reference in situacao.criterios
    }
    usados.update(
        _id_local_criterio(reference)
        for variante in variantes_especificas
        for reference in variante.criterios
    )

    gerais = []
    especificos = {}
    for criterion in question.criterios:
        if criterion.id not in usados:
            continue
        item = {
            "id_exibicao": display_identifier(criterion.id, display_mapping),
            "descricao": criterion.descricao,
        }
        if criterion.especifico:
            especificos.setdefault(criterion.publico or "Público específico", []).append(item)
        else:
            gerais.append(item)
    return gerais, especificos, display_mapping


def _juntar_publicos(publicos: list[str]) -> str:
    if len(publicos) <= 1:
        return publicos[0] if publicos else ""
    return ", ".join(publicos[:-1]) + " e " + publicos[-1]


def encaminhamentos_do_achado(achado, variantes_por_situacao, display_mapping):
    """Agrupa encaminhamentos idênticos e preserva seus fundamentos."""
    resultado = []
    for situacao in achado.situacoes:
        especificas = variantes_por_situacao.get(situacao.codigo, [])
        membros = [{
            "geral": True,
            "publico": "Demais jurisdicionados" if especificas else "",
            "tipo": situacao.tipo_encaminhamento or "Recomendação",
            "encaminhamento": situacao.encaminhamento,
            "criterios": list(situacao.criterios),
        }]
        membros.extend({
            "geral": False,
            "publico": variante.rotulo_publico,
            "tipo": variante.tipo_encaminhamento,
            "encaminhamento": variante.encaminhamento,
            "criterios": [_id_local_criterio(item) for item in variante.criterios],
        } for variante in especificas)

        grupos = []
        por_conteudo = {}
        for membro in membros:
            key = (
                membro["tipo"].strip().casefold(),
                membro["encaminhamento"].strip().rstrip(".").casefold(),
            )
            if key not in por_conteudo:
                por_conteudo[key] = len(grupos)
                grupos.append({"membros": [], "tipo": membro["tipo"],
                               "encaminhamento": membro["encaminhamento"]})
            grupos[por_conteudo[key]]["membros"].append(membro)

        total_membros = len(membros)
        for grupo in grupos:
            membros_grupo = grupo["membros"]
            contem_geral = any(membro["geral"] for membro in membros_grupo)
            if len(membros_grupo) == total_membros and contem_geral and especificas:
                publico = "Todos os jurisdicionados"
            else:
                publico = _juntar_publicos([
                    membro["publico"] for membro in membros_grupo if membro["publico"]
                ])

            criterios = []
            for membro in membros_grupo:
                for criterion_id in membro["criterios"]:
                    shown = display_identifier(criterion_id, display_mapping)
                    if shown not in criterios:
                        criterios.append(shown)
            grupo["publico"] = publico
            grupo["criterios"] = criterios
            del grupo["membros"]

        resultado.append({
            "situacao": f"{situacao.codigo} - {situacao.descricao.rstrip('.')}",
            "grupos": grupos,
        })
    return resultado


def dividir_dispositivo_criterio(descricao: str) -> tuple[str, str]:
    """Separa o dispositivo de sua explicação para aplicar negrito no DOCX."""
    candidates = []
    for separator in (" — ", " – ", " - ", ": "):
        position = descricao.find(separator)
        if position >= 0:
            candidates.append((position, separator))
    if not candidates:
        return descricao, ""
    position, separator = min(candidates, key=lambda item: item[0])
    return descricao[:position], descricao[position:]


def clone_properties(element, child_name):
    child = element.find(f"w:{child_name}", NS)
    return copy.deepcopy(child) if child is not None else None


def run_properties(paragraph, *, bold=None, underline=None):
    for run in paragraph.findall(".//w:r", NS):
        rpr = run.find("w:rPr", NS)
        has_bold = rpr is not None and rpr.find("w:b", NS) is not None
        has_underline = rpr is not None and rpr.find("w:u", NS) is not None
        if (bold is None or has_bold == bold) and (underline is None or has_underline == underline):
            return copy.deepcopy(rpr)
    return None


def make_run(text: str, properties=None):
    run = etree.Element(W + "r")
    if properties is not None:
        run.append(copy.deepcopy(properties))
    node = etree.SubElement(run, W + "t")
    if text.startswith(" ") or text.endswith(" "):
        node.set(f"{{{NS['xml']}}}space", "preserve")
    node.text = text
    return run


def make_paragraph(template, parts, *, left_indent=None, hanging=None):
    paragraph = etree.Element(W + "p")
    ppr = clone_properties(template, "pPr")
    if ppr is not None:
        paragraph.append(ppr)
    if left_indent is not None or hanging is not None:
        if ppr is None:
            ppr = etree.Element(W + "pPr")
            paragraph.insert(0, ppr)
        indent = ppr.find("w:ind", NS)
        if indent is None:
            indent = etree.SubElement(ppr, W + "ind")
        if left_indent is not None:
            indent.set(W + "left", str(left_indent))
        if hanging is not None:
            indent.set(W + "hanging", str(hanging))
    for text, properties in parts:
        paragraph.append(make_run(text, properties))
    return paragraph


def blank_paragraph(template):
    paragraph = etree.Element(W + "p")
    ppr = clone_properties(template, "pPr")
    if ppr is not None:
        paragraph.append(ppr)
    return paragraph


def replace_cell(cell, paragraphs):
    for child in list(cell):
        if child.tag != W + "tcPr":
            cell.remove(child)
    for paragraph in paragraphs:
        cell.append(paragraph)


def atualizar_documento(document_xml: bytes, dados):
    root = etree.fromstring(document_xml)
    body = root.find("w:body", NS)
    tables = body.findall("w:tbl", NS)
    if len(tables) < 6:
        raise ValueError(f"O modelo deveria conter 6 tabelas de achados, mas contém {len(tables)}")

    sample_cells = tables[0].findall("w:tr", NS)[1].findall("w:tc", NS)
    templates = {
        "finding_bold": sample_cells[0].findall("w:p", NS)[0],
        "finding_blank": sample_cells[0].findall("w:p", NS)[1],
        "finding_normal": sample_cells[0].findall("w:p", NS)[2],
        "criterion": sample_cells[1].findall("w:p", NS)[0],
        "criterion_blank": sample_cells[1].findall("w:p", NS)[1],
        "evidence_intro": sample_cells[2].findall("w:p", NS)[0],
        "evidence_item": sample_cells[2].findall("w:p", NS)[1],
        "cause": sample_cells[3].findall("w:p", NS)[0],
        "effect": sample_cells[4].findall("w:p", NS)[0],
        "effect_blank": sample_cells[4].findall("w:p", NS)[1],
        "referral": sample_cells[5].findall("w:p", NS)[0],
        "referral_blank": sample_cells[5].findall("w:p", NS)[1],
    }
    props = {
        "finding_bold": run_properties(templates["finding_bold"], bold=True),
        "normal": run_properties(templates["finding_normal"], bold=False),
        "bold": run_properties(templates["criterion"], bold=True),
        "criterion_normal": run_properties(templates["criterion"], bold=False),
        "evidence_bold": run_properties(templates["evidence_intro"], bold=True),
        "evidence_normal": run_properties(templates["evidence_intro"], bold=False),
        "cause_bold": run_properties(templates["cause"], bold=True),
        "effect_bold": run_properties(templates["effect"], bold=True),
        "effect_normal": run_properties(templates["effect"], bold=False),
        # A matriz oficial também é o modelo da próxima geração. As
        # propriedades procuradas podem estar em parágrafos posteriores ao
        # título da situação, por isso a busca abrange toda a célula.
        "referral_label": run_properties(sample_cells[5], bold=True, underline=True),
        "referral_normal": run_properties(sample_cells[5], bold=False),
    }

    for index, item in enumerate(dados):
        achado = item["achado"]
        cells = tables[index].findall("w:tr", NS)[1].findall("w:tc", NS)

        finding_paragraphs = [
            make_paragraph(templates["finding_bold"], [(f"ACHADO {index + 1:02d}", props["finding_bold"])]),
            blank_paragraph(templates["finding_blank"]),
            make_paragraph(templates["finding_normal"], [(achado.nome.rstrip("."), props["normal"])]),
            blank_paragraph(templates["finding_blank"]),
            make_paragraph(templates["finding_normal"], [
                ("Achado composto pela ocorrência de alguma dessas situações:", props["normal"]),
            ]),
        ]
        for situacao in achado.situacoes:
            finding_paragraphs.append(make_paragraph(
                templates["finding_normal"],
                [(f"• {situacao.codigo} - {situacao.descricao.rstrip('.')}", props["normal"])],
                left_indent=300,
                hanging=180,
            ))
        replace_cell(cells[0], finding_paragraphs)

        paragraphs = []
        for criterion in item["criterios"]:
            dispositivo, explicacao = dividir_dispositivo_criterio(criterion["descricao"])
            paragraphs.append(make_paragraph(templates["criterion"], [
                (f'{criterion["id_exibicao"]}: {dispositivo}', props["bold"]),
                (explicacao, props["criterion_normal"]),
            ]))
            paragraphs.append(blank_paragraph(templates["criterion_blank"]))
        for publico, criterios in item.get("criterios_especificos", {}).items():
            paragraphs.append(make_paragraph(templates["criterion"], [(publico, props["bold"])]))
            for criterio in criterios:
                dispositivo, explicacao = dividir_dispositivo_criterio(criterio["descricao"])
                paragraphs.append(make_paragraph(templates["criterion"], [
                    (f'{criterio["id_exibicao"]}: {dispositivo}', props["bold"]),
                    (explicacao, props["criterion_normal"]),
                ]))
                paragraphs.append(blank_paragraph(templates["criterion_blank"]))
        if paragraphs:
            paragraphs.pop()
        replace_cell(cells[1], paragraphs)

        paragraphs = [make_paragraph(templates["evidence_intro"], [
            ("Respostas ao Questionário iGovTI 2026", props["evidence_bold"]),
            (" - Situações caracterizadas pelas respostas declaradas às questões indicadas:", props["evidence_normal"]),
        ])]
        for evidence_index, evidence in enumerate(item["evidencias"]):
            if evidence_index:
                paragraphs.append(blank_paragraph(templates["criterion_blank"]))
            paragraphs.append(make_paragraph(templates["evidence_item"], [
                (evidence["situacao"], props["bold"]),
            ]))
            for evidence_item in evidence["itens"]:
                paragraphs.append(make_paragraph(templates["evidence_item"], [
                    (f"• {evidence_item.rstrip('.')}.", props["evidence_normal"]),
                ]))
        replace_cell(cells[2], paragraphs)

        replace_cell(cells[3], [
            make_paragraph(templates["cause"], [("Não investigada.", props["cause_bold"])])
        ])

        paragraphs = []
        for effect_index, (label, text) in enumerate(item["efeitos"]):
            paragraphs.append(make_paragraph(templates["effect"], [
                (label + ":", props["effect_bold"]),
                (" " + text, props["effect_normal"]),
            ]))
            if effect_index < len(item["efeitos"]) - 1:
                paragraphs.append(blank_paragraph(templates["effect_blank"]))
        replace_cell(cells[4], paragraphs)

        paragraphs = []
        for referral_index, situacao in enumerate(item["encaminhamentos"]):
            if referral_index:
                paragraphs.append(blank_paragraph(templates["referral_blank"]))
            paragraphs.append(make_paragraph(templates["referral"], [
                (situacao["situacao"].split(" - ", 1)[-1], props["bold"]),
            ]))
            for grupo in situacao["grupos"]:
                if grupo["publico"] not in {"", "Demais jurisdicionados", "Todos os jurisdicionados"}:
                    paragraphs.append(make_paragraph(templates["referral"], [
                        (grupo["publico"], props["bold"]),
                    ]))
                codigo_situacao = situacao["situacao"].split(" - ", 1)[0]
                referencias = ", ".join([codigo_situacao, *grupo["criterios"]])
                paragraphs.append(make_paragraph(templates["referral"], [
                    ("• ", props["referral_normal"]),
                    (f'Comunicação com {grupo["tipo"]}', props["referral_label"]),
                    (f' para que {grupo["encaminhamento"].rstrip(".")} [{referencias}].',
                     props["referral_normal"]),
                ], left_indent=360, hanging=180))
        replace_cell(cells[5], paragraphs)

    # A propriedade pageBreakBefore dentro da primeira célula de uma tabela
    # não é interpretada de modo consistente pelo Word. Remove-se a marcação
    # legada e insere-se uma quebra estrutural imediatamente antes da tabela.
    for table in tables[1:6]:
        first_paragraph = table.find("w:tr/w:tc/w:p", NS)
        ppr = first_paragraph.find("w:pPr", NS)
        if ppr is not None:
            page_break_before = ppr.find("w:pageBreakBefore", NS)
            if page_break_before is not None:
                ppr.remove(page_break_before)

    for child in list(body):
        if child.tag == W + "p" and child.find(".//w:br[@w:type='page']", NS) is not None:
            body.remove(child)

    for table in tables[1:6]:
        paragraph = etree.Element(W + "p")
        run = etree.SubElement(paragraph, W + "r")
        page_break = etree.SubElement(run, W + "br")
        page_break.set(W + "type", "page")
        body.insert(body.index(table), paragraph)

    sixth_table = tables[5]
    remove = False
    for child in list(body):
        if child is sixth_table:
            remove = True
            continue
        if remove and child.tag != W + "sectPr":
            body.remove(child)
    sect_pr = body.find("w:sectPr", NS)
    final_paragraph = etree.Element(W + "p")
    body.insert(body.index(sect_pr), final_paragraph)
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone="yes")


def atualizar_cabecalho(header_xml: bytes):
    root = etree.fromstring(header_xml)
    cell = root.find(".//w:tbl/w:tr/w:tc[3]", NS)
    paragraphs = cell.findall("w:p", NS)
    if len(paragraphs) < 3:
        raise ValueError("Cabeçalho do modelo incompatível")

    templates = list(paragraphs[:3])
    bold = [run_properties(paragraph, bold=True) for paragraph in templates]
    normal = [run_properties(paragraph, bold=False) for paragraph in templates]
    new_paragraphs = [
        make_paragraph(templates[0], [("FISCALIZAÇÃO", bold[0]), (": 18/2026", normal[0])]),
        make_paragraph(templates[1], [
            ("JURISDICIONADOS", bold[1]),
            (f": {AUDITED_ENTITIES_HEADER}", normal[1]),
        ]),
        make_paragraph(templates[2], [
            ("OBJETIVO DA AUDITORIA", bold[2]),
            (f": {AUDIT_OBJECTIVE_HEADER}", normal[2]),
        ]),
    ]
    replace_cell(cell, new_paragraphs)
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone="yes")


def montar_dados(repo: Path):
    achados = carregar_achados(repo)
    acoes, por_achado = carregar_acoes(repo)
    matriz_path = repo / "01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/matriz_planejamento-pos-comentarios-gestor.md"
    catalogo = carregar_catalogo_matriz(matriz_path)
    dados = []
    for achado, riscos, question in achados:
        ids_situacoes = {situacao.codigo for situacao in achado.situacoes}
        variantes_especificas = [
            variante for variante in catalogo.variantes
            if not variante.geral and variante.id_situacao in ids_situacoes
        ]
        variantes_por_situacao = {}
        for variante in variantes_especificas:
            variantes_por_situacao.setdefault(variante.id_situacao, []).append(variante)
        criterios, criterios_especificos, display_mapping = criterios_do_achado(
            question, achado, variantes_especificas
        )
        dados.append({
            "achado": achado,
            "criterios": criterios,
            "evidencias": evidencias_do_achado(achado, por_achado[achado.codigo], acoes),
            "riscos": list(riscos.values()),
            "efeitos": EFEITOS[achado.codigo],
            "criterios_especificos": criterios_especificos,
            "variantes_por_situacao": variantes_por_situacao,
            "encaminhamentos": encaminhamentos_do_achado(
                achado, variantes_por_situacao, display_mapping
            ),
        })
    if len(dados) != 6:
        raise ValueError(f"Esperados 6 achados, encontrados {len(dados)}")
    return dados


def gerar(modelo: Path, saida: Path, repo: Path):
    dados = montar_dados(repo)
    auditados = contar_auditados(repo)
    with zipfile.ZipFile(modelo, "r") as source:
        archive = [(copy.copy(info), source.read(info.filename)) for info in source.infolist()]
    with zipfile.ZipFile(saida, "w") as target:
        for info, original_content in archive:
            content = original_content
            if info.filename == "word/document.xml":
                content = atualizar_documento(content, dados)
            elif info.filename == "word/header1.xml":
                content = atualizar_cabecalho(content)
            target.writestr(info, content)
    print(f"OK: {len(dados)} achados e {auditados} jurisdicionados -> {saida}")


def parse_args():
    repo_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--modelo",
        type=Path,
        default=repo_root / "02-Execucao/04-Matriz_Achados/AN06 – Matriz de achados.docx",
    )
    parser.add_argument(
        "--saida",
        type=Path,
        default=repo_root / "02-Execucao/04-Matriz_Achados/AN06 – Matriz de achados.docx",
    )
    parser.add_argument("--repo", type=Path, default=repo_root)
    return parser.parse_args()


def main():
    args = parse_args()
    args.saida.parent.mkdir(parents=True, exist_ok=True)
    gerar(args.modelo.resolve(), args.saida.resolve(), args.repo.resolve())


if __name__ == "__main__":
    main()
