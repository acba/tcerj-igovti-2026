---
name: preencher-matriz-planejamento
description: Ensina Codex a criar, preencher, revisar e corrigir matriz de planejamento de auditoria governamental, especialmente em Markdown, DOCX convertido ou texto estruturado, e a manter planilha apartada de checklists de verificação de evidências. Use quando o usuário pedir para montar questões de auditoria, subquestões, riscos, fontes de informação, informações requeridas, critérios, procedimentos, evidências, possíveis achados, situações encontradas, regras de identificação, encaminhamentos ou prompts de avaliação de evidências por IA, ou para verificar a coerência e rastreabilidade entre esses campos em fiscalizações, auditorias, levantamentos ou trabalhos de controle externo.
---

# Preencher Matriz de Planejamento

## Objetivo

Produzir ou revisar matrizes de planejamento de auditoria governamental com linguagem simples, formal e impessoal, mantendo conexão explícita entre objetivo, questão de auditoria, riscos, fontes, informações requeridas, critérios, procedimentos, evidências e possíveis achados.

Tratar a matriz como instrumento de planejamento: não concluir achados reais sem evidência de execução. Usar "possíveis achados" apenas como hipóteses de auditoria vinculadas aos riscos e aos procedimentos previstos.

Quando solicitado, manter planilha apartada de checklists de verificação de evidências, usada para registrar prompts que serão enviados à API de modelo de IA ou aplicados por revisores humanos. A skill deve funcionar para qualquer tema de auditoria, levantamento ou fiscalização, não apenas para governança e gestão de TIC.

## Fluxo de Trabalho

1. Levantar contexto do trabalho.
   - Ler o arquivo da matriz existente antes de editar.
   - Se o usuário não informar o caminho da matriz, localizar o arquivo provável no repositório por nome, referências recentes ou estrutura do trabalho; confirmar por leitura do conteúdo, não por inferência de nome.
   - Ler documentos de planejamento, análise de riscos, questionário, metodologia, escopo, critérios ou deliberações citadas pelo usuário.
   - Para regras vinculadas a itens de questionário, formulário, base de dados ou sistema, conferir o texto, tipo, escala, opções e evidências previstas no instrumento aplicável antes de propor ou revisar regras.
   - Não inferir escopo apenas por nomes de arquivos.

2. Identificar a estrutura esperada.
   - Preservar o formato existente quando houver matriz prévia.
   - Quando criar uma matriz nova sem modelo local, usar seções nesta ordem: `questao`, `subquestoes`, `riscos`, `fontes_de_informacao`, `informacoes_requeridas`, `criterios`, `procedimentos`, `evidencias`, `variaveis_derivadas` (quando houver) e `possiveis_achados`.
   - Manter identificadores rastreáveis, como `Q1`, `R1.1`, `F1`, `IR1`, `C1`, `P1`, `E1`, `A1`, `S1.1`.
   - Em `possiveis_achados`, preferir poucos achados estruturantes por questão, compostos por `situacoes_encontradas`, quando isso reduzir fragmentação sem perder rastreabilidade.
   - Quando a questão tiver caráter de levantamento, usar `natureza: levantamento` e `gera_achado: false`, substituir `possiveis_achados` por campos como `o_que_a_analise_permite_dizer` e `limitacoes_e_cautelas`, e não criar `situacoes_encontradas`.

3. Definir ou revisar questões de auditoria.
   - Formular a questão como pergunta avaliável, vinculada ao objetivo e ao escopo.
   - Separar temas muito distintos em questões diferentes.
   - Evitar questão ampla demais que misture objetos, processos, unidades, riscos ou regimes normativos muito diferentes sem necessidade.
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
   - Quando uma expressão calculada for reutilizada nas regras de identificação, defini-la uma única vez em `variaveis_derivadas`, com apenas `nome`, `descricao` e `regra_de_calculo`; não repetir sua fórmula dentro das situações encontradas.
   - Toda situação encontrada deve apontar, em `referencias_matriz`, risco, procedimento e evidência: `referencias_matriz: [R3.2, P3, E3, P4, E4]`.
   - Toda situação encontrada deve indicar `descricao`, `severidade`, `itens_questionario` ou `fontes_de_verificacao`, `regra_de_identificacao`, `referencias_matriz`, `criterios`, `tipo_encaminhamento`, `fundamentacao_encaminhamento` e `encaminhamento`.
   - Usar `fundamentacao_encaminhamento` para a oração expositiva que vincula a providência aos critérios no relatório. Manter `encaminhamento` restrito à providência operativa iniciada por verbo.
   - Quando a força jurídica variar por público, manter a situação e sua regra factual únicas. Os campos `criterios`, `tipo_encaminhamento`, `fundamentacao_encaminhamento` e `encaminhamento` da situação formam a variante geral; declarar as exceções na lista `variantes`, aninhada na própria situação.
   - Cada variante aninhada herda da situação os campos jurídicos omitidos e substitui integralmente apenas os que declarar. Em especial, `criterios` substitui a lista geral, sem mesclagem. Não permitir `fundamentacao_encaminhamento` vazia, nem no caso geral nem quando declarada em variante, e nunca inferi-la dos critérios. Não permitir que variantes alterem descrição, severidade, itens, regra ou referências factuais.
   - Não declarar `id` nem `id_situacao` nas variantes. O motor gera o identificador com o código da situação e, quando houver um único segmento, com esse segmento; nos demais casos, usa o rótulo normalizado de `publico`.
   - Qualificar internamente cada critério pela questão (`Q6.C11`), ainda que a matriz e os relatórios exibam apenas `C11`. Declarar cada critério como objeto no bloco único `criterios`, com `id`, `descricao`, `natureza_fundamento` e `apto_a_fundamentar_determinacao`.
   - No mesmo bloco `criterios`, declarar os critérios condicionais acrescentando `publico` e `aplica_se`. Os seletores admitidos são apenas `segmentos`, `naturezas`, `tags_todas`, `tags_alguma` e `tags_excluidas`. Não criar blocos separados de metadados ou critérios específicos.
   - Em seletores, listas vazias ou campos ausentes não restringem. Há OR dentro de cada lista e AND entre dimensões preenchidas. Assim, `segmentos: [EXECUTIVO_ESTADUAL]` sozinho alcança todo esse segmento; natureza e tags, quando informadas, apenas estreitam o público.
   - Toda variante específica deve possuir `publico`, seletor `aplica_se` não vazio e ao menos um dos campos que podem ser sobrescritos. Exatamente uma variante específica pode ser aplicável ao par auditado/situação; na ausência dela, aplica-se a geral. Conflitos e colisões de identificadores gerados são erros bloqueantes.
   - Determinação deve conter ao menos um critério aplicável explicitamente marcado como apto a fundamentá-la. Essa validação não autoriza o motor a converter recomendações em determinações.
   - Questões de levantamento com `gera_achado: false` não devem conter `possiveis_achados`, `situacoes_encontradas`, `severidade`, `regra_de_identificacao` ou encaminhamentos individuais; devem conter procedimentos, evidências e limites suficientes para sustentar análise descritiva, agregada ou comparativa.

7. Manter checklists de verificação de evidências, quando solicitado.
   - Criar ou atualizar a planilha de checklists no caminho solicitado pelo usuário. Se não houver caminho definido, usar o mesmo diretório da matriz e nome descritivo, como `matriz_verificacao_evidencias.xlsx`.
   - Registrar uma linha por avaliação de evidência a ser realizada. Em regra, usar uma linha por par `situação encontrada` + `item de evidência`, pois a mesma evidência pode comprovar finalidades distintas em situações diferentes.
   - Usar as colunas: `id_avaliacao`, `questao_auditoria`, `situacao_encontrada`, `item_evidencia`, `descricao_avaliacao`, `prompt_checklist`.
   - Montar `id_avaliacao` em padrão estável, como `Qn-Sn.n-itemevi`, `Qn-Sn.n-documento`, ou outro padrão coerente com o instrumento usado.
   - O `prompt_checklist` deve orientar a avaliação exclusiva da evidência fornecida, mencionar o contexto da situação encontrada, resumir a evidência esperada no questionário e conter checklist objetivo.
   - O prompt deve solicitar saída estruturada em JSON, com `resultado` binário igual a `Conforme` ou `Não conforme`, além de `justificativa_sintetica`, `elementos_comprovados`, `lacunas` e `inconsistencias`.
   - Usar o `id_avaliacao` como coluna de resultado no processamento posterior, pois o mesmo item de evidência pode ter avaliações distintas para situações encontradas diferentes.
   - Quando a matriz consumir o resultado de avaliação de evidência, referenciar o alvo no atributo `regra_de_identificacao`, por exemplo: `avaliacao[Q2-S2.3-doc001] == "Não conforme"`.

## Estruturas Recomendadas

Cada achado estruturante pode ser composto por situações encontradas (`S1.1`, `S1.2` etc.). A ocorrência de uma ou mais situações pode caracterizar o achado estruturante, sem fragmentar o relatório em muitos achados autônomos.

Exemplo de situação encontrada:

```yaml
- S1.1:
    descricao: Ausência de formalização da unidade, função, processo ou controle avaliado.
    severidade: alta
    itens_questionario: [q0101, q0101evi]
    regra_de_identificacao:
    - (q0101 == F)
    - ou q0101evi são inexistentes, incompatíveis ou insuficientes para comprovar a formalização do objeto avaliado
    referencias_matriz: [R1.1, P1, E1, P2, E2]
    criterios: [C1, C5, C9]
    tipo_encaminhamento: Recomendação
    encaminhamento: formalize a unidade, função, processo ou controle avaliado em instrumento normativo, ato administrativo, organograma, manual, procedimento ou documento equivalente
```

Exemplo de questão de levantamento sem achado:

```yaml
natureza: levantamento
gera_achado: false
questao: QT. O conjunto avaliado apresentou evolução mensurável, em termos agregados, em relação ao ciclo anterior?

subquestoes:
- Houve evolução, estabilidade ou regressão agregada nos indicadores comparáveis?
- As diferenças metodológicas limitam a comparação dos resultados?

fontes_de_informacao:
- F1: Resultados do ciclo atual.
- F2: Resultados do ciclo anterior.

informacoes_requeridas:
- IR1: Universo comum de unidades avaliadas nos dois ciclos; [F1, F2]
- IR2: Indicadores comparáveis e limitações metodológicas; [F1, F2]

procedimentos:
- P1: Cruzar as unidades avaliadas nos dois ciclos; [IR1]
- P2: Calcular variação agregada dos indicadores comparáveis; [IR2]

evidencias:
- E1: Relação das unidades presentes nos dois ciclos; [P1]
- E2: Tabelas ou painéis com variação agregada e limitações; [P2]

o_que_a_analise_permite_dizer:
- Se houve evolução, estabilidade ou regressão agregada.
- Quais limitações reduzem a força das conclusões.
```

## Convenções de Instrumentos e Questionários

Quando a matriz for vinculada a questionário, formulário ou base estruturada, usar convenções explícitas para referenciar itens. O padrão abaixo é apenas um exemplo e deve ser adaptado ao instrumento do trabalho:

- `qXXXX`: item principal do questionário.
- `qXXXXext[A]`: subitem A de questão do tipo `adoption`/`detail_options`.
- `qXXXX[A]`: subitem A de questão do tipo `array`.
- `qXXXXevi`: evidência anexada à questão `qXXXX`.
- `qXXXXeviA`: evidência específica vinculada ao subitem `qXXXX[A]`.

Para subitens condicionais do tipo `adoption/detail_options`, a matriz pode usar regras como `(qXXXXext[A] != Sim)` apenas quando a metodologia do trabalho definir que subitem não marcado, não habilitado ou não aplicável será normalizado como valor diferente de `Sim`.

Ao criar regras, prefira condições objetivas com códigos ou subitens do questionário. Evite formulações vagas como "q0101 indica inexistência de formalização" quando for possível escrever `(q0101 == F)`.

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

Declarar todos os critérios em uma única lista estruturada. Os quatro primeiros campos são obrigatórios. `publico` e `aplica_se` devem aparecer somente em critérios cuja aplicação seja condicionada:

```yaml
criterios:
- id: C1
  descricao: >-
    COBIT 2019, APO01.04 - Definir e implementar as estruturas organizacionais:
    estabelecer estruturas necessárias para apoiar a governança e a gestão de TI.
  natureza_fundamento: boa_pratica
  apto_a_fundamentar_determinacao: false
- id: C11
  descricao: >-
    Norma aplicável especificamente ao Poder Executivo Estadual.
  natureza_fundamento: norma_regulamentar_vinculante
  apto_a_fundamentar_determinacao: true
  publico: Poder Executivo Estadual
  aplica_se:
    segmentos: [EXECUTIVO_ESTADUAL]
```

Usar o escalar YAML dobrado `>-` para descrições longas ou que contenham dois-pontos. Não usar os blocos legados `metadados_criterios` ou `criterios_especificos`.

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

### variaveis_derivadas

Usar esta seção somente quando uma expressão calculada for reutilizada nas regras de identificação. Posicioná-la depois de `evidencias` e antes de `possiveis_achados`. Manter cada definição limitada a `nome`, `descricao` e `regra_de_calculo`, em sincronia com o mapa de verificação.

```yaml
variaveis_derivadas:
- nome: existe_controle
  descricao: Indica que a organização declarou possuir o controle avaliado.
  regra_de_calculo: (qXXXX == Sim) | (qXXXX == Parcialmente)
```

### possiveis_achados

Formular como hipótese de deficiência estruturante, com escopo claro e rastreável. Quando houver muitas fragilidades relacionadas, preferir um achado estruturante com situações encontradas em vez de dezenas de achados pequenos.

Bom:

- `A4: Processo avaliado incipiente, sem controles mínimos formalizados e executados`

Fraco:

- `Problemas em contratações.`

### situacoes_encontradas

Desdobrar o achado estruturante em situações objetivas, mensuráveis por questionário, base de dados, análise documental, entrevista, inspeção, teste de amostra ou outro procedimento previsto.

Cada situação deve conter:

- `descricao`: condição negativa específica, em linguagem de achado potencial.
- `severidade`: `alta`, `media` ou `baixa`. Campo obrigatório em todas as situações encontradas.
- `itens_questionario` ou `fontes_de_verificacao`: itens, subitens, evidências, documentos, bases, amostras ou testes usados na regra.
- `regra_de_identificacao`: condições objetivas e análise de suficiência das evidências.
- `referencias_matriz`: riscos, procedimentos e evidências da matriz.
- `criterios`: critérios específicos aplicáveis à situação.
- `tipo_encaminhamento`: `Determinação` ou `Recomendação`, conforme a natureza da providência.
- `fundamentacao_encaminhamento`: oração expositiva completa que relaciona a providência aos fundamentos efetivamente aplicáveis, sem identificadores internos.
- `encaminhamento`: providência proporcional e executável, iniciada diretamente por verbo no imperativo, sem repetir "Determinar que" ou "Recomendar que".

Quando houver tratamento jurídico específico por público, acrescentar `variantes` ao final da situação. `publico` e `aplica_se` são obrigatórios; `criterios`, `tipo_encaminhamento`, `fundamentacao_encaminhamento` e `encaminhamento` são opcionais e sobrescrevem os campos gerais quando declarados:

```yaml
      variantes:
      - publico: Poder Executivo Estadual
        aplica_se:
          segmentos: [EXECUTIVO_ESTADUAL]
        criterios: [C1, C4, C11]
      - publico: Poder Judiciário Estadual
        aplica_se:
          segmentos: [JUDICIARIO_ESTADUAL]
        criterios: [C1, C4, C12]
        tipo_encaminhamento: Determinação
```

Posicionar `variantes` como o último campo da situação. Não usar o bloco global legado `variantes_especificas`.

Na classificação do encaminhamento, observar a Deliberação TCE-RJ nº 346/2024:

- Usar `Determinação` quando a medida tiver natureza mandamental e impuser providência concreta e imediata para prevenir ou corrigir irregularidade, remover seus efeitos ou impedir ato irregular. A proposta deve indicar ação ou abstenção necessária e, quando aplicável, prazo para cumprimento.
- Usar `Recomendação` quando a medida tiver natureza colaborativa e apresentar oportunidade de melhoria voltada ao aperfeiçoamento da gestão, preservando a avaliação de conveniência e oportunidade pelo destinatário.
- Não classificar automaticamente pela severidade. Considerar a natureza do critério, a força das evidências, a necessidade de providência imediata e a viabilidade da medida.
- Quando a verificação se apoiar apenas em resposta declaratória e não demonstrar irregularidade concreta que exija correção imediata, preferir `Recomendação`.

## Planilha de Checklists de Evidências

Quando a equipe precisar avaliar evidências com apoio de IA, manter uma planilha apartada:

- Caminho: definido pelo usuário ou, por padrão, no mesmo diretório da matriz.
- Aba recomendada: uma única aba consolidada chamada `Avaliacoes`, contendo as avaliações de todas as questões de auditoria. Se o trabalho exigir outro formato, registrar a convenção e manter consistência.
- Colunas obrigatórias: `id_avaliacao`, `questao_auditoria`, `situacao_encontrada`, `item_evidencia`, `descricao_avaliacao`, `prompt_checklist`.
- O `id_avaliacao` é o nome da coluna de resultado que será gerada pelo script para cada auditado. Não usar apenas `item_evidencia` como coluna de resultado, pois um mesmo item, como `doc001` ou `qXXXXevi`, pode alimentar avaliações diferentes.

O prompt de checklist deve:

- Ser escrito em português do Brasil, com linguagem formal, impessoal e operacional.
- Iniciar de forma genérica, por exemplo: "Você é avaliador de evidências de auditoria."
- Determinar que a análise seja feita exclusivamente sobre a evidência fornecida, sem buscar informações externas.
- Indicar o contexto da situação encontrada.
- Reproduzir ou resumir a evidência esperada no questionário.
- Usar checklist numerado com verificações objetivas.
- Pedir resultado binário como `Conforme` ou `Não conforme`.
- Determinar que `Conforme` só seja usado quando a evidência for existente, compatível e suficiente para todos os elementos essenciais da avaliação.
- Determinar que `Não conforme` seja usado quando a evidência for inexistente, ilegível, incompatível, desatualizada, meramente declaratória sem comprovação suficiente, ou quando faltar qualquer elemento essencial.
- Pedir justificativa sintética, lacunas e inconsistências.
- Solicitar saída em JSON quando o prompt for usado por API.
- Não permitir classificações intermediárias como `parcialmente conforme`, `parcialmente suficiente` ou `inconclusivo`.
- Não repetir dentro do prompt os metadados que já estão nas colunas da planilha, especialmente `id_avaliacao`, `item_evidencia` e a relação de critérios da matriz.

Exemplo de linha conceitual:

| id_avaliacao | questao_auditoria | situacao_encontrada | item_evidencia | descricao_avaliacao | prompt_checklist |
| --- | --- | --- | --- | --- | --- |
| Q1-S1.1-doc001 | Q1 - Tema Avaliado | S1.1 - Ausência de formalização do controle avaliado. | doc001 | Verificar se a evidência comprova formalização institucional do controle avaliado. | Você é avaliador de evidências... |

## Regras de Qualidade

- Preservar linguagem formal, impessoal e em português do Brasil.
- Distinguir levantamento, avaliação de maturidade, auditoria de conformidade e auditoria operacional quando o escopo indicar essa diferença.
- Não criar achados para temas que a equipe definiu como apenas exploratórios.
- Não usar resposta declaratória como única evidência quando houver previsão de análise documental ou teste de amostra.
- Garantir que cada possível achado tenha pelo menos um risco e um caminho de evidência associado.
- Garantir que cada situação encontrada tenha regra objetiva de identificação, `tipo_encaminhamento` válido e encaminhamento próprio.
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
- id: C1
  descricao: >-
    Critério aplicável, item ou prática específica.
  natureza_fundamento: boa_pratica
  apto_a_fundamentar_determinacao: false

procedimentos:
- P1: Aplicar questionário para verificar a existência de [controle]; [IR1]
- P2: Analisar documentação para verificar vigência, aprovação e conteúdo mínimo, de acordo com C1; [IR2]

evidencias:
- E1: Resposta negativa ou insuficiente sobre [controle]; [P1]
- E2: Ausência, desatualização ou insuficiência da documentação de [controle]; [P2]

variaveis_derivadas:
- nome: existe_controle
  descricao: Indica que a organização declarou possuir o controle avaliado.
  regra_de_calculo: (qXXXX == Sim) | (qXXXX == Parcialmente)

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
      tipo_encaminhamento: Recomendação
      encaminhamento: [ação proporcional e executável iniciada por verbo]
```
