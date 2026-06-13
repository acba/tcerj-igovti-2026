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
*   **Matriz de Planejamento (`gerar_matriz_planejamento_docx.py`):** Lê o arquivo Markdown e preenche um template do Word (`.docx`).
    *   *Como executar:*
        ```bash
        python scripts/gerar_matriz_planejamento_docx.py 01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/matriz_planejamento.md
        ```
*   **Matriz de Achados (`gerar_matriz_achados.py`):** Preenche o modelo formal Word da Matriz de Achados cruzando a matriz de planejamento e o mapa de verificação.
    *   *Como executar:*
        ```bash
        python scripts/gerar_matriz_achados.py
        ```

### 2. Coleta e Avaliação de Evidências (IA)
*   **Coletar Anexos (`coletar_anexos.py`):** Baixa de forma automatizada todas as evidências submetidas pelas organizações no LimeSurvey.
    *   *Como executar:*
        ```bash
        python scripts/coletar_anexos.py
        ```
        *(Nota: Caso a sessão expire, atualize os cookies nas linhas 19 a 23 do script).*
*   **Extração de Evidências (`extrair_evidencias.py`):** Extrai de forma estruturada e plana todos os arquivos ZIP baixados para a pasta temporária de trabalho `/tmp/tcerj-igovti-2026/evidencias_extraidas`.
    *   *Como executar:*
        ```bash
        python scripts/extrair_evidencias.py
        ```
*   **Avaliação de Evidências (`avaliacao_evidencias`):** Executa o pipeline de avaliação de evidências por IA.
    *   *Como executar (exemplo via OpenRouter):*
        ```bash
        export OPENROUTER_API_KEY="sua_chave_aqui"
        python -m scripts.avaliacao_evidencias \
          02-Execucao/01-Questionario/20260611-respostas-questionario.xlsx \
          /tmp/tcerj-igovti-2026/evidencias_extraidas \
          --questionario 01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md \
          --prompts-dir scripts/avaliacao_evidencias/prompts/igovti_2026_conservador_v2 \
          --prompt-version v2 \
          --provider openrouter \
          --model google/gemini-2.5-flash \
          --rpm 12 \
          --out-dir 02-Execucao/03-Execucao_Procedimentos/avaliacao_evidencias/saida_openrouter
        ```

## 👥 Equipe Técnica

*   **Unidade Técnica:** Coordenadoria de Auditoria de Tecnologia da Informação (CAD-TI/TCE-RJ).
*   **Responsável:** Equipe de Auditoria.

---
*© 2026 Tribunal de Contas do Estado do Rio de Janeiro - Repositório de Uso Interno/Restrito até a publicação do Relatório Final.*
