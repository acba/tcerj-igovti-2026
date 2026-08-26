{% set nome_achado = 'Governança de TIC insuficiente para avaliar, dirigir e monitorar a tecnologia da informação.' %}
{% set achado = auditado.get_achado_por_nome(nome_achado) %}
{% if achado %}
{% set situacao_modelo = 'Ausência de objetivos, indicadores ou metas para a gestão de TIC.' %}
{% set situacao_comite_formal = 'Comitê de TIC ou instância equivalente não instituído formalmente ou sem representação de áreas relevantes da organização.' %}
{% set situacao_comite_atuacao = 'Comitê de TIC ou instância equivalente sem atuação efetiva comprovada.' %}
{% set motivos_modelo = auditado.get_motivos_situacao(nome_achado, situacao_modelo) %}
{% set motivos_comite_formal = auditado.get_motivos_situacao(nome_achado, situacao_comite_formal) %}
{% set motivos_comite_atuacao = auditado.get_motivos_situacao(nome_achado, situacao_comite_atuacao) %}
{% set tem_modelo = situacao_modelo in achado.situacoes_encontradas and motivos_modelo %}
{% set tem_comite_formal = situacao_comite_formal in achado.situacoes_encontradas and motivos_comite_formal %}
{% set tem_comite_atuacao = situacao_comite_atuacao in achado.situacoes_encontradas and motivos_comite_atuacao %}
{% set qtd_situacoes_exibidas = (1 if tem_modelo else 0) + (1 if tem_comite_formal else 0) + (1 if tem_comite_atuacao else 0) %}

\newpage

## Achado {{ achado.numero }} – {{ achado.nome }}

### Critérios
{% if tem_modelo %}
* COBIT 2019, MEA01.04 - Avaliar o desempenho: monitorar e avaliar periodicamente o desempenho e a conformidade da TI em relação a objetivos, indicadores, metas e expectativas das partes interessadas;
{% endif %}
{% if tem_comite_formal or tem_comite_atuacao %}
* COBIT 2019, EDM01.02 - Dirigir o sistema de governança: orientar estruturas, princípios, processos e práticas de governança para assegurar que a TI apoie os objetivos organizacionais;
* Decreto nº 12.198/2024, arts. 5º e 6º, § 2º - Referência de governança digital para instituição de comitê ou colegiado equivalente;
* Acórdão TCE-RJ nº 44.490/2024-PLEN, itens II.1, III.1 e V.1 - Precedente pela instituição e atuação efetiva de instância colegiada de governança de TIC.
{% endif %}

### Evidências
{% set evidencias = auditado.get_evidencias_numeradas(nome_achado) %}
{% for evidencia in evidencias %}
{% set complemento_evidencia = evidencia.get('complemento') %}
{% set descricao_evidencia = evidencia.descricao.rstrip('.;') %}
* **{{ evidencia.ref }}:** {{ descricao_evidencia }}{{ ';' if not loop.last or complemento_evidencia else '.' }}
{% if complemento_evidencia %}  * {{ complemento_evidencia.rstrip('.;') }}{{ ';' if not loop.last else '.' }}
{% endif %}
{% endfor %}

### Situação encontrada

A governança de TIC compreende o conjunto de estruturas, papéis, responsabilidades, diretrizes e mecanismos de acompanhamento por meio dos quais a alta administração avalia, dirige e monitora o uso da tecnologia da informação. Sua finalidade é assegurar que os recursos de TIC apoiem os objetivos institucionais, sejam priorizados de forma transparente e tenham desempenho acompanhado com base em critérios objetivos.

Para que a governança de TIC esteja estruturada, a alta administração deve estabelecer objetivos, indicadores e metas para a gestão de TIC, além de assegurar a existência e o funcionamento regular de um Comitê de TIC ou instância colegiada equivalente.

Os critérios aplicáveis orientam o monitoramento do desempenho da TIC em relação a objetivos, indicadores e metas e a instituição de instância colegiada capaz de alinhar ações de TIC aos objetivos institucionais, priorizar investimentos e acompanhar o desempenho[^explica_governanca_tic_cobit]. A estruturação e a atuação do colegiado também encontram referência no Decreto nº 12.198/2024[^explica_decreto_cgd] e nas deliberações do Acórdão TCE-RJ nº 44.490/2024-PLEN[^explica_acordao_tcerj_governanca].

Com base na análise das respostas ao item 1001 do questionário aplicado e da avaliação das evidências documentais anexadas, não foi demonstrado atendimento integral a esses requisitos de governança. A Equipe de Auditoria identificou fragilidades nos seguintes aspectos:

{% if tem_modelo %}
* **Objetivos, indicadores e metas para a gestão de TIC**: a ausência desses elementos não demonstra aderência ao COBIT 2019, MEA01.04, e dificulta o direcionamento das prioridades, a medição dos resultados e o acompanhamento do desempenho da TIC pela alta administração.
{% endif %}
{% if tem_comite_formal %}
* **Instituição do Comitê de TIC**: a não instituição formal não se alinha ao COBIT 2019, EDM01.02, à diretriz de referência do Decreto nº 12.198/2024 e ao Acórdão TCE-RJ nº 44.490/2024-PLEN, dificultando a existência de instância colegiada para deliberação sobre prioridades, projetos, riscos, serviços, orçamento e contratações de TIC.
{% endif %}
{% if tem_comite_atuacao %}
* **Atuação do Comitê de TIC**: a ausência de atuação efetiva não se alinha ao COBIT 2019, EDM01.02, à diretriz de referência do Decreto nº 12.198/2024 e ao Acórdão TCE-RJ nº 44.490/2024-PLEN, o que pode comprometer a deliberação regular sobre prioridades, projetos, riscos, serviços, orçamento e contratações de TIC.
{% endif %}

{% if qtd_situacoes_exibidas == 1 %}
Essa situação ensejou o presente achado e será detalhada na subseção seguinte.
{% else %}
Essas situações ensejaram o presente achado e serão detalhadas nas subseções seguintes.
{% endif %}

[^explica_governanca_tic_cobit]: O COBIT 2019, MEA01.04, orienta o monitoramento e a avaliação periódica do desempenho da TIC em relação a objetivos, indicadores e metas. O EDM01.02 orienta a direção do sistema de governança por estruturas, princípios, processos e práticas que assegurem que a TIC apoie os objetivos organizacionais.

[^explica_decreto_cgd]: O Decreto nº 12.198/2024 disciplina, no âmbito federal, o Comitê de Governança Digital como colegiado responsável por diretrizes e estratégias sobre o uso de recursos digitais, servindo como referência normativa para a estruturação de instâncias colegiadas de governança digital.

[^explica_acordao_tcerj_governanca]: O Acórdão TCE-RJ 44.490/2024-PLEN, item II.1, registra a necessidade de estrutura de governança de TI, especialmente Comitê de Tecnologia da Informação ou instância equivalente, com participação de áreas relevantes e atribuições de alinhamento, priorização e monitoramento.

{% set situacao = situacao_modelo %}
{% if tem_modelo %}
#### Objetivos, indicadores e metas para a gestão de TIC

A alta administração deve estabelecer objetivos, indicadores e metas para orientar a gestão de TIC e acompanhar sua contribuição para os objetivos institucionais. Esses elementos permitem definir resultados esperados e avaliar periodicamente o desempenho da TIC.

O COBIT 2019, no objetivo MEA01.04, orienta o monitoramento e a avaliação periódica do desempenho e da conformidade da TIC em relação a objetivos, indicadores, metas e expectativas das partes interessadas.

A existência desses elementos deve ser demonstrada por instrumentos que formalizem objetivos, indicadores e metas para a gestão de TIC, acompanhados, quando cabível, de relatórios ou medições de desempenho.

Da análise das respostas ao item 1001 e da documentação apresentada, verificou-se que o estabelecimento de objetivos, indicadores ou metas para a gestão de TIC não se mostrou suficientemente demonstrado, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
{% set refs_motivo = motivo.get('refs', []) -%}
* {{ motivo.texto.rstrip('.;') }}{% if refs_motivo %} ({{ refs_motivo | join(', ') }}){% endif %}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência de objetivos, indicadores ou metas dificulta o direcionamento das prioridades, a medição dos resultados e o acompanhamento da contribuição da TIC para os objetivos institucionais.

{% endif %}

{% set situacao = situacao_comite_formal %}
{% if tem_comite_formal %}
#### Instituição formal do Comitê de TIC ou instância equivalente

O Comitê de TIC ou instância equivalente é mecanismo relevante para estruturar a participação da alta administração e das áreas interessadas nas decisões de tecnologia da informação. Sua formalização permite definir composição, competências, periodicidade mínima, forma de deliberação e responsabilidades pelo acompanhamento das decisões.

O Decreto nº 12.198/2024, art. 5º, adotado como critério de referência, prevê colegiado responsável por definir diretrizes e estratégias sobre uso de recursos digitais no âmbito federal. O Acórdão TCE-RJ 44.490/2024-PLEN, item II.1, reforça a necessidade de estrutura de governança de TI, especialmente Comitê de Tecnologia da Informação ou instância equivalente, com participação de áreas relevantes.

Em alinhamento, o COBIT 2019, no objetivo EDM01.02, orienta a direção do sistema de governança por estruturas, princípios, processos e práticas que assegurem que a TIC apoie os objetivos organizacionais.

A instituição formal do Comitê deve ser demonstrada por ato, norma, regimento, portaria ou documento equivalente que estabeleça a instância, sua composição, competências, periodicidade ou forma de deliberação.

Da análise das respostas ao item 1001 e da documentação apresentada, verificou-se que a instituição formal de Comitê de TIC ou instância equivalente não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
{% set refs_motivo = motivo.get('refs', []) -%}
* {{ motivo.texto.rstrip('.;') }}{% if refs_motivo %} ({{ refs_motivo | join(', ') }}){% endif %}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência de instituição formal do Comitê de TIC ou instância equivalente fragiliza a governança, uma vez que a organização deixa de contar com foro institucional normatizado para deliberação sobre prioridades, projetos, riscos, serviços, orçamento e contratações de TIC.

{% endif %}

{% set situacao = situacao_comite_atuacao %}
{% if tem_comite_atuacao %}
#### Atuação efetiva do Comitê de TIC ou instância equivalente

A instituição formal isolada do Comitê de TIC ou instância equivalente não é suficiente para assegurar governança efetiva. É necessário que a instância funcione de modo regular, com reuniões, pautas, atas, registros de deliberação, encaminhamentos e acompanhamento das decisões tomadas.

O COBIT 2019, no objetivo EDM01.02, orienta o funcionamento das estruturas de governança de modo que a TIC apoie os objetivos organizacionais. O Decreto nº 12.198/2024 e o Acórdão TCE-RJ nº 44.490/2024-PLEN também fundamentam a atuação efetiva da instância colegiada para alinhar as ações de TIC, priorizar investimentos e monitorar seu desempenho.

A atuação efetiva do Comitê deve ser demonstrada por atas, pautas, listas de presença, registros de deliberação, decisões, encaminhamentos ou acompanhamento de pendências. A ausência desses registros dificulta verificar se a instância colegiada exerce, de fato, seu papel de avaliação, direção e monitoramento da TIC.

Da análise das respostas ao item 1001 e da documentação apresentada, verificou-se que a atuação efetiva do Comitê de TIC ou instância equivalente não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
{% set refs_motivo = motivo.get('refs', []) -%}
* {{ motivo.texto.rstrip('.;') }}{% if refs_motivo %} ({{ refs_motivo | join(', ') }}){% endif %}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

Essa fragilidade operacional reduz a segurança de que decisões relevantes sobre prioridades, projetos, riscos, serviços, orçamento e contratações de TIC sejam submetidas ao crivo colegiado ou monitoradas formalmente.

{% endif %}

#### Conclusão

As fragilidades identificadas na governança de TIC reduzem a segurança de que a organização disponha de mecanismos suficientes para avaliar, dirigir e monitorar a tecnologia da informação de forma alinhada aos objetivos institucionais.

Em razão das lacunas descritas, são propostas medidas de encaminhamento, na forma de recomendação ou determinação, conforme a situação identificada, observados os critérios aplicáveis indicados nas seções anteriores.

### Propostas de Encaminhamento
{% for e in achado.encaminhamentos %}
* **Comunicação com {{ e.tipo }}** para que {{ e.encaminhamento.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}

{# Final do Achado - Governança e Comitê de TIC #}
{% endif %}
