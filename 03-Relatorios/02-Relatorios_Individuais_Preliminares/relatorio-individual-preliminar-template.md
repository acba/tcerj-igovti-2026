---
title: "RELATÓRIO INDIVIDUAL PRELIMINAR"
subtitle: {{ auditado.sigla }} - {{ auditado.nome }}
lang: pt-BR
figure-caption-position: above
---

# 1. Introdução

Este relatório apresenta os resultados preliminares do(a) **{{ auditado.sigla }}** relativos à Fiscalização TCE-RJ nº 18/2026 - iGovTI 2026, cujo objetivo é avaliar o grau de adoção de práticas de governança e gestão de tecnologia da informação e comunicação pelas organizações jurisdicionadas.

O trabalho foi realizado por meio de questionário eletrônico de autoavaliação de controles, método conhecido como *Control Self-Assessment* (CSA), no qual os gestores declararam a situação da organização em relação às práticas avaliadas e encaminharam evidências para corroborar as respostas prestadas. As evidências foram analisadas pela Equipe de Auditoria, nos termos definidos na matriz de planejamento e nos procedimentos de verificação aplicáveis.

O questionário do iGovTI 2026 foi estruturado para coletar informações sobre governança de TIC, gestão de TIC, segurança da informação, riscos, continuidade, serviços, contratações, estrutura organizacional, força de trabalho, soluções de TIC, projetos e temas emergentes, como inteligência artificial. A avaliação busca identificar capacidades, riscos, fragilidades, iniciativas e oportunidades de aprimoramento relacionadas ao uso institucional da tecnologia.

Os achados constantes deste relatório têm natureza preliminar e decorrem da análise das respostas declaradas, das evidências apresentadas e das regras de identificação previstas na matriz de planejamento. A manifestação do gestor poderá ser considerada pela Equipe de Auditoria antes da consolidação do relatório individual final.

# 2. Resultado do iGovTI 2026

O iGovTI 2026 é um índice composto que consolida resultados de governança e gestão de TIC em escala de 0 a 1. O componente **GovernancaTI** recebe peso de 0,477696299232863 no índice final, enquanto o componente **iGestTI** recebe peso de 0,522303700767137. Após o cálculo, a organização é classificada nos níveis de maturidade **Inexpressivo**, **Iniciando**, **Intermediário** ou **Aprimorado**.

As evidências anexadas e as justificativas textuais não entram diretamente no cálculo do índice. Elas são utilizadas pela Equipe de Auditoria para avaliar a consistência das respostas declaradas, apoiar eventuais ajustes de respostas e subsidiar a identificação de achados de auditoria.

O(A) **{{ auditado.sigla }}** obteve o **valor {{ '%0.2f' | format(iGovTI|float) }} para o iGovTI 2026**, correspondente ao nível **{{ iGovTI_maturidade }}** de maturidade.

![Distribuição dos resultados do iGovTI 2026 e posição do(a) {{ auditado.sigla }}]({{ auditado.sigla }}_comparativo_distribuicao_iGovTI.png){#fig:comparativo_distribuicao_iGovTI#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

A [@fig:componentes_igovti] apresenta a composição do resultado do(a) **{{ auditado.sigla }}** entre governança e gestão de TIC.

![Resultado do(a) {{ auditado.sigla }} por componentes do iGovTI 2026]({{ auditado.sigla }}_componentes_iGovTI.png){#fig:componentes_igovti#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

: Resultado sintético do iGovTI 2026 do(a) {{ auditado.sigla }} {#tbl:resultado_sintetico_igovti#}

| Componente | Peso no iGovTI 2026 | Valor | Nível |
|---|---:|---:|---|
| **Governança de TIC** | 0,477696299232863 | {{ '%0.2f' | format(GovernancaTI|float) }} | {{ GovernancaTI_maturidade }} |
| **Gestão de TIC** | 0,522303700767137 | {{ '%0.2f' | format(iGestTI|float) }} | {{ iGestTI_maturidade }} |
| **iGovTI 2026** | 1,000000000000000 | {{ '%0.2f' | format(iGovTI|float) }} | {{ iGovTI_maturidade }} |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

## 2.1. Questões avaliadas no relatório individual

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

## 2.2. Governança de TIC

A governança de TIC avalia a capacidade da alta administração de orientar, dirigir, monitorar e controlar o uso da tecnologia da informação, de modo alinhado aos objetivos institucionais, aos riscos relevantes e às necessidades das áreas finalísticas e administrativas.

No iGovTI 2026, a dimensão de governança consolida práticas relacionadas ao modelo de gestão de TIC, à atuação de comitês ou instâncias equivalentes, ao monitoramento do desempenho, à participação da alta administração e ao alinhamento entre decisões de TIC, estratégia organizacional, orçamento, riscos e valor público.

O(A) **{{ auditado.sigla }}** obteve o **valor {{ '%0.2f' | format(GovernancaTI|float) }} no componente Governança de TIC**, correspondente ao nível **{{ GovernancaTI_maturidade }}**.

![Resultado do componente Governança de TIC do(a) {{ auditado.sigla }}]({{ auditado.sigla }}_comparativo_distribuicao_GovernancaTI.png){#fig:comparativo_distribuicao_governancati#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

## 2.3. Gestão de TIC

A gestão de TIC avalia a capacidade da organização de planejar, executar, monitorar e aperfeiçoar processos, serviços, controles, recursos e contratações de tecnologia da informação, de forma compatível com suas necessidades institucionais.

No iGovTI 2026, o componente **iGestTI** consolida dimensões de planejamento de TIC, gestão de serviços, riscos e segurança da informação, estrutura de segurança da informação, processos de segurança da informação e gestão de soluções de TIC.

O(A) **{{ auditado.sigla }}** obteve o **valor {{ '%0.2f' | format(iGestTI|float) }} no componente Gestão de TIC**, correspondente ao nível **{{ iGestTI_maturidade }}**.

![Resultado do componente Gestão de TIC do(a) {{ auditado.sigla }}]({{ auditado.sigla }}_comparativo_distribuicao_iGestTI.png){#fig:comparativo_distribuicao_igestti#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

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
