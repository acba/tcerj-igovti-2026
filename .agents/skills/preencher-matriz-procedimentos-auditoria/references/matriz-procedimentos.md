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

### Ações de Verificação

Cabeçalho na linha 3:

| coluna | uso |
|---|---|
| `id` | identificador `AV01`, `AV02` |
| `id_fonte_informacao` | fonte onde a informação será buscada |
| `acao_exclusiva_auditados` | lista opcional de auditados aos quais a ação se aplica |
| `auditado_inexistente_e_achado` | `TRUE` se ausência do auditado na fonte configura achado |
| `descricao_auditado_inexistente` | evidência a registrar quando o auditado não existir na fonte |
| `informacao_requerida` | coluna/campo/target analisado, como `q1001` ou `Q2-S2.1-q1001evi` |
| `criterio` | critério aplicável, preferencialmente textual e específico |
| `descricao_evidencia` | evidência que será registrada quando a ação for aplicada |
| `complemento_evidencia` | complemento opcional |
| `descricao_situacao_inconforme` | frase que descreve a situação encontrada quando a ação for inconforme |
| `situacao_inconforme` | valor ou expressão que caracteriza inconformidade |
| `situacao_encontrada_nan_e_achado` | `TRUE` se célula vazia/NaN configura achado |
| `decodifica_sit_encontrada` | regra opcional para decodificar valor bruto |
| `tipo_encaminhamento` | `Recomendação`, `Determinação` ou outro tipo adotado pelo trabalho |
| `pre_encaminhamento` | texto opcional antes do encaminhamento |
| `encaminhamento` | providência proposta quando a ação/situação ocorrer |

## Convenções

- Manter cabeçalhos na linha 3 para compatibilidade com planilhas existentes.
- Usar `questionario` para respostas declaradas e colunas de upload do LimeSurvey.
- Usar `avaliacao_evidencias` para resultados de prompts de avaliação documental.
- Usar `questionario_e_avaliacao_evidencias` quando a regra combinar resposta declarada e resultado de avaliação de evidência na mesma expressão.
- Preferir uma ação por condição operacionalmente testável.
- Em regras compostas, preservar a expressão original em `situacao_inconforme` quando não houver decomposição segura.
- Manter `logica_achado` como expressão com IDs de ações. Use `|` para qualquer ação suficiente para caracterizar o achado e `&` apenas quando o achado depender de composição obrigatória.
- Não usar a planilha como relatório final; ela alimenta apuração e revisão humana.
