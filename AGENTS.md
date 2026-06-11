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

## Build, Test, and Development Commands

No build system or test runner is currently defined. Useful inspection commands:

```bash
rg --files -g '!**/.git/**'
find . -maxdepth 3 -type d | sort
rg -n "^## Grupo:|^### q|evidence_text:" 01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md
```

Do not add invented `npm`, `make`, or `pytest` commands unless the required project files are introduced.

## Running the Audit by CLI

Use the Argos virtual environment and CLI. Run the command from the Argos repository so its local imports resolve correctly. Write generated artifacts to `/tmp` unless the user explicitly requests a repository destination.

```bash
cd /home/acba/workspace/webapp-streamlit-argos

.venv/bin/python cli/run_audit.py \
  --auditados /home/acba/workspace/fiscalizacoes/tcerj-igovti-2026/02-Execucao/03-Execucao_Procedimentos/bd_auditados.xlsx \
  --mapa /home/acba/workspace/fiscalizacoes/tcerj-igovti-2026/02-Execucao/03-Execucao_Procedimentos/mapa-verificacao-achados.xlsx \
  --fontes /home/acba/workspace/fiscalizacoes/tcerj-igovti-2026/02-Execucao/01-Questionario/20260607-respostas-questionario.xlsx \
  --output-json /tmp/tcerj-igovti-2026/auditoria/resultado_auditoria.json \
  --output-xlsx /tmp/tcerj-igovti-2026/auditoria/tabelas_consolidadas_auditoria.xlsx
```

The audit inputs are the audited-organizations database, the verification/findings map, and every source workbook required by the `Fontes de Informação` sheet. When that sheet declares more than one source file, pass all of them after `--fontes`. Confirm that the CLI finishes without missing-source errors before using the JSON to generate reports.

## Generating an Individual Preliminary Report

First generate the common charts and the charts for the selected organizations. `--auditados` accepts one or more organization identifiers; when omitted, charts are generated for all organizations. Common charts are always regenerated.

```bash
cd /home/acba/workspace/fiscalizacoes/tcerj-igovti-2026

python3 scripts/gerar_graficos_relatorios_igovti.py \
  --auditados FTM \
  --output-root /tmp/tcerj-igovti-2026
```

The Markdown template references images only by filename. Before invoking Argos, prepare a flat resource directory containing both common and organization-specific charts, because Pandoc does not recursively search `img/<SIGLA>/`.

```bash
mkdir -p /tmp/tcerj-igovti-2026/relatorios-individuais/FTM-recursos

cp /tmp/tcerj-igovti-2026/relatorios-individuais/img/*.png \
  /tmp/tcerj-igovti-2026/relatorios-individuais/FTM-recursos/

cp /tmp/tcerj-igovti-2026/relatorios-individuais/img/FTM/*.png \
  /tmp/tcerj-igovti-2026/relatorios-individuais/FTM-recursos/
```

Then generate the report with the Argos CLI:

```bash
cd /home/acba/workspace/webapp-streamlit-argos

.venv/bin/python cli/generate_reports.py \
  --auditados /tmp/tcerj-igovti-2026/auditoria/resultado_auditoria.json \
  --templates /home/acba/workspace/fiscalizacoes/tcerj-igovti-2026/03-Relatorios/02-Relatorios_Individuais_Preliminares/relatorio-individual-preliminar-template.md \
  --context-files /home/acba/workspace/fiscalizacoes/tcerj-igovti-2026/02-Execucao/01-Questionario/iGovTI-2026.xlsx \
  --resource-files /tmp/tcerj-igovti-2026/relatorios-individuais/FTM-recursos \
  --auditados-select FTM \
  --output-dir /tmp/tcerj-igovti-2026/relatorios-individuais/FTM \
  --reference-docx /home/acba/workspace/webapp-streamlit-argos/docs/template-base-estilos-sigiloso.docx
```

If the audit was not rerun, the current repository result may be used instead of the temporary JSON: `02-Execucao/03-Execucao_Procedimentos/resultado_auditoria.json`. Replace `FTM` consistently in the chart command, resource directory, `--auditados-select`, and output directory for another organization. Validate that the final DOCX contains embedded media and that the Argos output has no `Could not fetch resource` warnings.

## Coding Style & Naming Conventions

Prefer Portuguese (Brazil) for project documentation. Preserve existing directory prefixes such as `01-Planejamento`, `02-Execucao`, and `03-Relatorios`. For questionnaire edits, preserve identifiers like `g0100`, `q0101`, `evidence_text`, `visible_if`, and LimeSurvey response codes in `.lss` files.

Keep Markdown concise and structured. Do not reformat entire `.docx` exports, `.lss` XML, CSVs, or generated PDFs unless explicitly required.

## Testing Guidelines

There are no automated tests yet. For documentation changes, verify links, paths, headings, and consistency with source documents. For questionnaire changes, compare the `.md` and `.lss` versions and validate LimeSurvey import/export before treating the change as complete.

## Commit & Pull Request Guidelines

No repository-specific commit convention was identified. Use short, imperative commit messages, for example: `Update iGovTI questionnaire evidence text`. Pull requests should describe the changed artifact, cite source documents used, identify affected audit phase, and note whether generated formats (`.pdf`, `.docx`, `.lss`) were updated.

## Agent-Specific Instructions

Answer from repository evidence, not filename inference. Read the relevant file before summarizing methodology, scope, criteria, questionnaire logic, or audit conclusions. Treat AI-generated outputs as drafts requiring human audit review. Nunca sugira comandos git, a menos que seja explicitamente solicitado pelo usuário.
