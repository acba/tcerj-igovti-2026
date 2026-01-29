# Esqueleto de Questionario (Core + Modulos)

Objetivo: definir um conjunto base (core) de praticas/questoes aplicaveis tanto a Prefeituras (esfera municipal) quanto a Organizacoes Estaduais (esfera estadual, multi-poder), e estender isso para dois questionarios:

- Questionario Municipal (Prefeituras) = Core + Modulo Municipal
- Questionario Estadual (Organizacoes estaduais - multi-poder) = Core + Modulo Estadual (comum) + Modulos opcionais por arranjo (ex.: Executivo/SETIC, Judiciario, MP, DP, Legislativo)

Premissas:

- O Core deve ser estavel (versionado) para permitir comparabilidade historica e comparacao entre esferas.
- Os Modulos capturam particularidades normativas/organizacionais de cada esfera e/ou arranjo institucional (incluindo diferencas entre Poderes/Orgaos autonomos) e podem evoluir mais rapidamente, com subindices proprios.
- Mesma escala, mesmas definicoes e mesma exigencia de evidencias para itens do Core nos dois instrumentos.

---

## 1) Modelo de resposta (padrao)

### 1.1 Escala (6 pontos)

Usar a mesma escala ja adotada nos instrumentos RJ/PE:

1. Nao adota
2. Ha decisao formal/plano aprovado para adotar
3. Adota em menor parte
4. Adota parcialmente
5. Adota em maior parte ou totalmente
6. Nao se aplica (com justificativa)

Regras:

- Para respostas 4 e 5, exigir evidencias.
- Para "Nao se aplica", exigir classificacao do motivo (ex.: vedacao legal externa; custo-beneficio; outras razoes) e justificativa/documento.

### 1.2 Responsabilidade e arranjos (capturar dependencia sem punir injustamente)

Para itens do Core, adicionar (quando fizer sentido) um qualificador padrao para diferenciar:

- Executa (interno)
- Executa com apoio de orgao central/terceiro (modelo compartilhado)
- Apenas consome/aderiu (nao executa, mas utiliza servico central)
- Terceirizado (executado por fornecedor sob governanca/controle do ente)

Isso reduz distorcao em Estado (servicos centralizados ou compartilhados por orgao central do Poder) e em Municipios (consorcios/terceiros).

### 1.3 Evidencias (padrao minimo)

Padronizar um "card" de evidencia por item (selecionavel):

- Ato/normativo (portaria, instrucao normativa, politica)
- Plano (PDTI/PEDTIC/plano de seguranca/plano de continuidade)
- Registro de governanca (ata de comite, decisao, relatorio executivo)
- Registro operacional (ticket/registro de incidente, changelog, relatorio de backup/teste)
- Registro de risco (mapa de riscos, tratamento, aceitacao)
- Contratacoes (ETP/TR, matriz de risco, SLA/indicadores, relatorios de fiscalizacao)

---

## 2) Estrutura do instrumento

### 2.1 Dominios

- GOV: Governanca de TI e governanca da transformacao digital
- PLA: Planejamento e gestao do portifolio de TI
- SVC: Gestao de servicos (ITSM) e nivel de servico
- RCO: Riscos e continuidade (TI e negocio)
- SEG: Seguranca da informacao (governanca + processos)
- SWP: Software e projetos (engenharia + gestao)
- PES: Pessoas e capacidade (perfis, competencias, dimensionamento)
- CON: Contratacoes de TI (planejamento, riscos, desempenho, transparencia)

Cada questao tem um ID estavel: `DOM-XX`.

### 2.2 Indices sugeridos

- Indice Core (comparavel entre esferas)
- Subindice Municipal (apenas para municipios)
- Subindice Estadual (comum a organizacoes estaduais, independente do Poder)
- Subindice por Arranjo (opcional): Executivo/SETIC, Judiciario, Legislativo, MP, DP, etc.

Observacao: publicar sempre o Indice Core; publicar subindices separadamente.

---

## 2.3 Bloco de caracterizacao (obrigatorio no inicio)

Objetivo: capturar o contexto para interpretar respostas do Core (especialmente quando ha prestacao compartilhada/centralizada de TIC).

- CXT-01 Esfera/ente: Municipio (Prefeitura) ou Estado (organizacao estadual)
- CXT-02 Para organizacoes estaduais: Poder/estrutura: Executivo, Judiciario, Legislativo, Ministerio Publico, Defensoria Publica, Tribunal de Contas, outro
- CXT-03 Arranjo de TIC: ha orgao central do Poder que define padroes/induz boas praticas/integra solucoes? (sim/nao)
- CXT-04 Prestacao de TIC: predominante interna, compartilhada (orgao central), terceirizada, hibrida
- CXT-05 Principais servicos consumidos de plataforma central (quando aplicavel): rede, e-mail, identidade, datacenter/nuvem, site/portal, seguranca (SOC), outros
- CXT-06 Normativos de TIC que se aplicam ao orgao (internos do Poder/organizacao e/ou externos): listar os principais

---

## 3) CORE (comum a Municipios e Estado)

Escopo: praticas universais, independentes de norma local especifica.

### GOV - Governanca

- GOV-01 Modelo de gestao de TI estabelecido pela alta administracao (diretrizes, papeis, comite, indicadores e metas)
- GOV-02 Monitoramento do desempenho da gestao de TI (rotinas, indicadores implantados, relatorios para lideranca)
- GOV-03 Auditoria interna agrega valor e cobre riscos criticos incluindo TI e seguranca (planejamento anual, cobertura minima)
- GOV-04 Servicos digitais com qualidade (interoperabilidade, usabilidade, acessibilidade, protecao de dados pessoais)
- GOV-05 Participacao do usuario e melhoria (pesquisas, uso de resultados, publicidade dos resultados)
- GOV-06 Metas de simplificacao do atendimento e ampliacao/otimizacao de canais (com gestao de riscos aplicada)

### PLA - Planejamento e portifolio

- PLA-01 Processo de planejamento de TI (integracao ao planejamento institucional, criterios de priorizacao, analise de custo/beneficio/risco, avaliacao periodica)
- PLA-02 Plano de TI vigente (aprovacao, publicacao quando aplicavel, conexao com orcamento e contratacoes, acompanhamento da execucao)

### SVC - Gestao de servicos e nivel de servico

- SVC-01 Catalogo de servicos (definicao, publicacao interna, manutencao)
- SVC-02 Gestao de mudancas (processo, registro, avaliacao de risco, aprovacao)
- SVC-03 Gestao de configuracao e ativos (inventario, relacao com servicos, controle de mudancas)
- SVC-04 Gestao de incidentes (processo, registros, escalonamento, metricas)
- SVC-05 Gestao de nivel de servico/ANS (acordos, indicadores, revisoes)

### RCO - Riscos e continuidade

- RCO-01 Gestao de riscos de TI para processos de negocio (identificar, analisar, tratar, acompanhar)
- RCO-02 Continuidade de servicos de TI (planos, testes, revisoes)
- RCO-03 Gestao de riscos organizacional implantada e integrada a TI
- RCO-04 Gestao de riscos criticos (criterios, tratamento, aceitacao, reporte)
- RCO-05 Continuidade do negocio (BIA/PCN, testes, revisoes, governanca)
- RCO-06 Estrutura de gestao de riscos definida (linhas de defesa, papeis)
- RCO-07 Atividades de segunda linha estabelecidas (monitoramento independente, conformidade, etc.)

### SEG - Seguranca da informacao

- SEG-01 Politica de seguranca da informacao (PSI) aprovada e vigente
- SEG-02 Comite/instancia de seguranca da informacao (quando aplicavel) e governanca do tema
- SEG-03 Gestor institucional de seguranca da informacao designado
- SEG-04 Responsavel por tratamento e resposta a incidentes (ETIR/CSIRT ou equivalente)
- SEG-05 Gestao de riscos de seguranca da informacao (processo integrado)
- SEG-06 Controle de acesso a informacao e ativos associados (processo + revisoes)
- SEG-07 Gestao de ativos de informacao (inventario, proprietarios, protecao)
- SEG-08 Classificacao e tratamento da informacao (rotulagem/regras)
- SEG-09 Gestao de incidentes de seguranca (registro, resposta, licoes aprendidas)
- SEG-10 Seguranca de infraestrutura/recursos de processamento, incluindo nuvem (baseline, hardening, logs, backups, etc.)
- SEG-11 Treinamento e conscientizacao periodica em seguranca

### SWP - Software e projetos

- SWP-01 Processo de software (ciclo de vida, requisitos, testes, mudancas, seguranca proporcional)
- SWP-02 Gestao de projetos de TI (metodologia, acompanhamento, entregas, riscos)

### PES - Pessoas e capacidade

- PES-01 Perfis profissionais desejados para ocupacoes de gestao definidos e documentados
- PES-02 Perfis profissionais desejados para ocupacoes tecnicas definidos e documentados
- PES-03 Dimensionamento quantitativo de pessoal por unidade/processo (necessidade x disponibilidade)
- PES-04 Provimento de vagas/selecoes alinhado a perfis (quando aplicavel)
- PES-05 Lacunas de competencias identificadas (inventario) e tratadas (plano de capacitacao)

### CON - Contratacoes de TI

- CON-01 Riscos nas contratacoes analisados em todo o ciclo (planejamento, selecao, gestao contratual)
- CON-02 Contratacao/gestao baseada em desempenho (metricas objetivas, SLA/indicadores, remuneracao vinculada quando aplicavel)
- CON-03 Prorrogacoes com avaliacao de necessidade e vantajosidade
- CON-04 Processo de planejamento das contratacoes definido e executado (ETP/TR, alinhamento ao plano de TI)
- CON-05 Processo de selecao de fornecedores definido e executado (procedimentos, papeis, modelos)
- CON-06 Processo de gestao de contratos definido e executado (fiscalizacao, papeis, modelos, capacidade)
- CON-07 Transparencia de documentos do ciclo de contratacao (resguardado sigilo legal)

---

## 4) MODULO MUNICIPAL (Prefeituras)

Escopo: itens especificos do contexto municipal, com enfase em conformidades nacionais e entregas tipicas de prefeitura.

### MUN - Governo digital, conformidades e integracoes

- MUN-01 Lei 14.129/2021 (Governo Digital): governanca, medidas e institucionalizacao local
- MUN-02 Carta de Servicos: existencia, atualizacao, publicidade e uso para melhoria
- MUN-03 Processo administrativo eletronico/digital (cobertura, governanca, integracao)
- MUN-04 SIAFIC: requisitos minimos de TI atendidos (governanca, integridade, disponibilidade)
- MUN-05 PNCP: integracao/publicacao quando cabivel e maturidade do processo associado

### MUN - Diagnostico de capacidade (variaveis explicativas)

Recomendacao: perguntas curtas, preferencialmente sem peso (ou com peso separado), para explicar desempenho do Core:

- MUN-D01 Estrutura formal de TI (posicionamento, subordinacao, autonomia)
- MUN-D02 Composicao do time (efetivos/terceirizados), rotatividade e dependencia de terceiros
- MUN-D03 Capacidade do controle interno para avaliar TI e contratos de TI

---

## 5) MODULO ESTADUAL (Organizacoes estaduais - multi-poder)

Escopo: itens especificos do contexto estadual, considerando que a auditoria inclui organizacoes de diferentes Poderes e orgaos autonomos. O modulo estadual se divide em:

- Modulo Estadual (comum): aplicavel a qualquer organizacao estadual, independentemente do Poder.
- Modulos por Arranjo (opcionais): perguntas adicionais quando existir um sistema/estrutura central de TIC no Poder (ex.: Executivo/SETIC, arranjo do Judiciario, etc.).

### EST (comum) - Governanca e conformidades internas do Poder/organizacao

- EST-C01 Existencia/organizacao do Setor de TI e dados do gestor responsavel
- EST-C02 Conhecimento dos normativos de TIC aplicaveis ao orgao (normas internas do Poder/organizacao e diretrizes externas pertinentes)
- EST-C03 Aderencia a normativos de TIC aplicaveis (por tema), com evidencias (ex.: governanca, seguranca, contratacoes, desenvolvimento, gestao de servicos)

### EST (arranjo) - Efetividade do orgao central do Poder como indutor/integrador (quando houver)

- EST-A01 Comunicacao recebida do orgao central (ultimos 12 meses) e satisfacao com relevancia
- EST-A02 Auxilio/orientacao recebida do orgao central (ultimos 12 meses) e satisfacao
- EST-A03 Percepcao sobre boas praticas induzidas (ajudam/nao ajudam)
- EST-A04 Avaliacao da qualidade/viabilidade/importancia dos atos e normativos emitidos pelo orgao central (com escala)
- EST-A05 Atuacao do orgao central como integrador de solucoes (atende necessidades) e atendimento/canais

### EST (arranjo) - Sites/portais e plataformas compartilhadas (quando aplicavel)

- EST-A06 Hospedagem/desenvolvimento/sustentacao de sites/portais em ambientes de plataforma central do Poder (modelo adotado e aderencia)

Observacao: itens EST-A01..EST-A06 sao excelentes "variaveis explicativas" para entender maturidade do Core em orgaos setoriais/aderentes a um arranjo central.

---

## 6) Mapeamento inicial (best effort) para instrumentos existentes

Objetivo: preservar comparabilidade e acelerar construcao dos dois questionarios reaproveitando questoes ja existentes.

### 6.1 Questionario Estadual - exemplo de mapeamento (Executivo/SETIC)

Mapeamento sugerido:

- GOV-01 ~ 1111
- GOV-02 ~ 1121
- GOV-03 ~ 1122
- GOV-04 ~ 1131
- GOV-05 ~ 1132
- GOV-06 ~ 1133
- PLA-01 ~ 2111
- PLA-02 ~ 2112
- SVC-01 ~ 2121
- SVC-02 ~ 2122
- SVC-03 ~ 2123
- SVC-04 ~ 2124
- SVC-05 ~ 2131
- RCO-01 ~ 2141
- RCO-02 ~ 2142
- RCO-03 ~ 2143
- RCO-04 ~ 2144
- RCO-05 ~ 2145
- RCO-06 ~ 2146
- RCO-07 ~ 2147
- SEG-01 ~ 2151
- SEG-02 ~ 2152
- SEG-03 ~ 2153
- SEG-04 ~ 2154
- SEG-05 ~ 2161
- SEG-06 ~ 2162
- SEG-07 ~ 2163
- SEG-08 ~ 2164
- SEG-09 ~ 2165
- SEG-10 ~ 2166
- SEG-11 ~ 2167
- SWP-01 ~ 2171
- SWP-02 ~ 2181
- PES-01 ~ 2211
- PES-02 ~ 2212
- PES-03 ~ 2213
- PES-04 ~ 2221
- PES-05 ~ 2231 + 2232
- CON-01 ~ 2311
- CON-02 ~ 2321
- CON-03 ~ 2322
- CON-04 ~ 2331
- CON-05 ~ 2342
- CON-06 ~ 2343
- CON-07 ~ 2344

Modulo por Arranjo (Executivo/SETIC), quando aplicavel:

- EST-C01 ~ 1011
- EST-C02 ~ 1021
- EST-C03 ~ 1022/1023/1024/1025 (por normativo)
- EST-A01..EST-A05 ~ 1031..1038

### 6.2 Questionario Municipal (Prefeituras)

Mapeamento sugerido (alto nivel):

- Core: reaproveitar itens de governanca/gestao/seguranca/servicos/contratacoes/projetos ja presentes no questionario municipal RJ (muito proximo ao modelo PE).
- Modulo Municipal: reaproveitar o bloco de "Conformidade Externa" (Lei 14.129/2021, Carta de Servicos, processo administrativo digital, SIAFIC, PNCP) e a aderencia a notas tecnicas quando fizer sentido para o publico municipal.

Observacao: para fechar o mapeamento com IDs exatos do instrumento municipal RJ, gerar uma planilha de correspondencia (Questao RJ municipal -> ID Core/Modulo) antes de publicar a versao final.

---

## 6.3 Mapeamento completo (esqueleto -> questionarios antigos)

Resposta objetiva: nao. O esqueleto NAO contem todas as questoes dos instrumentos antigos; ele consolida um Core comum e separa temas especificos em modulos. Abaixo esta o mapeamento item-a-item do esqueleto para:

- Municipal (RJ municipios): `docs/referencias/tcerj/municipios/CAS-TI - Questionário de Governança e Gestão de TI.pdf`
- Estadual (exemplo Executivo/SETIC): `docs/referencias/tcerj/setic/01-Questionário de Governança e Gestão de TI.pdf`

Convencao:

- Quando nao houver questao correspondente no instrumento antigo, marcar como `novo`.
- Itens de cabecalho (ex.: 1120, 1130, 2100 etc.) sao titulos de secao e nao foram tratados como questoes mapeaveis.
- Para o questionario estadual multi-poder: o mapeamento "SETIC" aplica-se apenas ao arranjo do Executivo/SETIC; para outros Poderes, os itens `EST-A..` devem ser mapeados ao orgao central equivalente (quando houver).

### CXT - Bloco de caracterizacao

| ID | Esqueleto | Municipal (antigo) | Estadual/SETIC (antigo) |
|---|---|---:|---:|
| CXT-01 | Esfera/ente | novo | novo |
| CXT-02 | Poder/estrutura (Estado) | novo | novo |
| CXT-03 | Existe orgao central de TIC no Poder? | novo | novo |
| CXT-04 | Prestacao de TIC (interna/compartilhada/terceirizada) | novo | novo |
| CXT-05 | Servicos consumidos de plataforma central | novo | novo |
| CXT-06 | Normativos de TIC aplicaveis (lista) | novo | novo |

### CORE - Mapeamento

| ID | Esqueleto | Municipal (antigo) | Estadual/SETIC (antigo) |
|---|---|---:|---:|
| GOV-01 | Modelo de gestao de TI | 1111 | 1111 |
| GOV-02 | Monitoramento do desempenho de TI | 1121 | 1121 |
| GOV-03 | Auditoria interna (inclui TI/Seg) | 1122 | 1122 |
| GOV-04 | Servicos digitais com qualidade | 1131 | 1131 |
| GOV-05 | Participacao do usuario e melhoria | 1132 | 1132 |
| GOV-06 | Metas de simplificacao/canais | 1133 | 1133 |
| PLA-01 | Processo de planejamento de TI | 2111 | 2111 |
| PLA-02 | Plano de TI vigente | 2112 | 2112 |
| SVC-01 | Catalogo de servicos | 2121 | 2121 |
| SVC-02 | Gestao de mudancas | 2122 | 2122 |
| SVC-03 | Configuracao e ativos | 2123 | 2123 |
| SVC-04 | Gestao de incidentes (servicos) | 2124 | 2124 |
| SVC-05 | Nivel de servico/ANS | 2131 | 2131 |
| RCO-01 | Riscos de TI para processos | 2141 | 2141 |
| RCO-02 | Continuidade de servicos de TI | 2142 | 2142 |
| RCO-03 | Riscos organizacionais implantados | 2143 | 2143 |
| RCO-04 | Riscos criticos geridos | 2144 | 2144 |
| RCO-05 | Continuidade do negocio | 2145 | 2145 |
| RCO-06 | Estrutura da gestao de riscos | 2146 | 2146 |
| RCO-07 | Atividades de segunda linha | 2147 | 2147 |
| SEG-01 | Politica de seguranca (PSI) | 2151 | 2151 |
| SEG-02 | Comite/instancia de seguranca | 2152 | 2152 |
| SEG-03 | Gestor institucional de seguranca | 2153 | 2153 |
| SEG-04 | Responsavel por resposta a incidentes | novo | 2154 |
| SEG-05 | Riscos de seguranca | 2161 | 2161 |
| SEG-06 | Controle de acesso | 2162 | 2162 |
| SEG-07 | Ativos de informacao | 2163 | 2163 |
| SEG-08 | Classificacao/tratamento | 2164 | 2164 |
| SEG-09 | Incidentes de seguranca | 2165 | 2165 |
| SEG-10 | Seguranca de infraestrutura (inclui nuvem) | 2166 | 2166 |
| SEG-11 | Treinamento/conscientizacao em seguranca | novo | 2167 |
| SWP-01 | Processo de software | 2171 | 2171 |
| SWP-02 | Gestao de projetos de TI | 2181 | 2181 |
| PES-01 | Perfis (gestao) | 2211 | 2211 |
| PES-02 | Perfis (tecnicos) | 2212 | 2212 |
| PES-03 | Dimensionamento de pessoal | 2213 | 2213 |
| PES-04 | Provimento alinhado a perfis | 2221 | 2221 |
| PES-05 | Lacunas de competencias (identificar e tratar) | 2231 | 2231 + 2232 |
| CON-01 | Riscos nas contratacoes | 2311 | 2311 |
| CON-02 | Contratar/gerir com base em desempenho | 2321 | 2321 |
| CON-03 | Prorrogacoes (necessidade/vantajosidade) | 2322 | 2322 |
| CON-04 | Planejamento das contratacoes | 2331 | 2331 |
| CON-05 | Processo de selecao de fornecedores | 2342 | 2342 |
| CON-06 | Processo de gestao de contratos | 2343 | 2343 |
| CON-07 | Transparencia do ciclo de contratacao | 2344 | 2344 |

### MODULO MUNICIPAL (Prefeituras) - Mapeamento

| ID | Esqueleto | Municipal (antigo) | Estadual/SETIC (antigo) |
|---|---|---:|---:|
| MUN-01 | Lei 14.129/2021 (recepcao + inducao local) | 1141 + 1142 | - |
| MUN-02 | Carta de Servicos | 1143 | - |
| MUN-03 | Processo administrativo eletronico/digital | 1144 | - |
| MUN-04 | SIAFIC (requisitos minimos de TI) | 1145 | - |
| MUN-05 | Integracao ao PNCP | 1146 | - |
| MUN-D01 | Estrutura formal de TI (posicionamento/autonomia) | novo | novo |
| MUN-D02 | Composicao do time e dependencia de terceiros | novo | novo |
| MUN-D03 | Capacidade do controle interno (TI/contratos) | novo | novo |

### MODULO ESTADUAL (multi-poder) - Mapeamento (exemplo Executivo/SETIC)

| ID | Esqueleto | Municipal (antigo) | Estadual/SETIC (antigo) |
|---|---|---:|---:|
| EST-C01 | Setor de TI e gestor responsavel | - | 1011 |
| EST-C02 | Conhecimento de normativos de TIC aplicaveis | - | 1021 |
| EST-C03 | Aderencia a normativos de TIC aplicaveis (por tema) | - | 1022 + 1023 + 1024 |
| EST-A01 | Comunicacao do orgao central (relevancia) | - | 1031 + 1032 |
| EST-A02 | Auxilio/orientacao do orgao central | - | 1033 + 1034 |
| EST-A03 | Boas praticas induzidas ajudam? | - | 1035 |
| EST-A04 | Avaliacao de qualidade/viabilidade dos normativos | - | 1036 |
| EST-A05 | Orgao central como integrador + atendimento/canais | - | 1037 + 1038 |
| EST-A06 | Sites/portais e plataformas compartilhadas | - | 1025 |

---

## 6.4 Questoes dos questionarios antigos que NAO ficaram no esqueleto (removidas)

Notas:

- A lista abaixo considera "questao" como itens numerados com ponto (ex.: 2241.). Titulos de secao (ex.: 1120, 2100) nao foram listados aqui.
- Essas questoes podem voltar como: (a) perguntas diagnosticas sem peso, (b) perguntas opcionais por arranjo, ou (c) itens de analise qualitativa (sem entrar no indice).

### Removidas do questionario Municipal (RJ municipios)

- 2241. A organizacao realiza formalmente a avaliacao de desempenho individual (nota/conceito) com criterio de metas do plano da unidade.
- 2251. A organizacao possui em sua estrutura cargos especificos para tecnologia da informacao.
- 2252. A organizacao possui plano de cargos formalizado contendo cargos especificos de TI.
- 2351. Nas contratacoes de bens e servicos de TI, a organizacao faz uso de Nota Tecnica do TCE-RJ (economicidade e/ou planejamento das contratacoes).

### Removidas do questionario Estadual (Executivo/SETIC)

- 2113. A organizacao recebeu orientacao e/ou interagiu com o Diretor Geral do SETIC (PRODERJ) durante a elaboracao do PEDTIC vigente.
- 2233. A organizacao utiliza as acoes de capacitacao ofertadas pelo programa Academia PRODERJ.
- 2351. Nas contratacoes de bens e servicos de TI, a organizacao faz uso da Nota Tecnica do TCE-RJ acerca do Planejamento das Contratacoes de TI (Nota Tecnica no 06/2023).
- 2361. As contratacoes de TI estao ocorrendo conforme previsto no PEDTIC e no PAC.
- 2362. Cite as tres principais dificuldades encontradas na realizacao de contratacoes de TI.

---

## 7) Produto final esperado (artefatos)

- `Questionario_Core.md` (lista de itens Core com IDs, texto padrao, evidencias e qualificadores)
- `Questionario_Municipal.md` = Core + Modulo Municipal
- `Questionario_Estadual.md` = Core + Modulo Estadual (comum) + modulos por arranjo (quando aplicavel)
- `Questionario_Estadual_Executivo_SETIC.md` (opcional) = apenas o modulo por arranjo do Executivo/SETIC, para reutilizar blocos existentes
- `Mapa_Correspondencia.xlsx` (instrumentos existentes -> Core/Modulos)
