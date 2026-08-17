# Revisão crítica da matriz de planejamento e do mapa de verificação de achados (posicionamento pós-comentários do gestor)

## Identificação

| Campo | Informação |
|---|---|
| Fiscalização | TCE-RJ nº 18/2026 — iGovTI 2026 |
| Objeto | `01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/matriz_planejamento.md` e `02-Execucao/03-Execucao_Procedimentos/01-Insumos/mapa-verificacao-achados.xlsx` |
| Base de resultado | `02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/03-pos-comentarios-gestor/resultado_auditoria.json` (113 organizações) |
| Data da análise | 14/08/2026 |
| Realizada por | DeepSeek V4 Flash |
| Natureza | Minuta técnica de revisão; propostas sujeitas à deliberação da Equipe de Auditoria |

---

## 1. Parecer executivo

O desenho da matriz e do mapa é sólido, rastreável e, em sua quase totalidade, proporcional: os critérios citam normas e referenciais com item específico (COBIT/ITIL/ISO, Lei 14.133/2021, Acórdãos TCU 1.411/2014 e TCE-RJ 44.490/2024), as regras são objetivas e os encaminhamentos trazem cláusulas de proporcionalidade ("compatível com o porte..."). **Nenhuma questão de auditoria, nenhum achado e nenhuma situação inconforme deve ser removida em bloco.** Há, porém, seis ajustes concretos de lógica, rastreabilidade e proporcionalidade que devem ser feitos, e um conjunto de encaminhamentos com fundamento jurídico e jurisprudencial suficiente para elevação a DETERMINAÇÃO.

A análise quantitativa pós-comentários mostra que os Achados 4 e 5 atingem 100% da população (113/113) e os Achados 2, 3 e 6 ficam entre 94,7% e 98,2%. A incidência quase universal não decorre apenas de regras exigentes: mesmo mínimos objetivos (formalização de ANS: 112/113 sem a prática; quantitativo necessário de pessoal: 107/113) concentram a população. Ainda assim, três situações têm problema real de lógica que produz **dupla contagem** do mesmo fato (S2.2/S2.3, S5.3/S5.4, S3.5/S6.3) e devem ser corrigidas.

---

## 2. Diagnóstico quantitativo pós-comentários do gestor

| Achado | Organizações | Incidência |
|---|---:|---:|
| A1 — Estrutura de TIC | 68 | 60,2% |
| A2 — Governança e Comitê de TIC | 107 | 94,7% |
| A3 — Planejamento de TIC | 108 | 95,6% |
| A4 — Capacidade institucional | 113 | 100,0% |
| A5 — Gestão de serviços | 113 | 100,0% |
| A6 — Contratações de TIC | 111 | 98,2% |

Situações com maior incidência (total de 2.096 ocorrências):

| Situação | Ocorrências |
|---|---:|
| S4.5 — Lacunas de competências não identificadas/tratadas | 112 |
| S4.4 — Perfis profissionais inexistentes/não usados na escolha de gestores | 111 |
| S5.2 — Níveis mínimos de serviço ausentes/frágeis | 111 |
| S5.4 — Gestão de configuração ausente/frágil | 110 |
| S5.1 — Catálogo de serviços ausente/insuficiente | 108 |
| S2.1 — Modelo básico de governança inexistente/insuficiente | 107 |
| S4.2 — Quantitativo necessário de pessoal não definido | 107 |
| S3.5 ≡ S6.3 — Plano/contratações sem vínculo com orçamento e planejamento | 106 (conjuntos idênticos) |
| S5.5 — Gestão de incidentes ausente/frágil | 102 |
| S3.1 — Processo formal de planejamento ausente/frágil | 98 |

Fonte: `resultado_auditoria.json` pós-comentários (113 organizações auditadas com resposta).

---

## 3. Item 1 — Ações de verificação do mapa: ajustes necessários

### 3.1 Quarenta e uma ações órfãs (sem efeito em achado ou motivo)

41 das 151 ações não constam de nenhuma lógica PA01–PA06 nem de nenhuma condição de exibição de "Motivos do Relatório" e não produzem nenhum efeito no resultado da auditoria (verificação feita no JSON de resultado: nenhuma delas aparece):

`AV26, AV28, AV30, AV32, AV35, AV37, AV43, AV44, AV47–AV52, AV60, AV61, AV65, AV68, AV69, AV72, AV102, AV104, AV106, AV109, AV111, AV113–AV115, AV117–AV123, AV130, AV131, AV135, AV138, AV139, AV142`

Classificação das órfãs por tratamento recomendado:

| Grupo | Ações | Recomendação |
|---|---|---|
| Gate pretendido para S4.1 | AV26 (q0101 ≠ F) | **Religar** em PA04: `(AV26 & (AV25 \| AV27))` — evita que organização sem área de TIC (S1.1) seja também apontada por S4.1 (ver 3.3) |
| Evidências de lacunas (q2705 B/C/D) | AV113–AV115 | **Religar** em PA04 junto a AV39–AV41 — hoje a rejeição da evidência de q2705 não gera situação, enquanto a de q2706ext[A] (AV116) gera (assimetria; ver 3.4) |
| Cargos efetivos (q2708 A/C) | AV30, AV32, AV104, AV106 | **Remover** — exigir "cargos efetivos" esbarra em reserva legal e não é mínimo aceitável; PA04 já usa corretamente apenas B/D |
| Perfis com competências/habilidades (q2701ext[C], q2702ext[C]) | AV35, AV37, AV109, AV111 | **Remover** — item mais exigente que o "A" já utilizado (definição documentada e publicada); manter apenas A |
| Complementos declaratórios de S4.6 (q2703ext[B/C], q2801ext[E/F], q2804[A/C]) | AV47–AV52, AV119–AV123 | **Remover** — se religados, elevariam S4.6 para quase toda a população; a regra atual `(AV45 & AV46) \| AV53` é a mais proporcional |
| Critérios técnicos de dimensionamento (q2703ext[B]) | AV28, AV102 | **Remover** — q2703ext[C] (quantitativo documentado) já é o mínimo utilizado em S4.2 |
| Uso da base de configuração em mudanças (q2203ext[B]) | AV65, AV135 | **Remover** — alta maturidade; S5.4 já exige o mínimo (base consolidada A e formalização C) |
| Incidentes: ANS na resolução, base de conhecimento, causa raiz (q2204 B/C/F) | AV68, AV69, AV72, AV138, AV139, AV142 | **Remover** — alta maturidade; PA05 já excluiu corretamente esses itens da situação |
| Incentivo/monitoramento de capacitação (q2706 B/C) | AV43, AV44, AV117, AV118 | **Remover** — o plano de capacitação (q2706ext[A]) é o mínimo; incentivo e monitoramento são maturidade |
| Inventário de ativos de informação (q2501 A/B) | AV60, AV61, AV130, AV131 | **Remover** — S5.3 já cobre inventário por q2203ext[A]/q2504ext[A]/[B]; manter q2501 apenas como dado do iGovTI |
| Ações de S4.2 duplicadas (q2703ext[B]) | AV28, AV102 (acima) | Remover |

Impacto: remoção não altera nenhum achado (ações não produzem efeito) e elimina risco de questionamento de rastreabilidade. Manter o registro das avaliações de evidência já produzidas nos `analyses*.jsonl` como memória de execução.

### 3.2 Falha de lógica S2.2/S2.3 — a mesma avaliação de evidência conta duas vezes

AV89 e AV90 avaliam o **mesmo target** (`q1001ext[E]`, valor "Não conforme" no painel) com descrições de situação diferentes (S2.2 e S2.3). Na prática:

- 17 organizações receberam S2.3 **sem nunca ter declarado comitê** (q1001ext[E] = Não ou N/A: CECIERJ, DETRAN, FSC, IPEM, IVB, LOTERJ, SEDEICS, SEEDUC, SEFAZ, SEINFRA, SEPM, SES, SETRAB, SETRANS, GUAPIMIRIM, JAPERI, SÃO PEDRO DA ALDEIA), contrariando a própria regra da matriz `(q1001ext[E] == Sim) & (q1001ext[F] != Sim)`;
- 7 organizações (DETRAN, SEEDUC, SEFAZ, SES, SETRAB, SETRANS, GUAPIMIRIM) receberam **simultaneamente** S2.2 e S2.3 pelo mesmo fato (evidência "Não conforme" de q1001ext[E] sem declaração).

Correção proposta:

- S2.2 → `(AV11)` apenas (declaração de não instituição). A insuficiência de evidência não pode, sozinha, caracterizar "não instituído";
- S2.3 → `(AV12 & (AV13 | AV91))` (declarou comitê E, e não declarou atuação F ou evidência de F não conforme). AV90 deixa de compor S2.3;
- Ajustar MR016–MR021 (condições de exibição que hoje usam `AV89`/`AV90` como alternativas).

Impacto estimado: S2.3 cai de 27 para cerca de 10–17 organizações (só quem declarou comitê — 10 com E=Sim e F=Não no resultado, mais eventuais casos de E=Sim com evidência de atuação não conforme), e desaparece a dupla contagem. S2.2 permanece ~75 (todas por declaração; verificado: nenhuma das 75 declarou comitê — AV89 nunca foi o gatilho real).

### 3.3 S4.1 sem gate — dupla contagem com S1.1

AV26 (q0101 ≠ F) foi criada para condicionar S4.1 a organizações que possuem área de TIC, mas ficou órfã. FTM, TURISRIO e SÃO JOÃO DA BARRA (q0101 = f) recebem hoje S1.1 **e** S4.1 pelo mesmo fato (sem área de TI e sem força de trabalho de SI). Corrigir PA04: `((AV26 & (AV25 | AV27)) | ...)` → S4.1 cai de 59 para 56 e ganha semântica correta.

### 3.4 Assimetria de evidência em S4.5

Em S4.5, a rejeição da evidência de `q2706ext[A]` (AV116) gera situação, mas a rejeição da evidência de `q2705ext[B/C/D]` (AV113–AV115, órfãs) não gera. Resultado: organização que **declara** identificar lacunas com evidência frágil escapa do achado, enquanto quem declara plano de capacitação com evidência frágil é apontada. Religar as três: `(AV39 | AV113) | (AV40 | AV114) | (AV41 | AV115) | (AV42 | AV116)`. Impacto na incidência: marginal (112 → ~112), mas fecha o loophole de "declara e não comprova".

### 3.5 Divergência matriz × mapa em S1.3 (harmonizar no sentido do mapa)

A matriz inclui `q0102 == B` (subordinação a secretaria/subsecretaria/diretoria-geral de nível estratégico) na regra de S1.3; o mapa exclui B (usa apenas C, D, E). Quantificação: com B, S1.3 atingiria 77 organizações; sem B, 27 (22 no resultado com ajustes de evidência). O mapa está correto: subordinação a instância de nível estratégico é posicionamento aceitável (a Portaria SGD/ME 778/2019 exige apenas vinculação *preferencial* à alta administração). **Ajustar a matriz**, não o mapa.

### 3.6 Dupla contagem S5.3/S5.4 por compartilhamento de q2203ext[A]

S5.3 (inventário) e S5.4 (configuração) usam o mesmo `q2203ext[A]` ("base de dados consolidada"); 95 organizações recebem as duas situações pelo mesmo item. Correção: manter `q2203ext[A]` apenas em S5.3; S5.4 passa a `(q2203ext[C] != Sim)` (formalização do processo). Impacto: incidência praticamente inalterada (110 → 108, ver dados na seção 5), mas cada situação passa a ter gatilho próprio e rastreável.

### 3.7 Sobreposição total S3.5 × S6.3

S3.5 (A3) e S6.3 (A6) usam exatamente os mesmos 4 itens (q2102ext[C], q2802ext[C], q2802ext[D], q2804[B]); os conjuntos de organizações são idênticos (106 = 106). Não é erro de dupla contagem no mesmo achado, mas gera aparência de punição dupla pelo mesmo fato em achados distintos. Tratamento recomendado: manter as duas situações (cada uma responde a subquestão própria das Q3 e Q6), registrando **nota metodológica explícita** na matriz de achados e no relatório consolidado. Alternativa de simplificação (se a equipe preferir): suprimir S6.3 e manter S3.5, reduzindo A6 a 3 situações — porém isso deixaria a subquestão "as contratações estão alinhadas ao plano de TIC/PCA?" sem resposta direta no Achado 6.

---

## 4. Item 2 — Questões de auditoria e achados: nada a remover

- **Q1–Q6 são essenciais, respondíveis e cobertas por critérios específicos**; os seis achados correspondem fielmente às questões. Manter.
- **QT (evolução agregada)** está corretamente configurada como levantamento (`gera_achado: false`) com critérios de comparabilidade e limitações. Manter.
- **A4 e A5 universais (100%)**: não remover. A incidência reflete o estágio de maturidade real (mesmo mínimos objetivos concentram a população). Recomenda-se reforçar, na matriz de achados e no relatório, a cláusula de proporcionalidade ("compatível com o porte e a complexidade") na narrativa desses achados, pois são os mais expostos a contestação.
- **A3/A6**: manter ambos, com a nota metodológica do item 3.7.

---

## 5. Item 3 — Situações inconformes: avaliação de proporcionalidade e recalibração

| Situação | Regra atual | Incidência | Avaliação e proposta |
|---|---|---|---|
| S1.3 (posicionamento, média) | matriz: inclui B; mapa: C/D/E | 22 (27 sem ajustes) | **Ajustar matriz** para excluir B (ver 3.5). Severidade média correta. |
| S2.2 (comitê não instituído, alta) | `AV11 \| AV89` | 75 | **Corrigir** para `AV11` apenas (ver 3.2). Severidade alta mantida (jurisprudência). |
| S2.3 (comitê sem atuação, média) | `(AV12 \| AV90) & (AV13 \| AV91)` | 27 | **Corrigir** para `AV12 & (AV13 \| AV91)` (ver 3.2). |
| S4.1 (sem força de trabalho, alta) | `total_TI==0 \| total_SI==0` | 59 | **Adicionar gate** AV26 (ver 3.3). Severidade alta questionável para orgãos com 1–2 técnicos acumulando SI — manter alta apenas para ausência total, ou rebaixar para média em S4.1. Avaliar com a equipe. |
| S4.2 (quantitativo não definido, alta) | `q2703ext[C] != Sim` | 107 | Mínimo razoável (estimativa documentada). Manter. Severidade alta compatível com risco de subdimensionamento. |
| S4.3 (cargos/funções, média) | `q2708[B] != Sim \| q2708[D] != Sim` | 91 | Correta a opção por B/D (funções formais) em vez de A/C (cargos efetivos). Manter. Encaminhamento já usa verbo suave ("avalie a necessidade..."). |
| S4.4 (perfis profissionais, média) | `q2701ext[A] \| q2702ext[A] \| q2704ext[B]` | 111 (112 na base) | O item dominante é q2704ext[B] (seleção por perfil — 112/113). É o mais próximo de "prática de alta maturidade" no conjunto, mas é a essência da situação e está no questionário. Manter regra; na narrativa, destacar que o encaminhamento deve respeitar a natureza das designações políticas (perfis mínimos, não concurso). |
| S4.5 (lacunas de competências, média) | `q2705 B/C/D + q2706[A]` | 112 | **Religar AV113–115** (ver 3.4). Regra razoável como mínimo (diagnóstico + plano); incidência 99% reflete realidade. Manter severidade média. |
| S4.6 (dependência externa, alta) | `((q0101 b\|c) & interno==0) \| predominio` | 17 | Regra proporcional; todos os 17 casos vieram de `predominio_terceiros` (AV53) e apenas IVB também por `(AV45 & AV46)`. Manter; para modelo "c" (Centralizada Externa, ex.: PRODERJ), avaliar caso a caso se a condição `interno==0` é adequada. |
| S5.2 (níveis mínimos de serviço, média) | `q2201ext[D] \| q2201ext[E]` | 111 | D (112) domina; E (108) pouco adiciona. Mínimo aceitável: manter (ANS formalizados e monitorados). Sem ajuste. |
| S5.3 (inventário, alta) | `q2203ext[A] \| q2504ext[A] \| q2504ext[B]` | 97 | **Manter q2203ext[A] aqui** (ver 3.6). Mínimo aceitável de controle patrimonial de TI. |
| S5.4 (configuração, média) | `q2203ext[A] \| q2203ext[C]` | 110 | **Passar a só `q2203ext[C]`** (ver 3.6) — remove dupla contagem com S5.3 sem mudar incidência (108). A CMDB relacional plena não é mínimo para órgãos pequenos. |
| S5.5 (incidentes, alta) | `q2204ext[A] \| [D] \| [E]` | 102 | Correta a exclusão de B/C/F (ANS em resolução, base de conhecimento, causa raiz). Manter. |
| S3.1 (processo de planejamento, alta) | 4 itens OR (A/B/C/D) | 98 (101 na base) | q2101ext[C] (análises de benefício/custo/risco) é o item mais exigente (96/113); retirá-lo reduziria para 95 — diferença pequena. Manter (o item consta da jurisprudência TCU 1.411/2014 como elemento do PDTI). |
| S2.1 (modelo básico, alta) | 4 itens OR (C/H + q1002 A/C) | 107 | q1002ext[C] (indicadores implantados) é o mais exigente (99/113); retirá-lo reduziria para 106. Manter. |
| S3.5/S6.3 (vínculo com orçamento e planejamento, alta) | mesmos 4 itens | 106/106 | Manter com nota metodológica (ver 3.7). |

Conclusão do item: nenhuma situação deve ser **removida**; cinco devem ser **ajustadas** (S1.3 na matriz; S2.2/S2.3, S4.1, S4.5, S5.4 no mapa).

---

## 6. Item 4 — Encaminhamentos: elevação de RECOMENDAÇÃO para DETERMINAÇÃO

Todos os 151 encaminhamentos do mapa estão como `Recomendação`. A jurisprudência consolidada (Acórdão TCE-RJ 44.490/2024-PLEN e Acórdão TCU 1.411/2014-Plenário, já citados como critérios na própria matriz) e normas com força vinculante (Lei 14.133/2021) sustentam a elevação de parte deles. A determinação é cabível mesmo sem normativo explícito para PDTI/PEDTIC/Comitê de TI porque o TCE-RJ já deliberou sobre o conteúdo mínimo de governança de TI no item II do Acórdão 44.490/2024-PLEN.

### Tier 1 — elevação com fundamento firme (jurisprudência e/ou lei expressa)

| Situação | Incidência | Fundamentos |
|---|---|---|
| S2.2 — Comitê de TIC não instituído | 75 | Acórdão TCE-RJ 44.490/2024-PLEN, item II.1 (estrutura de governança de TI, especialmente Comitê de TI ou instância equivalente, com participação de áreas relevantes, priorização de investimentos e monitoramento por indicadores); TCU 1.411/2014-Plenário (item 9.1.1) |
| S3.1 — Processo formal de planejamento de TIC | 98 | Acórdão TCE-RJ 44.490/2024, item II.3 (processo estruturado, com participação das principais secretarias, para elaborar, manter e revisar periodicamente o PDTI); TCU 1.411/2014, item 9.1.6 |
| S3.2 — Aprovação formal do plano de TIC | 82 | Acórdão TCE-RJ 44.490/2024, item II.3.5 (aprovação do PDTI pela autoridade máxima); TCU 1.411/2014, item 9.1.6 |
| S3.5 — Plano sem vínculo com orçamento e contratações | 106 | TCU 1.411/2014, item 9.1.6.4 (vinculação das ações priorizadas ao orçamento de TI); TCE-RJ 44.490/2024, item II.3.4 (alocação de recursos); Lei 14.133/2021, art. 18, § 1º, I (compatibilização com o plano de contratações anual) |
| S6.1 — Processo formal/padronizado de contratações de TIC | 98 | Lei 14.133/2021, art. 11, parágrafo único (governança das contratações) e art. 19, IV (modelos de minutas, TR e contratos padronizados) |
| S6.3 — Contratações sem alinhamento ao planejamento/PCA/orçamento | 106 | Lei 14.133/2021, art. 18, caput e § 1º, I (fase preparatória; compatibilização com o PCA) |
| S6.4 — Equipe de planejamento da contratação não designada | 45 | Lei 14.133/2021, art. 7º (agentes públicos para funções essenciais) e art. 18 (equipe de planejamento da contratação — confirmar o dispositivo exato antes da redação final; referência regulamentar federal: IN SGD/ME 58/2022) |

### Tier 2 — elevação avaliável, com cautela redacional

| Situação | Incidência | Fundamentos e cautela |
|---|---|---|
| S2.1 — Modelo básico de governança | 107 | TCE-RJ 44.490/2024, item II.1. Cautela: redigir objeto objetivo (papéis, responsabilidades, objetivos/indicadores/metas e acompanhamento periódico), sem detalhar ferramentas. |
| S3.4 — Plano sem alinhamento institucional | 73 | TCU 1.411/2014, itens 9.1.6.1/9.1.6.2. Objeto qualitativo; elevar apenas se a redação final permitir verificação objetiva. |
| S3.6 — Sem acompanhamento/revisão periódica | 89 | TCE-RJ 44.490/2024, item II.3 ("manter e revisar periodicamente"). Elevação defensável. |
| S6.2 — Sem análise prévia da área de TIC | 83 | Fundamento mais fraco: IN SGD/ME 94/2022 é norma federal de referência; Notas Técnicas TCE-RJ (ex.: 06/2023) orientam a prática. Sugestão: manter Recomendação, ou elevar apenas para órgãos estaduais vinculados ao SETIC/PRODERJ. |

### Manter como RECOMENDAÇÃO

- **S1.1–S1.3** (estrutura, atribuições, posicionamento): criação de estrutura/posicionamento é reserva do Chefe do Executivo; a Portaria SGD/ME 778/2019 é referência *preferencial*. Determinação seria invasiva e pouco verificável.
- **S4.1–S4.6** (força de trabalho, cargos, perfis, competências, dependência): cargos/carreiras têm reserva legal; os encaminhamentos usam verbos abertos ("avalie... adote medidas proporcionais") não adequados a determinação.
- **S5.1–S5.5** (catálogo, ANS, inventário, configuração, incidentes): práticas ancoradas em ITIL/COBIT, sem jurisprudência citada na matriz; manter como recomendação evita exigir "o que pode ter" como "o que deve ter".

### Implicações operacionais da elevação

- Alterar a coluna `tipo_encaminhamento` no mapa (e `tipo_encaminhamento` nas situações da matriz) e **re-executar** `executa_auditoria.py`, regerando `resultado_auditoria.json`, relatórios individuais e matriz de achados;
- Verificar nos templates de relatório individual (`relatorio-individual-preliminar-template.md`) e no relatório consolidado o tratamento da categoria "Determinação" (texto, numeração e encaminhamentos finais);
- Avaliar impacto no comparativo com a fiscalização anterior (a elevação muda o universo de "recomendações" monitoradas no próximo ciclo);
- A redação dos encaminhamentos elevados já inicia com verbos imperativos adequados ("institua", "estabeleça", "submeta", "integre"), o que facilita a conversão.

---

## 7. Implicações operacionais dos ajustes do mapa

1. As correções 3.1–3.6 alteram as lógicas PA01–PA06 e as condições MR016–MR021; após editar o mapa, revalidar com o CLI (`executa_auditoria.py --somente-dados` ou com `--skip-*` para os acessórios) e conferir o `resultado_auditoria.json` de teste em `/tmp/tcerj-igovti-2026`.
2. A remoção das 41 ações órfãs deve ser acompanhada da regeneração do painel (`gerar_fonte_ajustes_evidencias_auditoria.py`) e da revisão do catálogo de prompts (`igovti_2026_achados_binario_v1.yml`), mantendo apenas itens efetivamente avaliados pelo mapa. As análises já produzidas (`analyses*.jsonl`) permanecem como memória de execução.
3. Se a equipe optar por não remover as ações órfãs (ex.: para preservar histórico), registrar nota no mapa indicando que se trata de avaliações complementares não geradoras de achado — menos recomendável por expor a rastreabilidade.
4. Antes de aplicar qualquer mudança ao mapa de produção, executar os ajustes em cópia em `/tmp` e validar com o provider fake (validação estrutural), conforme AGENTS.md.

---

## 8. Resumo priorizado de propostas

| # | Proposta | Efeito |
|---|---|---|
| 1 | Corrigir PA02 (S2.2 = AV11; S2.3 = AV12 & (AV13 \| AV91)) e MR016–21 | Elimina dupla contagem do mesmo fato; S2.3 27 → ~10–17 |
| 2 | Religar AV26 em PA04 (gate S4.1) | S4.1 59 → 56; elimina dupla contagem com S1.1 |
| 3 | Religar AV113–115 em PA04 (evidências S4.5) | Fecha loophole "declara sem comprovar" |
| 4 | Remover 38 ações órfãs restantes (exceto AV26/AV113–115 religadas) | Rastreabilidade; sem alteração de achados |
| 5 | Ajustar matriz S1.3 (excluir q0102==B) e S4.6 (nota sobre modelo C) | Alinhamento matriz × mapa; 77 → 27 |
| 6 | S5.4 → apenas q2203ext[C]; manter q2203ext[A] só em S5.3 | Elimina dupla contagem S5.3/S5.4 (95 casos) |
| 7 | Nota metodológica S3.5 ≡ S6.3 (mesmos itens; 106 orgs) | Prevê alegação de punição dupla |
| 8 | Elevar a DETERMINAÇÃO: S2.2, S3.1, S3.2, S3.5, S6.1, S6.3, S6.4 (Tier 1) e avaliar S2.1, S3.4, S3.6, S6.2 (Tier 2) | Fortalece efetividade do controle externo |

---

## 9. Trechos sugeridos (lógicas atualizadas)

**PA01** (inalterado): `(AV01 | (AV02 & (AV03 | (AV04 | AV84))) | (AV05 & AV06))`

**PA02** (corrigido):
```
(((AV07 | AV85) | (AV08 | AV86) | (AV09 | AV87) | (AV10 | AV88)) | AV11 | (AV12 & (AV13 | AV91)))
```
S2.2 = `AV11`; S2.3 = `AV12 & (AV13 | AV91)`.

**PA03** (inalterado): `(((AV14|AV92)|(AV15|AV93)|(AV16|AV94)|(AV17|AV95)) | (AV18|AV96) | (AV19|AV97) | ((AV20|AV98)|(AV21|AV99)|(AV22|AV100)|AV23) | (AV24|AV101))`

**PA04** (corrigido):
```
((AV26 & (AV25 | AV27)) | (AV29 | AV103) | ((AV31 | AV105) | (AV33 | AV107)) | ((AV34 | AV108) | (AV36 | AV110) | (AV38 | AV112)) | ((AV39 | AV113) | (AV40 | AV114) | (AV41 | AV115) | (AV42 | AV116)) | ((AV45 & AV46) | AV53))
```

**PA05** (corrigido):
```
(((AV54 | AV124) | (AV55 | AV125) | (AV56 | AV126)) | ((AV57 | AV127) | (AV58 | AV128)) | ((AV59 | AV129) | (AV62 | AV132) | (AV63 | AV133)) | (AV66 | AV136) | ((AV67 | AV137) | (AV70 | AV140) | (AV71 | AV141)))
```
S5.4 = `(AV66 | AV136)` apenas (formalização do processo).

**PA06** (inalterado): `(((AV73|AV143)|(AV74|AV144)|(AV75|AV145)|(AV76|AV146)|(AV77|AV147)) | (AV78|AV148) | ((AV79|AV149)|(AV80|AV150)|(AV81|AV151)|AV82) | AV83)`

**Determinações (Tier 1)** — sugestão de redação final para o mapa (coluna `tipo_encaminhamento` = "Determinação"), mantendo as cláusulas de proporcionalidade já existentes:

- S2.2: "institua formalmente Comitê de TIC ou instância equivalente, compatível com o porte e a estrutura decisória da organização, atentando-se, minimamente, em definir sua composição, competências, periodicidade de reuniões, forma de registro das deliberações e acompanhamento dos encaminhamentos" (Acórdão TCE-RJ 44.490/2024-PLEN, item II.1);
- S3.1: "institua processo formal de planejamento de TIC, compatível com o porte e a maturidade da organização, atentando-se, minimamente, em definir etapas, responsáveis, participação das áreas demandantes e critérios de priorização das necessidades e iniciativas de TIC" (Acórdão TCE-RJ 44.490/2024-PLEN, item II.3);
- S3.2: "submeta o plano de TIC à aprovação formal do dirigente máximo ou de dirigente ou colegiado integrante da alta administração, mantendo registro do respectivo ato de aprovação" (Acórdão TCE-RJ 44.490/2024-PLEN, item II.3.5);
- S3.5: "integre o plano de TIC à proposta orçamentária, ao plano de contratações e às contratações de TIC, atentando-se, minimamente, em priorizar as demandas conforme sua relevância, seus riscos e a capacidade de execução da organização" (TCU 1.411/2014, item 9.1.6.4);
- S6.1: "formalize e padronize o processo de contratação de TIC, compatível com o porte, a complexidade e os riscos das contratações da organização, atentando-se, minimamente, em definir fluxo, etapas, papéis, responsabilidades, instâncias de aprovação e modelos de artefatos, manuais, listas de verificação ou orientações internas aplicáveis" (Lei 14.133/2021, arts. 11 e 19, IV);
- S6.3: "integre as contratações de TIC ao planejamento de TIC, ao plano de contratações e à proposta orçamentária, atentando-se, minimamente, em registrar a necessidade atendida, a prioridade, a disponibilidade de recursos e a justificativa das situações excepcionais" (Lei 14.133/2021, art. 18, § 1º, I);
- S6.4: "designe formalmente equipe responsável pelo planejamento das contratações de TIC, atentando-se, minimamente, em assegurar a participação da área requisitante, da área técnica de TIC e das demais áreas necessárias, com definição das responsabilidades de seus integrantes" (Lei 14.133/2021, arts. 7º e 18).

---

## 10. Ressalvas

- Esta análise foi gerada por modelo de IA como subsídio técnico; todas as propostas dependem de validação e deliberação da Equipe de Auditoria antes de qualquer alteração em artefatos de produção.
- As incidências informadas combinam a base de respostas processadas (`20260621-respostas-questionario-02-pos-avaliacao-evidencias.xlsx`, 113 organizações) com o resultado pós-comentários; pequenas diferenças entre base e resultado decorrem dos ajustes por avaliação de evidências e dos comentários do gestor.
- A elevação a DETERMINAÇÃO deve ser precedida de confirmação dos dispositivos citados (notadamente o artigo da Lei 14.133/2021 relativo à equipe de planejamento da contratação) e da redação final dos relatórios individuais.

---

# Adendo — Alterações no mapa com a premissa de lógica de processamento inalterada

**Premissa**: as fórmulas `logica_achado` (PA01–PA06, aba "Procedimentos de Auditoria") não serão alteradas. Abaixo, exclusivamente as alterações aplicáveis ao `mapa-verificacao-achados.xlsx` sob essa premissa (números de linha = linhas do Excel na aba "Ações de Verificação"; cabeçalho de exibição na linha 1 e cabeçalho de campos na linha 2).

## A. Remoções na aba "Ações de Verificação" (41 linhas órfãs — nenhum efeito no processamento)

| DE | PARA | Motivação/justificativa |
|---|---|---|
| AV26 (L29) presente | Linha removida | Ação criada para condicionar S4.1 a organização com área de TIC (`q0101 ≠ F`), mas nunca religada ao PA04. Não consta de nenhuma lógica nem de "Motivos do Relatório" e não aparece em nenhum resultado (verificado no `resultado_auditoria.json` pós-comentários). Religar exigiria alterar PA04 — vedado pela premissa. Sem efeito computacional; remove ruído de rastreabilidade. |
| AV113, AV114, AV115 (L116–118) presentes | Linhas removidas | Avaliações de evidência de `q2705ext[B/C/D]` sem efeito: enquanto `AV116` (q2706ext[A]) dispara S4.5, a rejeição de evidência de q2705 não gera situação (assimetria só corrigível alterando PA04 — vedado). Sem efeito computacional hoje. |
| AV30, AV32, AV104, AV106 (L33, L35, L107, L109) presentes | Linhas removidas | Cargos *efetivos* de TI/SI (`q2708[A]` e `[C]`): PA04 usa corretamente apenas `[B]/[D]` (funções formalmente atribuídas). Exigir cargos efetivos esbarra em reserva legal e não é mínimo aceitável; as ações são órfãs. |
| AV35, AV37, AV109, AV111 (L38, L40, L112, L114) presentes | Linhas removidas | `q2701ext[C]`/`q2702ext[C]` (competências e habilidades no perfil): item mais exigente que o "A" já utilizado em S4.4 (responsabilidades definidas, documentadas e publicadas). Órfãs; sem efeito. |
| AV47, AV48, AV49, AV50, AV51, AV52 (L50–55) e AV119–AV123 (L122–126) presentes | Linhas removidas | Complementos declaratórios de S4.6 (`q2703ext[B/C]`, `q2801ext[E/F]`, `q2804[A/C]`): se religados ao PA04, elevariam a incidência de S4.6 para quase toda a população; a regra atual `(AV45 & AV46) \| AV53` é a mais proporcional. Órfãs; sem efeito. |
| AV28, AV102 (L31, L105) presentes | Linhas removidas | `q2703ext[B]` (dimensionamento por critérios técnicos): redundante com o mínimo já usado em S4.2 (`q2703ext[C]` — quantitativo documentado). Órfãs; sem efeito. |
| AV65, AV135 (L68, L138) presentes | Linhas removidas | `q2203ext[B]` (uso da base de configuração em mudanças): prática de maturidade; S5.4 já exige o mínimo (base consolidada A e formalização C). Órfãs; sem efeito. |
| AV68, AV69, AV72, AV138, AV139, AV142 (L71, L72, L75, L141, L142, L145) presentes | Linhas removidas | `q2204ext[B/C/F]` (ANS na resolução, base de conhecimento, causa raiz): alta maturidade; PA05 excluiu corretamente esses itens da situação S5.5. Órfãs; sem efeito. |
| AV43, AV44, AV117, AV118 (L46, L47, L120, L121) presentes | Linhas removidas | `q2706ext[B/C]` (incentivo e monitoramento de capacitação): o mínimo é o plano de capacitação (`q2706ext[A]`, já usado em S4.5). Órfãs; sem efeito. |
| AV60, AV61, AV130, AV131 (L63, L64, L133, L134) presentes | Linhas removidas | `q2501ext[A/B]` (inventário de ativos de informação): cobertura de inventário já existe em S5.3 via `q2203ext[A]`/`q2504ext[A]/[B]`. Órfãs; sem efeito. |

> Nota: as 41 linhas não aparecem nas fórmulas PA01–PA06 nem nas condições de "Motivos do Relatório" (verificação programática). A remoção não altera nenhum resultado de achado e não quebra a validação do executor (as referências restantes continuam íntegras). Regenerar o painel de evidências (`gerar_fonte_ajustes_evidencias_auditoria.py`) após a edição; as análises já produzidas (`analyses*.jsonl`) permanecem como memória de execução.

## B. Coluna `tipo_encaminhamento` (aba "Ações de Verificação"): Recomendação → Determinação

Alteração exclusiva de classificação de saída (o executor lê a coluna apenas como rótulo para relatórios; não participa das lógicas PA01–PA06).

### B.1 Tier 1 — aplicar (37 linhas, 7 situações)

| DE (linhas) | PARA | Motivação/justificativa |
|---|---|---|
| AV11, AV89 (L14, L92) — S2.2 Comitê de TIC não instituído: `Recomendação` | `Determinação` | Acórdão TCE-RJ 44.490/2024-PLEN, item II.1 (estrutura de governança de TI, especialmente Comitê de TI ou instância equivalente, com participação de áreas relevantes, priorização de investimentos e monitoramento por indicadores); TCU 1.411/2014-Plenário, item 9.1.1. |
| AV14–AV17, AV92–AV95 (L17–20, L95–98) — S3.1 processo formal de planejamento: `Recomendação` | `Determinação` | Acórdão TCE-RJ 44.490/2024-PLEN, item II.3 (processo estruturado, com participação das principais secretarias, para elaborar, manter e revisar periodicamente o PDTI); TCU 1.411/2014, item 9.1.6. |
| AV18, AV96 (L21, L99) — S3.2 aprovação formal do plano: `Recomendação` | `Determinação` | Acórdão TCE-RJ 44.490/2024-PLEN, item II.3.5 (aprovação do PDTI pela autoridade máxima); TCU 1.411/2014, item 9.1.6. |
| AV20–AV23, AV98–AV100 (L23–26, L101–103) — S3.5 vínculo plano/orçamento/contratações: `Recomendação` | `Determinação` | TCU 1.411/2014, item 9.1.6.4 (vinculação das ações priorizadas ao orçamento de TI); TCE-RJ 44.490/2024, item II.3.4; Lei 14.133/2021, art. 18, § 1º, I. |
| AV73–AV77, AV143–AV147 (L76–80, L146–150) — S6.1 processo formal/padronizado de contratações: `Recomendação` | `Determinação` | Lei 14.133/2021, art. 11, parágrafo único (governança das contratações) e art. 19, IV (modelos de minutas, TR e contratos padronizados). |
| AV79–AV82, AV149–AV151 (L82–85, L152–154) — S6.3 contratações sem alinhamento ao planejamento/PCA/orçamento: `Recomendação` | `Determinação` | Lei 14.133/2021, art. 18, caput e § 1º, I (fase preparatória; compatibilização com o plano de contratações anual). |
| AV83 (L86) — S6.4 equipe de planejamento da contratação não designada: `Recomendação` | `Determinação` | Lei 14.133/2021, art. 7º (agentes públicos para funções essenciais) e art. 18 (equipe de planejamento da contratação — confirmar o dispositivo exato antes da redação final); referência regulamentar federal: IN SGD/ME 58/2022. |

### B.2 Tier 2 — avaliar pela equipe (14 linhas, 4 situações; recomendação: elevar com cautela)

| DE (linhas) | PARA (proposta) | Motivação/justificativa |
|---|---|---|
| AV07–AV10, AV85–AV88 (L10–13, L88–91) — S2.1 modelo básico de governança: `Recomendação` | `Determinação` (avaliável) | TCE-RJ 44.490/2024, item II.1; redigir objeto objetivo (papéis, responsabilidades, objetivos/indicadores/metas e acompanhamento periódico), sem detalhar ferramentas. |
| AV19, AV97 (L22, L100) — S3.4 plano sem alinhamento institucional: `Recomendação` | `Determinação` (avaliável) | TCU 1.411/2014, itens 9.1.6.1/9.1.6.2; objeto qualitativo — elevar apenas se a redação final permitir verificação objetiva. |
| AV24, AV101 (L27, L104) — S3.6 sem acompanhamento/revisão periódica: `Recomendação` | `Determinação` (avaliável) | TCE-RJ 44.490/2024, item II.3 ("manter e revisar periodicamente"). |
| AV78, AV148 (L81, L151) — S6.2 sem análise prévia da área de TIC: `Recomendação` | Manter `Recomendação` ou `Determinação` (avaliável) | Fundamento mais fraco: IN SGD/ME 94/2022 é norma federal de referência; Notas Técnicas TCE-RJ (ex.: 06/2023) orientam a prática. Se elevada, restringir a órgãos estaduais vinculados ao SETIC/PRODERJ. |

## C. Abas e colunas que NÃO devem ser alteradas (sob a premissa)

| Artefato | Motivo |
|---|---|
| `Procedimentos de Auditoria` — coluna `logica_achado` (PA01–PA06) | Premissa do usuário; qualquer correção de dupla contagem (S2.2/S2.3, S4.1, S5.3/S5.4) exigiria edição aqui e fica fora do escopo. |
| `Ações de Verificação` — `informacao_requerida`, `situacao_inconforme`, `criterio` | Participam da avaliação; alterá-las mudaria o processamento. |
| `Ações de Verificação` — colunas de flag (`acao_exclusiva_auditados`, `auditado_inexistente_e_achado`, `situacao_encontrada_nan_e_achado`, `decodifica_sit_encontrada`) | Todas vazias (comportamento padrão do executor); não há inconsistência a corrigir e preenchê-las alteraria o processamento. |
| `Motivos do Relatório` | Condições de exibição continuam válidas (nenhuma referencia ação órfã); as 26 situações das ações correspondem 1:1 às dos motivos. Sem edição. |
| `Fontes de Informação` e `Variáveis Temporárias` | Sem necessidade; todas as variáveis temporárias permanecem referenciadas por ações mantidas. |
| `encaminhamento`/`pre_encaminhamento` (textos) | Textos já iniciam com verbos imperativos compatíveis com determinação; não precisam de reescrita para a mudança de tipo. |

## D. Efeitos residuais que permanecem por conta da premissa (tratar fora do mapa)

| Efeito | Dado | Tratamento recomendado fora do mapa |
|---|---|---|
| S2.3 aplicada a 17 orgs sem comitê declarado e 7 orgs duplicadas (S2.2+S2.3) | 27 orgs em S2.3 | Nota metodológica no relatório consolidado/matriz de achados; registro de que a insuficiência de evidência não comprova inatividade. |
| S4.1 duplicada com S1.1 para 3 orgs sem área de TIC (FTM, TURISRIO, SÃO JOÃO DA BARRA) | 59 orgs em S4.1 | Registro de que a organização sem área de TIC já é apontada em S1.1. |
| S5.3 e S5.4 compartilham `q2203ext[A]` (95 orgs nas duas) | 97/110 | Nota metodológica; a mesma deficiência (base consolidada ausente) responde por duas situações. |
| S3.5 ≡ S6.3 (mesmos 4 itens; 106 orgs idênticas) | 106/106 | Nota metodológica de "lentes distintas" (Q3 × Q6), antecipando alegação de dupla punição. |

## E. Pós-edição do mapa

1. Re-executar `executa_auditoria.py` (ao menos `--somente-dados` em cópia de teste em `/tmp`) para validar o mapa editado e conferir que os resultados de achado são idênticos aos anteriores (esperado: só muda o campo `tipo_encaminhamento` dos encaminhamentos elevados).
2. Regenerar `painel-avaliacao-evidencias.xlsx` (`gerar_fonte_ajustes_evidencias_auditoria.py`) para que as colunas das ações removidas deixem de ser avaliadas.
3. Regerar matriz de achados e relatórios individuais/consolidado para propagar a nova classificação.
