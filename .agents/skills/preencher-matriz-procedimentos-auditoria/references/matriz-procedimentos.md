# Contrato Da Matriz De Procedimentos

Use esta referência ao criar ou revisar planilhas semelhantes a `entrada_mapa-verificacao-achados.xlsx`.

## Abas

### Fontes de Informação

Cabeçalho na linha 3:

| coluna | uso |
|---|---|
| `id` | identificador curto da fonte, como `questionario` ou `avaliacao_evidencias` |
| `descricao` | nome legível da fonte |
| `filepath` | caminho relativo do arquivo/base a ser analisado |
| `chave_jurisdicionado` | coluna usada para associar registro ao auditado |

### Procedimentos de Auditoria

Cabeçalho na linha 3:

| coluna | uso |
|---|---|
| `id` | identificador `PA01`, `PA02` |
| `descricao` | descrição operacional do procedimento |
| `logica_achado` | composição das ações de verificação, como `(AV01 \| AV02)` |
| `numero_achado` | número sequencial ou planejado do achado |
| `nome_achado` | nome do possível achado |

### Variáveis Temporárias

Cabeçalho na linha 3:

| coluna | uso |
|---|---|
| `id` | identificador `VT01`, `VT02` |
| `id_fonte_informacao` | fonte cujas colunas alimentam o cálculo |
| `nome` | nome da coluna temporária criada em memória |
| `expressao` | expressão calculada com colunas originais ou variáveis definidas anteriormente |
| `descricao` | significado do valor calculado |

As variáveis são calculadas na ordem das linhas. Uma variável pode utilizar outra definida anteriormente. Elas existem apenas durante o processamento e não alteram o arquivo da fonte de informação.

### Motivos do Relatório

Cabeçalho na linha 3:

| coluna | uso |
|---|---|
| `id` | identificador do motivo, como `MR001` |
| `id_procedimento` | procedimento ao qual o motivo se vincula, como `PA01` |
| `descricao_situacao_inconforme` | situação encontrada em que o motivo deve aparecer |
| `ordem` | ordem de exibição do motivo dentro da situação |
| `condicao_exibicao` | expressão lógica com ações de verificação, como `AV84` ou `AV04 & ~AV84` |
| `acoes_referencia` | ações cujas evidências serão citadas no relatório, como `AV04, AV84` |
| `texto_motivo` | texto a ser exibido no relatório; pode usar variáveis Jinja com os dados das ações, como `{{ AV01.situacao_encontrada }}` |
| `ativo` | `TRUE` ou `FALSE` para ativar ou desativar a regra sem removê-la |

Essa aba é opcional. Quando houver regras para uma situação encontrada, elas substituem, no relatório, a descrição bruta das ações de verificação daquela situação. Quando não houver regras aplicáveis, o sistema preserva o comportamento padrão e usa as descrições das evidências das ações que materializaram a situação.

### Ações de Verificação

Cabeçalho na linha 3:

| coluna | uso |
|---|---|
| `id` | identificador `AV01`, `AV02` |
| `id_fonte_informacao` | fonte onde a informação será buscada |
| `acao_exclusiva_auditados` | lista opcional de auditados aos quais a ação se aplica |
| `auditado_inexistente_e_achado` | `TRUE` se ausência do auditado na fonte configura achado |
| `descricao_auditado_inexistente` | evidência a registrar quando o auditado não existir na fonte |
| `informacao_requerida` | uma única coluna, campo ou variável analisada, como `q1001ext[A]` ou `total_TI` |
| `id_situacao` | identificador estável da situação, como `S6.4` |
| `criterio` | critério aplicável, preferencialmente textual e específico |
| `descricao_evidencia` | evidência que será registrada quando a ação for aplicada; aceita `@`, `{situacao_encontrada}`, `{item_avaliado}` e, quando existirem colunas auxiliares, `{avaliacao_justificativa}`, `{resposta_afirmada}` e `{pratica}` |
| `complemento_evidencia` | complemento opcional |
| `descricao_situacao_inconforme` | frase que descreve a situação encontrada quando a ação for inconforme |
| `situacao_inconforme` | valor ou expressão que caracteriza inconformidade |
| `situacao_encontrada_nan_e_achado` | `TRUE` se célula vazia/NaN configura achado |
| `decodifica_sit_encontrada` | regra opcional para decodificar valor bruto |
| `tipo_encaminhamento` | `Recomendação` ou `Determinação`, conforme atributo explícito da situação encontrada |
| `pre_encaminhamento` | campo legado sem uso na fundamentação dos encaminhamentos por situação |
| `encaminhamento` | providência proposta quando a ação/situação ocorrer |

Os campos `criterio`, `tipo_encaminhamento`, `pre_encaminhamento` e `encaminhamento` desta aba podem ser preservados para compatibilidade com produtos legados. Quando existirem as abas jurídicas abaixo, elas prevalecem após a identificação factual da situação. A fundamentação narrativa deve ser declarada na matriz de planejamento e sincronizada na aba `Variantes de Encaminhamento`, pois pertence à situação, não à ação.

### Critérios de Auditoria

Cabeçalho na linha 3. Registra `id_criterio` qualificado pela questão, `id_exibicao`, `questao`, `publico`, `descricao`, `natureza_fundamento`, `apto_a_fundamentar_determinacao` e os seletores `segmentos`, `naturezas`, `tags_todas`, `tags_alguma` e `tags_excluidas`. Esses dados são sincronizados do bloco estruturado único `criterios` da matriz de planejamento; critérios específicos são os itens que também declaram `publico` e `aplica_se`.

### Variantes de Encaminhamento

Cabeçalho na linha 3. Registra `id_variante`, `id_situacao`, `geral`, `publico`, os cinco seletores, `criterios`, `tipo_encaminhamento`, `fundamentacao_encaminhamento` e `encaminhamento`. Cada situação deve possuir exatamente uma variante geral. Na matriz, as específicas ficam aninhadas em `situacoes_encontradas[].variantes`; na planilha, são materializadas com os campos herdados e com identificador gerado automaticamente. Uma variante específica substitui a geral quando for a única aplicável ao auditado.

## Convenções

- Manter cabeçalhos na linha 3 para compatibilidade com planilhas existentes.
- Usar `questionario` para respostas declaradas e colunas de upload do LimeSurvey.
- Usar `avaliacao_evidencias` para resultados de prompts de avaliação documental.
- Usar `questionario_e_avaliacao_evidencias` quando a regra combinar resposta declarada e resultado de avaliação de evidência na mesma expressão.
- Preferir uma ação por condição operacionalmente testável.
- Cada ação deve consultar exatamente uma coluna da fonte de informação. Se a regra utilizar N colunas, criar N ações.
- Repetir nas ações oriundas da mesma situação encontrada a descrição e o `id_situacao`. Não duplicar ações em razão de critérios específicos por público.
- Nos seletores jurídicos, campos ausentes ou listas vazias são neutros; valores dentro da mesma lista operam por OR e dimensões preenchidas operam por AND.
- Não usar expressões livres nem `eval` para aplicabilidade. O cadastro materializa apenas `segmento_institucional`, `natureza_administrativa` e `tags_aplicabilidade`.
- Em regras compostas, preservar a expressão original em `situacao_inconforme` quando não houver decomposição segura.
- Manter em `situacao_inconforme` apenas a condição aplicável à coluna da própria ação.
- Preencher `situacao_inconforme` com os valores literais encontrados na fonte. Em itens-base de escolha única, converter o código da alternativa para seu texto completo, por exemplo `F` para `f) Inexistente / Informal: ...`; para negação, usar `~(<texto completo>)`.
- Em detalhamentos de itens `adoption`, usar os valores `Sim`, `Não` e `N/A` conforme a regra. Em matrizes `sim_nao`, usar `Sim` ou `Não`.
- Montar `logica_achado` substituindo cada condição da regra pelos IDs das ações, preservando `&`, `|` e parênteses. Combinar as diferentes situações encontradas do achado com `|`.
- Usar `Motivos do Relatório` para traduzir, de forma declarativa, as ações de verificação em motivos textuais acessíveis ao leitor do relatório, evitando lógica específica de achado no código Python.
- Em `Motivos do Relatório`, preencher `condicao_exibicao` com ações da própria lógica do achado sempre que possível. Usar negação, como `AV04 & ~AV84`, para evitar motivos duplicados quando uma avaliação documental mais específica prevalecer sobre uma resposta declarada.
- Em `acoes_referencia`, listar apenas ações cujas evidências devem aparecer entre parênteses no relatório como `E1`, `E2` etc.; para situações com motivos declarativos, a seção de evidências do achado também será limitada a essas ações referenciadas.
- Para ações baseadas no painel de avaliação de evidências, preferir redação que diferencie a resposta originalmente afirmada da conclusão da Equipe, por exemplo: `A organização declarou "{resposta_afirmada}" no {item_avaliado}, mas a evidência encaminhada foi considerada insuficiente para comprovar que {pratica}. Justificativa da avaliação: {avaliacao_justificativa}`.
- Preencher `tipo_encaminhamento` exclusivamente com `Determinação` ou `Recomendação`.
- Redigir `encaminhamento` como providência iniciada diretamente por verbo, sem repetir os prefixos "Determinar que" ou "Recomendar que".
- Não usar a planilha como relatório final; ela alimenta apuração e revisão humana.
