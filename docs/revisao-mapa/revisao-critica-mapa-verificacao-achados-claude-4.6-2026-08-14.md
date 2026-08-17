# Revisão Crítica da Matriz de Planejamento e Mapa de Verificação de Achados

**Fiscalização 18/2026 — iGovTI 2026 | Posição pós-comentários do gestor**

> **Data da análise:** 14/08/2026
> **Análise realizada por:** Claude Opus 4.6 (Anthropic), via Antigravity CLI
> **Fontes analisadas:**
> - `01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/matriz_planejamento.md`
> - `02-Execucao/03-Execucao_Procedimentos/01-Insumos/mapa-verificacao-achados.xlsx`
> - `02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/03-pos-comentarios-gestor/resultado_auditoria.json`
> - `01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md`
>
> **Nota:** Esta análise foi gerada por inteligência artificial como subsídio para a equipe de auditoria. As propostas aqui contidas são sugestões que requerem validação e deliberação humana antes de qualquer implementação.

---

## 1. Panorama Quantitativo — Diagnóstico de Partida

| Indicador | Valor |
|---|---|
| Organizações auditadas (com resposta) | 113 |
| Achados distintos | 6 (A1 a A6) |
| Situações inconformes distintas | 26 |
| Ações de verificação | 151 |
| Total de achados acumulados | 620 |
| Total de situações inconformes acumuladas | 2.096 |
| Encaminhamentos como **Recomendação** | 100% (24/24) |
| Encaminhamentos como **Determinação** | 0% (0/24) |

### 1.1 Distribuição dos Achados

| Achado | Nº orgs | % | Observação |
|---|---:|---:|---|
| **A4** – Capacidade institucional insuficiente | **113** | **100,0%** | ⚠️ Universal |
| **A5** – Gestão de serviços de TIC insuficiente | **113** | **100,0%** | ⚠️ Universal |
| **A6** – Fragilidades na governança de contratações | 111 | 98,2% | Quase universal |
| **A3** – Planejamento de TIC insuficiente | 108 | 95,6% | Quase universal |
| **A2** – Governança de TIC insuficiente | 107 | 94,7% | Quase universal |
| **A1** – Estrutura de TIC insuficiente | 68 | 60,2% | Frequência moderada |

### 1.2 Distribuição das Situações Inconformes (top 10)

| Situação | Achado | Nº orgs | % |
|---|---|---:|---:|
| Lacunas de competências não identificadas/tratadas | A4 | 112 | 99,1% |
| Perfis profissionais inexistentes/insuficientes | A4 | 111 | 98,2% |
| Níveis de serviço sem definição/monitoramento | A5 | 111 | 98,2% |
| Gestão de configuração ausente ou frágil | A5 | 110 | 97,3% |
| Catálogo de serviços inexistente/insuficiente | A5 | 108 | 95,6% |
| Modelo de governança inexistente/insuficiente | A2 | 107 | 94,7% |
| Quantitativo de pessoal de TIC não definido | A4 | 107 | 94,7% |
| Plano de TIC sem vínculo com orçamento | A3 | 106 | 93,8% |
| Contratações sem alinhamento ao planejamento | A6 | 106 | 93,8% |
| Gestão de incidentes inexistente/frágil | A5 | 102 | 90,3% |

---

## 2. Avaliação das Ações de Verificação — Proporcionalidade

Quando **100% das organizações** incorrem no mesmo achado, o problema pode não estar nas organizações — pode estar na **régua de exigência**. É preciso distinguir entre práticas essenciais (que todo órgão público deveria ter) e práticas desejáveis (que configuram boas práticas avançadas).

### 2.1 Achado 4 — Capacidade Institucional (100% de incidência)

O Achado 4 tem **6 situações inconformes** conectadas por **lógica disjuntiva pura** (OR):

```
(S4.1 | S4.2 | S4.3 | S4.4 | S4.5 | S4.6)
```

Isso significa que **basta uma** das seis situações para gerar o achado. As três situações mais frequentes são:

| Situação | % | Avaliação de Proporcionalidade |
|---|---:|---|
| **S4.5** – Lacunas de competências não identificadas/tratadas | 99,1% | ⚠️ **Excessivamente ampla.** Exige 4 itens simultaneamente: `q2705ext[B]`, `[C]`, `[D]` e `q2706ext[A]`. Qualquer um ausente gera a situação. Exigir que um município pequeno tenha diagnóstico formal de lacunas de competências em 4 dimensões (transversais, liderança, técnicas TI, técnicas SI) e ainda plano de capacitação é **desproporcional** para organizações com 1-3 profissionais de TI. |
| **S4.4** – Perfis profissionais inexistentes | 98,2% | ⚠️ **Parcialmente excessiva.** Combina `q2701ext[A]`, `q2702ext[A]` e `q2704ext[B]`. Exigir perfis formais de gestores **e** de colaboradores **e** seleção baseada em perfil é razoável para órgãos grandes, mas desproporcional para prefeituras pequenas com quadro mínimo. |
| **S4.2** – Quantitativo necessário não definido | 94,7% | ⚠️ **Razoável no conceito, mas a ação é restritiva.** Verifica `q2703ext[C]` (documentação formal). Nem todas as organizações pequenas têm condições de produzir estudo técnico de dimensionamento. |

**Oportunidades de melhoria no Achado 4:**

1. **Agrupar S4.4 e S4.5 em uma única situação** com threshold mais razoável — por exemplo, exigir que a organização tenha **ao menos perfis definidos para gestores de TI** (`q2701ext[A]`) e **ao menos identifique lacunas técnicas de TI** (`q2705ext[C]`), sem exigir os 7 itens cumulativos atuais.
2. **Transformar S4.3 (cargos específicos) em severidade baixa** — a inexistência de cargos específicos de TIC é uma limitação estrutural frequentemente fora da governabilidade do gestor de TI, dependendo de lei de criação de cargos.
3. **Reconsiderar se S4.2 (dimensionamento) é uma prática essencial ou desejável** para organizações com menos de 5 profissionais de TI.

### 2.2 Achado 5 — Gestão de Serviços de TIC (100% de incidência)

O Achado 5 também usa **lógica disjuntiva** entre as 5 situações:

```
(S5.1 | S5.2 | S5.3 | S5.4 | S5.5)
```

| Situação | % | Avaliação de Proporcionalidade |
|---|---:|---|
| **S5.2** – ANS sem definição/monitoramento | 98,2% | ⚠️ **Excessiva para muitos contextos.** Exigir que **todos** os órgãos tenham Acordos de Nível de Serviço formalizados e monitorados é uma prática avançada de ITIL. Para organizações com equipe de TI de 1-5 pessoas, é desproporcional. |
| **S5.4** – Gestão de configuração ausente/frágil | 97,3% | ⚠️ **Prática avançada.** CMDB formal com relacionamentos entre ativos, sistemas e infraestrutura é maturidade ITIL intermediária/avançada. Exigir `q2203ext[A]` (base consolidada) **e** `q2203ext[C]` (processo formalizado) simultaneamente é rigoroso demais para a maturidade média das organizações jurisdicionadas. |
| **S5.1** – Catálogo de serviços insuficiente | 95,6% | ⚠️ **Parcialmente excessiva.** Exige 3 itens (`q2201ext[A]`, `[B]`, `[C]`): metas definidas, catálogo atualizado e catálogo acessível. Seria mais proporcional exigir apenas a existência do catálogo (`[A]` ou `[C]`). |
| **S5.5** – Gestão de incidentes insuficiente | 90,3% | ✅ **Razoável.** Gestão de incidentes é prática fundamental. Porém, a verificação exige `q2204ext[A]` (priorização), `[D]` (formalização) **e** `[E]` (notificação de SI), o que é cumulativo. |
| **S5.3** – Inventário de ativos insuficiente | 85,8% | ✅ **Razoável.** Inventário de ativos é prática essencial de segurança. |

**Oportunidades de melhoria no Achado 5:**

1. **Considerar remover S5.2 (ANS) ou rebaixar para severidade baixa** — ANS formal é prática avançada; a maioria das organizações públicas de médio/pequeno porte não formaliza ANS internos.
2. **Simplificar S5.4 (gestão de configuração)** — exigir apenas inventário de ativos atualizado (`q2203ext[A]`), sem exigir processo formalizado (`q2203ext[C]`) e uso como insumo para mudanças (`q2203ext[B]`) simultaneamente.
3. **Reduzir a cumulatividade de S5.1 (catálogo)** — exigir apenas que a organização identifique os serviços prestados; metas e formalização do catálogo são práticas avançadas.

### 2.3 Achado 6 — Contratações de TIC (98,2% de incidência)

| Situação | % | Avaliação |
|---|---:|---|
| **S6.3** – Contratações sem alinhamento ao planejamento | 93,8% | ⚠️ **Critério muito amplo.** Usa 4 ações em OR: `q2102ext[C]`, `q2802ext[C]`, `q2802ext[D]`, `q2804[B]`. Basta um para disparar. |
| **S6.1** – Processo formal insuficiente | 86,7% | ✅ Razoável, mas com 5 itens em OR — talvez excessivo. |
| **S6.2** – Sem aprovação técnica da TI | 73,5% | ✅ **Razoável e essencial.** |
| **S6.4** – Sem equipe formalmente designada | 39,8% | ✅ Razoável. |

**Oportunidades de melhoria no Achado 6:**

1. **Revisar S6.3** — a sobreposição com S3.5 (do Achado 3) é parcial (`q2102ext[C]`, `q2802ext[C]`, `q2802ext[D]`, `q2804[B]` aparecem nos dois). Considerar se a dupla contagem é intencional ou se pode ser consolidada.
2. **Simplificar S6.1** — 5 itens em OR é muito amplo. Considerar manter apenas os essenciais: processo definido (`[A]`), papéis definidos (`[D]`) e aderência legal (`[G]`).

### 2.4 Achados 2 e 3 — Governança e Planejamento

| Situação | % | Avaliação |
|---|---:|---|
| **S2.1** – Modelo de governança insuficiente | 94,7% | ⚠️ **Critério amplo.** 4 itens em OR, qualquer ausência gera situação. |
| **S3.5** – Plano sem vínculo com orçamento | 93,8% | ⚠️ **Critério amplo com dupla contagem** (compartilha itens com S6.3). |
| **S3.1** – Processo de planejamento inexistente/frágil | 86,7% | ✅ Razoável. |
| **S3.2** – Aprovação formal ausente | 72,6% | ✅ Razoável. |
| **S2.2** – Comitê de TIC não instituído | 66,4% | ✅ Razoável. |

**Oportunidades de melhoria:**

1. **S2.1 é excessivamente ampla.** Modelo de governança é conceito abstrato. Exigir simultaneamente papéis (`q1001ext[C]`), objetivos/indicadores/metas (`q1001ext[H]`), rotinas de monitoramento (`q1002ext[A]`) e indicadores implantados (`q1002ext[C]`) é pedir 4 práticas avançadas em OR — basta faltar uma. Considerar reduzir para: papéis + objetivos/metas ou papéis + comitê.
2. **Eliminar a dupla contagem entre S3.5 e S6.3** — os mesmos itens (`q2102ext[C]`, `q2802ext[C]`, `q2802ext[D]`) alimentam duas situações em dois achados diferentes. Isso gera dois encaminhamentos pelo mesmo fato.

---

## 3. Avaliação das Situações Inconformes — Ajustes Propostos

### 3.1 Situações que merecem ser removidas ou reformuladas

| Situação | Achado | Incidência | Proposta |
|---|---|---:|---|
| **S4.3** – Ausência de cargos específicos de TIC/SI | A4 | 80,5% | **Remover ou rebaixar para observação.** A criação de cargos depende de lei em sentido estrito e está fora da governabilidade do gestor de TI. O encaminhamento ("avalie a necessidade") já é tímido — se a organização não tem autonomia para criar cargos, a recomendação é inócua. |
| **S5.2** – ANS sem definição/monitoramento | A5 | 98,2% | **Rebaixar severidade de Média para Baixa** ou **transformar em observação** dentro do relatório. ANS formal é prática ITIL avançada, incompatível com a maturidade de 98% do universo. |
| **S5.4** – Gestão de configuração ausente/frágil | A5 | 97,3% | **Simplificar a regra**: exigir apenas inventário atualizado (`q2203ext[A]`), sem exigir processo formalizado e uso como insumo para mudanças. CMDB formal é prática de maturidade intermediária-alta. |

### 3.2 Situações que merecem ajuste de escopo

| Situação | Achado | Proposta de ajuste |
|---|---|---|
| **S4.5** – Lacunas de competências | A4 | Reduzir de 4 para 2 itens obrigatórios: exigir apenas `q2705ext[C]` (lacunas técnicas de TI identificadas) e `q2706ext[A]` (plano de capacitação), sem exigir diagnóstico de lacunas transversais, de liderança e de SI cumulativamente. |
| **S4.4** – Perfis profissionais | A4 | Exigir apenas `q2701ext[A]` (perfis de gestores), sem cumulatividade com perfis de colaboradores e seleção baseada em perfil. |
| **S2.1** – Modelo de governança | A2 | Reduzir itens verificados: manter `q1001ext[C]` (papéis) e `q1001ext[H]` (objetivos/metas). Remover `q1002ext[A]` e `q1002ext[C]` (monitoramento) — que poderiam migrar para uma situação própria de menor severidade. |
| **S5.1** – Catálogo de serviços | A5 | Reduzir de 3 itens em OR para 1: exigir apenas que a organização possua catálogo (`q2201ext[A]`); metas e acessibilidade são incrementais. |

### 3.3 Impacto estimado dos ajustes

Se os ajustes acima fossem aplicados:

- **Achado 4** cairia de 100% para aproximadamente 75-85% (as organizações maiores continuariam, mas prefeituras pequenas com equipe mínima sairiam).
- **Achado 5** cairia de 100% para aproximadamente 85-90% (saindo organizações que já possuem inventário de ativos mas não possuem ANS formal ou CMDB).
- **Achados 2, 3 e 6** permaneceriam com alta incidência, mas com situações mais precisas e sem dupla contagem.

---

## 4. Avaliação de Questões de Auditoria

### 4.1 Questões que não necessitam ajuste

| Questão | Avaliação |
|---|---|
| **Q1** – Estrutura de TIC | ✅ Bem calibrada. Incidência de 60,2% indica régua proporcional. |
| **QT** – Evolução Agregada | ✅ Adequada como questão de levantamento, sem achados. |

### 4.2 Questões com oportunidade de calibração

| Questão | Problema | Proposta |
|---|---|---|
| **Q4** – Capacidade Institucional | Achado em 100% indica régua desproporcionada. | Simplificar S4.4 e S4.5 conforme item 3.2; considerar remover S4.3. |
| **Q5** – Gestão de Serviços | Achado em 100% indica régua desproporcionada. | Simplificar S5.2 e S5.4 conforme item 3.1; reduzir S5.1 conforme item 3.2. |
| **Q2** – Governança | 94,7% de incidência com S2.1 excessivamente ampla. | Reduzir S2.1 conforme item 3.2. |
| **Q3** e **Q6** | Dupla contagem entre S3.5 e S6.3. | Eliminar sobreposição, atribuindo os itens de orçamento/contratações a apenas um dos achados. |

---

## 5. Encaminhamentos: de Recomendação para Determinação

A distinção entre **Recomendação** e **Determinação** no direito brasileiro de controle externo segue o critério de vinculação normativa. Recomendação é utilizada quando a prática decorre de referencial técnico ou boa prática. Determinação é cabível quando há **comando normativo** — lei, decreto, resolução, deliberação plenária — que obriga a adoção da prática.

### 5.1 Situações que admitem Determinação

| Situação | Fundamento para Determinação | Proposta |
|---|---|---|
| **S2.2** – Comitê de TIC não instituído | **Decreto nº 12.198/2024, art. 5º** — institui o CGD como colegiado obrigatório para uso de recursos digitais na administração pública federal. Por analogia e por força do **Acórdão TCE-RJ 44.490/2024-PLEN, item II.1**, há deliberação plenária do TCE-RJ recomendando/determinando a instituição de comitê de TIC. Quando o órgão jurisdicionado já recebeu recomendação anterior não atendida, a conversão em determinação é plenamente justificada. | **Converter para DETERMINAÇÃO** para organizações que já receberam recomendação em ciclo anterior (iGovTI 2023). Para as demais, manter como Recomendação. |
| **S3.1** e **S3.2** – Planejamento de TIC e aprovação formal (PDTI/PEDTIC) | **Acórdão TCU 1.411/2014-Plenário, item 9.1.6** — determina a instituição de PDTI. **Acórdão TCE-RJ 44.490/2024-PLEN, item II.3 e subitens** — deliberação plenária do TCE-RJ com especificação detalhada do conteúdo mínimo do PDTI. A jurisprudência é consolidada e reiterada. | **Converter para DETERMINAÇÃO.** A existência de PDTI/PEDTIC vigente, aprovado e com processo formalizado é exigência consolidada na jurisprudência dos tribunais de contas. |
| **S6.2** – Contratações sem aprovação técnica da TI | **Lei 14.133/2021, arts. 18 e 19** — planejamento da contratação como fase obrigatória. **IN SGD/ME nº 94/2022, art. 1º, §1º** — referência de boa prática com ritos formais de contratação de TIC. A aprovação técnica pela área de TI é implícita na obrigação legal de estudo técnico preliminar. | **Converter para DETERMINAÇÃO**, pois decorre de obrigação legal (Lei 14.133/2021). |
| **S6.4** – Sem equipe de planejamento formalmente designada | **Lei 14.133/2021, art. 7º, caput e incisos** — designação de agentes públicos para funções essenciais nas contratações, incluindo equipe de planejamento. | **Converter para DETERMINAÇÃO**, pois a designação formal de equipe é comando legal direto. |
| **S6.1** – Processo formal de contratações de TIC | **Lei 14.133/2021** (múltiplos dispositivos) — a formalização do processo de contratação é obrigação legal. | **Converter para DETERMINAÇÃO** no que se refere à aderência às normas legais (`q2801ext[G]`); manter como Recomendação os aspectos de padronização de artefatos e modelos. |

### 5.2 Situações que devem permanecer como Recomendação

| Situação | Fundamento |
|---|---|
| **S1.1 a S1.3** – Estrutura de TIC | Não há comando legal que obrigue estrutura específica de TIC. Decorre de boas práticas (COBIT, ISO 38500). |
| **S2.1** – Modelo de governança | Prática derivada de referenciais técnicos (COBIT). Não há obrigação normativa direta. |
| **S2.3** – Comitê sem atuação efetiva | Prática derivada de boa governança. A atuação do comitê não é objeto de comando normativo direto. |
| **S3.4** – Alinhamento ao planejamento institucional | Boa prática gerencial. |
| **S3.6** – Acompanhamento periódico do plano | Boa prática gerencial. |
| **S4.1 a S4.6** – Capacidade institucional | Práticas de gestão de pessoas derivadas de COBIT e ISO 27001. Não há obrigação legal direta de dimensionamento ou perfis profissionais de TI. |
| **S5.1 a S5.5** – Gestão de serviços | Práticas ITIL/COBIT. Não há obrigação legal de catálogo de serviços, ANS, CMDB ou gestão de incidentes. |

### 5.3 Resumo da proposta de reclassificação

| Tipo | Atual | Proposta |
|---|---:|---:|
| **Recomendação** | 24 (100%) | 17 (71%) |
| **Determinação** | 0 (0%) | 5 (21%) |
| **Remoção/incorporação** | 0 | 2 (8%) |

---

## 6. Avaliação da Lógica dos Achados — Dupla Contagem

### 6.1 Sobreposição entre S3.5 (Achado 3) e S6.3 (Achado 6)

As seguintes ações de verificação alimentam **ambas** as situações:

| Ação | Item | Situação no A3 | Situação no A6 |
|---|---|---|---|
| AV20/AV98 | `q2102ext[C]` | S3.5 – Plano sem vínculo com orçamento | S6.3 – Contratações sem alinhamento |
| AV21/AV99 | `q2802ext[C]` | S3.5 | S6.3 |
| AV22/AV100 | `q2802ext[D]` | S3.5 | S6.3 |
| AV23 | `q2804[B]` | S3.5 | S6.3 |

**Problema:** A mesma falha gera dois achados e dois encaminhamentos com redações praticamente idênticas. Isso dilui a força da auditoria e gera duplicidade de recomendação para o mesmo fato.

**Proposta:** Atribuir os itens `q2802ext[C]` e `q2802ext[D]` exclusivamente a S6.3 (contratações), e `q2102ext[C]` exclusivamente a S3.5 (planejamento). O item `q2804[B]` é mais natural em S6.3. Isso eliminaria a sobreposição e daria redação mais precisa a cada encaminhamento.

---

## 7. Síntese das Oportunidades de Melhoria

### 7.1 Ações prioritárias (impacto alto)

| # | Ação | Impacto Esperado |
|---|---|---|
| 1 | **Simplificar S4.4 e S4.5** — reduzir itens obrigatórios | Achado 4 cai de 100% para ~80%, tornando-o mais seletivo |
| 2 | **Remover ou rebaixar S4.3** (cargos específicos) | Elimina achado fora da governabilidade do gestor |
| 3 | **Rebaixar S5.2** (ANS) para baixa severidade ou observação | Achado 5 cai de 100% para ~90% |
| 4 | **Simplificar S5.4** (configuração → apenas inventário) | Ajusta régua à maturidade real do universo |
| 5 | **Converter S2.2, S3.1, S3.2, S6.1 (parcial), S6.2, S6.4 para Determinação** | Reforça encaminhamentos com base normativa sólida |
| 6 | **Eliminar dupla contagem S3.5/S6.3** | Precisão nos achados e encaminhamentos |

### 7.2 Ações secundárias (calibração fina)

| # | Ação | Impacto Esperado |
|---|---|---|
| 7 | Reduzir S2.1 — separar monitoramento de modelo de governança | S2.1 mais precisa |
| 8 | Reduzir S5.1 — exigir apenas existência do catálogo | S5.1 mais proporcional |
| 9 | Reduzir S6.1 — manter apenas itens legalmente obrigatórios | Coerência com determinação parcial |

---

## 8. Conclusão

A matriz de planejamento e o mapa de verificação de achados do iGovTI 2026 estão **bem estruturados, rastreáveis e tecnicamente coerentes**. Os critérios utilizados são adequados e os encaminhamentos são proporcionais na maioria dos casos.

Entretanto, a análise dos resultados pós-comentários do gestor revela que **dois achados (A4 e A5) incidem sobre 100% das organizações auditadas**, o que indica que a régua de exigência dessas questões está acima da maturidade real do universo jurisdicionado. Quando um achado é universal, ele perde poder discriminatório e utilidade prática como instrumento de melhoria.

As oportunidades de melhoria concentram-se em:

1. **Proporcionalidade**: simplificar situações que exigem práticas avançadas (ANS, CMDB, diagnóstico de lacunas em 4 dimensões) ou fora da governabilidade (cargos específicos por lei).
2. **Força normativa**: converter 5 encaminhamentos de Recomendação para Determinação quando há fundamento legal ou jurisprudencial consolidado (PDTI, Comitê de TIC, aprovação técnica de contratações, equipe de planejamento, processo formalizado de contratação).
3. **Precisão**: eliminar dupla contagem entre achados de planejamento e contratações.

As modificações propostas não eliminam achados — **recalibram-nos** para que incidam sobre as organizações que de fato apresentam fragilidades materiais, aumentando a seletividade e a credibilidade da fiscalização.
