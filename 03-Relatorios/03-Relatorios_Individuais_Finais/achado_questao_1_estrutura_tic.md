{% set nome_achado = 'Estrutura de TIC insuficientemente formalizada, definida ou posicionada para gerir a tecnologia da informação.' %}
{% set achado = auditado.get_achado_por_nome(nome_achado) %}
{% if achado %}
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

Os critérios aplicáveis indicam que a organização deve estabelecer estrutura de TIC apropriada, definir e comunicar papéis e responsabilidades e posicionar a função de tecnologia de modo compatível com sua relevância estratégica. Esses requisitos decorrem dos objetivos APO01.04, APO01.05 e APO01.06 do COBIT 2019, conforme a situação examinada. Para o posicionamento organizacional, considera-se ainda a referência de vinculação preferencial da área de TIC à alta administração prevista no art. 4º, § 1º, da Portaria SGD/ME nº 778/2019. A formalização da estrutura e das atribuições também se relaciona ao princípio da eficiência previsto no art. 37, caput, da Constituição Federal.

Com base na análise das respostas aos itens 0101, 0102 e 0103 do questionário aplicado e da avaliação das evidências documentais anexadas, não foi demonstrado atendimento integral a esses requisitos de governança. A Equipe de Auditoria identificou as seguintes deficiências na estrutura de TIC da organização:

{% if tem_formalizacao %}
* **Formalização da área de TIC**: a ausência da formalização da área, unidade, setor ou função de TIC não demonstra aderência ao critério de definição de estruturas organizacionais do COBIT 2019, APO01.04, nem ao princípio da eficiência previsto no art. 37, caput, da Constituição Federal, o que pode prejudicar a responsabilização e o alinhamento da TIC aos objetivos institucionais.
{% endif %}
{% if tem_atribuicoes %}
* **Atribuições da área de TIC**: a insuficiência das atribuições formais da área de TIC não demonstra aderência ao critério de definição de papéis e responsabilidades do COBIT 2019, APO01.05, nem ao princípio da eficiência previsto no art. 37, caput, da Constituição Federal, o que pode favorecer atuação reativa e fragmentada por falta de clareza sobre responsabilidades de planejamento, coordenação, gestão e controle da TIC.
{% endif %}
{% if tem_posicionamento %}
* **Posicionamento organizacional**: o posicionamento informado não demonstrou compatibilidade suficiente com a relevância e as responsabilidades da função de TIC, conforme o critério do COBIT 2019, APO01.06, e a referência preferencial da Portaria SGD/ME nº 778/2019, art. 4º, § 1º, o que pode reduzir a capacidade de influência institucional da TIC e comprometer sua participação em decisões estratégicas, orçamentárias, contratuais e de gestão de riscos.
{% endif %}

{% if qtd_situacoes_exibidas == 1 %}
Essa situação ensejou o presente achado e será detalhada na subseção seguinte.
{% else %}
Essas situações ensejaram o presente achado e serão detalhadas nas subseções seguintes.
{% endif %}

{% set situacao = situacao_formalizacao %}
{% if tem_formalizacao %}
#### Formalização da área, unidade, setor ou função de TIC

A formalização da área, unidade, setor ou função de TIC é necessária para conferir reconhecimento institucional à atividade de tecnologia da informação, definir sua vinculação na estrutura organizacional e permitir a atribuição clara de responsabilidades.

O COBIT 2019, no objetivo APO01.04, orienta que a organização defina e implemente estruturas organizacionais necessárias para apoiar os objetivos de governança e gestão de TI. A formalização também contribui para a eficiência administrativa prevista no art. 37, caput, da Constituição Federal, ao explicitar a unidade ou função responsável pela TIC.

No contexto da fiscalização, essa formalização deve ser demonstrada por regimento, decreto, portaria, resolução, organograma, ato administrativo ou instrumento equivalente. A ausência de evidência suficiente de formalização fragiliza a identificação da unidade responsável pela coordenação da TIC e compromete a responsabilização por decisões, controles, serviços e investimentos de tecnologia.

Da análise da resposta ao item 0101 e da documentação apresentada, não foi demonstrada, com base nos elementos encaminhados, a formalização de área, unidade, setor ou função de TIC na estrutura organizacional, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = motivos_formalizacao -%}
{% if motivos %}

{% for motivo in motivos -%}
* {{ motivo.texto.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A não demonstração dessa formalização materializa o risco de inexistência de unidade ou função institucionalmente reconhecida para coordenar o uso da tecnologia da informação, prejudicando o alinhamento da TIC aos objetivos da organização.

{% endif %}

{% set situacao = situacao_atribuicoes %}
{% if tem_atribuicoes %}
#### Atribuições formais da área de TIC

A definição formal de atribuições da área de TIC é indispensável para delimitar responsabilidades, reduzir sobreposição ou lacunas de atuação e permitir que a gestão de tecnologia seja exercida de forma planejada e controlada.

O COBIT 2019, no objetivo APO01.05, orienta a definição, comunicação e manutenção de papéis e responsabilidades relacionados à governança e gestão de TI. Essa orientação abrange atribuições essenciais como governança, planejamento, gestão, sustentação tecnológica, sistemas, segurança da informação, contratos, dados e atividades correlatas.

A ausência de atribuições formalmente definidas ou a especificação de competências insuficientes para planejamento, coordenação, gestão, execução, monitoramento e controle da TIC expõe a organização a uma atuação reativa e fragmentada, com baixa clareza sobre os responsáveis por processos, serviços, riscos, contratações e controles de tecnologia.

Da análise das respostas aos itens 0101 e 0103 e da documentação apresentada, não foi demonstrada, com base nos elementos encaminhados, a formalização suficiente das atribuições da área de TIC abrangendo planejamento, coordenação, gestão, execução, monitoramento e controle da tecnologia da informação, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = motivos_atribuicoes -%}
{% if motivos %}

{% for motivo in motivos -%}
* {{ motivo.texto.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A não demonstração de atribuições formais suficientes compromete a capacidade de gestão da TIC e reduz a efetividade dos demais processos de governança e gestão, uma vez que a estrutura organizacional não explicita, de forma suficiente, quem deve decidir, executar, acompanhar e responder pelos resultados de tecnologia da informação.

{% endif %}

{% set situacao = situacao_posicionamento %}
{% if tem_posicionamento %}
#### Posicionamento organizacional da área de TIC

O posicionamento organizacional da área de TIC deve ser compatível com suas responsabilidades institucionais e com a dependência da organização em relação à tecnologia da informação. Não se trata de impor modelo único de estrutura, mas de assegurar que a função de TIC tenha capacidade de interação adequada com as instâncias decisórias responsáveis por estratégia, orçamento, contratações, riscos e prestação de serviços.

O COBIT 2019, no objetivo APO01.06, orienta o aprimoramento do posicionamento da função de TI para que a tecnologia seja tratada de modo compatível com sua relevância estratégica e com a necessidade de interação com a alta administração. Como referência complementar, o art. 4º, § 1º, da Portaria SGD/ME nº 778/2019 estabelece que a área de TIC deve, preferencialmente, estar vinculada à alta administração, com o intuito de apoiá-la na tomada de decisões e no alcance dos objetivos estratégicos.

Um posicionamento organizacional incompatível com a relevância e as responsabilidades da TIC acarreta o risco de baixa capacidade de influência institucional. Essa fragilidade compromete a participação da área em decisões estratégicas, orçamentárias, contratuais e de gestão de riscos, além de dificultar a priorização de iniciativas e a articulação com as áreas de negócio.

No âmbito da fiscalização, o posicionamento adequado deve ser demonstrado por organograma institucional, regimento interno ou documento equivalente, de modo que seja possível verificar a vinculação da área de TIC e sua compatibilidade com as responsabilidades que lhe foram atribuídas.

Da análise das respostas aos itens 0101 e 0102 e da documentação apresentada, o posicionamento organizacional da área de TIC não se mostrou suficientemente compatível com a relevância e as responsabilidades da função de tecnologia da informação, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = motivos_posicionamento -%}
{% if motivos %}

{% for motivo in motivos -%}
* {{ motivo.texto.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

{% endif %}

#### Conclusão

As fragilidades identificadas na estrutura de TIC reduzem a segurança de que a organização disponha de condições institucionais suficientes para coordenar, gerir e sustentar a tecnologia da informação de forma alinhada às necessidades institucionais.

Em razão das lacunas descritas, são propostas medidas de encaminhamento, na forma de recomendação ou determinação, conforme a situação e o regime normativo aplicável à organização, observados os critérios indicados neste achado.

{% include 'bloco_encaminhamentos_achado.md' %}

{## Final do Achado - Estrutura de TIC ##}
{% endif %}
