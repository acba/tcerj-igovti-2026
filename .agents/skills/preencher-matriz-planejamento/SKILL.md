---
name: preencher-matriz-planejamento
description: Ensina Codex a criar, preencher, revisar e corrigir matriz de planejamento de auditoria governamental, especialmente em Markdown, DOCX convertido ou texto estruturado, e a manter planilha apartada de checklists de verificação de evidências. Use quando o usuário pedir para montar questões de auditoria, subquestões, riscos, fontes de informação, informações requeridas, critérios, procedimentos, evidências, possíveis achados, situações encontradas, regras de identificação, encaminhamentos ou prompts de avaliação de evidências por IA, ou para verificar a coerência e rastreabilidade entre esses campos em fiscalizações, auditorias, levantamentos ou trabalhos de controle externo.
---

# Preencher Matriz de Planejamento

## Objetivo

Produzir ou revisar matrizes de planejamento de auditoria governamental com linguagem simples, formal e impessoal, mantendo conexão explícita entre objetivo, questão de auditoria, riscos, fontes, informações requeridas, critérios, procedimentos, evidências e possíveis achados.

Tratar a matriz como instrumento de planejamento: não concluir achados reais sem evidência de execução. Usar "possíveis achados" apenas como hipóteses de auditoria vinculadas aos riscos e aos procedimentos previstos.

Na Fiscalização TCE-RJ nº 18/2026 - iGovTI 2026, também manter, quando solicitado, a planilha apartada de checklists de verificação de evidências, usada para registrar os prompts que serão enviados à API de modelo de IA para avaliar evidências anexadas ao questionário.

## Fluxo de Trabalho

1. Levantar contexto do trabalho.
   - Ler o arquivo da matriz existente antes de editar.
   - Para este repositório, a matriz principal fica em `01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/matriz_planejamento.md`.
   - Ler documentos de planejamento, análise de riscos, questionário, metodologia, escopo, critérios ou deliberações citadas pelo usuário.
   - Para regras vinculadas a itens do questionário, conferir o texto dos itens em `01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md` antes de propor ou revisar regras.
   - Não inferir escopo apenas por nomes de arquivos.

2. Identificar a estrutura esperada.
   - Preservar o formato existente quando houver matriz prévia.
   - Na matriz atual, usar seções nesta ordem: `questao`, `subquestoes`, `riscos`, `fontes_de_informacao`, `informacoes_requeridas`, `criterios`, `procedimentos`, `evidencias`, `possiveis_achados`.
   - Manter identificadores rastreáveis, como `Q1`, `R1.1`, `F1`, `IR1`, `C1`, `P1`, `E1`, `A1`, `S1.1`.
   - Em `possiveis_achados`, preservar o padrão de 1 achado estruturante por questão de auditoria, composto por várias `situacoes_encontradas`.

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
   - Toda situação encontrada deve apontar, em `referencias_matriz`, risco, procedimento e evidência: `referencias_matriz: [R3.2, P3, E3, P4, E4]`.
   - Toda situação encontrada deve indicar `descricao`, `severidade`, `itens_questionario`, `regra_de_identificacao`, `referencias_matriz`, `criterios` e `encaminhamento`.

7. Manter checklists de verificação de evidências, quando solicitado.
   - Criar ou atualizar a planilha `matriz_verificaca_evidencias.xlsx` no mesmo diretório de `matriz_planejamento.md`.
   - Registrar uma linha por avaliação de evidência a ser realizada. Em regra, usar uma linha por par `situação encontrada` + `item de evidência`, pois a mesma evidência pode comprovar finalidades distintas em situações diferentes.
   - Usar as colunas: `id_avaliacao`, `questao_auditoria`, `situacao_encontrada`, `item_evidencia`, `descricao_avaliacao`, `prompt_checklist`.
   - Montar `id_avaliacao` no padrão `Qn-Sn.n-itemevi`, por exemplo `Q1-S1.6-q1001evi`.
   - O `prompt_checklist` deve orientar a avaliação exclusiva da evidência anexada, mencionar a questão, a situação encontrada, o item de evidência, a evidência esperada no questionário, os critérios aplicáveis e um checklist objetivo.
   - O prompt deve solicitar saída estruturada em JSON, com `resultado` binário igual a `Conforme` ou `Não conforme`, além de `justificativa_sintetica`, `elementos_comprovados`, `lacunas` e `inconsistencias`.
   - Usar o `id_avaliacao` como coluna de resultado no processamento posterior, pois o mesmo item de evidência pode ter avaliações distintas para situações encontradas diferentes.
   - Quando a matriz consumir o resultado de avaliação de evidência, referenciar o alvo no atributo `regra_de_identificacao`, por exemplo: `avaliacao[Q2-S2.3-q2102evi] == "Não conforme"`.

## Estrutura Atual da Matriz iGovTI 2026

A matriz atual da Fiscalização TCE-RJ nº 18/2026 - iGovTI 2026 trabalha com 6 questões de auditoria e 6 achados estruturantes:

- Q1 - Estrutura e Governança de TIC: A1 - Estrutura e governança de TIC insuficientes para avaliar, dirigir e monitorar a tecnologia da informação.
- Q2 - Planejamento de TIC: A2 - Planejamento de TIC inexistente, insuficiente, desatualizado ou desconectado da gestão, do orçamento e das contratações.
- Q3 - Capacidade Institucional de TIC e Segurança da Informação: A3 - Capacidade institucional insuficiente para sustentar a gestão de TIC e segurança da informação.
- Q4 - Gestão de Serviços de TIC: A4 - Gestão de serviços de TIC incipiente, sem controle mínimo sobre serviços, ativos e incidentes.
- Q5 - Segurança da Informação, Gestão de Riscos e Continuidade de TIC: A5 - Segurança e continuidade insuficientes para proteger dados e recuperar serviços críticos.
- Q6 - Contratações de TIC: A6 - Contratações de TIC sem governança técnica e controle de resultados.

Cada achado estruturante é composto por situações encontradas (`S1.1`, `S1.2` etc.). A ocorrência de uma ou mais situações pode caracterizar o achado estruturante, sem fragmentar o relatório em muitos achados autônomos.

O padrão atual de uma situação encontrada é:

```yaml
- S1.1:
    descricao: Ausência de formalização da área, unidade, setor ou função de TIC da organização.
    severidade: alta
    itens_questionario: [q0101, q0101evi]
    regra_de_identificacao:
    - (q0101 == F)
    - ou q0101evi são inexistentes, incompatíveis ou insuficientes para comprovar formalização da área, unidade, setor ou função de TIC
    referencias_matriz: [R1.1, P1, E1, P2, E2]
    criterios: [C1, C5, C9]
    encaminhamento: Recomendar que a organização formalize a área, unidade, setor ou função de TIC em regimento, decreto, portaria, resolução, organograma ou instrumento equivalente.
```

## Convenções do Questionário

Use as seguintes convenções ao referenciar itens do questionário:

- `qXXXX`: item principal do questionário.
- `qXXXXext[A]`: subitem A de questão do tipo `adoption`/`detail_options`.
- `qXXXX[A]`: subitem A de questão do tipo `array`.
- `qXXXXevi`: evidência anexada à questão `qXXXX`.
- `q2804eviA`: evidência específica vinculada ao subitem `q2804[A]`.

Para subitens condicionais do tipo `adoption/detail_options`, a matriz pode usar regras como `(qXXXXext[A] != Sim)`. Essa condição abrange tanto o subitem explicitamente não marcado quanto a ausência do subitem porque a resposta principal não habilitou os detalhes, desde que a base de apuração normalize esses casos como valor diferente de `Sim`.

Ao criar regras, prefira condições objetivas com códigos ou subitens do questionário. Evite formulações vagas como "q0101 indica inexistência de área formal de TIC" quando for possível escrever `(q0101 == F)`.

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

Formular como hipótese de deficiência estruturante, com escopo claro e rastreável. Na matriz atual, cada questão possui 1 possível achado principal, e as deficiências específicas ficam em `situacoes_encontradas`.

Bom:

- `A4: Gestão de serviços de TIC incipiente, sem controle mínimo sobre serviços, ativos e incidentes`

Fraco:

- `Problemas em contratações.`

### situacoes_encontradas

Desdobrar o achado estruturante em situações objetivas, mensuráveis pelo questionário e pelas evidências anexadas.

Cada situação deve conter:

- `descricao`: condição negativa específica, em linguagem de achado potencial.
- `severidade`: `alta`, `media` ou `baixa`. Campo obrigatório em todas as situações encontradas.
- `itens_questionario`: itens, subitens e evidências usados na regra.
- `regra_de_identificacao`: condições objetivas e análise de suficiência das evidências.
- `referencias_matriz`: riscos, procedimentos e evidências da matriz.
- `criterios`: critérios específicos aplicáveis à situação.
- `encaminhamento`: recomendação proporcional e executável.

## Planilha de Checklists de Evidências

Quando a equipe precisar avaliar evidências com apoio de IA, manter uma planilha apartada:

- Caminho: `01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/matriz_verificaca_evidencias.xlsx`.
- Aba sugerida: uma aba única por protótipo ou por questão, como `Q1_Checklists`, salvo orientação diferente do usuário.
- Colunas obrigatórias: `id_avaliacao`, `questao_auditoria`, `situacao_encontrada`, `item_evidencia`, `descricao_avaliacao`, `prompt_checklist`.
- O `id_avaliacao` é o nome da coluna de resultado que será gerada pelo script para cada auditado. Não usar apenas `item_evidencia` como coluna de resultado, pois um mesmo item, como `q2102evi`, pode alimentar avaliações diferentes.

O prompt de checklist deve:

- Ser escrito em português do Brasil, com linguagem formal, impessoal e operacional.
- Determinar que a análise seja feita exclusivamente sobre a evidência do item indicado, sem buscar informações externas.
- Indicar o contexto da situação encontrada e o item de evidência.
- Reproduzir ou resumir a evidência esperada no questionário.
- Indicar os critérios aplicáveis da matriz.
- Usar checklist numerado com verificações objetivas.
- Pedir resultado binário como `Conforme` ou `Não conforme`.
- Determinar que `Conforme` só seja usado quando a evidência for existente, compatível e suficiente para todos os elementos essenciais da avaliação.
- Determinar que `Não conforme` seja usado quando a evidência for inexistente, ilegível, incompatível, desatualizada, meramente declaratória sem comprovação suficiente, ou quando faltar qualquer elemento essencial.
- Pedir justificativa sintética, lacunas e inconsistências.
- Solicitar saída em JSON quando o prompt for usado por API.
- Não permitir classificações intermediárias como `parcialmente conforme`, `parcialmente suficiente` ou `inconclusivo`.

Exemplo de linha conceitual:

| id_avaliacao | questao_auditoria | situacao_encontrada | item_evidencia | descricao_avaliacao | prompt_checklist |
| --- | --- | --- | --- | --- | --- |
| Q1-S1.1-q0101evi | Q1 - Estrutura e Governança de TIC | S1.1 - Ausência de formalização da área, unidade, setor ou função de TIC da organização. | q0101evi | Verificar se a evidência comprova formalização institucional da área, unidade, setor ou função de TIC. | Você é avaliador de evidências... |

## Regras de Qualidade

- Preservar linguagem formal, impessoal e em português do Brasil.
- Distinguir levantamento, avaliação de maturidade, auditoria de conformidade e auditoria operacional quando o escopo indicar essa diferença.
- Não criar achados para temas que a equipe definiu como apenas exploratórios.
- Não usar resposta declaratória como única evidência quando houver previsão de análise documental ou teste de amostra.
- Garantir que cada possível achado tenha pelo menos um risco e um caminho de evidência associado.
- Garantir que cada situação encontrada tenha regra objetiva de identificação e encaminhamento próprio.
- Garantir que toda situação encontrada contenha `severidade` com valor `alta`, `media` ou `baixa`; ausência desse campo é falha da matriz.
- Garantir que cada subquestão esteja coberta por informações requeridas e procedimentos.
- Evitar duplicidade: se dois achados dependem das mesmas evidências, avaliar se devem ser subachados ou um único achado mais bem delimitado.
- Manter consistência de numeração. Ao mover tema entre questões, atualizar todos os prefixos `R`, `IR`, `P`, `E` e `A`.
- Ao revisar critérios, não aceitar referência genérica a lei, framework ou dimensão. Indicar artigo, inciso, item, processo, prática ou princípio específico, acompanhado de breve descrição.

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
- A1: [Achado estruturante]
  situacoes_encontradas:
  - S1.1:
      descricao: Ausência ou fragilidade de [controle].
      severidade: alta
      itens_questionario: [qXXXX, qXXXXevi]
      regra_de_identificacao:
      - (qXXXX == valor)
      - ou qXXXXevi são inexistentes, incompatíveis ou insuficientes para comprovar [controle]
      referencias_matriz: [R1.1, P1, E1, P2, E2]
      criterios: [C1]
      encaminhamento: Recomendar que a organização [ação proporcional e executável].
```
