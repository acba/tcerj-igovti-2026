# Alterações Propostas ao Mapa de Verificação de Achados

**Arquivo:** `02-Execucao/03-Execucao_Procedimentos/01-Insumos/mapa-verificacao-achados.xlsx`
**Data:** 14/08/2026 | **Análise:** Claude Opus (Anthropic)
**Premissa:** A lógica de processamento dos procedimentos de auditoria (scripts) **não será alterada**.

---

## Bloco 1 — Aba "Procedimentos de Auditoria" (coluna `logica_achado`)

As expressões de lógica de achado são o mecanismo central de composição. Alterá-las restringe ou amplia quais ações disparam o achado.

### PA02 — Achado 2: Governança de TIC

| Campo | DE (atual) | PARA (proposto) | Justificativa |
|---|---|---|---|
| `logica_achado` | `(((AV07 \| AV85) \| (AV08 \| AV86) \| (AV09 \| AV87) \| (AV10 \| AV88)) \| (AV11 \| AV89) \| ((AV12 \| AV90) & (AV13 \| AV91)))` | `(((AV07 \| AV85) \| (AV08 \| AV86)) \| (AV11 \| AV89) \| ((AV12 \| AV90) & (AV13 \| AV91)))` | **Remove AV09/AV87 (`q1002ext[A]`) e AV10/AV88 (`q1002ext[C]`) do grupo S2.1.** Monitorar desempenho da TI com rotinas e indicadores implantados é prática avançada de maturidade (COBIT MEA01). Mantê-la no achado faz S2.1 incidir em 94,7% do universo. Reduzindo a S2.1 para papéis/responsabilidades (`q1001ext[C]`) e objetivos/metas (`q1001ext[H]`), preserva-se o núcleo essencial da governança. As ações AV09/AV10/AV87/AV88 permanecem no mapa para fins de registro, mas não disparam o achado. |

### PA03 — Achado 3: Planejamento de TIC

| Campo | DE (atual) | PARA (proposto) | Justificativa |
|---|---|---|---|
| `logica_achado` | `(((AV14 \| AV92) \| (AV15 \| AV93) \| (AV16 \| AV94) \| (AV17 \| AV95)) \| (AV18 \| AV96) \| (AV19 \| AV97) \| ((AV20 \| AV98) \| (AV21 \| AV99) \| (AV22 \| AV100) \| AV23) \| (AV24 \| AV101))` | `(((AV14 \| AV92) \| (AV15 \| AV93) \| (AV16 \| AV94) \| (AV17 \| AV95)) \| (AV18 \| AV96) \| (AV19 \| AV97) \| (AV20 \| AV98) \| (AV24 \| AV101))` | **Elimina dupla contagem de S3.5.** Remove AV21/AV99 (`q2802ext[C]`), AV22/AV100 (`q2802ext[D]`) e AV23 (`q2804[B]`) do grupo S3.5 dentro do PA03. Esses itens referem-se a planejamento de contratações (PCA) e integração ao orçamento, que já são tratados em S6.3 (PA06). O item `q2102ext[C]` (plano de TI fundamenta proposta orçamentária) permanece em S3.5 como único verificador de vínculo orçamentário do planejamento de TIC. |

### PA04 — Achado 4: Capacidade Institucional

| Campo | DE (atual) | PARA (proposto) | Justificativa |
|---|---|---|---|
| `logica_achado` | `((AV25 \| AV27) \| (AV29 \| AV103) \| ((AV31 \| AV105) \| (AV33 \| AV107)) \| ((AV34 \| AV108) \| (AV36 \| AV110) \| (AV38 \| AV112)) \| (AV39 \| AV40 \| AV41 \| (AV42 \| AV116)) \| ((AV45 & AV46) \| AV53))` | `((AV25 \| AV27) \| (AV29 \| AV103) \| (AV34 \| AV108) \| (AV40 \| (AV42 \| AV116)) \| ((AV45 & AV46) \| AV53))` | **Três alterações acumuladas:** **(a)** Remove S4.3 inteiramente — `((AV31 \| AV105) \| (AV33 \| AV107))` (cargos específicos). Cargos dependem de lei; fora da governabilidade do gestor. **(b)** Simplifica S4.4 — mantém apenas `(AV34 \| AV108)` (perfis de gestores de TI). Remove `(AV36 \| AV110)` (perfis de colaboradores) e `(AV38 \| AV112)` (seleção por perfil). **(c)** Simplifica S4.5 — mantém `(AV40 \| (AV42 \| AV116))` (lacunas técnicas de TI + plano de capacitação). Remove AV39 (lacunas transversais) e AV41 (lacunas de SI). |

### PA05 — Achado 5: Gestão de Serviços de TIC

| Campo | DE (atual) | PARA (proposto) | Justificativa |
|---|---|---|---|
| `logica_achado` | `(((AV54 \| AV124) \| (AV55 \| AV125) \| (AV56 \| AV126)) \| ((AV57 \| AV127) \| (AV58 \| AV128)) \| ((AV59 \| AV129) \| (AV62 \| AV132) \| (AV63 \| AV133)) \| ((AV64 \| AV134) \| (AV66 \| AV136)) \| ((AV67 \| AV137) \| (AV70 \| AV140) \| (AV71 \| AV141)))` | `((AV54 \| AV124) \| ((AV59 \| AV129) \| (AV62 \| AV132) \| (AV63 \| AV133)) \| (AV64 \| AV134) \| ((AV67 \| AV137) \| (AV70 \| AV140) \| (AV71 \| AV141)))` | **Três alterações acumuladas:** **(a)** Simplifica S5.1 — mantém apenas `(AV54 \| AV124)` (organização possui catálogo com metas, `q2201ext[A]`). Remove `(AV55 \| AV125)` (catálogo atualizado/compatível) e `(AV56 \| AV126)` (catálogo acessível) do achado. **(b)** Remove S5.2 inteiramente — `((AV57 \| AV127) \| (AV58 \| AV128))` (ANS). Prática ITIL avançada, incompatível com 98,2% do universo. **(c)** Simplifica S5.4 — mantém `(AV64 \| AV134)` (inventário consolidado, `q2203ext[A]`). Remove `(AV66 \| AV136)` (processo formalizado, `q2203ext[C]`). CMDB formalizado é maturidade intermediária-alta. |

### PA01 e PA06

Sem alteração na `logica_achado`. PA01 está bem calibrado (60,2%). PA06 recebe apenas alterações de `tipo_encaminhamento` (Bloco 2).

---

## Bloco 2 — Aba "Ações de Verificação" (coluna `tipo_encaminhamento`)

Conversão de Recomendação → Determinação para ações com fundamento normativo direto.

### S2.2 — Comitê de TIC não instituído

| Ação | Item | DE | PARA | Justificativa |
|---|---|---|---|---|
| **AV11** | `q1001ext[E]` | Recomendação | **Determinação** | Acórdão TCE-RJ 44.490/2024-PLEN, item II.1 — deliberação plenária determinando instituição de comitê de TIC. Decreto nº 12.198/2024, art. 5º (referência federal). |
| **AV89** | `q1001ext[E]` | Recomendação | **Determinação** | Mesma base normativa (ação espelho de avaliação de evidências). |

### S3.1 — Processo formal de planejamento de TIC

| Ação | Item | DE | PARA | Justificativa |
|---|---|---|---|---|
| **AV14** | `q2101ext[A]` | Recomendação | **Determinação** | Acórdão TCU 1.411/2014-Plenário, item 9.1.6. Acórdão TCE-RJ 44.490/2024-PLEN, itens II.3 a II.3.5. Jurisprudência consolidada. |
| **AV15** | `q2101ext[B]` | Recomendação | **Determinação** | Idem. |
| **AV16** | `q2101ext[C]` | Recomendação | **Determinação** | Idem. |
| **AV17** | `q2101ext[D]` | Recomendação | **Determinação** | Idem. |
| **AV92** | `q2101ext[A]` | Recomendação | **Determinação** | Espelho de avaliação de evidências. |
| **AV93** | `q2101ext[B]` | Recomendação | **Determinação** | Idem. |
| **AV94** | `q2101ext[C]` | Recomendação | **Determinação** | Idem. |
| **AV95** | `q2101ext[D]` | Recomendação | **Determinação** | Idem. |

### S3.2 — Aprovação formal do plano de TIC

| Ação | Item | DE | PARA | Justificativa |
|---|---|---|---|---|
| **AV18** | `q2102ext[A]` | Recomendação | **Determinação** | Acórdão TCU 1.411/2014-Plenário. Acórdão TCE-RJ 44.490/2024-PLEN. A aprovação pelo dirigente máximo é requisito consolidado na jurisprudência. |
| **AV96** | `q2102ext[A]` | Recomendação | **Determinação** | Espelho de avaliação de evidências. |

### S6.1 — Processo formal de contratações (parcial: somente `q2801ext[G]`)

| Ação | Item | DE | PARA | Justificativa |
|---|---|---|---|---|
| **AV77** | `q2801ext[G]` | Recomendação | **Determinação** | Lei 14.133/2021 — aderência aos ritos legais de contratação é obrigação legal, não boa prática. |
| **AV147** | `q2801ext[G]` | Recomendação | **Determinação** | Espelho de avaliação de evidências. |

> **Nota:** As demais ações de S6.1 (AV73/AV143=`[A]`, AV74/AV144=`[C]`, AV75/AV145=`[D]`, AV76/AV146=`[E]`) permanecem como Recomendação, pois tratam de padronização de artefatos e modelos — boas práticas sem comando legal direto.

### S6.2 — Contratações sem aprovação técnica da TI

| Ação | Item | DE | PARA | Justificativa |
|---|---|---|---|---|
| **AV78** | `q2804[A]` | Recomendação | **Determinação** | Lei 14.133/2021, arts. 18 e 19 — análise técnica prévia é decorrência do dever legal de planejamento da contratação. IN SGD/ME nº 94/2022, art. 1º, §1º. |
| **AV148** | `q2804[A]` | Recomendação | **Determinação** | Espelho de avaliação de evidências. |

### S6.4 — Equipe de planejamento sem designação formal

| Ação | Item | DE | PARA | Justificativa |
|---|---|---|---|---|
| **AV83** | `q2804[C]` | Recomendação | **Determinação** | Lei 14.133/2021, art. 7º, caput e incisos — designação formal de agentes públicos para funções essenciais nas contratações é comando legal direto. |

**Resumo do Bloco 2:** 18 ações alteradas de Recomendação → Determinação.

---

## Bloco 3 — Aba "Motivos do Relatório" (coluna `ativo`)

Para cada situação removida ou simplificada no Bloco 1, os motivos correspondentes devem ser desativados para não gerar texto no relatório sobre ações que não compõem mais o achado.

### Motivos a desativar (`ativo`: `True` → `False`)

| Motivo | Procedimento | Situação inconforme | Ação referenciada | DE | PARA | Justificativa |
|---|---|---|---|---|---|---|
| **MR017** | PA02 | Modelo básico de governança insuficiente | AV09 | `True` | **`False`** | AV09 (`q1002ext[A]`) removida do achado — monitoramento é prática avançada. |
| **MR018** | PA02 | Modelo básico de governança insuficiente | AV87 | `True` | **`False`** | AV87 espelho de AV09. |
| **MR019** | PA02 | Modelo básico de governança insuficiente | AV10 | `True` | **`False`** | AV10 (`q1002ext[C]`) removida do achado — indicadores implantados é prática avançada. |
| **MR020** | PA02 | Modelo básico de governança insuficiente | AV88 | `True` | **`False`** | AV88 espelho de AV10. |
| **MR035** | PA03 | Plano de TIC sem vínculo com orçamento/contratações | AV21 | `True` | **`False`** | AV21 (`q2802ext[C]`) migrada para PA06/S6.3. Dupla contagem eliminada. |
| **MR036** | PA03 | Plano de TIC sem vínculo com orçamento/contratações | AV99 | `True` | **`False`** | AV99 espelho de AV21. |
| **MR037** | PA03 | Plano de TIC sem vínculo com orçamento/contratações | AV22 | `True` | **`False`** | AV22 (`q2802ext[D]`) migrada para PA06/S6.3. |
| **MR038** | PA03 | Plano de TIC sem vínculo com orçamento/contratações | AV100 | `True` | **`False`** | AV100 espelho de AV22. |
| **MR039** | PA03 | Plano de TIC sem vínculo com orçamento/contratações | AV23 | `True` | **`False`** | AV23 (`q2804[B]`) migrada para PA06/S6.3. |
| **MR071** | PA05 | Níveis mínimos de serviço (ANS) | AV57 | `True` | **`False`** | S5.2 inteiramente removida do achado — prática ITIL avançada. |
| **MR072** | PA05 | Níveis mínimos de serviço (ANS) | AV127 | `True` | **`False`** | Espelho de AV57. |
| **MR073** | PA05 | Níveis mínimos de serviço (ANS) | AV58 | `True` | **`False`** | AV58 parte de S5.2 removida. |
| **MR074** | PA05 | Níveis mínimos de serviço (ANS) | AV128 | `True` | **`False`** | Espelho de AV58. |
| **MR083** | PA05 | Gestão de configuração | AV66 | `True` | **`False`** | AV66 (`q2203ext[C]`) removida de S5.4 — formalização de processo é maturidade avançada. |
| **MR084** | PA05 | Gestão de configuração | AV136 | `True` | **`False`** | Espelho de AV66. |

> **Nota sobre S4.3, S4.4, S4.5 e S5.1:** Os motivos vinculados às ações removidas (AV31/AV105, AV33/AV107, AV36/AV110, AV38/AV112, AV39, AV41, AV55/AV125, AV56/AV126) devem ser igualmente desativados. Os IDs exatos (MR04x a MR06x) precisam ser confirmados na planilha, pois a extração obteve dados parciais para o PA04. A regra é: **todo MR cuja `condicao_exibicao` referencie exclusivamente ações removidas da lógica deve ter `ativo` = `False`**.

**Estimativa:** ~12 motivos adicionais a desativar no PA04 (S4.3: ~4 MRs; S4.4: ~4 MRs; S4.5: ~4 MRs) e ~4 motivos no PA05 (S5.1).

---

## Bloco 4 — Aba "Ações de Verificação" (colunas textuais)

Alterações de `descricao_situacao_inconforme` e `encaminhamento` para as situações cujo escopo foi reduzido, de modo que a redação reflita apenas os itens que efetivamente integram a lógica do achado.

### S4.4 — Perfis profissionais (escopo reduzido)

| Ações | Coluna | DE (resumo) | PARA (proposto) | Justificativa |
|---|---|---|---|---|
| **AV34, AV108** | `descricao_situacao_inconforme` | "Perfis profissionais de TIC e segurança da informação inexistentes, insuficientes ou **não utilizados na escolha de gestores**." | "Perfis profissionais dos gestores de TIC **inexistentes ou insuficientes**." | A verificação passou a cobrir apenas `q2701ext[A]` (perfis de gestores). Referência a colaboradores e seleção por perfil não integra mais o achado. |
| **AV34, AV108** | `encaminhamento` | "defina perfis profissionais mínimos para gestores **e colaboradores** de TIC e segurança da informação, atentando-se, minimamente, em estabelecer conhecimentos, habilidades, experiência e responsabilidades requeridos **e utilizar esses perfis na seleção e designação dos responsáveis**" | "defina perfis profissionais mínimos para os gestores de TIC, atentando-se, minimamente, em estabelecer conhecimentos, habilidades, experiência e responsabilidades requeridos" | Ajusta o encaminhamento ao escopo reduzido da situação. |

### S4.5 — Lacunas de competências (escopo reduzido)

| Ações | Coluna | DE (resumo) | PARA (proposto) | Justificativa |
|---|---|---|---|---|
| **AV40, AV42, AV116** | `descricao_situacao_inconforme` | "Lacunas de competências dos colaboradores e gestores de TIC e segurança da informação **não são identificadas ou tratadas**." | "Lacunas de competências técnicas de TIC **não são identificadas ou não possuem plano de capacitação**." | A verificação agora cobre apenas `q2705ext[C]` (lacunas técnicas TI) e `q2706ext[A]` (plano de capacitação). |
| **AV40, AV42, AV116** | `encaminhamento` | "realize diagnóstico periódico das lacunas de competências dos gestores e colaboradores de TIC e segurança da informação e estabeleça plano de tratamento, contemplando, conforme a necessidade, capacitação, realocação, provimento, apoio especializado, compartilhamento de estrutura ou contratação com transferência de conhecimento" | "identifique as lacunas de competências técnicas de TIC e estabeleça plano de capacitação ou tratamento, compatível com as necessidades e o porte da organização" | Simplifica e torna proporcional ao universo. |

### S5.1 — Catálogo de serviços (escopo reduzido)

| Ações | Coluna | DE (resumo) | PARA (proposto) | Justificativa |
|---|---|---|---|---|
| **AV54, AV124** | `descricao_situacao_inconforme` | "Inexistência ou insuficiência do catálogo de serviços de TIC." | Sem alteração (a redação já é compatível com escopo reduzido). | — |
| **AV54, AV124** | `encaminhamento` | "institua e mantenha atualizado catálogo de serviços de TIC, atentando-se, minimamente, em **identificar os serviços efetivamente prestados, seus responsáveis, usuários, condições de acesso e informações necessárias ao atendimento das áreas demandantes**" | "institua catálogo de serviços de TIC, atentando-se, minimamente, em identificar os serviços efetivamente prestados e seus responsáveis" | Remove exigências incrementais (condições de acesso, informações de atendimento) que inflacionavam a régua. |

### S5.4 — Gestão de configuração (escopo reduzido)

| Ações | Coluna | DE (resumo) | PARA (proposto) | Justificativa |
|---|---|---|---|---|
| **AV64, AV134** | `descricao_situacao_inconforme` | "Ausência ou fragilidade do processo de gestão de configuração." | "Ausência de inventário consolidado de ativos e configurações de TIC." | A situação verifica apenas `q2203ext[A]` (base consolidada e atualizada). Processo formalizado (`q2203ext[C]`) foi removido. |
| **AV64, AV134** | `encaminhamento` | "formalize e execute processo de gestão de configuração, atentando-se, minimamente, em manter base, ferramenta ou registro equivalente com os itens de configuração relevantes, seus responsáveis e os **relacionamentos entre ativos, sistemas, infraestrutura e serviços, com atualização periódica e uso das informações no planejamento e acompanhamento de mudanças**" | "mantenha inventário consolidado e atualizado dos ativos e configurações relevantes de TIC, identificando seus responsáveis e relacionamentos com os serviços prestados" | Remove exigência de processo formalizado e uso como insumo para mudanças. Mantém inventário como prática essencial. |

### S2.1 — Modelo de governança (escopo reduzido)

| Ações | Coluna | DE (resumo) | PARA (proposto) | Justificativa |
|---|---|---|---|---|
| **AV07, AV08, AV85, AV86** | `descricao_situacao_inconforme` | "Modelo básico de governança e gestão de TIC inexistente ou insuficiente quanto a papéis, responsabilidades, **objetivos, indicadores, metas ou acompanhamento**." | "Modelo básico de governança e gestão de TIC inexistente ou insuficiente quanto a papéis, responsabilidades, **objetivos ou metas**." | Remove referência a indicadores e acompanhamento, que não integram mais a lógica do achado nesta situação. |
| **AV07, AV08, AV85, AV86** | `encaminhamento` | "estabeleça modelo básico de governança e gestão de TIC, atentando-se, minimamente, em definir papéis e responsabilidades, objetivos, **indicadores, metas e forma de acompanhamento periódico** do desempenho da TIC pela alta administração" | "estabeleça modelo básico de governança e gestão de TIC, atentando-se, minimamente, em definir papéis e responsabilidades, objetivos e metas para a gestão de TIC" | Coerência com o escopo reduzido. Indicadores e acompanhamento são práticas avançadas. |

---

## Resumo Consolidado

| Bloco | Tipo de alteração | Qtd. de alterações |
|---|---|---:|
| **1** | `logica_achado` em Procedimentos | **4 expressões** (PA02, PA03, PA04, PA05) |
| **2** | `tipo_encaminhamento` em Ações | **18 ações** (Recomendação → Determinação) |
| **3** | `ativo` em Motivos do Relatório | **~27 motivos** (True → False) |
| **4** | `descricao_situacao_inconforme` e `encaminhamento` em Ações | **~20 ações** (ajuste textual) |
| | **Total de células alteradas** | **~69** |

### Impacto estimado nos resultados

| Indicador | Atual | Estimado após alterações |
|---|---|---|
| Achado 2 — incidência | 94,7% (107 orgs) | ~75-80% (~85-90 orgs) |
| Achado 3 — incidência | 95,6% (108 orgs) | ~85-90% (~96-102 orgs) |
| Achado 4 — incidência | **100,0% (113 orgs)** | ~75-85% (~85-96 orgs) |
| Achado 5 — incidência | **100,0% (113 orgs)** | ~85-90% (~96-102 orgs) |
| Achado 6 — incidência | 98,2% (111 orgs) | 98,2% (sem alteração na lógica) |
| Encaminhamentos tipo Determinação | 0 | **5 situações** (18 ações) |
| Situações ativas no achado | 26 | ~21 |

> **Nota:** Os impactos estimados são aproximações baseadas na frequência observada de cada ação de verificação nos resultados pós-comentários do gestor. A execução efetiva com o mapa alterado confirmará os valores reais.
