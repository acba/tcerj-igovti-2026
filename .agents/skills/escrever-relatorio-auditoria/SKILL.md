---
name: escrever-relatorio-auditoria
description: Draft and revise Brazilian Portuguese TCE-RJ audit report templates, report fragments, findings, appendices, and workpaper-derived narrative in the Markdown, Pandoc, and Jinja style used by relatorio_individual/relatorio/*.md. Use when Codex needs to write or edit .md reports with figures, table captions, footnotes, page breaks, includes, Jinja variables, conditionals, loops, iSegCiber and iMBC values, CIS Controls findings, recommendations, determinations, or FonteImagem source blocks.
---

# Escrever Relatório de Auditoria

## Overview

Write report text as audit-ready Brazilian Portuguese Markdown with Pandoc labels and Jinja templating. Preserve evidence integrity: read the relevant report template, fragment, spreadsheet, or workpaper before changing methodology, values, conclusions, or findings.

## Workflow

1. Identify whether the task is a full report template, a control section, an achado fragment, a plan-of-action section, or an appendix.
2. If working inside a repository, read the closest existing examples first, especially `relatorio_individual/relatorio/relatorio-individual-template.md` and matching `achado_controle_*.md` files.
3. Load `references/report-markup.md` when writing or revising syntax, structure, labels, footnotes, Jinja, figures, tables, achado fragments, or audit prose.
4. Keep variables and labels stable unless the user asks for new ones. Do not estimate percentages, iSegCiber/iMBC values, maturity levels, organization counts, or evidence conclusions.
5. Validate edited Markdown with `python3 scripts/check_report_markup.py <file.md>` when the script is available.

## Writing Rules

- Use formal Portuguese from the perspective of the `Equipe de Auditoria`.
- Use assertions supported by repository evidence. If validation was not performed, state the limitation in the text rather than implying confirmed noncompliance.
- For `achado_controle_*.md` files, follow the mandatory achado fragment contract in `references/report-markup.md`: initial `nome_achado`/`achado` definitions, `{% if achado %}` guard, `\newpage`, `## Achado {{ achado.numero }} – {{ achado.nome }}`, criteria, evidence loop, situation-found narrative, conditional situation subsections, conclusion, encaminhamento loop, final comment, and closing `{% endif %}`.
- Start `### Situação encontrada` with a concise paragraph that directly answers the audit question for the audited entity. Because an achado fragment only renders when at least one nonconforming situation exists, this answer is negative and must dynamically list the concrete fragilities found with Jinja conditionals, tying each present fragility to the breached criteria and expected effects.
- Use Jinja expressions for context-dependent values, for example `{{ '%0.2f' | format(iSegCiber|float) }}`.
- Use the available template context objects `auditado` (`Auditado`) and `achado` (`Achado`) according to `references/report-markup.md`.
- Use `__texto__` for underlined emphasis when proposing recommendations, determinations, or explicit caveats.
- Use Pandoc cross-references such as `[@fig:controles_avaliados]` and `[@tbl:painel_notas]`.
- Place figure and table source blocks immediately after the corresponding figure/table.
- Insert page breaks as a standalone `\newpage` line.

## Resources

- `references/report-markup.md`: exact Markdown, Pandoc, Jinja, figure, table, footnote, include, and achado-fragment patterns.
- `scripts/check_report_markup.py`: lightweight validator for common markup defects in generated `.md` report files.
