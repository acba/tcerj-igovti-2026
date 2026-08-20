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
RESULTADO_REVISADO = Path("/tmp/tcerj-igovti-2026/validacao-q5/resultado_auditoria.json")


FORMULAS = {
    "PA01": "(AV01 | (AV02 & (AV03 | (AV04 | AV84))) | (AV05 & AV06))",
    "PA02": "(AV08 | AV11 | (AV12 & AV13))",
    "PA03": "((AV14 | AV15 | AV17 | AV154) | (AV155 & (AV18 | AV19 | AV20 | AV24)))",
    "PA04": "((AV26 & AV25) | AV29 | (AV31 | AV33) | (AV45 & AV46))",
    "PA05": "((AV55 | AV56) | (AV54 | AV57 | AV58) | (AV62 | AV63) | (AV59 | AV66) | (AV67 | AV70 | AV71))",
    "PA06": "(((AV73 | AV143) | (AV152 | AV153)) | (AV78 | AV148) | (AV82 | (AV80 | AV150)) | AV83)",
}


Q6 = "A organização adota processo formal e padronizado para a fase preparatória das contratações de TIC, com responsabilidades definidas, análise técnica pela área de TIC e alinhamento aos instrumentos de planejamento?"
Q2 = "A organização possui mecanismos básicos de governança de TIC, incluindo objetivos, indicadores e metas, bem como Comitê de TIC ou instância equivalente formalmente instituída e atuante?"
A2 = "Governança de TIC insuficiente para avaliar, dirigir e monitorar a tecnologia da informação."
Q3 = "A organização utiliza o planejamento de TIC como instrumento efetivo de gestão, com processo formal, plano vigente, aprovação competente, alinhamento institucional, integração com orçamento e contratações e acompanhamento periódico?"
A3 = "Planejamento de TIC insuficiente para orientar a gestão, o orçamento e as contratações de TIC"
Q4 = "A organização dispõe de mecanismos mínimos para estruturar e dimensionar sua força de trabalho de TIC e segurança da informação, formalizar funções e preservar capacidade interna nos modelos de operação predominantemente terceirizados?"
A4 = "Capacidade institucional de pessoal de TIC e segurança da informação insuficientemente estruturada ou dimensionada"
Q5 = "A organização adota práticas mínimas de gestão de serviços de TIC, incluindo catálogo de serviços, níveis de serviço, inventário de ativos, gestão de configuração e tratamento de incidentes, de modo a assegurar eficiência, rastreabilidade e qualidade dos serviços prestados?"
A5 = "Gestão de serviços de TIC insuficiente para assegurar controle sobre serviços, ativos e incidentes"
Q2_BLOCK = """## Questão 02 - Governança e Comitê de TIC

questao: Q2. A organização possui mecanismos básicos de governança de TIC, incluindo objetivos, indicadores e metas, bem como Comitê de TIC ou instância equivalente formalmente instituída e atuante?

subquestoes:
- A alta administração estabeleceu objetivos, indicadores e metas para a gestão de TIC?
- O Comitê de TIC ou instância equivalente está formalmente instituído e conta com representantes de áreas relevantes da organização?
- O Comitê de TIC ou instância equivalente realiza as atividades previstas em seu ato constitutivo?

riscos:
- R2.1: Devido à ausência de objetivos, indicadores ou metas para a gestão de TIC, poderá haver dificuldade para direcionar prioridades, medir resultados e acompanhar a contribuição da TIC para os objetivos institucionais.
- R2.2: Devido à inexistência de Comitê de TIC ou instância equivalente, ou à ausência de representação de áreas relevantes em sua composição, poderá não haver instância colegiada adequada para alinhar prioridades e decisões relevantes de TIC às necessidades e aos objetivos institucionais.
- R2.3: Devido à ausência de atuação efetiva do Comitê de TIC ou instância equivalente, o colegiado poderá existir apenas formalmente, sem contribuir efetivamente para o direcionamento, a priorização e o acompanhamento da TIC.

fontes_de_informacao:
- F1: Respostas ao questionário eletrônico iGovTI.
- F2: Evidências anexadas ao questionário eletrônico.

informacoes_requeridas:
- IR1: Resposta sobre objetivos, indicadores e metas para a gestão de TIC estabelecidos pela alta administração; [F1, q1001ext[H]]
- IR2: Evidência anexada que demonstre a formalização dos objetivos, indicadores e metas para a gestão de TIC; [F2, q1001evi]
- IR3: Resposta sobre existência de Comitê de TIC ou instância equivalente composto por representantes de áreas relevantes da organização; [F1, q1001ext[E]]
- IR4: Evidência anexada que demonstre a instituição formal e a composição do Comitê de TIC ou instância equivalente; [F2, q1001evi]
- IR5: Resposta sobre a realização das atividades previstas no ato constitutivo do Comitê de TIC ou instância equivalente; [F1, q1001ext[F]]
- IR6: Evidência anexada que demonstre atuação efetiva do Comitê de TIC ou instância equivalente, como atas, pautas, listas de presença, registros de deliberação, decisões, encaminhamentos ou acompanhamento de pendências; [F2, q1001evi]

criterios:
- C1: COBIT 2019, EDM01.02 - Dirigir o sistema de governança: orientar estruturas, princípios, processos e práticas de governança para assegurar que a TI apoie os objetivos organizacionais.
- C2: COBIT 2019, MEA01.04 - Avaliar o desempenho: monitorar e avaliar periodicamente o desempenho e a conformidade da TI em relação a objetivos, indicadores, metas e expectativas das partes interessadas.
- C3: Decreto nº 12.198/2024, arts. 5º e 6º, § 2º – Referência de governança digital: instituição, no âmbito da Administração Pública federal direta, autárquica e fundacional, de Comitê de Governança Digital ou colegiado equivalente com função deliberativa sobre ações de governo digital e uso de recursos de TIC, incluindo a aprovação dos instrumentos de planejamento previstos no Decreto.
- C4: Acórdão TCE-RJ nº 44.490/2024-PLEN, itens II.1, III.1 e V.1 – Precedente pela instituição e atuação efetiva de instância colegiada de governança de TIC, com responsabilidade pelo alinhamento das ações de TIC aos objetivos institucionais, priorização dos investimentos e monitoramento do desempenho da TIC.

procedimentos:
- P1: Verificar, por meio da resposta à q1001ext[H], se a alta administração estabeleceu objetivos, indicadores e metas para a gestão de TIC; [IR1]
- P2: Validar, pela evidência anexada à q1001, a formalização dos objetivos, indicadores e metas para a gestão de TIC; [IR2]
- P3: Verificar, por meio da resposta à q1001ext[E], se a organização declarou dispor de Comitê de TIC ou instância equivalente composto por representantes de áreas relevantes; [IR3]
- P4: Validar, pela evidência anexada à q1001, a instituição formal e a composição do Comitê de TIC ou instância equivalente; [IR4]
- P5: Verificar, por meio da resposta à q1001ext[F], se o Comitê de TIC ou instância equivalente realiza as atividades previstas em seu ato constitutivo; [IR5]
- P6: Validar, pela evidência anexada à q1001, se há atas, pautas, registros de deliberação, encaminhamentos ou acompanhamento de decisões do Comitê de TIC ou instância equivalente; [IR6]

evidencias:
- E1: Resposta negativa sobre o estabelecimento de objetivos, indicadores ou metas para a gestão de TIC; [P1]
- E2: Ausência, desatualização, incompatibilidade ou insuficiência de evidência que demonstre objetivos, indicadores e metas para a gestão de TIC; [P2]
- E3: Resposta que indique inexistência de Comitê de TIC ou instância equivalente com representação de áreas relevantes da organização; [P3]
- E4: Ausência ou insuficiência de evidência que demonstre a instituição formal e a composição do Comitê de TIC ou instância equivalente; [P4]
- E5: Resposta que indique que o Comitê de TIC ou instância equivalente não realiza as atividades previstas em seu ato constitutivo; [P5]
- E6: Ausência, desatualização, incompatibilidade ou insuficiência de atas, registros de deliberação, encaminhamentos ou acompanhamento de decisões do Comitê de TIC ou instância equivalente; [P6]

possiveis_achados:
- A2: Governança de TIC insuficiente para avaliar, dirigir e monitorar a tecnologia da informação.
  situacoes_encontradas:
    - S2.1:
      descricao: Ausência de objetivos, indicadores ou metas para a gestão de TIC.
      severidade: alta
      itens_questionario: [q1001ext[H], q1001evi]
      regra_de_identificacao:
      - (q1001ext[H] != Sim)
      referencias_matriz: [R2.1, P1, E1, P2, E2]
      criterios: [C2]
      tipo_encaminhamento: Recomendação
      encaminhamento: estabeleça objetivos, indicadores e metas para a gestão de TIC, de modo a possibilitar o acompanhamento periódico do desempenho da TIC pela alta administração
    - S2.2:
      descricao: Comitê de TIC ou instância equivalente não instituído formalmente ou sem representação de áreas relevantes da organização.
      severidade: alta
      itens_questionario: [q1001ext[E], q1001evi]
      regra_de_identificacao:
      - (q1001ext[E] != Sim)
      referencias_matriz: [R2.2, P3, E3, P4, E4]
      criterios: [C1, C3, C4]
      tipo_encaminhamento: Determinação
      encaminhamento: institua formalmente Comitê de TIC ou instância colegiada equivalente, compatível com o porte e a estrutura decisória da organização, definindo em seu ato constitutivo, minimamente, a participação de representantes de áreas relevantes da organização, suas competências, a periodicidade de reuniões, a forma de registro das deliberações e os mecanismos de acompanhamento dos encaminhamentos
    - S2.3:
      descricao: Comitê de TIC ou instância equivalente sem atuação efetiva comprovada.
      severidade: media
      itens_questionario: [q1001ext[E], q1001ext[F], q1001evi]
      regra_de_identificacao:
      - (q1001ext[E] == Sim) & (q1001ext[F] != Sim)
      referencias_matriz: [R2.3, P5, E5, P6, E6]
      criterios: [C1, C3, C4]
      tipo_encaminhamento: Determinação
      encaminhamento: assegure o funcionamento efetivo do Comitê de TIC ou instância colegiada equivalente, mediante o exercício das competências previstas em seu ato constitutivo, com registro das deliberações e acompanhamento dos respectivos encaminhamentos"""
Q3_BLOCK = """## Questão 03 - Planejamento de TIC

questao: Q3. A organização utiliza o planejamento de TIC como instrumento efetivo de gestão, com processo formal, plano vigente, aprovação competente, alinhamento institucional, integração com orçamento e contratações e acompanhamento periódico?

subquestoes:
- A organização executa processo formal de planejamento de TIC, com critérios definidos para seleção e priorização das iniciativas?
- As áreas demandantes participam do processo de planejamento de TIC?
- O plano de TIC foi formalmente aprovado pela instância competente?
- O plano de TIC está alinhado ao planejamento institucional?
- O plano de TIC está integrado à proposta orçamentária da área de TIC e ao plano de contratações?
- O plano de TIC é acompanhado, revisto e atualizado periodicamente ou diante de mudanças relevantes?

riscos:
- R3.1: Devido à inexistência ou insuficiência do processo de planejamento de TIC, poderá não haver plano vigente e critérios adequados para seleção e priorização das iniciativas, favorecendo atuação reativa e desalinhada às necessidades institucionais.
- R3.2: Devido à ausência de aprovação formal do plano de TIC pela instância competente, o instrumento poderá não possuir legitimidade institucional para orientar a gestão, os projetos, o orçamento e as contratações de TIC.
- R3.4: Devido ao alinhamento insuficiente do plano de TIC ao planejamento institucional poderão ser executadas ações de TIC com baixo valor ou desconectadas das prioridades da organização.
- R3.5: Devido à ausência de integração entre planejamento de TIC, orçamento e contratações, poderão ocorrer aquisições reativas, não priorizadas ou desalinhadas.
- R3.6: Devido à ausência de acompanhamento da execução do plano de TIC, poderão deixar de ser identificados tempestivamente desvios, pendências ou mudanças que demandem ajustes nas iniciativas e prioridades planejadas.

fontes_de_informacao:
- F1: Respostas ao questionário eletrônico iGovTI.
- F2: Evidências anexadas no questionário eletrônico.

informacoes_requeridas:
- IR1: Respostas sobre execução do processo de planejamento de TIC, sua formalização e existência de critérios para seleção e priorização das iniciativas, bem como sobre a existência de plano de TIC vigente; [F1, q2101, q2101ext[B], q2101ext[D], q2102]
- IR2: Evidências que demonstrem a formalização do processo de planejamento de TIC e a existência de plano de TIC vigente; [F2, q2101evi, q2102evi]
- IR3: Resposta sobre participação das áreas demandantes no processo de planejamento de TIC; [F1, q2101ext[A]]
- IR4: Resposta sobre aprovação formal do plano de TIC pela instância competente; [F1, q2102ext[A]]
- IR5: Evidência anexada do ato de aprovação formal do plano de TIC; [F2, q2102evi]
- IR7: Resposta e evidência sobre alinhamento das iniciativas do plano de TIC ao planejamento institucional; [F1, F2, q2102ext[D], q2102evi]
- IR8: Resposta e evidência sobre a utilização do plano de TIC como referência para a elaboração da proposta orçamentária da área de TIC e do plano de contratações; [F1, F2, q2102ext[C], q2102evi]
- IR9: Resposta e evidência sobre acompanhamento da execução do plano de TIC; [F1, F2, q2102ext[E], q2102evi]

criterios:
- C1: COBIT 2019, APO02.05 - Definir o plano e o roteiro estratégico: estabelecer plano e roteiro de TIC que traduzam a estratégia em iniciativas, prioridades, recursos, dependências, prazos e benefícios esperados.
- C2: COBIT 2019, APO06.03 - Criar e manter orçamentos: elaborar e manter orçamento de TIC alinhado ao portfólio, ao planejamento e às prioridades aprovadas.
- C3: Acórdão 1.411/2014-TCU-Plenário, item 9.1.6 e subitens 9.1.6.1 a 9.1.6.4: necessidade de instituir formalmente plano diretor de TI, contemplando desdobramento de diretrizes estratégicas, vinculação das ações de TI a indicadores e metas de negócio, vinculação das ações de TI a indicadores e metas de serviços ao cidadão e vinculação das ações priorizadas ao orçamento de TI.
- C4: Acórdão TCE-RJ nº 44.490/2024-PLEN, itens II.3 e III.3 e respectivos subitens – Precedentes quanto ao estabelecimento formal de processo estruturado de planejamento de TIC, com participação das áreas relevantes, elaboração, manutenção e revisão periódica de PDTI, contemplando objetivos, indicadores e metas alinhados aos objetivos institucionais, riscos, projetos, aquisições, recursos necessários e ações de monitoramento após aprovação pela alta administração.

procedimentos:
- P1: Verificar, por meio das respostas à q2101, q2101ext[B] e q2101ext[D], se a organização executa processo de planejamento de TIC formalizado e com critérios definidos para seleção e priorização das iniciativas; [IR1]
- P2: Validar, pelas evidências anexadas à q2101 e q2102, a formalização mínima do processo de planejamento de TIC e sua materialização em plano de TIC vigente; [IR2]
- P3: Verificar, por meio da q2101ext[A], se há participação das áreas demandantes no processo de planejamento de TIC; [IR3]
- P4: Verificar, por meio da resposta à q2102ext[A], se o plano de TIC foi aprovado pelo dirigente máximo da organização ou por dirigente ou colegiado integrante da alta administração; [IR4]
- P5: Validar, pelas evidências anexadas à q2102, a aprovação formal do plano de TIC pela instância competente; [IR5]
- P7: Verificar, por meio da resposta e das evidências da q2102, se o plano está alinhado ao planejamento institucional; [IR7]
- P8: Verificar, por meio da resposta à q2102ext[C] e da evidência correspondente, se o plano de TIC fundamenta a proposta orçamentária da área de TIC e o plano de contratações; [IR8]
- P9: Verificar, por meio da resposta à q2102ext[E] e das evidências correspondentes, se é realizado acompanhamento concomitante à execução do plano de TIC; [IR9]

evidencias:
- E1: Resposta negativa ou insuficiente sobre a existência de processo de planejamento de TIC; [P1]
- E2: Ausência, desatualização, incompatibilidade ou insuficiência de evidência que discipline o processo de planejamento de TIC; [P2]
- E3: Resposta negativa ou insuficiente sobre participação das áreas demandantes; [P3]
- E4: Resposta negativa ou insuficiente sobre a aprovação formal do plano de TIC pela instância competente; [P4]
- E5: Ausência ou insuficiência de evidência do ato de aprovação formal do plano de TIC pela instância competente; [P5]
- E7: Inexistência ou insuficiência de alinhamento entre plano de TIC e planejamento institucional; [P7]
- E8: Ausência ou insuficiência de evidência de utilização do plano de TIC como referência para a proposta orçamentária da área de TIC e o plano de contratações; [P8]
- E9: Ausência ou insuficiência de evidência de acompanhamento da execução do plano de TIC; [P9]

possiveis_achados:
- A3: Planejamento de TIC insuficiente para orientar a gestão, o orçamento e as contratações de TIC
  situacoes_encontradas:
  - S3.1:
      descricao: Inexistência ou insuficiência do processo de planejamento de TIC para produzir e manter plano de TIC adequado.
      severidade: alta
      itens_questionario: [q2101ext[A], q2101ext[B], q2101ext[D], q2101evi, q2102]
      regra_de_identificacao:
      - existe_plano_ti = (q2102 == Adota parcialmente) | (q2102 == Adota em maior parte ou totalmente)
      - (q2101ext[A] != Sim) | (q2101ext[B] != Sim) | (q2101ext[D] != Sim) | ~existe_plano_ti
      referencias_matriz: [R3.1, P1, E1, P2, E2, P3, E3]
      criterios: [C1, C3, C4]
      tipo_encaminhamento: Determinação
      encaminhamento: institua processo formal de planejamento de TIC, compatível com o porte e a complexidade da organização, que assegure a elaboração e manutenção de plano de TIC, atentando-se, minimamente, em definir etapas, responsabilidades, participação das áreas demandantes e critérios de priorização das necessidades e iniciativas de TIC
  - S3.2:
      descricao: Ausência de aprovação formal do plano de TIC.
      severidade: alta
      itens_questionario: [q2102, q2102ext[A], q2102evi]
      regra_de_identificacao:
      - existe_plano_ti & (q2102ext[A] != Sim)
      referencias_matriz: [R3.2, P4, E4, P5, E5]
      criterios: [C3, C4]
      tipo_encaminhamento: Determinação
      encaminhamento: submeta o plano de TIC à aprovação formal do dirigente máximo ou de instância competente da alta administração, mantendo registro do respectivo ato de aprovação
  - S3.4:
      descricao: Plano de TIC sem alinhamento adequado ao planejamento institucional.
      severidade: media
      itens_questionario: [q2102, q2102ext[D], q2102evi]
      regra_de_identificacao:
      - existe_plano_ti & (q2102ext[D] != Sim)
      referencias_matriz: [R3.4, P7, E7]
      criterios: [C1, C3, C4]
      tipo_encaminhamento: Determinação
      encaminhamento: revise o plano de TIC para explicitar seu alinhamento ao planejamento institucional, às diretrizes superiores e às necessidades das áreas finalísticas e administrativas, relacionando objetivos, iniciativas, indicadores e metas de TIC aos resultados institucionais pretendidos
  - S3.5:
      descricao: Plano de TIC não utilizado como referência para a elaboração da proposta orçamentária e do plano de contratações.
      severidade: alta
      itens_questionario: [q2102, q2102ext[C], q2102evi]
      regra_de_identificacao:
      - existe_plano_ti & (q2102ext[C] != Sim)
      referencias_matriz: [R3.5, P8, E8]
      criterios: [C2, C4]
      tipo_encaminhamento: Determinação
      encaminhamento: integre o plano de TIC à elaboração da proposta orçamentária e do plano de contratações, de maneira proporcional ao porte, à estrutura e à capacidade de planejamento da organização
  - S3.6:
      descricao: Ausência de acompanhamento da execução do plano de TIC.
      severidade: media
      itens_questionario: [q2102, q2102ext[E], q2102evi]
      regra_de_identificacao:
      - existe_plano_ti & (q2102ext[E] != Sim)
      referencias_matriz: [R3.6, P9, E9]
      criterios: [C4]
      tipo_encaminhamento: Determinação
      encaminhamento: estabeleça e execute rotina periódica de acompanhamento da execução do plano de TIC, promovendo sua revisão periódica e os ajustes ou atualizações necessários, com registro das principais decisões e reprogramações"""
Q4_BLOCK = """## Questão 04 - Capacidade Institucional de TIC e Segurança da Informação

questao: Q4. A organização dispõe de mecanismos mínimos para estruturar e dimensionar sua força de trabalho de TIC e segurança da informação, formalizar funções e preservar capacidade interna nos modelos de operação predominantemente terceirizados?

subquestoes:
- A organização dispõe de profissionais que atuam regularmente em TIC?
- A organização definiu o quantitativo necessário de pessoal de TIC e segurança da informação?
- A organização possui cargos ou funções formalmente atribuídos à TIC e à segurança da informação?
- Nos modelos de operação predominantemente terceirizados, a organização mantém força de trabalho interna de TIC?

riscos:
- R4.1: Devido à ausência de profissionais atuando regularmente em TIC, poderá não haver capacidade operacional mínima para coordenar e sustentar as atividades e serviços tecnológicos da organização.
- R4.2: Devido à ausência de definição do quantitativo necessário de pessoal de TIC e segurança da informação, poderá haver subdimensionamento ou alocação inadequada da equipe.
- R4.3: Devido à ausência de cargos ou funções formalmente atribuídos à TIC ou à segurança da informação, poderá haver baixa clareza de responsabilidades e insuficiente capacidade de alocação e responsabilização dos profissionais.
- R4.6: Devido à operação predominantemente terceirizada sem profissionais internos de TIC, poderá haver insuficiência de capacidade interna para coordenação, supervisão e fiscalização das atividades terceirizadas, além de maior risco de dependência externa, perda de conhecimento e descontinuidade.

fontes_de_informacao:
- F1: Respostas ao questionário eletrônico iGovTI.
- F2: Evidências anexadas no questionário eletrônico.

informacoes_requeridas:
- IR1: Resposta sobre quantitativo de profissionais que atuam em TIC e segurança da informação, por área e tipo de vínculo; [F1, q0105]
- IR2: Resposta e evidência sobre definição do quantitativo necessário de pessoal de TIC e segurança da informação; [F1, F2, q2703, q2703evi]
- IR3: Resposta sobre existência de cargos ou funções formalmente atribuídos à TIC e à segurança da informação; [F1, q2708]
- IR9: Resposta sobre o modelo de operação predominante de TIC e o quantitativo de profissionais internos de TIC, para avaliação da dependência de terceiros e da capacidade interna de coordenação e fiscalização; [F1, q0101, q0105]

criterios:
- C1: COBIT 2019, APO01.05 - Estabelecer papéis e responsabilidades: definir, comunicar e manter papéis e responsabilidades relacionados à governança e gestão de TIC.
- C2: COBIT 2019, APO07.01 - Adquirir e manter pessoal adequado e apropriado: assegurar quantidade e perfil de profissionais compatíveis com as necessidades de TIC.
- C5: COBIT 2019, APO07.05 - Planejar e monitorar o uso de recursos humanos de TI e de negócio: planejar, alocar e acompanhar capacidade de pessoal para iniciativas, operações e serviços de TIC.
- C6: COBIT 2019, APO07.06 - Gerenciar pessoal contratado: controlar o uso de pessoal terceirizado ou externo, preservando responsabilização, supervisão e retenção de conhecimento.
- C12: Acórdão 1.411/2014-TCU-Plenário, item 9.1.6.5 - O PDTI deve contemplar o quantitativo necessário ou ideal para a força de trabalho em TI.
- C13: Acórdão 1.411/2014-TCU-Plenário, item 9.1.7 - A organização deve adotar providências para dotar o setor de TI de quantitativo adequado às necessidades de trabalho em TI, consideradas as necessidades das demais áreas.
- C14: Acórdão TCE-RJ nº 44.490/2024-PLEN, itens I.10.11, III.9.11 e IV.11.3 – Referência para avaliação da estrutura de recursos humanos de TIC quanto à suficiência quantitativa e qualitativa e à preservação de capacidade interna em atividades de planejamento, coordenação, fiscalização e controle.

procedimentos:
- P1: Verificar, por meio da q0105, o quantitativo informado de profissionais que atuam em TIC e segurança da informação, por área e tipo de vínculo; [IR1]
- P2: Verificar, por meio da q2703 e respectiva evidência, se há definição do quantitativo necessário de pessoal de TIC e segurança da informação; [IR2]
- P3: Verificar, por meio da q2708, se há cargos ou funções formalmente atribuídos à TIC e à segurança da informação; [IR3]
- P7: Verificar, por meio da resposta à q0101 e do quantitativo informado na q0105, se o modelo de operação de TIC é predominantemente terceirizado e não há profissionais internos de TIC; [IR9]

evidencias:
- E1: Quantitativo total declarado igual a zero para profissionais de TIC, desde que a organização tenha informado possuir estrutura formal de TIC; [P1]
- E2: Resposta negativa ou insuficiente sobre definição do quantitativo necessário de pessoal de TIC e segurança da informação, ou evidência inexistente/incompatível/insuficiente; [P2]
- E3: Resposta negativa sobre existência de cargos ou funções formalmente atribuídos à TIC ou à segurança da informação; [P3]
- E7: Modelo de operação de TIC predominantemente terceirizado (q0101 = B) sem profissionais internos de TIC (total de efetivos, comissionados, cedidos e temporários igual a zero); [P7]

possiveis_achados:
- A4: Capacidade institucional de pessoal de TIC e segurança da informação insuficientemente estruturada ou dimensionada
  situacoes_encontradas:
  - S4.1:
      descricao: Ausência de força de trabalho dedicada à TIC.
      severidade: alta
      itens_questionario: [q0101, q0105[TI_efetivos], q0105[TI_comissionados], q0105[TI_terceirizados], q0105[TI_cedidos], q0105[TI_temporarios], q0105[TI_estagiarios]]
      regra_de_identificacao:
      - total_TI = q0105[TI_efetivos] + q0105[TI_comissionados] + q0105[TI_terceirizados] + q0105[TI_cedidos] + q0105[TI_temporarios] + q0105[TI_estagiarios]
      - (q0101 in [A, B, D, E]) & (total_TI == 0)
      referencias_matriz: [R4.1, P1, E1]
      criterios: [C2, C13]
      tipo_encaminhamento: Recomendação
      encaminhamento: avalie a força de trabalho dedicada à TIC e adote medidas proporcionais para assegurar capacidade mínima de planejamento, gestão, proteção, contratação, fiscalização e sustentação dos serviços e ativos de TIC
  - S4.2:
      descricao: Ausência ou insuficiência de definição documentada do quantitativo necessário de pessoal de TIC e segurança da informação.
      severidade: média
      itens_questionario: [q2703ext[C], q2703evi]
      regra_de_identificacao:
      - (q2703ext[C] != Sim)
      referencias_matriz: [R4.2, P2, E2]
      criterios: [C5, C12]
      tipo_encaminhamento: Recomendação
      encaminhamento: estime e mantenha atualizado o quantitativo necessário de pessoal de TIC e segurança da informação, considerando o porte e a complexidade da organização, os serviços críticos, os sistemas mantidos, as contratações vigentes e os riscos relevantes
  - S4.3:
      descricao: Ausência de cargos ou funções formalmente atribuídos à TIC ou à segurança da informação.
      severidade: media
      itens_questionario: [q2708[B], q2708[D]]
      regra_de_identificacao:
      - (q2708[B] != Sim) | (q2708[D] != Sim)
      referencias_matriz: [R4.3, P3, E3]
      criterios: [C1, C2]
      tipo_encaminhamento: Recomendação
      encaminhamento: avalie a necessidade de formalizar a atribuição de cargos ou funções à TIC e à segurança da informação e adote solução compatível com as necessidades institucionais e a capacidade administrativa da organização
  - S4.6:
    descricao: Operação de TIC predominantemente terceirizada sem profissionais internos de TIC.
    severidade: alta
    itens_questionario: [q0101, q0105[TI_efetivos], q0105[TI_comissionados], q0105[TI_cedidos], q0105[TI_temporarios]]
    regra_de_identificacao:
      - total_TI_interno = q0105[TI_efetivos] + q0105[TI_comissionados] + q0105[TI_cedidos] + q0105[TI_temporarios]
      - (q0101 == B) & (total_TI_interno == 0)
    referencias_matriz: [R4.6, P7, E7]
    criterios: [C6, C14]
    tipo_encaminhamento: Recomendação
    encaminhamento: avalie o modelo de operação de TIC e adote medidas proporcionais para assegurar capacidade interna suficiente para coordenar, supervisionar e fiscalizar as atividades e os contratos de TIC executados predominantemente por terceiros, preservando responsabilização e retenção de conhecimento"""
Q5_BLOCK = """## Questão 05 - Gestão de Serviços de TIC

questao: Q5. A organização adota práticas mínimas de gestão de serviços de TIC, incluindo catálogo de serviços, níveis de serviço, inventário de ativos, gestão de configuração e tratamento de incidentes, de modo a assegurar eficiência, rastreabilidade e qualidade dos serviços prestados?

subquestoes:
- A organização mantém catálogo de serviços de TIC atualizado e acessível aos usuários e às equipes de suporte?
- O catálogo de serviços de TIC contém informações mínimas sobre os serviços efetivamente prestados?
- Existem Acordos de Níveis de Serviço ou metas mínimas formalmente definidas e monitoradas para os principais serviços de TIC?
- A organização mantém inventário atualizado dos ativos de TIC?
- Há processo formal de gestão de configuração, com identificação de itens de configuração relevantes para os serviços de TIC?
- A organização possui processo formal de gestão de incidentes de TIC?

riscos:
- R5.1: Devido à inexistência ou desatualização do catálogo de serviços de TIC, poderá não haver definição clara e padronizada dos serviços prestados, levando à prestação reativa e pouco transparente de serviços de TIC.
- R5.2: Devido à inexistência de níveis de serviço formalmente definidos ou monitorados, poderá não haver parâmetros objetivos de desempenho e qualidade dos serviços de TIC.
- R5.3: Devido à inexistência ou fragilidade do inventário de ativos e da gestão de configuração, poderá não haver controle adequado dos recursos tecnológicos e suas relações com os serviços prestados.
- R5.4: Devido à inexistência ou fragilidade do processo de gestão de incidentes de TIC, poderá não haver tratamento padronizado, tempestivo e rastreável dos incidentes.

fontes_de_informacao:
- F1: Respostas ao questionário eletrônico iGovTI.
- F2: Evidências anexadas no questionário eletrônico.

informacoes_requeridas:
- IR1: Resposta sobre adoção, atualização e disponibilidade do catálogo de serviços de TIC; [F1, q2201, q2201ext[B], q2201ext[C]]
- IR2: Evidência anexada contendo catálogo de serviços de TIC; [F2, q2201evi]
- IR3: Resposta sobre adoção da prática, metas no catálogo e existência de ANS ou metas mínimas de nível de serviço; [F1, q2201, q2201ext[A], q2201ext[D]]
- IR4: Resposta sobre monitoramento de ANS ou metas mínimas; [F1, q2201ext[E]]
- IR5: Evidência anexada contendo ANS, metas ou registros de monitoramento; [F2, q2201evi]
- IR6: Resposta sobre inventário e controle de dispositivos e softwares de TIC; [F1, q2504, q2504ext[A], q2504ext[B]]
- IR7: Evidência anexada contendo inventário de ativos de TIC; [F2, q2504evi]
- IR8: Respostas sobre existência de base consolidada de configurações e formalização do processo de gestão de configuração; [F1, q2203, q2203ext[A], q2203ext[C]]
- IR9: Evidência anexada contendo norma, procedimento, CMDB ou base equivalente de gestão de configuração; [F2, q2203evi]
- IR10: Respostas sobre adoção e formalização do processo de gestão de incidentes, critérios de priorização e escalamento e tratamento de incidentes de segurança da informação; [F1, q2204, q2204ext[A], q2204ext[D], q2204ext[E]]
- IR11: Evidência anexada contendo norma, procedimento ou fluxo de gestão de incidentes de TIC; [F2, q2204evi]
- IR13: Evidência anexada contendo registros de incidentes, chamados, tickets, relatórios de atendimento ou sistema equivalente; [F2, q2204evi]

criterios:
- C2: COBIT 2019, APO09.02 - Catalogar serviços facilitados por TI: definir, manter e comunicar catálogo de serviços, incluindo serviços prestados, características, requisitos e níveis de serviço esperados.
- C3: ITIL 4, prática de gerenciamento de nível de serviço: definir, acordar, monitorar, avaliar e reportar metas e níveis de serviço alinhados às necessidades das áreas usuárias.
- C4: ITIL 4, prática de gerenciamento de ativos de TI: planejar e gerenciar o ciclo de vida dos ativos de TI, mantendo informações suficientes para apoiar controle, custo, risco, valor e tomada de decisão.
- C6: COBIT 2019, BAI10.01 - Estabelecer e manter um modelo de configuração: definir escopo, granularidade, atributos, relacionamentos e responsáveis pela base de configuração.
- C8: COBIT 2019, DSS02.02, DSS02.04 e DSS02.07 - Requisições de serviço e incidentes gerenciados: registrar, classificar, priorizar, investigar, diagnosticar, resolver, acompanhar e reportar incidentes e requisições de serviço.
- C11: Acórdão TCE-RJ nº 44.490/2024-PLEN, itens II.7.4, III.9.4 e V.6.1 – Recomendações quanto à estruturação do catálogo de serviços de TIC, incluindo descrição dos serviços, metas, formas de acesso e disponibilidade aos usuários.
- C12: Acórdão TCE-RJ nº 44.490/2024-PLEN, itens II.7.5, III.9.5 e V.6.2 – Recomendações quanto à gestão de configuração e ativos de TIC, incluindo formalização do processo e manutenção de base consolidada de ativos e itens de configuração.
- C13: Acórdão TCE-RJ nº 44.490/2024-PLEN, itens II.7.6, III.9.6 e V.6.3 – Recomendações quanto à formalização e execução do processo de gestão de incidentes, incluindo registros, classificação, escalamento e tratamento.
- C14: Acórdão TCE-RJ nº 44.490/2024-PLEN, itens II.7.7, III.9.7 e V.6.4 – Recomendações quanto à definição, pactuação e monitoramento de níveis de serviço.
- C15: ABNT NBR ISO/IEC 20000-2:2021, item 8.2.4 – Gerenciamento de catálogo de serviço: orienta que o catálogo descreva os serviços e seus resultados pretendidos, contenha informações relevantes para sua utilização e seja disponibilizado às partes interessadas que necessitem acessá-lo.
- C16: ABNT NBR ISO/IEC 20000-2:2021, item 8.2.6 – Gerenciamento de configuração: orienta a identificação, o registro, o controle, o rastreamento e a verificação dos itens de configuração, bem como a manutenção de informações de configuração precisas relacionadas aos serviços.
- C17: ABNT NBR ISO/IEC 20000-2:2021, item 8.6.1 – Gerenciamento de incidente: orienta que os incidentes sejam registrados, classificados e priorizados, que as ações adotadas para sua resolução sejam registradas e rastreáveis e que sejam definidas responsabilidades para seu tratamento, incluindo procedimento documentado para incidentes graves.

procedimentos:
- P1: Verificar, por meio da q2201 e das q2201ext[B] e [C], a adoção da prática e a atualização e disponibilidade do catálogo de serviços de TIC; [IR1]
- P2: Validar, pela evidência anexada à q2201, se o catálogo contém informações mínimas sobre os serviços prestados; [IR2]
- P3: Verificar, por meio da q2201 e das q2201ext[A], [D] e [E], a adoção, definição, pactuação e monitoramento de metas ou níveis de serviço; [IR3, IR4]
- P4: Validar, pela evidência anexada à q2201, a existência de ANS, metas ou registros de monitoramento; [IR5]
- P5: Verificar, por meio da q2504 e das q2504ext[A] e [B], se a organização inventaria e controla dispositivos e softwares; [IR6]
- P6: Validar, pela evidência anexada à q2504, a existência e atualização do inventário de dispositivos e softwares; [IR7]
- P7: Verificar, por meio da q2203 e das q2203ext[A] e [C], se a organização mantém base consolidada de configurações e processo formalizado de gestão de configuração; [IR8]
- P8: Validar, pela evidência anexada à q2203, a existência de procedimento, base ou mecanismo equivalente de gestão de configuração; [IR9]
- P9: Verificar, por meio da q2204 e das q2204ext[A], [D] e [E], se a organização possui processo de gestão de incidentes formalizado, com critérios de priorização e escalamento e procedimentos para incidentes de segurança da informação; [IR10]
- P10: Validar, pela evidência anexada à q2204, a existência de procedimento ou fluxo formal de gestão de incidentes; [IR11]
- P12: Validar, pela evidência anexada à q2204, a existência de registros rastreáveis de incidentes, chamados ou tickets; [IR13]

evidencias:
- E1: Resposta negativa ou insuficiente sobre catálogo de serviços de TIC; [P1]
- E2: Ausência, desatualização, inacessibilidade ou insuficiência do catálogo de serviços de TIC; [P2]
- E3: Resposta negativa ou insuficiente sobre ANS ou metas mínimas de nível de serviço; [P3]
- E4: Ausência, desatualização ou insuficiência de ANS, metas ou registros de monitoramento; [P4]
- E5: Resposta negativa ou insuficiente sobre inventário de ativos de TIC; [P5]
- E6: Ausência, desatualização ou insuficiência de inventário de ativos de TIC; [P6]
- E7: Resposta negativa ou insuficiente quanto à manutenção de base consolidada de configurações ou à formalização do processo de gestão de configuração; [P7]
- E8: Ausência, desatualização ou insuficiência de norma, procedimento, CMDB ou base equivalente de gestão de configuração; [P8]
- E9: Resposta negativa ou insuficiente sobre processo formal de gestão de incidentes de TIC; [P9]
- E10: Ausência, desatualização ou insuficiência de norma, procedimento ou fluxo formal de gestão de incidentes; [P10]
- E12: Ausência, insuficiência ou baixa rastreabilidade dos registros de incidentes, chamados ou tickets; [P12]

possiveis_achados:
- A5: Gestão de serviços de TIC insuficiente para assegurar controle sobre serviços, ativos e incidentes
  situacoes_encontradas:
  - S5.1:
      descricao: Inexistência ou insuficiência do catálogo de serviços de TIC.
      severidade: media
      itens_questionario: [q2201, q2201ext[B], q2201ext[C], q2201evi]
      regra_de_identificacao:
      - (q2201ext[B] != Sim) | (q2201ext[C] != Sim)
      referencias_matriz: [R5.1, P1, E1, P2, E2]
      criterios: [C2, C11, C15]
      tipo_encaminhamento: Recomendação
      encaminhamento: institua e mantenha atualizado catálogo de serviços de TIC, atentando-se, minimamente, em identificar os serviços efetivamente prestados, seus responsáveis, usuários, condições de acesso e informações necessárias ao atendimento das áreas demandantes
  - S5.2:
      descricao: Ausência ou fragilidade na definição e no monitoramento de níveis mínimos de serviço de TIC.
      severidade: media
      itens_questionario: [q2201, q2201ext[A], q2201ext[D], q2201ext[E], q2201evi]
      regra_de_identificacao:
      - (q2201ext[A] != Sim) | (q2201ext[D] != Sim) | (q2201ext[E] != Sim)
      referencias_matriz: [R5.2, P3, E3, P4, E4]
      criterios: [C3, C14]
      tipo_encaminhamento: Recomendação
      encaminhamento: defina, acorde e monitore níveis de serviço para os serviços de TIC relevantes, estabelecendo metas e mecanismos de acompanhamento de seu cumprimento
  - S5.3:
      descricao: Inventário e controle de dispositivos e softwares de TIC inexistente ou insuficiente.
      severidade: alta
      itens_questionario: [q2504, q2504ext[A], q2504ext[B], q2504evi]
      regra_de_identificacao:
      - (q2504ext[A] != Sim) | (q2504ext[B] != Sim)
      referencias_matriz: [R5.3, P5, E5, P6, E6]
      criterios: [C4, C12]
      tipo_encaminhamento: Recomendação
      encaminhamento: estabeleça e mantenha inventário atualizado dos ativos tecnológicos sob gestão da organização, contemplando, minimamente, os dispositivos e softwares utilizados, com informações suficientes para sua identificação e controle
  - S5.4:
      descricao: Ausência ou fragilidade do processo de gestão de configuração.
      severidade: media
      itens_questionario: [q2203, q2203ext[A], q2203ext[C], q2203evi]
      regra_de_identificacao:
      - (q2203ext[A] != Sim) | (q2203ext[C] != Sim)
      referencias_matriz: [R5.3, P7, E7, P8, E8]
      criterios: [C6, C12, C16]
      tipo_encaminhamento: Recomendação
      encaminhamento: formalize e execute processo de gestão de configuração, atentando-se, minimamente, em manter base, ferramenta ou registro equivalente com os itens de configuração relevantes, seus responsáveis e os relacionamentos entre ativos
  - S5.5:
      descricao: Inexistência ou fragilidade do processo de gestão de incidentes de TIC.
      severidade: alta
      itens_questionario: [q2204, q2204ext[A], q2204ext[D], q2204ext[E], q2204evi]
      regra_de_identificacao:
      - (q2204ext[A] != Sim) | (q2204ext[D] != Sim) | (q2204ext[E] != Sim)
      referencias_matriz: [R5.4, P9, E9, P10, E10, P12, E12]
      criterios: [C8, C13, C17]
      tipo_encaminhamento: Recomendação
      encaminhamento: formalize e execute processo de gestão de incidentes de TIC, atentando-se, minimamente, em definir papéis, critérios de priorização e escalamento, tratamento de incidentes de serviços e de segurança da informação e registro sistemático e rastreável das ocorrências"""
CRITERIO_Q3_C5 = (
    "Lei nº 14.133/2021, art. 12, inciso VII e § 1º - Planejamento das contratações: "
    "o Plano de Contratações Anual, quando elaborado, deve alinhar-se ao planejamento "
    "estratégico, subsidiar a elaboração das leis orçamentárias e ser observado nas licitações "
    "e na execução contratual."
)
CRITERIO_Q3_C4 = (
    "Acórdão TCE-RJ nº 44.490/2024-PLEN, itens II.3 e III.3 e respectivos subitens – "
    "Precedentes quanto ao estabelecimento formal de processo estruturado de planejamento de TIC, "
    "com participação das áreas relevantes, elaboração, manutenção e revisão periódica de "
    "PDTI, contemplando objetivos, indicadores e metas alinhados aos objetivos institucionais, riscos, "
    "projetos, aquisições, recursos necessários e ações de monitoramento após aprovação pela alta "
    "administração."
)
CRITERIO_Q4_C12 = (
    "Acórdão 1.411/2014-TCU-Plenário, item 9.1.6.5 - O PDTI deve contemplar o "
    "quantitativo necessário ou ideal para a força de trabalho em TI."
)
CRITERIO_Q4_C13 = (
    "Acórdão 1.411/2014-TCU-Plenário, item 9.1.7 - A organização deve adotar "
    "providências para dotar o setor de TI de quantitativo adequado às necessidades "
    "de trabalho em TI, consideradas as necessidades das demais áreas."
)
CRITERIO_Q4_C14 = (
    "Acórdão TCE-RJ nº 44.490/2024-PLEN, itens I.10.11, III.9.11 e IV.11.3 – "
    "Referência para avaliação da estrutura de recursos humanos de TIC quanto à suficiência "
    "quantitativa e qualitativa e à preservação de capacidade interna em atividades de "
    "planejamento, coordenação, fiscalização e controle."
)
CRITERIO_Q5_C11 = (
    "Acórdão TCE-RJ nº 44.490/2024-PLEN, itens II.7.4, III.9.4 e V.6.1 – "
    "Recomendações quanto à estruturação do catálogo de serviços de TIC, incluindo descrição "
    "dos serviços, metas, formas de acesso e disponibilidade aos usuários."
)
CRITERIO_Q5_C12 = (
    "Acórdão TCE-RJ nº 44.490/2024-PLEN, itens II.7.5, III.9.5 e V.6.2 – "
    "Recomendações quanto à gestão de configuração e ativos de TIC, incluindo formalização "
    "do processo e manutenção de base consolidada de ativos e itens de configuração."
)
CRITERIO_Q5_C13 = (
    "Acórdão TCE-RJ nº 44.490/2024-PLEN, itens II.7.6, III.9.6 e V.6.3 – "
    "Recomendações quanto à formalização e execução do processo de gestão de incidentes, "
    "incluindo registros, classificação, escalamento e tratamento."
)
CRITERIO_Q5_C14 = (
    "Acórdão TCE-RJ nº 44.490/2024-PLEN, itens II.7.7, III.9.7 e V.6.4 – "
    "Recomendações quanto à definição, pactuação e monitoramento de níveis de serviço."
)
CRITERIO_Q5_C15 = (
    "ABNT NBR ISO/IEC 20000-2:2021, item 8.2.4 – Gerenciamento de catálogo de serviço: "
    "orienta que o catálogo descreva os serviços e seus resultados pretendidos, contenha "
    "informações relevantes para sua utilização e seja disponibilizado às partes interessadas "
    "que necessitem acessá-lo."
)
CRITERIO_Q5_C16 = (
    "ABNT NBR ISO/IEC 20000-2:2021, item 8.2.6 – Gerenciamento de configuração: orienta a "
    "identificação, o registro, o controle, o rastreamento e a verificação dos itens de configuração, "
    "bem como a manutenção de informações de configuração precisas relacionadas aos serviços."
)
CRITERIO_Q5_C17 = (
    "ABNT NBR ISO/IEC 20000-2:2021, item 8.6.1 – Gerenciamento de incidente: orienta que os "
    "incidentes sejam registrados, classificados e priorizados, que as ações adotadas para sua "
    "resolução sejam registradas e rastreáveis e que sejam definidas responsabilidades para seu "
    "tratamento, incluindo procedimento documentado para incidentes graves."
)
SITUACOES = {
    "s1.1": "Ausência de área, unidade, setor ou função de TIC formalmente instituída.",
    "s1.2": "Área de TIC sem atribuições formalmente definidas ou sem atribuições formais de gestão de TIC.",
    "s1.3": "Posicionamento organizacional inadequado da área de TIC.",
    "s2.1": "Ausência de objetivos, indicadores ou metas para a gestão de TIC.",
    "s2.2": "Comitê de TIC ou instância equivalente não instituído formalmente ou sem representação de áreas relevantes da organização.",
    "s2.3": "Comitê de TIC ou instância equivalente sem atuação efetiva comprovada.",
    "s3.1": "Inexistência ou insuficiência do processo de planejamento de TIC para produzir e manter plano de TIC adequado.",
    "s3.2": "Ausência de aprovação formal do plano de TIC.",
    "s3.4": "Plano de TIC sem alinhamento adequado ao planejamento institucional.",
    "s3.5": "Plano de TIC não utilizado como referência para a elaboração da proposta orçamentária e do plano de contratações.",
    "s3.6": "Ausência de acompanhamento da execução do plano de TIC.",
    "s4.1": "Ausência de força de trabalho dedicada à TIC.",
    "s4.2": "Ausência ou insuficiência de definição documentada do quantitativo necessário de pessoal de TIC e segurança da informação.",
    "s4.3": "Ausência de cargos ou funções formalmente atribuídos à TIC ou à segurança da informação.",
    "s4.6": "Operação de TIC predominantemente terceirizada sem profissionais internos de TIC.",
    "s5.1": "Inexistência ou insuficiência do catálogo de serviços de TIC.",
    "s5.2": "Ausência ou fragilidade na definição e no monitoramento de níveis mínimos de serviço de TIC.",
    "s5.3": "Inventário e controle de dispositivos e softwares de TIC inexistente ou insuficiente.",
    "s5.4": "Ausência ou fragilidade do processo de gestão de configuração.",
    "s5.5": "Inexistência ou fragilidade do processo de gestão de incidentes de TIC.",
    "s6.1": "Inexistência ou fragilidade de processo formal e padronizado para o planejamento das contratações de TIC.",
    "s6.2": "Contratações de TIC sem análise prévia e aprovação técnica da área de TIC.",
    "s6.3": "Contratações de TIC sem alinhamento ao planejamento de TIC e ao Plano de Contratações Anual.",
    "s6.4": "Contratações de TIC sem designação de equipe de planejamento com integrante técnico da área de TIC.",
}


SITUACOES_ANTERIORES = {
    "s1.1": SITUACOES["s1.1"],
    "s1.2": "Área de TIC sem atribuições formais suficientes para planejamento, coordenação, gestão, execução, monitoramento e controle da TIC.",
    "s1.3": SITUACOES["s1.3"],
    "s2.1": "Modelo básico de governança e gestão de TIC inexistente ou insuficiente quanto a papéis, responsabilidades, objetivos, indicadores, metas ou acompanhamento.",
    "s2.2": "Comitê de TIC ou instância equivalente não instituído formalmente.",
    "s2.3": "Comitê de TIC ou instância equivalente sem evidências suficientes de atuação efetiva.",
    "s3.1": "Inexistência ou fragilidade do processo formal de planejamento de TIC.",
    "s3.2": SITUACOES["s3.2"],
    "s3.4": SITUACOES["s3.4"],
    "s3.5": "Plano de TIC sem vínculo demonstrado com orçamento e contratações de TIC",
    "s3.6": "Ausência de acompanhamento, revisão ou atualização periódica do plano de TIC.",
    "s4.1": "Ausência de força de trabalho dedicada à TIC ou à segurança da informação.",
    "s4.2": "A organização não definiu o quantitativo necessário de pessoal de TIC e segurança da informação.",
    "s4.3": SITUACOES["s4.3"],
    "s4.4": "Perfis profissionais de TIC e segurança da informação inexistentes, insuficientes ou não utilizados na escolha de gestores.",
    "s4.5": "Lacunas de competências dos colaboradores e gestores de TIC e segurança da informação não são identificadas ou tratadas.",
    "s4.6": "Dependência externa relevante sem capacidade interna suficiente para coordenar e fiscalizar a TIC.",
    "s5.1": SITUACOES["s5.1"],
    "s5.2": SITUACOES["s5.2"],
    "s5.3": "Inexistência ou fragilidade do inventário de ativos de TIC.",
    "s5.4": SITUACOES["s5.4"],
    "s5.5": SITUACOES["s5.5"],
    "s6.1": "Inexistência ou fragilidade de processo formal e padronizado para contratações de TIC.",
    "s6.2": "Contratações de TIC sem análise prévia e aprovação técnica obrigatória da área de TIC.",
    "s6.3": "Contratações de TIC sem alinhamento demonstrado ao planejamento de TIC, ao plano de contratações ou à proposta orçamentária.",
    "s6.4": "Contratações de TIC sem equipe de planejamento formalmente designada e com participação técnica de TIC.",
}


DETERMINACOES = {
    "s2.2",
    "s2.3",
    "s3.1",
    "s3.2",
    "s3.4",
    "s3.5",
    "s3.6",
    "s6.1",
    "s6.3",
}


CRITERIOS_POR_SITUACAO = {
    "s1.1": (
        "COBIT 2019, APO01.04 - Definir e implementar as estruturas organizacionais: estabelecer estruturas organizacionais internas e externas necessárias para apoiar os objetivos de governança e gestão de TI.\n"
        "Constituição Federal, art. 37, caput - Princípio da eficiência."
    ),
    "s1.2": (
        "COBIT 2019, APO01.05 - Estabelecer papéis e responsabilidades: definir, comunicar e manter papéis e responsabilidades relacionados à governança e gestão de TI.\n"
        "Constituição Federal, art. 37, caput - Princípio da eficiência."
    ),
    "s1.3": (
        "COBIT 2019, APO01.06 - Aprimorar o posicionamento da função de TI: posicionar a função de tecnologia de modo compatível com sua relevância estratégica, responsabilidades e necessidade de interação com a alta administração.\n"
        "Portaria SGD/ME nº 778/2019, art. 4º, § 1º - Referência de posicionamento organizacional: para a obtenção de melhores resultados, a área de TIC de cada órgão ou entidade deve, preferencialmente, estar vinculada à alta administração, com o intuito de apoiá-la na tomada de decisões e no alcance dos objetivos estratégicos."
    ),
    "s2.1": (
        "COBIT 2019, MEA01.04 - Avaliar o desempenho: monitorar e avaliar periodicamente o desempenho e a conformidade da TI em relação a objetivos, indicadores, metas e expectativas das partes interessadas."
    ),
    "s2.2": (
        "COBIT 2019, EDM01.02 - Dirigir o sistema de governança: orientar estruturas, princípios, processos e práticas de governança para assegurar que a TI apoie os objetivos organizacionais.\n"
        "Decreto nº 12.198/2024, arts. 5º e 6º, § 2º – Referência de governança digital: instituição, no âmbito da Administração Pública federal direta, autárquica e fundacional, de Comitê de Governança Digital ou colegiado equivalente com função deliberativa sobre ações de governo digital e uso de recursos de TIC, incluindo a aprovação dos instrumentos de planejamento previstos no Decreto.\n"
        "Acórdão TCE-RJ nº 44.490/2024-PLEN, itens II.1, III.1 e V.1 – Precedente pela instituição e atuação efetiva de instância colegiada de governança de TIC, com responsabilidade pelo alinhamento das ações de TIC aos objetivos institucionais, priorização dos investimentos e monitoramento do desempenho da TIC."
    ),
    "s2.3": (
        "COBIT 2019, EDM01.02 - Dirigir o sistema de governança: orientar estruturas, princípios, processos e práticas de governança para assegurar que a TI apoie os objetivos organizacionais.\n"
        "Decreto nº 12.198/2024, arts. 5º e 6º, § 2º – Referência de governança digital: instituição, no âmbito da Administração Pública federal direta, autárquica e fundacional, de Comitê de Governança Digital ou colegiado equivalente com função deliberativa sobre ações de governo digital e uso de recursos de TIC, incluindo a aprovação dos instrumentos de planejamento previstos no Decreto.\n"
        "Acórdão TCE-RJ nº 44.490/2024-PLEN, itens II.1, III.1 e V.1 – Precedente pela instituição e atuação efetiva de instância colegiada de governança de TIC, com responsabilidade pelo alinhamento das ações de TIC aos objetivos institucionais, priorização dos investimentos e monitoramento do desempenho da TIC."
    ),
    "s3.1": (
        "COBIT 2019, APO02.05 - Definir o plano e o roteiro estratégico: estabelecer plano e roteiro de TIC que traduzam a estratégia em iniciativas, prioridades, recursos, dependências, prazos e benefícios esperados.\n"
        "Acórdão 1.411/2014-TCU-Plenário, item 9.1.6 e subitens 9.1.6.1 a 9.1.6.4: necessidade de instituir formalmente plano diretor de TI, contemplando desdobramento de diretrizes estratégicas, vinculação das ações de TI a indicadores e metas de negócio, vinculação das ações de TI a indicadores e metas de serviços ao cidadão e vinculação das ações priorizadas ao orçamento de TI.\n"
        + CRITERIO_Q3_C4
    ),
    "s3.2": (
        "Acórdão 1.411/2014-TCU-Plenário, item 9.1.6 e subitens 9.1.6.1 a 9.1.6.4: necessidade de instituir formalmente plano diretor de TI, contemplando desdobramento de diretrizes estratégicas, vinculação das ações de TI a indicadores e metas de negócio, vinculação das ações de TI a indicadores e metas de serviços ao cidadão e vinculação das ações priorizadas ao orçamento de TI.\n"
        + CRITERIO_Q3_C4
    ),
    "s3.4": (
        "COBIT 2019, APO02.05 - Definir o plano e o roteiro estratégico: estabelecer plano e roteiro de TIC que traduzam a estratégia em iniciativas, prioridades, recursos, dependências, prazos e benefícios esperados.\n"
        "Acórdão 1.411/2014-TCU-Plenário, item 9.1.6 e subitens 9.1.6.1 a 9.1.6.4: necessidade de instituir formalmente plano diretor de TI, contemplando desdobramento de diretrizes estratégicas, vinculação das ações de TI a indicadores e metas de negócio, vinculação das ações de TI a indicadores e metas de serviços ao cidadão e vinculação das ações priorizadas ao orçamento de TI.\n"
        + CRITERIO_Q3_C4
    ),
    "s3.5": (
        "COBIT 2019, APO06.03 - Criar e manter orçamentos: elaborar e manter orçamento de TIC alinhado ao portfólio, ao planejamento e às prioridades aprovadas.\n"
        + CRITERIO_Q3_C4
    ),
    "s3.6": (
        CRITERIO_Q3_C4
    ),
    "s4.1": (
        "COBIT 2019, APO07.01 - Adquirir e manter pessoal adequado e apropriado: assegurar quantidade e perfil de profissionais compatíveis com as necessidades de TIC.\n"
        + CRITERIO_Q4_C13
    ),
    "s4.2": (
        "COBIT 2019, APO07.05 - Planejar e monitorar o uso de recursos humanos de TI e de negócio: planejar, alocar e acompanhar capacidade de pessoal para iniciativas, operações e serviços de TIC.\n"
        + CRITERIO_Q4_C12
    ),
    "s4.3": (
        "COBIT 2019, APO01.05 - Estabelecer papéis e responsabilidades: definir, comunicar e manter papéis e responsabilidades relacionados à governança e gestão de TIC.\n"
        "COBIT 2019, APO07.01 - Adquirir e manter pessoal adequado e apropriado: assegurar quantidade e perfil de profissionais compatíveis com as necessidades de TIC."
    ),
    "s4.6": (
        "COBIT 2019, APO07.06 - Gerenciar pessoal contratado: controlar o uso de pessoal terceirizado ou externo, preservando responsabilização, supervisão e retenção de conhecimento.\n"
        + CRITERIO_Q4_C14
    ),
    "s5.1": (
        "COBIT 2019, APO09.02 - Catalogar serviços facilitados por TI: definir, manter e comunicar catálogo de serviços, incluindo serviços prestados, características, requisitos e níveis de serviço esperados.\n"
        + CRITERIO_Q5_C11 + "\n"
        + CRITERIO_Q5_C15
    ),
    "s5.2": (
        "ITIL 4, prática de gerenciamento de nível de serviço: definir, acordar, monitorar, avaliar e reportar metas e níveis de serviço alinhados às necessidades das áreas usuárias.\n"
        + CRITERIO_Q5_C14
    ),
    "s5.3": (
        "ITIL 4, prática de gerenciamento de ativos de TI: planejar e gerenciar o ciclo de vida dos ativos de TI, mantendo informações suficientes para apoiar controle, custo, risco, valor e tomada de decisão.\n"
        + CRITERIO_Q5_C12
    ),
    "s5.4": (
        "COBIT 2019, BAI10.01 - Estabelecer e manter um modelo de configuração: definir escopo, granularidade, atributos, relacionamentos e responsáveis pela base de configuração.\n"
        + CRITERIO_Q5_C12 + "\n"
        + CRITERIO_Q5_C16
    ),
    "s5.5": (
        "COBIT 2019, DSS02.02, DSS02.04 e DSS02.07 - Requisições de serviço e incidentes gerenciados: registrar, classificar, priorizar, investigar, diagnosticar, resolver, acompanhar e reportar incidentes e requisições de serviço.\n"
        + CRITERIO_Q5_C13 + "\n"
        + CRITERIO_Q5_C17
    ),
    "s6.1": (
        "Art. 11, parágrafo único, da Lei 14.133/2021: responsabilidade da alta administração pela governança das contratações, com processos, estruturas, gestão de riscos e controles internos.\n"
        "Art. 19, inciso IV, da Lei 14.133/2021: instituição de modelos de minutas de editais, termos de referência, contratos padronizados e demais documentos."
    ),
    "s6.2": (
        "Art. 11, parágrafo único, da Lei 14.133/2021: responsabilidade da alta administração pela governança das contratações, com processos, estruturas, gestão de riscos e controles internos.\n"
        "COBIT 2019, BAI02.04 - Obter aprovação dos requisitos da solução: obter aprovação formal dos requisitos funcionais, técnicos, de segurança e de conformidade antes de prosseguir com a solução.\n"
        "Instrução Normativa SGD/ME nº 94, de 23 de dezembro de 2022, art. 1º, § 1º: como referência de boa prática, a aplicação de ritos formais de contratação de TIC pode ser facultada para contratações diretas por dispensa em razão do valor (inciso II do art. 75 da Lei nº 14.133/2021), indicando a possibilidade de fluxos simplificados para aquisições de baixa complexidade ou valor."
    ),
    "s6.3": (
        "Art. 11, parágrafo único, da Lei 14.133/2021: responsabilidade da alta administração pela governança das contratações, com processos, estruturas, gestão de riscos e controles internos.\n"
        "Art. 18, caput e §1º, incisos I, IV, V, VIII, IX, X e XIII, da Lei 14.133/2021: fase preparatória caracterizada pelo planejamento, compatibilização com o plano de contratações anual e elementos mínimos do estudo técnico preliminar."
    ),
    "s6.4": (
        "Art. 11, parágrafo único, da Lei 14.133/2021: responsabilidade da alta administração pela governança das contratações, com processos, estruturas, gestão de riscos e controles internos.\n"
        "Art. 7º, caput, incisos I a III e §1º, da Lei 14.133/2021: designação de agentes públicos para funções essenciais, observados atribuições, formação, segregação de funções e inexistência de vínculos que comprometam a atuação."
    ),
}


ENCAMINHAMENTOS = {
    "s1.1": "formalize a área, unidade, setor ou função de TIC em instrumento compatível com a organização, definindo vinculação e responsabilidades essenciais de modo compatível com o porte, a complexidade e a dependência tecnológica da organização",
    "s1.2": "defina formalmente as atribuições da área de TIC, atentando-se, minimamente, em abranger as atividades de planejamento, coordenação, gestão e controle da TIC",
    "s1.3": "avalie o posicionamento organizacional da área de TIC e adote, quando necessário, medidas para assegurar interlocução adequada com a alta administração e participação nas decisões estratégicas, orçamentárias, contratuais e de gestão de riscos relacionadas à tecnologia da informação.",
    "s2.1": "estabeleça objetivos, indicadores e metas para a gestão de TIC, de modo a possibilitar o acompanhamento periódico do desempenho da TIC pela alta administração",
    "s2.2": "institua formalmente Comitê de TIC ou instância colegiada equivalente, compatível com o porte e a estrutura decisória da organização, definindo em seu ato constitutivo, minimamente, a participação de representantes de áreas relevantes da organização, suas competências, a periodicidade de reuniões, a forma de registro das deliberações e os mecanismos de acompanhamento dos encaminhamentos",
    "s2.3": "assegure o funcionamento efetivo do Comitê de TIC ou instância colegiada equivalente, mediante o exercício das competências previstas em seu ato constitutivo, com registro das deliberações e acompanhamento dos respectivos encaminhamentos",
    "s3.1": "institua processo formal de planejamento de TIC, compatível com o porte e a complexidade da organização, que assegure a elaboração e manutenção de plano de TIC, atentando-se, minimamente, em definir etapas, responsabilidades, participação das áreas demandantes e critérios de priorização das necessidades e iniciativas de TIC",
    "s3.2": "submeta o plano de TIC à aprovação formal do dirigente máximo ou de instância competente da alta administração, mantendo registro do respectivo ato de aprovação",
    "s3.4": "revise o plano de TIC para explicitar seu alinhamento ao planejamento institucional, às diretrizes superiores e às necessidades das áreas finalísticas e administrativas, relacionando objetivos, iniciativas, indicadores e metas de TIC aos resultados institucionais pretendidos",
    "s3.5": "integre o plano de TIC à elaboração da proposta orçamentária e do plano de contratações, de maneira proporcional ao porte, à estrutura e à capacidade de planejamento da organização",
    "s3.6": "estabeleça e execute rotina periódica de acompanhamento da execução do plano de TIC, promovendo sua revisão periódica e os ajustes ou atualizações necessários, com registro das principais decisões e reprogramações",
    "s4.1": "avalie a força de trabalho dedicada à TIC e adote medidas proporcionais para assegurar capacidade mínima de planejamento, gestão, proteção, contratação, fiscalização e sustentação dos serviços e ativos de TIC",
    "s4.2": "estime e mantenha atualizado o quantitativo necessário de pessoal de TIC e segurança da informação, considerando o porte e a complexidade da organização, os serviços críticos, os sistemas mantidos, as contratações vigentes e os riscos relevantes",
    "s4.3": "avalie a necessidade de formalizar a atribuição de cargos ou funções à TIC e à segurança da informação e adote solução compatível com as necessidades institucionais e a capacidade administrativa da organização",
    "s4.6": "avalie o modelo de operação de TIC e adote medidas proporcionais para assegurar capacidade interna suficiente para coordenar, supervisionar e fiscalizar as atividades e os contratos de TIC executados predominantemente por terceiros, preservando responsabilização e retenção de conhecimento",
    "s5.1": "institua e mantenha atualizado catálogo de serviços de TIC, atentando-se, minimamente, em identificar os serviços efetivamente prestados, seus responsáveis, usuários, condições de acesso e informações necessárias ao atendimento das áreas demandantes",
    "s5.2": "defina, acorde e monitore níveis de serviço para os serviços de TIC relevantes, estabelecendo metas e mecanismos de acompanhamento de seu cumprimento",
    "s5.3": "estabeleça e mantenha inventário atualizado dos ativos tecnológicos sob gestão da organização, contemplando, minimamente, os dispositivos e softwares utilizados, com informações suficientes para sua identificação e controle",
    "s5.4": "formalize e execute processo de gestão de configuração, atentando-se, minimamente, em manter base, ferramenta ou registro equivalente com os itens de configuração relevantes, seus responsáveis e os relacionamentos entre ativos",
    "s5.5": "formalize e execute processo de gestão de incidentes de TIC, atentando-se, minimamente, em definir papéis, critérios de priorização e escalamento, tratamento de incidentes de serviços e de segurança da informação e registro sistemático e rastreável das ocorrências",
    "s6.1": "formalize e padronize o processo de planejamento das contratações de TIC, com etapas, responsabilidades e artefatos padronizados, admitidos fluxos proporcionais à complexidade e ao risco",
    "s6.2": "estabeleça a submissão das contratações de TIC à análise prévia da área de TIC, de modo a verificar a compatibilidade da solução com os padrões tecnológicos, os requisitos institucionais e a arquitetura existente, admitindo fluxos simplificados para contratações de baixa complexidade ou baixo valor, desde que preservada análise técnica mínima compatível com o risco da contratação",
    "s6.3": "integre as contratações de TIC com os instrumentos de planejamento da organização e com o Plano de Contratações Anual, quando elaborado, justificando as situações excepcionais",
    "s6.4": "designe formalmente equipe de planejamento para as contratações de TIC, atentando-se, minimamente, em assegurar a participação de integrante da área requisitante e da área técnica de TIC, com definição das responsabilidades de seus integrantes",
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
        if proc["id"] == "PA01":
            proc["nome_achado"] = "Estrutura de TIC insuficientemente formalizada, definida ou posicionada para gerir a tecnologia da informação."
        if proc["id"] == "PA02":
            proc["descricao"] = f"Procedimento para verificar a questão Q2: {Q2}"
            proc["nome_achado"] = A2
        if proc["id"] == "PA03":
            proc["descricao"] = f"Procedimento para verificar a questão Q3: {Q3}"
            proc["nome_achado"] = A3
        if proc["id"] == "PA04":
            proc["descricao"] = f"Procedimento para verificar a questão Q4: {Q4}"
            proc["nome_achado"] = A4
        if proc["id"] == "PA05":
            proc["descricao"] = f"Procedimento para verificar a questão Q5: {Q5}"
            proc["nome_achado"] = A5
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

    av154 = copy.deepcopy(por_id["AV25"])
    av154.update(
        id="AV154",
        informacao_requerida="existe_plano_ti",
        descricao_evidencia="Resposta ao item 2102 que não caracteriza a existência de plano de TIC vigente, ainda que parcialmente adotado",
        situacao_inconforme="False",
    )
    av155 = copy.deepcopy(av154)
    av155.update(
        id="AV155",
        descricao_evidencia="Plano de TIC vigente declarado no item 2102, ao menos parcialmente adotado",
        descricao_situacao_inconforme=None,
        situacao_inconforme="True",
        tipo_encaminhamento="Determinação",
        encaminhamento=ENCAMINHAMENTOS["s3.1"],
        criterio=CRITERIOS_POR_SITUACAO["s3.1"],
    )
    por_id["AV154"] = av154
    por_id["AV155"] = av155

    situacao_por_ids = {
        "s1.1": {"AV01"},
        "s1.2": {"AV02", "AV03", "AV04", "AV84"},
        "s1.3": {"AV05", "AV06"},
        "s2.1": {"AV08"},
        "s2.2": {"AV11"},
        "s2.3": {"AV12", "AV13"},
        "s3.1": {"AV14", "AV15", "AV17", "AV154"},
        "s3.2": {"AV18"},
        "s3.4": {"AV19"},
        "s3.5": {"AV20"},
        "s3.6": {"AV24"},
        "s4.1": {"AV25", "AV26"},
        "s4.2": {"AV29"},
        "s4.3": {"AV31", "AV33"},
        "s4.6": {"AV45", "AV46"},
        "s5.1": {"AV55", "AV56"},
        "s5.2": {"AV54", "AV57", "AV58"},
        "s5.3": {"AV62", "AV63"},
        "s5.4": {"AV59", "AV66"},
        "s5.5": {"AV67", "AV70", "AV71"},
        "s6.1": {"AV73", "AV143", "AV152", "AV153"},
        "s6.2": {"AV78", "AV148"},
        "s6.3": {"AV80", "AV82", "AV150"},
        "s6.4": {"AV83"},
    }
    id_para_situacao = {acao_id: sid for sid, ids in situacao_por_ids.items() for acao_id in ids}
    ids_usados = set().union(*(ids_formula(formula) for formula in FORMULAS.values()))
    ids_sem_situacao = {"AV155"}
    if ids_usados != set(id_para_situacao) | ids_sem_situacao:
        raise AssertionError("Cadastro de situações não coincide com as ações usadas nas fórmulas.")

    acoes = []
    for acao_id in sorted(ids_usados, key=lambda valor: int(valor[2:])):
        row = copy.deepcopy(por_id[acao_id])
        sid = id_para_situacao.get(acao_id)
        if sid is None:
            acoes.append(row)
            continue
        row["descricao_situacao_inconforme"] = SITUACOES[sid]
        row["tipo_encaminhamento"] = "Determinação" if sid in DETERMINACOES else "Recomendação"
        row["criterio"] = CRITERIOS_POR_SITUACAO[sid]
        if sid in ENCAMINHAMENTOS:
            row["encaminhamento"] = ENCAMINHAMENTOS[sid]
        if acao_id == "AV45":
            row["situacao_inconforme"] = "b) Centralizada Terceirizada: Há uma área de TI centralizada e formal que faz a gestão, mas a execução operacional/técnica é predominantemente terceirizada (ex: fábricas de software, service desk)."
        if acao_id == "AV26":
            row["situacao_inconforme"] = (
                "(a) Centralizada Interna: Há uma área de TI centralizada e formal que atende toda a organização, utilizando equipe técnica majoritariamente própria (servidores). | "
                "b) Centralizada Terceirizada: Há uma área de TI centralizada e formal que faz a gestão, mas a execução operacional/técnica é predominantemente terceirizada (ex: fábricas de software, service desk). | "
                "d) Descentralizada: Diferentes secretarias, unidades ou setores possuem autonomia e mantêm suas próprias equipes, contratos ou infraestruturas de TI de forma independente. | "
                "e) Híbrida: Existe uma TI central formal para diretrizes e infraestrutura corporativa, mas as áreas de negócio possuem equipes próprias para sustentar sistemas específicos.)"
            )
        acoes.append(row)
    rewrite_sheet(ws_acoes, acao_headers, acoes)

    ws_motivos = wb["Motivos do Relatório"]
    motivos_headers, motivos_originais = rows_as_dicts(ws_motivos)
    motivos = []
    for motivo in motivos_originais:
        motivo = copy.deepcopy(motivo)
        if motivo["id"] == "MR010":
            motivo["condicao_exibicao"] = "AV08"
        elif motivo["id"] == "MR016":
            motivo["condicao_exibicao"] = "AV11"
        elif motivo["id"] == "MR018":
            motivo["condicao_exibicao"] = "AV12 & AV13"
        elif motivo["id"] == "MR020":
            motivo["condicao_exibicao"] = "AV12 & AV13"
        elif motivo["id"] == "MR022":
            motivo["condicao_exibicao"] = "AV14"
        elif motivo["id"] == "MR024":
            motivo["condicao_exibicao"] = "AV15"
        elif motivo["id"] == "MR028":
            motivo["condicao_exibicao"] = "AV17"
        elif motivo["id"] == "MR030":
            motivo["condicao_exibicao"] = "AV155 & AV18"
        elif motivo["id"] == "MR032":
            motivo["condicao_exibicao"] = "AV155 & AV19"
        elif motivo["id"] == "MR034":
            motivo["condicao_exibicao"] = "AV155 & AV20"
        elif motivo["id"] == "MR041":
            motivo["condicao_exibicao"] = "AV155 & AV24"
        elif motivo["id"] == "MR045":
            motivo["condicao_exibicao"] = "AV29"
        elif motivo["id"] == "MR047":
            motivo["condicao_exibicao"] = "AV31"
        elif motivo["id"] == "MR049":
            motivo["condicao_exibicao"] = "AV33"
        elif motivo["id"] == "MR065":
            motivo["condicao_exibicao"] = "AV54"
        elif motivo["id"] == "MR067":
            motivo["condicao_exibicao"] = "AV55"
        elif motivo["id"] == "MR069":
            motivo["condicao_exibicao"] = "AV56"
        elif motivo["id"] == "MR071":
            motivo["condicao_exibicao"] = "AV57"
        elif motivo["id"] == "MR073":
            motivo["condicao_exibicao"] = "AV58"
        elif motivo["id"] == "MR075":
            motivo["condicao_exibicao"] = "AV59"
        elif motivo["id"] == "MR077":
            motivo["condicao_exibicao"] = "AV62"
        elif motivo["id"] == "MR079":
            motivo["condicao_exibicao"] = "AV63"
        elif motivo["id"] == "MR083":
            motivo["condicao_exibicao"] = "AV66"
        elif motivo["id"] == "MR085":
            motivo["condicao_exibicao"] = "AV67"
        elif motivo["id"] == "MR087":
            motivo["condicao_exibicao"] = "AV70"
        elif motivo["id"] == "MR089":
            motivo["condicao_exibicao"] = "AV71"
        elif motivo["id"] == "MR043":
            motivo["condicao_exibicao"] = "AV26 & AV25"
            motivo["texto_motivo"] = "Item 0105: embora a organização tenha declarado estrutura formal de TIC no item 0101, informou não possuir profissionais atuando regularmente em tecnologia da informação"
        elif motivo["id"] == "MR062":
            motivo["texto_motivo"] = "A organização informou modelo de operação de TIC com execução predominantemente terceirizada, o que levou à análise de sua capacidade interna de coordenação e fiscalização"
        elif motivo["id"] == "MR063":
            motivo["texto_motivo"] = "Não foram identificados profissionais internos de TIC para coordenar e fiscalizar a execução das atividades de tecnologia da informação"
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
        texto_motivo="No subitem b) do item 2801, não houve declaração afirmativa quanto à prática avaliada: são disponibilizados artefatos padronizados para a fase de planejamento das contratações de TI, como Documento de Formalização da Demanda (DFD), Estudo Técnico Preliminar (ETP), Termo de Referência (TR), Matriz de Riscos ou documentos equivalentes",
    )
    motivo_b_evidencia = copy.deepcopy(next(row for row in motivos_originais if row["id"] == "MR092"))
    motivo_b_evidencia.update(
        id="MR112",
        descricao_situacao_inconforme=SITUACOES["s6.1"],
        condicao_exibicao="AV153",
        acoes_referencia="AV153",
        texto_motivo="No subitem b) do item 2801, a organização declarou a prática avaliada, mas a evidência foi insuficiente para comprovar que são disponibilizados artefatos padronizados para a fase de planejamento das contratações de TI, como Documento de Formalização da Demanda (DFD), Estudo Técnico Preliminar (ETP), Termo de Referência (TR), Matriz de Riscos ou documentos equivalentes",
    )
    motivos.extend([motivo_b, motivo_b_evidencia])
    motivo_sem_plano = copy.deepcopy(next(row for row in motivos_originais if row["id"] == "MR030"))
    motivo_sem_plano.update(
        id="MR113",
        descricao_situacao_inconforme=SITUACOES["s3.1"],
        condicao_exibicao="AV154",
        acoes_referencia="AV154",
        texto_motivo="No item 2102, a organização não declarou possuir plano de tecnologia da informação vigente, ainda que parcialmente adotado",
    )
    motivos.append(motivo_sem_plano)
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
    variaveis.append(
        {
            "id": "VT06",
            "id_fonte_informacao": "questionario",
            "nome": "existe_plano_ti",
            "expressao": "(q2102 == 'Adota parcialmente.') | (q2102 == 'Adota em maior parte ou totalmente.')",
            "descricao": "Indica que a organização declarou possuir plano de TIC vigente, ao menos parcialmente adotado.",
        }
    )
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
    alterado = False
    if not all(presentes):
        for coluna in colunas:
            ws.cell(1, ws.max_column + 1, coluna)
        alterado = True

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
    preenchidos = 0
    for row_index in range(2, ws.max_row + 1):
        auditado = str(ws.cell(row_index, auditado_col).value or "").strip().upper()
        registro = registros.get(auditado)
        valores = {
            "q2801ext[B]": "Não conforme" if registro is not None else None,
            "q2801ext[B]__resposta_afirmada": str(registro.get("Resposta afirmada") or "") if registro is not None else None,
            "q2801ext[B]__justificativa": str(registro.get("justificativa_final") or "") if registro is not None else None,
            "q2801ext[B]__pratica": "são disponibilizados artefatos padronizados para a fase de planejamento das contratações de TIC" if registro is not None else None,
        }
        for coluna, valor in valores.items():
            cell = ws.cell(row_index, novos_headers[coluna])
            if cell.value != valor:
                cell.value = valor
                alterado = True
        if registro is not None:
            preenchidos += 1
    if alterado:
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


def remove_once(text: str, line: str) -> str:
    """Remove uma linha exata, exigindo ocorrência única."""
    alvo = line + "\n"
    count = text.count(alvo)
    if count != 1:
        raise AssertionError(f"Esperada uma ocorrência da linha, encontradas {count}: {line[:100]!r}")
    return text.replace(alvo, "", 1)


def gerar_matriz() -> None:
    text = MATRIZ_ORIGINAL.read_text(encoding="utf-8")
    text = replace_once(
        text,
        "- A área de TIC possui atribuições formalmente definidas de planejamento, coordenação, gestão, execução, monitoramento e controle da TIC?",
        "- A área de TIC possui atribuições formalmente definidas relacionadas à gestão da TIC?",
    )
    text = replace_once(
        text,
        "- O posicionamento organizacional da área de TIC é compatível com suas atribuições e permite atuação adequada em decisões estratégicas, orçamentárias, contratuais e de gestão de riscos?",
        "- A área de TIC está posicionada em nível organizacional que favoreça sua interlocução com a alta administração e sua atuação estratégica?",
    )
    text = replace_once(
        text,
        "- R1.2: Devido à ausência de atribuições formais da área de TIC, poderá não haver clareza sobre responsabilidades de planejamento, coordenação, gestão, execução, monitoramento e controle da TIC, favorecendo atuação reativa e fragmentada.",
        "- R1.2: Devido à ausência de atribuições formais da área de TIC, poderá não haver clareza sobre responsabilidades de planejamento, coordenação, gestão e controle da TIC, favorecendo atuação reativa e fragmentada.",
    )
    text = replace_once(
        text,
        "- IR1: Resposta sobre existência formal de área, unidade, setor ou função de TIC e respectivo modelo de operação predominante da TIC; [F1, q0101]",
        "- IR1: Resposta sobre a existência formal de área, unidade, setor ou função de TIC; [F1, q0101]",
    )
    text = replace_once(
        text,
        "- IR4: Evidência anexada que demonstre atribuições formais relacionadas às principais funções de TIC, incluindo governança, planejamento, gestão, sustentação tecnológica, sistemas, segurança da informação, contratos, dados ou atividades correlatas; [F2, q0103evi]",
        "- IR4: Evidência anexada que demonstre atribuições formalmente definidas relacionadas à gestão da TIC; [F2, q0103evi]",
    )
    text = replace_once(
        text,
        "- P3: Verificar, por meio da resposta à q0103, se a área de TIC possui atribuições formalmente definidas; [IR3]",
        "- P3: Verificar, por meio da resposta à q0103, se a área de TIC possui atribuições formalmente definidas relacionadas à gestão da TIC; [IR3]",
    )
    text = replace_once(
        text,
        "- P4: Validar, pela evidência anexada à q0103, se as atribuições abrangem funções essenciais de TIC, como governança, planejamento, gestão, sustentação tecnológica, sistemas, segurança da informação, contratos, dados ou atividades correlatas; [IR4]",
        "- P4: Validar, pela evidência anexada à q0103, a existência de atribuições formalmente definidas relacionadas à gestão da TIC; [IR4]",
    )
    text = replace_once(
        text,
        "- E4: Ausência, desatualização, incompatibilidade ou insuficiência de evidência que defina atribuições essenciais da área de TIC, como governança, planejamento, gestão, sustentação tecnológica, sistemas, segurança da informação, contratos, dados ou atividades correlatas; [P4]",
        "- E4: Ausência ou insuficiência de evidência que demonstre atribuições formalmente definidas relacionadas à gestão da TIC; [P4]",
    )
    text = replace_once(
        text,
        "- A1: Estrutura de TIC insuficiente para coordenar, gerir e sustentar a tecnologia da informação.",
        "- A1: Estrutura de TIC insuficientemente formalizada, definida ou posicionada para gerir a tecnologia da informação.",
    )
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
            "- C7: Constituição Federal, art. 37, caput - Princípio da eficiência.",
            "- C8: Lei nº 14.133/2021, art. 11, parágrafo único - Dever da alta administração de implementar processos e estruturas de governança das contratações.",
        ],
        "- C5: COBIT 2019, APO01.05 - Estabelecer papéis e responsabilidades: definir, comunicar e manter papéis e responsabilidades relacionados à governança e gestão de TI.": [
            "- C6: Lei nº 14.133/2021, art. 11, parágrafo único - Dever da alta administração de implementar estruturas de governança das contratações.",
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

    # Enxugamento aprovado dos catálogos de critérios: mantém somente os critérios
    # citados pelas situações inconformes, com 2 a 3 critérios essenciais por situação.
    linhas_criterio_removidas = [
        "- C4: COBIT 2019, APO01.09 - Definição e comunicação de políticas e procedimentos: estabelecer e comunicar políticas e procedimentos de gestão de TI que orientem papéis, responsabilidades e controles.",
        "- C5: ABNT NBR ISO/IEC 38500:2025, item 5.6.1 - Governança efetiva de TI: responsabilização clara, estrutura adequada de tomada de decisão e direção organizacional compatível com o uso atual e futuro da tecnologia.",
        "- C8: Lei nº 14.133/2021, art. 11, parágrafo único - Dever da alta administração de implementar processos e estruturas de governança das contratações.",
        "- C1: COBIT 2019, EDM01.02 - Dirigir o sistema de governança: orientar estruturas, princípios, processos e práticas de governança para assegurar que a TI apoie os objetivos organizacionais.",
        "- C3: Decreto nº 12.198/2024, art. 5º - Instituição do CGD, colegiado responsável por definir diretrizes e estratégias sobre uso de recursos digitais nos órgãos e entidades da administração pública federal direta, autárquica e fundacional.",
        "- C5: COBIT 2019, APO01.05 - Estabelecer papéis e responsabilidades: definir, comunicar e manter papéis e responsabilidades relacionados à governança e gestão de TI.",
        "- C5: Lei nº 14.133/2021, arts. 11, parágrafo único, e 18, caput - Governança e planejamento da fase preparatória das contratações.",
        "- C6: Constituição Federal, art. 37, caput - Princípio da eficiência.",
        "- C3: COBIT 2019, APO07.02 - Identificar pessoal-chave de TI: identificar funções e pessoas críticas para reduzir dependência individual, perda de conhecimento e descontinuidade.",
        "- C4: COBIT 2019, APO07.03 - Manter habilidades e competências do pessoal: identificar, desenvolver e manter competências necessárias à execução das responsabilidades de TIC.",
        "- C7: COBIT 2019, APO10.04 - Gerenciar risco de fornecedores: identificar e tratar riscos decorrentes de fornecedores, contratos e dependências externas relevantes para TIC.",
        "- C8: COBIT 2019, DSS01.02 - Gerenciar serviços de TI terceirizados: assegurar que serviços terceirizados sejam supervisionados, medidos e integrados aos controles da organização.",
        "- C9: ABNT NBR ISO/IEC 27001:2022, cláusulas 5.3 e 7.2: definir responsabilidades e autoridades para segurança da informação e assegurar competências necessárias às funções atribuídas.",
        "- C10: ABNT NBR ISO/IEC 27002:2022, controles 5.2 e 6.3: definir papéis e responsabilidades de segurança da informação e promover conscientização, educação e treinamento em segurança.",
        "- C7: ITIL 4, prática de gerenciamento de incidentes: minimizar o impacto negativo dos incidentes por meio da restauração tempestiva da operação normal dos serviços e do registro rastreável do tratamento realizado.",
        "- C6: COBIT 2019, APO01.05 - Estabelecer papéis e responsabilidades: definir e comunicar papéis e responsabilidades relacionados à informação e à tecnologia.",
        "- C7: COBIT 2019, APO01.09 - Definir e comunicar políticas e procedimentos: manter políticas, procedimentos e orientações para direcionar processos de gestão de TIC.",
    ]
    for linha in linhas_criterio_removidas:
        text = remove_once(text, linha)

    # Q1: procedimentos e evidências sem ação de verificação correspondente no mapa
    # (q0101evi é impossível quando q0101 = F; q0102evi não é avaliado documentalmente).
    linhas_q1_removidas = [
        "- IR2: Evidência anexada que demonstre a formalização da área, unidade, setor ou função de TIC, como regimento, decreto, portaria, resolução, organograma, ato administrativo ou instrumento equivalente; [F2, q0101evi]",
        "- IR6: Evidência anexada que demonstre o posicionamento organizacional da área de TIC, como organograma institucional, regimento interno ou documento equivalente; [F2, q0102evi]",
        "- P2: Validar, pela evidência anexada à q0101, a formalização da área, unidade, setor ou função de TIC; [IR2]",
        "- P6: Validar, pela evidência anexada à q0102, a compatibilidade do posicionamento da área de TIC com suas atribuições institucionais; [IR6]",
        "- E2: Ausência, desatualização, incompatibilidade ou insuficiência de evidência que formalize a área, unidade, setor ou função de TIC; [P2]",
        "- E6: Evidência anexada inexistente, incompatível ou insuficiente para demonstrar posicionamento adequado da área de TIC; [P6]",
    ]
    for linha in linhas_q1_removidas:
        text = remove_once(text, linha)

    # Critérios jurisprudenciais incorporados pela revisão, com âncora própria no catálogo.
    insercoes_criterios = {
        "- C6: Lei nº 14.133/2021, art. 11, parágrafo único - Dever da alta administração de implementar estruturas de governança das contratações.": [
            "- C8: Acórdão TCU 1.411/2014-Plenário, item 9.1.2 - Precedente sobre funcionamento permanente e composição relevante do Comitê de TIC.",
        ],
        "- C11: Lei nº 14.133/2021, art. 117 - Dever de acompanhamento e fiscalização da execução contratual por representantes da Administração especialmente designados.": [
            f"- C12: {CRITERIO_Q4_C12}",
            f"- C13: {CRITERIO_Q4_C13}",
        ],
    }
    for anchor, novas in insercoes_criterios.items():
        text = replace_once(text, anchor, anchor + "\n" + "\n".join(novas))

    # Q4: escopo reduzido à capacidade institucional efetivamente testada (força de
    # trabalho, quantitativo, cargos e dependência de terceiros); perfis e lacunas de
    # competências deixam de sustentar situação inconforme e saem da matriz.
    text = replace_once(
        text,
        "questao: Q4. A organização dispõe de capacidade institucional mínima, em termos de força de trabalho, perfis profissionais, competências, funções e vínculos, para planejar, gerir, proteger, contratar, fiscalizar e sustentar a TIC e a segurança da informação de forma adequada às suas necessidades institucionais?",
        "questao: Q4. A organização dispõe de capacidade institucional mínima, em termos de força de trabalho, funções e vínculos, para planejar, gerir, proteger, contratar, fiscalizar e sustentar a TIC e a segurança da informação de forma adequada às suas necessidades institucionais?",
    )
    text = replace_once(
        text,
        "- A organização possui cargos, funções, perfis ou ocupações específicas de TIC e segurança da informação?",
        "- A organização possui cargos ou funções formalmente atribuídos à TIC e à segurança da informação?",
    )
    text = replace_once(
        text,
        "- R4.3: Devido à inexistência de cargos, funções, perfis ou ocupações específicas de TIC e segurança da informação, poderá haver baixa capacidade de atração, alocação, responsabilização e retenção de profissionais.",
        "- R4.3: Devido à ausência de cargos ou funções formalmente atribuídos à TIC ou à segurança da informação, poderá haver baixa clareza de responsabilidades e insuficiente capacidade de alocação e responsabilização dos profissionais.",
    )
    for linha in [
        "- A organização definiu perfis profissionais esperados para gestores e colaboradores de TIC e segurança da informação?",
        "- A organização identifica e trata lacunas de competências dos colaboradores e gestores de TIC e segurança da informação?",
        "- R4.4: Devido à ausência de perfis profissionais definidos para gestores e colaboradores de TIC e segurança da informação, poderá haver designação de pessoas sem competências compatíveis com as responsabilidades exercidas.",
        "- R4.5: Devido à ausência de identificação e tratamento de lacunas de competências, poderá haver incapacidade de executar práticas mínimas de planejamento, gestão, segurança, contratação, fiscalização e sustentação de TIC.",
    ]:
        text = remove_once(text, linha)
    text = replace_once(
        text,
        """- IR3: Resposta sobre existência de cargos específicos em TIC e segurança da informação; [F1, q2708]
- IR4: Resposta e evidência sobre perfis profissionais desejados para gestores de TIC e segurança da informação; [F1, F2, q2701, q2701evi]
- IR5: Resposta e evidência sobre perfis profissionais desejados para colaboradores de TIC e segurança da informação; [F1, F2, q2702, q2702evi]
- IR6: Resposta e evidência sobre escolha dos gestores de TIC e segurança da informação segundo perfis previamente definidos; [F1, F2, q2704, q2704evi]
- IR7: Resposta e evidência sobre identificação de lacunas de competências; [F1, F2, q2705, q2705evi]
- IR8: Resposta e evidência sobre tratamento das lacunas de competências; [F1, F2, q2706, q2706evi]
- IR9: Respostas e evidências que permitam avaliar dependência de terceiros e capacidade interna de coordenação e fiscalização; [F1, F2, q0101, q0105, q2703, q2801, q2804]""",
        """- IR3: Resposta sobre existência de cargos ou funções formalmente atribuídos à TIC e à segurança da informação; [F1, q2708]
- IR9: Resposta sobre o modelo de operação predominante de TIC e o quantitativo de profissionais internos de TIC, para avaliação da dependência de terceiros e da capacidade interna de coordenação e fiscalização; [F1, q0101, q0105]""",
    )
    text = replace_once(
        text,
        """- P3: Verificar, por meio da q2708, se há cargos específicos em TIC e segurança da informação; [IR3]
- P4: Verificar, por meio das q2701 e q2702 e respectivas evidências, se há perfis profissionais definidos para gestores e colaboradores de TIC e segurança da informação; [IR4, IR5]
- P5: Verificar, por meio da q2704 e respectiva evidência, se a escolha dos gestores de TIC e segurança da informação ocorre segundo perfis previamente definidos; [IR6]
- P6: Verificar, por meio das q2705 e q2706 e respectivas evidências, se lacunas de competências são identificadas e tratadas; [IR7, IR8]
- P7: Verificar, por cruzamento das respostas e evidências das q0101, q0105, q2703, q2801 e q2804, se há dependência excessiva de terceiros para atividades críticas sem capacidade interna suficiente de coordenação e fiscalização; [IR9]""",
        """- P3: Verificar, por meio da q2708, se há cargos ou funções formalmente atribuídos à TIC e à segurança da informação; [IR3]
- P7: Verificar, por meio da resposta à q0101 e do quantitativo de profissionais internos informado na q0105, se o modelo de operação de TIC é predominantemente terceirizado sem capacidade interna suficiente de coordenação e fiscalização; [IR9]""",
    )
    text = replace_once(
        text,
        """- E3: Resposta negativa sobre existência de cargos específicos em TIC e segurança da informação; [P3]
- E4: Resposta negativa ou insuficiente sobre perfis profissionais definidos para gestores ou colaboradores de TIC e segurança da informação, ou evidência inexistente/incompatível/insuficiente; [P4]
- E5: Resposta negativa ou insuficiente sobre escolha de gestores segundo perfis profissionais definidos, ou evidência inexistente/incompatível/insuficiente; [P5]
- E6: Resposta negativa ou insuficiente sobre identificação ou tratamento de lacunas de competências, ou evidência inexistente/incompatível/insuficiente; [P6]
- E7: Evidência, a partir das respostas e anexos do questionário, de dependência excessiva de terceiros em atividades críticas sem capacidade interna suficiente de coordenação, fiscalização ou retenção de conhecimento; [P7]""",
        """- E3: Resposta negativa sobre existência de cargos ou funções formalmente atribuídos à TIC ou à segurança da informação; [P3]
- E7: Modelo de operação de TIC predominantemente terceirizado (q0101 = B) sem profissionais internos de TIC (total de efetivos, comissionados, cedidos e temporários igual a zero); [P7]""",
    )
    # Q6: a equipe de planejamento é verificada pela resposta declarada (q2804[C]);
    # a evidência genérica de processo (q2801evi) não é testada nesta situação.
    text = replace_once(
        text,
        "- IR7: Resposta e evidência sobre equipe de planejamento formalmente designada e multidisciplinar; [F1, F2, q2804[C], q2801evi]",
        "- IR7: Resposta sobre equipe de planejamento formalmente designada e com participação técnica de TIC; [F1, q2804[C]]",
    )
    text = replace_once(
        text,
        "- P5: Verificar, por meio da q2804[C] e da q2801evi, se a equipe de planejamento da contratação é formalmente designada e possui participação técnica de TIC; [IR7]",
        "- P5: Verificar, por meio da q2804[C], se a equipe de planejamento da contratação é formalmente designada e possui participação técnica de TIC; [IR7]",
    )

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

    # Histórico da renumeração anteriormente proposta. A lista é mantida somente
    # para documentar a reversão; identificadores de auditoria são estáveis e as
    # lacunas decorrentes de itens retirados devem ser preservadas.
    renumeracoes = [
        # Q1
        ("- IR3: Resposta sobre atribuições e competências formalizadas da área de TIC; [F1, q0103]",
         "- IR2: Resposta sobre atribuições e competências formalizadas da área de TIC; [F1, q0103]"),
        ("- IR4: Evidência anexada que demonstre atribuições formais relacionadas às principais funções de TIC, incluindo governança, planejamento, gestão, sustentação tecnológica, sistemas, segurança da informação, contratos, dados ou atividades correlatas; [F2, q0103evi]",
         "- IR3: Evidência anexada que demonstre atribuições formais relacionadas às principais funções de TIC, incluindo governança, planejamento, gestão, sustentação tecnológica, sistemas, segurança da informação, contratos, dados ou atividades correlatas; [F2, q0103evi]"),
        ("- IR5: Resposta sobre posicionamento hierárquico da área de TIC na estrutura organizacional; [F1, q0102]",
         "- IR4: Resposta sobre posicionamento hierárquico da área de TIC na estrutura organizacional; [F1, q0102]"),
        ("- P3: Verificar, por meio da resposta à q0103, se a área de TIC possui atribuições formalmente definidas; [IR3]",
         "- P2: Verificar, por meio da resposta à q0103, se a área de TIC possui atribuições formalmente definidas; [IR2]"),
        ("- P4: Validar, pela evidência anexada à q0103, se as atribuições abrangem funções essenciais de TIC, como governança, planejamento, gestão, sustentação tecnológica, sistemas, segurança da informação, contratos, dados ou atividades correlatas; [IR4]",
         "- P3: Validar, pela evidência anexada à q0103, se as atribuições abrangem funções essenciais de TIC, como governança, planejamento, gestão, sustentação tecnológica, sistemas, segurança da informação, contratos, dados ou atividades correlatas; [IR3]"),
        ("- P5: Verificar, por meio da resposta à q0102, o posicionamento hierárquico da área de TIC; [IR5]",
         "- P4: Verificar, por meio da resposta à q0102, o posicionamento hierárquico da área de TIC; [IR4]"),
        ("- E3: Resposta negativa ou insuficiente sobre atribuições formalizadas da área de TIC; [P3]",
         "- E2: Resposta negativa ou insuficiente sobre atribuições formalizadas da área de TIC; [P2]"),
        ("- E4: Ausência, desatualização, incompatibilidade ou insuficiência de evidência que defina atribuições essenciais da área de TIC, como governança, planejamento, gestão, sustentação tecnológica, sistemas, segurança da informação, contratos, dados ou atividades correlatas; [P4]",
         "- E3: Ausência, desatualização, incompatibilidade ou insuficiência de evidência que defina atribuições essenciais da área de TIC, como governança, planejamento, gestão, sustentação tecnológica, sistemas, segurança da informação, contratos, dados ou atividades correlatas; [P3]"),
        ("- E5: Resposta que indique posicionamento inexistente ou incompatível da área de TIC; [P5]",
         "- E4: Resposta que indique posicionamento inexistente ou incompatível da área de TIC; [P4]"),
        ("referencias_matriz: [R1.2, P3, E3, P4, E4]", "referencias_matriz: [R1.2, P2, E2, P3, E3]"),
        ("referencias_matriz: [R1.3, P5, E5, P6, E6]", "referencias_matriz: [R1.3, P4, E4]"),
        # Q3
        ("- R3.4: Devido à falta de alinhamento do plano de TIC ao planejamento institucional, poderão ser executadas ações de TIC com baixo valor para a organização.",
         "- R3.3: Devido à falta de alinhamento do plano de TIC ao planejamento institucional, poderão ser executadas ações de TIC com baixo valor para a organização."),
        ("- R3.5: Devido à ausência de integração entre planejamento de TIC, orçamento e contratações, poderão ocorrer aquisições reativas, não priorizadas ou desalinhadas.",
         "- R3.4: Devido à ausência de integração entre planejamento de TIC, orçamento e contratações, poderão ocorrer aquisições reativas, não priorizadas ou desalinhadas."),
        ("- R3.6: Devido à ausência de acompanhamento e revisão do plano de TIC, poderão permanecer metas, iniciativas e prioridades incompatíveis com mudanças institucionais, orçamentárias ou tecnológicas.",
         "- R3.5: Devido à ausência de acompanhamento e revisão do plano de TIC, poderão permanecer metas, iniciativas e prioridades incompatíveis com mudanças institucionais, orçamentárias ou tecnológicas."),
        ("- IR7: Resposta e evidência sobre alinhamento do plano de TIC ao planejamento institucional; [F1, F2, q2102, q2102evi]",
         "- IR6: Resposta e evidência sobre alinhamento do plano de TIC ao planejamento institucional; [F1, F2, q2102, q2102evi]"),
        ("- IR8: Resposta e evidência sobre a previsão, no plano de TIC, dos recursos orçamentários necessários à execução das iniciativas; [F1, F2, q2102ext[C], q2102evi]",
         "- IR7: Resposta e evidência sobre a previsão, no plano de TIC, dos recursos orçamentários necessários à execução das iniciativas; [F1, F2, q2102ext[C], q2102evi]"),
        ("- IR9: Resposta e evidência sobre acompanhamento, revisão ou atualização do plano de TIC; [F1, F2, q2102, q2102evi]",
         "- IR8: Resposta e evidência sobre acompanhamento, revisão ou atualização do plano de TIC; [F1, F2, q2102, q2102evi]"),
        ("- P7: Verificar, por meio da resposta e das evidências da q2102, se o plano está alinhado ao planejamento institucional; [IR7]",
         "- P6: Verificar, por meio da resposta e das evidências da q2102, se o plano está alinhado ao planejamento institucional; [IR6]"),
        ("- P8: Verificar, por meio da resposta e da evidência da q2102ext[C], se o plano de TIC prevê os recursos orçamentários necessários à execução das iniciativas; [IR8]",
         "- P7: Verificar, por meio da resposta e da evidência da q2102ext[C], se o plano de TIC prevê os recursos orçamentários necessários à execução das iniciativas; [IR7]"),
        ("- P9: Verificar, por meio da resposta e das evidências da q2102, se há acompanhamento, revisão ou atualização periódica do plano de TIC; [IR9]",
         "- P8: Verificar, por meio da resposta e das evidências da q2102, se há acompanhamento, revisão ou atualização periódica do plano de TIC; [IR8]"),
        ("- E7: Inexistência ou insuficiência de alinhamento entre plano de TIC e planejamento institucional; [P7]",
         "- E6: Inexistência ou insuficiência de alinhamento entre plano de TIC e planejamento institucional; [P6]"),
        ("- E8: Inexistência ou insuficiência de previsão orçamentária no plano de TIC; [P8]",
         "- E7: Inexistência ou insuficiência de previsão orçamentária no plano de TIC; [P7]"),
        ("- E9: Ausência de registros de acompanhamento, revisão ou atualização do plano de TIC; [P9]",
         "- E8: Ausência de registros de acompanhamento, revisão ou atualização do plano de TIC; [P8]"),
        ("  - S3.4:", "  - S3.3:"),
        ("  - S3.5:", "  - S3.4:"),
        ("  - S3.6:", "  - S3.5:"),
        ("referencias_matriz: [R3.4, P7, E7]", "referencias_matriz: [R3.3, P6, E6]"),
        ("referencias_matriz: [R3.5, P8, E8]", "referencias_matriz: [R3.4, P7, E7]"),
        ("referencias_matriz: [R3.6, P9, E9]", "referencias_matriz: [R3.5, P8, E8]"),
        # Q4
        ("- R4.6: Devido à dependência excessiva de terceiros para atividades críticas de TIC, sem capacidade interna suficiente de coordenação e fiscalização, poderá haver perda de conhecimento, baixa governabilidade e risco de descontinuidade dos serviços.",
         "- R4.4: Devido à dependência excessiva de terceiros para atividades críticas de TIC, sem capacidade interna suficiente de coordenação e fiscalização, poderá haver perda de conhecimento, baixa governabilidade e risco de descontinuidade dos serviços."),
        ("- IR9: Resposta sobre o modelo de operação predominante de TIC e o quantitativo de profissionais internos de TIC, para avaliação da dependência de terceiros e da capacidade interna de coordenação e fiscalização; [F1, q0101, q0105]",
         "- IR4: Resposta sobre o modelo de operação predominante de TIC e o quantitativo de profissionais internos de TIC, para avaliação da dependência de terceiros e da capacidade interna de coordenação e fiscalização; [F1, q0101, q0105]"),
        ("- P7: Verificar, por meio da resposta à q0101 e do quantitativo de profissionais internos informado na q0105, se o modelo de operação de TIC é predominantemente terceirizado sem capacidade interna suficiente de coordenação e fiscalização; [IR9]",
         "- P4: Verificar, por meio da resposta à q0101 e do quantitativo de profissionais internos informado na q0105, se o modelo de operação de TIC é predominantemente terceirizado sem capacidade interna suficiente de coordenação e fiscalização; [IR4]"),
        ("- E7: Modelo de operação de TIC predominantemente terceirizado (q0101 = B) sem profissionais internos de TIC (total de efetivos, comissionados, cedidos e temporários igual a zero); [P7]",
         "- E4: Modelo de operação de TIC predominantemente terceirizado (q0101 = B) sem profissionais internos de TIC (total de efetivos, comissionados, cedidos e temporários igual a zero); [P4]"),
        ("  - S4.6:", "  - S4.4:"),
        ("    referencias_matriz: [R4.6, P7, E7]", "    referencias_matriz: [R4.4, P4, E4]"),
    ]
    renumeracoes = []
    texto_renumerado = "\n".join(lines)
    for antigo, novo in renumeracoes:
        n = texto_renumerado.count(antigo)
        if n != 1:
            raise AssertionError(f"Renumeração esperava uma ocorrência, encontradas {n}: {antigo[:90]!r}")
        texto_renumerado = texto_renumerado.replace(antigo, novo, 1)
    inicio_q2 = texto_renumerado.index("## Questão 02 - Governança e Comitê de TIC")
    inicio_q3 = texto_renumerado.index("## Questão 03 - Planejamento de TIC", inicio_q2)
    texto_renumerado = texto_renumerado[:inicio_q2] + Q2_BLOCK + "\n\n" + texto_renumerado[inicio_q3:]
    inicio_q3 = texto_renumerado.index("## Questão 03 - Planejamento de TIC")
    inicio_q4 = texto_renumerado.index("## Questão 04 - Capacidade Institucional de TIC e Segurança da Informação", inicio_q3)
    texto_renumerado = texto_renumerado[:inicio_q3] + Q3_BLOCK + "\n\n" + texto_renumerado[inicio_q4:]
    inicio_q4 = texto_renumerado.index("## Questão 04 - Capacidade Institucional de TIC e Segurança da Informação")
    inicio_q5 = texto_renumerado.index("## Questão 05 - Gestão de Serviços de TIC", inicio_q4)
    texto_renumerado = texto_renumerado[:inicio_q4] + Q4_BLOCK + "\n\n" + texto_renumerado[inicio_q5:]
    inicio_q5 = texto_renumerado.index("## Questão 05 - Gestão de Serviços de TIC")
    inicio_q6 = texto_renumerado.index("## Questão 06 - Contratações de TIC", inicio_q5)
    texto_renumerado = texto_renumerado[:inicio_q5] + Q5_BLOCK + "\n\n" + texto_renumerado[inicio_q6:]
    lines = texto_renumerado.splitlines()

    updates = {
        "S1.1": dict(descricao=SITUACOES["s1.1"], itens_questionario="[q0101]", referencias_matriz="[R1.1, P1, E1]", criterios="[C1, C7]", tipo_encaminhamento="Recomendação", encaminhamento=ENCAMINHAMENTOS["s1.1"]),
        "S1.2": dict(descricao=SITUACOES["s1.2"], itens_questionario="[q0101, q0103, q0103[D], q0103[G], q0103evi]", referencias_matriz="[R1.2, P3, E3, P4, E4]", criterios="[C2, C7]", tipo_encaminhamento="Recomendação", encaminhamento=ENCAMINHAMENTOS["s1.2"]),
        "S1.3": dict(itens_questionario="[q0102]", criterios="[C3, C6]", referencias_matriz="[R1.3, P5, E5]", encaminhamento=ENCAMINHAMENTOS["s1.3"]),
        "S2.1": dict(descricao=SITUACOES["s2.1"], itens_questionario="[q1001ext[H], q1001evi]", criterios="[C2]", tipo_encaminhamento="Recomendação", encaminhamento=ENCAMINHAMENTOS["s2.1"]),
        "S2.2": dict(descricao=SITUACOES["s2.2"], itens_questionario="[q1001ext[E], q1001evi]", referencias_matriz="[R2.2, P3, E3, P4, E4]", criterios="[C1, C3, C4]", tipo_encaminhamento="Determinação", encaminhamento=ENCAMINHAMENTOS["s2.2"]),
        "S2.3": dict(descricao=SITUACOES["s2.3"], criterios="[C1, C3, C4]", tipo_encaminhamento="Determinação", encaminhamento=ENCAMINHAMENTOS["s2.3"]),
        "S6.1": dict(descricao=SITUACOES["s6.1"], itens_questionario="[q2801ext[A], q2801ext[B], q2801evi]", criterios="[C1, C3]", tipo_encaminhamento="Determinação", encaminhamento=ENCAMINHAMENTOS["s6.1"]),
        "S6.2": dict(descricao=SITUACOES["s6.2"], criterios="[C1, C5, C8]", encaminhamento=ENCAMINHAMENTOS["s6.2"]),
        "S6.3": dict(descricao=SITUACOES["s6.3"], itens_questionario="[q2802ext[C], q2804[B], q2802evi]", criterios="[C1, C2]", tipo_encaminhamento="Determinação", encaminhamento=ENCAMINHAMENTOS["s6.3"]),
        "S6.4": dict(descricao=SITUACOES["s6.4"], itens_questionario="[q2804[C]]", criterios="[C1, C4]", encaminhamento=ENCAMINHAMENTOS["s6.4"]),
    }
    rules = {
        "S1.2": ["(q0101 != F) & ((q0103[G] == Sim) | (q0103[D] == Não))"],
        "S1.3": ["(q0101 != F) & ((q0102 == C) | (q0102 == D) | (q0102 == E))"],
        "S2.1": ["(q1001ext[H] != Sim)"],
        "S2.2": ["(q1001ext[E] != Sim)"],
        "S2.3": ["(q1001ext[E] == Sim) & (q1001ext[F] != Sim)"],
        "S6.1": ["(q2801ext[A] != Sim) | (q2801ext[B] != Sim)"],
        "S6.3": ["(q2802ext[C] != Sim) | (q2804[B] != Sim)"],
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
        ("AJ-038", "Mapa e matriz/S1.2 × S2.1", "q0103D e q1001C podiam gerar situações distintas pelo mesmo fato", "S1.2 mantém competências formais por q0103; S2.1 usa somente q1001H (AV08)", "Elimina sobreposição entre competência formal da área de TIC e direção estratégica exercida pela alta administração."),
        ("AJ-039", "Mapa e matriz/PA03/S3.5", "Plano de TIC sem previsão orçamentária demonstrada; encaminhamento exigia estimativa dos recursos e memória ou referência", SITUACOES["s3.5"] + " Encaminhamento: " + ENCAMINHAMENTOS["s3.5"], "Alinha a situação e o encaminhamento ao conteúdo efetivamente verificado por q2102ext[C], sem exigir estimativa orçamentária ou memória de cálculo não avaliadas pelo questionário."),
        ("AJ-040", "Mapa e matriz/PA06/Q6", "A organização adota controles mínimos na fase preparatória das contratações de TIC, com processo definido e análise técnica pela unidade competente?", Q6, "Substitui expressão genérica por requisitos verificáveis e cobre processo formal e padronizado, responsabilidades, análise técnica e alinhamento ao planejamento."),
        ("AJ-041", "Matriz/Q1, Q3 e Q4/identificadores", "Referências e situações renumeradas para eliminar lacunas", "Restaurar IR/P/E originais; S3.4, S3.5, S3.6 e S4.6", "Identificadores de auditoria são estáveis; a retirada de conteúdo deve preservar as lacunas e a rastreabilidade histórica."),
        ("AJ-042", "Matriz/PA02/S2.3", "Somente negativa declaratória de q1001ext[F]", "q1001ext[E] = Sim e (q1001ext[F] != Sim ou evidência de atuação insuficiente)", "Reproduz conceitualmente a fórmula AV12 & (AV13 | AV91) já utilizada no mapa."),
        ("AJ-043", "Mapa/Procedimentos de Auditoria/PA04", "Descrição anterior de Q4 com perfis profissionais e competências", "Descrição vigente da Q4 com força de trabalho, funções e vínculos", "Mantém identidade entre a questão da matriz e a descrição do procedimento operacional."),
        ("AJ-044", "Mapa e matriz/PA04/S4.3", "Ausência de cargos, funções, perfis ou ocupações específicas de TIC e segurança da informação", SITUACOES["s4.3"], "Limita a descrição ao conteúdo efetivamente testado por q2708[B] e q2708[D]."),
        ("AJ-045", "Matriz/PA01/S1.3", "itens_questionario: [q0102, q0102evi]", "itens_questionario: [q0102]", "Remove referência residual a evidência que não integra IR, procedimento, evidência nem ação de verificação da situação."),
        ("AJ-046", "Matriz/PA04/S4.1", "Indentação inconsistente nos campos da situação", "Indentação uniforme dos campos e regras", "Preserva a estrutura documental e evita ambiguidade de leitura ou processamento."),
        ("AJ-047", "Mapa/Motivos do Relatório/MR062", "Menção também à estrutura central externa", "Menção somente à execução predominantemente terceirizada", "AV45 aceita exclusivamente o modelo q0101=B; o motivo deve descrever o mesmo gatilho."),
        ("AJ-048", "Mapa/Motivos do Relatório/MR063", "Quantitativo interno insuficiente", "Ausência de profissionais internos de TIC", "AV46 testa total interno exatamente igual a zero, e não insuficiência quantitativa."),
        ("AJ-049", "Matriz/Q3/C5", "Critério legal específico ausente", f"C5: {CRITERIO_Q3_C5}", "Acrescenta à Q3 fundamento legal específico sobre integração entre PCA, planejamento estratégico e leis orçamentárias."),
        ("AJ-050", "Mapa e matriz/PA03/S3.4-S3.5", "S3.4: [C3, C4]; S3.5: [C2, C3, C4]", "S3.4: [C1, C3, C4]; S3.5: [C2, C4, C5]", "Limita cada situação a três critérios diretamente relacionados ao respectivo objeto; em S3.5, substitui o C3 pelo fundamento legal C5."),
        ("AJ-051", "Matriz/Q4/C12-C13", "Critérios jurisprudenciais específicos sobre força de trabalho de TIC ausentes", f"C12: {CRITERIO_Q4_C12} C13: {CRITERIO_Q4_C13}", "Cria identificadores novos para não reutilizar C3 e C4 removidos e preserva a rastreabilidade histórica."),
        ("AJ-052", "Mapa e matriz/PA04/S4.1-S4.2", "S4.1: [C2, C9]; S4.2: [C5, C9]", "S4.1: [C2, C13]; S4.2: [C5, C12]", "Substitui o critério ISO genérico por precedentes do TCU diretamente aderentes à existência e ao dimensionamento da força de trabalho de TIC."),
        ("AJ-053", "Mapa e matriz/PA01/Q1", "Escopo amplo das atribuições, C4 em S1.2 e título genérico do achado", "Gestão da TIC como núcleo; S1.2 com [C2, C7]; achado sobre formalização, definição e posicionamento", "Restringe a Q1 ao mínimo essencial efetivamente testado e mantém correspondência entre subquestão, informação requerida, procedimento, evidência, situação e critério."),
        ("AJ-054", "Mapa e matriz/PA01/S1.1-S1.3", "S1.1 e S1.2 como determinação; encaminhamentos anteriores de S1.2 e S1.3", "Todas as situações da Q1 como recomendação; encaminhamentos revisados", "Os gatilhos são predominantemente declaratórios ou apoiados em referenciais de boa prática e preservam espaço para solução organizacional proporcional."),
        ("AJ-055", "Mapa e matriz/PA02/Q2", "Questão, riscos, critérios e encaminhamentos anteriores", "Q2 revisada com C1 a C4 e foco em objetivos, composição e atuação do Comitê", "Mantém apenas os elementos essenciais de governança efetivamente abrangidos pelos itens H, E e F da q1001."),
        ("AJ-056", "Mapa e matriz/PA02/S2.1-S2.3", "AV08 | AV86; AV11 | AV89; AV12 & (AV13 | AV91)", "AV08; AV11; AV12 & AV13", "A decisão mais recente trata a avaliação documental como evidência de suporte, sem convertê-la em gatilho autônomo das situações; S2.1 retorna a recomendação."),
        ("AJ-057", "Mapa e matriz/PA03/Q3", "Questão, riscos, procedimentos, evidências e situações anteriores", "Q3 revisada com processo formal, plano vigente, aprovação, alinhamento, integração e acompanhamento", "Consolida a rastreabilidade da questão e preserva a lacuna S3.3, mantendo estáveis os identificadores das situações."),
        ("AJ-058", "Mapa/PA03/S3.1-S3.6", "Ações declaratórias e documentais sem gate comum de plano vigente", "VT06 existe_plano_ti; S3.1 inclui AV154; S3.2-S3.6 exigem AV155", "Restringe as situações sobre atributos do plano às organizações que declararam plano vigente ao menos parcialmente adotado; evidências permanecem como suporte, sem gatilho autônomo."),
        ("AJ-059", "Mapa e matriz/PA04/Q4", "Questão, riscos, critérios e situações anteriores", "Q4 revisada com foco em estruturação, dimensionamento, funções e capacidade interna nos modelos terceirizados", "Delimita a questão aos mecanismos mínimos efetivamente testados e incorpora o C14 como precedente específico do TCE-RJ."),
        ("AJ-060", "Mapa/PA04/S4.1-S4.6", "AV26 aceitava todo modelo diferente de F; AV103/AV105/AV107 eram gatilhos; S4.6 era determinação", "AV26 restrito a A/B/D/E; retirada dos gatilhos documentais; S4.6 como recomendação", "Exclui o modelo centralizado externo de S4.1, trata evidências documentais como suporte e reconhece que a regra de S4.6 indica oportunidade de melhoria sem comprovar irregularidade concreta de fiscalização."),
        ("AJ-061", "Mapa e matriz/PA05/Q5", "Questão, riscos, critérios, procedimentos e situações anteriores", "Q5 revisada com catálogo, níveis de serviço, inventário de ativos, gestão de configuração e incidentes", "Mantém apenas as práticas mínimas efetivamente testadas, explicita a rastreabilidade e incorpora referências específicas do TCE-RJ e da ABNT NBR ISO/IEC 20000-2:2021."),
        ("AJ-062", "Mapa/PA05/S5.1-S5.5", "Evidências documentais como gatilhos autônomos; q2203A em S5.3; S5.3 como determinação", "Regras declaratórias; q2504A/B em S5.3; q2203A/C em S5.4; todas as situações como recomendação", "Trata as evidências como suporte, separa inventário de ativos da gestão de configuração e ajusta a natureza dos encaminhamentos aos referenciais predominantemente orientadores."),
    ]
    tipo_rows = [
        ("S2.2", "Recomendação", "Determinação", "Decreto nº 12.198/2024, arts. 5º e 6º, § 2º; Acórdão TCE-RJ nº 44.490/2024, itens II.1, III.1 e V.1", "O Decreto é referência federal; a determinação se apoia também no precedente do TCE-RJ e deve admitir instância equivalente."),
        ("S3.4", "Recomendação", "Determinação", "Acórdão TCE-RJ nº 44.490/2024, item II.3", "O processo estruturado do PDTI determinado contempla objetivos, indicadores e metas de TI alinhados aos objetivos de negócio."),
        ("S3.5", "Recomendação", "Determinação", "Lei nº 14.133/2021, art. 12, VII e § 1º; Acórdão TCE-RJ nº 44.490/2024, item II.3", "Integração do plano de TIC à proposta orçamentária e ao PCA, observado o condicionamento legal 'quando elaborado'."),
        ("S2.3", "Recomendação", "Determinação", "Decreto nº 12.198/2024, arts. 5º e 6º, § 2º; Acórdão TCE-RJ nº 44.490/2024, itens II.1, III.1 e V.1", "Aplicável somente se a entidade declarou possuir Comitê; a atuação exigida deve observar seu ato constitutivo."),
        ("S3.1", "Recomendação", "Determinação", "Lei nº 14.133/2021, arts. 11 e 18; precedentes TCU/TCE-RJ", "Admitir instrumento equivalente a PDTI/PEDTIC, desde que satisfaça o resultado."),
        ("S3.2", "Recomendação", "Determinação", "Lei nº 14.133/2021, arts. 11 e 18; precedentes TCU/TCE-RJ", "A aprovação deve ser pela instância competente, sem impor colegiado específico."),
        ("S3.6", "Recomendação", "Determinação", "Acórdão TCE-RJ nº 44.490/2024, item II.3.5", "Vincular a obrigação ao plano efetivamente adotado."),
        ("S4.6", "Recomendação", "Determinação", "Lei nº 14.133/2021, art. 117", "Art. 117 exige fiscalização, não quadro próprio de TIC; regra calibrada para terceirização e ausência total de capacidade interna."),
        ("S5.3", "Recomendação", "Determinação", "LGPD, arts. 46 e 50", "A LGPD impõe segurança, mas não nomeia inventário; encaminhamento deve exigir resultado equivalente e proporcional ao tratamento de dados."),
        ("S6.1", "Recomendação", "Determinação", "Lei nº 14.133/2021, arts. 11 e 19, IV", "Art. 19, IV dirige-se aos órgãos com competência regulamentar; para os demais, exigir adoção de modelos aplicáveis, próprios ou compartilhados."),
        ("S6.3", "Recomendação", "Determinação", "Lei nº 14.133/2021, arts. 12, VII, e 18", "A compatibilização com o PCA é obrigatória quando o plano tiver sido elaborado."),
    ]
    result = [
        {"ID": rid, "Artefato / objeto": obj, "DE": old, "PARA": new, "Motivação / justificativa": why, "Situação": "Aplicado"}
        for rid, obj, old, new, why in rows
    ]
    for row in result:
        if row["ID"] in {"AJ-003", "AJ-004", "AJ-005", "AJ-042"}:
            row["Situação"] = "Superado por AJ-056"
        if row["ID"] in {"AJ-006", "AJ-049", "AJ-050"}:
            row["Situação"] = "Superado por AJ-057/AJ-058"
        if row["ID"] in {"AJ-032", "AJ-043"}:
            row["Situação"] = "Superado por AJ-059/AJ-060"
        if row["ID"] == "AJ-009":
            row["Situação"] = "Superado por AJ-061/AJ-062"
    for idx, (sid, old, new, fundamento, ressalva) in enumerate(tipo_rows, start=25):
        result.append(
            {
                "ID": f"AJ-{idx:03d}",
                "Artefato / objeto": f"Mapa e matriz/{sid}/tipo de encaminhamento",
                "DE": old,
                "PARA": new,
                "Motivação / justificativa": f"{fundamento}. Ressalva de aplicação: {ressalva}",
                "Situação": (
                    "Superado por AJ-059/AJ-060" if sid == "S4.6" else
                    "Superado por AJ-061/AJ-062" if sid == "S5.3" else
                    "Aplicado"
                ),
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
        ("S2.2", "Orientação anterior de manter AV89 como gatilho alternativo versus nova regra declaratória", "AV11", "Prevalece a decisão mais recente: a evidência documental permanece prevista na matriz como suporte, mas não gera autonomamente a situação."),
        ("S4.1", "AV26 & (AV25 | AV27) versus instrução posterior AV26 & AV25 e retirada de total_SI", "AV26 & AV25", "Prevalece a instrução posterior e específica; zero em SI não prova ausência da função."),
        ("S6.3", "Menção inicial a q2802 C-D e q2804B versus fórmula final AV82 | (AV80 | AV150)", "q2804B e q2802C", "Prevalece a fórmula final expressa; q2802D foi excluído."),
        ("S4.6", "Determinação por falta de fiscalização versus regra que testa apenas terceirização e ausência de pessoal interno", "q0101B & total_TI_interno=0, com recomendação", "A condição indica risco de insuficiência de capacidade interna, mas não comprova irregularidade concreta na fiscalização; o C14 sustenta avaliação proporcional."),
        ("S5.3 × S5.4", "q2203A tratado como inventário de ativos versus conteúdo de base consolidada de configurações", "q2504A/B em S5.3; q2203A/C em S5.4", "O inventário de dispositivos e softwares permanece distinto da base de itens de configuração e de seus relacionamentos; as evidências documentais apoiam a validação, mas não são gatilhos autônomos."),
        ("S6.1", "Exigir q2801B com painel sem a coluna", "Painel vigente ampliado com B e metadados", f"Foram materializados {painel_preenchidos} registros não conformes já avaliados; nenhum resultado foi inventado."),
        ("S1.2 × S2.1", "q0103D e q1001C mediam, em grande parte, a mesma formalização de responsabilidades", "S1.2 conserva q0103D; S2.1 passa a usar somente q1001H", "Distingue competência formal da unidade de direção estratégica por objetivos, indicadores e metas."),
        ("Q3/plano vigente", "Itens de detalhamento q2102ext aplicados mesmo quando não havia plano vigente", "VT06 define existe_plano_ti; S3.2 a S3.6 dependem desse gate", "Evita imputar deficiências de aprovação, alinhamento, integração ou acompanhamento a quem ainda não possui plano vigente; nesses casos, aplica-se S3.1."),
        ("Natureza jurídica", "Determinação baseada em dever de resultado versus norma sem artefato nominal", "Determinação com equivalência funcional e proporcionalidade", "Evita transformar PDTI, Comitê ou inventário em modelo organizacional único quando o dever jurídico admite solução equivalente."),
    ]
    for row in contradicoes:
        ws.append(row)
    estilizar_planilha(ws, {"A": 20, "B": 68, "C": 48, "D": 88})

    ws = wb.create_sheet("Encaminhamentos")
    ws.append(["Situação", "Tipo anterior", "Tipo aplicado", "Fundamento consolidado", "Ressalva de aplicação"])
    for sid, tipo_anterior, tipo_aplicado, fundamento, ressalva in [
        ("S2.2", "Recomendação", "Determinação", "Decreto nº 12.198/2024, arts. 5º e 6º, § 2º; Acórdão TCE-RJ nº 44.490/2024, itens II.1, III.1 e V.1", "O Decreto é referência federal; admitir Comitê ou instância equivalente compatível com a organização."),
        ("S3.4", "Recomendação", "Determinação", "Acórdão TCE-RJ nº 44.490/2024, item II.3", "PDTI determinado contempla objetivos, indicadores e metas de TI alinhados aos objetivos de negócio."),
        ("S3.5", "Recomendação", "Determinação", "Lei nº 14.133/2021, art. 12, VII e § 1º; Acórdão TCE-RJ nº 44.490/2024, item II.3", "Integração do plano de TIC à proposta orçamentária e ao PCA, observado o condicionamento legal 'quando elaborado'."),
        ("S2.3", "Recomendação", "Determinação", "Decreto nº 12.198/2024, arts. 5º e 6º, § 2º; Acórdão TCE-RJ nº 44.490/2024, itens II.1, III.1 e V.1", "Somente para quem declarou Comitê; observar as competências do ato constitutivo."),
        ("S3.1", "Recomendação", "Determinação", "Lei nº 14.133/2021, arts. 11 e 18; precedentes TCU/TCE-RJ", "Admitir instrumento equivalente a PDTI/PEDTIC."),
        ("S3.2", "Recomendação", "Determinação", "Lei nº 14.133/2021, arts. 11 e 18; precedentes TCU/TCE-RJ", "Aprovação pela instância competente."),
        ("S3.6", "Recomendação", "Determinação", "Acórdão TCE-RJ nº 44.490/2024, II.3.5", "Vincular ao plano adotado."),
        ("S4.6", "Determinação", "Recomendação", "Acórdão TCE-RJ nº 44.490/2024-PLEN, itens I.10.11, III.9.11 e IV.11.3", "A regra demonstra risco de capacidade interna, mas não comprova descumprimento concreto do dever de fiscalização."),
        ("S5.3", "Determinação", "Recomendação", CRITERIO_Q5_C12, "O precedente formula recomendações e o gatilho declaratório não demonstra, por si só, descumprimento de dever legal expresso."),
        ("S6.1", "Recomendação", "Determinação", "Lei nº 14.133/2021, arts. 11 e 19, IV", "Art. 19, IV, tem destinatário qualificado; admitir modelos compartilhados aplicáveis."),
        ("S6.3", "Recomendação", "Determinação", "Lei nº 14.133/2021, arts. 12, VII, e 18", "Compatibilização com PCA quando elaborado."),
    ]:
        ws.append([sid, tipo_anterior, tipo_aplicado, fundamento, ressalva])
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
        (7, "Eliminar variáveis temporárias não usadas e criar o gate do plano", "Aba Variáveis Temporárias", "Permanecem total_TI, total_TI_interno e existe_plano_ti."),
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
