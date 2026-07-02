{% set nome_achado = 'Estrutura de TIC insuficiente para coordenar, gerir e sustentar a tecnologia da informação.' %}
{% set achado = auditado.get_achado_por_nome(nome_achado) %}
{% if achado %}

\newpage

## Achado {{ achado.numero }} – {{ achado.nome }}

### Critérios
* COBIT 2019, APO01.04 - Definir e implementar as estruturas organizacionais: estabelecer estruturas organizacionais internas e externas necessárias para apoiar os objetivos de governança e gestão de TI;
* COBIT 2019, APO01.05 - Estabelecer papéis e responsabilidades: definir, comunicar e manter papéis e responsabilidades relacionados à governança e gestão de TI;
* COBIT 2019, APO01.06 - Aprimorar o posicionamento da função de TI: posicionar a função de tecnologia de modo compatível com sua relevância estratégica, responsabilidades e necessidade de interação com a alta administração;
* COBIT 2019, APO01.09 - Definição e comunicação de políticas e procedimentos: estabelecer e comunicar políticas e procedimentos de gestão de TI que orientem papéis, responsabilidades e controles;
* ABNT NBR ISO/IEC 38500:2025, item 5.6.1 - Governança efetiva de TI: responsabilização clara, estrutura adequada de tomada de decisão e direção organizacional compatível com o uso atual e futuro da tecnologia;
* Portaria SGD/ME nº 778/2019, art. 4º, § 1º - Como referência de boa prática, a área de TIC deve, preferencialmente, estar vinculada à alta administração para apoiá-la na tomada de decisões e no alcance dos objetivos estratégicos.

### Evidências
{% for evidencia in achado.evidencias %}
* {{ evidencia }};
{% endfor %}

### Situação encontrada

A existência de estrutura formal de TIC é requisito básico para que a organização disponha de unidade, setor ou função institucionalmente reconhecida para planejar, coordenar, gerir, executar, monitorar e controlar o uso da tecnologia da informação. Sob a perspectiva de governança de TIC, essa estruturação envolve três dimensões complementares: formalização da área ou função de TIC, definição de atribuições e competências essenciais e posicionamento organizacional adequado para participar das decisões estratégicas, orçamentárias, contratuais e de gestão de riscos.

Os critérios de boas práticas indicam que a organização deve estabelecer estruturas organizacionais apropriadas, comunicar papéis e responsabilidades de maneira clara, definir políticas e procedimentos de gestão de TIC e posicionar a função de tecnologia de modo compatível com sua relevância estratégica[^explica_estrutura_tic_cobit]. Esses requisitos convergem com as diretrizes da ABNT NBR ISO/IEC 38500:2025, que orienta sobre a necessidade de responsabilização clara e de estruturas adequadas de tomada de decisão para a governança efetiva de TI[^explica_estrutura_tic_iso38500], e com a referência de vinculação preferencial da área de TIC à alta administração prevista no art. 4º, § 1º, da Portaria SGD/ME nº 778/2019.

Com base na análise das respostas aos itens 0101, 0102 e 0103 do questionário aplicado e da avaliação das evidências documentais anexadas, constatou-se que a organização não atende integralmente a esses requisitos de governança. A Equipe de Auditoria identificou as seguintes deficiências na estrutura de TIC da organização:

{% set situacao_formalizacao = 'Ausência de área, unidade, setor ou função de TIC formalmente instituída.' %}
{% set situacao_atribuicoes = 'Área de TIC sem atribuições formais suficientes para planejamento, coordenação, gestão, execução, monitoramento e controle da TIC.' %}
{% set situacao_posicionamento = 'Posicionamento organizacional inadequado da área de TIC.' %}

{% if situacao_formalizacao in achado.situacoes_encontradas %}
* **Formalização da área de TIC**: a deficiência de formalização não demonstra aderência aos critérios de definição de estruturas organizacionais e de comunicação de políticas e procedimentos (COBIT 2019, APO01.04/APO01.09 e ABNT NBR ISO/IEC 38500:2025, item 5.6.1), o que pode prejudicar a responsabilização e o alinhamento da TIC aos objetivos institucionais.
{% endif %}
{% if situacao_atribuicoes in achado.situacoes_encontradas %}
* **Atribuições da área de TIC**: a insuficiência de atribuições formais não demonstra aderência aos critérios de definição de papéis e responsabilidades e de comunicação de políticas e procedimentos (COBIT 2019, APO01.05/APO01.09 e ABNT NBR ISO/IEC 38500:2025, item 5.6.1), o que pode favorecer atuação reativa e fragmentada por falta de clareza sobre responsabilidades de planejamento, coordenação, gestão, execução, monitoramento e controle da TIC.
{% endif %}
{% if situacao_posicionamento in achado.situacoes_encontradas %}
* **Posicionamento organizacional**: o posicionamento inadequado não demonstra aderência ao critério de aprimoramento do posicionamento da função de TI (COBIT 2019, APO01.06 e ABNT NBR ISO/IEC 38500:2025, item 5.6.1) e diverge da referência da Portaria SGD/ME nº 778/2019 (art. 4º, § 1º), o que pode reduzir a capacidade de influência institucional da TIC e comprometer sua participação em decisões estratégicas, orçamentárias, contratuais e de gestão de riscos.
{% endif %}

Essas situações ensejaram o presente achado e serão detalhadas nas seções subsequentes.

[^explica_estrutura_tic_cobit]: No domínio APO01 do COBIT 2019, a gestão da estrutura organizacional, de papéis, responsabilidades, políticas e posicionamento da função de TI é tratada como condição para que a tecnologia apoie os objetivos de governança e gestão da organização.

[^explica_estrutura_tic_iso38500]: A ABNT NBR ISO/IEC 38500:2025 orienta que a governança efetiva de TI pressupõe responsabilidades claras, estrutura adequada de decisão e direção organizacional compatível com o uso atual e futuro da tecnologia.

{% set situacao = 'Ausência de área, unidade, setor ou função de TIC formalmente instituída.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Formalização da área, unidade, setor ou função de TIC

A formalização da área, unidade, setor ou função de TIC é necessária para conferir reconhecimento institucional à atividade de tecnologia da informação, definir sua vinculação na estrutura organizacional e permitir a atribuição clara de responsabilidades.

O COBIT 2019, no objetivo APO01.04, orienta que a organização defina e implemente estruturas organizacionais necessárias para apoiar os objetivos de governança e gestão de TI. De forma complementar, o APO01.09 trata da definição e comunicação de políticas e procedimentos que orientem papéis, responsabilidades e controles.

No contexto da fiscalização, essa formalização deve ser demonstrada por regimento, decreto, portaria, resolução, organograma, ato administrativo ou instrumento equivalente. A ausência de evidência suficiente de formalização fragiliza a identificação da unidade responsável pela coordenação da TIC e compromete a responsabilização por decisões, controles, serviços e investimentos de tecnologia.

Essa deficiência materializa o risco de inexistência de unidade ou função institucionalmente reconhecida para coordenar o uso da tecnologia da informação, prejudicando o alinhamento da TIC aos objetivos da organização.

Diante disso, __será proposta recomendação para que a organização formalize a área, unidade, setor ou função de TIC em regimento, decreto, portaria, resolução, organograma ou instrumento equivalente, compatível com seu porte, complexidade e dependência tecnológica.__

{% endif %}

{% set situacao = 'Área de TIC sem atribuições formais suficientes para planejamento, coordenação, gestão, execução, monitoramento e controle da TIC.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Atribuições formais da área de TIC

A definição formal de atribuições da área de TIC é indispensável para delimitar responsabilidades, reduzir sobreposição ou lacunas de atuação e permitir que a gestão de tecnologia seja exercida de forma planejada e controlada.

O COBIT 2019, no objetivo APO01.05, orienta a definição, comunicação e manutenção de papéis e responsabilidades relacionados à governança e gestão de TI. Essa orientação abrange atribuições essenciais como governança, planejamento, gestão, sustentação tecnológica, sistemas, segurança da informação, contratos, dados e atividades correlatas.

A ausência de atribuições formalmente definidas ou a especificação de competências insuficientes para planejamento, coordenação, gestão, execução, monitoramento e controle da TIC expõe a organização a uma atuação reativa e fragmentada, com baixa clareza sobre os responsáveis por processos, serviços, riscos, contratações e controles de tecnologia.

Essa deficiência compromete a capacidade de gestão da TIC e reduz a efetividade dos demais processos de governança e gestão, uma vez que a estrutura organizacional não explicita quem deve decidir, executar, acompanhar e responder pelos resultados de tecnologia da informação.

Diante disso, __será proposta recomendação para que a organização defina formalmente as atribuições da área de TIC, contemplando planejamento, coordenação, gestão, execução, monitoramento e controle da TIC.__

{% endif %}

{% set situacao = 'Posicionamento organizacional inadequado da área de TIC.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Posicionamento organizacional da área de TIC

O posicionamento organizacional da área de TIC deve ser compatível com suas responsabilidades institucionais e com a dependência da organização em relação à tecnologia da informação. Não se trata de impor modelo único de estrutura, mas de assegurar que a função de TIC tenha capacidade de interação adequada com as instâncias decisórias responsáveis por estratégia, orçamento, contratações, riscos e prestação de serviços.

O COBIT 2019, no objetivo APO01.06, orienta o aprimoramento do posicionamento da função de TI para que a tecnologia seja tratada de modo compatível com sua relevância estratégica e com a necessidade de interação com a alta administração. A ABNT NBR ISO/IEC 38500:2025 reforça a necessidade de estrutura adequada de tomada de decisão para o uso atual e futuro da tecnologia. Como referência complementar de boa prática, o art. 4º, § 1º, da Portaria SGD/ME nº 778/2019 estabelece que a área de TIC deve, preferencialmente, estar vinculada à alta administração, com o intuito de apoiá-la na tomada de decisões e no alcance dos objetivos estratégicos.

Um posicionamento organizacional incompatível com a relevância e as responsabilidades da TIC acarreta o risco de baixa capacidade de influência institucional. Essa fragilidade compromete a participação da área em decisões estratégicas, orçamentárias, contratuais e de gestão de riscos, além de dificultar a priorização de iniciativas e a articulação com as áreas de negócio.

No âmbito da fiscalização, o posicionamento adequado deve ser demonstrado por organograma institucional, regimento interno ou documento equivalente, de modo que seja possível verificar a vinculação da área de TIC e sua compatibilidade com as responsabilidades que lhe foram atribuídas.

Diante disso, __será proposta recomendação para que a organização avalie e ajuste o posicionamento organizacional da área de TIC, de modo a assegurar interlocução adequada com a alta administração e a participação da função de TIC nas decisões estratégicas, orçamentárias, contratuais e de gestão de riscos.__

{% endif %}

#### Conclusão

As fragilidades identificadas na estrutura de TIC comprometem a capacidade da organização de coordenar, gerir e sustentar a tecnologia da informação de forma alinhada às necessidades institucionais. A ausência de formalização, a insuficiência de atribuições formais e o posicionamento organizacional inadequado reduzem a clareza de responsabilidades, dificultam a tomada de decisão e fragilizam o acompanhamento de riscos, serviços, contratações e iniciativas de TIC.

Diante do cenário exposto, formula-se proposta de encaminhamento com vistas a recomendar à organização que promova a adequação de sua estrutura de TIC, alinhando-a aos critérios de governança e gestão previstos no COBIT 2019 e na ABNT NBR ISO/IEC 38500:2025, bem como à diretriz de posicionamento organizacional constante do art. 4º, § 1º, da Portaria SGD/ME nº 778/2019.

### Propostas de Encaminhamento
{% for e in achado.encaminhamentos %}
* **Comunicação com {{ e.tipo }}** para que {{ e.encaminhamento }};
{% endfor %}

{## Final do Achado - Estrutura de TIC ##}
{% endif %}
