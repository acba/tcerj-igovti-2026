# Repository Guidelines

## Project Structure & Module Organization

This repository stores digital workpapers for TCE-RJ Fiscalization 18/2026, focused on iGovTI 2026. It is documentation-heavy, with Python automation for audit execution, chart generation, and report generation.

- `01-Planejamento/`: planning artifacts, methodology, survey files, strategy, audit plan, and planning matrix.
- `01-Planejamento/02-Metodologia_iGovTI/`: core iGovTI questionnaire in `.md`, `.lss`, `.docx`, and `.pdf`.
- `01-Planejamento/01-Estudos_Preliminares/Referencias_Externas/`: benchmark materials from TCU, TCE-PE, TCE-RJ, TCE-RS, and IEGM.
- `02-Execucao/`: reserved for responses, collected evidence, audit tests, preliminary findings, and findings matrix.
- `03-Relatorios/`: reserved for consolidated and individual reports.
- `04-Portal_iGovTI/`: portal requirements, currently `PRD.md`.
- `scripts/`: local automation, including generation of consolidated and individual iGovTI charts.

## Build, Test, and Development Commands / Local Automation

No build system or test runner is currently defined. Useful inspection commands:

```bash
rg --files -g '!**/.git/**'
find . -maxdepth 3 -type d | sort
rg -n "^## Grupo:|^### q|evidence_text:" 01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md
```

### Automation Scripts

Utility scripts are stored under `scripts/`. Always run them using the workspace virtual environment:

*   **`coletar_anexos_limesurvey.py`:** Downloads all evidence attachments from LimeSurvey using the session cookies in the script.
    ```bash
    python3 scripts/coletar_anexos_limesurvey.py
    ```
*   **`extrair_evidencias.py`:** Unpacks evidence ZIPs to `/tmp/tcerj-igovti-2026/evidencias_extraidas`.
    ```bash
    python3 scripts/extrair_evidencias.py
    ```
*   **`gerar_igovti.py`:** Generates the iGovTI 2026 result workbooks from the questionnaire responses and the two YAML index structures (official and comparable). By default it uses `02-Execucao/01-Questionario/20260621-respostas-questionario.xlsx` and maps LimeSurvey response IDs to organization names via `urls_anexos_limesurvey_consolidado.xlsx`.
    ```bash
    scripts/.venv/bin/python scripts/gerar_igovti.py
    ```
*   **`atualizar_conjunto_igovti.py`:** Orchestrates the full regeneration of the iGovTI 2026 artifact set. It runs `gerar_igovti.py`, then `consolidar_dados_comparativos_igovti.py`, then `calcular_contexto_relatorios_igovti.py`, producing the result workbooks, the 2023-2026 comparison workbook, the report context workbook, and the calculation record JSON. Use `--prefixo` to version the outputs and `--output-dir` to write to `/tmp` for validation before committing.
    ```bash
    scripts/.venv/bin/python scripts/atualizar_conjunto_igovti.py \
      --respostas 02-Execucao/01-Questionario/20260621-respostas-questionario.xlsx \
      --prefixo 20260621 \
      --output-dir /tmp/tcerj-igovti-2026
    ```
*   **`gerar_matriz_planejamento.py`:** Converts the matrix markdown template into DOCX.
    ```bash
    python3 scripts/gerar_matriz_planejamento.py 01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/matriz_planejamento.md
    ```
*   **`gerar_matriz_achados.py`:** Generates the findings matrix Word document.
    ```bash
    python3 scripts/gerar_matriz_achados.py
    ```
*   **`avaliar_evidencias_matriz_planejamento.py` / `avaliacao_evidencias`:** Runs the AI evidence evaluation pipeline. See [scripts/avaliacao_evidencias/README.md](file:///home/acba/workspace/fiscalizacoes/tcerj-igovti-2026/scripts/avaliacao_evidencias/README.md) for full commands.
*   **`run_avaliacao_evidencias_v2.py`:** Python orchestrator that runs several `avaliacao_evidencias` pipelines in parallel (one per model/provider) and shows stacked `rich.Progress` bars in the terminal with per-model progress, ETA, and a final summary table. Replaces the legacy `scripts/run_avaliacao_evidencias.sh`. Configure the list of active models at the top of the script (`MODELS = [...]`, set `enabled: True/False`). Supports automatic Gemini key rotation on 429: when `GEMINI_API_KEY` contains multiple comma-separated keys, the pipeline rotates to the next available key immediately on 429, and if all keys are exhausted simultaneously, it pauses by the smallest `Retry-After` and shows an alert in the terminal instead of recording errors. Run with:
    ```bash
    scripts/.venv/bin/python scripts/run_avaliacao_evidencias_v2.py
    ```
*   **`run_consolida_avaliacoes_v2.py`:** Python orchestrator for the judge-based consolidation (`consolidacao.py`). Runs one or more judges in parallel over all `analyses*.jsonl` and shows stacked `rich.Progress` bars per judge. Replaces the legacy `scripts/run_consolida_avaliacoes.sh`. Supports the same Gemini key rotation and pause-on-exhaustion behavior as the evaluation orchestrator. The consolidated record includes `started_at`, `finished_at`, `duration_seconds`, `reasoning_effort`, and (with `--store-prompts`) `prompt_payload`, in addition to the consolidation-specific fields (`opinion_count`, `opinion_sources`, `opiniao_auditoria`, `evidence_path`, `evidence_hash`). Configure the list of active judges at the top of the script (`JUDGES = [...]`, set `enabled: True/False`). Run with:
    ```bash
    scripts/.venv/bin/python scripts/run_consolida_avaliacoes_v2.py
    ```
*   **`agregar_analyses_por_item.py`:** Consolidates the conclusions stored in one or more evidence-evaluation JSONL files (`analyses*.jsonl`) by questionnaire item (`q0101`, `q2101`, etc.). It counts `conforme`, `nao_conforme`, `inconclusivo`, and `erro`, selects up to two representative evaluations with their justifications, and creates an XLSX with summary, traceability, and metadata sheets. Use `--referencia` to include only records produced by a specific model; the option may be repeated to combine models.
    ```powershell
    $analyses = Get-ChildItem `
      "02-Execucao\03-Execucao_Procedimentos\avaliacao_evidencias" `
      -Recurse -Filter "analyses*.jsonl" -File |
      Select-Object -ExpandProperty FullName

    .\scripts\.venv\Scripts\python.exe scripts\agregar_analyses_por_item.py `
      @analyses `
      --referencia "gemini-3.1-flash-lite" `
      --output "02-Execucao\03-Execucao_Procedimentos\avaliacao_evidencias\consolidado\agregado_avaliacoes_por_item_gemini-3.1-flash-lite.xlsx"
    ```
*   **`ajustar_respostas_questionario.py`:** Applies "Não Conforme" adjustments to the questionnaire responses. Replaces affirmative responses with blanks/No or 'Não adota' on evaluated items, based on the XLSX of adjustments. The auditor's review overrides the judge's score.
    ```bash
    scripts/.venv/bin/python scripts/ajustar_respostas_questionario.py \
      --respostas 02-Execucao/01-Questionario/20260621-respostas-questionario.xlsx \
      --ajustes ajustes_respostas_questionario_pos_avaliacao_evidencias.xlsx
    ```

Do not add invented `npm`, `make`, or `pytest` commands unless the required project files are introduced.

## Evidence Evaluation Prompts

Prompt Markdown files under `scripts/avaliacao_evidencias/prompts/` are generated artifacts. Do not edit them directly. Add or change evidence-evaluation prompts in the YAML catalog, then regenerate the Markdown prompt directory.

There are two prompt catalog formats:

- Full conservative catalog: `scripts/avaliacao_evidencias/prompt_catalogs/igovti_2026_conservador_v2.yml`, generated with `scripts.avaliacao_evidencias.prompt_catalog`.
- Binary findings catalog: `scripts/avaliacao_evidencias/prompt_catalogs/igovti_2026_achados_binario_v1.yml`, generated with `scripts.avaliacao_evidencias.prompt_catalog_achados`.

To add or alter a prompt in the binary findings set:

1. Edit `scripts/avaliacao_evidencias/prompt_catalogs/igovti_2026_achados_binario_v1.yml`.
2. Add the entry under `prompts` with `arquivo`, `coluna_evidencia`, `itens_avaliaveis`, and, when needed, `criterios_pratica_principal`, `criterios_comuns_itens`, or `criterios_por_item`.
   - Use `criterios_comuns_itens` for criteria shared by several alternatives and `excluir_criterios_comuns_itens` for exceptions.
   - Use `exibir_texto_itens: false` when the model must judge only the listed criteria, not the full questionnaire alternative text. The generated prompt records this choice and the pipeline masks `itens_afirmados[].texto` before calling the provider.
   - For adoption/detail items such as `q1001ext[A]`, keep item text visible when the selected detail text is itself the assertion to be checked.
   - Mark `gera_achado: true` on entries whose root question gives rise to a finding in `02-Execucao/03-Execucao_Procedimentos/mapa-verificacao-achados.xlsx`. The pipeline reads this attribute directly from the YAML catalog via `--catalog` (it does **not** alter the prompt Markdown, so existing `prompt_hash` checkpoints remain valid), records `gera_achado` in each analyses JSONL record, and the `--only-achados` flag filters to these questions.
3. Keep only items that can be evaluated by evidence. Do not add negative/no-upload items such as `q0101[F]`, `q0102[E]`, or `q0103[G]`.
4. Regenerate the Markdown prompts:
   ```bash
   scripts/.venv/bin/python -m scripts.avaliacao_evidencias.prompt_catalog_achados build \
     scripts/avaliacao_evidencias/prompt_catalogs/igovti_2026_achados_binario_v1.yml \
     01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md \
     scripts/avaliacao_evidencias/prompts/igovti_2026_achados_binario_v1
   ```
5. Validate with `provider fake` before remote IA execution.

For the binary findings set, run the pipeline with `--only-prompts-present`. This processes only columns covered by the prompt directory and records `nao_conforme` when an evaluable affirmed item has no attached evidence.
Use `--only-achados` to further restrict processing to columns whose prompt is marked `gera_achado: sim` (questions that give rise to a finding in the verification map). It implies the `--only-prompts-present` behavior, records `gera_achado: true` in each analyses JSONL record, and is the recommended mode when the goal is to evaluate only evidence relevant to findings.
The default incremental JSONL name is `analyses_<provider>_<model>.jsonl` inside `--out-dir`; pass `--out-file analyses.jsonl` or another name/path when a fixed output filename is required.
Use `--pdf2md` when PDF evidence should be converted with PyMuPDF4LLM into Markdown plus extracted images before provider evaluation.
Use `--docx2html` when DOCX evidence should be converted with Mammoth into HTML plus extracted images before provider evaluation.

The consolidation judge (`scripts.avaliacao_evidencias.consolidacao`) accepts `--only-achados` (plus `--catalog` or `--prompts-dir`) to consolidate only groups whose root question gives rise to a finding. The achados set is derived primarily from the `--catalog` YAML (`gera_achado` attribute), or, in its absence, from `--prompts-dir` markdown markers, or finally from the `gera_achado` field of the analyses records. The consolidated record also carries a `gera_achado` field for traceability.
The Python orchestrators (`run_avaliacao_evidencias_v2.py`, `run_consolida_avaliacoes_v2.py`) pass `--only-achados` when a model/judge config sets `only_achados: true` or when the environment variable `ONLY_ACHADOS=1` is set.

```bash
scripts/.venv/bin/python -m scripts.avaliacao_evidencias \
  02-Execucao/01-Questionario/20260621-respostas-questionario.xlsx \
  /tmp/tcerj-igovti-2026/evidencias_extraidas \
  --questionario 01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md \
  --prompts-dir scripts/avaliacao_evidencias/prompts/igovti_2026_achados_binario_v1 \
  --prompt-version igovti_2026_achados_binario_v1 \
  --only-prompts-present \
  --provider fake \
  --model fake \
  --out-dir /tmp/tcerj-igovti-2026/avaliacao_evidencias/teste-achados-binario
```

## Parallel Multi-Model Orchestration and Key Rotation

For running several models (or judges) in parallel with real-time progress visibility, use the Python orchestrators instead of the legacy `run_avaliacao_evidencias.sh` / `run_consolida_avaliacoes.sh` shell scripts.

*   **Evaluation:** `scripts/.venv/bin/python scripts/run_avaliacao_evidencias_v2.py` — launches one `avaliacao_evidencias` subprocess per active model. Each model gets a stacked `rich.Progress` bar showing `provider/model`, progress, percentage, completed/total, errors (`✗`), skipped (`⏭`), elapsed time, ETA, and status icon. Active models are configured at the top of the script (`MODELS = [...]`, set `enabled: True/False`).
*   **Consolidation:** `scripts/.venv/bin/python scripts/run_consolida_avaliacoes_v2.py` — same pattern for judges. Active judges are configured at the top (`JUDGES = [...]`).

Both orchestrators parse the JSON-line progress events emitted by the underlying Python modules (`pipeline.py` and `consolidacao.py`) to update the bars in real time, and emit a summary `rich.Table` at the end. `Ctrl+C` sends `terminate()` to all subprocesses and prints a partial summary.

**Automatic Gemini key rotation on 429:** when the `GEMINI_API_KEY` environment variable contains multiple comma-separated keys (e.g. `GEMINI_API_KEY="key1,key2,key3"`), both the evaluation pipeline and the consolidation judge rotate to the next available key **immediately on the first 429** `RESOURCE_EXHAUSTED` response — no legacy 30/60/120s retry on the same key. The `retryDelay` parsed from the Gemini error response marks each key as exhausted for that duration. Each rotation emits a `gemini_key_rotation` event (logged in real time with `from_key`, `reason`, `retry_after_seconds`, `available_keys`), and the final result record carries a `key_rotations` trace. Abandoning a key emits `gemini_key_abandoned`. If **all** keys are exhausted simultaneously, the pipeline pauses for the smallest remaining `Retry-After`, logs an `all_keys_exhausted` event, and the orchestrator shows a yellow alert (`⚠ ALERTA: Todas as chaves gemini exauridas — pausado por 48s [gemini/gemini-3.1-flash-lite]`) in the terminal. The same item is reprocessed after the pause — no rate-limit errors are recorded. After 5 consecutive 429 responses from the same key, that key is abandoned and the remaining keys continue to be tried. This behavior applies to both `consolidacao.py` and `pipeline.py` and is observed by both orchestrators.

## Running the Audit by CLI

Use the local virtual environment and CLI. Write generated artifacts to `/tmp` unless the user explicitly requests a repository destination.

```bash
cd /home/acba/workspace/fiscalizacoes/tcerj-igovti-2026

scripts/.venv/bin/python scripts/executa_auditoria.py \
  --auditados 02-Execucao/03-Execucao_Procedimentos/bd_auditados.xlsx \
  --mapa 02-Execucao/03-Execucao_Procedimentos/mapa-verificacao-achados.xlsx \
  --fontes 02-Execucao/01-Questionario/20260621-respostas-questionario.xlsx \
  --output-json /tmp/tcerj-igovti-2026/auditoria/resultado_auditoria.json \
  --output-xlsx /tmp/tcerj-igovti-2026/auditoria/tabelas_consolidadas_auditoria.xlsx
```

The audit inputs are the audited-organizations database, the verification/findings map, and every source workbook required by the `Fontes de Informação` sheet. When that sheet declares more than one source file, pass all of them after `--fontes`. Confirm that the CLI finishes without missing-source errors before using the JSON to generate reports.

## Generating an Individual Preliminary Report

Recalculate the statistical context and consolidate the longitudinal comparison whenever the questionnaire responses or either comparable index changes:

```bash
cd /home/acba/workspace/fiscalizacoes/tcerj-igovti-2026

python3 scripts/consolidar_dados_comparativos_igovti.py
python3 scripts/calcular_contexto_relatorios_igovti.py
```

The first command generates the auditable workbook `02-Execucao/02-Questionario iGovTI 2023/20260621-comparacao-iGovTI-2023-2026.xlsx`. The second generates the report context workbook and a JSON calculation record in `02-Execucao/01-Questionario/`. Pass alternative source and output paths through the scripts' command-line arguments when processing a later data version.

First generate the common charts and the charts for the selected organizations. `--auditados` accepts one or more organization identifiers; when omitted, charts are generated for all organizations. Common charts are always regenerated.

```bash
cd /home/acba/workspace/fiscalizacoes/tcerj-igovti-2026

python3 scripts/gerar_graficos_relatorios_igovti.py \
  --auditados FTM \
  --output-root /tmp/tcerj-igovti-2026
```

The Markdown template references images only by filename. The Argos CLI automatically resolves wildcards and flattens all resource files into a temporary directory internally. Reference the resource files directly, including glob patterns:

```bash
cd /home/acba/workspace/fiscalizacoes/tcerj-igovti-2026

scripts/.venv/bin/python scripts/gerar_relatorios_individuais.py \
  --auditados /tmp/tcerj-igovti-2026/auditoria/resultado_auditoria.json \
  --templates 03-Relatorios/02-Relatorios_Individuais_Preliminares/relatorio-individual-preliminar-template.md \
  --context-files 02-Execucao/01-Questionario/20260621-contexto-relatorios-igovti-2026.xlsx \
  --resource-files "/tmp/tcerj-igovti-2026/relatorios-individuais/img/**/*" "03-Relatorios/02-Relatorios_Individuais_Preliminares/img/igovti_2026_composicao_infografico_v6.png" \
  --auditados-select FTM \
  --output-dir /tmp/tcerj-igovti-2026/relatorios-individuais/FTM \
  --reference-docx scripts/resources/template-base-estilos-sigiloso.docx
```

If the audit was not rerun, the current repository result may be used instead of the temporary JSON: `02-Execucao/03-Execucao_Procedimentos/resultado_auditoria.json`. Replace `FTM` consistently in the `--auditados-select` and output directory for another organization. Validate that the final DOCX contains embedded media and that the Argos output has no `Could not fetch resource` warnings.

## Generating the Consolidated Report

Generate the consolidated report Word document (`.docx`) from the Markdown file using the local virtual environment `scripts/.venv`. The script automatically handles chart generation, copies and flattens all context images in a temporary directory (cleaning up afterwards so that no `.png` files are created in the docx folder), processes Markdown syntax, references, page breaks, and applies Word table styles.

```bash
cd /home/acba/workspace/fiscalizacoes/tcerj-igovti-2026

scripts/.venv/bin/python scripts/gerar_relatorio_consolidado.py
```

You can optionally pass custom input/output files (defaults are `03-Relatorios/01-Relatorio_Consolidado/Relatório_altaresolucao_novo.md` and `.docx`), custom context variables via `--context-vars key=value`, a context JSON file using `--context-json`, or custom resource paths/wildcards using `--resource-files`. For example:

```bash
scripts/.venv/bin/python scripts/gerar_relatorio_consolidado.py \
  caminho/do/relatorio.md \
  --output caminho/do/resultado.docx \
  --resource-files "/tmp/tcerj-igovti-2026/relatorios-individuais/img/**/*" "outras/imagens/*.png"
```



## Coding Style & Naming Conventions

Prefer Portuguese (Brazil) for project documentation. Preserve existing directory prefixes such as `01-Planejamento`, `02-Execucao`, and `03-Relatorios`. For questionnaire edits, preserve identifiers like `g0100`, `q0101`, `evidence_text`, `visible_if`, and LimeSurvey response codes in `.lss` files.

Keep Markdown concise and structured. Do not reformat entire `.docx` exports, `.lss` XML, CSVs, or generated PDFs unless explicitly required.

## Testing Guidelines

There are no automated tests yet. For documentation changes, verify links, paths, headings, and consistency with source documents. For questionnaire changes, compare the `.md` and `.lss` versions and validate LimeSurvey import/export before treating the change as complete.

## Commit & Pull Request Guidelines

No repository-specific commit convention was identified. Use short, imperative commit messages, for example: `Update iGovTI questionnaire evidence text`. Pull requests should describe the changed artifact, cite source documents used, identify affected audit phase, and note whether generated formats (`.pdf`, `.docx`, `.lss`) were updated.

## Agent-Specific Instructions

Answer from repository evidence, not filename inference. Read the relevant file before summarizing methodology, scope, criteria, questionnaire logic, or audit conclusions. Treat AI-generated outputs as drafts requiring human audit review. Nunca sugira comandos git, a menos que seja explicitamente solicitado pelo usuário.
