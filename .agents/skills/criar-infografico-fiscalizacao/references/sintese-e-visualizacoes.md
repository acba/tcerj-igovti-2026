# Síntese e escolha de visualizações

## Perguntas que orientam a peça

| Pergunta | Informação essencial |
|---|---|
| O que foi fiscalizado? | Objeto, abrangência, período e população efetivamente examinada |
| Por que a fiscalização foi feita? | Objetivo e relevância para serviços públicos, recursos ou direitos |
| O que foi encontrado? | Conclusão central e poucas constatações que a sustentem |
| O que foi proposto ou decidido? | Medidas principais, destinatários e prazo quando essenciais |
| Quais benefícios são esperados? | Melhorias possíveis, sem apresentar estimativas como resultados realizados |

As perguntas centrais são **o que foi fiscalizado** e **o que foi encontrado**. Identificar também os auditados e os benefícios estimados no relatório, com a ressalva de que dependem da implementação das medidas. Se o trabalho não estimar benefícios, registrar a ausência e solicitar a informação quando necessária, sem inventá-los. Um levantamento pode apresentar diagnóstico e oportunidades de atuação, sem achados de inconformidade ou propostas sancionatórias.

Priorizar a conclusão, não a sequência dos sistemas de processamento. Evitar copiar o resumo executivo inteiro. A página 1 pode combinar 100–180 palavras de contexto, auditados e benefícios, uma síntese do diagnóstico e duas visualizações que revelem sua composição. A segunda pode apresentar evolução, diferenças entre grupos, achados e encaminhamentos. Ajustar a extensão à complexidade e ao modelo fornecido, preservando a leitura A4.

Um gráfico agregado pode esconder diferenças relevantes. Se o relatório analisar dimensões ou grupos, selecionar uma dessas decomposições para acompanhar o resultado geral. Mapas, barras empilhadas e comparações temporais devem responder perguntas distintas. A riqueza da peça decorre da informação apresentada, sem exigir um número fixo de gráficos para todos os temas.

## Seleção dos números

Selecionar indicadores que respondam ao objetivo ou expliquem a conclusão. A faixa superior deve ser compreensível isoladamente: **113 organizações avaliadas** é mais preciso que **119 organizações**, quando o cálculo abrangeu somente 113 de 119.

Antes de exibir um valor, registrar em `dados-e-fontes.json`:

- identificação do indicador ou afirmação;
- valor, unidade e população considerada;
- denominador e fórmula quando houver cálculo;
- período, cenário e data de referência;
- arquivo ou peça de origem e localização verificável;
- natureza da informação: declaração, evidência, resultado de cálculo, proposta ou decisão;
- eventual limite necessário à interpretação.

Esse registro pode ser uma lista simples de objetos JSON, sem impor esquema a bases existentes. Guardá-lo junto dos produtos, sem expor referências internas extensas no layout. Incluir fontes resumidas na própria página.

Não somar percentuais de categorias que se sobrepõem. Não confundir número de temas com ocorrências por organização. Não apresentar um resultado intermediário como final. Em valores financeiros, distinguir contratado, executado, estimado e potencial economia.

## Escolha de gráfico

| Informação | Representação preferida | Cuidado |
|---|---|---|
| Frequência por tema ou grupo | Barras horizontais com rótulos diretos | Informar denominador e unidade. Começar o eixo das barras em zero. |
| Classificações exclusivas que completam o grupo | Barras simples ou empilhadas a 100% | Conferir as somas, o tratamento de ausentes e a legenda. |
| Dois períodos nas mesmas organizações | Pontos ligados, barras pareadas ou setas com valores | Identificar o grupo comum e as diferenças de método. |
| Evolução em vários períodos | Linhas | Mostrar datas, unidades e comparabilidade. |
| Diferenças entre dimensões e grupos | Barras agrupadas ou matriz de cores | Não criar ranking quando a comparação não controlar diferenças relevantes. |
| Distribuição espacial | Mapa coroplético ou símbolos proporcionais | Usar geometria confiável e indicador territorial adequado. |
| Composição hierárquica com grande diferença de tamanho | Mapa de árvore (*treemap*) | Área proporcional ao valor. Categorias pequenas podem exigir legenda externa. |
| Relação entre duas variáveis | Dispersão | Associação não demonstra causalidade. |
| Etapas de avaliação ou cenários | Fluxo com caixas e setas | A sequência deve representar o procedimento efetivamente aplicado. |
| Resultado predominantemente qualitativo | Quadro de constatações, riscos e medidas | Não inventar escala numérica para parecer um gráfico. |

Usar o gráfico que deixa a pergunta mais fácil de responder. Não inserir um mapa apenas porque o trabalho abrange municípios ou um gráfico de dispersão sem conclusão sustentada. Evitar 3D, efeitos de volume e decorações que mudem a percepção dos valores.

## Mapas

Usar arquivo geográfico fornecido, disponível no projeto ou de fonte oficial. Não desenhar limites territoriais de memória. Se for necessário buscar a geometria, registrar origem e data.

Em mapa de taxas, informar numerador e denominador. Não atribuir zero a município não avaliado ou sem resposta: representar como **sem dados**. Não exibir todo o território como fiscalizado quando o trabalho se restringir a parte dele.

Quando a geometria não estiver disponível, usar barras por território ou uma tabela curta. Não bloquear a síntese inteira por falta de um mapa opcional.

## Comparações e ressalvas

Apresentar a conclusão e conservar a ressalva que evita leitura errada. Exemplos de limites, somente quando aplicáveis:

- A comparação longitudinal considera as mesmas organizações nos dois períodos.
- O resultado final incorpora ajustes das respostas após avaliação de evidências.
- Uma diferença entre grupos é descritiva e pode refletir diferenças de porte ou atribuições.
- Os usos de uma tecnologia foram declarados, sem validação independente de cada solução.
- Não houve evidência estatística suficiente de melhora ou piora global.

Posicionar a ressalva junto da visualização. Uma nota ilegível no rodapé não substitui a explicação necessária para entender a conclusão.

## Encaminhamentos

Resumir as medidas pelo seu objeto: formalizar responsabilidades, aprimorar controles, acompanhar riscos ou elaborar plano de ação. Preservar a distinção entre determinação, recomendação e providência já realizada. Se os comandos diferirem entre públicos, mostrar essa diferença sem reproduzir todos os dispositivos normativos.

Não apresentar acompanhamento futuro específico como garantido quando depender do planejamento do órgão. Não afirmar responsabilização já reconhecida quando ainda houver apuração em processo apartado.

## Inspeção final

Comparar o texto e cada rótulo com o relatório final e a memória dos dados. Conferir o infográfico em tamanho A4, incluindo seções, gráficos e fontes. Se algo essencial não puder ser conferido, marcar como pendência na entrega, sem publicar a peça como final.
