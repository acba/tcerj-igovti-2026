#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Materializa a revisão pós-comentários do mapa e de seus artefatos sincronizados.

O script preserva todos os arquivos vigentes. As saídas são novas versões, com nomes
explícitos, e partem do estado corrente da matriz de planejamento para não descartar
ajustes humanos ainda não consolidados no Git.
"""

from __future__ import annotations

import copy
import json
import re
import shutil
from collections import defaultdict
from pathlib import Path

import pandas as pd
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter


ROOT = Path(__file__).resolve().parents[1]
MAPA_ORIGINAL = ROOT / "02-Execucao/03-Execucao_Procedimentos/01-Insumos/mapa-verificacao-achados.xlsx"
MAPA_SAIDA = ROOT / "02-Execucao/03-Execucao_Procedimentos/01-Insumos/mapa-verificacao-achados-pos-comentarios-gestor.xlsx"
MATRIZ_ORIGINAL = ROOT / "01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/matriz_planejamento.md"
MATRIZ_SAIDA = ROOT / "01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/matriz_planejamento-pos-comentarios-gestor.md"
PAINEL_ORIGINAL = ROOT / "02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor/fontes-auditoria-pos-comentarios/painel-avaliacao-evidencias.xlsx"
PAINEL_SAIDA = PAINEL_ORIGINAL
AJUSTES_EVIDENCIAS = ROOT / "02-Execucao/01-Questionario/02-Ajustes_Respostas/ajustes_respostas_questionario_pos_avaliacao_evidencias.xlsx"
PLANILHA_AJUSTES = ROOT / "docs/revisao-mapa/ajustes-mapa-verificacao-achados-pos-comentarios-gestor-2026-08-17.xlsx"
RESULTADO_ANTERIOR = Path("/tmp/tcerj-igovti-2026/revisao-mapa/resultado-auditoria-mapa-original-pos-comentarios.json")
RESULTADO_REVISADO = Path("/tmp/tcerj-igovti-2026/revisao-mapa/resultado-auditoria-mapa-revisado.json")


FORMULAS = {
    "PA01": "(AV01 | (AV02 & (AV03 | (AV04 | AV84))) | (AV05 & AV06))",
    "PA02": "((AV08 | AV86) | (AV11 | AV89) | (AV12 & (AV13 | AV91)))",
    "PA03": "(((AV17 | AV95) | ((AV14 | AV92) | (AV15 | AV93))) | (AV18 | AV96) | (AV19 | AV97) | (AV20 | AV98) | (AV24 | AV101))",
    "PA04": "((AV26 & AV25) | (AV29 | AV103) | ((AV31 | AV105) | (AV33 | AV107)) | (AV45 & AV46))",
    "PA05": "(((AV55 | AV125) | (AV56 | AV126)) | ((AV54 | AV124) | (AV57 | AV127) | (AV58 | AV128)) | ((AV59 | AV129) | (AV62 | AV132) | (AV63 | AV133)) | (AV66 | AV136) | ((AV67 | AV137) | (AV70 | AV140) | (AV71 | AV141)))",
    "PA06": "(((AV73 | AV143) | (AV152 | AV153)) | (AV78 | AV148) | (AV82 | (AV80 | AV150)) | AV83)",
}


Q6 = "A organização adota processo formal e padronizado para a fase preparatória das contratações de TIC, com responsabilidades definidas, análise técnica pela área de TIC e alinhamento aos instrumentos de planejamento?"
SITUACOES = {
    "s1.1": "Ausência de área, unidade, setor ou função de TIC formalmente instituída.",
    "s1.2": "Área de TIC sem atribuições formalmente definidas ou sem atribuições formais de governança, planejamento ou gestão de TIC.",
    "s1.3": "Posicionamento organizacional inadequado da área de TIC.",
    "s2.1": "Ausência de objetivos, indicadores ou metas para a gestão de TIC.",
    "s2.2": "Comitê de TIC ou instância equivalente não instituído formalmente.",
    "s2.3": "Comitê de TIC ou instância equivalente sem atuação efetiva comprovada.",
    "s3.1": "Inexistência ou fragilidade do processo formal de planejamento de TIC.",
    "s3.2": "Ausência de aprovação formal do plano de TIC.",
    "s3.4": "Plano de TIC sem alinhamento adequado ao planejamento institucional.",
    "s3.5": "Plano de TIC não utilizado como referência para a elaboração da proposta orçamentária e do plano de contratações.",
    "s3.6": "Ausência de acompanhamento, revisão ou atualização periódica do plano de TIC.",
    "s4.1": "Ausência de força de trabalho dedicada à TIC.",
    "s4.2": "A organização não definiu o quantitativo necessário de pessoal de TIC e segurança da informação.",
    "s4.3": "Ausência de cargos, funções, perfis ou ocupações específicas de TIC e segurança da informação.",
    "s4.6": "Dependência externa relevante sem capacidade interna suficiente para coordenar e fiscalizar a TIC.",
    "s5.1": "Inexistência ou insuficiência do catálogo de serviços de TIC.",
    "s5.2": "Ausência ou fragilidade na definição e no monitoramento de níveis mínimos de serviço de TIC.",
    "s5.3": "Inexistência ou fragilidade do inventário de ativos de TIC.",
    "s5.4": "Ausência ou fragilidade do processo de gestão de configuração.",
    "s5.5": "Inexistência ou fragilidade do processo de gestão de incidentes de TIC.",
    "s6.1": "Inexistência ou fragilidade de processo formal e padronizado para o planejamento das contratações de TIC.",
    "s6.2": "Contratações de TIC sem análise prévia e aprovação técnica da área de TIC.",
    "s6.3": "Contratações de TIC sem alinhamento ao planejamento de TIC e ao Plano de Contratações Anual.",
    "s6.4": "Contratações de TIC sem designação de Equipe de Planejamento com integrante técnico da área de TIC.",
}


SITUACOES_ANTERIORES = {
    "s1.1": SITUACOES["s1.1"],
    "s1.2": "Área de TIC sem atribuições formais suficientes para planejamento, coordenação, gestão, execução, monitoramento e controle da TIC.",
    "s1.3": SITUACOES["s1.3"],
    "s2.1": "Modelo básico de governança e gestão de TIC inexistente ou insuficiente quanto a papéis, responsabilidades, objetivos, indicadores, metas ou acompanhamento.",
    "s2.2": SITUACOES["s2.2"],
    "s2.3": "Comitê de TIC ou instância equivalente sem evidências suficientes de atuação efetiva.",
    "s3.1": SITUACOES["s3.1"],
    "s3.2": SITUACOES["s3.2"],
    "s3.4": SITUACOES["s3.4"],
    "s3.5": "Plano de TIC sem vínculo demonstrado com orçamento e contratações de TIC",
    "s3.6": SITUACOES["s3.6"],
    "s4.1": "Ausência de força de trabalho dedicada à TIC ou à segurança da informação.",
    "s4.2": SITUACOES["s4.2"],
    "s4.3": SITUACOES["s4.3"],
    "s4.4": "Perfis profissionais de TIC e segurança da informação inexistentes, insuficientes ou não utilizados na escolha de gestores.",
    "s4.5": "Lacunas de competências dos colaboradores e gestores de TIC e segurança da informação não são identificadas ou tratadas.",
    "s4.6": SITUACOES["s4.6"],
    "s5.1": SITUACOES["s5.1"],
    "s5.2": SITUACOES["s5.2"],
    "s5.3": SITUACOES["s5.3"],
    "s5.4": SITUACOES["s5.4"],
    "s5.5": SITUACOES["s5.5"],
    "s6.1": "Inexistência ou fragilidade de processo formal e padronizado para contratações de TIC.",
    "s6.2": "Contratações de TIC sem análise prévia e aprovação técnica obrigatória da área de TIC.",
    "s6.3": "Contratações de TIC sem alinhamento demonstrado ao planejamento de TIC, ao plano de contratações ou à proposta orçamentária.",
    "s6.4": "Contratações de TIC sem equipe de planejamento formalmente designada e com participação técnica de TIC.",
}


DETERMINACOES = {
    "s1.1",
    "s1.2",
    "s2.2",
    "s2.3",
    "s3.1",
    "s3.2",
    "s3.6",
    "s4.6",
    "s5.3",
    "s5.5",
    "s6.1",
    "s6.3",
}


CRITERIOS_ADICIONAIS = {
    "s1.1": (
        "Constituição Federal, art. 37, caput: princípios da legalidade e da eficiência.",
        "Lei nº 14.133/2021, art. 11, parágrafo único: dever da alta administração de implementar processos e estruturas de governança das contratações.",
    ),
    "s1.2": (
        "Constituição Federal, art. 37, caput: princípios da legalidade e da eficiência.",
        "Lei nº 14.133/2021, art. 11, parágrafo único: dever da alta administração de implementar processos e estruturas de governança das contratações.",
    ),
    "s2.2": (
        "Lei nº 14.133/2021, art. 11, parágrafo único: dever da alta administração de implementar estruturas de governança das contratações.",
        "Acórdão TCU nº 1.411/2014-Plenário, item 9.1.2: precedente sobre funcionamento permanente e composição relevante do Comitê de TIC.",
    ),
    "s2.3": (
        "Constituição Federal, art. 37, caput: princípio da eficiência.",
        "Acórdão TCE-RJ nº 44.490/2024-PLEN, item II.1: precedente de determinação para Comitê de TIC com responsabilidades de alinhamento, priorização e monitoramento.",
    ),
    "s3.1": (
        "Lei nº 14.133/2021, arts. 11, parágrafo único, e 18, caput: governança e planejamento da fase preparatória das contratações.",
    ),
    "s3.2": (
        "Lei nº 14.133/2021, arts. 11, parágrafo único, e 18, caput: governança e planejamento da fase preparatória das contratações.",
    ),
    "s3.6": (
        "Constituição Federal, art. 37, caput: princípio da eficiência.",
        "Acórdão TCE-RJ nº 44.490/2024-PLEN, item II.3.5: precedente de determinação para divulgação e monitoramento do PDTI após aprovação.",
    ),
    "s4.6": (
        "Lei nº 14.133/2021, art. 117: dever de acompanhamento e fiscalização da execução contratual por representantes da Administração especialmente designados.",
    ),
    "s5.3": (
        "Lei nº 13.709/2018, arts. 46 e 50: medidas técnicas e administrativas de segurança e regras de boas práticas e governança no tratamento de dados pessoais.",
    ),
    "s5.5": (
        "Lei nº 13.709/2018, arts. 46 e 48: deveres de segurança e comunicação de incidente que possa acarretar risco ou dano relevante aos titulares.",
        "Acórdão TCE-RJ nº 44.490/2024-PLEN: precedente de controle sobre governança e gestão de TIC.",
    ),
    "s6.1": (
        "Lei nº 14.133/2021, arts. 11, parágrafo único, e 19, IV: governança das contratações e instituição de modelos padronizados.",
    ),
    "s6.3": (
        "Lei nº 14.133/2021, arts. 12, VII, e 18, caput: plano de contratações anual e compatibilização da fase preparatória com o PCA, sempre que elaborado, e com as leis orçamentárias.",
    ),
}


ENCAMINHAMENTOS = {
    "s1.1": "formalize a área, unidade, setor ou função de TIC em instrumento compatível com a organização, definindo vinculação e responsabilidades essenciais, admitida estrutura equivalente que assegure o resultado de governança exigido",
    "s1.2": "defina formalmente as atribuições da área de TIC, incluindo, no mínimo, responsabilidades de governança, planejamento e gestão de TIC, em instrumento compatível com a estrutura da organização",
    "s2.1": "estabeleça objetivos, indicadores e metas para a gestão de TIC, aprovados ou formalmente definidos pela alta administração, e mantenha-os vinculados aos resultados institucionais pretendidos",
    "s2.2": "institua formalmente Comitê de TIC ou instância colegiada equivalente, compatível com o porte e a estrutura decisória da organização, com composição, competências, periodicidade e forma de registro definidas",
    "s2.3": "assegure o funcionamento efetivo do Comitê de TIC ou instância equivalente, realizando reuniões, registrando deliberações e acompanhando os encaminhamentos relevantes",
    "s3.1": "institua processo formal de planejamento de TIC, compatível com o porte e a maturidade da organização, com participação das áreas demandantes, critérios de priorização, etapas e responsabilidades definidos",
    "s3.2": "submeta o plano de TIC à aprovação formal do dirigente máximo ou de instância competente da alta administração, mantendo registro do ato de aprovação",
    "s3.5": "integre o plano de TIC à elaboração da proposta orçamentária e do plano de contratações, de maneira proporcional ao porte, à estrutura e à capacidade de planejamento da organização",
    "s3.6": "estabeleça e execute rotina periódica de acompanhamento, revisão e atualização do plano de TIC, registrando execução, pendências, reprogramações e deliberações",
    "s4.1": "avalie a força de trabalho dedicada à TIC e adote medidas proporcionais para assegurar capacidade mínima de planejamento, gestão, contratação, fiscalização e sustentação dos serviços e ativos de TIC",
    "s4.6": "assegure capacidade interna suficiente para coordenar, aprovar tecnicamente e fiscalizar as atividades e os contratos de TIC executados predominantemente por terceiros, preservando responsabilização e retenção de conhecimento",
    "s5.2": "defina, pactue e monitore níveis mínimos de serviço ou metas de atendimento para os serviços de TIC relevantes, incluindo metas no catálogo, indicadores, responsáveis e periodicidade de medição",
    "s5.3": "estabeleça e mantenha atualizado inventário de ativos de TIC, com informações suficientes sobre equipamentos, sistemas, softwares, licenças, serviços em nuvem, responsáveis e ciclo de vida",
    "s5.4": "formalize e execute processo de gestão de configuração, mantendo base, ferramenta ou registro equivalente com os itens relevantes e seus relacionamentos, responsabilidades e rotina de atualização",
    "s5.5": "formalize e execute processo de gestão de incidentes de TIC, com papéis, priorização, escalamento, tratamento, registro rastreável e comunicação dos incidentes de segurança sujeitos à LGPD",
    "s6.1": "formalize e padronize o processo de planejamento das contratações de TIC, com etapas, responsabilidades e artefatos padronizados, admitidos fluxos proporcionais à complexidade e ao risco",
    "s6.2": "estabeleça a submissão das contratações de TIC à análise prévia da área de TIC, com avaliação técnica mínima compatível com a complexidade e o risco da solução",
    "s6.3": "compatibilize as contratações de TIC com os instrumentos de planejamento da organização e com o Plano de Contratações Anual, quando elaborado, justificando as situações excepcionais",
    "s6.4": "designe formalmente Equipe de Planejamento para as contratações de TIC, assegurando integrante técnico da área de TIC e definição das responsabilidades dos participantes",
}


def ids_formula(expressao: str) -> set[str]:
    return set(re.findall(r"AV\d+", expressao))


def rows_as_dicts(ws) -> tuple[list[str], list[dict]]:
    headers = [cell.value for cell in ws[3]]
    rows = [dict(zip(headers, values)) for values in ws.iter_rows(min_row=4, values_only=True)]
    return headers, rows


def rewrite_sheet(ws, headers: list[str], rows: list[dict], template_row: int = 4) -> None:
    template_styles = []
    for col in range(1, len(headers) + 1):
        source = ws.cell(template_row if ws.max_row >= template_row else 3, col)
        template_styles.append(
            (
                copy.copy(source._style),
                copy.copy(source.alignment),
                copy.copy(source.protection),
                source.number_format,
            )
        )
    max_existing = max(ws.max_row, 4)
    if max_existing >= 4:
        ws.delete_rows(4, max_existing - 3)
    for row_index, data in enumerate(rows, start=4):
        for col_index, header in enumerate(headers, start=1):
            cell = ws.cell(row_index, col_index, data.get(header))
            style, alignment, protection, number_format = template_styles[col_index - 1]
            cell._style = copy.copy(style)
            cell.alignment = copy.copy(alignment)
            cell.protection = copy.copy(protection)
            cell.number_format = number_format
    ws.auto_filter.ref = f"A3:{get_column_letter(len(headers))}{max(3, 3 + len(rows))}"


def append_criterio(row: dict, textos: tuple[str, ...]) -> None:
    criterio = str(row.get("criterio") or "").strip()
    partes = [criterio] if criterio else []
    for texto in textos:
        if texto not in criterio:
            partes.append(texto)
    row["criterio"] = "\n".join(partes)


def gerar_mapa() -> tuple[list[str], list[str]]:
    shutil.copy2(MAPA_ORIGINAL, MAPA_SAIDA)
    wb = load_workbook(MAPA_SAIDA)

    ws_fontes = wb["Fontes de Informação"]
    fontes_headers, fontes = rows_as_dicts(ws_fontes)
    for fonte in fontes:
        if fonte["id"] == "questionario":
            fonte["descricao"] = "Questionário eletrônico iGovTI — respostas pós-comentários do gestor"
            fonte["filepath"] = "20260716-respostas-questionario-pos-comentarios-gestor.xlsx"
        elif fonte["id"] == "avaliacao_evidencias_ajustes":
            fonte["descricao"] = "Painel consolidado da avaliação de evidências pós-comentários do gestor"
            fonte["filepath"] = "painel-avaliacao-evidencias.xlsx"
    rewrite_sheet(ws_fontes, fontes_headers, fontes)

    ws_proc = wb["Procedimentos de Auditoria"]
    proc_headers, procedimentos = rows_as_dicts(ws_proc)
    for proc in procedimentos:
        proc["logica_achado"] = FORMULAS[proc["id"]]
        if proc["id"] == "PA06":
            proc["descricao"] = f"Procedimento para verificar a questão Q6: {Q6}"
    rewrite_sheet(ws_proc, proc_headers, procedimentos)

    ws_acoes = wb["Ações de Verificação"]
    acao_headers, acoes_originais = rows_as_dicts(ws_acoes)
    por_id = {row["id"]: row for row in acoes_originais}

    av152 = copy.deepcopy(por_id["AV73"])
    av152.update(
        id="AV152",
        informacao_requerida="q2801ext[B]",
        descricao_evidencia="Resposta negativa ao detalhamento b) do item 2801 do Questionário, para verificar se são disponibilizados artefatos padronizados para a fase de planejamento das contratações de TIC",
    )
    av153 = copy.deepcopy(por_id["AV143"])
    av153.update(id="AV153", informacao_requerida="q2801ext[B]")
    por_id["AV152"] = av152
    por_id["AV153"] = av153

    situacao_por_ids = {
        "s1.1": {"AV01"},
        "s1.2": {"AV02", "AV03", "AV04", "AV84"},
        "s1.3": {"AV05", "AV06"},
        "s2.1": {"AV08", "AV86"},
        "s2.2": {"AV11", "AV89"},
        "s2.3": {"AV12", "AV13", "AV91"},
        "s3.1": {"AV14", "AV15", "AV17", "AV92", "AV93", "AV95"},
        "s3.2": {"AV18", "AV96"},
        "s3.4": {"AV19", "AV97"},
        "s3.5": {"AV20", "AV98"},
        "s3.6": {"AV24", "AV101"},
        "s4.1": {"AV25", "AV26"},
        "s4.2": {"AV29", "AV103"},
        "s4.3": {"AV31", "AV33", "AV105", "AV107"},
        "s4.6": {"AV45", "AV46"},
        "s5.1": {"AV55", "AV56", "AV125", "AV126"},
        "s5.2": {"AV54", "AV57", "AV58", "AV124", "AV127", "AV128"},
        "s5.3": {"AV59", "AV62", "AV63", "AV129", "AV132", "AV133"},
        "s5.4": {"AV66", "AV136"},
        "s5.5": {"AV67", "AV70", "AV71", "AV137", "AV140", "AV141"},
        "s6.1": {"AV73", "AV143", "AV152", "AV153"},
        "s6.2": {"AV78", "AV148"},
        "s6.3": {"AV80", "AV82", "AV150"},
        "s6.4": {"AV83"},
    }
    id_para_situacao = {acao_id: sid for sid, ids in situacao_por_ids.items() for acao_id in ids}
    ids_usados = set().union(*(ids_formula(formula) for formula in FORMULAS.values()))
    if ids_usados != set(id_para_situacao):
        raise AssertionError("Cadastro de situações não coincide com as ações usadas nas fórmulas.")

    criterios_nivel_servico = por_id["AV57"]["criterio"]
    acoes = []
    for acao_id in sorted(ids_usados, key=lambda valor: int(valor[2:])):
        row = copy.deepcopy(por_id[acao_id])
        sid = id_para_situacao[acao_id]
        row["descricao_situacao_inconforme"] = SITUACOES[sid]
        row["tipo_encaminhamento"] = "Determinação" if sid in DETERMINACOES else "Recomendação"
        if sid in ENCAMINHAMENTOS:
            row["encaminhamento"] = ENCAMINHAMENTOS[sid]
        append_criterio(row, CRITERIOS_ADICIONAIS.get(sid, ()))
        if acao_id == "AV45":
            row["situacao_inconforme"] = "b) Centralizada Terceirizada: Há uma área de TI centralizada e formal que faz a gestão, mas a execução operacional/técnica é predominantemente terceirizada (ex: fábricas de software, service desk)."
        if acao_id in {"AV54", "AV124"}:
            row["criterio"] = criterios_nivel_servico
            row["encaminhamento"] = ENCAMINHAMENTOS["s5.2"]
        acoes.append(row)
    rewrite_sheet(ws_acoes, acao_headers, acoes)

    ws_motivos = wb["Motivos do Relatório"]
    motivos_headers, motivos_originais = rows_as_dicts(ws_motivos)
    motivos = []
    for motivo in motivos_originais:
        motivo = copy.deepcopy(motivo)
        if motivo["id"] == "MR016":
            motivo["condicao_exibicao"] = "AV11 & ~AV89"
        elif motivo["id"] == "MR018":
            motivo["condicao_exibicao"] = "AV12 & (AV13 | AV91)"
        elif motivo["id"] == "MR020":
            motivo["condicao_exibicao"] = "AV12 & AV13 & ~AV91"
        elif motivo["id"] == "MR021":
            motivo["condicao_exibicao"] = "AV12 & AV91"
        elif motivo["id"] == "MR043":
            motivo["condicao_exibicao"] = "AV26 & AV25"
            motivo["texto_motivo"] = "Item 0105: embora a organização tenha declarado estrutura formal de TIC no item 0101, informou não possuir profissionais atuando regularmente em tecnologia da informação"
        ids_motivo = ids_formula(str(motivo.get("condicao_exibicao") or "")) | ids_formula(str(motivo.get("acoes_referencia") or ""))
        if not ids_motivo.issubset(ids_usados):
            continue
        refs = re.findall(r"AV\d+", str(motivo.get("acoes_referencia") or ""))
        sid = id_para_situacao[refs[0]] if refs else None
        if sid:
            motivo["descricao_situacao_inconforme"] = SITUACOES[sid]
        motivos.append(motivo)

    motivo_b = copy.deepcopy(next(row for row in motivos_originais if row["id"] == "MR091"))
    motivo_b.update(
        id="MR111",
        descricao_situacao_inconforme=SITUACOES["s6.1"],
        condicao_exibicao="AV152 & ~AV153",
        acoes_referencia="AV152",
        texto_motivo="Item 2801b: a organização informou que não disponibiliza artefatos padronizados para a fase de planejamento das contratações de TIC",
    )
    motivo_b_evidencia = copy.deepcopy(next(row for row in motivos_originais if row["id"] == "MR092"))
    motivo_b_evidencia.update(
        id="MR112",
        descricao_situacao_inconforme=SITUACOES["s6.1"],
        condicao_exibicao="AV153",
        acoes_referencia="AV153",
        texto_motivo="Item 2801b: a organização declarou disponibilizar artefatos padronizados para o planejamento das contratações de TIC, mas a evidência foi insuficiente para comprovar a prática",
    )
    motivos.extend([motivo_b, motivo_b_evidencia])
    grupos: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for motivo in motivos:
        grupos[(motivo["id_procedimento"], motivo["descricao_situacao_inconforme"])].append(motivo)
    for grupo in grupos.values():
        grupo.sort(key=lambda row: (int(row.get("ordem") or 0), int(str(row["id"])[2:])))
        for ordem, motivo in enumerate(grupo, start=1):
            motivo["ordem"] = ordem
    motivos.sort(key=lambda row: int(str(row["id"])[2:]))
    rewrite_sheet(ws_motivos, motivos_headers, motivos)

    ws_vars = wb["Variáveis Temporárias"]
    vars_headers, variaveis_originais = rows_as_dicts(ws_vars)
    variaveis = [row for row in variaveis_originais if row["id"] in {"VT01", "VT03"}]
    rewrite_sheet(ws_vars, vars_headers, variaveis)

    wb.save(MAPA_SAIDA)
    removidas = sorted(set(por_id) - ids_usados, key=lambda valor: int(valor[2:]))
    return sorted(ids_usados, key=lambda valor: int(valor[2:])), removidas


def gerar_painel() -> int:
    wb = load_workbook(PAINEL_ORIGINAL)
    ws = wb[wb.sheetnames[0]]
    headers = [cell.value for cell in ws[1]]
    colunas = [
        "q2801ext[B]",
        "q2801ext[B]__resposta_afirmada",
        "q2801ext[B]__justificativa",
        "q2801ext[B]__pratica",
    ]
    presentes = [coluna in headers for coluna in colunas]
    if any(presentes) and not all(presentes):
        raise ValueError("O painel contém apenas parte das colunas q2801ext[B]; revisão manual necessária.")
    if not all(presentes):
        for coluna in colunas:
            ws.cell(1, ws.max_column + 1, coluna)

    ajustes = pd.read_excel(AJUSTES_EVIDENCIAS)
    ajustes = ajustes[ajustes["Código do item avaliado"].astype(str).eq("q2801ext[B]")].copy()
    parecer = ajustes["Avaliação do auditor revisor"].fillna("").astype(str).str.strip()
    resultado = ajustes["Resultado da avaliação do juiz"].fillna("").astype(str).str.strip()
    ajustes["resultado_final"] = parecer.where(~parecer.str.lower().isin({"", "nan", "none", "sem_parecer", "sem parecer", "não revisado", "nao revisado"}), resultado)
    just_revisor = ajustes["Justificativa do auditor revisor"].fillna("").astype(str).str.strip()
    ajustes["justificativa_final"] = just_revisor.where(~parecer.str.lower().isin({"", "nan", "none", "sem_parecer", "sem parecer", "não revisado", "nao revisado"}), ajustes["Justificativa do juiz"].fillna("").astype(str).str.strip())
    ajustes = ajustes[ajustes["resultado_final"].str.casefold().eq("não conforme")]
    registros = {str(row["Auditado"]).strip().upper(): row for _, row in ajustes.iterrows()}
    header_map = {cell.value: cell.column for cell in ws[1]}
    auditado_col = header_map["Auditado"]
    novos_headers = {cell.value: cell.column for cell in ws[1]}
    for row_index in range(2, ws.max_row + 1):
        for coluna in colunas:
            ws.cell(row_index, novos_headers[coluna]).value = None
    preenchidos = 0
    for row_index in range(2, ws.max_row + 1):
        auditado = str(ws.cell(row_index, auditado_col).value or "").strip().upper()
        registro = registros.get(auditado)
        if registro is None:
            continue
        ws.cell(row_index, novos_headers["q2801ext[B]"], "Não conforme")
        ws.cell(row_index, novos_headers["q2801ext[B]__resposta_afirmada"], str(registro.get("Resposta afirmada") or ""))
        ws.cell(row_index, novos_headers["q2801ext[B]__justificativa"], str(registro.get("justificativa_final") or ""))
        ws.cell(row_index, novos_headers["q2801ext[B]__pratica"], "são disponibilizados artefatos padronizados para a fase de planejamento das contratações de TIC")
        preenchidos += 1
    wb.save(PAINEL_ORIGINAL)
    return preenchidos


def situation_blocks(lines: list[str]) -> dict[str, tuple[int, int]]:
    starts = []
    for idx, line in enumerate(lines):
        match = re.match(r"^(\s*)- (S\d+\.\d+):\s*$", line)
        if match:
            starts.append((match.group(2), idx, len(match.group(1))))
    blocks = {}
    for pos, (sid, start, indent) in enumerate(starts):
        end = len(lines)
        for next_sid, next_start, next_indent in starts[pos + 1 :]:
            if next_indent == indent:
                end = next_start
                break
        for idx in range(start + 1, end):
            if lines[idx].startswith("## ") or lines[idx].strip() == "---":
                end = idx
                break
        blocks[sid] = (start, end)
    return blocks


def set_field(block: list[str], field: str, value: str) -> list[str]:
    pattern = re.compile(rf"^(\s*){re.escape(field)}:\s*.*$")
    for idx, line in enumerate(block):
        match = pattern.match(line)
        if match:
            block[idx] = f"{match.group(1)}{field}: {value}"
            return block
    raise AssertionError(f"Campo {field} não localizado no bloco {block[0].strip()}.")


def set_rule(block: list[str], rules: list[str]) -> list[str]:
    for idx, line in enumerate(block):
        if line.strip() != "regra_de_identificacao:":
            continue
        base_indent = len(line) - len(line.lstrip())
        end = idx + 1
        first_rule_indent = base_indent
        while end < len(block) and re.match(r"^\s*-\s+", block[end]):
            if end == idx + 1:
                first_rule_indent = len(block[end]) - len(block[end].lstrip())
            end += 1
        rule_indent = " " * first_rule_indent
        return block[: idx + 1] + [f"{rule_indent}- {rule}" for rule in rules] + block[end:]
    raise AssertionError(f"Regra não localizada no bloco {block[0].strip()}.")


def replace_once(text: str, old: str, new: str) -> str:
    if new in text:
        return text
    count = text.count(old)
    if count != 1:
        raise AssertionError(f"Esperada uma ocorrência, encontradas {count}: {old[:100]!r}")
    return text.replace(old, new, 1)


def replace_one_of(text: str, olds: tuple[str, ...], new: str) -> str:
    """Substitui uma dentre redações de origem conhecidas, preservando idempotência."""
    if new in text:
        return text
    encontrados = [old for old in olds if old in text]
    if len(encontrados) != 1:
        raise AssertionError(
            f"Esperada uma redação de origem, encontradas {len(encontrados)}: "
            + " | ".join(old[:80] for old in olds)
        )
    return text.replace(encontrados[0], new, 1)


def gerar_matriz() -> None:
    text = MATRIZ_ORIGINAL.read_text(encoding="utf-8")
    text = replace_once(
        text,
        "questao: Q6. A organização adota processo formal e padronizado para planejamento, contratação, fiscalização e gestão de soluções de TIC, com participação técnica da área de TIC e alinhamento ao planejamento?",
        f"questao: Q6. {Q6}",
    )
    text = replace_once(
        text,
        "- A alta administração estabeleceu modelo básico de governança e gestão de TIC, com papéis, responsabilidades, objetivos, indicadores ou metas para a TIC?",
        "- A alta administração estabeleceu objetivos, indicadores e metas para a gestão de TIC?",
    )
    text = replace_once(
        text,
        "- R2.1: Devido à ausência de modelo básico de governança e gestão de TIC, poderá haver baixa clareza sobre papéis, responsabilidades, objetivos, indicadores, metas e acompanhamento do desempenho da TIC.",
        "- R2.1: Devido à ausência de objetivos, indicadores ou metas para a gestão de TIC, poderá haver dificuldade para direcionar prioridades, medir resultados e acompanhar a contribuição da TIC para os objetivos institucionais.",
    )
    text = replace_once(
        text,
        "- IR1: Respostas sobre existência de diretrizes, papéis, responsabilidades, objetivos, indicadores, metas e práticas básicas de governança e gestão de TIC estabelecidas pela alta administração; [F1, q1001, q1002]",
        "- IR1: Resposta sobre objetivos, indicadores e metas para a gestão de TIC estabelecidos pela alta administração; [F1, q1001ext[H]]",
    )
    text = replace_once(
        text,
        "- IR2: Evidências anexadas que demonstrem modelo básico de governança e gestão de TIC, incluindo políticas, diretrizes, definição de papéis e responsabilidades, objetivos, indicadores, metas, relatórios de acompanhamento, medições de desempenho ou instrumentos equivalentes; [F2, q1001evi, q1002evi]",
        "- IR2: Evidência anexada que demonstre a formalização dos objetivos, indicadores e metas para a gestão de TIC; [F2, q1001evi]",
    )
    text = replace_once(
        text,
        "- P1: Verificar, por meio das respostas às q1001 e q1002, se há modelo básico de governança e gestão de TIC com papéis, responsabilidades, objetivos, indicadores, metas ou monitoramento; [IR1]",
        "- P1: Verificar, por meio da resposta à q1001ext[H], se a alta administração estabeleceu objetivos, indicadores e metas para a gestão de TIC; [IR1]",
    )
    text = replace_once(
        text,
        "- P2: Validar, pelas evidências anexadas às q1001 e q1002, a existência e suficiência do modelo básico de governança e gestão de TIC; [IR2]",
        "- P2: Validar, pela evidência anexada à q1001, a formalização dos objetivos, indicadores e metas para a gestão de TIC; [IR2]",
    )
    text = replace_once(
        text,
        "- E1: Resposta negativa ou insuficiente sobre modelo básico de governança e gestão de TIC; [P1]",
        "- E1: Resposta negativa sobre o estabelecimento de objetivos, indicadores ou metas para a gestão de TIC; [P1]",
    )
    text = replace_once(
        text,
        "- E2: Ausência, desatualização, incompatibilidade ou insuficiência de evidências que demonstrem diretrizes, papéis, responsabilidades, objetivos, indicadores, metas ou acompanhamento de TIC; [P2]",
        "- E2: Ausência, desatualização, incompatibilidade ou insuficiência de evidência que demonstre objetivos, indicadores e metas para a gestão de TIC; [P2]",
    )
    insercoes = {
        "- C6: Portaria SGD/ME nº 778/2019, art. 4º, § 1º - Referência de posicionamento organizacional: para a obtenção de melhores resultados, a área de TIC de cada órgão ou entidade deve, preferencialmente, estar vinculada à alta administração, com o intuito de apoiá-la na tomada de decisões e no alcance dos objetivos estratégicos.": [
            "- C7: Constituição Federal, art. 37, caput - Princípios da legalidade e da eficiência.",
            "- C8: Lei nº 14.133/2021, art. 11, parágrafo único - Dever da alta administração de implementar processos e estruturas de governança das contratações.",
        ],
        "- C5: COBIT 2019, APO01.05 - Estabelecer papéis e responsabilidades: definir, comunicar e manter papéis e responsabilidades relacionados à governança e gestão de TI.": [
            "- C6: Lei nº 14.133/2021, art. 11, parágrafo único - Dever da alta administração de implementar estruturas de governança das contratações.",
            "- C7: Constituição Federal, art. 37, caput - Princípio da eficiência.",
        ],
        "- C4: Acórdão TCE-RJ 44.490/2024-PLEN, item II.3 e subitens II.3.1 a II.3.5: necessidade de estabelecer processo estruturado, com participação de representantes das principais secretarias, para elaborar, manter e revisar periodicamente o PDTI, contemplando objetivos, indicadores e metas de TI alinhados aos objetivos de negócio, riscos que possam impactar objetivos e metas, projetos, aquisições e ações necessárias, alocação de recursos e ações de divulgação e monitoramento do PDTI após aprovação pela autoridade máxima.": [
            "- C5: Lei nº 14.133/2021, arts. 11, parágrafo único, e 18, caput - Governança e planejamento da fase preparatória das contratações.",
            "- C6: Constituição Federal, art. 37, caput - Princípio da eficiência.",
        ],
        "- C10: ABNT NBR ISO/IEC 27002:2022, controles 5.2 e 6.3: definir papéis e responsabilidades de segurança da informação e promover conscientização, educação e treinamento em segurança.": [
            "- C11: Lei nº 14.133/2021, art. 117 - Dever de acompanhamento e fiscalização da execução contratual por representantes da Administração especialmente designados.",
        ],
        "- C8: COBIT 2019, DSS02.02, DSS02.04 e DSS02.07 - Requisições de serviço e incidentes gerenciados: registrar, classificar, priorizar, investigar, diagnosticar, resolver, acompanhar e reportar incidentes e requisições de serviço.": [
            "- C9: Lei nº 13.709/2018, arts. 46 e 50 - Medidas técnicas e administrativas de segurança e regras de boas práticas e governança no tratamento de dados pessoais.",
            "- C10: Lei nº 13.709/2018, arts. 46 e 48 - Deveres de segurança e comunicação de incidente que possa acarretar risco ou dano relevante aos titulares.",
        ],
    }
    for anchor, novas in insercoes.items():
        text = replace_once(text, anchor, anchor + "\n" + "\n".join(novas))

    text = replace_one_of(
        text,
        (
            "- IR8: Resposta e evidência sobre integração do plano de TIC com orçamento, plano de contratações, projetos ou contratações de TIC; [F1, F2, q2102, q2802, q2804[B]]",
            "- IR8: Resposta e evidência sobre previsão orçamentária do plano de TIC; [F1, F2, q2102, q2102evi]",
        ),
        "- IR8: Resposta e evidência sobre a previsão, no plano de TIC, dos recursos orçamentários necessários à execução das iniciativas; [F1, F2, q2102ext[C], q2102evi]",
    )
    text = replace_one_of(
        text,
        (
            "- P8: Verificar, por meio das respostas e evidências das q2102, q2802 e q2804[B], se o plano de TIC se integra a orçamento, plano de contratações, projetos ou contratações; [IR8]",
            "- P8: Verificar, por meio da resposta e das evidências da q2102, se o plano de TIC prevê a estimativa de recursos orçamentários para sua execução; [IR8]",
        ),
        "- P8: Verificar, por meio da resposta e da evidência da q2102ext[C], se o plano de TIC prevê os recursos orçamentários necessários à execução das iniciativas; [IR8]",
    )
    text = replace_one_of(
        text,
        (
            "- E8: Inexistência ou insuficiência de vínculo entre plano de TIC, orçamento, plano de contratações, projetos ou contratações de TIC; [P8]",
            "- E8: Resposta negativa ou insuficiente sobre a previsão orçamentária do plano de TIC, ou evidência inexistente, incompatível ou insuficiente; [P8]",
        ),
        "- E8: Inexistência ou insuficiência de previsão orçamentária no plano de TIC; [P8]",
    )
    text = replace_once(
        text,
        "- E1: Quantitativo declarado igual a zero para profissionais de TIC ou segurança da informação, ou incompatível com a estrutura de TIC declarada pela organização; [P1]",
        "- E1: Quantitativo total declarado igual a zero para profissionais de TIC, desde que a organização tenha informado possuir estrutura formal de TIC; [P1]",
    )
    itens_s41_inline = "      itens_questionario: [q0101, q0105[TI_efetivos], q0105[TI_comissionados], q0105[TI_terceirizados], q0105[TI_cedidos], q0105[TI_temporarios], q0105[TI_estagiarios]]"
    itens_s41_multiline = "      itens_questionario:\n        - [q0101, q0105[TI_efetivos], q0105[TI_comissionados], q0105[TI_terceirizados], q0105[TI_cedidos], q0105[TI_temporarios], q0105[TI_estagiarios]]"
    if itens_s41_inline not in text and itens_s41_multiline not in text:
        text = replace_one_of(
            text,
            (
                "    itens_questionario:\n      - [q0105[TI_efetivos], q0105[TI_comissionados], q0105[TI_terceirizados], q0105[TI_cedidos], q0105[TI_temporarios], q0105[TI_estagiarios], q0105[SI_efetivos], q0105[SI_comissionados], q0105[SI_terceirizados], q0105[SI_cedidos], q0105[SI_temporarios], q0105[SI_estagiarios]]",
                "      itens_questionario:\n        - [q0105[TI_efetivos], q0105[TI_comissionados], q0105[TI_terceirizados], q0105[TI_cedidos], q0105[TI_temporarios], q0105[TI_estagiarios], q0105[SI_efetivos], q0105[SI_comissionados], q0105[SI_terceirizados], q0105[SI_cedidos], q0105[SI_temporarios], q0105[SI_estagiarios]]",
            ),
            itens_s41_multiline,
        )
    text = replace_once(
        text,
        "- IR1: Resposta sobre existência, atualização e disponibilidade do catálogo de serviços de TIC; [F1, q2201]",
        "- IR1: Resposta sobre atualização e disponibilidade do catálogo de serviços de TIC; [F1, q2201ext[B], q2201ext[C]]",
    )
    text = replace_once(
        text,
        "- IR3: Resposta sobre existência de ANS ou metas mínimas de nível de serviço; [F1, q2201ext[D]]",
        "- IR3: Resposta sobre metas no catálogo e existência de ANS ou metas mínimas de nível de serviço; [F1, q2201ext[A], q2201ext[D]]",
    )
    text = replace_once(
        text,
        "- P1: Verificar, por meio da resposta à q2201, a existência, atualização e disponibilidade do catálogo de serviços de TIC; [IR1]",
        "- P1: Verificar, por meio das respostas às q2201ext[B] e q2201ext[C], a atualização e a disponibilidade do catálogo de serviços de TIC; [IR1]",
    )
    text = replace_once(
        text,
        "- P3: Verificar, por meio da q2201ext[D] e da q2201ext[E], a existência e monitoramento de ANS ou metas mínimas de nível de serviço; [IR3, IR4]",
        "- P3: Verificar, por meio das q2201ext[A], q2201ext[D] e q2201ext[E], a definição, pactuação e monitoramento de metas ou níveis de serviço; [IR3, IR4]",
    )
    text = replace_one_of(
        text,
        (
            "- IR6: Resposta e evidência sobre aderência das contratações ao plano de TIC, ao plano de contratações e à proposta orçamentária; [F1, F2, q2102ext[C], q2802ext[C], q2802ext[D], q2804[B], q2102evi, q2802evi]",
            "- IR6: Resposta e evidência sobre alinhamento das contratações ao Plano de Contratações Anual; [F1, F2, q2802ext[C], q2804[B], q2802evi]",
        ),
        "- IR6: Resposta e evidência sobre alinhamento das contratações aos instrumentos de planejamento e ao Plano de Contratações Anual; [F1, F2, q2802ext[C], q2804[B], q2802evi]",
    )
    text = replace_one_of(
        text,
        (
            "- P4: Verificar, por meio das q2102ext[C], q2802ext[C], q2802ext[D], q2804[B] e evidências q2102evi/q2802evi, se as contratações de TIC estão aderentes ao plano de TIC, ao plano de contratações e à proposta orçamentária; [IR6]",
            "- P4: Verificar, por meio das q2802ext[C], q2804[B] e evidências q2802evi, se as contratações de TIC estão alinhadas ao Plano de Contratações Anual; [IR6]",
        ),
        "- P4: Verificar, por meio das q2802ext[C], q2804[B] e da evidência q2802evi, se as contratações de TIC estão alinhadas aos instrumentos de planejamento e ao Plano de Contratações Anual; [IR6]",
    )

    lines = text.splitlines()
    for sid_remover in ("S4.4", "S4.5"):
        blocks = situation_blocks(lines)
        if sid_remover in blocks:
            start, end = blocks[sid_remover]
            del lines[start:end]

    updates = {
        "S1.1": dict(descricao=SITUACOES["s1.1"], criterios="[C1, C4, C5, C7, C8]", tipo_encaminhamento="Determinação", encaminhamento=ENCAMINHAMENTOS["s1.1"]),
        "S1.2": dict(descricao=SITUACOES["s1.2"], itens_questionario="[q0101, q0103, q0103[D], q0103[G], q0103evi]", referencias_matriz="[R1.2, P3, E3, P4, E4]", criterios="[C2, C4, C5, C7, C8]", tipo_encaminhamento="Determinação", encaminhamento=ENCAMINHAMENTOS["s1.2"]),
        "S2.1": dict(descricao=SITUACOES["s2.1"], itens_questionario="[q1001ext[H], q1001evi]", encaminhamento=ENCAMINHAMENTOS["s2.1"]),
        "S2.2": dict(itens_questionario="[q1001ext[E], q1001evi]", referencias_matriz="[R2.2, P3, E3, P4, E4]", criterios="[C3, C4, C5, C6]", tipo_encaminhamento="Determinação", encaminhamento=ENCAMINHAMENTOS["s2.2"]),
        "S2.3": dict(descricao=SITUACOES["s2.3"], criterios="[C2, C3, C4, C7]", tipo_encaminhamento="Determinação", encaminhamento=ENCAMINHAMENTOS["s2.3"]),
        "S3.1": dict(itens_questionario="[q2101ext[A], q2101ext[B], q2101ext[D], q2101evi]", criterios="[C1, C3, C4, C5]", tipo_encaminhamento="Determinação", encaminhamento=ENCAMINHAMENTOS["s3.1"]),
        "S3.2": dict(criterios="[C1, C3, C4, C5]", tipo_encaminhamento="Determinação", encaminhamento=ENCAMINHAMENTOS["s3.2"]),
        "S3.5": dict(descricao=SITUACOES["s3.5"], itens_questionario="[q2102ext[C], q2102evi]", referencias_matriz="[R3.5, P8, E8]", encaminhamento=ENCAMINHAMENTOS["s3.5"]),
        "S3.6": dict(criterios="[C1, C3, C4, C6]", tipo_encaminhamento="Determinação", encaminhamento=ENCAMINHAMENTOS["s3.6"]),
        "S4.1": dict(descricao=SITUACOES["s4.1"], encaminhamento=ENCAMINHAMENTOS["s4.1"]),
        "S4.6": dict(itens_questionario="[q0101, q0105[TI_efetivos], q0105[TI_comissionados], q0105[TI_cedidos], q0105[TI_temporarios]]", criterios="[C6, C7, C8, C11]", tipo_encaminhamento="Determinação", encaminhamento=ENCAMINHAMENTOS["s4.6"]),
        "S5.1": dict(itens_questionario="[q2201, q2201ext[B], q2201ext[C], q2201evi]"),
        "S5.2": dict(itens_questionario="[q2201ext[A], q2201ext[D], q2201ext[E], q2201evi]", encaminhamento=ENCAMINHAMENTOS["s5.2"]),
        "S5.3": dict(criterios="[C4, C5, C9]", tipo_encaminhamento="Determinação", encaminhamento=ENCAMINHAMENTOS["s5.3"]),
        "S5.4": dict(itens_questionario="[q2203ext[C], q2203evi]", encaminhamento=ENCAMINHAMENTOS["s5.4"]),
        "S5.5": dict(criterios="[C7, C8, C10]", tipo_encaminhamento="Determinação", encaminhamento=ENCAMINHAMENTOS["s5.5"]),
        "S6.1": dict(descricao=SITUACOES["s6.1"], itens_questionario="[q2801ext[A], q2801ext[B], q2801evi]", criterios="[C1, C3, C7]", tipo_encaminhamento="Determinação", encaminhamento=ENCAMINHAMENTOS["s6.1"]),
        "S6.2": dict(descricao=SITUACOES["s6.2"], encaminhamento=ENCAMINHAMENTOS["s6.2"]),
        "S6.3": dict(descricao=SITUACOES["s6.3"], itens_questionario="[q2802ext[C], q2804[B], q2802evi]", criterios="[C1, C2]", tipo_encaminhamento="Determinação", encaminhamento=ENCAMINHAMENTOS["s6.3"]),
        "S6.4": dict(descricao=SITUACOES["s6.4"], encaminhamento=ENCAMINHAMENTOS["s6.4"]),
    }
    rules = {
        "S1.2": ["(q0101 != F) & ((q0103[G] == Sim) | (q0103[D] == Não))"],
        "S2.1": ["(q1001ext[H] != Sim)"],
        "S2.2": [
            "(q1001ext[E] != Sim)",
            "ou q1001evi é inexistente, incompatível ou insuficiente para comprovar a instituição formal do Comitê de TIC ou instância equivalente",
        ],
        "S2.3": ["(q1001ext[E] == Sim) & (q1001ext[F] != Sim)"],
        "S3.1": ["(q2101ext[D] != Sim) | ((q2101ext[A] != Sim) | (q2101ext[B] != Sim))"],
        "S3.5": ["(q2102ext[C] != Sim)"],
        "S4.1": [
            "total_TI = q0105[TI_efetivos] + q0105[TI_comissionados] + q0105[TI_terceirizados] + q0105[TI_cedidos] + q0105[TI_temporarios] + q0105[TI_estagiarios]",
            "(q0101 != F) & (total_TI == 0)",
        ],
        "S4.6": [
            "total_TI_interno = q0105[TI_efetivos] + q0105[TI_comissionados] + q0105[TI_cedidos] + q0105[TI_temporarios]",
            "(q0101 == B) & (total_TI_interno == 0)",
        ],
        "S5.1": ["(q2201ext[B] != Sim) | (q2201ext[C] != Sim)"],
        "S5.2": ["(q2201ext[A] != Sim) | (q2201ext[D] != Sim) | (q2201ext[E] != Sim)"],
        "S5.4": ["(q2203ext[C] != Sim)"],
        "S6.1": ["(q2801ext[A] != Sim) | (q2801ext[B] != Sim)"],
        "S6.3": ["(q2804[B] != Sim) | (q2802ext[C] != Sim)"],
    }
    blocks = situation_blocks(lines)
    for sid, fields in updates.items():
        start, end = blocks[sid]
        block = lines[start:end]
        for field, value in fields.items():
            block = set_field(block, field, value)
        if sid in rules:
            block = set_rule(block, rules[sid])
        lines[start:end] = block
        blocks = situation_blocks(lines)

    MATRIZ_SAIDA.write_text("\n".join(lines) + "\n", encoding="utf-8")


def ajuste_rows(removidas: list[str]) -> list[dict]:
    rows = [
        ("AJ-001", "Mapa/PA04/S4.1", "AV25 | AV27", "AV26 & AV25", "Aplica o gate de existência de estrutura formal e elimina a inferência inválida baseada no total de SI."),
        ("AJ-002", "Mapa/S4.1", "Ausência de força de trabalho dedicada à TIC ou à segurança da informação", SITUACOES["s4.1"], "O questionário exige registro na área predominante; zero em SI não demonstra ausência da função."),
        ("AJ-003", "Mapa/PA02/S2.2", "AV11 na consolidação anterior", "AV11 | AV89", "Mantém, por orientação da equipe, tanto a negativa declarada quanto a insuficiência da evidência de instituição formal como gatilhos de S2.2."),
        ("AJ-004", "Mapa/PA02/S2.3", "(AV12 | AV90) & (AV13 | AV91)", "AV12 & (AV13 | AV91)", "A situação de inatividade só é aplicável a quem declarou possuir Comitê."),
        ("AJ-005", "Mapa/PA02/S2.1", "Oito ações sobre quatro requisitos", "AV08 | AV86", "Separa S2.1 de S1.2 e restringe a situação aos objetivos, indicadores e metas definidos pela alta administração."),
        ("AJ-006", "Mapa/PA03/S3.1", "A, B, C e D cumulativos", "(AV17 | AV95) | ((AV14 | AV92) | (AV15 | AV93))", "Retira análise de benefícios/custos/riscos como gatilho autônomo e conserva formalização, participação e priorização."),
        ("AJ-007", "Mapa/PA03/S3.5", "q2102C, q2802C, q2802D e q2804B", "q2102C (AV20 | AV98)", "Elimina bis in idem entre planejamento de TIC e execução das contratações."),
        ("AJ-008", "Mapa/PA06/S6.3", "q2102C, q2802C, q2802D e q2804B", "q2804B | q2802C (AV82 | AV80 | AV150)", "Reserva a situação para execução/alinhamento das contratações e PCA; a fórmula final específica prevalece sobre a menção anterior a q2802D."),
        ("AJ-009", "Mapa/PA05/S5.3-S5.4", "q2203A compartilhado", "q2203A apenas em S5.3; S5.4 apenas q2203C", "Separa base consolidada/inventário da formalização do processo de configuração."),
        ("AJ-010", "Mapa/PA05/S5.1-S5.2", "q2201A em catálogo", "q2201A em níveis de serviço", "O item A verifica metas por serviço e é semanticamente aderente ao bloco de níveis de serviço."),
        ("AJ-011", "Mapa/PA04/S4.4", "Situação geradora de achado", "Retirada do achado", "Resposta negativa sobre perfis não comprova inadequação das pessoas designadas; permanece como indicador de maturidade na matriz."),
        ("AJ-012", "Mapa/PA04/S4.5", "Situação geradora de achado", "Retirada do achado", "Identificação e tratamento de lacunas são referenciais de maturidade sem matriz normativa suficiente para imputação automática."),
        ("AJ-013", "Mapa/PA04/S4.6", "((q0101 B ou C) e total interno zero) ou predomínio de terceiros", "q0101 B e total interno zero (AV45 & AV46)", "Modelo C pode representar estrutura compartilhada legítima; predomínio de terceiros não prova incapacidade de fiscalização."),
        ("AJ-014", "Mapa/PA01/S1.3", "q0102 B, C, D e E", "q0102 C, D e E", "Subordinação estratégica (B) é compatível com a referência preferencial da Portaria SGD/ME nº 778/2019."),
        ("AJ-015", "Mapa/PA06/Q6", "Questão ampla sobre todo o ciclo", Q6, "Alinha o enunciado às situações efetivamente testadas na fase preparatória."),
        ("AJ-016", "Mapa/PA06/S6.1", "q2801 A, C, D, E e G", "q2801 A e B; AV152/AV153 incluídas", "A situação passa a testar processo definido e artefatos padronizados da fase de planejamento."),
        ("AJ-017", "Mapa/PA06/S6.2", "Análise prévia e aprovação técnica obrigatória", SITUACOES["s6.2"], "Retira qualificação absoluta não contida no próprio critério e preserva análise técnica proporcional."),
        ("AJ-018", "Mapa/PA06/S6.4", "Equipe formalmente designada e com participação técnica", SITUACOES["s6.4"], "Explicita o integrante técnico da área de TIC como núcleo da situação."),
        ("AJ-019", "Mapa/Ações de Verificação", "151 ações, inclusive 41 órfãs", "Somente ações referenciadas nas seis fórmulas", "Remove código morto e impede divergência silenciosa entre ações, motivos e lógica do achado."),
        ("AJ-020", "Mapa/Motivos do Relatório", "Motivos associados às regras antigas", "Motivos filtrados, recondicionados e acrescidos de q2801B", "Mantém o relatório individual coerente com os novos gatilhos e elimina referências a ações removidas."),
        ("AJ-021", "Mapa/Variáveis Temporárias", "VT01 a VT05", "VT01 e VT03", "total_SI, total_TI_terceiros e predominio_terceiros deixaram de ser usados."),
        ("AJ-022", "Mapa/Fontes de Informação", "Base pós-evidências e texto com erro de codificação", "Base e painel pós-comentários; acentuação corrigida", "A versão do mapa deve apontar para o mesmo estado temporal dos dados usados na reexecução."),
        ("AJ-023", "Painel pós-comentários", "Sem q2801ext[B]", "Coluna e metadados q2801ext[B] incorporados ao painel vigente", "O catálogo já avaliava B, mas o painel fora filtrado pelo mapa antigo; a ação documental exige a coluna."),
        ("AJ-024", "Matriz de Planejamento", "Regras, itens, descrições e tipos anteriores", "Versão pós-comentários sincronizada", "As condições do possível achado devem ser idênticas às ações e fórmulas operacionais do mapa."),
        ("AJ-038", "Mapa e matriz/S1.2 × S2.1", "q0103D e q1001C podiam gerar situações distintas pelo mesmo fato", "S1.2 mantém competências formais por q0103; S2.1 usa somente q1001H (AV08/AV86)", "Elimina sobreposição entre competência formal da área de TIC e direção estratégica exercida pela alta administração."),
        ("AJ-039", "Mapa e matriz/PA03/S3.5", "Plano de TIC sem previsão orçamentária demonstrada; encaminhamento exigia estimativa dos recursos e memória ou referência", SITUACOES["s3.5"] + " Encaminhamento: " + ENCAMINHAMENTOS["s3.5"], "Alinha a situação e o encaminhamento ao conteúdo efetivamente verificado por q2102ext[C], sem exigir estimativa orçamentária ou memória de cálculo não avaliadas pelo questionário."),
        ("AJ-040", "Mapa e matriz/PA06/Q6", "A organização adota controles mínimos na fase preparatória das contratações de TIC, com processo definido e análise técnica pela unidade competente?", Q6, "Substitui expressão genérica por requisitos verificáveis e cobre processo formal e padronizado, responsabilidades, análise técnica e alinhamento ao planejamento."),
    ]
    tipo_rows = [
        ("S1.1", "Recomendação", "Determinação", "CF/88, art. 37; Lei nº 14.133/2021, art. 11, parágrafo único", "Dever de resultado; admitir estrutura equivalente e observar a competência de auto-organização."),
        ("S1.2", "Recomendação", "Determinação", "CF/88, art. 37; Lei nº 14.133/2021, art. 11, parágrafo único", "Exigir atribuições mínimas, sem impor desenho organizacional único."),
        ("S2.2", "Recomendação", "Determinação", "Lei nº 14.133/2021, art. 11; Acórdãos TCE-RJ nº 44.490/2024 e TCU nº 1.411/2014", "O precedente TCE-RJ contém determinação; o precedente TCU citado contém recomendação."),
        ("S2.3", "Recomendação", "Determinação", "CF/88, art. 37; Acórdão TCE-RJ nº 44.490/2024", "Aplicável somente se a entidade declarou possuir Comitê."),
        ("S3.1", "Recomendação", "Determinação", "Lei nº 14.133/2021, arts. 11 e 18; precedentes TCU/TCE-RJ", "Admitir instrumento equivalente a PDTI/PEDTIC, desde que satisfaça o resultado."),
        ("S3.2", "Recomendação", "Determinação", "Lei nº 14.133/2021, arts. 11 e 18; precedentes TCU/TCE-RJ", "A aprovação deve ser pela instância competente, sem impor colegiado específico."),
        ("S3.6", "Recomendação", "Determinação", "CF/88, art. 37; Acórdão TCE-RJ nº 44.490/2024, item II.3.5", "Vincular a obrigação ao plano efetivamente adotado."),
        ("S4.6", "Recomendação", "Determinação", "Lei nº 14.133/2021, art. 117", "Art. 117 exige fiscalização, não quadro próprio de TIC; regra calibrada para terceirização e ausência total de capacidade interna."),
        ("S5.3", "Recomendação", "Determinação", "LGPD, arts. 46 e 50", "A LGPD impõe segurança, mas não nomeia inventário; encaminhamento deve exigir resultado equivalente e proporcional ao tratamento de dados."),
        ("S5.5", "Recomendação", "Determinação", "LGPD, arts. 46 e 48", "Art. 48 alcança incidentes com risco ou dano relevante; a rotina deve contemplar essa qualificação."),
        ("S6.1", "Recomendação", "Determinação", "Lei nº 14.133/2021, arts. 11 e 19, IV", "Art. 19, IV dirige-se aos órgãos com competência regulamentar; para os demais, exigir adoção de modelos aplicáveis, próprios ou compartilhados."),
        ("S6.3", "Recomendação", "Determinação", "Lei nº 14.133/2021, arts. 12, VII, e 18", "A compatibilização com o PCA é obrigatória quando o plano tiver sido elaborado."),
    ]
    result = [
        {"ID": rid, "Artefato / objeto": obj, "DE": old, "PARA": new, "Motivação / justificativa": why, "Situação": "Aplicado"}
        for rid, obj, old, new, why in rows
    ]
    for idx, (sid, old, new, fundamento, ressalva) in enumerate(tipo_rows, start=25):
        result.append(
            {
                "ID": f"AJ-{idx:03d}",
                "Artefato / objeto": f"Mapa e matriz/{sid}/tipo de encaminhamento",
                "DE": old,
                "PARA": new,
                "Motivação / justificativa": f"{fundamento}. Ressalva de aplicação: {ressalva}",
                "Situação": "Aplicado",
            }
        )
    result.append(
        {
            "ID": "AJ-037",
            "Artefato / objeto": "Mapa/Ações removidas",
            "DE": ", ".join(removidas),
            "PARA": "Excluídas da versão pós-comentários",
            "Motivação / justificativa": "Ações órfãs, pertencentes às situações retiradas ou incompatíveis com as regras calibradas.",
            "Situação": "Aplicado",
        }
    )
    return sorted(result, key=lambda row: int(str(row["ID"])[3:]))


def estilizar_planilha(ws, widths: dict[str, float] | None = None) -> None:
    fill = PatternFill("solid", fgColor="1F4E78")
    for cell in ws[1]:
        cell.fill = fill
        cell.font = Font(color="FFFFFF", bold=True)
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)
    if widths:
        for column, width in widths.items():
            ws.column_dimensions[column].width = width


def gerar_planilha_ajustes(removidas: list[str], painel_preenchidos: int) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Ajustes"
    ajustes = ajuste_rows(removidas)
    headers = list(ajustes[0])
    ws.append(headers)
    for row in ajustes:
        ws.append([row[h] for h in headers])
    estilizar_planilha(ws, {"A": 12, "B": 42, "C": 60, "D": 60, "E": 95, "F": 14})

    ws = wb.create_sheet("Contradições resolvidas")
    ws.append(["Tema", "Propostas em tensão", "Decisão aplicada", "Justificativa"])
    contradicoes = [
        ("S2.2", "Proposta anterior de restringir a situação a AV11 versus orientação de manter a avaliação documental AV89", "AV11 | AV89", "A negativa declarada e a insuficiência da prova de instituição formal permanecem como gatilhos alternativos; a eventual concomitância com S2.3 deve ser interpretada como formalização não comprovada e atuação não comprovada."),
        ("S4.1", "AV26 & (AV25 | AV27) versus instrução posterior AV26 & AV25 e retirada de total_SI", "AV26 & AV25", "Prevalece a instrução posterior e específica; zero em SI não prova ausência da função."),
        ("S6.3", "Menção inicial a q2802 C-D e q2804B versus fórmula final AV82 | (AV80 | AV150)", "q2804B e q2802C", "Prevalece a fórmula final expressa; q2802D foi excluído."),
        ("S4.6", "Determinação por falta de fiscalização versus predomínio de terceiros como gatilho", "q0101B & total_TI_interno=0", "Predomínio, isoladamente, não prova infração ao art. 117; modelo C é legítimo."),
        ("S6.1", "Exigir q2801B com painel sem a coluna", "Painel vigente ampliado com B e metadados", f"Foram materializados {painel_preenchidos} registros não conformes já avaliados; nenhum resultado foi inventado."),
        ("S1.2 × S2.1", "q0103D e q1001C mediam, em grande parte, a mesma formalização de responsabilidades", "S1.2 conserva q0103D; S2.1 passa a usar somente q1001H", "Distingue competência formal da unidade de direção estratégica por objetivos, indicadores e metas."),
        ("Natureza jurídica", "Determinação baseada em dever de resultado versus norma sem artefato nominal", "Determinação com equivalência funcional e proporcionalidade", "Evita transformar PDTI, Comitê ou inventário em modelo organizacional único quando o dever jurídico admite solução equivalente."),
    ]
    for row in contradicoes:
        ws.append(row)
    estilizar_planilha(ws, {"A": 20, "B": 68, "C": 48, "D": 88})

    ws = wb.create_sheet("Encaminhamentos")
    ws.append(["Situação", "Tipo anterior", "Tipo aplicado", "Fundamento consolidado", "Ressalva de aplicação"])
    for sid, _, _, fundamento, ressalva in [
        ("S1.1", "Recomendação", "Determinação", "CF/88, art. 37; Lei nº 14.133/2021, art. 11, parágrafo único", "Admitir estrutura equivalente; não impor criação de órgão por ato do jurisdicionado se houver reserva legal."),
        ("S1.2", "Recomendação", "Determinação", "CF/88, art. 37; Lei nº 14.133/2021, art. 11, parágrafo único", "Exigir atribuições mínimas, não desenho organizacional único."),
        ("S2.2", "Recomendação", "Determinação", "Lei nº 14.133/2021, art. 11; Acórdãos TCE-RJ nº 44.490/2024 e TCU nº 1.411/2014", "TCU 1.411/2014, item 9.1, é recomendação; TCE-RJ 44.490/2024 contém determinação para casos auditados."),
        ("S2.3", "Recomendação", "Determinação", "CF/88, art. 37; Acórdão TCE-RJ nº 44.490/2024", "Somente para quem declarou Comitê."),
        ("S3.1", "Recomendação", "Determinação", "Lei nº 14.133/2021, arts. 11 e 18; precedentes TCU/TCE-RJ", "Admitir instrumento equivalente a PDTI/PEDTIC."),
        ("S3.2", "Recomendação", "Determinação", "Lei nº 14.133/2021, arts. 11 e 18; precedentes TCU/TCE-RJ", "Aprovação pela instância competente."),
        ("S3.6", "Recomendação", "Determinação", "CF/88, art. 37; Acórdão TCE-RJ nº 44.490/2024, II.3.5", "Vincular ao plano adotado."),
        ("S4.6", "Recomendação", "Determinação", "Lei nº 14.133/2021, art. 117", "A norma impõe fiscalização, não quadro próprio; regra exige terceirização e zero de pessoal interno."),
        ("S5.3", "Recomendação", "Determinação", "LGPD, arts. 46 e 50", "Inventário é meio de demonstrar segurança/governança, não artefato nominal da LGPD."),
        ("S5.5", "Recomendação", "Determinação", "LGPD, arts. 46 e 48", "Comunicação legal para incidentes com risco ou dano relevante."),
        ("S6.1", "Recomendação", "Determinação", "Lei nº 14.133/2021, arts. 11 e 19, IV", "Art. 19, IV, tem destinatário qualificado; admitir modelos compartilhados aplicáveis."),
        ("S6.3", "Recomendação", "Determinação", "Lei nº 14.133/2021, arts. 12, VII, e 18", "Compatibilização com PCA quando elaborado."),
    ]:
        ws.append([sid, "Recomendação", "Determinação", fundamento, ressalva])
    estilizar_planilha(ws, {"A": 12, "B": 18, "C": 18, "D": 70, "E": 90})

    ws = wb.create_sheet("Ações removidas")
    ws.append(["Ação", "Tratamento", "Motivo"])
    for acao_id in removidas:
        ws.append([acao_id, "Removida da versão pós-comentários", "Órfã, pertencente a S4.4/S4.5 ou excluída por calibração/desacoplamento da regra."])
    estilizar_planilha(ws, {"A": 14, "B": 38, "C": 85})

    ws = wb.create_sheet("Ordem de implementação")
    ws.append(["Ordem", "Etapa", "Produto / controle", "Critério de aceite"])
    etapas = [
        (1, "Congelar os insumos vigentes e criar versões novas", "Mapa, matriz e painel com nomes pós-comentários", "Nenhum arquivo vigente substituído."),
        (2, "Resolver contradições e fixar as fórmulas canônicas", "Aba Contradições resolvidas", "Uma única regra por situação, com precedência documentada."),
        (3, "Atualizar as fontes temporais do mapa", "Aba Fontes de Informação", "Base e painel pós-comentários identificados pelo nome correto."),
        (4, "Calibrar as ações declaratórias e documentais", "Aba Ações de Verificação", "Todas as colunas existem nas fontes e cada ação pertence a uma fórmula."),
        (5, "Reescrever as seis fórmulas de achado", "Aba Procedimentos de Auditoria", "Fórmulas parseáveis e sem ação inexistente."),
        (6, "Sincronizar motivos do relatório", "Aba Motivos do Relatório", "Condições e referências usam somente ações mantidas."),
        (7, "Eliminar variáveis temporárias não usadas", "Aba Variáveis Temporárias", "Somente total_TI e total_TI_interno permanecem."),
        (8, "Materializar q2801B no painel pós-comentários", "Painel revisado", "Coluna e metadados presentes; dados derivados de avaliações existentes."),
        (9, "Sincronizar a matriz de planejamento", "Matriz pós-comentários", "Descrições, itens, regras, critérios e tipos iguais ao mapa."),
        (10, "Executar validação estrutural", "Validador do executa_auditoria.py", "Sem erro e sem aviso de ação órfã."),
        (11, "Reexecutar a auditoria somente-dados", "JSON/XLSX temporários", "Processamento integral dos auditados sem erro de fonte, coluna ou lógica."),
        (12, "Comparar impacto e revisar amostras limítrofes", "Comparativo antes/depois", "Dupla contagem removida e determinações confirmadas pela equipe de auditoria."),
        (13, "Regenerar matriz de achados e relatórios", "Produtos derivados", "Produtos usam exclusivamente o novo mapa e os insumos pós-comentários."),
        (14, "Aprovação humana final", "Registro de revisão", "Equipe confirma mérito, critérios, proporcionalidade e competência de cada determinação."),
    ]
    for row in etapas:
        ws.append(row)
    estilizar_planilha(ws, {"A": 10, "B": 58, "C": 48, "D": 90})

    ws = wb.create_sheet("Validações")
    ws.append(["Validação", "Resultado", "Observação"])
    resultados_disponiveis = RESULTADO_ANTERIOR.exists() and RESULTADO_REVISADO.exists()
    for row in [
        ("Original preservado", "Aprovado", f"Foi criada nova versão; {MAPA_ORIGINAL.relative_to(ROOT)} não foi sobrescrito."),
        ("Mapa estrutural", "Aprovado" if resultados_disponiveis else "Pendente de execução", "Validador de scripts/executa_auditoria.py concluído sem erro." if resultados_disponiveis else "scripts/executa_auditoria.py"),
        ("Ações órfãs", "Aprovado: zero" if resultados_disponiveis else "Pendente de execução", f"As {len(set().union(*(ids_formula(formula) for formula in FORMULAS.values())))} ações remanescentes são referenciadas nas fórmulas."),
        ("Execução pós-comentários", "Aprovada" if resultados_disponiveis else "Pendente de execução", "113 auditados avaliados; 6 cadastros sem resposta válida não foram individualmente executados." if resultados_disponiveis else "Saída em /tmp/tcerj-igovti-2026/revisao-mapa"),
        ("Sincronia matriz × mapa", "Aprovada" if resultados_disponiveis else "Pendente de execução", f"Regras críticas conferidas e DOCX de validação gerado a partir de {MATRIZ_SAIDA.relative_to(ROOT)}."),
        ("Revisão humana", "Obrigatória", "As saídas são minuta técnica para deliberação da equipe de auditoria."),
    ]:
        ws.append(row)
    estilizar_planilha(ws, {"A": 38, "B": 28, "C": 95})

    if resultados_disponiveis:
        def contar_situacoes(path: Path) -> tuple[dict[str, int], int, int]:
            data = json.loads(path.read_text(encoding="utf-8"))
            contagem: dict[str, int] = defaultdict(int)
            achados_org_procedimento = 0
            avaliados = 0
            for auditado in data.values():
                if auditado.get("status_avaliacao") == "avaliado":
                    avaliados += 1
                for procedimento in auditado.get("procedimentos_executados", []):
                    achado = procedimento.get("achado")
                    if not achado:
                        continue
                    achados_org_procedimento += 1
                    for situacao in achado.get("situacoes_encontradas", []):
                        contagem[situacao] += 1
            return dict(contagem), achados_org_procedimento, avaliados

        antes, achados_antes, avaliados_antes = contar_situacoes(RESULTADO_ANTERIOR)
        depois, achados_depois, avaliados_depois = contar_situacoes(RESULTADO_REVISADO)
        ws = wb.create_sheet("Impacto da reexecução")
        ws.append(["Situação", "Descrição anterior", "Ocorrências antes", "Descrição revisada", "Ocorrências depois", "Variação", "Observação"])
        for sid in sorted(set(SITUACOES_ANTERIORES) | set(SITUACOES), key=lambda valor: tuple(map(int, valor[1:].split(".")))):
            descricao_antes = SITUACOES_ANTERIORES.get(sid, "Não configurada")
            descricao_depois = SITUACOES.get(sid, "Retirada do achado")
            qtd_antes = antes.get(descricao_antes, 0)
            qtd_depois = depois.get(descricao_depois, 0) if sid in SITUACOES else 0
            observacao = "Situação retirada" if sid not in SITUACOES else ("Sem ocorrência na base pós-comentários" if qtd_depois == 0 else "")
            ws.append([sid.upper(), descricao_antes, qtd_antes, descricao_depois, qtd_depois, qtd_depois - qtd_antes, observacao])
        ws.append(["TOTAL", "Situações registradas", sum(antes.values()), "Situações registradas", sum(depois.values()), sum(depois.values()) - sum(antes.values()), ""])
        ws.append(["ACHADOS", "Órgão × procedimento", achados_antes, "Órgão × procedimento", achados_depois, achados_depois - achados_antes, ""])
        ws.append(["AUDITADOS", "Avaliados", avaliados_antes, "Avaliados", avaliados_depois, avaliados_depois - avaliados_antes, ""])
        estilizar_planilha(ws, {"A": 14, "B": 62, "C": 20, "D": 62, "E": 20, "F": 14, "G": 45})

    PLANILHA_AJUSTES.parent.mkdir(parents=True, exist_ok=True)
    wb.save(PLANILHA_AJUSTES)


def main() -> None:
    ids_usados, removidas = gerar_mapa()
    painel_preenchidos = gerar_painel()
    gerar_matriz()
    gerar_planilha_ajustes(removidas, painel_preenchidos)
    print(f"Mapa: {MAPA_SAIDA}")
    print(f"Matriz: {MATRIZ_SAIDA}")
    print(f"Painel: {PAINEL_SAIDA}")
    print(f"Planilha de ajustes: {PLANILHA_AJUSTES}")
    print(f"Ações usadas: {len(ids_usados)}")
    print(f"Ações removidas: {len(removidas)}")
    print(f"Registros q2801ext[B] materializados: {painel_preenchidos}")


if __name__ == "__main__":
    main()
