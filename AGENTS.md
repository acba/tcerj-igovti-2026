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
*   **`gerar_matriz_planejamento.py`:** Converts the matrix markdown template into DOCX.
    ```bash
    python3 scripts/gerar_matriz_planejamento.py 01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/matriz_planejamento.md
    ```
*   **`gerar_matriz_achados.py`:** Generates the findings matrix Word document.
    ```bash
    python3 scripts/gerar_matriz_achados.py
    ```
*   **`avaliar_evidencias_matriz_planejamento.py` / `avaliacao_evidencias`:** Runs the AI evidence evaluation pipeline. See [scripts/avaliacao_evidencias/README.md](file:///home/acba/workspace/fiscalizacoes/tcerj-igovti-2026/scripts/avaliacao_evidencias/README.md) for full commands.

Do not add invented `npm`, `make`, or `pytest` commands unless the required project files are introduced.

## Running the Audit by CLI

Use the local virtual environment and CLI. Write generated artifacts to `/tmp` unless the user explicitly requests a repository destination.

```bash
cd /home/acba/workspace/fiscalizacoes/tcerj-igovti-2026

scripts/.venv/bin/python scripts/executa_auditoria.py \
  --auditados 02-Execucao/03-Execucao_Procedimentos/bd_auditados.xlsx \
  --mapa 02-Execucao/03-Execucao_Procedimentos/mapa-verificacao-achados.xlsx \
  --fontes 02-Execucao/01-Questionario/20260611-respostas-questionario.xlsx \
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

The first command generates the auditable workbook `02-Execucao/02-Questionario iGovTI 2023/20260611-comparacao-iGovTI-2023-2026.xlsx`. The second generates the report context workbook and a JSON calculation record in `02-Execucao/01-Questionario/`. Pass alternative source and output paths through the scripts' command-line arguments when processing a later data version.

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
  --context-files 02-Execucao/01-Questionario/20260611-contexto-relatorios-igovti-2026.xlsx \
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
