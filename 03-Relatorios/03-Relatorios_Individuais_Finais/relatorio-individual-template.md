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
A SESP não concluiu o questionário eletrônico de comentários, mas apresentou esclarecimentos por e-mail e pelo Ofício SESP-GABSEC nº 1.067, recebido em 21/7/2026. Informou que a servidora anteriormente indicada como ponto focal havia se desvinculado da Secretaria, que a demanda somente fora encaminhada internamente em 17/7/2026 e que, quando a pendência foi identificada, o link estava expirado. Indicou novo ponto focal e solicitou novo prazo e acesso. Em 24/7/2026, a Equipe informou que os prazos da fiscalização haviam se encerrado, mas que a manifestação seria considerada no relatório final.
{% else %}
Não foi identificada manifestação da organização na etapa de comentários do gestor. Permanece, portanto, a ausência de esclarecimentos nessa etapa.
{% endif %}

Os registros acima não equivalem a resposta válida nem permitem incorporar dados ao cálculo do iGovTI. Constituem, contudo, elementos relevantes para a análise das circunstâncias e do grau de cooperação da organização. As comunicações da fiscalização e os respectivos registros de ciência integram o Anexo AN10 do relatório de auditoria.

As circunstâncias da ausência de resposta válida serão examinadas em processo apartado já autuado, conforme informado na Seção 4.5 do relatório de auditoria, com oportunidade para apresentação de razões de defesa. A ausência de resposta válida, por si só, não caracteriza obstrução à auditoria ou sonegação de informações, nem implica responsabilização ou aplicação automática de sanção.

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

A avaliação das organizações jurisdicionadas baseia-se no método de autoavaliação de controles (*Control Self-Assessment* – CSA), operacionalizado mediante questionário eletrônico. A ferramenta permitiu aos gestores informarem o nível de adoção das práticas de governança e gestão de TIC com envio da documentação probatória correspondente. A Equipe de Auditoria examinou esses elementos para verificar as práticas declaradas e identificar inconformidades.

O questionário do iGovTI 2026 foi estruturado com o objetivo de diagnosticar aspectos essenciais de governança e gestão de TIC, abrangendo[^observacao_conteudo_igovti26] segurança da informação, gestão de riscos, continuidade de negócios, serviços de tecnologia, contratações de TIC, estrutura e força de trabalho, desenvolvimento de soluções, gestão de projetos e uso de inteligência artificial. Para além do diagnóstico situacional de cada organização, o instrumento serve como referencial para futuras ações de fiscalização.


[^observacao_conteudo_igovti26]: Nem todos esses temas integram o cálculo do índice: a composição do iGovTI considera apenas as práticas e dimensões descritas nesta seção

O iGovTI 2026 reúne os resultados de diferentes práticas em um índice que varia de zero a um. Para calculá-lo, as respostas do questionário são convertidas em valores numéricos, conforme a [@tbl:conversao_categorias].

: Critérios de valoração das respostas qualitativas do questionário iGovTI 2026 {#tbl:conversao_categorias#}

| Categoria de Resposta Declarada | Coeficiente Numérico |
|:--------------------------------------------------|:--------------------:|
| Não adota | 0,00 |
| Há decisão formal ou plano aprovado para adotá-lo | 0,05 |
| Adota em menor parte | 0,15 |
| Adota parcialmente | 0,50 |
| Adota em maior parte ou totalmente | 1,00 |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

Nas questões com itens de detalhamento, a pontuação da questão principal é reduzida proporcionalmente à quantidade de itens não atendidos. Em seguida, as pontuações são combinadas conforme os pesos definidos para cada prática e dimensão. O índice final reúne dois componentes: **Governança de TIC, com peso de 47,8%**, e **Gestão de TIC, com peso de 52,2%**. Governança reúne quatro questões, enquanto Gestão reúne seis dimensões e 18 questões principais, conforme a [@fig:composicao_igovti_2026].

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

Para fins de interpretação dos resultados, essas mesmas faixas são utilizadas de forma descritiva para os componentes de Governança de TIC e Gestão de TIC, bem como para as práticas e dimensões que os compõem.

## 2.1. Cenário Geral

A análise consolidada apresentada nesta seção fundamenta-se nos resultados calculados para as {{ universo_2026_n|int }} organizações com resposta válida e índice iGovTI 2026 calculado. A análise visa contextualizar o resultado individual da organização **{{ auditado.sigla }}** e identificar os principais padrões de maturidade observados no conjunto avaliado.

A distribuição por nível de maturidade, apresentada na [@fig:distribuicao_maturidade_igovti_2026], evidencia concentração nos estágios iniciais. Das {{ universo_2026_n|int }} organizações, {{ maturidade_inexpressivo_n|int }} ({{ ('%0.1f' | format(maturidade_inexpressivo_pct|float)) | replace('.', ',') }}%) foram classificadas no nível **Inexpressivo** e {{ maturidade_iniciando_n|int }} ({{ ('%0.1f' | format(maturidade_iniciando_pct|float)) | replace('.', ',') }}%) no nível **Iniciando**. Assim, {{ igovti_abaixo_040_n|int }} organizações ({{ ('%0.1f' | format(igovti_abaixo_040_pct|float)) | replace('.', ',') }}%) obtiveram resultado inferior a 0,40. Somente {{ maturidade_intermediario_n|int }} organizações ({{ ('%0.1f' | format(maturidade_intermediario_pct|float)) | replace('.', ',') }}%) alcançaram o nível **Intermediário** e {{ maturidade_aprimorado_n|int }} ({{ ('%0.1f' | format(maturidade_aprimorado_pct|float)) | replace('.', ',') }}%) o nível **Aprimorado**.

![Distribuição das organizações por nível de maturidade do iGovTI 2026](igovti_2026_distribuicao_maturidade.png){#fig:distribuicao_maturidade_igovti_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

O iGovTI apresentou média de {{ ('%0.3f' | format(igovti_geral_media|float)) | replace('.', ',') }} e mediana de {{ ('%0.3f' | format(igovti_geral_mediana|float)) | replace('.', ',') }}. O primeiro quartil foi {{ ('%0.3f' | format(igovti_geral_q1|float)) | replace('.', ',') }} e o terceiro quartil, {{ ('%0.3f' | format(igovti_geral_q3|float)) | replace('.', ',') }}, o que evidencia a concentração de 50% das organizações avaliadas nesse intervalo, bem como a permanência de pelo menos 75% das entidades abaixo do nível Intermediário.

A média superior à mediana indica que um grupo reduzido de organizações com pontuações elevadas aumenta a média do conjunto. O valor máximo foi {{ ('%0.3f' | format(igovti_geral_maximo|float)) | replace('.', ',') }}, e apenas {{ maturidade_aprimorado_n|int }} organizações atingiram o nível Aprimorado. Ainda assim, predominam resultados nos níveis iniciais de maturidade. {{ igovti_geral_zeros_n|int }} organizações apresentaram valor igual a zero no índice calculado.

: Estatísticas descritivas do iGovTI 2026 e de seus componentes principais {#tbl:estatisticas_componentes_igovti#}

| Indicador | Média | 1º quartil | Mediana | 3º quartil | Organizações com valor ≥ 0,40 |
|---|---:|---:|---:|---:|---:|
| **iGovTI** | {{ ('%0.3f' | format(igovti_geral_media|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(igovti_geral_q1|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(igovti_geral_mediana|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(igovti_geral_q3|float)) | replace('.', ',') }} | {{ igovti_geral_a_partir_040_n|int }} ({{ ('%0.1f' | format(igovti_geral_a_partir_040_pct|float)) | replace('.', ',') }}%) |
| **Governança de TIC** | {{ ('%0.3f' | format(governanca_geral_media|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(governanca_geral_q1|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(governanca_geral_mediana|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(governanca_geral_q3|float)) | replace('.', ',') }} | {{ governanca_geral_a_partir_040_n|int }} ({{ ('%0.1f' | format(governanca_geral_a_partir_040_pct|float)) | replace('.', ',') }}%) |
| **Gestão de TIC** | {{ ('%0.3f' | format(igest_geral_media|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(igest_geral_q1|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(igest_geral_mediana|float)) | replace('.', ',') }} | {{ ('%0.3f' | format(igest_geral_q3|float)) | replace('.', ',') }} | {{ igest_geral_a_partir_040_n|int }} ({{ ('%0.1f' | format(igest_geral_a_partir_040_pct|float)) | replace('.', ',') }}%) |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

No conjunto avaliado, o componente Gestão de TIC apresentou média de {{ ('%0.3f' | format(igest_geral_media|float)) | replace('.', ',') }} e mediana de {{ ('%0.3f' | format(igest_geral_mediana|float)) | replace('.', ',') }}, enquanto Governança de TIC apresentou média de {{ ('%0.3f' | format(governanca_geral_media|float)) | replace('.', ',') }} e mediana de {{ ('%0.3f' | format(governanca_geral_mediana|float)) | replace('.', ',') }}. Os valores centrais dos três indicadores permaneceram concentrados nos níveis inferiores de maturidade, embora as distribuições apresentem diferenças entre si.

A [@fig:distribuicao_componentes_igovti_2026] permite comparar a distribuição do índice global com a de seus dois componentes principais, evidenciando diferenças nos valores centrais e na dispersão dos resultados.

![Distribuição do iGovTI 2026 e dos componentes Governança de TIC e Gestão de TIC](igovti_2026_distribuicao_componentes.png){#fig:distribuicao_componentes_igovti_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

A [@fig:governanca_vs_gestao_igovti_2026] apresenta a posição simultânea das organizações nos componentes Governança de TIC e Gestão de TIC. Pontos acima da diagonal indicam resultado de Gestão superior ao de Governança; pontos abaixo indicam a situação inversa; e pontos próximos à diagonal representam valores semelhantes nos dois componentes. As cores dos pontos representam o nível de maturidade da organização segundo o iGovTI global.

![Relação entre os componentes Governança de TIC e Gestão de TIC no conjunto avaliado](igovti_2026_governanca_vs_gestao.png){#fig:governanca_vs_gestao_igovti_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

No conjunto avaliado, o resultado de Gestão de TIC superou o de Governança de TIC em {{ gestao_maior_governanca_n|int }} organizações ({{ ('%0.1f' | format(gestao_maior_governanca_pct|float)) | replace('.', ',') }}%); Governança de TIC foi superior em {{ governanca_maior_gestao_n|int }} ({{ ('%0.1f' | format(governanca_maior_gestao_pct|float)) | replace('.', ',') }}%); e houve igualdade em {{ governanca_gestao_iguais_n|int }} ({{ ('%0.1f' | format(governanca_gestao_iguais_pct|float)) | replace('.', ',') }}%). Esses dados descrevem a distribuição conjunta dos componentes e não constituem, isoladamente, medida de equilíbrio ou adequação institucional.

Em conjunto, os resultados evidenciam predominância de níveis iniciais de maturidade no universo avaliado, tanto no índice global quanto em seus componentes de Governança e Gestão de TIC, embora as distribuições apresentem diferenças entre si e entre as organizações. Esse panorama constitui a referência para a análise individual apresentada na seção seguinte.

## 2.2. Cenário atual - {{ auditado.sigla }}

Apresentado o panorama geral do universo fiscalizado, esta subseção detalha o resultado individual da organização jurisdicionada. A organização **{{ auditado.sigla }}** obteve o **valor {{ ('%0.4f' | format(iGovTI|float)) | replace('.', ',') }} para o iGovTI 2026**, correspondente ao nível **{{ iGovTI_maturidade }}** de maturidade.

A [@fig:comparativo_distribuicao_iGovTI] apresenta os resultados das organizações avaliadas e a posição de **{{ auditado.sigla }}** nesse conjunto. As linhas verticais indicam a média e a mediana, e o marcador “X” identifica o resultado individual. Pequenas diferenças de pontuação devem ser interpretadas com cautela. O índice não fornece uma margem de erro estatística, e seus resultados dependem da qualidade das respostas e dos documentos apresentados.

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

O componente Governança de TIC avalia o grau de adoção de práticas relacionadas à capacidade da alta administração de orientar, dirigir, monitorar e controlar o uso da tecnologia da informação, de modo alinhado aos objetivos institucionais, aos riscos relevantes e às necessidades das áreas finalísticas e administrativas.

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

{% set governanca_val = (GovernancaTI|default(0))|float %}
{%- if governanca_val < 0.15 %}
{%- set governanca_nivel = "Inexpressivo" %}
{%- elif governanca_val < 0.40 %}
{%- set governanca_nivel = "Iniciando" %}
{%- elif governanca_val < 0.70 %}
{%- set governanca_nivel = "Intermediário" %}
{%- else %}
{%- set governanca_nivel = "Aprimorado" %}
{%- endif %}
{%- set praticas_gov = [q1001|float, q1002|float, q1003|float, q1004|float] %}
{%- set gov_qtd_baixas = (praticas_gov | select('<', 0.40) | list)|length %}
{%- set gov_qtd_altas = (praticas_gov | select('>=', 0.70) | list)|length %}
Com o resultado obtido ({{ ('%0.4f' | format(governanca_val)) | replace('.', ',') }}), o componente Governança de TIC da organização **{{ auditado.sigla }}** situa-se no nível **{{ governanca_nivel }}** de maturidade.

Em relação ao conjunto avaliado, o resultado ficou {% if governanca_val > governanca_geral_media and governanca_val > governanca_geral_mediana %}acima da média ({{ ('%0.3f' | format(governanca_geral_media|float)) | replace('.', ',') }}) e da mediana ({{ ('%0.3f' | format(governanca_geral_mediana|float)) | replace('.', ',') }}) do conjunto avaliado{% elif governanca_val < governanca_geral_media and governanca_val < governanca_geral_mediana %}abaixo da média ({{ ('%0.3f' | format(governanca_geral_media|float)) | replace('.', ',') }}) e da mediana ({{ ('%0.3f' | format(governanca_geral_mediana|float)) | replace('.', ',') }}) do conjunto avaliado{% elif governanca_val >= governanca_geral_mediana and governanca_val < governanca_geral_media %}entre a mediana ({{ ('%0.3f' | format(governanca_geral_mediana|float)) | replace('.', ',') }}) e a média ({{ ('%0.3f' | format(governanca_geral_media|float)) | replace('.', ',') }}) do conjunto avaliado{% elif governanca_val >= governanca_geral_media and governanca_val < governanca_geral_mediana %}entre a média ({{ ('%0.3f' | format(governanca_geral_media|float)) | replace('.', ',') }}) e a mediana ({{ ('%0.3f' | format(governanca_geral_mediana|float)) | replace('.', ',') }}) do conjunto avaliado{% else %}próximo da média e da mediana do conjunto avaliado (média de {{ ('%0.3f' | format(governanca_geral_media|float)) | replace('.', ',') }} e mediana de {{ ('%0.3f' | format(governanca_geral_mediana|float)) | replace('.', ',') }}){% endif %}.

Em relação às práticas componentes, {% if gov_qtd_baixas == 4 %}as quatro práticas avaliadas situaram-se nos níveis iniciais de maturidade, evidenciando pontuações baixas nas quatro práticas{% elif gov_qtd_altas == 4 %}as quatro práticas avaliadas situaram-se no nível Aprimorado{% elif gov_qtd_baixas >= 3 %}predominaram resultados nos níveis iniciais de maturidade, embora haja variação entre as práticas avaliadas{% elif gov_qtd_altas >= 3 %}predominaram resultados no nível Aprimorado, embora haja variação entre as práticas avaliadas{% else %}os resultados variaram entre as práticas avaliadas, com resultados distribuídos entre diferentes níveis de maturidade{% endif %}. 

A Seção 3 apresenta as situações identificadas pela auditoria, os critérios aplicáveis e as evidências examinadas, nos limites dos procedimentos executados.

### 2.2.2. Gestão de TIC

O componente Gestão de TIC avalia o grau de adoção de práticas relacionadas ao planejamento, à execução, ao monitoramento e ao aperfeiçoamento dos processos, serviços, controles e soluções de tecnologia da informação, de forma compatível com suas necessidades institucionais.

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

A [@fig:perfil_dimensoes_gestao_auditado] apresenta o perfil da organização **{{ auditado.sigla }}** nas seis dimensões de Gestão de TIC e o compara com a média e a mediana das {{ universo_2026_n|int }} organizações com resposta válida e índice calculado. As faixas coloridas ao fundo representam os níveis de maturidade do iGovTI 2026.

![Perfil da organização nas dimensões de Gestão de TIC em comparação com os demais]({{ auditado.sigla }}_perfil_dimensoes_iGestTI.png){#fig:perfil_dimensoes_gestao_auditado#}{width=90%}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

{% set gestao_val = (iGestTI|default(0))|float %}
{%- if gestao_val < 0.15 %}
{%- set gestao_nivel = "Inexpressivo" %}
{%- elif gestao_val < 0.40 %}
{%- set gestao_nivel = "Iniciando" %}
{%- elif gestao_val < 0.70 %}
{%- set gestao_nivel = "Intermediário" %}
{%- else %}
{%- set gestao_nivel = "Aprimorado" %}
{%- endif %}
{%- set dimensoes_valores = [
  (PlanejamentoTI|default(0))|float,
  (ServicosTI|default(0))|float,
  (RiscosTISegInfo|default(0))|float,
  (EstruturaSegInfo|default(0))|float,
  (ProcessoSegInfo|default(0))|float,
  (GerirSoluçõesTI|default(0))|float
] %}
{%- set gest_qtd_baixas = (dimensoes_valores | select('<', 0.40) | list)|length %}
{%- set gest_qtd_altas = (dimensoes_valores | select('>=', 0.70) | list)|length %}
Com o resultado obtido ({{ ('%0.4f' | format(gestao_val)) | replace('.', ',') }}), o componente Gestão de TIC da organização **{{ auditado.sigla }}** situa-se no nível **{{ gestao_nivel }}** de maturidade.

Em relação ao conjunto avaliado, o resultado ficou {% if gestao_val > igest_geral_media and gestao_val > igest_geral_mediana %}acima da média ({{ ('%0.3f' | format(igest_geral_media|float)) | replace('.', ',') }}) e da mediana ({{ ('%0.3f' | format(igest_geral_mediana|float)) | replace('.', ',') }}) do conjunto avaliado{% elif gestao_val < igest_geral_media and gestao_val < igest_geral_mediana %}abaixo da média ({{ ('%0.3f' | format(igest_geral_media|float)) | replace('.', ',') }}) e da mediana ({{ ('%0.3f' | format(igest_geral_mediana|float)) | replace('.', ',') }}) do conjunto avaliado{% elif gestao_val >= igest_geral_mediana and gestao_val < igest_geral_media %}entre a mediana ({{ ('%0.3f' | format(igest_geral_mediana|float)) | replace('.', ',') }}) e a média ({{ ('%0.3f' | format(igest_geral_media|float)) | replace('.', ',') }}) do conjunto avaliado{% elif gestao_val >= igest_geral_media and gestao_val < igest_geral_mediana %}entre a média ({{ ('%0.3f' | format(igest_geral_media|float)) | replace('.', ',') }}) e a mediana ({{ ('%0.3f' | format(igest_geral_mediana|float)) | replace('.', ',') }}) do conjunto avaliado{% else %}próximo da média e da mediana do conjunto avaliado (média de {{ ('%0.3f' | format(igest_geral_media|float)) | replace('.', ',') }} e mediana de {{ ('%0.3f' | format(igest_geral_mediana|float)) | replace('.', ',') }}){% endif %}.

Quanto ao perfil operacional, {% if gest_qtd_baixas == 6 %}as seis dimensões situaram-se nos níveis iniciais de maturidade, de modo que o baixo resultado de Gestão de TIC não se concentrou em uma única dimensão avaliada{% elif gest_qtd_altas == 6 %}as seis dimensões situaram-se no nível Aprimorado{% elif gest_qtd_baixas >= 4 %}predominaram resultados nos níveis iniciais de maturidade, embora haja variação entre as dimensões avaliadas{% elif gest_qtd_altas >= 4 %}predominaram resultados no nível Aprimorado, embora haja variação entre as dimensões avaliadas{% else %}os resultados variaram entre as dimensões avaliadas, com resultados distribuídos entre diferentes níveis de maturidade{% endif %}.
{% if tem_comparacao_2023 %}
## 2.3. Comparação longitudinal entre 2023 e 2026

Para comparar os resultados de 2023 e 2026, foram calculados índices específicos, considerando apenas as práticas comparáveis entre os questionários. Esses índices não substituem os valores oficiais de cada ano. O Apêndice A apresenta a metodologia e as limitações da comparação.

No caso da organização **{{ auditado.sigla }}**, o iGovTI ajustado comparável passou de {{ ('%0.4f' | format(comparacao_igovti_2023|float)) | replace('.', ',') }}, em 2023, para {{ ('%0.4f' | format(comparacao_igovti_2026|float)) | replace('.', ',') }}, em 2026, com variação absoluta de {{ ('%+0.4f' | format(comparacao_delta_igovti|float)) | replace('.', ',') }}.

{% if comparacao_direcao_igovti == 'avanço' %}
{% if comparacao_nivel_2023 == comparacao_nivel_2026 %}
O índice comparável aumentou, embora a organização tenha permanecido no nível **{{ comparacao_nivel_2026 }}** de maturidade.
{% else %}
O índice comparável aumentou, acompanhado da passagem do nível **{{ comparacao_nivel_2023 }}** para o nível **{{ comparacao_nivel_2026 }}** de maturidade.
{% endif %}
{% elif comparacao_direcao_igovti == 'regressão' %}
{% if comparacao_nivel_2023 == comparacao_nivel_2026 %}
O índice comparável diminuiu, embora a organização tenha permanecido no nível **{{ comparacao_nivel_2026 }}** de maturidade.
{% else %}
O índice comparável diminuiu, acompanhado da passagem do nível **{{ comparacao_nivel_2023 }}** para o nível **{{ comparacao_nivel_2026 }}** de maturidade.
{% endif %}
{% else %}
{% if comparacao_nivel_2023 == comparacao_nivel_2026 %}
Não foi observada variação relevante no índice comparável, e a organização permaneceu no nível **{{ comparacao_nivel_2026 }}** de maturidade.
{% else %}
Não foi observada variação relevante no índice comparável, embora o resultado tenha ultrapassado o limite entre os níveis **{{ comparacao_nivel_2023 }}** e **{{ comparacao_nivel_2026 }}** de maturidade.
{% endif %}
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

A [@fig:evolucao_individual_igovti_comparavel] apresenta os resultados dos três indicadores nos dois anos. As diferenças representam mudanças nas pontuações das práticas comparáveis, mas não comprovam, por si só, melhora ou piora do funcionamento da TIC. A interpretação deve considerar mudanças na organização, a qualidade das respostas, as diferenças de verificação documental entre os anos e os achados apresentados neste relatório.

![Evolução comparável da organização {{ auditado.sigla }} entre 2023 e 2026]({{ auditado.sigla }}_evolucao_igovti_2023_2026.png){#fig:evolucao_individual_igovti_comparavel#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

\newpage

## 2.4. Síntese dos resultados
{% else %}
\newpage

## 2.3. Síntese dos resultados
{% endif %}

{% set igovti_val = (iGovTI|default(0))|float %}
{% set gov_sintese_val = (GovernancaTI|default(0))|float %}
{% set gest_sintese_val = (iGestTI|default(0))|float %}
{%- if gov_sintese_val < 0.15 %}
{%- set gov_sintese_nivel = "Inexpressivo" %}
{%- elif gov_sintese_val < 0.40 %}
{%- set gov_sintese_nivel = "Iniciando" %}
{%- elif gov_sintese_val < 0.70 %}
{%- set gov_sintese_nivel = "Intermediário" %}
{%- else %}
{%- set gov_sintese_nivel = "Aprimorado" %}
{%- endif %}
{%- if gest_sintese_val < 0.15 %}
{%- set gest_sintese_nivel = "Inexpressivo" %}
{%- elif gest_sintese_val < 0.40 %}
{%- set gest_sintese_nivel = "Iniciando" %}
{%- elif gest_sintese_val < 0.70 %}
{%- set gest_sintese_nivel = "Intermediário" %}
{%- else %}
{%- set gest_sintese_nivel = "Aprimorado" %}
{%- endif %}
Em síntese, a organização **{{ auditado.sigla }}** obteve o índice global iGovTI 2026 de **{{ ('%0.4f' | format(igovti_val)) | replace('.', ',') }}**, correspondente ao nível **{{ iGovTI_maturidade }}** de maturidade, com Governança de TIC em **{{ ('%0.4f' | format(gov_sintese_val)) | replace('.', ',') }}** (nível {{ gov_sintese_nivel }}) e Gestão de TIC em **{{ ('%0.4f' | format(gest_sintese_val)) | replace('.', ',') }}** (nível {{ gest_sintese_nivel }}).

Em comparação com o conjunto de {{ universo_2026_n|int }} organizações avaliadas, o índice global situou-se {% if igovti_val > igovti_geral_media and igovti_val > igovti_geral_mediana %}acima da média ({{ ('%0.3f' | format(igovti_geral_media|float)) | replace('.', ',') }}) e da mediana ({{ ('%0.3f' | format(igovti_geral_mediana|float)) | replace('.', ',') }}) apuradas{% elif igovti_val < igovti_geral_media and igovti_val < igovti_geral_mediana %}abaixo da média ({{ ('%0.3f' | format(igovti_geral_media|float)) | replace('.', ',') }}) e da mediana ({{ ('%0.3f' | format(igovti_geral_mediana|float)) | replace('.', ',') }}) apuradas{% elif igovti_val >= igovti_geral_mediana and igovti_val < igovti_geral_media %}entre a mediana ({{ ('%0.3f' | format(igovti_geral_mediana|float)) | replace('.', ',') }}) e a média ({{ ('%0.3f' | format(igovti_geral_media|float)) | replace('.', ',') }}) apuradas{% elif igovti_val >= igovti_geral_media and igovti_val < igovti_geral_mediana %}entre a média ({{ ('%0.3f' | format(igovti_geral_media|float)) | replace('.', ',') }}) e a mediana ({{ ('%0.3f' | format(igovti_geral_mediana|float)) | replace('.', ',') }}) apuradas{% else %}próximo da média e da mediana do conjunto (média de {{ ('%0.3f' | format(igovti_geral_media|float)) | replace('.', ',') }} e mediana de {{ ('%0.3f' | format(igovti_geral_mediana|float)) | replace('.', ',') }}){% endif %}.

{% set itens_sintese = [
  q1001|float, q1002|float, q1003|float, q1004|float,
  (PlanejamentoTI|default(0))|float, (ServicosTI|default(0))|float,
  (RiscosTISegInfo|default(0))|float, (EstruturaSegInfo|default(0))|float,
  (ProcessoSegInfo|default(0))|float, (GerirSoluçõesTI|default(0))|float
] %}
{%- set total_altas = (itens_sintese | select('>=', 0.70) | list)|length %}
{%- set total_baixas = (itens_sintese | select('<', 0.40) | list)|length %}
{% if total_baixas == 10 %}Os resultados das práticas de Governança de TIC e das dimensões de Gestão de TIC concentram-se integralmente nos níveis iniciais de maturidade, indicando que a baixa pontuação da organização se distribui por diferentes aspectos considerados no cálculo do índice, e não por um componente isolado.{% elif total_baixas >= 7 %}Predominaram resultados nos níveis iniciais de maturidade entre as práticas de Governança de TIC e as dimensões de Gestão de TIC, embora haja variação entre os componentes avaliados.{% elif total_altas == 10 %}Os resultados das práticas de Governança de TIC e das dimensões de Gestão de TIC concentram-se integralmente no nível Aprimorado.{% elif total_altas >= 7 %}Predominaram resultados no nível Aprimorado entre as práticas de Governança de TIC e as dimensões de Gestão de TIC, embora haja variação entre os componentes avaliados.{% else %}O perfil apresenta heterogeneidade entre as práticas de Governança de TIC e as dimensões de Gestão de TIC, com resultados distribuídos entre diferentes níveis de maturidade.{% endif %}

{% if tem_comparacao_2023 %}
{% if comparacao_direcao_igovti == 'avanço' %}
Na comparação entre 2023 e 2026, o índice comparável da organização aumentou. Esse resultado foi calculado a partir dos itens comparáveis entre os questionários e não corresponde à comparação direta dos índices oficiais.
{% elif comparacao_direcao_igovti == 'regressão' %}
Na comparação entre 2023 e 2026, o índice comparável da organização diminuiu. Esse resultado foi calculado a partir dos itens comparáveis entre os questionários e não corresponde à comparação direta dos índices oficiais.
{% else %}
Na comparação entre 2023 e 2026, o índice comparável da organização não apresentou variação relevante. Esse resultado foi calculado a partir dos itens comparáveis entre os questionários e não corresponde à comparação direta dos índices oficiais.
{% endif %}
{% endif %}

Os resultados do iGovTI {% if tem_comparacao_2023 %}e da análise longitudinal {% endif %}possuem natureza diagnóstica e não constituem, isoladamente, evidência de conformidade ou inconformidade. As situações específicas identificadas pela auditoria, os critérios aplicáveis e os respectivos encaminhamentos são apresentados na Seção 3.

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

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

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

Os achados resultam da avaliação das respostas de **{{ auditado.sigla }}** ao questionário iGovTI 2026 e dos documentos apresentados. A Equipe de Auditoria comparou as práticas declaradas com as evidências disponíveis, considerando a legislação aplicável e os critérios técnicos adotados na fiscalização.

{% if teve_comentarios_gestor %}
As constatações apresentadas já consideram as manifestações e os documentos encaminhados na etapa de comentários do gestor, conforme detalhado na Seção 4.
{% else %}
Na etapa de comentários do gestor, não foi identificada resposta válida da organização. Permanecem, portanto, as conclusões decorrentes das respostas e evidências anteriormente avaliadas.
{% endif %}


{% include 'achado_questao_1_estrutura_tic.md' %}

{% include 'achado_questao_2_governanca_comite_tic.md' %}

{% include 'achado_questao_3_planejamento_tic.md' %}

{% include 'achado_questao_4_capacidade_institucional_tic_si.md' %}

{% include 'achado_questao_5_gestao_servicos_tic.md' %}

{% include 'achado_questao_6_contratacoes_tic.md' %}

{% else %}

Com base na avaliação das respostas e das evidências da organização **{{ auditado.sigla }}**{% if teve_comentarios_gestor %}, bem como dos seus comentários{% endif %}, nos limites dos procedimentos executados, não foram identificadas situações que ensejassem achado individual nas Questões 1 a 6.
{% if not teve_comentarios_gestor %}

Na etapa de comentários do gestor, não foi identificada resposta válida da organização. Permanecem, portanto, as conclusões decorrentes das respostas e evidências anteriormente avaliadas.
{% endif %}

{% endif %}

{% if teve_comentarios_gestor %}

\newpage

# 4. Análise dos comentários do gestor

Esta seção apresenta a manifestação da Equipe de Auditoria sobre os comentários e documentos encaminhados pela organização. As conclusões refletem a situação verificada em **{{ comentarios_gestor.data_referencia }}**.

A análise dos comentários e dos documentos pode afastar situações inconformes, retirar os achados correspondentes ou atualizar respostas do questionário. Na reavaliação de respostas anteriormente reduzidas, a restauração fica limitada ao valor originalmente declarado.

As manifestações apresentadas nas Seções 4.1 e 4.2 tratam das situações e dos itens do relatório preliminar. Depois dessa etapa, a Equipe de Auditoria revisou e simplificou os procedimentos e recalculou os resultados dos três cenários com as mesmas regras. Por isso, os resultados finais e os impactos apresentados na Seção 4.3 podem diferir das quantidades ou das descrições constantes do relatório preliminar.

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

## 4.3. Efeitos dos comentários do gestor nos resultados finais

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

{% endif %}

{% if auditado.tem_achados %}

\newpage

{% if teve_comentarios_gestor %}
# 5. Plano de ação
{% else %}
# 4. Plano de ação
{% endif %}

Para facilitar o atendimento das propostas constantes da Seção 3, a Equipe de Auditoria apresenta modelo de plano de ação contendo os encaminhamentos mantidos após a etapa de comentários do gestor.

Para fins de elaboração do plano de ação, as medidas associadas a determinações deverão ser tratadas como providências de cumprimento, caso sejam acolhidas na decisão plenária. Quanto às recomendações, em conformidade com o art. 4º, incisos I e II, da Deliberação TCE-RJ nº 346/2024, cabe à unidade jurisdicionada avaliar a conveniência e a oportunidade de implementá-las. A eventual decisão pela não adoção deverá ser motivada, com indicação das razões consideradas e das medidas alternativas destinadas a tratar a situação que ensejou a recomendação.

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

Como a composição e os pesos do índice mudaram, a diferença entre os valores oficiais de 2023 e 2026 não indica, por si só, evolução ou retrocesso das organizações. A comparação exige considerar os itens comparáveis entre os questionários e as diferenças de escopo, respondentes e qualidade das evidências.

Para comparar os dois anos, foram calculados índices específicos, utilizando apenas as práticas comparáveis entre os questionários e uma estrutura comum de cálculo. Foram identificadas {{ comparacao_pareados_n|int }} organizações com respostas nos dois anos, equivalentes a {{ ('%0.1f' | format(comparacao_cobertura_2026_pct|float)) | replace('.', ',') }}% das organizações com respostas completas em 2026. A comparação individual foi apresentada somente para essas organizações.

Os resultados ajustados comparáveis têm finalidade exclusivamente analítica. Eles não substituem os índices oficiais de cada ciclo, não eliminam integralmente os efeitos de alterações de respondentes ou de contexto institucional e não constituem, isoladamente, evidência de conformidade ou de inconformidade.

{% if teve_ajuste %}

\newpage

# Apêndice B. Ajustes nas respostas declaradas

A Equipe de Auditoria, em busca da melhor representação do cenário atual de governança e gestão de TIC, ajustou respostas de **{{ auditado.sigla }}** ao questionário iGovTI 2026 com base na análise dos documentos apresentados.

Foram considerados os elementos enviados com o questionário e, quando apresentados, os comentários do gestor. Na reavaliação de respostas anteriormente reduzidas, a restauração ficou limitada ao valor originalmente declarado.


A tabela a seguir apresenta as respostas efetivamente alteradas nessa etapa e suas justificativas.

: Relação de respostas ajustadas {#tbl:ajuste_respostas#}

| Questão | Resposta anterior | Resposta ajustada | Justificativa |
|---|---|---|---|
{%- for ajuste in ajustes_respostas %}
| **{{ ajuste.codigo_questao }}** | {{ ajuste.de }} | {{ ajuste.para }} | {{ ajuste.justificativa }} |{% endfor %}

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

{% endif %}

{% endif %}
