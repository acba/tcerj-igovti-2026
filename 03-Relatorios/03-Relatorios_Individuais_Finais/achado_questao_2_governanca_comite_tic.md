{% set id_achado = 'Q2' %}{# Q2 — Governança e Comitê de TIC #}
{% set achado = auditado.get_achado_por_id(id_achado) %}
{% if achado %}
{% set narrativa_criterios = {
    'Q2.C1':
        'O COBIT 2019, na prática EDM01.02, orienta a direção do sistema de governança por estruturas, princípios, processos e práticas que assegurem que a tecnologia da informação apoie os objetivos organizacionais.',

    'Q2.C2':
        'O COBIT 2019, na prática MEA01.04, orienta monitorar e avaliar periodicamente o desempenho e a conformidade da TIC em relação a objetivos, indicadores, metas e expectativas das partes interessadas.',

    'Q2.C3':
        'O Decreto federal nº 12.198/2024, art. 6º, § 2º, é adotado como referência de governança digital quanto à deliberação sobre ações de governo digital e uso de recursos de TIC por comitê ou colegiado equivalente.',

    'Q2.C4':
        'O Acórdão TCE-RJ nº 44.490/2024-PLEN, item II.1, registra precedente pela instituição e atuação efetiva de instância colegiada de governança de TIC, responsável pelo alinhamento das ações aos objetivos institucionais, pela priorização dos investimentos e pelo monitoramento do desempenho da tecnologia.',

    'Q2.C5':
        'Para os órgãos e entidades do Poder Executivo Estadual, a Portaria PRODERJ/PRE nº 825/2021, Anexo C, art. 5º, determina a instituição de Comitê Permanente do PEDTIC com composição multidisciplinar.',

    'Q2.C6':
        'Para os órgãos do Poder Judiciário Estadual, o art. 7º da Resolução CNJ nº 370/2021 determina que cada órgão constitua ou mantenha Comitê de Governança de TIC multidisciplinar, com a composição e as atribuições definidas no dispositivo.',

    'Q2.C7':
        'Para o Ministério Público Estadual, o art. 13 da Resolução CNMP nº 171/2017 determina que cada unidade ou ramo disponha de Comitê Estratégico de TI com a composição mínima definida no dispositivo.',

    'Q2.C8':
        'Para os órgãos do Poder Judiciário Estadual, o art. 7º, inciso I, da Resolução CNJ nº 370/2021 determina que o Comitê de Governança de TIC apoie o desenvolvimento e o estabelecimento de estratégias, indicadores e metas institucionais.',

    'Q2.C9':
        'Para o Ministério Público Estadual, o art. 11, § 1º, da Resolução CNMP nº 171/2017 determina que o PETI contenha contribuições da TI para os objetivos estratégicos, indicadores de resultado e, pelo menos, uma meta para cada indicador.',

    'Q2.C10':
        'Para o Ministério Público Estadual, o art. 14 da Resolução CNMP nº 171/2017 determina que o Comitê Estratégico de TI exerça as competências de deliberação, acompanhamento e prestação de contas previstas no dispositivo.'
} %}
{% set s_modelo_governanca = auditado.get_situacao(id_achado, 'S2.1') %}{# S2.1 — Objetivos, indicadores e metas para a gestão de TIC #}
{% set s_instituicao_comite = auditado.get_situacao(id_achado, 'S2.2') %}{# S2.2 — Instituição formal do Comitê de TIC #}
{% set s_atuacao_comite = auditado.get_situacao(id_achado, 'S2.3') %}{# S2.3 — Atuação efetiva do Comitê de TIC #}
{% set situacoes_achado = [s_modelo_governanca, s_instituicao_comite, s_atuacao_comite] %}
{% set qtd_situacoes_exibidas = situacoes_achado | selectattr('ativa') | list | length %}

\newpage

## Achado {{ achado.numero }} – {{ achado.nome }}

{% include 'bloco_criterios_achado.md' %}

{% include 'bloco_evidencias_achado.md' %}

### Situação encontrada

A governança de TIC compreende o conjunto de estruturas, papéis, responsabilidades, diretrizes e mecanismos de acompanhamento por meio dos quais a alta administração avalia, dirige e monitora o uso da tecnologia da informação. Sua finalidade é assegurar que os recursos de TIC apoiem os objetivos institucionais, sejam priorizados de forma transparente e tenham desempenho acompanhado com base em critérios objetivos.

Para que a governança de TIC opere de forma estruturada, a administração deve estabelecer objetivos, indicadores e metas que orientem a atuação da tecnologia e assegurar o funcionamento regular de instâncias colegiadas com representação multidisciplinar. Tais mecanismos conferem legitimidade à priorização de investimentos, viabilizam a prestação de contas e asseguram que a TIC atue alinhada às necessidades estratégicas da organização.

Com base na análise das respostas ao item 1001 do questionário aplicado e da avaliação das evidências documentais anexadas, não foi demonstrado atendimento integral a esses requisitos de governança. A Equipe de Auditoria identificou fragilidades nos seguintes aspectos:

{% if s_modelo_governanca.ativa %}
* **Objetivos, indicadores e metas para a gestão de TIC**: ausência de definição e acompanhamento de metas e indicadores para a tecnologia da informação, em desacordo com as práticas de governança aplicáveis, prejudicando o direcionamento das prioridades e a medição do desempenho da TIC.
{% endif %}
{% if s_instituicao_comite.ativa %}
* **Instituição do Comitê de TIC**: ausência de ato formal de instituição da instância colegiada ou de representação multidisciplinar das áreas de negócio, contrariando os critérios aplicáveis, o que inviabiliza a tomada de decisão colegiada sobre prioridades e investimentos de tecnologia.
{% endif %}
{% if s_atuacao_comite.ativa %}
* **Atuação do Comitê de TIC**: ausência de comprovação de funcionamento regular e deliberação efetiva da instância colegiada, divergindo das orientações de governança aplicáveis, o que compromete o monitoramento contínuo das ações, contratações e riscos de TIC.
{% endif %}

{% if qtd_situacoes_exibidas == 1 %}
Essa situação ensejou o presente achado e será detalhada na subseção seguinte.
{% else %}
Essas situações ensejaram o presente achado e serão detalhadas nas subseções seguintes.
{% endif %}

{% if s_modelo_governanca.ativa %}
#### Objetivos, indicadores e metas para a gestão de TIC

A alta administração deve estabelecer objetivos, indicadores e metas para orientar a gestão de TIC e acompanhar sua contribuição para os objetivos institucionais. Esses elementos permitem definir resultados esperados e avaliar periodicamente o desempenho da TIC.

{% for criterio in s_modelo_governanca.criterios %}
{{ narrativa_criterios[criterio.id] }}
{% endfor %}

A existência desses elementos deve ser demonstrada por instrumentos que formalizem objetivos, indicadores e metas para a gestão de TIC, acompanhados, quando cabível, de relatórios ou medições de desempenho.

Da análise das respostas ao item 1001 e da documentação apresentada, verificou-se que o estabelecimento de objetivos, indicadores ou metas para a gestão de TIC não se mostrou suficientemente demonstrado, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% if s_modelo_governanca.motivos %}

{% for motivo in s_modelo_governanca.motivos -%}
* {{ motivo.texto.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A inexistência de objetivos, indicadores e metas formalizados contraria as diretrizes aplicáveis, dificultando o direcionamento das prioridades, a medição dos resultados e o acompanhamento da contribuição da tecnologia da informação para os objetivos institucionais.

{% endif %}

{% if s_instituicao_comite.ativa %}
#### Instituição formal do Comitê de TIC ou instância equivalente

O Comitê de TIC ou instância equivalente é mecanismo relevante para estruturar a participação da alta administração e das áreas interessadas nas decisões de tecnologia da informação. Sua formalização permite definir composição, competências, periodicidade mínima, forma de deliberação e responsabilidades pelo acompanhamento das decisões.

{% for criterio in s_instituicao_comite.criterios %}
{{ narrativa_criterios[criterio.id] }}
{% endfor %}

A instituição formal do Comitê deve ser demonstrada por ato, norma, regimento, portaria ou documento equivalente que estabeleça a instância, sua composição, competências, periodicidade ou forma de deliberação.

Da análise das respostas ao item 1001 e da documentação apresentada, verificou-se que a instituição formal de Comitê de TIC ou instância equivalente não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% if s_instituicao_comite.motivos %}

{% for motivo in s_instituicao_comite.motivos -%}
* {{ motivo.texto.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A não instituição formal do Comitê de TIC ou a ausência de representação das áreas de negócio diverge dos critérios aplicáveis, privando a organização de foro institucional legitimado para deliberação colegiada sobre prioridades, projetos, riscos, serviços, orçamento e contratações de TIC.

{% endif %}

{% if s_atuacao_comite.ativa %}
#### Atuação efetiva do Comitê de TIC ou instância equivalente

A instituição formal isolada do Comitê de TIC ou instância equivalente não é suficiente para assegurar governança efetiva. É necessário que a instância funcione de modo regular, com reuniões, pautas, atas, registros de deliberação, encaminhamentos e acompanhamento das decisões tomadas.

{% for criterio in s_atuacao_comite.criterios %}
{{ narrativa_criterios[criterio.id] }}
{% endfor %}

A atuação efetiva do Comitê deve ser demonstrada por atas, pautas, listas de presença, registros de deliberação, decisões, encaminhamentos ou acompanhamento de pendências. A ausência desses registros dificulta verificar se a instância colegiada exerce, de fato, seu papel de avaliação, direção e monitoramento da TIC.

Da análise das respostas ao item 1001 e da documentação apresentada, verificou-se que a atuação efetiva do Comitê de TIC ou instância equivalente não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% if s_atuacao_comite.motivos %}

{% for motivo in s_atuacao_comite.motivos -%}
* {{ motivo.texto.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A falta de comprovação de funcionamento regular e de deliberações documentadas contraria os critérios de governança aplicáveis, reduzindo a segurança de que decisões relevantes sobre prioridades, projetos, riscos, serviços, orçamento e contratações de TIC sejam avaliadas e acompanhadas pelo colegiado.

{% endif %}

#### Conclusão

As fragilidades identificadas na governança de TIC reduzem a segurança de que a organização disponha de mecanismos suficientes para avaliar, dirigir e monitorar a tecnologia da informação de forma alinhada aos objetivos institucionais.

Em razão das lacunas descritas, são propostas medidas de encaminhamento, na forma de recomendação ou determinação, conforme a situação identificada, observados os critérios aplicáveis indicados nas seções anteriores.

{% include 'bloco_encaminhamentos_achado.md' %}

{# Final do Achado - Governança e Comitê de TIC #}
{% endif %}
