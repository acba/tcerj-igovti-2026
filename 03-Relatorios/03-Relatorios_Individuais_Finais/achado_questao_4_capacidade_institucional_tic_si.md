{% set id_achado = 'Q4' %}{# Q4 — Capacidade institucional de pessoal de TIC e SI #}
{% set achado = auditado.get_achado_por_id(id_achado) %}
{% if achado %}
{% set narrativa_criterios = {
    'Q4.C1':
        'A prática APO01.05 do COBIT 2019 orienta a definição, comunicação e manutenção de papéis e responsabilidades formalmente atribuídos.',

    'Q4.C2':
        'A prática APO07.01 do COBIT 2019 orienta assegurar quantidade e perfil de profissionais compatíveis com as necessidades institucionais de TIC.',

    'Q4.C5':
        'A prática APO07.05 do COBIT 2019 orienta o planejamento, a alocação e o acompanhamento da capacidade de pessoal para as atividades e serviços de TIC.',

    'Q4.C6':
        'A prática APO07.06 do COBIT 2019 orienta controlar o uso de pessoal contratado ou terceirizado, preservando a responsabilização, supervisão e retenção de conhecimento na organização.',

    'Q4.C12':
        'O Acórdão 1.411/2014-TCU-Plenário, item 9.1.6.5, estabelece precedente no sentido de que o planejamento de TIC contemple o quantitativo necessário ou ideal da força de trabalho.',

    'Q4.C13':
        'O Acórdão 1.411/2014-TCU-Plenário, item 9.1.7, orienta a adoção de providências para dotar a área de tecnologia de quantitativo de pessoal adequado às necessidades institucionais.',

    'Q4.C14':
        'O Acórdão TCE-RJ nº 44.490/2024-PLEN, item I.10.11, constitui precedente para a avaliação da estrutura de recursos humanos de TIC e a preservação de capacidade interna em atividades de planejamento, coordenação, fiscalização e controle.',

    'Q4.C15':
        'Para os órgãos do Poder Judiciário Estadual, o art. 24 da Resolução CNJ nº 370/2021 determina a composição de quadro permanente de servidores dedicados à área de TIC em quantitativo compatível com a demanda e com o referencial aplicável.',

    'Q4.C16':
        'Para os órgãos do Poder Judiciário Estadual, o art. 8º, § 1º, da Resolução CNJ nº 468/2022 determina que a assessoria técnica terceirizada ao planejamento e à avaliação da qualidade de soluções de TIC permaneça sob supervisão exclusiva de membro ou servidor do órgão.'
} %}
{% set s_forca_trabalho = auditado.get_situacao(id_achado, 'S4.1') %}{# S4.1 — Força de trabalho dedicada à TIC #}
{% set s_dimensionamento = auditado.get_situacao(id_achado, 'S4.2') %}{# S4.2 — Dimensionamento da força de trabalho de TIC e SI #}
{% set s_cargos_funcoes = auditado.get_situacao(id_achado, 'S4.3') %}{# S4.3 — Cargos ou funções formais de segurança da informação #}
{% set s_terceiros = auditado.get_situacao(id_achado, 'S4.6') %}{# S4.6 — Operação predominantemente terceirizada #}
{% set situacoes_achado = [s_forca_trabalho, s_dimensionamento, s_cargos_funcoes, s_terceiros] %}
{% set qtd_situacoes_exibidas = situacoes_achado | selectattr('ativa') | list | length %}

## Achado {{ achado.numero }} – {{ achado.nome }}

{% include 'bloco_criterios_achado.md' %}

{% include 'bloco_evidencias_achado.md' %}

### Situação encontrada

A capacidade institucional de TIC e segurança da informação pressupõe força de trabalho compatível, dimensionamento documentado, funções formalmente atribuídas e capacidade interna para planejar, coordenar, gerir, proteger, contratar, fiscalizar e sustentar o ambiente tecnológico.

A existência de equipes qualificadas e devidamente dimensionadas é indispensável para que a administração pública execute serviços digitais seguros e mantenha a continuidade operacional. O estabelecimento de processos de planejamento de pessoal, a definição de atribuições específicas de proteção à informação e a preservação de competências técnicas internas reduzem a vulnerabilidade do ambiente computacional e resguardam os ativos da organização.

Com base na análise das respostas aos itens 0101, 0105, 2703 e 2708 e das evidências documentais anexadas, não foi demonstrada capacidade institucional suficiente. A Equipe de Auditoria identificou fragilidades nos seguintes aspectos:

{% if s_forca_trabalho.ativa %}
* **Força de trabalho dedicada à TIC**: ausência de profissionais dedicados com atuação regular em TIC, em desacordo com os parâmetros de governança aplicáveis, comprometendo rotinas essenciais de sustentação, planejamento e contratação tecnológica.
{% endif %}
{% if s_dimensionamento.ativa %}
* **Dimensionamento de pessoal de TIC e segurança**: ausência de definição técnica documentada do quantitativo ideal da força de trabalho, divergindo das diretrizes aplicáveis, elevando o risco de subdimensionamento e alocação inadequada de recursos humanos.
{% endif %}
{% if s_cargos_funcoes.ativa %}
* **Cargos ou funções formais de segurança da informação**: ausência de atribuição formal de cargos ou funções específicas para a área de segurança da informação, em desacordo com as práticas de governança aplicáveis, reduzindo a clareza sobre quem responde pelos controles e medidas de proteção à informação.
{% endif %}
{% if s_terceiros.ativa %}
* **Operação predominantemente terceirizada**: execução de atividades de TIC dependente de terceiros sem profissionais internos suficientes para coordenação e supervisão, contrariando os critérios aplicáveis, elevando o risco de perda de governabilidade e retenção de conhecimento.
{% endif %}

{% if qtd_situacoes_exibidas == 1 %}
Essa situação ensejou o presente achado e será detalhada na subseção seguinte.
{% else %}
Essas situações ensejaram o presente achado e serão detalhadas nas subseções seguintes.
{% endif %}

{% if s_forca_trabalho.ativa %}
#### Força de trabalho dedicada à TIC

A organização deve dispor de força de trabalho dedicada à TIC, compatível com sua estrutura, porte, serviços prestados, sistemas mantidos, contratações e riscos relevantes.

{% for criterio in s_forca_trabalho.criterios %}
{{ narrativa_criterios[criterio.id] }}
{% endfor %}

Da análise das respostas aos itens 0101 e 0105, verificou-se que não foi demonstrada a existência de profissional que atuasse regularmente em TIC, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% if s_forca_trabalho.motivos %}

{% for motivo in s_forca_trabalho.motivos -%}
* {{ motivo.texto.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A inexistência de profissionais dedicados à tecnologia diverge das diretrizes aplicáveis, reduzindo criticamente a capacidade da organização de gerir sistemas, fiscalizar contratos e sustentar as operações de TIC.

{% endif %}

{% if s_dimensionamento.ativa %}
#### Quantitativo necessário de pessoal de TIC e segurança da informação

A definição do quantitativo necessário de pessoal permite avaliar se a força de trabalho disponível é compatível com as demandas, riscos e responsabilidades da organização.

{% for criterio in s_dimensionamento.criterios %}
{{ narrativa_criterios[criterio.id] }}
{% endfor %}

Da análise das respostas ao item 2703 e da documentação apresentada, verificou-se que a definição do quantitativo necessário de pessoal de TIC e segurança da informação com base em critério ou procedimento técnico não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% if s_dimensionamento.motivos %}

{% for motivo in s_dimensionamento.motivos -%}
* {{ motivo.texto.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência de dimensionamento técnico documentado contraria as orientações aplicáveis, privando a gestão de parâmetros objetivos para fundamentar planos de capacitação, contratações ou provimentos na área de tecnologia e segurança da informação.

{% endif %}

{% if s_cargos_funcoes.ativa %}
#### Cargos ou funções formalmente atribuídos à área de segurança da informação

A atribuição formal de cargos ou funções dedicados à área de segurança da informação é indispensável para delimitar responsabilidades na proteção de dados, gestão de vulnerabilidades e resposta a incidentes, prevenindo a dispersão ou improvisação de atribuições críticas.

{% for criterio in s_cargos_funcoes.criterios %}
{{ narrativa_criterios[criterio.id] }}
{% endfor %}

Da análise das respostas ao item 2708 e da documentação apresentada, verificou-se que a existência de cargos ou funções formalmente atribuídos à área de segurança da informação não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% if s_cargos_funcoes.motivos %}

{% for motivo in s_cargos_funcoes.motivos -%}
* {{ motivo.texto.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência de cargos ou funções formalmente atribuídos à área de segurança da informação diverge dos critérios aplicáveis, comprometendo a clareza institucional sobre quem responde pelos controles e medidas de proteção e enfraquecendo a postura de segurança cibernética da organização.

{% endif %}

{% if s_terceiros.ativa %}
#### Operação predominantemente terceirizada sem profissionais internos de TIC

A utilização de terceiros ou de estrutura externa para execução de atividades de TIC não elimina a responsabilidade da organização pela coordenação, planejamento, aprovação técnica, fiscalização contratual e retenção de conhecimento.

{% for criterio in s_terceiros.criterios %}
{{ narrativa_criterios[criterio.id] }}
{% endfor %}

Da análise das respostas aos itens 0101 e 0105 e da documentação apresentada, verificou-se que a existência de capacidade interna para coordenar, planejar, fiscalizar e reter conhecimento quando a operação de TIC depende de terceiros ou de estrutura externa não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% if s_terceiros.motivos %}

{% for motivo in s_terceiros.motivos -%}
* {{ motivo.texto.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

O estabelecimento de modelo operacional baseado predominantemente em terceiros sem capacidade interna de supervisão contraria as diretrizes de governança aplicáveis, reduzindo a governabilidade técnica, a retenção de conhecimento e a continuidade das operações de TIC.

{% endif %}

#### Conclusão

As fragilidades identificadas na capacidade institucional de TIC e segurança da informação reduzem a segurança de que a organização disponha, conforme aplicável ao caso concreto, de força de trabalho, dimensionamento documentado, cargos ou funções formalmente atribuídos e mecanismos de supervisão suficientes para sustentar a gestão, a proteção, as contratações, a fiscalização e a continuidade dos serviços tecnológicos.

Em razão das lacunas descritas, são propostas medidas de encaminhamento, na forma de recomendação ou determinação, conforme a situação e o regime normativo aplicável à organização, observados os critérios indicados nas seções anteriores.

{% include 'bloco_encaminhamentos_achado.md' %}

{# Final do Achado - Capacidade institucional de TIC e segurança da informação #}
{% endif %}
