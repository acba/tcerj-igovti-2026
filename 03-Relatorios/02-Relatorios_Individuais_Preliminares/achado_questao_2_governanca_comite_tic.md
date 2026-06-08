{% set nome_achado = 'Governança de TIC insuficiente para avaliar, dirigir e monitorar a tecnologia da informação.' %}
{% set achado = auditado.get_achado_por_nome(nome_achado) %}
{% if achado %}

\newpage

## Achado {{ achado.numero }} – {{ achado.nome }}

### Critérios
* COBIT 2019, EDM01.02 - Dirigir o sistema de governança: orientar estruturas, princípios, processos e práticas de governança para assegurar que a TI apoie os objetivos organizacionais;
* COBIT 2019, MEA01.04 - Avaliar o desempenho: monitorar e avaliar periodicamente o desempenho e a conformidade da TI em relação a objetivos, indicadores, metas e expectativas das partes interessadas;
* Decreto nº 12.198/2024, art. 5º - Instituição do CGD, colegiado responsável por definir diretrizes e estratégias sobre uso de recursos digitais nos órgãos e entidades da administração pública federal direta, autárquica e fundacional;
* Acórdão TCE-RJ 44.490/2024-PLEN, item II.1: necessidade de estrutura de governança de TI, especialmente Comitê de Tecnologia da Informação ou instância equivalente, com participação de áreas relevantes, responsabilidade de alinhar as ações de TI aos objetivos institucionais, priorizar investimentos e monitorar o desempenho da TI com base em indicadores e metas;
* COBIT 2019, APO01.05 - Estabelecer papéis e responsabilidades: definir, comunicar e manter papéis e responsabilidades relacionados à governança e gestão de TI.

### Evidências
{% for evidencia in achado.evidencias %}
* {{ evidencia }};
{% endfor %}

### Situação encontrada
{% set situacao_modelo = 'Ausência ou insuficiência de modelo básico de governança e gestão de TIC com papéis, responsabilidades, objetivos, indicadores, metas ou acompanhamento.' %}
{% set situacao_comite_formal = 'Comitê de TIC ou instância equivalente não instituído formalmente.' %}
{% set situacao_comite_atuacao = 'Comitê de TIC ou instância equivalente sem evidências suficientes de atuação efetiva.' %}
Conclui-se que o(a) {{ auditado.sigla }} não demonstrou atender integralmente ao requisito de possuir mecanismos básicos de governança de TIC estabelecidos pela alta administração, incluindo modelo de governança e gestão, objetivos, indicadores, metas e Comitê de TIC ou instância equivalente formalmente instituída e atuante, pois a Equipe de Auditoria identificou fragilidades{% if situacao_modelo in achado.situacoes_encontradas %} no modelo básico de governança e gestão de TIC{% endif %}{% if situacao_comite_formal in achado.situacoes_encontradas %}{% if situacao_modelo in achado.situacoes_encontradas %}, {% else %} {% endif %}na instituição formal do Comitê de TIC ou instância equivalente{% endif %}{% if situacao_comite_atuacao in achado.situacoes_encontradas %}{% if situacao_modelo in achado.situacoes_encontradas or situacao_comite_formal in achado.situacoes_encontradas %} e {% else %} {% endif %}na atuação efetiva do Comitê de TIC ou instância equivalente{% endif %}.{% if situacao_modelo in achado.situacoes_encontradas %} A ausência ou insuficiência de modelo básico de governança e gestão de TIC contraria os critérios de direção do sistema de governança e avaliação de desempenho, previstos no COBIT 2019, EDM01.02 e MEA01.04, bem como o Acórdão TCE-RJ 44.490/2024-PLEN, item II.1, e pode gerar baixa clareza sobre papéis, responsabilidades, objetivos, indicadores, metas e acompanhamento do desempenho da TIC.{% endif %}{% if situacao_comite_formal in achado.situacoes_encontradas %} A não instituição formal do Comitê de TIC ou instância equivalente contraria o Decreto nº 12.198/2024, art. 5º, o Acórdão TCE-RJ 44.490/2024-PLEN, item II.1, e o critério de definição de papéis e responsabilidades do COBIT 2019, APO01.05, podendo impedir a existência de instância colegiada para deliberação sobre prioridades, projetos, riscos, serviços, orçamento e contratações de TIC.{% endif %}{% if situacao_comite_atuacao in achado.situacoes_encontradas %} A ausência de evidências suficientes de atuação efetiva do Comitê de TIC ou instância equivalente contraria os critérios de avaliação de desempenho e funcionamento de estrutura colegiada de governança, previstos no COBIT 2019, MEA01.04, no Decreto nº 12.198/2024, art. 5º, e no Acórdão TCE-RJ 44.490/2024-PLEN, item II.1, podendo comprometer a deliberação efetiva sobre prioridades, projetos, riscos, serviços, orçamento e contratações de TIC.{% endif %}

A governança de TIC compreende o conjunto de estruturas, papéis, responsabilidades, diretrizes e mecanismos de acompanhamento por meio dos quais a alta administração avalia, dirige e monitora o uso da tecnologia da informação. Sua finalidade é assegurar que os recursos de TIC apoiem os objetivos institucionais, sejam priorizados de forma transparente e tenham desempenho acompanhado com base em critérios objetivos.

Sob a perspectiva da Questão 2 da matriz de planejamento, a existência de governança mínima exige, ao menos, que a alta administração estabeleça modelo básico de governança e gestão de TIC, com papéis, responsabilidades, objetivos, indicadores, metas ou forma de acompanhamento, e que exista Comitê de TIC ou instância equivalente formalmente instituída e atuante.

Os critérios adotados pela matriz indicam que a organização deve orientar estruturas, princípios, processos e práticas de governança, monitorar o desempenho e a conformidade da TIC, definir papéis e responsabilidades e instituir instância colegiada capaz de alinhar ações de TIC aos objetivos institucionais, priorizar investimentos e acompanhar desempenho com base em indicadores e metas[^explica_governanca_tic_cobit]. Esses requisitos também se conectam à necessidade de instância colegiada de governança digital, conforme referência do Decreto nº 12.198/2024[^explica_decreto_cgd], e ao entendimento expresso no Acórdão TCE-RJ 44.490/2024-PLEN[^explica_acordao_tcerj_governanca].

Com base na análise das respostas aos itens q1001, q1002, q1001ext[E] e q1001ext[F] do questionário aplicado e da avaliação das evidências anexadas aos itens q1001evi e q1002evi, conforme apontado na seção de Evidências, a Equipe de Auditoria constatou as seguintes deficiências na governança de TIC da organização:

{% for situacao in achado.situacoes_encontradas %}
* **{{ situacao }}**
{% endfor %}

Essas situações ensejaram o presente achado e serão detalhadas nas seções subsequentes.

[^explica_governanca_tic_cobit]: No COBIT 2019, o sistema de governança deve ser dirigido por estruturas, princípios, processos e práticas que assegurem que a TI apoie os objetivos organizacionais, com papéis e responsabilidades definidos e desempenho periodicamente monitorado.

[^explica_decreto_cgd]: O Decreto nº 12.198/2024 disciplina, no âmbito federal, o Comitê de Governança Digital como colegiado responsável por diretrizes e estratégias sobre o uso de recursos digitais, servindo como referência normativa para a estruturação de instâncias colegiadas de governança digital.

[^explica_acordao_tcerj_governanca]: O Acórdão TCE-RJ 44.490/2024-PLEN, item II.1, registra a necessidade de estrutura de governança de TI, especialmente Comitê de Tecnologia da Informação ou instância equivalente, com participação de áreas relevantes e atribuições de alinhamento, priorização e monitoramento.

{% set situacao = 'Ausência ou insuficiência de modelo básico de governança e gestão de TIC com papéis, responsabilidades, objetivos, indicadores, metas ou acompanhamento.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Modelo básico de governança e gestão de TIC

O modelo básico de governança e gestão de TIC deve explicitar como a alta administração orienta, acompanha e responsabiliza a atuação da tecnologia da informação. Esse modelo deve conter, ao menos, diretrizes, papéis, responsabilidades, objetivos, indicadores, metas e forma de acompanhamento periódico.

O COBIT 2019, no objetivo EDM01.02, orienta a direção do sistema de governança por meio de estruturas, princípios, processos e práticas que assegurem que a TI apoie os objetivos organizacionais. Em complemento, o objetivo MEA01.04 trata do monitoramento e da avaliação periódica do desempenho e da conformidade da TI em relação a objetivos, indicadores, metas e expectativas das partes interessadas.

No contexto da Questão 2 da matriz de planejamento, a existência e a suficiência desse modelo devem ser demonstradas por políticas, diretrizes, definição de papéis e responsabilidades, objetivos, indicadores, metas, relatórios de acompanhamento, medições de desempenho ou instrumentos equivalentes.

Quando a organização não estabelece modelo básico de governança e gestão de TIC, ou quando os documentos apresentados são insuficientes para demonstrar papéis, responsabilidades, objetivos, indicadores, metas ou acompanhamento, há risco de baixa clareza sobre a direção da TIC e sobre os resultados esperados da área.

Diante disso, __será proposta recomendação para que a alta administração estabeleça modelo básico de governança e gestão de TIC, com papéis, responsabilidades, objetivos, indicadores, metas e forma de acompanhamento periódico.__

{% endif %}

{% set situacao = 'Comitê de TIC ou instância equivalente não instituído formalmente.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Instituição formal do Comitê de TIC ou instância equivalente

O Comitê de TIC ou instância equivalente é mecanismo relevante para estruturar a participação da alta administração e das áreas interessadas nas decisões de tecnologia da informação. Sua formalização permite definir composição, competências, periodicidade mínima, forma de deliberação e responsabilidades pelo acompanhamento das decisões.

O Decreto nº 12.198/2024, art. 5º, adotado como critério de referência pela matriz, prevê colegiado responsável por definir diretrizes e estratégias sobre uso de recursos digitais no âmbito federal. O Acórdão TCE-RJ 44.490/2024-PLEN, item II.1, reforça a necessidade de estrutura de governança de TI, especialmente Comitê de Tecnologia da Informação ou instância equivalente, com participação de áreas relevantes.

Em alinhamento, o COBIT 2019, no objetivo APO01.05, orienta a definição, comunicação e manutenção de papéis e responsabilidades relacionados à governança e gestão de TI.

No contexto da Questão 2, a instituição formal do Comitê deve ser demonstrada por ato, norma, regimento, portaria ou documento equivalente que estabeleça a instância, sua composição, competências, periodicidade ou forma de deliberação.

A ausência de instituição formal do Comitê de TIC ou instância equivalente fragiliza a governança, pois pode inexistir foro institucional para deliberação sobre prioridades, projetos, riscos, serviços, orçamento e contratações de TIC.

Diante disso, __será proposta recomendação para que a organização institua formalmente Comitê de TIC ou instância equivalente, definindo composição, competências, periodicidade mínima, forma de registro das deliberações e acompanhamento dos encaminhamentos.__

{% endif %}

{% set situacao = 'Comitê de TIC ou instância equivalente sem evidências suficientes de atuação efetiva.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Atuação efetiva do Comitê de TIC ou instância equivalente

A mera instituição formal do Comitê de TIC ou instância equivalente não é suficiente para assegurar governança efetiva. É necessário que a instância funcione de modo regular, com reuniões, pautas, atas, registros de deliberação, encaminhamentos e acompanhamento das decisões tomadas.

O COBIT 2019, no objetivo MEA01.04, exige monitoramento e avaliação periódica do desempenho e da conformidade da TI. O Acórdão TCE-RJ 44.490/2024-PLEN, item II.1, também aponta a responsabilidade de alinhar as ações de TI aos objetivos institucionais, priorizar investimentos e monitorar o desempenho da TI com base em indicadores e metas.

No contexto da Questão 2, a atuação efetiva do Comitê deve ser demonstrada por atas, pautas, listas de presença, registros de deliberação, decisões, encaminhamentos ou acompanhamento de pendências. A ausência desses registros impede verificar se a instância colegiada exerce, de fato, seu papel de avaliação, direção e monitoramento da TIC.

Essa deficiência pode fazer com que decisões relevantes sobre prioridades, projetos, riscos, serviços, orçamento e contratações de TIC não sejam submetidas a deliberação colegiada ou não tenham acompanhamento formal.

Diante disso, __será proposta recomendação para que a organização assegure o funcionamento efetivo do Comitê de TIC ou instância equivalente, com reuniões periódicas, atas, deliberações, encaminhamentos e acompanhamento das decisões sobre prioridades, projetos, riscos, serviços, orçamento e contratações de TIC.__

{% endif %}

#### Conclusão

As fragilidades identificadas na governança de TIC comprometem a capacidade da organização de avaliar, dirigir e monitorar a tecnologia da informação de forma alinhada aos objetivos institucionais. A ausência ou insuficiência de modelo básico de governança, a inexistência formal de Comitê de TIC ou instância equivalente e a falta de evidências de atuação efetiva reduzem a clareza de responsabilidades, a qualidade da priorização e a capacidade de acompanhamento das decisões de TIC.

Diante das situações apresentadas, será sugerida proposta de encaminhamento à organização para que promova a adequação de seus mecanismos de governança de TIC, alinhando-os aos critérios previstos no COBIT 2019, no Decreto nº 12.198/2024 e no Acórdão TCE-RJ 44.490/2024-PLEN.

### Propostas de Encaminhamento
{% for e in achado.encaminhamentos %}
* **Comunicação com {{ e.tipo }}** para que {{ e.encaminhamento }};
{% endfor %}

{# Final do Achado - Governança e Comitê de TIC #}
{% endif %}
