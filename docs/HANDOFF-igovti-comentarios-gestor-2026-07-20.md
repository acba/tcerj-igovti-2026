# Handoff — integridade dos comentários do gestor e relatório final iGovTI 2026
> Atualização mais recente: 20/07/2026, após interrupção controlada do reparo no Windows. Leia primeiro a seção seguinte. Quando houver divergência, ela prevalece sobre números, modelos e comandos históricos mais abaixo.

## Estado operacional atualizado — 20/07/2026

### Situação no momento do handoff

- O usuário pediu para parar o reparo. Os dois processos Python dessa execução, PIDs `18936` e `23496`, iniciados às `16:32:13`, foram encerrados. A verificação retornou zero processos remanescentes desses PIDs.
- Depois da parada foi executado `validar-integridade`, sem chamadas a modelos.
- Estado autoritativo atual: `status = reparo_necessario`, `25` casos da seção 1, `16` casos da seção 2, total de `41` casos para reparo.
- Universo validado: `1.814` casos; `1.522` casos de IA integralmente válidos, além dos casos determinísticos tratados separadamente pela rotina.
- Há `445` avisos individuais históricos e `503` violações diagnósticas. Esses números não são quantidades de casos problemáticos: um mesmo caso pode gerar várias violações, e avisos isolados não exigem reparo quando ainda existe quórum e parecer consolidado válido.
- O arquivo autoritativo é `02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor/preflight/validacao-integridade.json`, atualizado após a interrupção.
- Não gere ajustes ou produtos finais enquanto o status não for `conforme` e as duas contagens de reparo não forem zero.

### Coleta e preparação dos anexos concluídas

- A relação de respostas usada é `02-Execucao/05-Comentarios_Gestor/01-Coleta_LimeSurvey/20260716-respostas-bruto.xlsx`.
- Foram coletados os anexos faltantes das respostas LimeSurvey da IRM (`response id 79`) e da SETUR (`response id 97`) com a sessão fornecida pelo usuário. Cookies e tokens não foram persistidos no repositório nem devem ser incluídos em logs ou neste handoff.
- Foram extraídos `50` ZIPs em `02-Execucao/05-Comentarios_Gestor/01-Coleta_LimeSurvey/Evidencias_Coletadas/evidencias_extraidas`.
- Dois nomes excediam o limite de caminho do Windows; foram criados aliases curtos acessíveis. O preflight dos anexos passou depois desse ajuste.
- Uma cópia filtrada dos casos então considerados problemáticos foi criada para inspeção em `C:/tmp/tcerj-igovti-2026/comentarios-gestor-casos-problematicos-20260720-141530`, com o arquivo principal `casos-problematicos.xlsx`. Essa cópia é histórica; use o manifesto atual de 41 casos para qualquer nova análise.

### Correção da falsa reclassificação de casos

Foi corrigido `scripts/comentarios_gestor_integridade.py`. Antes, a validação selecionava simplesmente o registro mais recente por caso/modelo. Assim, uma resposta válida antiga era descartada quando vinha depois um `error` ou uma resposta concluída fora do escopo. A consolidação já preservava a resposta válida, mas o relatório de integridade não, inflando os “problemáticos”.

A rotina agora agrupa os registros e seleciona o registro concluído, válido e pertencente à identidade esperada mais recente. Somente quando não há nenhum registro válido ela reporta o erro ou registro inválido mais recente. Isso vale para avaliações individuais e consolidadas.

Arquivos principais dessa correção:

- `scripts/comentarios_gestor_integridade.py`;
- `scripts/tests/test_comentarios_gestor_integridade.py`.

Os dois testes de regressão cobrem erro posterior e resposta fora do escopo posterior. Antes da mudança de configuração de execução, a suíte completa tinha `74` testes aprovados.

### GPT indisponível sem alterar o quórum histórico

O usuário informou que o GPT falha em todas as consultas nesta máquina. Isso foi confirmado nos 20 registros mais recentes do checkpoint: todos retornavam `HTTP 502 Bad Gateway`, `upstream_failure`/`fetch failed`.

Desabilitar o GPT com `enabled: false` elevou artificialmente o manifesto de `44` para `434` casos, pois o quórum continuava em três e os três modelos restantes passaram a ser exigidos por unanimidade. Essa alteração foi desfeita.

Foi implementada em `scripts/run_comentarios_gestor.py` a distinção entre:

- `enabled: true`: a identidade do modelo continua elegível para o quórum e opiniões históricas válidas são preservadas;
- `execute: false`: nenhuma nova chamada é enviada a esse modelo.

A configuração atual em `scripts/avaliacao_evidencias/configs/comentarios_gestor_models_v1.json` é:

- Gemini 3.1 Flash Lite: `enabled: true`, execução ativa;
- GPT 5.6 Luna: `enabled: true`, `execute: false`;
- MiniMax M3: `enabled: true`, execução ativa;
- Qwen 3.7 Plus: `enabled: true`, execução ativa;
- Gemini 3.5 Flash permanece desabilitado conforme decisão do usuário.

O quórum permanece `3 de 4`: opiniões válidas antigas do GPT contam, mas ele não recebe novas chamadas. `evaluate_section` executa apenas as rotas com `execute: true`; manifesto, materialização dos checkpoints, consolidação e validação continuam considerando todos os modelos `enabled`.

Arquivos dessa mudança:

- `scripts/run_comentarios_gestor.py`;
- `scripts/avaliacao_evidencias/configs/comentarios_gestor_models_v1.json`;
- `scripts/tests/test_comentarios_gestor_pipeline.py`.

Foram adicionados testes para preservar um modelo apenas para histórico e rejeitar `execute: true` com `enabled: false`. Os `46` testes diretamente relacionados a comentários do gestor e integridade passaram fora da limitação de escrita temporária do sandbox. O próximo agente deve executar a suíte completa para obter a nova contagem global.

### Progresso das tentativas de reparo

- Após a correção do seletor de registros, o manifesto caiu para `44` casos: 28 da seção 1 e 16 da seção 2.
- A primeira retomada saneou dois casos antes de ser interrompida para retirar o GPT das novas chamadas: restaram `42` (26 + 16).
- A retomada com `execute: false` para o GPT saneou mais um caso antes da parada solicitada: restam `41` (25 + 16).
- Os checkpoints são append-only; não apague nem trunque arquivos `analyses*.jsonl`.
- Na última retomada o arquivo bruto do GPT permaneceu inalterado desde `16:24:42`, confirmando que não houve novas chamadas. Qwen e MiniMax gravaram resultados da seção 1; a seção 2 não chegou a ser retomada nessa execução.
- O Qwen apresentou chamadas longas e já produziu respostas inválidas de escopo/coerência em tentativas anteriores. MiniMax também apresentou timeouts em ocasiões anteriores. A rotina deve terminar a fila, reconsolidar e então recalcular o manifesto; não avalie progresso apenas pelo volume de linhas anexadas.

### Como o próximo agente deve continuar

Ambiente Windows funcional nesta máquina:

```powershell
$env:TEMP=(Resolve-Path -LiteralPath '.tmp-tests').Path
$env:TMP=$env:TEMP
$env:TMPDIR=$env:TEMP
$python='C:\Users\augustocba\AppData\Local\anaconda3\envs\igovti\python.exe'
```

O Python de `scripts/.venv` foi bloqueado por política de grupo; use o Python Conda acima. As chaves estão em `.env`; carregue-as com `python -m dotenv run` e nunca exiba o arquivo.

1. Confirme que não existe reparo ativo e execute a suíte completa:

```powershell
Get-Process python -ErrorAction SilentlyContinue
& $python -m unittest discover -s scripts/tests -p 'test_*.py'
```

2. Revalide antes de chamar modelos e confirme que o ponto de partida ainda é 25 + 16:

```powershell
& $python scripts/run_comentarios_gestor.py validar-integridade `
  --respostas-comentarios '02-Execucao\05-Comentarios_Gestor\01-Coleta_LimeSurvey\20260716-respostas-bruto.xlsx' `
  --evidencias-comentarios-root '02-Execucao\05-Comentarios_Gestor\01-Coleta_LimeSurvey\Evidencias_Coletadas\evidencias_extraidas' `
  --out-dir '02-Execucao\05-Comentarios_Gestor\02-Avaliacao_Comentarios_Gestor'
```

3. Retome somente o reparo dirigido. Não use `completo`:

```powershell
& $python -m dotenv run -- $python scripts/run_comentarios_gestor.py reparar-integridade `
  --respostas-comentarios '02-Execucao\05-Comentarios_Gestor\01-Coleta_LimeSurvey\20260716-respostas-bruto.xlsx' `
  --evidencias-comentarios-root '02-Execucao\05-Comentarios_Gestor\01-Coleta_LimeSurvey\Evidencias_Coletadas\evidencias_extraidas' `
  --out-dir '02-Execucao\05-Comentarios_Gestor\02-Avaliacao_Comentarios_Gestor'
```

4. Ao término, execute `validar-integridade` novamente. A porta obrigatória continua sendo `status = conforme`, seção 1 = 0 e seção 2 = 0. Se houver pendências, examine `casos-reprocessamento.json` e exemplos de `violacoes` antes de repetir; não volte a reavaliar todo o universo.

5. Somente depois da porta conforme, prossiga para `gerar-ajustes` e para as etapas de produtos e relatórios já descritas nas seções históricas abaixo.

### Cuidados para o próximo agente

- Preserve as alterações existentes e os checkpoints; o worktree contém mudanças do usuário e produtos de execução.
- Não reative Gemini 3.5 Flash.
- Não transforme `execute` do GPT em `true` enquanto persistirem os 502 nesta máquina.
- Não use `enabled: false` para o GPT sem também rediscutir o quórum/metodologia; isso foi o que criou os 434 falsos pendentes.
- Não interprete `qtd. violações` como quantidade de organizações ou casos: é quantidade de regras diagnósticas infringidas.
- O relatório de integridade corrigido preserva avaliações válidas anteriores a erros posteriores; não reverta essa seleção para “último registro”.
- Trate avaliações e ajustes gerados por IA como minutas sujeitas à revisão da equipe de auditoria.

## Objetivo da próxima sessão

Retomar com segurança o reparo dirigido das avaliações dos comentários do gestor, validar a integridade de dados e pareceres, regenerar os produtos pós-contraditório e revisar os relatórios finais — especialmente o AN08 e o Capítulo 5 do relatório consolidado — antes da geração dos DOCX definitivos.

Repositório: `/home/acba/workspace/fiscalizacoes/202601-igovti`

Antes de agir, leia `AGENTS.md`. O worktree já estava amplamente modificado pelo usuário e por trabalhos anteriores; preserve alterações não relacionadas e não reverta arquivos em bloco.

## Contexto do incidente

Foi investigada uma inconsistência grave na avaliação dos comentários do gestor: no caso `UERJ / A5G20`, uma opinião individual devolveu corretamente `A5G20`, mas também introduziu uma conclusão externa sobre `q2708`. A consolidação e o mapeamento de ajustes aceitavam a união dos códigos retornados pelos avaliadores. Isso permitiu que a conclusão externa gerasse ajustes em respostas sem vínculo com `A5G20`, removendo indevidamente uma situação do resultado final.

O preflight e o arquivo `resumo-secao-2.json` apenas tornavam o efeito visível; não eram a origem do erro. A origem era combinada:

1. ausência de validação de pertencimento da resposta ao caso;
2. construção do escopo do juiz pela união das conclusões dos modelos;
3. mapeamento da seção 1 pelo estado temporal global, sem exigir que o motivo específico estivesse `afastado`;
4. ausência de uma porta de integridade antes da aplicação dos ajustes.

A inspeção mais ampla encontrou casos com códigos externos, motivos ausentes ou externos, estados temporais incompatíveis com os estados dos motivos e duas decisões antigas classificadas como `inconclusiva`. O usuário determinou que não exista classificação inconclusiva: insuficiência de elementos deve resultar em manutenção da situação, com não acolhimento ou acolhimento parcial conforme os motivos efetivamente afastados.

## Decisões substantivas já tomadas

- Ajustes da seção 1 devem ser aplicados por motivo, e somente quando o motivo ativo correspondente estiver classificado como `afastado`.
- Uma situação `mantida` pode gerar ajustes parciais se parte dos motivos tiver sido afastada.
- `afastada_na_data_base` e `corrigida_posteriormente` só são coerentes quando todos os motivos ativos tiverem sido afastados.
- Ausência ou insuficiência de prova mantém a situação; não usar `inconclusiva` nem `inconclusivo` no perfil temporal dos comentários do gestor.
- O juiz deve receber os itens autoritativos do caso, nunca a união de códigos sugeridos pelos avaliadores.
- Um caso pode ser consolidado com o quórum configurado de três avaliações válidas. A ausência de um avaliador opcional não invalida o caso; avaliação inválida conta como aviso e só exige reparo quando derruba o quórum ou quando o parecer consolidado é inválido.
- O reparo deve alcançar somente os casos afetados, mas usar todos os avaliadores atualmente habilitados. A configuração atual tem cinco avaliadores habilitados, inclusive `qwen3.7-plus`; o usuário aceitou o reparo dirigido com os avaliadores configurados, não uma reavaliação completa do universo pelo Qwen.
- Caso UERJ `A4G13`: restaurar `q2708[A] = Sim` e `q2708[B] = Sim`; manter `q2708[C] = Não` e `q2708[D] = Não`. A situação `A4G13` permanece caracterizada pelo fundamento relativo à segurança da informação. A legislação e o Manual de Cargos apresentados bastam para comprovar os cargos/funções de TIC.
- Não gerar ajustes, resultados ou relatórios definitivos enquanto a validação de integridade não estiver `conforme` e sem casos de reprocessamento.

## Implementação realizada nesta sessão

### Contrato de escopo e coerência

Criado `scripts/avaliacao_evidencias/scope_validation.py`, com validação determinística de:

- conjunto exato e cardinalidade dos `item_codigo`;
- duplicidade e códigos externos;
- conjunto exato dos motivos ativos;
- estados temporais permitidos;
- estados dos motivos permitidos;
- coerência entre estado temporal e estados dos motivos.

Integrações principais:

- `scripts/comentarios_gestor_pipeline.py` rejeita respostas individuais e pareceres do juiz fora do escopo;
- checkpoints inválidos não são tratados como avaliações utilizáveis;
- `scripts/avaliacao_evidencias/consolidation_core.py` prefere itens autoritativos gravados no caso; para checkpoints legados, só aceita fallback quando todas as opiniões possuem exatamente o mesmo conjunto de códigos;
- o juiz dos comentários recebe itens autoritativos, não a união das conclusões.

### Nova versão do prompt temporal

Criado:

`scripts/avaliacao_evidencias/prompt_catalogs/igovti_2026_comentarios_gestor_atual_v3.yml`

O catálogo exige preservação exata de `item_codigo` e `id_motivo`, elimina `inconclusiva` e manda manter a situação quando a prova for insuficiente.

O default foi atualizado em:

- `scripts/comentarios_gestor_pipeline.py`;
- `scripts/gerar_pacote_relatorios_igovti.py`.

Também foram removidos os estados temporais/motivos inconclusivos de:

- `scripts/avaliacao_evidencias/providers/response.py`;
- `scripts/avaliacao_evidencias/providers/base.py`;
- `scripts/avaliacao_evidencias/providers/fake.py`.

### Mapeamento dos ajustes por motivo

`mapear_ajustes_secao1` foi alterado para:

- validar o parecer antes do mapeamento;
- exigir que a conclusão pertença ao código da situação;
- correlacionar `id_motivo` do parecer com os motivos ativos do contexto;
- gerar ajustes somente para ações de motivos `afastado`;
- aceitar ajustes parciais de situações `mantida`;
- registrar justificativa e estado do motivo no papel de trabalho.

O caso contaminado `UERJ / A5G20` deixou de gerar qualquer ajuste em `q2708`.

### Revisão técnica reprodutível da UERJ

Criado:

`02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor/revisoes_respostas.yml`

Ele registra de forma declarativa e aprovada os ajustes `q2708[A]` e `q2708[B]` para `Sim`, vinculados ao caso `UERJ / A4G13`, ao `case_id` vigente e às referências documentais. `carregar_revisoes_respostas` materializa essas decisões e recusa revisões sem correspondência com o parecer vigente.

Antes da interrupção, uma leitura sem escrita confirmou:

- `q2708[B] = Sim` pelo motivo `MR048` afastado;
- `q2708[A] = Sim` pela revisão técnica documentada;
- `q2708[B] = Sim` também garantido pela revisão técnica;
- nenhum ajuste de `UERJ / A5G20` em `q2708`.

### Validação e reparo dirigido no CLI

Criado `scripts/comentarios_gestor_integridade.py`.

Adicionadas ações em `scripts/run_comentarios_gestor.py`:

- `validar-integridade`;
- `reparar-integridade`.

Artefatos produzidos:

- `02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor/preflight/validacao-integridade.json`;
- `.../validacao-integridade.xlsx`;
- `.../casos-reprocessamento.json`.

`reparar-integridade`:

1. prepara os casos autoritativos;
2. lê o manifesto de reparo;
3. reavalia somente os casos afetados com todos os avaliadores habilitados;
4. reconsolida somente os pareceres afetados;
5. preserva os demais registros;
6. valida novamente o conjunto.

`gerar-ajustes` e a ação `completo` agora bloqueiam a aplicação dos ajustes quando a integridade estiver reprovada.

As novas rotinas foram expostas em `scripts/argos_cli.py`. O orquestrador principal passou a aceitar `--revisoes-respostas` e usar o catálogo v3.

### Testes

Última execução local:

```bash
scripts/.venv/bin/python -m unittest discover -s scripts/tests -p 'test_*.py'
```

Resultado: 71 testes aprovados.

## Estado atual dos dados

Última validação completa, antes da tentativa de reparo:

- status: `reparo_necessario`;
- seção 1: 65 casos no manifesto;
- seção 2: 16 casos no manifesto;
- total: 81 casos.

O arquivo autoritativo para conferir esses números é:

`02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor/preflight/validacao-integridade.json`

Há centenas de avisos sobre avaliações individuais antigas inválidas, mas um caso só entra no reparo quando o quórum fica abaixo de três ou quando o parecer consolidado vigente viola o contrato. Não transformar todo aviso isolado em reprocessamento integral.

## Execução interrompida

Foi iniciado `reparar-integridade`, mas o usuário pediu para parar. Não há processo ativo; isso foi confirmado com `ps`.

A tentativa acrescentou registros de erro aos checkpoints históricos de três avaliadores, sem apagar resultados anteriores:

- Gemini 3.1;
- Gemini 3.5;
- GPT Luna.

Erros observados: `Temporary failure in name resolution`, inclusive durante upload Gemini. Os checkpoints são append-only. Não apague esses registros: a retomada, com `skip_errors=False`, repetirá as identidades que terminaram em erro. Não há evidência de chamadas bem-sucedidas ou consolidações novas nessa tentativa curta.

O `resumo-execucao.json` não representa a tentativa abortada; consulte os checkpoints e refaça a validação.

## Próximos passos obrigatórios

### 1. Garantir rede e executar novamente os testes

Não exponha o conteúdo de `.env`. Carregue-o no shell apenas para a execução:

```bash
cd /home/acba/workspace/fiscalizacoes/202601-igovti
scripts/.venv/bin/python -m unittest discover -s scripts/tests -p 'test_*.py'
set -a
source .env
set +a
```

### 2. Retomar o reparo dirigido

```bash
scripts/.venv/bin/python scripts/run_comentarios_gestor.py reparar-integridade \
  --respostas-comentarios 02-Execucao/05-Comentarios_Gestor/01-Coleta_LimeSurvey/20260716-respostas-bruto.xlsx \
  --evidencias-comentarios-root 02-Execucao/05-Comentarios_Gestor/01-Coleta_LimeSurvey/Evidencias_Coletadas/evidencias_extraidas \
  --out-dir 02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor
```

Não execute `completo`: com a versão nova do prompt, isso pode disparar reavaliação desnecessária do universo completo. O comando correto é `reparar-integridade`.

### 3. Validar novamente

```bash
scripts/.venv/bin/python scripts/run_comentarios_gestor.py validar-integridade \
  --respostas-comentarios 02-Execucao/05-Comentarios_Gestor/01-Coleta_LimeSurvey/20260716-respostas-bruto.xlsx \
  --evidencias-comentarios-root 02-Execucao/05-Comentarios_Gestor/01-Coleta_LimeSurvey/Evidencias_Coletadas/evidencias_extraidas \
  --out-dir 02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor
```

Porta obrigatória:

- `status = conforme`;
- zero casos de reprocessamento nas duas seções;
- nenhum parecer temporal inconclusivo;
- nenhum código ou motivo externo;
- pelo menos três avaliações válidas por caso.

Se falhar, não gerar ajustes. Investigue os casos remanescentes e repita o reparo.

### 4. Gerar e revisar os ajustes

Execute `gerar-ajustes` com os mesmos caminhos e com:

`--revisoes-respostas 02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor/revisoes_respostas.yml`

O comando possui porta de integridade. Depois, revise todas as linhas de `Ajustes` e `Pendências` em:

`02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor/ajustes_respostas_questionario_pos_comentarios_gestor.xlsx`

Pendências materiais devem ser resolvidas por decisão técnica explícita e reprodutível em `revisoes_respostas.yml`; não inventar valores.

Confirme especialmente os quatro itens `q2708` da UERJ e a permanência de `A4G13`.

### 5. Gerar produtos e cenários finais

A sequência completa, já detalhada na resposta anterior ao usuário, é:

1. `gerar_produtos_pos_comentarios_gestor.py` — somente os três produtos básicos;
2. orquestrador `gerar_pacote_relatorios_igovti.py`, etapas 19 a 21 — iGovTI corrente, auditoria pós-comentários e impactos;
3. `03-Relatorios/99-Avaliacao_Comentarios_Gestor/calcular_dados_comentarios_gestor.py` com avaliação final, ajustes e impactos;
4. revisão manual do AN08 e do Capítulo 5;
5. geração do DOCX do AN08;
6. etapas 22 e 23 — gráficos e relatórios individuais finais;
7. etapas 24 e 25 — relatório consolidado e validação final.

Use `--force-stage` nas etapas 19 a 25 para não adotar produtos antigos como definitivos. Não retome pela etapa 17 depois do reparo dirigido.

## Controles de qualidade antes da assinatura

O próximo agente deve verificar, a partir dos produtos finais e não de números antigos do Markdown:

- coerência entre base pós-comentários, iGovTI, auditoria, impactos, relatórios individuais, AN08 e relatório consolidado;
- ausência de `inconclusiva` em produtos e narrativa institucional;
- tabela manifestação do gestor × decisão técnica;
- concordâncias com situação ajustada apenas quando algum motivo tiver sido efetivamente afastado;
- justificativa de não acolhimento ou acolhimento parcial;
- totais de respondentes, não respondentes, manifestações, anexos e itens reavaliados;
- redução de situações e achados;
- variação do iGovTI;
- permanência de achados sustentados por motivos não afastados;
- nomes dos DOCX iguais à lista de anexos;
- inexistência de referências institucionais a providers, modelos, juiz de IA ou automação decisória;
- linguagem formal, simples, objetiva, imparcial e impessoal;
- recursos gráficos incorporados e nenhuma advertência de mídia ausente;
- `02-Execucao/00-Controle_Execucao/validacao-final.json` aprovado.

O script estatístico não edita `anexo-avaliacao-comentarios-gestor.md`; a atualização do texto do AN08 é atividade técnica/editorial manual baseada na memória de cálculo validada.

## Arquivos centrais para inspeção

- `scripts/avaliacao_evidencias/scope_validation.py`
- `scripts/comentarios_gestor_integridade.py`
- `scripts/comentarios_gestor_pipeline.py`
- `scripts/run_comentarios_gestor.py`
- `scripts/comentarios_gestor_produtos.py`
- `scripts/avaliacao_evidencias/consolidation_core.py`
- `scripts/avaliacao_evidencias/prompt_catalogs/igovti_2026_comentarios_gestor_atual_v3.yml`
- `scripts/avaliacao_evidencias/configs/comentarios_gestor_models_v1.json`
- `02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor/revisoes_respostas.yml`
- `02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor/revisoes_pareceres.yml`
- `02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor/preflight/validacao-integridade.json`
- `03-Relatorios/99-Avaliacao_Comentarios_Gestor/anexo-avaliacao-comentarios-gestor.md`
- `03-Relatorios/01-Relatorio_Consolidado/Relatório_altaresolucao_novo.md`

## Suggested skills

- `escrever-relatorio-auditoria`: usar na revisão do AN08, do Capítulo 5 e do relatório consolidado, depois que os dados finais estiverem estabilizados.
- `handoff`: usar novamente se a execução precisar ser interrompida antes da validação final.

Não é necessário usar uma skill de matriz de planejamento para esta continuação, salvo se a investigação revelar erro no mapa de verificação ou na lógica dos achados.
