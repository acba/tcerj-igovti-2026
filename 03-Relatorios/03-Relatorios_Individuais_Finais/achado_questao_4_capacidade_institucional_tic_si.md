{% set nome_achado = 'Capacidade institucional de pessoal de TIC e segurança da informação insuficientemente estruturada ou dimensionada' %}
{% set achado = auditado.get_achado_por_nome(nome_achado) %}
{% if achado %}
{% set situacao_forca = 'Ausência de força de trabalho dedicada à TIC.' %}
{% set situacao_quantitativo = 'Ausência ou insuficiência de definição documentada do quantitativo necessário de pessoal de TIC e segurança da informação.' %}
{% set situacao_cargos = 'Ausência de cargos ou funções formalmente atribuídos à TIC ou à segurança da informação.' %}
{% set situacao_terceiros = 'Operação de TIC predominantemente terceirizada sem profissionais internos de TIC.' %}
{% set motivos_forca = auditado.get_motivos_situacao(nome_achado, situacao_forca) %}
{% set motivos_quantitativo = auditado.get_motivos_situacao(nome_achado, situacao_quantitativo) %}
{% set motivos_cargos = auditado.get_motivos_situacao(nome_achado, situacao_cargos) %}
{% set motivos_terceiros = auditado.get_motivos_situacao(nome_achado, situacao_terceiros) %}
{% set tem_forca = situacao_forca in achado.situacoes_encontradas and motivos_forca %}
{% set tem_quantitativo = situacao_quantitativo in achado.situacoes_encontradas and motivos_quantitativo %}
{% set tem_cargos = situacao_cargos in achado.situacoes_encontradas and motivos_cargos %}
{% set tem_terceiros = situacao_terceiros in achado.situacoes_encontradas and motivos_terceiros %}
{% set qtd_situacoes_exibidas = (1 if tem_forca else 0) + (1 if tem_quantitativo else 0) + (1 if tem_cargos else 0) + (1 if tem_terceiros else 0) %}

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

A capacidade institucional de TIC e segurança da informação pressupõe força de trabalho compatível, dimensionamento documentado, funções formalmente atribuídas e capacidade interna para planejar, coordenar, gerir, proteger, contratar, fiscalizar e sustentar o ambiente tecnológico.

Os critérios aplicáveis indicam que a organização deve formalizar papéis e responsabilidades, dimensionar o quadro de pessoal e preservar supervisão e retenção de conhecimento quando utilizar prestadores externos[^explica_capacidade_tic].

Com base na análise das respostas aos itens 0101, 0105, 2703 e 2708 e das evidências documentais, não foi demonstrada capacidade institucional suficiente. A Equipe de Auditoria identificou fragilidades nos seguintes aspectos:

{% if tem_forca %}
* **Força de trabalho dedicada**: a ausência de profissionais dedicados à TIC não demonstra aderência ao COBIT 2019 (APO07.01) e ao Acórdão 1.411/2014-TCU-Plenário (item 9.1.7), podendo comprometer atividades mínimas de planejamento, gestão, contratação, fiscalização e sustentação.
{% endif %}
{% if tem_quantitativo %}
* **Dimensionamento de pessoal**: a ausência de definição documentada do quantitativo necessário não demonstra aderência ao COBIT 2019 (APO07.05) e ao Acórdão 1.411/2014-TCU-Plenário (item 9.1.6.5), elevando o risco de subdimensionamento ou alocação inadequada.
{% endif %}
{% if tem_cargos %}
* **Cargos ou funções atribuídos**: a ausência de atribuição formal não demonstra aderência ao COBIT 2019 (APO01.05 e APO07.01), podendo reduzir a clareza de responsabilidades e a capacidade de alocação dos profissionais.
{% endif %}
{% if tem_terceiros %}
* **Operação predominantemente terceirizada**: a inexistência de profissionais internos não demonstra aderência ao COBIT 2019 (APO07.06) e ao Acórdão TCE-RJ nº 44.490/2024-PLEN, elevando riscos à coordenação, supervisão, fiscalização e retenção de conhecimento.
{% endif %}

{% if qtd_situacoes_exibidas == 1 %}
Essa situação ensejou o presente achado e será detalhada na subseção seguinte.
{% else %}
Essas situações ensejaram o presente achado e serão detalhadas nas subseções seguintes.
{% endif %}

[^explica_capacidade_tic]: Os critérios de capacidade institucional de TIC e segurança da informação concentram-se em pessoal adequado, papéis, responsabilidades, dimensionamento, retenção de conhecimento e supervisão de terceiros.

{% set situacao = situacao_forca %}
{% if tem_forca %}
#### Força de trabalho dedicada à TIC

A organização deve dispor de força de trabalho dedicada à TIC, compatível com sua estrutura, porte, serviços prestados, sistemas mantidos, contratações e riscos relevantes.

O COBIT 2019, APO07.01, orienta a manutenção de pessoal adequado, e o Acórdão 1.411/2014-TCU-Plenário, item 9.1.7, orienta a adoção de providências para dotar o setor de TI de quantitativo adequado às necessidades.

Da análise das respostas aos itens 0101 e 0105, verificou-se que não foi demonstrada a existência de profissional que atuasse regularmente em TIC, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
{% set refs_motivo = motivo.get('refs', []) -%}
* {{ motivo.texto.rstrip('.;') }}{% if refs_motivo %} ({{ refs_motivo | join(', ') }}){% endif %}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência de profissionais que atuem regularmente em TIC reduz a segurança quanto à capacidade da organização de executar rotinas essenciais de planejamento, gestão, segurança da informação, contratação, fiscalização contratual e sustentação das operações de TIC.

{% endif %}

{% set situacao = situacao_quantitativo %}
{% if tem_quantitativo %}
#### Quantitativo necessário de pessoal de TIC e segurança da informação

A definição do quantitativo necessário de pessoal permite avaliar se a força de trabalho disponível é compatível com as demandas, riscos e responsabilidades da organização.

O COBIT 2019, APO07.05, orienta o planejamento e monitoramento da capacidade de pessoal, e o Acórdão 1.411/2014-TCU-Plenário, item 9.1.6.5, estabelece como referência que o PDTI contemple o quantitativo necessário ou ideal da força de trabalho em TI.

Da análise das respostas ao item 2703 e da documentação apresentada, verificou-se que a definição do quantitativo necessário de pessoal de TIC e segurança da informação com base em critério ou procedimento técnico não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
{% set refs_motivo = motivo.get('refs', []) -%}
* {{ motivo.texto.rstrip('.;') }}{% if refs_motivo %} ({{ refs_motivo | join(', ') }}){% endif %}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência de dimensionamento técnico do quadro de pessoal reduz a disponibilidade de bases objetivas para subsidiar decisões sobre contratações, provimentos, planos de capacitação ou eventual compartilhamento de estruturas com outras organizações.

{% endif %}

{% set situacao = situacao_cargos %}
{% if tem_cargos %}
#### Cargos ou funções formalmente atribuídos à TIC ou à segurança da informação

Cargos ou funções formalmente atribuídos à TIC e à segurança da informação ajudam a estruturar responsabilidades e reduzir improvisação na alocação de pessoas.

O COBIT 2019, APO01.05 e APO07.01, orienta a definição de papéis e responsabilidades e a manutenção de pessoal adequado.

Da análise das respostas ao item 2708, verificou-se que a existência de cargos ou funções formalmente atribuídos à TIC ou à segurança da informação não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
{% set refs_motivo = motivo.get('refs', []) -%}
* {{ motivo.texto.rstrip('.;') }}{% if refs_motivo %} ({{ refs_motivo | join(', ') }}){% endif %}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência de cargos ou funções formalmente atribuídos à TIC e à segurança da informação pode reduzir a clareza de responsabilidades e a capacidade de alocação e responsabilização dos profissionais.

{% endif %}

{% set situacao = situacao_terceiros %}
{% if tem_terceiros %}
#### Operação predominantemente terceirizada sem profissionais internos de TIC

A utilização de terceiros ou de estrutura externa para execução de atividades de TIC não elimina a responsabilidade da organização pela coordenação, planejamento, aprovação técnica, fiscalização contratual e retenção de conhecimento.

O COBIT 2019, APO07.06, orienta o controle de pessoal contratado, e o Acórdão TCE-RJ nº 44.490/2024-PLEN fornece referência para preservar capacidade interna de planejamento, coordenação, fiscalização e controle.

Da análise das respostas aos itens 0101 e 0105 e da documentação apresentada, verificou-se que a existência de capacidade interna para coordenar, planejar, fiscalizar e reter conhecimento quando a operação de TIC depende de terceiros ou de estrutura externa não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
{% set refs_motivo = motivo.get('refs', []) -%}
* {{ motivo.texto.rstrip('.;') }}{% if refs_motivo %} ({{ refs_motivo | join(', ') }}){% endif %}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

O estabelecimento de modelo operacional baseado predominantemente em recursos externos, sem capacidade interna suficiente de coordenação e supervisão, pode reduzir a governabilidade técnica, a retenção de conhecimento e a continuidade das operações de TIC.

{% endif %}

#### Conclusão

As fragilidades identificadas na capacidade institucional de TIC e segurança da informação reduzem a segurança de que a organização disponha, conforme aplicável ao caso concreto, de força de trabalho, dimensionamento documentado, cargos ou funções formalmente atribuídos e mecanismos de supervisão suficientes para sustentar a gestão, a proteção, as contratações, a fiscalização e a continuidade dos serviços tecnológicos.

Em razão das lacunas descritas, são propostas recomendações voltadas à adequação dos aspectos de capacidade institucional de TIC e segurança da informação efetivamente apontados neste achado, observados os critérios aplicáveis indicados nas seções anteriores.

### Propostas de Encaminhamento
{% for e in achado.encaminhamentos %}
* **Comunicação com {{ e.tipo }}** para que {{ e.encaminhamento.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}

{# Final do Achado - Capacidade institucional de TIC e segurança da informação #}
{% endif %}
