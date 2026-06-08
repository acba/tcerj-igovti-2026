{% set nome_achado = 'Planejamento de TIC inexistente, insuficiente, desatualizado ou desconectado da gestão, do orçamento e das contratações' %}
{% set achado = auditado.get_achado_por_nome(nome_achado) %}
{% if achado %}

\newpage

## Achado {{ achado.numero }} – {{ achado.nome }}

### Critérios
* COBIT 2019, APO02.05 - Definir o plano e o roteiro estratégico: estabelecer plano e roteiro de TIC que traduzam a estratégia em iniciativas, prioridades, recursos, dependências, prazos e benefícios esperados;
* COBIT 2019, APO06.03 - Criar e manter orçamentos: elaborar e manter orçamento de TIC alinhado ao portfólio, ao planejamento e às prioridades aprovadas;
* Acórdão 1.411/2014-TCU-Plenário, item 9.1.6 e subitens 9.1.6.1 a 9.1.6.4: necessidade de instituir formalmente plano diretor de TI, contemplando desdobramento de diretrizes estratégicas, vinculação das ações de TI a indicadores e metas de negócio, vinculação das ações de TI a indicadores e metas de serviços ao cidadão e vinculação das ações priorizadas ao orçamento de TI;
* Acórdão TCE-RJ 44.490/2024-PLEN, item II.3 e subitens II.3.1 a II.3.5: necessidade de estabelecer processo estruturado, com participação de representantes das principais secretarias, para elaborar, manter e revisar periodicamente o PDTI, contemplando objetivos, indicadores e metas de TI alinhados aos objetivos de negócio, riscos que possam impactar objetivos e metas, projetos, aquisições e ações necessárias, alocação de recursos e ações de divulgação e monitoramento do PDTI após aprovação pela autoridade máxima.

### Evidências
{% for evidencia in achado.evidencias %}
* {{ evidencia }};
{% endfor %}

### Situação encontrada
{% set situacao_processo = 'Inexistência ou fragilidade do processo formal de planejamento de TIC.' %}
{% set situacao_plano = 'Inexistência, desatualização, ausência de vigência ou ausência de aprovação formal do plano de TIC.' %}
{% set situacao_conteudo = 'Plano de TIC sem conteúdo mínimo suficiente para orientar a gestão.' %}
{% set situacao_alinhamento = 'Plano de TIC sem alinhamento adequado ao planejamento institucional.' %}
{% set situacao_integracao = 'Plano de TIC sem integração adequada com orçamento, plano de contratações, projetos ou contratações de TIC.' %}
{% set situacao_acompanhamento = 'Ausência de acompanhamento, revisão ou atualização periódica do plano de TIC.' %}
Conclui-se que o(a) {{ auditado.sigla }} não demonstrou utilizar o planejamento de TIC como instrumento efetivo de gestão, com processo formal, plano vigente, aprovação competente, alinhamento institucional, integração com orçamento e contratações e acompanhamento periódico, pois a Equipe de Auditoria identificou fragilidades nos seguintes aspectos:{% if situacao_processo in achado.situacoes_encontradas %} processo formal de planejamento de TIC;{% endif %}{% if situacao_plano in achado.situacoes_encontradas %} existência, vigência ou aprovação formal do plano de TIC;{% endif %}{% if situacao_conteudo in achado.situacoes_encontradas %} conteúdo mínimo do plano de TIC;{% endif %}{% if situacao_alinhamento in achado.situacoes_encontradas %} alinhamento do plano ao planejamento institucional;{% endif %}{% if situacao_integracao in achado.situacoes_encontradas %} integração com orçamento, plano de contratações, projetos ou contratações de TIC;{% endif %}{% if situacao_acompanhamento in achado.situacoes_encontradas %} acompanhamento, revisão ou atualização periódica do plano de TIC;{% endif %}.{% if situacao_processo in achado.situacoes_encontradas %} A inexistência ou fragilidade do processo formal contraria os critérios de planejamento estratégico de TIC previstos no COBIT 2019, APO02.05, no Acórdão 1.411/2014-TCU-Plenário e no Acórdão TCE-RJ 44.490/2024-PLEN, podendo levar à atuação reativa e sem critérios objetivos de seleção e priorização de iniciativas.{% endif %}{% if situacao_plano in achado.situacoes_encontradas %} A inexistência, desatualização, ausência de vigência ou ausência de aprovação formal do plano de TIC contraria os mesmos critérios de formalização e aprovação do planejamento de TIC, podendo deixar a gestão, os projetos, o orçamento e as contratações sem direcionamento formal.{% endif %}{% if situacao_conteudo in achado.situacoes_encontradas %} A insuficiência de conteúdo mínimo contraria os critérios de definição de plano e roteiro estratégico, com objetivos, iniciativas, responsáveis, prazos, metas ou indicadores, e pode reduzir a clareza sobre prioridades e responsabilidades.{% endif %}{% if situacao_alinhamento in achado.situacoes_encontradas %} A falta de alinhamento ao planejamento institucional contraria os critérios que exigem desdobramento de diretrizes estratégicas e vinculação das ações de TIC aos objetivos de negócio, podendo resultar em iniciativas de baixo valor para a organização.{% endif %}{% if situacao_integracao in achado.situacoes_encontradas %} A ausência de integração com orçamento, plano de contratações, projetos ou contratações contraria o COBIT 2019, APO06.03, o Acórdão 1.411/2014-TCU-Plenário e o Acórdão TCE-RJ 44.490/2024-PLEN, podendo gerar aquisições reativas, não priorizadas ou desalinhadas.{% endif %}{% if situacao_acompanhamento in achado.situacoes_encontradas %} A ausência de acompanhamento, revisão ou atualização periódica contraria os critérios de manutenção e monitoramento do PDTI, podendo manter metas, iniciativas e prioridades incompatíveis com mudanças institucionais, orçamentárias ou tecnológicas.{% endif %}

O planejamento de TIC é instrumento fundamental para traduzir diretrizes institucionais em iniciativas, prioridades, recursos, prazos, responsáveis e resultados esperados. Sua ausência ou fragilidade reduz a capacidade da organização de direcionar investimentos, selecionar demandas, coordenar projetos e alinhar contratações às necessidades institucionais.

Sob a perspectiva da Questão 3 da matriz de planejamento, a organização deve executar processo formal de planejamento, contar com plano de TIC vigente e aprovado, assegurar participação das áreas demandantes, definir conteúdo mínimo, alinhar o plano ao planejamento institucional, integrá-lo ao orçamento e às contratações e acompanhá-lo periodicamente.

Os critérios adotados pela matriz indicam que o planejamento de TIC deve estabelecer plano e roteiro estratégico, manter orçamento alinhado ao portfólio e às prioridades aprovadas, vincular ações de TIC a indicadores, metas e orçamento e contemplar processo estruturado de elaboração, manutenção e revisão periódica do PDTI[^explica_planejamento_tic].

Com base na análise das respostas aos itens q2101, q2101ext[A], q2102, q2102ext[A], q2102ext[C], q2102ext[D], q2102ext[E], q2802ext[C], q2802ext[D] e q2804[B] do questionário aplicado e da avaliação das evidências anexadas aos itens q2101evi, q2102evi e q2802evi, conforme apontado na seção de Evidências, a Equipe de Auditoria constatou as seguintes deficiências no planejamento de TIC da organização:

{% for situacao in achado.situacoes_encontradas %}
* **{{ situacao }}**
{% endfor %}

Essas situações ensejaram o presente achado e serão detalhadas nas seções subsequentes.

[^explica_planejamento_tic]: Os critérios de planejamento de TIC adotados pela matriz convergem para a necessidade de plano formal, aprovado, vigente, alinhado à estratégia institucional, integrado ao orçamento e às contratações e acompanhado periodicamente.

{% set situacao = 'Inexistência ou fragilidade do processo formal de planejamento de TIC.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Processo formal de planejamento de TIC

O processo formal de planejamento de TIC deve definir etapas, responsáveis, participação das áreas demandantes e critérios mínimos de priorização. Esse processo é necessário para que o planejamento deixe de ser uma atividade eventual e passe a constituir rotina institucional de identificação, seleção, priorização e acompanhamento de demandas de tecnologia.

O COBIT 2019, no objetivo APO02.05, orienta a definição de plano e roteiro estratégico de TIC que traduzam a estratégia em iniciativas, prioridades, recursos, dependências, prazos e benefícios esperados. O Acórdão TCE-RJ 44.490/2024-PLEN, item II.3, também aponta a necessidade de processo estruturado, com participação de representantes das principais secretarias, para elaborar, manter e revisar periodicamente o PDTI.

No contexto da Questão 3, o processo deve ser demonstrado por norma, procedimento, guia ou instrumento equivalente que discipline a elaboração, revisão, aprovação e acompanhamento do planejamento de TIC.

A inexistência ou fragilidade desse processo expõe a organização à atuação reativa, sem critérios objetivos de seleção e priorização de iniciativas.

Diante disso, __será proposta recomendação para que a organização institua processo formal de planejamento de TIC, com etapas, responsáveis, participação das áreas demandantes e critérios mínimos de priorização.__

{% endif %}

{% set situacao = 'Inexistência, desatualização, ausência de vigência ou ausência de aprovação formal do plano de TIC.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Existência, vigência e aprovação do plano de TIC

O plano de TIC deve estar formalmente instituído, vigente e aprovado pela instância competente, de modo a orientar a gestão, os projetos, os investimentos e as contratações de tecnologia da informação.

O Acórdão 1.411/2014-TCU-Plenário e o Acórdão TCE-RJ 44.490/2024-PLEN reforçam a necessidade de plano diretor ou instrumento equivalente formalmente instituído, aprovado e capaz de orientar as ações de TIC.

No contexto da Questão 3, a existência, vigência e aprovação do plano devem ser demonstradas por documento vigente e ato de aprovação, ou instrumento equivalente, compatível com o porte e as necessidades da organização.

Quando o plano é inexistente, desatualizado, sem vigência ou sem aprovação formal, a organização fica sem direcionamento institucional válido para a gestão, os projetos, o orçamento e as contratações de TIC.

Diante disso, __será proposta recomendação para que a organização elabore, aprove e mantenha vigente plano de TIC compatível com seu porte, suas prioridades institucionais e sua capacidade de execução.__

{% endif %}

{% set situacao = 'Plano de TIC sem conteúdo mínimo suficiente para orientar a gestão.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Conteúdo mínimo do plano de TIC

O plano de TIC deve conter elementos suficientes para orientar a gestão e permitir acompanhamento objetivo de sua execução. Esses elementos incluem, no mínimo, objetivos, iniciativas priorizadas, responsáveis, prazos, metas ou indicadores.

O COBIT 2019, APO02.05, exige que o plano e o roteiro estratégico traduzam a estratégia em iniciativas, prioridades, recursos, dependências, prazos e benefícios esperados. O Acórdão TCE-RJ 44.490/2024-PLEN também prevê que o PDTI contemple objetivos, indicadores e metas de TI alinhados aos objetivos de negócio, riscos, projetos, aquisições, alocação de recursos e ações de monitoramento.

Na ausência desses elementos mínimos, o plano perde capacidade de orientar decisões e de permitir acompanhamento efetivo, pois não explicita suficientemente o que será feito, por quem, em que prazo e com quais critérios de sucesso.

Diante disso, __será proposta recomendação para que o plano de TIC contenha, no mínimo, objetivos, iniciativas priorizadas, responsáveis, prazos, metas ou indicadores de acompanhamento.__

{% endif %}

{% set situacao = 'Plano de TIC sem alinhamento adequado ao planejamento institucional.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Alinhamento ao planejamento institucional

O plano de TIC deve demonstrar como suas iniciativas apoiam os objetivos institucionais, as diretrizes superiores e as necessidades das áreas finalísticas e administrativas.

O Acórdão 1.411/2014-TCU-Plenário exige o desdobramento de diretrizes estratégicas e a vinculação das ações de TI a indicadores e metas de negócio. O Acórdão TCE-RJ 44.490/2024-PLEN também prevê objetivos, indicadores e metas de TI alinhados aos objetivos de negócio.

Quando o plano de TIC não explicita esse alinhamento, há risco de execução de iniciativas tecnológicas com baixo valor institucional, desconectadas das prioridades da organização e das necessidades dos usuários internos e externos.

Diante disso, __será proposta recomendação para que a organização revise o plano de TIC para explicitar seu alinhamento ao planejamento institucional, às diretrizes superiores e às necessidades das áreas finalísticas e administrativas.__

{% endif %}

{% set situacao = 'Plano de TIC sem integração adequada com orçamento, plano de contratações, projetos ou contratações de TIC.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Integração com orçamento, plano de contratações e contratações de TIC

O planejamento de TIC deve ser integrado à proposta orçamentária, ao plano de contratações, aos projetos e às contratações executadas. Essa integração é necessária para que as iniciativas priorizadas tenham suporte financeiro, sejam convertidas em contratações coerentes e possam ser acompanhadas ao longo da execução.

O COBIT 2019, APO06.03, orienta a criação e manutenção de orçamento de TIC alinhado ao portfólio, ao planejamento e às prioridades aprovadas. O Acórdão 1.411/2014-TCU-Plenário também exige vinculação das ações priorizadas ao orçamento de TI, e o Acórdão TCE-RJ 44.490/2024-PLEN prevê projetos, aquisições, ações necessárias e alocação de recursos no PDTI.

A ausência de integração entre planejamento, orçamento e contratações aumenta o risco de aquisições reativas, não priorizadas ou desalinhadas às necessidades institucionais.

Diante disso, __será proposta recomendação para que a organização vincule o plano de TIC à proposta orçamentária, ao plano de contratações e às contratações de TIC executadas, priorizando demandas conforme relevância, risco e capacidade de execução.__

{% endif %}

{% set situacao = 'Ausência de acompanhamento, revisão ou atualização periódica do plano de TIC.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Acompanhamento, revisão e atualização do plano de TIC

O plano de TIC deve ser acompanhado, revisto e atualizado periodicamente ou diante de mudanças relevantes, com registro de execução, pendências, reprogramações e deliberações. Essa rotina permite verificar o andamento das iniciativas, ajustar prioridades e manter o plano compatível com mudanças institucionais, orçamentárias ou tecnológicas.

O Acórdão TCE-RJ 44.490/2024-PLEN prevê a manutenção e revisão periódica do PDTI, bem como ações de divulgação e monitoramento após sua aprovação pela autoridade máxima.

Quando não há acompanhamento, revisão ou atualização periódica, metas e iniciativas podem permanecer desatualizadas, inviáveis ou incompatíveis com as necessidades atuais da organização.

Diante disso, __será proposta recomendação para que a organização estabeleça rotina de acompanhamento, revisão e atualização do plano de TIC, com registro de execução, pendências, reprogramações e deliberações.__

{% endif %}

#### Conclusão

As fragilidades identificadas no planejamento de TIC comprometem a capacidade da organização de direcionar iniciativas, priorizar recursos, alinhar projetos às necessidades institucionais e integrar orçamento e contratações à estratégia de tecnologia.

Diante das situações apresentadas, será sugerida proposta de encaminhamento à organização para que promova a adequação de seu processo e de seu plano de TIC, alinhando-os aos critérios previstos no COBIT 2019, no Acórdão 1.411/2014-TCU-Plenário e no Acórdão TCE-RJ 44.490/2024-PLEN.

### Propostas de Encaminhamento
{% for e in achado.encaminhamentos %}
* **Comunicação com {{ e.tipo }}** para que {{ e.encaminhamento }};
{% endfor %}

{# Final do Achado - Planejamento de TIC #}
{% endif %}
