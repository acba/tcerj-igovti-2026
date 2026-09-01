{% set nome_achado = 'Fragilidades na governança técnica da fase preparatória das contratações de TIC' %}
{% set achado = auditado.get_achado_por_nome(nome_achado) %}
{% if achado %}
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

Os critérios aplicáveis estabelecem, conforme cada situação examinada, a responsabilidade da alta administração pela governança das contratações, a padronização dos documentos da fase preparatória, o alinhamento da contratação ao planejamento, a designação dos agentes responsáveis e a aprovação técnica dos requisitos da solução[^explica_contratacoes_tic].

Com base na análise das respostas aos itens 2801 e 2804 do questionário aplicado e da avaliação das evidências documentais anexadas, não foi demonstrado atendimento suficiente das contratações de TIC da organização a essas diretrizes. A Equipe de Auditoria identificou fragilidades nos seguintes aspectos:

{% if tem_processo %}
* **Processo de contratação de TIC**: a fragilidade ou ausência de fluxo padronizado não demonstra aderência aos arts. 11, parágrafo único, e 19, inciso IV, da Lei nº 14.133/2021 e ao Acórdão nº 2.342/2016-TCU-Plenário, acarretando indefinição de etapas, responsabilidades e artefatos aplicáveis.
{% endif %}
{% if tem_aprovacao %}
* **Aprovação técnica de TIC**: a falta de avaliação prévia pela área técnica não demonstra aderência ao art. 11, parágrafo único, da Lei nº 14.133/2021, ao COBIT 2019, BAI02.04, e à Instrução Normativa SGD/ME nº 94/2022, adotada como referência de boa prática, favorecendo a contratação de soluções incompatíveis com o ambiente tecnológico existente.
{% endif %}
{% if tem_aderencia %}
* **Alinhamento ao planejamento**: a ausência de alinhamento demonstrado ao planejamento de TIC e ao Plano de Contratações Anual não demonstra aderência aos arts. 11, 12 e 18 da Lei nº 14.133/2021 e ao Acórdão TCE-RJ nº 44.490/2024-PLEN, podendo resultar em contratações reativas ou desconectadas das prioridades institucionais.
{% endif %}
{% if tem_equipe %}
{% set criterios_equipe = auditado.get_criterios_situacao(nome_achado, 'S6.4') %}
* **Equipe de planejamento**: a ausência de designação formal de equipe com integrante técnico da área de TIC não demonstra aderência aos critérios aplicáveis descritos na seção Critérios, podendo comprometer a qualidade técnica da instrução da contratação.
{% endif %}

{% if qtd_situacoes_exibidas == 1 %}
Essa situação ensejou o presente achado e será detalhada na subseção seguinte.
{% else %}
Essas situações ensejaram o presente achado e serão detalhadas nas subseções seguintes.
{% endif %}

[^explica_contratacoes_tic]: A relação dos critérios efetivamente aplicáveis e sua vinculação com cada situação encontra-se na seção Critérios deste achado.

{% set situacao = situacao_processo %}
{% if tem_processo %}
#### Processo formal e padronizado para contratações de TIC

O processo de contratação de TIC deve estabelecer fluxo, etapas, papéis, responsabilidades, modelos mínimos de artefatos, manuais, checklists ou orientações internas. Esses elementos reduzem improvisação, aumentam padronização e permitem controle sobre a qualidade da instrução processual.

O art. 11, parágrafo único, da Lei nº 14.133/2021 atribui à alta administração responsabilidade pela governança das contratações, com processos, estruturas, gestão de riscos e controles internos. O art. 19, inciso IV, prevê a instituição de modelos de documentos padronizados. O Acórdão nº 2.342/2016-TCU-Plenário, item 9.1.7, constitui precedente quanto à formalização do processo de trabalho para o planejamento de cada contratação.

Da análise das respostas ao item 2801 e da documentação apresentada, verificou-se que a existência de processo formal e padronizado para contratações de TIC, com etapas, responsabilidades e artefatos aplicáveis, não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
* {{ motivo.texto.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência de fluxo processual regulamentado e de modelos padronizados reduz a segurança quanto à conformidade das contratações de TIC e eleva o risco de atrasos processuais, indefinição de papéis e inconsistências na elaboração dos documentos da fase preparatória.

{% endif %}

{% set situacao = situacao_aprovacao %}
{% if tem_aprovacao %}
#### Análise prévia e aprovação técnica da área de TIC

As contratações de TIC devem ser submetidas à análise prévia e aprovação técnica da área de TIC, inclusive quando demandadas por outras áreas da organização. Essa análise é necessária para verificar compatibilidade técnica, integração com o ambiente existente e aderência a padrões institucionais.

O art. 11, parágrafo único, da Lei nº 14.133/2021 atribui à alta administração responsabilidade pela governança das contratações. O COBIT 2019, BAI02.04, orienta a obtenção de aprovação formal dos requisitos funcionais, técnicos, de segurança e de conformidade antes de prosseguir com a solução. De forma complementar, a Instrução Normativa SGD/ME nº 94/2022, adotada como referência de boa prática, disciplina a participação da área técnica na fase de planejamento, admitida a proporcionalidade dos procedimentos à relevância estratégica, à complexidade e ao valor da aquisição.

Da análise das respostas ao item 2804 e da documentação apresentada, verificou-se que a submissão das contratações de TIC à análise prévia ou aprovação técnica da área de TIC, inclusive quando demandadas por outras áreas, não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
* {{ motivo.texto.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência de análise prévia ou aprovação técnica da área de TIC reduz a segurança de que as soluções contratadas sejam compatíveis com o ambiente tecnológico existente e com os requisitos institucionais, observada a proporcionalidade em relação à complexidade, ao risco e ao valor da contratação.

{% endif %}

{% set situacao = situacao_aderencia %}
{% if tem_aderencia %}
#### Alinhamento ao planejamento de TIC e ao Plano de Contratações Anual

As contratações de TIC devem estar alinhadas ao planejamento de TIC e, quando elaborado, ao Plano de Contratações Anual. Essa vinculação demonstra que a contratação decorre de necessidade planejada e contribui para os objetivos institucionais.

Os arts. 12 e 18 da Lei nº 14.133/2021 preveem a compatibilização da contratação com o Plano de Contratações Anual, quando elaborado, e a demonstração de seu alinhamento com o planejamento da Administração. O art. 11 reforça a responsabilidade da alta administração pela governança das contratações. O Acórdão TCE-RJ nº 44.490/2024-PLEN também fundamenta a estruturação do planejamento anual das contratações.

Da análise das respostas ao item 2804 e da documentação apresentada, verificou-se que o alinhamento das contratações de TIC ao planejamento de TIC e ao Plano de Contratações Anual não se mostrou suficientemente demonstrado, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
* {{ motivo.texto.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência de alinhamento das contratações de TIC ao planejamento de TIC e ao Plano de Contratações Anual eleva o risco de contratações reativas, desconectadas das prioridades institucionais ou incompatíveis com a programação anual da Administração.

{% endif %}

{% set situacao = situacao_equipe %}
{% if tem_equipe %}
#### Equipe de planejamento da contratação de TIC

As contratações de TIC devem contar com equipe de planejamento formalmente designada e com participação de integrante técnico da área de TIC. A designação formal favorece a responsabilização e a qualidade técnica da instrução.

{% set criterios_equipe = auditado.get_criterios_situacao(nome_achado, 'S6.4') %}
Para esta situação, foram aplicados os critérios apresentados na seção Critérios, conforme o regime normativo aplicável à organização.

Da análise das respostas ao item 2804 e da documentação apresentada, verificou-se que a designação formal de equipe de planejamento da contratação de TIC com integrante técnico da área de TIC não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
* {{ motivo.texto.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência de designação formal da equipe de planejamento, com participação técnica de TIC quando aplicável, reduz a segurança quanto à qualidade técnica das estimativas de mercado, dos estudos de viabilidade e da especificação do objeto no ETP, no TR ou em instrumentos equivalentes.

{% endif %}

#### Conclusão

As fragilidades evidenciadas na fase preparatória das contratações de TIC reduzem a segurança de que a organização disponha de controles suficientes para assegurar, conforme aplicável ao caso concreto, processo formal de contratação, participação técnica da área de TIC, alinhamento ao planejamento e adequada instrução dos processos. Essas fragilidades elevam o risco de contratações insuficientemente fundamentadas, pouco rastreáveis ou desalinhadas às necessidades institucionais, à complexidade e aos riscos das soluções de TIC pretendidas.

Em razão das lacunas descritas, são propostas medidas de encaminhamento, na forma de recomendação ou determinação, conforme a situação identificada, observados os critérios aplicáveis indicados nas seções anteriores.

{% include 'bloco_encaminhamentos_achado.md' %}

{# Final do Achado - Contratações de TIC #}
{% endif %}
