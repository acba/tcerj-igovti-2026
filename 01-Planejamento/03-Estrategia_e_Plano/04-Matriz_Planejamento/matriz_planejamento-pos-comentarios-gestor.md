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
- id: C1
  descricao: >-
    COBIT 2019, APO01.04 - Definir e implementar as estruturas organizacionais: estabelecer estruturas organizacionais internas e externas necessárias para apoiar os objetivos de governança e gestão de TI.
  natureza_fundamento: boa_pratica
  apto_a_fundamentar_determinacao: false
- id: C2
  descricao: >-
    COBIT 2019, APO01.05 - Estabelecer papéis e responsabilidades: definir, comunicar e manter papéis e responsabilidades relacionados à governança e gestão de TI.
  natureza_fundamento: boa_pratica
  apto_a_fundamentar_determinacao: false
- id: C3
  descricao: >-
    COBIT 2019, APO01.06 - Aprimorar o posicionamento da função de TI: posicionar a função de tecnologia de modo compatível com sua relevância estratégica, responsabilidades e necessidade de interação com a alta administração.
  natureza_fundamento: boa_pratica
  apto_a_fundamentar_determinacao: false
- id: C6
  descricao: >-
    Portaria SGD/ME nº 778/2019, art. 4º, § 1º - Referência de posicionamento organizacional: para a obtenção de melhores resultados, a área de TIC de cada órgão ou entidade deve, preferencialmente, estar vinculada à alta administração, com o intuito de apoiá-la na tomada de decisões e no alcance dos objetivos estratégicos.
  natureza_fundamento: referencial_nao_vinculante
  apto_a_fundamentar_determinacao: false
- id: C7
  descricao: >-
    Constituição Federal, art. 37, caput - Princípio da eficiência.
  natureza_fundamento: norma_geral
  apto_a_fundamentar_determinacao: false
- id: C8
  descricao: >-
    Decreto Estadual nº 47.278/2020 (alterado pelo Decreto nº 48.997/2024), arts. 4º e 6º, I a XI, e Portaria PRODERJ/PRE nº 825/2021, Anexo A, arts. 1º, IX, 8º e 9º — estruturação obrigatória do Sistema Estadual de TIC (SETIC), instituição dos Níveis Setoriais de TIC (NSTIC) e definição das atribuições mínimas da unidade de TIC nos órgãos e entidades do Poder Executivo Estadual.
  natureza_fundamento: norma_regulamentar_vinculante
  apto_a_fundamentar_determinacao: true
  publico: Poder Executivo Estadual
  aplica_se:
    segmentos: [EXECUTIVO_ESTADUAL]
- id: C9
  descricao: >-
    Resolução CNJ nº 370/2021, arts. 21 a 23 e Ato Normativo TJ nº 32/2023, arts. 3º e 8º a 10 — dever de estruturação organizacional formal de TIC, com definição de atribuições regimentais e posicionamento compatível no Poder Judiciário Estadual.
  natureza_fundamento: norma_regulamentar_vinculante
  apto_a_fundamentar_determinacao: true
  publico: Poder Judiciário Estadual
  aplica_se:
    segmentos: [JUDICIARIO_ESTADUAL]
- id: C10
  descricao: >-
    Resolução CNMP nº 171/2017, arts. 9º, 16, 18 e 33 e Resoluções GPGJ nº 2.675/2025 e nº 2.785/2026, arts. 7º a 10 e 13 — instituição formal da unidade de TIC, atribuições de gestão e posicionamento estratégico subordinado à alta administração no Ministério Público Estadual.
  natureza_fundamento: norma_regulamentar_vinculante
  apto_a_fundamentar_determinacao: true
  publico: Ministério Público Estadual
  aplica_se:
    segmentos: [MINISTERIO_PUBLICO_ESTADUAL]

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
      variantes:
      - publico: Poder Executivo Estadual
        aplica_se:
          segmentos: [EXECUTIVO_ESTADUAL]
        criterios: [C1, C8]
        tipo_encaminhamento: Determinação
      - publico: Poder Judiciário Estadual
        aplica_se:
          segmentos: [JUDICIARIO_ESTADUAL]
        criterios: [C1, C9]
        tipo_encaminhamento: Determinação
      - publico: Ministério Público Estadual
        aplica_se:
          segmentos: [MINISTERIO_PUBLICO_ESTADUAL]
        criterios: [C1, C10]
        tipo_encaminhamento: Determinação
    - S1.2:
      descricao: Área de TIC sem atribuições formalmente definidas ou sem atribuições formais de gestão de TIC.
      severidade: alta
      itens_questionario: [q0101, q0103, q0103[D], q0103[G], q0103evi]
      regra_de_identificacao:
      - (q0101 != F) & ((q0103[G] == Sim) | (q0103[D] == Não) | (avaliacao_documental[q0103[D]] == Não conforme))
      referencias_matriz: [R1.2, P3, E3, P4, E4]
      criterios: [C2, C7]
      tipo_encaminhamento: Recomendação
      encaminhamento: defina formalmente as atribuições da área de TIC, atentando-se, minimamente, em abranger as atividades de planejamento, coordenação, gestão e controle da TIC
      variantes:
      - publico: Poder Executivo Estadual
        aplica_se:
          segmentos: [EXECUTIVO_ESTADUAL]
        criterios: [C2, C8]
        tipo_encaminhamento: Determinação
      - publico: Poder Judiciário Estadual
        aplica_se:
          segmentos: [JUDICIARIO_ESTADUAL]
        criterios: [C2, C9]
        tipo_encaminhamento: Determinação
      - publico: Ministério Público Estadual
        aplica_se:
          segmentos: [MINISTERIO_PUBLICO_ESTADUAL]
        criterios: [C2, C10]
        tipo_encaminhamento: Determinação
    - S1.3:
      descricao: Posicionamento organizacional inadequado da área de TIC.
      severidade: media
      itens_questionario: [q0101, q0102]
      regra_de_identificacao:
      - ((q0101 == A) | (q0101 == B) | (q0101 == E)) & ((q0102 == C) | (q0102 == D) | (q0102 == E))
      referencias_matriz: [R1.3, P5, E5]
      criterios: [C3, C6]
      tipo_encaminhamento: Recomendação
      encaminhamento: avalie o posicionamento organizacional da área de TIC e adote, quando necessário, medidas para assegurar interlocução adequada com a alta administração e participação nas decisões estratégicas, orçamentárias, contratuais e de gestão de riscos relacionadas à tecnologia da informação.
      variantes:
      - publico: Poder Executivo Estadual
        aplica_se:
          segmentos: [EXECUTIVO_ESTADUAL]
        criterios: [C3, C8]
        tipo_encaminhamento: Recomendação
      - publico: Poder Judiciário Estadual
        aplica_se:
          segmentos: [JUDICIARIO_ESTADUAL]
        criterios: [C3, C9]
        tipo_encaminhamento: Recomendação
      - publico: Ministério Público Estadual
        aplica_se:
          segmentos: [MINISTERIO_PUBLICO_ESTADUAL]
        criterios: [C3, C10]
        tipo_encaminhamento: Recomendação

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
- id: C1
  descricao: >-
    COBIT 2019, EDM01.02 - Dirigir o sistema de governança: orientar estruturas, princípios, processos e práticas de governança para assegurar que a TI apoie os objetivos organizacionais.
  natureza_fundamento: boa_pratica
  apto_a_fundamentar_determinacao: false
- id: C2
  descricao: >-
    COBIT 2019, MEA01.04 - Avaliar o desempenho: monitorar e avaliar periodicamente o desempenho e a conformidade da TI em relação a objetivos, indicadores, metas e expectativas das partes interessadas.
  natureza_fundamento: boa_pratica
  apto_a_fundamentar_determinacao: false
- id: C3
  descricao: >-
    Decreto nº 12.198/2024, arts. 5º e 6º, § 2º – Referência de governança digital: instituição, no âmbito da Administração Pública federal direta, autárquica e fundacional, de Comitê de Governança Digital ou colegiado equivalente com função deliberativa sobre ações de governo digital e uso de recursos de TIC, incluindo a aprovação dos instrumentos de planejamento previstos no Decreto.
  natureza_fundamento: referencial_nao_vinculante
  apto_a_fundamentar_determinacao: false
- id: C4
  descricao: >-
    Acórdão TCE-RJ nº 44.490/2024-PLEN, itens II.1, III.1 e V.1 – Precedente pela instituição e atuação efetiva de instância colegiada de governança de TIC, com responsabilidade pelo alinhamento das ações de TIC aos objetivos institucionais, priorização dos investimentos e monitoramento do desempenho da TIC.
  natureza_fundamento: jurisprudencia_tce_rj
  apto_a_fundamentar_determinacao: true
- id: C5
  descricao: >-
    Portaria PRODERJ/PRE nº 825/2021, Anexo C, arts. 2º, 5º, 6º, 13 e 14 e Decreto Estadual nº 46.644/2019, arts. 3º e 4º — instituição obrigatória do Comitê Permanente do PEDTIC com composição multidisciplinar, definição de metas, indicadores e registros formais das deliberações no Poder Executivo Estadual.
  natureza_fundamento: norma_regulamentar_vinculante
  apto_a_fundamentar_determinacao: true
  publico: Poder Executivo Estadual
  aplica_se:
    segmentos: [EXECUTIVO_ESTADUAL]
- id: C6
  descricao: >-
    Resolução CNJ nº 370/2021, arts. 7º, 8º, 42, 44, 46 e 48 e Atos Normativos TJ nº 27/2022 e nº 32/2023 — instituição obrigatória do Comitê de Governança de TIC (CGTIC), metas, indicadores estratégicos e reuniões periódicas no Poder Judiciário Estadual.
  natureza_fundamento: norma_regulamentar_vinculante
  apto_a_fundamentar_determinacao: true
  publico: Poder Judiciário Estadual
  aplica_se:
    segmentos: [JUDICIARIO_ESTADUAL]
- id: C7
  descricao: >-
    Resolução CNMP nº 171/2017, arts. 11 a 14 e Resoluções GPGJ nº 2.540/2023 e nº 2.785/2026 — instituição obrigatória do Comitê Estratégico de TI (CETI), metas, reuniões trimestrais e relatório anual no Ministério Público Estadual.
  natureza_fundamento: norma_regulamentar_vinculante
  apto_a_fundamentar_determinacao: true
  publico: Ministério Público Estadual
  aplica_se:
    segmentos: [MINISTERIO_PUBLICO_ESTADUAL]

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
      - (q1001ext[H] != Sim) | (avaliacao_documental[q1001ext[H]] == Não conforme)
      referencias_matriz: [R2.1, P1, E1, P2, E2]
      criterios: [C2]
      tipo_encaminhamento: Recomendação
      encaminhamento: estabeleça objetivos, indicadores e metas para a gestão de TIC, de modo a possibilitar o acompanhamento periódico do desempenho da TIC pela alta administração
      variantes:
      - publico: Poder Executivo Estadual
        aplica_se:
          segmentos: [EXECUTIVO_ESTADUAL]
        criterios: [C2, C5]
        tipo_encaminhamento: Recomendação
      - publico: Poder Judiciário Estadual
        aplica_se:
          segmentos: [JUDICIARIO_ESTADUAL]
        criterios: [C2, C6]
        tipo_encaminhamento: Determinação
      - publico: Ministério Público Estadual
        aplica_se:
          segmentos: [MINISTERIO_PUBLICO_ESTADUAL]
        criterios: [C2, C7]
        tipo_encaminhamento: Determinação
    - S2.2:
      descricao: Comitê de TIC ou instância equivalente não instituído formalmente ou sem representação de áreas relevantes da organização.
      severidade: alta
      itens_questionario: [q1001ext[E], q1001evi]
      regra_de_identificacao:
      - (q1001ext[E] != Sim) | (avaliacao_documental[q1001ext[E]] == Não conforme)
      referencias_matriz: [R2.2, P3, E3, P4, E4]
      criterios: [C1, C3, C4]
      tipo_encaminhamento: Determinação
      encaminhamento: institua formalmente Comitê de TIC ou instância colegiada equivalente, compatível com o porte e a estrutura decisória da organização, definindo em seu ato constitutivo, minimamente, a participação de representantes de áreas relevantes da organização, suas competências, a periodicidade de reuniões, a forma de registro das deliberações e os mecanismos de acompanhamento dos encaminhamentos
      variantes:
      - publico: Poder Executivo Estadual
        aplica_se:
          segmentos: [EXECUTIVO_ESTADUAL]
        criterios: [C1, C4, C5]
        tipo_encaminhamento: Determinação
      - publico: Poder Judiciário Estadual
        aplica_se:
          segmentos: [JUDICIARIO_ESTADUAL]
        criterios: [C1, C4, C6]
        tipo_encaminhamento: Determinação
      - publico: Ministério Público Estadual
        aplica_se:
          segmentos: [MINISTERIO_PUBLICO_ESTADUAL]
        criterios: [C1, C4, C7]
        tipo_encaminhamento: Determinação
    - S2.3:
      descricao: Comitê de TIC ou instância equivalente sem atuação efetiva comprovada.
      severidade: media
      itens_questionario: [q1001ext[E], q1001ext[F], q1001evi]
      regra_de_identificacao:
      - (q1001ext[E] == Sim) & (avaliacao_documental[q1001ext[E]] != Não conforme) & ((q1001ext[F] != Sim) | (avaliacao_documental[q1001ext[F]] == Não conforme))
      referencias_matriz: [R2.3, P5, E5, P6, E6]
      criterios: [C1, C3, C4]
      tipo_encaminhamento: Determinação
      encaminhamento: assegure o funcionamento efetivo do Comitê de TIC ou instância colegiada equivalente, mediante o exercício das competências previstas em seu ato constitutivo, com registro das deliberações e acompanhamento dos respectivos encaminhamentos
      variantes:
      - publico: Poder Executivo Estadual
        aplica_se:
          segmentos: [EXECUTIVO_ESTADUAL]
        criterios: [C1, C4, C5]
        tipo_encaminhamento: Determinação
      - publico: Poder Judiciário Estadual
        aplica_se:
          segmentos: [JUDICIARIO_ESTADUAL]
        criterios: [C1, C4, C6]
        tipo_encaminhamento: Determinação
      - publico: Ministério Público Estadual
        aplica_se:
          segmentos: [MINISTERIO_PUBLICO_ESTADUAL]
        criterios: [C1, C4, C7]
        tipo_encaminhamento: Determinação

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
- R3.1: Devido à inexistência ou insuficiência do processo de planejamento de TIC, poderá não haver plano vigente e participação adequada das áreas demandantes, favorecendo atuação reativa e desalinhada às necessidades institucionais.
- R3.2: Devido à ausência de aprovação formal do plano de TIC pela instância competente, o instrumento poderá não possuir legitimidade institucional para orientar a gestão, os projetos, o orçamento e as contratações de TIC.
- R3.4: Devido ao alinhamento insuficiente do plano de TIC ao planejamento institucional poderão ser executadas ações de TIC com baixo valor ou desconectadas das prioridades da organização.
- R3.5: Devido à ausência de integração entre planejamento de TIC, orçamento e contratações, poderão ocorrer aquisições reativas, não priorizadas ou desalinhadas.
- R3.6: Devido à ausência de acompanhamento da execução do plano de TIC, poderão deixar de ser identificados tempestivamente desvios, pendências ou mudanças que demandem ajustes nas iniciativas e prioridades planejadas.

fontes_de_informacao:
- F1: Respostas ao questionário eletrônico iGovTI.
- F2: Evidências anexadas no questionário eletrônico.

informacoes_requeridas:
- IR1: Respostas sobre execução e formalização do processo de planejamento de TIC, bem como sobre a existência de plano de TIC vigente; [F1, q2101, q2101ext[D], q2102]
- IR2: Evidência que demonstre a formalização do processo de planejamento de TIC; [F2, q2101evi]
- IR3: Resposta sobre participação das áreas demandantes no processo de planejamento de TIC; [F1, q2101ext[A]]
- IR4: Resposta sobre aprovação formal do plano de TIC pela instância competente; [F1, q2102ext[A]]
- IR5: Evidência anexada do ato de aprovação formal do plano de TIC; [F2, q2102evi]
- IR7: Resposta e evidência sobre alinhamento das iniciativas do plano de TIC ao planejamento institucional; [F1, F2, q2102ext[D], q2102evi]
- IR8: Resposta e evidência sobre a utilização do plano de TIC como referência para a elaboração da proposta orçamentária da área de TIC e do plano de contratações; [F1, F2, q2102ext[C], q2102evi]
- IR9: Resposta e evidência sobre acompanhamento da execução do plano de TIC; [F1, F2, q2102ext[E], q2102evi]

criterios:
- id: C1
  descricao: >-
    COBIT 2019, APO02.05 - Definir o plano e o roteiro estratégico: estabelecer plano e roteiro de TIC que traduzam a estratégia em iniciativas, prioridades, recursos, dependências, prazos e benefícios esperados.
  natureza_fundamento: boa_pratica
  apto_a_fundamentar_determinacao: false
- id: C2
  descricao: >-
    COBIT 2019, APO06.03 - Criar e manter orçamentos: elaborar e manter orçamento de TIC alinhado ao portfólio, ao planejamento e às prioridades aprovadas.
  natureza_fundamento: boa_pratica
  apto_a_fundamentar_determinacao: false
- id: C3
  descricao: >-
    Acórdão 1.411/2014-TCU-Plenário, item 9.1.6 e subitens 9.1.6.1 a 9.1.6.4: necessidade de instituir formalmente plano diretor de TI, contemplando desdobramento de diretrizes estratégicas, vinculação das ações de TI a indicadores e metas de negócio, vinculação das ações de TI a indicadores e metas de serviços ao cidadão e vinculação das ações priorizadas ao orçamento de TI.
  natureza_fundamento: jurisprudencia_outro_orgao
  apto_a_fundamentar_determinacao: false
- id: C4
  descricao: >-
    Acórdão TCE-RJ nº 44.490/2024-PLEN, itens II.3 e III.3 e respectivos subitens – Precedentes quanto ao estabelecimento formal de processo estruturado de planejamento de TIC, com participação das áreas relevantes, elaboração, manutenção e revisão periódica de PDTI, contemplando objetivos, indicadores e metas alinhados aos objetivos institucionais, riscos, projetos, aquisições, recursos necessários e ações de monitoramento após aprovação pela alta administração.
  natureza_fundamento: jurisprudencia_tce_rj
  apto_a_fundamentar_determinacao: true
- id: C5
  descricao: >-
    Portaria PRODERJ/PRE nº 825/2021, arts. 1º a 5º e Anexo C, arts. 1º a 14, e IN PRODERJ/PRE nº 05/2024, art. 5º — obrigatoriedade de elaboração, alinhamento institucional, aprovação pela autoridade máxima, integração com orçamento/PCA e revisão periódica do PEDTIC no Poder Executivo Estadual.
  natureza_fundamento: norma_regulamentar_vinculante
  apto_a_fundamentar_determinacao: true
  publico: Poder Executivo Estadual
  aplica_se:
    segmentos: [EXECUTIVO_ESTADUAL]
- id: C6
  descricao: >-
    Resolução CNJ nº 370/2021, arts. 6º a 8º, 42, 46 e 48 e Atos Normativos TJ nº 32/2023 e nº 27/2022 — rito de elaboração, alinhamento, aprovação pela Presidência, integração orçamentária e acompanhamento do PDTIC no Poder Judiciário Estadual.
  natureza_fundamento: norma_regulamentar_vinculante
  apto_a_fundamentar_determinacao: true
  publico: Poder Judiciário Estadual
  aplica_se:
    segmentos: [JUDICIARIO_ESTADUAL]
- id: C7
  descricao: >-
    Resolução CNMP nº 171/2017, arts. 9º, 11, 12, 14 e 16, Resolução CNMP nº 283/2024, arts. 4º a 6º e Resoluções GPGJ nº 2.785/2026 e nº 2.540/2023 — rito de elaboração, alinhamento institucional, aprovação pelo PGJ, integração orçamentária/PAC e acompanhamento do PETI/PDTI no Ministério Público Estadual.
  natureza_fundamento: norma_regulamentar_vinculante
  apto_a_fundamentar_determinacao: true
  publico: Ministério Público Estadual
  aplica_se:
    segmentos: [MINISTERIO_PUBLICO_ESTADUAL]

procedimentos:
- P1: Verificar, por meio das respostas à q2101 e q2101ext[D], se a organização executa processo de planejamento de TIC formalizado; [IR1]
- P2: Validar, pela evidência anexada à q2101, a formalização mínima do processo de planejamento de TIC; [IR2]
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

variaveis_derivadas:
- nome: existe_plano_ti
  descricao: Indica que a organização declarou possuir plano de TIC vigente, ao menos parcialmente adotado.
  regra_de_calculo: (q2102 == Adota parcialmente.) | (q2102 == Adota em maior parte ou totalmente.)

possiveis_achados:
- A3: Planejamento de TIC insuficiente para orientar a gestão, o orçamento e as contratações de TIC
  situacoes_encontradas:
  - S3.1:
      descricao: Inexistência ou insuficiência do processo de planejamento de TIC para produzir e manter plano de TIC adequado.
      severidade: alta
      itens_questionario: [q2101ext[A], q2101ext[D], q2101evi, q2102]
      regra_de_identificacao:
      - (q2101ext[A] != Sim) | (avaliacao_documental[q2101ext[A]] == Não conforme) | (q2101ext[D] != Sim) | (avaliacao_documental[q2101ext[D]] == Não conforme) | ~existe_plano_ti
      referencias_matriz: [R3.1, P1, E1, P2, E2, P3, E3]
      criterios: [C1, C3, C4]
      tipo_encaminhamento: Determinação
      encaminhamento: institua processo formal de planejamento de TIC, compatível com o porte e a complexidade da organização, que assegure a elaboração e manutenção de plano de TIC, atentando-se, minimamente, em definir etapas, responsabilidades e participação das áreas demandantes
      variantes:
      - publico: Poder Executivo Estadual
        aplica_se:
          segmentos: [EXECUTIVO_ESTADUAL]
        criterios: [C1, C4, C5]
        tipo_encaminhamento: Determinação
      - publico: Poder Judiciário Estadual
        aplica_se:
          segmentos: [JUDICIARIO_ESTADUAL]
        criterios: [C1, C4, C6]
        tipo_encaminhamento: Determinação
      - publico: Ministério Público Estadual
        aplica_se:
          segmentos: [MINISTERIO_PUBLICO_ESTADUAL]
        criterios: [C1, C4, C7]
        tipo_encaminhamento: Determinação
  - S3.2:
      descricao: Ausência de aprovação formal do plano de TIC.
      severidade: alta
      itens_questionario: [q2102, q2102ext[A], q2102evi]
      regra_de_identificacao:
      - existe_plano_ti & ((q2102ext[A] != Sim) | (avaliacao_documental[q2102ext[A]] == Não conforme))
      referencias_matriz: [R3.2, P4, E4, P5, E5]
      criterios: [C3, C4]
      tipo_encaminhamento: Determinação
      encaminhamento: submeta o plano de TIC à aprovação formal do dirigente máximo ou de instância competente da alta administração, mantendo registro do respectivo ato de aprovação
      variantes:
      - publico: Poder Executivo Estadual
        aplica_se:
          segmentos: [EXECUTIVO_ESTADUAL]
        criterios: [C4, C5]
        tipo_encaminhamento: Determinação
      - publico: Poder Judiciário Estadual
        aplica_se:
          segmentos: [JUDICIARIO_ESTADUAL]
        criterios: [C4, C6]
        tipo_encaminhamento: Determinação
      - publico: Ministério Público Estadual
        aplica_se:
          segmentos: [MINISTERIO_PUBLICO_ESTADUAL]
        criterios: [C4, C7]
        tipo_encaminhamento: Determinação
  - S3.4:
      descricao: Plano de TIC sem alinhamento adequado ao planejamento institucional.
      severidade: media
      itens_questionario: [q2102, q2102ext[D], q2102evi]
      regra_de_identificacao:
      - existe_plano_ti & ((q2102ext[D] != Sim) | (avaliacao_documental[q2102ext[D]] == Não conforme))
      referencias_matriz: [R3.4, P7, E7]
      criterios: [C1, C3, C4]
      tipo_encaminhamento: Determinação
      encaminhamento: revise o plano de TIC para explicitar seu alinhamento ao planejamento institucional, às diretrizes superiores e às necessidades das áreas finalísticas e administrativas, relacionando objetivos, iniciativas, indicadores e metas de TIC aos resultados institucionais pretendidos
      variantes:
      - publico: Poder Executivo Estadual
        aplica_se:
          segmentos: [EXECUTIVO_ESTADUAL]
        criterios: [C1, C4, C5]
        tipo_encaminhamento: Determinação
      - publico: Poder Judiciário Estadual
        aplica_se:
          segmentos: [JUDICIARIO_ESTADUAL]
        criterios: [C1, C4, C6]
        tipo_encaminhamento: Determinação
      - publico: Ministério Público Estadual
        aplica_se:
          segmentos: [MINISTERIO_PUBLICO_ESTADUAL]
        criterios: [C1, C4, C7]
        tipo_encaminhamento: Determinação
  - S3.5:
      descricao: Plano de TIC não utilizado como referência para a elaboração da proposta orçamentária e do plano de contratações.
      severidade: alta
      itens_questionario: [q2102, q2102ext[C], q2102evi]
      regra_de_identificacao:
      - existe_plano_ti & ((q2102ext[C] != Sim) | (avaliacao_documental[q2102ext[C]] == Não conforme))
      referencias_matriz: [R3.5, P8, E8]
      criterios: [C2, C4]
      tipo_encaminhamento: Determinação
      encaminhamento: integre o plano de TIC à elaboração da proposta orçamentária e do plano de contratações, de maneira proporcional ao porte, à estrutura e à capacidade de planejamento da organização
      variantes:
      - publico: Poder Executivo Estadual
        aplica_se:
          segmentos: [EXECUTIVO_ESTADUAL]
        criterios: [C2, C4, C5]
        tipo_encaminhamento: Determinação
      - publico: Poder Judiciário Estadual
        aplica_se:
          segmentos: [JUDICIARIO_ESTADUAL]
        criterios: [C2, C4, C6]
        tipo_encaminhamento: Determinação
      - publico: Ministério Público Estadual
        aplica_se:
          segmentos: [MINISTERIO_PUBLICO_ESTADUAL]
        criterios: [C2, C4, C7]
        tipo_encaminhamento: Determinação
  - S3.6:
      descricao: Ausência de acompanhamento da execução do plano de TIC.
      severidade: media
      itens_questionario: [q2102, q2102ext[E], q2102evi]
      regra_de_identificacao:
      - existe_plano_ti & ((q2102ext[E] != Sim) | (avaliacao_documental[q2102ext[E]] == Não conforme))
      referencias_matriz: [R3.6, P9, E9]
      criterios: [C4]
      tipo_encaminhamento: Determinação
      encaminhamento: estabeleça e execute rotina periódica de acompanhamento da execução do plano de TIC, promovendo sua revisão periódica e os ajustes ou atualizações necessários, com registro das principais decisões e reprogramações
      variantes:
      - publico: Poder Executivo Estadual
        aplica_se:
          segmentos: [EXECUTIVO_ESTADUAL]
        criterios: [C4, C5]
        tipo_encaminhamento: Determinação
      - publico: Poder Judiciário Estadual
        aplica_se:
          segmentos: [JUDICIARIO_ESTADUAL]
        criterios: [C4, C6]
        tipo_encaminhamento: Determinação
      - publico: Ministério Público Estadual
        aplica_se:
          segmentos: [MINISTERIO_PUBLICO_ESTADUAL]
        criterios: [C4, C7]
        tipo_encaminhamento: Determinação

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
- IR3: Resposta e evidência sobre existência de cargos ou funções formalmente atribuídos à TIC e à segurança da informação; [F1, F2, q2708, q2708evi]
- IR9: Resposta sobre o modelo de operação predominante de TIC e os quantitativos total e interno de profissionais de TIC, para avaliação da dependência de terceiros e da capacidade interna de coordenação e fiscalização; [F1, q0101, q0105]

criterios:
- id: C1
  descricao: >-
    COBIT 2019, APO01.05 - Estabelecer papéis e responsabilidades: definir, comunicar e manter papéis e responsabilidades relacionados à governança e gestão de TIC.
  natureza_fundamento: boa_pratica
  apto_a_fundamentar_determinacao: false
- id: C2
  descricao: >-
    COBIT 2019, APO07.01 - Adquirir e manter pessoal adequado e apropriado: assegurar quantidade e perfil de profissionais compatíveis com as necessidades de TIC.
  natureza_fundamento: boa_pratica
  apto_a_fundamentar_determinacao: false
- id: C5
  descricao: >-
    COBIT 2019, APO07.05 - Planejar e monitorar o uso de recursos humanos de TI e de negócio: planejar, alocar e acompanhar capacidade de pessoal para iniciativas, operações e serviços de TIC.
  natureza_fundamento: boa_pratica
  apto_a_fundamentar_determinacao: false
- id: C6
  descricao: >-
    COBIT 2019, APO07.06 - Gerenciar pessoal contratado: controlar o uso de pessoal terceirizado ou externo, preservando responsabilização, supervisão e retenção de conhecimento.
  natureza_fundamento: boa_pratica
  apto_a_fundamentar_determinacao: false
- id: C12
  descricao: >-
    Acórdão 1.411/2014-TCU-Plenário, item 9.1.6.5 - O PDTI deve contemplar o quantitativo necessário ou ideal para a força de trabalho em TI.
  natureza_fundamento: jurisprudencia_outro_orgao
  apto_a_fundamentar_determinacao: false
- id: C13
  descricao: >-
    Acórdão 1.411/2014-TCU-Plenário, item 9.1.7 - A organização deve adotar providências para dotar o setor de TI de quantitativo adequado às necessidades de trabalho em TI, consideradas as necessidades das demais áreas.
  natureza_fundamento: jurisprudencia_outro_orgao
  apto_a_fundamentar_determinacao: false
- id: C14
  descricao: >-
    Acórdão TCE-RJ nº 44.490/2024-PLEN, itens I.10.11, III.9.11 e IV.11.3 – Referência para avaliação da estrutura de recursos humanos de TIC quanto à suficiência quantitativa e qualitativa e à preservação de capacidade interna em atividades de planejamento, coordenação, fiscalização e controle.
  natureza_fundamento: jurisprudencia_tce_rj
  apto_a_fundamentar_determinacao: true
- id: C15
  descricao: >-
    Decreto Estadual nº 47.278/2020, arts. 4º e 6º e IN PRODERJ/PRE nº 07/2025, arts. 11, 17 e 18 — capacidade técnica da área de TIC e designação formal obrigatória de Gestor de Segurança da Informação e responsável por incidentes no Poder Executivo Estadual.
  natureza_fundamento: norma_regulamentar_vinculante
  apto_a_fundamentar_determinacao: true
  publico: Poder Executivo Estadual
  aplica_se:
    segmentos: [EXECUTIVO_ESTADUAL]
- id: C16
  descricao: >-
    Resolução CNJ nº 370/2021, art. 24, caput e §§ 1º a 3º, Resolução CNJ nº 468/2022, art. 8º, § 1º e Resolução CNJ nº 396/2021, art. 7º — exigência de quadro permanente e exclusivo de servidores de TIC, dimensionamento documentado por guia técnico, vedação de terceirização de gestão e papéis formais de cibersegurança no Poder Judiciário Estadual.
  natureza_fundamento: norma_regulamentar_vinculante
  apto_a_fundamentar_determinacao: true
  publico: Poder Judiciário Estadual
  aplica_se:
    segmentos: [JUDICIARIO_ESTADUAL]
- id: C17
  descricao: >-
    Resolução CNMP nº 171/2017, arts. 16 e 33, Resolução CNMP nº 283/2024, art. 9º, § 2º e art. 33 e Resoluções GPGJ nº 2.675/2025 e nº 2.757/2025 — quadro próprio de TIC, vedação de terceirização de atividades exclusivas e atribuição de funções formais de TIC e segurança no Ministério Público Estadual.
  natureza_fundamento: norma_regulamentar_vinculante
  apto_a_fundamentar_determinacao: true
  publico: Ministério Público Estadual
  aplica_se:
    segmentos: [MINISTERIO_PUBLICO_ESTADUAL]

procedimentos:
- P1: Verificar, por meio da q0105, o quantitativo informado de profissionais que atuam em TIC e segurança da informação, por área e tipo de vínculo; [IR1]
- P2: Verificar, por meio da q2703 e respectiva evidência, se há definição do quantitativo necessário de pessoal de TIC e segurança da informação; [IR2]
- P3: Verificar, por meio da q2708 e da respectiva evidência, se há cargos ou funções formalmente atribuídos à TIC e à segurança da informação; [IR3]
- P7: Verificar, por meio da resposta à q0101 e dos quantitativos informados na q0105, se o modelo de operação de TIC é predominantemente terceirizado, há profissionais atuando em TIC e não há profissionais internos de TIC; [IR9]

evidencias:
- E1: Quantitativo total declarado igual a zero para profissionais de TIC, desde que a organização tenha informado possuir estrutura formal de TIC; [P1]
- E2: Resposta negativa ou insuficiente sobre definição do quantitativo necessário de pessoal de TIC e segurança da informação, ou evidência inexistente/incompatível/insuficiente; [P2]
- E3: Resposta negativa ou evidência inexistente, incompatível ou insuficiente sobre cargos ou funções formalmente atribuídos à TIC ou à segurança da informação; [P3]
- E7: Modelo de operação de TIC predominantemente terceirizado (q0101 = B), com profissionais atuando em TIC, mas sem profissionais internos de TIC (total de efetivos, comissionados, cedidos e temporários igual a zero); [P7]

variaveis_derivadas:
- nome: total_TI
  descricao: Total de profissionais que atuam regularmente em tecnologia da informação.
  regra_de_calculo: q0105[TI_efetivos] + q0105[TI_comissionados] + q0105[TI_terceirizados] + q0105[TI_cedidos] + q0105[TI_temporarios] + q0105[TI_estagiarios]
- nome: total_TI_interno
  descricao: Total de profissionais internos de tecnologia da informação, excluídos terceirizados e estagiários.
  regra_de_calculo: q0105[TI_efetivos] + q0105[TI_comissionados] + q0105[TI_cedidos] + q0105[TI_temporarios]

possiveis_achados:
- A4: Capacidade institucional de pessoal de TIC e segurança da informação insuficientemente estruturada ou dimensionada
  situacoes_encontradas:
  - S4.1:
      descricao: Ausência de força de trabalho dedicada à TIC.
      severidade: alta
      itens_questionario: [q0101, q0105[TI_efetivos], q0105[TI_comissionados], q0105[TI_terceirizados], q0105[TI_cedidos], q0105[TI_temporarios], q0105[TI_estagiarios]]
      regra_de_identificacao:
      - (q0101 in [A, B, D, E]) & (total_TI == 0)
      referencias_matriz: [R4.1, P1, E1]
      criterios: [C2, C13]
      tipo_encaminhamento: Recomendação
      encaminhamento: avalie a força de trabalho dedicada à TIC e adote medidas proporcionais para assegurar capacidade mínima de planejamento, gestão, proteção, contratação, fiscalização e sustentação dos serviços e ativos de TIC
      variantes:
      - publico: Poder Executivo Estadual
        aplica_se:
          segmentos: [EXECUTIVO_ESTADUAL]
        criterios: [C2, C15]
        tipo_encaminhamento: Recomendação
      - publico: Poder Judiciário Estadual
        aplica_se:
          segmentos: [JUDICIARIO_ESTADUAL]
        criterios: [C2, C16]
        tipo_encaminhamento: Determinação
      - publico: Ministério Público Estadual
        aplica_se:
          segmentos: [MINISTERIO_PUBLICO_ESTADUAL]
        criterios: [C2, C17]
        tipo_encaminhamento: Recomendação
  - S4.2:
      descricao: Ausência ou insuficiência de definição documentada do quantitativo necessário de pessoal de TIC e segurança da informação.
      severidade: media
      itens_questionario: [q2703ext[C], q2703evi]
      regra_de_identificacao:
      - (q2703ext[C] != Sim) | (avaliacao_documental[q2703ext[C]] == Não conforme)
      referencias_matriz: [R4.2, P2, E2]
      criterios: [C5, C12]
      tipo_encaminhamento: Recomendação
      encaminhamento: estime e mantenha atualizado o quantitativo necessário de pessoal de TIC e segurança da informação, considerando o porte e a complexidade da organização, os serviços críticos, os sistemas mantidos, as contratações vigentes e os riscos relevantes
      variantes:
      - publico: Poder Executivo Estadual
        aplica_se:
          segmentos: [EXECUTIVO_ESTADUAL]
        criterios: [C5, C15]
        tipo_encaminhamento: Recomendação
      - publico: Poder Judiciário Estadual
        aplica_se:
          segmentos: [JUDICIARIO_ESTADUAL]
        criterios: [C5, C16]
        tipo_encaminhamento: Determinação
      - publico: Ministério Público Estadual
        aplica_se:
          segmentos: [MINISTERIO_PUBLICO_ESTADUAL]
        criterios: [C5, C17]
        tipo_encaminhamento: Recomendação
  - S4.3:
      descricao: Ausência de cargos ou funções formalmente atribuídos à TIC ou à segurança da informação.
      severidade: media
      itens_questionario: [q2708[B], q2708[D], q2708evi]
      regra_de_identificacao:
      - (q2708[B] != Sim) | (avaliacao_documental[q2708[B]] == Não conforme) | (q2708[D] != Sim) | (avaliacao_documental[q2708[D]] == Não conforme)
      referencias_matriz: [R4.3, P3, E3]
      criterios: [C1, C2]
      tipo_encaminhamento: Recomendação
      encaminhamento: avalie a necessidade de formalizar a atribuição de cargos ou funções à TIC e à segurança da informação e adote solução compatível com as necessidades institucionais e a capacidade administrativa da organização
      variantes:
      - publico: Poder Executivo Estadual
        aplica_se:
          segmentos: [EXECUTIVO_ESTADUAL]
        criterios: [C1, C15]
        tipo_encaminhamento: Recomendação
      - publico: Poder Judiciário Estadual
        aplica_se:
          segmentos: [JUDICIARIO_ESTADUAL]
        criterios: [C1, C16]
        tipo_encaminhamento: Recomendação
      - publico: Ministério Público Estadual
        aplica_se:
          segmentos: [MINISTERIO_PUBLICO_ESTADUAL]
        criterios: [C1, C17]
        tipo_encaminhamento: Recomendação
  - S4.6:
      descricao: Operação de TIC predominantemente terceirizada sem profissionais internos de TIC.
      severidade: alta
      itens_questionario: [q0101, q0105[TI_efetivos], q0105[TI_comissionados], q0105[TI_terceirizados], q0105[TI_cedidos], q0105[TI_temporarios], q0105[TI_estagiarios]]
      regra_de_identificacao:
      - (q0101 == B) & (total_TI_interno == 0) & (total_TI > 0)
      referencias_matriz: [R4.6, P7, E7]
      criterios: [C6, C14]
      tipo_encaminhamento: Recomendação
      encaminhamento: avalie o modelo de operação de TIC e adote medidas proporcionais para assegurar capacidade interna suficiente para coordenar, supervisionar e fiscalizar as atividades e os contratos de TIC executados predominantemente por terceiros, preservando responsabilização e retenção de conhecimento
      variantes:
      - publico: Poder Executivo Estadual
        aplica_se:
          segmentos: [EXECUTIVO_ESTADUAL]
        criterios: [C6, C14, C15]
        tipo_encaminhamento: Recomendação
      - publico: Poder Judiciário Estadual
        aplica_se:
          segmentos: [JUDICIARIO_ESTADUAL]
        criterios: [C6, C14, C16]
        tipo_encaminhamento: Determinação
      - publico: Ministério Público Estadual
        aplica_se:
          segmentos: [MINISTERIO_PUBLICO_ESTADUAL]
        criterios: [C6, C14, C17]
        tipo_encaminhamento: Determinação

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
- id: C2
  descricao: >-
    COBIT 2019, APO09.02 - Catalogar serviços facilitados por TI: definir, manter e comunicar catálogo de serviços, incluindo serviços prestados, características, requisitos e níveis de serviço esperados.
  natureza_fundamento: boa_pratica
  apto_a_fundamentar_determinacao: false
- id: C3
  descricao: >-
    ITIL 4, prática de gerenciamento de nível de serviço: definir, acordar, monitorar, avaliar e reportar metas e níveis de serviço alinhados às necessidades das áreas usuárias.
  natureza_fundamento: boa_pratica
  apto_a_fundamentar_determinacao: false
- id: C4
  descricao: >-
    ITIL 4, prática de gerenciamento de ativos de TI: planejar e gerenciar o ciclo de vida dos ativos de TI, mantendo informações suficientes para apoiar controle, custo, risco, valor e tomada de decisão.
  natureza_fundamento: boa_pratica
  apto_a_fundamentar_determinacao: false
- id: C6
  descricao: >-
    COBIT 2019, BAI10.01 - Estabelecer e manter um modelo de configuração: definir escopo, granularidade, atributos, relacionamentos e responsáveis pela base de configuração.
  natureza_fundamento: boa_pratica
  apto_a_fundamentar_determinacao: false
- id: C8
  descricao: >-
    COBIT 2019, DSS02.02, DSS02.04 e DSS02.07 - Requisições de serviço e incidentes gerenciados: registrar, classificar, priorizar, investigar, diagnosticar, resolver, acompanhar e reportar incidentes e requisições de serviço.
  natureza_fundamento: boa_pratica
  apto_a_fundamentar_determinacao: false
- id: C11
  descricao: >-
    Acórdão TCE-RJ nº 44.490/2024-PLEN, itens II.7.4, III.9.4 e V.6.1 – Recomendações quanto à estruturação do catálogo de serviços de TIC, incluindo descrição dos serviços, metas, formas de acesso e disponibilidade aos usuários.
  natureza_fundamento: jurisprudencia_tce_rj
  apto_a_fundamentar_determinacao: false
- id: C12
  descricao: >-
    Acórdão TCE-RJ nº 44.490/2024-PLEN, itens II.7.5, III.9.5 e V.6.2 – Recomendações quanto à gestão de configuração e ativos de TIC, incluindo formalização do processo e manutenção de base consolidada de ativos e itens de configuração.
  natureza_fundamento: jurisprudencia_tce_rj
  apto_a_fundamentar_determinacao: false
- id: C13
  descricao: >-
    Acórdão TCE-RJ nº 44.490/2024-PLEN, itens II.7.6, III.9.6 e V.6.3 – Recomendações quanto à formalização e execução do processo de gestão de incidentes, incluindo registros, classificação, escalamento e tratamento.
  natureza_fundamento: jurisprudencia_tce_rj
  apto_a_fundamentar_determinacao: false
- id: C14
  descricao: >-
    Acórdão TCE-RJ nº 44.490/2024-PLEN, itens II.7.7, III.9.7 e V.6.4 – Recomendações quanto à definição, pactuação e monitoramento de níveis de serviço.
  natureza_fundamento: jurisprudencia_tce_rj
  apto_a_fundamentar_determinacao: false
- id: C15
  descricao: >-
    ABNT NBR ISO/IEC 20000-2:2021, item 8.2.4 – Gerenciamento de catálogo de serviço: orienta que o catálogo descreva os serviços e seus resultados pretendidos, contenha informações relevantes para sua utilização e seja disponibilizado às partes interessadas que necessitem acessá-lo.
  natureza_fundamento: norma_tecnica
  apto_a_fundamentar_determinacao: false
- id: C16
  descricao: >-
    ABNT NBR ISO/IEC 20000-2:2021, item 8.2.6 – Gerenciamento de configuração: orienta a identificação, o registro, o controle, o rastreamento e a verificação dos itens de configuração, bem como a manutenção de informações de configuração precisas relacionadas aos serviços.
  natureza_fundamento: norma_tecnica
  apto_a_fundamentar_determinacao: false
- id: C17
  descricao: >-
    ABNT NBR ISO/IEC 20000-2:2021, item 8.6.1 – Gerenciamento de incidente: orienta que os incidentes sejam registrados, classificados e priorizados, que as ações adotadas para sua resolução sejam registradas e rastreáveis e que sejam definidas responsabilidades para seu tratamento, incluindo procedimento documentado para incidentes graves.
  natureza_fundamento: norma_tecnica
  apto_a_fundamentar_determinacao: false
- id: C18
  descricao: >-
    Decreto Estadual nº 47.278/2020, arts. 5º, XI e 6º, V e IN PRODERJ/PRE nº 07/2025, arts. 11 a 13, 17 e 18 e Anexo (itens 7.1, 8.1, 8.9.2.1, 8.14) — obrigatoriedade de inventário permanente de ativos e licenças, gestão de incidentes de segurança e SLA contratual no Poder Executivo Estadual.
  natureza_fundamento: norma_regulamentar_vinculante
  apto_a_fundamentar_determinacao: true
  publico: Poder Executivo Estadual
  aplica_se:
    segmentos: [EXECUTIVO_ESTADUAL]
- id: C19
  descricao: >-
    Resolução CNJ nº 370/2021, arts. 18 a 21, 23 e 34, Resolução CNJ nº 396/2021, arts. 6º a 8º e Ato Normativo TJ nº 28/2022 — obrigatoriedade de catálogo de serviços de TIC, acordos de níveis de serviço com metas operacionais, inventário de ativos e gestão de incidentes no Poder Judiciário Estadual.
  natureza_fundamento: norma_regulamentar_vinculante
  apto_a_fundamentar_determinacao: true
  publico: Poder Judiciário Estadual
  aplica_se:
    segmentos: [JUDICIARIO_ESTADUAL]
- id: C20
  descricao: >-
    Resolução CNMP nº 171/2017, arts. 14, 23, 26, 27 e 28, Resolução CNMP nº 294/2024 e Resoluções GPGJ nº 2.785/2026 e nº 2.757/2025 — obrigatoriedade de catálogo de serviços, ANS, inventário permanente de ativos e gestão de incidentes de serviços e segurança no Ministério Público Estadual.
  natureza_fundamento: norma_regulamentar_vinculante
  apto_a_fundamentar_determinacao: true
  publico: Ministério Público Estadual
  aplica_se:
    segmentos: [MINISTERIO_PUBLICO_ESTADUAL]

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
      - (q2201ext[B] != Sim) | (avaliacao_documental[q2201ext[B]] == Não conforme) | (q2201ext[C] != Sim) | (avaliacao_documental[q2201ext[C]] == Não conforme)
      referencias_matriz: [R5.1, P1, E1, P2, E2]
      criterios: [C2, C11, C15]
      tipo_encaminhamento: Recomendação
      encaminhamento: institua e mantenha atualizado catálogo de serviços de TIC, atentando-se, minimamente, em identificar os serviços efetivamente prestados, seus responsáveis, usuários, condições de acesso e informações necessárias ao atendimento das áreas demandantes
      variantes:
      - publico: Poder Executivo Estadual
        aplica_se:
          segmentos: [EXECUTIVO_ESTADUAL]
        criterios: [C2, C11, C15, C18]
        tipo_encaminhamento: Recomendação
      - publico: Poder Judiciário Estadual
        aplica_se:
          segmentos: [JUDICIARIO_ESTADUAL]
        criterios: [C2, C15, C19]
        tipo_encaminhamento: Determinação
      - publico: Ministério Público Estadual
        aplica_se:
          segmentos: [MINISTERIO_PUBLICO_ESTADUAL]
        criterios: [C2, C15, C20]
        tipo_encaminhamento: Determinação
  - S5.2:
      descricao: Ausência ou fragilidade na definição e no monitoramento de níveis mínimos de serviço de TIC.
      severidade: media
      itens_questionario: [q2201, q2201ext[A], q2201ext[D], q2201ext[E], q2201evi]
      regra_de_identificacao:
      - (q2201ext[A] != Sim) | (avaliacao_documental[q2201ext[A]] == Não conforme) | (q2201ext[D] != Sim) | (avaliacao_documental[q2201ext[D]] == Não conforme) | (q2201ext[E] != Sim) | (avaliacao_documental[q2201ext[E]] == Não conforme)
      referencias_matriz: [R5.2, P3, E3, P4, E4]
      criterios: [C3, C14]
      tipo_encaminhamento: Recomendação
      encaminhamento: defina, acorde e monitore níveis de serviço para os serviços de TIC relevantes, estabelecendo metas e mecanismos de acompanhamento de seu cumprimento
      variantes:
      - publico: Poder Executivo Estadual
        aplica_se:
          segmentos: [EXECUTIVO_ESTADUAL]
        criterios: [C3, C14, C18]
        tipo_encaminhamento: Recomendação
      - publico: Poder Judiciário Estadual
        aplica_se:
          segmentos: [JUDICIARIO_ESTADUAL]
        criterios: [C3, C19]
        tipo_encaminhamento: Determinação
      - publico: Ministério Público Estadual
        aplica_se:
          segmentos: [MINISTERIO_PUBLICO_ESTADUAL]
        criterios: [C3, C20]
        tipo_encaminhamento: Determinação
  - S5.3:
      descricao: Inventário e controle de dispositivos e softwares de TIC inexistente ou insuficiente.
      severidade: alta
      itens_questionario: [q2504, q2504ext[A], q2504ext[B], q2504evi]
      regra_de_identificacao:
      - (q2504ext[A] != Sim) | (avaliacao_documental[q2504ext[A]] == Não conforme) | (q2504ext[B] != Sim) | (avaliacao_documental[q2504ext[B]] == Não conforme)
      referencias_matriz: [R5.3, P5, E5, P6, E6]
      criterios: [C4, C12]
      tipo_encaminhamento: Recomendação
      encaminhamento: estabeleça e mantenha inventário atualizado dos ativos tecnológicos sob gestão da organização, contemplando, minimamente, os dispositivos e softwares utilizados, com informações suficientes para sua identificação e controle
      variantes:
      - publico: Poder Executivo Estadual
        aplica_se:
          segmentos: [EXECUTIVO_ESTADUAL]
        criterios: [C4, C18]
        tipo_encaminhamento: Determinação
      - publico: Poder Judiciário Estadual
        aplica_se:
          segmentos: [JUDICIARIO_ESTADUAL]
        criterios: [C4, C19]
        tipo_encaminhamento: Determinação
      - publico: Ministério Público Estadual
        aplica_se:
          segmentos: [MINISTERIO_PUBLICO_ESTADUAL]
        criterios: [C4, C20]
        tipo_encaminhamento: Determinação
  - S5.4:
      descricao: Ausência ou fragilidade do processo de gestão de configuração.
      severidade: media
      itens_questionario: [q2203, q2203ext[A], q2203ext[C], q2203evi]
      regra_de_identificacao:
      - (q2203ext[A] != Sim) | (avaliacao_documental[q2203ext[A]] == Não conforme) | (q2203ext[C] != Sim) | (avaliacao_documental[q2203ext[C]] == Não conforme)
      referencias_matriz: [R5.3, P7, E7, P8, E8]
      criterios: [C6, C12, C16]
      tipo_encaminhamento: Recomendação
      encaminhamento: formalize e execute processo de gestão de configuração, atentando-se, minimamente, em manter base, ferramenta ou registro equivalente com os itens de configuração relevantes, seus responsáveis e os relacionamentos entre ativos
      variantes:
      - publico: Poder Executivo Estadual
        aplica_se:
          segmentos: [EXECUTIVO_ESTADUAL]
        criterios: [C6, C16, C18]
        tipo_encaminhamento: Recomendação
      - publico: Poder Judiciário Estadual
        aplica_se:
          segmentos: [JUDICIARIO_ESTADUAL]
        criterios: [C6, C16, C19]
        tipo_encaminhamento: Recomendação
      - publico: Ministério Público Estadual
        aplica_se:
          segmentos: [MINISTERIO_PUBLICO_ESTADUAL]
        criterios: [C6, C16, C20]
        tipo_encaminhamento: Recomendação
  - S5.5:
      descricao: Inexistência ou fragilidade do processo de gestão de incidentes de TIC.
      severidade: alta
      itens_questionario: [q2204, q2204ext[A], q2204ext[D], q2204ext[E], q2204evi]
      regra_de_identificacao:
      - (q2204ext[A] != Sim) | (avaliacao_documental[q2204ext[A]] == Não conforme) | (q2204ext[D] != Sim) | (avaliacao_documental[q2204ext[D]] == Não conforme) | (q2204ext[E] != Sim) | (avaliacao_documental[q2204ext[E]] == Não conforme)
      referencias_matriz: [R5.4, P9, E9, P10, E10, P12, E12]
      criterios: [C8, C13, C17]
      tipo_encaminhamento: Recomendação
      encaminhamento: formalize e execute processo de gestão de incidentes de TIC, atentando-se, minimamente, em definir papéis, critérios de priorização e escalamento, tratamento de incidentes de serviços e de segurança da informação e registro sistemático e rastreável das ocorrências
      variantes:
      - publico: Poder Executivo Estadual
        aplica_se:
          segmentos: [EXECUTIVO_ESTADUAL]
        criterios: [C8, C17, C18]
        tipo_encaminhamento: Determinação
      - publico: Poder Judiciário Estadual
        aplica_se:
          segmentos: [JUDICIARIO_ESTADUAL]
        criterios: [C8, C17, C19]
        tipo_encaminhamento: Determinação
      - publico: Ministério Público Estadual
        aplica_se:
          segmentos: [MINISTERIO_PUBLICO_ESTADUAL]
        criterios: [C8, C17, C20]
        tipo_encaminhamento: Determinação

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
- IR1: Resposta sobre definição do processo de planejamento das contratações de TIC, incluindo etapas, responsabilidades e artefatos resultantes; [F1, q2801, q2801ext[A]]
- IR2: Resposta e evidência sobre papéis e responsabilidades nas contratações de TIC; [F1, F2, q2801, q2801evi]
- IR3: Resposta sobre disponibilização de modelos e artefatos padronizados para o planejamento das contratações de TIC; [F1, q2801, q2801ext[B]]
- IR4: Resposta sobre submissão obrigatória das contratações de TIC à análise prévia e aprovação técnica da área de TIC; [F1, q2804[A]]
- IR5: Evidência específica sobre aprovação técnica da área de TIC; [F2, q2804eviA]
- IR6: Resposta sobre alinhamento das contratações aos instrumentos de planejamento e ao Plano de Contratações Anual; [F1, q2804[B]]
- IR7: Resposta sobre equipe de planejamento formalmente designada e com participação técnica de TIC; [F1, q2804[C]]

criterios:
- id: C1
  descricao: >-
    Lei nº 14.133/2021, art. 11, parágrafo único: responsabilidade da alta administração pela governança das contratações, com processos, estruturas, gestão de riscos e controles internos.
  natureza_fundamento: norma_legal_vinculante
  apto_a_fundamentar_determinacao: true
- id: C2
  descricao: >-
    Lei nº 14.133/2021, arts. 12, VII e §1º, e 18, caput e §1º, II – a fase preparatória deve compatibilizar-se com o Plano de Contratações Anual, quando elaborado, e deve ser demonstrado o alinhamento da contratação com o planejamento da Administração.
  natureza_fundamento: norma_legal_vinculante
  apto_a_fundamentar_determinacao: true
- id: C3
  descricao: >-
    Lei nº 14.133/2021, art. 19, inciso IV: instituição de modelos de minutas de editais, termos de referência, contratos padronizados e demais documentos.
  natureza_fundamento: norma_legal_vinculante
  apto_a_fundamentar_determinacao: true
- id: C4
  descricao: >-
    Lei nº 14.133/2021, art. 7º, caput, incisos I a III e §1º: designação de agentes públicos para funções essenciais, observados atribuições, formação, segregação de funções e inexistência de vínculos que comprometam a atuação.
  natureza_fundamento: norma_legal_vinculante
  apto_a_fundamentar_determinacao: true
- id: C5
  descricao: >-
    COBIT 2019, BAI02.04 - Obter aprovação dos requisitos da solução: obter aprovação formal dos requisitos funcionais, técnicos, de segurança e de conformidade antes de prosseguir com a solução.
  natureza_fundamento: boa_pratica
  apto_a_fundamentar_determinacao: false
- id: C8
  descricao: >-
    Instrução Normativa SGD/ME nº 94/2022, arts. 2º, IV, 9º, 10, 11 e 12, §6º – referência de boa prática para estruturação da fase de planejamento das contratações de TIC, instituição da Equipe de Planejamento da Contratação e participação do integrante técnico da área de TIC, observada sua aplicação direta aos integrantes do SISP e as hipóteses de simplificação de procedimentos previstas na norma.
  natureza_fundamento: referencial_nao_vinculante
  apto_a_fundamentar_determinacao: false
- id: C9
  descricao: >-
    Acórdão TCE-RJ nº 44.490/2024-PLEN, itens III.7 e IV.9 – Determinações para estruturação do processo de planejamento anual das contratações, contemplando consolidação das demandas, participação das áreas, aprovação e publicidade do plano.
  natureza_fundamento: jurisprudencia_tce_rj
  apto_a_fundamentar_determinacao: true
- id: C10
  descricao: >-
    Acórdão nº 2.342/2016-TCU-Plenário, item 9.1.7 – Precedente quanto à definição, aprovação e formalização de processo de trabalho para o planejamento de cada contratação, com controles internos mínimos.
  natureza_fundamento: jurisprudencia_outro_orgao
  apto_a_fundamentar_determinacao: false
- id: C11
  descricao: >-
    Decreto Estadual nº 48.816/2023, no âmbito de aplicação do ato — referência específica para a fase preparatória das contratações; não é considerado, isoladamente, fundamento suficiente para determinar a composição mínima da equipe de planejamento.
  natureza_fundamento: norma_regulamentar_vinculante
  apto_a_fundamentar_determinacao: false
  publico: Poder Executivo Estadual
  aplica_se:
    segmentos: [EXECUTIVO_ESTADUAL]
- id: C12
  descricao: >-
    Resolução CNJ nº 468/2022, art. 7º — a equipe de planejamento da contratação de solução de TIC deve ser formalmente instituída e conter integrantes demandante, técnico e administrativo.
  natureza_fundamento: norma_regulamentar_vinculante
  apto_a_fundamentar_determinacao: true
  publico: Poder Judiciário Estadual
  aplica_se:
    segmentos: [JUDICIARIO_ESTADUAL]
- id: C13
  descricao: >-
    Resolução CNMP nº 283/2024, arts. 8º e 9º — a equipe de planejamento da contratação de solução de TIC deve ser instituída com integrante técnico, integrante requisitante e integrante administrativo.
  natureza_fundamento: norma_regulamentar_vinculante
  apto_a_fundamentar_determinacao: true
  publico: Ministério Público Estadual
  aplica_se:
    segmentos: [MINISTERIO_PUBLICO_ESTADUAL]
- id: C14
  descricao: >-
    IN PRODERJ/PRE nº 05/2024, arts. 1º, 4º a 8º, 11 e 28, Decreto Estadual nº 47.278/2020, art. 7º e Decreto Estadual nº 48.749/2023 — rito de planejamento com DOD, ETP, Riscos e TR, aprovação prévia técnica da área de TIC, anuência do PRODERJ e vedação de contratação fora do PEDTIC e PCA no Poder Executivo Estadual.
  natureza_fundamento: norma_regulamentar_vinculante
  apto_a_fundamentar_determinacao: true
  publico: Poder Executivo Estadual
  aplica_se:
    segmentos: [EXECUTIVO_ESTADUAL]
- id: C15
  descricao: >-
    Resolução CNJ nº 468/2022, arts. 4º a 7º, 10, 11, 14, 15 e 29 e Ato Normativo TJ nº 27/2022, arts. 5º e 6º — rito de planejamento das contratações de TIC, alinhamento ao PDTIC/PAC e assinatura técnica obrigatória da área de TIC no Poder Judiciário Estadual.
  natureza_fundamento: norma_regulamentar_vinculante
  apto_a_fundamentar_determinacao: true
  publico: Poder Judiciário Estadual
  aplica_se:
    segmentos: [JUDICIARIO_ESTADUAL]
- id: C16
  descricao: >-
    Resolução CNMP nº 283/2024, arts. 2º, 4º a 6º, 8º a 10, 16, 17, 20 e 33 e Resolução GPGJ nº 2.785/2026, art. 13, III — rito padronizado de contratação de TI, alinhamento ao PDTI/PAC e validação/subscrição técnica compulsória no Ministério Público Estadual.
  natureza_fundamento: norma_regulamentar_vinculante
  apto_a_fundamentar_determinacao: true
  publico: Ministério Público Estadual
  aplica_se:
    segmentos: [MINISTERIO_PUBLICO_ESTADUAL]

procedimentos:
- P1: Verificar, por meio da q2801 e das q2801ext[A] e [B], se o processo de planejamento das contratações de TIC possui etapas e responsabilidades definidas e artefatos padronizados; [IR1, IR2, IR3]
- P2: Validar, pelas evidências anexadas à q2801, a existência de fluxo, papéis, responsabilidades, modelos, manuais, checklists ou normativos orientativos; [IR1, IR2, IR3]
- P3: Verificar, por meio da q2804[A] e da q2804eviA, se as contratações de TIC são submetidas à análise prévia e aprovação técnica da área de TIC; [IR4, IR5]
- P4: Verificar, por meio da q2804[B], se as contratações de TIC estão alinhadas aos instrumentos de planejamento e ao Plano de Contratações Anual; [IR6]
- P5: Verificar, por meio da q2804[C], se a equipe de planejamento da contratação é formalmente designada e possui participação técnica de TIC; [IR7]

evidencias:
- E1: Resposta negativa ou insuficiente sobre processo formal e padronizado para contratações de TIC; [P1]
- E2: Ausência, desatualização ou insuficiência de evidências de fluxo, papéis, responsabilidades, modelos, manuais, checklists ou normativos orientativos; [P2]
- E3: Resposta negativa ou insuficiente sobre análise prévia e aprovação técnica da área de TIC; [P3]
- E4: Quando declarada a adoção da prática, ausência ou insuficiência de norma que estabeleça a análise e aprovação técnica da área de TIC ou de evidência de sua aplicação em caso concreto; [P3]
- E5: Resposta negativa ou insuficiente sobre aderência das contratações ao plano de TIC ou ao plano de contratações; [P4]
- E6: Resposta negativa ou insuficiente sobre equipe de planejamento formalmente designada e com participação técnica de TIC; [P5]

possiveis_achados:
- A6: Fragilidades na governança técnica da fase preparatória das contratações de TIC
  situacoes_encontradas:
  - S6.1:
      descricao: Inexistência ou fragilidade de processo formal e padronizado para o planejamento das contratações de TIC.
      severidade: alta
      itens_questionario: [q2801, q2801ext[A], q2801ext[B], q2801evi]
      regra_de_identificacao:
      - (q2801ext[A] != Sim) | (avaliacao_documental[q2801ext[A]] == Não conforme) | (q2801ext[B] != Sim) | (avaliacao_documental[q2801ext[B]] == Não conforme)
      referencias_matriz: [R6.1, R6.2, P1, E1, P2, E2]
      criterios: [C1, C3, C10]
      tipo_encaminhamento: Recomendação
      encaminhamento: formalize e padronize o processo de planejamento das contratações de TIC, definindo etapas, responsabilidades e artefatos aplicáveis, podendo adotar modelos institucionais ou centralizados já existentes e prevendo fluxos proporcionais à natureza, complexidade e risco da contratação
      variantes:
      - publico: Poder Executivo Estadual
        aplica_se:
          segmentos: [EXECUTIVO_ESTADUAL]
        criterios: [C1, C3, C14]
        tipo_encaminhamento: Determinação
      - publico: Poder Judiciário Estadual
        aplica_se:
          segmentos: [JUDICIARIO_ESTADUAL]
        criterios: [C1, C3, C15]
        tipo_encaminhamento: Determinação
      - publico: Ministério Público Estadual
        aplica_se:
          segmentos: [MINISTERIO_PUBLICO_ESTADUAL]
        criterios: [C1, C3, C16]
        tipo_encaminhamento: Determinação
  - S6.2:
      descricao: Contratações de TIC sem análise prévia e aprovação técnica da área de TIC.
      severidade: alta
      itens_questionario: [q2804[A], q2804eviA]
      regra_de_identificacao:
      - (q2804[A] != Sim) | (avaliacao_documental[q2804[A]] == Não conforme)
      referencias_matriz: [R6.3, P3, E3, E4]
      criterios: [C1, C5, C8]
      tipo_encaminhamento: Recomendação
      encaminhamento: estabeleça a submissão das contratações de TIC à análise prévia da área de TIC, de modo a verificar a compatibilidade da solução com os padrões tecnológicos, os requisitos institucionais e a arquitetura existente, admitindo procedimentos simplificados e proporcionais à natureza, ao risco e ao valor da contratação, preservada análise técnica compatível
      variantes:
      - publico: Poder Executivo Estadual
        aplica_se:
          segmentos: [EXECUTIVO_ESTADUAL]
        criterios: [C1, C14]
        tipo_encaminhamento: Determinação
      - publico: Poder Judiciário Estadual
        aplica_se:
          segmentos: [JUDICIARIO_ESTADUAL]
        criterios: [C1, C15]
        tipo_encaminhamento: Determinação
      - publico: Ministério Público Estadual
        aplica_se:
          segmentos: [MINISTERIO_PUBLICO_ESTADUAL]
        criterios: [C1, C16]
        tipo_encaminhamento: Determinação
  - S6.3:
      descricao: Contratações de TIC sem alinhamento ao planejamento de TIC e ao Plano de Contratações Anual.
      severidade: alta
      itens_questionario: [q2804[B]]
      regra_de_identificacao:
      - (q2804[B] != Sim)
      referencias_matriz: [R6.3, P4, E5]
      criterios: [C1, C2, C9]
      tipo_encaminhamento: Determinação
      encaminhamento: assegure que as contratações de TIC sejam compatíveis com os instrumentos de planejamento de TIC e, quando elaborado, com o Plano de Contratações Anual, promovendo os ajustes ou justificativas cabíveis nos casos excepcionais
      variantes:
      - publico: Poder Executivo Estadual
        aplica_se:
          segmentos: [EXECUTIVO_ESTADUAL]
        criterios: [C1, C2, C9, C14]
        tipo_encaminhamento: Determinação
      - publico: Poder Judiciário Estadual
        aplica_se:
          segmentos: [JUDICIARIO_ESTADUAL]
        criterios: [C1, C2, C9, C15]
        tipo_encaminhamento: Determinação
      - publico: Ministério Público Estadual
        aplica_se:
          segmentos: [MINISTERIO_PUBLICO_ESTADUAL]
        criterios: [C1, C2, C9, C16]
        tipo_encaminhamento: Determinação
  - S6.4:
      descricao: Contratações de TIC sem designação de equipe de planejamento com integrante técnico da área de TIC.
      severidade: alta
      itens_questionario: [q2804[C]]
      regra_de_identificacao:
      - (q2804[C] != Sim)
      referencias_matriz: [R6.4, P5, E6]
      criterios: [C1, C4, C8]
      tipo_encaminhamento: Recomendação
      encaminhamento: designe formalmente equipe de planejamento para as contratações de TIC, atentando-se, minimamente, em assegurar a participação de integrante da área requisitante e da área técnica de TIC, com definição das responsabilidades de seus integrantes
      variantes:
      - publico: Poder Executivo Estadual
        aplica_se:
          segmentos: [EXECUTIVO_ESTADUAL]
          naturezas: [ADMINISTRACAO_DIRETA, AUTARQUIA, FUNDACAO]
        criterios: [C1, C4, C11]
      - publico: Poder Judiciário Estadual
        aplica_se:
          segmentos: [JUDICIARIO_ESTADUAL]
        criterios: [C1, C4, C12]
        tipo_encaminhamento: Determinação
      - publico: Ministério Público Estadual
        aplica_se:
          segmentos: [MINISTERIO_PUBLICO_ESTADUAL]
        criterios: [C1, C4, C13]
        tipo_encaminhamento: Determinação

---

## Questão Transversal - Diagnóstico do iGovTI 2026

natureza: levantamento
gera_achado: false
questao: QTD. Qual é o grau de adoção das práticas de governança e gestão de TIC pelas organizações avaliadas no iGovTI 2026, globalmente e por componente e dimensão?

subquestoes:
- Como se distribuem os resultados do iGovTI 2026 entre as faixas de maturidade definidas na metodologia?
- Qual é o desempenho agregado das organizações nos componentes Governança de TIC e Gestão de TIC e nas dimensões que compõem o índice?
- Há diferenças relevantes nos resultados entre segmentos institucionais com quantidade suficiente de organizações para análise?
- Quais práticas avaliadas apresentam os maiores e os menores graus de adoção?

fontes_de_informacao:
- F1: Respostas válidas e processadas do questionário eletrônico iGovTI 2026.
- F2: Metodologia de cálculo e estrutura do índice iGovTI 2026.
- F3: Resultados individuais e agregados calculados para o iGovTI 2026, seus componentes e suas dimensões.
- F4: Cadastro das organizações avaliadas, com os atributos institucionais necessários aos recortes analíticos.

informacoes_requeridas:
- IR1: Universo de organizações avaliadas, respondentes válidos e respectivos atributos institucionais; [F1, F4]
- IR2: Resultado individual do iGovTI 2026, respectiva faixa de maturidade e resultados dos componentes Governança de TIC e Gestão de TIC; [F2, F3]
- IR3: Resultados individuais e agregados das dimensões Planejamento de TIC, Gestão de serviços de TIC, Riscos de TI e de segurança da informação, Estrutura de segurança da informação, Processos de segurança da informação e Gestão de soluções de TIC; [F2, F3]
- IR4: Pontuações normalizadas das práticas e dos itens que compõem o iGovTI 2026, com seus denominadores e regras de tratamento; [F1, F2, F3]
- IR5: Registros de completude, consistência, ajustes e limitações relevantes das bases utilizadas no cálculo; [F1, F2, F3]

procedimentos:
- P1: Validar o universo de organizações avaliadas e calcular ou conferir, conforme a metodologia do iGovTI 2026, o índice, a faixa de maturidade, os componentes e as dimensões de cada organização; [IR1, IR2, IR3]
- P2: Consolidar a distribuição das organizações por faixa de maturidade e calcular medidas descritivas do iGovTI 2026 para o universo avaliado; [IR1, IR2]
- P3: Consolidar e comparar os resultados dos componentes Governança de TIC e Gestão de TIC e das seis dimensões que compõem o índice; [IR2, IR3]
- P4: Segregar os resultados por Poder, esfera, natureza institucional ou outro segmento pertinente, quando a quantidade e a composição das organizações permitirem comparação descritiva adequada; [IR1, IR2, IR3]
- P5: Identificar as práticas e os itens com maiores e menores graus de adoção, informando a medida utilizada, o número de respostas válidas e o tratamento das respostas não aplicáveis; [IR4]
- P6: Verificar a completude e a consistência das bases e registrar as limitações que afetem o cálculo ou a interpretação dos resultados; [IR5]

evidencias:
- E1: Relação consolidada das organizações avaliadas, dos respondentes válidos e dos atributos institucionais utilizados na análise; [P1]
- E2: Memória de cálculo ou base de resultados com o iGovTI 2026, a faixa de maturidade, os componentes e as dimensões de cada organização; [P1]
- E3: Tabelas, gráficos ou painéis com a distribuição por faixa de maturidade e as medidas descritivas do iGovTI 2026; [P2]
- E4: Tabelas, gráficos ou painéis com os resultados agregados dos componentes e das dimensões do índice; [P3]
- E5: Quadros comparativos por segmento institucional, acompanhados do quantitativo de organizações de cada grupo; [P4]
- E6: Relação das práticas e dos itens com maiores e menores graus de adoção, acompanhada dos respectivos percentuais, pontuações ou medidas de síntese e denominadores; [P5]
- E7: Registro das verificações de completude e consistência e das limitações relevantes para interpretação dos resultados; [P6]

o_que_a_analise_permite_dizer:
- Qual é o grau de adoção das práticas de governança e gestão de TIC no universo avaliado em 2026, segundo o índice e as faixas de maturidade definidas na metodologia.
- Como se comportam, em termos agregados, os componentes Governança de TIC e Gestão de TIC e as seis dimensões que compõem o iGovTI 2026.
- Quais segmentos institucionais apresentam resultados distintos, quando houver quantidade e composição adequadas para comparação descritiva.
- Quais práticas e itens do questionário concentram os maiores e os menores graus de adoção.

limitacoes_e_cautelas:
- A questão tem caráter de levantamento e diagnóstico agregado, não gerando achado ou encaminhamento individual por organização.
- O iGovTI 2026 mensura o grau de adoção segundo as respostas e as regras da metodologia; o resultado não comprova, isoladamente, a efetividade das práticas nem conformidade jurídica.
- Os resultados agregados não substituem a avaliação individualizada das fragilidades abrangidas pelas Questões 1 a 6.
- Médias e demais medidas de síntese devem ser apresentadas com a distribuição dos resultados, para evitar que ocultem diferenças relevantes entre as organizações.
- Comparações entre segmentos institucionais devem considerar o tamanho, a composição e a cobertura de cada grupo e não devem ser tratadas como inferência causal.
- Práticas ou itens com universos de respostas distintos devem ser comparados somente com indicação dos respectivos denominadores e do tratamento das respostas não aplicáveis.

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
- O atendimento dos encaminhamentos anteriores deve ser analisado conforme o conteúdo de cada encaminhamento, as evidências disponíveis e a compatibilidade com os dados coletados no iGovTI 2026.\n