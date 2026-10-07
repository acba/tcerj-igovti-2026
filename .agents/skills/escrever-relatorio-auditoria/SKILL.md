---
name: escrever-relatorio-auditoria
description: Redigir, revisar e simplificar relatórios de auditoria do TCE-RJ, achados, apêndices, anexos e templates em português brasileiro, com linguagem simples, formal, impessoal, imparcial e objetiva. Use para melhorar a compreensão de textos de auditoria e para editar relatórios em Markdown, Pandoc e Jinja, preservando dados, evidências, critérios, conclusões, encaminhamentos, variáveis, condições, figuras, tabelas e notas de rodapé.
---

# Escrever Relatório de Auditoria

## Objetivo

Produzir texto que o leitor compreenda na primeira leitura, sem precisar conhecer os bastidores do processamento dos dados. Preservar a precisão técnica, a fundamentação e a rastreabilidade das conclusões. Fazer o mínimo de alterações necessário para atender ao pedido.

## Fluxo de trabalho

1. Identificar o documento, o público, o trecho solicitado e se o pedido autoriza alterações ou apenas propostas de redação.
2. Ler o texto vigente e os exemplos mais próximos no repositório. Antes de alterar afirmações, consultar as fontes que sustentam os dados, a metodologia, os critérios e as conclusões. Não inferir o conteúdo pelo nome do arquivo.
3. Consultar `references/linguagem-simples.md` para simplificação da narrativa e exemplos de antes e depois. Consultar `references/report-markup.md` para sintaxe Markdown, Pandoc, Jinja, figuras, tabelas, notas, includes e fragmentos de achado.
4. Identificar o que o leitor precisa entender: o que foi examinado, como, qual foi o resultado e qual é o limite da conclusão. Explicar somente o necessário para essa compreensão.
5. Revisar os trechos selecionados. Preservar valores, conceitos, critérios, identificadores, condições e referências. Não ampliar o escopo nem reescrever o documento inteiro por preferência de estilo.
6. Conferir o diff e a coerência com os anexos e relatórios relacionados. Distinguir uma melhoria de redação de uma mudança metodológica ou factual.
7. Quando a validação de marcação estiver solicitada ou prevista no fluxo aplicável, usar `scripts/check_report_markup.py` desta skill. Se houver geração autorizada, conferir recursos, referências e conversão no produto gerado. Informar o que foi efetivamente conferido e as limitações.
8. Entregar propostas com localização e antes/depois quando o pedido for apenas de avaliação. Após alterações autorizadas, informar os arquivos e trechos alterados. Respeitar as restrições vigentes de geração, deploy e commit.

## Linguagem simples e formal

- Usar português brasileiro, com redação formal, impessoal, imparcial e objetiva, da perspectiva da equipe de auditoria.
- Preferir palavras conhecidas e verbos que indiquem a ação. Explicitar o objeto: respostas atualizadas, índices recalculados, documentos examinados ou situações afastadas.
- Evitar cadeias de substantivos abstratos, rótulos de processamento e explicações que dependam do conhecimento dos sistemas internos. Substituir o termo pelo seu significado no contexto, sem troca automática de sinônimos.
- Manter uma ideia principal por parágrafo. Separar procedimentos, resultados e limitações quando sua reunião dificultar a leitura.
- Apresentar a informação principal antes dos detalhes. Em comparações, identificar os grupos ou períodos, apresentar o resultado e explicar o alcance da conclusão.
- Explicar termos técnicos indispensáveis na primeira ocorrência ou em nota. Preservar nomes de testes, conceitos jurídicos e definições estatísticas quando necessários à precisão.
- Evitar repetições entre resumo, corpo e anexo. Usar referência ao anexo para os detalhes que não sejam essenciais ao argumento do relatório.
- Usar pontuação conforme a estrutura da frase. Ponto e vírgula pode separar itens de uma enumeração. Não substituir mecanicamente por pontos que quebrem a construção.
- Não acrescentar gráficos, notas, etapas de processamento ou detalhes metodológicos sem utilidade para a interpretação.

## Precisão e integridade da evidência

- Não estimar percentuais, índices, níveis de maturidade, contagens ou conclusões sobre evidências. Preservar a população e o denominador de cada resultado, inclusive nos subgrupos.
- Distinguir prática declarada, comprovação documental e funcionamento efetivo. Ausência de comprovação não equivale à inexistência da prática.
- Distinguir resposta negativa de item vazio ou detalhe não apresentado porque a questão não o disponibilizou. Não converter ausência de resposta em declaração do auditado.
- Distinguir ajustes registrados de respostas efetivamente alteradas e destas de seus efeitos sobre situações, achados e índices.
- Identificar as bases e etapas em linguagem compreensível. Não misturar resultados iniciais, posteriores à avaliação de evidências e finais após os comentários do gestor.
- Distinguir o índice oficial de índices calculados para comparação com itens comuns. Uma diferença de composição das bases deve ser explicada quando afetar a interpretação.
- Descrever o tratamento dos comentários do gestor conforme o objetivo e os procedimentos efetivamente adotados. Não inventar separação temporal entre retificação e adoção posterior se ela não orientar a conclusão do trabalho.
- Não apresentar variação de índice como comprovação de funcionamento efetivo. Não apresentar ausência de significância estatística como igualdade dos resultados.
- Distinguir proposta de encaminhamento, decisão e providência já realizada. Atualizar o estado de processos e medidas somente com fundamento nas fontes.
- Se uma afirmação depender de verificação ainda não realizada, não a apresentar como confirmada. Explicitar apenas as limitações relevantes à interpretação.

## Preservação dos templates e da marcação

- Manter variáveis, filtros, condições, loops, includes, identificadores, rótulos e referências, salvo alteração solicitada. Simplificar o texto ao redor das expressões Jinja sem mudar sua lógica.
- Para `achado_controle_*.md`, seguir o contrato de `references/report-markup.md`: definições iniciais de `nome_achado`/`achado`, guarda `{% if achado %}`, `\newpage`, título `## Achado {{ achado.numero }} – {{ achado.nome }}`, critérios, loop de evidências, situação encontrada, subseções condicionais, conclusão, loop de encaminhamentos, comentário final e fechamento `{% endif %}`.
- Iniciar `### Situação encontrada` com resposta direta à questão de auditoria, limitada às fragilidades presentes. Usar condições Jinja para vinculá-las aos critérios aplicáveis e aos efeitos sustentados pelas evidências.
- Usar expressões Jinja para valores dependentes do contexto, como `{{ '%0.2f' | format(iSegCiber|float) }}`, e os objetos `auditado` e `achado` conforme a referência técnica.
- Preservar células numéricas, figuras e seus caminhos durante revisão de linguagem. Usar referências Pandoc como `[@fig:controles_avaliados]` e `[@tbl:painel_notas]`.
- Usar `__texto__` para ênfase sublinhada em recomendações, determinações ou ressalvas conforme o padrão do relatório.
- Posicionar a fonte imediatamente após a figura ou tabela. Inserir `\newpage` em linha própria.
- Usar identificadores descritivos para notas de rodapé. Em notas com vários parágrafos, recuar os parágrafos de continuação em quatro espaços. A aparência no Markdown não comprova a conversão correta. Quando solicitado, conferir a nota no DOCX gerado.

## Recursos

- `references/linguagem-simples.md`: orientações e exemplos para melhorar a compreensão sem alterar o sentido técnico.
- `references/report-markup.md`: padrões exatos de Markdown, Pandoc, Jinja e fragmentos de achado.
- `scripts/check_report_markup.py`: verificador de defeitos comuns de marcação em relatórios Markdown.
