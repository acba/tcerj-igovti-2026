---
title: "RELATÓRIO INDIVIDUAL PRELIMINAR"
subtitle: PIORCASO - Organização Pública de Teste - Pior Caso
lang: pt-BR
figure-caption-position: above
---

# 1. Introdução

Este relatório apresenta os resultados preliminares do(a) **PIORCASO** relativos à Fiscalização TCE-RJ nº 18/2026 - iGovTI 2026, cujo objetivo é avaliar o grau de adoção de práticas de governança e gestão de tecnologia da informação e comunicação pelas organizações jurisdicionadas.

O trabalho foi realizado por meio de questionário eletrônico de autoavaliação de controles, método conhecido como *Control Self-Assessment* (CSA), no qual os gestores declararam a situação da organização em relação às práticas avaliadas e encaminharam evidências para corroborar as respostas prestadas. As evidências foram analisadas pela Equipe de Auditoria, nos termos definidos na matriz de planejamento e nos procedimentos de verificação aplicáveis.

O questionário do iGovTI 2026 foi estruturado para coletar informações sobre governança de TIC, gestão de TIC, segurança da informação, riscos, continuidade, serviços, contratações, estrutura organizacional, força de trabalho, soluções de TIC, projetos e temas emergentes, como inteligência artificial. A avaliação busca identificar capacidades, riscos, fragilidades, iniciativas e oportunidades de aprimoramento relacionadas ao uso institucional da tecnologia.

Os achados constantes deste relatório têm natureza preliminar e decorrem da análise das respostas declaradas, das evidências apresentadas e das regras de identificação previstas na matriz de planejamento. A manifestação do gestor poderá ser considerada pela Equipe de Auditoria antes da consolidação do relatório individual final.

# 2. Resultado do iGovTI 2026

O iGovTI 2026 é um índice composto que consolida resultados de governança e gestão de TIC em escala de 0 a 1. As respostas categóricas ao questionário são inicialmente convertidas em valores numéricos: **Não adota** = 0; **Há decisão formal ou plano aprovado para adotá-lo** = 0,05; **Adota em menor parte** = 0,15; **Adota parcialmente** = 0,50; e **Adota em maior parte ou totalmente** = 1,00. A resposta **Não se aplica** recebe valor 0,50 na estrutura de cálculo, sem prejuízo da avaliação da justificativa apresentada e da aderência dessa opção ao contexto da organização.

Quando a questão possui itens de detalhamento, a pontuação da resposta principal pode ser reduzida conforme os itens efetivamente atendidos. Na sequência, os valores são combinados por somas ponderadas em uma árvore de agregação. O componente **GovernancaTI** resulta de quatro práticas diretamente ponderadas; o **iGestTI** reúne seis dimensões: PlanejamentoTI, ServicosTI, RiscosTISegInfo, EstruturaSegInfo, ProcessoSegInfo e GerirSoluçõesTI. O índice final é calculado pela seguinte expressão:

`iGovTI = 0,477696299232863 x GovernancaTI + 0,522303700767137 x iGestTI`

Após o cálculo, a organização é classificada nos níveis de maturidade **Inexpressivo** (`0 <= iGovTI < 0,15`), **Iniciando** (`0,15 <= iGovTI < 0,40`), **Intermediário** (`0,40 <= iGovTI < 0,70`) ou **Aprimorado** (`0,70 <= iGovTI <= 1,00`).

As evidências anexadas e as justificativas textuais não entram diretamente no cálculo do índice. Elas são utilizadas pela Equipe de Auditoria para avaliar a consistência das respostas declaradas, apoiar eventuais ajustes de respostas e subsidiar a identificação de achados de auditoria.

O(A) **PIORCASO** obteve o **valor 0.00 para o iGovTI 2026**, correspondente ao nível **Inexpressivo** de maturidade.

![Figura 1 - Distribuição dos resultados do iGovTI 2026 e posição do(a) PIORCASO](PIORCASO_comparativo_distribuicao_iGovTI.png)
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

A Figura 2 apresenta a composição do resultado do(a) **PIORCASO** entre governança e gestão de TIC.

![Figura 2 - Resultado do(a) PIORCASO por componentes do iGovTI 2026](PIORCASO_componentes_iGovTI.png)
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

: Tabela 1 - Resultado sintético do iGovTI 2026 do(a) PIORCASO

| Componente | Peso no iGovTI 2026 | Valor | Nível |
|---|---:|---:|---|
| **Governança de TIC** | 0,477696299232863 | 0.00 | Inexpressivo |
| **Gestão de TIC** | 0,522303700767137 | 0.00 | Inexpressivo |
| **iGovTI 2026** | 1,000000000000000 | 0.00 | Inexpressivo |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

## 2.1. Principais alterações em relação ao iGovTI 2023

A estrutura de 2026 preservou a escala de 0 a 1, as categorias de resposta e as quatro faixas de maturidade empregadas em 2023, mas alterou de forma relevante a composição dos agregados e seus pesos. As principais diferenças estão sintetizadas na Tabela 2.

: Tabela 2 - Principais diferenças entre as estruturas do iGovTI 2023 e do iGovTI 2026

| Aspecto | iGovTI 2023 | iGovTI 2026 | Implicação analítica |
|---|---|---|---|
| **Composição do índice final** | GovernancaTI e iGestTI com pesos iguais de 0,50. | GovernancaTI com peso 0,477696 e iGestTI com peso 0,522304. | A gestão passou a ter participação ligeiramente superior no índice final. |
| **Governança de TIC** | Agregação hierárquica de ModeloTI, MonitorAvaliaTI e ResultadoTI. | Agregação direta de quatro práticas relativas ao modelo de gestão, monitoramento, auditoria interna e simplificação de serviços públicos. | O componente tornou-se mais direto e incorporou práticas com escopo distinto da estrutura anterior. |
| **Gestão de TIC** | Agregação de PlanejamentoTI, PessoasTI e ProcessosTI; este último reunia serviços, níveis de serviço, riscos, segurança, software, projetos e contratos. | Agregação direta de PlanejamentoTI, ServicosTI, RiscosTISegInfo, EstruturaSegInfo, ProcessoSegInfo e GerirSoluçõesTI. | O índice passou a evidenciar separadamente seis capacidades operacionais e de segurança. |
| **Pessoas e contratações** | PessoasTI e iGestContratosTI integravam o cálculo do iGestTI. | Não integram a árvore de cálculo do iGovTI 2026, embora continuem relevantes para o diagnóstico e para a auditoria. | Mudanças nessas matérias não explicam diretamente a variação do índice de 2026. |
| **Serviços, software e projetos** | Serviços e níveis de serviço eram agregados distintos; software e projetos integravam ProcessosTI. | Serviços foram consolidados em ServicosTI; software e projetos foram reunidos em GerirSoluçõesTI. | A leitura deve considerar a nova delimitação conceitual dos componentes. |
| **Codificação das respostas** | Estrutura voltada principalmente a rótulos textuais já decodificados. | Inclui códigos nativos exportados pelo LimeSurvey, além dos rótulos textuais de contingência. | Reduz ambiguidades de conversão e aproxima o cálculo da base original de respostas. |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

Em razão dessas alterações, a diferença entre os valores nominais de 2023 e 2026 não deve ser interpretada automaticamente como evolução ou retrocesso institucional. Uma análise temporal válida exige a harmonização das questões e dos agregados comparáveis, além da consideração de mudanças de escopo, pesos, respondentes e qualidade das evidências.

## 2.2. Questões avaliadas no relatório individual

A matriz de planejamento do iGovTI 2026 definiu questões de auditoria voltadas à avaliação da governança e da gestão de TIC. Para fins deste relatório individual preliminar, os possíveis achados decorrem das Questões 1 a 6, que tratam de temas passíveis de responsabilização institucional específica por organização.

: Tabela 3 - Questões de auditoria com avaliação individual preliminar

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

## 2.3. Governança de TIC

A governança de TIC avalia a capacidade da alta administração de orientar, dirigir, monitorar e controlar o uso da tecnologia da informação, de modo alinhado aos objetivos institucionais, aos riscos relevantes e às necessidades das áreas finalísticas e administrativas.

No iGovTI 2026, a dimensão de governança consolida práticas relacionadas ao modelo de gestão de TIC, à atuação de comitês ou instâncias equivalentes, ao monitoramento do desempenho, à participação da alta administração e ao alinhamento entre decisões de TIC, estratégia organizacional, orçamento, riscos e valor público.

O(A) **PIORCASO** obteve o **valor 0.00 no componente Governança de TIC**, correspondente ao nível **Inexpressivo**.

![Figura 3 - Resultado do componente Governança de TIC do(a) PIORCASO](PIORCASO_comparativo_distribuicao_GovernancaTI.png)
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

## 2.4. Gestão de TIC

A gestão de TIC avalia a capacidade da organização de planejar, executar, monitorar e aperfeiçoar processos, serviços, controles, recursos e contratações de tecnologia da informação, de forma compatível com suas necessidades institucionais.

No iGovTI 2026, o componente **iGestTI** consolida dimensões de planejamento de TIC, gestão de serviços, riscos e segurança da informação, estrutura de segurança da informação, processos de segurança da informação e gestão de soluções de TIC.

O(A) **PIORCASO** obteve o **valor 0.00 no componente Gestão de TIC**, correspondente ao nível **Inexpressivo**.

![Figura 4 - Resultado do componente Gestão de TIC do(a) PIORCASO](PIORCASO_comparativo_distribuicao_iGestTI.png)
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```


# 3. Análise integrada dos resultados do iGovTI 2026

A análise consolidada apresentada nesta seção utiliza os resultados calculados para as 114 organizações únicas constantes da planilha `iGovTI-2026.xlsx`. A base possuía 115 linhas, mas um registro incompleto e não submetido da CODIN foi desconsiderado por duplicar a organização e não representar uma resposta concluída. O objetivo da análise é contextualizar o resultado individual do(a) **PIORCASO**, identificar padrões de maturidade, assimetrias entre governança e gestão e capacidades que se mostram mais ou menos desenvolvidas no conjunto avaliado.

Os resultados permanecem sujeitos às limitações inerentes à autoavaliação. O índice traduz a adoção declarada das práticas segundo a estrutura de cálculo, enquanto a confirmação de sua efetiva institucionalização depende da análise das evidências. Por essa razão, a posição relativa e os padrões estatísticos constituem elementos de diagnóstico e priorização, mas não configuram, isoladamente, achado de auditoria.

## 3.1. Quadro geral

A distribuição por nível de maturidade, apresentada na Figura 5, evidencia concentração nos estágios iniciais. Das 114 organizações, 52 (45,6%) foram classificadas no nível **Inexpressivo** e 41 (36,0%) no nível **Iniciando**. Assim, 93 organizações (81,6%) obtiveram resultado inferior a 0,40. Somente 15 organizações (13,2%) alcançaram o nível **Intermediário** e seis (5,3%) o nível **Aprimorado**.

![Figura 5 - Distribuição das organizações por nível de maturidade do iGovTI 2026](igovti_2026_distribuicao_maturidade.png)
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

O iGovTI apresentou média de 0,234 e mediana de 0,174. O primeiro quartil foi 0,074 e o terceiro quartil, 0,329, o que significa que metade das organizações se concentrou nesse intervalo e que pelo menos 75% permaneceram abaixo do nível Intermediário. A média superior à mediana, combinada com o valor máximo de 0,843 e com apenas seis organizações no nível Aprimorado, caracteriza uma distribuição assimétrica à direita: um grupo reduzido de resultados elevados desloca a média para cima, sem alterar o quadro predominante de baixa maturidade. Seis organizações apresentaram valor igual a zero no índice calculado.

A posição específica do(a) **PIORCASO** nessa distribuição pode ser observada na Figura 1. Diferenças pequenas entre organizações próximas devem ser interpretadas com cautela, pois o índice não dispõe de margem de erro estimada e pode ser afetado pela qualidade das respostas e das evidências apresentadas.

## 3.2. Relação entre governança e gestão de TIC

Os indicadores descritivos da Tabela 4 mostram que o componente de gestão apresentou resultados superiores aos de governança no conjunto avaliado. A média do iGestTI foi 0,258, ante 0,207 para GovernancaTI; as medianas foram, respectivamente, 0,201 e 0,148. As duas médias situaram-se no nível Iniciando, enquanto a mediana de GovernancaTI permaneceu no nível Inexpressivo e a mediana de iGestTI, no nível Iniciando.

: Tabela 4 - Estatísticas descritivas do iGovTI 2026 e de seus componentes principais

| Indicador | Média | 1º quartil | Mediana | 3º quartil | Organizações com valor >= 0,40 |
|---|---:|---:|---:|---:|---:|
| **iGovTI** | 0,234 | 0,074 | 0,174 | 0,329 | 21 (18,4%) |
| **GovernancaTI** | 0,207 | 0,029 | 0,148 | 0,261 | 22 (19,3%) |
| **iGestTI** | 0,258 | 0,094 | 0,201 | 0,369 | 27 (23,7%) |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

A Figura 6 permite comparar a dispersão dos três indicadores. O iGestTI superou GovernancaTI em 73 organizações (64,0%); o movimento inverso ocorreu em 35 (30,7%); e houve igualdade em seis (5,3%). O padrão indica que, para a maior parte das organizações, as capacidades operacionais de gestão se situaram em patamar superior ao dos mecanismos de direção, monitoramento e controle exercidos pela alta administração. Essa diferença, contudo, não elimina a baixa maturidade da gestão: 87 organizações (76,3%) também obtiveram iGestTI inferior a 0,40.

![Figura 6 - Distribuição do iGovTI 2026 e dos componentes GovernancaTI e iGestTI](igovti_2026_distribuicao_componentes.png)
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>


No caso do(a) **PIORCASO**, GovernancaTI e iGestTI apresentaram o mesmo valor. A igualdade dos componentes não implica equilíbrio em nível adequado, razão pela qual a análise deve considerar o nível de maturidade alcançado e as fragilidades específicas evidenciadas em cada dimensão.


## 3.3. Dimensões da gestão de TIC

A decomposição do iGestTI revela diferenças relevantes entre as seis dimensões avaliadas. Conforme a Tabela 5, PlanejamentoTI apresentou a maior média (0,380) e a maior mediana (0,326). Foi também a dimensão de maior resultado em 60 organizações (52,6%), considerados os empates. Esse padrão indica que processos e instrumentos de planejamento estão mais disseminados do que as capacidades operacionais, de segurança e de gestão de soluções.

: Tabela 5 - Estatísticas descritivas das dimensões do iGestTI

| Dimensão | Média | Mediana | Resultados iguais a zero | Organizações com valor inferior a 0,40 |
|---|---:|---:|---:|---:|
| **PlanejamentoTI** | 0,380 | 0,326 | 16 (14,0%) | 65 (57,0%) |
| **ServicosTI** | 0,233 | 0,147 | 18 (15,8%) | 87 (76,3%) |
| **RiscosTISegInfo** | 0,188 | 0,101 | 31 (27,2%) | 95 (83,3%) |
| **EstruturaSegInfo** | 0,274 | 0,140 | 26 (22,8%) | 79 (69,3%) |
| **ProcessoSegInfo** | 0,270 | 0,208 | 12 (10,5%) | 87 (76,3%) |
| **GerirSoluçõesTI** | 0,210 | 0,150 | 28 (24,6%) | 95 (83,3%) |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

A distribuição completa das seis dimensões é apresentada na Figura 7, incluindo medianas, intervalos interquartis e médias.

![Figura 7 - Distribuição dos resultados das seis dimensões que compõem o iGestTI](igovti_2026_distribuicao_dimensoes_gestao.png)
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

As maiores fragilidades agregadas concentram-se em **RiscosTISegInfo** e **GerirSoluçõesTI**. As duas dimensões apresentaram as menores médias e registraram valores inferiores a 0,40 em 95 organizações (83,3%). RiscosTISegInfo apareceu entre as dimensões de menor resultado de 50 organizações (43,9%), enquanto GerirSoluçõesTI ocupou essa posição em 44 (38,6%), considerados os empates. O quadro indica que a formalização do planejamento, quando existente, frequentemente não é acompanhada, na mesma intensidade, por gestão de riscos, continuidade, desenvolvimento de software e gestão de projetos.

EstruturaSegInfo apresentou média de 0,274 e mediana de apenas 0,140. Essa diferença, associada à ampla dispersão observada na Figura 7, evidencia heterogeneidade: um grupo de organizações possui estruturas de segurança mais consolidadas, enquanto parcela expressiva permanece próxima dos níveis inferiores. ProcessoSegInfo mostrou mediana superior à de EstruturaSegInfo, mas 76,3% das organizações ainda permaneceram abaixo de 0,40, o que recomenda examinar separadamente a existência da estrutura formal e a execução contínua dos processos de segurança.

## 3.4. Associações entre capacidades

A análise de correlação apresentada na Figura 8 mostra que as dimensões de gestão evoluem de forma associada. A relação linear mais elevada ocorreu entre ServicosTI e GerirSoluçõesTI (`r = 0,82`), seguida por ServicosTI e ProcessoSegInfo (`r = 0,78`). Em termos descritivos, organizações com gestão de serviços mais estruturada também tendem a apresentar melhores capacidades para desenvolver e gerenciar soluções e para executar processos de segurança da informação.

![Figura 8 - Correlação entre as dimensões que compõem o iGestTI](igovti_2026_correlacao_dimensoes_gestao.png)
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

Essas associações não demonstram relação de causa e efeito e são parcialmente esperadas, pois as dimensões integram um mesmo construto de maturidade de gestão. Ainda assim, o padrão recomenda uma abordagem coordenada: catálogo e níveis de serviço, ativos, mudanças, incidentes, segurança, desenvolvimento de software e projetos compartilham informações, papéis, processos e mecanismos de monitoramento. O aprimoramento sustentável do iGovTI deve ser orientado por riscos e vinculado aos objetivos institucionais.

## 3.5. Evolução das organizações avaliadas em 2023 e 2026

A comparação temporal foi realizada a partir das planilhas `iGovTI-2023-SETIC-Ajustado-Comparavel.xlsx`, `iGovTI-2023-Municipios-Ajustado-Comparavel.xlsx` e `iGovTI-2026-Ajustado-Comparavel.xlsx`. Essas bases recalculam os resultados de 2023 e 2026 segundo uma estrutura harmonizada, na qual GovernancaTI e iGestTI possuem pesos iguais de 0,50. Foram mantidas apenas as organizações identificadas nos dois ciclos.

Após a padronização de acentos, sinais, prefixos municipais e variações inequívocas de sigla, foram pareadas 70 organizações: 66 integrantes do conjunto estadual e quatro municípios. Não foram equiparadas unidades cuja mudança de denominação pudesse estar associada a alteração de competências ou de estrutura administrativa. No caso da CODIN, foi considerado o envio concluído em 26 de maio de 2026; o segundo registro existente na base de 2026 foi desconsiderado por se tratar de tentativa não submetida e com respostas incompletas.

A harmonização reduz parte das diferenças entre os questionários, mas não elimina todas as limitações de comparabilidade. Os resultados podem refletir mudanças efetivas nas práticas, alterações na interpretação das questões, diferenças na qualidade das respostas e evidências ou mudanças institucionais ocorridas no período. Portanto, as variações devem ser lidas como evolução ou regressão dos resultados declarados e recalculados, e não como comprovação isolada de melhoria ou deterioração da gestão.

### 3.5.1. Evolução geral do índice

Na amostra pareada, a média do iGovTI passou de 0,184, em 2023, para 0,248, em 2026, correspondendo a aumento absoluto de 0,064. A mediana passou de 0,151 para 0,199. A elevação da média foi acompanhada por aumento da dispersão: o desvio-padrão passou de 0,146 para 0,192 e o terceiro quartil, de 0,230 para 0,381. Esse resultado indica melhora do nível central, mas também maior diferenciação entre as organizações.

A Figura 9 apresenta as distribuições pareadas nos dois ciclos. Das 70 organizações, 44 (62,9%) aumentaram o iGovTI e 26 (37,1%) registraram redução. Em 32 casos (45,7%), o aumento foi igual ou superior a 0,05; em 13 (18,6%), a redução alcançou pelo menos 0,05 em valor absoluto; e 25 organizações (35,7%) permaneceram no intervalo de variação entre -0,05 e +0,05.

![Figura 9 - Distribuição do iGovTI comparável das organizações comuns em 2023 e 2026](igovti_comparavel_distribuicao_2023_2026.png)
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

O resultado médio de GovernancaTI aumentou de 0,155 para 0,211, enquanto o iGestTI passou de 0,213 para 0,284. Assim, o avanço médio do índice foi sustentado pelos dois componentes, com variação ligeiramente maior na gestão. Entre as 44 organizações que evoluíram, 30 apresentaram crescimento simultâneo de governança e gestão; entre as 26 que regrediram, 15 apresentaram redução simultânea dos dois componentes. Nos demais casos, a variação positiva de um componente compensou apenas parcialmente o movimento contrário do outro.

### 3.5.2. Mudanças de nível de maturidade

A Tabela 6 demonstra as transições entre níveis. Houve avanço de faixa para 24 organizações (34,3%), regressão para dez (14,3%) e permanência no mesmo nível para 36 (51,4%). O número de organizações nos níveis Intermediário ou Aprimorado passou de cinco, em 2023, para 16, em 2026. Apesar dessa melhora, 54 das 70 organizações comuns (77,1%) permaneceram abaixo do nível Intermediário em 2026.

: Tabela 6 - Transição dos níveis de maturidade do iGovTI comparável entre 2023 e 2026

| Nível em 2023 / nível em 2026 | Inexpressivo | Iniciando | Intermediário | Aprimorado | Total em 2023 |
|---|---:|---:|---:|---:|---:|
| **Inexpressivo** | 19 | 12 | 4 | 0 | 35 |
| **Iniciando** | 10 | 13 | 7 | 0 | 30 |
| **Intermediário** | 0 | 0 | 3 | 1 | 4 |
| **Aprimorado** | 0 | 0 | 0 | 1 | 1 |
| **Total em 2026** | 29 | 25 | 14 | 2 | 70 |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

![Figura 10 - Matriz de transição das organizações entre os níveis de maturidade do iGovTI comparável](igovti_comparavel_transicao_maturidade_2023_2026.png)
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

As dez regressões de faixa ocorreram do nível Iniciando para o Inexpressivo. Não foram observadas regressões a partir dos níveis Intermediário ou Aprimorado. Por outro lado, quatro organizações avançaram diretamente do nível Inexpressivo para o Intermediário, sete passaram de Iniciando para Intermediário e uma evoluiu de Intermediário para Aprimorado.

### 3.5.3. Variação dos agregados e das práticas

A Tabela 7 apresenta a evolução média dos agregados utilizados na estrutura comparável. Os maiores avanços ocorreram em PlanejamentoTI (+0,171), EstruturaSegInfo (+0,154), gestão de serviços de TI (+0,114), ProcessoSegInfo (+0,113) e gestão de níveis de serviço (+0,110). Esses resultados indicam maior adoção declarada de instrumentos de planejamento, estruturas de segurança e processos operacionais de gestão de serviços.

: Tabela 7 - Variação média dos agregados comparáveis entre 2023 e 2026

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

![Figura 11 - Variação média dos agregados comparáveis entre 2023 e 2026](igovti_comparavel_variacao_agregados_2023_2026.png)
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

A única redução média ocorreu em PessoasTI, que passou de 0,202 para 0,134. A prática regrediu em 41 organizações, melhorou em 24 e permaneceu estável em cinco. O resultado indica que os avanços em planejamento, serviços e segurança não foram acompanhados por evolução equivalente na gestão da força de trabalho, das competências e do desempenho das equipes de TIC.

O agregado ResultadoTI apresentou crescimento médio reduzido (+0,014) e maior frequência de regressões do que de avanços: 31 organizações diminuíram seu resultado, 25 melhoraram e 14 permaneceram estáveis. MonitorAvaliaTI também apresentou evolução limitada (+0,049), com mediana de variação igual a zero. Esses resultados sugerem que a formalização de estruturas e processos avançou mais do que o monitoramento sistemático de desempenho e a demonstração de resultados associados à TIC.

O agregado ProcessosContratacao apresentou variação média de apenas +0,002. Esse agregado foi analisado de forma complementar, mas não integra o cálculo do iGovTI na estrutura harmonizada utilizada nesta comparação e, portanto, não explica as variações do índice.

### 3.5.4. Organizações com os maiores avanços

Os dez maiores aumentos do iGovTI comparável estão apresentados na Tabela 8. A Figura 12 permite visualizar conjuntamente os maiores avanços e regressões.

: Tabela 8 - Organizações com os maiores avanços no iGovTI comparável

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

### 3.5.5. Organizações com as maiores regressões

As dez maiores reduções do iGovTI comparável estão apresentadas na Tabela 9. Entre as 26 organizações que regrediram, as maiores quedas médias ocorreram em ResultadoTI (-0,198), PessoasTI (-0,144), processo de software (-0,089), gestão de riscos (-0,078), modelo de gestão (-0,076) e gestão de níveis de serviço (-0,074).

: Tabela 9 - Organizações com as maiores regressões no iGovTI comparável

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

![Figura 12 - Organizações com as maiores variações do iGovTI comparável](igovti_comparavel_maiores_variacoes_2023_2026.png)
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

Em 15 das 26 organizações que regrediram, houve redução simultânea de GovernancaTI e iGestTI. Nas demais, a melhora de um componente não foi suficiente para compensar a queda do outro. O predomínio de perdas em ResultadoTI e PessoasTI indica que parte das regressões está associada à menor adoção declarada de práticas voltadas à entrega e mensuração de resultados, simplificação dos serviços públicos, dimensionamento da força de trabalho, desenvolvimento de competências e avaliação de desempenho.

### 3.5.6. Resultados dos municípios comuns

O grupo municipal comum aos dois ciclos contém apenas quatro organizações, razão pela qual não é adequado generalizar seus resultados para o conjunto dos municípios jurisdicionados. Rio das Ostras apresentou o maior avanço, de 0,059 para 0,253, passando do nível Inexpressivo para Iniciando. Maricá aumentou de 0,171 para 0,216 e permaneceu no nível Iniciando. Saquarema e Volta Redonda permaneceram no nível Inexpressivo e registraram reduções de 0,063 e 0,036, respectivamente.

: Tabela 10 - Evolução do iGovTI comparável nos municípios presentes nos dois ciclos

| Município | iGovTI 2023 | iGovTI 2026 | Variação | Nível em 2023 | Nível em 2026 |
|---|---:|---:|---:|---|---|
| **Maricá** | 0,171 | 0,216 | +0,046 | Iniciando | Iniciando |
| **Rio das Ostras** | 0,059 | 0,253 | +0,194 | Inexpressivo | Iniciando |
| **Saquarema** | 0,090 | 0,027 | -0,063 | Inexpressivo | Inexpressivo |
| **Volta Redonda** | 0,062 | 0,026 | -0,036 | Inexpressivo | Inexpressivo |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

Em síntese, a comparação harmonizada indica avanço médio das práticas de governança e gestão de TIC entre 2023 e 2026, especialmente em planejamento, gestão de serviços e segurança da informação. Esse avanço não foi generalizado: mais de um terço das organizações regrediu no índice, a gestão de pessoas apresentou redução média e a maioria das organizações comuns permaneceu abaixo do nível Intermediário. Os resultados recomendam que a análise das organizações com maior regressão seja aprofundada mediante confronto das respostas com as evidências e com eventuais mudanças institucionais ocorridas no período.

## 3.6. Leitura integrada do resultado individual

A Figura 13 apresenta o perfil do(a) **PIORCASO** nas seis dimensões de gestão e o compara com as medianas observadas nas 114 organizações únicas. Essa visualização permite distinguir fragilidades sistêmicas, comuns ao conjunto avaliado, de lacunas particularmente acentuadas no auditado.

![Figura 13 - Perfil do(a) PIORCASO nas dimensões do iGestTI em comparação com as medianas gerais](PIORCASO_perfil_dimensoes_iGestTI.png)
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

A priorização de melhorias não deve buscar apenas a elevação numérica do índice. Recomenda-se concentrar esforços nas capacidades com menor resultado que, simultaneamente, estejam associadas a riscos relevantes, serviços críticos, obrigações normativas e necessidades institucionais do(a) **PIORCASO**. Os achados apresentados na seção seguinte complementam essa leitura quantitativa mediante o exame das respostas, das evidências e dos critérios de auditoria aplicáveis.




```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```


# 4. Resultados da Auditoria

Os achados de auditoria apresentados a seguir decorrem da avaliação preliminar das respostas do(a) **PIORCASO** ao questionário iGovTI 2026, das evidências encaminhadas e das situações encontradas previstas na matriz de planejamento.

Cada achado apresenta os critérios aplicáveis, as evidências consideradas, a situação encontrada no auditado, a conclusão da Equipe de Auditoria e as propostas de encaminhamento. Como os achados são renderizados apenas quando há ao menos uma situação encontrada, cada seção responde objetivamente à respectiva questão de auditoria de forma negativa, delimitando as fragilidades identificadas, os critérios infringidos e os efeitos esperados.






```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```


## Achado 1 – Estrutura de TIC insuficiente para coordenar, gerir e sustentar a tecnologia da informação.

### Critérios
* COBIT 2019, APO01.04 - Definir e implementar as estruturas organizacionais: estabelecer estruturas organizacionais internas e externas necessárias para apoiar os objetivos de governança e gestão de TI;
* COBIT 2019, APO01.05 - Estabelecer papéis e responsabilidades: definir, comunicar e manter papéis e responsabilidades relacionados à governança e gestão de TI;
* COBIT 2019, APO01.06 - Aprimorar o posicionamento da função de TI: posicionar a função de tecnologia de modo compatível com sua relevância estratégica, responsabilidades e necessidade de interação com a alta administração;
* COBIT 2019, APO01.09 - Definição e comunicação de políticas e procedimentos: estabelecer e comunicar políticas e procedimentos de gestão de TI que orientem papéis, responsabilidades e controles;
* ABNT NBR ISO/IEC 38500:2025, item 5.6.1 - Governança efetiva de TI: responsabilização clara, estrutura adequada de tomada de decisão e direção organizacional compatível com o uso atual e futuro da tecnologia.

### Evidências

* Resposta declarada no questionário iGovTI 2026 indicando não adoção das práticas avaliadas;

* Ausência de documentação comprobatória suficiente nos arquivos encaminhados pelo auditado;

* Resultado dos procedimentos de auditoria aplicáveis à questão;


### Situação encontrada



A partir da análise das informações fornecidas, verificou-se que a organização PIORCASO não demonstrou atender integralmente ao requisito de possuir área, unidade, setor ou função de TIC formalmente instituída, com atribuições definidas e posicionamento organizacional compatível com suas responsabilidades institucionais, pois a Equipe de Auditoria identificou fragilidades na formalização da área, unidade, setor ou função de TIC, nas atribuições formais da área de TIC e no posicionamento organizacional da área de TIC. A deficiência de formalização contraria os critérios de definição de estruturas organizacionais e de comunicação de políticas e procedimentos, previstos no COBIT 2019, APO01.04 e APO01.09, bem como o requisito de governança efetiva da ABNT NBR ISO/IEC 38500:2025, item 5.6.1, e pode prejudicar a responsabilização e o alinhamento da TIC aos objetivos da organização. A insuficiência de atribuições formais contraria os critérios de definição de papéis e responsabilidades e de comunicação de políticas e procedimentos, previstos no COBIT 2019, APO01.05 e APO01.09, bem como o requisito de governança efetiva da ABNT NBR ISO/IEC 38500:2025, item 5.6.1, e pode favorecer atuação reativa e fragmentada por falta de clareza sobre responsabilidades de planejamento, coordenação, gestão, execução, monitoramento e controle da TIC. O posicionamento organizacional inadequado contraria o critério de aprimoramento do posicionamento da função de TI, previsto no COBIT 2019, APO01.06, e o requisito de estrutura adequada de tomada de decisão da ABNT NBR ISO/IEC 38500:2025, item 5.6.1, podendo reduzir a capacidade de influência institucional da TIC e comprometer sua participação em decisões estratégicas, orçamentárias, contratuais e de gestão de riscos.

A existência de estrutura formal de TIC é requisito básico para que a organização disponha de unidade, setor ou função institucionalmente reconhecida para planejar, coordenar, gerir, executar, monitorar e controlar o uso da tecnologia da informação. Sem essa definição, a TIC tende a operar de forma reativa, fragmentada e com baixa capacidade de responsabilização perante a alta administração.

Sob a perspectiva de governança, a estrutura de TIC deve ser compatível com o porte, a complexidade, a dependência tecnológica e as responsabilidades institucionais da organização. Essa estruturação envolve três dimensões complementares: formalização da área ou função de TIC, definição de atribuições e competências essenciais e posicionamento organizacional adequado para participar das decisões estratégicas, orçamentárias, contratuais e de gestão de riscos.

Os critérios adotados pela matriz de planejamento da Questão 1 indicam que a organização deve estabelecer estruturas organizacionais apropriadas, comunicar papéis e responsabilidades, definir políticas e procedimentos de gestão de TIC e posicionar a função de tecnologia de modo compatível com sua relevância estratégica[^explica_estrutura_tic_cobit]. Esses requisitos convergem com a ABNT NBR ISO/IEC 38500:2025, que trata da necessidade de responsabilização clara e de estruturas adequadas de tomada de decisão para a governança efetiva de TI[^explica_estrutura_tic_iso38500].

Com base na análise das respostas aos itens q0101, q0103 e q0102 do questionário aplicado e da avaliação das evidências anexadas aos itens q0101evi, q0103evi e q0102evi, conforme apontado na seção de Evidências, a Equipe de Auditoria constatou as seguintes deficiências na estrutura de TIC da organização:


* **Ausência de formalização da área, unidade, setor ou função de TIC da organização.**

* **Área de TIC sem atribuições formais suficientes para planejamento, coordenação, gestão, execução, monitoramento e controle da TIC.**

* **Posicionamento organizacional inadequado da área de TIC.**


Essas situações ensejaram o presente achado e serão detalhadas nas seções subsequentes.

[^explica_estrutura_tic_cobit]: No domínio APO01 do COBIT 2019, a gestão da estrutura organizacional, de papéis, responsabilidades, políticas e posicionamento da função de TI é tratada como condição para que a tecnologia apoie os objetivos de governança e gestão da organização.

[^explica_estrutura_tic_iso38500]: A ABNT NBR ISO/IEC 38500:2025 orienta que a governança efetiva de TI pressupõe responsabilidades claras, estrutura adequada de decisão e direção organizacional compatível com o uso atual e futuro da tecnologia.



#### Formalização da área, unidade, setor ou função de TIC

A formalização da área, unidade, setor ou função de TIC é necessária para conferir reconhecimento institucional à atividade de tecnologia da informação, definir sua vinculação na estrutura organizacional e permitir a atribuição clara de responsabilidades.

O COBIT 2019, no objetivo APO01.04, orienta que a organização defina e implemente estruturas organizacionais necessárias para apoiar os objetivos de governança e gestão de TI. De forma complementar, o APO01.09 trata da definição e comunicação de políticas e procedimentos que orientem papéis, responsabilidades e controles.

No contexto da Questão 1 da matriz de planejamento, essa formalização deve ser demonstrada por regimento, decreto, portaria, resolução, organograma, ato administrativo ou instrumento equivalente. A ausência de evidência suficiente de formalização fragiliza a identificação da unidade responsável pela coordenação da TIC e compromete a responsabilização por decisões, controles, serviços e investimentos de tecnologia.

Essa deficiência materializa o risco de inexistência de unidade ou função institucionalmente reconhecida para coordenar o uso da tecnologia da informação, prejudicando o alinhamento da TIC aos objetivos da organização.

Diante disso, [será proposta recomendação para que a organização formalize a área, unidade, setor ou função de TIC em regimento, decreto, portaria, resolução, organograma ou instrumento equivalente, compatível com seu porte, complexidade e dependência tecnológica.]{.underline}





#### Atribuições formais da área de TIC

A definição formal de atribuições da área de TIC é indispensável para delimitar responsabilidades, reduzir sobreposição ou lacunas de atuação e permitir que a gestão de tecnologia seja exercida de forma planejada e controlada.

O COBIT 2019, no objetivo APO01.05, orienta a definição, comunicação e manutenção de papéis e responsabilidades relacionados à governança e gestão de TI. Essa orientação abrange, no caso da Questão 1, atribuições essenciais como governança, planejamento, gestão, sustentação tecnológica, sistemas, segurança da informação, contratos, dados e atividades correlatas.

Quando a área de TIC existe, mas não possui atribuições formalmente definidas ou apresenta competências insuficientes para planejamento, coordenação, gestão, execução, monitoramento e controle da TIC, a organização fica exposta à atuação reativa e fragmentada, com baixa clareza sobre responsáveis por processos, serviços, riscos, contratações e controles tecnológicos.

Essa deficiência compromete a capacidade de gestão da TIC e reduz a efetividade dos demais processos de governança e gestão, pois a estrutura formal não explicita quem deve decidir, executar, acompanhar e responder pelos resultados de tecnologia da informação.

Diante disso, [será proposta recomendação para que a organização defina formalmente as atribuições da área de TIC, contemplando planejamento, coordenação, gestão, execução, monitoramento e controle da TIC.]{.underline}





#### Posicionamento organizacional da área de TIC

O posicionamento organizacional da área de TIC deve ser compatível com suas responsabilidades institucionais e com a dependência da organização em relação à tecnologia da informação. Não se trata de impor modelo único de estrutura, mas de assegurar que a função de TIC tenha capacidade de interação adequada com as instâncias decisórias responsáveis por estratégia, orçamento, contratações, riscos e prestação de serviços.

O COBIT 2019, no objetivo APO01.06, orienta o aprimoramento do posicionamento da função de TI para que a tecnologia seja tratada de modo compatível com sua relevância estratégica e com a necessidade de interação com a alta administração. A ABNT NBR ISO/IEC 38500:2025 reforça a necessidade de estrutura adequada de tomada de decisão para o uso atual e futuro da tecnologia.

Quando a área de TIC está posicionada de forma incompatível com suas atribuições, há risco de baixa capacidade de influência institucional. Essa fragilidade pode comprometer a participação da TIC em decisões estratégicas, orçamentárias, contratuais e de gestão de riscos, além de dificultar a priorização de iniciativas e a articulação com as áreas demandantes.

No âmbito da Questão 1, o posicionamento adequado deve ser demonstrado por organograma institucional, regimento interno ou documento equivalente, de modo que seja possível verificar a vinculação da área de TIC e sua compatibilidade com as responsabilidades que lhe foram atribuídas.

Diante disso, [será proposta recomendação para que a organização avalie e ajuste o posicionamento organizacional da área de TIC, de modo a permitir participação adequada em decisões estratégicas, orçamentárias, contratuais e de gestão de riscos.]{.underline}



#### Conclusão

As fragilidades identificadas na estrutura de TIC comprometem a capacidade da organização de coordenar, gerir e sustentar a tecnologia da informação de forma alinhada às necessidades institucionais. A ausência de formalização, a insuficiência de atribuições formais e o posicionamento organizacional inadequado reduzem a clareza de responsabilidades, dificultam a tomada de decisão e fragilizam o acompanhamento de riscos, serviços, contratações e iniciativas de TIC.

Diante das situações apresentadas, será sugerida proposta de encaminhamento à organização para que promova a adequação de sua estrutura de TIC, alinhando-a aos critérios de governança e gestão previstos no COBIT 2019 e na ABNT NBR ISO/IEC 38500:2025.

### Propostas de Encaminhamento

* **Comunicação com Recomendação** para que formalize a estrutura de TIC, suas atribuições e seu posicionamento organizacional.;











```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```


## Achado 2 – Governança de TIC insuficiente para avaliar, dirigir e monitorar a tecnologia da informação.

### Critérios
* COBIT 2019, EDM01.02 - Dirigir o sistema de governança: orientar estruturas, princípios, processos e práticas de governança para assegurar que a TI apoie os objetivos organizacionais;
* COBIT 2019, MEA01.04 - Avaliar o desempenho: monitorar e avaliar periodicamente o desempenho e a conformidade da TI em relação a objetivos, indicadores, metas e expectativas das partes interessadas;
* Decreto nº 12.198/2024, art. 5º - Instituição do CGD, colegiado responsável por definir diretrizes e estratégias sobre uso de recursos digitais nos órgãos e entidades da administração pública federal direta, autárquica e fundacional;
* Acórdão TCE-RJ 44.490/2024-PLEN, item II.1: necessidade de estrutura de governança de TI, especialmente Comitê de Tecnologia da Informação ou instância equivalente, com participação de áreas relevantes, responsabilidade de alinhar as ações de TI aos objetivos institucionais, priorizar investimentos e monitorar o desempenho da TI com base em indicadores e metas;
* COBIT 2019, APO01.05 - Estabelecer papéis e responsabilidades: definir, comunicar e manter papéis e responsabilidades relacionados à governança e gestão de TI.

### Evidências

* Resposta declarada no questionário iGovTI 2026 indicando não adoção das práticas avaliadas;

* Ausência de documentação comprobatória suficiente nos arquivos encaminhados pelo auditado;

* Resultado dos procedimentos de auditoria aplicáveis à questão;


### Situação encontrada



A partir da análise das informações fornecidas, verificou-se que a organização PIORCASO não demonstrou atender integralmente ao requisito de possuir mecanismos básicos de governança de TIC estabelecidos pela alta administração, incluindo modelo de governança e gestão, objetivos, indicadores, metas e Comitê de TIC ou instância equivalente formalmente instituída e atuante, pois a Equipe de Auditoria identificou fragilidades no modelo básico de governança e gestão de TIC, na instituição formal do Comitê de TIC ou instância equivalente e na atuação efetiva do Comitê de TIC ou instância equivalente. A ausência ou insuficiência de modelo básico de governança e gestão de TIC contraria os critérios de direção do sistema de governança e avaliação de desempenho, previstos no COBIT 2019, EDM01.02 e MEA01.04, bem como o Acórdão TCE-RJ 44.490/2024-PLEN, item II.1, e pode gerar baixa clareza sobre papéis, responsabilidades, objetivos, indicadores, metas e acompanhamento do desempenho da TIC. A não instituição formal do Comitê de TIC ou instância equivalente contraria o Decreto nº 12.198/2024, art. 5º, o Acórdão TCE-RJ 44.490/2024-PLEN, item II.1, e o critério de definição de papéis e responsabilidades do COBIT 2019, APO01.05, podendo impedir a existência de instância colegiada para deliberação sobre prioridades, projetos, riscos, serviços, orçamento e contratações de TIC. A ausência de evidências suficientes de atuação efetiva do Comitê de TIC ou instância equivalente contraria os critérios de avaliação de desempenho e funcionamento de estrutura colegiada de governança, previstos no COBIT 2019, MEA01.04, no Decreto nº 12.198/2024, art. 5º, e no Acórdão TCE-RJ 44.490/2024-PLEN, item II.1, podendo comprometer a deliberação efetiva sobre prioridades, projetos, riscos, serviços, orçamento e contratações de TIC.

A governança de TIC compreende o conjunto de estruturas, papéis, responsabilidades, diretrizes e mecanismos de acompanhamento por meio dos quais a alta administração avalia, dirige e monitora o uso da tecnologia da informação. Sua finalidade é assegurar que os recursos de TIC apoiem os objetivos institucionais, sejam priorizados de forma transparente e tenham desempenho acompanhado com base em critérios objetivos.

Sob a perspectiva da Questão 2 da matriz de planejamento, a existência de governança mínima exige, ao menos, que a alta administração estabeleça modelo básico de governança e gestão de TIC, com papéis, responsabilidades, objetivos, indicadores, metas ou forma de acompanhamento, e que exista Comitê de TIC ou instância equivalente formalmente instituída e atuante.

Os critérios adotados pela matriz indicam que a organização deve orientar estruturas, princípios, processos e práticas de governança, monitorar o desempenho e a conformidade da TIC, definir papéis e responsabilidades e instituir instância colegiada capaz de alinhar ações de TIC aos objetivos institucionais, priorizar investimentos e acompanhar desempenho com base em indicadores e metas[^explica_governanca_tic_cobit]. Esses requisitos também se conectam à necessidade de instância colegiada de governança digital, conforme referência do Decreto nº 12.198/2024[^explica_decreto_cgd], e ao entendimento expresso no Acórdão TCE-RJ 44.490/2024-PLEN[^explica_acordao_tcerj_governanca].

Com base na análise das respostas aos itens q1001, q1002, q1001ext[E] e q1001ext[F] do questionário aplicado e da avaliação das evidências anexadas aos itens q1001evi e q1002evi, conforme apontado na seção de Evidências, a Equipe de Auditoria constatou as seguintes deficiências na governança de TIC da organização:


* **Ausência ou insuficiência de modelo básico de governança e gestão de TIC com papéis, responsabilidades, objetivos, indicadores, metas ou acompanhamento.**

* **Comitê de TIC ou instância equivalente não instituído formalmente.**

* **Comitê de TIC ou instância equivalente sem evidências suficientes de atuação efetiva.**


Essas situações ensejaram o presente achado e serão detalhadas nas seções subsequentes.

[^explica_governanca_tic_cobit]: No COBIT 2019, o sistema de governança deve ser dirigido por estruturas, princípios, processos e práticas que assegurem que a TI apoie os objetivos organizacionais, com papéis e responsabilidades definidos e desempenho periodicamente monitorado.

[^explica_decreto_cgd]: O Decreto nº 12.198/2024 disciplina, no âmbito federal, o Comitê de Governança Digital como colegiado responsável por diretrizes e estratégias sobre o uso de recursos digitais, servindo como referência normativa para a estruturação de instâncias colegiadas de governança digital.

[^explica_acordao_tcerj_governanca]: O Acórdão TCE-RJ 44.490/2024-PLEN, item II.1, registra a necessidade de estrutura de governança de TI, especialmente Comitê de Tecnologia da Informação ou instância equivalente, com participação de áreas relevantes e atribuições de alinhamento, priorização e monitoramento.



#### Modelo básico de governança e gestão de TIC

O modelo básico de governança e gestão de TIC deve explicitar como a alta administração orienta, acompanha e responsabiliza a atuação da tecnologia da informação. Esse modelo deve conter, ao menos, diretrizes, papéis, responsabilidades, objetivos, indicadores, metas e forma de acompanhamento periódico.

O COBIT 2019, no objetivo EDM01.02, orienta a direção do sistema de governança por meio de estruturas, princípios, processos e práticas que assegurem que a TI apoie os objetivos organizacionais. Em complemento, o objetivo MEA01.04 trata do monitoramento e da avaliação periódica do desempenho e da conformidade da TI em relação a objetivos, indicadores, metas e expectativas das partes interessadas.

No contexto da Questão 2 da matriz de planejamento, a existência e a suficiência desse modelo devem ser demonstradas por políticas, diretrizes, definição de papéis e responsabilidades, objetivos, indicadores, metas, relatórios de acompanhamento, medições de desempenho ou instrumentos equivalentes.

Quando a organização não estabelece modelo básico de governança e gestão de TIC, ou quando os documentos apresentados são insuficientes para demonstrar papéis, responsabilidades, objetivos, indicadores, metas ou acompanhamento, há risco de baixa clareza sobre a direção da TIC e sobre os resultados esperados da área.

Diante disso, [será proposta recomendação para que a alta administração estabeleça modelo básico de governança e gestão de TIC, com papéis, responsabilidades, objetivos, indicadores, metas e forma de acompanhamento periódico.]{.underline}





#### Instituição formal do Comitê de TIC ou instância equivalente

O Comitê de TIC ou instância equivalente é mecanismo relevante para estruturar a participação da alta administração e das áreas interessadas nas decisões de tecnologia da informação. Sua formalização permite definir composição, competências, periodicidade mínima, forma de deliberação e responsabilidades pelo acompanhamento das decisões.

O Decreto nº 12.198/2024, art. 5º, adotado como critério de referência pela matriz, prevê colegiado responsável por definir diretrizes e estratégias sobre uso de recursos digitais no âmbito federal. O Acórdão TCE-RJ 44.490/2024-PLEN, item II.1, reforça a necessidade de estrutura de governança de TI, especialmente Comitê de Tecnologia da Informação ou instância equivalente, com participação de áreas relevantes.

Em alinhamento, o COBIT 2019, no objetivo APO01.05, orienta a definição, comunicação e manutenção de papéis e responsabilidades relacionados à governança e gestão de TI.

No contexto da Questão 2, a instituição formal do Comitê deve ser demonstrada por ato, norma, regimento, portaria ou documento equivalente que estabeleça a instância, sua composição, competências, periodicidade ou forma de deliberação.

A ausência de instituição formal do Comitê de TIC ou instância equivalente fragiliza a governança, pois pode inexistir foro institucional para deliberação sobre prioridades, projetos, riscos, serviços, orçamento e contratações de TIC.

Diante disso, [será proposta recomendação para que a organização institua formalmente Comitê de TIC ou instância equivalente, definindo composição, competências, periodicidade mínima, forma de registro das deliberações e acompanhamento dos encaminhamentos.]{.underline}





#### Atuação efetiva do Comitê de TIC ou instância equivalente

A mera instituição formal do Comitê de TIC ou instância equivalente não é suficiente para assegurar governança efetiva. É necessário que a instância funcione de modo regular, com reuniões, pautas, atas, registros de deliberação, encaminhamentos e acompanhamento das decisões tomadas.

O COBIT 2019, no objetivo MEA01.04, exige monitoramento e avaliação periódica do desempenho e da conformidade da TI. O Acórdão TCE-RJ 44.490/2024-PLEN, item II.1, também aponta a responsabilidade de alinhar as ações de TI aos objetivos institucionais, priorizar investimentos e monitorar o desempenho da TI com base em indicadores e metas.

No contexto da Questão 2, a atuação efetiva do Comitê deve ser demonstrada por atas, pautas, listas de presença, registros de deliberação, decisões, encaminhamentos ou acompanhamento de pendências. A ausência desses registros impede verificar se a instância colegiada exerce, de fato, seu papel de avaliação, direção e monitoramento da TIC.

Essa deficiência pode fazer com que decisões relevantes sobre prioridades, projetos, riscos, serviços, orçamento e contratações de TIC não sejam submetidas a deliberação colegiada ou não tenham acompanhamento formal.

Diante disso, [será proposta recomendação para que a organização assegure o funcionamento efetivo do Comitê de TIC ou instância equivalente, com reuniões periódicas, atas, deliberações, encaminhamentos e acompanhamento das decisões sobre prioridades, projetos, riscos, serviços, orçamento e contratações de TIC.]{.underline}



#### Conclusão

As fragilidades identificadas na governança de TIC comprometem a capacidade da organização de avaliar, dirigir e monitorar a tecnologia da informação de forma alinhada aos objetivos institucionais. A ausência ou insuficiência de modelo básico de governança, a inexistência formal de Comitê de TIC ou instância equivalente e a falta de evidências de atuação efetiva reduzem a clareza de responsabilidades, a qualidade da priorização e a capacidade de acompanhamento das decisões de TIC.

Diante das situações apresentadas, será sugerida proposta de encaminhamento à organização para que promova a adequação de seus mecanismos de governança de TIC, alinhando-os aos critérios previstos no COBIT 2019, no Decreto nº 12.198/2024 e no Acórdão TCE-RJ 44.490/2024-PLEN.

### Propostas de Encaminhamento

* **Comunicação com Recomendação** para que institua e mantenha modelo de governança e comitê de TIC com atuação efetiva.;











```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```


## Achado 3 – Planejamento de TIC inexistente, insuficiente, desatualizado ou desconectado da gestão, do orçamento e das contratações

### Critérios
* COBIT 2019, APO02.05 - Definir o plano e o roteiro estratégico: estabelecer plano e roteiro de TIC que traduzam a estratégia em iniciativas, prioridades, recursos, dependências, prazos e benefícios esperados;
* COBIT 2019, APO06.03 - Criar e manter orçamentos: elaborar e manter orçamento de TIC alinhado ao portfólio, ao planejamento e às prioridades aprovadas;
* Acórdão 1.411/2014-TCU-Plenário, item 9.1.6 e subitens 9.1.6.1 a 9.1.6.4: necessidade de instituir formalmente plano diretor de TI, contemplando desdobramento de diretrizes estratégicas, vinculação das ações de TI a indicadores e metas de negócio, vinculação das ações de TI a indicadores e metas de serviços ao cidadão e vinculação das ações priorizadas ao orçamento de TI;
* Acórdão TCE-RJ 44.490/2024-PLEN, item II.3 e subitens II.3.1 a II.3.5: necessidade de estabelecer processo estruturado, com participação de representantes das principais secretarias, para elaborar, manter e revisar periodicamente o PDTI, contemplando objetivos, indicadores e metas de TI alinhados aos objetivos de negócio, riscos que possam impactar objetivos e metas, projetos, aquisições e ações necessárias, alocação de recursos e ações de divulgação e monitoramento do PDTI após aprovação pela autoridade máxima.

### Evidências

* Resposta declarada no questionário iGovTI 2026 indicando não adoção das práticas avaliadas;

* Ausência de documentação comprobatória suficiente nos arquivos encaminhados pelo auditado;

* Resultado dos procedimentos de auditoria aplicáveis à questão;


### Situação encontrada





A partir da análise das informações fornecidas, verificou-se que a organização PIORCASO não demonstrou utilizar o planejamento de TIC como instrumento efetivo de gestão, com processo formal, plano vigente, aprovação competente, alinhamento institucional, integração com orçamento e contratações e acompanhamento periódico, pois a Equipe de Auditoria identificou fragilidades nos seguintes aspectos: processo formal de planejamento de TIC; aprovação formal do plano de TIC; alinhamento do plano ao planejamento institucional; integração com orçamento, plano de contratações, projetos ou contratações de TIC; acompanhamento, revisão ou atualização periódica do plano de TIC;. A inexistência ou fragilidade do processo formal contraria os critérios de planejamento estratégico de TIC previstos no COBIT 2019, APO02.05, no Acórdão 1.411/2014-TCU-Plenário e no Acórdão TCE-RJ 44.490/2024-PLEN, podendo levar à atuação reativa e sem critérios objetivos de seleção e priorização de iniciativas. A ausência de aprovação formal do plano de TIC contraria os critérios de formalização e aprovação do planejamento de TIC e reduz sua legitimidade institucional para orientar a gestão, os projetos, o orçamento e as contratações. A falta de alinhamento ao planejamento institucional contraria os critérios que exigem desdobramento de diretrizes estratégicas e vinculação das ações de TIC aos objetivos de negócio, podendo resultar em iniciativas de baixo valor para a organização. A ausência de integração com orçamento, plano de contratações, projetos ou contratações contraria o COBIT 2019, APO06.03, o Acórdão 1.411/2014-TCU-Plenário e o Acórdão TCE-RJ 44.490/2024-PLEN, podendo gerar aquisições reativas, não priorizadas ou desalinhadas. A ausência de acompanhamento, revisão ou atualização periódica contraria os critérios de manutenção e monitoramento do PDTI, podendo manter metas, iniciativas e prioridades incompatíveis com mudanças institucionais, orçamentárias ou tecnológicas.

O planejamento de TIC é instrumento fundamental para traduzir diretrizes institucionais em iniciativas, prioridades, recursos, prazos, responsáveis e resultados esperados. Sua ausência ou fragilidade reduz a capacidade da organização de direcionar investimentos, selecionar demandas, coordenar projetos e alinhar contratações às necessidades institucionais.

Sob a perspectiva da Questão 3 da matriz de planejamento, a organização deve executar processo formal de planejamento, contar com plano de TIC formalmente aprovado, assegurar participação das áreas demandantes, alinhar o plano ao planejamento institucional, integrá-lo ao orçamento e às contratações e acompanhá-lo periodicamente.

Os critérios adotados pela matriz indicam que o planejamento de TIC deve estabelecer plano e roteiro estratégico, manter orçamento alinhado ao portfólio e às prioridades aprovadas, vincular ações de TIC a indicadores, metas e orçamento e contemplar processo estruturado de elaboração, manutenção e revisão periódica do PDTI[^explica_planejamento_tic].

Com base na análise das respostas aos itens q2101, q2101ext[A], q2102, q2102ext[A], q2102ext[C], q2102ext[D], q2102ext[E], q2802ext[C], q2802ext[D] e q2804[B] do questionário aplicado e da avaliação das evidências anexadas aos itens q2101evi, q2102evi e q2802evi, conforme apontado na seção de Evidências, a Equipe de Auditoria constatou as seguintes deficiências no planejamento de TIC da organização:


* **Inexistência ou fragilidade do processo formal de planejamento de TIC.**

* **Ausência de aprovação formal do plano de TIC.**

* **Plano de TIC sem alinhamento adequado ao planejamento institucional.**

* **Plano de TIC sem integração adequada com orçamento, plano de contratações, projetos ou contratações de TIC.**

* **Ausência de acompanhamento, revisão ou atualização periódica do plano de TIC.**


Essas situações ensejaram o presente achado e serão detalhadas nas seções subsequentes.

[^explica_planejamento_tic]: Os critérios de planejamento de TIC adotados pela matriz convergem para a necessidade de plano formal, aprovado, vigente, alinhado à estratégia institucional, integrado ao orçamento e às contratações e acompanhado periodicamente.



#### Processo formal de planejamento de TIC

O processo formal de planejamento de TIC deve definir etapas, responsáveis, participação das áreas demandantes e critérios mínimos de priorização. Esse processo é necessário para que o planejamento deixe de ser uma atividade eventual e passe a constituir rotina institucional de identificação, seleção, priorização e acompanhamento de demandas de tecnologia.

O COBIT 2019, no objetivo APO02.05, orienta a definição de plano e roteiro estratégico de TIC que traduzam a estratégia em iniciativas, prioridades, recursos, dependências, prazos e benefícios esperados. O Acórdão TCE-RJ 44.490/2024-PLEN, item II.3, também aponta a necessidade de processo estruturado, com participação de representantes das principais secretarias, para elaborar, manter e revisar periodicamente o PDTI.

No contexto da Questão 3, o processo deve ser demonstrado por norma, procedimento, guia ou instrumento equivalente que discipline a elaboração, revisão, aprovação e acompanhamento do planejamento de TIC.

A inexistência ou fragilidade desse processo expõe a organização à atuação reativa, sem critérios objetivos de seleção e priorização de iniciativas.

Diante disso, [será proposta recomendação para que a organização institua processo formal de planejamento de TIC, com etapas, responsáveis, participação das áreas demandantes e critérios mínimos de priorização.]{.underline}





#### Aprovação formal do plano de TIC

O plano de TIC deve ser formalmente aprovado pelo dirigente máximo da organização ou por dirigente ou colegiado integrante da alta administração, de modo a conferir legitimidade institucional ao instrumento.

O Acórdão 1.411/2014-TCU-Plenário e o Acórdão TCE-RJ 44.490/2024-PLEN reforçam a necessidade de plano diretor ou instrumento equivalente formalmente instituído e aprovado, capaz de orientar as ações de TIC.

No contexto da Questão 3, a aprovação deve ser demonstrada por ato formal da instância competente ou por registro equivalente que identifique o plano aprovado, a autoridade responsável e a data da deliberação.

Sem aprovação formal, o plano pode não representar decisão institucional válida nem possuir autoridade suficiente para orientar a gestão, os projetos, o orçamento e as contratações de TIC.

Diante disso, [será proposta recomendação para que a organização submeta o plano de TIC à aprovação formal do dirigente máximo ou de dirigente ou colegiado integrante da alta administração, mantendo registro do respectivo ato de aprovação.]{.underline}





#### Alinhamento ao planejamento institucional

O plano de TIC deve demonstrar como suas iniciativas apoiam os objetivos institucionais, as diretrizes superiores e as necessidades das áreas finalísticas e administrativas.

O Acórdão 1.411/2014-TCU-Plenário exige o desdobramento de diretrizes estratégicas e a vinculação das ações de TI a indicadores e metas de negócio. O Acórdão TCE-RJ 44.490/2024-PLEN também prevê objetivos, indicadores e metas de TI alinhados aos objetivos de negócio.

Quando o plano de TIC não explicita esse alinhamento, há risco de execução de iniciativas tecnológicas com baixo valor institucional, desconectadas das prioridades da organização e das necessidades dos usuários internos e externos.

Diante disso, [será proposta recomendação para que a organização revise o plano de TIC para explicitar seu alinhamento ao planejamento institucional, às diretrizes superiores e às necessidades das áreas finalísticas e administrativas.]{.underline}





#### Integração com orçamento, plano de contratações e contratações de TIC

O planejamento de TIC deve ser integrado à proposta orçamentária, ao plano de contratações, aos projetos e às contratações executadas. Essa integração é necessária para que as iniciativas priorizadas tenham suporte financeiro, sejam convertidas em contratações coerentes e possam ser acompanhadas ao longo da execução.

O COBIT 2019, APO06.03, orienta a criação e manutenção de orçamento de TIC alinhado ao portfólio, ao planejamento e às prioridades aprovadas. O Acórdão 1.411/2014-TCU-Plenário também exige vinculação das ações priorizadas ao orçamento de TI, e o Acórdão TCE-RJ 44.490/2024-PLEN prevê projetos, aquisições, ações necessárias e alocação de recursos no PDTI.

A ausência de integração entre planejamento, orçamento e contratações aumenta o risco de aquisições reativas, não priorizadas ou desalinhadas às necessidades institucionais.

Diante disso, [será proposta recomendação para que a organização vincule o plano de TIC à proposta orçamentária, ao plano de contratações e às contratações de TIC executadas, priorizando demandas conforme relevância, risco e capacidade de execução.]{.underline}





#### Acompanhamento, revisão e atualização do plano de TIC

O plano de TIC deve ser acompanhado, revisto e atualizado periodicamente ou diante de mudanças relevantes, com registro de execução, pendências, reprogramações e deliberações. Essa rotina permite verificar o andamento das iniciativas, ajustar prioridades e manter o plano compatível com mudanças institucionais, orçamentárias ou tecnológicas.

O Acórdão TCE-RJ 44.490/2024-PLEN prevê a manutenção e revisão periódica do PDTI, bem como ações de divulgação e monitoramento após sua aprovação pela autoridade máxima.

Quando não há acompanhamento, revisão ou atualização periódica, metas e iniciativas podem permanecer desatualizadas, inviáveis ou incompatíveis com as necessidades atuais da organização.

Diante disso, [será proposta recomendação para que a organização estabeleça rotina de acompanhamento, revisão e atualização do plano de TIC, com registro de execução, pendências, reprogramações e deliberações.]{.underline}



#### Conclusão

As fragilidades identificadas no planejamento de TIC comprometem a capacidade da organização de direcionar iniciativas, priorizar recursos, alinhar projetos às necessidades institucionais e integrar orçamento e contratações à estratégia de tecnologia.

Diante das situações apresentadas, será sugerida proposta de encaminhamento à organização para que promova a adequação de seu processo e de seu plano de TIC, alinhando-os aos critérios previstos no COBIT 2019, no Acórdão 1.411/2014-TCU-Plenário e no Acórdão TCE-RJ 44.490/2024-PLEN.

### Propostas de Encaminhamento

* **Comunicação com Recomendação** para que formalize, aprove, execute e acompanhe plano de TIC alinhado à estratégia, ao orçamento e às contratações.;











```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```


## Achado 4 – Capacidade institucional insuficiente para sustentar a gestão de TIC e segurança da informação

### Critérios
* COBIT 2019, APO01.05 - Estabelecer papéis e responsabilidades: definir, comunicar e manter papéis e responsabilidades relacionados à governança e gestão de TIC;
* COBIT 2019, APO07.01 - Adquirir e manter pessoal adequado e apropriado: assegurar quantidade e perfil de profissionais compatíveis com as necessidades de TIC;
* COBIT 2019, APO07.02 - Identificar pessoal-chave de TI: identificar funções e pessoas críticas para reduzir dependência individual, perda de conhecimento e descontinuidade;
* COBIT 2019, APO07.03 - Manter habilidades e competências do pessoal: identificar, desenvolver e manter competências necessárias à execução das responsabilidades de TIC;
* COBIT 2019, APO07.05 - Planejar e monitorar o uso de recursos humanos de TI e de negócio: planejar, alocar e acompanhar capacidade de pessoal para iniciativas, operações e serviços de TIC;
* COBIT 2019, APO07.06 - Gerenciar pessoal contratado: controlar o uso de pessoal terceirizado ou externo, preservando responsabilização, supervisão e retenção de conhecimento;
* COBIT 2019, APO10.04 - Gerenciar risco de fornecedores: identificar e tratar riscos decorrentes de fornecedores, contratos e dependências externas relevantes para TIC;
* COBIT 2019, DSS01.02 - Gerenciar serviços de TI terceirizados: assegurar que serviços terceirizados sejam supervisionados, medidos e integrados aos controles da organização;
* ABNT NBR ISO/IEC 27001:2022, cláusulas 5.3 e 7.2: definir responsabilidades e autoridades para segurança da informação e assegurar competências necessárias às funções atribuídas;
* ABNT NBR ISO/IEC 27002:2022, controles 5.2 e 6.3: definir papéis e responsabilidades de segurança da informação e promover conscientização, educação e treinamento em segurança.

### Evidências

* Resposta declarada no questionário iGovTI 2026 indicando não adoção das práticas avaliadas;

* Ausência de documentação comprobatória suficiente nos arquivos encaminhados pelo auditado;

* Resultado dos procedimentos de auditoria aplicáveis à questão;


### Situação encontrada






A partir da análise das informações fornecidas, verificou-se que a organização PIORCASO não demonstrou dispor de capacidade institucional mínima, em termos de força de trabalho, perfis profissionais, competências, funções e vínculos, para planejar, gerir, proteger, contratar, fiscalizar e sustentar a TIC e a segurança da informação de forma adequada às suas necessidades institucionais, pois a Equipe de Auditoria identificou fragilidades nos seguintes aspectos: força de trabalho mínima dedicada à TIC ou à segurança da informação; definição do quantitativo necessário de pessoal; cargos, funções, perfis ou ocupações específicas; perfis profissionais e sua utilização na escolha de gestores; identificação e tratamento de lacunas de competências; capacidade interna mínima diante de modelo terceirizado ou externo;. A ausência de força de trabalho mínima contraria os critérios de pessoal adequado, planejamento de recursos humanos e competências em segurança da informação, previstos no COBIT 2019, APO07.01 e APO07.05, e na ABNT NBR ISO/IEC 27001:2022, cláusulas 5.3 e 7.2, podendo inviabilizar o planejamento, a gestão, a proteção, a contratação, a fiscalização e a sustentação da TIC. A ausência de definição do quantitativo necessário contraria os critérios de aquisição, manutenção, planejamento e monitoramento de pessoal de TIC, podendo causar subdimensionamento ou alocação inadequada da equipe. A ausência de cargos, funções, perfis ou ocupações específicas contraria os critérios de papéis, responsabilidades, pessoal adequado e identificação de pessoal-chave, podendo reduzir a capacidade de atração, alocação, responsabilização e retenção de profissionais. A inexistência, insuficiência ou não utilização de perfis profissionais contraria os critérios de definição de papéis, manutenção de competências e responsabilidades de segurança da informação, podendo levar à designação de gestores e colaboradores sem competências compatíveis com suas responsabilidades. A ausência de identificação ou tratamento de lacunas de competências contraria os critérios de manutenção de habilidades e competências, responsabilidades de segurança da informação e educação e treinamento, podendo comprometer a execução de práticas mínimas de planejamento, gestão, segurança, contratação, fiscalização e sustentação de TIC. A dependência de terceiros sem capacidade interna mínima contraria os critérios de gestão de pessoal contratado, risco de fornecedores e serviços terceirizados de TI, podendo gerar perda de conhecimento, baixa governabilidade e risco de descontinuidade dos serviços.

A capacidade institucional de TIC e segurança da informação envolve a existência de pessoas, competências, perfis, funções e vínculos suficientes para sustentar atividades críticas de planejamento, gestão, proteção, contratação, fiscalização e operação. A mera existência formal de área de TIC não é suficiente quando a organização não dispõe de capacidade mínima para coordenar e supervisionar suas responsabilidades.

Sob a perspectiva da Questão 4 da matriz de planejamento, a organização deve conhecer sua força de trabalho, definir o quantitativo necessário, possuir cargos ou funções compatíveis, estabelecer perfis profissionais, identificar e tratar lacunas de competências e manter capacidade interna mínima mesmo quando utiliza terceiros ou estrutura externa.

Os critérios adotados pela matriz indicam que a organização deve definir papéis e responsabilidades, assegurar quantidade e perfil adequados de pessoal, identificar pessoal-chave, manter habilidades e competências, planejar recursos humanos, controlar pessoal contratado e tratar riscos decorrentes de fornecedores e dependências externas[^explica_capacidade_tic].

Com base na análise das respostas aos itens q0101, q0105, q2701, q2702, q2703, q2704, q2705, q2706, q2708, q2801 e q2804 do questionário aplicado e da avaliação das evidências anexadas aos itens q2701evi, q2702evi, q2703evi, q2704evi, q2705evi, q2706evi, q2801evi e q2804eviA, conforme apontado na seção de Evidências, a Equipe de Auditoria constatou as seguintes deficiências na capacidade institucional de TIC e segurança da informação:


* **Ausência de força de trabalho mínima dedicada à TIC ou à segurança da informação.**

* **A organização não definiu o quantitativo necessário de pessoal de TIC e segurança da informação.**

* **Ausência de cargos, funções, perfis ou ocupações específicas de TIC e segurança da informação.**

* **Perfis profissionais de TIC e segurança da informação inexistentes, insuficientes ou não utilizados na escolha de gestores.**

* **Lacunas de competências dos colaboradores e gestores de TIC e segurança da informação não são identificadas ou tratadas.**

* **Modelo de operação de TIC predominantemente terceirizado ou externo, sem capacidade interna mínima declarada para coordenação, planejamento, aprovação técnica ou fiscalização das atividades críticas de TIC.**


Essas situações ensejaram o presente achado e serão detalhadas nas seções subsequentes.

[^explica_capacidade_tic]: Os critérios de capacidade institucional de TIC e segurança da informação adotados pela matriz concentram-se em pessoal adequado, competências, papéis, responsabilidades, retenção de conhecimento e supervisão de terceiros.



#### Força de trabalho mínima dedicada à TIC ou à segurança da informação

A organização deve dispor de força de trabalho mínima dedicada à TIC e à segurança da informação, compatível com sua estrutura, porte, serviços prestados, sistemas mantidos, contratações e riscos relevantes.

O COBIT 2019, APO07.01 e APO07.05, orienta a manutenção de pessoal adequado e o planejamento e monitoramento da capacidade de recursos humanos. A ABNT NBR ISO/IEC 27001:2022, cláusulas 5.3 e 7.2, exige responsabilidades definidas e competências necessárias às funções atribuídas em segurança da informação.

A ausência de profissionais dedicados, ou quantitativo incompatível com a estrutura declarada, pode impedir a execução mínima de atividades de planejamento, gestão, proteção, contratação, fiscalização e sustentação da TIC.

Diante disso, [será proposta recomendação para que a organização avalie sua força de trabalho dedicada à TIC e à segurança da informação e adote medidas proporcionais para assegurar capacidade mínima de planejamento, gestão, proteção, contratação, fiscalização e sustentação da TIC.]{.underline}





#### Quantitativo necessário de pessoal de TIC e segurança da informação

A definição do quantitativo necessário de pessoal permite avaliar se a força de trabalho disponível é compatível com as demandas, riscos e responsabilidades da organização.

O COBIT 2019, APO07.01 e APO07.05, exige que a organização assegure quantidade e perfil de profissionais compatíveis com as necessidades de TIC e planeje a alocação de recursos humanos para iniciativas, operações e serviços.

Sem estimativa do quantitativo mínimo necessário, a organização fica sem base objetiva para dimensionamento, alocação, contratação, capacitação ou compartilhamento de estrutura.

Diante disso, [será proposta recomendação para que a organização estime o quantitativo mínimo necessário de pessoal de TIC e segurança da informação, considerando porte, complexidade, serviços críticos, sistemas mantidos, contratações e riscos relevantes.]{.underline}





#### Cargos, funções, perfis ou ocupações específicas de TIC e segurança da informação

Cargos, funções, gratificações, perfis ou ocupações específicas de TIC e segurança da informação ajudam a estruturar responsabilidades, atrair profissionais, definir requisitos mínimos e reduzir improvisação na alocação de pessoas.

O COBIT 2019, APO01.05, APO07.01 e APO07.02, orienta a definição de papéis e responsabilidades, a manutenção de pessoal adequado e a identificação de funções críticas de TI.

A ausência desses instrumentos pode reduzir a capacidade de atração, alocação, responsabilização e retenção de profissionais com perfil compatível com as necessidades institucionais.

Diante disso, [será proposta recomendação para que a organização avalie a necessidade de instituir cargos, funções, gratificações, perfis ou ocupações específicas de TIC e segurança da informação, compatíveis com suas necessidades institucionais.]{.underline}





#### Perfis profissionais de TIC e segurança da informação

A definição de perfis profissionais mínimos para gestores e colaboradores de TIC e segurança da informação é necessária para que as pessoas designadas possuam competências compatíveis com suas responsabilidades.

O COBIT 2019, APO01.05 e APO07.03, orienta a definição de papéis, responsabilidades e competências necessárias. A ABNT NBR ISO/IEC 27001:2022 também exige competências adequadas às funções atribuídas em segurança da informação.

Quando perfis profissionais são inexistentes, insuficientes ou não utilizados na escolha de gestores, aumenta o risco de designação de responsáveis sem qualificação compatível com atividades críticas de TIC e segurança da informação.

Diante disso, [será proposta recomendação para que a organização defina perfis profissionais mínimos para gestores e colaboradores de TIC e segurança da informação e utilize esses perfis como referência para designação de responsáveis.]{.underline}





#### Identificação e tratamento de lacunas de competências

A organização deve identificar periodicamente lacunas de competências dos gestores e colaboradores de TIC e segurança da informação e definir medidas de tratamento, como capacitação, realocação, provimento, apoio especializado, compartilhamento de estrutura ou contratação com transferência de conhecimento.

O COBIT 2019, APO07.03, orienta a manutenção de habilidades e competências necessárias à execução das responsabilidades de TIC. A ABNT NBR ISO/IEC 27002:2022, controles 5.2 e 6.3, reforça a definição de responsabilidades e a promoção de conscientização, educação e treinamento em segurança.

Sem diagnóstico e tratamento de lacunas, a organização pode não possuir competências suficientes para executar práticas mínimas de planejamento, gestão, segurança, contratação, fiscalização e sustentação de TIC.

Diante disso, [será proposta recomendação para que a organização realize diagnóstico periódico de lacunas de competências e estabeleça plano de tratamento, contemplando capacitação, realocação, provimento, apoio especializado, compartilhamento de estrutura ou contratação com transferência de conhecimento.]{.underline}





#### Capacidade interna mínima em modelo terceirizado ou externo

A utilização de terceiros ou de estrutura externa para execução de atividades de TIC não elimina a responsabilidade da organização pela coordenação, planejamento, aprovação técnica, fiscalização, tomada de decisão e retenção de conhecimento.

O COBIT 2019, APO07.06, APO10.04 e DSS01.02, orienta o controle de pessoal contratado, a gestão de riscos de fornecedores e a supervisão de serviços terceirizados de TI, preservando responsabilização, medição, integração aos controles e retenção de conhecimento.

Quando o modelo de operação é predominantemente terceirizado ou externo sem capacidade interna mínima declarada, a organização fica exposta à perda de conhecimento, baixa governabilidade, dependência excessiva e risco de descontinuidade dos serviços.

Diante disso, [será proposta recomendação para que a organização avalie seu modelo de operação de TIC e adote medidas para assegurar capacidade interna mínima de coordenação, planejamento, aprovação técnica, fiscalização contratual, tomada de decisão e retenção de conhecimento, especialmente quando a execução das atividades de TIC depender predominantemente de terceiros ou de estrutura externa.]{.underline}



#### Conclusão

As fragilidades identificadas na capacidade institucional de TIC e segurança da informação comprometem a sustentabilidade da gestão, da proteção, das contratações, da fiscalização e da continuidade dos serviços tecnológicos da organização.

Diante das situações apresentadas, será sugerida proposta de encaminhamento à organização para que promova a adequação de sua capacidade institucional de TIC e segurança da informação, alinhando-a aos critérios previstos no COBIT 2019 e nas normas ABNT NBR ISO/IEC 27001:2022 e ABNT NBR ISO/IEC 27002:2022.

### Propostas de Encaminhamento

* **Comunicação com Recomendação** para que dimensione e desenvolva capacidade institucional mínima de TIC e segurança da informação.;











```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```


## Achado 5 – Gestão de serviços de TIC incipiente, sem controle mínimo sobre serviços, ativos e incidentes

### Critérios
* ITIL 4, prática de gerenciamento do catálogo de serviços: manter fonte única de informações consistentes sobre serviços e ofertas de serviço, disponível para usuários e equipes de suporte;
* COBIT 2019, APO09.02 - Catalogar serviços facilitados por TI: definir, manter e comunicar catálogo de serviços, incluindo serviços prestados, características, requisitos e níveis de serviço esperados;
* ITIL 4, prática de gerenciamento de nível de serviço: definir, acordar, monitorar, avaliar e reportar metas e níveis de serviço alinhados às necessidades das áreas usuárias;
* ITIL 4, prática de gerenciamento de ativos de TI: planejar e gerenciar o ciclo de vida dos ativos de TI, mantendo informações suficientes para apoiar controle, custo, risco, valor e tomada de decisão;
* ITIL 4, prática de gerenciamento de configuração de serviço: assegurar informações precisas e confiáveis sobre itens de configuração e seus relacionamentos com serviços, sistemas e infraestrutura;
* COBIT 2019, BAI10.01 - Estabelecer e manter um modelo de configuração: definir escopo, granularidade, atributos, relacionamentos e responsáveis pela base de configuração;
* ITIL 4, prática de gerenciamento de incidentes: minimizar o impacto negativo dos incidentes por meio da restauração tempestiva da operação normal dos serviços e do registro rastreável do tratamento realizado;
* COBIT 2019, DSS02.02, DSS02.04 e DSS02.07 - Requisições de serviço e incidentes gerenciados: registrar, classificar, priorizar, investigar, diagnosticar, resolver, acompanhar e reportar incidentes e requisições de serviço.

### Evidências

* Resposta declarada no questionário iGovTI 2026 indicando não adoção das práticas avaliadas;

* Ausência de documentação comprobatória suficiente nos arquivos encaminhados pelo auditado;

* Resultado dos procedimentos de auditoria aplicáveis à questão;


### Situação encontrada





A partir da análise das informações fornecidas, verificou-se que a organização PIORCASO não demonstrou adotar práticas mínimas de gestão de serviços de TIC, incluindo catálogo de serviços, níveis de serviço, inventário de ativos, gestão de configuração e tratamento de incidentes, de modo a assegurar eficiência, continuidade, rastreabilidade e qualidade dos serviços prestados, pois a Equipe de Auditoria identificou fragilidades nos seguintes aspectos: catálogo de serviços de TIC; ANS, metas mínimas ou monitoramento de níveis de serviço; inventário de ativos de TIC; gestão de configuração; gestão de incidentes de TIC;. A fragilidade no catálogo de serviços contraria a ITIL 4 e o COBIT 2019, APO09.02, podendo gerar prestação reativa e pouco transparente de serviços de TIC. A ausência de ANS, metas mínimas ou monitoramento de níveis de serviço contraria os critérios de catálogo e gerenciamento de nível de serviço, podendo impedir avaliação objetiva de desempenho e qualidade dos serviços. A inexistência ou fragilidade do inventário de ativos contraria a ITIL 4, prática de gerenciamento de ativos de TI, e a prática de gerenciamento de configuração, podendo reduzir o controle sobre recursos tecnológicos, custos, riscos e tomada de decisão. A ausência ou fragilidade da gestão de configuração contraria a ITIL 4 e o COBIT 2019, BAI10.01, podendo prejudicar a confiabilidade das informações sobre itens de configuração e seus relacionamentos com serviços, sistemas e infraestrutura. A inexistência ou fragilidade da gestão de incidentes contraria a ITIL 4 e o COBIT 2019, DSS02.02, DSS02.04 e DSS02.07, podendo comprometer o tratamento padronizado, tempestivo e rastreável dos incidentes de TIC.

A gestão de serviços de TIC organiza a forma como a tecnologia é entregue aos usuários e às áreas demandantes. Catálogo de serviços, níveis de serviço, inventário de ativos, gestão de configuração e gestão de incidentes constituem práticas mínimas para assegurar transparência, continuidade, qualidade, rastreabilidade e controle operacional.

Sob a perspectiva da Questão 5 da matriz de planejamento, a organização deve manter catálogo de serviços formalmente instituído, atualizado e acessível, definir e monitorar níveis de serviço, manter inventário de ativos de TIC, possuir processo de gestão de configuração e tratar incidentes de forma sistemática e rastreável.

Os critérios adotados pela matriz indicam que a organização deve manter fonte única e consistente de informações sobre serviços, definir níveis de serviço, gerenciar ativos e configurações e registrar, classificar, priorizar, resolver, acompanhar e reportar incidentes e requisições de serviço[^explica_gestao_servicos_tic].

Com base na análise das respostas aos itens q2201, q2201ext[A], q2201ext[B], q2201ext[C], q2201ext[D], q2201ext[E], q2203, q2203ext[A], q2203ext[B], q2203ext[C], q2204, q2204ext[A], q2204ext[B], q2204ext[C], q2204ext[D], q2204ext[E], q2204ext[F], q2501 e q2504 do questionário aplicado e da avaliação das evidências anexadas aos itens q2201evi, q2203evi, q2204evi, q2501evi e q2504evi, conforme apontado na seção de Evidências, a Equipe de Auditoria constatou as seguintes deficiências na gestão de serviços de TIC:


* **Inexistência, desatualização, indisponibilidade ou insuficiência do catálogo de serviços de TIC.**

* **Inexistência de ANS, metas mínimas ou monitoramento de níveis de serviço para os principais serviços de TIC.**

* **Inexistência ou fragilidade do inventário de ativos de TIC.**

* **Ausência ou fragilidade do processo de gestão de configuração.**

* **Inexistência ou fragilidade do processo de gestão de incidentes de TIC.**


Essas situações ensejaram o presente achado e serão detalhadas nas seções subsequentes.

[^explica_gestao_servicos_tic]: As práticas de gestão de serviços de TIC adotadas como critério pela matriz baseiam-se em ITIL 4 e COBIT 2019 e abrangem catálogo, níveis de serviço, ativos, configuração e incidentes.



#### Catálogo de serviços de TIC

O catálogo de serviços de TIC deve constituir fonte única de informações consistentes sobre os serviços prestados, acessível aos usuários e às áreas demandantes. Deve conter informações mínimas sobre os serviços efetivamente prestados, suas características, requisitos, canais de atendimento e níveis esperados de serviço.

A ITIL 4, na prática de gerenciamento do catálogo de serviços, orienta a manutenção de informações consistentes e disponíveis sobre serviços e ofertas de serviço. O COBIT 2019, APO09.02, exige a definição, manutenção e comunicação do catálogo de serviços facilitados por TI.

A inexistência, desatualização, indisponibilidade ou insuficiência do catálogo pode gerar prestação reativa, pouco transparente e sem definição clara dos serviços de TIC disponíveis.

Diante disso, [será proposta recomendação para que a organização institua e mantenha atualizado catálogo de serviços de TIC, acessível aos usuários e áreas demandantes, com informações mínimas sobre os serviços efetivamente prestados.]{.underline}





#### Níveis de serviço e metas de atendimento

A definição de Acordos de Níveis de Serviço, metas mínimas ou parâmetros equivalentes permite pactuar expectativas, medir desempenho e avaliar a qualidade dos principais serviços de TIC.

A ITIL 4, na prática de gerenciamento de nível de serviço, orienta a definição, monitoramento, avaliação e reporte de metas e níveis de serviço alinhados às necessidades das áreas usuárias. O COBIT 2019, APO09.02, também relaciona o catálogo à comunicação de requisitos e níveis de serviço esperados.

Sem ANS, metas mínimas ou monitoramento, a organização não dispõe de parâmetros objetivos para avaliar desempenho, tempestividade e qualidade dos serviços prestados.

Diante disso, [será proposta recomendação para que a organização defina e monitore níveis mínimos de serviço ou metas de atendimento para os serviços de TIC mais relevantes.]{.underline}





#### Inventário de ativos de TIC

O inventário de ativos de TIC deve permitir conhecer e controlar equipamentos, servidores, sistemas, *softwares*, licenças, serviços em nuvem, responsáveis e componentes de infraestrutura.

A ITIL 4, na prática de gerenciamento de ativos de TI, orienta o gerenciamento do ciclo de vida dos ativos, mantendo informações suficientes para apoiar controle, custo, risco, valor e tomada de decisão.

A inexistência ou fragilidade do inventário reduz a visibilidade sobre os recursos tecnológicos e compromete controles de segurança, gestão de custos, planejamento de capacidade, gestão de configuração e resposta a incidentes.

Diante disso, [será proposta recomendação para que a organização mantenha inventário atualizado de ativos de TIC, contemplando ao menos equipamentos, servidores, sistemas, softwares, licenças, serviços em nuvem, responsáveis e componentes de infraestrutura.]{.underline}





#### Gestão de configuração

A gestão de configuração deve manter informações precisas e confiáveis sobre itens de configuração relevantes, seus atributos, responsáveis e relacionamentos com ativos, sistemas, infraestrutura e serviços.

A ITIL 4, na prática de gerenciamento de configuração de serviço, orienta assegurar informações confiáveis sobre itens de configuração e seus relacionamentos. O COBIT 2019, BAI10.01, exige a definição de escopo, granularidade, atributos, relacionamentos e responsáveis pela base de configuração.

Sem processo mínimo de gestão de configuração, a organização perde capacidade de compreender dependências entre ativos e serviços, planejar mudanças, avaliar impactos e manter registros atualizados.

Diante disso, [será proposta recomendação para que a organização formalize e execute processo mínimo de gestão de configuração, mantendo base, ferramenta ou registro equivalente com itens de configuração relevantes, relacionamentos entre ativos, sistemas, infraestrutura e serviços, responsáveis, atualização periódica e uso das informações no planejamento e acompanhamento de mudanças.]{.underline}





#### Gestão de incidentes de TIC

A gestão de incidentes de TIC deve definir papéis, responsabilidades, critérios de priorização, escalamento, tratamento, registro sistemático, histórico das ocorrências e análise posterior de incidentes relevantes ou recorrentes.

A ITIL 4, na prática de gerenciamento de incidentes, orienta minimizar impactos negativos por meio da restauração tempestiva da operação normal e do registro rastreável do tratamento realizado. O COBIT 2019, DSS02.02, DSS02.04 e DSS02.07, exige registrar, classificar, priorizar, investigar, diagnosticar, resolver, acompanhar e reportar incidentes e requisições de serviço.

Quando o processo de gestão de incidentes é inexistente ou frágil, incidentes podem ser tratados de forma improvisada, sem rastreabilidade, histórico, priorização, escalamento ou análise de recorrência.

Diante disso, [será proposta recomendação para que a organização formalize e execute processo mínimo de gestão de incidentes de TIC, contemplando papéis, responsabilidades, critérios de priorização, escalamento, tratamento de incidentes de serviços e de segurança da informação, registro sistemático em ferramenta, sistema, planilha ou base equivalente, histórico das ocorrências e análise posterior de incidentes relevantes ou recorrentes.]{.underline}



#### Conclusão

As fragilidades identificadas na gestão de serviços de TIC comprometem a eficiência, a continuidade, a rastreabilidade e a qualidade dos serviços prestados, além de reduzirem o controle da organização sobre seus ativos, configurações e incidentes.

Diante das situações apresentadas, será sugerida proposta de encaminhamento à organização para que promova a adequação de suas práticas mínimas de gestão de serviços de TIC, alinhando-as aos critérios de ITIL 4 e COBIT 2019.

### Propostas de Encaminhamento

* **Comunicação com Recomendação** para que implemente processos mínimos de gestão de serviços, ativos, configuração e incidentes de TIC.;











```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```


## Achado 6 – Contratações de TIC sem governança técnica e controle de resultados

### Critérios
* Art. 11, parágrafo único, da Lei 14.133/2021: responsabilidade da alta administração pela governança das contratações, com processos, estruturas, gestão de riscos e controles internos;
* Art. 18, caput e §1º, incisos I, IV, V, VIII, IX, X e XIII, da Lei 14.133/2021: fase preparatória caracterizada pelo planejamento, compatibilização com o plano de contratações anual e elementos mínimos do estudo técnico preliminar;
* Art. 6º, inciso XXIII, alíneas "d", "e", "f" e "g", da Lei 14.133/2021: termo de referência deve conter requisitos da contratação, modelo de execução, modelo de gestão contratual e critérios de medição e pagamento;
* Art. 19, inciso IV, da Lei 14.133/2021: instituição de modelos de minutas de editais, termos de referência, contratos padronizados e demais documentos;
* Art. 7º, caput, incisos I a III e §1º, da Lei 14.133/2021: designação de agentes públicos para funções essenciais, observados atribuições, formação, segregação de funções e inexistência de vínculos que comprometam a atuação;
* Art. 46, caput e §2º, da Lei 13.709/2018: adoção de medidas de segurança, técnicas e administrativas, desde a concepção do produto ou serviço até sua execução;
* COBIT 2019, BAI02.04 - Obter aprovação dos requisitos da solução: obter aprovação formal dos requisitos funcionais, técnicos, de segurança e de conformidade antes de prosseguir com a solução;
* COBIT 2019, APO01.05 - Estabelecer papéis e responsabilidades: definir e comunicar papéis e responsabilidades relacionados à informação e à tecnologia;
* COBIT 2019, APO01.09 - Definir e comunicar políticas e procedimentos: manter políticas, procedimentos e orientações para direcionar processos de gestão de TIC;
* COBIT 2019, APO10.03 - Gerenciar relacionamentos e contratos com fornecedores: estabelecer e acompanhar contratos, responsabilidades, níveis de serviço e obrigações de fornecedores;
* COBIT 2019, APO10.05 - Monitorar desempenho e conformidade de fornecedores: acompanhar desempenho, conformidade, qualidade e resultados pactuados com fornecedores.

### Evidências

* Resposta declarada no questionário iGovTI 2026 indicando não adoção das práticas avaliadas;

* Ausência de documentação comprobatória suficiente nos arquivos encaminhados pelo auditado;

* Resultado dos procedimentos de auditoria aplicáveis à questão;


### Situação encontrada






A partir da análise das informações fornecidas, verificou-se que a organização PIORCASO não demonstrou adotar processo formal e padronizado para planejamento, contratação, fiscalização e gestão de soluções de TIC, com participação técnica da área de TIC, alinhamento ao planejamento, requisitos de segurança e critérios objetivos de entrega e desempenho, pois a Equipe de Auditoria identificou fragilidades nos seguintes aspectos: processo formal e padronizado para contratações de TIC; análise prévia e aprovação técnica da área de TIC; aderência ao plano de TIC, ao plano de contratações ou à proposta orçamentária; equipe de planejamento formalmente designada e com participação técnica de TIC; requisitos técnicos, análise de riscos, segurança da informação, proteção de dados ou critérios objetivos de aceite nos artefatos de planejamento; níveis mínimos de serviço, métricas de desempenho ou critérios objetivos de fiscalização e recebimento;. A inexistência ou fragilidade de processo formal contraria a governança das contratações prevista no art. 11 da Lei 14.133/2021, a padronização documental do art. 19, inciso IV, e o COBIT 2019, APO01.09, podendo gerar falta de clareza quanto a etapas, instâncias decisórias e critérios de aprovação. A ausência de análise prévia e aprovação técnica da área de TIC contraria a governança das contratações, a aprovação formal de requisitos da solução prevista no COBIT 2019, BAI02.04, e a definição de papéis e responsabilidades do COBIT 2019, APO01.05, podendo resultar em soluções incompatíveis com padrões técnicos, segurança ou prioridades institucionais. A falta de aderência ao planejamento, ao plano de contratações ou à proposta orçamentária contraria os arts. 11 e 18 da Lei 14.133/2021, podendo gerar contratações reativas, desalinhadas ou sem compatibilidade com prioridades e disponibilidade orçamentária. A ausência de equipe de planejamento formalmente designada e com participação técnica de TIC contraria a governança das contratações, o art. 7º da Lei 14.133/2021 e a definição de papéis e responsabilidades do COBIT 2019, APO01.05, podendo fragilizar a instrução e a avaliação técnica da contratação. A insuficiência dos artefatos de planejamento contraria os arts. 18 e 6º, inciso XXIII, da Lei 14.133/2021 e o art. 46 da LGPD, podendo levar a contratações sem requisitos técnicos, riscos, segurança, proteção de dados ou critérios objetivos de aceite. A ausência de níveis mínimos de serviço, métricas de desempenho ou critérios objetivos de fiscalização e recebimento contraria o art. 6º, inciso XXIII, da Lei 14.133/2021 e o COBIT 2019, APO10.03 e APO10.05, podendo gerar pagamento desvinculado da entrega de resultados, qualidade ou desempenho.

As contratações de TIC exigem governança técnica, planejamento adequado, participação da área de TIC e mecanismos objetivos de fiscalização e mensuração de resultados. A complexidade das soluções tecnológicas, os riscos de segurança da informação e a dependência operacional dos serviços tornam insuficiente uma instrução contratual genérica ou sem análise técnica especializada.

Sob a perspectiva da Questão 6 da matriz de planejamento, a organização deve possuir processo formal e padronizado para contratações de TIC, definir papéis e responsabilidades, utilizar modelos e orientações, submeter contratações à análise técnica da área de TIC, assegurar alinhamento ao planejamento e ao orçamento, designar equipe de planejamento, prever requisitos técnicos e de segurança e estabelecer níveis de serviço e critérios objetivos de fiscalização e recebimento.

Os critérios adotados pela matriz indicam que a alta administração é responsável pela governança das contratações, que a fase preparatória deve conter planejamento compatível com o plano de contratações e elementos mínimos do estudo técnico preliminar, que os termos de referência devem prever requisitos, modelo de execução, modelo de gestão e critérios de medição e pagamento, e que a gestão de TIC deve aprovar requisitos, definir papéis e acompanhar contratos e desempenho de fornecedores[^explica_contratacoes_tic].

Com base na análise das respostas aos itens q2801, q2801ext[A], q2801ext[B], q2801ext[C], q2801ext[D], q2801ext[E], q2801ext[F], q2801ext[G], q2804[A], q2804[B], q2804[C], q2804[D], q2804[E], q2102ext[C], q2802ext[C] e q2802ext[D] do questionário aplicado e da avaliação das evidências anexadas aos itens q2801evi, q2804eviA, q2102evi e q2802evi, conforme apontado na seção de Evidências, a Equipe de Auditoria constatou as seguintes deficiências nas contratações de TIC da organização:


* **Inexistência ou fragilidade de processo formal e padronizado para contratações de TIC.**

* **Contratações de TIC sem análise prévia e aprovação técnica obrigatória da área de TIC.**

* **Contratações de TIC sem aderência ao plano de TIC, ao plano de contratações ou à proposta orçamentária.**

* **Contratações de TIC sem equipe de planejamento formalmente designada e com participação técnica de TIC.**

* **Artefatos de planejamento das contratações de TIC sem requisitos técnicos, análise de riscos, segurança da informação, proteção de dados ou critérios objetivos de aceite.**

* **Contratações de TIC sem níveis mínimos de serviço, métricas de desempenho ou critérios objetivos de fiscalização e recebimento.**


Essas situações ensejaram o presente achado e serão detalhadas nas seções subsequentes.

[^explica_contratacoes_tic]: Os critérios de contratações de TIC adotados pela matriz combinam requisitos legais da Lei 14.133/2021, requisitos de segurança e proteção de dados da LGPD e boas práticas do COBIT 2019 sobre requisitos, papéis, procedimentos, contratos e desempenho de fornecedores.



#### Processo formal e padronizado para contratações de TIC

O processo de contratação de TIC deve estabelecer fluxo, etapas, papéis, responsabilidades, modelos mínimos de artefatos, manuais, checklists ou orientações internas. Esses elementos reduzem improvisação, aumentam padronização e permitem controle sobre a qualidade da instrução processual.

O art. 11, parágrafo único, da Lei 14.133/2021 atribui à alta administração responsabilidade pela governança das contratações, com processos, estruturas, gestão de riscos e controles internos. O art. 19, inciso IV, prevê a instituição de modelos de documentos padronizados, e o COBIT 2019, APO01.09, orienta a definição e comunicação de políticas e procedimentos.

Sem processo formal e padronizado, pode não haver clareza quanto às etapas, instâncias decisórias, critérios de aprovação e artefatos mínimos das contratações de TIC.

Diante disso, [será proposta recomendação para que a organização formalize processo de contratação de TIC, contemplando fluxo, etapas, papéis, responsabilidades, modelos mínimos de artefatos, manuais, checklists ou orientações internas.]{.underline}





#### Análise prévia e aprovação técnica da área de TIC

As contratações de TIC devem ser submetidas à análise prévia e aprovação técnica da área de TIC, inclusive quando demandadas por outras áreas da organização. Essa análise é necessária para verificar compatibilidade técnica, segurança, integração com o ambiente existente, riscos e aderência a padrões institucionais.

O COBIT 2019, BAI02.04, orienta a obtenção de aprovação formal dos requisitos funcionais, técnicos, de segurança e de conformidade antes de prosseguir com a solução. O COBIT 2019, APO01.05, reforça a definição de papéis e responsabilidades relacionados à informação e à tecnologia.

Sem análise e aprovação técnica obrigatória, a organização pode contratar soluções incompatíveis com padrões técnicos, requisitos institucionais, segurança ou prioridades definidas.

Diante disso, [será proposta recomendação para que as contratações de TIC sejam submetidas à análise prévia e aprovação técnica da área de TIC, inclusive quando demandadas por outras áreas da organização.]{.underline}





#### Aderência ao planejamento, plano de contratações e proposta orçamentária

As contratações de TIC devem estar vinculadas ao planejamento de TIC, ao plano de contratações e à proposta orçamentária. Essa vinculação demonstra que a contratação decorre de prioridade definida, possui respaldo orçamentário e contribui para objetivos institucionais.

O art. 18 da Lei 14.133/2021 prevê a compatibilização da contratação com o plano de contratações anual e o planejamento da Administração. O art. 11 também reforça a responsabilidade da alta administração pela governança das contratações.

A ausência de aderência ao planejamento, ao plano de contratações ou à proposta orçamentária aumenta o risco de aquisições reativas, desalinhadas, não priorizadas ou sem justificativa adequada.

Diante disso, [será proposta recomendação para que a organização condicione as contratações de TIC à vinculação com o planejamento de TIC, com o plano de contratações e com a proposta orçamentária, ressalvadas situações excepcionais devidamente justificadas.]{.underline}





#### Equipe de planejamento da contratação de TIC

As contratações de TIC devem contar com equipe de planejamento formalmente designada, com participação da área requisitante, da área técnica de TIC e das demais áreas necessárias. A designação formal favorece responsabilização, segregação de funções e qualidade técnica da instrução.

O art. 7º da Lei 14.133/2021 trata da designação de agentes públicos para funções essenciais, observadas atribuições, formação e segregação de funções. O COBIT 2019, APO01.05, orienta a definição e comunicação de papéis e responsabilidades.

Sem equipe formalmente designada e com participação técnica de TIC, os artefatos de planejamento podem ser incompletos ou tecnicamente frágeis.

Diante disso, [será proposta recomendação para que a organização designe formalmente equipe de planejamento da contratação de TIC, com participação da área requisitante, área técnica de TIC e demais áreas necessárias.]{.underline}





#### Artefatos de planejamento das contratações de TIC

Os artefatos de planejamento das contratações de TIC devem contemplar requisitos técnicos, análise de riscos, requisitos de segurança da informação, proteção de dados pessoais quando aplicável e critérios objetivos de aceite.

O art. 18 da Lei 14.133/2021 define elementos mínimos da fase preparatória, e o art. 6º, inciso XXIII, prevê que o termo de referência contenha requisitos da contratação, modelo de execução, modelo de gestão contratual e critérios de medição e pagamento. O art. 46 da LGPD exige medidas técnicas e administrativas de segurança desde a concepção do produto ou serviço até sua execução.

Sem esses elementos, a contratação pode resultar em solução inadequada, riscos não tratados, baixa segurança, problemas de proteção de dados e dificuldade de verificar se a entrega atende às necessidades da Administração.

Diante disso, [será proposta recomendação para que os artefatos de planejamento das contratações de TIC contemplem requisitos técnicos, análise de riscos, requisitos de segurança da informação, proteção de dados pessoais quando aplicável e critérios objetivos de aceite.]{.underline}





#### Níveis de serviço, métricas de desempenho e critérios de fiscalização

Os instrumentos de contratação de TIC devem estabelecer níveis mínimos de serviço, indicadores, critérios de medição, critérios de recebimento e vinculação do pagamento à efetiva entrega de resultados ou níveis de qualidade.

O art. 6º, inciso XXIII, da Lei 14.133/2021 exige modelo de gestão contratual e critérios de medição e pagamento no termo de referência. O COBIT 2019, APO10.03 e APO10.05, orienta o estabelecimento e acompanhamento de contratos, responsabilidades, níveis de serviço, desempenho, conformidade, qualidade e resultados pactuados com fornecedores.

Sem níveis mínimos de serviço, métricas de desempenho ou critérios objetivos de fiscalização e recebimento, a organização fica exposta ao pagamento desvinculado da qualidade, desempenho ou resultado efetivamente entregue.

Diante disso, [será proposta recomendação para que os TRs, projetos básicos, contratos ou instrumentos equivalentes de TIC estabeleçam níveis mínimos de serviço, indicadores, critérios de medição, critérios de recebimento e vinculação do pagamento à efetiva entrega de resultados ou níveis de qualidade.]{.underline}



#### Conclusão

As fragilidades identificadas nas contratações de TIC comprometem a governança técnica, o alinhamento ao planejamento, a qualidade dos artefatos, a gestão de riscos, a segurança da informação e o controle de resultados.

Diante das situações apresentadas, será sugerida proposta de encaminhamento à organização para que promova a adequação de seu processo de contratação de TIC, alinhando-o aos critérios previstos na Lei 14.133/2021, na Lei 13.709/2018 e no COBIT 2019.

### Propostas de Encaminhamento

* **Comunicação com Recomendação** para que formalize a governança técnica das contratações de TIC e vincule pagamentos a resultados mensuráveis.;







```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```


# 5. Plano de ação

Para facilitar o atendimento das propostas constantes da Seção 4, a Equipe de Auditoria elaborou modelo de plano de ação contendo os encaminhamentos preliminarmente propostos ao(à) **PIORCASO**.

Cumpre alertar que, em conformidade com o art. 4º, incisos I e II, da Deliberação TCE-RJ nº 346/2024, cabe à unidade jurisdicionada avaliar a conveniência e a oportunidade de implementar as recomendações. Ressalta-se, contudo, que a eventual decisão pela não aderência deve ser motivada: o gestor deverá demonstrar formalmente, sob pena de responsabilização, que o não atendimento constitui a medida mais adequada às circunstâncias do caso concreto, em seu julgamento, bem como apresentar as medidas alternativas adotadas para sanar a situação que ensejou a recomendação.

: Tabela 11 - Plano de ação contendo os encaminhamentos preliminarmente propostos

| Achado | Ação | Avaliação de Viabilidade | Quem? | Quando? |
|---|---|---|---|---|
| **1** | formalize a estrutura de TIC, suas atribuições e seu posicionamento organizacional. | | | |
| **2** | institua e mantenha modelo de governança e comitê de TIC com atuação efetiva. | | | |
| **3** | formalize, aprove, execute e acompanhe plano de TIC alinhado à estratégia, ao orçamento e às contratações. | | | |
| **4** | dimensione e desenvolva capacidade institucional mínima de TIC e segurança da informação. | | | |
| **5** | implemente processos mínimos de gestão de serviços, ativos, configuração e incidentes de TIC. | | | |
| **6** | formalize a governança técnica das contratações de TIC e vincule pagamentos a resultados mensuráveis. | | | |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>






```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```


# Apêndice A. Ajustes nas respostas declaradas

A Equipe de Auditoria, em busca da melhor representação do cenário atual de governança e gestão de TIC da organização, ajustou resposta(s) declarada(s) pelo(a) **PIORCASO** ao questionário iGovTI 2026.

Para tanto, foram utilizadas as justificativas e evidências fornecidas pelo jurisdicionado quando do envio das respostas ao questionário. Ressalta-se que a verificação dessa documentação foi realizada nos termos dos procedimentos definidos para a fiscalização, de modo que nem todas as evidências encaminhadas foram, necessariamente, objeto de análise exaustiva pela Equipe de Auditoria.

Seguem as alterações realizadas após a avaliação das respostas e da amostra de evidências, bem como as justificativas apresentadas pela Equipe:

: Tabela 12 - Relação de respostas ajustadas pela Equipe após validação

| Questão | Resposta original | Resposta ajustada | Justificativa |
|---|---|---|---|
| **q1001** | Adota em maior parte ou totalmente | Não adota | Não foram apresentadas evidências suficientes da prática declarada. |
| **q2102** | Adota parcialmente | Não adota | Não foi apresentado plano de TIC vigente e formalmente aprovado. |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>
