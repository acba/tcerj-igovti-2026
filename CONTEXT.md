# iGovTI 2026

Vocabulário compartilhado para avaliação de evidências e achados do questionário iGovTI 2026.

## Language

**Produto de auditoria**:
Saída útil e deliberadamente solicitada no fluxo da auditoria, como resultado estruturado, planilha, relatório, gráfico, survey ou documento DOCX.
_Avoid_: artefato, arquivo gerado, saída intermediária

**Registro de execução**:
Manifesto e log mínimos que demonstram como os produtos de auditoria foram gerados, incluindo entradas, parâmetros, versões, hashes, dependências, tempos e estados relevantes.
_Avoid_: produto de auditoria, arquivo temporário, cache

**Intermediário de execução**:
Dado transitório necessário ao processamento, sem valor próprio como papel de trabalho e que não deve ser persistido no repositório.
_Avoid_: produto de auditoria, registro de execução, papel de trabalho

**Cenário de auditoria**:
Versão imutável e identificada da base usada em uma fase do fluxo da auditoria. Ajustes e avaliações originam um novo cenário; índices, procedimentos e relatórios declaram o cenário do qual derivam.
_Avoid_: planilha corrente, base sobrescrita, estado mutável

**Insumo canônico**:
Entrada autoral ou coletada cuja leitura deve permanecer compatível no Argos: cadastro de auditados, mapa de verificação e achados, matriz de planejamento e planilhas brutas de respostas dos surveys.
_Avoid_: produto derivado, intermediário de execução, qualquer arquivo de entrada

**Acervo de avaliações**:
Conjunto persistente de avaliações consolidadas de evidências e de comentários do gestor, incluindo identidades, hashes, pareceres, opiniões e contexto necessários à migração sem perda e à rastreabilidade.
_Avoid_: cache de modelo, produto regenerável, resultado final isolado

**Pacote de auditoria**:
Conjunto opcional e versionado que acrescenta índices, prompts, surveys, templates e produtos específicos a uma fiscalização. O fluxo básico de procedimentos usa diretamente os insumos canônicos e o mapa de verificação, sem exigir pacote ou manifesto; extensões Python só são admitidas quando a configuração declarativa não for suficiente.
_Avoid_: núcleo Argos, pasta de scripts, configuração obrigatória

**Núcleo Argos**:
Distribuição autônoma e genérica responsável por TUI, execução não interativa, cenários, operações, dependências, integrações e rastreabilidade. É incubada em `argos-cli/` sem importar código externo à distribuição e destinada a repositório próprio após a validação de paridade.
_Avoid_: pacote de auditoria, scripts iGovTI, orquestrador legado

**Espaço de trabalho de fiscalização**:
Unidade isolada que representa uma fiscalização identificada por número e nome, reúne seus insumos canônicos, cenários, operações, produtos, registros de execução e acervo de avaliações e possui seu próprio arquivo SQLite.
_Avoid_: banco global, diretório compartilhado, cenário de auditoria

**Fiscalização ativa**:
Fiscalização selecionada na sessão atual do Argos. Todas as operações e registros da sessão são vinculados a ela; para mudar de fiscalização, a sessão é encerrada e outro espaço de trabalho é aberto ou criado.
_Avoid_: contexto global mutável, banco compartilhado, troca implícita

**Versão fixada do pacote**:
Versão imutável do pacote de auditoria vinculada a uma fiscalização por seus arquivos e hash. Atualizações são novas versões explicitamente carregadas e não reinterpretam cenários ou produtos existentes.
_Avoid_: configuração corrente, pacote sobrescrito, atualização implícita

**Operação transformadora**:
Operação que altera a base de dados da fiscalização e, por isso, cria um novo cenário imutável vinculado ao cenário de origem, à transformação e aos hashes dos insumos.
_Avoid_: geração de relatório, cálculo de índice, atualização direta

**Operação de produto**:
Operação somente de leitura que consome um cenário e materializa um ou mais produtos de auditoria sem criar ou alterar cenário.
_Avoid_: ajuste de respostas, mutação de base, transformação de cenário

**Motor de execução**:
Módulo que planeja operações, valida pré-condições e saídas, coordena adapters, publica produtos ou novos cenários de forma segura e confirma o registro de execução. As operações não persistem diretamente.
_Avoid_: operação transformadora, script orquestrador, interface TUI

**Execução**:
Instância identificada de um plano de operações, com estado persistido, entradas fixadas, progresso, eventos, pendências, revisão e saídas. Pode ser retomada enquanto suas identidades e entradas continuarem válidas.
_Avoid_: rotina subprocessada, cenário de auditoria, produto de auditoria

**Evento de execução**:
Registro append-only e compacto de uma transição, tentativa externa, cancelamento, pendência ou publicação, vinculado à execução e, quando aplicável, à unidade de trabalho. Guarda estado, tempo, referências e métricas necessárias para reconstruir o fluxo, sem duplicar prompts, evidências ou payloads completos.
_Avoid_: log textual descartável, cópia de intermediários, payload integral no histórico

**Retomada de execução**:
Continuação do mesmo plano a partir das unidades que ainda não possuem resultado válido. Unidades concluídas e publicadas não são chamadas novamente; se um insumo material mudar, o ramo fica desatualizado e só prossegue após uma ação explícita de reavaliação.
_Avoid_: repetir o plano inteiro, reconstruir estado por log textual, rerun automático de avaliação concluída

**Cancelamento cooperativo**:
Solicitação que impede novas unidades, sinaliza as unidades em andamento e só aceita resultados completos publicados atomicamente. Adapters tentam interromper chamadas externas; quando o provider não permite, a unidade permanece interrompida e retomável, sem apagar resultados já concluídos.
_Avoid_: matar processo sem estado, apagar produtos válidos, publicar resultado parcial

**Falha indeterminada de chamada externa**:
Estado em que não é possível saber se o provider aceitou ou concluiu uma requisição, como após timeout ou desconexão durante o envio. Não autoriza retry automático; exige resolução explícita ou uma garantia de idempotência do adapter.
_Avoid_: erro definitivo, retry cego, avaliação duplicada

**Retry idempotente**:
Nova tentativa técnica limitada e rastreável, permitida somente quando a rejeição do provider é conhecida ou quando o adapter dispõe de uma chave de idempotência. Retries pertencem à mesma unidade e não criam outra avaliação.
_Avoid_: nova revisão, loop infinito, segunda avaliação do mesmo contexto

**Estados de execução**:
Ciclo explícito `planned`, `ready`, `running`, `awaiting_input`, `awaiting_review`, `completed`, `failed` ou `cancelled`, com transições validadas e sem inferência por texto de processo.
_Avoid_: código de saída, status implícito, log de console

**Proveniência do produto**:
Identidade que relaciona um produto à fiscalização, ao cenário, à operação e versão do pacote, aos parâmetros normalizados e aos hashes dos insumos, evidências e templates que o produziram. O caminho do arquivo é apenas localização.
_Avoid_: nome do arquivo, data de geração isolada, produto sobrescrito

**Avaliação versionada**:
Registro imutável de avaliação de evidência ou comentário ligado ao cenário, caso, evidência e identidade lógica. Nova avaliação ou revisão se relaciona por `supersedes_identity`, preservando os registros anteriores.
_Avoid_: parecer sobrescrito, resultado corrente sem histórico, cache de modelo

**Slot lógico de avaliação**:
Lugar estável de uma intenção de avaliação dentro de uma fiscalização e de um cenário, definido pelo tipo, caso e perfil do modelo. O slot identifica qual avaliação deve existir, sem mudar por caminho, nome, timestamp ou outro metadado incidental dos arquivos.
_Avoid_: hash gigante de todos os insumos, revisão, resultado corrente

**Snapshot semântico de entrada**:
Descrição normalizada do contexto efetivamente usado em uma avaliação, incluindo a versão do prompt, o caso, o conteúdo significativo dos anexos processados e, numa consolidação, as opiniões-fonte. Diferenças incidentais de caminho, ordem ou metadado não mudam o snapshot; mudança material torna a revisão potencialmente desatualizada.
_Avoid_: slot lógico, caminho bruto, identificador de upload do provider

**Revisão de avaliação**:
Resultado imutável produzido para um slot e um snapshot semântico específicos. Uma nova revisão só nasce de uma reavaliação explicitamente solicitada para um contexto materialmente novo; revisões anteriores permanecem consultáveis e relacionadas por sucessão.
_Avoid_: sobrescrever o resultado, repetir silenciosamente o mesmo contexto, cache sem linhagem

**Atualidade da avaliação**:
Relação entre uma revisão e o snapshot semântico atualmente declarado para o mesmo slot. Uma revisão pode estar `current`, `stale`, `unknown` ou `failed`; `stale` sinaliza mudança material, mas não autoriza nova chamada ao modelo por si só.
_Avoid_: rerun automático, validade baseada em timestamp, apagar revisão antiga

**Relação de avaliação**:
Vínculo rastreável que informa quais revisões individuais foram usadas por uma avaliação consolidada, seu papel e eventuais avaliadores ausentes. A relação aponta para revisões imutáveis, não para o último resultado encontrado por nome.
_Avoid_: lista textual sem identidade, média anônima, vínculo apenas por caminho

**Decisão humana**:
Registro separado da avaliação automatizada, com revisor, data, justificativa e hash do caso avaliado, usado para aprovar, rejeitar ou revisar uma conclusão sem apagar o histórico.
_Avoid_: edição silenciosa, override sem identidade, opinião de modelo

**AIService**:
Fachada genérica que recebe prompt, schema e referências de arquivos e devolve a resposta estruturada de um provider; adapters internos tratam transporte, upload e representação dos anexos.
_Avoid_: lógica de auditoria no provider, SDK exposto ao domínio, prompt montado pelo adapter

**AttachmentProcessingService**:
Serviço extensível que detecta, expande e prepara anexos para uma requisição de IA. Aplica o mesmo pipeline recursivo a arquivos diretos e a membros de ZIPs aninhados, produzindo partes processadas e relatório de pendências/ignorados.
_Avoid_: análise de conformidade, ZIP tratado como exceção, arquivo descartado sem registro

**Pendência de anexo**:
Registro técnico de arquivo que não foi processado por falta de processor, erro ou formato não suportado. Não bloqueia a requisição e acompanha a resposta do modelo para permitir reprocessamento posterior.
_Avoid_: evidência ausente, falha de auditoria, arquivo silenciosamente ignorado

**Anexo ignorado**:
Arquivo excluído intencionalmente por uma regra explícita, como cache, banco local ou temporário, com caminho, hash e regra registrados no relatório de processamento.
_Avoid_: anexo pendente, arquivo descartado sem justificativa

**Relatório de processamento de anexos**:
Metadado retornado com a avaliação do modelo, separando arquivos processados, pendentes e ignorados, com hashes, linhagem, motivos e versões dos processors; não é incluído automaticamente no prompt.
_Avoid_: conclusão do modelo, prompt de avaliação, lista informal de arquivos

**ProductRendererService**:
Dispatcher interno que recebe a definição de um produto e o draft calculado por uma operação, encaminha para o renderer de formato e devolve bytes/metadados antes da publicação pelo `ArtifactStoreService`.
_Avoid_: operação de auditoria, escritor direto no repositório, renderização de produtos não solicitados

**ProductDraft**:
Dados estruturados já calculados por uma operação, acompanhados do contexto, template e recursos necessários para materializar um produto solicitado.
_Avoid_: produto publicado, intermediário persistido, resultado sem proveniência

**Bundle de produtos**:
Conjunto de produtos relacionados publicado como um único ZIP, com manifesto e hashes dos membros; arquivos individuais só são materializados quando solicitados separadamente.
_Avoid_: pasta de temporários, coleção sem identidade, artefatos auxiliares

**ExecutionScheduler**:
Agendador global que libera unidades independentes do grafo, reserva um orçamento compartilhado de CPU, memória, rede e tokens e retoma somente o que ainda não possui resultado válido.
_Avoid_: pool privado por rotina, paralelismo sem limite, pipeline linear

**ResourceProfile**:
Declaração de recursos estimados por unidade de trabalho, incluindo CPU, memória, slots de rede, provider e tokens, usada pelo `ExecutionScheduler` antes de iniciar a tarefa.
_Avoid_: quantidade fixa de workers, limite apenas de threads, estimativa sem enforcement

**Unidade de trabalho paralela**:
Parte isolada de uma operação, como uma avaliação por caso/modelo, um relatório por auditado ou um gráfico, que pode concluir sem escrever no mesmo produto de outra unidade.
_Avoid_: etapa inteira paralelizada sem dependências, worker compartilhando arquivo de saída

**Operação**:
Capacidade versionada declarada pelo pacote de auditoria, com entradas, pré-condições, política de execução e saídas conhecidas. Pode ser transformadora ou de produto; sua implementação não persiste diretamente.
_Avoid_: script, comando, etapa linear sem contrato

**Plano de execução**:
Seleção validada de operações e dependências necessárias para atender a uma solicitação de produto ou operação avulsa, incluindo entradas ausentes, estados esperados e ordem de execução.
_Avoid_: lista manual de scripts, comando montado, execução já iniciada

**Grafo de operações**:
Grafo acíclico orientado por insumos e produtos lógicos, no qual cada operação declara o que consome e produz. O motor resolve dependências a partir do produto solicitado e executa somente o subgrafo necessário.
_Avoid_: sequência fixa de scripts, pipeline linear, ordem manual

**Chave de validade da operação**:
Identidade derivada da fiscalização, cenário, id e versão da operação, versões das extensões, parâmetros normalizados e hashes dos insumos, evidências, memórias de cálculo e templates. Somente uma chave igual e produtos íntegros autoriza reutilização.
_Avoid_: nome do arquivo, timestamp, cache sem hash

**Bloqueio por ramo**:
Suspensão localizada de uma operação e de seus descendentes quando falta insumo ou revisão; operações independentes do mesmo plano podem continuar, e o produto solicitado só é concluído quando todo o subgrafo necessário estiver válido.
_Avoid_: pausa global, falha de toda a fiscalização, espera implícita

**Operação avulsa**:
Solicitação de uma única operação pelo usuário, planejada e executada pelo mesmo grafo, validações, estados, cache e registro usados por fluxos guiados. Não é atalho para contornar dependências.
_Avoid_: execução especial, comando direto sem contrato, bypass do motor

**Fluxo básico de procedimentos**:
Execução genérica que recebe cadastro de auditados, mapa de verificação e achados e uma ou mais fontes de informação, valida os contratos e produz os resultados dos procedimentos sem depender de configuração específica de uma auditoria.
_Avoid_: pacote de auditoria, pipeline iGovTI, manifesto obrigatório

**Catálogo de operações**:
Registro único das rotinas disponíveis no Argos, com identificador, nome, categoria, descrição, parâmetros, validações, pré-condições, saídas e handler in-process. O TUI e o modo não interativo consomem o mesmo catálogo.
_Avoid_: lista duplicada no TUI, parser isolado, comando subprocessado

**Memória de cálculo**:
Arquivo declarativo, como YAML, que define os dados, fórmulas, pesos, dimensões e regras necessários para uma operação genérica de cálculo de índice. A operação recebe a memória como insumo e não incorpora índices específicos no núcleo.
_Avoid_: cálculo iGovTI, fórmula embutida, índice fixo

**Coluna de evidência**:
Campo do questionário em que o auditado anexa evidência documental para uma questão ou subitem específico.
_Avoid_: arquivo de evidência, upload, checklist

**Ação de verificação**:
Teste definido na matriz de procedimentos para avaliar uma informação requerida e identificar eventual situação encontrada ou achado.
_Avoid_: prompt, questão, coluna

**Prompt de avaliação de evidência**:
Instrução de análise usada para julgar se a evidência sustenta as afirmações do auditado associadas a uma coluna de evidência.
_Avoid_: checklist, ação de verificação

**Item afirmado**:
Alternativa, subitem ou prática declarada pelo auditado que deve ser confrontada com a evidência correspondente; itens não declarados não são positivados por inferência a partir da evidência.
_Avoid_: resposta bruta, achado

**Coluna candidata a prompt de achado**:
Coluna de evidência incluída no conjunto de prompts por estar associada, pela matriz de procedimentos, a uma ou mais informações requeridas que podem ensejar situação encontrada ou achado. A matriz seleciona a coluna; dentro dela, avaliam-se todos os itens afirmados pelo auditado que o pipeline enviar.
_Avoid_: ação candidata, subitem obrigatório

**Conjunto parcial de prompts**:
Conjunto de prompts que cobre apenas colunas de evidência selecionadas por critério de auditoria, sem representar a totalidade das evidências do questionário.
_Avoid_: catálogo incompleto, erro de prompt ausente

**Catálogo versionado de prompts**:
Artefato explícito que define quais colunas de evidência serão avaliadas e quais critérios de conformidade serão aplicados. A matriz de procedimentos orienta sua criação e conferência, mas não altera automaticamente seu conteúdo.
_Avoid_: geração implícita pela matriz, lista dinâmica

**Catálogo enxuto de prompts**:
Catálogo versionado de prompts que registra apenas a regra comum, os critérios da prática principal, os critérios por alternativa ou item detalhado e o formato de saída esperado.
_Avoid_: checklist extenso, matriz duplicada

**Julgamento binário de evidência**:
Regra de avaliação em que uma afirmação do auditado é classificada apenas como `conforme` ou `nao_conforme`, salvo falha técnica externa à evidência.
_Avoid_: inconclusivo, parcialmente conforme

**Conclusão de evidência**:
Registro JSON compatível com o pipeline que expressa o julgamento de um item afirmado, sua justificativa e os elementos de rastreabilidade usados na análise.
_Avoid_: resposta livre, parecer textual

**Linha do dashboard de avaliação**:
Representação visual de uma conclusão de evidência individual, enriquecida com metadados do processamento que a produziu.
_Avoid_: registro bruto, linha do JSONL

**Resposta avaliada no dashboard**:
Afirmação do auditado que foi efetivamente avaliada pelo pipeline e aparece em uma conclusão de evidência; não representa todas as respostas do questionário.
_Avoid_: resposta completa do questionário, base LimeSurvey

**Prática principal**:
Afirmação de adoção declarada na questão-base, distinta dos detalhamentos marcados pelo auditado. Sua conformidade depende de critérios próprios definidos para a questão, e não da soma automática dos subitens conformes.
_Avoid_: resumo dos detalhamentos, média dos subitens

**Critério da prática principal**:
Condição substantiva, definida por questão, para julgar a conformidade da afirmação de adoção da prática principal.
_Avoid_: critério automático, contagem de subitens

**Critério do item detalhado**:
Condição substantiva para julgar a conformidade de um subitem, alternativa ou detalhamento específico afirmado pelo auditado.
_Avoid_: critério geral da questão

**Suficiência documental mínima**:
Exigência comum de que a evidência sustente diretamente o item afirmado e contenha elemento verificável citável, como trecho, página, aba, linha, imagem, ato, ata, relatório, registro ou equivalente.
_Avoid_: plausibilidade, inferência ampla

**Alternativa declarada**:
Opção de resposta selecionada pelo auditado em uma questão de alternativa única; sua conformidade é julgada por critério específico da própria alternativa.
_Avoid_: prática principal, resposta textual

**Item sem exigência de evidência**:
Resposta ou subitem que pode compor achado pela regra da matriz, mas não deve gerar julgamento de evidência porque o questionário não solicita upload para essa condição.
_Avoid_: evidência negativa, prompt de ausência

**Item avaliável por evidência**:
Resposta, alternativa ou subitem que pode chegar ao pipeline porque aciona uma coluna de evidência no questionário; somente esses itens recebem critérios no prompt de avaliação de evidência.
_Avoid_: item de achado, item da matriz

**Evidência ausente**:
Condição em que o auditado afirma item avaliável por evidência, mas não envia o anexo esperado. Deve produzir julgamento `nao_conforme` para o item afirmado, em vez de simples ausência de análise.
_Avoid_: item ignorado, sem escopo

**Dashboard de avaliação de evidências**:
Artefato estático de visualização usado para explorar conclusões de evidência, estados de conformidade, auditados, questões, colunas de evidência e justificativas produzidas pelo pipeline.
_Avoid_: sistema de auditoria, fonte de verdade

**Grupo de comparação de modelos**:
Conjunto de conclusões de evidência referentes ao mesmo auditado, item afirmado e evidência, produzido por um ou mais modelos de avaliação para apoiar a revisão comparativa pelo analista.
_Avoid_: linha do JSONL, média dos modelos

**Consenso entre modelos**:
Situação em que dois ou mais modelos atribuem o mesmo estado substantivo a um grupo de comparação de modelos. Divergência ocorre quando há estados substantivos diferentes para o mesmo grupo.
_Avoid_: conclusão final de auditoria, decisão automática

**Arquivo estático de dashboard**:
Dashboard de avaliação de evidências distribuído como um único HTML, com dados iniciais embutidos e possibilidade de carregar outro `analyses.jsonl` local para exploração.
_Avoid_: aplicação web, backend
