---
title: "ANEXO - Impacto da Avaliação de Evidências"
lang: pt-BR
figure-caption-position: above
---

\newpage

# 1. Objetivo

Este anexo apresenta a análise do impacto da avaliação de evidências sobre as respostas ao questionário iGovTI 2026 e, consequentemente, sobre o cálculo do índice. A análise busca distinguir o resultado que seria obtido apenas com os ajustes iniciais de saneamento das respostas daquele efetivamente apurado após a verificação das evidências apresentadas pelos auditados.

A comparação é relevante porque o iGovTI 2026 não se limitou à autodeclaração dos respondentes. As respostas afirmativas que exigiam comprovação foram submetidas a avaliação de evidências, e as situações em que a evidência não confirmou a prática declarada foram ajustadas na base de respostas. Assim, o índice final reflete, em maior medida, práticas demonstradas documentalmente, e não apenas práticas declaradas.

# 2. Metodologia da comparação

Foram considerados dois cenários:

* **Cenário com ajuste inicial**: base de respostas brutas do LimeSurvey, com aplicação exclusiva do arquivo `ajustes_respostas_questionario_inicial.xlsx`;
* **Cenário final pós-evidência**: resultado oficial do iGovTI 2026, calculado após todos os ajustes, inclusive os decorrentes da avaliação de evidências registrada em `ajustes_respostas_questionario_pos_avaliacao_evidencias.xlsx`.

O primeiro cenário foi gerado a partir da aplicação do ajuste inicial sobre a base `20260621-respostas-questionario-bruto.xlsx`. Em seguida, o iGovTI foi recalculado com a mesma metodologia aplicada ao resultado oficial. Como validação, aplicou-se também o ajuste pós-evidência sobre o cenário inicial e recalculou-se o índice; o resultado reproduziu exatamente o iGovTI final oficial, tanto nos valores dos indicadores quanto nos níveis de maturidade.

Os valores apresentados neste anexo utilizam a diferença **resultado final menos resultado com ajuste inicial**. Portanto, diferenças negativas indicam redução de pontuação após a avaliação das evidências.

Para avaliar o efeito da avaliação de evidências também sobre os achados e situações inconformes, a rotina de execução dos procedimentos de auditoria foi executada em dois cenários. No primeiro, utilizou-se a base de respostas brutas com os ajustes iniciais e apenas a fonte de informação do questionário. Nesse cenário, as ações de verificação originalmente dependentes do painel de avaliação de evidências foram neutralizadas em mapa temporário, utilizado apenas para a execução comparativa, para que não produzissem inconformidade sem a respectiva fonte probatória. No segundo, utilizou-se a base final pós-evidência, com a fonte de respostas ajustadas e o painel consolidado de avaliação de evidências. Desse modo, a comparação reflete o acréscimo produzido pela etapa de avaliação de evidências na execução dos procedimentos de auditoria.

: Síntese da base comparada {#tbl:impacto_evidencias_base#}

| Elemento analisado | Resultado |
|---|---:|
| Organizações no cenário com ajuste inicial | 113 |
| Organizações no cenário final | 113 |
| Registros de não conformidade no arquivo pós-evidência | 1.966 |
| Células efetivamente alteradas pelo ajuste pós-evidência | 1.964 |
| Organizações com pelo menos uma célula alterada | 103 |
| Organizações com redução no iGovTI | 90 |
| Organizações sem variação no iGovTI | 23 |
| Organizações com aumento no iGovTI | 0 |

<div custom-style="FonteImagem">(Fonte: elaboração própria, com base nas respostas ao questionário iGovTI 2026 e nos ajustes decorrentes da avaliação de evidências)</div>

# 3. Impacto agregado no iGovTI

A avaliação de evidências teve impacto material sobre o resultado agregado do iGovTI 2026. A média do índice passou de **0,235**, no cenário com apenas o ajuste inicial, para **0,184**, no cenário final, redução média de **0,051 ponto**. A mediana passou de **0,175** para **0,134**, redução de **0,041 ponto**.

Esse comportamento indica que a avaliação de evidências não produziu efeito pontual restrito a poucos auditados. Ao contrário, houve redução no iGovTI de **90 das 113 organizações**, equivalentes a **79,6%** do universo avaliado. Nenhuma organização apresentou aumento no índice em razão dos ajustes pós-evidência.

: Impacto agregado por indicador {#tbl:impacto_evidencias_indicadores#}

| Indicador | Média com ajuste inicial | Média final | Redução média | Organizações com redução |
|---|---:|---:|---:|---:|
| iGovTI | 0,235 | 0,184 | -0,051 | 90 |
| Governança de TI | 0,208 | 0,161 | -0,047 | 42 |
| Gestão de TI | 0,259 | 0,205 | -0,054 | 87 |
| Planejamento de TI | 0,381 | 0,291 | -0,091 | 44 |
| Serviços de TI | 0,234 | 0,140 | -0,094 | 53 |
| Gestão de riscos de TI e segurança da informação | 0,187 | 0,165 | -0,022 | 10 |
| Estrutura de segurança da informação | 0,275 | 0,258 | -0,017 | 11 |
| Processos de segurança da informação | 0,274 | 0,200 | -0,075 | 62 |
| Gestão de soluções de TI | 0,213 | 0,193 | -0,020 | 12 |

<div custom-style="FonteImagem">(Fonte: elaboração própria, com base na memória de cálculo do iGovTI 2026)</div>

Os maiores efeitos médios ocorreram em **Serviços de TI**, **Planejamento de TI** e **Processos de segurança da informação**. Esse resultado sugere que, nesses domínios, parte relevante das práticas declaradas dependia de evidências formais que não foram apresentadas ou não demonstraram suficientemente a adoção informada no questionário.

O impacto foi menor nas dimensões **Estrutura de segurança da informação**, **Gestão de soluções de TI** e **Gestão de riscos de TI e segurança da informação**. Essa menor redução não significa, necessariamente, melhor qualidade das evidências nessas dimensões; pode refletir menor quantidade de respostas afirmativas sujeitas a ajuste, menor peso relativo dos itens afetados ou concentração dos ajustes em grupos específicos de auditados.

# 4. Efeito nos níveis de maturidade

A avaliação de evidências também alterou a distribuição dos níveis de maturidade. No cenário com ajuste inicial, havia **50 organizações** no nível "Inexpressivo"; no cenário final, esse quantitativo subiu para **61 organizações**. O número de organizações em níveis iguais ou superiores a "Intermediário" caiu de **20** para **13**.

: Distribuição dos níveis de maturidade {#tbl:impacto_evidencias_maturidade#}

| Nível de maturidade | Cenário com ajuste inicial | Cenário final | Variação |
|---|---:|---:|---:|
| Inexpressivo | 50 | 61 | +11 |
| Iniciando | 43 | 39 | -4 |
| Intermediário | 14 | 9 | -5 |
| Aprimorado | 6 | 4 | -2 |

<div custom-style="FonteImagem">(Fonte: elaboração própria, com base na memória de cálculo do iGovTI 2026)</div>

Ao todo, **18 organizações** foram reclassificadas para nível inferior após a avaliação de evidências. A mudança mais frequente foi de "Iniciando" para "Inexpressivo", com **10 organizações**. Também houve **6 organizações** que passaram de "Intermediário" para "Iniciando", uma organização que passou de "Aprimorado" para "Intermediário" e uma organização que passou de "Aprimorado" diretamente para "Inexpressivo".

Esse deslocamento reforça a conclusão de que a avaliação documental afetou não apenas a pontuação numérica, mas a leitura qualitativa do estágio de maturidade. Em termos práticos, parte das organizações que, pela autodeclaração saneada, aparentava estar em estágio mais elevado não manteve esse posicionamento quando exigida a comprovação documental das práticas.

# 5. Organizações com maiores reduções de pontuação

As maiores reduções concentraram-se em organizações que apresentavam pontuação inicial relativamente alta e tiveram quantidade expressiva de respostas ajustadas após a avaliação de evidências. A redução mais acentuada ocorreu no DETRAN, cujo iGovTI passou de **0,843** para **0,149**, com queda de **0,694 ponto** e reclassificação de "Aprimorado" para "Inexpressivo".

: Organizações com maiores reduções no iGovTI {#tbl:impacto_evidencias_maiores_reducoes#}

| Organização | iGovTI com ajuste inicial | iGovTI final | Redução | Maturidade inicial | Maturidade final | Registros pós-evidência |
|---|---:|---:|---:|---|---|---:|
| DETRAN | 0,843 | 0,149 | -0,694 | Aprimorado | Inexpressivo | 118 |
| SEFAZ | 0,646 | 0,216 | -0,430 | Intermediário | Iniciando | 69 |
| RIOPREVIDENCIA | 0,625 | 0,391 | -0,234 | Intermediário | Iniciando | 44 |
| TERESÓPOLIS | 0,664 | 0,442 | -0,223 | Intermediário | Intermediário | 44 |
| SES | 0,556 | 0,351 | -0,204 | Intermediário | Iniciando | 52 |
| DPGE | 0,347 | 0,171 | -0,176 | Iniciando | Iniciando | 54 |
| CODERTE | 0,376 | 0,218 | -0,158 | Iniciando | Iniciando | 24 |
| DUQUE DE CAXIAS | 0,344 | 0,196 | -0,148 | Iniciando | Iniciando | 48 |
| SEEDUC | 0,299 | 0,152 | -0,147 | Iniciando | Iniciando | 26 |
| SEINFRA | 0,341 | 0,212 | -0,129 | Iniciando | Iniciando | 23 |

<div custom-style="FonteImagem">(Fonte: elaboração própria, com base na memória de cálculo do iGovTI 2026 e nos ajustes decorrentes da avaliação de evidências)</div>

Esses resultados devem ser interpretados com cautela. A existência de muitos registros pós-evidência não equivale, isoladamente, à maior perda no índice, pois o impacto depende do peso dos itens na estrutura do iGovTI, da pontuação inicial da organização e da dimensão atingida. Ainda assim, a concentração de reduções em organizações com pontuações iniciais mais elevadas indica que a avaliação de evidências funcionou como mecanismo relevante de controle da consistência das autodeclarações.

# 6. Itens mais afetados pela avaliação de evidências

Os registros pós-evidência concentraram-se em práticas ligadas à segurança dos recursos de processamento da informação, às contratações de tecnologia da informação, ao catálogo e níveis de serviço, ao planejamento de TI e ao modelo de gestão de TI.

: Itens-base com maior quantidade de registros pós-evidência {#tbl:impacto_evidencias_itens#}

| Item-base | Tema avaliado | Registros | Auditados afetados |
|---|---|---:|---:|
| q2504 | Gestão da segurança dos recursos de processamento da informação, inclusive nuvem | 267 | 56 |
| q2802 | Processo de planejamento anual das contratações | 179 | 55 |
| q2801 | Processos de trabalho relativos às contratações de TI | 143 | 32 |
| q2201 | Catálogo de serviços de TI e monitoramento de níveis de serviço | 90 | 30 |
| q2102 | Plano de tecnologia da informação vigente | 89 | 39 |
| q1001 | Modelo de gestão de tecnologia da informação | 87 | 30 |
| q2803 | Publicidade dos documentos das contratações de TI | 80 | 15 |
| q2204 | Gestão de incidentes de serviços de TI e de segurança da informação | 76 | 27 |
| q2501 | Gestão de ativos associados à informação | 74 | 30 |
| q2203 | Gestão de configuração e ativos de serviços de TI | 73 | 34 |

<div custom-style="FonteImagem">(Fonte: elaboração própria, com base no arquivo de ajustes decorrentes da avaliação de evidências)</div>

A concentração em q2504, q2802, q2801 e q2803 é coerente com as dimensões que mais perderam pontuação: **Serviços de TI**, **Planejamento de TI** e **Processos de segurança da informação**. Em especial, os itens de contratações de TI aparecem com frequência elevada, o que sugere fragilidade na comprovação de planejamento, formalização, transparência ou execução dos processos relacionados a contratações.

Também se observa volume expressivo de ajustes em itens de governança e gestão de serviços, como modelo de gestão de TI, plano de TI, catálogo de serviços, gestão de incidentes e gestão de configuração e ativos. Esses itens normalmente exigem evidências formais, atualizadas e institucionalizadas, como normas, planos, registros de execução, relatórios, publicações e atas. A ausência, insuficiência ou inadequação desses documentos reduz a confiabilidade da resposta afirmativa.

# 7. Organizações com maior conformidade nas evidências avaliadas

Além da análise das reduções, foi examinada a taxa de conformidade dos pareceres consolidados de avaliação de evidências. Essa taxa corresponde à proporção de conclusões avaliadas como "Conforme" em relação ao total de conclusões avaliadas para cada organização. Como o parecer consolidado é registrado por item ou afirmação avaliada, e não apenas por arquivo anexado, a leitura deve ser feita como conformidade das **conclusões de evidência avaliadas**.

Houve **4 organizações** em que todas as conclusões avaliadas foram consideradas conformes: **BARRA DO PIRAÍ**, **PETRÓPOLIS**, **SUDERJ** e **ARARUAMA**. A interpretação desse resultado deve considerar, contudo, que essas organizações tiveram baixo volume de itens avaliados, variando de 4 a 9 conclusões. Assim, o percentual de 100% indica consistência integral no conjunto analisado, mas não deve ser comparado diretamente com organizações que apresentaram dezenas de itens submetidos à avaliação.

: Organizações com todas as conclusões de evidência consideradas conformes {#tbl:impacto_evidencias_todas_conformes#}

| Organização | Conclusões avaliadas | Conclusões conformes | Conclusões não conformes | Taxa de conformidade |
|---|---:|---:|---:|---:|
| BARRA DO PIRAÍ | 9 | 9 | 0 | 100,0% |
| PETRÓPOLIS | 9 | 9 | 0 | 100,0% |
| SUDERJ | 5 | 5 | 0 | 100,0% |
| ARARUAMA | 4 | 4 | 0 | 100,0% |

<div custom-style="FonteImagem">(Fonte: elaboração própria, com base nos pareceres consolidados da avaliação de evidências)</div>

Considerando organizações com pelo menos 10 conclusões avaliadas, as maiores taxas de conformidade foram observadas em **SEPLAG**, **TCE-RJ**, **TJRJ**, **PRODERJ** e **NITERÓI**. Nesse grupo, a quantidade maior de itens avaliados torna a taxa mais informativa para comparação relativa, embora ainda dependa do perfil das práticas declaradas e do conjunto de evidências submetido por cada auditado.

: Organizações com maior taxa de conformidade, entre aquelas com pelo menos 10 conclusões avaliadas {#tbl:impacto_evidencias_maior_conformidade#}

| Organização | Conclusões avaliadas | Conclusões conformes | Conclusões não conformes | Taxa de conformidade |
|---|---:|---:|---:|---:|
| SEPLAG | 77 | 70 | 7 | 90,9% |
| TCE-RJ | 50 | 45 | 5 | 90,0% |
| TJRJ | 106 | 94 | 12 | 88,7% |
| PRODERJ | 78 | 69 | 9 | 88,5% |
| NITERÓI | 46 | 40 | 6 | 87,0% |
| ITAGUAÍ | 25 | 21 | 4 | 84,0% |
| MARICÁ | 48 | 40 | 8 | 83,3% |
| UENF | 22 | 18 | 4 | 81,8% |
| CASIMIRO DE ABREU | 27 | 22 | 5 | 81,5% |
| LOTERJ | 21 | 17 | 4 | 81,0% |

<div custom-style="FonteImagem">(Fonte: elaboração própria, com base nos pareceres consolidados da avaliação de evidências)</div>

Esses resultados mostram que a avaliação de evidências não produziu apenas reduções. Também permitiu identificar organizações cujas declarações foram, em maior proporção, confirmadas pela documentação apresentada. Em termos de confiabilidade das respostas, esses casos indicam melhor aderência entre autodeclaração e comprovação documental, especialmente quando a taxa elevada de conformidade veio acompanhada de volume relevante de itens avaliados.

# 8. Impacto nos achados e situações inconformes

Quando a auditoria é comparada no critério metodologicamente adequado, isto é, cenário inicial com apenas a fonte de respostas contra cenário final com respostas ajustadas e painel de avaliação de evidências, observa-se impacto relevante sobre os achados. No cenário com ajuste inicial e sem painel de evidências, foram identificadas **598 marcações de achados por auditado**. No cenário final, esse total passou para **625**, acréscimo de **27 marcações**.

O impacto foi ainda mais expressivo nas situações inconformes. O total passou de **1.887**, no cenário inicial, para **2.140**, no cenário final, com acréscimo de **253 situações inconformes**. O mesmo acréscimo ocorreu nos encaminhamentos associados. Não houve remoção de marcações: a avaliação de evidências apenas acrescentou achados, situações inconformes e encaminhamentos que não seriam identificados pela autodeclaração saneada isoladamente.

: Impacto dos ajustes pós-evidência nos achados e situações inconformes {#tbl:impacto_evidencias_achados_situacoes#}

| Medida | Cenário com ajuste inicial | Cenário final | Variação | Organizações com aumento | Organizações sem variação | Organizações com redução |
|---|---:|---:|---:|---:|---:|---:|
| Marcações de achados por auditado | 598 | 625 | +27 | 21 | 92 | 0 |
| Situações inconformes | 1.887 | 2.140 | +253 | 82 | 31 | 0 |
| Encaminhamentos associados | 1.887 | 2.140 | +253 | 82 | 31 | 0 |

<div custom-style="FonteImagem">(Fonte: elaboração própria, com base na execução comparativa dos procedimentos de auditoria)</div>

O acréscimo concentrou-se nos achados relativos a contratações de TIC e planejamento de TIC. O Achado 6 passou de **102** para **112** organizações, e o Achado 3 passou de **100** para **109**. Também houve aumento nos achados de estrutura de TIC, governança de TIC e gestão de serviços de TIC.

: Impacto por achado {#tbl:impacto_evidencias_por_achado#}

| Achado | Cenário com ajuste inicial | Cenário final | Variação |
|---|---:|---:|---:|
| 1. Estrutura de TIC insuficiente | 67 | 71 | +4 |
| 2. Governança de TIC insuficiente | 104 | 107 | +3 |
| 3. Planejamento de TIC insuficiente | 100 | 109 | +9 |
| 4. Capacidade institucional insuficiente | 113 | 113 | 0 |
| 5. Gestão de serviços de TIC insuficiente | 112 | 113 | +1 |
| 6. Fragilidades na fase preparatória das contratações de TIC | 102 | 112 | +10 |

<div custom-style="FonteImagem">(Fonte: elaboração própria, com base na execução comparativa dos procedimentos de auditoria)</div>

As situações inconformes com maior acréscimo foram aquelas em que a resposta afirmativa dependia de documentação formal capaz de demonstrar planejamento, aprovação, integração orçamentária, análise técnica ou inventário. O maior impacto ocorreu na situação relativa a contratações de TIC sem análise prévia e aprovação técnica obrigatória da área de TIC, cujo registro passou de **38** para **86** organizações.

: Situações inconformes com maior acréscimo {#tbl:impacto_evidencias_situacoes_maior_acrescimo#}

| Situação inconforme | Cenário com ajuste inicial | Cenário final | Variação |
|---|---:|---:|---:|
| Contratações de TIC sem análise prévia e aprovação técnica obrigatória da área de TIC | 38 | 86 | +48 |
| Ausência de aprovação formal do plano de TIC | 65 | 87 | +22 |
| Inexistência ou fragilidade do inventário de ativos de TIC | 85 | 106 | +21 |
| Plano de TIC sem vínculo demonstrado com orçamento e contratações de TIC | 89 | 108 | +19 |
| Contratações de TIC sem alinhamento demonstrado ao planejamento de TIC, ao plano de contratações ou à proposta orçamentária | 89 | 108 | +19 |
| Inexistência ou fragilidade de processo formal e padronizado para contratações de TIC | 85 | 99 | +14 |
| Comitê de TIC ou instância equivalente não instituído formalmente | 75 | 86 | +11 |
| Ausência de cargos, funções, perfis ou ocupações específicas de TIC e segurança da informação | 82 | 93 | +11 |
| Perfis profissionais de TIC e segurança da informação inexistentes, insuficientes ou não utilizados na escolha de gestores | 101 | 112 | +11 |
| Inexistência ou insuficiência do catálogo de serviços de TIC | 99 | 110 | +11 |

<div custom-style="FonteImagem">(Fonte: elaboração própria, com base na execução comparativa dos procedimentos de auditoria)</div>

As organizações com maior acréscimo de situações inconformes foram **SEFAZ** (+11), **DETRAN** (+10), **SES** (+10), **CGE** (+10), **RIOPREVIDENCIA** (+8), **FAPERJ** (+7) e **IEEA** (+7). Em termos de achados, o maior acréscimo ocorreu na **SEFAZ**, que passou de 3 para 6 achados. Também se destacaram **DETRAN**, **RJPREV**, **PGE** e **CEPERJ**, com acréscimo de 2 achados cada.

Esse resultado demonstra que a avaliação de evidências teve dupla função. No iGovTI, reduziu a pontuação quando práticas declaradas não foram comprovadas. Na execução dos procedimentos de auditoria, ampliou a identificação de inconformidades, especialmente em temas que exigem documentação institucionalizada e rastreável. Assim, o cenário final representa diagnóstico mais rigoroso e mais aderente à comprovação documental disponível.

# 9. Interpretação dos resultados

A avaliação de evidências reduziu de forma significativa o resultado do iGovTI 2026. A redução média de **0,051 ponto** no índice geral e a reclassificação de **18 organizações** para níveis inferiores demonstram que a etapa de validação documental teve efeito substantivo sobre as conclusões do trabalho.

O efeito observado indica que parte das práticas declaradas no questionário não estava acompanhada de evidência suficiente para sustentar a pontuação correspondente. Esse achado metodológico é relevante para a interpretação do iGovTI 2026: o resultado final tende a ser mais conservador do que um resultado baseado apenas em autodeclaração, pois privilegia práticas comprovadas em detrimento de declarações não confirmadas documentalmente.

Não se deve interpretar a redução de pontuação, por si só, como juízo definitivo sobre inexistência absoluta da prática em todos os casos. O ajuste indica que, no processo de auditoria, a documentação apresentada não demonstrou suficientemente a situação declarada, segundo os critérios de avaliação aplicados. Assim, a conclusão mais adequada é que houve insuficiência de comprovação para fins de pontuação no iGovTI 2026.

Sob a perspectiva do relatório consolidado, a avaliação de evidências aumenta a confiabilidade do diagnóstico, mas também torna o resultado menos comparável a levantamentos baseados predominantemente em autodeclaração. Quando houver comparação longitudinal ou comparação com trabalhos anteriores que não tenham exigido o mesmo nível de comprovação documental, essa diferença metodológica deve ser explicitada para evitar interpretações indevidas.

# 10. Conclusão

A avaliação de evidências foi determinante para o resultado final do iGovTI 2026. Sem essa etapa, a média do índice seria **0,235**; com a validação documental, a média final foi **0,184**. A diferença decorreu de **1.964 alterações efetivas** em respostas de **103 organizações**, com redução no iGovTI de **90 organizações** e deslocamento de **18 organizações** para níveis inferiores de maturidade.

Os resultados demonstram que a etapa de validação documental não foi acessória. Ela alterou materialmente a leitura do cenário de governança e gestão de tecnologia da informação, sobretudo em serviços de TI, planejamento de TI, processos de segurança da informação e contratações de TI. Também ampliou a matriz de achados, com acréscimo de **27 marcações de achados por auditado** e **253 situações inconformes** quando comparado o cenário de autodeclaração saneada com o cenário final validado por evidências. Dessa forma, o iGovTI 2026 final e os achados consolidados devem ser compreendidos como resultados apurados a partir de respostas submetidas a teste de consistência documental e da análise probatória registrada nas fontes de informação.

Essa conclusão reforça a necessidade de que as organizações aprimorem não apenas a execução das práticas de governança e gestão de TI, mas também sua formalização, documentação, atualização e capacidade de comprovação perante instâncias de controle.
