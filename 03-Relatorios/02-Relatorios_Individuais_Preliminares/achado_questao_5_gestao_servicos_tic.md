{% set nome_achado = 'Gestão de serviços de TIC incipiente, sem controle mínimo sobre serviços, ativos e incidentes' %}
{% set achado = auditado.get_achado_por_nome(nome_achado) %}
{% if achado %}

\newpage

## Achado {{ achado.numero }} – {{ achado.nome }}

### Critérios
* ITIL 4, prática de gerenciamento do catálogo de serviços: manter fonte única de informações consistentes sobre serviços e ofertas de serviço, disponível para usuários e equipes de suporte;
* COBIT 2019, APO09.02 - Catalogar serviços facilitados por TI: definir, manter e comunicar catálogo de serviços, incluindo serviços prestados, características, requisitos e níveis de serviço esperados;
* ITIL 4, prática de gerenciamento de nível de serviço: definir, acordar, monitorar, avaliar e reportar metas e níveis de serviço alinhados às necessidades das áreas usuárias;
* ITIL 4, prática de gerenciamento de ativos de TI: planejar e gerenciar o ciclo de vida dos ativos de TI, mantendo informações suficientes para apoiar controle, custo, risco, valor e tomada de decisão;
* ITIL 4, prática de gerenciamento de configuração de serviço: assegurar informações precisas e confiáveis sobre itens de configuração e seus relacionamentos com serviços, sistemas e infraestrutura;
* COBIT 2019, BAI10.01 - Estabelecer e manter um modelo de configuração: definir escopo, granularidade, atributos, relacionamentos e responsáveis pela base de configuração;
* ITIL 4, prática de gerenciamento de incidentes: minimizar o impacto negativo dos incidentes por meio da restauração tempestiva da operação normal dos serviços e do registro rastreável do tratamento realizado;
* COBIT 2019, DSS02.02, DSS02.04 e DSS02.07 - Requisições de serviço e incidentes gerenciados: registrar, classificar, priorizar, investigar, diagnosticar, resolver, acompanhar e reportar incidentes e requisições de serviço.

### Evidências
{% for evidencia in achado.evidencias %}
* {{ evidencia }};
{% endfor %}

### Situação encontrada
{% set situacao_catalogo = 'Inexistência, desatualização, indisponibilidade ou insuficiência do catálogo de serviços de TIC.' %}
{% set situacao_ans = 'Inexistência de ANS, metas mínimas ou monitoramento de níveis de serviço para os principais serviços de TIC.' %}
{% set situacao_inventario = 'Inexistência ou fragilidade do inventário de ativos de TIC.' %}
{% set situacao_configuracao = 'Ausência ou fragilidade do processo de gestão de configuração.' %}
{% set situacao_incidentes = 'Inexistência ou fragilidade do processo de gestão de incidentes de TIC.' %}
Conclui-se que o(a) {{ auditado.sigla }} não demonstrou adotar práticas mínimas de gestão de serviços de TIC, incluindo catálogo de serviços, níveis de serviço, inventário de ativos, gestão de configuração e tratamento de incidentes, de modo a assegurar eficiência, continuidade, rastreabilidade e qualidade dos serviços prestados, pois a Equipe de Auditoria identificou fragilidades nos seguintes aspectos:{% if situacao_catalogo in achado.situacoes_encontradas %} catálogo de serviços de TIC;{% endif %}{% if situacao_ans in achado.situacoes_encontradas %} ANS, metas mínimas ou monitoramento de níveis de serviço;{% endif %}{% if situacao_inventario in achado.situacoes_encontradas %} inventário de ativos de TIC;{% endif %}{% if situacao_configuracao in achado.situacoes_encontradas %} gestão de configuração;{% endif %}{% if situacao_incidentes in achado.situacoes_encontradas %} gestão de incidentes de TIC;{% endif %}.{% if situacao_catalogo in achado.situacoes_encontradas %} A fragilidade no catálogo de serviços contraria a ITIL 4 e o COBIT 2019, APO09.02, podendo gerar prestação reativa e pouco transparente de serviços de TIC.{% endif %}{% if situacao_ans in achado.situacoes_encontradas %} A ausência de ANS, metas mínimas ou monitoramento de níveis de serviço contraria os critérios de catálogo e gerenciamento de nível de serviço, podendo impedir avaliação objetiva de desempenho e qualidade dos serviços.{% endif %}{% if situacao_inventario in achado.situacoes_encontradas %} A inexistência ou fragilidade do inventário de ativos contraria a ITIL 4, prática de gerenciamento de ativos de TI, e a prática de gerenciamento de configuração, podendo reduzir o controle sobre recursos tecnológicos, custos, riscos e tomada de decisão.{% endif %}{% if situacao_configuracao in achado.situacoes_encontradas %} A ausência ou fragilidade da gestão de configuração contraria a ITIL 4 e o COBIT 2019, BAI10.01, podendo prejudicar a confiabilidade das informações sobre itens de configuração e seus relacionamentos com serviços, sistemas e infraestrutura.{% endif %}{% if situacao_incidentes in achado.situacoes_encontradas %} A inexistência ou fragilidade da gestão de incidentes contraria a ITIL 4 e o COBIT 2019, DSS02.02, DSS02.04 e DSS02.07, podendo comprometer o tratamento padronizado, tempestivo e rastreável dos incidentes de TIC.{% endif %}

A gestão de serviços de TIC organiza a forma como a tecnologia é entregue aos usuários e às áreas demandantes. Catálogo de serviços, níveis de serviço, inventário de ativos, gestão de configuração e gestão de incidentes constituem práticas mínimas para assegurar transparência, continuidade, qualidade, rastreabilidade e controle operacional.

Sob a perspectiva da Questão 5 da matriz de planejamento, a organização deve manter catálogo de serviços formalmente instituído, atualizado e acessível, definir e monitorar níveis de serviço, manter inventário de ativos de TIC, possuir processo de gestão de configuração e tratar incidentes de forma sistemática e rastreável.

Os critérios adotados pela matriz indicam que a organização deve manter fonte única e consistente de informações sobre serviços, definir níveis de serviço, gerenciar ativos e configurações e registrar, classificar, priorizar, resolver, acompanhar e reportar incidentes e requisições de serviço[^explica_gestao_servicos_tic].

Com base na análise das respostas aos itens q2201, q2201ext[A], q2201ext[B], q2201ext[C], q2201ext[D], q2201ext[E], q2203, q2203ext[A], q2203ext[B], q2203ext[C], q2204, q2204ext[A], q2204ext[B], q2204ext[C], q2204ext[D], q2204ext[E], q2204ext[F], q2501 e q2504 do questionário aplicado e da avaliação das evidências anexadas aos itens q2201evi, q2203evi, q2204evi, q2501evi e q2504evi, conforme apontado na seção de Evidências, a Equipe de Auditoria constatou as seguintes deficiências na gestão de serviços de TIC:

{% for situacao in achado.situacoes_encontradas %}
* **{{ situacao }}**
{% endfor %}

Essas situações ensejaram o presente achado e serão detalhadas nas seções subsequentes.

[^explica_gestao_servicos_tic]: As práticas de gestão de serviços de TIC adotadas como critério pela matriz baseiam-se em ITIL 4 e COBIT 2019 e abrangem catálogo, níveis de serviço, ativos, configuração e incidentes.

{% set situacao = 'Inexistência, desatualização, indisponibilidade ou insuficiência do catálogo de serviços de TIC.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Catálogo de serviços de TIC

O catálogo de serviços de TIC deve constituir fonte única de informações consistentes sobre os serviços prestados, acessível aos usuários e às áreas demandantes. Deve conter informações mínimas sobre os serviços efetivamente prestados, suas características, requisitos, canais de atendimento e níveis esperados de serviço.

A ITIL 4, na prática de gerenciamento do catálogo de serviços, orienta a manutenção de informações consistentes e disponíveis sobre serviços e ofertas de serviço. O COBIT 2019, APO09.02, exige a definição, manutenção e comunicação do catálogo de serviços facilitados por TI.

A inexistência, desatualização, indisponibilidade ou insuficiência do catálogo pode gerar prestação reativa, pouco transparente e sem definição clara dos serviços de TIC disponíveis.

Diante disso, __será proposta recomendação para que a organização institua e mantenha atualizado catálogo de serviços de TIC, acessível aos usuários e áreas demandantes, com informações mínimas sobre os serviços efetivamente prestados.__

{% endif %}

{% set situacao = 'Inexistência de ANS, metas mínimas ou monitoramento de níveis de serviço para os principais serviços de TIC.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Níveis de serviço e metas de atendimento

A definição de Acordos de Níveis de Serviço, metas mínimas ou parâmetros equivalentes permite pactuar expectativas, medir desempenho e avaliar a qualidade dos principais serviços de TIC.

A ITIL 4, na prática de gerenciamento de nível de serviço, orienta a definição, monitoramento, avaliação e reporte de metas e níveis de serviço alinhados às necessidades das áreas usuárias. O COBIT 2019, APO09.02, também relaciona o catálogo à comunicação de requisitos e níveis de serviço esperados.

Sem ANS, metas mínimas ou monitoramento, a organização não dispõe de parâmetros objetivos para avaliar desempenho, tempestividade e qualidade dos serviços prestados.

Diante disso, __será proposta recomendação para que a organização defina e monitore níveis mínimos de serviço ou metas de atendimento para os serviços de TIC mais relevantes.__

{% endif %}

{% set situacao = 'Inexistência ou fragilidade do inventário de ativos de TIC.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Inventário de ativos de TIC

O inventário de ativos de TIC deve permitir conhecer e controlar equipamentos, servidores, sistemas, *softwares*, licenças, serviços em nuvem, responsáveis e componentes de infraestrutura.

A ITIL 4, na prática de gerenciamento de ativos de TI, orienta o gerenciamento do ciclo de vida dos ativos, mantendo informações suficientes para apoiar controle, custo, risco, valor e tomada de decisão.

A inexistência ou fragilidade do inventário reduz a visibilidade sobre os recursos tecnológicos e compromete controles de segurança, gestão de custos, planejamento de capacidade, gestão de configuração e resposta a incidentes.

Diante disso, __será proposta recomendação para que a organização mantenha inventário atualizado de ativos de TIC, contemplando ao menos equipamentos, servidores, sistemas, softwares, licenças, serviços em nuvem, responsáveis e componentes de infraestrutura.__

{% endif %}

{% set situacao = 'Ausência ou fragilidade do processo de gestão de configuração.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Gestão de configuração

A gestão de configuração deve manter informações precisas e confiáveis sobre itens de configuração relevantes, seus atributos, responsáveis e relacionamentos com ativos, sistemas, infraestrutura e serviços.

A ITIL 4, na prática de gerenciamento de configuração de serviço, orienta assegurar informações confiáveis sobre itens de configuração e seus relacionamentos. O COBIT 2019, BAI10.01, exige a definição de escopo, granularidade, atributos, relacionamentos e responsáveis pela base de configuração.

Sem processo mínimo de gestão de configuração, a organização perde capacidade de compreender dependências entre ativos e serviços, planejar mudanças, avaliar impactos e manter registros atualizados.

Diante disso, __será proposta recomendação para que a organização formalize e execute processo mínimo de gestão de configuração, mantendo base, ferramenta ou registro equivalente com itens de configuração relevantes, relacionamentos entre ativos, sistemas, infraestrutura e serviços, responsáveis, atualização periódica e uso das informações no planejamento e acompanhamento de mudanças.__

{% endif %}

{% set situacao = 'Inexistência ou fragilidade do processo de gestão de incidentes de TIC.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Gestão de incidentes de TIC

A gestão de incidentes de TIC deve definir papéis, responsabilidades, critérios de priorização, escalamento, tratamento, registro sistemático, histórico das ocorrências e análise posterior de incidentes relevantes ou recorrentes.

A ITIL 4, na prática de gerenciamento de incidentes, orienta minimizar impactos negativos por meio da restauração tempestiva da operação normal e do registro rastreável do tratamento realizado. O COBIT 2019, DSS02.02, DSS02.04 e DSS02.07, exige registrar, classificar, priorizar, investigar, diagnosticar, resolver, acompanhar e reportar incidentes e requisições de serviço.

Quando o processo de gestão de incidentes é inexistente ou frágil, incidentes podem ser tratados de forma improvisada, sem rastreabilidade, histórico, priorização, escalamento ou análise de recorrência.

Diante disso, __será proposta recomendação para que a organização formalize e execute processo mínimo de gestão de incidentes de TIC, contemplando papéis, responsabilidades, critérios de priorização, escalamento, tratamento de incidentes de serviços e de segurança da informação, registro sistemático em ferramenta, sistema, planilha ou base equivalente, histórico das ocorrências e análise posterior de incidentes relevantes ou recorrentes.__

{% endif %}

#### Conclusão

As fragilidades identificadas na gestão de serviços de TIC comprometem a eficiência, a continuidade, a rastreabilidade e a qualidade dos serviços prestados, além de reduzirem o controle da organização sobre seus ativos, configurações e incidentes.

Diante das situações apresentadas, será sugerida proposta de encaminhamento à organização para que promova a adequação de suas práticas mínimas de gestão de serviços de TIC, alinhando-as aos critérios de ITIL 4 e COBIT 2019.

### Propostas de Encaminhamento
{% for e in achado.encaminhamentos %}
* **Comunicação com {{ e.tipo }}** para que {{ e.encaminhamento }};
{% endfor %}

{## Final do Achado - Gestão de serviços de TIC ##}
{% endif %}
