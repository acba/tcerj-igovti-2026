# Relatório técnico - relação entre achados de auditoria e notas do iGovTI 2026

## 1. Objetivo

Este relatório examina a relação entre os achados de auditoria registrados na execução dos procedimentos e as notas do iGovTI 2026 das organizações avaliadas. A análise foi atualizada com os artefatos mais recentes gerados em `/tmp/tcerj-igovti-2026`, contemplando resultados do índice, resultado estruturado da auditoria e tabelas consolidadas de achados, situações inconformes e encaminhamentos.

## 2. Fontes e método

Foram cruzadas três fontes: `/tmp/tcerj-igovti-2026/02-Execucao/01-Questionario/04-Resultados_iGovTI/20260621-iGovTI-2026.xlsx`, aba `resultados`; `/tmp/tcerj-igovti-2026/02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/resultado_auditoria.json`; e `/tmp/tcerj-igovti-2026/02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/tabelas_consolidadas_auditoria.xlsx`, abas `Achados por Auditado`, `Situações Inconformes`, `Encaminhamentos por Auditado` e `Ranking de Auditados`.

A unidade de análise foi a organização auditada. Entraram no cruzamento **113 organizações** presentes simultaneamente nas bases. Para cada organização foram calculados a quantidade de achados distintos, a quantidade de situações inconformes, a quantidade de encaminhamentos associados, o iGovTI, o iGestTI, a nota de governança e os componentes do índice. Foram aplicadas correlações de Spearman e Pearson, comparação de médias por achado, análise de sensibilidade por recortes de iGovTI, prevalência das situações inconformes e identificação de casos divergentes em relação à tendência geral.

A correlação de Spearman foi priorizada porque a quantidade de achados é discreta e limitada a seis categorias. Essa limitação cria efeito de teto e exige cautela na interpretação. O arquivo JSON estruturado foi usado como conferência cruzada da contagem de achados; foram identificadas **0 divergências** entre a contagem derivada das tabelas consolidadas e a contagem dos procedimentos no JSON.

## 3. Resultado executivo

O resultado central da análise é que **na base atualizada a correlação entre iGovTI e a carga de achados é negativa**. Considerando todas as organizações, a correlação de Spearman entre `iGovTI` e `qtd_achados` foi **-0.322** (p = **0.0005**) e entre `iGovTI` e `qtd_situacoes` foi **-0.598** (p = **< 0.0001**).

Essa evidência é coerente com a expectativa de auditoria: organizações com maior maturidade relativa tendem a apresentar menos achados e, principalmente, menos situações inconformes. A relação é mais forte quando se usa a quantidade de situações inconformes, porque a contagem de achados está quase saturada na amostra.

Em termos de controle externo, o principal insight é que **o iGovTI se relaciona com a carga de fragilidades, mas a quantidade de achados distintos perdeu poder discriminatório por efeito de teto**. A quantidade de situações inconformes é mais granular e informativa, pois diferencia organizações que materializam os mesmos achados em poucas ou muitas fragilidades concretas.

## 4. Visão geral da base

- iGovTI médio: **0.188**; mediana: **0.136**.
- Média de achados distintos: **5.743**; mediana: **6.0**.
- Média de situações inconformes: **22.301**; mediana: **23.0**.
- Marcações de achados por auditado: **649**.
- Situações inconformes registradas: **2520**.
- Encaminhamentos associados nas tabelas consolidadas: **2520**.
- Organizações com 4 ou mais achados: **113 de 113**, ou **100.0%**.
- Organizações com 5 ou 6 achados: **106 de 113**, ou **93.8%**.
- Organizações com todos os 6 achados: **91 de 113**, ou **80.5%**.

A alta concentração em 5 a 6 achados mostra forte efeito de teto. Nessa configuração, a simples contagem de achados distingue mal as organizações em situação crítica. A quantidade de situações inconformes recupera parte da granularidade, pois diferencia organizações que materializam os mesmos achados em poucas ou muitas fragilidades concretas.

## 5. Correlações principais

### 5.1. Quantidade de achados

| Indicador | Spearman r | p Spearman | Pearson r | p Pearson | n |
| --- | --- | --- | --- | --- | --- |
| PlanejamentoTI | -0.335 | 0.0003 | -0.471 | < 0.0001 | 113 |
| iGovTI | -0.322 | 0.0005 | -0.594 | < 0.0001 | 113 |
| GerirSoluçõesTI | -0.315 | 0.0007 | -0.582 | < 0.0001 | 113 |
| ProcessoSegInfo | -0.313 | 0.0007 | -0.479 | < 0.0001 | 113 |
| GovernancaTI | -0.305 | 0.0010 | -0.582 | < 0.0001 | 113 |
| iGestTI | -0.299 | 0.0013 | -0.539 | < 0.0001 | 113 |

### 5.2. Quantidade de situações inconformes

| Indicador | Spearman r | p Spearman | Pearson r | p Pearson | n |
| --- | --- | --- | --- | --- | --- |
| PlanejamentoTI | -0.659 | < 0.0001 | -0.763 | < 0.0001 | 113 |
| iGestTI | -0.628 | < 0.0001 | -0.771 | < 0.0001 | 113 |
| iGovTI | -0.598 | < 0.0001 | -0.769 | < 0.0001 | 113 |
| RiscosTISegInfo | -0.445 | < 0.0001 | -0.559 | < 0.0001 | 113 |
| ProcessoSegInfo | -0.444 | < 0.0001 | -0.592 | < 0.0001 | 113 |
| GovernancaTI | -0.434 | < 0.0001 | -0.679 | < 0.0001 | 113 |

As correlações mais fortes com situações inconformes aparecem em `PlanejamentoTI`, `iGestTI` e `iGovTI`. Para situações inconformes, a associação com `iGestTI` chegou a **-0.628**. Esse resultado indica que a carga de fragilidades acompanha fortemente os componentes de gestão, planejamento e operação, e não apenas a governança formal. Na prática, organizações com melhor pontuação nesses componentes tendem a apresentar menos situações inconformes.

![Relação entre iGovTI 2026 e achados de auditoria](img/achados_vs_igovti_2026.png){#fig:achados_vs_igovti_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria, com base nos artefatos de execução do iGovTI 2026)</div>

![Matriz de correlação entre achados e notas](img/correlacao_achados_notas_igovti_2026.png){#fig:correlacao_achados_notas_igovti_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria, com base nos artefatos de execução do iGovTI 2026)</div>

## 6. Análise de sensibilidade

| Recorte | n | Spearman iGovTI x achados | p achados | Spearman iGovTI x situações | p situações |
| --- | --- | --- | --- | --- | --- |
| Todos | 113 | -0.322 | 0.0005 | -0.598 | < 0.0001 |
| iGovTI > 0 | 108 | -0.307 | 0.0012 | -0.582 | < 0.0001 |
| iGovTI >= 0,10 | 70 | -0.397 | 0.0007 | -0.576 | < 0.0001 |
| Sem Q1 de iGovTI | 84 | -0.308 | 0.0044 | -0.579 | < 0.0001 |
| iGovTI >= mediana | 57 | -0.452 | 0.0004 | -0.549 | < 0.0001 |

A sensibilidade confirma a robustez da relação negativa. A associação permanece estatisticamente relevante na base completa, quando se excluem organizações com iGovTI igual a zero, quando se restringe a análise a iGovTI igual ou superior a 0,10 e quando se observa apenas a metade superior da distribuição. Ainda assim, a magnitude é maior e mais estável para situações inconformes do que para achados distintos, reforçando que **a quantidade de situações deve ser usada como medida principal de intensidade das fragilidades**.

## 7. Quartis e níveis de maturidade

### 7.1. Quartis de iGovTI

| Quartil iGovTI | Organizações | Mín. iGovTI | Máx. iGovTI | Média iGovTI | Média de achados | Média de situações | % com 5 ou 6 achados | % com até 3 achados |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q1 menor iGovTI | 29 | 0.000 | 0.066 | 0.029 | 5.931 | 24.000 | 100.0% | 0.0% |
| Q2 | 28 | 0.070 | 0.136 | 0.104 | 5.821 | 23.536 | 100.0% | 0.0% |
| Q3 | 28 | 0.137 | 0.239 | 0.183 | 5.821 | 22.536 | 100.0% | 0.0% |
| Q4 maior iGovTI | 28 | 0.239 | 0.777 | 0.441 | 5.393 | 19.071 | 75.0% | 0.0% |

![Achados e situações por quartil de iGovTI](img/achados_por_quartil_igovti_2026.png){#fig:achados_por_quartil_igovti_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria, com base nos artefatos de execução do iGovTI 2026)</div>

O primeiro quartil concentra a maior média de situações inconformes e praticamente todos os auditados dos três primeiros quartis têm 5 ou 6 achados. O quarto quartil apresenta redução da média de achados e, sobretudo, da média de situações. Isso sugere que a maturidade medida pelo iGovTI está associada a menor intensidade de fragilidades, mas a saturação dos achados faz com que a melhora apareça de forma mais clara nas situações inconformes.

### 7.2. Níveis de maturidade declarados pelo iGovTI

| Nível de maturidade | Organizações | Média iGovTI | Média de achados | Média de situações | % com 6 achados | % com 5 ou 6 achados |
| --- | --- | --- | --- | --- | --- | --- |
| Inexpressivo | 60 | 0.070 | 5.883 | 23.767 | 88.3% | 100.0% |
| Iniciando | 39 | 0.231 | 5.821 | 21.667 | 82.1% | 100.0% |
| Intermediário | 10 | 0.512 | 5.200 | 19.500 | 60.0% | 60.0% |
| Aprimorado | 4 | 0.730 | 4.250 | 13.500 | 0.0% | 25.0% |

O recorte por nível de maturidade reforça que a distribuição de achados não segue uma relação linear simples. Mesmo nos níveis superiores da amostra, a média de achados permanece elevada, o que recomenda separar a comunicação do índice da comunicação dos achados. O índice informa maturidade relativa; os achados indicam descumprimentos, fragilidades ou lacunas verificadas nos critérios da fiscalização.

## 8. Achados e situações mais informativos

### 8.1. Prevalência dos achados

| Achado | n com achado | n sem achado | % | Média iGovTI com | Média iGovTI sem | Diferença sem - com | r ponto-bisserial | p-valor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Achado 1 - Estrutura de TIC insuficiente para coordenar, gerir e sustentar a tecnologia... | 95 | 18 | 84.1% | 0.174 | 0.264 | 0.090 | -0.187 | 0.0475 |
| Achado 2 - Governança de TIC insuficiente para avaliar, dirigir e monitorar a tecnologia... | 107 | 6 | 94.7% | 0.161 | 0.663 | 0.502 | -0.636 | < 0.0001 |
| Achado 3 - Planejamento de TIC inexistente, insuficiente, desatualizado ou desconectado... | 109 | 4 | 96.5% | 0.170 | 0.681 | 0.511 | -0.534 | < 0.0001 |
| Achado 4 - Capacidade institucional insuficiente para sustentar a gestão de TIC e... | 113 | 0 | 100.0% | 0.188 |  |  |  |  |
| Achado 5 - Gestão de serviços de TIC incipiente, sem controle mínimo sobre serviços,... | 113 | 0 | 100.0% | 0.188 |  |  |  |  |
| Achado 6 - Fragilidades na governança técnica da fase preparatória das contratações de TIC | 112 | 1 | 99.1% | 0.184 | 0.657 | 0.473 | -0.251 | 0.0074 |

O achado mais disseminado foi **Achado 5 - Gestão de serviços de TIC incipiente, sem controle mínimo sobre serviços, ativos e incidentes**, presente em **113 organizações** (**100.0%**). Mesmo o achado menos frequente, **Achado 1 - Estrutura de TIC insuficiente para coordenar, gerir e sustentar a tecnologia da informação.**, alcançou **95 organizações** (**84.1%**), o que demonstra amplitude sistêmica das fragilidades encontradas.

### 8.2. Situações inconformes mais frequentes

| Achado | Situação inconforme | n | % |
| --- | --- | --- | --- |
| Achado 4 | Ausência de cargos, funções, perfis ou ocupações específicas de TIC e segurança da informação. | 113 | 100.0% |
| Achado 5 | Ausência ou fragilidade do processo de gestão de configuração. | 113 | 100.0% |
| Achado 4 | Modelo de operação de TIC predominantemente terceirizado ou externo, sem capacidade interna mínima... | 113 | 100.0% |
| Achado 5 | Inexistência de ANS, metas mínimas de níveis de serviço para os principais serviços de TIC. | 112 | 99.1% |
| Achado 4 | Lacunas de competências dos colaboradores e gestores de TIC e segurança da informação não são identificadas... | 112 | 99.1% |
| Achado 4 | Perfis profissionais de TIC e segurança da informação inexistentes, insuficientes ou não utilizados na... | 112 | 99.1% |
| Achado 4 | Ausência de força de trabalho mínima dedicada à TIC ou à segurança da informação. | 111 | 98.2% |
| Achado 5 | Inexistência ou fragilidade do processo de gestão de incidentes de TIC. | 111 | 98.2% |
| Achado 5 | Inexistência ou insuficiência do catálogo de serviços de TIC. | 110 | 97.3% |
| Achado 4 | A organização não definiu o quantitativo necessário de pessoal de TIC e segurança da informação. | 109 | 96.5% |
| Achado 5 | Inexistência ou fragilidade do inventário de ativos de TIC. | 109 | 96.5% |
| Achado 6 | Contratações de TIC sem aderência ao plano de TIC, ao plano de contratações ou à proposta orçamentária. | 108 | 95.6% |

![Situações inconformes mais frequentes](img/situacoes_mais_frequentes_igovti_2026.png){#fig:situacoes_mais_frequentes_igovti_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria, com base nos artefatos de execução do iGovTI 2026)</div>

A situação inconforme mais frequente foi **"Ausência de cargos, funções, perfis ou ocupações específicas de TIC e segurança da informação."**, registrada em **113 organizações** (**100.0%**). Esse tipo de leitura é especialmente útil para o corpo deliberativo porque indica problemas transversais, cuja resposta pode exigir orientação normativa, indução de boas práticas, priorização de capacitação ou monitoramento em bloco, e não apenas recomendações atomizadas por jurisdicionado.

### 8.3. Coocorrência de achados

Os pares de achados com maior coocorrência foram:

| Par de achados | n | % |
| --- | --- | --- |
| Achados 4 + 5 | 113 | 100.0% |
| Achados 4 + 6 | 112 | 99.1% |
| Achados 5 + 6 | 112 | 99.1% |

A coocorrência elevada mostra que as fragilidades não aparecem isoladamente. Em especial, deficiências de capacidade institucional, gestão de serviços e contratações tendem a compor o mesmo quadro de baixa capacidade de sustentação da TIC. Para a fiscalização, isso sugere que recomendações pontuais podem ter menor efetividade se não forem acompanhadas de medidas estruturantes de governança, força de trabalho, planejamento e responsabilização.

## 9. Casos divergentes

### 9.1. Mais achados do que o esperado pela nota iGovTI

| Auditado | iGovTI | Maturidade | Achados | Situações | Achados esperados | Diferença |
| --- | --- | --- | --- | --- | --- | --- |
| IASERJ | 0.497 | Intermediário | 6 | 26 | 5.16 | 0.84 |
| RJPREV | 0.459 | Intermediário | 6 | 20 | 5.23 | 0.77 |
| CEASA | 0.457 | Intermediário | 6 | 25 | 5.24 | 0.76 |
| TERESÓPOLIS | 0.442 | Intermediário | 6 | 23 | 5.27 | 0.73 |
| ISP | 0.441 | Intermediário | 6 | 23 | 5.27 | 0.73 |
| AGERIO | 0.434 | Intermediário | 6 | 21 | 5.28 | 0.72 |
| TCE-RJ | 0.379 | Iniciando | 6 | 22 | 5.38 | 0.62 |
| MESQUITA | 0.378 | Iniciando | 6 | 23 | 5.39 | 0.61 |
| AGENERSA | 0.356 | Iniciando | 6 | 19 | 5.43 | 0.57 |
| SES | 0.351 | Iniciando | 6 | 23 | 5.44 | 0.56 |
| FS | 0.344 | Iniciando | 6 | 19 | 5.45 | 0.55 |
| GSI | 0.334 | Iniciando | 6 | 19 | 5.47 | 0.53 |

### 9.2. Menos achados do que o esperado pela nota iGovTI

| Auditado | iGovTI | Maturidade | Achados | Situações | Achados esperados | Diferença |
| --- | --- | --- | --- | --- | --- | --- |
| CGE | 0.451 | Intermediário | 4 | 16 | 5.25 | -1.25 |
| EMATER | 0.011 | Inexpressivo | 5 | 21 | 6.08 | -1.08 |
| BARRA DO PIRAÍ | 0.037 | Inexpressivo | 5 | 23 | 6.03 | -1.03 |
| FUNARJ | 0.070 | Inexpressivo | 5 | 22 | 5.97 | -0.97 |
| LOTERJ | 0.088 | Inexpressivo | 5 | 23 | 5.93 | -0.93 |
| UENF | 0.098 | Inexpressivo | 5 | 23 | 5.91 | -0.91 |
| PRODERJ | 0.629 | Intermediário | 4 | 14 | 4.91 | -0.91 |
| MPERJ | 0.657 | Intermediário | 4 | 14 | 4.86 | -0.86 |
| SEPLAG | 0.657 | Intermediário | 4 | 13 | 4.86 | -0.86 |
| IOERJ | 0.127 | Inexpressivo | 5 | 22 | 5.86 | -0.86 |
| SETUR | 0.132 | Inexpressivo | 5 | 23 | 5.85 | -0.85 |
| CECIERJ | 0.158 | Iniciando | 5 | 22 | 5.80 | -0.80 |

Esses casos são úteis para revisão qualitativa. Organizações com muitos achados acima do esperado podem ter pontuação global que mascara fragilidades procedimentais relevantes. Organizações com poucos achados abaixo do esperado podem ter iGovTI muito baixo por ausência de práticas, mas menor número de categorias distintas de achados geradas pelas regras de execução. Nesses casos, a ausência relativa de achados não deve ser confundida com suficiência de controles.

## 10. Insights para controle externo

1. **O iGovTI é um sinalizador relevante de maturidade, mas não substitui a execução dos procedimentos.** A relação encontrada é negativa e estatisticamente relevante, sobretudo quando se observa a quantidade de situações inconformes.
2. **Há forte efeito de teto na quantidade de achados.** Como 100.0% das organizações têm 4 ou mais achados e 93.8% têm 5 ou 6, a contagem de achados perde poder discriminatório. A quantidade de situações inconformes deve ser usada como medida complementar.
3. **O primeiro quartil de iGovTI deve ser tratado como grupo prioritário.** Ele concentra maturidade muito baixa e a maior média de situações inconformes.
4. **A melhoria de maturidade aparece mais claramente na redução de situações do que na redução de achados.** Como alguns achados atingem praticamente toda a amostra, a contagem de situações é mais adequada para priorização e monitoramento.
5. **As situações inconformes mais frequentes indicam problemas sistêmicos.** Quando uma mesma situação aparece em grande parte da amostra, a resposta de controle externo pode combinar recomendações individuais com orientação transversal aos jurisdicionados.
6. **Para seleção de fiscalizações futuras, recomenda-se combinar quatro variáveis:** iGovTI, quantidade de situações inconformes, natureza dos achados e divergência entre nota e achados esperados. Usar apenas a nota pode deixar de priorizar casos relevantes.
7. **Para comunicação do resultado, convém evitar reduzir a análise à nota do índice.** A evidência desta base aponta uma dinâmica mais completa: maior iGovTI está associado a menos fragilidades, mas a saturação dos achados exige olhar a quantidade e a natureza das situações inconformes.

## 11. Limitações

- A análise é transversal e não demonstra causalidade.
- A quantidade de achados é limitada a seis categorias, o que cria efeito de teto.
- Os achados derivam das regras e do escopo dos procedimentos desta fiscalização; portanto, a ausência de determinado achado não deve ser lida como ausência de risco fora do escopo.
- As avaliações de evidências e os artefatos de execução automatizada devem ser tratados como insumos sujeitos à revisão humana da equipe de auditoria.
- As correlações foram calculadas sobre os dados consolidados disponíveis; alterações posteriores nos ajustes de resposta, comentários do gestor ou reavaliações de evidência podem modificar os resultados.

## 12. Artefatos gerados

- Script reexecutável: `scripts/analisar_achados_igovti_2026.py`.
- Planilha de apoio: `03-Relatorios/99-Avaliacao_IgovTi_Achados/analise_achados_igovti_2026.xlsx`.
- Gráficos: `03-Relatorios/99-Avaliacao_IgovTi_Achados/img/achados_vs_igovti_2026.png`, `correlacao_achados_notas_igovti_2026.png`, `achados_por_quartil_igovti_2026.png` e `situacoes_mais_frequentes_igovti_2026.png`.
