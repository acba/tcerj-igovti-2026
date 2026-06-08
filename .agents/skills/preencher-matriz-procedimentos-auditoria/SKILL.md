---
name: preencher-matriz-procedimentos-auditoria
description: Criar, preencher, revisar e corrigir matriz de procedimentos de auditoria em planilha Excel, com abas de Fontes de Informação, Procedimentos de Auditoria e Ações de Verificação, a partir de matriz de planejamento em Markdown/YAML-like. Use quando o usuário pedir para transformar matriz de planejamento em mapa de verificação, mapa de procedimentos, matriz de procedimentos, ações de verificação, composição de achados, lógica de achado, fontes de informação analisadas, ou planilha semelhante a entrada_mapa-verificacao-achados.xlsx.
---

# Preencher Matriz De Procedimentos De Auditoria

## Objetivo

Gerar ou revisar uma planilha operacional que conecte fontes de informação, ações de verificação e achados prováveis planejados. A matriz é instrumento de execução: não declarar achados reais sem dados processados.

## Workflow

1. Ler a matriz de planejamento antes de gerar a planilha.
   - Confirmar questões, possíveis achados, situações encontradas, `regra_de_identificacao`, `criterios`, `referencias_matriz` e `encaminhamento`.
   - Se houver questionário, base ou planilha de avaliações de evidências, ler seus cabeçalhos quando necessário para confirmar códigos como `q1001`, `q1001ext[E]`, `q1001evi` e `avaliacao[Q2-S2.1-q1001evi]`.

2. Ler o contrato da planilha em `references/matriz-procedimentos.md` quando criar ou alterar o arquivo Excel.

3. Usar `scripts/gerar_matriz_procedimentos.py` para uma primeira versão quando a fonte for uma matriz Markdown no padrão de `matriz_planejamento.md`.

4. Revisar a planilha gerada.
   - Conferir se todos os possíveis achados viraram linhas em `Procedimentos de Auditoria`.
   - Conferir se cada regra relevante de `regra_de_identificacao` virou uma ação em `Ações de Verificação`.
   - Conferir expressões complexas com `&`, `|`, precondições ou `avaliacao[...]`; o script preserva a expressão, mas a equipe deve validar se a lógica operacional está adequada.
   - Conferir divergências entre a matriz e planilhas de prompts de evidência antes de tratar a matriz como final.

## Geração Rápida

Exemplo:

```bash
python3 .agents/skills/preencher-matriz-procedimentos-auditoria/scripts/gerar_matriz_procedimentos.py \
  01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/matriz_planejamento.md \
  02-Execucao/02-Testes_Auditoria/matriz_procedimentos_auditoria.xlsx
```

Com caminhos de fontes explícitos:

```bash
python3 .agents/skills/preencher-matriz-procedimentos-auditoria/scripts/gerar_matriz_procedimentos.py \
  01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/matriz_planejamento.md \
  02-Execucao/02-Testes_Auditoria/matriz_procedimentos_auditoria.xlsx \
  --questionario-filepath 01-Coleta_Dados/20260607-respostas-questionario.xlsx \
  --avaliacao-filepath 02-Testes_Auditoria/avaliacao_evidencias/resultados_avaliacao_evidencias.xlsx
```

## Regras De Mapeamento

- `Fontes de Informação`: registrar cada tabela/arquivo analisado e a coluna que identifica o auditado.
- `Procedimentos de Auditoria`: criar um procedimento por possível achado (`A1`, `A2` etc.), com `logica_achado` composta pelos IDs das ações de verificação aplicáveis.
- `Ações de Verificação`: criar ações a partir das regras das situações encontradas (`S1.1`, `S1.2` etc.).
- Regras com códigos de questionário usam a fonte `questionario`.
- Regras com `avaliacao[ID]` usam a fonte `avaliacao_evidencias`.
- Quando uma regra mistura fonte de questionário e avaliação de evidência, usar a fonte composta `questionario_e_avaliacao_evidencias`, preservar a expressão em `situacao_inconforme` e revisar manualmente.
- Usar `tipo_encaminhamento` como `Recomendação` quando o encaminhamento iniciar por "Recomendar"; usar `Determinação` quando iniciar por "Determinar".

## Validação

Depois de gerar ou editar:

```bash
python3 .agents/skills/preencher-matriz-procedimentos-auditoria/scripts/gerar_matriz_procedimentos.py --check \
  02-Execucao/02-Testes_Auditoria/matriz_procedimentos_auditoria.xlsx
```

Verificar manualmente:

- A aba `Ações de Verificação` tem cabeçalho na linha 3.
- Toda ação tem `id`, `id_fonte_informacao`, `informacao_requerida`, `criterio`, `descricao_evidencia`, `descricao_situacao_inconforme`, `situacao_inconforme`, `tipo_encaminhamento` e `encaminhamento`.
- Toda ação citada em `logica_achado` existe.
- Toda fonte citada em `Ações de Verificação` existe em `Fontes de Informação`.
- Nenhum texto de achado real foi afirmado como conclusão de execução.

## Recursos

- `references/matriz-procedimentos.md`: contrato das abas, colunas e convenções de preenchimento.
- `scripts/gerar_matriz_procedimentos.py`: gera e valida planilhas de matriz de procedimentos.
