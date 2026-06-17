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
        2.  No catálogo binário, cada entrada deve indicar `arquivo`, `coluna_evidencia`, `itens_avaliaveis` e, se aplicável, `criterios_pratica_principal` ou `criterios_por_item`.
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
          02-Execucao/01-Questionario/20260611-respostas-questionario.xlsx \
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
          02-Execucao/01-Questionario/20260611-respostas-questionario.xlsx \
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

        Use `--auditados SIGLA` para processar apenas organizações específicas. Use `--list-only` para conferir as análises candidatas sem chamar o provedor. O parâmetro `--only-prompts-present` é obrigatório para conjuntos parciais de prompts, como `igovti_2026_achados_binario_v1`.

*   **Agregação das Avaliações (`agregar_analyses_por_item.py`):** Consolida os resultados de um ou mais arquivos `analyses.jsonl` por item do questionário, como `q0101`, `q1001` ou `q2101`. Para cada item, calcula o total de avaliações e os quantitativos de `conforme`, `nao_conforme`, `inconclusivo` e `erro`. A planilha também apresenta até dois exemplos de avaliações, com auditado, modelo, evidência, afirmação avaliada e justificativa.

    A saída possui três abas:

    - `Resumo por item`: uma linha por item, com quantitativos, percentuais e exemplos;
    - `Rastreabilidade`: todas as conclusões individuais usadas na agregação;
    - `Metadados`: arquivos processados, referência aplicada e totais da execução.

    O parâmetro `--referencia` filtra os registros pelo valor do campo `model` do `analyses.jsonl`. Ele pode ser repetido quando for necessário combinar mais de um modelo. Sem esse parâmetro, todos os modelos encontrados serão agregados.

    *Como executar no Windows PowerShell, considerando somente o modelo `gemini-3.1-flash-lite`:*

    ```powershell
    $analyses = Get-ChildItem `
      "02-Execucao\03-Execucao_Procedimentos\avaliacao_evidencias" `
      -Recurse -Filter analyses.jsonl -File |
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
