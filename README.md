# Fiscalização 18/2026 - Índice de Governança de TI (iGovTI)

**Tribunal de Contas do Estado do Rio de Janeiro (TCE-RJ)**
*Auditoria Temática de Governança e Gestão de Tecnologia da Informação*

---

## 📌 Visão Geral

Este repositório armazena os **Papéis de Trabalho Digitais** referentes à Fiscalização nº 18/2026. O objetivo principal é avaliar o nível de maturidade em Governança de TI dos órgãos jurisdicionados estaduais e municipais do Rio de Janeiro, resultando na composição do índice **iGovTI-RJ**.

A auditoria adota uma abordagem baseada em riscos e conformidade, alinhada às normas internacionais de auditoria (ISSAIs) e aos frameworks de boas práticas de mercado (COBIT, ITIL, ISO 27001).

## 🎯 Objetivos

### Objetivo Geral
Avaliar se as estruturas de governança e gestão de TI dos jurisdicionados são adequadas para garantir o alinhamento estratégico, a conformidade legal (especialmente LGPD e leis de Governo Digital), a otimização de recursos e a mitigação de riscos operacionais.

### Objetivos Específicos
1.  **Diagnóstico:** Mapear a situação atual ("As-Is") da TI pública no estado.
2.  **Segurança:** Identificar vulnerabilidades críticas em segurança da informação.
3.  **Transparência:** Fomentar a publicação ativa de dados e serviços digitais.
4.  **Ranking:** Estabelecer um índice comparativo (iGovTI) para estimular a melhoria contínua.

## 📂 Estrutura do Repositório (Papéis de Trabalho)

A organização dos diretórios segue o ciclo de vida da auditoria governamental e os requisitos de documentação das normas da INTOSAI.

```text
tcerj-fisc-18-2026-igovti/
├── 01-Planejamento/           # Inteligência e Metodologia
│   ├── 01-Estudos_Preliminares/  # Benchmarking, Análise de Riscos e Monitoramento
│   ├── 02-Metodologia_iGovTI/    # Construção do Questionário e Critérios
│   └── 03-Estrategia_e_Plano/    # Documentos Formais (ISSAI 200/4000)
│
├── 02-Execucao/               # Campo e Evidências
│   ├── 01-Coleta_Dados/          # Respostas dos questionários e evidências brutas
│   ├── 02-Testes_Auditoria/      # Scripts de análise e validação
│   ├── 03-Achados_Preliminares/  # Descrição dos achados (situação encontrada, critérios de avaliação, evidências e propostas de encaminhamento)
│   └── 04-Matriz_Achados/        # Confronto Critério vs. Condição
│
├── 03-Relatorios/             # Produtos Finais
│   ├── Minutas, Relatórios Individuais e Relatório Consolidado
│
├── 04-Portal_iGovTI/          # Portal da Fiscalização
│   └── Documentação e requisitos do Portal da Fiscalização
│
└── 99-Gestao/                 # Administrativo
    ├── 01-Oficios_Apresentacao   # Portarias, Cronogramas, Ofícios e TSIDs
    ├── 02-TSIDs/                 # Termos de Solicitação de Informação e Documentos
    └── 99-Supervisao/            # Checklist de Supervisão
```

## ⚖️ Conformidade com Normas (ISSAIs)

Este projeto foi estruturado para garantir aderência às Normas Internacionais das Entidades Fiscalizadoras Superiores (ISSAIs):

*   **ISSAI 100 (Princípios):** Controles de Ética e Independência em `99-Gestao/`.
*   **ISSAI 4000 (Conformidade):**
    *   **Planejamento:** Matriz de Riscos em `01-Planejamento/01-Estudos_Preliminares`.
    *   **Execução:** Segregação clara entre evidências e achados em `02-Execucao`.
    *   **Responsabilização:** Matriz específica para nexo causal.

## 🛠️ Metodologia e Ferramentas

*   **iGovTI (Metodologia):** Baseada no modelo federal do TCU (iGG/iESGo), adaptada para a realidade municipal fluminense (foco em *Conformidade Legal* e *Estrutura Mínima*) e estadual (foco em *Governança Sistêmica* e *Segurança*).
*   **Análise de Dados:** Scripts de validação e cruzamento de dados localizados na pasta `scripts/`.
*   **Portal iGovTI:** Ferramenta web para dar publicidade aos resultados (especificações em `04-Portal_iGovTI/`).

## 🐍 Scripts de Automação

O repositório conta com scripts utilitários na pasta `scripts/` para automatizar etapas essenciais da fiscalização:

### 📋 Instalação de Dependências
Para rodar os scripts, instale as dependências declaradas no arquivo [requirements.txt](file:///home/acba/workspace/fiscalizacoes/tcerj-igovti-2026/scripts/requirements.txt):
```bash
pip install -r scripts/requirements.txt
```

### 1. Geração de Matrizes
*   **Matriz de Planejamento (`gerar_matriz_planejamento.py`):** Lê o arquivo Markdown e preenche um template do Word (`.docx`).
    *   *Como executar:*
        ```bash
        python scripts/gerar_matriz_planejamento.py 01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/matriz_planejamento.md
        ```
*   **Matriz de Achados (`gerar_matriz_achados.py`):** Preenche o modelo formal Word da Matriz de Achados cruzando a matriz de planejamento e o mapa de verificação.
    *   *Como executar:*
        ```bash
        python scripts/gerar_matriz_achados.py
        ```

### 2. Coleta e Avaliação de Evidências (IA)
*   **Coletar Anexos (`coletar_anexos_limesurvey.py`):** Baixa de forma automatizada todas as evidências submetidas pelas organizações no LimeSurvey.
    *   *Como executar:*
        ```bash
        python scripts/coletar_anexos_limesurvey.py
        ```
        *(Nota: Caso a sessão expire, atualize os cookies nas linhas 19 a 23 do script).*
*   **Extração de Evidências (`extrair_evidencias.py`):** Extrai de forma estruturada e plana todos os arquivos ZIP baixados para a pasta temporária de trabalho `/tmp/tcerj-igovti-2026/evidencias_extraidas`.
    *   *Como executar:*
        ```bash
        python scripts/extrair_evidencias.py
        ```
*   **Avaliação de Evidências (`avaliacao_evidencias`):** Executa o pipeline de avaliação de evidências por IA.
    *   *Como adicionar ou alterar um prompt:*
        1.  Edite o catálogo YAML, não os arquivos Markdown gerados:
            - catálogo conservador completo: `scripts/avaliacao_evidencias/prompt_catalogs/igovti_2026_conservador_v2.yml`;
            - catálogo binário para achados: `scripts/avaliacao_evidencias/prompt_catalogs/igovti_2026_achados_binario_v1.yml`.
        2.  No catálogo binário, cada entrada deve indicar `arquivo`, `coluna_evidencia`, `itens_avaliaveis` e, se aplicável, `criterios_pratica_principal`, `criterios_comuns_itens` ou `criterios_por_item`.
            - Use `criterios_comuns_itens` para critérios compartilhados por várias alternativas e `excluir_criterios_comuns_itens` para exceções.
            - Use `exibir_texto_itens: false` quando a avaliação deve considerar apenas os critérios listados, não o texto integral da alternativa do questionário. O pipeline respeita essa marcação e mascara `itens_afirmados[].texto` antes de chamar o provedor.
            - Em questões `adoption` com detalhamentos, como `q1001ext[A]`, mantenha o texto visível quando o detalhamento marcado for a própria afirmação a validar.
        3.  Não inclua itens que não exigem evidência no questionário, como `q0101[F]`, `q0102[E]` e `q0103[G]`.
        4.  Regenere os prompts Markdown após qualquer alteração no YAML.

    *   *Regenerar prompts conservadores:*
        ```bash
        scripts/.venv/bin/python -m scripts.avaliacao_evidencias.prompt_catalog build \
          scripts/avaliacao_evidencias/prompt_catalogs/igovti_2026_conservador_v2.yml \
          01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md \
          scripts/avaliacao_evidencias/prompts/igovti_2026_conservador_v2
        ```

    *   *Regenerar prompts binários para achados:*
        ```bash
        scripts/.venv/bin/python -m scripts.avaliacao_evidencias.prompt_catalog_achados build \
          scripts/avaliacao_evidencias/prompt_catalogs/igovti_2026_achados_binario_v1.yml \
          01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md \
          scripts/avaliacao_evidencias/prompts/igovti_2026_achados_binario_v1
        ```

    *   *Validar sem chamar IA remota (provider fake):*
        ```bash
        scripts/.venv/bin/python -m scripts.avaliacao_evidencias \
          02-Execucao/01-Questionario/20260621-respostas-questionario.xlsx \
          /tmp/tcerj-igovti-2026/evidencias_extraidas \
          --questionario 01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md \
          --prompts-dir scripts/avaliacao_evidencias/prompts/igovti_2026_achados_binario_v1 \
          --prompt-version igovti_2026_achados_binario_v1 \
          --only-prompts-present \
          --provider fake \
          --model fake \
          --out-dir /tmp/tcerj-igovti-2026/avaliacao_evidencias/teste-achados-binario
        ```

    *   *Como executar a avaliação binária de achados via OpenRouter:*
        ```bash
        export OPENROUTER_API_KEY="sua_chave_aqui"
        scripts/.venv/bin/python -m scripts.avaliacao_evidencias \
          02-Execucao/01-Questionario/20260621-respostas-questionario.xlsx \
          /tmp/tcerj-igovti-2026/evidencias_extraidas \
          --questionario 01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md \
          --prompts-dir scripts/avaliacao_evidencias/prompts/igovti_2026_achados_binario_v1 \
          --prompt-version igovti_2026_achados_binario_v1 \
          --only-prompts-present \
          --provider openrouter \
          --model google/gemini-2.5-flash \
          --rpm 12 \
          --out-dir 02-Execucao/03-Execucao_Procedimentos/avaliacao_evidencias/achados_binario_openrouter
        ```

    *   *Como executar via provider OpenAI-compatible local (`openai-oauth`):*
        ```bash
        scripts/.venv/bin/python -m scripts.avaliacao_evidencias \
          02-Execucao/01-Questionario/20260621-respostas-questionario.xlsx \
          02-Execucao/01-Questionario/Evidencias_Coletadas/evidencias_extraidas \
          --questionario 01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md \
          --prompts-dir scripts/avaliacao_evidencias/prompts/igovti_2026_achados_binario_v1 \
          --prompt-version igovti_2026_achados_binario_v1 \
          --only-prompts-present \
          --provider openai \
          --model gpt-5.4-mini \
          --rpm 12 \
          --out-dir 02-Execucao/03-Execucao_Procedimentos/avaliacao_evidencias/achados_binario_openai_gpt-5.4-mini
        ```

        O provider `openai` usa por padrão o endpoint local `http://127.0.0.1:10531/v1` e envia PDFs por `/v1/responses` como `input_file` em modo streaming. O proxy local normalmente não exige chave; se necessário, use `OPENAI_API_KEY`.

        Use `--auditados SIGLA` para processar apenas organizações específicas. Use `--list-only` para conferir as análises candidatas sem chamar o provedor. O parâmetro `--only-prompts-present` é obrigatório para conjuntos parciais de prompts, como `igovti_2026_achados_binario_v1`. Por padrão, o JSONL incremental é gravado como `analyses_<provider>_<model>.jsonl`; use `--out-file nome.jsonl` para escolher outro nome ou caminho. Para evidências PDF que devem ser avaliadas como Markdown com imagens extraídas, use `--pdf2md`. Para evidências DOCX que devem ser avaliadas como HTML com imagens extraídas, use `--docx2html`.

    *   **Orquestrador multi-modelo com barras de progresso (`run_avaliacao_evidencias_v2.py`):** Lança vários pipelines de avaliação em paralelo (cada um com seu provider, modelo e flags) e exibe **barras de progresso empilhadas** no terminal via `rich.Progress` — uma por modelo ativo. Substitui o antigo `scripts/run_avaliacao_evidencias.sh` com visibilidade de progresso em tempo real. Cada barra mostra: provider/modelo, barra de progresso, percentual, concluídos/total, erros (`✗`), puladas (`⏭`), tempo decorrido, ETA e status. Ao final, imprime uma tabela `rich.Table` com o resumo de cada modelo.

        A lista de modelos a executar está no topo do script (`MODELS = [...]`). Para ativar ou desativar modelos, edite o campo `enabled` de cada bloco; para adicionar um novo, copie um bloco e ajuste provider, model, rpm, reasoning, pdf2md, docx2html, store_prompts. Os modelos ativos por padrão são `gemini-3.1-flash-lite` (provider `gemini`) e `minimax-m3` (provider `opencodego`).

        *Rotação automática de chaves em 429 (Gemini):* quando a variável de ambiente `GEMINI_API_KEY` contém múltiplas chaves separadas por vírgula, o pipeline rotaciona para a próxima chave disponível imediatamente ao receber 429, em vez de esperar 30/60/120s. Se todas as chaves estiverem exauridas simultaneamente, o pipeline **pausa** pelo menor `Retry-After` e exibe um alerta amarelo no terminal; nenhum item é gravado como erro por rate limit. Limite de 5× 429 consecutivos na mesma chave faz com que ela seja abandonada (as outras continuam sendo tentadas). As demais flags de cada modelo (rpm, reasoning, pdf2md, docx2html, store_prompts) são preservadas pelo orquestrador.

        ```bash
        cd /home/acba/workspace/fiscalizacoes/tcerj-igovti-2026
        scripts/.venv/bin/python scripts/run_avaliacao_evidencias_v2.py
        ```

        O atalho `Ctrl+C` interrompe todos os subprocesses em paralelo com `terminate()` e exibe um resumo parcial do que foi processado até o momento.

*   **Consolidação por juiz IA (`consolidacao.py` + orquestrador):** Consolida as avaliações dos modelos em um parecer por evidência. Lê todos os `analyses*.jsonl` encontrados em `02-Execucao/03-Execucao_Procedimentos/avaliacao_evidencias/`, agrupa por `(auditado, questao, coluna_evidencia, evidencia)`, e envia cada grupo a um juiz IA com as avaliações preliminares + a evidência reenviada (quando `--evidencias-root` é informado). O juiz retorna um parecer consolidado (`conforme` / `nao_conforme` / `inconclusivo` / `erro`) com justificativa, lacunas e referências, sem mencionar provedores/modelos no texto. A opinião da equipe de auditoria pode ser injetada no prompt do juiz via `--auditor-opinions` (JSONL/JSON/CSV com campo `opiniao_auditoria` ou `parecer`).

    *Orquestrador multi-juiz com barras de progresso (`run_consolida_avaliacoes_v2.py`):* Lança vários juízes em paralelo (cada um com seu `judge_provider`/`judge_model`) e exibe **barras de progresso empilhadas** no terminal via `rich.Progress` — uma por juiz. Substitui o antigo `scripts/run_consolida_avaliacoes.sh`. Cada barra mostra: provider/modelo do juiz, barra de progresso, percentual, concluídos/total, erros (`✗`), puladas (`⏭`), tempo, ETA e status. Ao final, tabela `rich.Table` com o resumo por juiz. Suporta `--reasoning` e `--store-prompts` para paridade com a avaliação de evidências.

    O registro consolidado inclui: `identity`, `status`, `auditado`, `questao`, `coluna_evidencia`, `evidencia`, `judge_provider`, `judge_model`, `opinion_count`, `opinion_sources` (identities + providers + models das opiniões recebidas), `opiniao_auditoria`, `evidence_path`, `evidence_hash`, `result`, `error`, `started_at`, `finished_at`, `duration_seconds` e `reasoning_effort`. Com `--store-prompts`, também grava `prompt_payload` (payload textual enviado ao juiz). A rotação de chaves em 429 e a pausa por chaves exauridas funcionam do mesmo modo que na avaliação de evidências.

    A lista de juízes está no topo do script (`JUDGES = [...]`). Por padrão, apenas `gemini-3.1-flash-lite` (como juiz) está ativo. Para executar:

    ```bash
    cd /home/acba/workspace/fiscalizacoes/tcerj-igovti-2026
    scripts/.venv/bin/python scripts/run_consolida_avaliacoes_v2.py
    ```

    Para executar manualmente um juiz específico (sem o orquestrador), use o módulo `consolidacao`:

    ```bash
    export GEMINI_API_KEY="sua_chave_aqui"
    scripts/.venv/bin/python -m scripts.avaliacao_evidencias.consolidacao \
        02-Execucao/03-Execucao_Procedimentos/avaliacao_evidencias/analyses*.jsonl \
        --evidencias-root 02-Execucao/01-Questionario/Evidencias_Coletadas/evidencias_extraidas \
        --judge-provider gemini \
        --judge-model gemini-3.1-flash-lite \
        --reasoning high \
        --out-dir 02-Execucao/03-Execucao_Procedimentos/avaliacao_evidencias/consolidado
    ```

    Use `--auditor-opinions caminho/do/revisao_equipe.jsonl` para injetar opiniões textuais da equipe no prompt do juiz. Os registros consolidados são gravados como `consolidated.jsonl` dentro de `--out-dir`, e um XLSX de pareceres consolidados (`pareceres_consolidados.xlsx`) é gerado ao final. O JSONL exportado pelo **dashboard de revisão humana** (`scripts/dashboard_avaliacao_evidencias.html`) pode ser alimentado diretamente como `--auditor-opinions`, fechando o ciclo de revisão humana → juiz IA.

*   **Agregação das Avaliações (`agregar_analyses_por_item.py`):** Consolida os resultados de um ou mais arquivos JSONL de avaliação (`analyses*.jsonl`) por item do questionário, como `q0101`, `q1001` ou `q2101`. Para cada item, calcula o total de avaliações e os quantitativos de `conforme`, `nao_conforme`, `inconclusivo` e `erro`. A planilha também apresenta até dois exemplos de avaliações, com auditado, modelo, evidência, afirmação avaliada e justificativa.

    A saída possui três abas:

    - `Resumo por item`: uma linha por item, com quantitativos, percentuais e exemplos;
    - `Rastreabilidade`: todas as conclusões individuais usadas na agregação;
    - `Metadados`: arquivos processados, referência aplicada e totais da execução.

    O parâmetro `--referencia` filtra os registros pelo valor do campo `model` do JSONL de avaliação. Ele pode ser repetido quando for necessário combinar mais de um modelo. Sem esse parâmetro, todos os modelos encontrados serão agregados.

    *Como executar no Windows PowerShell, considerando somente o modelo `gemini-3.1-flash-lite`:*

    ```powershell
    $analyses = Get-ChildItem `
      "02-Execucao\03-Execucao_Procedimentos\avaliacao_evidencias" `
      -Recurse -Filter "analyses*.jsonl" -File |
      Select-Object -ExpandProperty FullName

    .\scripts\.venv\Scripts\python.exe scripts\agregar_analyses_por_item.py `
      @analyses `
      --referencia "gemini-3.1-flash-lite" `
      --output "02-Execucao\03-Execucao_Procedimentos\avaliacao_evidencias\consolidado\agregado_avaliacoes_por_item_gemini-3.1-flash-lite.xlsx"
    ```

    *Como agregar todos os modelos:*

    ```powershell
    .\scripts\.venv\Scripts\python.exe scripts\agregar_analyses_por_item.py `
      @analyses `
      --output "02-Execucao\03-Execucao_Procedimentos\avaliacao_evidencias\consolidado\agregado_avaliacoes_por_item.xlsx"
    ```

    *Como combinar duas referências:*

    ```powershell
    .\scripts\.venv\Scripts\python.exe scripts\agregar_analyses_por_item.py `
      @analyses `
      --referencia "gemini-3.1-flash-lite" `
      --referencia "mimo-v2.5-pro" `
      --output "02-Execucao\03-Execucao_Procedimentos\avaliacao_evidencias\consolidado\agregado_modelos_selecionados.xlsx"
    ```

### 3. Geração de Relatórios
*   **Geração do Relatório Consolidado (`gerar_relatorio_consolidado.py`):** Converte o Markdown do Relatório Consolidado para Word (`.docx`) aplicando referências cruzadas, quebras de página, sublinhados do Pandoc e estilos de tabela. O script automaticamente gera os gráficos e planifica todas as imagens em uma pasta temporária (sem poluir a pasta do relatório). Aceita o arquivo Markdown como parâmetro posicional, gera a saída com o mesmo nome `.docx` por padrão, e suporta recursos adicionais e wildcards via `--resource-files`.
    *   *Como executar:*
        ```bash
        scripts/.venv/bin/python scripts/gerar_relatorio_consolidado.py
        ```




## 👥 Equipe Técnica

*   **Unidade Técnica:** Coordenadoria de Auditoria de Tecnologia da Informação (CAD-TI/TCE-RJ).
*   **Responsável:** Equipe de Auditoria.

---
*© 2026 Tribunal de Contas do Estado do Rio de Janeiro - Repositório de Uso Interno/Restrito até a publicação do Relatório Final.*
