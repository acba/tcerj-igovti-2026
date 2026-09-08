---
title: "RELATÓRIO INDIVIDUAL"
subtitle: {{ auditado.sigla }} - {{ auditado.nome }}
lang: pt-BR
figure-caption-position: above
---

# 1. Introdução

Este relatório apresenta os resultados da organização **{{ auditado.sigla }}** relativos à Fiscalização TCE-RJ nº 18/2026, realizada pelo TCE-RJ para avaliar o grau de adoção de práticas de governança e gestão de tecnologia da informação e comunicação pelas organizações jurisdicionadas.

O trabalho abrangeu órgãos e entidades de todos os poderes da Administração Pública Estadual e um conjunto de prefeituras municipais.

{% if auditado.status_avaliacao == "nao_respondente" %}

# 2. Ausência de resposta válida ao questionário

A organização **{{ auditado.sigla }}** integrou o universo da Fiscalização TCE-RJ nº 18/2026. Contudo, não foi identificada resposta válida ao questionário iGovTI 2026 nas bases processadas pela Equipe de Auditoria.

Como não houve submissão final, eventuais registros incompletos não constituem declaração definitiva da organização. Por essa razão, não foi possível calcular o índice individual, avaliar a consistência das práticas declaradas ou executar os procedimentos de auditoria individualizados previstos para as organizações respondentes.

Assim, este relatório registra a ausência de resposta válida e não contém achados decorrentes da avaliação de evidências. Na etapa de comentários do gestor, foi facultado à organização apresentar esclarecimentos, comprovação de eventual resposta encaminhada ou justificativa para a ausência de resposta.

{% if auditado.sigla == "EMOP" %}
A exportação integral da coleta registra que a EMOP iniciou o preenchimento, respondeu parte dos blocos do questionário e anexou cinco arquivos. O registro, contudo, permaneceu incompleto e sem data de submissão final. Em 23/6/2026, o ponto focal solicitou a reabertura do questionário e informou ter estado ausente por problemas de saúde. Na etapa de comentários do gestor, a EMOP confirmou a ausência de resposta válida, sem acrescentar, naquele instrumento, justificativa textual ou arquivo comprobatório.
{% elif auditado.sigla == "PESAGRO" %}
Na etapa de comentários do gestor, a PESAGRO confirmou a ausência de resposta válida, sem apresentar justificativa textual ou arquivo comprobatório naquele instrumento.
{% elif auditado.sigla == "SESP" %}
A SESP não concluiu o questionário eletrônico de comentários, mas apresentou esclarecimentos por e-mail e pelo Ofício SESP-GABSEC nº 1.067, recebido em 21/7/2026. Informou que a servidora anteriormente indicada como ponto focal havia se desvinculado da Secretaria, que a demanda somente fora encaminhada internamente em 17/7/2026 e que, quando a pendência foi identificada, o link estava expirado; indicou novo ponto focal e solicitou novo prazo e acesso. Em 24/7/2026, a Equipe informou que os prazos da fiscalização haviam se encerrado, mas que a manifestação seria considerada no relatório final.
{% else %}
Não foi identificada manifestação da organização na etapa de comentários do gestor. Permanece, portanto, a ausência de esclarecimentos nessa etapa.
{% endif %}

Os registros acima não equivalem a resposta válida nem permitem incorporar dados ao cálculo do iGovTI. Constituem, contudo, elementos relevantes para a análise das circunstâncias e do grau de cooperação da organização. As comunicações da fiscalização e os respectivos registros de ciência integram o Anexo AN10 do relatório consolidado.

O relatório consolidado propõe a abertura de processo apartado para apuração individualizada das circunstâncias da ausência de resposta válida, com oportunidade para apresentação de razões de defesa. A ausência de submissão válida, isoladamente, não caracteriza obstrução à auditoria ou sonegação de informações, nem pressupõe reconhecimento antecipado de responsabilidade ou aplicação automática de sanção.

{% else %}

# 2. iGovTI 2026

{% set rotulos_dimensoes_gestao = {
  'PlanejamentoTI': 'Planejamento de TIC',
  'ServicosTI': 'Gestão de serviços de TIC',
  'RiscosTISegInfo': 'Riscos de TI e de segurança da informação',
  'EstruturaSegInfo': 'Estrutura de segurança da informação',
  'ProcessoSegInfo': 'Processos de segurança da informação',
  'GerirSoluçõesTI': 'Gestão de soluções de TIC'
} %}

A avaliação das organizações jurisdicionadas baseia-se no método de autoavaliação de controles (*Control Self-Assessment* – CSA), operacionalizado mediante questionário eletrônico. A ferramenta permitiu aos gestores declarar o nível de adoção das práticas de tecnologia da informação com a documentação probatória correspondente. As evidências anexadas e as justificativas apresentadas foram submetidas à análise de consistência, servindo de subsídio para eventuais ajustes na pontuação declarada e para a identificação de inconformidades ou achados de auditoria.

O questionário do iGovTI 2026 foi estruturado com o objetivo de diagnosticar aspectos essenciais de governança e gestão de TIC, abrangendo[^observacao_conteudo_igovti26] segurança da informação, gestão de riscos, continuidade de negócios, serviços de tecnologia, contratações de TIC, estrutura e força de trabalho, desenvolvimento de soluções, gestão de projetos e uso de inteligência artificial. Para além do diagnóstico situacional de cada organização, o instrumento serve como referencial para futuras ações de fiscalização.


[^observacao_conteudo_igovti26]: Nem todos esses temas integram o cálculo do índice: a composição do iGovTI considera apenas as práticas e dimensões descritas nesta seção

O iGovTI 2026 constitui um índice composto, mensurado em uma escala de 0 a 1. A quantificação do índice inicia-se com a conversão das respostas categóricas declaradas em coeficientes numéricos, conforme os critérios de valoração estabelecidos na [@tbl:conversao_categorias].

: Critérios de valoração das respostas qualitativas do questionário iGovTI 2026 {#tbl:conversao_categorias#}

| Categoria de Resposta Declarada | Coeficiente Numérico |
|:--------------------------------------------------|:--------------------:|
| Não adota | 0,00 |
| Há decisão formal ou plano aprovado para adotá-lo | 0,05 |
| Adota em menor parte | 0,15 |
| Adota parcialmente | 0,50 |
| Adota em maior parte ou totalmente | 1,00 |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

Nas questões que admitem itens de detalhamento, a pontuação da questão principal sofre deduções proporcionais à quantidade de itens não atendidos pela organização. Subsequentemente, os valores são consolidados por meio de agregação ponderada em uma estrutura hierárquica. O índice final é composto por dois blocos principais, conforme detalhado na [@fig:composicao_igovti_2026]: **Governança de TIC (peso de 47,8%)**, formado por 4 questões de agregação direta; **Gestão de TIC (iGestTI) (peso de 52,2%)**, estruturado em 6 dimensões operacionais que consolidam 20 questões principais ponderadas.

![Composição do iGovTI 2026](igovti_2026_composicao_infografico.png){#fig:composicao_igovti_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

Com base na pontuação consolidada do iGovTI 2026, a organização é classificada em um de quatro níveis de maturidade, cujos intervalos de pontuação estão definidos na [@tbl:faixas_maturidade] e representados graficamente na parte inferior da [@fig:composicao_igovti_2026].

: Intervalos de pontuação para enquadramento nos níveis de maturidade {#tbl:faixas_maturidade#}

| Nível de Maturidade | Intervalo do Índice (iGovTI) |
|:--------------------------------------------------|:--------------------:|
| **Inexpressivo** | 0,00 ≤ iGovTI < 0,15 |
| **Iniciando** | 0,15 ≤ iGovTI < 0,40 |
| **Intermediário** | 0,40 ≤ iGovTI < 0,70 |
| **Aprimorado** | 0,70 ≤ iGovTI ≤ 1,00 |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

## 2.1. Cenário Geral

A análise consolidada apresentada nesta seção fundamenta-se nos resultados calculados para as {{ universo_2026_n|int }} organizações com resposta válida e índice iGovTI 2026 calculado. A análise visa contextualizar o resultado individual da organização **{{ auditado.sigla }}**, identificar padrões de maturidade, assimetrias entre governança e gestão e capacidades desenvolvidas no conjunto avaliado.

A distribuição por nível de maturidade, apresentada na [@fig:distribuicao_maturidade_igovti_2026], evidencia concentração nos estágios iniciais. Das {{ universo_2026_n|int }} organizações, {{ maturidade_inexpressivo_n|int }} ({{ ('%0.1f' | format(maturidade_inexpressivo_pct|float)) | replace('.', ',') }}%) foram classificadas no nível **Inexpressivo** e {{ maturidade_iniciando_n|int }} ({{ ('%0.1f' | format(maturidade_iniciando_pct|float)) | replace('.', ',') }}%) no nível **Iniciando**. Assim, {{ igovti_abaixo_040_n|int }} organizações ({{ ('%0.1f' | format(igovti_abaixo_040_pct|float)) | replace('.', ',') }}%) obtiveram resultado inferior a 0,40. Somente {{ maturidade_intermediario_n|int }} organizações ({{ ('%0.1f' | format(maturidade_intermediario_pct|float)) | replace('.', ',') }}%) alcançaram o nível **Intermediário** e {{ maturidade_aprimorado_n|int }} ({{ ('%0.1f' | format(maturidade_aprimorado_pct|float)) | replace('.', ',') }}%) o nível **Aprimorado**.

![Distribuição das organizações por nível de maturidade do iGovTI 2026](igovti_2026_distribuicao_maturidade.png){#fig:distribuicao_maturidade_igovti_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

O iGovTI apresentou média de {{ ('%0.3f' | format(igovti_geral_media|float)) | replace('.', ',') }} e mediana de {{ ('%0.3f' | format(igovti_geral_mediana|float)) | replace('.', ',') }}. O primeiro quartil foi {{ ('%0.3f' | format(igovti_geral_q1|float)) | replace('.', ',') }} e o terceiro quartil, {{ ('%0.3f' | format(igovti_geral_q3|float)) | replace('.', ',') }}, o que evidencia a concentração de 50% das organizações avaliadas nesse intervalo, bem como a permanência de pelo menos 75% das entidades abaixo do nível Intermediário. A divergência positiva entre a média e a mediana, combinada com o valor máximo de {{ ('%0.3f' | format(igovti_geral_maximo|float)) | replace('.', ',') }} e com apenas {{ maturidade_aprimorado_n|int }} organizações no nível Aprimorado, caracteriza uma distribuição com assimetria à direita (positiva): um grupo reduzido de resultados elevados desloca a média para cima, sem alterar o quadro predominante de baixa maturidade. {{ igovti_geral_zeros_n|int }} organizações apresentaram valor igual a zero no índice calculado.

## 2.2. Cenário atual - {{ auditado.sigla }}

Apresentado o panorama geral do universo fiscalizado, esta subseção detalha o desempenho específico da organização jurisdicionada. A organização **{{ auditado.sigla }}** obteve o **valor {{ ('%0.4f' | format(iGovTI|float)) | replace('.', ',') }} para o iGovTI 2026**, correspondente ao nível **{{ iGovTI_maturidade }}** de maturidade.

A [@fig:comparativo_distribuicao_iGovTI] apresenta a distribuição contínua dos resultados do iGovTI 2026 e a posição da organização **{{ auditado.sigla }}** nesse conjunto. As linhas verticais indicam a média e a mediana das organizações avaliadas, e o marcador “X” identifica o resultado individual. Diferenças marginais de pontuação entre organizações adjacentes devem ser interpretadas com cautela, pois o modelo matemático de composição do índice não pressupõe estimativa de erro amostral e os resultados estão sujeitos à qualidade e à fidedignidade das informações declaradas.

![Distribuição contínua dos resultados do iGovTI 2026 e posição da organização {{ auditado.sigla }}]({{ auditado.sigla }}_comparativo_distribuicao_iGovTI.png){#fig:comparativo_distribuicao_iGovTI#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

A [@fig:componentes_igovti] apresenta a composição do resultado da organização **{{ auditado.sigla }}** entre governança e gestão de TIC.

![Resultado da organização {{ auditado.sigla }} por componentes do iGovTI 2026]({{ auditado.sigla }}_componentes_iGovTI.png){#fig:componentes_igovti#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

: Resultado sintético do iGovTI 2026 da organização {{ auditado.sigla }} {#tbl:resultado_sintetico_igovti#}

| Componente | Peso no iGovTI 2026 | Valor {{ auditado.sigla }} |
|:--------------------------------------------------|------------------------------:|--------------------:|
| **Governança de TIC** | 0,4777 | {{ ('%0.4f' | format(GovernancaTI|float)) | replace('.', ',') }} |
| **Gestão de TIC** | 0,5223 | {{ ('%0.4f' | format(iGestTI|float)) | replace('.', ',') }} |
| **iGovTI 2026** | 1,0000 | {{ ('%0.4f' | format(iGovTI|float)) | replace('.', ',') }} |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

### 2.2.1. Governança de TIC

A governança de TIC avalia a capacidade da alta administração de orientar, dirigir, monitorar e controlar o uso da tecnologia da informação, de modo alinhado aos objetivos institucionais, aos riscos relevantes e às necessidades das áreas finalísticas e administrativas.

No iGovTI 2026, o componente Governança de TIC agrega diretamente quatro práticas: estabelecimento do modelo de gestão de TIC, monitoramento do desempenho da gestão de TIC pela alta administração, atuação da auditoria interna em apoio à governança de TIC e definição de metas para simplificar os serviços públicos.

A organização **{{ auditado.sigla }}** obteve o **valor {{ ('%0.4f' | format(GovernancaTI|float)) | replace('.', ',') }} no componente Governança de TIC**.

![Resultado do componente Governança de TIC da organização {{ auditado.sigla }}]({{ auditado.sigla }}_comparativo_distribuicao_GovernancaTI.png){#fig:comparativo_distribuicao_governancati#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

#### Composição do componente Governança de TIC

A [@tbl:estatisticas_praticas_governanca] discrimina os valores das quatro práticas que compõem a Governança de TIC. Cada prática varia de 0 a 1. A tabela apresenta o peso de cada prática, o valor obtido pela organização e as estatísticas descritivas do conjunto avaliado (média e mediana). O valor individual já incorpora as deduções previstas para os itens de detalhamento, quando aplicáveis.

: Composição do resultado de Governança de TIC e estatísticas descritivas das práticas {#tbl:estatisticas_praticas_governanca#}

| Prática | Peso | Valor {{ auditado.sigla }} | Média | Mediana |
|---|---:|---:|---:|---:|
| **Modelo de gestão de TIC** | {{ ('%0.4f' | format(governanca_modelo_gestao_peso|float)) | replace('.', ',') }} | {{ ('%0.4f' | format(q1001|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(governanca_modelo_gestao_geral_media|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(governanca_modelo_gestao_geral_mediana|float)) | replace('.', ',') }} |
| **Monitoramento do desempenho da gestão de TIC** | {{ ('%0.4f' | format(governanca_monitoramento_desempenho_peso|float)) | replace('.', ',') }} | {{ ('%0.4f' | format(q1002|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(governanca_monitoramento_desempenho_geral_media|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(governanca_monitoramento_desempenho_geral_mediana|float)) | replace('.', ',') }} |
| **Atuação da auditoria interna em apoio à governança de TIC** | {{ ('%0.4f' | format(governanca_auditoria_interna_peso|float)) | replace('.', ',') }} | {{ ('%0.4f' | format(q1003|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(governanca_auditoria_interna_geral_media|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(governanca_auditoria_interna_geral_mediana|float)) | replace('.', ',') }} |
| **Simplificação dos serviços públicos** | {{ ('%0.4f' | format(governanca_simplificacao_servicos_peso|float)) | replace('.', ',') }} | {{ ('%0.4f' | format(q1004|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(governanca_simplificacao_servicos_geral_media|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(governanca_simplificacao_servicos_geral_mediana|float)) | replace('.', ',') }} |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

O valor de Governança de TIC da organização resulta da composição ponderada das quatro práticas, conforme os pesos apresentados na tabela. No conjunto avaliado, **{{ governanca_pratica_maior_media_nome }}** apresentou a maior média ({{ ('%0.3f' | format(governanca_pratica_maior_media_valor|float)) | replace('.', ',') }}), enquanto **{{ governanca_pratica_menor_media_nome }}** registrou a menor ({{ ('%0.3f' | format(governanca_pratica_menor_media_valor|float)) | replace('.', ',') }}). A comparação deve considerar os pesos distintos das práticas.

A [@fig:perfil_praticas_governanca_auditado] compara o perfil da organização com a média e a mediana das {{ universo_2026_n|int }} organizações com resposta válida e índice calculado.

![Perfil da organização nas práticas de Governança de TIC em comparação com os demais]({{ auditado.sigla }}_perfil_praticas_GovernancaTI.png){#fig:perfil_praticas_governanca_auditado#}{width=90%}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

### 2.2.2. Gestão de TIC

A gestão de TIC avalia a capacidade da organização de planejar, executar, monitorar e aperfeiçoar os processos, serviços, controles e soluções de tecnologia da informação abrangidos pelo índice, de forma compatível com suas necessidades institucionais.

No iGovTI 2026, o componente **Gestão de TIC (iGestTI)** consolida seis dimensões operacionais: Planejamento de TIC, Gestão de serviços de TIC, Riscos de TI e de segurança da informação, Estrutura de segurança da informação, Processos de segurança da informação e Gestão de soluções de TIC.

A organização **{{ auditado.sigla }}** obteve o **valor {{ ('%0.4f' | format(iGestTI|float)) | replace('.', ',') }} no componente Gestão de TIC**.

![Resultado do componente Gestão de TIC da organização {{ auditado.sigla }}]({{ auditado.sigla }}_comparativo_distribuicao_iGestTI.png){#fig:comparativo_distribuicao_igestti#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

#### Composição do componente Gestão de TIC

A [@tbl:estatisticas_dimensoes_gestao] discrimina os valores das seis dimensões que compõem a Gestão de TIC. Cada dimensão varia de 0 a 1. A tabela apresenta o peso de cada dimensão, o valor obtido pela organização e as estatísticas descritivas do conjunto avaliado (média e mediana).

: Composição do resultado de Gestão de TIC e estatísticas descritivas das dimensões {#tbl:estatisticas_dimensoes_gestao#}

| Dimensão | Peso | Valor {{ auditado.sigla }} | Média | Mediana |
|---|---:|---:|---:|---:|
| **Planejamento de TIC** | {{ ('%0.4f' | format(planejamento_peso|float)) | replace('.', ',') }} | {{ ('%0.4f' | format((PlanejamentoTI|default(0))|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(planejamento_geral_media|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(planejamento_geral_mediana|float)) | replace('.', ',') }} |
| **Gestão de serviços de TIC** | {{ ('%0.4f' | format(servicos_peso|float)) | replace('.', ',') }} | {{ ('%0.4f' | format((ServicosTI|default(0))|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(servicos_geral_media|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(servicos_geral_mediana|float)) | replace('.', ',') }} |
| **Riscos de TI e de segurança da informação** | {{ ('%0.4f' | format(riscos_seguranca_peso|float)) | replace('.', ',') }} | {{ ('%0.4f' | format((RiscosTISegInfo|default(0))|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(riscos_seguranca_geral_media|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(riscos_seguranca_geral_mediana|float)) | replace('.', ',') }} |
| **Estrutura de segurança da informação** | {{ ('%0.4f' | format(estrutura_seguranca_peso|float)) | replace('.', ',') }} | {{ ('%0.4f' | format((EstruturaSegInfo|default(0))|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(estrutura_seguranca_geral_media|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(estrutura_seguranca_geral_mediana|float)) | replace('.', ',') }} |
| **Processos de segurança da informação** | {{ ('%0.4f' | format(processos_seguranca_peso|float)) | replace('.', ',') }} | {{ ('%0.4f' | format((ProcessoSegInfo|default(0))|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(processos_seguranca_geral_media|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(processos_seguranca_geral_mediana|float)) | replace('.', ',') }} |
| **Gestão de soluções de TIC** | {{ ('%0.4f' | format(gestao_solucoes_peso|float)) | replace('.', ',') }} | {{ ('%0.4f' | format((GerirSoluçõesTI|default(0))|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(gestao_solucoes_geral_media|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(gestao_solucoes_geral_mediana|float)) | replace('.', ',') }} |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

O valor de Gestão de TIC da organização resulta da composição ponderada das seis dimensões, conforme os pesos apresentados na tabela. Conforme a [@tbl:estatisticas_dimensoes_gestao], {% if dimensao_maior_media_nome == dimensao_maior_mediana_nome %}**{{ rotulos_dimensoes_gestao.get(dimensao_maior_media_nome, dimensao_maior_media_nome) }}** apresentou a maior média ({{ ('%0.3f' | format(dimensao_maior_media_valor|float)) | replace('.', ',') }}) e a maior mediana ({{ ('%0.3f' | format(dimensao_maior_mediana_valor|float)) | replace('.', ',') }}){% else %}**{{ rotulos_dimensoes_gestao.get(dimensao_maior_media_nome, dimensao_maior_media_nome) }}** apresentou a maior média ({{ ('%0.3f' | format(dimensao_maior_media_valor|float)) | replace('.', ',') }}), enquanto **{{ rotulos_dimensoes_gestao.get(dimensao_maior_mediana_nome, dimensao_maior_mediana_nome) }}** apresentou a maior mediana ({{ ('%0.3f' | format(dimensao_maior_mediana_valor|float)) | replace('.', ',') }}){% endif %}. A dimensão com maior média também figurou entre as de maior resultado em {{ dimensao_maior_media_maior_resultado_n|int }} organizações ({{ ('%0.1f' | format(dimensao_maior_media_maior_resultado_pct|float)) | replace('.', ',') }}%), considerados os empates.

A distribuição completa das seis dimensões é apresentada na [@fig:distribuicao_dimensoes_gestao_2026], incluindo medianas, intervalos interquartis e médias.

![Distribuição dos resultados das seis dimensões de Gestão de TIC](igovti_2026_distribuicao_dimensoes_gestao.png){#fig:distribuicao_dimensoes_gestao_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

A [@fig:maturidade_dimensoes_igovti_2026] explicita a composição de cada dimensão por nível de maturidade e permite verificar em quais capacidades se concentram as organizações nos estágios iniciais.

![Distribuição dos níveis de maturidade das organizações nas dimensões de Gestão de TIC](igovti_2026_maturidade_dimensoes.png){#fig:maturidade_dimensoes_igovti_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

As menores médias foram observadas em **{{ rotulos_dimensoes_gestao.get(dimensao_fragil_1_nome, dimensao_fragil_1_nome) }}** ({{ ('%0.3f' | format(dimensao_fragil_1_media|float)) | replace('.', ',') }}) e **{{ rotulos_dimensoes_gestao.get(dimensao_fragil_2_nome, dimensao_fragil_2_nome) }}** ({{ ('%0.3f' | format(dimensao_fragil_2_media|float)) | replace('.', ',') }}). A primeira registrou valor inferior a 0,40 em {{ dimensao_fragil_1_abaixo_040_n|int }} organizações ({{ ('%0.1f' | format(dimensao_fragil_1_abaixo_040_pct|float)) | replace('.', ',') }}%) e apareceu entre as dimensões de menor resultado de {{ dimensao_fragil_1_menor_resultado_n|int }} organizações ({{ ('%0.1f' | format(dimensao_fragil_1_menor_resultado_pct|float)) | replace('.', ',') }}%), considerados os empates. Para a segunda, esses quantitativos foram, respectivamente, {{ dimensao_fragil_2_abaixo_040_n|int }} ({{ ('%0.1f' | format(dimensao_fragil_2_abaixo_040_pct|float)) | replace('.', ',') }}%) e {{ dimensao_fragil_2_menor_resultado_n|int }} ({{ ('%0.1f' | format(dimensao_fragil_2_menor_resultado_pct|float)) | replace('.', ',') }}%). Os resultados mostram diferenças entre as distribuições das seis dimensões. Essas diferenças devem ser interpretadas em conjunto com os resultados individuais e os achados de auditoria, sem pressupor relação causal entre as dimensões.

A dimensão Estrutura de segurança da informação apresentou média de {{ ('%0.3f' | format(estrutura_seguranca_geral_media|float)) | replace('.', ',') }} e mediana de {{ ('%0.3f' | format(estrutura_seguranca_geral_mediana|float)) | replace('.', ',') }}. A dispersão observada na [@fig:distribuicao_dimensoes_gestao_2026] demonstra a heterogeneidade dos resultados nessa dimensão. A dimensão Processos de segurança da informação apresentou mediana superior à de Estrutura de segurança da informação, mas {{ ('%0.1f' | format(processos_seguranca_geral_abaixo_040_pct|float)) | replace('.', ',') }}% das organizações permaneceram abaixo de 0,40. A leitura conjunta desses indicadores permite distinguir a existência de estrutura formal da execução contínua dos processos de segurança.

## 2.3. Relação entre governança e gestão de TIC

{% set gov_val = (GovernancaTI|default(0))|float %}
{% set gest_val = (iGestTI|default(0))|float %}

{% if (gov_val < 0.15) and (gest_val < 0.15) %}
Na organização **{{ auditado.sigla }}**, os componentes Governança de TIC e Gestão de TIC situaram-se no nível **Inexpressivo** (valores inferiores a 0,1500). A diferença observada entre os componentes não permite concluir, isoladamente, pela existência de assimetria operacional relevante. A interpretação deve considerar os valores absolutos, a composição de cada componente e os achados de auditoria.
{% elif (gov_val >= 0.70) and (gest_val >= 0.70) %}
Na organização **{{ auditado.sigla }}**, os componentes Governança de TIC e Gestão de TIC situaram-se no nível **Aprimorado**. Eventual diferença entre os componentes representa variação relativa do perfil e não demonstra, por si só, fragilidade estrutural. A interpretação deve considerar a composição de cada componente e os achados de auditoria.
{% elif gov_val < gest_val %}
Na organização **{{ auditado.sigla }}**, o resultado de Governança de TIC foi inferior ao de Gestão de TIC. Essa diferença sinaliza a necessidade de examinar, em conjunto com as evidências e os achados correspondentes, os mecanismos pelos quais a alta administração direciona, monitora e avalia a TIC.
{% elif gest_val < gov_val %}
Na organização **{{ auditado.sigla }}**, o resultado de Gestão de TIC foi inferior ao de Governança de TIC. Essa diferença sinaliza a necessidade de examinar, em conjunto com as evidências e os achados correspondentes, como as diretrizes de governança se refletem nos processos, controles, serviços e soluções de TIC.
{% else %}
Na organização **{{ auditado.sigla }}**, Governança de TIC e Gestão de TIC apresentaram o mesmo valor. A igualdade não demonstra, por si só, equilíbrio em nível adequado. A interpretação deve considerar o nível de maturidade, a composição de cada componente e os achados de auditoria.
{% endif %}

Os indicadores da [@tbl:estatisticas_componentes_igovti] permitem comparar os resultados da organização com o conjunto avaliado. Nesse conjunto, a média da Gestão de TIC foi {{ ('%0.3f' | format(igest_geral_media|float)) | replace('.', ',') }}, ante {{ ('%0.3f' | format(governanca_geral_media|float)) | replace('.', ',') }} para Governança de TIC; as medianas foram, respectivamente, {{ ('%0.3f' | format(igest_geral_mediana|float)) | replace('.', ',') }} e {{ ('%0.3f' | format(governanca_geral_mediana|float)) | replace('.', ',') }}. As duas médias situaram-se no nível Iniciando. A mediana de Governança de TIC situou-se no nível Inexpressivo, e a de Gestão de TIC, no nível Iniciando.

: Estatísticas descritivas do iGovTI 2026 e de seus componentes principais {#tbl:estatisticas_componentes_igovti#}

| Indicador | Média | 1º quartil | Mediana | 3º quartil | Organizações com valor igual ou superior a 0,40 | Valor {{ auditado.sigla }} |
|---|---:|---:|---:|---:|---:|---:|
| **iGovTI** | {{ ('%0.3f' | format(igovti_geral_media|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(igovti_geral_q1|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(igovti_geral_mediana|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(igovti_geral_q3|float)) | replace('.', ',') }} | {{ igovti_geral_a_partir_040_n|int }} ({{ ('%0.1f' | format(igovti_geral_a_partir_040_pct|float)) | replace('.', ',') }}%) | {{ ('%0.4f' | format((iGovTI|default(0))|float)) | replace('.', ',') }} |
| **Governança de TIC** | {{ ('%0.3f' | format(governanca_geral_media|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(governanca_geral_q1|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(governanca_geral_mediana|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(governanca_geral_q3|float)) | replace('.', ',') }} | {{ governanca_geral_a_partir_040_n|int }} ({{ ('%0.1f' | format(governanca_geral_a_partir_040_pct|float)) | replace('.', ',') }}%) | {{ ('%0.4f' | format((GovernancaTI|default(0))|float)) | replace('.', ',') }} |
| **Gestão de TIC** | {{ ('%0.3f' | format(igest_geral_media|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(igest_geral_q1|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(igest_geral_mediana|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(igest_geral_q3|float)) | replace('.', ',') }} | {{ igest_geral_a_partir_040_n|int }} ({{ ('%0.1f' | format(igest_geral_a_partir_040_pct|float)) | replace('.', ',') }}%) | {{ ('%0.4f' | format((iGestTI|default(0))|float)) | replace('.', ',') }} |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

No conjunto avaliado, o resultado de Gestão de TIC superou o de Governança de TIC em {{ gestao_maior_governanca_n|int }} organizações ({{ ('%0.1f' | format(gestao_maior_governanca_pct|float)) | replace('.', ',') }}%); o resultado de Governança de TIC foi superior em {{ governanca_maior_gestao_n|int }} organizações ({{ ('%0.1f' | format(governanca_maior_gestao_pct|float)) | replace('.', ',') }}%); e houve igualdade em {{ governanca_gestao_iguais_n|int }} ({{ ('%0.1f' | format(governanca_gestao_iguais_pct|float)) | replace('.', ',') }}%). Além disso, {{ igest_geral_abaixo_040_n|int }} organizações ({{ ('%0.1f' | format(igest_geral_abaixo_040_pct|float)) | replace('.', ',') }}%) obtiveram resultado de Gestão de TIC inferior a 0,40.

![Distribuição do iGovTI 2026 e dos componentes Governança de TIC e Gestão de TIC](igovti_2026_distribuicao_componentes.png){#fig:distribuicao_componentes_igovti_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

A [@fig:governanca_vs_gestao_igovti_2026] apresenta a posição simultânea das organizações nos dois componentes. Pontos acima da diagonal representam resultado de Gestão de TIC superior ao de Governança de TIC; pontos abaixo da diagonal representam a situação inversa.

![Relação entre os resultados de Governança de TIC e Gestão de TIC](igovti_2026_governanca_vs_gestao.png){#fig:governanca_vs_gestao_igovti_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

## 2.4. Síntese do perfil individual

A [@fig:perfil_dimensoes_gestao_auditado] apresenta o perfil da organização **{{ auditado.sigla }}** nas seis dimensões de Gestão de TIC e o compara com a média e a mediana das {{ universo_2026_n|int }} organizações com resposta válida e índice calculado. As faixas coloridas ao fundo representam os níveis de maturidade do iGovTI 2026.

![Perfil da organização nas dimensões de Gestão de TIC em comparação com os demais]({{ auditado.sigla }}_perfil_dimensoes_iGestTI.png){#fig:perfil_dimensoes_gestao_auditado#}{width=90%}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

{% set planejamento_val = (PlanejamentoTI|default(0))|float %}

{% if planejamento_val < 0.40 %}
O resultado em Planejamento de TIC ({{ ('%0.4f' | format(planejamento_val))|replace('.', ',') }}) situa-se nos níveis Inexpressivo ou Iniciando. Esse resultado deve ser considerado na definição das prioridades de aprimoramento, em conjunto com os riscos, as necessidades institucionais e os achados de auditoria.
{% endif %}

A [@fig:percentis_indicadores_auditado] compara a posição da organização **{{ auditado.sigla }}** com as demais organizações avaliadas em cada indicador. A letra "P" indica a posição relativa (percentil) no conjunto: **P50** representa posição próxima ao centro da distribuição; **P90** indica que a organização obteve resultado igual ou superior ao de aproximadamente 90% das organizações avaliadas; e **P20** indica que apenas cerca de 20% das organizações tiveram resultado igual ou inferior. Assim, quanto maior o valor de "P", melhor é a posição relativa da organização naquele indicador.

Essa comparação deve ser interpretada com cautela. A posição relativa não substitui o valor do índice, o nível de maturidade nem a análise de conformidade realizada nos achados de auditoria. Ela serve apenas para indicar se o resultado da organização ficou relativamente abaixo, próximo ou acima do conjunto avaliado.

![Comparação da posição relativa da organização {{ auditado.sigla }} nos indicadores avaliados]({{ auditado.sigla }}_percentis_indicadores.png){#fig:percentis_indicadores_auditado#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

{% if tem_comparacao_2023 %}
### 2.4.1. Evolução comparável entre 2023 e 2026

A análise longitudinal foi realizada exclusivamente para organizações com correspondência institucional validada nas bases de 2023 e 2026. Para reduzir os efeitos das alterações promovidas no questionário e na estrutura de cálculo, foram utilizados, em ambos os anos, índices ajustados formados por práticas e agregados comparáveis. Esses valores têm finalidade analítica e não substituem os resultados oficiais divulgados em cada ciclo.

No caso da organização **{{ auditado.sigla }}**, o iGovTI ajustado comparável passou de {{ ('%0.4f' | format(comparacao_igovti_2023|float)) | replace('.', ',') }}, em 2023, para {{ ('%0.4f' | format(comparacao_igovti_2026|float)) | replace('.', ',') }}, em 2026, com variação absoluta de {{ ('%+0.4f' | format(comparacao_delta_igovti|float)) | replace('.', ',') }}.

{% if comparacao_direcao_igovti == 'avanço' %}
{% if comparacao_nivel_2023 == comparacao_nivel_2026 %}
O resultado indica avanço no conjunto harmonizado de práticas avaliadas, embora a organização tenha permanecido no nível **{{ comparacao_nivel_2026 }}** de maturidade.
{% else %}
O resultado indica avanço no conjunto harmonizado de práticas avaliadas, acompanhado da passagem do nível **{{ comparacao_nivel_2023 }}** para o nível **{{ comparacao_nivel_2026 }}** de maturidade.
{% endif %}
{% elif comparacao_direcao_igovti == 'regressão' %}
{% if comparacao_nivel_2023 == comparacao_nivel_2026 %}
O resultado indica regressão no conjunto harmonizado de práticas avaliadas, embora a organização tenha permanecido no nível **{{ comparacao_nivel_2026 }}** de maturidade.
{% else %}
O resultado indica regressão no conjunto harmonizado de práticas avaliadas, acompanhada da passagem do nível **{{ comparacao_nivel_2023 }}** para o nível **{{ comparacao_nivel_2026 }}** de maturidade.
{% endif %}
{% else %}
Não foi observada variação material no conjunto harmonizado de práticas avaliadas, e a organização permaneceu no nível **{{ comparacao_nivel_2026 }}**.
{% endif %}

: Evolução dos componentes ajustados comparáveis da organização {{ auditado.sigla }} {#tbl:evolucao_componentes_comparaveis#}

| Indicador | 2023 | 2026 | Variação absoluta |
|---|---:|---:|---:|
| **iGovTI ajustado comparável** | {{ ('%0.4f' | format(comparacao_igovti_2023|float)) | replace('.', ',') }} | {{ ('%0.4f' | format(comparacao_igovti_2026|float)) | replace('.', ',') }} | {{ ('%+0.4f' | format(comparacao_delta_igovti|float)) | replace('.', ',') }} |
| **Governança de TIC** | {{ ('%0.4f' | format(comparacao_governanca_2023|float)) | replace('.', ',') }} | {{ ('%0.4f' | format(comparacao_governanca_2026|float)) | replace('.', ',') }} | {{ ('%+0.4f' | format(comparacao_delta_governanca|float)) | replace('.', ',') }} |
| **Gestão de TIC** | {{ ('%0.4f' | format(comparacao_igest_2023|float)) | replace('.', ',') }} | {{ ('%0.4f' | format(comparacao_igest_2026|float)) | replace('.', ',') }} | {{ ('%+0.4f' | format(comparacao_delta_igest|float)) | replace('.', ',') }} |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

{% if comparacao_principais_avancos %}
Os principais avanços foram observados em {{ comparacao_principais_avancos }}.
{% endif %}
{% if comparacao_principais_regressoes %}
As principais regressões foram observadas em {{ comparacao_principais_regressoes }}.
{% endif %}

A [@fig:evolucao_individual_igovti_comparavel] apresenta a trajetória dos três indicadores. A variação deve ser interpretada como mudança nas respostas às práticas harmonizadas, e não como comprovação isolada de melhora ou piora da efetividade da TIC. A leitura deve considerar eventuais alterações institucionais, a qualidade das informações declaradas e os achados de auditoria apresentados neste relatório.

![Evolução comparável da organização {{ auditado.sigla }} entre 2023 e 2026]({{ auditado.sigla }}_evolucao_igovti_2023_2026.png){#fig:evolucao_individual_igovti_comparavel#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>
{% endif %}

A priorização de melhorias deve considerar as capacidades com menor resultado e sua relação com riscos relevantes, serviços críticos, obrigações normativas e necessidades institucionais da organização **{{ auditado.sigla }}**. A elevação numérica do índice, de forma isolada, não constitui o objetivo da avaliação.

\newpage

# 3. Resultados da Auditoria

No âmbito desta fiscalização, foram definidas questões de auditoria para orientar a avaliação da governança e da gestão de TIC. Para fins deste relatório individual, os achados decorrem da verificação das Questões 1 a 6.

: Questões de auditoria com avaliação individual {#tbl:questoes_avaliadas_individualmente#}

| Questão | Tema | Síntese do objeto avaliado |
|---|---|---|
| **Q1** | Estrutura de TIC | Existência formal, atribuições e posicionamento organizacional da área, unidade, setor ou função responsável pela TIC. |
| **Q2** | Governança e comitê de TIC | Estabelecimento de objetivos, indicadores e metas e instituição e atuação do Comitê de TIC ou instância equivalente. |
| **Q3** | Planejamento de TIC | Processo de planejamento, plano de TIC vigente, aprovação, alinhamento institucional, integração orçamentária e acompanhamento. |
| **Q4** | Capacidade institucional de TIC e segurança da informação | Existência e dimensionamento da força de trabalho, atribuição formal de cargos ou funções e capacidade interna em modelos de operação predominantemente terceirizados. |
| **Q5** | Gestão de serviços de TIC | Catálogo de serviços, níveis mínimos de serviço, inventário de ativos, gestão de configuração e tratamento de incidentes. |
| **Q6** | Contratações de TIC | Fluxo de contratação, papéis, modelos orientativos, aprovação técnica, alinhamento ao planejamento e equipe de planejamento. |

{% if auditado.tem_achados %}


{% set achados_identificados = auditado.get_achados() %}
{% set questoes_sem_achado = [] %}
{% if 'achado1' not in achados_identificados %}{% set _ = questoes_sem_achado.append('1') %}{% endif %}
{% if 'achado2' not in achados_identificados %}{% set _ = questoes_sem_achado.append('2') %}{% endif %}
{% if 'achado3' not in achados_identificados %}{% set _ = questoes_sem_achado.append('3') %}{% endif %}
{% if 'achado4' not in achados_identificados %}{% set _ = questoes_sem_achado.append('4') %}{% endif %}
{% if 'achado5' not in achados_identificados %}{% set _ = questoes_sem_achado.append('5') %}{% endif %}
{% if 'achado6' not in achados_identificados %}{% set _ = questoes_sem_achado.append('6') %}{% endif %}
{% if questoes_sem_achado %}
__Não foram identificados achados individuais relacionados {% if questoes_sem_achado|length == 1 %}à Questão{% else %}às Questões{% endif %} {% for questao in questoes_sem_achado %}{% if loop.first %}{{ questao }}{% elif loop.last %} e {{ questao }}{% else %}, {{ questao }}{% endif %}{% endfor %} para esta organização__. Por essa razão, os achados apresentados a seguir preservam a numeração vinculada às questões de auditoria que lhes deram origem.
{% endif %}

Os achados de auditoria decorrem da avaliação das respostas da organização **{{ auditado.sigla }}** ao questionário iGovTI 2026 e da correspondente análise de consistência documental realizada por esta Equipe de Auditoria. O trabalho consistiu no confronto sistemático entre as práticas de governança e gestão autodeclaradas pela organização e as evidências comprobatórias efetivamente encaminhadas, à luz da legislação aplicável e de padrões técnicos de referência internacional.

As constatações apresentadas já consideram as manifestações e os documentos encaminhados na etapa de comentários do gestor, conforme detalhado na Seção 4.


{% include 'achado_questao_1_estrutura_tic.md' %}

{% include 'achado_questao_2_governanca_comite_tic.md' %}

{% include 'achado_questao_3_planejamento_tic.md' %}

{% include 'achado_questao_4_capacidade_institucional_tic_si.md' %}

{% include 'achado_questao_5_gestao_servicos_tic.md' %}

{% include 'achado_questao_6_contratacoes_tic.md' %}

{% else %}

Com base na avaliação das respostas, das evidências e dos comentários da organização **{{ auditado.sigla }}**, nos limites dos procedimentos executados, não foram identificadas situações que ensejassem achado individual nas Questões 1 a 6.

{% endif %}

\newpage

# 4. Análise dos comentários do gestor

Esta seção apresenta a manifestação da Equipe de Auditoria sobre os comentários e documentos encaminhados pela organização. As conclusões refletem a situação verificada em **{{ comentarios_gestor.data_referencia }}**. O acolhimento de uma manifestação pode afastar situação inconforme, remover achado dela decorrente ou restaurar resposta do questionário até o limite do valor originalmente declarado.

As manifestações reproduzidas nas Seções 4.1 e 4.2 referem-se às situações e aos itens constantes do relatório individual preliminar. Após essa etapa, a Equipe de Auditoria calibrou e simplificou os procedimentos e reexecutou os três cenários com o mapa revisado. Por isso, a posição corrente e a síntese de impactos da Seção 4.3 foram recalculadas com as regras revisadas e podem diferir, em quantidade ou redação, das situações sobre as quais o gestor se manifestou.

{% if teve_comentarios_gestor %}

## 4.1. Manifestações sobre situações e achados

{% if comentarios_gestor.situacoes %}

: Avaliação das manifestações sobre situações e achados {#tbl:comentarios_gestor_situacoes#}

| Achado / situação | Manifestação do gestor | Decisão | Manifestação da Equipe de Auditoria |
|---|---|---|---|
{%- for item in comentarios_gestor.situacoes %}
| **Achado {{ item.achado }} — {{ item.situacao }}** | {{ item.manifestacao_gestor }} | **{{ item.decisao }}** | {{ item.manifestacao_equipe }} |{% endfor %}

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

{% else %}

A organização não apresentou manifestação avaliável sobre situações ou achados individualizados.

{% endif %}

## 4.2. Reavaliação de itens do questionário

{% if comentarios_gestor.itens_questionario %}

: Avaliação das manifestações sobre itens do questionário {#tbl:comentarios_gestor_itens#}

| Questão / itens | Manifestação do gestor | Decisão | Manifestação da Equipe de Auditoria |
|---|---|---|---|
{%- for item in comentarios_gestor.itens_questionario %}
| **{{ item.codigo }} — {{ item.itens }}** | {{ item.manifestacao_gestor }} | **{{ item.decisao }}** | {{ item.manifestacao_equipe }} |{% endfor %}

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

{% else %}

A organização não apresentou manifestação avaliável sobre itens do questionário sujeitos à reavaliação.

{% endif %}

## 4.3. Impacto das manifestações na posição corrente

{% set impacto = comentarios_gestor.resumo_impacto %}
{% set variacao_situacoes = (impacto.situacoes_atuais|int) - (impacto.situacoes_antes|int) %}
{% set variacao_achados = (impacto.achados_atuais|int) - (impacto.achados_antes|int) %}

: Síntese dos efeitos dos comentários do gestor {#tbl:comentarios_gestor_impactos#}

| Indicador | Antes dos comentários | Posição em {{ comentarios_gestor.data_referencia }} | Variação |
|---|---:|---:|---:|
| Situações inconformes | {{ impacto.situacoes_antes }} | {{ impacto.situacoes_atuais }} | {{ ('+' ~ variacao_situacoes) if variacao_situacoes > 0 else variacao_situacoes }} |
| Achados | {{ impacto.achados_antes }} | {{ impacto.achados_atuais }} | {{ ('+' ~ variacao_achados) if variacao_achados > 0 else variacao_achados }} |
{% if impacto.igovti_anterior is not none and impacto.igovti_atual is not none %}
| iGovTI | {{ ('%0.4f' | format(impacto.igovti_anterior|float)) | replace('.', ',') }} | {{ ('%0.4f' | format(impacto.igovti_atual|float)) | replace('.', ',') }} | {{ ('%+0.4f' | format(impacto.variacao_igovti|float)) | replace('.', ',') }} |
{% endif %}

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

{% else %}

Não foi identificada resposta válida da organização ao questionário de comentários do gestor. Permanecem, portanto, as conclusões decorrentes das respostas e evidências anteriormente avaliadas.

{% endif %}

{% if auditado.tem_achados %}

\newpage

# 5. Plano de ação

Para facilitar o atendimento das propostas constantes da Seção 3, a Equipe de Auditoria apresenta modelo de plano de ação contendo os encaminhamentos mantidos após a análise dos comentários do gestor.

Para fins de elaboração do plano de ação, as medidas associadas a determinações deverão ser tratadas como providências de cumprimento, caso sejam acolhidas na decisão plenária. Quanto às recomendações, em conformidade com o art. 4º, incisos I e II, da Deliberação TCE-RJ nº 346/2024, cabe à unidade jurisdicionada avaliar a conveniência e a oportunidade de implementá-las. A eventual decisão pela não adoção deverá ser motivada, com indicação das razões consideradas e, quando cabível, das medidas alternativas destinadas a tratar a situação que ensejou a recomendação.

: Plano de ação contendo os encaminhamentos propostos {#tbl:plano_acao#}

| Achado | Tipo | Medida proposta | Avaliação de viabilidade | Quem? | Quando? |
|---|---|---|---|---|---|
{%- for item in auditado.get_plano_acao() %}
| **{{ item.achado_num }}** | **{{ item.tipo }}** | {{ item.encaminhamento }} | | | |{% endfor %}

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

{% endif %}

\newpage

# Apêndice A. Comparabilidade com o ciclo anterior (iGovTI 2023 vs. iGovTI 2026)

A estrutura de 2026 preservou a escala de 0 a 1, as categorias de resposta e as quatro faixas de maturidade empregadas em 2023, mas alterou de forma relevante a composição dos agregados e seus pesos. As principais diferenças estão sintetizadas na [@tbl:diferencas_igovti_2023_2026].

: Principais diferenças entre as estruturas do iGovTI 2023 e do iGovTI 2026 {#tbl:diferencas_igovti_2023_2026#}

| Aspecto | iGovTI 2023 | iGovTI 2026 | Implicação analítica |
|---|---|---|---|
| **Composição do índice final** | Governança de TIC e Gestão de TIC com pesos iguais de 0,50. | Governança de TIC com peso 0,4777 e Gestão de TIC com peso 0,5223. | A gestão passou a ter participação ligeiramente superior no índice final. |
| **Governança de TIC** | Agregação hierárquica de ModeloTI, MonitorAvaliaTI e ResultadoTI. | Agregação direta de quatro práticas relativas ao modelo de gestão, monitoramento, auditoria interna e simplificação de serviços públicos. | O componente tornou-se mais direto e incorporou práticas com escopo distinto da estrutura anterior. |
| **Gestão de TIC** | Agregação de Planejamento de TIC, Pessoas e Processos de TIC; este último reunia serviços, níveis de serviço, riscos, segurança, software, projetos e contratos. | Agregação direta das seis dimensões de Gestão de TIC descritas neste relatório. | O índice passou a evidenciar separadamente seis capacidades operacionais e de segurança. |
| **Pessoas e contratações** | Pessoas e contratações de TIC integravam o cálculo da Gestão de TIC. | Não integram a árvore de cálculo do iGovTI 2026, embora continuem relevantes para o diagnóstico e para a auditoria. | Mudanças nessas matérias não explicam diretamente a variação do índice de 2026. |
| **Serviços, software e projetos** | Serviços e níveis de serviço eram agregados distintos; software e projetos integravam Processos de TIC. | Serviços foram consolidados na dimensão Gestão de serviços de TIC; software e projetos foram reunidos na dimensão Gestão de soluções de TIC. | A leitura deve considerar a nova delimitação conceitual dos componentes. |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

Em razão dessas alterações, a diferença entre os valores nominais de 2023 e 2026 não deve ser interpretada automaticamente como evolução ou retrocesso institucional. Uma análise temporal válida exige a harmonização das questões e dos agregados comparáveis, além da consideração de mudanças de escopo, pesos, respondentes e qualidade das evidências.

Para viabilizar a análise longitudinal, foram elaboradas estruturas ajustadas comparáveis para 2023 e 2026, com a manutenção apenas das práticas passíveis de correspondência entre os instrumentos e a aplicação de uma estrutura comum de agregação. Após a normalização das siglas e a validação das correspondências institucionais, foram identificadas {{ comparacao_pareados_n|int }} organizações presentes nos dois ciclos, equivalentes a {{ ('%0.1f' | format(comparacao_cobertura_2026_pct|float)) | replace('.', ',') }}% das organizações com respostas completas em 2026. A comparação individual foi apresentada somente para esse conjunto pareado.

Os resultados ajustados comparáveis têm finalidade exclusivamente analítica. Eles não substituem os índices oficiais de cada ciclo, não eliminam integralmente os efeitos de alterações de respondentes ou de contexto institucional e não constituem, isoladamente, evidência de conformidade ou de inconformidade.

{% if teve_ajuste %}

\newpage

# Apêndice B. Ajustes nas respostas declaradas

A Equipe de Auditoria, em busca da melhor representação do cenário atual de governança e gestão de TIC, ajustou resposta(s) declarada(s) pela organização **{{ auditado.sigla }}** ao questionário iGovTI 2026.

Para tanto, foram utilizadas as justificativas e evidências fornecidas pelo jurisdicionado no questionário original e na etapa de comentários do gestor. A resposta restaurada não supera o valor originalmente declarado pela organização.

Seguem as alterações mantidas na base corrente após a avaliação das respostas, das evidências e dos comentários do gestor, bem como as justificativas apresentadas pela Equipe:

: Relação de respostas ajustadas pela Equipe após validação {#tbl:ajuste_respostas#}

| Questão | Resposta original | Resposta ajustada | Justificativa |
|---|---|---|---|
{%- for ajuste in ajustes_respostas %}
| **{{ ajuste.codigo_questao }}** | {{ ajuste.de }} | {{ ajuste.para }} | {{ ajuste.justificativa }} |{% endfor %}

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

{% endif %}

{% endif %}
