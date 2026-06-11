---
title: "RELATÓRIO INDIVIDUAL PRELIMINAR"
subtitle: {{ auditado.sigla }} - {{ auditado.nome }}
lang: pt-BR
figure-caption-position: above
---

# 1. Introdução

Este relatório apresenta os resultados preliminares da organização **{{ auditado.sigla }}** relativos à Fiscalização TCE-RJ nº 18/2026, realizada pelo TCE-RJ entre fevereiro e junho de 2026 para avaliar o grau de adoção de práticas de governança e gestão de tecnologia da informação e comunicação pelas organizações jurisdicionadas.

O trabalho abrangeu órgãos e entidades de todos os poderes da Administração Pública Estadual e um conjunto de prefeituras municipais.

# 2. iGovTI 2026

A avaliação das organizações jurisdicionadas baseia-se no método de autoavaliação de controles (*Control Self-Assessment* – CSA), operacionalizado mediante questionário eletrônico. A ferramenta permitiu aos gestores declarar o nível de adoção das práticas de tecnologia da informação avaliadas e encaminhar a documentação probatória correspondente. As evidências anexadas e as justificativas apresentadas foram submetidas à análise de consistência por esta Equipe de Auditoria, servindo de subsídio para eventuais ajustes na pontuação declarada e para a identificação de inconformidades ou achados de auditoria.

O questionário do iGovTI 2026 foi estruturado com o objetivo de diagnosticar aspectos essenciais de governança e gestão de TIC, abrangendo segurança da informação, gestão de riscos, continuidade de negócios, serviços de tecnologia, contratações de TIC, estrutura e força de trabalho, desenvolvimento de soluções, gestão de projetos e temas emergentes, a exemplo do uso de inteligência artificial. Para além do diagnóstico situacional de cada organização, o instrumento serve como referencial metodológico para futuras ações de melhoria de gestão.

O iGovTI 2026 constitui um índice sintético composto, mensurado em uma escala de 0 a 1. A quantificação do índice inicia-se com a conversão das respostas categóricas declaradas em coeficientes numéricos, conforme os critérios de valoração estabelecidos na [@tbl:conversao_categorias].

: Critérios de valoração das respostas qualitativas do questionário iGovTI 2026 {#tbl:conversao_categorias#}

| Categoria de Resposta Declarada | Coeficiente Numérico |
|:--------------------------------------------------|:--------------------:|
| Não adota | 0,00 |
| Há decisão formal ou plano aprovado para adotá-lo | 0,05 |
| Adota em menor parte | 0,15 |
| Adota parcialmente | 0,50 |
| Adota em maior parte ou totalmente | 1,00 |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

Nas questões que admitem itens de detalhamento (requisitos específicos), a pontuação da questão principal sofre deduções proporcionais à quantidade de itens não atendidos pela organização. Subsequentemente, os valores são consolidados por meio de agregação ponderada em uma estrutura hierárquica. O índice final é composto por dois blocos principais, conforme detalhado na [@fig:composicao_igovti_2026]:
1. **Governança de TIC (peso de 47,8%)**: formado por 4 questões de agregação direta;
2. **Gestão de TIC (iGestTI) (peso de 52,2%)**: estruturado em 6 dimensões operacionais que consolidam 20 questões principais ponderadas.

![Composição do iGovTI 2026](igovti_2026_composicao_infografico_v6.png){#fig:composicao_igovti_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

Com base na pontuação consolidada do iGovTI 2026, a organização é classificada em um de quatro níveis de maturidade, cujos intervalos de pontuação estão definidos na [@tbl:faixas_maturidade] e representados graficamente na parte inferior da [@fig:composicao_igovti_2026].

: Intervalos de pontuação para enquadramento nos níveis de maturidade {#tbl:faixas_maturidade#}

| Nível de Maturidade | Intervalo do Índice (iGovTI) |
|:--------------------------------------------------|:--------------------:|
| **Inexpressivo** | $0,00 \le \text{iGovTI} < 0,15$ |
| **Iniciando** | $0,15 \le \text{iGovTI} < 0,40$ |
| **Intermediário** | $0,40 \le \text{iGovTI} < 0,70$ |
| **Aprimorado** | $0,70 \le \text{iGovTI} \le 1,00$ |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

## 2.1. Cenário Geral

A análise consolidada apresentada nesta seção fundamenta-se nos resultados calculados para as 114 organizações que integram o universo amostral da fiscalização. A análise visa contextualizar o resultado individual do(a) **{{ auditado.sigla }}**, identificar padrões de maturidade, assimetrias entre governança e gestão e capacidades desenvolvidas no conjunto avaliado.

A distribuição por nível de maturidade, apresentada na [@fig:distribuicao_maturidade_igovti_2026], evidencia concentração nos estágios iniciais. Das 114 organizações, 52 (45,6%) foram classificadas no nível **Inexpressivo** e 41 (36,0%) no nível **Iniciando**. Assim, 93 organizações (81,6%) obtiveram resultado inferior a 0,40. Somente 15 organizações (13,2%) alcançaram o nível **Intermediário** e seis (5,3%) o nível **Aprimorado**.

![Distribuição das organizações por nível de maturidade do iGovTI 2026](igovti_2026_distribuicao_maturidade.png){#fig:distribuicao_maturidade_igovti_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

O iGovTI apresentou média de 0,234 e mediana de 0,174. O primeiro quartil foi 0,074 e o terceiro quartil, 0,329, o que evidencia a concentração de 50% das organizações avaliadas nesse intervalo, bem como a permanência de pelo menos 75% das entidades abaixo do nível Intermediário. A divergência positiva entre a média e a mediana, combinada com o valor máximo de 0,843 e com apenas seis organizações no nível Aprimorado, caracteriza uma distribuição com assimetria à direita (positiva): um grupo reduzido de resultados elevados desloca a média para cima, sem alterar o quadro predominante de baixa maturidade. Seis organizações apresentaram valor igual a zero no índice calculado.

A distribuição contínua da [@fig:distribuicao_continua_igovti_2026] complementa a classificação por faixas e permite observar a concentração dos resultados, os limites de maturidade e a distância entre a mediana e os valores mais elevados.

![Distribuição contínua dos resultados do iGovTI 2026](igovti_2026_distribuicao_continua.png){#fig:distribuicao_continua_igovti_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

A posição específica do(a) **{{ auditado.sigla }}** nessa distribuição pode ser observada na [@fig:comparativo_distribuicao_iGovTI]. Diferenças marginais de pontuação entre organizações adjacentes no ranking devem ser interpretadas com cautela analítica, visto que o modelo matemático de composição do índice não pressupõe estimativa de erro amostral e que os resultados estão sujeitos à qualidade e à fidedignidade declaratória do jurisdicionado.

## 2.2. Cenário atual - {{ auditado.sigla }}

Apresentado o panorama geral do universo fiscalizado, esta subseção detalha o desempenho específico da organização jurisdicionada. O(A) **{{ auditado.sigla }}** obteve o **valor {{ ('%0.4f' | format(iGovTI|float)) | replace('.', ',') }} para o iGovTI 2026**, correspondente ao nível **{{ iGovTI_maturidade }}** de maturidade.

![Distribuição dos resultados do iGovTI 2026 e posição do(a) {{ auditado.sigla }}]({{ auditado.sigla }}_comparativo_distribuicao_iGovTI.png){#fig:comparativo_distribuicao_iGovTI#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

A [@fig:componentes_igovti] apresenta a composição do resultado do(a) **{{ auditado.sigla }}** entre governança e gestão de TIC.

![Resultado do(a) {{ auditado.sigla }} por componentes do iGovTI 2026]({{ auditado.sigla }}_componentes_iGovTI.png){#fig:componentes_igovti#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

: Resultado sintético do iGovTI 2026 do(a) {{ auditado.sigla }} {#tbl:resultado_sintetico_igovti#}

| Componente | Peso no iGovTI 2026 | Valor |
|:--------------------------------------------------|------------------------------:|--------------------:|
| **Governança de TIC** | 0,4777 | {{ ('%0.4f' | format(GovernancaTI|float)) | replace('.', ',') }} |
| **Gestão de TIC** | 0,5223 | {{ ('%0.4f' | format(iGestTI|float)) | replace('.', ',') }} |
| **iGovTI 2026** | 1,0000 | {{ ('%0.4f' | format(iGovTI|float)) | replace('.', ',') }} |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

### 2.2.1. Governança de TIC

A governança de TIC avalia a capacidade da alta administração de orientar, dirigir, monitorar e controlar o uso da tecnologia da informação, de modo alinhado aos objetivos institucionais, aos riscos relevantes e às necessidades das áreas finalísticas e administrativas.

No iGovTI 2026, a dimensão de governança consolida práticas relacionadas ao modelo de gestão de TIC, à atuação de comitês ou instâncias equivalentes, no monitoramento do desempenho, à participação da alta administração e ao alinhamento entre decisões de TIC, estratégia organizacional, orçamento, riscos e valor público.

O(A) **{{ auditado.sigla }}** obteve o **valor {{ ('%0.4f' | format(GovernancaTI|float)) | replace('.', ',') }} no componente Governança de TIC**.

![Resultado do componente Governança de TIC do(a) {{ auditado.sigla }}]({{ auditado.sigla }}_comparativo_distribuicao_GovernancaTI.png){#fig:comparativo_distribuicao_governancati#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

### 2.2.2. Gestão de TIC

A gestão de TIC avalia a capacidade da organização de planejar, executar, monitorar e aperfeiçoar processos, serviços, controles, recursos e contratações de tecnologia da informação, de forma compatível com suas necessidades institucionais.

No iGovTI 2026, o componente **iGestTI** consolida dimensões de planejamento de TIC, gestão de serviços, riscos e segurança da informação, estrutura de segurança da informação, processos de segurança da informação e gestão de soluções de TIC.

O(A) **{{ auditado.sigla }}** obteve o **valor {{ ('%0.4f' | format(iGestTI|float)) | replace('.', ',') }} no componente Gestão de TIC**.

![Resultado do componente Gestão de TIC do(a) {{ auditado.sigla }}]({{ auditado.sigla }}_comparativo_distribuicao_iGestTI.png){#fig:comparativo_distribuicao_igestti#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

## 2.3. Relação entre governança e gestão de TIC

Os indicadores descritivos da [@tbl:estatisticas_componentes_igovti] mostram que o componente de gestão apresentou resultados superiores aos de governança no conjunto avaliado. A média do iGestTI foi 0,258, ante 0,207 para GovernancaTI; as medianas foram, respectivamente, 0,201 e 0,148. As duas médias situaram-se no nível Iniciando, enquanto a mediana de GovernancaTI permaneceu no nível Inexpressivo e a mediana de iGestTI, no nível Iniciando.

: Estatísticas descritivas do iGovTI 2026 e de seus componentes principais {#tbl:estatisticas_componentes_igovti#}

| Indicador | Média | 1º quartil | Mediana | 3º quartil | Organizações com valor >= 0,40 | Valor {{ auditado.sigla }} |
|---|---:|---:|---:|---:|---:|---:|
| **iGovTI** | 0,234 | 0,074 | 0,174 | 0,329 | 21 (18,4%) | {{ ('%0.4f' | format((iGovTI|default(0))|float)) | replace('.', ',') }} |
| **GovernancaTI** | 0,207 | 0,029 | 0,148 | 0,261 | 22 (19,3%) | {{ ('%0.4f' | format((GovernancaTI|default(0))|float)) | replace('.', ',') }} |
| **iGestTI** | 0,258 | 0,094 | 0,201 | 0,369 | 27 (23,7%) | {{ ('%0.4f' | format((iGestTI|default(0))|float)) | replace('.', ',') }} |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

A [@fig:distribuicao_componentes_igovti_2026] permite comparar a dispersão dos três indicadores. O iGestTI superou GovernancaTI em 73 organizações (64,0%); o movimento inverso ocorreu em 35 (30,7%); e houve igualdade em seis (5,3%). O padrão indica que, para a maior parte das organizações, as capacidades operacionais de gestão se situaram em patamar superior ao dos mecanismos de direção, monitoramento e controle exercidos pela alta administração. Essa diferença, contudo, não elimina a baixa maturidade da gestão: 87 organizações (76,3%) também obtiveram iGestTI inferior a 0,40.

![Distribuição do iGovTI 2026 e dos componentes GovernancaTI e iGestTI](igovti_2026_distribuicao_componentes.png){#fig:distribuicao_componentes_igovti_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

A [@fig:governanca_vs_gestao_igovti_2026] mostra a posição simultânea das organizações nos dois componentes. Pontos abaixo da diagonal representam resultado de gestão superior ao de governança; pontos acima da diagonal representam a situação inversa.

![Relação entre os resultados de governança e gestão de TIC](igovti_2026_governanca_vs_gestao.png){#fig:governanca_vs_gestao_igovti_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

{% if (GovernancaTI|float < 0.15) and (iGestTI|float < 0.15) %}
No caso da organização **{{ auditado.sigla }}**, tanto o componente de Governança de TIC quanto o de Gestão de TIC situam-se no nível **Inexpressivo** (valores abaixo de 0,1500). Esse cenário revela que a organização se encontra em estágio inicial de estruturação institucional de tecnologia da informação. Diante disso, a diferença residual entre os componentes não reflete uma assimetria operacional relevante, mas sim a necessidade urgente de implantação simultânea de mecanismos fundamentais de governança (direção e controle) e processos operacionais de gestão.
{% elif GovernancaTI|float < iGestTI|float %}
No caso da organização **{{ auditado.sigla }}**, o componente GovernancaTI ficou abaixo do iGestTI. Esse perfil indica que o principal desequilíbrio relativo se encontra nos mecanismos pelos quais a alta administração direciona, monitora e avalia a TIC, devendo a leitura ser aprofundada à luz das evidências e dos achados relacionados à governança.
{% elif GovernancaTI|float > iGestTI|float %}
No caso da organização **{{ auditado.sigla }}**, o componente iGestTI ficou abaixo de GovernancaTI. Esse perfil indica que as principais oportunidades relativas se concentram na transformação das diretrizes de governança em processos, controles e capacidades operacionais de gestão, devendo a leitura ser aprofundada à luz das evidências e dos achados correspondentes.
{% else %}
No caso da organização **{{ auditado.sigla }}**, GovernancaTI e iGestTI apresentaram o mesmo valor. A igualdade dos componentes não implica equilíbrio em nível adequado, razão pela qual a análise deve considerar o nível de maturidade alcançado e as fragilidades específicas evidenciadas em cada dimensão.
{% endif %}

## 2.4. Dimensões da gestão de TIC

A decomposição do iGestTI revela diferenças relevantes entre as seis dimensões avaliadas. Conforme a [@tbl:estatisticas_dimensoes_gestao], PlanejamentoTI apresentou a maior média (0,380) e a maior mediana (0,326). Foi também a dimensão de maior resultado em 60 organizações (52,6%), considerados os empates. Esse padrão indica que processos e instrumentos de planejamento estão mais disseminados do que as capacidades operacionais, de segurança e de gestão de soluções.

: Estatísticas descritivas das dimensões do iGestTI {#tbl:estatisticas_dimensoes_gestao#}

| Dimensão | Média | Mediana | Resultados iguais a zero | Organizações com valor inferior a 0,40 | Valor {{ auditado.sigla }} |
|---|---:|---:|---:|---:|---:|
| **PlanejamentoTI** | 0,380 | 0,326 | 16 (14,0%) | 65 (57,0%) | {{ ('%0.4f' | format((PlanejamentoTI|default(0))|float)) | replace('.', ',') }} |
| **ServicosTI** | 0,233 | 0,147 | 18 (15,8%) | 87 (76,3%) | {{ ('%0.4f' | format((ServicosTI|default(0))|float)) | replace('.', ',') }} |
| **RiscosTISegInfo** | 0,188 | 0,101 | 31 (27,2%) | 95 (83,3%) | {{ ('%0.4f' | format((RiscosTISegInfo|default(0))|float)) | replace('.', ',') }} |
| **EstruturaSegInfo** | 0,274 | 0,140 | 26 (22,8%) | 79 (69,3%) | {{ ('%0.4f' | format((EstruturaSegInfo|default(0))|float)) | replace('.', ',') }} |
| **ProcessoSegInfo** | 0,270 | 0,208 | 12 (10,5%) | 87 (76,3%) | {{ ('%0.4f' | format((ProcessoSegInfo|default(0))|float)) | replace('.', ',') }} |
| **GerirSoluçõesTI** | 0,210 | 0,150 | 28 (24,6%) | 95 (83,3%) | {{ ('%0.4f' | format((GerirSoluçõesTI|default(0))|float)) | replace('.', ',') }} |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

A distribuição completa das seis dimensões é apresentada na [@fig:distribuicao_dimensoes_gestao_2026], incluindo medianas, intervalos interquartis e médias.

![Distribuição dos resultados das seis dimensões que compõem o iGestTI](igovti_2026_distribuicao_dimensoes_gestao.png){#fig:distribuicao_dimensoes_gestao_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

A [@fig:maturidade_dimensoes_igovti_2026] explicita a composição de cada dimensão por nível de maturidade e permite verificar em quais capacidades se concentram as organizações nos estágios iniciais.

![Composição dos níveis de maturidade nas dimensões do iGestTI](igovti_2026_maturidade_dimensoes.png){#fig:maturidade_dimensoes_igovti_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

As maiores fragilidades agregadas concentram-se em **RiscosTISegInfo** e **GerirSoluçõesTI**. As duas dimensões apresentaram as menores médias e registraram valores inferiores a 0,40 em 95 organizações (83,3%). RiscosTISegInfo apareceu entre as dimensões de menor resultado de 50 organizações (43,9%), enquanto GerirSoluçõesTI ocupou essa posição em 44 (38,6%), considerados os empates. O quadro indica que a formalização do planejamento, quando existente, frequentemente não é acompanhada, na mesma intensidade, por gestão de riscos, continuidade, desenvolvimento de software e gestão de projetos.

EstruturaSegInfo apresentou média de 0,274 e mediana de apenas 0,140. Essa diferença, associada à ampla dispersão observada na [@fig:distribuicao_dimensoes_gestao_2026], evidencia heterogeneidade: um grupo de organizações possui estruturas de segurança mais consolidadas, enquanto parcela expressiva permanece próxima dos níveis inferiores. ProcessoSegInfo mostrou mediana superior à de EstruturaSegInfo, mas 76,3% das organizações ainda permaneceram abaixo de 0,40, o que recomenda examinar separadamente a existência da estrutura formal e a execução contínua dos processos de segurança.

## 2.5. Leitura integrada do resultado individual

A [@fig:perfil_dimensoes_gestao_auditado] apresenta o perfil do(a) **{{ auditado.sigla }}** nas seis dimensões de gestão e o compara com as medianas observadas nas 114 organizações. A comparação linear da [@fig:comparacao_dimensoes_gestao_auditado] permite identificar com maior precisão a distância entre o resultado individual e a mediana geral em cada dimensão.

![Perfil do(a) {{ auditado.sigla }} nas dimensões do iGestTI em comparação com as medianas gerais]({{ auditado.sigla }}_perfil_dimensoes_iGestTI.png){#fig:perfil_dimensoes_gestao_auditado#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

![Comparação do resultado individual e da mediana nas dimensões do iGestTI]({{ auditado.sigla }}_comparacao_dimensoes_iGestTI.png){#fig:comparacao_dimensoes_gestao_auditado#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

{% if PlanejamentoTI|float < iGestTI|float %}
Chama a atenção o fato de o resultado em PlanejamentoTI ({{ ('%0.4f' | format(PlanejamentoTI|float))|replace('.', ',') }}) situar-se abaixo da média das dimensões operacionais de gestão. Esse cenário atípico sugere que os poucos processos operacionais eventualmente adotados pela organização ocorrem de forma descentralizada ou sem a coordenação de diretrizes estratégicas formais, evidenciando a necessidade de priorização da dimensão de Planejamento de TIC.
{% endif %}

A [@fig:percentis_indicadores_auditado] informa a posição relativa do auditado no conjunto avaliado. O percentil não representa nível de maturidade nem grau de atendimento a critério; indica apenas a proporção de organizações com resultado igual ou inferior ao do(a) **{{ auditado.sigla }}**.

![Posição percentílica do(a) {{ auditado.sigla }} nos indicadores avaliados]({{ auditado.sigla }}_percentis_indicadores.png){#fig:percentis_indicadores_auditado#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

A [@fig:diagnostico_questoes_auditoria_auditado] sintetiza a proporção de ações de verificação atômicas conformes em cada questão de auditoria. Essa medida tem finalidade diagnóstica, deriva das regras do mapa de verificação e não integra o cálculo do iGovTI. A [@fig:praticas_criticas_auditado] detalha as práticas inconformes que sustentam esse diagnóstico e deve ser interpretada em conjunto com os achados da Seção 3.

![Diagnóstico das questões de auditoria do(a) {{ auditado.sigla }}]({{ auditado.sigla }}_diagnostico_questoes_auditoria.png){#fig:diagnostico_questoes_auditoria_auditado#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

![Práticas críticas identificadas nas respostas do(a) {{ auditado.sigla }}]({{ auditado.sigla }}_praticas_criticas.png){#fig:praticas_criticas_auditado#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

A composição declarada da força de trabalho de TIC e de segurança da informação é apresentada na [@fig:forca_trabalho_auditado]. Os quantitativos não compõem o índice e não medem, isoladamente, suficiência de pessoal; sua avaliação depende do porte, da complexidade, da terceirização, dos serviços mantidos e dos riscos da organização.

![Composição declarada da força de trabalho de TIC e segurança da informação]({{ auditado.sigla }}_forca_trabalho_tic_si.png){#fig:forca_trabalho_auditado#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

A [@fig:evolucao_individual_igovti_comparavel] apresenta a evolução do auditado quando existe correspondência válida na base harmonizada de 2023 e 2026. Na ausência de par comparável, a própria figura registra a indisponibilidade, sem inferir evolução a partir de índices calculados por metodologias distintas. As justificativas metodológicas e as limitações para a comparação direta entre os resultados de 2023 e 2026 estão detalhadas no Apêndice A.

![Evolução comparável do(a) {{ auditado.sigla }} entre 2023 e 2026]({{ auditado.sigla }}_evolucao_igovti_2023_2026.png){#fig:evolucao_individual_igovti_comparavel#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

A priorização de melhorias não deve buscar apenas a elevação numérica do índice. Recomenda-se concentrar esforços nas capacidades com menor resultado que, simultaneamente, estejam associadas a riscos relevantes, serviços críticos, obrigações normativas e necessidades institucionais do(a) **{{ auditado.sigla }}**.

## 2.6. Questões avaliadas no relatório individual

Para o iGovTI 2026, a Equipe definiu questões de auditoria voltadas à avaliação da governança e da gestão de TIC. Para fins deste relatório individual preliminar, os possíveis achados decorrem das Questões 1 a 6, que tratam de temas passíveis de responsabilização institucional específica por organização.

: Questões de auditoria com avaliação individual preliminar {#tbl:questoes_avaliadas_individualmente#}

| Questão | Tema | Síntese do objeto avaliado |
|---|---|---|
| **Q1** | Estrutura de TIC | Existência formal, atribuições e posicionamento organizacional da área, unidade, setor ou função responsável pela TIC. |
| **Q2** | Governança e comitê de TIC | Modelo de governança e gestão de TIC, objetivos, indicadores, metas e atuação do comitê ou instância equivalente. |
| **Q3** | Planejamento de TIC | Processo de planejamento, plano de TIC vigente, aprovação, alinhamento institucional, integração orçamentária e acompanhamento. |
| **Q4** | Capacidade institucional de TIC e segurança da informação | Força de trabalho, perfis, competências, funções, vínculos e capacidade interna para sustentar a TIC e a segurança da informação. |
| **Q5** | Gestão de serviços de TIC | Catálogo de serviços, níveis mínimos de serviço, inventário de ativos, gestão de configuração e tratamento de incidentes. |
| **Q6** | Contratações de TIC | Fluxo de contratação, papéis, modelos orientativos, aprovação técnica, alinhamento ao planejamento e equipe de planejamento. |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

\newpage

{% if auditado.tem_achados %}

\newpage

# 3. Resultados da Auditoria

Os achados de auditoria apresentados a seguir decorrem da avaliação preliminar das respostas do(a) **{{ auditado.sigla }}** ao questionário iGovTI 2026, das evidências encaminhadas e das situações encontradas definidas pela Equipe.

Cada achado apresenta os critérios aplicáveis, as evidências consideradas, a situação encontrada no auditado, a conclusão da Equipe de Auditoria e as propostas de encaminhamento.

{% include 'achado_questao_1_estrutura_tic.md' %}

{% include 'achado_questao_2_governanca_comite_tic.md' %}

{% include 'achado_questao_3_planejamento_tic.md' %}

{% include 'achado_questao_4_capacidade_institucional_tic_si.md' %}

{% include 'achado_questao_5_gestao_servicos_tic.md' %}

{% include 'achado_questao_6_contratacoes_tic.md' %}

\newpage

# 4. Plano de ação

Para facilitar o atendimento das propostas constantes da Seção 3, a Equipe de Auditoria elaborou modelo de plano de ação contendo os encaminhamentos preliminarmente propostos à  organização.

Cumpre alertar que, em conformidade com o art. 4º, incisos I e II, da Deliberação TCE-RJ nº 346/2024, cabe à unidade jurisdicionada avaliar a conveniência e a oportunidade de implementar as recomendações. Ressalta-se, contudo, que a eventual decisão pela não aderência deve ser motivada: o gestor deverá demonstrar formalmente, sob pena de responsabilização, que o não atendimento constitui a medida mais adequada às circunstâncias do caso concreto, em seu julgamento, bem como apresentar as medidas alternativas adotadas para sanar a situação que ensejou a recomendação.

: Plano de ação contendo os encaminhamentos preliminarmente propostos {#tbl:plano_acao#}

| Achado | Ação | Avaliação de Viabilidade | Quem? | Quando? |
|---|---|---|---|---|
{%- for item in auditado.get_plano_acao() %}
| **{{ item.achado_num }}** | {{ item.encaminhamento }} | | | |{% endfor %}

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

{% else %}

\newpage

# 3. Resultados da Auditoria

Com base na avaliação preliminar das respostas e das evidências do(a) **{{ auditado.sigla }}**, não foram identificadas situações que ensejassem achado individual nas Questões 1 a 6.

{% endif %}

\newpage

# Apêndice A. Comparabilidade com o ciclo anterior (iGovTI 2023 vs. iGovTI 2026)

A estrutura de 2026 preservou a escala de 0 a 1, as categorias de resposta e as quatro faixas de maturidade empregadas em 2023, mas alterou de forma relevante a composição dos agregados e seus pesos. As principais diferenças estão sintetizadas na [@tbl:diferencas_igovti_2023_2026].

: Principais diferenças entre as estruturas do iGovTI 2023 e do iGovTI 2026 {#tbl:diferencas_igovti_2023_2026#}

| Aspecto | iGovTI 2023 | iGovTI 2026 | Implicação analítica |
|---|---|---|---|
| **Composição do índice final** | GovernancaTI e iGestTI com pesos iguais de 0,50. | GovernancaTI com peso 0,4777 e iGestTI com peso 0,5223. | A gestão passou a ter participação ligeiramente superior no índice final. |
| **Governança de TIC** | Agregação hierárquica de ModeloTI, MonitorAvaliaTI e ResultadoTI. | Agregação direta de quatro práticas relativas ao modelo de gestão, monitoramento, auditoria interna e simplificação de serviços públicos. | O componente tornou-se mais direto e incorporou práticas com escopo distinto da estrutura anterior. |
| **Gestão de TIC** | Agregação de PlanejamentoTI, PessoasTI e ProcessosTI; este último reunia serviços, níveis de serviço, riscos, segurança, software, projetos e contratos. | Agregação direta de PlanejamentoTI, ServicosTI, RiscosTISegInfo, EstruturaSegInfo, ProcessoSegInfo e GerirSoluçõesTI. | O índice passou a evidenciar separadamente seis capacidades operacionais e de segurança. |
| **Pessoas e contratações** | PessoasTI e iGestContratosTI integravam o cálculo do iGestTI. | Não integram a árvore de cálculo do iGovTI 2026, embora continuem relevantes para o diagnóstico e para a auditoria. | Mudanças nessas matérias não explicam diretamente a variação do índice de 2026. |
| **Serviços, software e projetos** | Serviços e níveis de serviço eram agregados distintos; software e projetos integravam ProcessosTI. | Serviços foram consolidados em ServicosTI; software e projetos foram reunidos em GerirSoluçõesTI. | A leitura deve considerar a nova delimitação conceitual dos componentes. |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

Em razão dessas alterações, a diferença entre os valores nominais de 2023 e 2026 não deve ser interpretada automaticamente como evolução ou retrocesso institucional. Uma análise temporal válida exige a harmonização das questões e dos agregados comparáveis, além da consideração de mudanças de escopo, pesos, respondentes e qualidade das evidências.

{% if teve_ajuste %}

\newpage

# Apêndice B. Ajustes nas respostas declaradas

A Equipe de Auditoria, em busca da melhor representação do cenário atual de governança e gestão de TIC da organização, ajustou resposta(s) declarada(s) pelo(a) **{{ auditado.sigla }}** ao questionário iGovTI 2026.

Para tanto, foram utilizadas as justificativas e evidências fornecidas pelo jurisdicionado quando do envio das respostas ao questionário. Ressalta-se que a verificação dessa documentação foi realizada nos termos dos procedimentos definidos para a fiscalização, de modo que nem todas as evidências encaminhadas foram, necessariamente, objeto de análise exaustiva pela Equipe de Auditoria.

Seguem as alterações realizadas após a avaliação das respostas e da amostra de evidências, bem como as justificativas apresentadas pela Equipe:

: Relação de respostas ajustadas pela Equipe após validação {#tbl:ajuste_respostas#}

| Questão | Resposta original | Resposta ajustada | Justificativa |
|---|---|---|---|
{%- for ajuste in ajustes_respostas %}
| **{{ ajuste.codigo_questao }}** | {{ ajuste.de }} | {{ ajuste.para }} | {{ ajuste.justificativa }} |{% endfor %}

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

{% endif %}
