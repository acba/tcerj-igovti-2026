# Repository Guidelines

## Project Context

This repository stores the digital workpapers for TCE-RJ Fiscalization 18/2026, focused on iGovTI 2026. It is documentation-heavy, with Python automation for questionnaire processing, evidence evaluation, iGovTI calculation, audit execution, chart generation, and report generation.

Work from repository evidence, not filename inference. Read the relevant source before summarizing methodology, scope, criteria, questionnaire logic, findings, or audit conclusions. Treat AI-generated outputs as drafts that require human audit review.

## Project Structure

- `01-Planejamento/`: planning artifacts, preliminary studies, iGovTI methodology, strategy, audit plan, and planning matrix.
- `01-Planejamento/01-Estudos_Preliminares/`: antecedentes, benchmark references, external criteria, and risk analysis.
- `01-Planejamento/02-Metodologia_iGovTI/`: iGovTI 2026 questionnaire, LimeSurvey file, calculation methodology, and YAML index structures.
- `01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/`: structured planning matrix and related planning outputs.
- `02-Execucao/01-Questionario/`: questionnaire responses, adjusted responses, calculation outputs, and collected evidence.
- `02-Execucao/02-Questionario iGovTI 2023/`: 2023 datasets and 2023-2026 comparison outputs.
- `02-Execucao/03-Execucao_Procedimentos/`: audited-organization database, verification/findings map, audit execution outputs, and evidence-evaluation results.
- `02-Execucao/04-Matriz_Achados/`: generated findings matrix and traceability outputs.
- `03-Relatorios/01-Relatorio_Consolidado/`: consolidated report Markdown/DOCX sources.
- `03-Relatorios/02-Relatorios_Individuais_Preliminares/`: individual preliminary report templates and finding fragments.
- `04-Portal_iGovTI/`: portal requirements, currently `PRD.md`.
- `scripts/`: local automation.

## Methodology Sequence

When explaining or changing workflow documentation, keep the methodology in this order:

1. Preliminary studies and audit approach.
2. Planning matrix preparation.
3. iGovTI methodology and index structure creation.
4. Audit procedures matrix / verification map creation.
5. Questionnaire construction and LimeSurvey publication.
6. Formal communication to audited organizations with individualized survey links.
7. Response and attachment collection.
8. Initial response adjustments for rectifications, survey bugs, or data sanitation.
9. Response and evidence evaluation.
10. Post-evidence response adjustments.
11. Statistics, iGovTI indexes, charts, and longitudinal comparison.
12. Audit procedure execution and finding consolidation.
13. Individual preliminary report drafting.
14. Consolidated report drafting.
15. Portal/publication preparation.

`README.md` is the user-facing reference for this sequence. Keep AGENTS.md focused on operational guidance for agents.

## Local Automation

No build system or test runner is currently defined. Use the workspace virtual environment for project scripts:

```bash
scripts/.venv/bin/python <script>
```

Useful inspection commands:

```bash
rg --files -g '!**/.git/**'
find . -maxdepth 3 -type d | sort
rg -n "^## Grupo:|^### q|evidence_text:" 01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md
```

Do not add invented `npm`, `make`, or `pytest` commands unless the required project files are introduced.

### Core Commands

Run the complete report package workflow from the raw LimeSurvey export:

```bash
scripts/.venv/bin/python scripts/gerar_pacote_relatorios_igovti.py \
  --respostas-bruto 02-Execucao/01-Questionario/01-Coleta_LimeSurvey/20260621-respostas-questionario-bruto.xlsx \
  --data-final-preenchimento-comentarios-gestor 06/07/2026 \
  --email-contato-comentarios-gestor auditoriati@tcerj.tc.br \
  --numero-fiscalizacao-comentarios-gestor 18/2026 \
  --nome-fiscalizacao-comentarios-gestor "iGovTI 2026" \
  --output-dir C:/tmp/tcerj-igovti-2026-ultima-versao
```

This applies recorded adjustments, recalculates iGovTI artifacts, executes the audit, generates charts, individual reports, and the consolidated report. The script logs each stage and command to the terminal.

Generate the planning matrix DOCX:

```bash
scripts/.venv/bin/python scripts/gerar_matriz_planejamento.py \
  01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/matriz_planejamento.md
```

Convert the questionnaire Markdown to LimeSurvey LSS:

```bash
scripts/.venv/bin/python scripts/resources/md2lss.py \
  01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md \
  01-Planejamento/02-Metodologia_iGovTI/igovti_2026.lss
```

Download LimeSurvey evidence attachments:

```bash
scripts/.venv/bin/python scripts/coletar_anexos_limesurvey.py
```

Extract evidence ZIPs:

```bash
scripts/.venv/bin/python scripts/extrair_evidencias.py
```

Generate iGovTI 2026 result workbooks:

```bash
scripts/.venv/bin/python scripts/gerar_igovti.py \
  --respostas 02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario.xlsx
```

Regenerate the full iGovTI artifact set:

```bash
scripts/.venv/bin/python scripts/gerar_artefatos_igovti.py \
  --respostas 02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario.xlsx \
  --prefixo 20260621 \
  --output-dir C:/tmp/tcerj-igovti-2026
```

Apply response adjustments:

```bash
scripts/.venv/bin/python scripts/ajustar_respostas_questionario.py \
  --respostas 02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario.xlsx \
  --ajustes 02-Execucao/01-Questionario/02-Ajustes_Respostas/ajustes_respostas_questionario_pos_avaliacao_evidencias.xlsx \
  --output 02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario-pos-avaliacao-evidencias.xlsx
```

Generate the derived evidence-adjustment source used by audit procedures:

```bash
scripts/.venv/bin/python scripts/gerar_fonte_ajustes_evidencias_auditoria.py
```

This creates `02-Execucao/03-Execucao_Procedimentos/99-Avaliacao_Evidencias/painel-avaliacao-evidencias.xlsx`, a wide workbook keyed by `Auditado`, restricted by default to questionnaire items already used in `mapa-verificacao-achados.xlsx`.

Generate the findings matrix DOCX:

```bash
scripts/.venv/bin/python scripts/gerar_matriz_achados.py
```

Run audit procedures and write outputs to `/tmp` for validation:

```bash
scripts/.venv/bin/python scripts/executa_auditoria.py \
  --auditados 02-Execucao/03-Execucao_Procedimentos/01-Insumos/bd_auditados.xlsx \
  --mapa 02-Execucao/03-Execucao_Procedimentos/01-Insumos/mapa-verificacao-achados.xlsx \
  --fontes \
    02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario-pos-avaliacao-evidencias.xlsx \
    02-Execucao/03-Execucao_Procedimentos/99-Avaliacao_Evidencias/painel-avaliacao-evidencias.xlsx \
  --resultado-auditoria-json C:/tmp/tcerj-igovti-2026/02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/resultado_auditoria.json \
  --tabelas-auditoria-xlsx C:/tmp/tcerj-igovti-2026/02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/tabelas_consolidadas_auditoria.xlsx \
  --data-final-preenchimento-comentarios-gestor 06/07/2026 \
  --email-contato-comentarios-gestor auditoriati@tcerj.tc.br \
  --numero-fiscalizacao-comentarios-gestor 18/2026 \
  --nome-fiscalizacao-comentarios-gestor "iGovTI 2026"
```

`resultado_auditoria.json` is compact by default and omits the full list of evaluated actions. Use `--resultado-auditoria-detalhado-json C:/tmp/tcerj-igovti-2026/02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/resultado_auditoria_detalhado.json` only when a detailed debugging trace is required.

The audit CLI validates the map before execution and fails on missing sources/actions/columns, invalid booleans, and malformed finding logic. Use `--somente-dados` for a data-only run, or `--skip-relatorios-procedimentos`, `--skip-anexo-evidencias`, and `--skip-comentarios-gestor` to skip specific accessory outputs.

Generate individual report charts:

```bash
scripts/.venv/bin/python scripts/gerar_graficos_relatorios_consolidado_individuais_igovti.py \
  --auditados FTM \
  --output-root C:/tmp/tcerj-igovti-2026
```

Generate an individual preliminary report:

```bash
scripts/.venv/bin/python scripts/gerar_relatorios_individuais.py \
  --auditados C:/tmp/tcerj-igovti-2026/02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/resultado_auditoria.json \
  --templates 03-Relatorios/02-Relatorios_Individuais_Preliminares/relatorio-individual-preliminar-template.md \
  --context-files 02-Execucao/01-Questionario/04-Resultados_iGovTI/20260621-contexto-relatorios-igovti-2026.xlsx \
  --ajustes-respostas 02-Execucao/01-Questionario/02-Ajustes_Respostas/ajustes_respostas_questionario_pos_avaliacao_evidencias.xlsx \
  --resource-files "C:/tmp/tcerj-igovti-2026/relatorios-individuais/img/**/*" "03-Relatorios/02-Relatorios_Individuais_Preliminares/img/igovti_2026_composicao_infografico_v6.png" \
  --auditados-select FTM \
  --output-dir C:/tmp/tcerj-igovti-2026/relatorios-individuais/FTM \
  --reference-docx scripts/resources/template-base-estilos-sigiloso.docx
```

Generate the consolidated report DOCX:

```bash
scripts/.venv/bin/python scripts/gerar_relatorio_consolidado.py
```

## Evidence Evaluation

Prompt Markdown files under `scripts/avaliacao_evidencias/prompts/` are generated artifacts. Do not edit them directly. Add or change prompts in the YAML catalog, then regenerate the Markdown prompt directory.

The active prompt catalog in this repository is:

```text
scripts/avaliacao_evidencias/prompt_catalogs/igovti_2026_achados_binario_v1.yml
```

To add or alter a prompt in the binary findings set:

1. Edit `scripts/avaliacao_evidencias/prompt_catalogs/igovti_2026_achados_binario_v1.yml`.
2. Add the entry under `prompts` with `arquivo`, `coluna_evidencia`, `itens_avaliaveis`, and, when needed, `criterios_pratica_principal`, `criterios_comuns_itens`, or `criterios_por_item`.
3. Use `criterios_comuns_itens` for criteria shared by several alternatives and `excluir_criterios_comuns_itens` for exceptions.
4. Use `exibir_texto_itens: false` when the model must judge only the listed criteria, not the full questionnaire alternative text.
5. For adoption/detail items such as `q1001ext[A]`, keep item text visible when the selected detail text is itself the assertion to be checked.
6. Mark `gera_achado: true` on entries whose root question gives rise to a finding in `02-Execucao/03-Execucao_Procedimentos/01-Insumos/mapa-verificacao-achados.xlsx`.
7. Keep only items that can be evaluated by evidence. Do not add negative/no-upload items such as `q0101[F]`, `q0102[E]`, or `q0103[G]`.

Regenerate the binary findings prompts:

```bash
scripts/.venv/bin/python -m scripts.avaliacao_evidencias.prompt_catalog_achados build \
  scripts/avaliacao_evidencias/prompt_catalogs/igovti_2026_achados_binario_v1.yml \
  01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md \
  scripts/avaliacao_evidencias/prompts/igovti_2026_achados_binario_v1
```

Validate with `provider fake` before remote AI execution:

```bash
scripts/.venv/bin/python -m scripts.avaliacao_evidencias \
  02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario.xlsx \
  C:/tmp/tcerj-igovti-2026/evidencias_extraidas \
  --questionario 01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md \
  --prompts-dir scripts/avaliacao_evidencias/prompts/igovti_2026_achados_binario_v1 \
  --prompt-version igovti_2026_achados_binario_v1 \
  --only-prompts-present \
  --provider fake \
  --model fake \
  --out-dir C:/tmp/tcerj-igovti-2026/02-Execucao/03-Execucao_Procedimentos/99-Avaliacao_Evidencias/individuais/teste-achados-binario
```

For the binary findings set, run the pipeline with `--only-prompts-present`. Use `--only-achados` to restrict processing to questions whose prompt is marked `gera_achado: true`. Use `--pdf2md` for PDF evidence that should be converted with PyMuPDF4LLM before provider evaluation. Use `--docx2html` for DOCX evidence that should be converted with Mammoth before provider evaluation.

Run the configured parallel evaluators:

```bash
scripts/.venv/bin/python scripts/run_avaliacao_evidencias_v2.py
```

Run configured consolidation judges:

```bash
scripts/.venv/bin/python scripts/run_consolida_avaliacoes_v2.py
```

Aggregate evaluations by questionnaire item:

```bash
scripts/.venv/bin/python scripts/agregar_analyses_por_item.py \
  02-Execucao/03-Execucao_Procedimentos/99-Avaliacao_Evidencias/individuais/analyses*.jsonl \
  --output 02-Execucao/03-Execucao_Procedimentos/99-Avaliacao_Evidencias/consolidado/agregado_avaliacoes_por_item.xlsx
```

### Manager Comments Evidence Reassessment

Use `scripts/avaliar_comentarios_gestor.py` to reassess items previously marked `Não conforme` after the audited organization submits manager comments and optional new PDF/ZIP evidence in the comments survey. The script reuses the evidence-evaluation prompts and produces `analyses*.jsonl` compatible with `scripts.avaliacao_evidencias.consolidacao`.

Generate individual reassessments from the LimeSurvey comments export and extracted attachments:

```bash
scripts/.venv/bin/python scripts/avaliar_comentarios_gestor.py avaliar \
  --respostas-comentarios C:/tmp/tcerj-igovti-2026/02-Execucao/05-Comentarios_Gestor/respostas-comentarios-gestor.xlsx \
  --evidencias-comentarios-root C:/tmp/tcerj-igovti-2026/02-Execucao/05-Comentarios_Gestor/evidencias_extraidas \
  --ajustes-pos-avaliacao-evidencias 02-Execucao/01-Questionario/02-Ajustes_Respostas/ajustes_respostas_questionario_pos_avaliacao_evidencias.xlsx \
  --questionario 01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md \
  --prompts-dir scripts/avaliacao_evidencias/prompts/igovti_2026_achados_binario_v1 \
  --prompt-version igovti_2026_comentarios_gestor_v1 \
  --provider fake \
  --model fake \
  --out-dir C:/tmp/tcerj-igovti-2026/02-Execucao/05-Comentarios_Gestor/99-Reavaliacao_Evidencias/individuais
```

Consolidate those reassessments with the existing judge pipeline:

```bash
scripts/.venv/bin/python -m scripts.avaliacao_evidencias.consolidacao \
  C:/tmp/tcerj-igovti-2026/02-Execucao/05-Comentarios_Gestor/99-Reavaliacao_Evidencias/individuais/analyses*.jsonl \
  --evidencias-root C:/tmp/tcerj-igovti-2026/02-Execucao/05-Comentarios_Gestor/evidencias_extraidas \
  --judge-provider fake \
  --judge-model fake \
  --out-dir C:/tmp/tcerj-igovti-2026/02-Execucao/05-Comentarios_Gestor/99-Reavaliacao_Evidencias/consolidado
```

Generate reverse adjustments from the consolidated reassessment:

```bash
scripts/.venv/bin/python scripts/avaliar_comentarios_gestor.py gerar-ajustes \
  --consolidado C:/tmp/tcerj-igovti-2026/02-Execucao/05-Comentarios_Gestor/99-Reavaliacao_Evidencias/consolidado/consolidated.jsonl \
  --ajustes-pos-avaliacao-evidencias 02-Execucao/01-Questionario/02-Ajustes_Respostas/ajustes_respostas_questionario_pos_avaliacao_evidencias.xlsx \
  --output C:/tmp/tcerj-igovti-2026/02-Execucao/05-Comentarios_Gestor/99-Reavaliacao_Evidencias/ajustes_respostas_questionario_pos_comentarios_gestor.xlsx
```

Apply reverse adjustments over the post-evidence-adjusted response base:

```bash
scripts/.venv/bin/python scripts/ajustar_respostas_questionario.py \
  --respostas 02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario-pos-avaliacao-evidencias.xlsx \
  --ajustes C:/tmp/tcerj-igovti-2026/02-Execucao/05-Comentarios_Gestor/99-Reavaliacao_Evidencias/ajustes_respostas_questionario_pos_comentarios_gestor.xlsx \
  --output C:/tmp/tcerj-igovti-2026/02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario-pos-comentarios-gestor.xlsx
```

The reverse-adjustment XLSX intentionally includes only items whose consolidated reassessment is `Conforme`; each row restores the original `Resposta afirmada` through the `Resposta ajustada` column. Treat the generated adjustments as a draft subject to audit review before using them as the definitive response base. On Linux/macOS, replace `C:/tmp/tcerj-igovti-2026` with `/tmp/tcerj-igovti-2026`.

The orchestrators support Gemini key rotation when `GEMINI_API_KEY` contains multiple comma-separated keys. On 429, they rotate keys, pause only when all keys are exhausted, and avoid recording rate-limit failures for items that can be retried after the pause.

See `scripts/avaliacao_evidencias/README.md` for deeper pipeline details.

## Output Policy

Write generated artifacts to `C:/tmp/tcerj-igovti-2026` on Windows or `/tmp/tcerj-igovti-2026` on Linux/macOS unless the user explicitly requests a repository destination. This keeps validation runs separate from auditable repository artifacts.

When a script creates DOCX, XLSX, JSON, LSS, ZIP, or chart outputs, report the generated paths in the final response. For report generation, validate that there are no missing-resource warnings and that expected media files are embedded when the tooling exposes that information.

## Coding and Documentation Style

Prefer Portuguese (Brazil) for project documentation and audit narrative. Preserve directory prefixes such as `01-Planejamento`, `02-Execucao`, and `03-Relatorios`.

For questionnaire edits, preserve identifiers such as `g0100`, `q0101`, `evidence_text`, `visible_if`, and LimeSurvey response codes in `.md` and `.lss` files.

Keep Markdown concise and structured. Do not reformat entire `.docx` exports, `.lss` XML, CSVs, generated PDFs, or large workbooks unless explicitly required.

For Python changes, follow the surrounding style. Prefer existing helper modules under `scripts/resources/` and `scripts/avaliacao_evidencias/` instead of introducing new ad hoc parsing logic.

## Testing and Validation

There are no automated tests yet. Choose validation based on the changed artifact:

- Documentation: verify links, paths, headings, command consistency, and alignment with source documents.
- Questionnaire changes: compare `.md` and `.lss`; validate LimeSurvey import/export before treating the change as complete.
- Prompt catalog changes: regenerate prompts and run the `provider fake` validation command.
- iGovTI calculation changes: run `gerar_artefatos_igovti.py` to the temporary package directory and inspect the generated XLSX/JSON paths.
- Audit execution changes: run `executa_auditoria.py` to the temporary package directory with the current audit inputs.
- Report changes: regenerate the target report and check for missing resources or conversion warnings.

## Agent-Specific Instructions

- Answer from repository evidence, not filename inference.
- Read the relevant file before summarizing methodology, scope, criteria, questionnaire logic, or audit conclusions.
- Treat AI-generated outputs as drafts requiring human audit review.
- Do not suggest git commands unless the user explicitly asks for git help.
- Do not edit generated prompt Markdown directly; edit the YAML catalog and regenerate.
- Do not overwrite user changes or unrelated generated artifacts.
