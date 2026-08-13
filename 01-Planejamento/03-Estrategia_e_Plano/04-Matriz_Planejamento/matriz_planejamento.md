---
title: "Fiscalização TCE-RJ nº 18/2026 - iGovTI 2026"
---

# Matriz de Planejamento

## Questão Geral de Auditoria

questao_geral: Qual é o grau de adoção das práticas de governança e gestão de TIC das organizações avaliadas, segundo o iGovTI 2026, e quais fragilidades relevantes estão presentes?
---

## Questão 01 - Estrutura de TIC

questao: Q1. A organização possui área, unidade, setor ou função de TIC formalmente instituída, com atribuições definidas e posicionamento organizacional compatível com suas responsabilidades institucionais?

subquestoes:
- A organização possui área, unidade, setor ou função de TIC formalmente instituída?
- A área de TIC possui atribuições formalmente definidas de planejamento, coordenação, gestão, execução, monitoramento e controle da TIC?
- O posicionamento organizacional da área de TIC é compatível com suas atribuições e permite atuação adequada em decisões estratégicas, orçamentárias, contratuais e de gestão de riscos?

riscos:
- R1.1: Devido à ausência de formalização da área de TIC, poderá não haver unidade ou função institucionalmente reconhecida para coordenar o uso da tecnologia da informação, prejudicando a responsabilização e o alinhamento da TIC aos objetivos da organização.
- R1.2: Devido à ausência de atribuições formais da área de TIC, poderá não haver clareza sobre responsabilidades de planejamento, coordenação, gestão, execução, monitoramento e controle da TIC, favorecendo atuação reativa e fragmentada.
- R1.3: Devido ao posicionamento organizacional inadequado da área de TIC, poderá haver baixa capacidade de influência institucional, comprometendo a participação da TIC em decisões estratégicas, orçamentárias, contratuais e de gestão de riscos.

fontes_de_informacao:
- F1: Respostas ao questionário eletrônico iGovTI.
- F2: Evidências anexadas ao questionário eletrônico.

informacoes_requeridas:
- IR1: Resposta sobre existência formal de área, unidade, setor ou função de TIC e respectivo modelo de operação predominante da TIC; [F1, q0101]
- IR2: Evidência anexada que demonstre a formalização da área, unidade, setor ou função de TIC, como regimento, decreto, portaria, resolução, organograma, ato administrativo ou instrumento equivalente; [F2, q0101evi]
- IR3: Resposta sobre atribuições e competências formalizadas da área de TIC; [F1, q0103]
- IR4: Evidência anexada que demonstre atribuições formais relacionadas às principais funções de TIC, incluindo governança, planejamento, gestão, sustentação tecnológica, sistemas, segurança da informação, contratos, dados ou atividades correlatas; [F2, q0103evi]
- IR5: Resposta sobre posicionamento hierárquico da área de TIC na estrutura organizacional; [F1, q0102]
- IR6: Evidência anexada que demonstre o posicionamento organizacional da área de TIC, como organograma institucional, regimento interno ou documento equivalente; [F2, q0102evi]

criterios:
- C1: COBIT 2019, APO01.04 - Definir e implementar as estruturas organizacionais: estabelecer estruturas organizacionais internas e externas necessárias para apoiar os objetivos de governança e gestão de TI.
- C2: COBIT 2019, APO01.05 - Estabelecer papéis e responsabilidades: definir, comunicar e manter papéis e responsabilidades relacionados à governança e gestão de TI.
- C3: COBIT 2019, APO01.06 - Aprimorar o posicionamento da função de TI: posicionar a função de tecnologia de modo compatível com sua relevância estratégica, responsabilidades e necessidade de interação com a alta administração.
- C4: COBIT 2019, APO01.09 - Definição e comunicação de políticas e procedimentos: estabelecer e comunicar políticas e procedimentos de gestão de TI que orientem papéis, responsabilidades e controles.
- C5: ABNT NBR ISO/IEC 38500:2025, item 5.6.1 - Governança efetiva de TI: responsabilização clara, estrutura adequada de tomada de decisão e direção organizacional compatível com o uso atual e futuro da tecnologia.
- C6: Portaria SGD/ME nº 778/2019, art. 4º, § 1º - Referência de posicionamento organizacional: para a obtenção de melhores resultados, a área de TIC de cada órgão ou entidade deve, preferencialmente, estar vinculada à alta administração, com o intuito de apoiá-la na tomada de decisões e no alcance dos objetivos estratégicos.

procedimentos:
- P1: Verificar, por meio da resposta à q0101, se a organização possui área, unidade, setor ou função de TIC formalmente instituída; [IR1]
- P2: Validar, pela evidência anexada à q0101, a formalização da área, unidade, setor ou função de TIC; [IR2]
- P3: Verificar, por meio da resposta à q0103, se a área de TIC possui atribuições formalmente definidas; [IR3]
- P4: Validar, pela evidência anexada à q0103, se as atribuições abrangem funções essenciais de TIC, como governança, planejamento, gestão, sustentação tecnológica, sistemas, segurança da informação, contratos, dados ou atividades correlatas; [IR4]
- P5: Verificar, por meio da resposta à q0102, o posicionamento hierárquico da área de TIC; [IR5]
- P6: Validar, pela evidência anexada à q0102, a compatibilidade do posicionamento da área de TIC com suas atribuições institucionais; [IR6]

evidencias:
- E1: Resposta negativa ou insuficiente sobre formalização da área, unidade, setor ou função de TIC; [P1]
- E2: Ausência, desatualização, incompatibilidade ou insuficiência de evidência que formalize a área, unidade, setor ou função de TIC; [P2]
- E3: Resposta negativa ou insuficiente sobre atribuições formalizadas da área de TIC; [P3]
- E4: Ausência, desatualização, incompatibilidade ou insuficiência de evidência que defina atribuições essenciais da área de TIC, como governança, planejamento, gestão, sustentação tecnológica, sistemas, segurança da informação, contratos, dados ou atividades correlatas; [P4]
- E5: Resposta que indique posicionamento inexistente ou incompatível da área de TIC; [P5]
- E6: Evidência anexada inexistente, incompatível ou insuficiente para demonstrar posicionamento adequado da área de TIC; [P6]

possiveis_achados:
- A1: Estrutura de TIC insuficiente para coordenar, gerir e sustentar a tecnologia da informação.
  situacoes_encontradas:
    - S1.1:
      descricao: Ausência de área, unidade, setor ou função de TIC formalmente instituída.
      severidade: alta
      itens_questionario: [q0101, q0101evi]
      regra_de_identificacao:
      - (q0101 == F)
      referencias_matriz: [R1.1, P1, E1, P2, E2]
      criterios: [C1, C4, C5]
      tipo_encaminhamento: Recomendação
      encaminhamento: formalize a área, unidade, setor ou função de TIC em regimento, decreto, portaria, resolução, organograma ou instrumento equivalente, definindo sua vinculação e suas responsabilidades essenciais de modo compatível com o porte, a complexidade e a dependência tecnológica da organização
    - S1.2:
      descricao: Área de TIC sem atribuições formais suficientes para planejamento, coordenação, gestão, execução, monitoramento e controle da TIC.
      severidade: alta
      itens_questionario: [q0101, q0103, q0103[D], q0103[G], q0103evi]
      regra_de_identificacao:
      - (q0101 != F) & ((q0103[G] == Sim) | (q0103[D] == Não))
      referencias_matriz: [R1.2, P3, E3, P4, E4]
      criterios: [C2, C4, C5]
      tipo_encaminhamento: Recomendação
      encaminhamento: defina formalmente as atribuições da área de TIC, atentando-se, minimamente, em abranger as atividades de planejamento, coordenação, gestão, execução, monitoramento e controle da TIC
    - S1.3:
      descricao: Posicionamento organizacional inadequado da área de TIC.
      severidade: media
      itens_questionario: [q0102, q0102evi]
      regra_de_identificacao:
      - (q0101 != F) & ((q0102 == B) | (q0102 == C) | (q0102 == D) | (q0102 == E))
      referencias_matriz: [R1.3, P5, E5, P6, E6]
      criterios: [C3, C5, C6]
      tipo_encaminhamento: Recomendação
      encaminhamento: avalie e ajuste o posicionamento organizacional da área de TIC, atentando-se, minimamente, em assegurar interlocução adequada com a alta administração e participação nas decisões estratégicas, orçamentárias, contratuais e de gestão de riscos relacionadas à tecnologia da informação

## Questão 02 - Governança e Comitê de TIC

questao: Q2. A organização possui mecanismos básicos de governança de TIC estabelecidos pela alta administração, incluindo modelo de governança e gestão, objetivos, indicadores, metas e Comitê de TIC ou instância equivalente formalmente instituída e atuante?

subquestoes:
- A alta administração estabeleceu modelo básico de governança e gestão de TIC, com papéis, responsabilidades, objetivos, indicadores ou metas para a TIC?
- O Comitê de TIC ou instância equivalente está formalmente instituído?
- O Comitê de TIC ou instância equivalente atua de forma efetiva, com reuniões, registros de deliberação ou encaminhamentos formais?

riscos:
- R2.1: Devido à ausência de modelo básico de governança e gestão de TIC, poderá haver baixa clareza sobre papéis, responsabilidades, objetivos, indicadores, metas e acompanhamento do desempenho da TIC.
- R2.2: Devido à inexistência de Comitê de TIC ou instância equivalente, poderá não haver instância colegiada para deliberação sobre prioridades, projetos, riscos, serviços, orçamento e contratações de TIC.
- R2.3: Devido à ausência de evidências de atuação efetiva do Comitê de TIC ou instância equivalente, poderá não haver deliberação efetiva sobre prioridades, projetos, riscos, serviços, orçamento e contratações de TIC.

fontes_de_informacao:
- F1: Respostas ao questionário eletrônico iGovTI.
- F2: Evidências anexadas ao questionário eletrônico.

informacoes_requeridas:
- IR1: Respostas sobre existência de diretrizes, papéis, responsabilidades, objetivos, indicadores, metas e práticas básicas de governança e gestão de TIC estabelecidas pela alta administração; [F1, q1001, q1002]
- IR2: Evidências anexadas que demonstrem modelo básico de governança e gestão de TIC, incluindo políticas, diretrizes, definição de papéis e responsabilidades, objetivos, indicadores, metas, relatórios de acompanhamento, medições de desempenho ou instrumentos equivalentes; [F2, q1001evi, q1002evi]
- IR3: Resposta sobre existência de Comitê de TIC ou instância equivalente formalmente instituído; [F1, q1001ext[E]]
- IR4: Evidência anexada que demonstre instituição formal do Comitê de TIC ou instância equivalente, com composição, competências, periodicidade ou forma de deliberação; [F2, q1001evi]
- IR5: Resposta sobre existência de reuniões ou atuação efetiva do Comitê de TIC ou instância equivalente; [F1, q1001ext[F]]
- IR6: Evidência anexada que demonstre atuação efetiva do Comitê de TIC ou instância equivalente, como atas, pautas, listas de presença, registros de deliberação, decisões, encaminhamentos ou acompanhamento de pendências; [F2, q1001evi]

criterios:
- C1: COBIT 2019, EDM01.02 - Dirigir o sistema de governança: orientar estruturas, princípios, processos e práticas de governança para assegurar que a TI apoie os objetivos organizacionais.
- C2: COBIT 2019, MEA01.04 - Avaliar o desempenho: monitorar e avaliar periodicamente o desempenho e a conformidade da TI em relação a objetivos, indicadores, metas e expectativas das partes interessadas.
- C3: Decreto nº 12.198/2024, art. 5º - Instituição do CGD, colegiado responsável por definir diretrizes e estratégias sobre uso de recursos digitais nos órgãos e entidades da administração pública federal direta, autárquica e fundacional.
- C4: Acórdão TCE-RJ 44.490/2024-PLEN, item II.1: necessidade de estrutura de governança de TI, especialmente Comitê de Tecnologia da Informação ou instância equivalente, com participação de áreas relevantes, responsabilidade de alinhar as ações de TI aos objetivos institucionais, priorizar investimentos e monitorar o desempenho da TI com base em indicadores e metas.
- C5: COBIT 2019, APO01.05 - Estabelecer papéis e responsabilidades: definir, comunicar e manter papéis e responsabilidades relacionados à governança e gestão de TI.

procedimentos:
- P1: Verificar, por meio das respostas às q1001 e q1002, se há modelo básico de governança e gestão de TIC com papéis, responsabilidades, objetivos, indicadores, metas ou monitoramento; [IR1]
- P2: Validar, pelas evidências anexadas às q1001 e q1002, a existência e suficiência do modelo básico de governança e gestão de TIC; [IR2]
- P3: Verificar, por meio da resposta à q1001ext[E], se o Comitê de TIC ou instância equivalente está formalmente instituído; [IR3]
- P4: Validar, pela evidência anexada à q1001, se há ato, norma, regimento, portaria ou documento equivalente que formalize o Comitê de TIC ou instância equivalente; [IR4]
- P5: Verificar, por meio da resposta à q1001ext[F], se há reuniões, deliberações ou atuação efetiva do Comitê de TIC ou instância equivalente; [IR5]
- P6: Validar, pela evidência anexada à q1001, se há atas, pautas, registros de deliberação, encaminhamentos ou acompanhamento de decisões do Comitê de TIC ou instância equivalente; [IR6]

evidencias:
- E1: Resposta negativa ou insuficiente sobre modelo básico de governança e gestão de TIC; [P1]
- E2: Ausência, desatualização, incompatibilidade ou insuficiência de evidências que demonstrem diretrizes, papéis, responsabilidades, objetivos, indicadores, metas ou acompanhamento de TIC; [P2]
- E3: Resposta negativa ou insuficiente sobre instituição formal de Comitê de TIC ou instância equivalente; [P3]
- E4: Ausência, desatualização, incompatibilidade ou insuficiência de evidência que formalize Comitê de TIC ou instância equivalente; [P4]
- E5: Resposta negativa ou insuficiente sobre reuniões, deliberações ou atuação efetiva do Comitê de TIC ou instância equivalente; [P5]
- E6: Ausência, desatualização, incompatibilidade ou insuficiência de atas, registros de deliberação, encaminhamentos ou acompanhamento de decisões do Comitê de TIC ou instância equivalente; [P6]

possiveis_achados:
- A2: Governança de TIC insuficiente para avaliar, dirigir e monitorar a tecnologia da informação.
  situacoes_encontradas:
    - S2.1:
      descricao: Modelo básico de governança e gestão de TIC inexistente ou insuficiente quanto a papéis, responsabilidades, objetivos, indicadores, metas ou acompanhamento.
      severidade: alta
      itens_questionario: [q1001ext[C], q1001ext[H], q1002ext[A], q1002ext[C], q1001evi, q1002evi]
      regra_de_identificacao:
      - (q1001ext[C] != Sim) | (q1001ext[H] != Sim) | (q1002ext[A] != Sim) | (q1002ext[C] != Sim)
      referencias_matriz: [R2.1, P1, E1, P2, E2]
      criterios: [C1, C2, C4]
      tipo_encaminhamento: Recomendação
      encaminhamento: estabeleça modelo básico de governança e gestão de TIC, atentando-se, minimamente, em definir papéis e responsabilidades, objetivos, indicadores, metas e forma de acompanhamento periódico do desempenho da TIC pela alta administração
    - S2.2:
      descricao: Comitê de TIC ou instância equivalente não instituído formalmente.
      severidade: alta
      itens_questionario: [q1001ext[E], q1001evi]
      regra_de_identificacao:
      - (q1001ext[E] != Sim)
      referencias_matriz: [R2.2, P3, E3, P4, E4]
      criterios: [C3, C4, C5]
      tipo_encaminhamento: Recomendação
      encaminhamento: institua formalmente Comitê de TIC ou instância equivalente, compatível com o porte e a estrutura decisória da organização, atentando-se, minimamente, em definir sua composição, competências, periodicidade de reuniões, forma de registro das deliberações e acompanhamento dos encaminhamentos
    - S2.3:
      descricao: Comitê de TIC ou instância equivalente sem evidências suficientes de atuação efetiva.
      severidade: media
      itens_questionario: [q1001ext[E], q1001ext[F], q1001evi]
      regra_de_identificacao:
      - (q1001ext[E] == Sim) & (q1001ext[F] != Sim)
      referencias_matriz: [R2.3, P5, E5, P6, E6]
      criterios: [C2, C3, C4]
      tipo_encaminhamento: Recomendação
      encaminhamento: assegure o funcionamento efetivo do Comitê de TIC ou instância equivalente, compatível com o porte e a estrutura decisória da organização, atentando-se, minimamente, em realizar reuniões periódicas, registrar deliberações e acompanhar decisões sobre prioridades, projetos, riscos, serviços, orçamento e contratações de TIC

## Questão 03 - Planejamento de TIC

questao: Q3. A organização utiliza o planejamento de TIC como instrumento efetivo de gestão, com processo formal, plano vigente, aprovação competente, alinhamento institucional, integração com orçamento e contratações e acompanhamento periódico?

subquestoes:
- A organização executa processo formal de planejamento de TIC?
- As áreas demandantes participam do processo de planejamento de TIC?
- O plano de TIC foi formalmente aprovado pela instância competente?
- O plano de TIC está alinhado ao planejamento institucional?
- O plano de TIC está integrado à proposta orçamentária da área de TIC e ao plano de contratações?
- O plano de TIC é acompanhado, revisto e atualizado periodicamente ou diante de mudanças relevantes?

riscos:
- R3.1: Devido à inexistência ou fragilidade do processo formal de planejamento de TIC, poderá haver atuação reativa, sem critérios objetivos de seleção e priorização de iniciativas.
- R3.2: Devido à ausência de aprovação formal do plano de TIC pela instância competente, o instrumento poderá não possuir legitimidade institucional para orientar a gestão, os projetos, o orçamento e as contratações de TIC.
- R3.4: Devido à falta de alinhamento do plano de TIC ao planejamento institucional, poderão ser executadas ações de TIC com baixo valor para a organização.
- R3.5: Devido à ausência de integração entre planejamento de TIC, orçamento e contratações, poderão ocorrer aquisições reativas, não priorizadas ou desalinhadas.
- R3.6: Devido à ausência de acompanhamento e revisão do plano de TIC, poderão permanecer metas, iniciativas e prioridades incompatíveis com mudanças institucionais, orçamentárias ou tecnológicas.

fontes_de_informacao:
- F1: Respostas ao questionário eletrônico iGovTI.
- F2: Evidências anexadas no questionário eletrônico.

informacoes_requeridas:
- IR1: Resposta sobre existência de processo formal de planejamento de TIC; [F1, q2101]
- IR2: Evidência anexada sobre norma, procedimento, guia ou instrumento equivalente que discipline o processo de planejamento de TIC; [F2, q2101evi]
- IR3: Resposta sobre participação das áreas demandantes no processo de planejamento de TIC; [F1, q2101ext[A]]
- IR4: Resposta sobre aprovação formal do plano de TIC pela instância competente; [F1, q2102ext[A]]
- IR5: Evidência anexada do ato de aprovação formal do plano de TIC; [F2, q2102evi]
- IR7: Resposta e evidência sobre alinhamento do plano de TIC ao planejamento institucional; [F1, F2, q2102, q2102evi]
- IR8: Resposta e evidência sobre integração do plano de TIC com orçamento, plano de contratações, projetos ou contratações de TIC; [F1, F2, q2102, q2802, q2804[B]]
- IR9: Resposta e evidência sobre acompanhamento, revisão ou atualização do plano de TIC; [F1, F2, q2102, q2102evi]

criterios:
- C1: COBIT 2019, APO02.05 - Definir o plano e o roteiro estratégico: estabelecer plano e roteiro de TIC que traduzam a estratégia em iniciativas, prioridades, recursos, dependências, prazos e benefícios esperados.
- C2: COBIT 2019, APO06.03 - Criar e manter orçamentos: elaborar e manter orçamento de TIC alinhado ao portfólio, ao planejamento e às prioridades aprovadas.
- C3: Acórdão 1.411/2014-TCU-Plenário, item 9.1.6 e subitens 9.1.6.1 a 9.1.6.4: necessidade de instituir formalmente plano diretor de TI, contemplando desdobramento de diretrizes estratégicas, vinculação das ações de TI a indicadores e metas de negócio, vinculação das ações de TI a indicadores e metas de serviços ao cidadão e vinculação das ações priorizadas ao orçamento de TI.
- C4: Acórdão TCE-RJ 44.490/2024-PLEN, item II.3 e subitens II.3.1 a II.3.5: necessidade de estabelecer processo estruturado, com participação de representantes das principais secretarias, para elaborar, manter e revisar periodicamente o PDTI, contemplando objetivos, indicadores e metas de TI alinhados aos objetivos de negócio, riscos que possam impactar objetivos e metas, projetos, aquisições e ações necessárias, alocação de recursos e ações de divulgação e monitoramento do PDTI após aprovação pela autoridade máxima.

procedimentos:
- P1: Verificar, por meio da resposta à q2101, se a organização executa processo formal de planejamento de TIC; [IR1]
- P2: Validar, pelas evidências anexadas à q2101, a formalização mínima do processo de planejamento de TIC; [IR2]
- P3: Verificar, por meio da q2101ext[A], se há participação das áreas demandantes no processo de planejamento de TIC; [IR3]
- P4: Verificar, por meio da resposta à q2102ext[A], se o plano de TIC foi aprovado pelo dirigente máximo da organização ou por dirigente ou colegiado integrante da alta administração; [IR4]
- P5: Validar, pelas evidências anexadas à q2102, a aprovação formal do plano de TIC pela instância competente; [IR5]
- P7: Verificar, por meio da resposta e das evidências da q2102, se o plano está alinhado ao planejamento institucional; [IR7]
- P8: Verificar, por meio das respostas e evidências das q2102, q2802 e q2804[B], se o plano de TIC se integra a orçamento, plano de contratações, projetos ou contratações; [IR8]
- P9: Verificar, por meio da resposta e das evidências da q2102, se há acompanhamento, revisão ou atualização periódica do plano de TIC; [IR9]

evidencias:
- E1: Resposta negativa ou insuficiente sobre a existência de processo de planejamento de TIC; [P1]
- E2: Ausência, desatualização, incompatibilidade ou insuficiência de evidência que discipline o processo de planejamento de TIC; [P2]
- E3: Resposta negativa ou insuficiente sobre participação das áreas demandantes; [P3]
- E4: Resposta negativa ou insuficiente sobre a aprovação formal do plano de TIC pela instância competente; [P4]
- E5: Ausência ou insuficiência de evidência do ato de aprovação formal do plano de TIC pela instância competente; [P5]
- E7: Inexistência ou insuficiência de alinhamento entre plano de TIC e planejamento institucional; [P7]
- E8: Inexistência ou insuficiência de vínculo entre plano de TIC, orçamento, plano de contratações, projetos ou contratações de TIC; [P8]
- E9: Ausência de registros de acompanhamento, revisão ou atualização do plano de TIC; [P9]

possiveis_achados:
- A3: Planejamento de TIC insuficiente para orientar a gestão, o orçamento e as contratações de TIC
  situacoes_encontradas:
  - S3.1:
      descricao: Inexistência ou fragilidade do processo formal de planejamento de TIC.
      severidade: alta
      itens_questionario: [q2101ext[A], q2101ext[B], q2101ext[C], q2101ext[D], q2101evi]
      regra_de_identificacao:
      - (q2101ext[A] != Sim) | (q2101ext[B] != Sim) | (q2101ext[C] != Sim) | (q2101ext[D] != Sim)
      referencias_matriz: [R3.1, P1, E1, P2, E2, P3, E3]
      criterios: [C1, C3, C4]
      tipo_encaminhamento: Recomendação
      encaminhamento: institua processo formal de planejamento de TIC, compatível com o porte e a maturidade da organização, atentando-se, minimamente, em definir etapas, responsáveis, participação das áreas demandantes e critérios de priorização das necessidades e iniciativas de TIC
  - S3.2:
      descricao: Ausência de aprovação formal do plano de TIC.
      severidade: alta
      itens_questionario: [q2102ext[A], q2102evi]
      regra_de_identificacao:
      - (q2102ext[A] != Sim)
      referencias_matriz: [R3.2, P4, E4, P5, E5]
      criterios: [C1, C3, C4]
      tipo_encaminhamento: Recomendação
      encaminhamento: submeta o plano de TIC à aprovação formal do dirigente máximo ou de dirigente ou colegiado integrante da alta administração, mantendo registro do respectivo ato de aprovação
  - S3.4:
      descricao: Plano de TIC sem alinhamento adequado ao planejamento institucional.
      severidade: media
      itens_questionario: [q2102ext[D], q2102evi]
      regra_de_identificacao:
      - (q2102ext[D] != Sim)
      referencias_matriz: [R3.4, P7, E7]
      criterios: [C1, C3, C4]
      tipo_encaminhamento: Recomendação
      encaminhamento: revise o plano de TIC para explicitar seu alinhamento ao planejamento institucional, às diretrizes superiores e às necessidades das áreas finalísticas e administrativas, relacionando objetivos, iniciativas, indicadores e metas de TIC aos resultados institucionais pretendidos
  - S3.5:
      descricao: Plano de TIC sem vínculo demonstrado com orçamento e contratações de TIC
      severidade: alta
      itens_questionario: [q2102ext[C], q2802ext[C], q2802ext[D], q2804[B], q2102evi, q2802evi]
      regra_de_identificacao:
      - (q2102ext[C] != Sim) | (q2802ext[C] != Sim) | (q2802ext[D] != Sim) | (q2804[B] != Sim)
      referencias_matriz: [R3.5, P8, E8]
      criterios: [C2, C3, C4]
      tipo_encaminhamento: Recomendação
      encaminhamento: integre o plano de TIC à proposta orçamentária, ao plano de contratações e às contratações de TIC, atentando-se, minimamente, em priorizar as demandas conforme sua relevância, seus riscos e a capacidade de execução da organização
  - S3.6:
      descricao: Ausência de acompanhamento, revisão ou atualização periódica do plano de TIC.
      severidade: media
      itens_questionario: [q2102ext[E], q2102evi]
      regra_de_identificacao:
      - (q2102ext[E] != Sim)
      referencias_matriz: [R3.6, P9, E9]
      criterios: [C1, C3, C4]
      tipo_encaminhamento: Recomendação
      encaminhamento: estabeleça e execute rotina periódica de acompanhamento, revisão e atualização do plano de TIC, atentando-se, minimamente, em registrar a execução das iniciativas, as pendências, as reprogramações e as deliberações adotadas

---

## Questão 04 - Capacidade Institucional de TIC e Segurança da Informação

questao: Q4. A organização dispõe de capacidade institucional mínima, em termos de força de trabalho, perfis profissionais, competências, funções e vínculos, para planejar, gerir, proteger, contratar, fiscalizar e sustentar a TIC e a segurança da informação de forma adequada às suas necessidades institucionais?

subquestoes:
- A organização conhece o quantitativo de profissionais que atuam regularmente em TIC e segurança da informação, por área e tipo de vínculo?
- A organização definiu o quantitativo necessário de pessoal de TIC e segurança da informação?
- A organização possui cargos, funções, perfis ou ocupações específicas de TIC e segurança da informação?
- A organização definiu perfis profissionais esperados para gestores e colaboradores de TIC e segurança da informação?
- A organização identifica e trata lacunas de competências dos colaboradores e gestores de TIC e segurança da informação?
- A dependência de terceiros é compatível com a capacidade interna de coordenação, fiscalização e retenção de conhecimento?


riscos:
- R4.1: Devido à ausência de informações estruturadas sobre a força de trabalho de TIC e segurança da informação, poderá não haver base mínima para dimensionamento, alocação e planejamento da capacidade institucional.
- R4.2: Devido à ausência de definição do quantitativo necessário de pessoal de TIC e segurança da informação, poderá haver subdimensionamento ou alocação inadequada da equipe.
- R4.3: Devido à inexistência de cargos, funções, perfis ou ocupações específicas de TIC e segurança da informação, poderá haver baixa capacidade de atração, alocação, responsabilização e retenção de profissionais.
- R4.4: Devido à ausência de perfis profissionais definidos para gestores e colaboradores de TIC e segurança da informação, poderá haver designação de pessoas sem competências compatíveis com as responsabilidades exercidas.
- R4.5: Devido à ausência de identificação e tratamento de lacunas de competências, poderá haver incapacidade de executar práticas mínimas de planejamento, gestão, segurança, contratação, fiscalização e sustentação de TIC.
- R4.6: Devido à dependência excessiva de terceiros para atividades críticas de TIC, sem capacidade interna suficiente de coordenação e fiscalização, poderá haver perda de conhecimento, baixa governabilidade e risco de descontinuidade dos serviços.

fontes_de_informacao:
- F1: Respostas ao questionário eletrônico iGovTI.
- F2: Evidências anexadas no questionário eletrônico.

informacoes_requeridas:
- IR1: Resposta sobre quantitativo de profissionais que atuam em TIC e segurança da informação, por área e tipo de vínculo; [F1, q0105]
- IR2: Resposta e evidência sobre definição do quantitativo necessário de pessoal de TIC e segurança da informação; [F1, F2, q2703, q2703evi]
- IR3: Resposta sobre existência de cargos específicos em TIC e segurança da informação; [F1, q2708]
- IR4: Resposta e evidência sobre perfis profissionais desejados para gestores de TIC e segurança da informação; [F1, F2, q2701, q2701evi]
- IR5: Resposta e evidência sobre perfis profissionais desejados para colaboradores de TIC e segurança da informação; [F1, F2, q2702, q2702evi]
- IR6: Resposta e evidência sobre escolha dos gestores de TIC e segurança da informação segundo perfis previamente definidos; [F1, F2, q2704, q2704evi]
- IR7: Resposta e evidência sobre identificação de lacunas de competências; [F1, F2, q2705, q2705evi]
- IR8: Resposta e evidência sobre tratamento das lacunas de competências; [F1, F2, q2706, q2706evi]
- IR9: Respostas e evidências que permitam avaliar dependência de terceiros e capacidade interna de coordenação e fiscalização; [F1, F2, q0101, q0105, q2703, q2801, q2804]

criterios:
- C1: COBIT 2019, APO01.05 - Estabelecer papéis e responsabilidades: definir, comunicar e manter papéis e responsabilidades relacionados à governança e gestão de TIC.
- C2: COBIT 2019, APO07.01 - Adquirir e manter pessoal adequado e apropriado: assegurar quantidade e perfil de profissionais compatíveis com as necessidades de TIC.
- C3: COBIT 2019, APO07.02 - Identificar pessoal-chave de TI: identificar funções e pessoas críticas para reduzir dependência individual, perda de conhecimento e descontinuidade.
- C4: COBIT 2019, APO07.03 - Manter habilidades e competências do pessoal: identificar, desenvolver e manter competências necessárias à execução das responsabilidades de TIC.
- C5: COBIT 2019, APO07.05 - Planejar e monitorar o uso de recursos humanos de TI e de negócio: planejar, alocar e acompanhar capacidade de pessoal para iniciativas, operações e serviços de TIC.
- C6: COBIT 2019, APO07.06 - Gerenciar pessoal contratado: controlar o uso de pessoal terceirizado ou externo, preservando responsabilização, supervisão e retenção de conhecimento.
- C7: COBIT 2019, APO10.04 - Gerenciar risco de fornecedores: identificar e tratar riscos decorrentes de fornecedores, contratos e dependências externas relevantes para TIC.
- C8: COBIT 2019, DSS01.02 - Gerenciar serviços de TI terceirizados: assegurar que serviços terceirizados sejam supervisionados, medidos e integrados aos controles da organização.
- C9: ABNT NBR ISO/IEC 27001:2022, cláusulas 5.3 e 7.2: definir responsabilidades e autoridades para segurança da informação e assegurar competências necessárias às funções atribuídas.
- C10: ABNT NBR ISO/IEC 27002:2022, controles 5.2 e 6.3: definir papéis e responsabilidades de segurança da informação e promover conscientização, educação e treinamento em segurança.

procedimentos:
- P1: Verificar, por meio da q0105, o quantitativo informado de profissionais que atuam em TIC e segurança da informação, por área e tipo de vínculo; [IR1]
- P2: Verificar, por meio da q2703 e respectiva evidência, se há definição do quantitativo necessário de pessoal de TIC e segurança da informação; [IR2]
- P3: Verificar, por meio da q2708, se há cargos específicos em TIC e segurança da informação; [IR3]
- P4: Verificar, por meio das q2701 e q2702 e respectivas evidências, se há perfis profissionais definidos para gestores e colaboradores de TIC e segurança da informação; [IR4, IR5]
- P5: Verificar, por meio da q2704 e respectiva evidência, se a escolha dos gestores de TIC e segurança da informação ocorre segundo perfis previamente definidos; [IR6]
- P6: Verificar, por meio das q2705 e q2706 e respectivas evidências, se lacunas de competências são identificadas e tratadas; [IR7, IR8]
- P7: Verificar, por cruzamento das respostas e evidências das q0101, q0105, q2703, q2801 e q2804, se há dependência excessiva de terceiros para atividades críticas sem capacidade interna suficiente de coordenação e fiscalização; [IR9]

evidencias:
- E1: Quantitativo declarado igual a zero para profissionais de TIC ou segurança da informação, ou incompatível com a estrutura de TIC declarada pela organização; [P1]
- E2: Resposta negativa ou insuficiente sobre definição do quantitativo necessário de pessoal de TIC e segurança da informação, ou evidência inexistente/incompatível/insuficiente; [P2]
- E3: Resposta negativa sobre existência de cargos específicos em TIC e segurança da informação; [P3]
- E4: Resposta negativa ou insuficiente sobre perfis profissionais definidos para gestores ou colaboradores de TIC e segurança da informação, ou evidência inexistente/incompatível/insuficiente; [P4]
- E5: Resposta negativa ou insuficiente sobre escolha de gestores segundo perfis profissionais definidos, ou evidência inexistente/incompatível/insuficiente; [P5]
- E6: Resposta negativa ou insuficiente sobre identificação ou tratamento de lacunas de competências, ou evidência inexistente/incompatível/insuficiente; [P6]
- E7: Evidência, a partir das respostas e anexos do questionário, de dependência excessiva de terceiros em atividades críticas sem capacidade interna suficiente de coordenação, fiscalização ou retenção de conhecimento; [P7]

possiveis_achados:
- A4: Capacidade institucional insuficiente para sustentar a gestão de TIC e segurança da informação
  situacoes_encontradas:
  - S4.1:
    descricao: Ausência de força de trabalho dedicada à TIC ou à segurança da informação.
    severidade: alta
    itens_questionario:
      - [q0105[TI_efetivos], q0105[TI_comissionados], q0105[TI_terceirizados], q0105[TI_cedidos], q0105[TI_temporarios], q0105[TI_estagiarios], q0105[SI_efetivos], q0105[SI_comissionados], q0105[SI_terceirizados], q0105[SI_cedidos], q0105[SI_temporarios], q0105[SI_estagiarios]]
    regra_de_identificacao:
      - total_TI = q0105[TI_efetivos] + q0105[TI_comissionados] + q0105[TI_terceirizados] + q0105[TI_cedidos] + q0105[TI_temporarios] + q0105[TI_estagiarios]
      - total_SI = q0105[SI_efetivos] + q0105[SI_comissionados] + q0105[SI_terceirizados] + q0105[SI_cedidos] + q0105[SI_temporarios] + q0105[SI_estagiarios]
      - (total_TI == 0) | (total_SI == 0)
      referencias_matriz: [R4.1, P1, E1]
      criterios: [C2, C5, C9]
    tipo_encaminhamento: Recomendação
    encaminhamento: avalie a força de trabalho dedicada à TIC e à segurança da informação e adote medidas proporcionais para assegurar capacidade mínima de planejamento, gestão, proteção, contratação, fiscalização e sustentação dos serviços e ativos de TIC
  - S4.2:
      descricao: A organização não definiu o quantitativo necessário de pessoal de TIC e segurança da informação.
      severidade: alta
      itens_questionario: [q2703ext[C], q2703evi]
      regra_de_identificacao:
      - (q2703ext[C] != Sim)
      referencias_matriz: [R4.2, P2, E2]
      criterios: [C2, C5, C9]
      tipo_encaminhamento: Recomendação
      encaminhamento: estime e mantenha atualizado o quantitativo necessário de pessoal de TIC e segurança da informação, considerando o porte e a complexidade da organização, os serviços críticos, os sistemas mantidos, as contratações vigentes e os riscos relevantes
  - S4.3:
      descricao: Ausência de cargos, funções, perfis ou ocupações específicas de TIC e segurança da informação.
      severidade: media
      itens_questionario: [q2708[B], q2708[D]]
      regra_de_identificacao:
      - (q2708[B] != Sim) | (q2708[D] != Sim)
      referencias_matriz: [R4.3, P3, E3]
      criterios: [C1, C2, C3]
      tipo_encaminhamento: Recomendação
      encaminhamento: avalie a necessidade de instituir cargos, funções, gratificações, perfis ou ocupações específicas de TIC e segurança da informação e adote a solução compatível com as necessidades institucionais e a capacidade administrativa da organização
  - S4.4:
      descricao: Perfis profissionais de TIC e segurança da informação inexistentes, insuficientes ou não utilizados na escolha de gestores.
      severidade: media
      itens_questionario: [q2701ext[A], q2702ext[A], q2704ext[B], q2701evi, q2702evi, q2704evi]
      regra_de_identificacao:
      - (q2701ext[A] != Sim) | (q2702ext[A] != Sim) | (q2704ext[B] != Sim)
      referencias_matriz: [R4.4, P4, E4, P5, E5]
      criterios: [C1, C4, C9]
      tipo_encaminhamento: Recomendação
      encaminhamento: defina perfis profissionais mínimos para gestores e colaboradores de TIC e segurança da informação, atentando-se, minimamente, em estabelecer conhecimentos, habilidades, experiência e responsabilidades requeridos e utilizar esses perfis na seleção e designação dos responsáveis
  - S4.5:
      descricao: Lacunas de competências dos colaboradores e gestores de TIC e segurança da informação não são identificadas ou tratadas.
      severidade: media
      itens_questionario: [q2705ext[B], q2705ext[C], q2705ext[D], q2706ext[A], q2705evi, q2706evi]
      regra_de_identificacao:
      - (q2705ext[B] != Sim) | (q2705ext[C] != Sim) | (q2705ext[D] != Sim) | (q2706ext[A] != Sim)
      referencias_matriz: [R4.5, P6, E6]
      criterios: [C4, C9, C10]
      tipo_encaminhamento: Recomendação
      encaminhamento: realize diagnóstico periódico das lacunas de competências dos gestores e colaboradores de TIC e segurança da informação e estabeleça plano de tratamento, contemplando, conforme a necessidade, capacitação, realocação, provimento, apoio especializado, compartilhamento de estrutura ou contratação com transferência de conhecimento
  - S4.6:
    descricao: Dependência externa relevante sem capacidade interna suficiente para coordenar e fiscalizar a TIC.
    severidade: alta
    itens_questionario: [q0101, q0105[TI_efetivos], q0105[TI_comissionados], q0105[TI_cedidos], q0105[TI_temporarios], q0105[TI_terceirizados]]
    regra_de_identificacao:
      - total_TI_interno = q0105[TI_efetivos] + q0105[TI_comissionados] + q0105[TI_cedidos] + q0105[TI_temporarios]
      - total_TI_terceiros = q0105[TI_terceirizados]
      - predominio_terceiros = total_TI_terceiros > total_TI_interno
      - (((q0101 == B) | (q0101 == C)) & (total_TI_interno == 0)) | (predominio_terceiros == True)
    referencias_matriz: [R4.6, P7, E7]
    criterios: [C6, C7, C8]
    tipo_encaminhamento: Recomendação
    encaminhamento: avalie o modelo de operação de TIC e adote medidas proporcionais para assegurar capacidade interna suficiente de coordenação, planejamento, aprovação técnica, fiscalização contratual e retenção de conhecimento, especialmente quando a execução das atividades de TIC depender predominantemente de terceiros ou de estrutura externa
---

## Questão 05 - Gestão de Serviços de TIC

questao: Q5. A organização adota práticas mínimas de gestão de serviços de TIC, incluindo catálogo de serviços, níveis de serviço, inventário de ativos, gestão de configuração e tratamento de incidentes, de modo a assegurar eficiência, continuidade, rastreabilidade e qualidade dos serviços prestados?

subquestoes:
- A organização possui catálogo de serviços de TIC formalmente instituído, atualizado e acessível aos usuários e às áreas demandantes?
- O catálogo de serviços de TIC contém informações mínimas sobre os serviços efetivamente prestados?
- Existem Acordos de Níveis de Serviço ou metas mínimas formalmente definidas e monitoradas para os principais serviços de TIC?
- A organização mantém inventário atualizado dos ativos de TIC?
- Há processo formal de gestão de configuração, com identificação de itens de configuração relevantes para os serviços de TIC?
- A organização possui processo formal de gestão de incidentes de TIC?
- Os incidentes de TIC são registrados de forma sistemática, com rastreabilidade e histórico?

riscos:
- R5.1: Devido à inexistência ou desatualização do catálogo de serviços de TIC, poderá não haver definição clara e padronizada dos serviços prestados, levando à prestação reativa e pouco transparente de serviços de TIC.
- R5.2: Devido à inexistência de níveis de serviço formalmente definidos ou monitorados, poderá não haver parâmetros objetivos de desempenho e qualidade dos serviços de TIC.
- R5.3: Devido à inexistência ou fragilidade do inventário de ativos e da gestão de configuração, poderá não haver controle adequado dos recursos tecnológicos e suas relações com os serviços prestados.
- R5.4: Devido à inexistência ou fragilidade do processo de gestão de incidentes de TIC, poderá não haver tratamento padronizado, tempestivo e rastreável dos incidentes.

fontes_de_informacao:
- F1: Respostas ao questionário eletrônico iGovTI.
- F2: Evidências anexadas no questionário eletrônico.

informacoes_requeridas:
- IR1: Resposta sobre existência, atualização e disponibilidade do catálogo de serviços de TIC; [F1, q2201]
- IR2: Evidência anexada contendo catálogo de serviços de TIC; [F2, q2201evi]
- IR3: Resposta sobre existência de ANS ou metas mínimas de nível de serviço; [F1, q2201ext[D]]
- IR4: Resposta sobre monitoramento de ANS ou metas mínimas; [F1, q2201ext[E]]
- IR5: Evidência anexada contendo ANS, metas ou registros de monitoramento; [F2, q2201evi]
- IR6: Resposta sobre existência de inventário de ativos de TIC; [F1, q2203, q2501, q2504]
- IR7: Evidência anexada contendo inventário de ativos de TIC; [F2, q2203evi, q2501evi, q2504evi]
- IR8: Resposta sobre existência de processo formal de gestão de configuração; [F1, q2203]
- IR9: Evidência anexada contendo norma, procedimento, CMDB ou base equivalente de gestão de configuração; [F2, q2203evi]
- IR10: Resposta sobre existência de processo formal de gestão de incidentes de TIC; [F1, q2204]
- IR11: Evidência anexada contendo norma, procedimento ou fluxo de gestão de incidentes de TIC; [F2, q2204evi]
- IR12: Resposta sobre registro sistemático dos incidentes de TIC; [F1, q2204]
- IR13: Evidência anexada contendo registros de incidentes, chamados, tickets, relatórios de atendimento ou sistema equivalente; [F2, q2204evi]

criterios:
- C1: ITIL 4, prática de gerenciamento do catálogo de serviços: manter fonte única de informações consistentes sobre serviços e ofertas de serviço, disponível para usuários e equipes de suporte.
- C2: COBIT 2019, APO09.02 - Catalogar serviços facilitados por TI: definir, manter e comunicar catálogo de serviços, incluindo serviços prestados, características, requisitos e níveis de serviço esperados.
- C3: ITIL 4, prática de gerenciamento de nível de serviço: definir, acordar, monitorar, avaliar e reportar metas e níveis de serviço alinhados às necessidades das áreas usuárias.
- C4: ITIL 4, prática de gerenciamento de ativos de TI: planejar e gerenciar o ciclo de vida dos ativos de TI, mantendo informações suficientes para apoiar controle, custo, risco, valor e tomada de decisão.
- C5: ITIL 4, prática de gerenciamento de configuração de serviço: assegurar informações precisas e confiáveis sobre itens de configuração e seus relacionamentos com serviços, sistemas e infraestrutura.
- C6: COBIT 2019, BAI10.01 - Estabelecer e manter um modelo de configuração: definir escopo, granularidade, atributos, relacionamentos e responsáveis pela base de configuração.
- C7: ITIL 4, prática de gerenciamento de incidentes: minimizar o impacto negativo dos incidentes por meio da restauração tempestiva da operação normal dos serviços e do registro rastreável do tratamento realizado.
- C8: COBIT 2019, DSS02.02, DSS02.04 e DSS02.07 - Requisições de serviço e incidentes gerenciados: registrar, classificar, priorizar, investigar, diagnosticar, resolver, acompanhar e reportar incidentes e requisições de serviço.

procedimentos:
- P1: Verificar, por meio da resposta à q2201, a existência, atualização e disponibilidade do catálogo de serviços de TIC; [IR1]
- P2: Validar, pela evidência anexada à q2201, se o catálogo contém informações mínimas sobre os serviços prestados; [IR2]
- P3: Verificar, por meio da q2201ext[D] e da q2201ext[E], a existência e monitoramento de ANS ou metas mínimas de nível de serviço; [IR3, IR4]
- P4: Validar, pela evidência anexada à q2201, a existência de ANS, metas ou registros de monitoramento; [IR5]
- P5: Verificar, por meio das respostas às q2203, q2501 e q2504, a existência de inventário de ativos de TIC; [IR6]
- P6: Validar, pelas evidências anexadas às q2203, q2501 e q2504, a existência e suficiência do inventário de ativos de TIC; [IR7]
- P7: Verificar, por meio da resposta à q2203, a existência de processo formal de gestão de configuração; [IR8]
- P8: Validar, pela evidência anexada à q2203, a existência de procedimento, base ou mecanismo equivalente de gestão de configuração; [IR9]
- P9: Verificar, por meio da resposta à q2204, a existência de processo formal de gestão de incidentes de TIC; [IR10]
- P10: Validar, pela evidência anexada à q2204, a existência de procedimento ou fluxo formal de gestão de incidentes; [IR11]
- P11: Verificar, por meio da resposta à q2204, se há registro sistemático dos incidentes de TIC; [IR12]
- P12: Validar, pela evidência anexada à q2204, a existência de registros rastreáveis de incidentes, chamados ou tickets; [IR13]

evidencias:
- E1: Resposta negativa ou insuficiente sobre catálogo de serviços de TIC; [P1]
- E2: Ausência, desatualização, inacessibilidade ou insuficiência do catálogo de serviços de TIC; [P2]
- E3: Resposta negativa ou insuficiente sobre ANS ou metas mínimas de nível de serviço; [P3]
- E4: Ausência, desatualização ou insuficiência de ANS, metas ou registros de monitoramento; [P4]
- E5: Resposta negativa ou insuficiente sobre inventário de ativos de TIC; [P5]
- E6: Ausência, desatualização ou insuficiência de inventário de ativos de TIC; [P6]
- E7: Resposta negativa ou insuficiente sobre processo formal de gestão de configuração; [P7]
- E8: Ausência, desatualização ou insuficiência de norma, procedimento, CMDB ou base equivalente de gestão de configuração; [P8]
- E9: Resposta negativa ou insuficiente sobre processo formal de gestão de incidentes de TIC; [P9]
- E10: Ausência, desatualização ou insuficiência de norma, procedimento ou fluxo formal de gestão de incidentes; [P10]
- E11: Resposta negativa ou insuficiente sobre registro sistemático de incidentes de TIC; [P11]
- E12: Ausência, insuficiência ou baixa rastreabilidade dos registros de incidentes, chamados ou tickets; [P12]

possiveis_achados:
- A5: Gestão de serviços de TIC insuficiente para assegurar controle sobre serviços, ativos e incidentes
  situacoes_encontradas:
  - S5.1:
      descricao: Inexistência ou insuficiência do catálogo de serviços de TIC.
      severidade: media
      itens_questionario: [q2201, q2201ext[A], q2201ext[B], q2201ext[C], q2201evi]
      regra_de_identificacao:
      - (q2201ext[A] != Sim) | (q2201ext[B] != Sim) | (q2201ext[C] != Sim)
      referencias_matriz: [R5.1, P1, E1, P2, E2]
      criterios: [C1, C2]
      tipo_encaminhamento: Recomendação
      encaminhamento: institua e mantenha atualizado catálogo de serviços de TIC, atentando-se, minimamente, em identificar os serviços efetivamente prestados, seus responsáveis, usuários, condições de acesso e informações necessárias ao atendimento das áreas demandantes
  - S5.2:
      descricao: Ausência ou fragilidade na definição e no monitoramento de níveis mínimos de serviço de TIC.
      severidade: media
      itens_questionario: [q2201ext[D], q2201ext[E], q2201evi]
      regra_de_identificacao:
      - (q2201ext[D] != Sim) | (q2201ext[E] != Sim)
      referencias_matriz: [R5.2, P3, E3, P4, E4]
      criterios: [C2, C3]
      tipo_encaminhamento: Recomendação
      encaminhamento: defina, pactue e monitore níveis mínimos de serviço ou metas de atendimento para os serviços de TIC mais relevantes, estabelecendo indicadores, responsáveis, periodicidade de medição e forma de comunicação dos resultados
  - S5.3:
      descricao: Inexistência ou fragilidade do inventário de ativos de TIC.
      severidade: alta
      itens_questionario: [q2203ext[A], q2504ext[A], q2504ext[B], q2203evi, q2504evi]
      regra_de_identificacao:
      - (q2203ext[A] != Sim) | (q2504ext[A] != Sim) | (q2504ext[B] != Sim)
      referencias_matriz: [R5.3, P5, E5, P6, E6]
      criterios: [C4, C5]
      tipo_encaminhamento: Recomendação
      encaminhamento: estabeleça e mantenha atualizado inventário de ativos de TIC, atentando-se, minimamente, em registrar equipamentos, servidores, sistemas, softwares, licenças, serviços em nuvem, componentes de infraestrutura, responsáveis e informações necessárias ao controle do ciclo de vida dos ativos
  - S5.4:
      descricao: Ausência ou fragilidade do processo de gestão de configuração.
      severidade: media
      itens_questionario: [q2203ext[A], q2203ext[C], q2203evi]
      regra_de_identificacao:
      - (q2203ext[A] != Sim) | (q2203ext[C] != Sim)
      referencias_matriz: [R5.3, P7, E7, P8, E8]
      criterios: [C5, C6]
      tipo_encaminhamento: Recomendação
      encaminhamento: formalize e execute processo de gestão de configuração, atentando-se, minimamente, em manter base, ferramenta ou registro equivalente com os itens de configuração relevantes, seus responsáveis e os relacionamentos entre ativos, sistemas, infraestrutura e serviços, com atualização periódica e uso das informações no planejamento e acompanhamento de mudanças
  - S5.5:
      descricao: Inexistência ou fragilidade do processo de gestão de incidentes de TIC.
      severidade: alta
      itens_questionario: [q2204ext[A], q2204ext[D], q2204ext[E], q2204evi]
      regra_de_identificacao:
      - (q2204ext[A] != Sim) | (q2204ext[D] != Sim) | (q2204ext[E] != Sim)
      referencias_matriz: [R5.4, P9, E9, P10, E10, P11, E11, P12, E12]
      criterios: [C7, C8]
      tipo_encaminhamento: Recomendação
      encaminhamento: formalize e execute processo de gestão de incidentes de TIC, atentando-se, minimamente, em definir papéis, responsabilidades, critérios de priorização e escalamento, tratamento de incidentes de serviços e de segurança da informação, registro sistemático e rastreável das ocorrências e análise posterior dos incidentes relevantes ou recorrentes

---

## Questão 06 - Contratações de TIC

questao: Q6. A organização adota processo formal e padronizado para planejamento, contratação, fiscalização e gestão de soluções de TIC, com participação técnica da área de TIC e alinhamento ao planejamento?

subquestoes:
- A organização possui fluxo formalizado e padronizado para contratações de TIC?
- A organização definiu papéis e responsabilidades nas contratações de TIC?
- A organização dispõe de modelos, manuais, checklists ou normativos orientativos para elaboração dos artefatos das contratações de TIC?
- As contratações de TIC são submetidas à análise prévia e aprovação técnica da área de TIC?
- As contratações de TIC estão alinhadas ao plano de TIC e ao plano de contratações?
- A equipe de planejamento da contratação é formalmente designada e possui participação técnica de TIC?

riscos:
- R6.1: Devido à inexistência ou fragilidade de fluxo formal e padronizado para contratações de TIC, poderá não haver clareza quanto às etapas, instâncias decisórias e critérios de aprovação.
- R6.2: Devido à ausência de definição formal de papéis, responsabilidades, modelos e orientações, poderá haver instrução processual incompleta, inconsistente ou tecnicamente frágil.
- R6.3: Devido à ausência de análise técnica prévia da área de TIC e de alinhamento ao planejamento, poderão ser contratadas soluções incompatíveis com padrões técnicos, requisitos institucionais ou prioridades definidas.
- R6.4: Devido à ausência de equipe de planejamento formalmente designada e de participação técnica da área de TIC, a instrução da contratação poderá não considerar adequadamente as necessidades institucionais e os aspectos técnicos da solução.

fontes_de_informacao:
- F1: Respostas ao questionário eletrônico iGovTI.
- F2: Evidências anexadas no questionário eletrônico.

informacoes_requeridas:
- IR1: Resposta e evidência sobre processos de trabalho relativos às contratações de TIC; [F1, F2, q2801, q2801evi]
- IR2: Resposta e evidência sobre papéis e responsabilidades nas contratações de TIC; [F1, F2, q2801, q2801evi]
- IR3: Resposta e evidência sobre modelos, manuais, checklists ou normativos orientativos para contratações de TIC; [F1, F2, q2801, q2801evi]
- IR4: Resposta sobre submissão obrigatória das contratações de TIC à análise prévia e aprovação técnica da área de TIC; [F1, q2804[A]]
- IR5: Evidência específica sobre aprovação técnica da área de TIC em caso concreto; [F2, q2804eviA]
- IR6: Resposta e evidência sobre aderência das contratações ao plano de TIC, ao plano de contratações e à proposta orçamentária; [F1, F2, q2102ext[C], q2802ext[C], q2802ext[D], q2804[B], q2102evi, q2802evi]
- IR7: Resposta e evidência sobre equipe de planejamento formalmente designada e multidisciplinar; [F1, F2, q2804[C], q2801evi]

criterios:
- C1: Art. 11, parágrafo único, da Lei 14.133/2021: responsabilidade da alta administração pela governança das contratações, com processos, estruturas, gestão de riscos e controles internos.
- C2: Art. 18, caput e §1º, incisos I, IV, V, VIII, IX, X e XIII, da Lei 14.133/2021: fase preparatória caracterizada pelo planejamento, compatibilização com o plano de contratações anual e elementos mínimos do estudo técnico preliminar.
- C3: Art. 19, inciso IV, da Lei 14.133/2021: instituição de modelos de minutas de editais, termos de referência, contratos padronizados e demais documentos.
- C4: Art. 7º, caput, incisos I a III e §1º, da Lei 14.133/2021: designação de agentes públicos para funções essenciais, observados atribuições, formação, segregação de funções e inexistência de vínculos que comprometam a atuação.
- C5: COBIT 2019, BAI02.04 - Obter aprovação dos requisitos da solução: obter aprovação formal dos requisitos funcionais, técnicos, de segurança e de conformidade antes de prosseguir com a solução.
- C6: COBIT 2019, APO01.05 - Estabelecer papéis e responsabilidades: definir e comunicar papéis e responsabilidades relacionados à informação e à tecnologia.
- C7: COBIT 2019, APO01.09 - Definir e comunicar políticas e procedimentos: manter políticas, procedimentos e orientações para direcionar processos de gestão de TIC.
- C8: Instrução Normativa SGD/ME nº 94, de 23 de dezembro de 2022, art. 1º, § 1º: como referência de boa prática, a aplicação de ritos formais de contratação de TIC pode ser facultada para contratações diretas por dispensa em razão do valor (inciso II do art. 75 da Lei nº 14.133/2021), indicando a possibilidade de fluxos simplificados para aquisições de baixa complexidade ou valor.

procedimentos:
- P1: Verificar, por meio da q2801, a existência de processo formal e padronizado para contratações de TIC; [IR1]
- P2: Validar, pelas evidências anexadas à q2801, a existência de fluxo, papéis, responsabilidades, modelos, manuais, checklists ou normativos orientativos; [IR1, IR2, IR3]
- P3: Verificar, por meio da q2804[A] e da q2804eviA, se as contratações de TIC são submetidas à análise prévia e aprovação técnica da área de TIC; [IR4, IR5]
- P4: Verificar, por meio das q2102ext[C], q2802ext[C], q2802ext[D], q2804[B] e evidências q2102evi/q2802evi, se as contratações de TIC estão aderentes ao plano de TIC, ao plano de contratações e à proposta orçamentária; [IR6]
- P5: Verificar, por meio da q2804[C] e da q2801evi, se a equipe de planejamento da contratação é formalmente designada e possui participação técnica de TIC; [IR7]

evidencias:
- E1: Resposta negativa ou insuficiente sobre processo formal e padronizado para contratações de TIC; [P1]
- E2: Ausência, desatualização ou insuficiência de evidências de fluxo, papéis, responsabilidades, modelos, manuais, checklists ou normativos orientativos; [P2]
- E3: Resposta negativa ou insuficiente sobre análise prévia e aprovação técnica da área de TIC; [P3]
- E4: Ausência de evidência específica de aprovação técnica da área de TIC em caso concreto; [P3]
- E5: Resposta negativa ou insuficiente sobre aderência das contratações ao plano de TIC ou ao plano de contratações; [P4]
- E6: Resposta negativa ou insuficiente sobre equipe de planejamento formalmente designada e com participação técnica de TIC; [P5]

possiveis_achados:
- A6: Fragilidades na governança técnica da fase preparatória das contratações de TIC
  situacoes_encontradas:
  - S6.1:
      descricao: Inexistência ou fragilidade de processo formal e padronizado para contratações de TIC.
      severidade: alta
      itens_questionario: [q2801ext[A], q2801ext[C], q2801ext[D], q2801ext[E], q2801ext[G], q2801evi]
      regra_de_identificacao:
      - (q2801ext[A] != Sim) | (q2801ext[C] != Sim) | (q2801ext[D] != Sim) | (q2801ext[E] != Sim) | (q2801ext[G] != Sim)
      referencias_matriz: [R6.1, R6.2, P1, E1, P2, E2]
      criterios: [C1, C3, C7]
      tipo_encaminhamento: Recomendação
      encaminhamento: formalize e padronize o processo de contratação de TIC, compatível com o porte, a complexidade e os riscos das contratações da organização, atentando-se, minimamente, em definir fluxo, etapas, papéis, responsabilidades, instâncias de aprovação e modelos de artefatos, manuais, listas de verificação ou orientações internas aplicáveis
  - S6.2:
      descricao: Contratações de TIC sem análise prévia e aprovação técnica obrigatória da área de TIC.
      severidade: alta
      itens_questionario: [q2804[A], q2804eviA]
      regra_de_identificacao:
      - (q2804[A] != Sim)
      referencias_matriz: [R6.3, P3, E3, E4]
      criterios: [C1, C5, C6, C8]
      tipo_encaminhamento: Recomendação
      encaminhamento: estabeleça a submissão das contratações de TIC à análise prévia da área de TIC, inclusive quando demandadas por outras áreas, de modo a verificar a compatibilidade da solução com os padrões tecnológicos, os requisitos institucionais e a arquitetura existente, admitindo fluxos simplificados para contratações de baixa complexidade ou baixo valor, desde que preservada análise técnica mínima compatível com o risco da contratação
  - S6.3:
      descricao: Contratações de TIC sem alinhamento demonstrado ao planejamento de TIC, ao plano de contratações ou à proposta orçamentária.
      severidade: alta
      itens_questionario: [q2102ext[C], q2802ext[C], q2802ext[D], q2804[B], q2102evi, q2802evi]
      regra_de_identificacao:
      - (q2102ext[C] != Sim) | (q2802ext[C] != Sim) | (q2802ext[D] != Sim) | (q2804[B] != Sim)
      referencias_matriz: [R6.3, P4, E5]
      criterios: [C1, C2]
      tipo_encaminhamento: Recomendação
      encaminhamento: integre as contratações de TIC ao planejamento de TIC, ao plano de contratações e à proposta orçamentária, atentando-se, minimamente, em registrar a necessidade atendida, a prioridade, a disponibilidade de recursos e a justificativa das situações excepcionais
  - S6.4:
      descricao: Contratações de TIC sem equipe de planejamento formalmente designada e com participação técnica de TIC.
      severidade: alta
      itens_questionario: [q2804[C], q2801evi]
      regra_de_identificacao:
      - (q2804[C] != Sim)
      referencias_matriz: [R6.4, P5, E6]
      criterios: [C1, C4, C6]
      tipo_encaminhamento: Recomendação
      encaminhamento: designe formalmente equipe responsável pelo planejamento das contratações de TIC, atentando-se, minimamente, em assegurar a participação da área requisitante, da área técnica de TIC e das demais áreas necessárias, com definição das responsabilidades de seus integrantes

---

## Questão Transversal - Evolução agregada em relação à fiscalização anterior

natureza: levantamento
gera_achado: false
questao: QT. As organizações anteriormente avaliadas apresentaram evolução mensurável, em termos agregados, em governança e gestão de TIC e no atendimento aos encaminhamentos da fiscalização anterior?

subquestoes:
- Houve variação agregada positiva, negativa ou estável nos indicadores comparáveis de governança e gestão de TIC?
- Quais dimensões, práticas ou indicadores agregados apresentaram maior evolução?
- Quais dimensões, práticas ou indicadores agregados permaneceram estáveis ou regrediram?
- Qual foi o grau agregado de atendimento aos encaminhamentos propostos na fiscalização anterior?
- Há diferença relevante entre a evolução agregada dos municípios avaliados em 2023 e a evolução agregada das organizações do Poder Executivo?
- As diferenças metodológicas entre os ciclos limitam a comparabilidade dos resultados?

fontes_de_informacao:
- F1: Resultados, respostas e indicadores calculados no iGovTI 2026 para as organizações também avaliadas na fiscalização anterior.
- F2: Resultados, respostas, indicadores, achados e encaminhamentos da fiscalização anterior de 2023 relativa ao iGovTI em municípios.
- F3: Resultados, respostas, indicadores, achados e encaminhamentos da fiscalização anterior de 2023 relativa ao iGovTI nas organizações do Poder Executivo estadual.
- F4: Metodologias de cálculo, dicionários de variáveis, questionários, planilhas de correspondência e demais registros necessários para compatibilizar os ciclos de avaliação.
- F5: Informações, evidências e registros produzidos no iGovTI 2026 que permitam inferir, em termos agregados, atendimento, não atendimento ou atendimento parcial dos encaminhamentos anteriores.

informacoes_requeridas:
- IR1: Relação das organizações avaliadas na fiscalização anterior que também integram o iGovTI 2026, segregadas, quando aplicável, entre municípios e organizações do Poder Executivo estadual; [F1, F2, F3]
- IR2: Indicadores, dimensões, práticas, faixas de maturidade ou métricas da fiscalização anterior que sejam comparáveis com os resultados do iGovTI 2026; [F1, F2, F3, F4]
- IR3: Tabela de correspondência entre indicadores, práticas, dimensões ou métricas dos ciclos de avaliação, com indicação do grau de comparabilidade; [F4]
- IR4: Distribuição agregada dos resultados da fiscalização anterior e do iGovTI 2026, incluindo quantitativo e percentual de organizações por nível, faixa, dimensão, prática ou indicador comparável; [F1, F2, F3]
- IR5: Variação agregada entre os ciclos, incluindo evolução, estabilidade ou regressão por indicador, dimensão, prática ou faixa de maturidade comparável; [F1, F2, F3, F4]
- IR6: Relação dos encaminhamentos propostos na fiscalização anterior e sua classificação agregada quanto a atendimento, atendimento parcial, não atendimento ou impossibilidade de avaliação; [F2, F3, F5]
- IR7: Limitações metodológicas que afetem a comparação entre os ciclos, incluindo alteração de questionário, pesos, fórmulas, universo avaliado, escala de resposta ou critérios de classificação; [F1, F2, F3, F4]

criterios_de_comparabilidade:
- CT1: Comparar apenas organizações presentes nos dois ciclos ou, quando houver alteração de universo, explicitar separadamente o universo comum e o universo total de cada ciclo.
- CT2: Comparar apenas indicadores, dimensões, práticas ou faixas com correspondência metodológica suficiente; quando a correspondência for parcial, registrar a limitação e evitar conclusão categórica.
- CT3: Utilizar quantitativos absolutos e percentuais para descrever variações agregadas, distinguindo evolução, estabilidade e regressão.
- CT4: Distinguir mudança em resultado agregado de atendimento efetivo de encaminhamento; melhoria no indicador não implica, por si só, cumprimento integral da recomendação anterior.
- CT5: Classificar atendimento dos encaminhamentos anteriores em categorias explícitas, como atendido, parcialmente atendido, não atendido e não avaliável, com base em evidências disponíveis nos autos, registros da fiscalização anterior e informações do iGovTI 2026.
- CT6: Registrar limitações decorrentes de mudanças metodológicas, de diferenças de escopo, de alteração de pesos, de alteração de itens do questionário ou de indisponibilidade de dados históricos.

procedimentos:
- P1: Identificar o conjunto de organizações avaliadas na fiscalização anterior e cruzá-lo com o universo de organizações respondentes do iGovTI 2026; [IR1]
- P2: Construir tabela de correspondência entre indicadores, dimensões, práticas, faixas de maturidade ou métricas comparáveis entre a fiscalização anterior e o iGovTI 2026; [IR2, IR3]
- P3: Calcular, para o conjunto comum de organizações, a distribuição agregada dos resultados nos dois ciclos, por indicador, dimensão, prática ou faixa de maturidade comparável; [IR4]
- P4: Calcular a variação agregada entre os ciclos, distinguindo evolução, estabilidade e regressão, em quantitativos absolutos e percentuais; [IR5]
- P5: Segregar, quando aplicável, os resultados agregados dos municípios avaliados em 2023 e das organizações do Poder Executivo estadual avaliadas em 2023; [IR1, IR4, IR5]
- P6: Classificar, em termos agregados, o atendimento dos encaminhamentos da fiscalização anterior, com base nos registros disponíveis e nas evidências ou respostas do iGovTI 2026; [IR6]
- P7: Identificar limitações metodológicas da comparação e indicar quais conclusões podem ou não ser extraídas dos dados disponíveis; [IR7]

evidencias:
- E1: Relação consolidada das organizações presentes nos dois ciclos de avaliação; [P1]
- E2: Tabela de correspondência entre itens, indicadores, dimensões, práticas ou faixas comparáveis entre a fiscalização anterior e o iGovTI 2026; [P2]
- E3: Tabelas, gráficos ou painéis com distribuição agregada dos resultados da fiscalização anterior e do iGovTI 2026; [P3]
- E4: Cálculo da variação agregada dos resultados, em números absolutos e percentuais, indicando evolução, estabilidade ou regressão; [P4]
- E5: Comparativo agregado entre municípios avaliados em 2023 e organizações do Poder Executivo estadual avaliadas em 2023, quando os dados permitirem a segregação; [P5]
- E6: Quadro consolidado de atendimento, atendimento parcial, não atendimento ou impossibilidade de avaliação dos encaminhamentos anteriores; [P6]
- E7: Registro das limitações metodológicas e das cautelas necessárias para interpretação dos resultados comparativos; [P7]

o_que_a_analise_permite_dizer:
- Se, no conjunto comum de organizações, houve evolução, estabilidade ou regressão agregada em governança e gestão de TIC entre a fiscalização anterior e o iGovTI 2026.
- Quais dimensões, práticas ou indicadores comparáveis concentraram os maiores avanços agregados.
- Quais dimensões, práticas ou indicadores comparáveis permaneceram com baixa evolução, estagnaram ou regrediram em termos agregados.
- Se os encaminhamentos da fiscalização anterior foram atendidos, parcialmente atendidos, não atendidos ou não puderam ser avaliados, em termos agregados.
- Se há diferença relevante entre a evolução agregada dos municípios avaliados em 2023 e das organizações do Poder Executivo estadual avaliadas em 2023.
- Em que medida diferenças metodológicas entre os ciclos limitam a força das conclusões comparativas.

limitacoes_e_cautelas:
- A questão tem caráter de levantamento e análise longitudinal agregada, não gerando achado individual por organização.
- A comparação não deve ser feita questão a questão quando não houver equivalência metodológica suficiente entre os instrumentos de avaliação.
- A evolução agregada não autoriza, isoladamente, concluir que todas as organizações evoluíram individualmente.
- A regressão agregada não autoriza, isoladamente, concluir descumprimento individual de encaminhamento anterior.
- O atendimento dos encaminhamentos anteriores deve ser analisado conforme o conteúdo de cada encaminhamento, as evidências disponíveis e a compatibilidade com os dados coletados no iGovTI 2026.
