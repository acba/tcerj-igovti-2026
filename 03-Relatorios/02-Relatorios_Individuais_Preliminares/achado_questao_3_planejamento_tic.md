{% set nome_achado = 'Planejamento de TIC insuficiente para orientar a gestão, o orçamento e as contratações de TIC' %}
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

O planejamento de TIC é instrumento fundamental para traduzir diretrizes institucionais em iniciativas, prioridades, recursos, prazos, responsáveis e resultados esperados. Sob a perspectiva de governança pública, a administração deve executar processo formal de planejamento, contar com plano de TIC formalmente aprovado, assegurar participação das áreas finalísticas, alinhar o plano ao planejamento institucional, integrá-lo ao orçamento e às contratações e acompanhá-lo periodicamente.

Os critérios de boas práticas indicam que o planejamento de TIC deve estabelecer plano e roteiro estratégico, manter orçamento alinhado ao portfólio e às prioridades aprovadas, vincular ações de TIC a indicadores, metas e orçamento de TI, e contemplar processo estruturado de elaboração, manutenção e revisão periódica do PDTI[^explica_planejamento_tic].

Com base na análise das respostas aos itens 2101, 2102, 2802 e 2804 do questionário aplicado e da avaliação das evidências documentais anexadas, constatou-se que a organização não atende integralmente a esses requisitos de planejamento. A Equipe de Auditoria identificou fragilidades nos seguintes aspectos:

{% set situacao_processo = 'Inexistência ou fragilidade do processo formal de planejamento de TIC.' %}
{% set situacao_plano = 'Ausência de aprovação formal do plano de TIC.' %}
{% set situacao_alinhamento = 'Plano de TIC sem alinhamento adequado ao planejamento institucional.' %}
{% set situacao_integracao = 'Plano de TIC sem vínculo demonstrado com orçamento e contratações de TIC' %}
{% set situacao_acompanhamento = 'Ausência de acompanhamento, revisão ou atualização periódica do plano de TIC.' %}

{% if situacao_processo in achado.situacoes_encontradas %}
* **Processo formal de planejamento**: a fragilidade no processo de elaboração não demonstra aderência aos critérios do COBIT 2019 (APO02.05), do Acórdão 1.411/2014-TCU-Plenário e do Acórdão TCE-RJ 44.490/2024-PLEN, o que pode favorecer atuação reativa e sem critérios objetivos de seleção e priorização de iniciativas.
{% endif %}
{% if situacao_plano in achado.situacoes_encontradas %}
* **Aprovação formal do plano**: a ausência de aprovação formal não demonstra aderência aos critérios de formalização do planejamento de TIC, reduzindo sua legitimidade institucional para orientar a gestão, os projetos, o orçamento e as contratações da organização.
{% endif %}
{% if situacao_alinhamento in achado.situacoes_encontradas %}
* **Alinhamento estratégico**: a falta de alinhamento ao planejamento institucional não demonstra aderência ao princípio de vinculação da TIC aos objetivos de negócio, o que pode resultar em investimentos e iniciativas com baixo valor público para o órgão.
{% endif %}
{% if situacao_integracao in achado.situacoes_encontradas %}
* **Integração orçamentária e operacional**: a ausência de vínculo demonstrado com orçamento e contratações de TIC não demonstra aderência ao COBIT 2019 (APO06.03), ao Acórdão 1.411/2014-TCU-Plenário e ao Acórdão TCE-RJ 44.490/2024-PLEN, favorecendo aquisições reativas, não priorizadas e desalinhadas das metas de TIC.
{% endif %}
{% if situacao_acompanhamento in achado.situacoes_encontradas %}
* **Acompanhamento e revisão**: a ausência de acompanhamento ou atualização periódica não demonstra aderência aos critérios de manutenção e monitoramento do PDTI, elevando o risco de manutenção de metas, iniciativas e prioridades incompatíveis com mudanças institucionais, orçamentárias ou tecnológicas.
{% endif %}

Essas situações ensejaram o presente achado e serão detalhadas nas seções subsequentes.

[^explica_planejamento_tic]: Os critérios de planejamento de TIC convergem para a necessidade de plano formal, aprovado, vigente, alinhado à estratégia institucional, integrado ao orçamento e às contratações e acompanhado periodicamente.

{% set situacao = 'Inexistência ou fragilidade do processo formal de planejamento de TIC.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Processo formal de planejamento de TIC

O processo formal de planejamento de TIC deve definir etapas, responsáveis, participação das áreas demandantes e critérios mínimos de priorização. Esse processo é necessário para que o planejamento deixe de ser uma atividade eventual e passe a constituir rotina institucional de identificação, seleção, priorização e acompanhamento de demandas de tecnologia.

O COBIT 2019, no objetivo APO02.05, orienta a definição de plano e roteiro estratégico de TIC que traduzam a estratégia em iniciativas, prioridades, recursos, dependências, prazos e benefícios esperados. O Acórdão TCE-RJ 44.490/2024-PLEN, item II.3, também aponta a necessidade de processo estruturado, com participação de representantes das principais secretarias, para elaborar, manter e revisar periodicamente o PDTI.

O processo deve ser demonstrado por norma, procedimento, guia ou instrumento equivalente que discipline a elaboração, revisão, aprovação e acompanhamento do planejamento de TIC.

A inexistência ou fragilidade desse processo expõe a organização a uma atuação reativa e à alocação de recursos em iniciativas de tecnologia sem critérios claros de priorização.

Diante disso, __será proposta recomendação para que a organização institua processo formal de planejamento de TIC, com etapas, responsáveis, participação das áreas demandantes e critérios mínimos de priorização.__

{% endif %}

{% set situacao = 'Ausência de aprovação formal do plano de TIC.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Aprovação formal do plano de TIC

O plano de TIC deve ser formalmente aprovado pelo dirigente máximo da organização ou por dirigente ou colegiado integrante da alta administração, de modo a conferir legitimidade institucional ao instrumento.

O Acórdão 1.411/2014-TCU-Plenário e o Acórdão TCE-RJ 44.490/2024-PLEN reforçam a necessidade de plano diretor ou instrumento equivalente formalmente instituído e aprovado, capaz de orientar as ações de TIC.

A aprovação deve ser demonstrada por ato formal da instância competente ou por registro equivalente que identifique o plano aprovado, a autoridade responsável e a data da deliberação.

A ausência de aprovação formal desprovê o plano de legitimidade institucional, retirando-lhe a autoridade regulatória necessária para orientar a gestão, os projetos, o orçamento e as contratações de tecnologia da informação.

Diante disso, __será proposta recomendação para que a organização submeta o plano de TIC à aprovação formal do dirigente máximo ou de dirigente ou colegiado integrante da alta administração, mantendo registro do respectivo ato de aprovação.__

{% endif %}

{% set situacao = 'Plano de TIC sem alinhamento adequado ao planejamento institucional.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Alinhamento ao planejamento institucional

O plano de TIC deve demonstrar como suas iniciativas apoiam os objetivos institucionais, as diretrizes superiores e as necessidades das áreas finalísticas e administrativas.

O Acórdão 1.411/2014-TCU-Plenário exige o desdobramento de diretrizes estratégicas e a vinculação das ações de TI a indicadores e metas de negócio. O Acórdão TCE-RJ 44.490/2024-PLEN também prevê objetivos, indicadores e metas de TI alinhados aos objetivos de negócio.

A ausência de demonstração explícita desse alinhamento eleva o risco de execução de iniciativas tecnológicas com baixo valor agregado para a Administração Pública, desalinhadas das prioridades do órgão e das demandas dos usuários internos e da sociedade.

Diante disso, __será proposta recomendação para que a organização revise o plano de TIC para explicitar seu alinhamento ao planejamento institucional, às diretrizes superiores e às necessidades das áreas finalísticas e administrativas.__

{% endif %}

{% set situacao = 'Plano de TIC sem vínculo demonstrado com orçamento e contratações de TIC' %}
{% if situacao in achado.situacoes_encontradas %}
#### Vínculo com orçamento e contratações de TIC

O planejamento de TIC deve ser vinculado com a proposta orçamentária, o plano de contratações e as contratações executadas. Essa integração é necessária para que as iniciativas priorizadas tenham suporte financeiro, sejam convertidas em contratações coerentes e possam ser acompanhadas ao longo da execução.

O COBIT 2019, APO06.03, orienta a criação e manutenção de orçamento de TIC alinhado ao portfólio, ao planejamento e às prioridades aprovadas. O Acórdão 1.411/2014-TCU-Plenário também exige vinculação das ações priorizadas ao orçamento de TI, e o Acórdão TCE-RJ 44.490/2024-PLEN prevê projetos, aquisições, ações necessárias e alocação de recursos no PDTI.

A falta de integração entre o planejamento de tecnologia, as previsões orçamentárias globais e as contratações executadas resulta em aquisições isoladas, reativas e desprovidas de priorização técnica.

Diante disso, __será proposta recomendação para que a organização vincule o plano de TIC à proposta orçamentária, ao plano de contratações e às contratações de TIC executadas, priorizando demandas conforme relevância, risco e capacidade de execução.__

{% endif %}

{% set situacao = 'Ausência de acompanhamento, revisão ou atualização periódica do plano de TIC.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Acompanhamento, revisão e atualização do plano de TIC

O plano de TIC deve ser acompanhado, revisto e atualizado periodicamente ou diante de mudanças relevantes, com registro de execução, pendências, reprogramações e deliberações. Essa rotina permite verificar o andamento das iniciativas, ajustar prioridades e manter o plano compatível com mudanças institucionais, orçamentárias ou tecnológicas.

O Acórdão TCE-RJ 44.490/2024-PLEN prevê a manutenção e revisão periódica do PDTI, bem como ações de divulgação e monitoramento após sua aprovação pela autoridade máxima.

A ausência de uma rotina sistemática de monitoramento e atualização impede a adaptação do planejamento estratégico a mudanças no contexto institucional, orçamentário ou tecnológico, mantendo iniciativas que podem não mais refletir o interesse público ou a viabilidade operacional.

Diante disso, __será proposta recomendação para que a organização estabeleça rotina de acompanhamento, revisão e atualização do plano de TIC, com registro de execução, pendências, reprogramações e deliberações.__

{% endif %}

#### Conclusão

As fragilidades identificadas no planejamento de TIC comprometem a capacidade da organização de direcionar iniciativas, priorizar recursos, alinhar projetos às necessidades institucionais e integrar orçamento e contratações à estratégia de tecnologia.

Diante do cenário exposto, formula-se proposta de encaminhamento com vistas a recomendar à organização que promova a adequação de seu processo de planejamento e do respectivo plano de TIC, em alinhamento aos critérios previstos no COBIT 2019, nas orientações do Acórdão 1.411/2014-TCU-Plenário e nas deliberações do Acórdão TCE-RJ 44.490/2024-PLEN.

### Propostas de Encaminhamento
{% for e in achado.encaminhamentos %}
* **Comunicação com {{ e.tipo }}** para que {{ e.encaminhamento }};
{% endfor %}

{# Final do Achado - Planejamento de TIC #}
{% endif %}
