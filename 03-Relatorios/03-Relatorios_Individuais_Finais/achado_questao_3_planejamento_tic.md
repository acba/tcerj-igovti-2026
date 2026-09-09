{% set nome_achado = 'Planejamento de TIC insuficiente para orientar a gestão, o orçamento e as contratações de TIC' %}
{% set achado = auditado.get_achado_por_nome(nome_achado) %}
{% if achado %}
{% set narrativa_criterios = {
    'Q3.C1':
        'O COBIT 2019, na prática APO02.05, orienta estabelecer plano e roteiro de TIC que traduzam a estratégia em iniciativas, prioridades, recursos, dependências, prazos e benefícios esperados.',

    'Q3.C2':
        'O COBIT 2019, na prática APO06.03, orienta a elaboração e a manutenção de orçamento de TIC alinhado ao portfólio, ao planejamento e às prioridades aprovadas.',

    'Q3.C3':
        'O Acórdão nº 1.411/2014-TCU-Plenário, item 9.1.6, constitui precedente quanto à instituição formal de plano diretor de TI contemplando diretrizes estratégicas e os elementos mínimos de gestão.',

    'Q3.C4':
        'O Acórdão TCE-RJ nº 44.490/2024-PLEN, item II.3, estabelece precedente quanto à formalização de processo estruturado de planejamento de TIC e à elaboração, aprovação, alinhamento, integração orçamentária e monitoramento do plano de TIC.',

    'Q3.C5':
        'Para os órgãos e entidades do Poder Executivo Estadual, o art. 2º da Portaria PRODERJ/PRE nº 825/2021 atribui aos níveis setoriais de TIC a responsabilidade pela elaboração do PEDTIC.',

    'Q3.C6':
        'Para os órgãos e entidades do Poder Executivo Estadual, a Portaria PRODERJ/PRE nº 825/2021, Anexo C, art. 11, parágrafo único, determina expressamente que o PEDTIC seja submetido à aprovação formal da alta direção do órgão ou entidade.',

    'Q3.C7':
        'Para os órgãos e entidades do Poder Executivo Estadual, o art. 3º da Portaria PRODERJ/PRE nº 825/2021 determina que o PEDTIC seja elaborado em conformidade com as diretrizes e metas governamentais e com a governança estadual de TIC.',

    'Q3.C8':
        'Para os órgãos e entidades do Poder Executivo Estadual, a Portaria PRODERJ/PRE nº 825/2021, Anexo C, art. 13, estabelece que a execução do PEDTIC seja monitorada e reportada na forma prevista no dispositivo.',

    'Q3.C9':
        'Para os órgãos do Poder Judiciário Estadual, o art. 6º da Resolução CNJ nº 370/2021 determina a elaboração e manutenção de PDTIC alinhado ao planejamento institucional, exigindo que a proposta orçamentária de TIC guarde integral harmonia com o plano.',

    'Q3.C10':
        'Para os órgãos do Poder Judiciário Estadual, o art. 7º, inciso II, da Resolução CNJ nº 370/2021 atribui ao Comitê de Governança de TIC a competência para aprovar projetos e planos estratégicos.',

    'Q3.C11':
        'Para o Ministério Público Estadual, o art. 12 da Resolução CNMP nº 171/2017 determina que cada unidade elabore PDTI, submeta-o à aprovação da instância de governança em TI e acompanhe sua implementação.',

    'Q3.C12':
        'Para o Ministério Público Estadual, o art. 11 da Resolução CNMP nº 171/2017 determina que o PETI desdobre o planejamento estratégico institucional e contenha as contribuições da TI para os objetivos estratégicos.',

    'Q3.C13':
        'Para os órgãos e entidades do Poder Executivo Estadual, o art. 5º da IN PRODERJ/PRE nº 5/2024 determina que as contratações de TIC devam estar previstas no PEDTIC e indicadas no Plano de Contratações Anual.',

    'Q3.C14':
        'Para o Ministério Público Estadual, o art. 5º da Resolução CNMP nº 283/2024 determina que as contratações de TI devam constar do plano de contratações anual, observado o respectivo PDTI.'
} %}
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

{% include 'bloco_criterios_achado.md' %}

{% include 'bloco_evidencias_achado.md' %}

### Situação encontrada

O planejamento de TIC é instrumento fundamental para traduzir diretrizes institucionais em iniciativas, prioridades, recursos, prazos, responsáveis e resultados esperados. Sob a perspectiva de governança pública, a administração deve executar processo formal de planejamento, contar com plano de TIC formalmente aprovado, assegurar participação das áreas finalísticas, alinhar o plano ao planejamento institucional, integrá-lo ao orçamento e às contratações e acompanhá-lo periodicamente.

O planejamento estruturado de TIC permite à organização antecipar demandas tecnológicas, orientar a distribuição de investimentos e vincular iniciativas aos resultados pretendidos pela gestão. A formalização de um processo de planejamento, a aprovação institucional do plano, sua convergência com as prioridades corporativas, a integração às peças orçamentárias e o monitoramento contínuo da execução asseguram a entrega de valor público e conferem transparência à aplicação dos recursos de tecnologia.

Com base na análise das respostas aos itens 2101 e 2102 do questionário aplicado e da avaliação das evidências documentais anexadas, não foi demonstrado atendimento integral a esses requisitos de planejamento. A Equipe de Auditoria identificou fragilidades nos seguintes aspectos:

{% if tem_processo %}
* **Processo formal de planejamento**: inexistência ou insuficiência de processo institucionalizado para elaboração e manutenção do plano de TIC com participação das áreas demandantes, divergindo das diretrizes de governança aplicáveis, o que favorece atuação reativa e desarticulada.
{% endif %}
{% if tem_plano %}
* **Aprovação formal do plano**: ausência de ato formal de aprovação do plano de TIC pela autoridade ou instância colegiada competente, em descompasso com os critérios aplicáveis, reduzindo a legitimidade institucional do instrumento.
{% endif %}
{% if tem_alinhamento %}
* **Alinhamento estratégico**: ausência de demonstração de alinhamento entre as iniciativas de tecnologia e o planejamento institucional, contrariando os parâmetros aplicáveis, o que eleva o risco de dispersão de esforços e investimentos de baixo valor público.
{% endif %}
{% if tem_integracao %}
* **Integração com orçamento e contratações**: ausência de utilização do plano de TIC como base para a proposta orçamentária e o plano de contratações, divergindo dos critérios de governança aplicáveis, favorecendo a desconexão entre as metas planejadas e os recursos orçamentários alocados.
{% endif %}
{% if tem_acompanhamento %}
* **Acompanhamento e revisão**: ausência de monitoramento periódico e de rotinas de revisão da execução do plano de TIC, em desacordo com as diretrizes aplicáveis, dificultando o ajuste tempestivo de metas e cronogramas frente a mudanças operacionais.
{% endif %}

{% if qtd_situacoes_exibidas == 1 %}
Essa situação ensejou o presente achado e será detalhada na subseção seguinte.
{% else %}
Essas situações ensejaram o presente achado e serão detalhadas nas subseções seguintes.
{% endif %}

{% set situacao = situacao_processo %}
{% if tem_processo %}
{% set criterios_processo = auditado.get_criterios_situacao(nome_achado, 'S3.1') %}
#### Processo formal de planejamento de TIC

O processo formal de planejamento de TIC deve definir etapas, responsáveis e participação das áreas demandantes. Esse processo é necessário para que o planejamento deixe de ser uma atividade eventual e passe a constituir rotina institucional de elaboração e manutenção do plano de TIC.

{% for criterio in criterios_processo %}
{{ narrativa_criterios[criterio.id] }}
{% endfor %}

O processo deve ser demonstrado por norma, procedimento, guia ou instrumento equivalente que discipline a elaboração, revisão, aprovação e acompanhamento do planejamento de TIC.

Da análise das respostas ao item 2101 e da documentação apresentada, verificou-se que o processo formal de planejamento de TIC não se mostrou suficientemente estruturado quanto a etapas, responsáveis e participação das áreas demandantes, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
* {{ motivo.texto.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A fragilidade ou inexistência de processo institucionalizado de planejamento de TIC diverge dos critérios aplicáveis, reduz a participação das áreas demandantes e expõe a organização a uma atuação puramente reativa.

{% endif %}

{% set situacao = situacao_plano %}
{% if tem_plano %}
{% set criterios_plano = auditado.get_criterios_situacao(nome_achado, 'S3.2') %}
#### Aprovação formal do plano de TIC

O plano de TIC deve ser formalmente aprovado pelo dirigente máximo da organização ou por dirigente ou colegiado integrante da alta administração, de modo a conferir legitimidade institucional ao instrumento.

{% for criterio in criterios_plano %}
{{ narrativa_criterios[criterio.id] }}
{% endfor %}

A aprovação deve ser demonstrada por ato formal da instância competente ou por registro equivalente que identifique o plano aprovado, a autoridade responsável e a data da deliberação.

Da análise das respostas ao item 2102 e da documentação apresentada, verificou-se que a aprovação formal do plano de TIC por autoridade ou instância competente não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
* {{ motivo.texto.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência de ato formal de aprovação do plano de TIC pela autoridade competente contraria os critérios aplicáveis, comprometendo a legitimidade do instrumento para vincular a atuação das unidades e orientar a aplicação de recursos.

{% endif %}

{% set situacao = situacao_alinhamento %}
{% if tem_alinhamento %}
{% set criterios_alinhamento = auditado.get_criterios_situacao(nome_achado, 'S3.4') %}
#### Alinhamento ao planejamento institucional

O plano de TIC deve demonstrar como suas iniciativas apoiam os objetivos institucionais, as diretrizes superiores e as necessidades das áreas finalísticas e administrativas.

{% for criterio in criterios_alinhamento %}
{{ narrativa_criterios[criterio.id] }}
{% endfor %}

Da análise das respostas ao item 2102 e da documentação apresentada, verificou-se que o alinhamento do plano de TIC ao planejamento institucional, às diretrizes superiores ou às necessidades das áreas finalísticas e administrativas não se mostrou suficientemente demonstrado, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
* {{ motivo.texto.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A falta de desdobramento e alinhamento explícito das metas de TIC com os objetivos institucionais diverge dos critérios aplicáveis, elevando o risco de execução de ações desalinhadas das prioridades da organização.

{% endif %}

{% set situacao = situacao_integracao %}
{% if tem_integracao %}
{% set criterios_integracao = auditado.get_criterios_situacao(nome_achado, 'S3.5') %}
#### Vínculo com orçamento e contratações de TIC

O plano de TIC deve ser utilizado como referência para a elaboração da proposta orçamentária da área de TIC e do plano de contratações. Essa integração contribui para que as iniciativas planejadas sejam consideradas na alocação de recursos e na programação das contratações.

{% for criterio in criterios_integracao %}
{{ narrativa_criterios[criterio.id] }}
{% endfor %}

Da análise das respostas ao item 2102 e da documentação apresentada, verificou-se que a utilização do plano de TIC como referência para a elaboração da proposta orçamentária e do plano de contratações não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
* {{ motivo.texto.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A não utilização do plano de TIC como balizador da proposta orçamentária e do planejamento de contratações contraria os parâmetros aplicáveis, favorecendo descompassos entre as metas tecnológicas e a disponibilidade orçamentária.

{% endif %}

{% set situacao = situacao_acompanhamento %}
{% if tem_acompanhamento %}
{% set criterios_acompanhamento = auditado.get_criterios_situacao(nome_achado, 'S3.6') %}
#### Acompanhamento, revisão e atualização do plano de TIC

O plano de TIC deve ser acompanhado, revisto e atualizado periodicamente ou diante de mudanças relevantes, com registro de execução, pendências, reprogramações e deliberações. Essa rotina permite verificar o andamento das iniciativas, ajustar prioridades e manter o plano compatível com mudanças institucionais, orçamentárias ou tecnológicas.

{% for criterio in criterios_acompanhamento %}
{{ narrativa_criterios[criterio.id] }}
{% endfor %}

Da análise das respostas ao item 2102 e da documentação apresentada, verificou-se que a rotina de acompanhamento, revisão ou atualização periódica do plano de TIC não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
* {{ motivo.texto.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência de sistemática documentada de acompanhamento e revisão periódica diverge dos critérios aplicáveis, impedindo o controle sobre o alcance das metas e a reprogramação tempestiva de iniciativas.

{% endif %}

#### Conclusão

As fragilidades identificadas no planejamento de TIC reduzem a segurança de que a organização disponha, conforme aplicável ao caso concreto, de processo e instrumento suficientes para direcionar iniciativas, priorizar recursos, alinhar projetos às necessidades institucionais e integrar orçamento e contratações à estratégia de tecnologia.

Em razão das lacunas descritas, são propostas determinações voltadas à adequação dos aspectos de planejamento de TIC efetivamente apontados neste achado, observados os critérios aplicáveis indicados nas seções anteriores.

{% include 'bloco_encaminhamentos_achado.md' %}

{# Final do Achado - Planejamento de TIC #}
{% endif %}
