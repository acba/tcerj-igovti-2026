# Repository Guidelines

## Project Structure & Module Organization

This repository stores digital workpapers for TCE-RJ Fiscalization 18/2026, focused on iGovTI 2026. It is documentation-heavy and currently has no application source tree.

- `01-Planejamento/`: planning artifacts, methodology, survey files, strategy, audit plan, and planning matrix.
- `01-Planejamento/02-Metodologia_iGovTI/`: core iGovTI questionnaire in `.md`, `.lss`, `.docx`, and `.pdf`.
- `01-Planejamento/01-Estudos_Preliminares/Referencias_Externas/`: benchmark materials from TCU, TCE-PE, TCE-RJ, TCE-RS, and IEGM.
- `02-Execucao/`: reserved for responses, collected evidence, audit tests, preliminary findings, and findings matrix.
- `03-Relatorios/`: reserved for consolidated and individual reports.
- `04-Portal_iGovTI/`: portal requirements, currently `PRD.md`.
- `scripts/`: reserved for automation; no executable scripts were identified.

## Build, Test, and Development Commands

No build system, package manifest, test runner, or local application entry point is currently defined. Useful inspection commands:

```bash
rg --files -g '!**/.git/**'
find . -maxdepth 3 -type d | sort
rg -n "^## Grupo:|^### q|evidence_text:" 01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md
```

Do not add invented `npm`, `make`, or `pytest` commands unless the required project files are introduced.

## Coding Style & Naming Conventions

Prefer Portuguese (Brazil) for project documentation. Preserve existing directory prefixes such as `01-Planejamento`, `02-Execucao`, and `03-Relatorios`. For questionnaire edits, preserve identifiers like `g0100`, `q0101`, `evidence_text`, `visible_if`, and LimeSurvey response codes in `.lss` files.

Keep Markdown concise and structured. Do not reformat entire `.docx` exports, `.lss` XML, CSVs, or generated PDFs unless explicitly required.

## Testing Guidelines

There are no automated tests yet. For documentation changes, verify links, paths, headings, and consistency with source documents. For questionnaire changes, compare the `.md` and `.lss` versions and validate LimeSurvey import/export before treating the change as complete.

## Commit & Pull Request Guidelines

No repository-specific commit convention was identified. Use short, imperative commit messages, for example: `Update iGovTI questionnaire evidence text`. Pull requests should describe the changed artifact, cite source documents used, identify affected audit phase, and note whether generated formats (`.pdf`, `.docx`, `.lss`) were updated.

## Agent-Specific Instructions

Answer from repository evidence, not filename inference. Read the relevant file before summarizing methodology, scope, criteria, questionnaire logic, or audit conclusions. Treat AI-generated outputs as drafts requiring human audit review.
