import os
import re
from typing import List, Dict, Set
from argos_classes import Auditado, Achado


DEFAULT_ADMIN_NAME = 'CAD-TI'
DEFAULT_ADMIN_EMAIL = 'auditoriati@tcerj.tc.br'
DEFAULT_FISCALIZACAO_NUMERO = '18/2026'
DEFAULT_FISCALIZACAO_NOME = 'iGovTI 2026'

class LimeSurveyGenerator:
    """Gera .lss consolidado espelhando EXATAMENTE o template DOCX"""

    def __init__(self):
        self.language = 'pt-BR'
        self.format = 'G'

    def _esc(self, text: str) -> str:
        """Escapa para CDATA"""
        if not text:
            return ''
        return str(text).replace(']]>', ']]]]><![CDATA[>')

    def generate_xml(
        self,
        auditados: List[Auditado],
        admin_name: str = DEFAULT_ADMIN_NAME,
        admin_email: str = DEFAULT_ADMIN_EMAIL,
        expires: str = '',
        reavaliacao_evidencias: list[dict[str, object]] | None = None,
        auditados_nao_respondentes: List[Auditado] | None = None,
        fiscalizacao_numero: str = DEFAULT_FISCALIZACAO_NUMERO,
        fiscalizacao_nome: str = DEFAULT_FISCALIZACAO_NOME,
    ) -> str:
        """Gera um único XML consolidado para todos os auditados"""
        reavaliacao_evidencias = reavaliacao_evidencias or {}
        auditados_nao_respondentes = auditados_nao_respondentes or []
        if not auditados and not reavaliacao_evidencias and not auditados_nao_respondentes:
            return ""

        # Mapeia situações únicas e quais auditados as possuem
        # Chave: (numero_achado, nome_achado, texto_situacao)
        # Valor: Set de siglas
        situacoes_map: Dict[tuple, Set[str]] = {}
        # Para armazenar evidências acumuladas por situação (opcional, mas bom para contexto)
        evidencias_map: Dict[tuple, Set[str]] = {}

        for auditado in auditados:
            achados = [p.achado for p in auditado.procedimentos_executados if p.achado is not None]
            for achado in achados:
                sits = achado.situacoes_encontradas if achado.situacoes_encontradas else ['']

                for sit in sits:
                    key = (achado.numero, achado.nome, sit)

                    if key not in situacoes_map:
                        situacoes_map[key] = set()
                        evidencias_map[key] = set()

                    situacoes_map[key].add(auditado.sigla)

                    # Adiciona evidências do achado ao contexto da situação
                    for ev in achado.evidencias:
                        evidencias_map[key].add(ev)

        xml = self._build_xml(
            situacoes_map,
            evidencias_map,
            admin_name,
            admin_email,
            expires,
            reavaliacao_evidencias,
            auditados_nao_respondentes,
            fiscalizacao_numero,
            fiscalizacao_nome,
        )
        return xml

    def _build_xml(
        self,
        situacoes_map: Dict[tuple, Set[str]],
        evidencias_map: Dict[tuple, Set[str]],
        admin_name: str,
        admin_email: str,
        expires: str,
        reavaliacao_evidencias: list[dict[str, object]],
        auditados_nao_respondentes: List[Auditado],
        fiscalizacao_numero: str,
        fiscalizacao_nome: str,
    ) -> str:
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n<document>\n'
        xml += ' <LimeSurveyDocType>Survey</LimeSurveyDocType>\n'
        xml += ' <DBVersion>363</DBVersion>\n'
        xml += ' <languages>\n  <language>pt-BR</language>\n </languages>\n'

        def safe_sort_key(x):
            import pandas as pd
            num = x[0]
            sit = x[2]
            if pd.isna(sit) or sit is None:
                sit = ""
            else:
                sit = str(sit).strip()

            try:
                if num is None or pd.isna(num):
                    val = 0
                elif isinstance(num, (int, float)):
                    import math
                    val = int(num) if not math.isnan(num) else 0
                else:
                    val = int(float(str(num).strip()))
            except (ValueError, TypeError):
                val = str(num)
            
            if isinstance(val, int):
                return (0, val, sit)
            else:
                return (1, val, sit)

        sorted_keys = sorted(situacoes_map.keys(), key=safe_sort_key)
        reavaliacao_entries = self._sort_reavaliacao_evidencias(reavaliacao_evidencias)

        # ORDEM CORRETA:
        xml += self._build_answers(sorted_keys, reavaliacao_entries, auditados_nao_respondentes)       # 1. answers
        xml += self._build_groups(
            sorted_keys,
            situacoes_map,
            evidencias_map,
            reavaliacao_entries,
            auditados_nao_respondentes,
            fiscalizacao_nome,
        )        # 2. groups
        questions_xml, upload_qids, ciencia_qid, ciencia_gid = self._build_questions(
            sorted_keys,
            reavaliacao_entries,
            auditados_nao_respondentes,
            fiscalizacao_nome,
        )
        xml += questions_xml     # 3. questions
        xml += self._build_subquestions(ciencia_qid, ciencia_gid) # 4. subquestions
        xml += self._build_question_attributes(upload_qids) # 5. question_attributes
        xml += self._build_surveys(admin_name, admin_email, expires)              # 6. surveys
        xml += self._build_surveys_lang(admin_email, fiscalizacao_numero, fiscalizacao_nome) # 7. surveys_languagesettings

        xml += '</document>'
        return xml

    def _sort_reavaliacao_evidencias(
        self,
        reavaliacao_evidencias: list[dict[str, object]],
    ) -> list[dict[str, object]]:
        return sorted(
            (dict(entry) for entry in reavaliacao_evidencias),
            key=lambda item: self._base_sort_key(item.get("base", "")),
        )

    def _base_sort_key(self, base: object) -> tuple[int, str]:
        match = re.search(r"(\d+)", str(base or ""))
        return (int(match.group(1)) if match else 999999, str(base or ""))

    def _build_groups(
        self,
        sorted_keys: List[tuple],
        situacoes_map: Dict[tuple, Set[str]],
        evidencias_map: Dict[tuple, Set[str]],
        reavaliacao_entries: list[dict[str, object]],
        auditados_nao_respondentes: List[Auditado],
        fiscalizacao_nome: str,
    ) -> str:
        xml = ' <groups>\n  <fields>\n'
        xml += '   <fieldname>gid</fieldname>\n   <fieldname>sid</fieldname>\n'
        xml += '   <fieldname>group_name</fieldname>\n   <fieldname>group_order</fieldname>\n'
        xml += '   <fieldname>description</fieldname>\n   <fieldname>language</fieldname>\n'
        xml += '   <fieldname>randomization_group</fieldname>\n   <fieldname>grelevance</fieldname>\n'
        xml += '  </fields>\n  <rows>\n'

        # Grupo 1: Identificação (Sempre visível)
        xml += '   <row>\n'
        xml += '    <gid><![CDATA[1]]></gid>\n    <sid><![CDATA[0]]></sid>\n'
        xml += '    <group_name><![CDATA[Identificação]]></group_name>\n'
        xml += '    <group_order><![CDATA[1]]></group_order>\n'
        xml += '    <description><![CDATA[Por favor, preencha seus dados:]]></description>\n'
        xml += '    <language><![CDATA[pt-BR]]></language>\n'
        xml += '    <randomization_group/>\n    <grelevance/>\n'
        xml += '   </row>\n'

        gid = 2
        group_order = 2

        for key in sorted_keys:
            achado_num, achado_nome, situacao_texto = key
            siglas = sorted(list(situacoes_map[key]), key=str)
            evidencias = sorted(list(evidencias_map[key]), key=str)

            # Constrói a grelevance
            conditions = [f'TOKEN:FIRSTNAME == "{sigla}"' for sigla in siglas]
            grelevance = " OR ".join(conditions)

            # Descrição completa
            desc = f'<h4>Achado {achado_num}: {self._esc(achado_nome)}</h4>'
            desc += '<p>O Relatório Individual apresenta e descreve as situações que ensejaram a ocorrência deste achado, as evidências levantadas, critérios aplicados as propostas de encaminhamento sugeridas pela Equipe de Auditoria.</p>'

            # Situação Específica deste grupo
            if situacao_texto:
                desc += f'<p><strong>Situação identificada:</strong> {self._esc(situacao_texto)}</p>'

            # Instruções
            desc += '<hr/>'
            desc += '<p><strong>INSTRUÇÕES:</strong></p>'
            desc += '<ul>'
            desc += '<li>Se <strong>concordar</strong>: Use o campo "Comentários" para informar ações corretivas, avaliação sobre as propostas e consequências práticas.</li>'
            desc += '<li>Se <strong>discordar</strong>: Use o campo "Justificativa" para apresentar as razões da discordância e envie documentos comprobatórios.</li>'
            desc += '</ul>'

            group_name = f'Achado {achado_num}'

            xml += '   <row>\n'
            xml += f'    <gid><![CDATA[{gid}]]></gid>\n    <sid><![CDATA[0]]></sid>\n'
            xml += f'    <group_name><![CDATA[{group_name}]]></group_name>\n'
            xml += f'    <group_order><![CDATA[{group_order}]]></group_order>\n'
            xml += f'    <description><![CDATA[{desc}]]></description>\n'
            xml += '    <language><![CDATA[pt-BR]]></language>\n'
            xml += '    <randomization_group/>\n'
            xml += f'    <grelevance><![CDATA[{grelevance}]]></grelevance>\n'
            xml += '   </row>\n'

            gid += 1
            group_order += 1

        for entry in reavaliacao_entries:
            base = str(entry.get("base", ""))
            base_texto = str(entry.get("base_texto", base))
            auditados = sorted(str(auditado) for auditado in (entry.get("auditados") or []))
            conditions = [f'TOKEN:FIRSTNAME == "{self._esc(auditado)}"' for auditado in auditados]
            grelevance = " OR ".join(conditions) if conditions else "0"

            desc = '<h4>Retificação ou suplementação de evidências</h4>'
            desc += f'<p><strong>Questão-base {self._esc(base)}:</strong> {self._esc(base_texto)}</p>'
            desc += '<p>A avaliação de evidências indicou não conformidade em pelo menos um item ou subitem vinculado a esta questão-base. Caso entenda necessário, a organização poderá apresentar esclarecimentos e encaminhar evidência suplementar para reavaliação.</p>'
            desc += '<p>Consulte no relatório individual ou anexo correspondente os itens específicos avaliados como não conformes.</p>'

            xml += '   <row>\n'
            xml += f'    <gid><![CDATA[{gid}]]></gid>\n    <sid><![CDATA[0]]></sid>\n'
            xml += f'    <group_name><![CDATA[Reavaliação de evidências - {self._esc(base)}]]></group_name>\n'
            xml += f'    <group_order><![CDATA[{group_order}]]></group_order>\n'
            xml += f'    <description><![CDATA[{desc}]]></description>\n'
            xml += '    <language><![CDATA[pt-BR]]></language>\n'
            xml += '    <randomization_group/>\n'
            xml += f'    <grelevance><![CDATA[{grelevance}]]></grelevance>\n'
            xml += '   </row>\n'

            gid += 1
            group_order += 1

        if auditados_nao_respondentes:
            siglas = sorted({auditado.sigla for auditado in auditados_nao_respondentes}, key=str)
            conditions = [f'TOKEN:FIRSTNAME == "{self._esc(sigla)}"' for sigla in siglas]
            grelevance = " OR ".join(conditions) if conditions else "0"

            fiscalizacao_nome = self._esc(fiscalizacao_nome)
            desc = f'<h4>Manifestação sobre ausência de resposta ao questionário {fiscalizacao_nome}</h4>'
            desc += f'<p>Não foi identificada resposta válida ao questionário {fiscalizacao_nome} para esta organização nas bases processadas pela Equipe de Auditoria.</p>'
            desc += '<p>Esta seção permite apresentar esclarecimentos, comprovação de eventual resposta encaminhada ou justificativa para a ausência de resposta válida.</p>'
            desc += '<p>A manifestação nesta seção não corresponde à contestação de achados nem à reavaliação de evidências, pois não houve resposta válida e documentação comprobatória avaliadas para a organização.</p>'

            xml += '   <row>\n'
            xml += f'    <gid><![CDATA[{gid}]]></gid>\n    <sid><![CDATA[0]]></sid>\n'
            xml += '    <group_name><![CDATA[Ausência de resposta ao questionário]]></group_name>\n'
            xml += f'    <group_order><![CDATA[{group_order}]]></group_order>\n'
            xml += f'    <description><![CDATA[{desc}]]></description>\n'
            xml += '    <language><![CDATA[pt-BR]]></language>\n'
            xml += '    <randomization_group/>\n'
            xml += f'    <grelevance><![CDATA[{grelevance}]]></grelevance>\n'
            xml += '   </row>\n'

            gid += 1
            group_order += 1

        xml += '   <row>\n'
        xml += f'    <gid><![CDATA[{gid}]]></gid>\n    <sid><![CDATA[0]]></sid>\n'
        xml += '    <group_name><![CDATA[Ciência]]></group_name>\n'
        xml += f'    <group_order><![CDATA[{group_order}]]></group_order>\n'
        xml += '    <description/>\n'
        xml += '    <language><![CDATA[pt-BR]]></language>\n'
        xml += '    <randomization_group/>\n    <grelevance/>\n'
        xml += '   </row>\n'

        xml += '  </rows>\n </groups>\n'
        return xml

    def _build_questions(
        self,
        sorted_keys: List[tuple],
        reavaliacao_entries: list[dict[str, object]],
        auditados_nao_respondentes: List[Auditado],
        fiscalizacao_nome: str,
    ) -> tuple[str, list[int], int, int]:
        xml = ' <questions>\n  <fields>\n'
        xml += '   <fieldname>qid</fieldname>\n   <fieldname>parent_qid</fieldname>\n'
        xml += '   <fieldname>sid</fieldname>\n   <fieldname>gid</fieldname>\n'
        xml += '   <fieldname>type</fieldname>\n   <fieldname>title</fieldname>\n'
        xml += '   <fieldname>question</fieldname>\n   <fieldname>preg</fieldname>\n'
        xml += '   <fieldname>help</fieldname>\n   <fieldname>other</fieldname>\n'
        xml += '   <fieldname>mandatory</fieldname>\n   <fieldname>question_order</fieldname>\n'
        xml += '   <fieldname>language</fieldname>\n   <fieldname>scale_id</fieldname>\n'
        xml += '   <fieldname>same_default</fieldname>\n   <fieldname>relevance</fieldname>\n'
        xml += '   <fieldname>modulename</fieldname>\n'
        xml += '  </fields>\n  <rows>\n'

        qid = 1
        upload_qids: list[int] = []

        # Identificação (4 perguntas) - Grupo 1
        for title, question, mandatory in [
            ('nome', 'Nome completo', 'Y'),
            ('cargo', 'Cargo/Função', 'Y'),
            ('email', 'E-mail', 'Y'),
            ('telefone', 'Telefone (opcional)', 'N')
        ]:
            xml += self._q_row(qid, 1, title, question, 'S', mandatory, qid)
            qid += 1

        # Achados
        gid = 2

        for idx, key in enumerate(sorted_keys, 1):
            achado_num, achado_nome, situacao_texto = key
            q_order = 1
            base_code = f'A{achado_num}G{idx}'

            # P1: Concordância (4 opções)
            if situacao_texto:
                q_text = f'No que tange à situação "<strong>{self._esc(situacao_texto)}</strong>" apontada no Relatório Individual, a organização:'
            else:
                q_text = f'Em relação ao Achado {achado_num}, a organização:'

            xml += self._q_row(qid, gid, f'{base_code}Conc', q_text, 'L', 'Y', q_order)
            qid += 1
            q_order += 1

            # Logic expressions
            relevance_conc = f'(({base_code}Conc.NAOK == "SQ001" or {base_code}Conc.NAOK == "SQ002" or {base_code}Conc.NAOK == "SQ003"))'
            relevance_disc = f'(({base_code}Conc.NAOK == "SQ006"))'
            relevance_evi  = f'(({base_code}Conc.NAOK == "SQ001" or {base_code}Conc.NAOK == "SQ002" or {base_code}Conc.NAOK == "SQ006"))'

            # P2: Comentários (se concordar)
            q_text_coment = '(Opcional) Caso desejável, encaminhem seus comentários contemplando a perspectiva da organização e as ações corretivas que pretendem tomar, bem como avaliação sobre as propostas de determinação e/ou recomendação formuladas, informando sobre as consequências práticas de sua implementação e eventuais alternativas.'
            xml += self._q_row(qid, gid, f'{base_code}Com',
                q_text_coment,
                'T', 'N', q_order,
                'Se concordar de alguma forma com o achado, use este campo para tecer esclarecimentos.',
                relevance=relevance_conc)
            qid += 1
            q_order += 1

            # P3: Justificativa (se discordar)
            q_text_justif = 'Ajude-nos a entender por que você escolheu a opção acima'
            xml += self._q_row(qid, gid, f'{base_code}Jus',
                q_text_justif,
                'T', 'Y', q_order,
                'Se discordar, apresente as razões da sua discordância.',
                relevance=relevance_disc)
            qid += 1
            q_order += 1

            # P4: Documentos
            xml += self._q_row(qid, gid, f'{base_code}Evi',
                'Caso necessário, envie documentos que evidenciem suas justificativas',
                '|', 'N', q_order,
                'É aceito arquivo com extensão PDF ou ZIP. Caso haja mais de um arquivo, compactar em formato ZIP.',
                relevance=relevance_evi)
            upload_qids.append(qid)
            qid += 1
            q_order += 1

            # Avança Grupo
            gid += 1

        for idx, entry in enumerate(reavaliacao_entries, 1):
            base = str(entry.get("base", ""))
            safe_base = re.sub(r"[^A-Za-z0-9]", "", base).upper() or f"B{idx}"
            base_code = f'REV{safe_base}'

            xml += self._q_row(qid, gid, f'{base_code}Com',
                'Caso deseje, apresente comentários, esclarecimentos ou retificações sobre a avaliação de evidências desta questão.',
                'T', 'N', 1,
                'Campo opcional para contextualizar a evidência suplementar ou apresentar esclarecimentos adicionais.')
            qid += 1

            xml += self._q_row(qid, gid, f'{base_code}Evi',
                'Caso deseje, envie uma evidência suplementar para reavaliação',
                '|', 'N', 2,
                'É aceito um arquivo com extensão PDF ou ZIP. Caso haja mais de um documento, compactar em formato ZIP.')
            upload_qids.append(qid)
            qid += 1
            gid += 1

        if auditados_nao_respondentes:
            xml += self._q_row(qid, gid, 'NRStatus',
                f'Em relação à ausência de resposta válida ao questionário {self._esc(fiscalizacao_nome)}, a organização:',
                'L', 'Y', 1,
                'Selecione a opção que melhor descreve a manifestação da organização.')
            qid += 1

            relevance_texto = '((NRStatus.NAOK == "SQ002" or NRStatus.NAOK == "SQ003"))'
            xml += self._q_row(qid, gid, 'NRTexto',
                'Apresente os esclarecimentos, a comprovação do envio anterior ou a justificativa para a ausência de resposta válida.',
                'T', 'Y', 2,
                'Informe data, protocolo, e-mail, processo ou outro elemento de comprovação, quando aplicável.',
                relevance=relevance_texto)
            qid += 1

            xml += self._q_row(qid, gid, 'NREvi',
                'Caso necessário, envie documento que comprove a manifestação apresentada.',
                '|', 'N', 3,
                'É aceito um arquivo com extensão PDF ou ZIP. Caso haja mais de um documento, compactar em formato ZIP.',
                relevance=relevance_texto)
            upload_qids.append(qid)
            qid += 1
            gid += 1

        ciencia_qid = qid
        ciencia_gid = gid
        xml += self._q_row(
            ciencia_qid,
            ciencia_gid,
            'qciencia',
            '',
            'M',
            'Y',
            0,
        )

        xml += '  </rows>\n </questions>\n'
        return xml, upload_qids, ciencia_qid, ciencia_gid

    def _build_subquestions(self, ciencia_qid: int, ciencia_gid: int) -> str:
        subquestion_qid = ciencia_qid + 1
        declaracao = (
            'Declaro estar ciente de que a responsabilidade pelas respostas dadas ao questionário '
            'é do dirigente máximo da organização, com base nas respostas providas pelos diversos '
            'setores da organização e reunidas por mim.'
        )
        xml = ' <subquestions>\n  <fields>\n'
        xml += '   <fieldname>qid</fieldname>\n   <fieldname>parent_qid</fieldname>\n'
        xml += '   <fieldname>sid</fieldname>\n   <fieldname>gid</fieldname>\n'
        xml += '   <fieldname>type</fieldname>\n   <fieldname>title</fieldname>\n'
        xml += '   <fieldname>question</fieldname>\n   <fieldname>help</fieldname>\n'
        xml += '   <fieldname>other</fieldname>\n   <fieldname>question_order</fieldname>\n'
        xml += '   <fieldname>language</fieldname>\n   <fieldname>scale_id</fieldname>\n'
        xml += '   <fieldname>same_default</fieldname>\n   <fieldname>relevance</fieldname>\n'
        xml += '  </fields>\n  <rows>\n'
        xml += '   <row>\n'
        xml += f'    <qid><![CDATA[{subquestion_qid}]]></qid>\n'
        xml += f'    <parent_qid><![CDATA[{ciencia_qid}]]></parent_qid>\n'
        xml += '    <sid><![CDATA[0]]></sid>\n'
        xml += f'    <gid><![CDATA[{ciencia_gid}]]></gid>\n'
        xml += '    <type><![CDATA[T]]></type>\n'
        xml += '    <title><![CDATA[SQ001]]></title>\n'
        xml += f'    <question><![CDATA[{declaracao}]]></question>\n'
        xml += '    <help/>\n    <other><![CDATA[N]]></other>\n'
        xml += '    <question_order><![CDATA[1]]></question_order>\n'
        xml += '    <language><![CDATA[pt-BR]]></language>\n'
        xml += '    <scale_id><![CDATA[0]]></scale_id>\n'
        xml += '    <same_default><![CDATA[0]]></same_default>\n'
        xml += '    <relevance><![CDATA[1]]></relevance>\n'
        xml += '   </row>\n'
        xml += '  </rows>\n </subquestions>\n'
        return xml

    def _q_row(self, qid: int, gid: int, title: str, question: str, qtype: str,
               mandatory: str, order: int, help_text: str = '', relevance: str = '1') -> str:
        """Gera linha de pergunta"""
        xml = '   <row>\n'
        xml += f'    <qid><![CDATA[{qid}]]></qid>\n'
        xml += '    <parent_qid><![CDATA[0]]></parent_qid>\n'
        xml += '    <sid><![CDATA[0]]></sid>\n'
        xml += f'    <gid><![CDATA[{gid}]]></gid>\n'
        xml += f'    <type><![CDATA[{qtype}]]></type>\n'
        xml += f'    <title><![CDATA[{title}]]></title>\n'
        xml += f'    <question><![CDATA[{question}]]></question>\n'
        xml += '    <preg/>\n'
        xml += f'    <help><![CDATA[{help_text}]]></help>\n'
        xml += '    <other><![CDATA[N]]></other>\n'
        xml += f'    <mandatory><![CDATA[{mandatory}]]></mandatory>\n'
        xml += f'    <question_order><![CDATA[{order}]]></question_order>\n'
        xml += '    <language><![CDATA[pt-BR]]></language>\n'
        xml += '    <scale_id><![CDATA[0]]></scale_id>\n'
        xml += '    <same_default><![CDATA[0]]></same_default>\n'
        xml += f'    <relevance><![CDATA[{relevance}]]></relevance>\n'
        xml += '    <modulename/>\n'
        xml += '   </row>\n'
        return xml

    def _build_answers(
        self,
        sorted_keys: List[tuple],
        reavaliacao_entries: list[dict[str, object]],
        auditados_nao_respondentes: List[Auditado],
    ) -> str:
        """Gera opções de resposta para perguntas de lista."""
        xml = ' <answers>\n  <fields>\n'
        xml += '   <fieldname>qid</fieldname>\n   <fieldname>code</fieldname>\n'
        xml += '   <fieldname>answer</fieldname>\n   <fieldname>sortorder</fieldname>\n'
        xml += '   <fieldname>assessment_value</fieldname>\n   <fieldname>language</fieldname>\n'
        xml += '   <fieldname>scale_id</fieldname>\n'
        xml += '  </fields>\n  <rows>\n'

        # QID inicial: 5 (após as 4 perguntas de identificação)
        qid = 5

        for _ in sorted_keys:
            for code, answer, sort in [
                ('SQ001', 'Concorda e já atendeu às propostas de encaminhamento', 1),
                ('SQ002', 'Concorda e já está atendendo às propostas de encaminhamento', 2),
                ('SQ003', 'Concorda, mas ainda não adotou nenhuma medida para atender às propostas de encaminhamento', 3),
                ('SQ006', 'Discorda da sinalização de inadequação', 4)
            ]:
                xml += '   <row>\n'
                xml += f'    <qid><![CDATA[{qid}]]></qid>\n'
                xml += f'    <code><![CDATA[{code}]]></code>\n'
                xml += f'    <answer><![CDATA[{answer}]]></answer>\n'
                xml += f'    <sortorder><![CDATA[{sort}]]></sortorder>\n'
                xml += '    <assessment_value><![CDATA[0]]></assessment_value>\n'
                xml += '    <language><![CDATA[pt-BR]]></language>\n'
                xml += '    <scale_id><![CDATA[0]]></scale_id>\n'
                xml += '   </row>\n'

            # Avança 4 perguntas por situação
            qid += 4

        if auditados_nao_respondentes:
            qid += len(reavaliacao_entries) * 2
            for code, answer, sort in [
                ('SQ001', 'Confirma a ausência de resposta válida ao questionário', 1),
                ('SQ002', 'Informa que encaminhou resposta e deseja apresentar comprovação', 2),
                ('SQ003', 'Apresenta justificativa para a ausência de resposta válida', 3),
            ]:
                xml += '   <row>\n'
                xml += f'    <qid><![CDATA[{qid}]]></qid>\n'
                xml += f'    <code><![CDATA[{code}]]></code>\n'
                xml += f'    <answer><![CDATA[{answer}]]></answer>\n'
                xml += f'    <sortorder><![CDATA[{sort}]]></sortorder>\n'
                xml += '    <assessment_value><![CDATA[0]]></assessment_value>\n'
                xml += '    <language><![CDATA[pt-BR]]></language>\n'
                xml += '    <scale_id><![CDATA[0]]></scale_id>\n'
                xml += '   </row>\n'

        xml += '  </rows>\n </answers>\n'
        return xml

    def _build_question_attributes(self, upload_qids: list[int]) -> str:
        if not upload_qids:
            return ''

        xml = ' <question_attributes>\n  <fields>\n'
        xml += '   <fieldname>qid</fieldname>\n   <fieldname>attribute</fieldname>\n'
        xml += '   <fieldname>value</fieldname>\n   <fieldname>language</fieldname>\n'
        xml += '  </fields>\n  <rows>\n'

        for qid in upload_qids:
            for attribute, value in [
                ('allowed_filetypes', 'pdf,zip'),
                ('max_num_of_files', '1'),
            ]:
                xml += '   <row>\n'
                xml += f'    <qid><![CDATA[{qid}]]></qid>\n'
                xml += f'    <attribute><![CDATA[{attribute}]]></attribute>\n'
                xml += f'    <value><![CDATA[{value}]]></value>\n'
                xml += '    <language/>\n'
                xml += '   </row>\n'

        xml += '  </rows>\n </question_attributes>\n'
        return xml

    def _build_surveys(self, admin_name: str, admin_email: str, expires: str) -> str:
        expires_xml = f'<expires><![CDATA[{self._esc(expires)}]]></expires>' if expires else '<expires/>'
        xml = ' <surveys>\n  <fields>\n'
        xml += '   <fieldname>sid</fieldname>\n   <fieldname>gsid</fieldname>\n'
        xml += '   <fieldname>admin</fieldname>\n   <fieldname>expires</fieldname>\n'
        xml += '   <fieldname>startdate</fieldname>\n   <fieldname>adminemail</fieldname>\n'
        xml += '   <fieldname>anonymized</fieldname>\n   <fieldname>faxto</fieldname>\n'
        xml += '   <fieldname>format</fieldname>\n   <fieldname>savetimings</fieldname>\n'
        xml += '   <fieldname>template</fieldname>\n   <fieldname>language</fieldname>\n'
        xml += '   <fieldname>additional_languages</fieldname>\n   <fieldname>datestamp</fieldname>\n'
        xml += '   <fieldname>usecookie</fieldname>\n   <fieldname>allowregister</fieldname>\n'
        xml += '   <fieldname>allowsave</fieldname>\n   <fieldname>autonumber_start</fieldname>\n'
        xml += '   <fieldname>autoredirect</fieldname>\n   <fieldname>allowprev</fieldname>\n'
        xml += '   <fieldname>printanswers</fieldname>\n   <fieldname>ipaddr</fieldname>\n'
        xml += '   <fieldname>refurl</fieldname>\n   <fieldname>showsurveypolicynotice</fieldname>\n'
        xml += '   <fieldname>publicstatistics</fieldname>\n   <fieldname>publicgraphs</fieldname>\n'
        xml += '   <fieldname>listpublic</fieldname>\n   <fieldname>htmlemail</fieldname>\n'
        xml += '   <fieldname>sendconfirmation</fieldname>\n   <fieldname>tokenanswerspersistence</fieldname>\n'
        xml += '   <fieldname>assessments</fieldname>\n   <fieldname>usecaptcha</fieldname>\n'
        xml += '   <fieldname>usetokens</fieldname>\n   <fieldname>bounce_email</fieldname>\n'
        xml += '   <fieldname>emailresponseto</fieldname>\n   <fieldname>emailnotificationto</fieldname>\n'
        xml += '   <fieldname>tokenlength</fieldname>\n   <fieldname>showxquestions</fieldname>\n'
        xml += '   <fieldname>showgroupinfo</fieldname>\n   <fieldname>shownoanswer</fieldname>\n'
        xml += '   <fieldname>showqnumcode</fieldname>\n   <fieldname>bounceprocessing</fieldname>\n'
        xml += '   <fieldname>showwelcome</fieldname>\n   <fieldname>showprogress</fieldname>\n'
        xml += '   <fieldname>questionindex</fieldname>\n   <fieldname>navigationdelay</fieldname>\n'
        xml += '   <fieldname>nokeyboard</fieldname>\n   <fieldname>alloweditaftercompletion</fieldname>\n'
        xml += '  </fields>\n  <rows>\n   <row>\n'
        xml += '    <sid><![CDATA[0]]></sid>\n    <gsid><![CDATA[1]]></gsid>\n'
        xml += f'    <admin><![CDATA[{self._esc(admin_name)}]]></admin>\n'
        xml += f'    {expires_xml}\n    <startdate/>\n'
        xml += f'    <adminemail><![CDATA[{self._esc(admin_email)}]]></adminemail>\n'
        xml += '    <anonymized><![CDATA[N]]></anonymized>\n    <faxto/>\n'
        xml += '    <format><![CDATA[G]]></format>\n'
        xml += '    <savetimings><![CDATA[N]]></savetimings>\n'
        xml += '    <template><![CDATA[fruity]]></template>\n'
        xml += '    <language><![CDATA[pt-BR]]></language>\n    <additional_languages/>\n'
        xml += '    <datestamp><![CDATA[Y]]></datestamp>\n'
        xml += '    <usecookie><![CDATA[N]]></usecookie>\n'
        xml += '    <allowregister><![CDATA[N]]></allowregister>\n'
        xml += '    <allowsave><![CDATA[Y]]></allowsave>\n'
        xml += '    <autonumber_start><![CDATA[0]]></autonumber_start>\n'
        xml += '    <autoredirect><![CDATA[N]]></autoredirect>\n'
        xml += '    <allowprev><![CDATA[Y]]></allowprev>\n'
        xml += '    <printanswers><![CDATA[Y]]></printanswers>\n'
        xml += '    <ipaddr><![CDATA[N]]></ipaddr>\n    <refurl><![CDATA[N]]></refurl>\n'
        xml += '    <showsurveypolicynotice><![CDATA[0]]></showsurveypolicynotice>\n'
        xml += '    <publicstatistics><![CDATA[N]]></publicstatistics>\n'
        xml += '    <publicgraphs><![CDATA[N]]></publicgraphs>\n'
        xml += '    <listpublic><![CDATA[N]]></listpublic>\n'
        xml += '    <htmlemail><![CDATA[Y]]></htmlemail>\n'
        xml += '    <sendconfirmation><![CDATA[Y]]></sendconfirmation>\n'
        xml += '    <tokenanswerspersistence><![CDATA[Y]]></tokenanswerspersistence>\n'
        xml += '    <assessments><![CDATA[N]]></assessments>\n'
        xml += '    <usecaptcha><![CDATA[N]]></usecaptcha>\n'
        xml += '    <usetokens><![CDATA[N]]></usetokens>\n'
        xml += f'    <bounce_email><![CDATA[{self._esc(admin_email)}]]></bounce_email>\n'
        xml += '    <emailresponseto/>\n    <emailnotificationto/>\n'
        xml += '    <tokenlength><![CDATA[15]]></tokenlength>\n'
        xml += '    <showxquestions><![CDATA[N]]></showxquestions>\n'
        xml += '    <showgroupinfo><![CDATA[B]]></showgroupinfo>\n'
        xml += '    <shownoanswer><![CDATA[N]]></shownoanswer>\n'
        xml += '    <showqnumcode><![CDATA[X]]></showqnumcode>\n'
        xml += '    <bounceprocessing><![CDATA[N]]></bounceprocessing>\n'
        xml += '    <showwelcome><![CDATA[Y]]></showwelcome>\n'
        xml += '    <showprogress><![CDATA[Y]]></showprogress>\n'
        xml += '    <questionindex><![CDATA[0]]></questionindex>\n'
        xml += '    <navigationdelay><![CDATA[0]]></navigationdelay>\n'
        xml += '    <nokeyboard><![CDATA[N]]></nokeyboard>\n'
        xml += '    <alloweditaftercompletion><![CDATA[N]]></alloweditaftercompletion>\n'
        xml += '   </row>\n  </rows>\n </surveys>\n'
        return xml

    def _build_surveys_lang(self, admin_email: str, fiscalizacao_numero: str, fiscalizacao_nome: str) -> str:
        fiscalizacao_numero = self._esc(fiscalizacao_numero)
        fiscalizacao_nome = self._esc(fiscalizacao_nome)
        admin_email = self._esc(admin_email)
        fiscalizacao_label = f"Fiscalização TCE-RJ nº {fiscalizacao_numero} - {fiscalizacao_nome}"
        welcome = f'''<div class="container mt-3" style="margin-top:20px;margin-bottom:20px;">
  <div class="row align-items-center">
    <div class="col-md-4">
      <img alt="Logotipo TCERJ" class="img-fluid" src="https://www.tcerj.tc.br/cdn-storage/logos/logo-horizontal-colorida-para_fundo_branco@3x.png" style="max-width:300px;" />
    </div>

    <div class="col-md-8">
      <h1 style="font-size:16px;font-weight:bold;color:#444;margin:0;margin-top:20px;">SECRETARIA-GERAL DE CONTROLE EXTERNO</h1>
      <p style="font-size:12px;color:#666;margin:2px 0;">SUBSECRETARIA DE CONTROLE DE POLÍTICAS DE CIDADANIA</p>
      <p style="font-size:12px;color:#666;margin:2px 0;">COORDENADORIA DE AUDITORIA EM POLÍTICAS DE TECNOLOGIA DA INFORMAÇÃO</p>
    </div>
  </div>
</div>

<div style="text-align:justify;color:#000000;">
  <p style="color:#000000;">Prezado(a) Gestor(a) da {{TOKEN:FIRSTNAME}},</p>

  <p style="color:#000000;">Este questionário integra a fase de comentários do gestor da {fiscalizacao_label}, realizada pela Coordenadoria de Auditoria em Políticas de Tecnologia da Informação (CAD-TI).</p>

  <p style="color:#000000;">O instrumento permite que a organização se manifeste sobre os apontamentos apresentados no Relatório Individual Preliminar, inclusive quanto às situações encontradas, às propostas de encaminhamento, às consequências práticas de sua implementação e, quando aplicável, aos itens avaliados como não conformes na etapa de avaliação das evidências.</p>

  <p style="color:#000000;">Para cada situação disponibilizada, a organização deverá informar se concorda ou discorda do apontamento. Em caso de concordância, poderá registrar comentários, providências adotadas ou planejadas e considerações sobre os encaminhamentos propostos. Em caso de discordância, deverá apresentar justificativa objetiva e, quando necessário, encaminhar documentação comprobatória.</p>

  <p style="color:#000000;">Quando houver seção de reavaliação de evidências, a organização poderá apresentar esclarecimentos, retificações ou evidência suplementar em formato PDF ou ZIP, limitada aos itens indicados para reanálise.</p>

  <p style="color:#000000;">Para organizações em que não tenha sido identificada resposta válida ao questionário {fiscalizacao_nome}, será disponibilizada seção própria para apresentação de esclarecimentos, comprovação de eventual envio anterior ou justificativa para a ausência de resposta.</p>

  <p style="color:#000000;margin-top:5px;"><strong>Observações importantes:</strong></p>

  <ol>
    <li style="margin-bottom:10px;">A etapa de comentários do gestor é facultativa, mas constitui oportunidade para esclarecimento de fatos, correção de informações, apresentação de documentos e manifestação sobre os apontamentos preliminares.</li>
    <li style="margin-bottom:10px;">As manifestações devem ser objetivas e acompanhadas de documentação comprobatória sempre que a organização pretender afastar ou modificar situação apontada pela Equipe de Auditoria.</li>
    <li style="margin-bottom:10px;">Os arquivos anexados devem estar em formato PDF ou ZIP. Caso haja mais de um documento, recomenda-se compactá-los em um único arquivo ZIP.</li>
    <li style="margin-bottom:10px;">As informações prestadas serão analisadas pela Equipe de Auditoria antes da consolidação dos resultados e poderão subsidiar ajustes, ratificações ou complementações no relatório final.</li>
  </ol>
</div>'''

        endtext = f'''<p style="color:#000000;">Prezado(a),</p>

<p style="color:#000000;">Agradecemos pela participação na fase de comentários do gestor da {fiscalizacao_label}.</p>

<p style="color:#000000;">As manifestações, justificativas e evidências encaminhadas serão analisadas pela Equipe de Auditoria para fins de apreciação dos esclarecimentos apresentados, reavaliação dos pontos cabíveis e consolidação dos resultados da fiscalização.</p>

<p style="color:#000000;">O envio deste questionário não implica acolhimento automático das manifestações apresentadas. A análise será realizada à luz dos critérios de auditoria, das informações anteriormente prestadas, das evidências disponíveis e da documentação eventualmente encaminhada nesta etapa.</p>

<p style="color:#000000;">Após a análise dos comentários do gestor, os resultados poderão subsidiar ajustes nos apontamentos preliminares, manutenção das conclusões, complementação de evidências e elaboração dos produtos finais da fiscalização.</p>

<p style="color:#000000;">Em caso de dúvidas, entre em contato com a Coordenadoria de Auditoria em Políticas de Tecnologia da Informação (CAD-TI) pelo e-mail {admin_email}.</p>'''

        xml = ' <surveys_languagesettings>\n  <fields>\n'
        xml += '   <fieldname>surveyls_survey_id</fieldname>\n   <fieldname>surveyls_language</fieldname>\n'
        xml += '   <fieldname>surveyls_title</fieldname>\n   <fieldname>surveyls_description</fieldname>\n'
        xml += '   <fieldname>surveyls_welcometext</fieldname>\n   <fieldname>surveyls_endtext</fieldname>\n'
        xml += '   <fieldname>surveyls_url</fieldname>\n   <fieldname>surveyls_urldescription</fieldname>\n'
        xml += '   <fieldname>surveyls_email_invite_subj</fieldname>\n   <fieldname>surveyls_email_invite</fieldname>\n'
        xml += '   <fieldname>surveyls_email_remind_subj</fieldname>\n   <fieldname>surveyls_email_remind</fieldname>\n'
        xml += '   <fieldname>surveyls_email_register_subj</fieldname>\n   <fieldname>surveyls_email_register</fieldname>\n'
        xml += '   <fieldname>surveyls_email_confirm_subj</fieldname>\n   <fieldname>surveyls_email_confirm</fieldname>\n'
        xml += '   <fieldname>surveyls_dateformat</fieldname>\n   <fieldname>surveyls_numberformat</fieldname>\n'
        xml += '   <fieldname>email_admin_notification_subj</fieldname>\n   <fieldname>email_admin_notification</fieldname>\n'
        xml += '   <fieldname>email_admin_responses_subj</fieldname>\n   <fieldname>email_admin_responses</fieldname>\n'
        xml += '  </fields>\n  <rows>\n   <row>\n'
        xml += '    <surveyls_survey_id><![CDATA[0]]></surveyls_survey_id>\n'
        xml += '    <surveyls_language><![CDATA[pt-BR]]></surveyls_language>\n'
        xml += f'    <surveyls_title><![CDATA[Comentários do Gestor - {fiscalizacao_label}]]></surveyls_title>\n'
        xml += f'    <surveyls_description><![CDATA[{fiscalizacao_label}]]></surveyls_description>\n'
        xml += f'    <surveyls_welcometext><![CDATA[{welcome}]]></surveyls_welcometext>\n'
        xml += f'    <surveyls_endtext><![CDATA[{endtext}]]></surveyls_endtext>\n'
        xml += '    <surveyls_url/>\n    <surveyls_urldescription/>\n'
        xml += f'    <surveyls_email_invite_subj><![CDATA[Questionário - {fiscalizacao_label}]]></surveyls_email_invite_subj>\n'
        xml += '    <surveyls_email_invite/>\n    <surveyls_email_remind_subj/>\n'
        xml += '    <surveyls_email_remind/>\n    <surveyls_email_register_subj/>\n'
        xml += '    <surveyls_email_register/>\n    <surveyls_email_confirm_subj/>\n'
        xml += '    <surveyls_email_confirm/>\n'
        xml += '    <surveyls_dateformat><![CDATA[5]]></surveyls_dateformat>\n'
        xml += '    <surveyls_numberformat><![CDATA[0]]></surveyls_numberformat>\n'
        xml += '    <email_admin_notification_subj/>\n    <email_admin_notification/>\n'
        xml += '    <email_admin_responses_subj/>\n    <email_admin_responses/>\n'
        xml += '   </row>\n  </rows>\n </surveys_languagesettings>\n'
        return xml
