# Proposta de ajuste do mapa de verificação de achados

**Fiscalização TCE-RJ nº 18/2026 — iGovTI 2026**

| Campo | Informação |
|---|---|
| Objeto | `02-Execucao/03-Execucao_Procedimentos/01-Insumos/mapa-verificacao-achados.xlsx` |
| Premissa | As fórmulas `logica_achado` (PA01–PA06, aba "Procedimentos de Auditoria") **não serão alteradas** |
| Data da proposta | 14/08/2026 |
| Análise realizada por | **DeepSeek Flash** (modelo `opencode-go/deepseek-v4-flash`) |
| Natureza | Proposta técnica sujeita à validação e deliberação da Equipe de Auditoria |

Números de linha = linhas do Excel na aba "Ações de Verificação" (linha 1 = cabeçalho de exibição; linha 2 = cabeçalho de campos; dados a partir da linha 3).

---

## 1. Remoções na aba "Ações de Verificação" (41 linhas órfãs — nenhum efeito no processamento)

As 41 ações abaixo não constam de nenhuma lógica PA01–PA06 nem de nenhuma condição de "Motivos do Relatório" (verificação programática) e não aparecem em nenhum resultado (verificado no `resultado_auditoria.json` pós-comentários do gestor). A remoção não altera nenhum resultado de achado e não quebra a validação do executor (`executa_auditoria.py` lê as ações pelo `id`, não pela posição da linha).

| DE | PARA | Motivação/justificativa |
|---|---|---|
| AV26 (L29) presente | Linha removida | Ação criada para condicionar S4.1 a organização com área de TIC (`q0101 ≠ F`), mas nunca religada ao PA04. Religar exigiria alterar PA04 — vedado pela premissa. Sem efeito computacional; remove ruído de rastreabilidade. |
| AV113, AV114, AV115 (L116–118) presentes | Linhas removidas | Avaliações de evidência de `q2705ext[B/C/D]` sem efeito: enquanto `AV116` (q2706ext[A]) dispara S4.5, a rejeição de evidência de q2705 não gera situação (assimetria só corrigível alterando PA04 — vedado). Sem efeito computacional hoje. |
| AV30, AV32, AV104, AV106 (L33, L35, L107, L109) presentes | Linhas removidas | Cargos *efetivos* de TI/SI (`q2708[A]` e `[C]`): PA04 usa corretamente apenas `[B]/[D]` (funções formalmente atribuídas). Exigir cargos efetivos esbarra em reserva legal e não é mínimo aceitável; as ações são órfãs. |
| AV35, AV37, AV109, AV111 (L38, L40, L112, L114) presentes | Linhas removidas | `q2701ext[C]`/`q2702ext[C]` (competências e habilidades no perfil): item mais exigente que o "A" já utilizado em S4.4 (responsabilidades definidas, documentadas e publicadas). Órfãs; sem efeito. |
| AV47, AV48, AV49, AV50, AV51, AV52 (L50–55) e AV119–AV123 (L122–126) presentes | Linhas removidas | Complementos declaratórios de S4.6 (`q2703ext[B/C]`, `q2801ext[E/F]`, `q2804[A/C]`): se religados ao PA04, elevariam a incidência de S4.6 para quase toda a população; a regra atual `(AV45 & AV46) \| AV53` é a mais proporcional. Órfãs; sem efeito. |
| AV28, AV102 (L31, L105) presentes | Linhas removidas | `q2703ext[B]` (dimensionamento por critérios técnicos): redundante com o mínimo já usado em S4.2 (`q2703ext[C]` — quantitativo documentado). Órfãs; sem efeito. |
| AV65, AV135 (L68, L138) presentes | Linhas removidas | `q2203ext[B]` (uso da base de configuração em mudanças): prática de maturidade; S5.4 já exige o mínimo (base consolidada A e formalização C). Órfãs; sem efeito. |
| AV68, AV69, AV72, AV138, AV139, AV142 (L71, L72, L75, L141, L142, L145) presentes | Linhas removidas | `q2204ext[B/C/F]` (ANS na resolução, base de conhecimento, causa raiz): alta maturidade; PA05 excluiu corretamente esses itens da situação S5.5. Órfãs; sem efeito. |
| AV43, AV44, AV117, AV118 (L46, L47, L120, L121) presentes | Linhas removidas | `q2706ext[B/C]` (incentivo e monitoramento de capacitação): o mínimo é o plano de capacitação (`q2706ext[A]`, já usado em S4.5). Órfãs; sem efeito. |
| AV60, AV61, AV130, AV131 (L63, L64, L133, L134) presentes | Linhas removidas | `q2501ext[A/B]` (inventário de ativos de informação): cobertura de inventário já existe em S5.3 via `q2203ext[A]`/`q2504ext[A]/[B]`. Órfãs; sem efeito. |

---

## 2. Coluna `tipo_encaminhamento` (aba "Ações de Verificação"): Recomendação → Determinação

Alteração exclusiva de classificação de saída: o executor lê a coluna apenas como rótulo para relatórios; não participa das lógicas PA01–PA06. Os textos de `encaminhamento` já iniciam com verbos imperativos compatíveis com determinação e não precisam de reescrita.

### 2.1 Tier 1 — aplicar (37 linhas, 7 situações)

| DE (linhas) | PARA | Motivação/justificativa |
|---|---|---|
| AV11, AV89 (L14, L92) — S2.2 Comitê de TIC não instituído: `Recomendação` | `Determinação` | Acórdão TCE-RJ 44.490/2024-PLEN, item II.1 (estrutura de governança de TI, especialmente Comitê de TI ou instância equivalente, com participação de áreas relevantes, priorização de investimentos e monitoramento por indicadores); TCU 1.411/2014-Plenário, item 9.1.1. |
| AV14–AV17, AV92–AV95 (L17–20, L95–98) — S3.1 processo formal de planejamento: `Recomendação` | `Determinação` | Acórdão TCE-RJ 44.490/2024-PLEN, item II.3 (processo estruturado, com participação das principais secretarias, para elaborar, manter e revisar periodicamente o PDTI); TCU 1.411/2014, item 9.1.6. |
| AV18, AV96 (L21, L99) — S3.2 aprovação formal do plano: `Recomendação` | `Determinação` | Acórdão TCE-RJ 44.490/2024-PLEN, item II.3.5 (aprovação do PDTI pela autoridade máxima); TCU 1.411/2014, item 9.1.6. |
| AV20–AV23, AV98–AV100 (L23–26, L101–103) — S3.5 vínculo plano/orçamento/contratações: `Recomendação` | `Determinação` | TCU 1.411/2014, item 9.1.6.4 (vinculação das ações priorizadas ao orçamento de TI); TCE-RJ 44.490/2024, item II.3.4; Lei 14.133/2021, art. 18, § 1º, I. |
| AV73–AV77, AV143–AV147 (L76–80, L146–150) — S6.1 processo formal/padronizado de contratações: `Recomendação` | `Determinação` | Lei 14.133/2021, art. 11, parágrafo único (governança das contratações) e art. 19, IV (modelos de minutas, TR e contratos padronizados). |
| AV79–AV82, AV149–AV151 (L82–85, L152–154) — S6.3 contratações sem alinhamento ao planejamento/PCA/orçamento: `Recomendação` | `Determinação` | Lei 14.133/2021, art. 18, caput e § 1º, I (fase preparatória; compatibilização com o plano de contratações anual). |
| AV83 (L86) — S6.4 equipe de planejamento da contratação não designada: `Recomendação` | `Determinação` | Lei 14.133/2021, art. 7º (agentes públicos para funções essenciais) e art. 18 (equipe de planejamento da contratação — confirmar o dispositivo exato antes da redação final); referência regulamentar federal: IN SGD/ME 58/2022. |

### 2.2 Tier 2 — avaliar pela equipe (14 linhas, 4 situações)

| DE (linhas) | PARA (proposta) | Motivação/justificativa |
|---|---|---|
| AV07–AV10, AV85–AV88 (L10–13, L88–91) — S2.1 modelo básico de governança: `Recomendação` | `Determinação` (avaliável) | TCE-RJ 44.490/2024, item II.1; redigir objeto objetivo (papéis, responsabilidades, objetivos/indicadores/metas e acompanhamento periódico), sem detalhar ferramentas. |
| AV19, AV97 (L22, L100) — S3.4 plano sem alinhamento institucional: `Recomendação` | `Determinação` (avaliável) | TCU 1.411/2014, itens 9.1.6.1/9.1.6.2; objeto qualitativo — elevar apenas se a redação final permitir verificação objetiva. |
| AV24, AV101 (L27, L104) — S3.6 sem acompanhamento/revisão periódica: `Recomendação` | `Determinação` (avaliável) | TCE-RJ 44.490/2024, item II.3 ("manter e revisar periodicamente"). |
| AV78, AV148 (L81, L151) — S6.2 sem análise prévia da área de TIC: `Recomendação` | Manter `Recomendação` ou `Determinação` (avaliável) | Fundamento mais fraco: IN SGD/ME 94/2022 é norma federal de referência; Notas Técnicas TCE-RJ (ex.: 06/2023) orientam a prática. Se elevada, restringir a órgãos estaduais vinculados ao SETIC/PRODERJ. |

---

## 3. Abas e colunas que NÃO devem ser alteradas (sob a premissa)

| Artefato | Motivo |
|---|---|
| `Procedimentos de Auditoria` — coluna `logica_achado` (PA01–PA06) | Premissa do usuário; qualquer correção de dupla contagem (S2.2/S2.3, S4.1, S5.3/S5.4) exigiria edição aqui e fica fora do escopo. |
| `Ações de Verificação` — `informacao_requerida`, `situacao_inconforme`, `criterio` | Participam da avaliação; alterá-las mudaria o processamento. |
| `Ações de Verificação` — colunas de flag (`acao_exclusiva_auditados`, `auditado_inexistente_e_achado`, `situacao_encontrada_nan_e_achado`, `decodifica_sit_encontrada`) | Todas vazias (comportamento padrão do executor); não há inconsistência a corrigir e preenchê-las alteraria o processamento. |
| `Motivos do Relatório` | Condições de exibição continuam válidas (nenhuma referencia ação órfã); as 26 situações das ações correspondem 1:1 às dos motivos. Sem edição. |
| `Fontes de Informação` e `Variáveis Temporárias` | Sem necessidade; todas as variáveis temporárias permanecem referenciadas por ações mantidas. |
| `encaminhamento`/`pre_encaminhamento` (textos) | Textos já iniciam com verbos imperativos compatíveis com determinação; não precisam de reescrita para a mudança de tipo. |

---

## 4. Efeitos residuais que permanecem por conta da premissa (tratar fora do mapa)

| Efeito | Dado | Tratamento recomendado fora do mapa |
|---|---|---|
| S2.3 aplicada a 17 orgs sem comitê declarado e 7 orgs duplicadas (S2.2+S2.3) | 27 orgs em S2.3 | Nota metodológica no relatório consolidado/matriz de achados; registro de que a insuficiência de evidência não comprova inatividade. |
| S4.1 duplicada com S1.1 para 3 orgs sem área de TIC (FTM, TURISRIO, SÃO JOÃO DA BARRA) | 59 orgs em S4.1 | Registro de que a organização sem área de TIC já é apontada em S1.1. |
| S5.3 e S5.4 compartilham `q2203ext[A]` (95 orgs nas duas) | 97/110 | Nota metodológica; a mesma deficiência (base consolidada ausente) responde por duas situações. |
| S3.5 ≡ S6.3 (mesmos 4 itens; 106 orgs idênticas) | 106/106 | Nota metodológica de "lentes distintas" (Q3 × Q6), antecipando alegação de dupla punição. |

---

## 5. Pós-edição do mapa

1. Re-executar `executa_auditoria.py` (ao menos `--somente-dados` em cópia de teste em `/tmp`) para validar o mapa editado e conferir que os resultados de achado são idênticos aos anteriores (esperado: só muda o campo `tipo_encaminhamento` dos encaminhamentos elevados).
2. Regenerar `painel-avaliacao-evidencias.xlsx` (`gerar_fonte_ajustes_evidencias_auditoria.py`) para que as colunas das ações removidas deixem de ser avaliadas.
3. Regerar matriz de achados e relatórios individuais/consolidado para propagar a nova classificação.

---

*Proposta gerada por DeepSeek Flash como subsídio técnico; todas as alterações dependem de validação e deliberação da Equipe de Auditoria antes de qualquer edição no artefato de produção.*
