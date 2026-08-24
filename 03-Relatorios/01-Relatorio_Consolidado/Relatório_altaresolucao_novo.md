---
title: "RELATÓRIO DE AUDITORIA GOVERNAMENTAL"
lang: pt-BR
figure-caption-position: above
toc-depth: 3
toc-title: SUMÁRIO
---

\newpage

**DADOS DA FISCALIZAÇÃO**

|  |  |
| --- | --- |
| Número da fiscalização: | 18/2026 |
| Modalidade: | AUDITORIA DE CONFORMIDADE |
| Forma de autorização: | ORDINÁRIA |
| Ato originário: | PROCESSO TCE-RJ nº 303.389-0/2025 |
| Jurisdicionados: | 84 organizações estaduais (AGENERSA, AGERIO, AGETRANSP, ALERJ, CEASA, CECIERJ, CEDAE, CEHAB, CENTRAL, CEPERJ, CGE, CODERTE, CODIN, DEGASE, DERRJ, DETRAN, DETRO, DPGE, DRM, EMATER, EMOP, FAETEC, FAPERJ, FIA, FIPERJ, FLXIII, FMIS, FS, FSC, FTM, FUNARJ, GSI, IEEA, INEA, IOERJ, IPEM, IRM, ISP, ITERJ, IVB, JUCERJA, LOTERJ, MPERJ, PESAGRO, PGE, PROCON, PRODERJ, RIOPREVIDENCIA, RIOTRILHOS, RJPREV, SEAP, SEAPPA, SECC, SECEC, SECID, SECTI, SEDCON, SEDEC, SEDEICS, SEDSDH, SEEDUC, SEEL, SEENEMAR, SEFAZ, SEGOV, SEHAB, SEIJES, SEINFRA, SEPLAG, SEPM, SEPOL, SERGB, SES, SESP, SETD, SETRAB, SETRANS, SETUR, SUDERJ, TCE-RJ, TJRJ, TURISRIO, UENF e UERJ) e 35 prefeituras municipais (Angra dos Reis, Araruama, Armação dos Búzios, Arraial do Cabo, Barra do Piraí, Belford Roxo, Cabo Frio, Campos dos Goytacazes, Casimiro de Abreu, Duque de Caxias, Guapimirim, Itaguaí, Japeri, Macaé, Magé, Maricá, Mesquita, Niterói, Nova Friburgo, Nova Iguaçu, Paraty, Petrópolis, Porto Real, Quatis, Queimados, Quissamã, Rio das Ostras, São Gonçalo, São João da Barra, São João de Meriti, São Pedro da Aldeia, Saquarema, Seropédica, Teresópolis e Volta Redonda). |
| Objetivo da fiscalização: | Avaliar o grau de adoção dos jurisdicionados às boas práticas de governança e gestão de TI. |
| Ofícios de apresentação: | AUD/SGE/GAP 3232/25 a 3241/25, 3243/25 a 3268/25 todos de 06/08/2025. |
| Período abrangido: | janeiro/24 a julho/26 |
| Período de execução: | 02/02/26 a 16/07/26 |
| Equipe: | Augusto César Benvenuto de Almeida, mat. 02/4823;  João Paulo de Freitas Ramirez, mat. 02/4820 |
| Supervisão: | Bruno Mattos Souza de Souza Melo, mat. 02/4258 |

\newpage

::: {.toc}
:::

\newpage

# LISTA DE ANEXOS

| **ANEXOS** | |
| --- | --- |
| **Documento nº** | **Descrição** |
| AN01 | **Ofícios de Apresentação**  (arquivo digital “*AN01 - Ofícios de Apresentação.zip*”) |
| AN02 | **Matriz de Planejamento**  (arquivo digital “AN02 - Matriz de Planejamento.docx”) |
| AN03 | **Questionário iGovTI 2026, metodologia e resultado**  (arquivo digital “AN03 – Questionário iGovTI 2026 e informações.zip”) |
| AN04 | **Evidências** (arquivo digital “AN04 – Evidências dos achados.docx”) |
| AN05 | **Respostas aos Questionários (avaliação de respostas e comentários do gestor) e planilhas de ajustes**  (arquivo digital “*AN05 – Respostas aos questionários e ajustes.zip*”) |
| AN06 | Matriz de Achados  (arquivo digital “AN06 – Matriz de Achados.docx”) |
| AN07 | **Impacto da avaliação das evidências**  (arquivo digital “AN07 – Impacto da avaliação das evidências.docx”) |
| AN08 | **Avaliação dos comentários do gestor**  (arquivo digital “AN08 – Avaliação dos comentários do gestor.docx”) |
| AN09 | **Cenário de utilização de inteligência artificial no ERJ**  (arquivo digital “AN09 – Cenário de utilização de IA no ERJ.docx”) |
| AN10 | **Comunicações da fiscalização e registros de ciência dos não respondentes** (arquivo digital “AN10 – Comunicações da fiscalização e registros de ciência dos não respondentes.pdf”) |
| AN11 | **Análise longitudinal do iGovTI 2023–2026**  (arquivo digital “analise-estatistica-longitudinal-igovti-2023-2026.docx”) |
| AN12 a AN124 | **Informações das organizações (TSIDs, respostas, evidências enviadas, comentários do gestor e relatório individual)**  *(arquivos digitais “ANXX – [ORGANIZAÇÃO].zip”)* |



\newpage

# 1. RESUMO

#### O que o TCE-RJ fiscalizou?

O TCE-RJ realizou auditoria de conformidade, com contornos operacionais, para avaliar a adoção de boas práticas de governança e gestão de TIC nas organizações públicas do Rio de Janeiro, traçar um panorama de maturidade e analisar a evolução em relação ao cenário mensurado em 2023.

A fiscalização abrangeu 119 organizações, sendo 35 prefeituras e 84 organizações estaduais de diferentes poderes e naturezas jurídicas. Destas, 113 responderam ao questionário e integraram o cálculo do iGovTI e os achados consolidados. As outras 6 foram classificadas como não respondentes e tratadas separadamente[^nao_respondentes_obstrucao].

A avaliação examinou a estrutura e a governança de TIC, o planejamento, a força de trabalho, a gestão de serviços e as contratações. A metodologia combinou questionário eletrônico de autoavaliação, análise documental, procedimentos de auditoria, cálculo do iGovTI 2026 e classificação em quatro níveis de maturidade (Inexpressivo, Iniciando, Intermediário e Aprimorado). A comparação longitudinal considerou as 68 organizações presentes em 2023 e 2026.

Os resultados finais apresentados neste relatório incorporam os ajustes decorrentes da análise documental e dos comentários dos gestores.

#### O que o TCE-RJ encontrou?

A fiscalização constatou cenário de baixa maturidade e fragilidades recorrentes na governança e gestão de TIC fluminense. A média do iGovTI 2026 foi de 0,189 (mediana de 0,136), com 87,6% (99 de 113 respondentes) das organizações nos níveis mais baixos (53,1% Inexpressivo e 34,5% Iniciando). Apenas 9 atingiram o nível Intermediário e 5 o Aprimorado.

Na comparação das 68 organizações presentes nos dois ciclos, as respostas declaradas após os ajustes iniciais indicam evolução: a média comparável passou de 0,180, em 2023, para 0,248, em 2026, com aumento em 43 organizações e redução em 25. Após a avaliação das evidências e dos comentários dos gestores, a média de 2026 ficou em 0,189, com aumento em 32 organizações e redução em 36. Assim, houve melhora no cenário autodeclarado, mas os resultados finais não permitem afirmar que ocorreu melhora ou piora geral. A Estrutura de Segurança da Informação foi o único componente com melhora confirmada nos dois cenários.[^comparacao_longitudinal_cenarios]

[^comparacao_longitudinal_cenarios]: Em 2026, foram solicitadas e avaliadas evidências para todas as práticas passíveis de comprovação. Em 2023, embora também tenha havido análise pela equipe, a exigência de anexos e o exame direto abrangeram conjunto menor de práticas. O cenário final de 2026 possui, portanto, maior grau de verificação. O cenário-base aproxima a comparação das respostas declaradas, mas não comprova, por si só, a efetiva adoção das práticas. A metodologia, os cálculos e as demais ressalvas constam do Anexo AN11.

Foram consolidados seis achados de auditoria:

- **Achado 1 – Estrutura de TIC:** 66 organizações (58,4%) apresentam fragilidades na formalização, nas atribuições ou no posicionamento da função de TIC.
- **Achado 2 – Governança de TIC:** 101 organizações (89,4%) apresentam ausência de objetivos, indicadores ou metas ou fragilidades na instituição e atuação do comitê de TIC.
- **Achado 3 – Planejamento de TIC:** 99 organizações (87,6%) apresentam fragilidades quanto ao processo de planejamento, à aprovação, ao alinhamento, à integração com orçamento e contratações ou ao acompanhamento do plano.
- **Achado 4 – Capacidade institucional:** 109 organizações (96,5%) apresentam fragilidades no dimensionamento, na atribuição formal de cargos ou funções ou na preservação de capacidade interna em modelos terceirizados.
- **Achado 5 – Gestão de serviços de TIC:** 113 organizações (100,0%) apresentam fragilidades na gestão de serviços, abrangendo catálogo de serviços, níveis de serviço, ativos, configuração ou tratamento de incidentes.
- **Achado 6 – Contratações de TIC:** 103 organizações (91,2%) apresentam fragilidades na governança técnica da fase preparatória das contratações de TIC.

Entre as manifestações individualizadas recebidas na etapa de comentários do gestor, 84,0% expressaram concordância com as situações apontadas no diagnóstico preliminar. A análise das manifestações e das evidências complementares resultou em 160 ajustes distribuídos por 41 organizações, com impacto na remoção de situações inconformes e achados ou ajustes nas notas que compõem o iGovTI em 34 organizações. O índice foi elevado em 23 organizações. Os ajustes corrigiram conclusões específicas, mas não alteraram de forma ampla o diagnóstico consolidado da fiscalização.

#### Qual é a proposta de encaminhamento?

Propõem-se determinações e recomendações individualizadas nos relatórios das organizações avaliadas, complementadas por recomendações transversais destinadas ao aprimoramento da governança e da gestão de TIC, organizadas em cinco eixos:

* **Estrutura e Governança:** formalização da TI e instituição ativa de comitês gestores multidisciplinares.
* **Planejamento:** elaboração e revisão do PDTI com vinculação direta ao orçamento anual.
* **Recursos Humanos:** dimensionamento de equipes e planos para reduzir a dependência crítica de terceirizados.
* **Serviços e Ativos:** instituição de catálogo de serviços, inventário de ativos e gestão de incidentes.
* **Contratações:** padronização do fluxo de contratações e obrigatoriedade de anuência técnica prévia da área de TIC.

Os benefícios esperados da adoção dessas medidas incluem o fortalecimento da governança e da gestão de TIC, o aprimoramento do planejamento, da capacidade institucional, da gestão de serviços e das contratações e a elevação gradual do nível de maturidade das organizações avaliadas.

#### Quais os próximos passos?

O Tribunal poderá acompanhar a implementação por meio de monitoramento ou de avaliações futuras, nos termos da Resolução TCE-RJ nº 422/2023, com foco na execução dos planos de ação registrados em processo administrativo eletrônico e na institucionalização das práticas e dos controles objeto dos encaminhamentos.

[^nao_respondentes_obstrucao]: Para as organizações que não apresentaram resposta válida ao questionário eletrônico, será sugerida a abertura de processos apartados para apuração das circunstâncias da ausência de resposta, assegurada aos responsáveis a oportunidade de apresentar razões de defesa.

\newpage

# 2. INTRODUÇÃO

Trata-se de auditoria de conformidade, com contornos operacionais, autorizada no âmbito do processo TCE-RJ nº 303.389-0/2025. O trabalho tem por objeto as práticas de governança e gestão de tecnologia da informação adotadas pelas organizações da Administração Pública Estadual e Municipal do Estado do Rio de Janeiro.

Os trabalhos foram conduzidos em conformidade com as Normas Brasileiras de Auditoria do Setor Público (NBASP) e de acordo com os padrões estabelecidos no Manual de Auditoria deste Tribunal de Contas do Estado do Rio de Janeiro (TCE-RJ).

## 2.1 Antecedentes

A presente fiscalização insere-se no conjunto de ações de controle externo planejadas por esta Corte de Contas para avaliar e induzir a maturidade da governança e da gestão de Tecnologia da Informação e Comunicação (TIC) sob sua jurisdição.

Um importante marco nesse tema foi o levantamento realizado no âmbito do Processo nº 105.096-3/2020, que avaliou aspectos-chave da governança de TI das principais organizações da esfera estadual que utilizam soluções de tecnologia da informação, mensurando suas práticas pelo Índice de Governança e Gestão de TI (iGovTI).

Posteriormente, no ano de 2023, o Tribunal realizou duas auditorias de conformidade com o escopo de verificar as políticas de governança e gestão de TI como norteadoras das contratações de TIC. A primeira delas, autuada no Processo nº 205.089-9/2023, avaliou a maturidade dessas práticas em nível municipal, alcançando as prefeituras de Maricá, Rio das Ostras, Saquarema e Volta Redonda. A segunda, processada sob o nº 109.009-4/2023, concentrou-se nas organizações que compõem o Sistema Estadual de Tecnologia da Informação e Comunicação (SETIC) do Executivo Estadual.

Paralelamente às avaliações gerais de governança, este Tribunal realizou fiscalizações dedicadas a aspectos específicos de segurança. Nesse sentido, as auditorias de conformidade dos Processos nº 105.895-5/2024 e 107.097-5/2025 verificaram a adoção de controles e a aderência das organizações públicas estaduais às boas práticas de segurança da informação, como a ISO 27001/2022 e os Controles CIS v8.

Em razão de a segurança da informação e a segurança cibernética terem sido objeto de fiscalizações específicas recentes a presente auditoria não formulou questão de auditoria nem achado autônomo destinado a avaliar a implementação ou a efetividade dos controles e processos específicos desses temas.

## 2.2 Objetivo e escopo

O objeto do presente trabalho consiste nas práticas de governança e gestão de TI de 119 jurisdicionados estaduais e municipais do Estado do Rio de Janeiro.

Os objetivos específicos da fiscalização compreendem: mensurar o grau de adoção das práticas de governança e gestão de TIC, expresso pelo índice de maturidade iGovTI 2026; analisar sua evolução em relação a 2023, considerando as organizações avaliadas nos dois ciclos e uma base comparável de práticas; e identificar fragilidades relevantes e situações inconformes na governança e na gestão de TIC das organizações avaliadas, propondo encaminhamentos para o aprimoramento dos controles internos.

Para orientar os exames, foi formulada a seguinte questão geral de auditoria: **Qual é o grau de adoção das práticas de governança e gestão de TIC das organizações avaliadas, segundo o iGovTI 2026, e quais fragilidades relevantes estão presentes?**

A questão geral foi desdobrada em seis questões específicas, que estruturaram os procedimentos de auditoria e a consolidação dos achados:

* **Q1 – Estrutura de TIC:** A organização possui área, unidade, setor ou função de TIC formalmente instituída, com atribuições definidas e posicionamento organizacional compatível com suas responsabilidades institucionais?
* **Q2 – Governança e Comitê de TIC:** A organização possui mecanismos básicos de governança de TIC, incluindo objetivos, indicadores e metas, bem como Comitê de TIC ou instância equivalente formalmente instituída e atuante?
* **Q3 – Planejamento de TIC:** A organização utiliza o planejamento de TIC como instrumento efetivo de gestão, com processo formal, plano vigente, aprovação competente, alinhamento institucional, integração com orçamento e contratações e acompanhamento periódico?
* **Q4 – Capacidade institucional de TIC e segurança da informação:** A organização dispõe de mecanismos mínimos para estruturar e dimensionar sua força de trabalho de TIC e segurança da informação, formalizar funções e preservar capacidade interna nos modelos de operação predominantemente terceirizados?
* **Q5 – Gestão de Serviços de TIC:** A organização adota práticas mínimas de gestão de serviços de TIC, incluindo catálogo de serviços, níveis de serviço, inventário de ativos, gestão de configuração e tratamento de incidentes, de modo a assegurar eficiência, rastreabilidade e qualidade dos serviços prestados?
* **Q6 – Contratações de TIC:** A organização adota processo formal e padronizado para a fase preparatória das contratações de TIC, com responsabilidades definidas, análise técnica pela área de TIC e alinhamento aos instrumentos de planejamento?

Cada questão específica corresponde ao achado de mesmo número apresentado na Seção 4.3. A cadeia de rastreabilidade do trabalho é completada pelos critérios sintetizados na Seção 2.4, pelos procedimentos e pelo tratamento das evidências descritos na Seção 2.5 e detalhados nos anexos, e pelos encaminhamentos consolidados no Capítulo 7 e individualizados nos relatórios das organizações auditadas.

O escopo abrangeu 119 organizações, sendo 84 organizações estaduais de diferentes poderes e naturezas jurídicas e 35 prefeituras municipais. Desse total, 113 (cento e treze) apresentaram resposta válida ao questionário e foram consideradas nos resultados do iGovTI e nos achados consolidados. As seis organizações sem resposta válida foram tratadas como não respondentes. O período de execução dos trabalhos de campo ocorreu entre fevereiro e julho de 2026.

## 2.3 Limitações

A principal limitação metodológica do trabalho reside no caráter predominantemente autodeclaratório das informações fornecidas pelas organizações por meio do questionário eletrônico.

Visando mitigar os riscos de assimetria informacional, a Equipe de Auditoria requereu dos auditados o envio de evidências documentais correspondentes às respostas prestadas. A análise limitou-se ao confronto das declarações com os documentos encaminhados, sem a realização de testes locais de validação de controles.

A limitação não impediu a execução dos procedimentos planejados, mas restringe as conclusões à adoção declarada e documentalmente demonstrada das práticas, sem assegurar sua efetividade operacional.

A não aceitação de determinada evidência ou de esclarecimento apresentado pelo gestor não significa, necessariamente, que a atividade declarada inexista. Significa que, considerados o detalhamento e a documentação disponibilizados, o escopo definido e os meios operacionais previstos para esta fiscalização, a Equipe de Auditoria não obteve elementos suficientes e adequados para assegurar a prática. Entrevistas adicionais, inspeções em sistemas, observação direta ou testes locais poderiam produzir evidência complementar, mas não integraram os procedimentos executados.

Essa limitação recomenda que a diferença entre a autodeclaração e o resultado após a avaliação documental e dos comentários do gestor seja interpretada como diferença de asseguração documental, e não, isoladamente, como prova de inexistência da atividade.

## 2.4 Critérios aplicados

Os exames fundamentaram-se em normas legais aplicáveis, jurisprudência e referenciais de controle externo, padrões técnicos de governança e gestão de TIC e boas práticas reconhecidas, conforme a natureza de cada questão de auditoria.

Entre os principais critérios, destacam-se a Constituição Federal, a Lei nº 14.133/2021, o Acórdão TCE-RJ nº 44.490/2024-PLEN, os Acórdãos TCU nº 1.411/2014-Plenário e nº 2.342/2016-Plenário, o COBIT 2019, o ITIL 4 e a ABNT NBR ISO/IEC 20000-2:2021. O Decreto Federal nº 12.198/2024, a Portaria SGD/ME nº 778/2019 e a Instrução Normativa SGD/ME nº 94/2022 foram utilizados como referenciais de boa prática quando não vinculantes ao jurisdicionado avaliado.

Os referenciais técnicos, a jurisprudência de outros órgãos de controle e as boas práticas sem caráter vinculante foram utilizados para caracterizar as práticas esperadas e subsidiar recomendações, não constituindo, isoladamente, fundamento para determinações ou sanções, enquanto as determinações foram fundamentadas em deveres legais aplicáveis ou em deliberações do TCE-RJ.

## 2.5 Metodologia utilizada

A metodologia combinou quatro frentes de trabalho: questionário eletrônico de autoavaliação, análise das evidências encaminhadas, cálculo do iGovTI 2026 e execução de procedimentos de auditoria para identificação de achados. O objetivo foi produzir um diagnóstico quantitativo de maturidade e, ao mesmo tempo, verificar a consistência das práticas declaradas pelos gestores.

A sequência metodológica adotada está sintetizada na [@fig:fluxo_metodologia_igovti_2026] e detalhada nos parágrafos seguintes.

Na fase de planejamento, a Equipe de Auditoria elaborou questionário estruturado com base nas métricas de iGovTI do Tribunal de Contas da União (TCU) dos anos de 2021 e 2024. O instrumento foi adaptado ao contexto dos jurisdicionados do TCE-RJ e estruturado para avaliar temas essenciais de governança e gestão de TIC, como segurança da informação, gestão de riscos, continuidade de negócios, serviços de tecnologia, contratações de TIC, estrutura e força de trabalho, desenvolvimento de soluções, gestão de projetos e uso de inteligência artificial.

O questionário foi disponibilizado em meio eletrônico, por meio do sistema *LimeSurvey*, com links individualizados encaminhados às organizações. A avaliação adotou o método de autoavaliação de controles (*Control Self-Assessment* — CSA): cada gestor informou o nível de adoção das práticas avaliadas e, quando aplicável, anexou documentos para comprovar a resposta. Dos 119 jurisdicionados abrangidos no escopo, 113 apresentaram resposta válida e integraram as análises estatísticas e os achados consolidados. Os seis casos sem resposta válida foram classificados como não respondentes.

![Fluxo metodológico da fiscalização iGovTI 2026](fluxo_metodologia_igovti_2026.png){#fig:fluxo_metodologia_igovti_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

Após a coleta, a base de respostas passou por saneamento e ajustes registrados pela Equipe de Auditoria, incluindo retificações solicitadas pelos auditados, correções de inconsistências e tratamento de problemas identificados no questionário. Essa base constitui o cenário-base de autodeclaração: preserva a visão declarada pelo auditado, após os ajustes iniciais, mas ainda sem a influência dos juízos da Equipe de Auditoria sobre a suficiência das evidências.

Em seguida, as respostas e evidências foram analisadas para verificar se a documentação apresentada sustentava as práticas declaradas. Quando a evidência não comprovou a resposta afirmada, a resposta foi ajustada ou considerada não conforme, conforme a regra aplicável ao item avaliado. O recálculo do índice e a reexecução dos procedimentos sobre essa base formaram o cenário pós-avaliação de evidências. Depois da apreciação dos comentários dos gestores e das evidências complementares aceitas, novo recálculo e nova execução formaram o cenário pós-comentários do gestor, adotado para as conclusões e os encaminhamentos finais.

Com a base ajustada pós-avaliação dos comentários do gestor, foi calculado o iGovTI 2026. O índice é medido em escala de 0 a 1. Para calcular a nota, as respostas categóricas foram convertidas em coeficientes numéricos: Não adota = 0,00; Há decisão formal ou plano aprovado para adotá-lo = 0,05; Adota em menor parte = 0,15; Adota parcialmente = 0,50; e Adota em maior parte ou totalmente = 1,00. Nas questões com itens de detalhamento, a pontuação da questão principal sofre deduções proporcionais aos itens não atendidos. Depois disso, os valores são consolidados por agregação ponderada.

O índice final é composto por dois blocos principais, conforme sintetizado na [@fig:composicao_igovti_2026]: Governança de TIC, com peso de 47,8%, formado por quatro questões de agregação direta; e Gestão de TIC (iGestTI), com peso de 52,2%, estruturado em seis dimensões operacionais que consolidam vinte questões principais ponderadas.

![Composição do iGovTI 2026](igovti_2026_composicao_infografico.png){#fig:composicao_igovti_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

Com base na pontuação consolidada, cada organização com resposta válida foi classificada em um de quatro níveis de maturidade: Inexpressivo (0,00 ≤ iGovTI < 0,15), Iniciando (0,15 ≤ iGovTI < 0,40), Intermediário (0,40 ≤ iGovTI < 0,70) e Aprimorado (0,70 ≤ iGovTI ≤ 1,00).

A apuração do iGovTI permitiu comparar o grau de adoção das práticas avaliadas entre as organizações e subsidiou a comparação longitudinal com o ciclo de 2023, mediante estrutura ajustada de itens comparáveis.

Paralelamente ao cálculo do índice, a Equipe de Auditoria executou os procedimentos definidos na matriz de planejamento. Para o cenário-base, os resultados são indicativos da autodeclaração, e não achados definitivos, pois ainda não incorporam a validação probatória. No cenário pós-avaliação de evidências, os procedimentos identificaram situações inconformes preliminares, agrupadas nos respectivos achados. No cenário pós-comentários do gestor, a reexecução consolidou os achados, as situações inconformes, as evidências e as propostas de encaminhamento de cada organização avaliada.

Com base no cenário pós-avaliação de evidências, foram elaborados os relatórios individuais preliminares que foram remetidos aos auditados para etapa de comentários do gestor. Esses relatórios apresentaram a nota do iGovTI, a posição relativa no conjunto de jurisdicionados, os achados identificados, as situações encontradas, os ajustes decorrentes da análise documental e o plano de ação proposto. Para os não respondentes, foi registrada a ausência de resposta válida.

Depois da apreciação dos comentários e das evidências complementares, a Equipe de Auditoria recalculou os resultados, reexecutou os procedimentos e elaborou os relatórios individuais finais. Os dados e as conclusões resultantes dessa etapa foram consolidados neste relatório.

## 2.6 Benefícios estimados

Espera-se que a implementação dos encaminhamentos decorrentes desta fiscalização contribua para o aprimoramento da governança e da gestão de TIC nas organizações avaliadas, especialmente quanto à estrutura, ao planejamento, à capacidade institucional, à gestão de serviços e às contratações de tecnologia.

A efetiva obtenção desses benefícios dependerá das medidas adotadas pelas organizações e poderá ser verificada em ações posteriores de controle.

\newpage

# 3. VISÃO GERAL DO OBJETO

O objeto desta fiscalização são as práticas de governança e de gestão de Tecnologia da Informação e Comunicação (TIC) adotadas pelas organizações da Administração Pública Estadual e Municipal do Estado do Rio de Janeiro sob jurisdição deste Tribunal. A TIC apoia a execução de políticas públicas, a prestação de serviços, a gestão de informações e a realização de contratações. Portanto, a forma como cada organização direciona, estrutura, planeja, opera e controla a TIC impacta diretamente o alcance de seus objetivos e a adequada prestação dos serviços públicos.

O escopo abrangeu 119 organizações jurisdicionadas, sendo 84 organizações estaduais de diferentes poderes e naturezas jurídicas e 35 prefeituras municipais. Desse total, 113 apresentaram resposta válida ao questionário e integraram as análises de maturidade e os achados consolidados. As outras 6 foram classificadas como não respondentes, conforme registrado na Introdução.

A presente seção descreve as características do objeto necessárias à compreensão do relatório: o conteúdo das práticas avaliadas, os arranjos institucionais mais relevantes no Estado do Rio de Janeiro, os instrumentos de planejamento de TIC e a forma como a mensuração da maturidade tem sido realizada por Tribunais de Contas. Os resultados da avaliação constam do capítulo seguinte.

## 3.1. Governança e gestão de TIC

No setor público, a governança de TIC compreende o conjunto de estruturas, processos e práticas pelos quais a alta administração avalia as necessidades institucionais e das partes interessadas, define a direção do uso da tecnologia e monitora o desempenho e a conformidade em relação a essa direção. Seu propósito é assegurar que a TIC gere valor público, mitigue riscos relevantes e permaneça alinhada aos objetivos organizacionais.

A ABNT NBR ISO/IEC 38500:2025 estabelece modelo de governança de TIC estruturado em três atividades — avaliar, dirigir e monitorar —, ilustradas na [@fig:modelo_governanca_ti_iso_38500]. Avaliar consiste em compreender o ambiente interno e externo e o grau em que a organização é apoiada e habilitada pelo uso de TIC. Dirigir consiste em definir como a organização deve ser apoiada e habilitada pelo uso adequado da TIC, inclusive por meio de priorizações e decisões. Monitorar consiste em verificar se o que foi planejado e direcionado está sendo executado e se os resultados e a conformidade permanecem adequados.

![Modelo de Governança de TIC segundo a ABNT NBR ISO/IEC 38500](modelo_governanca_ti_iso_38500.png){#fig:modelo_governanca_ti_iso_38500#}
<div custom-style="FonteImagem">(Fonte: elaboração própria, adaptado da ABNT NBR ISO/IEC 38500:2025)</div>

A gestão de TIC, por sua vez, é a função encarregada de planejar, construir, executar e acompanhar processos e serviços em alinhamento com a direção estabelecida pela governança. Enquanto a governança define e supervisiona o rumo, a gestão realiza a operação e a entrega. As instâncias de gestão podem ser táticas — por exemplo, a área de TIC — ou operacionais, quando executam processos de apoio ou finalísticos dependentes de tecnologia.

No âmbito desta fiscalização, a distinção entre governança e gestão é operacionalmente relevante: o iGovTI 2026 mensura, em blocos distintos, o grau de adoção de práticas de direção e de práticas operacionais, e os achados de auditoria examinaram fragilidades em estrutura de TIC, governança, planejamento, capacidade institucional, gestão de serviços e contratações de TIC.

## 3.2. Mecanismos, princípios e responsabilidades na Governança Pública

A governança pública opera, entre outras perspectivas, por meio de mecanismos de liderança, estratégia e controle. A liderança compreende práticas de integridade, competência, responsabilidade e motivação exercidas pela alta administração. A estratégia envolve a definição de objetivos, diretrizes e planos, bem como o alinhamento entre partes interessadas. O controle compreende processos estruturados para gerenciar riscos e assegurar a execução ordenada, ética, eficiente e eficaz das atividades.

Esses mecanismos, previstos no Decreto Federal nº 9.203/2017 para a administração pública federal, são adotados neste trabalho como referencial conceitual de boa governança, em conjunto com o Referencial Básico de Governança do Tribunal de Contas da União (TCU). Não possuem eficácia normativa vinculante sobre os jurisdicionados estaduais e municipais do Estado do Rio de Janeiro.

No mesmo sentido, os princípios de governança pública do art. 3º do Decreto nº 9.203/2017 — capacidade de resposta, integridade, confiabilidade, melhoria regulatória, prestação de contas e responsabilidade, e transparência — orientam a leitura do objeto sob a perspectiva do interesse público e da *accountability*. Complementarmente, o Referencial Básico de Governança do TCU reforça a necessidade de tratamento equitativo e participativo das partes interessadas.

A alta administração é a principal responsável pela governança, inclusive da TIC. Cabe a ela estabelecer políticas e objetivos, decidir sobre prioridades e recursos e acompanhar resultados. Na área de TIC, a instituição de comitê de TIC ou instância equivalente, compatível com o porte e a complexidade da organização, constitui prática relevante para priorizar investimentos, integrar áreas de negócio e técnica e assegurar que a TIC suporte os objetivos institucionais.

Além dos referenciais de governança pública, os exames desta auditoria fundamentam-se em padrões consagrados de governança e gestão de TIC — em especial o *COBIT 2019*, o *ITIL 4* e a ABNT NBR ISO/IEC 38500:2025 —, utilizados como critérios técnicos de avaliação das práticas.

## 3.3. Planejamento de TIC e integração entre governança e gestão

A integração entre governança e gestão materializa-se, de forma recorrente, em instrumentos de planejamento de TIC. O Plano Estratégico de TIC e o Plano Diretor de TIC, usualmente referidos pelas siglas PETI e PDTI — ou por denominações equivalentes, como PDTIC e PEDTIC —, vinculam necessidades, prioridades, ações, prazos, recursos e riscos de tecnologia aos objetivos organizacionais.

O plano de TIC, quando aprovado pela alta administração e efetivamente utilizado, deve conter, no mínimo, o inventário de necessidades, metas e ações, a dimensão orçamentária e a gestão de riscos associados. Por meio desses instrumentos, a governança exerce o papel de direcionamento, e a gestão dispõe de referência para a execução, o monitoramento e a priorização de contratações e iniciativas de TIC.

A experiência de fiscalizações anteriores deste Tribunal indica que a mera existência formal de plano de TIC não assegura, por si só, o uso do instrumento como base de decisão. São aspectos críticos a qualidade do planejamento, a vinculação com orçamento e contratações, a atuação efetiva de instâncias colegiadas e a atualização periódica do plano. Esses elementos orientaram a priorização do tema de planejamento na presente fiscalização e a formulação dos procedimentos relacionados ao Achado 3.

## 3.4. Arranjos institucionais e diversidade do universo auditado

Os jurisdicionados abrangidos por este trabalho adotam arranjos distintos de governança e gestão de TIC, conforme a esfera, o poder, o porte e a natureza jurídica da organização. Não há um único modelo normativo aplicável ao conjunto das 119 organizações. A fiscalização considerou essa heterogeneidade ao adotar questionário comum de práticas, critérios técnicos de referência e análise proporcional à realidade declarada e documentada por cada organização.

No Poder Executivo do Estado do Rio de Janeiro, o Decreto Estadual nº 48.997/2024 define o modelo atual de gestão e governança de TIC e organiza o Sistema Estadual de Tecnologia da Informação e Comunicação (SETIC). O SETIC compreende o conjunto de recursos humanos, tecnológicos e de equipamentos voltados ao estabelecimento e à implementação de políticas de informação e comunicação pública, estruturando-se em dois níveis: Direção Geral, sob competência do PRODERJ; e nível setorial, representado pelas assessorias de informática, ou setores equivalentes, dos órgãos da administração direta e indireta.

No modelo do SETIC, o PRODERJ exerce competências de coordenação e supervisão do Sistema, normatização de aspectos de TIC, elaboração e disponibilização de atas de registro de preços para contratação de bens e serviços de TIC, bem como avaliação e consolidação dos planos de TIC dos órgãos do nível setorial.

No Poder Judiciário, a Resolução CNJ nº 370/2021, que estabelece a Estratégia Nacional de Tecnologia da Informação e Comunicação do Poder Judiciário (ENTIC-JUD), dispõe que cada órgão elabore e mantenha o Plano Diretor de Tecnologia da Informação e Comunicação (PDTIC), alinhado ao Planejamento Estratégico Institucional, ao Planejamento Estratégico Nacional do Poder Judiciário e à própria ENTIC-JUD.

Em relação aos municípios e às demais organizações não abrangidas por esses marcos específicos, a ausência de modelo setorial único não dispensa a adoção de práticas básicas de estrutura, governança, planejamento, gestão de pessoas, serviços e contratações de TIC. Nesses casos, o parâmetro de avaliação desta fiscalização são as boas práticas de referência e a estrutura do iGovTI 2026, consideradas as evidências apresentadas e o porte da organização.

Fiscalizações anteriores deste Tribunal, com escopos e conjuntos de auditados distintos — em especial a avaliação de quatro prefeituras no Processo TCE-RJ nº 205.089-9/2023 e a avaliação de organizações do SETIC no Processo TCE-RJ nº 109.009-4/2023 —, já haviam registrado heterogeneidade de práticas e fragilidades recorrentes em governança e gestão de TIC. A presente auditoria, com base ampliada de 113 organizações respondentes, apresenta no capítulo 4 o diagnóstico consolidado atualizado.

## 3.5. Relevância do objeto e riscos associados

A relevância da governança e da gestão de TIC decorre do papel da tecnologia na continuidade dos serviços públicos, na proteção de informações, na eficiência do gasto e na qualidade das contratações. Fragilidades na formalização da área de TIC, na direção pela alta administração, no planejamento, na capacidade de pessoal, na gestão de serviços e ativos e no controle das contratações elevam riscos de desperdício, de dependência crítica de terceiros, de interrupção de serviços, de baixa entrega de valor e de decisões de investimento desalinhadas das prioridades institucionais.

Estudos e fiscalizações de referência reforçam a materialidade desses riscos no contexto fluminense. No iGovTI do IEGM 2024, mensuração distinta da adotada neste trabalho, a maior parte dos municípios do Estado do Rio de Janeiro apresentou baixa incidência declarada de PDTI/PDTIC, em contraste com maior presença declarada de elementos de presença digital.

O censo de acompanhamento de contratações de TIC da Coordenadoria de Auditoria de Tecnologia da Informação (CAD-TI), de 2025, apontou, em bases próprias e com caráter indicativo, fragilidades recorrentes no papel da TI no planejamento e na fiscalização contratual, sobretudo na esfera municipal. As auditorias deste Tribunal sobre contratações de TIC no SETIC e sobre segurança da informação e segurança cibernética, realizadas entre 2024 e 2025, aprofundaram, em escopos específicos, problemas de planejamento, de capacidade instalada e de formalização de controles de segurança.

Esses elementos não substituem os resultados da presente fiscalização; servem para contextualizar o objeto e a priorização dos temas avaliados. O diagnóstico desta auditoria fundamenta-se nas respostas ao questionário iGovTI 2026, na análise das evidências documentais e na execução dos procedimentos de auditoria.

## 3.6. Mensuração da governança e gestão de TIC pelos Tribunais de Contas

Desde 2010, o TCU avalia a governança e a gestão de TIC na administração pública federal por meio do iGovTI, índice baseado em questionário específico sobre práticas do tema. Em edições mais recentes, o iGovTI integra o iESGo, instrumento mais amplo de avaliação de governança e gestão públicas.

Outros Tribunais de Contas também têm utilizado questionários, levantamentos e índices para diagnosticar a maturidade de TIC em suas jurisdições. O Tribunal de Contas de Pernambuco formalizou a apuração periódica do iGovTI e, em 2025, utilizou base derivada do questionário do TCU de 2021, com adaptações para restringir o escopo à área de TIC.[^referencia_igovti_tce_pe]

O Tribunal de Contas do Estado do Rio Grande do Sul realizou, em 2025, levantamento de governança de TI voltado aos executivos municipais, com diagnóstico estruturado em dimensões como estrutura/equipe de TI e governança de TI.[^referencia_diagnostico_tce_rs] No âmbito do IEGM, há também um índice denominado iGovTI, voltado a aspectos de tecnologia, governo digital e transparência municipal, com questionário, escala e objetivos próprios.[^referencia_iegm_igovti]

[^referencia_igovti_tce_pe]: O iGovTI-TCE-PE é um levantamento de autoavaliação instituído em 2023, com periodicidade bienal, destinado a organizações estaduais e municipais de Pernambuco. O instrumento utiliza questões extraídas do iGG 2021 do TCU, calcula o índice e seus componentes em escala de zero a um e produz relatórios para apoio ao aprimoramento da governança e da gestão de TI. O próprio TCE-PE ressalva que os resultados decorrem das respostas das organizações e não representam medida precisa quando não há verificação da totalidade das informações fornecidas. TRIBUNAL DE CONTAS DO ESTADO DE PERNAMBUCO. *Sobre o iGovTI-TCE-PE*. Disponível em: <https://www.tcepe.tc.br/internet/index.php/sobre-o-igovti-tce-pe>. Acesso em: 12 ago. 2026.

[^referencia_diagnostico_tce_rs]: O diagnóstico do TCE-RS abrangeu os 497 Poderes Executivos municipais gaúchos e examinou aspectos de estrutura, equipe, planejamento e governança de TI. Entre os resultados divulgados, 59,6% dos municípios não possuíam área de TI formalmente instituída, 66% contavam com equipes de até dois profissionais, 1,4% possuíam PDTI, 2% tinham comitê de governança de TI formalizado e 86,7% estavam no nível inicial de maturidade em governança. TRIBUNAL DE CONTAS DO ESTADO DO RIO GRANDE DO SUL. *TCE-RS divulga diagnóstico sobre estrutura e governança de TI dos municípios gaúchos*. 11 dez. 2025. Disponível em: <https://tcers.tc.br/noticia/tce-rs-divulga-diagnostico-sobre-estrutura-e-governanca-de-ti-dos-municipios-gauchos/>. Acesso em: 12 ago. 2026.

[^referencia_iegm_igovti]: O Índice de Efetividade da Gestão Municipal (IEGM) consolida sete dimensões da gestão municipal, entre elas o i-GovTI. O portal nacional apresenta resultados dos municípios participantes e classifica os índices em faixas que vão de baixo nível de adequação a altamente efetiva. INSTITUTO RUI BARBOSA. *IEGM Brasil*. Disponível em: <https://iegm.irbcontas.org.br/>. Acesso em: 12 ago. 2026.

No TCE-RJ, as mensurações do iGovTI anteriores a esta fiscalização ocorreram nas auditorias dos Processos nº 205.089-9/2023, relativa a quatro prefeituras municipais, e nº 109.009-4/2023, relativa a organizações do SETIC. Em ambas, utilizou-se questionário baseado no modelo do TCU de 2021, com adaptações. O núcleo de práticas de governança e gestão de TIC foi preservado como base de comparabilidade; itens adicionais de cada fiscalização foram tratados como módulos complementares, sem integrar o cômputo do índice.

O iGovTI 2026 do TCE-RJ preserva a lógica de mensuração de maturidade em governança e gestão de TIC, com adaptações destinadas a reforçar o foco na área de TIC, a qualidade das respostas e a vinculação com evidências documentais, mantendo base comparável com o ciclo de 2023 na estrutura ajustada de itens. A composição do índice, os níveis de maturidade e a forma de cálculo constam da Introdução; os resultados constam do capítulo seguinte.

Esses referenciais conceituais, normativos e históricos contextualizam o objeto e subsidiam a compreensão da metodologia e dos critérios adotados. A avaliação das 113 organizações respondentes, a comparação longitudinal e os achados de auditoria são apresentados a seguir.

\newpage

# 4. RESULTADOS DA AUDITORIA

Esta seção apresenta os resultados consolidados obtidos na avaliação do Índice de Governança e Gestão de TI (iGovTI 2026), a comparação dos três cenários de processamento, a comparação longitudinal com o ciclo anterior e os achados de auditoria resultantes da validação das informações autodeclaradas e das evidências documentais encaminhadas pelas organizações jurisdicionadas.

## 4.1. Resultados gerais do iGovTI 2026

A mensuração da maturidade em governança e gestão de tecnologia da informação e comunicação, realizada junto a 113 organizações jurisdicionadas da Administração Pública Estadual e Municipal do Estado do Rio de Janeiro, revela um cenário predominantemente incipiente e marcado por fragilidades recorrentes de formalização, coordenação, planejamento, capacidade institucional e controle operacional da TIC.

A análise do Índice de Governança e Gestão de TI (iGovTI 2026) demonstra concentração de organizações com avaliações baixas. Esse resultado indica que, para a maioria das organizações avaliadas, os mecanismos de direção e os processos operacionais de tecnologia ainda não apresentam grau de formalização e efetividade compatível com o nível mínimo esperado de maturidade institucional.

![Distribuição das organizações por nível de maturidade do iGovTI 2026](igovti_2026_distribuicao_maturidade.png){#fig:distribuicao_maturidade_igovti_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

A distribuição por nível de maturidade, apresentada na [@fig:distribuicao_maturidade_igovti_2026], mostra forte concentração nos estágios iniciais. Das organizações avaliadas, 60 (53,1%) foram classificadas no nível Inexpressivo e 39 (34,5%) no nível Iniciando. Assim, 99 organizações (87,6%) obtiveram resultado inferior a 0,40. Somente 9 organizações (8,0%) alcançaram o nível Intermediário e 5 (4,4%) o nível Aprimorado.[^cautela_ranking]

[^cautela_ranking]: Diferenças marginais de pontuação entre organizações adjacentes no ranking devem ser interpretadas com cautela analítica, visto que o modelo matemático de composição do índice não pressupõe estimativa de erro amostral e que os resultados estão sujeitos à qualidade e à fidedignidade declaratória do jurisdicionado.

O iGovTI apresentou média de 0,189 e mediana de 0,136. O primeiro quartil foi 0,066 e o terceiro quartil, 0,239, o que evidencia a concentração de metade das organizações avaliadas nesse intervalo, bem como a permanência de pelo menos 75% das organizações abaixo do nível Intermediário.

A divergência positiva entre a média e a mediana, combinada com o valor máximo de 0,788 e com apenas cinco organizações no nível Aprimorado, caracteriza uma distribuição com assimetria à direita: um grupo reduzido de resultados elevados desloca a média para cima, sem alterar o quadro predominante de baixa maturidade. Destaca-se que 5 organizações (4,4%) apresentaram valor igual a zero no índice calculado, o que indica uma possível ausência das práticas necessárias mensuradas pelo modelo aplicado.

### 4.1.1. Comparação dos cenários

A [@tbl:cenarios_igovti] apresenta o iGovTI nos três estados preservados pelo fluxo de processamento. O cenário-base retrata a autodeclaração dos gestores após as retificações e os ajustes iniciais de saneamento, mas antes dos juízos da Equipe de Auditoria sobre as evidências. O cenário pós-evidências incorpora a validação documental, e o cenário pós-comentários incorpora, adicionalmente, as manifestações e evidências complementares acolhidas no contraditório.

: Evolução do iGovTI nos três cenários de processamento {#tbl:cenarios_igovti#}

| Cenário | Média | Mediana | Inexpressivo | Iniciando | Intermediário | Aprimorado | iGovTI < 0,40 |
|:---|---:|---:|---:|---:|---:|---:|---:|
| **Base de autodeclaração saneada** | 0,235 | 0,175 | 50 (44,2%) | 43 (38,1%) | 14 (12,4%) | 6 (5,3%) | 93 (82,3%) |
| **Pós-avaliação de evidências** | 0,184 | 0,134 | 61 (54,0%) | 39 (34,5%) | 9 (8,0%) | 4 (3,5%) | 100 (88,5%) |
| **Pós-comentários do gestor** | 0,189 | 0,136 | 60 (53,1%) | 39 (34,5%) | 9 (8,0%) | 5 (4,4%) | 99 (87,6%) |

<div custom-style="FonteImagem">(Fonte: elaboração própria a partir das bases rastreáveis de cada cenário)</div>

A avaliação das evidências influenciou materialmente os resultados. Da base para o cenário pós-evidências, a média passou de 0,235 para 0,184, 90 organizações tiveram redução no índice e 18 foram reposicionadas para nível de maturidade inferior.[^impacto_evidencias_igovti] Após os comentários, a média subiu para 0,189, sem retornar ao patamar autodeclarado. A diferença entre os cenários não permite concluir, por si só, que toda prática retirada inexista: indica que parte das declarações não alcançou o grau de comprovação documental requerido nos procedimentos e que parte delas foi posteriormente sustentada pelos elementos acolhidos no contraditório.

O cenário-base é relevante como referência da percepção institucional dos auditados, mas não constitui asseguração independente da existência ou da efetividade das práticas. Para as conclusões, os achados e os encaminhamentos deste relatório, prevalece o cenário pós-comentários do gestor.

[^impacto_evidencias_igovti]: A comparação considerou a base após os ajustes iniciais de saneamento e a base resultante da avaliação das evidências. Foram efetivamente alteradas 1.964 células de respostas de 103 organizações. A análise detalhada consta do Anexo "AN07 – Impacto da avaliação das evidências".

A distribuição contínua da [@fig:distribuicao_continua_igovti_2026] complementa a classificação por faixas e permite observar a concentração dos resultados, os limites de maturidade e a distância entre a mediana e os valores mais elevados. A leitura conjunta das duas figuras demonstra que a baixa maturidade não decorre apenas do enquadramento por faixas, mas também da distribuição efetiva das notas, concentrada nos intervalos inferiores da escala.

![Distribuição contínua dos resultados do iGovTI 2026](igovti_2026_distribuicao_continua.png){#fig:distribuicao_continua_igovti_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

### 4.1.2. Relação entre Governança e Gestão de TIC

A decomposição do iGovTI 2026 entre seus dois componentes principais — Governança de TIC (peso de 47,8%) e Gestão de TIC (iGestTI, peso de 52,2%) — revela assimetrias relevantes entre a capacidade de direção e a capacidade operacional das organizações.

Os indicadores descritivos apresentados na [@tbl:estatisticas_componentes_igovti] mostram que os resultados operacionais de gestão foram ligeiramente superiores aos de governança no conjunto avaliado. A média da Gestão de TIC foi 0,210, ante 0,166 para Governança de TIC; as medianas foram, respectivamente, 0,155 e 0,117. As duas médias situaram-se no nível Iniciando, enquanto a mediana de Governança de TIC permaneceu no nível Inexpressivo e a mediana de Gestão de TIC, no nível Iniciando.

: Estatísticas descritivas do iGovTI 2026 e de seus componentes principais {#tbl:estatisticas_componentes_igovti#}

| Indicador | Média | 1º quartil | Mediana | 3º quartil | Mínimo | Máximo | Organizações com valor ≥ 0,40 |
|:---|---:|---:|---:|---:|---:|---:|---:|
| **Governança de TIC** | 0,166 | 0,016 | 0,117 | 0,215 | 0,000 | 0,865 | 15 (13,3%) |
| **Gestão de TIC** | 0,210 | 0,082 | 0,155 | 0,285 | 0,000 | 0,802 | 17 (15,0%) |
| **iGovTI 2026** | 0,189 | 0,066 | 0,136 | 0,239 | 0,000 | 0,788 | 14 (12,4%) |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

A [@fig:distribuicao_componentes_igovti_2026] permite comparar a dispersão dos três indicadores. O resultado em Gestão de TIC superou o de Governança de TIC em 75 organizações (66,4%); o movimento inverso ocorreu em 33 (29,2%); e houve igualdade em 5 (4,4%). O padrão indica que, para a maior parte das organizações, as capacidades operacionais de gestão se situaram em patamar superior ao dos mecanismos de direção, monitoramento e controle exercidos pela alta administração. Essa diferença, contudo, não elimina a baixa maturidade da gestão: 96 organizações (85,0%) também obtiveram resultado em Gestão de TIC inferior a 0,40.

![Distribuição do iGovTI 2026 e dos componentes Governança de TIC e Gestão de TIC](igovti_2026_distribuicao_componentes.png){#fig:distribuicao_componentes_igovti_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

A [@fig:governanca_vs_gestao_igovti_2026] mostra a posição simultânea das organizações nos dois componentes. Pontos acima da diagonal representam resultado de gestão superior ao de governança, enquanto pontos abaixo da diagonal representam a situação inversa. A concentração de pontos próxima à origem reforça que, mesmo quando há diferença entre os componentes, a maior parte das organizações permanece distante de patamar intermediário tanto em direção e monitoramento (nível de governança) quanto em execução e controle operacional (nivel de gestão).

![Relação entre os resultados de governança e gestão de TIC](igovti_2026_governanca_vs_gestao.png){#fig:governanca_vs_gestao_igovti_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

### 4.1.3. Desempenho por dimensões da Gestão de TIC

A decomposição da Gestão de TIC revela diferenças relevantes entre as seis dimensões avaliadas. Conforme a [@tbl:estatisticas_dimensoes_gestao], Planejamento de TIC apresentou a maior média (0,305) e a maior mediana (0,163). Essa dimensão também figurou como a de maior resultado em 52 organizações (46,0%), considerados os empates. Esse resultado indica que as organizações possuem alguma capacidade de planejar e elaborar planos de TIC (como PDTIs), mas frequentemente encontram dificuldades para converter essas diretrizes em processos operacionais e de segurança.

: Estatísticas descritivas das dimensões de Gestão de TIC {#tbl:estatisticas_dimensoes_gestao#}

| Dimensão | Média | Mediana | Mínimo | Máximo | Resultados iguais a zero | Organizações com valor inferior a 0,40 |
|:---|---:|---:|---:|---:|---:|---:|
| **Planejamento de TIC** | 0,305 | 0,163 | 0,000 | 1,000 | 20 (17,7%) | 78 (69,0%) |
| **Gestão de Serviços de TIC** | 0,150 | 0,077 | 0,000 | 0,724 | 20 (17,7%) | 100 (88,5%) |
| **Gestão de Riscos de TI e Segurança da Informação** | 0,165 | 0,097 | 0,000 | 1,000 | 32 (28,3%) | 97 (85,8%) |
| **Estrutura de Segurança da Informação** | 0,258 | 0,130 | 0,000 | 1,000 | 25 (22,1%) | 83 (73,5%) |
| **Processos de Segurança da Informação** | 0,205 | 0,147 | 0,000 | 0,822 | 10 (8,8%) | 95 (84,1%) |
| **Gestão de Soluções de TIC** | 0,193 | 0,150 | 0,000 | 1,000 | 26 (23,0%) | 101 (89,4%) |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

A distribuição completa das seis dimensões é apresentada na [@fig:distribuicao_dimensoes_gestao_2026], incluindo medianas, intervalos interquartis e médias. A figura permite identificar que as diferenças entre dimensões não alteram o diagnóstico geral: mesmo as capacidades com melhor desempenho relativo ainda apresentam grande quantidade de organizações abaixo de 0,40.

![Distribuição dos resultados das seis dimensões de Gestão de TIC](igovti_2026_distribuicao_dimensoes_gestao.png){#fig:distribuicao_dimensoes_gestao_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

As menores médias foram observadas em Gestão de Serviços de TIC (0,150) e Gestão de Riscos de TI e Segurança da Informação (0,165). A primeira registrou valor inferior a 0,40 em 100 organizações (88,5%) e apareceu entre as dimensões de menor resultado de 33 organizações (29,2%), considerados os empates.

Para a segunda, esses quantitativos foram, respectivamente, 97 organizações (85,8%) e 42 organizações (37,2%). O quadro indica que a formalização do planejamento, quando existente, frequentemente não é acompanhada, na mesma intensidade, pelas demais capacidades operacionais, de serviços e de segurança.

A dimensão Estrutura de Segurança da Informação apresentou média de 0,258 e mediana de 0,130. Essa diferença, associada à ampla dispersão observada na [@fig:distribuicao_dimensoes_gestao_2026], evidencia heterogeneidade: um grupo de organizações possui estruturas de segurança mais consolidadas, enquanto parcela expressiva permanece próxima dos níveis inferiores. A dimensão Processos de Segurança da Informação mostrou mediana superior à de Estrutura de Segurança da Informação, mas 84,1% das organizações ainda permaneceram abaixo de 0,40, o que recomenda examinar separadamente a existência da estrutura formal e a execução contínua dos processos de segurança.

A [@fig:maturidade_dimensoes_igovti_2026] explicita a composição de cada dimensão por nível de maturidade e permite verificar em quais capacidades se concentram as organizações nos estágios iniciais. Essa leitura é útil para orientar ações de indução e monitoramento, pois evidencia que a melhoria do iGovTI depende de avanços simultâneos em planejamento, serviços, riscos, segurança e soluções de TIC, e não apenas da existência formal de planos.

![Distribuição dos níveis de maturidade das organizações nas dimensões de Gestão de TIC](igovti_2026_maturidade_dimensoes.png){#fig:maturidade_dimensoes_igovti_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

### 4.1.4. Resultados por esfera

Os resultados apresentam diferença relevante entre as organizações estaduais e os municípios. Conforme a [@tbl:diagnostico_segmentos], as organizações estaduais alcançaram média de 0,220 no iGovTI, enquanto os municípios registraram 0,120. As medianas foram, respectivamente, 0,152 e 0,077. Embora os dois segmentos permaneçam concentrados nos níveis iniciais de maturidade, os valores mostram que as fragilidades são mais acentuadas no conjunto municipal.

: Resultados do iGovTI 2026 por segmento institucional {#tbl:diagnostico_segmentos#}

| Segmento | Organizações | Média do iGovTI | Mediana do iGovTI | Média de Governança | Média de Gestão |
|:---|---:|---:|---:|---:|---:|
{% for item in diagnostico_segmentos %}
| {{ item.segmento }} | {{ item.n }} | {{ ('%0.3f' | format(item.iGovTI_media)) | replace('.', ',') }} | {{ ('%0.3f' | format(item.iGovTI_mediana)) | replace('.', ',') }} | {{ ('%0.3f' | format(item.GovernancaTI_media)) | replace('.', ',') }} | {{ ('%0.3f' | format(item.iGestTI_media)) | replace('.', ',') }} |
{% endfor %}

<div custom-style="FonteImagem">(Fonte: elaboração própria, com base nos resultados finais do iGovTI 2026 e no cadastro das organizações avaliadas)</div>

A diferença entre os segmentos foi mais intensa em Gestão de TIC do que em Governança de TIC. Na gestão, a média das organizações estaduais foi 0,251, mais que o dobro da média municipal, de 0,119. Na governança, os resultados foram 0,187 e 0,120. Assim, entre as organizações estaduais, a capacidade operacional apresentou resultado superior ao dos mecanismos de direção e monitoramento. Nos municípios, os dois componentes permaneceram praticamente no mesmo patamar e com baixa adoção.

O exame das dimensões da Gestão de TIC reforça essa diferença. As maiores distâncias foram observadas em Planejamento de TIC, com médias de 0,396 no segmento estadual e 0,102 no municipal, e em Gestão de Soluções de TIC, com médias de 0,243 e 0,082. O resultado indica maior dificuldade dos municípios para estruturar o planejamento e organizar a gestão das soluções tecnológicas, sem afastar as fragilidades também presentes nas organizações estaduais.

Essa comparação possui caráter descritivo. O cadastro permite separar o universo apenas entre organizações estaduais e municípios e não contém informações suficientes para controlar diferenças de porte, atribuições, estrutura administrativa, capacidade financeira ou dependência tecnológica. Por essa razão, os resultados não permitem atribuir a diferença observada à esfera governamental, mas indicam a conveniência de considerar as limitações institucionais dos municípios na formulação de ações de orientação, apoio e acompanhamento.

### 4.1.5. Práticas com maior e menor grau de adoção

A análise das práticas permite identificar os aspectos relativamente mais disseminados e aqueles que apresentam maior deficiência no conjunto avaliado. A [@tbl:diagnostico_praticas] apresenta as cinco maiores e as cinco menores pontuações médias.

: Práticas com maior e menor grau de adoção no iGovTI 2026 {#tbl:diagnostico_praticas#}

| Grupo | Item | Prática | Média | Não se aplica |
|:---|:---:|:---|---:|---:|
{% for item in diagnostico_praticas_maior_adocao %}
| Maior adoção | {{ item.id }} | {{ item.descricao }} | {{ ('%0.3f' | format(item.media)) | replace('.', ',') }} | {{ item.nao_aplicavel }} |
{% endfor %}
{% for item in diagnostico_praticas_menor_adocao %}
| Menor adoção | {{ item.id }} | {{ item.descricao }} | {{ ('%0.3f' | format(item.media)) | replace('.', ',') }} | {{ item.nao_aplicavel }} |
{% endfor %}

<div custom-style="FonteImagem">(Fonte: elaboração própria, com base nas respostas finais ajustadas e na estrutura oficial do iGovTI 2026)</div>

As práticas com maior pontuação foram a instituição de política de segurança da informação, a execução do processo de planejamento de TIC e a existência de plano de TIC vigente. Esse resultado é coerente com o melhor desempenho relativo da dimensão Planejamento de TIC. Também figuraram nesse grupo a gestão de ativos associados à informação e ao controle de acesso e a gestão da segurança dos recursos de processamento.

Apesar da posição relativa, nenhuma dessas práticas alcançou média igual ou superior a 0,40. A maior média foi 0,338, referente à política de segurança da informação. Portanto, a presença dessas práticas entre as mais adotadas não indica maturidade elevada, mas apenas desempenho superior ao dos demais itens avaliados.

As menores médias foram registradas na elaboração do catálogo de serviços e no monitoramento dos níveis de serviço, no recebimento de serviços de auditoria interna pela instância superior de governança, na classificação e no tratamento de informações, no monitoramento da gestão de TIC pela alta administração e na gestão de configuração e ativos. As médias variaram de 0,103 a 0,142. Em três dessas práticas — catálogo e níveis de serviço, auditoria interna e monitoramento pela alta administração — a mediana foi igual a zero, indicando que pelo menos metade das organizações não alcançou pontuação nesses itens.

O contraste sugere que instrumentos formais, como política e plano de TIC, estão relativamente mais disseminados do que práticas que exigem execução contínua, acompanhamento da alta administração, avaliação independente e manutenção sistemática de informações operacionais. Esse resultado reforça o diagnóstico de que o principal desafio não se limita à elaboração de documentos, mas envolve sua utilização efetiva para dirigir, monitorar e controlar a TIC.

## 4.2. Comparação longitudinal entre 2023 e 2026

A estrutura de 2026 preservou a escala de 0 a 1, as categorias de resposta e as quatro faixas de maturidade empregadas em 2023, mas alterou de forma relevante a composição dos agregados e seus pesos. As principais diferenças metodológicas estão sintetizadas na [@tbl:diferencas_igovti_2023_2026].

: Principais diferenças entre as estruturas do iGovTI 2023 e do iGovTI 2026 {#tbl:diferencas_igovti_2023_2026#}

| Aspecto | iGovTI 2023 | iGovTI 2026 | Implicação analítica |
|:---|:---|:---|:---|
| **Composição do índice final** | Governança de TIC e Gestão de TIC com pesos iguais de 0,50. | Governança de TIC com peso 0,4777 e Gestão de TIC com peso 0,5223. | A gestão passou a ter participação ligeiramente superior no índice final. |
| **Governança de TIC** | Agregação hierárquica dos componentes ModeloTI, MonitorAvaliaTI e ResultadoTI. | Agregação direta de quatro práticas relativas ao modelo de gestão, monitoramento, auditoria interna e simplificação de serviços públicos. | O componente tornou-se mais direto e incorporou práticas com escopo distinto da estrutura anterior. |
| **Gestão de TIC** | Agregação de Planejamento de TIC, Pessoas e Processos de TIC; este último reunia serviços, níveis de serviço, riscos, segurança, software, projetos e contratos. | Agregação direta das seis dimensões de Gestão de TIC descritas neste relatório. | O índice passou a evidenciar separadamente seis capacidades operacionais e de segurança. |
| **Pessoas e contratações** | Pessoas e contratações de TIC integravam o cálculo da Gestão de TIC. | Não integram a árvore de cálculo do iGovTI 2026, embora continuem relevantes para o diagnóstico e para a auditoria. | Mudanças nessas matérias não explicam diretamente a variação do índice oficial de 2026. |
| **Serviços, software e projetos** | Serviços e níveis de serviço eram agregados distintos; software e projetos integravam Processos de TIC. | Serviços foram consolidados na dimensão Gestão de Serviços de TIC; software e projetos foram reunidos na dimensão Gestão de Soluções de TIC. | A leitura deve considerar a nova delimitação conceitual dos componentes. |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

Em razão dessas alterações, a diferença entre os valores nominais de 2023 e 2026 não deve ser interpretada automaticamente como evolução ou retrocesso institucional. Uma análise temporal válida exige a harmonização das questões e dos agregados comparáveis, além da consideração de mudanças de escopo, pesos, respondentes e qualidade das evidências.

Para viabilizar a análise longitudinal, foram elaboradas estruturas ajustadas comparáveis para 2023 e 2026, com a manutenção apenas das práticas passíveis de correspondência entre os instrumentos e a aplicação de estrutura comum de agregação. Após a normalização das siglas e a validação das correspondências institucionais, foram identificadas 68 organizações presentes nos dois ciclos, equivalentes a 60,2% das organizações com respostas completas em 2026.

Os resultados ajustados comparáveis têm finalidade exclusivamente analítica. Eles não substituem os índices oficiais de cada ciclo, não eliminam integralmente os efeitos de alterações de respondentes ou de contexto institucional e não constituem, isoladamente, evidência de conformidade ou de inconformidade.

A comparação foi realizada sob duas perspectivas. O cenário-base representa as respostas autodeclaradas após correções iniciais de preenchimento e saneamento, bem como solicitações de retificações por parte dos gestores. O cenário final incorpora a avaliação das evidências e os ajustes decorrentes dos comentários dos gestores. A apresentação conjunta é necessária porque a verificação documental de 2026 foi mais abrangente que a realizada em 2023.

: Resultado longitudinal do iGovTI nos dois cenários de 2026 {#tbl:comparacao_longitudinal_cenarios#}

| Referência | Média do iGovTI comparável | Organizações com aumento em relação a 2023 | Organizações com redução em relação a 2023 | Leitura do resultado |
|:---|---:|---:|---:|:---|
| **2023** | 0,180 | – | – | Referência histórica |
| **2026 – cenário-base** | 0,248 | 43 | 25 | **As respostas declaradas indicam evolução** |
| **2026 – cenário final** | 0,189 | 32 | 36 | Não foi confirmada mudança geral |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

No cenário-base, o aumento médio de 0,068 foi acompanhado de elevação do índice em 43 das 68 organizações. Esse movimento permite afirmar que houve evolução no conjunto das respostas autodeclaradas. Na classificação por nível de maturidade, 22 organizações avançaram, nove regrediram e 37 permaneceram no mesmo nível.

No cenário final, o aumento médio foi de apenas 0,009, com quantidades próximas de organizações com elevação e redução do índice. Os resultados, portanto, não permitem afirmar que houve melhora ou piora geral após a verificação documental. Nesse cenário, 14 organizações avançaram de nível de maturidade, 15 regrediram e 39 permaneceram no mesmo nível. Ao final, 58 das 68 organizações (85,3%) continuavam abaixo do nível Intermediário.

A leitura dos componentes reforça essa diferença. No cenário-base, foram identificadas melhoras no iGovTI geral, na Gestão de TIC e nas capacidades de planejamento, serviços, estrutura e processos de segurança da informação e gestão de projetos. No cenário final, apenas a melhora da Estrutura de Segurança da Informação permaneceu confirmada. Esse é o resultado positivo mais seguro da comparação, pois aparece tanto nas respostas declaradas quanto após a avaliação das evidências.

As reduções observadas em Gestão de Pessoas de TIC e Processos de Contratação de TIC foram confirmadas apenas no cenário final. Como não apareceram com a mesma clareza no cenário-base, não é possível atribuí-las exclusivamente à piora das práticas das organizações. Parte da diferença pode decorrer da maior abrangência da avaliação documental realizada em 2026. Para Governança de TIC, modelo de gestão, monitoramento, resultados, níveis de serviço, riscos e processo de software, nenhum dos dois cenários forneceu elementos suficientes para afirmar que houve mudança geral.

Conclui-se que as respostas autodeclaradas indicam evolução entre 2023 e 2026, mas essa melhora geral não foi confirmada após a avaliação das evidências. As duas leituras são complementares: a primeira retrata a percepção declarada pelas organizações; a segunda apresenta o que a fiscalização conseguiu assegurar com base na documentação examinada. Em ambas, permanece elevada a concentração de organizações nos níveis iniciais de maturidade.

## 4.3. Achados de Auditoria

Os exames e procedimentos de auditoria aplicados sobre as informações autodeclaradas pelas 113 organizações respondentes avaliadas e a respectiva validação documental permitiram constatar fragilidades sistemáticas nos controles de governança, planejamento, capacidade institucional, gestão de serviços e contratações de tecnologia da informação.

Os achados decorrem da avaliação das Questões 1 a 6. As evidências que embasam as constatações encontram-se consolidadas nos anexos da fiscalização e individualizadas nos relatórios preliminares de cada uma das 113 organizações que apresentaram resposta válida e foram avaliadas. As causas específicas das inconformidades não foram objeto de procedimento próprio de identificação causal nesta etapa. Portanto, os encaminhamentos foram formulados com foco na correção das fragilidades observadas e no aprimoramento proporcional das capacidades institucionais.

A execução dos mesmos procedimentos nos três cenários permite distinguir a visão autodeclarada, o resultado da validação documental e o estado final após o contraditório, conforme a [@tbl:cenarios_procedimentos_auditoria]. No cenário-base, os quantitativos constituem sinalizações geradas pelas regras de auditoria sobre a autodeclaração saneada, ainda sem validação probatória; por isso, não devem ser interpretados como achados definitivos.

: Execução dos procedimentos de auditoria nos três cenários {#tbl:cenarios_procedimentos_auditoria#}

| Cenário | Natureza do resultado | Marcações por organização e achado | Situações identificadas |
|:---|:---|---:|---:|
| **Base de autodeclaração saneada** | Sinalizações anteriores à validação probatória | 565 | 1.252 |
| **Pós-avaliação de evidências** | Achados após validação documental | 602 | 1.458 |
| **Pós-comentários do gestor** | Achados finais após o contraditório | 591 | 1.419 |

<div custom-style="FonteImagem">(Fonte: elaboração própria a partir dos resultados rastreáveis da execução dos procedimentos)</div>

A validação documental ampliou a identificação de fragilidades em relação ao cenário-base, com acréscimo de 37 marcações e 206 situações.[^impacto_evidencias_achados] O contraditório reduziu o resultado para 591 marcações por organização e achado e 1.419 situações. A síntese e as narrativas seguintes refletem esse estado final.

[^impacto_evidencias_achados]: Na execução dos procedimentos de auditoria sobre a base pós-avaliação de evidências, foram registradas 602 marcações de achados por auditado e 1.458 situações inconformes. A metodologia, os resultados por organização e as limitações da comparação constam do Anexo "AN07 – Impacto da avaliação das evidências".

: Síntese quantitativa dos achados e situações inconformes {#tbl:sintese_achados_auditoria#}

| Achado | Tema | Organizações com achado | Situações inconformes consolidadas mais frequentes |
|:---:|:---|---:|:---|
| **1** | Estrutura de TIC | 66 (58,4%) | Área de TIC sem atribuições formalmente definidas ou sem atribuições formais de gestão de TIC: 55; posicionamento organizacional inadequado: 18; ausência de área, unidade, setor ou função de TIC formalmente instituída: 5. |
| **2** | Governança e comitê de TIC | 101 (89,4%) | Ausência de objetivos, indicadores ou metas para a gestão de TIC: 94; comitê não instituído formalmente ou sem representação de áreas relevantes: 75; comitê sem atuação efetiva comprovada: 27. |
| **3** | Planejamento de TIC | 99 (87,6%) | Processo de planejamento inexistente ou insuficiente: 88; ausência de acompanhamento da execução do plano: 31; ausência de aprovação formal: 25. |
| **4** | Capacidade institucional de TIC e segurança da informação | 109 (96,5%) | Definição documentada do quantitativo necessário de pessoal inexistente ou insuficiente: 107; ausência de cargos ou funções formalmente atribuídos à TIC ou à segurança da informação: 91; operação predominantemente terceirizada sem profissionais internos de TIC: 1. |
| **5** | Gestão de serviços de TIC | 113 (100,0%) | Ausência ou fragilidade na definição e no monitoramento de níveis mínimos de serviço de TIC: 111; ausência ou fragilidade do processo de gestão de configuração: 110; inexistência ou insuficiência do catálogo de serviços de TIC: 108. |
| **6** | Governança técnica das contratações de TIC | 103 (91,2%) | Processo formal e padronizado para o planejamento das contratações inexistente ou frágil: 87; contratações sem análise prévia e aprovação técnica da área de TIC: 83; contratações sem equipe de planejamento com integrante técnico de TIC: 45. |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

A distribuição das ocorrências por esfera governamental é apresentada nos gráficos específicos dos achados. Esses gráficos permitem verificar se a fragilidade se concentra em determinado grupo ou se possui caráter transversal. A elevada incidência dos achados 2 a 6 indica que os problemas não se limitam a casos isolados; trata-se de fragilidades disseminadas, com potencial de comprometer a capacidade de planejamento, contratação, operação e monitoramento da TIC nas organizações avaliadas.

\newpage

### 4.3.1. Achado 1 - Estrutura de TIC insuficientemente formalizada, definida ou posicionada para gerir a tecnologia da informação

Este achado avalia se a organização possui área, unidade, setor ou função de TIC formalmente instituída, com atribuições definidas e posicionamento compatível com suas responsabilidades institucionais. Os critérios aplicáveis são o COBIT 2019 (APO01.04, APO01.05 e APO01.06), a Portaria SGD/ME nº 778/2019, utilizada como referência para o posicionamento organizacional, e o princípio da eficiência previsto no art. 37, caput, da Constituição Federal.

Com base na análise das respostas e evidências dos itens q0101, q0102 e q0103, constatou-se que 66 organizações (58,4%) apresentam fragilidades na estrutura de TIC. A situação mais frequente foi a existência de área de TIC sem atribuições formalmente definidas ou sem atribuições formais de gestão de TIC, identificada em 55 organizações. Também foram constatados posicionamento organizacional inadequado em 18 organizações e ausência de área, unidade, setor ou função de TIC formalmente instituída em 5 organizações.

![Frequência de organizações com estrutura de TIC insuficiente, segregada por esfera governamental](igovti_2026_achado1_esferas.png){#fig:achado1_esferas#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

Essas situações reduzem a segurança de que a organização disponha de condições institucionais suficientes para coordenar, gerir e sustentar a tecnologia da informação de forma alinhada às necessidades institucionais.

A ausência de formalização dificulta a responsabilização, a insuficiência de atribuições favorece atuação reativa e fragmentada e o posicionamento incompatível com a relevância da função de TIC reduz sua capacidade de interlocução com a alta administração e de participação em decisões estratégicas, orçamentárias, contratuais e de gestão de riscos.

Diante disso, são propostas recomendações para que as organizações afetadas formalizem a área, unidade, setor ou função de TIC em instrumento compatível; definam atribuições que abranjam, minimamente, planejamento, coordenação, gestão e controle da TIC; e avaliem o posicionamento organizacional da área para assegurar interlocução adequada com a alta administração e participação nas decisões relevantes.

### 4.3.2. Achado 2 - Governança de TIC insuficiente para avaliar, dirigir e monitorar a tecnologia da informação

Este achado avalia o estabelecimento de objetivos, indicadores e metas para a gestão de TIC e a instituição e atuação efetiva de Comitê de TIC ou instância equivalente. Os critérios decorrem do COBIT 2019 (MEA01.04 e EDM01.02), do Decreto nº 12.198/2024, como referência de governança digital, e do Acórdão TCE-RJ nº 44.490/2024-PLEN.

Com base na análise das respostas e evidências dos itens q1001ext[H], q1001ext[E] e q1001ext[F], constatou-se que 101 organizações (89,4%) apresentam fragilidades na governança de TIC. A ausência de objetivos, indicadores ou metas para a gestão de TIC foi identificada em 94 organizações; a não instituição formal de Comitê de TIC ou instância equivalente, ou sua composição sem representantes de áreas relevantes, ocorreu em 75; e a ausência de atuação efetiva comprovada do colegiado, em 27.

![Frequência de organizações com governança de TIC insuficiente, segregada por esfera governamental](igovti_2026_achado2_esferas.png){#fig:achado2_esferas#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

O achado demonstra que a governança de TIC ainda é frequentemente tratada de forma documental ou episódica, sem mecanismos regulares de direção, acompanhamento e responsabilização. A ausência de objetivos, indicadores ou metas dificulta o direcionamento das prioridades e a avaliação do desempenho da TIC; a inexistência de instância colegiada reduz a participação das áreas relevantes nas decisões de tecnologia; e a falta de atuação efetiva do comitê compromete o acompanhamento das deliberações e de seus encaminhamentos.

Diante disso, propõe-se recomendação para o estabelecimento de objetivos, indicadores e metas de TIC. Para as situações relativas ao comitê, são propostas determinações para sua instituição formal, com representação de áreas relevantes e regras mínimas de funcionamento, e para a comprovação de atuação efetiva, mediante exercício das competências, registro das deliberações e acompanhamento dos encaminhamentos.

### 4.3.3. Achado 3 - Planejamento de TIC insuficiente para orientar a gestão, o orçamento e as contratações de TIC

Este achado avalia a existência de processo formal de planejamento, plano de TIC vigente e aprovado, alinhamento ao planejamento institucional, integração com orçamento e contratações e acompanhamento periódico. Os critérios centrais decorrem do COBIT 2019 (APO02.05 e APO06.03), do Acórdão 1.411/2014-TCU-Plenário e do Acórdão TCE-RJ nº 44.490/2024-PLEN.

Com base na análise dos itens q2101 e q2102 e das respectivas evidências, constatou-se que 99 organizações (87,6%) apresentam fragilidades no planejamento de TIC. Foram identificados processo de planejamento inexistente ou insuficiente para produzir e manter plano adequado em 88 organizações; ausência de acompanhamento da execução do plano em 31; ausência de aprovação formal em 25; plano não utilizado como referência para a proposta orçamentária e o plano de contratações em 20; e alinhamento inadequado ao planejamento institucional em 17.

![Frequência de organizações com planejamento de TIC deficiente, segregada por esfera governamental](igovti_2026_achado3_esferas.png){#fig:achado3_esferas#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

A insuficiência de planejamento compromete a conversão das necessidades institucionais em iniciativas, prioridades, recursos, prazos e benefícios esperados. Quando o plano de TIC não está aprovado, alinhado ao planejamento institucional, integrado ao orçamento e ao plano de contratações, ou periodicamente acompanhado, a organização tende a executar ações reativas, sem previsibilidade orçamentária e sem mecanismo suficiente de monitoramento de resultados.

Diante disso, são propostas determinações para que as organizações afetadas instituam processo formal de planejamento com participação das áreas demandantes; submetam o plano à aprovação competente; explicitem seu alinhamento institucional; integrem-no à proposta orçamentária e ao plano de contratações de maneira proporcional; e estabeleçam rotina periódica de acompanhamento, revisão e atualização.

### 4.3.4. Achado 4 - Capacidade institucional de pessoal de TIC e segurança da informação insuficientemente estruturada ou dimensionada

Este achado avalia a existência de força de trabalho dedicada, a definição documentada do quantitativo necessário, a atribuição formal de cargos ou funções e a preservação de capacidade interna nos modelos predominantemente terceirizados. Os critérios decorrem do COBIT 2019 (APO01.05, APO07.01, APO07.05 e APO07.06), do Acórdão 1.411/2014-TCU-Plenário, itens 9.1.6.5 e 9.1.7, e do Acórdão TCE-RJ nº 44.490/2024-PLEN.

Com base na análise das respostas e evidências relacionadas à força de trabalho, constatou-se que 109 organizações (96,5%) apresentam fragilidades de capacidade institucional. A ausência ou insuficiência de definição documentada do quantitativo necessário de pessoal de TIC e segurança da informação ocorreu em 107 organizações; a ausência de cargos ou funções formalmente atribuídos à TIC ou à segurança da informação, em 91; e a operação predominantemente terceirizada sem profissionais internos de TIC, em uma organização. A situação de ausência absoluta de força de trabalho dedicada à TIC não ocorreu no cenário final.

![Frequência de organizações com capacidade institucional de TIC insuficiente, segregada por esfera governamental](igovti_2026_achado4_esferas.png){#fig:achado4_esferas#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

O achado evidencia gargalo transversal. A ausência de força de trabalho dedicada, de dimensionamento documentado e de cargos ou funções formalmente atribuídos à TIC ou à segurança da informação limita a capacidade de planejar, contratar, fiscalizar, operar e proteger serviços de TIC. Em organizações com operação predominantemente terceirizada, a ausência de profissionais internos tende a agravar riscos de perda de conhecimento, baixa supervisão contratual e descontinuidade de serviços.

Diante disso, são propostas recomendações para que as organizações afetadas avaliem a força de trabalho dedicada à TIC; estimem e mantenham atualizado o quantitativo necessário de pessoal; avaliem a necessidade de formalizar cargos ou funções atribuídos à TIC e à segurança da informação; e, quando o modelo for predominantemente terceirizado, assegurem capacidade interna suficiente para coordenação, supervisão, fiscalização, responsabilização e retenção de conhecimento.

### 4.3.5. Achado 5 - Gestão de serviços de TIC insuficiente para assegurar controle sobre serviços, ativos e incidentes

Este achado avalia catálogo de serviços, níveis mínimos de serviço, inventário de dispositivos e softwares, gestão de configuração e gestão de incidentes. Os critérios decorrem do COBIT 2019 (APO09.02, BAI10.01, DSS02.02, DSS02.04 e DSS02.07), da ITIL 4, da ABNT NBR ISO/IEC 20000-2:2021 e do Acórdão TCE-RJ nº 44.490/2024-PLEN.

Com base na análise das respostas e evidências relacionadas à gestão de serviços de TIC, constatou-se que 113 organizações (100,0%) apresentam fragilidades nesse tema. As situações mais frequentes foram ausência ou fragilidade na definição e no monitoramento de níveis mínimos de serviço, em 111 organizações; ausência ou fragilidade do processo de gestão de configuração, em 110; inexistência ou insuficiência do catálogo de serviços, em 108; inexistência ou fragilidade do processo de gestão de incidentes, em 102; e inventário e controle de dispositivos e softwares inexistente ou insuficiente, em 86.

![Frequência de organizações com gestão de serviços de TIC insuficiente, segregada por esfera governamental](igovti_2026_achado5_esferas.png){#fig:achado5_esferas#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

O conjunto de fragilidades aumenta o risco de atuação predominantemente reativa na gestão dos serviços de TIC. Sem catálogo de serviços, usuários e áreas demandantes não dispõem de visão clara dos serviços, responsáveis, condições de acesso e canais de atendimento. Sem níveis mínimos de serviço, a organização não controla qualidade, desempenho e expectativas. Sem inventário e gestão de configuração, há baixa rastreabilidade dos ativos, sistemas, dependências e impactos de mudanças. Sem processo de incidentes, falhas de serviços e de segurança tendem a ser tratadas de forma inconsistente e pouco aprendida.

Diante disso, são propostas recomendações para que as organizações afetadas instituam e mantenham catálogo de serviços de TIC; definam, pactuem e monitorem níveis mínimos de serviço ou metas de atendimento; estabeleçam e mantenham inventário de ativos; formalizem e executem processo de gestão de configuração; e formalizem e executem processo de gestão de incidentes de TIC.

### 4.3.6. Achado 6 - Fragilidades na governança técnica da fase preparatória das contratações de TIC

Este achado avalia a governança técnica da fase preparatória das contratações de TIC, incluindo processo formal e padronizado, análise prévia e aprovação técnica pela área de TIC, alinhamento aos instrumentos de planejamento e designação formal de equipe com participação técnica. Os critérios decorrem dos arts. 7º, 11, 12, 18 e 19 da Lei nº 14.133/2021, do COBIT 2019 (BAI02.04), da Instrução Normativa SGD/ME nº 94/2022 como referência de boa prática, do Acórdão TCE-RJ nº 44.490/2024-PLEN e do Acórdão nº 2.342/2016-TCU-Plenário.

Com base na análise das respostas e evidências relacionadas às contratações, constatou-se que 103 organizações (91,2%) apresentam fragilidades na governança técnica da fase preparatória. Foram identificados processo formal e padronizado inexistente ou frágil em 87 organizações; contratações sem análise prévia e aprovação técnica da área de TIC em 83; ausência de equipe de planejamento designada com integrante técnico de TIC em 45; e contratações sem alinhamento ao planejamento de TIC e ao Plano de Contratações Anual em 33.

![Frequência de organizações com fragilidades na governança técnica da fase preparatória das contratações de TIC, segregada por esfera governamental](igovti_2026_achado6_esferas.png){#fig:achado6_esferas#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

O achado demonstra que a fase preparatória das aquisições de tecnologia ainda é frequentemente conduzida sem governança técnica suficiente. A ausência de fluxo padronizado aumenta a dependência de iniciativas isoladas; a falta de análise técnica da área de TIC eleva riscos de incompatibilidade, vulnerabilidade e duplicidade de soluções; o desalinhamento ao planejamento e ao orçamento favorece contratações reativas; e a ausência de equipe formal de planejamento compromete a qualidade dos estudos preliminares, dos requisitos, da análise de riscos e da fiscalização futura.

Diante disso, são propostas recomendações para formalizar e padronizar o processo de planejamento das contratações, submeter as contratações à análise prévia da área de TIC e designar equipe de planejamento com participação requisitante e técnica. Para o desalinhamento, propõe-se determinação para assegurar compatibilidade com os instrumentos de planejamento de TIC e, quando elaborado, com o Plano de Contratações Anual, admitidas justificativas cabíveis em situações excepcionais.

## 4.4. Cenário de utilização de inteligência artificial

As questões sobre inteligência artificial tiveram caráter diagnóstico e complementaram a avaliação do iGovTI 2026. A análise buscou identificar o grau de utilização institucional de IA, a existência de diretrizes, contratações, controles sobre IA generativa e os principais riscos associados ao tema.

O cenário apurado indica baixa institucionalização. Das 113 organizações respondentes, 32 (28,3%) declararam algum grau de uso institucional, decisão formal ou plano para IA, mas apenas 16 (14,2%) informaram adoção parcial ou em maior parte/total.

As diretrizes e controles são ainda menos disseminados: 11 organizações (9,7%) declararam diretrizes de IA em nível parcial ou superior, e 11 (9,7%) declararam controles de IA generativa em nível parcial ou superior. Além disso, 89 organizações (78,8%) informaram não adotar medidas para identificar ou controlar o uso não autorizado ou não mapeado de IA generativa.

![Estágio de institucionalização da inteligência artificial](cenario_institucionalizacao_ia.png){#fig:institucionalizacao_ia#}
<div custom-style="FonteImagem">(Fonte: elaboração própria, com base nas respostas finais ajustadas do questionário iGovTI 2026)</div>

A [@fig:institucionalizacao_ia] evidencia o descompasso entre a utilização institucional de IA e a formalização de mecanismos de governança. Enquanto 28,3% das organizações declararam ao menos planejamento ou algum grau de utilização institucional, somente 19,5% informaram algum estágio de adoção de controles sobre o uso não autorizado ou não mapeado de IA generativa. Considerando apenas adoção parcial ou superior, os percentuais foram de 14,2% para utilização institucional e de 9,7% tanto para diretrizes quanto para controles de IA generativa.

Conforme demonstra a [@fig:institucionalizacao_ia], o principal risco identificado decorre da combinação entre a disponibilidade crescente de ferramentas de IA, especialmente generativa, e a baixa formalização de inventários, diretrizes e controles institucionais.

Esse cenário amplia a possibilidade de uso difuso dessas ferramentas sem regras para dados em *prompts*, avaliação prévia de riscos, validação, transparência e revisão humana, e recomenda atuação preventiva e orientativa, sem prejuízo de fiscalizações específicas quando o uso de IA envolver dados sensíveis, serviços críticos, contratações relevantes ou decisões que afetem direitos de cidadãos.

A análise detalhada consta no anexo "AN09 – Cenário de utilização de IA no ERJ".

## 4.5. Ausência de resposta ao questionário e necessidade de apuração específica

Das 119 organizações abrangidas pela fiscalização, seis não apresentaram resposta válida ao questionário eletrônico encaminhado na segunda etapa de solicitação de informações. Por essa razão, não integraram o cálculo do iGovTI 2026 nem a apuração dos achados consolidados.

A comunicação inicial ocorreu mediante envio do ofício de apresentação e do TSID 1, oportunidade em que as organizações indicaram tempestivamente seus pontos focais para interlocução com a Equipe de Auditoria. Posteriormente, o TSID 2, contendo o link individualizado para preenchimento do questionário, foi encaminhado aos pontos focais indicados. Apesar das reiterações realizadas pela Equipe, não foi apresentada resposta válida ao instrumento.

Na fase de comentários do gestor, foi encaminhado o TSID 3 também às organizações sem resposta válida, para que pudessem confirmar a não participação, prestar esclarecimentos ou apresentar justificativas. Duas organizações confirmaram que não participaram da coleta, enquanto as outras não apresentaram manifestação.

Os registros de envio, ciência e recebimento das comunicações, com indicação de data e hora, encontram-se reunidos no Anexo AN10 – Comunicações da fiscalização e registros de ciência. Esses elementos justificam a abertura de processos apartados para apuração das circunstâncias da ausência de resposta ao questionário, assegurando-se aos responsáveis a oportunidade de apresentar razões de defesa. A proposta constante do capítulo 7 não pressupõe reconhecimento antecipado de responsabilidade nem aplicação automática de sanção.

\newpage

# 5. COMENTÁRIOS DO GESTOR E ANÁLISE DA EQUIPE

Visando fortalecer o caráter dialógico da fiscalização e assegurar o contraditório, foram encaminhados relatórios individuais preliminares às 113 organizações que apresentaram resposta válida e foram avaliadas, com indicação das situações inconformes identificadas, das evidências consideradas e dos encaminhamentos propostos. Também foi oportunizada manifestação, em apartado, às seis organizações que não apresentaram resposta válida ao questionário iGovTI 2026.

Foram consideradas somente submissões concluídas e, nos casos de reenvio, preservou-se a manifestação mais recente. A consolidação abrangeu os comentários sobre as situações e os encaminhamentos, os pedidos de reavaliação de respostas ajustadas após o exame das evidências e as manifestações das organizações sem resposta válida ao questionário.

As manifestações foram confrontadas com os critérios aplicáveis e o conjunto probatório de evidências enviadas. Todas as manifestações recebidas foram examinadas.

## 5.1. Participação e panorama geral

Foram recebidas manifestações válidas de 80 das 119 organizações abrangidas (67,2%). Esse total compreende 78 das 113 organizações que responderam ao iGovTI 2026 e receberam relatório individual (69,0%) e duas das seis organizações sem resposta válida ao questionário (33,3%).

Das 113 organizações que responderam ao iGovTI 2026, 103 tiveram pelo menos um item ou subitem da resposta ajustado porque a evidência apresentada não comprovou a declaração correspondente. Para essas organizações, o questionário de comentários disponibilizou campos específicos para a apresentação de esclarecimentos ou evidências complementares e eventual reavaliação do ajuste. Entre as 103 organizações, 72 participaram da etapa de comentários e 56 apresentaram pelo menos um pedido de reavaliação.

![Participação na etapa de comentários do gestor](../99-Avaliacao_Comentarios_Gestor/img/01-participacao.png){#fig:comentarios_gestor_participacao#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

O índice de participação deve ser considerado na interpretação dos resultados: as proporções apresentadas descrevem as situações sobre as quais houve manifestação e não podem ser extrapoladas, isoladamente, para a totalidade das organizações fiscalizadas.

Foram registradas 1.471 manifestações individualizadas sobre situações encontradas. Houve concordância em 1.235 casos (84,0%) e discordância em 236 (16,0%). Entre as concordâncias, 584 informaram providências em curso, 626 reconheceram a situação sem medida adotada e somente 25 declararam atendimento concluído. Foram apresentados 268 anexos nessa seção.

![Cenário geral das manifestações sobre as situações encontradas](../99-Avaliacao_Comentarios_Gestor/img/02-panorama-geral.png){#fig:comentarios_gestor_panorama_geral#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

: Distribuição geral das manifestações dos gestores {#tbl:comentarios_gestor_distribuicao_geral#}

| Manifestação | Quantidade | Percentual |
|---|---:|---:|
| Concorda e já atendeu | 25 | 1,7% |
| Concorda e está atendendo | 584 | 39,7% |
| Concorda, sem medida adotada | 626 | 42,6% |
| Discorda | 236 | 16,0% |
| **Total** | **1.471** | **100,0%** |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

Os resultados demonstram elevada convergência dos gestores com o diagnóstico preliminar, mas o reconhecimento das fragilidades não equivale à sua correção. Apenas 1,7% das manifestações declarou atendimento concluído, enquanto 42,6% reconheceu a situação sem indicar medida adotada e 39,7% informou providências ainda em curso. As medidas anunciadas deverão, portanto, ser acompanhadas quanto à formalização, ao prazo, à abrangência e à efetiva implementação.

A leitura estruturada dos campos livres identificou como temas mais recorrentes: formalização, normas e governança; ferramentas, ativos e processos operacionais; planejamento e planos de ação; força de trabalho e competências; documentos e evidências adicionais; e orçamento, recursos e contratações. Também foram mencionadas dependência de terceiros ou de estruturas compartilhadas e solicitações de orientação.

## 5.2. Manifestações por achado

A distribuição das manifestações por achado consta da [@fig:comentarios_gestor_por_achado] e da [@tbl:comentarios_gestor_por_achado_tabela]. O Achado 6 apresentou a maior proporção de discordâncias (25,8%), seguido dos Achados 3 (16,8%), 2 (16,2%) e 5 (16,0%). O Achado 1 registrou a maior convergência, com três discordâncias em 52 manifestações.

![Manifestações dos gestores por achado](../99-Avaliacao_Comentarios_Gestor/img/03-manifestacoes-por-achado.png){#fig:comentarios_gestor_por_achado#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

: Manifestações dos gestores por achado {#tbl:comentarios_gestor_por_achado_tabela#}

| Achado | Total | Atendido | Em atendimento | Sem medida | Discordância | % discordância |
|---:|---:|---:|---:|---:|---:|---:|
| Estrutura de TIC | 52 | 4 | 25 | 20 | 3 | 5,8% |
| Governança de TIC | 148 | 6 | 63 | 55 | 24 | 16,2% |
| Planejamento de TIC | 321 | 8 | 131 | 128 | 54 | 16,8% |
| Capacidade de pessoal de TIC | 339 | 1 | 130 | 174 | 34 | 10,0% |
| Gestão de serviços de TIC | 375 | 1 | 156 | 158 | 60 | 16,0% |
| Contratações de TIC | 236 | 5 | 79 | 91 | 61 | 25,8% |
| **Total** | **1.471** | **25** | **584** | **626** | **236** | **16,0%** |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

Nos gráficos a seguir, a categoria "Situação encontrada inexistente" representa as organizações respondentes cujo relatório individual não continha a situação correspondente. Não se trata de alternativa selecionada pelo gestor.

### 5.2.1. Achado 1 - Estrutura de TIC insuficientemente formalizada, definida ou posicionada para gerir a tecnologia da informação

No Achado 1, foram recebidas 52 manifestações: quatro registraram atendimento concluído, 25 informaram providências em curso, 20 reconheceram a situação sem medida adotada e três discordaram dos apontamentos. A taxa de discordância foi de 5,8%, a menor entre os seis achados. As discordâncias se referiram ao posicionamento organizacional da área de TIC e à suficiência de suas atribuições formais.

![Manifestações sobre as situações encontradas do Achado 1](../99-Avaliacao_Comentarios_Gestor/img/achado-1-situacoes.png){#fig:comentarios_gestor_achado_1#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

Os atos normativos, organogramas, regimentos, portarias e documentos equivalentes eventualmente apresentados devem demonstrar, de forma conjugada, a formalização da função de TIC, a suficiência de suas atribuições e a adequação de seu posicionamento. Providências futuras ou planos ainda não implementados evidenciam compromisso de aprimoramento, mas não afastam, por si só, a situação existente na data-base.

### 5.2.2. Achado 2 - Governança de TIC insuficiente para avaliar, dirigir e monitorar a tecnologia da informação

No Achado 2, foram recebidas 148 manifestações, das quais 124 expressaram concordância e 24 discordância (16,2%). A situação relativa ao Comitê de TIC ou instância equivalente sem evidências suficientes de atuação efetiva apresentou a maior taxa de discordância do achado: seis de 15 manifestações (40,0%). A não instituição formal do comitê recebeu 11 discordâncias em 60 manifestações (18,3%).

![Manifestações sobre as situações encontradas do Achado 2](../99-Avaliacao_Comentarios_Gestor/img/achado-2-situacoes.png){#fig:comentarios_gestor_achado_2#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

A análise técnica deve distinguir a existência formal dos mecanismos de governança de sua atuação efetiva. Atos de instituição ou designação, desacompanhados de registros de deliberações, priorização, acompanhamento e responsabilização, não comprovam necessariamente o funcionamento regular da governança de TIC.

### 5.2.3. Achado 3 - Planejamento de TIC insuficiente para orientar a gestão, o orçamento e as contratações de TIC

No Achado 3, foram recebidas 321 manifestações: oito informaram atendimento concluído, 131 providências em curso, 128 concordância sem medida adotada e 54 discordância (16,8%). As maiores taxas de discordância se referiram ao plano de TIC sem vínculo demonstrado com o orçamento e as contratações, com 17 discordâncias em 75 manifestações (22,7%), e à ausência de aprovação formal do plano, com 12 discordâncias em 63 manifestações (19,0%).

![Manifestações sobre as situações encontradas do Achado 3](../99-Avaliacao_Comentarios_Gestor/img/achado-3-situacoes.png){#fig:comentarios_gestor_achado_3#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

A existência isolada de documento de planejamento não comprova que o processo esteja formalizado, aprovado, alinhado ao planejamento institucional, integrado ao orçamento e às contratações e periodicamente acompanhado. Planos elaborados ou aprovados após a data-base podem demonstrar providência corretiva, mas devem ser diferenciados da situação existente no período auditado.

### 5.2.4. Achado 4 - Capacidade institucional de pessoal de TIC e segurança da informação insuficientemente estruturada ou dimensionada

No Achado 4, foram recebidas 339 manifestações, das quais 305 expressaram concordância e 34 discordância (10,0%). Em 174 manifestações, equivalentes a 51,3% do total do achado, o gestor reconheceu a situação sem indicar medida adotada. A maior taxa de discordância ocorreu na situação de dependência externa relevante sem capacidade interna suficiente para coordenar e fiscalizar a TIC, com duas discordâncias em dez manifestações (20,0%).

![Manifestações sobre as situações encontradas do Achado 4](../99-Avaliacao_Comentarios_Gestor/img/achado-4-situacoes.png){#fig:comentarios_gestor_achado_4#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

Estudos de dimensionamento, descrições de cargos ou funções, matrizes de competências, planos de capacitação e designações formais devem ser examinados quanto à vigência, abrangência e efetiva aplicação. Alegações de escassez de pessoal, ausência de cargos especializados ou restrição orçamentária contextualizam as dificuldades enfrentadas, mas não afastam automaticamente a insuficiência de capacidade institucional.

### 5.2.5. Achado 5 - Gestão de serviços de TIC insuficiente para assegurar controle sobre serviços, ativos e incidentes

No Achado 5, foram recebidas 375 manifestações: uma informou atendimento concluído, 156 providências em curso, 158 concordância sem medida adotada e 60 discordância (16,0%). A situação relativa à inexistência ou fragilidade do inventário de ativos de TIC concentrou 17 discordâncias em 73 manifestações (23,3%). Nas demais situações do achado, as taxas de discordância variaram de 13,3% a 14,9%.

![Manifestações sobre as situações encontradas do Achado 5](../99-Avaliacao_Comentarios_Gestor/img/achado-5-situacoes.png){#fig:comentarios_gestor_achado_5#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

Catálogos de serviços, inventários, registros de configuração, definições de níveis de serviço e registros de incidentes devem demonstrar formalização, atualização, abrangência e uso efetivo. Relações incompletas de ativos, controles informais ou documentos sem data e responsabilidade definida devem ser avaliados com cautela, pois podem demonstrar atividade parcial sem comprovar o processo requerido.

### 5.2.6. Achado 6 - Fragilidades na governança técnica da fase preparatória das contratações de TIC

No Achado 6, foram recebidas 236 manifestações: cinco informaram atendimento concluído, 79 providências em curso, 91 concordância sem medida adotada e 61 discordância (25,8%). Foi a maior proporção de discordâncias entre os seis achados. As situações mais contestadas foram as contratações sem análise prévia e aprovação técnica obrigatória da área de TIC, com 19 discordâncias em 59 manifestações (32,2%); as contratações sem alinhamento demonstrado ao planejamento de TIC e ao Plano de Contratações Anual, com 20 em 75 (26,7%); e a inexistência ou fragilidade de processo formal e padronizado para contratações de TIC, com 18 em 70 (25,7%).

![Manifestações sobre as situações encontradas do Achado 6](../99-Avaliacao_Comentarios_Gestor/img/achado-6-situacoes.png){#fig:comentarios_gestor_achado_6#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

A análise das discordâncias deve verificar se as contratações de TIC foram submetidas a processo padronizado e proporcional ao risco, à complexidade e ao valor, com participação da área técnica e vínculo demonstrado com o planejamento de TIC e o Plano de Contratações Anual. A regularidade formal do procedimento licitatório, isoladamente, não comprova a suficiência da governança técnica da contratação de TIC.

## 5.3. Pedidos de reavaliação de evidências

Os pedidos de reavaliação de evidências constituem universo distinto das discordâncias sobre os achados. Enquanto estas questionam as situações e os encaminhamentos constantes dos relatórios individuais, os pedidos de reavaliação pretendem rever respostas anteriormente ajustadas em razão da insuficiência ou não conformidade das evidências apresentadas.

Foram identificadas 103 organizações elegíveis com itens ou subitens avaliados como não conformes. Houve pedido de reavaliação em 340 combinações (48,1%), apresentado por 56 organizações. Foram recebidos 333 comentários e 116 anexos.

![Questões-base com maior número de pedidos de reavaliação](../99-Avaliacao_Comentarios_Gestor/img/04-reavaliacoes-por-questao.png){#fig:comentarios_gestor_reavaliacoes#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

As questões 2504, 2802, 2708, 2801, 2804 e 2102 concentraram o maior número absoluto de pedidos. As novas evidências devem ser examinadas individualmente para verificar se comprovam a afirmação original ou se permanecem insuficientes.

: Questões-base com maior número de pedidos de reavaliação {#tbl:comentarios_gestor_reavaliacoes_tabela#}

| Questão-base | Elegíveis | Pedidos | % dos elegíveis | Arquivos |
|---|---:|---:|---:|---:|
| Q2504 | 56 | 27 | 48,2% | 10 |
| Q2802 | 55 | 25 | 45,5% | 11 |
| Q2708 | 38 | 21 | 55,3% | 8 |
| Q2801 | 32 | 20 | 62,5% | 4 |
| Q2804 | 48 | 20 | 41,7% | 7 |
| Q2102 | 39 | 20 | 51,3% | 10 |
| Q2201 | 30 | 15 | 50,0% | 5 |
| Q2501 | 30 | 14 | 46,7% | 6 |
| Q2701 | 28 | 14 | 50,0% | 3 |
| Q0103 | 31 | 13 | 41,9% | 6 |
| Q1001 | 30 | 13 | 43,3% | 7 |
| Q2702 | 28 | 13 | 46,4% | 3 |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

Após a validação conjunta das duas seções, três pedidos já saneados de modo seguro na seção de manifestação quanto aos achados foram retirados da segunda para evitar dupla avaliação. Os 337 casos remanescentes foram submetidos à decisão técnica: 22 foram acolhidos integralmente (6,5%), 24 parcialmente (7,1%) e 291 não foram acolhidos (86,4%). O acolhimento parcial foi aplicado quando apenas parte dos itens reunidos na solicitação recebeu comprovação suficiente.

## 5.4. Resultado da avaliação das manifestações

Na primeira seção, 261 manifestações demandaram avaliação individualizada: as 236 discordâncias e as 25 declarações de atendimento concluído. Desse conjunto, 46 foram acolhidas integralmente, seis foram parcialmente acolhidas e alteraram parte dos fundamentos, e 209 não foram acolhidas. As demais manifestações de concordância sem atendimento concluído não tiveram os eventuais anexos avaliados.

: Resultado consolidado da avaliação {#tbl:comentarios_gestor_resultado_avaliacao#}

| Seção avaliada | Acolhida | Parcialmente acolhida | Não acolhida | Total |
|---|---:|---:|---:|---:|
| Situações submetidas a avaliação individualizada | 46 | 6 | 209 | 261 |
| Reavaliação de respostas e evidências | 22 | 24 | 291 | 337 |

<div custom-style="FonteImagem">(Fonte: elaboração própria a partir da avaliação consolidada)</div>

A distribuição proporcional dos resultados das duas seções é apresentada na [@fig:comentarios_gestor_resultados_avaliacao].

![Resultado consolidado da avaliação dos comentários do gestor](../99-Avaliacao_Comentarios_Gestor/img/05-resultados-avaliacao.png){#fig:comentarios_gestor_resultados_avaliacao#}
<div custom-style="FonteImagem">(Fonte: elaboração própria a partir da avaliação consolidada)</div>

A predominância de não acolhimentos decorreu, em grande parte, do próprio teor das respostas. Somadas, as 626 concordâncias sem medida adotada e as 584 declarações de providências em curso representam 82,3% das manifestações sobre situações. Planos em elaboração, processos iniciados, compromissos futuros e providências posteriores não demonstram, por si sós, conformidade.

Também foram mantidas situações quando os elementos apresentados eram declaratórios, incompletos, sem vigência demonstrada ou incapazes de comprovar todos os atributos exigidos, como formalização, abrangência, atualização, monitoramento e funcionamento efetivo.

Documentos gerais ou exemplos pontuais tampouco foram considerados suficientes quando demonstravam apenas parte da prática avaliada. Restrições de pessoal, orçamento ou estrutura e dependência de terceiros contextualizam a dificuldade de implementação, mas não eliminam o risco nem comprovam conformidade.

## 5.5. Ajustes e impactos nos resultados

A consolidação das duas seções e das revisões técnicas documentadas resultou em 160 ajustes distintos, distribuídos por 41 organizações e 73 itens do questionário. Os ajustes restauraram respostas inicialmente declaradas e tecnicamente sustentadas.

Na comparação por identidade, 47 situações deixaram de subsistir em 28 organizações, enquanto oito situações foram acrescentadas pela recomposição das condições avaliadas. O estoque agregado apresentou redução líquida de 39 registros, passando de 1.458 para 1.419, queda de 2,7%. Foram ainda afastadas 11 marcações de achado em nove organizações, reduzindo-se o total de 602 para 591.

O iGovTI aumentou em 23 das 113 organizações com resposta válida, sem redução em qualquer organização. A média passou de 0,1841 para 0,1890, acréscimo de 0,0049, equivalente a 0,49 ponto percentual. Entre as 23 organizações alcançadas, o aumento médio foi de 2,42 pontos percentuais e o maior acréscimo individual foi de 16,01 pontos percentuais.

: Síntese dos impactos dos comentários do gestor {#tbl:comentarios_gestor_impactos#}

| Dimensão | Resultado |
|---|---:|
| Ajustes distintos aplicados | 160 |
| Organizações com respostas ajustadas | 41 |
| Situações removidas por identidade | 47, em 28 organizações |
| Redução líquida do estoque de situações | 39, de 1.458 para 1.419 |
| Achados afastados | 11, em 9 organizações |
| Redução do estoque de achados | de 602 para 591 |
| Organizações com aumento do iGovTI | 23 |
| Variação da média do iGovTI | de 0,1841 para 0,1890 |
| Organizações com impacto em situação, achado ou iGovTI | 34 |

<div custom-style="FonteImagem">(Fonte: elaboração própria a partir da comparação dos resultados anterior e posterior aos comentários do gestor)</div>

A [@fig:comentarios_gestor_impactos_organizacoes] apresenta o alcance organizacional das avaliações da etapa de comentários do gestor.

![Organizações alcançadas pelos impactos dos comentários do gestor](../99-Avaliacao_Comentarios_Gestor/img/06-impactos-organizacoes.png){#fig:comentarios_gestor_impactos_organizacoes#}
<div custom-style="FonteImagem">(Fonte: elaboração própria a partir da comparação dos resultados anterior e posterior aos comentários do gestor)</div>

O alcance foi material e individualizável, embora não tenha alterado de forma ampla o diagnóstico consolidado da fiscalização.

## 5.6. Manifestações das organizações sem resposta válida

Das seis organizações sem resposta válida ao questionário iGovTI 2026, EMOP e PESAGRO responderam à etapa de comentários e confirmaram a ausência de resposta válida, sem apresentar justificativa textual ou arquivo comprobatório. CEHAB, SEDCON, SEPOL e SESP não apresentaram manifestação.

As duas confirmações corroboram a inexistência de resposta válida nas bases processadas, mas não constituem, por si mesmas, análise de responsabilidade. Para as quatro organizações sem manifestação, permanece a ausência de esclarecimentos nesta etapa. Conforme exposto na Seção 4.5, eventual apuração deverá considerar os registros de comunicação, ciência, prazos e circunstâncias individualizadas, com garantia do contraditório.

## 5.7. Conclusão

O contraditório confirmou a aderência geral do diagnóstico: 84,0% das manifestações concordaram com as situações encontradas. Ao mesmo tempo, produziu correções concretas e rastreáveis, com 52 acolhimentos integrais ou parciais nas 261 manifestações submetidas a decisão técnica individualizada e 46 acolhimentos integrais ou parciais nos 337 pedidos de reavaliação remanescentes.

O saldo final foi de 160 ajustes em 41 organizações, com impacto em situação inconforme, achado ou iGovTI para 34 organizações. Foram removidas 47 situações por identidade, afastadas 11 marcações de achado e elevados os índices de 23 organizações. Apesar desses efeitos, permaneceram 1.419 situações e 591 marcações por organização e achado no estado atualizado, e o aumento médio do iGovTI foi de 0,49 ponto percentual. As manifestações acolhidas corrigiram conclusões específicas, mas não afastaram o quadro estrutural de baixa maturidade identificado pela fiscalização.

As providências em curso e as correções posteriores também fornecem subsídios para os planos de ação. Seu acompanhamento deverá verificar responsáveis, prazos, abrangência e evidências de implementação efetiva. A metodologia, a participação, as razões de não acolhimento e a memória detalhada dos impactos constam do Anexo "AN08 – Avaliação dos comentários do gestor".

Após a etapa de comentários dos gestores, a Equipe de Auditoria promoveu simplificação dos procedimentos de auditoria. A revisão refinou regras de identificação e eliminou sobreposições. Os resultados apresentados neste relatório foram integralmente recalculados com base nos procedimentos revisados, inclusive nos cenários pós-ajuste inicial, pós-avaliação de evidências e pós-comentários do gestor. Por essa razão, as quantidades finais não são diretamente comparáveis às constantes dos relatórios preliminares.

\newpage

# 6. CONSIDERAÇÕES FINAIS

A presente fiscalização avaliou a maturidade da governança e da gestão de tecnologia da informação e comunicação no âmbito das organizações jurisdicionadas, por meio do iGovTI 2026, da análise longitudinal em relação ao ciclo anterior e da execução de procedimentos de auditoria voltados à validação das informações autodeclaradas e das evidências documentais encaminhadas.

Os resultados demonstram que a governança e a gestão de TIC ainda se encontram, de forma predominante, em estágio inicial de maturidade. Das 113 organizações avaliadas, 99 obtiveram resultado inferior a 0,40 no iGovTI 2026, concentrando-se nos níveis Inexpressivo e Iniciando. A baixa mediana do índice e a concentração dos resultados nos quartis inferiores indicam que as fragilidades observadas não se restringem a casos isolados, mas compõem quadro abrangente de insuficiência de formalização, coordenação, planejamento, capacidade institucional e controle operacional da TIC.

A comparação longitudinal entre os ciclos de 2023 e 2026, realizada sobre bases ajustadas e comparáveis, apresenta duas leituras complementares. O cenário-base indica evolução das respostas declaradas: a média passou de 0,180 para 0,248. No cenário final, após a avaliação das evidências e dos comentários dos gestores, a média ficou em 0,189, e os resultados não permitem afirmar que houve melhora ou piora geral. A melhora da Estrutura de Segurança da Informação foi confirmada nos dois cenários. Esse quadro recomenda cautela na leitura da evolução, sem desconsiderar os avanços declarados nem atribuir automaticamente à piora institucional as reduções decorrentes de uma verificação documental mais abrangente.

Os procedimentos de auditoria confirmaram a materialidade das fragilidades apontadas pelo índice. Foram consolidados seis achados, relacionados à estrutura de TIC, governança de TIC, planejamento de TIC, capacidade institucional, gestão de serviços de TIC e contratações de TIC. Em todos esses temas, verificou-se incidência expressiva de situações inconformes, com destaque para fragilidades na definição de papéis e responsabilidades, na atuação da alta administração, na integração entre planejamento, orçamento e contratações, na composição e capacitação da força de trabalho, no controle de serviços, ativos e incidentes e na governança técnica das aquisições de tecnologia.

A preservação dos três cenários amplia a transparência do diagnóstico. No cenário-base de autodeclaração saneada, a média do iGovTI foi 0,235 e a execução das regras revisadas produziu 565 sinalizações e 1.252 situações. Após a avaliação das evidências, a média passou a 0,184, com 602 marcações de achado e 1.458 situações; após os comentários dos gestores, alcançou 0,189, com 591 marcações e 1.419 situações. A diferença evidencia a distância entre o que foi autodeclarado, o que pôde ser documentalmente assegurado e o que foi revisto no contraditório, sem autorizar a conclusão automática de que toda prática não comprovada inexista.

As conclusões e os encaminhamentos adotam o cenário pós-comentários do gestor, por ser o estado que incorpora a validação documental e o contraditório. O cenário-base permanece apresentado como referência declaratória, sujeito tanto a sobrestimar práticas insuficientemente demonstradas quanto a não refletir atividades que os procedimentos, dentro dos limites de escopo e dos meios operacionais da fiscalização, não conseguiram assegurar.

Ressalta-se que a metodologia empregada não teve por objetivo identificar causas específicas para cada inconformidade. Por essa razão, os encaminhamentos propostos concentram-se na correção das fragilidades constatadas e no aprimoramento proporcional das capacidades institucionais, preservando espaço para que cada organização, conforme seu porte, complexidade, riscos e contexto administrativo, defina os meios adequados para implementar as melhorias necessárias.

Conclui-se que o trabalho alcançou seu objetivo ao produzir diagnóstico consolidado da maturidade de governança e gestão de TIC, validar evidências apresentadas pelos jurisdicionados, identificar fragilidades recorrentes e estruturar encaminhamentos individualizados e proporcionais.

Os resultados indicam a necessidade de atuação indutora deste Tribunal para promover a formalização de estruturas e processos, fortalecer a governança e a capacidade institucional de TIC e aprimorar o controle das contratações, dos serviços e dos riscos tecnológicos no âmbito das organizações fiscalizadas.

\newpage

# 7. PROPOSTA DE ENCAMINHAMENTO

**CONSIDERANDO** o pleno atendimento ao objetivo proposto pela auditoria, qual seja, o de avaliar o grau de adoção de boas práticas de governança e gestão de tecnologia da informação e comunicação pelos jurisdicionados;

**CONSIDERANDO** que o foco do presente trabalho é induzir os jurisdicionados a maior maturidade em governança e gestão de TIC, em alinhamento com modelos consagrados como o COBIT 2019 e o ITIL 4;

**CONSIDERANDO** que a governança e a gestão de TIC não se esgotam nas práticas abordadas nesta auditoria, e que devem ser encaradas como um processo de melhoria contínua, norteado por mecanismos de direção, avaliação e monitoramento, centrados na definição de papéis, responsabilidades, indicadores e metas;

**CONSIDERANDO** o caráter orientador e dialógico do presente trabalho, assim como o alinhamento à diretriz de incremento de eficiência e efetividade na gestão administrativa;

**CONSIDERANDO** o caráter sensível das análises e informações constantes dos 113 relatórios individuais anexos (AN12 a AN124), correspondentes às organizações que apresentaram resposta válida e foram avaliadas, e a necessidade de classificá-los como informação reservada, nos termos do inciso I, § 3º, art. 8º c/c incisos IV, V, VIII do art. 9º da Resolução TCE-RJ nº 433/2023;

**CONSIDERANDO** que os resultados decorrentes das ações previstas no Plano de Ação poderão ser objeto de avaliação futura por meio de Monitoramento, considerando os preceitos definidos na Resolução TCE-RJ nº 422/2023;

**CONSIDERANDO** que a metodologia empregada neste trabalho não abordou as causas específicas dos problemas identificados e que as recomendações focam na implementação de medidas de governança e gestão de TIC baseadas no COBIT 2019 e no ITIL 4, conforme os critérios e referenciais adotados na auditoria;

Sugere-se ao Egrégio Plenário desta Corte de Contas a adoção das seguintes propostas:

1. **COMUNICAÇÃO COM DETERMINAÇÃO** à Secretaria Geral da Presidência, por meio da sua coordenadoria competente, para que encaminhe, em anexo aos ofícios de comunicação da decisão, cópia do Acórdão proferido e do respectivo relatório individual (AN12 a AN124) a cada uma das 113 organizações que apresentaram resposta válida e foram avaliadas, de forma a garantir a ciência efetiva acerca da decisão proferida por esta Corte, **tendo em vista o caráter sigiloso dos anexos individuais, em que cada organização destinatária só deve ter acesso ao seu próprio relatório individual**;
2. **COMUNICAÇÃO COM DETERMINAÇÃO** às 113 organizações que apresentaram resposta válida, foram avaliadas e são destinatárias dos relatórios individuais anexos (AN12 a AN124), nos termos do artigo 15, inciso I, do Regimento Interno deste Tribunal, para que **elaborem, no prazo máximo de 60 (sessenta) dias a contar da ciência da decisão plenária, plano de ação estruturado**, formalmente registrado em processo administrativo eletrônico próprio, destinado ao registro e ao acompanhamento de sua execução, contemplando as medidas necessárias ao cumprimento das **DETERMINAÇÕES** e à avaliação da adoção das **RECOMENDAÇÕES** dispostas no respectivo **RELATÓRIO INDIVIDUAL**, alertando-as de que o não atendimento injustificado as sujeita às sanções previstas no art. 63 da Lei Complementar Estadual n.º 63/1990, sendo desnecessário o encaminhamento de comprovação ou esclarecimentos nos autos deste processo, já que a verificação quanto ao atendimento poderá ser realizada em auditoria futura desta Corte de Contas.

Para orientar a elaboração do plano de ação, apresenta-se o modelo referencial da [@tbl:modelo_plano_acao]. Cada uma das 113 organizações avaliadas deverá adaptá-lo às determinações e recomendações constantes de seu próprio relatório individual, indicando medidas, responsáveis e prazos compatíveis com sua realidade institucional.

: Modelo referencial de plano de ação {#tbl:modelo_plano_acao#}

| Determinação ou recomendação | Medida a adotar | Etapas ou providências | Unidade e responsável | Prazo | Indicador ou evidência de conclusão |
|---|---|---|---|---|---|
| [Indicar o item do relatório individual] | [Descrever a medida] | [Informar as principais etapas] | [Indicar a unidade e o responsável] | [Indicar a data ou o período] | [Indicar o documento, ato, registro ou resultado esperado] |

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

3. **ABERTURA DE PROCESSO APARTADO PARA APURAÇÃO DE POSSÍVEL OBSTRUÇÃO À AUDITORIA**, para cada uma das organizações fiscalizadas que não apresentaram resposta válida ao questionário eletrônico, apesar das comunicações e reiterações registradas no Anexo AN10, a saber: **Companhia Estadual de Habitação do Rio de Janeiro (CEHAB)**, **Empresa de Obras Públicas do Estado do Rio de Janeiro (EMOP)**, **Empresa de Pesquisa Agropecuária do Estado do Rio de Janeiro (PESAGRO)**, **Secretaria de Estado de Defesa do Consumidor (SEDCON)**, **Secretaria de Estado de Polícia Civil (SEPOL)** e **Secretaria de Estado de Segurança Pública (SESP)**, com expedição de **NOTIFICAÇÃO**, nos termos regimentais, para que os respectivos responsáveis apresentem razões de defesa acerca da ausência de resposta válida às solicitações da fiscalização, conduta passível de aplicação de multa, nos termos do art. 63, incisos V e VI, da Lei Complementar Estadual n.º 63/1990;
4. **COMUNICAÇÃO às Unidades de Controle Interno das 113 organizações que apresentaram resposta válida, foram avaliadas e são destinatárias de relatório individual,** nos termos do artigo 15, inciso I, do Regimento Interno deste Tribunal, para que tomem **CIÊNCIA** do inteiro teor do presente Relatório de Auditoria Governamental, bem como do Relatório Individual da correspondente organização (AN12 a AN124), e acompanhem a elaboração e a execução do respectivo plano de ação, a fim de assegurar seu efetivo cumprimento;
5. **ARQUIVAMENTO** do presente processo.


\newpage


O presente relatório foi objeto de supervisão conforme as disposições da Portaria SGE n° 05/2019, no Manual de Auditoria Governamental do TCE-RJ, aprovado pela Resolução nº 373, de 16/06/21 e em material armazenado nos assentamentos internos desta Coordenadoria, estando, portanto, **APROVADO** por esta supervisão e encaminhado à sua apreciação para adoção das medidas cabíveis.

**CAD-TI, {{ data_hoje }}**

|  |  |  |
| --- | --- | --- |
| **AUGUSTO CÉSAR BENVENUTO DE ALMEIDA**  **Matrícula 02/4823** | Auditor de Controle Externo | Equipe de Auditoria |
| **JOÃO PAULO DE FREITAS RAMIREZ**  **Matrícula 02/4820** | Auditor de Controle Externo | Equipe de Auditoria |
| **BRUNO MATTOS SOUZA DE SOUZA MELO**  **Matrícula 02/4258** | Auditor de Controle Externo | Supervisor |

\newpage

**DE ACORDO**.

À **SUB-CIDADANIA**, em prosseguimento.

**CAD-TI, {{ data_hoje }}**

**ALBERTO DE FONTES TAVARES NETO**

**Coordenador-Geral**

**Matrícula 02/4260**
