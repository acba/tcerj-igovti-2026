# Relatório técnico - relação entre achados de auditoria e notas do iGovTI 2026

## 1. Objetivo

Este relatório examina a relação entre os achados de auditoria registrados na execução dos procedimentos e as notas do iGovTI 2026 das organizações avaliadas. A análise foi feita com base nos artefatos efetivamente gerados no repositório, em especial a planilha de resultados do iGovTI 2026 e as tabelas consolidadas da execução da auditoria.

## 2. Fontes e método

Foram cruzadas duas bases principais: `02-Execucao/01-Questionario/04-Resultados_iGovTI/20260621-iGovTI-2026.xlsx`, aba `resultados`, e `02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/tabelas_consolidadas_auditoria.xlsx`, abas `Achados por Auditado` e `Situações Inconformes`.

A unidade de análise foi a organização auditada. Entraram no cruzamento **113 organizações** presentes simultaneamente nas bases. Para cada organização foram calculados a quantidade de achados distintos, a quantidade de situações inconformes, o iGovTI, o iGestTI, a nota de governança e os componentes do índice. Foram aplicadas correlações de Spearman e Pearson, comparação de médias por achado e análise de sensibilidade por recortes de iGovTI.

A correlação de Spearman foi priorizada porque a quantidade de achados é discreta e limitada a seis categorias. Essa limitação cria efeito de teto e exige cautela na interpretação.

## 3. Resultado executivo

O resultado mais importante é contraintuitivo: **na base analisada, a correlação entre iGovTI e quantidade de achados é positiva, não negativa**. Considerando todas as organizações, a correlação de Spearman entre `iGovTI` e `qtd_achados` foi **0.413** (p = **0.0000**) e entre `iGovTI` e `qtd_situacoes` foi **0.496** (p = **0.0000**).

Essa evidência **não deve ser interpretada como se organizações mais maduras fossem piores**. O padrão observado sugere outra leitura: os achados estão saturados em grande parte da amostra e a relação positiva é puxada sobretudo pela diferença entre o quartil mais baixo de iGovTI e as demais organizações. Quando se restringe a análise a organizações com iGovTI igual ou superior a 0,10, a correlação entre iGovTI e achados praticamente desaparece.

Em termos de auditoria, o principal insight é que **o iGovTI isolado não ordena bem a carga de achados depois que a organização sai do patamar mais baixo de maturidade**. A quantidade de situações inconformes é mais granular e informativa que a quantidade de achados distintos, mas também precisa ser lida em conjunto com a natureza dos achados.

## 4. Visão geral da base

- iGovTI médio: **0.188**; mediana: **0.136**.
- Média de achados distintos: **4.65**; mediana: **5.0**.
- Média de situações inconformes: **12.19**; mediana: **12.0**.
- Organizações com 4 ou mais achados: **97 de 113**, ou **85.8%**.
- Organizações com 5 ou 6 achados: **65 de 113**, ou **57.5%**.

A alta concentração em 4 a 6 achados mostra efeito de teto. Por isso, a contagem de achados distingue mal as organizações quando a maior parte delas já apresenta muitos achados. A quantidade de situações inconformes ajuda a recuperar parte dessa variação.

## 5. Correlações principais

### 5.1. Quantidade de achados

| Indicador | Spearman r | p-valor | n |
| --- | --- | --- | --- |
| iGestTI | 0.433 | 0.0000 | 113 |
| iGovTI | 0.413 | 0.0000 | 113 |
| EstruturaSegInfo | 0.339 | 0.0002 | 113 |
| RiscosTISegInfo | 0.320 | 0.0006 | 113 |
| ProcessoSegInfo | 0.299 | 0.0013 | 113 |

### 5.2. Quantidade de situações inconformes

| Indicador | Spearman r | p-valor | n |
| --- | --- | --- | --- |
| iGestTI | 0.515 | 0.0000 | 113 |
| iGovTI | 0.496 | 0.0000 | 113 |
| EstruturaSegInfo | 0.430 | 0.0000 | 113 |
| GovernancaTI | 0.369 | 0.0001 | 113 |
| ProcessoSegInfo | 0.368 | 0.0001 | 113 |

As correlações mais fortes aparecem com `iGestTI` e `iGovTI`. Isso indica que a carga de achados acompanha mais os componentes de gestão do que apenas governança formal. O resultado também sugere que as organizações que declaram ou evidenciam mais elementos de gestão acabam expondo mais pontos verificáveis, enquanto organizações de maturidade muito baixa podem gerar menos categorias distintas de achados, embora permaneçam em situação de risco.

![Relação entre iGovTI 2026 e achados de auditoria](img/achados_vs_igovti_2026.png){#fig:achados_vs_igovti_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria, com base nos artefatos de execução do iGovTI 2026)</div>

![Matriz de correlação entre achados e notas](img/correlacao_achados_notas_igovti_2026.png){#fig:correlacao_achados_notas_igovti_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria, com base nos artefatos de execução do iGovTI 2026)</div>

## 6. Análise de sensibilidade

| Recorte | n | Spearman iGovTI x achados | p achados | Spearman iGovTI x situações | p situações |
| --- | --- | --- | --- | --- | --- |
| Todos | 113 | 0.413 | 0.0000 | 0.496 | 0.0000 |
| iGovTI > 0 | 108 | 0.371 | 0.0001 | 0.464 | 0.0000 |
| iGovTI >= 0,10 | 70 | -0.039 | 0.7507 | 0.069 | 0.5725 |
| Sem Q1 de iGovTI | 84 | 0.109 | 0.3218 | 0.210 | 0.0553 |

A sensibilidade é decisiva para a interpretação. A associação positiva é estatisticamente relevante na base completa e permanece quando se excluem apenas organizações com iGovTI igual a zero. Contudo, quando a análise se restringe às organizações com iGovTI igual ou superior a 0,10, a relação entre nota e quantidade de achados deixa de ser relevante. O mesmo ocorre ao remover o primeiro quartil, embora a quantidade de situações ainda apresente uma associação fraca e limítrofe.

Isso indica que o iGovTI é útil para separar o estrato de maturidade extremamente baixa dos demais, mas **não é suficiente, sozinho, para prever a quantidade de achados entre organizações que já têm algum nível de estrutura ou prática declarada**.

## 7. Quartis de iGovTI

| Quartil iGovTI | Organizações | Mín. iGovTI | Máx. iGovTI | Média iGovTI | Média de achados | Média de situações | % com 5 ou 6 achados | % com até 3 achados |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q1 menor iGovTI | 29 | 0.000 | 0.066 | 0.029 | 3.793 | 8.724 | 20.7% | 31.0% |
| Q2 | 28 | 0.070 | 0.136 | 0.104 | 4.607 | 11.500 | 64.3% | 17.9% |
| Q3 | 28 | 0.137 | 0.239 | 0.183 | 5.214 | 14.786 | 82.1% | 3.6% |
| Q4 maior iGovTI | 28 | 0.239 | 0.777 | 0.441 | 5.000 | 13.857 | 64.3% | 3.6% |

![Achados e situações por quartil de iGovTI](img/achados_por_quartil_igovti_2026.png){#fig:achados_por_quartil_igovti_2026#}
<div custom-style="FonteImagem">(Fonte: elaboração própria, com base nos artefatos de execução do iGovTI 2026)</div>

O primeiro quartil tem menos achados distintos em média, mas isso não implica menor risco. Pelo contrário: ele reúne organizações com iGovTI muito baixo. A leitura mais plausível é que, em patamares muito baixos, a ausência ou incipiência de práticas reduz o número de categorias distintas materializadas pela regra de achado, enquanto nos quartis intermediários há mais elementos passíveis de verificação e, portanto, mais situações inconformes identificáveis.

## 8. Achados mais informativos

| Achado | n com achado | n sem achado | Média iGovTI com achado | Média iGovTI sem achado | Diferença sem - com | r ponto-bisserial | p-valor |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Achado 1 - Estrutura de TIC | 95 | 18 | 0.174 | 0.264 | 0.090 | -0.187 | 0.0475 |
| Achado 4 - Capacidade institucional | 106 | 7 | 0.186 | 0.220 | 0.034 | -0.047 | 0.6217 |
| Achado 3 - Planejamento de TIC | 91 | 22 | 0.185 | 0.199 | 0.013 | -0.030 | 0.7531 |
| Achado 6 - Contratações de TIC | 109 | 4 | 0.189 | 0.171 | -0.018 | 0.019 | 0.8442 |
| Achado 2 - Governança de TIC | 47 | 66 | 0.240 | 0.151 | -0.090 | 0.250 | 0.0075 |
| Achado 5 - Gestão de serviços de TIC | 77 | 36 | 0.238 | 0.082 | -0.156 | 0.411 | 0.0000 |

Dois padrões chamam atenção. O Achado 1 aparece associado a iGovTI menor, o que é coerente com a natureza estrutural da fragilidade. Já os Achados 2 e 5 aparecem, em média, em organizações com iGovTI mais alto. Isso reforça que determinados achados podem depender de maior densidade de práticas, serviços ou estruturas verificáveis. Em outras palavras, algumas organizações de maior pontuação não deixam de ter fragilidades; elas apenas têm fragilidades mais específicas e auditáveis.

## 9. Casos divergentes

### 9.1. Mais achados do que o esperado pela nota iGovTI

| Auditado | iGovTI | Maturidade | Achados | Situações | Achados esperados | Diferença |
| --- | --- | --- | --- | --- | --- | --- |
| SEPM | 0.061 | Inexpressivo | 6 | 15 | 4.48 | 1.52 |
| FLXIII | 0.088 | Inexpressivo | 6 | 16 | 4.52 | 1.48 |
| SETRAB | 0.092 | Inexpressivo | 6 | 13 | 4.52 | 1.48 |
| IVB | 0.113 | Inexpressivo | 6 | 14 | 4.55 | 1.45 |
| DETRO | 0.125 | Inexpressivo | 6 | 19 | 4.57 | 1.43 |
| FIPERJ | 0.129 | Inexpressivo | 6 | 16 | 4.57 | 1.43 |
| MACAÉ | 0.136 | Inexpressivo | 6 | 17 | 4.58 | 1.42 |
| DETRAN | 0.149 | Inexpressivo | 6 | 20 | 4.60 | 1.40 |
| SEEDUC | 0.152 | Iniciando | 6 | 18 | 4.60 | 1.40 |
| ARRAIAL DO CABO | 0.162 | Iniciando | 6 | 12 | 4.61 | 1.39 |

### 9.2. Menos achados do que o esperado pela nota iGovTI

| Auditado | iGovTI | Maturidade | Achados | Situações | Achados esperados | Diferença |
| --- | --- | --- | --- | --- | --- | --- |
| EMATER | 0.011 | Inexpressivo | 1 | 2 | 4.42 | -3.42 |
| SETUR | 0.132 | Inexpressivo | 2 | 6 | 4.57 | -2.57 |
| FUNARJ | 0.070 | Inexpressivo | 2 | 4 | 4.49 | -2.49 |
| SUDERJ | 0.015 | Inexpressivo | 2 | 4 | 4.42 | -2.42 |
| SEIJES | 0.000 | Inexpressivo | 2 | 4 | 4.41 | -2.41 |
| SEPLAG | 0.657 | Intermediário | 3 | 8 | 5.25 | -2.25 |
| CECIERJ | 0.158 | Iniciando | 3 | 8 | 4.61 | -1.61 |
| FTM | 0.107 | Inexpressivo | 3 | 8 | 4.54 | -1.54 |
| TURISRIO | 0.089 | Inexpressivo | 3 | 8 | 4.52 | -1.52 |
| LOTERJ | 0.088 | Inexpressivo | 3 | 7 | 4.52 | -1.52 |

Esses casos são úteis para revisão qualitativa. Organizações com muitos achados acima do esperado podem ter pontuação global que mascara fragilidades procedimentais relevantes. Organizações com poucos achados abaixo do esperado podem ter iGovTI muito baixo por ausência de práticas, mas menor número de categorias distintas de achados geradas pelas regras de execução.

## 10. Insights para controle externo

1. **O iGovTI é um sinalizador de risco, mas não substitui a execução dos procedimentos.** A relação encontrada é positiva e moderada na base completa, não a relação negativa simples que seria intuitiva.
2. **Há forte efeito de teto na quantidade de achados.** Como 85,8% das organizações têm 4 ou mais achados, a contagem de achados perde poder discriminatório. A quantidade de situações inconformes deve ser usada como medida complementar.
3. **O primeiro quartil de iGovTI deve ser tratado como grupo próprio.** Ele concentra maturidade extremamente baixa e menos achados distintos, o que pode refletir ausência de práticas verificáveis, não menor risco.
4. **Achados de governança e serviços podem aparecer mais em organizações com alguma maturidade.** Isso sugere que maior formalização ou maior escopo de serviços pode expor fragilidades específicas que não aparecem da mesma forma em organizações muito incipientes.
5. **Para seleção de fiscalizações futuras, recomenda-se combinar quatro variáveis:** iGovTI, quantidade de situações inconformes, natureza dos achados e divergência entre nota e achados esperados. Usar apenas a nota pode deixar de priorizar casos relevantes.
6. **Para comunicação do resultado, convém evitar narrativa linear do tipo “nota baixa gera mais achados”.** A evidência desta base aponta uma dinâmica mais complexa: baixa maturidade extrema, saturação de achados e maior granularidade das situações inconformes.

## 11. Limitações

- A análise é transversal e não demonstra causalidade.
- A quantidade de achados é limitada a seis categorias, o que cria efeito de teto.
- Os achados derivam das regras e do escopo dos procedimentos desta fiscalização; portanto, a ausência de determinado achado não deve ser lida como ausência de risco fora do escopo.
- Os dados de evidência e avaliações automatizadas devem ser tratados como insumos sujeitos à revisão humana da equipe de auditoria.

## 12. Artefatos gerados

- Planilha de apoio: `02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/analise_achados_igovti_2026.xlsx`.
- Gráficos: `02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/img/achados_vs_igovti_2026.png`, `correlacao_achados_notas_igovti_2026.png` e `achados_por_quartil_igovti_2026.png`.
