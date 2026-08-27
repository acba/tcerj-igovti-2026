{% set nome_achado = 'Gestão de serviços de TIC insuficiente para assegurar controle sobre serviços, ativos e incidentes' %}
{% set achado = auditado.get_achado_por_nome(nome_achado) %}
{% if achado %}
{% set situacao_catalogo = 'Inexistência ou insuficiência do catálogo de serviços de TIC.' %}
{% set situacao_ans = 'Ausência ou fragilidade na definição e no monitoramento de níveis mínimos de serviço de TIC.' %}
{% set situacao_inventario = 'Inventário e controle de dispositivos e softwares de TIC inexistente ou insuficiente.' %}
{% set situacao_configuracao = 'Ausência ou fragilidade do processo de gestão de configuração.' %}
{% set situacao_incidentes = 'Inexistência ou fragilidade do processo de gestão de incidentes de TIC.' %}
{% set motivos_catalogo = auditado.get_motivos_situacao(nome_achado, situacao_catalogo) %}
{% set motivos_ans = auditado.get_motivos_situacao(nome_achado, situacao_ans) %}
{% set motivos_inventario = auditado.get_motivos_situacao(nome_achado, situacao_inventario) %}
{% set motivos_configuracao = auditado.get_motivos_situacao(nome_achado, situacao_configuracao) %}
{% set motivos_incidentes = auditado.get_motivos_situacao(nome_achado, situacao_incidentes) %}
{% set tem_catalogo = situacao_catalogo in achado.situacoes_encontradas and motivos_catalogo %}
{% set tem_ans = situacao_ans in achado.situacoes_encontradas and motivos_ans %}
{% set tem_inventario = situacao_inventario in achado.situacoes_encontradas and motivos_inventario %}
{% set tem_configuracao = situacao_configuracao in achado.situacoes_encontradas and motivos_configuracao %}
{% set tem_incidentes = situacao_incidentes in achado.situacoes_encontradas and motivos_incidentes %}
{% set qtd_situacoes_exibidas = (1 if tem_catalogo else 0) + (1 if tem_ans else 0) + (1 if tem_inventario else 0) + (1 if tem_configuracao else 0) + (1 if tem_incidentes else 0) %}

\newpage

## Achado {{ achado.numero }} – {{ achado.nome }}

### Critérios
{% for criterio in auditado.get_criterios_achado(nome_achado) %}
* **{{ criterio.id_exibicao }}:** {{ criterio.descricao }} [{{ criterio.situacoes | join(', ') }}]{{ '.' if loop.last else ';' }}
{% endfor %}

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

A gestão de serviços de TIC organiza a forma como as soluções e o suporte tecnológico são entregues aos usuários e às áreas demandantes do órgão. Catálogo de serviços, Acordos de Nível de Serviço (ANS), inventário de ativos, gestão de configuração e gestão de incidentes constituem práticas básicas e integradas necessárias para assegurar a transparência operacional, continuidade do negócio, governabilidade financeira, controle de ativos e qualidade de suporte técnico.

Os critérios aplicáveis indicam que a organização deve manter catálogo de serviços, estabelecer e monitorar níveis de serviço, administrar o ciclo de vida dos ativos tecnológicos, controlar os itens de configuração relevantes e tratar os incidentes de forma padronizada e rastreável[^explica_gestao_servicos_tic].

Com base na análise das respostas aos itens 2201, 2203, 2204 e 2504 do questionário aplicado e da avaliação das evidências documentais anexadas, não foi demonstrada adoção suficiente dessas práticas mínimas. A Equipe de Auditoria identificou fragilidades nos seguintes aspectos:

{% if tem_catalogo %}
* **Catálogo de serviços de TIC**: a fragilidade ou ausência do catálogo não demonstra aderência ao COBIT 2019, APO09.02, ao Acórdão TCE-RJ nº 44.490/2024-PLEN e à ABNT NBR ISO/IEC 20000-2:2021, item 8.2.4, podendo resultar em prestação reativa, sem transparência ou definição clara das entregas técnicas disponíveis.
{% endif %}
{% if tem_ans %}
* **Níveis mínimos de serviço**: a ausência de parâmetros ou acompanhamento não demonstra aderência à prática de gerenciamento de nível de serviço da ITIL 4 e ao Acórdão TCE-RJ nº 44.490/2024-PLEN, dificultando a avaliação objetiva da qualidade e tempestividade dos serviços prestados.
{% endif %}
{% if tem_inventario %}
* **Inventário de ativos de TIC**: a fragilidade ou inexistência de inventário não demonstra aderência à prática de gerenciamento de ativos de TI da ITIL 4 e ao Acórdão TCE-RJ nº 44.490/2024-PLEN, reduzindo o controle sobre recursos tecnológicos, licenciamentos de software, custos e riscos associados.
{% endif %}
{% if tem_configuracao %}
* **Gestão de configuração**: a ausência de processo formal e de base consolidada não demonstra aderência ao COBIT 2019, BAI10.01, ao Acórdão TCE-RJ nº 44.490/2024-PLEN e à ABNT NBR ISO/IEC 20000-2:2021, item 8.2.6, podendo prejudicar a confiabilidade das informações sobre os itens de configuração e seus relacionamentos.
{% endif %}
{% if tem_incidentes %}
* **Gestão de incidentes de TIC**: a inexecução ou informalidade no processo de atendimento não demonstra aderência ao COBIT 2019, DSS02.02, DSS02.04 e DSS02.07, ao Acórdão TCE-RJ nº 44.490/2024-PLEN e à ABNT NBR ISO/IEC 20000-2:2021, item 8.6.1, dificultando o tratamento padronizado, tempestivo e rastreável de falhas tecnológicas.
{% endif %}

{% if qtd_situacoes_exibidas == 1 %}
Essa situação ensejou o presente achado e será detalhada na subseção seguinte.
{% else %}
Essas situações ensejaram o presente achado e serão detalhadas nas subseções seguintes.
{% endif %}

[^explica_gestao_servicos_tic]: Os critérios variam conforme a situação: COBIT APO09.02, Acórdão TCE-RJ nº 44.490/2024-PLEN e ISO/IEC 20000-2 para catálogo; ITIL 4 e o Acórdão para níveis de serviço e ativos; COBIT BAI10.01, o Acórdão e ISO/IEC 20000-2 para configuração; e COBIT DSS02, o Acórdão e ISO/IEC 20000-2 para incidentes.

{% set situacao = situacao_catalogo %}
{% if tem_catalogo %}
#### Catálogo de serviços de TIC

O catálogo de serviços de TIC deve constituir fonte única de informações consistentes sobre os serviços prestados, acessível aos usuários e às áreas demandantes. Deve conter informações mínimas sobre os serviços efetivamente prestados, suas características, requisitos, canais de atendimento e níveis esperados de serviço.

O COBIT 2019, APO09.02, exige a definição, manutenção e comunicação do catálogo de serviços facilitados por TIC. O Acórdão TCE-RJ nº 44.490/2024-PLEN e a ABNT NBR ISO/IEC 20000-2:2021, item 8.2.4, também orientam a estruturação e disponibilização do catálogo.

Da análise das respostas ao item 2201 e da documentação apresentada, verificou-se que a existência de catálogo de serviços de TIC atualizado, acessível aos usuários e com informações mínimas sobre os serviços prestados não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
{% set refs_motivo = motivo.get('refs', []) -%}
* {{ motivo.texto.rstrip('.;') }}{% if refs_motivo %} ({{ refs_motivo | join(', ') }}){% endif %}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A inexistência, desatualização ou falta de divulgação do catálogo de serviços dificulta que os usuários conheçam o portfólio de entregas e os canais corretos de atendimento, elevando o risco de prestação de suporte de forma reativa, informal ou pouco transparente.

{% endif %}

{% set situacao = situacao_ans %}
{% if tem_ans %}
#### Níveis de serviço e metas de atendimento

A definição de Acordos de Níveis de Serviço, metas mínimas ou parâmetros equivalentes permite pactuar expectativas, medir desempenho e avaliar a qualidade dos principais serviços de TIC.

A ITIL 4, na prática de gerenciamento de nível de serviço, orienta a definição, o monitoramento, a avaliação e o reporte de metas e níveis de serviço alinhados às necessidades das áreas usuárias. O Acórdão TCE-RJ nº 44.490/2024-PLEN também recomenda a definição, a pactuação e o monitoramento de níveis de serviço.

Da análise das respostas ao item 2201 e da documentação apresentada, verificou-se que a definição ou o monitoramento de níveis mínimos de serviço, metas ou parâmetros equivalentes para os serviços de TIC relevantes não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
{% set refs_motivo = motivo.get('refs', []) -%}
* {{ motivo.texto.rstrip('.;') }}{% if refs_motivo %} ({{ refs_motivo | join(', ') }}){% endif %}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência de níveis mínimos de serviço, metas estruturadas ou parâmetros equivalentes reduz a disponibilidade de bases objetivas para monitorar e avaliar a qualidade, o tempo de resposta e a eficiência dos serviços prestados.

{% endif %}

{% set situacao = situacao_inventario %}
{% if tem_inventario %}
#### Inventário de ativos de TIC

O inventário de ativos de TIC deve permitir conhecer e controlar os dispositivos conectados à rede e os *softwares* instalados.

A ITIL 4, na prática de gerenciamento de ativos de TI, orienta o gerenciamento do ciclo de vida dos ativos, mantendo informações suficientes para apoiar controle, custo, risco, valor e tomada de decisão. O Acórdão TCE-RJ nº 44.490/2024-PLEN também recomenda a estruturação da gestão de ativos de TIC.

Da análise das respostas ao item 2504 e da documentação apresentada, verificou-se que a existência de inventário de dispositivos e softwares de TIC atualizado e abrangente não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
{% set refs_motivo = motivo.get('refs', []) -%}
* {{ motivo.texto.rstrip('.;') }}{% if refs_motivo %} ({{ refs_motivo | join(', ') }}){% endif %}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência de inventário atualizado de dispositivos e *softwares* reduz a segurança quanto ao controle dos recursos tecnológicos, elevando riscos relacionados a custos, conformidade e segurança da informação.
{% endif %}

{% set situacao = situacao_configuracao %}
{% if tem_configuracao %}
#### Gestão de configuração

A gestão de configuração deve manter informações precisas e confiáveis sobre itens de configuração relevantes, seus atributos, responsáveis e relacionamentos com ativos, sistemas, infraestrutura e serviços.

O COBIT 2019, BAI10.01, exige a definição de escopo, granularidade, atributos, relacionamentos e responsáveis pela base de configuração. O Acórdão TCE-RJ nº 44.490/2024-PLEN e a ABNT NBR ISO/IEC 20000-2:2021, item 8.2.6, também orientam a formalização do processo e a manutenção de informações confiáveis sobre os itens de configuração.

Da análise das respostas ao item 2203 e da documentação apresentada, verificou-se que a existência de processo mínimo de gestão de configuração com registro de itens relevantes, atributos, responsáveis e relacionamentos entre ativos, sistemas, infraestrutura e serviços não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
{% set refs_motivo = motivo.get('refs', []) -%}
* {{ motivo.texto.rstrip('.;') }}{% if refs_motivo %} ({{ refs_motivo | join(', ') }}){% endif %}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência de registros suficientes de configuração dificulta o mapeamento lógico das dependências entre servidores, bancos de dados, aplicações e serviços finalísticos, podendo reduzir a capacidade de análise de riscos em mudanças operacionais e de tratamento de falhas sistêmicas.

{% endif %}

{% set situacao = situacao_incidentes %}
{% if tem_incidentes %}
#### Gestão de incidentes de TIC

A gestão de incidentes de TIC deve definir papéis, critérios de priorização e escalamento, procedimentos para incidentes de serviços e de segurança da informação e registros sistemáticos e rastreáveis das ocorrências.

O COBIT 2019, DSS02.02, DSS02.04 e DSS02.07, orienta registrar, classificar, priorizar, investigar, diagnosticar, resolver, acompanhar e reportar incidentes e requisições de serviço. O Acórdão TCE-RJ nº 44.490/2024-PLEN e a ABNT NBR ISO/IEC 20000-2:2021, item 8.6.1, também orientam a formalização, a execução e a rastreabilidade do processo.

Da análise das respostas ao item 2204 e da documentação apresentada, verificou-se que a existência de processo formal de gestão de incidentes de TIC, com critérios de priorização e escalamento, procedimentos para incidentes de segurança da informação e registros rastreáveis, não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
{% set refs_motivo = motivo.get('refs', []) -%}
* {{ motivo.texto.rstrip('.;') }}{% if refs_motivo %} ({{ refs_motivo | join(', ') }}){% endif %}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

O tratamento assistemático ou sem registro centralizado das falhas tecnológicas dificulta o acompanhamento do histórico de incidentes e a restauração tempestiva dos serviços afetados.

{% endif %}

#### Conclusão

As fragilidades identificadas na gestão de serviços de TIC reduzem a segurança de que a organização disponha, conforme aplicável ao caso concreto, de práticas suficientes para assegurar eficiência, continuidade, rastreabilidade, qualidade dos serviços prestados e controle sobre ativos, configurações e incidentes.

Em razão das lacunas descritas, são propostas recomendações voltadas à estruturação e à adequação das práticas de gestão de serviços de TIC efetivamente apontadas neste achado, observados os critérios aplicáveis indicados nas seções anteriores.

### Propostas de Encaminhamento
{% for e in achado.encaminhamentos %}
* **Comunicação com {{ e.tipo }}** para que {{ e.encaminhamento.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}

{# Final do Achado - Gestão de serviços de TIC #}
{% endif %}
