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

O método utilizado para avaliar as organizações foi o de autoavaliação de controles, conhecido como *Control Self-Assessment* (CSA). Por meio desse método, foi disponibilizado questionário eletrônico para que os gestores informassem a situação da organização em relação às práticas avaliadas e encaminhassem evidências destinadas a corroborar as respostas prestadas. As evidências anexadas e as justificativas textuais foram utilizadas pela Equipe de Auditoria para avaliar a consistência das respostas declaradas, apoiar eventuais ajustes e subsidiar a identificação de achados de auditoria.

O questionário do iGovTI 2026 foi estruturado para coletar informações sobre governança de TIC, gestão de TIC, segurança da informação, riscos, continuidade, serviços, contratações, estrutura organizacional, força de trabalho, soluções de TIC, projetos e temas emergentes, como inteligência artificial. Além de permitir o diagnóstico individual das organizações, as questões também devem servir como referência para a condução de futuras iniciativas de aprimoramento da governança e da gestão de TIC.

O iGovTI 2026 é um índice composto que consolida resultados de governança e gestão de TIC em escala de 0 a 1. As respostas categóricas ao questionário são inicialmente convertidas em valores numéricos: **Não adota** = 0; **Há decisão formal ou plano aprovado para adotá-lo** = 0,05; **Adota em menor parte** = 0,15; **Adota parcialmente** = 0,50; e **Adota em maior parte ou totalmente** = 1,00.

Quando a questão possui itens de detalhamento, a pontuação da resposta principal pode ser reduzida conforme os itens efetivamente atendidos. Na sequência, os valores são combinados por somas ponderadas em uma árvore de agregação. O componente **GovernancaTI** resulta de quatro práticas diretamente ponderadas; o **iGestTI** reúne seis dimensões: PlanejamentoTI, ServicosTI, RiscosTISegInfo, EstruturaSegInfo, ProcessoSegInfo e GerirSoluçõesTI. O índice final é calculado pela seguinte expressão:

`iGovTI = 0,477696299232863 x GovernancaTI + 0,522303700767137 x iGestTI`

Após o cálculo, a organização é classificada nos níveis de maturidade **Inexpressivo** (`0 <= iGovTI < 0,15`), **Iniciando** (`0,15 <= iGovTI < 0,40`), **Intermediário** (`0,40 <= iGovTI < 0,70`) ou **Aprimorado** (`0,70 <= iGovTI <= 1,00`).

## 2.1. Cenário Geral

A análise consolidada apresentada nesta seção utiliza os resultados calculados para as 114 organizações da fiscalização. O objetivo da análise é contextualizar o resultado individual do(a) **{{ auditado.sigla }}**, identificar padrões de maturidade, assimetrias entre governança e gestão e capacidades que se mostram mais ou menos desenvolvidas no conjunto avaliado.

A distribuição por nível de maturidade, apresentada na [@fig:distribuicao_maturidade_igovti_2026], evidencia concentração nos estágios iniciais. Das 114 organizações, 52 (45,6%) foram classificadas no nível **Inexpressivo** e 41 (36,0%) no nível **Iniciando**. Assim, 93 organizações (81,6%) obtiveram resultado inferior a 0,40. Somente 15 organizações (13,2%) alcançaram o nível **Intermediário** e seis (5,3%) o nível **Aprimorado**.

![Distribuição das organizações por nível de maturidade do iGovTI 2026](igovti_2026_distribuicao_maturidade.png){#fig:distribuicao_maturidade_igovti_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

O iGovTI apresentou média de 0,234 e mediana de 0,174. O primeiro quartil foi 0,074 e o terceiro quartil, 0,329, o que significa que metade das organizações se concentrou nesse intervalo e que pelo menos 75% permaneceram abaixo do nível Intermediário. A média superior à mediana, combinada com o valor máximo de 0,843 e com apenas seis organizações no nível Aprimorado, caracteriza uma distribuição assimétrica à direita: um grupo reduzido de resultados elevados desloca a média para cima, sem alterar o quadro predominante de baixa maturidade. Seis organizações apresentaram valor igual a zero no índice calculado.

A posição específica do(a) **{{ auditado.sigla }}** nessa distribuição pode ser observada na [@fig:comparativo_distribuicao_iGovTI]. Diferenças pequenas entre organizações próximas devem ser interpretadas com cautela, pois o índice não dispõe de margem de erro estimada e pode ser afetado pela qualidade das respostas e das evidências apresentadas.

## 2.2. Cenário atual - {{ auditado.sigla }}

Uma vez apresentada a visão geral do iGovTI 2026, passa-se ao resultado específico da organização. O(A) **{{ auditado.sigla }}** obteve o **valor {{ '%0.2f' | format(iGovTI|float) }} para o iGovTI 2026**, correspondente ao nível **{{ iGovTI_maturidade }}** de maturidade.

![Distribuição dos resultados do iGovTI 2026 e posição do(a) {{ auditado.sigla }}]({{ auditado.sigla }}_comparativo_distribuicao_iGovTI.png){#fig:comparativo_distribuicao_iGovTI#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

A [@fig:componentes_igovti] apresenta a composição do resultado do(a) **{{ auditado.sigla }}** entre governança e gestão de TIC.

![Resultado do(a) {{ auditado.sigla }} por componentes do iGovTI 2026]({{ auditado.sigla }}_componentes_iGovTI.png){#fig:componentes_igovti#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

: Resultado sintético do iGovTI 2026 do(a) {{ auditado.sigla }} {#tbl:resultado_sintetico_igovti#}

| Componente | Peso no iGovTI 2026 | Valor |
|---|---:|---:|---|
| **Governança de TIC** | 0,477696299232863 | {{ '%0.2f' | format(GovernancaTI|float) }} |
| **Gestão de TIC** | 0,522303700767137 | {{ '%0.2f' | format(iGestTI|float) }} |
| **iGovTI 2026** | 1,000000000000000 | {{ '%0.2f' | format(iGovTI|float) }} |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

### 2.2.1. Governança de TIC

A governança de TIC avalia a capacidade da alta administração de orientar, dirigir, monitorar e controlar o uso da tecnologia da informação, de modo alinhado aos objetivos institucionais, aos riscos relevantes e às necessidades das áreas finalísticas e administrativas.

No iGovTI 2026, a dimensão de governança consolida práticas relacionadas ao modelo de gestão de TIC, à atuação de comitês ou instâncias equivalentes, ao monitoramento do desempenho, à participação da alta administração e ao alinhamento entre decisões de TIC, estratégia organizacional, orçamento, riscos e valor público.

O(A) **{{ auditado.sigla }}** obteve o **valor {{ '%0.2f' | format(GovernancaTI|float) }} no componente Governança de TIC**.

![Resultado do componente Governança de TIC do(a) {{ auditado.sigla }}]({{ auditado.sigla }}_comparativo_distribuicao_GovernancaTI.png){#fig:comparativo_distribuicao_governancati#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

### 2.2.2. Gestão de TIC

A gestão de TIC avalia a capacidade da organização de planejar, executar, monitorar e aperfeiçoar processos, serviços, controles, recursos e contratações de tecnologia da informação, de forma compatível com suas necessidades institucionais.

No iGovTI 2026, o componente **iGestTI** consolida dimensões de planejamento de TIC, gestão de serviços, riscos e segurança da informação, estrutura de segurança da informação, processos de segurança da informação e gestão de soluções de TIC.

O(A) **{{ auditado.sigla }}** obteve o **valor {{ '%0.2f' | format(iGestTI|float) }} no componente Gestão de TIC**.

![Resultado do componente Gestão de TIC do(a) {{ auditado.sigla }}]({{ auditado.sigla }}_comparativo_distribuicao_iGestTI.png){#fig:comparativo_distribuicao_igestti#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

## 2.3. Relação entre governança e gestão de TIC

Os indicadores descritivos da [@tbl:estatisticas_componentes_igovti] mostram que o componente de gestão apresentou resultados superiores aos de governança no conjunto avaliado. A média do iGestTI foi 0,258, ante 0,207 para GovernancaTI; as medianas foram, respectivamente, 0,201 e 0,148. As duas médias situaram-se no nível Iniciando, enquanto a mediana de GovernancaTI permaneceu no nível Inexpressivo e a mediana de iGestTI, no nível Iniciando.

: Estatísticas descritivas do iGovTI 2026 e de seus componentes principais {#tbl:estatisticas_componentes_igovti#}

| Indicador | Média | 1º quartil | Mediana | 3º quartil | Organizações com valor >= 0,40 |
|---|---:|---:|---:|---:|---:|
| **iGovTI** | 0,234 | 0,074 | 0,174 | 0,329 | 21 (18,4%) |
| **GovernancaTI** | 0,207 | 0,029 | 0,148 | 0,261 | 22 (19,3%) |
| **iGestTI** | 0,258 | 0,094 | 0,201 | 0,369 | 27 (23,7%) |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

A [@fig:distribuicao_componentes_igovti_2026] permite comparar a dispersão dos três indicadores. O iGestTI superou GovernancaTI em 73 organizações (64,0%); o movimento inverso ocorreu em 35 (30,7%); e houve igualdade em seis (5,3%). O padrão indica que, para a maior parte das organizações, as capacidades operacionais de gestão se situaram em patamar superior ao dos mecanismos de direção, monitoramento e controle exercidos pela alta administração. Essa diferença, contudo, não elimina a baixa maturidade da gestão: 87 organizações (76,3%) também obtiveram iGestTI inferior a 0,40.

![Distribuição do iGovTI 2026 e dos componentes GovernancaTI e iGestTI](igovti_2026_distribuicao_componentes.png){#fig:distribuicao_componentes_igovti_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

{% if GovernancaTI|float < iGestTI|float %}
No caso da organização **{{ auditado.sigla }}**, o componente GovernancaTI ficou abaixo do iGestTI. Esse perfil indica que o principal desequilíbrio relativo se encontra nos mecanismos pelos quais a alta administração direciona, monitora e avalia a TIC, devendo a leitura ser aprofundada à luz das evidências e dos achados relacionados à governança.
{% elif GovernancaTI|float > iGestTI|float %}
No caso da organização **{{ auditado.sigla }}**, o componente iGestTI ficou abaixo de GovernancaTI. Esse perfil indica que as principais oportunidades relativas se concentram na transformação das diretrizes de governança em processos, controles e capacidades operacionais de gestão, devendo a leitura ser aprofundada à luz das evidências e dos achados correspondentes.
{% else %}
No caso da organização **{{ auditado.sigla }}**, GovernancaTI e iGestTI apresentaram o mesmo valor. A igualdade dos componentes não implica equilíbrio em nível adequado, razão pela qual a análise deve considerar o nível de maturidade alcançado e as fragilidades específicas evidenciadas em cada dimensão.
{% endif %}

## 2.4. Dimensões da gestão de TIC

A decomposição do iGestTI revela diferenças relevantes entre as seis dimensões avaliadas. Conforme a [@tbl:estatisticas_dimensoes_gestao], PlanejamentoTI apresentou a maior média (0,380) e a maior mediana (0,326). Foi também a dimensão de maior resultado em 60 organizações (52,6%), considerados os empates. Esse padrão indica que processos e instrumentos de planejamento estão mais disseminados do que as capacidades operacionais, de segurança e de gestão de soluções.

: Estatísticas descritivas das dimensões do iGestTI {#tbl:estatisticas_dimensoes_gestao#}

| Dimensão | Média | Mediana | Resultados iguais a zero | Organizações com valor inferior a 0,40 |
|---|---:|---:|---:|---:|
| **PlanejamentoTI** | 0,380 | 0,326 | 16 (14,0%) | 65 (57,0%) |
| **ServicosTI** | 0,233 | 0,147 | 18 (15,8%) | 87 (76,3%) |
| **RiscosTISegInfo** | 0,188 | 0,101 | 31 (27,2%) | 95 (83,3%) |
| **EstruturaSegInfo** | 0,274 | 0,140 | 26 (22,8%) | 79 (69,3%) |
| **ProcessoSegInfo** | 0,270 | 0,208 | 12 (10,5%) | 87 (76,3%) |
| **GerirSoluçõesTI** | 0,210 | 0,150 | 28 (24,6%) | 95 (83,3%) |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

A distribuição completa das seis dimensões é apresentada na [@fig:distribuicao_dimensoes_gestao_2026], incluindo medianas, intervalos interquartis e médias.

![Distribuição dos resultados das seis dimensões que compõem o iGestTI](igovti_2026_distribuicao_dimensoes_gestao.png){#fig:distribuicao_dimensoes_gestao_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

As maiores fragilidades agregadas concentram-se em **RiscosTISegInfo** e **GerirSoluçõesTI**. As duas dimensões apresentaram as menores médias e registraram valores inferiores a 0,40 em 95 organizações (83,3%). RiscosTISegInfo apareceu entre as dimensões de menor resultado de 50 organizações (43,9%), enquanto GerirSoluçõesTI ocupou essa posição em 44 (38,6%), considerados os empates. O quadro indica que a formalização do planejamento, quando existente, frequentemente não é acompanhada, na mesma intensidade, por gestão de riscos, continuidade, desenvolvimento de software e gestão de projetos.

EstruturaSegInfo apresentou média de 0,274 e mediana de apenas 0,140. Essa diferença, associada à ampla dispersão observada na [@fig:distribuicao_dimensoes_gestao_2026], evidencia heterogeneidade: um grupo de organizações possui estruturas de segurança mais consolidadas, enquanto parcela expressiva permanece próxima dos níveis inferiores. ProcessoSegInfo mostrou mediana superior à de EstruturaSegInfo, mas 76,3% das organizações ainda permaneceram abaixo de 0,40, o que recomenda examinar separadamente a existência da estrutura formal e a execução contínua dos processos de segurança.

## 2.5. Associações entre capacidades

A análise de correlação apresentada na [@fig:correlacao_dimensoes_gestao_2026] mostra que as dimensões de gestão evoluem de forma associada. A relação linear mais elevada ocorreu entre ServicosTI e GerirSoluçõesTI (`r = 0,82`), seguida por ServicosTI e ProcessoSegInfo (`r = 0,78`). Em termos descritivos, organizações com gestão de serviços mais estruturada também tendem a apresentar melhores capacidades para desenvolver e gerenciar soluções e para executar processos de segurança da informação.

![Correlação entre as dimensões que compõem o iGestTI](igovti_2026_correlacao_dimensoes_gestao.png){#fig:correlacao_dimensoes_gestao_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

Essas associações não demonstram relação de causa e efeito e são parcialmente esperadas, pois as dimensões integram um mesmo construto de maturidade de gestão. Ainda assim, o padrão recomenda uma abordagem coordenada: catálogo e níveis de serviço, ativos, mudanças, incidentes, segurança, desenvolvimento de software e projetos compartilham informações, papéis, processos e mecanismos de monitoramento. O aprimoramento sustentável do iGovTI deve ser orientado por riscos e vinculado aos objetivos institucionais.

## 2.6. Principais alterações em relação ao iGovTI 2023

A estrutura de 2026 preservou a escala de 0 a 1, as categorias de resposta e as quatro faixas de maturidade empregadas em 2023, mas alterou de forma relevante a composição dos agregados e seus pesos. As principais diferenças estão sintetizadas na [@tbl:diferencas_igovti_2023_2026].

: Principais diferenças entre as estruturas do iGovTI 2023 e do iGovTI 2026 {#tbl:diferencas_igovti_2023_2026#}

| Aspecto | iGovTI 2023 | iGovTI 2026 | Implicação analítica |
|---|---|---|---|
| **Composição do índice final** | GovernancaTI e iGestTI com pesos iguais de 0,50. | GovernancaTI com peso 0,477696 e iGestTI com peso 0,522304. | A gestão passou a ter participação ligeiramente superior no índice final. |
| **Governança de TIC** | Agregação hierárquica de ModeloTI, MonitorAvaliaTI e ResultadoTI. | Agregação direta de quatro práticas relativas ao modelo de gestão, monitoramento, auditoria interna e simplificação de serviços públicos. | O componente tornou-se mais direto e incorporou práticas com escopo distinto da estrutura anterior. |
| **Gestão de TIC** | Agregação de PlanejamentoTI, PessoasTI e ProcessosTI; este último reunia serviços, níveis de serviço, riscos, segurança, software, projetos e contratos. | Agregação direta de PlanejamentoTI, ServicosTI, RiscosTISegInfo, EstruturaSegInfo, ProcessoSegInfo e GerirSoluçõesTI. | O índice passou a evidenciar separadamente seis capacidades operacionais e de segurança. |
| **Pessoas e contratações** | PessoasTI e iGestContratosTI integravam o cálculo do iGestTI. | Não integram a árvore de cálculo do iGovTI 2026, embora continuem relevantes para o diagnóstico e para a auditoria. | Mudanças nessas matérias não explicam diretamente a variação do índice de 2026. |
| **Serviços, software e projetos** | Serviços e níveis de serviço eram agregados distintos; software e projetos integravam ProcessosTI. | Serviços foram consolidados em ServicosTI; software e projetos foram reunidos em GerirSoluçõesTI. | A leitura deve considerar a nova delimitação conceitual dos componentes. |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

Em razão dessas alterações, a diferença entre os valores nominais de 2023 e 2026 não deve ser interpretada automaticamente como evolução ou retrocesso institucional. Uma análise temporal válida exige a harmonização das questões e dos agregados comparáveis, além da consideração de mudanças de escopo, pesos, respondentes e qualidade das evidências.

## 2.7. Evolução das organizações avaliadas em 2023 e 2026

A comparação temporal foi realizada a partir das planilhas `iGovTI-2023-SETIC-Ajustado-Comparavel.xlsx`, `iGovTI-2023-Municipios-Ajustado-Comparavel.xlsx` e `iGovTI-2026-Ajustado-Comparavel.xlsx`. Essas bases recalculam os resultados de 2023 e 2026 segundo uma estrutura harmonizada, na qual GovernancaTI e iGestTI possuem pesos iguais de 0,50. Foram mantidas apenas as organizações identificadas nos dois ciclos.

Após a padronização de acentos, sinais, prefixos municipais e variações inequívocas de sigla, foram pareadas 70 organizações: 66 integrantes do conjunto estadual e quatro municípios. Não foram equiparadas unidades cuja mudança de denominação pudesse estar associada a alteração de competências ou de estrutura administrativa. No caso da CODIN, foi considerado o envio concluído em 26 de maio de 2026; o segundo registro existente na base de 2026 foi desconsiderado por se tratar de tentativa não submetida e com respostas incompletas.

A harmonização reduz parte das diferenças entre os questionários, mas não elimina todas as limitações de comparabilidade. Os resultados podem refletir mudanças efetivas nas práticas, alterações na interpretação das questões, diferenças na qualidade das respostas e evidências ou mudanças institucionais ocorridas no período. Portanto, as variações devem ser lidas como evolução ou regressão dos resultados declarados e recalculados, e não como comprovação isolada de melhoria ou deterioração da gestão.

### 2.7.1. Evolução geral do índice

Na amostra pareada, a média do iGovTI passou de 0,184, em 2023, para 0,248, em 2026, correspondendo a aumento absoluto de 0,064. A mediana passou de 0,151 para 0,199. A elevação da média foi acompanhada por aumento da dispersão: o desvio-padrão passou de 0,146 para 0,192 e o terceiro quartil, de 0,230 para 0,381. Esse resultado indica melhora do nível central, mas também maior diferenciação entre as organizações.

A [@fig:distribuicao_igovti_comparavel_2023_2026] apresenta as distribuições pareadas nos dois ciclos. Das 70 organizações, 44 (62,9%) aumentaram o iGovTI e 26 (37,1%) registraram redução. Em 32 casos (45,7%), o aumento foi igual ou superior a 0,05; em 13 (18,6%), a redução alcançou pelo menos 0,05 em valor absoluto; e 25 organizações (35,7%) permaneceram no intervalo de variação entre -0,05 e +0,05.

![Distribuição do iGovTI comparável das organizações comuns em 2023 e 2026](igovti_comparavel_distribuicao_2023_2026.png){#fig:distribuicao_igovti_comparavel_2023_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

O resultado médio de GovernancaTI aumentou de 0,155 para 0,211, enquanto o iGestTI passou de 0,213 para 0,284. Assim, o avanço médio do índice foi sustentado pelos dois componentes, com variação ligeiramente maior na gestão. Entre as 44 organizações que evoluíram, 30 apresentaram crescimento simultâneo de governança e gestão; entre as 26 que regrediram, 15 apresentaram redução simultânea dos dois componentes. Nos demais casos, a variação positiva de um componente compensou apenas parcialmente o movimento contrário do outro.

### 2.7.2. Mudanças de nível de maturidade

A [@tbl:transicao_maturidade_2023_2026] demonstra as transições entre níveis. Houve avanço de faixa para 24 organizações (34,3%), regressão para dez (14,3%) e permanência no mesmo nível para 36 (51,4%). O número de organizações nos níveis Intermediário ou Aprimorado passou de cinco, em 2023, para 16, em 2026. Apesar dessa melhora, 54 das 70 organizações comuns (77,1%) permaneceram abaixo do nível Intermediário em 2026.

: Transição dos níveis de maturidade do iGovTI comparável entre 2023 e 2026 {#tbl:transicao_maturidade_2023_2026#}

| Nível em 2023 / nível em 2026 | Inexpressivo | Iniciando | Intermediário | Aprimorado | Total em 2023 |
|---|---:|---:|---:|---:|---:|
| **Inexpressivo** | 19 | 12 | 4 | 0 | 35 |
| **Iniciando** | 10 | 13 | 7 | 0 | 30 |
| **Intermediário** | 0 | 0 | 3 | 1 | 4 |
| **Aprimorado** | 0 | 0 | 0 | 1 | 1 |
| **Total em 2026** | 29 | 25 | 14 | 2 | 70 |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

![Matriz de transição das organizações entre os níveis de maturidade do iGovTI comparável](igovti_comparavel_transicao_maturidade_2023_2026.png){#fig:transicao_maturidade_igovti_comparavel#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

As dez regressões de faixa ocorreram do nível Iniciando para o Inexpressivo. Não foram observadas regressões a partir dos níveis Intermediário ou Aprimorado. Por outro lado, quatro organizações avançaram diretamente do nível Inexpressivo para o Intermediário, sete passaram de Iniciando para Intermediário e uma evoluiu de Intermediário para Aprimorado.

### 2.7.3. Variação dos agregados e das práticas

A [@tbl:variacao_agregados_comparaveis] apresenta a evolução média dos agregados utilizados na estrutura comparável. Os maiores avanços ocorreram em PlanejamentoTI (+0,171), EstruturaSegInfo (+0,154), gestão de serviços de TI (+0,114), ProcessoSegInfo (+0,113) e gestão de níveis de serviço (+0,110). Esses resultados indicam maior adoção declarada de instrumentos de planejamento, estruturas de segurança e processos operacionais de gestão de serviços.

: Variação média dos agregados comparáveis entre 2023 e 2026 {#tbl:variacao_agregados_comparaveis#}

| Agregado ou prática | Média em 2023 | Média em 2026 | Variação |
|---|---:|---:|---:|
| **iGovTI** | 0,184 | 0,248 | +0,064 |
| **GovernancaTI** | 0,155 | 0,211 | +0,056 |
| **iGestTI** | 0,213 | 0,284 | +0,071 |
| Modelo de gestão de TI | 0,182 | 0,283 | +0,101 |
| Monitoramento e avaliação de TI | 0,078 | 0,127 | +0,049 |
| Resultados e simplificação dos serviços | 0,212 | 0,226 | +0,014 |
| Planejamento de TI | 0,298 | 0,469 | +0,171 |
| Gestão de pessoas de TI | 0,202 | 0,134 | **-0,068** |
| Gestão de serviços de TI | 0,165 | 0,278 | +0,114 |
| Gestão de níveis de serviço | 0,122 | 0,232 | +0,110 |
| Gestão de riscos de TI | 0,111 | 0,193 | +0,082 |
| Estrutura de segurança da informação | 0,135 | 0,290 | +0,154 |
| Processos de segurança da informação | 0,177 | 0,290 | +0,113 |
| Processo de software | 0,199 | 0,264 | +0,065 |
| Gestão de projetos de TI | 0,147 | 0,231 | +0,084 |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

![Variação média dos agregados comparáveis entre 2023 e 2026](igovti_comparavel_variacao_agregados_2023_2026.png){#fig:variacao_agregados_igovti_comparavel#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

A única redução média ocorreu em PessoasTI, que passou de 0,202 para 0,134. A prática regrediu em 41 organizações, melhorou em 24 e permaneceu estável em cinco. O resultado indica que os avanços em planejamento, serviços e segurança não foram acompanhados por evolução equivalente na gestão da força de trabalho, das competências e do desempenho das equipes de TIC.

O agregado ResultadoTI apresentou crescimento médio reduzido (+0,014) e maior frequência de regressões do que de avanços: 31 organizações diminuíram seu resultado, 25 melhoraram e 14 permaneceram estáveis. MonitorAvaliaTI também apresentou evolução limitada (+0,049), com mediana de variação igual a zero. Esses resultados sugerem que a formalização de estruturas e processos avançou mais do que o monitoramento sistemático de desempenho e a demonstração de resultados associados à TIC.

O agregado ProcessosContratacao apresentou variação média de apenas +0,002. Esse agregado foi analisado de forma complementar, mas não integra o cálculo do iGovTI na estrutura harmonizada utilizada nesta comparação e, portanto, não explica as variações do índice.

### 2.7.4. Organizações com os maiores avanços

Os dez maiores aumentos do iGovTI comparável estão apresentados na [@tbl:maiores_avancos_igovti_comparavel]. A [@fig:maiores_variacoes_igovti_comparavel] permite visualizar conjuntamente os maiores avanços e regressões.

: Organizações com os maiores avanços no iGovTI comparável {#tbl:maiores_avancos_igovti_comparavel#}

| Organização | iGovTI 2023 | iGovTI 2026 | Variação | Práticas com maiores aumentos |
|---|---:|---:|---:|---|
| **RJPREV** | 0,048 | 0,576 | **+0,527** | Planejamento de TI (+1,000); monitoramento e avaliação de TI (+0,796); gestão de níveis de serviço (+0,717). |
| **SEPLAG** | 0,077 | 0,511 | **+0,434** | Gestão de riscos de TI (+1,000); planejamento de TI (+0,950); gestão de projetos de TI (+0,850). |
| **RIOPREVIDENCIA** | 0,187 | 0,551 | **+0,364** | Processo de software (+0,808); gestão de projetos de TI (+0,787); monitoramento e avaliação de TI (+0,584). |
| **DETRAN** | 0,315 | 0,666 | **+0,351** | Gestão de níveis de serviço (+1,000); gestão de riscos de TI (+0,904); modelo de gestão de TI (+0,856). |
| **CEASA** | 0,084 | 0,420 | **+0,336** | Gestão de pessoas de TI (+0,500); modelo de gestão de TI (+0,500); estrutura de segurança da informação (+0,399). |
| **CODERTE** | 0,086 | 0,419 | **+0,332** | Resultados e simplificação dos serviços (+0,729); modelo de gestão de TI (+0,472); monitoramento e avaliação de TI (+0,380). |
| **SETD** | 0,409 | 0,714 | **+0,305** | Gestão de projetos de TI (+0,680); planejamento de TI (+0,587); gestão de serviços de TI (+0,544). |
| **SES** | 0,212 | 0,487 | **+0,276** | Processos de segurança da informação (+0,703); resultados e simplificação dos serviços (+0,607); gestão de serviços de TI (+0,575). |
| **CODIN** | 0,155 | 0,413 | **+0,258** | Monitoramento e avaliação de TI (+0,760); planejamento de TI (+0,565); estrutura de segurança da informação (+0,337). |
| **FS** | 0,136 | 0,370 | **+0,234** | Planejamento de TI (+0,628); gestão de projetos de TI (+0,575); gestão de serviços de TI (+0,495). |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

Entre as 44 organizações que evoluíram, os aumentos médios mais elevados ocorreram em PlanejamentoTI (+0,294), EstruturaSegInfo (+0,260), gestão de níveis de serviço (+0,219), gestão de serviços (+0,216) e ProcessoSegInfo (+0,206). Em 30 dessas organizações, GovernancaTI e iGestTI avançaram simultaneamente, indicando evolução mais abrangente do que a simples compensação entre componentes.

### 2.7.5. Organizações com as maiores regressões

As dez maiores reduções do iGovTI comparável estão apresentadas na [@tbl:maiores_regressoes_igovti_comparavel]. Entre as 26 organizações que regrediram, as maiores quedas médias ocorreram em ResultadoTI (-0,198), PessoasTI (-0,144), processo de software (-0,089), gestão de riscos (-0,078), modelo de gestão (-0,076) e gestão de níveis de serviço (-0,074).

: Organizações com as maiores regressões no iGovTI comparável {#tbl:maiores_regressoes_igovti_comparavel#}

| Organização | iGovTI 2023 | iGovTI 2026 | Variação | Práticas com maiores reduções |
|---|---:|---:|---:|---|
| **SEGOV** | 0,349 | 0,115 | **-0,234** | Processo de software (-0,808); gestão de níveis de serviço (-0,708); planejamento de TI (-0,640). |
| **EMOP** | 0,250 | 0,026 | **-0,224** | Gestão de serviços de TI (-0,866); resultados e simplificação dos serviços (-0,450); gestão de riscos de TI (-0,426). |
| **EMATER** | 0,217 | 0,014 | **-0,204** | Gestão de projetos de TI (-0,490); resultados e simplificação dos serviços (-0,325); estrutura de segurança da informação (-0,312). |
| **SEAP** | 0,275 | 0,117 | **-0,158** | Modelo de gestão de TI (-0,472); planejamento de TI (-0,409); resultados e simplificação dos serviços (-0,142). |
| **LOTERJ** | 0,186 | 0,055 | **-0,131** | Resultados e simplificação dos serviços (-0,300); gestão de pessoas de TI (-0,284); gestão de projetos de TI (-0,150). |
| **IVB** | 0,253 | 0,124 | **-0,128** | Gestão de pessoas de TI (-0,598); resultados e simplificação dos serviços (-0,575); modelo de gestão de TI (-0,150). |
| **SEPM** | 0,222 | 0,097 | **-0,125** | Resultados e simplificação dos serviços (-0,717); modelo de gestão de TI (-0,100); gestão de riscos de TI (-0,069). |
| **SECC** | 0,170 | 0,053 | **-0,117** | Resultados e simplificação dos serviços (-0,500); modelo de gestão de TI (-0,150); processo de software (-0,150). |
| **SUDERJ** | 0,111 | 0,001 | **-0,110** | Modelo de gestão de TI (-0,150); planejamento de TI (-0,150); resultados e simplificação dos serviços (-0,150). |
| **TURISRIO** | 0,183 | 0,075 | **-0,108** | Gestão de riscos de TI (-0,426); planejamento de TI (-0,225); gestão de pessoas de TI (-0,170). |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

![Organizações com as maiores variações do iGovTI comparável](igovti_comparavel_maiores_variacoes_2023_2026.png){#fig:maiores_variacoes_igovti_comparavel#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

Em 15 das 26 organizações que regrediram, houve redução simultânea de GovernancaTI e iGestTI. Nas demais, a melhora de um componente não foi suficiente para compensar a queda do outro. O predomínio de perdas em ResultadoTI e PessoasTI indica que parte das regressões está associada à menor adoção declarada de práticas voltadas à entrega e mensuração de resultados, simplificação dos serviços públicos, dimensionamento da força de trabalho, desenvolvimento de competências e avaliação de desempenho.

### 2.7.6. Resultados dos municípios comuns

O grupo municipal comum aos dois ciclos contém apenas quatro organizações, razão pela qual não é adequado generalizar seus resultados para o conjunto dos municípios jurisdicionados. Rio das Ostras apresentou o maior avanço, de 0,059 para 0,253, passando do nível Inexpressivo para Iniciando. Maricá aumentou de 0,171 para 0,216 e permaneceu no nível Iniciando. Saquarema e Volta Redonda permaneceram no nível Inexpressivo e registraram reduções de 0,063 e 0,036, respectivamente.

: Evolução do iGovTI comparável nos municípios presentes nos dois ciclos {#tbl:evolucao_municipios_igovti_comparavel#}

| Município | iGovTI 2023 | iGovTI 2026 | Variação | Nível em 2023 | Nível em 2026 |
|---|---:|---:|---:|---|---|
| **Maricá** | 0,171 | 0,216 | +0,046 | Iniciando | Iniciando |
| **Rio das Ostras** | 0,059 | 0,253 | +0,194 | Inexpressivo | Iniciando |
| **Saquarema** | 0,090 | 0,027 | -0,063 | Inexpressivo | Inexpressivo |
| **Volta Redonda** | 0,062 | 0,026 | -0,036 | Inexpressivo | Inexpressivo |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

Em síntese, a comparação harmonizada indica avanço médio das práticas de governança e gestão de TIC entre 2023 e 2026, especialmente em planejamento, gestão de serviços e segurança da informação. Esse avanço não foi generalizado: mais de um terço das organizações regrediu no índice, a gestão de pessoas apresentou redução média e a maioria das organizações comuns permaneceu abaixo do nível Intermediário. Os resultados recomendam que a análise das organizações com maior regressão seja aprofundada mediante confronto das respostas com as evidências e com eventuais mudanças institucionais ocorridas no período.

## 2.8. Leitura integrada do resultado individual

A [@fig:perfil_dimensoes_gestao_auditado] apresenta o perfil do(a) **{{ auditado.sigla }}** nas seis dimensões de gestão e o compara com as medianas observadas nas 114 organizações únicas. Essa visualização permite distinguir fragilidades sistêmicas, comuns ao conjunto avaliado, de lacunas particularmente acentuadas no auditado.

![Perfil do(a) {{ auditado.sigla }} nas dimensões do iGestTI em comparação com as medianas gerais]({{ auditado.sigla }}_perfil_dimensoes_iGestTI.png){#fig:perfil_dimensoes_gestao_auditado#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

A priorização de melhorias não deve buscar apenas a elevação numérica do índice. Recomenda-se concentrar esforços nas capacidades com menor resultado que, simultaneamente, estejam associadas a riscos relevantes, serviços críticos, obrigações normativas e necessidades institucionais do(a) **{{ auditado.sigla }}**. Os achados apresentados na Seção 3 complementam essa leitura quantitativa mediante o exame das respostas, das evidências e dos critérios de auditoria aplicáveis.

## 2.9. Questões avaliadas no relatório individual

A matriz de planejamento do iGovTI 2026 definiu questões de auditoria voltadas à avaliação da governança e da gestão de TIC. Para fins deste relatório individual preliminar, os possíveis achados decorrem das Questões 1 a 6, que tratam de temas passíveis de responsabilização institucional específica por organização.

: Questões de auditoria com avaliação individual preliminar {#tbl:questoes_avaliadas_individualmente#}

| Questão | Tema | Síntese do objeto avaliado |
|---|---|---|
| **Q1** | Estrutura de TIC | Formalização, atribuições e posicionamento organizacional da área, unidade, setor ou função de TIC. |
| **Q2** | Governança e comitê de TIC | Modelo de governança, atuação da alta administração, comitê de TIC, monitoramento de desempenho e gestão de riscos. |
| **Q3** | Planejamento de TIC | Existência, formalização, atualização, alinhamento e execução do plano de TIC. |
| **Q4** | Capacidade institucional de TIC e segurança da informação | Gestão de riscos, continuidade, segurança da informação, força de trabalho e capacidade institucional para sustentar a TIC. |
| **Q5** | Gestão de serviços de TIC | Catálogo de serviços, níveis de serviço, gestão de ativos, incidentes, problemas, mudanças, disponibilidade e continuidade operacional. |
| **Q6** | Contratações de TIC | Planejamento, aprovação técnica, alinhamento, equipe de planejamento, análise de riscos, fiscalização e controle de resultados das contratações de TIC. |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

As Questões 7 e Transversal possuem natureza de levantamento e análise agregada, não gerando achado individual por organização. Seus resultados serão tratados, quando aplicável, em relatório consolidado, com as cautelas metodológicas necessárias à comparação entre ciclos e entre trabalhos anteriores.

\newpage

{% if auditado.tem_achados %}

\newpage

# 3. Resultados da Auditoria

Os achados de auditoria apresentados a seguir decorrem da avaliação preliminar das respostas do(a) **{{ auditado.sigla }}** ao questionário iGovTI 2026, das evidências encaminhadas e das situações encontradas previstas na matriz de planejamento.

Cada achado apresenta os critérios aplicáveis, as evidências consideradas, a situação encontrada no auditado, a conclusão da Equipe de Auditoria e as propostas de encaminhamento. Como os achados são renderizados apenas quando há ao menos uma situação encontrada, cada seção responde objetivamente à respectiva questão de auditoria de forma negativa, delimitando as fragilidades identificadas, os critérios infringidos e os efeitos esperados.

{% include 'achado_questao_1_estrutura_tic.md' %}

{% include 'achado_questao_2_governanca_comite_tic.md' %}

{% include 'achado_questao_3_planejamento_tic.md' %}

{% include 'achado_questao_4_capacidade_institucional_tic_si.md' %}

{% include 'achado_questao_5_gestao_servicos_tic.md' %}

{% include 'achado_questao_6_contratacoes_tic.md' %}

\newpage

# 4. Plano de ação

Para facilitar o atendimento das propostas constantes da Seção 3, a Equipe de Auditoria elaborou modelo de plano de ação contendo os encaminhamentos preliminarmente propostos ao(à) **{{ auditado.sigla }}**.

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

Com base na avaliação preliminar das respostas e das evidências do(a) **{{ auditado.sigla }}**, não foram identificadas situações que ensejassem achado individual nas Questões 1 a 6 da matriz de planejamento.

{% endif %}

{% if teve_ajuste %}

\newpage

# Apêndice A. Ajustes nas respostas declaradas

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
