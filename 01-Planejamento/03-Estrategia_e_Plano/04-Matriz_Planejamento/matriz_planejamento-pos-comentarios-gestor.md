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
- A área de TIC possui atribuições formalmente definidas relacionadas à gestão da TIC?
- A área de TIC está posicionada em nível organizacional que favoreça sua interlocução com a alta administração e sua atuação estratégica?

riscos:
- R1.1: Devido à ausência de formalização da área de TIC, poderá não haver unidade ou função institucionalmente reconhecida para coordenar o uso da tecnologia da informação, prejudicando a responsabilização e o alinhamento da TIC aos objetivos da organização.
- R1.2: Devido à ausência de atribuições formais da área de TIC, poderá não haver clareza sobre responsabilidades de planejamento, coordenação, gestão e controle da TIC, favorecendo atuação reativa e fragmentada.
- R1.3: Devido ao posicionamento organizacional inadequado da área de TIC, poderá haver baixa capacidade de influência institucional, comprometendo a participação da TIC em decisões estratégicas, orçamentárias, contratuais e de gestão de riscos.

fontes_de_informacao:
- F1: Respostas ao questionário eletrônico iGovTI.
- F2: Evidências anexadas ao questionário eletrônico.

informacoes_requeridas:
- IR1: Resposta sobre a existência formal de área, unidade, setor ou função de TIC; [F1, q0101]
- IR3: Resposta sobre atribuições e competências formalizadas da área de TIC; [F1, q0103]
- IR4: Evidência anexada que demonstre atribuições formalmente definidas relacionadas à gestão da TIC; [F2, q0103evi]
- IR5: Resposta sobre posicionamento hierárquico da área de TIC na estrutura organizacional; [F1, q0102]

criterios:
- C1: COBIT 2019, APO01.04 - Definir e implementar as estruturas organizacionais: estabelecer estruturas organizacionais internas e externas necessárias para apoiar os objetivos de governança e gestão de TI.
- C2: COBIT 2019, APO01.05 - Estabelecer papéis e responsabilidades: definir, comunicar e manter papéis e responsabilidades relacionados à governança e gestão de TI.
- C3: COBIT 2019, APO01.06 - Aprimorar o posicionamento da função de TI: posicionar a função de tecnologia de modo compatível com sua relevância estratégica, responsabilidades e necessidade de interação com a alta administração.
- C6: Portaria SGD/ME nº 778/2019, art. 4º, § 1º - Referência de posicionamento organizacional: para a obtenção de melhores resultados, a área de TIC de cada órgão ou entidade deve, preferencialmente, estar vinculada à alta administração, com o intuito de apoiá-la na tomada de decisões e no alcance dos objetivos estratégicos.
- C7: Constituição Federal, art. 37, caput - Princípio da eficiência.

procedimentos:
- P1: Verificar, por meio da resposta à q0101, se a organização possui área, unidade, setor ou função de TIC formalmente instituída; [IR1]
- P3: Verificar, por meio da resposta à q0103, se a área de TIC possui atribuições formalmente definidas relacionadas à gestão da TIC; [IR3]
- P4: Validar, pela evidência anexada à q0103, a existência de atribuições formalmente definidas relacionadas à gestão da TIC; [IR4]
- P5: Verificar, por meio da resposta à q0102, o posicionamento hierárquico da área de TIC; [IR5]

evidencias:
- E1: Resposta negativa ou insuficiente sobre formalização da área, unidade, setor ou função de TIC; [P1]
- E3: Resposta negativa ou insuficiente sobre atribuições formalizadas da área de TIC; [P3]
- E4: Ausência ou insuficiência de evidência que demonstre atribuições formalmente definidas relacionadas à gestão da TIC; [P4]
- E5: Resposta que indique posicionamento inexistente ou incompatível da área de TIC; [P5]

possiveis_achados:
- A1: Estrutura de TIC insuficientemente formalizada, definida ou posicionada para gerir a tecnologia da informação.
  situacoes_encontradas:
    - S1.1:
      descricao: Ausência de área, unidade, setor ou função de TIC formalmente instituída.
      severidade: alta
      itens_questionario: [q0101]
      regra_de_identificacao:
      - (q0101 == F)
      referencias_matriz: [R1.1, P1, E1]
      criterios: [C1, C7]
      tipo_encaminhamento: Recomendação
      encaminhamento: formalize a área, unidade, setor ou função de TIC em instrumento compatível com a organização, definindo vinculação e responsabilidades essenciais de modo compatível com o porte, a complexidade e a dependência tecnológica da organização
    - S1.2:
      descricao: Área de TIC sem atribuições formalmente definidas ou sem atribuições formais de gestão de TIC.
      severidade: alta
      itens_questionario: [q0101, q0103, q0103[D], q0103[G], q0103evi]
      regra_de_identificacao:
      - (q0101 != F) & ((q0103[G] == Sim) | (q0103[D] == Não))
      referencias_matriz: [R1.2, P3, E3, P4, E4]
      criterios: [C2, C7]
      tipo_encaminhamento: Recomendação
      encaminhamento: defina formalmente as atribuições da área de TIC, atentando-se, minimamente, em abranger as atividades de planejamento, coordenação, gestão e controle da TIC
    - S1.3:
      descricao: Posicionamento organizacional inadequado da área de TIC.
      severidade: media
      itens_questionario: [q0102]
      regra_de_identificacao:
      - (q0101 != F) & ((q0102 == C) | (q0102 == D) | (q0102 == E))
      referencias_matriz: [R1.3, P5, E5]
      criterios: [C3, C6]
      tipo_encaminhamento: Recomendação
      encaminhamento: avalie o posicionamento organizacional da área de TIC e adote, quando necessário, medidas para assegurar interlocução adequada com a alta administração e participação nas decisões estratégicas, orçamentárias, contratuais e de gestão de riscos relacionadas à tecnologia da informação.

## Questão 02 - Governança e Comitê de TIC

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
      encaminhamento: assegure o funcionamento efetivo do Comitê de TIC ou instância colegiada equivalente, mediante o exercício das competências previstas em seu ato constitutivo, com registro das deliberações e acompanhamento dos respectivos encaminhamentos

## Questão 03 - Planejamento de TIC

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
      encaminhamento: estabeleça e execute rotina periódica de acompanhamento da execução do plano de TIC, promovendo sua revisão periódica e os ajustes ou atualizações necessários, com registro das principais decisões e reprogramações

## Questão 04 - Capacidade Institucional de TIC e Segurança da Informação

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
    encaminhamento: avalie o modelo de operação de TIC e adote medidas proporcionais para assegurar capacidade interna suficiente para coordenar, supervisionar e fiscalizar as atividades e os contratos de TIC executados predominantemente por terceiros, preservando responsabilização e retenção de conhecimento

## Questão 05 - Gestão de Serviços de TIC

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
      encaminhamento: formalize e execute processo de gestão de incidentes de TIC, atentando-se, minimamente, em definir papéis, critérios de priorização e escalamento, tratamento de incidentes de serviços e de segurança da informação e registro sistemático e rastreável das ocorrências

## Questão 06 - Contratações de TIC

questao: Q6. A organização adota processo formal e padronizado para a fase preparatória das contratações de TIC, com responsabilidades definidas, análise técnica pela área de TIC e alinhamento aos instrumentos de planejamento?

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
- IR6: Resposta e evidência sobre alinhamento das contratações aos instrumentos de planejamento e ao Plano de Contratações Anual; [F1, F2, q2802ext[C], q2804[B], q2802evi]
- IR7: Resposta sobre equipe de planejamento formalmente designada e com participação técnica de TIC; [F1, q2804[C]]

criterios:
- C1: Art. 11, parágrafo único, da Lei 14.133/2021: responsabilidade da alta administração pela governança das contratações, com processos, estruturas, gestão de riscos e controles internos.
- C2: Art. 18, caput e §1º, incisos I, IV, V, VIII, IX, X e XIII, da Lei 14.133/2021: fase preparatória caracterizada pelo planejamento, compatibilização com o plano de contratações anual e elementos mínimos do estudo técnico preliminar.
- C3: Art. 19, inciso IV, da Lei 14.133/2021: instituição de modelos de minutas de editais, termos de referência, contratos padronizados e demais documentos.
- C4: Art. 7º, caput, incisos I a III e §1º, da Lei 14.133/2021: designação de agentes públicos para funções essenciais, observados atribuições, formação, segregação de funções e inexistência de vínculos que comprometam a atuação.
- C5: COBIT 2019, BAI02.04 - Obter aprovação dos requisitos da solução: obter aprovação formal dos requisitos funcionais, técnicos, de segurança e de conformidade antes de prosseguir com a solução.
- C8: Instrução Normativa SGD/ME nº 94, de 23 de dezembro de 2022, art. 1º, § 1º: como referência de boa prática, a aplicação de ritos formais de contratação de TIC pode ser facultada para contratações diretas por dispensa em razão do valor (inciso II do art. 75 da Lei nº 14.133/2021), indicando a possibilidade de fluxos simplificados para aquisições de baixa complexidade ou valor.

procedimentos:
- P1: Verificar, por meio da q2801, a existência de processo formal e padronizado para contratações de TIC; [IR1]
- P2: Validar, pelas evidências anexadas à q2801, a existência de fluxo, papéis, responsabilidades, modelos, manuais, checklists ou normativos orientativos; [IR1, IR2, IR3]
- P3: Verificar, por meio da q2804[A] e da q2804eviA, se as contratações de TIC são submetidas à análise prévia e aprovação técnica da área de TIC; [IR4, IR5]
- P4: Verificar, por meio das q2802ext[C], q2804[B] e da evidência q2802evi, se as contratações de TIC estão alinhadas aos instrumentos de planejamento e ao Plano de Contratações Anual; [IR6]
- P5: Verificar, por meio da q2804[C], se a equipe de planejamento da contratação é formalmente designada e possui participação técnica de TIC; [IR7]

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
      descricao: Inexistência ou fragilidade de processo formal e padronizado para o planejamento das contratações de TIC.
      severidade: alta
      itens_questionario: [q2801ext[A], q2801ext[B], q2801evi]
      regra_de_identificacao:
      - (q2801ext[A] != Sim) | (q2801ext[B] != Sim)
      referencias_matriz: [R6.1, R6.2, P1, E1, P2, E2]
      criterios: [C1, C3]
      tipo_encaminhamento: Determinação
      encaminhamento: formalize e padronize o processo de planejamento das contratações de TIC, com etapas, responsabilidades e artefatos padronizados, admitidos fluxos proporcionais à complexidade e ao risco
  - S6.2:
      descricao: Contratações de TIC sem análise prévia e aprovação técnica da área de TIC.
      severidade: alta
      itens_questionario: [q2804[A], q2804eviA]
      regra_de_identificacao:
      - (q2804[A] != Sim)
      referencias_matriz: [R6.3, P3, E3, E4]
      criterios: [C1, C5, C8]
      tipo_encaminhamento: Recomendação
      encaminhamento: estabeleça a submissão das contratações de TIC à análise prévia da área de TIC, de modo a verificar a compatibilidade da solução com os padrões tecnológicos, os requisitos institucionais e a arquitetura existente, admitindo fluxos simplificados para contratações de baixa complexidade ou baixo valor, desde que preservada análise técnica mínima compatível com o risco da contratação
  - S6.3:
      descricao: Contratações de TIC sem alinhamento ao planejamento de TIC e ao Plano de Contratações Anual.
      severidade: alta
      itens_questionario: [q2802ext[C], q2804[B], q2802evi]
      regra_de_identificacao:
      - (q2802ext[C] != Sim) | (q2804[B] != Sim)
      referencias_matriz: [R6.3, P4, E5]
      criterios: [C1, C2]
      tipo_encaminhamento: Determinação
      encaminhamento: integre as contratações de TIC com os instrumentos de planejamento da organização e com o Plano de Contratações Anual, quando elaborado, justificando as situações excepcionais
  - S6.4:
      descricao: Contratações de TIC sem designação de equipe de planejamento com integrante técnico da área de TIC.
      severidade: alta
      itens_questionario: [q2804[C]]
      regra_de_identificacao:
      - (q2804[C] != Sim)
      referencias_matriz: [R6.4, P5, E6]
      criterios: [C1, C4]
      tipo_encaminhamento: Recomendação
      encaminhamento: designe formalmente equipe de planejamento para as contratações de TIC, atentando-se, minimamente, em assegurar a participação de integrante da área requisitante e da área técnica de TIC, com definição das responsabilidades de seus integrantes

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
