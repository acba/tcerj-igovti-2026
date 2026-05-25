---
name: preencher-matriz-planejamento
description: Ensina Codex a criar, preencher, revisar e corrigir matriz de planejamento de auditoria governamental, especialmente em Markdown, DOCX convertido ou texto estruturado. Use quando o usuário pedir para montar questões de auditoria, subquestões, riscos, fontes de informação, informações requeridas, critérios, procedimentos, evidências e possíveis achados, ou para verificar a coerência e rastreabilidade entre esses campos em fiscalizações, auditorias, levantamentos ou trabalhos de controle externo.
---

# Preencher Matriz de Planejamento

## Objetivo

Produzir ou revisar matrizes de planejamento de auditoria governamental com linguagem simples, formal e impessoal, mantendo conexão explícita entre objetivo, questão de auditoria, riscos, fontes, informações requeridas, critérios, procedimentos, evidências e possíveis achados.

Tratar a matriz como instrumento de planejamento: não concluir achados reais sem evidência de execução. Usar "possíveis achados" apenas como hipóteses de auditoria vinculadas aos riscos e aos procedimentos previstos.

## Fluxo de Trabalho

1. Levantar contexto do trabalho.
   - Ler o arquivo da matriz existente antes de editar.
   - Ler documentos de planejamento, análise de riscos, questionário, metodologia, escopo, critérios ou deliberações citadas pelo usuário.
   - Não inferir escopo apenas por nomes de arquivos.

2. Identificar a estrutura esperada.
   - Preservar o formato existente quando houver matriz prévia.
   - Se não houver formato definido, usar seções nesta ordem: `questao`, `subquestoes`, `riscos`, `fontes_de_informacao`, `informacoes_requeridas`, `criterios`, `procedimentos`, `evidencias`, `possiveis_achados`.
   - Manter identificadores rastreáveis, como `Q1`, `R1.1`, `F1`, `IR1`, `C1`, `P1`, `E1`, `A1.1`.

3. Definir ou revisar questões de auditoria.
   - Formular a questão como pergunta avaliável, vinculada ao objetivo e ao escopo.
   - Separar temas muito distintos em questões diferentes.
   - Evitar questão ampla demais que misture governança, segurança, contratações, continuidade e desempenho sem necessidade.
   - Quando o usuário excluir um tema do rol de achados, registrar como observação de levantamento, se útil, sem criar possíveis achados para ele.

4. Desdobrar subquestões.
   - Fazer subquestões diretamente testáveis por questionário, análise documental, entrevista ou inspeção.
   - Cobrir existência formal, vigência, conteúdo mínimo, implementação e acompanhamento quando isso for relevante.
   - Usar termos objetivos: "formalmente instituído", "vigente", "aprovado", "atualizado", "monitorado", "com responsáveis e prazos".

5. Construir riscos.
   - Escrever cada risco no padrão: "Devido a [causa], poderá [condição de risco], o que poderá levar a [efeito], impactando [consequência institucional]."
   - Não transformar o risco em achado definitivo.
   - Numerar riscos por questão: `R2.1`, `R2.2`.

6. Conectar campos da matriz.
   - Toda informação requerida deve apontar fonte: `IR3: ...; [F1, F2]`.
   - Todo procedimento deve apontar informação requerida e, quando aplicável, questão ou item do instrumento: `P3: ...; [IR3, q2201]`.
   - Toda evidência deve apontar procedimento: `E3: ...; [P3]`.
   - Todo possível achado deve apontar risco, procedimento e evidência: `A3.2: ...; [R3.2, P3, E3, P4, E4]`.

## Campos da Matriz

### fontes_de_informacao

Listar quem ou o que fornecerá dados:

- Área responsável pelo processo auditado.
- Alta administração ou instância de governança.
- Comitê, comissão, gestor formal ou unidade técnica.
- Sistemas, bases, portais, processos administrativos ou ferramentas.
- Documentos normativos, planos, relatórios, atas e registros operacionais.

### informacoes_requeridas

Descrever a informação necessária para responder à subquestão, sem ainda dizer como será testada.

Exemplos:

- `IR1: Declaração de existência de política formal vigente; [F1]`
- `IR2: Política formal, ato de aprovação, histórico de revisão e evidência de divulgação; [F1, F2]`
- `IR3: Registros de monitoramento, relatórios, painéis ou atas de acompanhamento; [F1, F3]`

### criterios

Usar critérios normativos, técnicos ou referenciais aceitos para avaliar a condição.

Preferir:

- Leis, decretos, resoluções, normas internas e deliberações aplicáveis.
- COBIT, ITIL, ISO, NIST ou outros frameworks quando compatíveis com o objeto.
- Acórdãos, notas técnicas e entendimentos dos tribunais de contas.
- Metodologia ou regulamento específico da fiscalização.

Não citar critério genérico sem utilidade prática. Indicar a prática, item ou obrigação sempre que possível.

### procedimentos

Descrever ações de auditoria executáveis.

Usar verbos como:

- Aplicar questionário.
- Analisar documento.
- Verificar amostra.
- Comparar registros.
- Entrevistar responsáveis.
- Inspecionar sistema ou ferramenta.
- Recalcular indicador.
- Testar aderência.

Evitar procedimento vago como "avaliar a governança" sem dizer qual informação será examinada.

### evidencias

Registrar que evidência confirmará ou refutará a condição planejada.

Incluir tanto respostas declaratórias quanto documentos ou registros:

- Resposta negativa ou insuficiente a item do questionário.
- Ausência, desatualização ou insuficiência de normativo, plano, relatório ou ata.
- Registros operacionais incompatíveis com a declaração.
- Amostra documental que comprove falha de implementação.

### possiveis_achados

Formular como hipótese de deficiência, com escopo claro e rastreável.

Bom:

- `A4.3: Inexistência ou insuficiência de modelos padronizados para elaboração dos artefatos das contratações de TIC; [R4.3, P5, E5, P6, E6]`

Fraco:

- `Problemas em contratações.`

## Regras de Qualidade

- Preservar linguagem formal, impessoal e em português do Brasil.
- Distinguir levantamento, avaliação de maturidade, auditoria de conformidade e auditoria operacional quando o escopo indicar essa diferença.
- Não criar achados para temas que a equipe definiu como apenas exploratórios.
- Não usar resposta declaratória como única evidência quando houver previsão de análise documental ou teste de amostra.
- Garantir que cada possível achado tenha pelo menos um risco e um caminho de evidência associado.
- Garantir que cada subquestão esteja coberta por informações requeridas e procedimentos.
- Evitar duplicidade: se dois achados dependem das mesmas evidências, avaliar se devem ser subachados ou um único achado mais bem delimitado.
- Manter consistência de numeração. Ao mover tema entre questões, atualizar todos os prefixos `R`, `IR`, `P`, `E` e `A`.

## Padrão de Escrita

Use frases diretas:

- "A organização possui..."
- "A organização executa..."
- "O plano está..."
- "Os incidentes são..."
- "Devido à ausência de..."
- "Analisar amostra de..."

Evite:

- Conclusões antes dos testes.
- Linguagem alarmista.
- Jargão sem necessidade.
- Critérios sem referência.
- Procedimentos que não geram evidência.

## Modelo Compacto

```markdown
## Questão 01 - Tema

questao: Q1. A organização [verbo avaliável] [objeto] [finalidade]?

subquestoes:
- A organização possui [controle] formalmente instituído?
- O [controle] está vigente, aprovado e atualizado?

riscos:
- R1.1: Devido à ausência de [causa], poderá haver [condição], o que poderá levar a [efeito], impactando [consequência].

fontes_de_informacao:
- F1: Área responsável.
- F2: Sistema ou processo administrativo.

informacoes_requeridas:
- IR1: Declaração de existência de [controle]; [F1]
- IR2: Documento formal, registros de aprovação e evidências de atualização; [F1, F2]

criterios:
- C1: Critério aplicável, item ou prática específica.

procedimentos:
- P1: Aplicar questionário para verificar a existência de [controle]; [IR1]
- P2: Analisar documentação para verificar vigência, aprovação e conteúdo mínimo, de acordo com C1; [IR2]

evidencias:
- E1: Resposta negativa ou insuficiente sobre [controle]; [P1]
- E2: Ausência, desatualização ou insuficiência da documentação de [controle]; [P2]

possiveis_achados:
- A1.1: Ausência ou fragilidade de [controle]; [R1.1, P1, E1, P2, E2]
```
