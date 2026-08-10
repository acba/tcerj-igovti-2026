# Fluxo de avaliação dos comentários do gestor

Este documento explica, em linguagem operacional, como funciona a avaliação dos comentários do gestor: avaliação e consolidação das seções 1 e 2, validação de integridade, revisão humana e geração dos produtos pós-comentários.

Os pareceres produzidos com auxílio de IA são minutas técnicas. Os casos prioritários definidos neste fluxo precisam de revisão e aprovação da equipe de auditoria antes da geração dos ajustes e dos produtos posteriores.

## 1. Visão geral

```text
Respostas do LimeSurvey + anexos + resultados anteriores da auditoria
                              │
                              ▼
                    Avaliação da seção 1
                              │
                              ▼
                   Consolidação da seção 1
                              │
                identifica itens já saneados
                              │
                              ▼
                    Avaliação da seção 2
               sem repetir os itens já saneados
                              │
                              ▼
                   Consolidação da seção 2
                              │
                              ▼
                   Validação de integridade
                              │
                              ▼
            Seleção automática dos casos prioritários
                              │
                              ▼
                       Revisão humana
                  ┌───────────┴───────────┐
                  │                       │
          há pendências             tudo aprovado
                  │                       │
          fluxo permanece                 ▼
          awaiting_review          planilha de ajustes
                                          │
                                          ▼
                              base pós-comentários
                                          │
                                          ▼
                                iGovTI e auditoria
                                          │
                                          ▼
                           impactos, gráficos e relatórios
```

O diretório central da avaliação é:

```text
02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor/
```

## 2. Entradas do processo

### 2.1. Respostas e documentos dos gestores

- `02-Execucao/05-Comentarios_Gestor/01-Coleta_LimeSurvey/20260716-respostas-bruto.xlsx`: respostas exportadas do LimeSurvey;
- `02-Execucao/05-Comentarios_Gestor/01-Coleta_LimeSurvey/Evidencias_Coletadas/evidencias_extraidas/`: anexos apresentados pelos gestores;
- `02-Execucao/05-Comentarios_Gestor/questionario_comentarios_gestor.lss`: estrutura do questionário usada para interpretar as colunas da exportação.

### 2.2. Situação anterior aos comentários

- `02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/02-pos-avaliacao-evidencias/resultado_auditoria.json`: situações encontradas antes dos comentários;
- `02-Execucao/03-Execucao_Procedimentos/01-Insumos/mapa-verificacao-achados.xlsx`: relação entre perguntas, procedimentos, situações e achados;
- `02-Execucao/01-Questionario/02-Ajustes_Respostas/ajustes_respostas_questionario_pos_avaliacao_evidencias.xlsx`: ajustes decorrentes da avaliação inicial de evidências;
- `02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario-02-pos-avaliacao-evidencias.xlsx`: base de respostas vigente antes dos comentários;
- `02-Execucao/03-Execucao_Procedimentos/99-Avaliacao_Evidencias/painel-avaliacao-evidencias.xlsx`: painel de evidências usado pelos procedimentos de auditoria.

## 3. Preparação e avaliação da seção 1

### 3.1. O que é avaliado

A seção 1 trata da manifestação do gestor sobre as situações encontradas no relatório preliminar. A análise procura responder:

> Depois de considerar a manifestação e os documentos apresentados, a situação apontada pela auditoria ainda existia na data de referência?

O resultado pode indicar, entre outros estados:

- situação mantida;
- situação afastada na data-base;
- situação corrigida posteriormente;
- situação inconclusiva;
- situação mantida com alteração parcial dos fundamentos.

Quando a situação possui vários motivos, cada motivo também pode receber conclusão própria.

### 3.2. Preparação dos casos

Antes de chamar os modelos, o pipeline:

1. elimina respostas incompletas, testes e duplicidades;
2. conserva a submissão válida mais recente;
3. localiza comentários e anexos;
4. relaciona cada manifestação à situação correspondente;
5. cria um `Case ID` para o caso;
6. calcula a identidade lógica esperada para cada modelo.

Arquivos gerados:

- `preflight/resumo-secao-1.json`: contagens e detalhes da preparação;
- `preflight/submissoes-excluidas.json`: respostas descartadas e respectivos motivos;
- `individuais/secao-1/manifesto-casos.json`: casos vigentes e identidades esperadas;
- `configuracao-modelos-efetiva.json`: configuração de modelos, juiz e quórum efetivamente utilizada.

Os caminhos acima são relativos a `02-Avaliacao_Comentarios_Gestor/`.

### 3.3. Avaliações individuais

Cada avaliador analisa o mesmo caso de forma independente. Para cada modelo são mantidos dois arquivos:

- `individuais/secao-1/analyses_model_<modelo>.jsonl`: histórico completo, inclusive tentativas antigas e erros;
- `individuais/secao-1/analyses_clean_model_<modelo>.jsonl`: somente a avaliação vigente e compatível com o manifesto atual.

A planilha para leitura humana é:

```text
individuais/secao-1/avaliacoes_modelos.xlsx
```

O arquivo `individuais/secao-1/deterministicos.jsonl` registra casos que podem ser resolvidos por regra objetiva, sem julgamento de IA.

## 4. Consolidação da seção 1

O modelo juiz recebe as opiniões válidas, a manifestação e as evidências e produz um único parecer consolidado. O juiz deve respeitar o quórum e as regras de coerência da seção 1; não se trata de uma votação simples.

Arquivos em `consolidado/secao-1/`:

- `consolidated.jsonl`: histórico de todas as consolidações;
- `consolidated_clean.jsonl`: somente o parecer vigente de cada caso;
- `pareceres_consolidados.xlsx`: versão legível dos pareceres;
- `pendencias_quorum.json`: casos sem avaliações válidas suficientes;
- `links-manifestacoes/`: capturas auditáveis dos links apresentados como evidência;
- arquivos `.bak`: cópias de segurança que não alimentam o fluxo.

O arquivo que alimenta as etapas seguintes é `consolidated_clean.jsonl`.

## 5. Como a seção 1 interfere na seção 2

Antes de preparar a seção 2, o pipeline lê o consolidado vigente da seção 1.

Quando a seção 1 demonstra de forma segura que um item estava atendido ou foi saneado, o pipeline tenta recuperar o valor positivo originalmente declarado pelo auditado. Se o valor puder ser identificado sem suposição, o item é retirado da seção 2. Isso evita avaliar novamente algo já resolvido.

Se a conversão for ambígua — por exemplo, quando não é possível identificar qual nível de uma escala deve ser restaurado — o sistema não inventa valor. O item permanece como pendência.

O resultado dessa preparação fica em:

```text
preflight/resumo-secao-2.json
```

Na execução de 23/07/2026, 33 ocorrências de itens foram excluídas da seção 2. Isso retirou completamente três casos e reduziu o universo da seção 2 de 340 para 337 casos.

## 6. Avaliação da seção 2

### 6.1. O que é avaliado

A seção 2 trata de respostas do questionário que haviam sido alteradas para não conformes por insuficiência de evidência. A análise procura responder:

> Com os novos documentos enviados nos comentários do gestor, o item agora pode ser considerado conforme?

Cada item recebe conclusão como `conforme` ou `nao_conforme`.

### 6.2. Arquivos gerados

Arquivos em `individuais/secao-2/`:

- `manifesto-casos.json`: casos vigentes da seção 2;
- `analyses_model_<modelo>.jsonl`: histórico completo de cada avaliador;
- `analyses_clean_model_<modelo>.jsonl`: opiniões vigentes;
- `avaliacoes_modelos.xlsx`: comparação legível entre os avaliadores.

Quando for necessário entender uma divergência entre avaliadores, `avaliacoes_modelos.xlsx` é o principal arquivo de consulta desta fase.

## 7. Consolidação da seção 2

O juiz reúne as avaliações válidas e produz uma conclusão única para cada item.

Arquivos em `consolidado/secao-2/`:

- `consolidated.jsonl`: histórico das consolidações;
- `consolidated_clean.jsonl`: decisões vigentes;
- `pareceres_consolidados.xlsx`: versão para leitura humana;
- `pendencias_quorum.json`: casos sem quórum;
- `links-manifestacoes/`: capturas auditáveis dos links utilizados.

O caso CGE/q2203 foi resolvido por decisão humana estruturada em `revisoes_pareceres.yml`. No consolidado vigente, sua origem aparece como `revisao_humana`.

## 8. Validação de integridade

Antes da revisão humana, o pipeline verifica se:

- todos os casos esperados estão presentes;
- cada caso possui quórum mínimo;
- os pareceres têm estrutura válida;
- nenhum caso atual está usando parecer incompatível ou antigo;
- as conclusões cobrem exatamente os itens esperados.

Arquivos gerados em `preflight/`:

- `validacao-integridade.json`: resultado técnico detalhado;
- `validacao-integridade.xlsx`: versão legível;
- `casos-reprocessamento.json`: casos que precisam voltar aos modelos.

Um erro histórico de avaliador isolado não exige reprocessamento quando o caso ainda possui quórum válido e parecer consolidado correto.

Na validação de 23/07/2026:

- 598 casos eram esperados;
- 598 casos estavam integralmente válidos;
- nenhum caso precisava de reprocessamento.

## 9. Seleção dos casos prioritários

A revisão humana não é exigida para todos os casos. Um caso é prioritário quando ao menos uma dimensão apresenta:

1. empate entre os avaliadores; ou
2. decisão do juiz contrária à maioria estrita dos avaliadores.

Exemplos:

- 2 votos conforme e 2 não conforme: prioritário por empate;
- 3 votos conforme, 1 não conforme e juiz não conforme: prioritário por juiz contra maioria;
- 3 votos conforme, 1 não conforme e juiz conforme: não prioritário.

Uma divergência isolada, sem empate e sem decisão do juiz contra a maioria, não torna o caso prioritário.

Na classificação de 23/07/2026 foram identificados:

- 48 casos prioritários;
- 71 dimensões divergentes;
- 27 casos da seção 1;
- 21 casos da seção 2.

## 10. Revisão humana

A revisão deve ser feita em:

```text
02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor/revisao-humana-pareceres.xlsx
```

### 10.1. Abas da planilha

#### Casos prioritários

Contém uma linha por caso que exige revisão. As colunas principais são:

- `Seção`;
- `Auditado`;
- `Código`;
- `Motivos da prioridade`;
- `Case ID`;
- `Identidade do parecer`;
- `Status da revisão`;
- `Revisor`;
- `Data da revisão`;
- `Fundamento da revisão`.

#### Divergências

Explica por que o caso foi selecionado, mostrando:

- item, situação ou motivo em divergência;
- voto de cada avaliador;
- contagem dos votos;
- posição da maioria;
- decisão do juiz;
- tipo da prioridade.

#### Universo consolidado

Mostra todos os pareceres das duas seções, inclusive os não prioritários. Essa aba demonstra que a seleção foi aplicada ao universo completo.

#### Controle

Apresenta as quantidades de pareceres, prioridades, aprovações e pendências.

### 10.2. Como revisar cada caso

1. Localize o caso na aba `Casos prioritários`.
2. Consulte a mesma combinação de seção, auditado, código e `Case ID` na aba `Divergências`.
3. Abra `consolidado/secao-1/pareceres_consolidados.xlsx` ou `consolidado/secao-2/pareceres_consolidados.xlsx`.
4. Se necessário, abra também `individuais/secao-1/avaliacoes_modelos.xlsx` ou `individuais/secao-2/avaliacoes_modelos.xlsx`.
5. Confira a manifestação do gestor e as evidências referenciadas.
6. Decida se o parecer consolidado pode ser aprovado.

Se concordar com o parecer:

1. selecione `Aprovado` em `Status da revisão`;
2. informe o auditor em `Revisor`;
3. informe a data em `Data da revisão`;
4. registre uma justificativa curta em `Fundamento da revisão`. O fundamento não é tecnicamente obrigatório, mas é recomendado para rastreabilidade.

Se discordar do parecer:

1. mantenha `Reprovado` enquanto a correção estiver pendente;
2. não marque o caso como aprovado apenas para liberar o fluxo;
3. registre a decisão técnica substitutiva em `revisoes_pareceres.yml`;
4. reconsolide a seção ou repita o pipeline;
5. confira a nova identidade e aprove a versão corrigida.

Uma revisão estruturada em `revisoes_pareceres.yml` deve identificar auditado, seção, código, `Case ID`, identidade do parecer, revisor, data e conclusões substitutivas. O registro CGE/q2203 serve como exemplo.

### 10.3. Função de cada arquivo de revisão

- `revisao-humana-pareceres.xlsx`: controle da aprovação dos casos prioritários;
- `revisoes_pareceres.yml`: substituição ou revisão da decisão e da redação do parecer;
- `revisoes_respostas.yml`: resolução de valores de respostas quando o mapeamento automático é ambíguo.

`revisoes_respostas.yml` não deve ser usado para corrigir um parecer consolidado.

### 10.4. Proteção contra aprovação obsoleta

A aprovação só é reaproveitada enquanto permanecerem iguais:

- `Case ID`;
- identidade do parecer;
- hash do resultado.

Se os documentos, avaliações ou conclusões mudarem, a aprovação anterior deixa de valer e o caso volta para revisão.

O resultado do gate é registrado em:

```text
preflight/validacao-revisao-humana.json
```

Enquanto houver pelo menos uma pendência, o pipeline retorna código 3 e estado `awaiting_review`.

## 11. Produtos gerados depois da aprovação

Somente depois que todos os casos prioritários estiverem aprovados o pipeline gera os ajustes vigentes.

### 11.1. Planilha de ajustes

```text
02-Avaliacao_Comentarios_Gestor/
ajustes_respostas_questionario_pos_comentarios_gestor.xlsx
```

Abas:

- `Ajustes`: mudanças seguras que podem ser aplicadas;
- `Pendências`: mudanças que não podem ser feitas automaticamente;
- `Saneados seção 1`: ajustes originados na consolidação da seção 1.

Essa planilha é alimentada pelos dois `consolidated_clean.jsonl` e pelas revisões de respostas autorizadas.

### 11.2. Painel de evidências pós-comentários

```text
02-Avaliacao_Comentarios_Gestor/
fontes-auditoria-pos-comentarios/painel-avaliacao-evidencias.xlsx
```

O painel impede que uma não conformidade já saneada seja criada novamente quando os procedimentos de auditoria forem reexecutados.

## 12. Produtos básicos pós-comentários

Depois da aprovação, `scripts/gerar_produtos_pos_comentarios_gestor.py` materializa três produtos básicos.

### 12.1. Base corrente de respostas

```text
02-Execucao/01-Questionario/03-Respostas_Processadas/
<AAAAMMDD>-respostas-questionario-pos-comentarios-gestor.xlsx
```

Ela é produzida aplicando a planilha de ajustes sobre a base pós-avaliação de evidências e alimenta o novo cálculo do iGovTI e a nova execução da auditoria.

### 12.2. Quadro de avaliação dos comentários

```text
02-Execucao/05-Comentarios_Gestor/03-Produtos_Pos_Comentarios/
avaliacao_comentarios_gestor.xlsx
```

Abas:

- `Seção 1 - situações`;
- `Seção 2 - itens`.

Esse quadro é voltado aos relatórios e à apresentação institucional. Ele não substitui `revisao-humana-pareceres.xlsx`, que é a planilha do gate.

### 12.3. Contexto para os relatórios

```text
02-Execucao/05-Comentarios_Gestor/03-Produtos_Pos_Comentarios/
contexto-relatorios-comentarios-gestor.json
```

O JSON organiza por auditado as situações, os itens reavaliados, as decisões e as manifestações da equipe. Ele alimenta os relatórios individuais finais.

## 13. Etapas posteriores do orquestrador

Depois da aprovação e da geração dos produtos básicos, o orquestrador executa, nesta ordem:

1. cálculo do iGovTI do cenário pós-comentários;
2. reexecução dos procedimentos de auditoria;
3. cálculo dos impactos dos comentários;
4. estatísticas finais dos comentários;
5. gráficos finais;
6. relatórios individuais finais;
7. relatório consolidado;
8. validação final dos produtos.

Principais destinos:

- `02-Execucao/01-Questionario/04-Resultados_iGovTI/03-pos-comentarios-gestor/`;
- `02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/03-pos-comentarios-gestor/`;
- `02-Execucao/05-Comentarios_Gestor/03-Produtos_Pos_Comentarios/impactos-comentarios-gestor.json`;
- `02-Execucao/05-Comentarios_Gestor/03-Produtos_Pos_Comentarios/impactos-comentarios-gestor.xlsx`;
- `03-Relatorios/99-Avaliacao_Comentarios_Gestor/dados/`;
- `03-Relatorios/99-Avaliacao_Comentarios_Gestor/img/`;
- `03-Relatorios/03-Relatorios_Individuais_Finais/`.

## 14. Retomada do fluxo

Depois de preencher e salvar `revisao-humana-pareceres.xlsx`, deve-se repetir o mesmo comando do orquestrador completo. Ele retomará a etapa de comentários, validará as aprovações e somente seguirá para os ajustes e produtos posteriores se todas forem válidas.

Também é possível validar isoladamente o gate com a ação `validar-revisao`, desde que sejam informados os mesmos insumos e o mesmo diretório de saída utilizados na execução completa.

## 15. Atenção aos produtos já existentes

Alguns produtos pós-comentários podem existir no repositório por terem sido gerados em execuções anteriores. A mera existência do arquivo não significa que ele represente a revisão humana atual.

Enquanto `preflight/validacao-revisao-humana.json` indicar `awaiting_review`, os produtos posteriores devem ser tratados como anteriores ou provisórios. Eles só passam a representar o fluxo corrente depois que:

1. todos os casos prioritários forem revisados;
2. o gate indicar `approved`;
3. o orquestrador for executado novamente;
4. os ajustes, a base, o iGovTI, a auditoria, os impactos e os relatórios forem regenerados.

## 16. Estado registrado em 23/07/2026

- seção 1: 261 consolidações vigentes;
- seção 2: 337 consolidações vigentes;
- integridade: 598 de 598 casos válidos;
- casos para reprocessamento: zero;
- casos prioritários: 48;
- prioridades da seção 1: 27;
- prioridades da seção 2: 21;
- dimensões divergentes: 71;
- estado do fluxo: `awaiting_review`.

