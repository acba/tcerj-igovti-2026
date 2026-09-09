{% set nome_achado = 'Fragilidades na governança técnica da fase preparatória das contratações de TIC' %}
{% set achado = auditado.get_achado_por_nome(nome_achado) %}
{% if achado %}
{% set narrativa_criterios = {
    'Q6.C1':
        'A Lei nº 14.133/2021, em seu art. 11, parágrafo único, atribui à alta administração a responsabilidade pela governança das contratações, exigindo a implementação de processos, estruturas, gestão de riscos e controles internos.',

    'Q6.C2':
        'A Lei nº 14.133/2021, no art. 12, inciso VII, estabelece que as contratações devem observar o plano de contratações anual, quando elaborado, garantindo o alinhamento com o planejamento institucional.',

    'Q6.C3':
        'A Lei nº 14.133/2021, no art. 19, inciso IV, prevê a instituição de modelos de minutas de editais, termos de referência, contratos padronizados e demais documentos da fase preparatória.',

    'Q6.C4':
        'A Lei nº 14.133/2021, no art. 7º, caput, determina que a autoridade máxima promova a gestão por competências e designe formalmente agentes públicos para o desempenho das funções essenciais das contratações.',

    'Q6.C5':
        'O COBIT 2019, na prática BAI02.04, orienta a obtenção de aprovação formal dos requisitos funcionais, técnicos, de segurança e de conformidade antes de prosseguir com a contratação da solução.',

    'Q6.C8':
        'Como referência de boa prática, a Instrução Normativa SGD/ME nº 94/2022, art. 12, § 6º, prevê a assinatura do termo de referência pela Equipe de Planejamento da Contratação e pela autoridade máxima da área de TIC, seguida da aprovação pela autoridade competente.',

    'Q6.C9':
        'O Acórdão TCE-RJ nº 44.490/2024-PLEN, item III.7, constitui precedente quanto à estruturação do processo de planejamento anual das contratações, contemplando a consolidação das demandas, participação das áreas, aprovação e publicidade do plano.',

    'Q6.C10':
        'O Acórdão nº 2.342/2016-TCU-Plenário, item 9.1.7, traz precedente quanto à definição, aprovação e formalização de processo de trabalho para o planejamento de cada contratação, com controles internos mínimos.',

    'Q6.C11':
        'Para os órgãos e entidades do Poder Executivo Estadual, o art. 4º da IN PRODERJ/PRE nº 5/2024 determina que os pedidos de contratação de soluções de TIC sejam instruídos com os documentos de planejamento definidos no dispositivo.',

    'Q6.C12':
        'Para os órgãos e entidades do Poder Executivo Estadual, o art. 5º da IN PRODERJ/PRE nº 5/2024 determina expressamente que as contratações de TIC devam estar previstas no PEDTIC e indicadas no Plano de Contratações Anual.',

    'Q6.C13':
        'Para os órgãos do Poder Judiciário Estadual, o art. 10 da Resolução CNJ nº 468/2022 estabelece a obrigatoriedade da execução da fase de planejamento da contratação de TIC nas hipóteses regulamentadas.',

    'Q6.C14':
        'Para os órgãos do Poder Judiciário Estadual, o art. 4º da Resolução CNJ nº 468/2022 determina que as contratações de TIC sejam precedidas de Plano de Contratações de TIC alinhado ao PDTIC e aos planejamentos institucionais.',

    'Q6.C15':
        'Para os órgãos do Poder Judiciário Estadual, o art. 7º da Resolução CNJ nº 468/2022 determina que a fase de planejamento seja coordenada por equipe formalmente designada, composta pelos setores demandante, técnico e administrativo.',

    'Q6.C16':
        'Para o Ministério Público Estadual, o art. 8º da Resolução CNMP nº 283/2024 determina que a etapa de planejamento da solução compreenda, no mínimo, a instituição da equipe de planejamento, o estudo técnico preliminar e o termo de referência.',

    'Q6.C17':
        'Para o Ministério Público Estadual, o art. 5º da Resolução CNMP nº 283/2024 determina que as contratações de TI devam constar do plano de contratações anual, observado o respectivo PDTI.',

    'Q6.C18':
        'Para o Ministério Público Estadual, o art. 9º da Resolução CNMP nº 283/2024 determina que a Equipe de Planejamento da Solução seja formalmente designada e conte com representantes das áreas requisitante, de TI e administrativa.'
} %}
{% set situacao_processo = 'Inexistência ou fragilidade de processo formal e padronizado para o planejamento das contratações de TIC.' %}
{% set situacao_aprovacao = 'Contratações de TIC sem análise prévia e aprovação técnica da área de TIC.' %}
{% set situacao_aderencia = 'Contratações de TIC sem alinhamento ao planejamento de TIC e ao Plano de Contratações Anual.' %}
{% set situacao_equipe = 'Contratações de TIC sem designação de equipe de planejamento com integrante técnico da área de TIC.' %}
{% set motivos_processo = auditado.get_motivos_situacao(nome_achado, situacao_processo) %}
{% set motivos_aprovacao = auditado.get_motivos_situacao(nome_achado, situacao_aprovacao) %}
{% set motivos_aderencia = auditado.get_motivos_situacao(nome_achado, situacao_aderencia) %}
{% set motivos_equipe = auditado.get_motivos_situacao(nome_achado, situacao_equipe) %}
{% set tem_processo = situacao_processo in achado.situacoes_encontradas and motivos_processo %}
{% set tem_aprovacao = situacao_aprovacao in achado.situacoes_encontradas and motivos_aprovacao %}
{% set tem_aderencia = situacao_aderencia in achado.situacoes_encontradas and motivos_aderencia %}
{% set tem_equipe = situacao_equipe in achado.situacoes_encontradas and motivos_equipe %}
{% set qtd_situacoes_exibidas = (1 if tem_processo else 0) + (1 if tem_aprovacao else 0) + (1 if tem_aderencia else 0) + (1 if tem_equipe else 0) %}

\newpage

## Achado {{ achado.numero }} – {{ achado.nome }}

{% include 'bloco_criterios_achado.md' %}

{% include 'bloco_evidencias_achado.md' %}

### Situação encontrada

As contratações de TIC devem observar governança técnica, planejamento prévio proporcional à complexidade do objeto, participação da área de tecnologia quando cabível e alinhamento aos instrumentos de planejamento. A complexidade dos ativos de tecnologia e a dependência das atividades finalísticas em relação aos serviços de TIC demandam controles compatíveis com a relevância, o risco e o valor da contratação.

A governança das contratações de TIC visa assegurar que os processos de aquisição de bens e serviços tecnológicos sejam planejados de forma transparente, motivada e tecnicamente consistente. A padronização da fase preparatória, a avaliação técnica prévia dos requisitos, a aderência aos planos institucionais e a designação formal dos responsáveis pela instrução processual garantem a seleção de soluções vantajosas, compatíveis com a infraestrutura existente e aderentes ao interesse público.

Com base na análise das respostas aos itens 2801 e 2804 do questionário aplicado e da avaliação das evidências documentais anexadas, não foi demonstrado atendimento suficiente das contratações de TIC da organização a essas diretrizes. A Equipe de Auditoria identificou fragilidades nos seguintes aspectos:

{% if tem_processo %}
* **Processo de contratação de TIC**: inexistência ou fragilidade de fluxo formal e padronizado para a fase preparatória das contratações de TIC, divergindo das diretrizes de governança aplicáveis, gerando indefinição de etapas e inconsistências na elaboração dos artefatos processuais.
{% endif %}
{% if tem_aprovacao %}
* **Aprovação técnica de TIC**: ausência de análise prévia e aprovação técnica pela área de TIC nas contratações do setor, contrariando os critérios aplicáveis, elevando o risco de aquisição de soluções incompatíveis com a infraestrutura existente.
{% endif %}
{% if tem_aderencia %}
* **Alinhamento ao planejamento**: ausência de demonstração do alinhamento da contratação ao planejamento de TIC ou ao Plano de Contratações Anual, em desacordo com as diretrizes aplicáveis, favorecendo a execução de compras reativas ou desarticuladas.
{% endif %}
{% if tem_equipe %}
* **Equipe de planejamento**: ausência de designação formal da equipe de planejamento da contratação com participação de integrante técnico de TIC, divergindo das normas e boas práticas aplicáveis, comprometendo a qualidade técnica dos estudos preliminares e do termo de referência.
{% endif %}

{% if qtd_situacoes_exibidas == 1 %}
Essa situação ensejou o presente achado e será detalhada na subseção seguinte.
{% else %}
Essas situações ensejaram o presente achado e serão detalhadas nas subseções seguintes.
{% endif %}

{% set situacao = situacao_processo %}
{% if tem_processo %}
{% set criterios_processo = auditado.get_criterios_situacao(nome_achado, 'S6.1') %}
#### Processo formal e padronizado para contratações de TIC

O processo de contratação de TIC deve estabelecer fluxo, etapas, papéis, responsabilidades, modelos mínimos de artefatos, manuais, checklists ou orientações internas. Esses elementos reduzem improvisação, aumentam padronização e permitem controle sobre a qualidade da instrução processual.

{% for criterio in criterios_processo %}
{{ narrativa_criterios[criterio.id] }}
{% endfor %}

Da análise das respostas ao item 2801 e da documentação apresentada, verificou-se que a existência de processo formal e padronizado para contratações de TIC, com etapas, responsabilidades e artefatos aplicáveis, não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
* {{ motivo.texto.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência de fluxo regulamentado e de modelos padronizados de documentos contraria os critérios aplicáveis, elevando o risco de atrasos, indefinição de responsabilidades e fragilidade técnica e jurídica na elaboração dos artefatos da fase preparatória.

{% endif %}

{% set situacao = situacao_aprovacao %}
{% if tem_aprovacao %}
{% set criterios_aprovacao = auditado.get_criterios_situacao(nome_achado, 'S6.2') %}
#### Análise prévia e aprovação técnica da área de TIC

As contratações de TIC devem ser submetidas à análise prévia e aprovação técnica da área de TIC, inclusive quando demandadas por outras áreas da organização. Essa análise é necessária para verificar compatibilidade técnica, integração com o ambiente existente e aderência a padrões institucionais.

{% for criterio in criterios_aprovacao %}
{{ narrativa_criterios[criterio.id] }}
{% endfor %}

Da análise das respostas ao item 2804 e da documentação apresentada, verificou-se que a submissão das contratações de TIC à análise prévia ou aprovação técnica da área de TIC, inclusive quando demandadas por outras áreas, não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
* {{ motivo.texto.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A falta de manifestação formal prévia da área técnica diverge dos parâmetros aplicáveis, fragilizando a garantia de compatibilidade dos bens e serviços adquiridos com os padrões e a infraestrutura tecnológica do órgão.

{% endif %}

{% set situacao = situacao_aderencia %}
{% if tem_aderencia %}
{% set criterios_aderencia = auditado.get_criterios_situacao(nome_achado, 'S6.3') %}
#### Alinhamento ao planejamento de TIC e ao Plano de Contratações Anual

As contratações de TIC devem estar alinhadas ao planejamento de TIC e, quando elaborado, ao Plano de Contratações Anual. Essa vinculação demonstra que a contratação decorre de necessidade planejada e contribui para os objetivos institucionais.

{% for criterio in criterios_aderencia %}
{{ narrativa_criterios[criterio.id] }}
{% endfor %}

Da análise das respostas ao item 2804 e da documentação apresentada, verificou-se que o alinhamento das contratações de TIC ao planejamento de TIC e ao Plano de Contratações Anual não se mostrou suficientemente demonstrado, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
* {{ motivo.texto.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência de demonstração do vínculo entre as contratações realizadas e os instrumentos de planejamento contraria os critérios aplicáveis, aumentando a probabilidade de contratações reativas, desnecessárias ou fora das prioridades institucionais.

{% endif %}

{% set situacao = situacao_equipe %}
{% if tem_equipe %}
{% set criterios_equipe = auditado.get_criterios_situacao(nome_achado, 'S6.4') %}
#### Equipe de planejamento da contratação de TIC

As contratações de TIC devem contar com equipe de planejamento formalmente designada e com participação de integrante técnico da área de TIC. A designação formal favorece a responsabilização e a qualidade técnica da instrução.

{% for criterio in criterios_equipe %}
{{ narrativa_criterios[criterio.id] }}
{% endfor %}

Da análise das respostas ao item 2804 e da documentação apresentada, verificou-se que a designação formal de equipe de planejamento da contratação de TIC com integrante técnico da área de TIC não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
* {{ motivo.texto.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência de designação formal da equipe de planejamento com integrante técnico de TIC diverge dos critérios aplicáveis, prejudicando a fundamentação técnica dos estudos preliminares e a precisão da especificação do objeto no termo de referência.

{% endif %}

#### Conclusão

As fragilidades evidenciadas na fase preparatória das contratações de TIC reduzem a segurança de que a organização disponha de controles suficientes para assegurar, conforme aplicável ao caso concreto, processo formal de contratação, participação técnica da área de TIC, alinhamento ao planejamento e adequada instrução dos processos. Essas fragilidades elevam o risco de contratações insuficientemente fundamentadas, pouco rastreáveis ou desalinhadas às necessidades institucionais, à complexidade e aos riscos das soluções de TIC pretendidas.

Em razão das lacunas descritas, são propostas medidas de encaminhamento, na forma de recomendação ou determinação, conforme a situação identificada, observados os critérios aplicáveis indicados nas seções anteriores.

{% include 'bloco_encaminhamentos_achado.md' %}

{# Final do Achado - Contratações de TIC #}
{% endif %}
