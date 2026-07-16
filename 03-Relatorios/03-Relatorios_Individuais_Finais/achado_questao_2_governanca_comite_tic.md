{% set nome_achado = 'Governança de TIC insuficiente para avaliar, dirigir e monitorar a tecnologia da informação.' %}
{% set achado = auditado.get_achado_por_nome(nome_achado) %}
{% if achado %}
{% set situacao_modelo = 'Modelo básico de governança e gestão de TIC inexistente ou insuficiente quanto a papéis, responsabilidades, objetivos, indicadores, metas ou acompanhamento.' %}
{% set situacao_comite_formal = 'Comitê de TIC ou instância equivalente não instituído formalmente.' %}
{% set situacao_comite_atuacao = 'Comitê de TIC ou instância equivalente sem evidências suficientes de atuação efetiva.' %}
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
* COBIT 2019, EDM01.02 - Dirigir o sistema de governança: orientar estruturas, princípios, processos e práticas de governança para assegurar que a TI apoie os objetivos organizacionais;
{% endif %}
{% if tem_modelo or tem_comite_atuacao %}
* COBIT 2019, MEA01.04 - Avaliar o desempenho: monitorar e avaliar periodicamente o desempenho e a conformidade da TI em relação a objetivos, indicadores, metas e expectativas das partes interessadas;
{% endif %}
{% if tem_comite_formal or tem_comite_atuacao %}
* Decreto nº 12.198/2024, art. 5º - Instituição do CGD, colegiado responsável por definir diretrizes e estratégias sobre uso de recursos digitais nos órgãos e entidades da administração pública federal direta, autárquica e fundacional;
* Acórdão TCE-RJ 44.490/2024-PLEN, item II.1: necessidade de estrutura de governança de TI, especialmente Comitê de Tecnologia da Informação ou instância equivalente, com participação de áreas relevantes, responsabilidade de alinhar as ações de TI aos objetivos institucionais, priorizar investimentos e monitorar o desempenho da TI com base em indicadores e metas;
{% endif %}
{% if tem_modelo or tem_comite_formal %}
* COBIT 2019, APO01.05 - Estabelecer papéis e responsabilidades: definir, comunicar e manter papéis e responsabilidades relacionados à governança e gestão de TI.
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

Para que a governança de TIC esteja estruturada, a alta administração deve estabelecer modelo básico de governança e gestão de TIC, com papéis, responsabilidades, objetivos, indicadores e metas claras, além de assegurar a existência e o funcionamento regular de um Comitê de TIC ou instância colegiada equivalente.

Os critérios de boas práticas orientam que a organização deve dirigir o sistema de governança, monitorar o desempenho e a conformidade da TIC, definir papéis e responsabilidades e instituir instância colegiada capaz de alinhar ações de TIC aos objetivos institucionais, priorizar investimentos e acompanhar o desempenho com base em indicadores e metas[^explica_governanca_tic_cobit]. Esses requisitos convergem com a necessidade de instância colegiada de governança digital, conforme diretriz do Decreto nº 12.198/2024[^explica_decreto_cgd], e com as deliberações do Acórdão TCE-RJ 44.490/2024-PLEN[^explica_acordao_tcerj_governanca].

Com base na análise das respostas aos itens 1001 e 1002 do questionário aplicado e da avaliação das evidências documentais anexadas, não foi demonstrado atendimento integral a esses requisitos de governança. A Equipe de Auditoria identificou fragilidades nos seguintes aspectos:

{% if tem_modelo %}
* **Modelo básico de governança e gestão de TIC**: a ausência ou insuficiência de modelo formalizado não demonstra aderência aos critérios de direção do sistema de governança e avaliação de desempenho (COBIT 2019, EDM01.02/MEA01.04) e ao Acórdão TCE-RJ 44.490/2024-PLEN (item II.1), gerando baixa clareza sobre papéis, responsabilidades, objetivos, indicadores e metas da TIC.
{% endif %}
{% if tem_comite_formal %}
* **Instituição do Comitê de TIC**: a não instituição formal não se alinha ao Acórdão TCE-RJ 44.490/2024-PLEN (item II.1), ao COBIT 2019 (APO01.05) e à diretriz de referência do Decreto nº 12.198/2024 (art. 5º), dificultando a existência de instância colegiada para deliberação sobre prioridades, projetos, riscos, serviços, orçamento e contratações de TIC.
{% endif %}
{% if tem_comite_atuacao %}
* **Atuação do Comitê de TIC**: a ausência de atuação efetiva contraria os critérios de avaliação de desempenho de estruturas colegiadas (COBIT 2019, MEA01.04 e Acórdão TCE-RJ 44.490/2024-PLEN, item II.1) e a diretriz de referência do Decreto nº 12.198/2024 (art. 5º), o que pode comprometer a deliberação regular sobre prioridades, projetos, riscos, serviços, orçamento e contratações de TIC.
{% endif %}

{% if qtd_situacoes_exibidas == 1 %}
Essa situação ensejou o presente achado e será detalhada na subseção seguinte.
{% else %}
Essas situações ensejaram o presente achado e serão detalhadas nas subseções seguintes.
{% endif %}

[^explica_governanca_tic_cobit]: No COBIT 2019, o sistema de governança deve ser dirigido por estruturas, princípios, processos e práticas que assegurem que a TI apoie os objetivos organizacionais, com papéis e responsabilidades definidos e desempenho periodicamente monitorado.

[^explica_decreto_cgd]: O Decreto nº 12.198/2024 disciplina, no âmbito federal, o Comitê de Governança Digital como colegiado responsável por diretrizes e estratégias sobre o uso de recursos digitais, servindo como referência normativa para a estruturação de instâncias colegiadas de governança digital.

[^explica_acordao_tcerj_governanca]: O Acórdão TCE-RJ 44.490/2024-PLEN, item II.1, registra a necessidade de estrutura de governança de TI, especialmente Comitê de Tecnologia da Informação ou instância equivalente, com participação de áreas relevantes e atribuições de alinhamento, priorização e monitoramento.

{% set situacao = situacao_modelo %}
{% if tem_modelo %}
#### Modelo básico de governança e gestão de TIC

O modelo básico de governança e gestão de TIC deve explicitar como a alta administração orienta, acompanha e responsabiliza a atuação da tecnologia da informação. Esse modelo deve conter, ao menos, diretrizes, papéis, responsabilidades, objetivos, indicadores, metas e forma de acompanhamento periódico.

O COBIT 2019, no objetivo EDM01.02, orienta a direção do sistema de governança por meio de estruturas, princípios, processos e práticas que assegurem que a TI apoie os objetivos organizacionais. Em complemento, o objetivo MEA01.04 trata do monitoramento e da avaliação periódica do desempenho e da conformidade da TI em relação a objetivos, indicadores, metas e expectativas das partes interessadas.

A existência e a suficiência desse modelo devem ser demonstradas por políticas, diretrizes, definição de papéis e responsabilidades, objetivos, indicadores, metas, relatórios de acompanhamento, medições de desempenho ou instrumentos equivalentes.

Da análise das respostas aos itens 1001 e 1002 e da documentação apresentada, verificou-se que o modelo básico de governança e gestão de TIC não se mostrou suficientemente estruturado quanto a papéis, responsabilidades, objetivos, indicadores, metas ou forma de acompanhamento periódico, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
{% set refs_motivo = motivo.get('refs', []) -%}
* {{ motivo.texto.rstrip('.;') }}{% if refs_motivo %} ({{ refs_motivo | join(', ') }}){% endif %}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência ou a insuficiência de um modelo básico de governança e gestão de TIC acarreta o risco de indefinição sobre a direção estratégica da tecnologia da informação e sobre os resultados esperados da função de TIC.

{% endif %}

{% set situacao = situacao_comite_formal %}
{% if tem_comite_formal %}
#### Instituição formal do Comitê de TIC ou instância equivalente

O Comitê de TIC ou instância equivalente é mecanismo relevante para estruturar a participação da alta administração e das áreas interessadas nas decisões de tecnologia da informação. Sua formalização permite definir composição, competências, periodicidade mínima, forma de deliberação e responsabilidades pelo acompanhamento das decisões.

O Decreto nº 12.198/2024, art. 5º, adotado como critério de referência, prevê colegiado responsável por definir diretrizes e estratégias sobre uso de recursos digitais no âmbito federal. O Acórdão TCE-RJ 44.490/2024-PLEN, item II.1, reforça a necessidade de estrutura de governança de TI, especialmente Comitê de Tecnologia da Informação ou instância equivalente, com participação de áreas relevantes.

Em alinhamento, o COBIT 2019, no objetivo APO01.05, orienta a definição, comunicação e manutenção de papéis e responsabilidades relacionados à governança e gestão de TI.

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

O COBIT 2019, no objetivo MEA01.04, exige monitoramento e avaliação periódica do desempenho e da conformidade da TI. O Acórdão TCE-RJ 44.490/2024-PLEN, item II.1, também aponta a responsabilidade de alinhar as ações de TI aos objetivos institucionais, priorizar investimentos e monitorar o desempenho da TI com base em indicadores e metas.

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

Em razão das lacunas descritas, são propostas recomendações voltadas à estruturação e à adequação dos mecanismos de governança de TIC efetivamente apontados neste achado, observados os critérios aplicáveis indicados nas seções anteriores.

### Propostas de Encaminhamento
{% for e in achado.encaminhamentos %}
* **Comunicação com {{ e.tipo }}** para que {{ e.encaminhamento.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}

{# Final do Achado - Governança e Comitê de TIC #}
{% endif %}
