{% set nome_achado = 'Planejamento de TIC insuficiente para orientar a gestão, o orçamento e as contratações de TIC' %}
{% set achado = auditado.get_achado_por_nome(nome_achado) %}
{% if achado %}
{% set situacao_processo = 'Inexistência ou insuficiência do processo de planejamento de TIC para produzir e manter plano de TIC adequado.' %}
{% set situacao_plano = 'Ausência de aprovação formal do plano de TIC.' %}
{% set situacao_alinhamento = 'Plano de TIC sem alinhamento adequado ao planejamento institucional.' %}
{% set situacao_integracao = 'Plano de TIC não utilizado como referência para a elaboração da proposta orçamentária e do plano de contratações.' %}
{% set situacao_acompanhamento = 'Ausência de acompanhamento da execução do plano de TIC.' %}
{% set motivos_processo = auditado.get_motivos_situacao(nome_achado, situacao_processo) %}
{% set motivos_plano = auditado.get_motivos_situacao(nome_achado, situacao_plano) %}
{% set motivos_alinhamento = auditado.get_motivos_situacao(nome_achado, situacao_alinhamento) %}
{% set motivos_integracao = auditado.get_motivos_situacao(nome_achado, situacao_integracao) %}
{% set motivos_acompanhamento = auditado.get_motivos_situacao(nome_achado, situacao_acompanhamento) %}
{% set tem_processo = situacao_processo in achado.situacoes_encontradas and motivos_processo %}
{% set tem_plano = situacao_plano in achado.situacoes_encontradas and motivos_plano %}
{% set tem_alinhamento = situacao_alinhamento in achado.situacoes_encontradas and motivos_alinhamento %}
{% set tem_integracao = situacao_integracao in achado.situacoes_encontradas and motivos_integracao %}
{% set tem_acompanhamento = situacao_acompanhamento in achado.situacoes_encontradas and motivos_acompanhamento %}
{% set qtd_situacoes_exibidas = (1 if tem_processo else 0) + (1 if tem_plano else 0) + (1 if tem_alinhamento else 0) + (1 if tem_integracao else 0) + (1 if tem_acompanhamento else 0) %}

\newpage

## Achado {{ achado.numero }} – {{ achado.nome }}

### Critérios
{% if tem_processo or tem_alinhamento %}
* COBIT 2019, APO02.05 - Definir o plano e o roteiro estratégico: estabelecer plano e roteiro de TIC que traduzam a estratégia em iniciativas, prioridades, recursos, dependências, prazos e benefícios esperados;
{% endif %}
{% if tem_integracao %}
* COBIT 2019, APO06.03 - Criar e manter orçamentos: elaborar e manter orçamento de TIC alinhado ao portfólio, ao planejamento e às prioridades aprovadas;
{% endif %}
{% if tem_processo or tem_plano or tem_alinhamento %}
* Acórdão 1.411/2014-TCU-Plenário, item 9.1.6 e subitens 9.1.6.1 a 9.1.6.4: necessidade de instituir formalmente plano diretor de TI, contemplando desdobramento de diretrizes estratégicas, vinculação das ações de TI a indicadores e metas de negócio, vinculação das ações de TI a indicadores e metas de serviços ao cidadão e vinculação das ações priorizadas ao orçamento de TI;
{% endif %}
{% if tem_processo or tem_plano or tem_alinhamento or tem_integracao or tem_acompanhamento %}
* Acórdão TCE-RJ 44.490/2024-PLEN, item II.3 e subitens II.3.1 a II.3.5: necessidade de estabelecer processo estruturado, com participação de representantes das principais secretarias, para elaborar, manter e revisar periodicamente o PDTI, contemplando objetivos, indicadores e metas de TI alinhados aos objetivos de negócio, riscos que possam impactar objetivos e metas, projetos, aquisições e ações necessárias, alocação de recursos e ações de divulgação e monitoramento do PDTI após aprovação pela autoridade máxima.
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

O planejamento de TIC é instrumento fundamental para traduzir diretrizes institucionais em iniciativas, prioridades, recursos, prazos, responsáveis e resultados esperados. Sob a perspectiva de governança pública, a administração deve executar processo formal de planejamento, contar com plano de TIC formalmente aprovado, assegurar participação das áreas finalísticas, alinhar o plano ao planejamento institucional, integrá-lo ao orçamento e às contratações e acompanhá-lo periodicamente.

Os critérios de boas práticas indicam que o planejamento de TIC deve estabelecer plano e roteiro estratégico, manter orçamento alinhado ao portfólio e às prioridades aprovadas, vincular ações de TIC a indicadores, metas e orçamento de TI, e contemplar processo estruturado de elaboração, manutenção e revisão periódica do PDTI[^explica_planejamento_tic].

Com base na análise das respostas aos itens 2101 e 2102 do questionário aplicado e da avaliação das evidências documentais anexadas, não foi demonstrado atendimento integral a esses requisitos de planejamento. A Equipe de Auditoria identificou fragilidades nos seguintes aspectos:

{% if tem_processo %}
* **Processo formal de planejamento**: a fragilidade no processo de elaboração não demonstra aderência ao COBIT 2019, APO02.05, ao Acórdão nº 1.411/2014-TCU-Plenário e ao Acórdão TCE-RJ nº 44.490/2024-PLEN, o que pode favorecer atuação reativa e insuficiente participação das áreas demandantes.
{% endif %}
{% if tem_plano %}
* **Aprovação formal do plano**: a ausência de aprovação formal não demonstra aderência ao Acórdão nº 1.411/2014-TCU-Plenário e ao Acórdão TCE-RJ nº 44.490/2024-PLEN, reduzindo a legitimidade institucional do plano para orientar a gestão, os projetos, o orçamento e as contratações da organização.
{% endif %}
{% if tem_alinhamento %}
* **Alinhamento estratégico**: a falta de alinhamento ao planejamento institucional não demonstra aderência ao COBIT 2019, APO02.05, ao Acórdão nº 1.411/2014-TCU-Plenário e ao Acórdão TCE-RJ nº 44.490/2024-PLEN, o que pode resultar em investimentos e iniciativas com baixo valor público para o órgão.
{% endif %}
{% if tem_integracao %}
* **Integração com orçamento e contratações**: a ausência de utilização do plano de TIC como referência para a proposta orçamentária e o plano de contratações não demonstra aderência ao COBIT 2019, APO06.03, e ao Acórdão TCE-RJ nº 44.490/2024-PLEN, favorecendo a desconexão entre as iniciativas planejadas e os recursos necessários à sua execução.
{% endif %}
{% if tem_acompanhamento %}
* **Acompanhamento e revisão**: a ausência de acompanhamento ou atualização periódica não demonstra aderência ao Acórdão TCE-RJ nº 44.490/2024-PLEN, elevando o risco de manutenção de metas, iniciativas e prioridades incompatíveis com mudanças institucionais, orçamentárias ou tecnológicas.
{% endif %}

{% if qtd_situacoes_exibidas == 1 %}
Essa situação ensejou o presente achado e será detalhada na subseção seguinte.
{% else %}
Essas situações ensejaram o presente achado e serão detalhadas nas subseções seguintes.
{% endif %}

[^explica_planejamento_tic]: Os critérios de planejamento de TIC convergem para a necessidade de plano formal, aprovado, vigente, alinhado à estratégia institucional, integrado ao orçamento e às contratações e acompanhado periodicamente.

{% set situacao = situacao_processo %}
{% if tem_processo %}
#### Processo formal de planejamento de TIC

O processo formal de planejamento de TIC deve definir etapas, responsáveis e participação das áreas demandantes. Esse processo é necessário para que o planejamento deixe de ser uma atividade eventual e passe a constituir rotina institucional de elaboração e manutenção do plano de TIC.

O COBIT 2019, no objetivo APO02.05, orienta a definição de plano e roteiro estratégico de TIC que traduzam a estratégia em iniciativas, prioridades, recursos, dependências, prazos e benefícios esperados. O Acórdão TCE-RJ 44.490/2024-PLEN, item II.3, também aponta a necessidade de processo estruturado, com participação de representantes das principais secretarias, para elaborar, manter e revisar periodicamente o PDTI.

O processo deve ser demonstrado por norma, procedimento, guia ou instrumento equivalente que discipline a elaboração, revisão, aprovação e acompanhamento do planejamento de TIC.

Da análise das respostas ao item 2101 e da documentação apresentada, verificou-se que o processo formal de planejamento de TIC não se mostrou suficientemente estruturado quanto a etapas, responsáveis e participação das áreas demandantes, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
{% set refs_motivo = motivo.get('refs', []) -%}
* {{ motivo.texto.rstrip('.;') }}{% if refs_motivo %} ({{ refs_motivo | join(', ') }}){% endif %}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A inexistência ou fragilidade desse processo expõe a organização a uma atuação reativa e reduz a participação das áreas demandantes na definição das necessidades de tecnologia.

{% endif %}

{% set situacao = situacao_plano %}
{% if tem_plano %}
#### Aprovação formal do plano de TIC

O plano de TIC deve ser formalmente aprovado pelo dirigente máximo da organização ou por dirigente ou colegiado integrante da alta administração, de modo a conferir legitimidade institucional ao instrumento.

O Acórdão 1.411/2014-TCU-Plenário e o Acórdão TCE-RJ 44.490/2024-PLEN reforçam a necessidade de plano diretor ou instrumento equivalente formalmente instituído e aprovado, capaz de orientar as ações de TIC.

A aprovação deve ser demonstrada por ato formal da instância competente ou por registro equivalente que identifique o plano aprovado, a autoridade responsável e a data da deliberação.

Da análise das respostas ao item 2102 e da documentação apresentada, verificou-se que a aprovação formal do plano de TIC por autoridade ou instância competente não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
{% set refs_motivo = motivo.get('refs', []) -%}
* {{ motivo.texto.rstrip('.;') }}{% if refs_motivo %} ({{ refs_motivo | join(', ') }}){% endif %}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência de comprovação da aprovação formal do plano de TIC reduz a segurança quanto à legitimidade institucional do instrumento para orientar a gestão, os projetos, o orçamento e as contratações de tecnologia da informação.

{% endif %}

{% set situacao = situacao_alinhamento %}
{% if tem_alinhamento %}
#### Alinhamento ao planejamento institucional

O plano de TIC deve demonstrar como suas iniciativas apoiam os objetivos institucionais, as diretrizes superiores e as necessidades das áreas finalísticas e administrativas.

O COBIT 2019, APO02.05, orienta que o plano e o roteiro estratégico traduzam a estratégia institucional em iniciativas de TIC. O Acórdão nº 1.411/2014-TCU-Plenário exige o desdobramento de diretrizes estratégicas e a vinculação das ações de TI a indicadores e metas de negócio. O Acórdão TCE-RJ nº 44.490/2024-PLEN também prevê objetivos, indicadores e metas de TI alinhados aos objetivos de negócio.

Da análise das respostas ao item 2102 e da documentação apresentada, verificou-se que o alinhamento do plano de TIC ao planejamento institucional, às diretrizes superiores ou às necessidades das áreas finalísticas e administrativas não se mostrou suficientemente demonstrado, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
{% set refs_motivo = motivo.get('refs', []) -%}
* {{ motivo.texto.rstrip('.;') }}{% if refs_motivo %} ({{ refs_motivo | join(', ') }}){% endif %}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência desse alinhamento eleva o risco de execução de iniciativas tecnológicas pouco aderentes às prioridades institucionais, às necessidades das áreas finalísticas e administrativas e à geração de valor público.

{% endif %}

{% set situacao = situacao_integracao %}
{% if tem_integracao %}
#### Vínculo com orçamento e contratações de TIC

O plano de TIC deve ser utilizado como referência para a elaboração da proposta orçamentária da área de TIC e do plano de contratações. Essa integração contribui para que as iniciativas planejadas sejam consideradas na alocação de recursos e na programação das contratações.

O COBIT 2019, APO06.03, orienta a criação e manutenção de orçamento de TIC alinhado ao portfólio, ao planejamento e às prioridades aprovadas. O Acórdão TCE-RJ nº 44.490/2024-PLEN prevê que o PDTI contemple projetos, aquisições, ações necessárias e alocação de recursos.

Da análise das respostas ao item 2102 e da documentação apresentada, verificou-se que a utilização do plano de TIC como referência para a elaboração da proposta orçamentária e do plano de contratações não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
{% set refs_motivo = motivo.get('refs', []) -%}
* {{ motivo.texto.rstrip('.;') }}{% if refs_motivo %} ({{ refs_motivo | join(', ') }}){% endif %}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A falta de integração demonstrada entre o plano de TIC, a proposta orçamentária e o plano de contratações eleva o risco de insuficiência de recursos para as iniciativas planejadas e de contratações desconectadas das prioridades institucionais.

{% endif %}

{% set situacao = situacao_acompanhamento %}
{% if tem_acompanhamento %}
#### Acompanhamento, revisão e atualização do plano de TIC

O plano de TIC deve ser acompanhado, revisto e atualizado periodicamente ou diante de mudanças relevantes, com registro de execução, pendências, reprogramações e deliberações. Essa rotina permite verificar o andamento das iniciativas, ajustar prioridades e manter o plano compatível com mudanças institucionais, orçamentárias ou tecnológicas.

O Acórdão TCE-RJ 44.490/2024-PLEN prevê a manutenção e revisão periódica do PDTI, bem como ações de divulgação e monitoramento após sua aprovação pela autoridade máxima.

Da análise das respostas ao item 2102 e da documentação apresentada, verificou-se que a rotina de acompanhamento, revisão ou atualização periódica do plano de TIC não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
{% set refs_motivo = motivo.get('refs', []) -%}
* {{ motivo.texto.rstrip('.;') }}{% if refs_motivo %} ({{ refs_motivo | join(', ') }}){% endif %}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência de rotina sistemática de monitoramento e atualização dificulta a adaptação do planejamento de TIC a mudanças no contexto institucional, orçamentário ou tecnológico, elevando o risco de manutenção de iniciativas, prioridades ou metas desatualizadas.

{% endif %}

#### Conclusão

As fragilidades identificadas no planejamento de TIC reduzem a segurança de que a organização disponha, conforme aplicável ao caso concreto, de processo e instrumento suficientes para direcionar iniciativas, priorizar recursos, alinhar projetos às necessidades institucionais e integrar orçamento e contratações à estratégia de tecnologia.

Em razão das lacunas descritas, são propostas determinações voltadas à adequação dos aspectos de planejamento de TIC efetivamente apontados neste achado, observados os critérios aplicáveis indicados nas seções anteriores.

### Propostas de Encaminhamento
{% for e in achado.encaminhamentos %}
* **Comunicação com {{ e.tipo }}** para que {{ e.encaminhamento.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}

{# Final do Achado - Planejamento de TIC #}
{% endif %}
