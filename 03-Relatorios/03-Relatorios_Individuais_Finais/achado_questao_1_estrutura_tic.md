{% set nome_achado = 'Estrutura de TIC insuficientemente formalizada, definida ou posicionada para gerir a tecnologia da informação.' %}
{% set achado = auditado.get_achado_por_nome(nome_achado) %}
{% if achado %}
{% set narrativa_criterios = {
    'Q1.C1':
        'O COBIT 2019, na prática APO01.04, orienta a definição e a implementação das estruturas organizacionais necessárias para apoiar os objetivos de governança e gestão de TIC.',

    'Q1.C2':
        'A prática APO01.05 do COBIT 2019 orienta a definição, comunicação e manutenção de papéis e responsabilidades relacionados à governança e gestão de TIC.',

    'Q1.C3':
        'O COBIT 2019, na prática APO01.06, orienta o posicionamento da função de tecnologia de modo compatível com sua relevância estratégica e com a necessidade de interação com a alta administração.',

    'Q1.C6':
        'Como referência de posicionamento organizacional, o art. 4º, § 1º, da Portaria SGD/ME nº 778/2019 prevê que a área de TIC deve, preferencialmente, estar vinculada à alta administração para apoiá-la na tomada de decisões e no alcance dos objetivos estratégicos.',

    'Q1.C7':
        'A formalização da estrutura e a definição clara de competências também se relacionam ao princípio da eficiência previsto no art. 37, caput, da Constituição Federal.',

    'Q1.C8':
        'Para os órgãos e entidades do Poder Executivo Estadual, o art. 4º do Decreto Estadual nº 48.997/2024 determina que o nível setorial do SETIC seja representado por assessoria de informática ou setor equivalente e exerça as competências de TIC previstas no dispositivo.',

    'Q1.C9':
        'Para os órgãos do Poder Judiciário Estadual, o art. 21 da Resolução CNJ nº 370/2021 determina que cada órgão constitua e mantenha estruturas organizacionais adequadas e compatíveis com a demanda de TIC, contemplando os macroprocessos mínimos definidos no dispositivo.',

    'Q1.C10':
        'Para o Ministério Público Estadual, o art. 16 da Resolução CNMP nº 171/2017 estabelece que a gestão de TI compete à área de TI da unidade ou do ramo, à qual são atribuídas as atividades previstas no dispositivo.',

    'Q1.C11':
        'No âmbito do Ministério Público Estadual, o art. 1º da Resolução GPGJ nº 2.675/2025 dispõe que a Secretaria-Geral de Modernização Tecnológica e Inovação do MPRJ é diretamente subordinada ao Procurador-Geral de Justiça.'
} %}
{% set situacao_formalizacao = 'Ausência de área, unidade, setor ou função de TIC formalmente instituída.' %}
{% set situacao_atribuicoes = 'Área de TIC sem atribuições formalmente definidas ou sem atribuições formais de gestão de TIC.' %}
{% set situacao_posicionamento = 'Posicionamento organizacional inadequado da área de TIC.' %}
{% set motivos_formalizacao = auditado.get_motivos_situacao(nome_achado, situacao_formalizacao) %}
{% set motivos_atribuicoes = auditado.get_motivos_situacao(nome_achado, situacao_atribuicoes) %}
{% set motivos_posicionamento = auditado.get_motivos_situacao(nome_achado, situacao_posicionamento) %}
{% set tem_formalizacao = situacao_formalizacao in achado.situacoes_encontradas and motivos_formalizacao %}
{% set tem_atribuicoes = situacao_atribuicoes in achado.situacoes_encontradas and motivos_atribuicoes %}
{% set tem_posicionamento = situacao_posicionamento in achado.situacoes_encontradas and motivos_posicionamento %}
{% set qtd_situacoes_exibidas = (1 if tem_formalizacao else 0) + (1 if tem_atribuicoes else 0) + (1 if tem_posicionamento else 0) %}

\newpage

## Achado {{ achado.numero }} – {{ achado.nome }}

{% include 'bloco_criterios_achado.md' %}

{% include 'bloco_evidencias_achado.md' %}

### Situação encontrada

A existência de estrutura formal de TIC é requisito básico para que a organização disponha de unidade, setor ou função institucionalmente reconhecida para planejar, coordenar, gerir, executar, monitorar e controlar o uso da tecnologia da informação. Sob a perspectiva de governança de TIC, essa estruturação envolve três dimensões complementares: formalização da área ou função de TIC, definição de atribuições e competências essenciais e posicionamento organizacional adequado para participar das decisões estratégicas, orçamentárias, contratuais e de gestão de riscos.

Para que a governança de TIC opere com eficácia, é indispensável que a organização estabeleça formalmente suas estruturas de tecnologia, defina com clareza as competências e responsabilidades de gestão e assegure posicionamento organizacional compatível com sua relevância institucional. A observância desses parâmetros confere legitimidade às decisões, viabiliza a integração da tecnologia aos objetivos estratégicos e mitiga riscos de atuação desarticulada ou reativa.

Com base na análise das respostas aos itens 0101, 0102 e 0103 do questionário aplicado e da avaliação das evidências documentais anexadas, não foi demonstrado atendimento integral a esses requisitos de governança. A Equipe de Auditoria identificou as seguintes deficiências na estrutura de TIC da organização:

{% if tem_formalizacao %}
* **Formalização da área de TIC**: ausência de ato formal de criação ou instituição da área ou função de TIC na estrutura organizacional, em desacordo com os critérios de governança aplicáveis, o que prejudica a responsabilização e o alinhamento da tecnologia aos objetivos institucionais.
{% endif %}
{% if tem_atribuicoes %}
* **Atribuições da área de TIC**: ausência ou insuficiência de competências formais para planejamento, coordenação, gestão e controle da TIC, divergindo das diretrizes de governança aplicáveis, o que favorece atuação reativa e fragmentada da tecnologia.
{% endif %}
{% if tem_posicionamento %}
* **Posicionamento organizacional**: posicionamento hierárquico da área de TIC em nível incompatível com sua relevância estratégica, em descompasso com os parâmetros de governança aplicáveis, o que reduz sua capacidade de influência institucional e compromete sua participação nas decisões estratégicas e orçamentárias.
{% endif %}

{% if qtd_situacoes_exibidas == 1 %}
Essa situação ensejou o presente achado e será detalhada na subseção seguinte.
{% else %}
Essas situações ensejaram o presente achado e serão detalhadas nas subseções seguintes.
{% endif %}

{% set situacao = situacao_formalizacao %}
{% if tem_formalizacao %}
{% set criterios_formalizacao = auditado.get_criterios_situacao(nome_achado, 'S1.1') %}
#### Formalização da área, unidade, setor ou função de TIC

A formalização da área, unidade, setor ou função de TIC é necessária para conferir reconhecimento institucional à atividade de tecnologia da informação, definir sua vinculação na estrutura organizacional e permitir a atribuição clara de responsabilidades.

{% for criterio in criterios_formalizacao %}
{{ narrativa_criterios[criterio.id] }}
{% endfor %}

No contexto da fiscalização, essa formalização deve ser demonstrada por regimento, decreto, portaria, resolução, organograma, ato administrativo ou instrumento equivalente. A ausência de evidência suficiente de formalização fragiliza a identificação da unidade responsável pela coordenação da TIC e compromete a responsabilização por decisões, controles, serviços e investimentos de tecnologia.

Da análise da resposta ao item 0101 e da documentação apresentada, não foi demonstrada, com base nos elementos encaminhados, a formalização de área, unidade, setor ou função de TIC na estrutura organizacional, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = motivos_formalizacao -%}
{% if motivos %}

{% for motivo in motivos -%}
* {{ motivo.texto.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência de ato formal de instituição da área ou função de TIC contraria os critérios aplicáveis, materializando o risco de inexistência de unidade ou função institucionalmente reconhecida para coordenar o uso da tecnologia da informação e prejudicando o alinhamento da TIC aos objetivos da organização.

{% endif %}

{% set situacao = situacao_atribuicoes %}
{% if tem_atribuicoes %}
{% set criterios_atribuicoes = auditado.get_criterios_situacao(nome_achado, 'S1.2') %}
#### Atribuições formais da área de TIC

A definição formal de atribuições da área de TIC é indispensável para delimitar responsabilidades, reduzir sobreposição ou lacunas de atuação e permitir que a gestão de tecnologia seja exercida de forma planejada e controlada.

{% for criterio in criterios_atribuicoes %}
{{ narrativa_criterios[criterio.id] }}
{% endfor %}

A ausência de atribuições formalmente definidas ou a especificação de competências insuficientes para planejamento, coordenação, gestão, execução, monitoramento e controle da TIC expõe a organização a uma atuação reativa e fragmentada, com baixa clareza sobre os responsáveis por processos, serviços, riscos, contratações e controles de tecnologia.

Da análise das respostas aos itens 0101 e 0103 e da documentação apresentada, não foi demonstrada, com base nos elementos encaminhados, a formalização suficiente das atribuições da área de TIC abrangendo planejamento, coordenação, gestão, execução, monitoramento e controle da tecnologia da informação, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = motivos_atribuicoes -%}
{% if motivos %}

{% for motivo in motivos -%}
* {{ motivo.texto.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

O cenário identificado diverge dos critérios aplicáveis ao não demonstrar atribuições formais suficientes para a gestão da tecnologia da informação, o que compromete a capacidade de coordenação da área e reduz a efetividade dos processos de governança institucional.

{% endif %}

{% set situacao = situacao_posicionamento %}
{% if tem_posicionamento %}
{% set criterios_posicionamento = auditado.get_criterios_situacao(nome_achado, 'S1.3') %}
#### Posicionamento organizacional da área de TIC

O posicionamento organizacional da área de TIC deve ser compatível com suas responsabilidades institucionais e com a dependência da organização em relação à tecnologia da informação. Não se trata de impor modelo único de estrutura, mas de assegurar que a função de TIC tenha capacidade de interação adequada com as instâncias decisórias responsáveis por estratégia, orçamento, contratações, riscos e prestação de serviços.

{% for criterio in criterios_posicionamento %}
{{ narrativa_criterios[criterio.id] }}
{% endfor %}

No âmbito da fiscalização, o posicionamento adequado deve ser demonstrado por organograma institucional, regimento interno ou documento equivalente, de modo que seja possível verificar a vinculação da área de TIC e sua compatibilidade com as responsabilidades que lhe foram atribuídas.

Da análise das respostas aos itens 0101 e 0102 e da documentação apresentada, o posicionamento organizacional da área de TIC não se mostrou suficientemente compatível com a relevância e as responsabilidades da função de tecnologia da informação, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = motivos_posicionamento -%}
{% if motivos %}

{% for motivo in motivos -%}
* {{ motivo.texto.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A subordinação da área de TIC em nível hierárquico distante da alta administração contraria as diretrizes de governança aplicáveis, reduz sua capacidade de interlocução institucional e prejudica sua participação direta em decisões estratégicas, orçamentárias e de gestão de riscos.

{% endif %}

#### Conclusão

As fragilidades identificadas na estrutura de TIC reduzem a segurança de que a organização disponha de condições institucionais suficientes para coordenar, gerir e sustentar a tecnologia da informação de forma alinhada às necessidades institucionais.

Em razão das lacunas descritas, são propostas medidas de encaminhamento, na forma de recomendação ou determinação, conforme a situação e o regime normativo aplicável à organização, observados os critérios indicados neste achado.

{% include 'bloco_encaminhamentos_achado.md' %}

{## Final do Achado - Estrutura de TIC ##}
{% endif %}
