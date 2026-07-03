{% set nome_achado = 'Estrutura de TIC insuficiente para coordenar, gerir e sustentar a tecnologia da informação.' %}
{% set achado = auditado.get_achado_por_nome(nome_achado) %}
{% if achado %}
{% set situacao_formalizacao = 'Ausência de área, unidade, setor ou função de TIC formalmente instituída.' %}
{% set situacao_atribuicoes = 'Área de TIC sem atribuições formais suficientes para planejamento, coordenação, gestão, execução, monitoramento e controle da TIC.' %}
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

### Critérios
{% if tem_formalizacao %}
* COBIT 2019, APO01.04 - Definir e implementar as estruturas organizacionais: estabelecer estruturas organizacionais internas e externas necessárias para apoiar os objetivos de governança e gestão de TI;
{% endif %}
{% if tem_atribuicoes %}
* COBIT 2019, APO01.05 - Estabelecer papéis e responsabilidades: definir, comunicar e manter papéis e responsabilidades relacionados à governança e gestão de TI;
{% endif %}
{% if tem_posicionamento %}
* COBIT 2019, APO01.06 - Aprimorar o posicionamento da função de TI: posicionar a função de tecnologia de modo compatível com sua relevância estratégica, responsabilidades e necessidade de interação com a alta administração;
{% endif %}
{% if tem_formalizacao or tem_atribuicoes %}
* COBIT 2019, APO01.09 - Definição e comunicação de políticas e procedimentos: estabelecer e comunicar políticas e procedimentos de gestão de TI que orientem papéis, responsabilidades e controles;
{% endif %}
{% if tem_formalizacao or tem_atribuicoes or tem_posicionamento %}
* ABNT NBR ISO/IEC 38500:2025, item 5.6.1 - Governança efetiva de TI: responsabilização clara, estrutura adequada de tomada de decisão e direção organizacional compatível com o uso atual e futuro da tecnologia;
{% endif %}
{% if tem_posicionamento %}
* Portaria SGD/ME nº 778/2019, art. 4º, § 1º - Como referência de boa prática, a área de TIC deve, preferencialmente, estar vinculada à alta administração para apoiá-la na tomada de decisões e no alcance dos objetivos estratégicos.
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

A existência de estrutura formal de TIC é requisito básico para que a organização disponha de unidade, setor ou função institucionalmente reconhecida para planejar, coordenar, gerir, executar, monitorar e controlar o uso da tecnologia da informação. Sob a perspectiva de governança de TIC, essa estruturação envolve três dimensões complementares: formalização da área ou função de TIC, definição de atribuições e competências essenciais e posicionamento organizacional adequado para participar das decisões estratégicas, orçamentárias, contratuais e de gestão de riscos.

Os critérios de boas práticas indicam que a organização deve estabelecer estruturas organizacionais apropriadas, comunicar papéis e responsabilidades de maneira clara, definir políticas e procedimentos de gestão de TIC e posicionar a função de tecnologia de modo compatível com sua relevância estratégica[^explica_estrutura_tic_cobit]. Esses requisitos convergem com as diretrizes da ABNT NBR ISO/IEC 38500:2025, que orienta sobre a necessidade de responsabilização clara e de estruturas adequadas de tomada de decisão para a governança efetiva de TI[^explica_estrutura_tic_iso38500], e com a referência de vinculação preferencial da área de TIC à alta administração prevista no art. 4º, § 1º, da Portaria SGD/ME nº 778/2019.

Com base na análise das respostas aos itens 0101, 0102 e 0103 do questionário aplicado e da avaliação das evidências documentais anexadas, não foi demonstrado atendimento integral a esses requisitos de governança. A Equipe de Auditoria identificou as seguintes deficiências na estrutura de TIC da organização:

{% if tem_formalizacao %}
* **Formalização da área de TIC**: a ausência de demonstração da formalização da área, unidade, setor ou função de TIC não evidencia aderência aos critérios de definição de estruturas organizacionais e de comunicação de políticas e procedimentos (COBIT 2019, APO01.04/APO01.09 e ABNT NBR ISO/IEC 38500:2025, item 5.6.1), o que pode prejudicar a responsabilização e o alinhamento da TIC aos objetivos institucionais.
{% endif %}
{% if tem_atribuicoes %}
* **Atribuições da área de TIC**: a insuficiência de comprovação das atribuições formais da área de TIC não evidencia aderência aos critérios de definição de papéis e responsabilidades e de comunicação de políticas e procedimentos (COBIT 2019, APO01.05/APO01.09 e ABNT NBR ISO/IEC 38500:2025, item 5.6.1), o que pode favorecer atuação reativa e fragmentada por falta de clareza sobre responsabilidades de planejamento, coordenação, gestão, execução, monitoramento e controle da TIC.
{% endif %}
{% if tem_posicionamento %}
* **Posicionamento organizacional**: o posicionamento informado não demonstrou compatibilidade suficiente com a relevância e as responsabilidades da função de TIC, em desacordo com o critério de aprimoramento do posicionamento da função de TI (COBIT 2019, APO01.06 e ABNT NBR ISO/IEC 38500:2025, item 5.6.1) e com a referência da Portaria SGD/ME nº 778/2019 (art. 4º, § 1º), o que pode reduzir a capacidade de influência institucional da TIC e comprometer sua participação em decisões estratégicas, orçamentárias, contratuais e de gestão de riscos.
{% endif %}

{% if qtd_situacoes_exibidas == 1 %}
Essa situação ensejou o presente achado e será detalhada na subseção seguinte.
{% else %}
Essas situações ensejaram o presente achado e serão detalhadas nas subseções seguintes.
{% endif %}

[^explica_estrutura_tic_cobit]: No domínio APO01 do COBIT 2019, a gestão da estrutura organizacional, de papéis, responsabilidades, políticas e posicionamento da função de TI é tratada como condição para que a tecnologia apoie os objetivos de governança e gestão da organização.

[^explica_estrutura_tic_iso38500]: A ABNT NBR ISO/IEC 38500:2025 orienta que a governança efetiva de TI pressupõe responsabilidades claras, estrutura adequada de decisão e direção organizacional compatível com o uso atual e futuro da tecnologia.

{% set situacao = situacao_formalizacao %}
{% if tem_formalizacao %}
#### Formalização da área, unidade, setor ou função de TIC

A formalização da área, unidade, setor ou função de TIC é necessária para conferir reconhecimento institucional à atividade de tecnologia da informação, definir sua vinculação na estrutura organizacional e permitir a atribuição clara de responsabilidades.

O COBIT 2019, no objetivo APO01.04, orienta que a organização defina e implemente estruturas organizacionais necessárias para apoiar os objetivos de governança e gestão de TI. De forma complementar, o APO01.09 trata da definição e comunicação de políticas e procedimentos que orientem papéis, responsabilidades e controles.

No contexto da fiscalização, essa formalização deve ser demonstrada por regimento, decreto, portaria, resolução, organograma, ato administrativo ou instrumento equivalente. A ausência de evidência suficiente de formalização fragiliza a identificação da unidade responsável pela coordenação da TIC e compromete a responsabilização por decisões, controles, serviços e investimentos de tecnologia.

Da análise da resposta ao item 0101 e da documentação apresentada, não foi demonstrada, com base nos elementos encaminhados, a formalização de área, unidade, setor ou função de TIC na estrutura organizacional, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = motivos_formalizacao -%}
{% if motivos %}

{% for motivo in motivos -%}
{% set refs_motivo = motivo.get('refs', []) -%}
* {{ motivo.texto.rstrip('.;') }}{% if refs_motivo %} ({{ refs_motivo | join(', ') }}){% endif %}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A não demonstração dessa formalização materializa o risco de inexistência de unidade ou função institucionalmente reconhecida para coordenar o uso da tecnologia da informação, prejudicando o alinhamento da TIC aos objetivos da organização.

Diante disso, __será proposta recomendação para que a organização formalize a área, unidade, setor ou função de TIC em regimento, decreto, portaria, resolução, organograma ou instrumento equivalente, compatível com seu porte, complexidade e dependência tecnológica.__

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
{% set refs_motivo = motivo.get('refs', []) -%}
* {{ motivo.texto.rstrip('.;') }}{% if refs_motivo %} ({{ refs_motivo | join(', ') }}){% endif %}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A não demonstração de atribuições formais suficientes compromete a capacidade de gestão da TIC e reduz a efetividade dos demais processos de governança e gestão, uma vez que a estrutura organizacional não explicita, de forma suficiente, quem deve decidir, executar, acompanhar e responder pelos resultados de tecnologia da informação.

Diante disso, __será proposta recomendação para que a organização defina formalmente as atribuições da área de TIC, contemplando planejamento, coordenação, gestão, execução, monitoramento e controle da TIC.__

{% endif %}

{% set situacao = situacao_posicionamento %}
{% if tem_posicionamento %}
#### Posicionamento organizacional da área de TIC

O posicionamento organizacional da área de TIC deve ser compatível com suas responsabilidades institucionais e com a dependência da organização em relação à tecnologia da informação. Não se trata de impor modelo único de estrutura, mas de assegurar que a função de TIC tenha capacidade de interação adequada com as instâncias decisórias responsáveis por estratégia, orçamento, contratações, riscos e prestação de serviços.

O COBIT 2019, no objetivo APO01.06, orienta o aprimoramento do posicionamento da função de TI para que a tecnologia seja tratada de modo compatível com sua relevância estratégica e com a necessidade de interação com a alta administração. A ABNT NBR ISO/IEC 38500:2025 reforça a necessidade de estrutura adequada de tomada de decisão para o uso atual e futuro da tecnologia. Como referência complementar de boa prática, o art. 4º, § 1º, da Portaria SGD/ME nº 778/2019 estabelece que a área de TIC deve, preferencialmente, estar vinculada à alta administração, com o intuito de apoiá-la na tomada de decisões e no alcance dos objetivos estratégicos.

Um posicionamento organizacional incompatível com a relevância e as responsabilidades da TIC acarreta o risco de baixa capacidade de influência institucional. Essa fragilidade compromete a participação da área em decisões estratégicas, orçamentárias, contratuais e de gestão de riscos, além de dificultar a priorização de iniciativas e a articulação com as áreas de negócio.

No âmbito da fiscalização, o posicionamento adequado deve ser demonstrado por organograma institucional, regimento interno ou documento equivalente, de modo que seja possível verificar a vinculação da área de TIC e sua compatibilidade com as responsabilidades que lhe foram atribuídas.

Da análise das respostas aos itens 0101 e 0102 e da documentação apresentada, o posicionamento organizacional da área de TIC não se mostrou suficientemente compatível com a relevância e as responsabilidades da função de tecnologia da informação, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = motivos_posicionamento -%}
{% if motivos %}

{% for motivo in motivos -%}
{% set refs_motivo = motivo.get('refs', []) -%}
* {{ motivo.texto.rstrip('.;') }}{% if refs_motivo %} ({{ refs_motivo | join(', ') }}){% endif %}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

Diante disso, __será proposta recomendação para que a organização avalie e ajuste o posicionamento organizacional da área de TIC, de modo a assegurar interlocução adequada com a alta administração e a participação da função de TIC nas decisões estratégicas, orçamentárias, contratuais e de gestão de riscos.__

{% endif %}

#### Conclusão

As fragilidades identificadas na estrutura de TIC reduzem a segurança de que a organização disponha de condições institucionais suficientes para coordenar, gerir e sustentar a tecnologia da informação de forma alinhada às necessidades institucionais.

Diante do cenário efetivamente identificado, formula-se proposta de encaminhamento com vistas a recomendar à organização que promova a adequação de sua estrutura de TIC, alinhando-a aos critérios de governança e gestão aplicáveis previstos no COBIT 2019 e na ABNT NBR ISO/IEC 38500:2025{% if tem_posicionamento %}, bem como à diretriz de posicionamento organizacional constante do art. 4º, § 1º, da Portaria SGD/ME nº 778/2019{% endif %}.

### Propostas de Encaminhamento
{% for e in achado.encaminhamentos %}
* **Comunicação com {{ e.tipo }}** para que {{ e.encaminhamento }};
{% endfor %}

{## Final do Achado - Estrutura de TIC ##}
{% endif %}
