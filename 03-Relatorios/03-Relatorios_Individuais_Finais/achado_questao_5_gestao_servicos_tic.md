{% set nome_achado = 'Gestão de serviços de TIC insuficiente para assegurar controle sobre serviços, ativos e incidentes' %}
{% set achado = auditado.get_achado_por_nome(nome_achado) %}
{% if achado %}
{% set narrativa_criterios = {
    'Q5.C2':
        'O COBIT 2019, na prática APO09.02, orienta definir, manter e comunicar catálogo de serviços de TIC, contemplando características, requisitos e níveis de serviço esperados.',

    'Q5.C3':
        'A ITIL 4, na prática de gerenciamento de nível de serviço, orienta definir, acordar, monitorar, avaliar e reportar metas e níveis de serviço alinhados às necessidades das áreas usuárias.',

    'Q5.C4':
        'A ITIL 4, na prática de gerenciamento de ativos de TI, orienta planejar e gerenciar o ciclo de vida dos ativos de TIC, mantendo informações suficientes para apoiar controle, custo, risco, valor e tomada de decisão.',

    'Q5.C6':
        'O COBIT 2019, na prática BAI10.01, orienta estabelecer e manter modelo de configuração, definindo escopo, granularidade, atributos, relacionamentos e responsáveis pela base de configuração.',

    'Q5.C8':
        'O COBIT 2019, na prática DSS02.02, orienta registrar, classificar e priorizar incidentes e requisições de serviço conforme critérios definidos.',

    'Q5.C11':
        'O Acórdão TCE-RJ nº 44.490/2024-PLEN, item II.7.4, registra precedente quanto à estruturação do catálogo de serviços de TIC, incluindo descrição dos serviços, metas, formas de acesso e disponibilidade aos usuários.',

    'Q5.C12':
        'O Acórdão TCE-RJ nº 44.490/2024-PLEN, item II.7.5, registra precedente quanto à gestão de configuração e ativos de TIC, incluindo a formalização do processo e a manutenção de base consolidada de ativos e itens de configuração.',

    'Q5.C13':
        'O Acórdão TCE-RJ nº 44.490/2024-PLEN, item II.7.6, estabelece precedente quanto à formalização e à execução do processo de gestão de incidentes, incluindo registros, classificação, escalamento e tratamento.',

    'Q5.C14':
        'O Acórdão TCE-RJ nº 44.490/2024-PLEN, item II.7.7, traz precedente quanto à definição, pactuação e monitoramento de níveis de serviço.',

    'Q5.C15':
        'A ABNT NBR ISO/IEC 20000-2:2021, item 8.2.4, orienta que o catálogo descreva os serviços e seus resultados pretendidos, contenha informações relevantes para sua utilização e seja disponibilizado às partes interessadas.',

    'Q5.C16':
        'A ABNT NBR ISO/IEC 20000-2:2021, item 8.2.6, orienta a identificação, o registro, o controle, o rastreamento e a verificação dos itens de configuração, bem como a manutenção de informações precisas de configuração.',

    'Q5.C17':
        'A ABNT NBR ISO/IEC 20000-2:2021, item 8.6.1, orienta que os incidentes sejam registrados, classificados e priorizados, com ações resolutivas registradas e rastreáveis e responsabilidades definidas para seu tratamento.',

    'Q5.C18':
        'Para os órgãos e entidades do Poder Executivo Estadual, o art. 4º, inciso V, do Decreto Estadual nº 48.997/2024 determina que o nível setorial alimente as bases de dados corporativas com o inventário permanente de equipamentos, licenças e softwares utilizados.',

    'Q5.C19':
        'Para os órgãos do Poder Judiciário Estadual, o art. 21, inciso IV, alínea d, da Resolução CNJ nº 370/2021 determina que a estrutura de TIC contemple o macroprocesso de catálogo de serviços.',

    'Q5.C20':
        'Para os órgãos do Poder Judiciário Estadual, o art. 34, § 2º, da Resolução CNJ nº 370/2021 determina que a gestão dos ativos de infraestrutura tecnológica seja realizada mediante processos de registro e monitoramento da localização de cada ativo.',

    'Q5.C21':
        'Para os órgãos do Poder Judiciário Estadual, o art. 21, inciso IV, alínea f, da Resolução CNJ nº 370/2021 determina que a estrutura de TIC contemple o macroprocesso de gestão de incidentes.',

    'Q5.C22':
        'Para o Ministério Público Estadual, o art. 23 da Resolução CNMP nº 171/2017 determina que a regulamentação da gestão dos serviços de TI contemple catálogo, acordos de nível de serviço e gestão de incidentes.',

    'Q5.C23':
        'Para o Ministério Público Estadual, o art. 26, inciso II, da Resolução CNMP nº 171/2017 determina que a regulamentação da infraestrutura de TI contemple o controle e a gestão dos itens de configuração e dos ativos de TI.'
} %}
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

{% include 'bloco_criterios_achado.md' %}

{% include 'bloco_evidencias_achado.md' %}

### Situação encontrada

A gestão de serviços de TIC organiza a forma como as soluções e o suporte tecnológico são entregues aos usuários e às áreas demandantes do órgão. Catálogo de serviços, Acordos de Nível de Serviço (ANS), inventário de ativos, gestão de configuração e gestão de incidentes constituem práticas básicas e integradas necessárias para assegurar a transparência operacional, continuidade do negócio, controle de custos, controle de ativos e qualidade de suporte técnico.

A adoção de processos estruturados para entrega e suporte de serviços tecnológicos assegura previsibilidade operacional, padronização no atendimento a demandas e rastreabilidade sobre a infraestrutura instalada. Práticas consolidadas de catálogo de serviços, acordos de níveis de serviço, inventário de ativos, gestão de configurações e atendimento a incidentes conferem estabilidade ao ambiente computacional e resguardam a continuidade das atividades institucionais.

Com base na análise das respostas aos itens 2201, 2203, 2204 e 2504 do questionário aplicado e da avaliação das evidências documentais anexadas, não foi demonstrada adoção suficiente dessas práticas mínimas. A Equipe de Auditoria identificou fragilidades nos seguintes aspectos:

{% if tem_catalogo %}
* **Catálogo de serviços de TIC**: ausência ou desatualização de catálogo estruturado e divulgado aos usuários com as características e canais dos serviços prestados, divergindo das boas práticas aplicáveis, favorecendo a prestação reativa de suporte.
{% endif %}
{% if tem_ans %}
* **Níveis mínimos de serviço**: ausência de definição formal ou monitoramento de metas e parâmetros mínimos de desempenho para os serviços essenciais de TIC, em desacordo com as diretrizes aplicáveis, dificultando a aferição objetiva da tempestividade do suporte.
{% endif %}
{% if tem_inventario %}
* **Inventário de ativos de TIC**: inexistência ou deficiência de inventário atualizado e abrangente de dispositivos e *softwares*, contrariando os critérios aplicáveis, reduzindo o controle sobre ativos computacionais, licenciamentos e custos decorrentes.
{% endif %}
{% if tem_configuracao %}
* **Gestão de configuração**: ausência de processo formalizado e de base de itens de configuração com seus atributos e relacionamentos, divergindo dos critérios de governança aplicáveis, podendo reduzir a confiabilidade das informações sobre o ambiente tecnológico.
{% endif %}
{% if tem_incidentes %}
* **Gestão de incidentes de TIC**: ausência ou fragilidade no fluxo padronizado de registro, classificação e tratamento de incidentes operacionais e de segurança, em descompasso com os parâmetros aplicáveis, dificultando o restabelecimento tempestivo das operações.
{% endif %}

{% if qtd_situacoes_exibidas == 1 %}
Essa situação ensejou o presente achado e será detalhada na subseção seguinte.
{% else %}
Essas situações ensejaram o presente achado e serão detalhadas nas subseções seguintes.
{% endif %}

{% set situacao = situacao_catalogo %}
{% if tem_catalogo %}
{% set criterios_catalogo = auditado.get_criterios_situacao(nome_achado, 'S5.1') %}
#### Catálogo de serviços de TIC

O catálogo de serviços de TIC deve constituir fonte única de informações consistentes sobre os serviços prestados, acessível aos usuários e às áreas demandantes. Deve conter informações mínimas sobre os serviços efetivamente prestados, suas características, requisitos, canais de atendimento e níveis esperados de serviço.

{% for criterio in criterios_catalogo %}
{{ narrativa_criterios[criterio.id] }}
{% endfor %}

Da análise das respostas ao item 2201 e da documentação apresentada, verificou-se que a existência de catálogo de serviços de TIC atualizado, acessível aos usuários e com informações mínimas sobre os serviços prestados não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
* {{ motivo.texto.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência ou insuficiência de catálogo de serviços estruturado e divulgado contraria as orientações aplicáveis, privando os usuários de clareza sobre o portfólio de entregas e os canais formais de atendimento.

{% endif %}

{% set situacao = situacao_ans %}
{% if tem_ans %}
{% set criterios_ans = auditado.get_criterios_situacao(nome_achado, 'S5.2') %}
#### Níveis de serviço e metas de atendimento

A definição de Acordos de Níveis de Serviço, metas mínimas ou parâmetros equivalentes permite pactuar expectativas, medir desempenho e avaliar a qualidade dos principais serviços de TIC.

{% for criterio in criterios_ans %}
{{ narrativa_criterios[criterio.id] }}
{% endfor %}

Da análise das respostas ao item 2201 e da documentação apresentada, verificou-se que a definição ou o monitoramento de níveis mínimos de serviço, metas ou parâmetros equivalentes para os serviços de TIC relevantes não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
* {{ motivo.texto.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A não pactuação e o não monitoramento de metas de atendimento divergem dos parâmetros aplicáveis, impedindo a verificação contínua da qualidade e tempestividade dos serviços prestados.

{% endif %}

{% set situacao = situacao_inventario %}
{% if tem_inventario %}
{% set criterios_inventario = auditado.get_criterios_situacao(nome_achado, 'S5.3') %}
#### Inventário de ativos de TIC

O inventário de ativos de TIC deve permitir conhecer e controlar os dispositivos conectados à rede e os *softwares* instalados.

{% for criterio in criterios_inventario %}
{{ narrativa_criterios[criterio.id] }}
{% endfor %}

Da análise das respostas ao item 2504 e da documentação apresentada, verificou-se que a existência de inventário de dispositivos e softwares de TIC atualizado e abrangente não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
* {{ motivo.texto.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência de inventário consolidado e atualizado de ativos contraria os critérios aplicáveis, fragilizando a gestão patrimonial dos recursos tecnológicos e elevando riscos operacionais e de custos.

{% endif %}

{% set situacao = situacao_configuracao %}
{% if tem_configuracao %}
{% set criterios_configuracao = auditado.get_criterios_situacao(nome_achado, 'S5.4') %}
#### Gestão de configuração

A gestão de configuração deve manter informações precisas e confiáveis sobre itens de configuração relevantes, seus atributos, responsáveis e relacionamentos com ativos, sistemas, infraestrutura e serviços.

{% for criterio in criterios_configuracao %}
{{ narrativa_criterios[criterio.id] }}
{% endfor %}

Da análise das respostas ao item 2203 e da documentação apresentada, verificou-se que a existência de processo mínimo de gestão de configuração com registro de itens relevantes, atributos, responsáveis e relacionamentos entre ativos, sistemas, infraestrutura e serviços não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
* {{ motivo.texto.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência de processo formal e de registros de configuração diverge dos critérios de governança aplicáveis, podendo reduzir a capacidade de análise de riscos em mudanças operacionais e de diagnóstico de falhas sistêmicas.

{% endif %}

{% set situacao = situacao_incidentes %}
{% if tem_incidentes %}
{% set criterios_incidentes = auditado.get_criterios_situacao(nome_achado, 'S5.5') %}
#### Gestão de incidentes de TIC

A gestão de incidentes de TIC deve definir papéis, critérios de priorização e escalamento, procedimentos para incidentes de serviços e de segurança da informação e registros sistemáticos e rastreáveis das ocorrências.

{% for criterio in criterios_incidentes %}
{{ narrativa_criterios[criterio.id] }}
{% endfor %}

Da análise das respostas ao item 2204 e da documentação apresentada, verificou-se que a existência de processo formal de gestão de incidentes de TIC, com critérios de priorização e escalamento, procedimentos para incidentes de segurança da informação e registros rastreáveis, não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
* {{ motivo.texto.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência ou fragilidade de fluxo formalizado e de registros rastreáveis para incidentes contraria os parâmetros aplicáveis, dificultando o tratamento tempestivo de falhas operacionais e de segurança.

{% endif %}

#### Conclusão

As fragilidades identificadas na gestão de serviços de TIC reduzem a segurança de que a organização disponha, conforme aplicável ao caso concreto, de práticas suficientes para assegurar eficiência, continuidade, rastreabilidade, qualidade dos serviços prestados e controle sobre ativos, configurações e incidentes.

Em razão das lacunas descritas, são propostas medidas de encaminhamento, na forma de recomendação ou determinação, conforme a situação e o regime normativo aplicável à organização, observados os critérios indicados nas seções anteriores.

{% include 'bloco_encaminhamentos_achado.md' %}

{# Final do Achado - Gestão de serviços de TIC #}
{% endif %}
