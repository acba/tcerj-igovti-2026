# TCE-RJ Report Markdown And Markup

Use this reference for TCE-RJ audit report `.md` files that mix Markdown, Pandoc labels/cross-references, and Jinja templating.

## Core Syntax

- Write in Brazilian Portuguese, formal audit style.
- Preserve YAML frontmatter in full report templates:

```markdown
---
title: "RELATÓRIO INDIVIDUAL"
subtitle: {{ auditado.sigla }} - {{ auditado.nome }}
lang: pt-BR
figure-caption-position: above
---
```

- Use Jinja variables exactly when values come from rendering context:

```markdown
O(A) {{ auditado.sigla }} obteve o **valor {{ '%0.2f' | format(iSegCiber|float) }} para o iSegCiber**.
```

- Use `{% if %}`, `{% else %}`, `{% for %}`, `{% set %}`, `{% include %}`, and `{# comentario #}` normally. Keep `{%- ... %}` only when whitespace control is needed inside tables or lists.
- Include fragments with paths relative to the rendering template:

```markdown
{% include 'achado_controle_7.md' %}
```

- Insert page breaks as a standalone line:

```markdown
\newpage
```

- Use `__texto__` for underlined emphasis:

```markdown
__Ressalta-se que o escopo desta avaliação se limitou à análise das informações prestadas no plano de ação apresentado.__
```

## Template Context Objects

The report renderer provides an `auditado` object of type `Auditado`. Achado fragments commonly retrieve an `achado` object from it.

### Auditado

Represents the audited entity and stores the procedure results for that entity.

Attributes:

- `nome` (`str`): full name of the audited entity.
- `sigla` (`str`): acronym or key name used in report text, filenames, and most lookups.
- `foi_auditado` (`bool`): true after audit procedures are executed for this entity.
- `procedimentos_executados` (`list`): executed `ProcedimentoAuditoria` objects copied with entity-specific results.
- `tem_achados` (`bool`): true when any executed procedure produced a finding.

Methods:

- `get_nomes_achados()`: returns strings formatted like `"1. Nome do Achado"` for identified findings.
- `get_achados()`: returns a dictionary whose keys identify findings, such as `"achado1"`, and whose values are `Achado` objects.
- `get_achado_por_nome(nome_achado)`: returns the `Achado` object with the exact finding name, or `None` when absent.
- `get_situacoes_inconformes()`: returns a consolidated list of all nonconforming situation strings from all findings.
- `get_encaminhamentos()`: returns a consolidated deduplicated list of finding encaminhamento strings.
- `get_plano_acao()`: returns a list of dictionaries suitable for the plan-of-action table. Each item contains the finding number, encaminhamento type, and encaminhamento description.

Common usage:

```markdown
{% if auditado.tem_achados %}
{% include 'achado_controle_7.md' %}
{% endif %}

{%- for item in auditado.get_plano_acao() %}
| **{{ item.achado_num }}** | {{ item.encaminhamento }} | | | |{% endfor %}
```

### Achado

Represents a specific audit finding with its situations, evidence, and proposed encaminhamentos.

Attributes:

- `numero` (`int` or `str`): finding identifier.
- `nome` (`str`): descriptive finding title.
- `situacoes_encontradas` (`list`): nonconforming situation strings that materialize the finding.
- `encaminhamentos` (`list`): dictionaries/objects with `tipo`, `fundamentacao_encaminhamento` e `encaminhamento`.
- `evidencias` (`list`): evidence strings supporting the finding.

Common usage:

```markdown
{% set nome_achado = 'Medidas básicas de segurança cibernética insuficientes na gestão de vulnerabilidades nos ativos da organização' %}
{% set achado = auditado.get_achado_por_nome(nome_achado) %}
{% if achado %}

## Achado {{ achado.numero }} – {{ achado.nome }}

### Evidências
{% for evidencia in achado.evidencias %}
* {{ evidencia }};
{% endfor %}

{% set situacao = 'A organização não estabelece e mantém adequadamente um processo de gestão de vulnerabilidades'%}
{% if situacao in achado.situacoes_encontradas %}
...
{% endif %}

### Propostas de Encaminhamento
{% for e in achado.encaminhamentos %}
* **Comunicação com {{ e.tipo }}** para que, {{ e.fundamentacao_encaminhamento }}, {{ e.encaminhamento }};
{% endfor %}

{% endif %}
```

Rules:

- Match `nome_achado` and `situacao` strings exactly with the values produced by the audit procedures.
- Guard achado fragments with `{% if achado %}` so absent findings do not render empty sections.
- In Jinja, dictionary keys can be accessed with dot syntax when compatible, as in `{{ e.tipo }}` and `{{ item.achado_num }}`.
- Nos relatórios individuais finais, omitir identificadores internos de critérios, situações e evidências (`C1`, `S1.1`, `E1`). Apresentar critérios específicos no corpo, somente ao destinatário aplicável, sem nota de rodapé.
- Usar a fundamentação declarada na matriz; não reconstruí-la no template a partir da lista de critérios.

## Figures

Use this exact pattern for figures, with the source block immediately after the image:

```markdown
![Dimensões e controles avaliados](controles_avaliados.png){#fig:controles_avaliados#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>
```

Rules:

- Label format: `{#fig:nome_descritivo#}`.
- Reference in text with `[@fig:nome_descritivo]`.
- Use image paths as they will exist beside the rendered report, often `{{ auditado.sigla }}_arquivo.png`.
- If width is necessary, keep the `fig:` label and the source block:

```markdown
![Níveis de maturidade](cenario_geral_niveis_maturidade.png){ width=80% }{#fig:cenario_geral_niveis_maturidade#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>
```

## Tables

Place the table caption before the Markdown table:

```markdown
: Avaliação dos encaminhamentos {#tbl:ajuste_respostas#}

| Encaminhamento proposto | Status | Avaliação |
|---|---|---|
{%- for d in pa_detalhes %}
| {{ d.encaminhamento }} | {{ d.status }} | {{ d.analise_critica }} |{% endfor %}

<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>
```

Rules:

- Label format: `{#tbl:nome_descritivo#}`.
- Reference in text with `[@tbl:nome_descritivo]`.
- Keep the source block after the table.
- Preserve Jinja loops inside table rows. When a loop emits rows, close the loop at the end of the row unless readability requires a separate line.

## Footnotes

Use named footnotes. Reference in the text with `[^id]` and define with `[^id]: texto`.

```markdown
Os Controles CIS v8.1[^explica_controles_cis] constituem um conjunto prioritário.

[^explica_controles_cis]: Os Controles CIS constituem um conjunto prioritário e prescritivo de práticas recomendadas de segurança cibernética.
```

Rules:

- Use descriptive snake_case identifiers such as `explica_iso_27002`, `explica_mb_c7`, or `referencia_ppsi_politica_logs`.
- End references with `Acesso em: {{ data_hoje_abnt }}.` when the access date is rendered dynamically.
- Keep footnote definitions near the section where they are used, before detailed conditional subsections when practical.

## Report Structure

Full individual reports commonly follow:

1. `# 1. Introdução`
2. `# 2. Adequação às boas práticas de segurança da informação e segurança cibernética`
3. `## 2.1. Cenário Geral`
4. `## 2.2. Cenário atual - {{ auditado.sigla }}`
5. control subsections such as `### 2.2.1. Controle 07 – Gestão de vulnerabilidades`
6. conditional `# 3. Resultados da Auditoria`
7. conditional achado includes
8. `# 4. Plano de Ação`
9. appendices for evidence adjustments and gestor comments.

Control sections use this pattern:

```markdown
### 2.2.N. Controle XX – Nome do controle

Este controle avalia...

Um dos resultados esperados desse controle é...

Nesse controle (iMBCXX) a organização apresentou **valor {{ '%0.2f' | format(iMBCXX|float) }}**, alcançando um **nível "{{ iMBCXX_aderencia }}" de aderência** e sua posição relativa pode ser vista na [@fig:comparativo_distribuicao_iMBCXX].

![Histograma do nível de adoção do controle XX por todos auditados]({{auditado.sigla}}_comparativo_distribuicao_iMBCXX.png){#fig:comparativo_distribuicao_iMBCXX#}
<div custom-style="FonteImagem">(Fonte: elaboração própria)</div>

Para alcançar o resultado, considerou-se o seguinte conjunto de medidas de segurança básica, apontado na [@tbl:medidas_controle_XX]:
```

## Achado Fragment Structure

Use one fragment per control and follow this structure faithfully. Do not turn achado fragments into standalone reports, generic summaries, or free-form notes.

Mandatory order:

1. Define `nome_achado` with the exact finding title used by the audit procedures.
2. Retrieve `achado` with `auditado.get_achado_por_nome(nome_achado)`.
3. Guard the whole fragment with `{% if achado %}`.
4. Insert a standalone `\newpage`.
5. Render `## Achado {{ achado.numero }} – {{ achado.nome }}`.
6. Write `### Critérios` with legal, normative, CIS Controls, and ISO criteria as bullets ending with semicolon, except the final item may end with period.
7. Write `### Evidências` with a Jinja loop over `achado.evidencias`.
8. Write `### Situação encontrada` and start it with a concise paragraph that directly answers the audit question for `{{ auditado.sigla }}`. Because the fragment only renders when an achado exists, the answer is negative. This opening paragraph must dynamically identify the concrete fragilities found with `{% if situacao_x in achado.situacoes_encontradas %}` blocks and, for each present fragility, state the breached criteria and expected effects.
9. Continue `### Situação encontrada` with the control/risk/legal/good-practice narrative.
10. List `achado.situacoes_encontradas` before the detailed subsections.
11. Define footnotes used in the general situation narrative near that narrative.
12. For each possible situation or grouped situations, use `{% set situacao = ... %}` or `{% set situacaoA = ... %}` and a conditional `####` subsection.
13. In each conditional subsection, explain the measure, expected practice, evidence analysis, risk, and proposed recommendation/determination with `__...__` emphasis when appropriate.
14. Write `#### Conclusão`.
15. Write `### Propostas de Encaminhamento` with a loop over `achado.encaminhamentos`.
16. Close with a Jinja comment identifying the achado and then `{% endif %}`.

Canonical skeleton:

```markdown
{% set nome_achado = 'Medidas básicas de segurança cibernética insuficientes ...' %}
{% set achado = auditado.get_achado_por_nome(nome_achado) %}
{% if achado %}

\newpage

## Achado {{ achado.numero }} – {{ achado.nome }}

### Critérios
* Lei Federal nº 12.527/2011 (LAI), art. 6º, incisos II e III (...);
* Lei Federal nº 13.709/2018 (LGPD), art. 6º, inciso VII, art. 46 e art. 47 (...);
* Controles CIS versão 8.1, medidas de segurança ...;

### Evidências
{% for evidencia in achado.evidencias %}
* {{ evidencia }};
{% endfor %}

### Situação encontrada
{% set situacao_a = 'Situação encontrada A exatamente como gerada pelo procedimento' %}
{% set situacao_b = 'Situação encontrada B exatamente como gerada pelo procedimento' %}
{% set situacao_c = 'Situação encontrada C exatamente como gerada pelo procedimento' %}
A partir da análise das informações fornecidas, verificou-se que a organização {{ auditado.sigla }} não demonstrou atender integralmente à questão de auditoria, pois a Equipe de Auditoria identificou fragilidades{% if situacao_a in achado.situacoes_encontradas %} na dimensão A{% endif %}{% if situacao_b in achado.situacoes_encontradas %}{% if situacao_a in achado.situacoes_encontradas %}, {% else %} {% endif %}na dimensão B{% endif %}{% if situacao_c in achado.situacoes_encontradas %}{% if situacao_a in achado.situacoes_encontradas or situacao_b in achado.situacoes_encontradas %} e {% else %} {% endif %}na dimensão C{% endif %}.{% if situacao_a in achado.situacoes_encontradas %} A fragilidade na dimensão A contraria [critérios aplicáveis] e pode causar [efeitos esperados].{% endif %}{% if situacao_b in achado.situacoes_encontradas %} A fragilidade na dimensão B contraria [critérios aplicáveis] e pode causar [efeitos esperados].{% endif %}{% if situacao_c in achado.situacoes_encontradas %} A fragilidade na dimensão C contraria [critérios aplicáveis] e pode causar [efeitos esperados].{% endif %}

Parágrafo sobre o objetivo do controle, a relevância para segurança da informação e o risco decorrente da ausência ou ineficiência do processo.

Parágrafo relacionando o dever legal de segurança com LAI, LGPD e demais normas aplicáveis.

No contexto do controle, o cumprimento desses requisitos materializa-se na adoção de práticas consagradas, como a ABNT NBR ISO/IEC 27002:2022[^explica_iso_cx] e as medidas de higiene cibernética do Controle XX dos Controles CIS v8.1[^explica_mb_cx].

Para assegurar uma gestão eficaz e conforme, a organização deve adotar, minimamente, as medidas básicas do Controle XX...

Com base na análise dos itens XXXX do questionário aplicado e da avaliação dos documentos encaminhados, conforme apontado na seção de Evidências, a Equipe de Auditoria constatou as seguintes deficiências nos controles da organização:

{% for situacao in achado.situacoes_encontradas %}
* **{{ situacao }};**{% endfor %}

Essas situações ensejaram o presente achado e serão detalhadas nas seções subsequentes.

[^explica_mb_cx]: ...

[^explica_iso_cx]: ...

{% set situacao = 'A organização não ...'%}
{% if situacao in achado.situacoes_encontradas %}
#### Título específico da situação

Texto técnico e jurídico da situação encontrada.

Da análise das respostas e da documentação fornecida ao item XXXX, verificou-se que ...

Diante disso, __será proposta recomendação para que a organização ...__.

{% endif %}

#### Conclusão
As fragilidades identificadas ... comprometem ...

Diante das situações apresentadas, será sugerida proposta de encaminhamento à organização para que promova a adequação de seus controles, alinhando-se às práticas da ABNT NBR ISO/IEC 27002:2022 e do CIS Controls v8.1.

### Propostas de Encaminhamento
{% for e in achado.encaminhamentos %}
* **Comunicação com {{ e.tipo }}** para que {{ e.encaminhamento }};
{% endfor %}

{# Final do Achado - Nome resumido #}
{% endif %}
```

For conditional subsections:

```markdown
{% set situacao = 'A organização não estabelece e mantém adequadamente um processo de gestão de vulnerabilidades'%}
{% if situacao in achado.situacoes_encontradas %}
#### Processo de gestão de vulnerabilidade

...

Diante disso, __será proposta recomendação para que a organização estabeleça, mantenha e revise periodicamente seu processo de gestão de vulnerabilidades__.

{% endif %}
```

Required concrete pattern from `achado_controle_7.md`:

```markdown
{% set nome_achado = 'Medidas básicas de segurança cibernética insuficientes na gestão de vulnerabilidades nos ativos da organização' %}
{% set achado = auditado.get_achado_por_nome(nome_achado) %}
{% if achado %}

\newpage

## Achado {{ achado.numero }} – {{ achado.nome }}

### Critérios
...

### Evidências
{% for evidencia in achado.evidencias %}
* {{ evidencia }};
{%- endfor %}

### Situação encontrada
...

{% set situacao = 'A organização não estabelece e mantém adequadamente um processo de gestão de vulnerabilidades'%}
{% if situacao in achado.situacoes_encontradas %}
#### Processo de gestão de vulnerabilidade
...
{% endif %}

#### Conclusão
...

### Propostas de Encaminhamento
{% for e in achado.encaminhamentos %}
* **Comunicação com {{ e.tipo }}** para que {{ e.encaminhamento }};
{%- endfor %}

{# Final do Achado - Gestão de vulnerabilidades #}
{% endif %}
```

For grouped situations:

```markdown
{% set situacaoA = '...' %}
{% set situacaoB = '...' %}
{% if situacaoA in achado.situacoes_encontradas or situacaoB in achado.situacoes_encontradas %}
#### Título comum
...
{% endif %}
```

## Audit Prose Style

- Prefer paragraphs that explain control objective, risk, legal criterion, good practice, evidence basis, deficiency, and proposed measure.
- Use "Com base na análise..." to introduce findings from questionnaire/evidence review.
- Use "Diante disso, __será proposta recomendação..." or "será proposta **DETERMINAÇÃO**..." for proposed outcomes.
- Do not write that a decision was breached unless the evidence and procedural stage support that conclusion.
- Distinguish preliminary plan-of-action review from validated audit testing.
- Use `*framework*`, `*software*`, `*logs*`, `*backup*`, `*malware*`, `*e-mail*`, and similar technical terms consistently.

## Evidence Integrity

- Do not update numeric indicators or maturity labels by estimation.
- Preserve variables such as `iSegCiber`, `iMBC7`, `ms71`, `iMBC17_aderencia`, `pa_Indice_Cobertura`, and `auditado.sigla`.
- Before changing methodology, scope, findings, or conclusions, read the relevant source workpaper or spreadsheet-derived context in the repository.
- Treat generated narrative as draft audit work that requires human audit review.
