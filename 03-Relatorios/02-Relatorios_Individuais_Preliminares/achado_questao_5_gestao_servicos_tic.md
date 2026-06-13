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

A gestão de serviços de TIC organiza a forma como as soluções e o suporte tecnológico são entregues aos usuários e às áreas demandantes do órgão. Catálogo de serviços, Acordos de Nível de Serviço (ANS), inventário de ativos, gestão de configuração e gestão de incidentes constituem práticas básicas e integradas necessárias para assegurar a transparência operacional, continuidade do negócio, governabilidade financeira, controle de ativos e qualidade de suporte técnico.

Os critérios de boas práticas baseados na ITIL 4 e no COBIT 2019 indicam que a organização deve manter fonte unificada e consistente de informações sobre seu catálogo, estabelecer metas mensuráveis de atendimento, administrar ativamente o ciclo de vida dos ativos tecnológicos, rastrear os relacionamentos lógicos de configuração e registrar de forma sistemática e auditável todas as ocorrências operacionais e incidentes de segurança[^explica_gestao_servicos_tic].

Com base na análise das respostas aos itens q2201, q2203, q2204, q2501 e q2504 do questionário aplicado e da avaliação das evidências documentais anexadas, constatou-se que a organização apresenta lacunas operacionais nessas práticas mínimas. A Equipe de Auditoria identificou fragilidades nos seguintes aspectos:

{% set situacao_catalogo = 'Inexistência, desatualização, indisponibilidade ou insuficiência do catálogo de serviços de TIC.' %}
{% set situacao_ans = 'Inexistência de ANS, metas mínimas ou monitoramento de níveis de serviço para os principais serviços de TIC.' %}
{% set situacao_inventario = 'Inexistência ou fragilidade do inventário de ativos de TIC.' %}
{% set situacao_configuracao = 'Ausência ou fragilidade do processo de gestão de configuração.' %}
{% set situacao_incidentes = 'Inexistência ou fragilidade do processo de gestão de incidentes de TIC.' %}

{% if situacao_catalogo in achado.situacoes_encontradas %}
* **Catálogo de serviços de TIC**: a fragilidade ou ausência do catálogo contraria a ITIL 4 e o COBIT 2019 (APO09.02), resultando em prestação reativa, sem transparência ou definição clara das entregas técnicas disponíveis.
{% endif %}
{% if situacao_ans in achado.situacoes_encontradas %}
* **Níveis mínimos de serviço (ANS)**: a ausência de parâmetros ou acompanhamento contraria os critérios de catálogo e gerenciamento de nível de serviço (ITIL 4 e COBIT 2019, APO09.02), impedindo a avaliação objetiva da qualidade e tempestividade dos serviços prestados.
{% endif %}
{% if situacao_inventario in achado.situacoes_encontradas %}
* **Inventário de ativos de TIC**: a fragilidade ou inexistência de inventário contraria a prática de gerenciamento de ativos de TI (ITIL 4), reduzindo substancialmente o controle sobre recursos tecnológicos, licenciamentos de software, custos e riscos associados.
{% endif %}
{% if situacao_configuracao in achado.situacoes_encontradas %}
* **Gestão de configuração**: a ausência de mapeamento lógico contraria a ITIL 4 e o COBIT 2019 (BAI10.01), prejudicando a confiabilidade das dependências operacionais entre infraestrutura, sistemas e serviços críticos.
{% endif %}
{% if situacao_incidentes in achado.situacoes_encontradas %}
* **Gestão de incidentes de TIC**: a inexecução ou informalidade no processo de atendimento contraria a ITIL 4 e o COBIT 2019 (DSS02.02, DSS02.04 e DSS02.07), inviabilizando o tratamento padronizado, célere e rastreável de falhas tecnológicas.
{% endif %}

Essas situações ensejaram o presente achado e serão detalhadas nas seções subsequentes.

[^explica_gestao_servicos_tic]: As práticas de gestão de serviços de TIC adotadas como critério baseiam-se em ITIL 4 e COBIT 2019 e abrangem catálogo, níveis de serviço, ativos, configuração e incidentes.

{% set situacao = 'Inexistência, desatualização, indisponibilidade ou insuficiência do catálogo de serviços de TIC.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Catálogo de serviços de TIC

O catálogo de serviços de TIC deve constituir fonte única de informações consistentes sobre os serviços prestados, acessível aos usuários e às áreas demandantes. Deve conter informações mínimas sobre os serviços efetivamente prestados, suas características, requisitos, canais de atendimento e níveis esperados de serviço.

A ITIL 4, na prática de gerenciamento do catálogo de serviços, orienta a manutenção de informações consistentes e disponíveis sobre serviços e ofertas de serviço. O COBIT 2019, APO09.02, exige a definição, manutenção e comunicação do catálogo de serviços facilitados por TI.

A inexistência, desatualização ou falta de divulgação do catálogo de serviços inviabiliza que os usuários conheçam o portfólio de entregas e os canais corretos de atendimento, gerando um modelo reativo e informal de prestação de suporte.

Diante disso, __será proposta recomendação para que a organização institua e mantenha atualizado catálogo de serviços de TIC, acessível aos usuários e áreas demandantes, com informações mínimas sobre os serviços efetivamente prestados.__

{% endif %}

{% set situacao = 'Inexistência de ANS, metas mínimas ou monitoramento de níveis de serviço para os principais serviços de TIC.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Níveis de serviço e metas de atendimento

A definição de Acordos de Níveis de Serviço, metas mínimas ou parâmetros equivalentes permite pactuar expectativas, medir desempenho e avaliar a qualidade dos principais serviços de TIC.

A ITIL 4, na prática de gerenciamento de nível de serviço, orienta a definição, monitoramento, avaliação e reporte de metas e níveis de serviço alinhados às necessidades das áreas usuárias. O COBIT 2019, APO09.02, também relaciona o catálogo à comunicação de requisitos e níveis de serviço esperados.

A ausência de Acordos de Nível de Serviço (ANS) e de metas estruturadas priva a administração de bases quantitativas para monitorar e auditar a qualidade, o tempo de resposta e a eficiência dos serviços prestados.

Diante disso, __será proposta recomendação para que a organização defina e monitore níveis mínimos de serviço ou metas de atendimento para os serviços de TIC mais relevantes.__

{% endif %}

{% set situacao = 'Inexistência ou fragilidade do inventário de ativos de TIC.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Inventário de ativos de TIC

O inventário de ativos de TIC deve permitir conhecer e controlar equipamentos, servidores, sistemas, *softwares*, licenças, serviços em nuvem, responsáveis e componentes de infraestrutura.

A ITIL 4, na prática de gerenciamento de ativos de TI, orienta o gerenciamento do ciclo de vida dos ativos, mantendo informações suficientes para apoiar controle, custo, risco, valor e tomada de decisão.

A falta de controle efetivo sobre os ativos de hardware e software expõe a organização a custos imprevistos, riscos de desconformidade de licenças, falhas de segurança cibernética e dificuldades operacionais no planejamento de capacidade.

Diante disso, __será proposta recomendação para que a organização mantenha inventário atualizado de ativos de TIC, contemplando ao menos equipamentos, servidores, sistemas, softwares, licenças, serviços em nuvem, responsáveis e componentes de infraestrutura.__

{% endif %}

{% set situacao = 'Ausência ou fragilidade do processo de gestão de configuração.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Gestão de configuração

A gestão de configuração deve manter informações precisas e confiáveis sobre itens de configuração relevantes, seus atributos, responsáveis e relacionamentos com ativos, sistemas, infraestrutura e serviços.

A ITIL 4, na prática de gerenciamento de configuração de serviço, orienta assegurar informações confiáveis sobre itens de configuração e seus relacionamentos. O COBIT 2019, BAI10.01, exige a definição de escopo, granularidade, atributos, relacionamentos e responsáveis pela base de configuração.

A ausência de registros de configuração impede o mapeamento lógico das dependências entre servidores, bancos de dados, aplicações e serviços finalísticos, inviabilizando a análise de risco em mudanças operacionais e a mitigação de falhas sistêmicas.

Diante disso, __será proposta recomendação para que a organização formalize e execute processo mínimo de gestão de configuração, mantendo base, ferramenta ou registro equivalente com itens de configuração relevantes, relacionamentos entre ativos, sistemas, infraestrutura e serviços, responsáveis, atualização periódica e uso das informações no planejamento e acompanhamento de mudanças.__

{% endif %}

{% set situacao = 'Inexistência ou fragilidade do processo de gestão de incidentes de TIC.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Gestão de incidentes de TIC

A gestão de incidentes de TIC deve definir papéis, responsabilidades, critérios de priorização, escalamento, tratamento, registro sistemático, histórico das ocorrências e análise posterior de incidentes relevantes ou recorrentes.

A ITIL 4, na prática de gerenciamento de incidentes, orienta minimizar impactos negativos por meio da restauração tempestiva da operação normal e do registro rastreável do tratamento realizado. O COBIT 2019, DSS02.02, DSS02.04 e DSS02.07, exige registrar, classificar, priorizar, investigar, diagnosticar, resolver, acompanhar e reportar incidentes e requisições de serviço.

O tratamento assistemático e sem registro centralizado das falhas tecnológicas impede o acompanhamento do histórico de incidentes, inviabilizando a identificação de causas raiz e prolongando o período de indisponibilidade dos sistemas corporativos.

Diante disso, __será proposta recomendação para que a organização formalize e execute processo mínimo de gestão de incidentes de TIC, contemplando papéis, responsabilidades, critérios de priorização, escalamento, tratamento de incidentes de serviços e de segurança da informação, registro sistemático em ferramenta, sistema, planilha ou base equivalente, histórico das ocorrências e análise posterior de incidentes relevantes ou recorrentes.__

{% endif %}

#### Conclusão

As fragilidades identificadas na gestão de serviços de TIC comprometem a eficiência, a continuidade, a rastreabilidade e a qualidade dos serviços prestados, além de reduzirem o controle da organização sobre seus ativos, configurações e incidentes.

Diante do cenário exposto, formula-se proposta de encaminhamento com vistas a recomendar à organização que estruture e promova a adequação de suas práticas mínimas de gestão de serviços de TIC, em alinhamento às boas práticas da ITIL 4 e do COBIT 2019.

### Propostas de Encaminhamento
{% for e in achado.encaminhamentos %}
* **Comunicação com {{ e.tipo }}** para que {{ e.encaminhamento }};
{% endfor %}

{# Final do Achado - Gestão de serviços de TIC #}
{% endif %}
