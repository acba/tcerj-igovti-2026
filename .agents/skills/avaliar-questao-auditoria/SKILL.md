---
name: avaliar-questao-auditoria
description: Avaliar e revisar criticamente uma questão de auditoria em matriz de planejamento, incluindo questão, subquestões, riscos, fontes, informações requeridas, critérios, procedimentos, evidências, possíveis achados, situações encontradas, regras de identificação, encaminhamentos e prompts/checklists associados na planilha de verificação de evidências. Use quando o usuário pedir para reavaliar, revisar, criticar, auditar, validar ou melhorar uma questão da matriz de planejamento, especialmente no contexto iGovTI 2026.
---

# Avaliar Questão de Auditoria

## Objetivo

Avaliar criticamente uma questão da matriz de planejamento e seus artefatos associados, com linguagem formal, impessoal e imparcial. A avaliação deve verificar se a questão é respondível, rastreável, mensurável, proporcional e coerente com o questionário iGovTI e com a planilha de checklists de evidências.

## Fontes A Ler

Antes de concluir, ler os artefatos aplicáveis:

- Matriz principal: `01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/matriz_planejamento.md`.
- Questionário iGovTI: `01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md`.
- Planilha de checklists: `01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/matriz_verificaca_evidencias.xlsx`, quando a questão tiver evidências avaliadas por prompt.
- Documentos normativos ou referenciais citados, quando a especificidade ou atualidade do critério precisar ser confirmada.

Não avaliar por inferência a partir de nomes de arquivos. Se o usuário colar uma questão no prompt, confrontar com os arquivos locais quando isso for relevante.

## Fluxo

1. Identificar a questão avaliada.
   - Se o usuário informar `Q2`, `Questão 02` ou similar, extrair a seção correspondente da matriz.
   - Se o usuário colar a questão, usar o texto colado e apontar divergências relevantes em relação ao arquivo local, se houver.

2. Levantar os itens do questionário.
   - Conferir todos os `qXXXX`, `qXXXXext[A]`, `qXXXX[A]` e `qXXXXevi` citados.
   - Verificar tipo do item (`single`, `multi`, `array`, `adoption`) e texto de `evidence_text`.
   - Para `adoption/detail_options`, considerar válida a convenção de que `(qXXXXext[A] != Sim)` cobre subitem não marcado e subitem não habilitado pela resposta principal, desde que a base de apuração normalize ambos como diferente de `Sim`.

3. Levantar checklists de evidência.
   - Abrir a planilha `.xlsx` com `openpyxl` ou ferramenta equivalente.
   - Confirmar que a planilha usa uma única aba consolidada chamada `Avaliacoes`; múltiplas abas por questão, como `Q1_Checklists`, devem ser apontadas como desconformidade estrutural.
   - Filtrar as linhas da questão avaliada pelo campo `questao_auditoria` ou pelo prefixo de `id_avaliacao`.
   - Conferir colunas obrigatórias: `id_avaliacao`, `questao_auditoria`, `situacao_encontrada`, `item_evidencia`, `descricao_avaliacao`, `prompt_checklist`.
   - Conferir se o `id_avaliacao` é o target usado nas regras, não apenas o `item_evidencia`.

## Rubrica De Avaliação

Avaliar, no mínimo:

1. **Respondibilidade da questão:** se a questão de auditoria pode ser respondida com informações requeridas, procedimentos, respostas e evidências previstas.
2. **Cobertura das subquestões:** se cada subquestão tem informação requerida, procedimento e evidência correspondente.
3. **Critérios:** se cada critério é específico, com artigo, inciso, item, processo, prática, salvaguarda, princípio ou deliberação concreta, seguido de breve descrição.
4. **Informações requeridas:** se todas foram mencionadas e usadas nos procedimentos.
5. **Procedimentos:** se todos foram usados nas evidências e, quando houver achado, nas situações encontradas.
6. **Coesão:** se riscos ou critérios de comparabilidade, informações requeridas, procedimentos, evidências, situações encontradas ou resultados esperados se conectam sem lacunas ou redundâncias relevantes.
7. **Natureza da questão:** se a questão gera achado ou possui `natureza: levantamento` e `gera_achado: false`; nesse último caso, não exigir `possiveis_achados`, `situacoes_encontradas`, `severidade`, `regra_de_identificacao` ou encaminhamentos.
8. **Situações encontradas:** quando a questão gera achado, se são coerentes, válidas, essenciais, proporcionais e suficientes para responder à questão e às subquestões.
9. **Severidade:** quando a questão gera achado, se toda situação encontrada possui `severidade` preenchida com `alta`, `media` ou `baixa`, e se o valor é proporcional à criticidade da situação.
10. **Objetividade das regras:** quando a questão gera achado, se cada situação pode ser verificada por respostas do iGovTI, evidências anexadas ou avaliações binárias de evidência.
11. **Suficiência do achado estruturante:** quando a questão gera achado, se o possível achado responde negativamente à questão quando uma ou mais situações ocorrem.
12. **Questões de levantamento:** quando `gera_achado: false`, se `o_que_a_analise_permite_dizer`, `limitacoes_e_cautelas`, evidências e procedimentos são suficientes para sustentar conclusões descritivas, agregadas ou comparativas.
13. **Prompts de evidência:** se cada evidência que exige análise documental tem avaliação própria na planilha; em questões de levantamento sem situações encontradas, registrar que a ausência de prompts é aceitável quando não houver avaliação documental binária por achado.

## Avaliação Dos Prompts

Para cada linha da planilha associada à questão, verificar:

- `id_avaliacao` único, estável e aderente ao padrão `Qn-Sn.n-itemevi`.
- `questao_auditoria` e `situacao_encontrada` correspondem à matriz.
- `item_evidencia` existe no questionário ou na matriz.
- `descricao_avaliacao` sintetiza claramente o teste documental.
- `prompt_checklist` começa com formulação genérica, como "Você é avaliador de evidências de auditoria", sem restringir indevidamente a avaliação a uma fiscalização específica.
- `prompt_checklist` determina análise exclusiva da evidência fornecida.
- O prompt menciona a situação e a evidência esperada.
- O prompt não repete metadados que já estão nas colunas da planilha, especialmente `id_avaliacao`, `item_evidencia` e a relação de critérios da matriz.
- O checklist é objetivo, verificável e compatível com a situação encontrada.
- A saída exigida é JSON com `resultado` binário `Conforme` ou `Não conforme`.
- O prompt veda classificações intermediárias e define quando usar `Não conforme`.
- A regra de identificação da situação usa o target `avaliacao[id_avaliacao] == "Não conforme"` quando depende da avaliação da evidência.

Apontar avaliações ausentes, duplicadas, amplas demais, fracas, incompatíveis com a situação ou com risco de gerar resultado ambíguo.

## Relatório De Saída

Estruturar a resposta assim, adaptando ao tamanho da tarefa:

- **Conclusão Geral:** síntese sobre maturidade da questão e principais fragilidades.
- **Achados Da Revisão:** problemas, lacunas ou riscos metodológicos, em ordem de relevância.
- **Avaliação Por Critério:** resposta objetiva para os itens da rubrica.
- **Avaliação De Severidade:** quando aplicável, confirmação de presença do campo `severidade` em todas as situações e crítica sobre a proporcionalidade dos valores; quando a questão for de levantamento, registrar que o item não se aplica.
- **Avaliação Dos Prompts:** quando aplicável, cobertura da planilha, qualidade dos prompts e aderência aos targets da matriz; quando a questão for de levantamento sem avaliação documental binária, registrar que não há prompts esperados.
- **Propostas De Melhoria:** recomendações concretas de redação, regra, critério, evidência, prompt ou encaminhamento.
- **Trechos Sugeridos:** quando útil, fornecer blocos YAML/Markdown ou descrições de linhas de planilha.

Se o usuário pedir para corrigir, editar os arquivos diretamente e depois validar:

- conferir trecho alterado da matriz;
- abrir a planilha com `openpyxl` e validar abas, colunas, IDs e contagem de linhas;
- informar claramente o que foi alterado e o que não foi alterado.

## Princípios

- Ser justo: não exigir prova além do escopo definido pela matriz e pelo questionário.
- Não transformar a revisão em achado real; tratar tudo como hipótese de planejamento.
- Evitar recomendações que aumentem desnecessariamente o ônus dos auditados.
- Preferir ajustes que aumentem rastreabilidade, objetividade e proporcionalidade.
- Tratar ausência de `severidade` em situação encontrada como falha relevante da matriz, mesmo quando os demais campos estejam coerentes.
- Distinguir resposta declaratória negativa, resposta positiva sem evidência suficiente, evidência inexistente, evidência incompatível, evidência insuficiente e inconsistência entre respostas.
