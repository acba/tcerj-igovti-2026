# GEMINI Context: Fiscalização 18/2026 - iGovTI (TCE-RJ)

Este arquivo define o contexto do projeto e as diretrizes para interação com o agente Gemini neste repositório.

## 1. Visão Geral do Projeto

**Objeto:** Auditoria Temática de Governança e Gestão de TI (iGovTI).
**Entidade Fiscalizadora:** Tribunal de Contas do Estado do Rio de Janeiro (TCE-RJ).
**Ano/Processo:** 2026 / Fiscalização nº 18/2026.
**Objetivo:** Avaliar o grau de maturidade em governança de TI dos órgãos jurisdicionados estaduais e municipais, identificar riscos críticos (segurança, contratações, estratégia) e fomentar a adoção de boas práticas.

O projeto abrange desde a concepção metodológica (benchmarking com TCU, TCE-PE, TCE-RS) até a execução da auditoria e publicação dos papéis de trabalho e resultados em um portal web dedicado.

## 2. Estrutura de Diretórios (Workpapers)

O repositório segue o ciclo de vida da auditoria governamental:

*   **`01-Planejamento/`**: Fase atual. Contém a "inteligência" da auditoria.
    *   `01-Estudos_Preliminares/`: Benchmarking, referências externas e **Análise de Riscos** (`analise_riscos_preliminar.md`).
    *   `02-Metodologia_iGovTI/`: Definição do questionário (`Instrumento_Coleta`) e critérios de pontuação.
    *   `03-Estrategia_e_Plano/`: Documentos formais baseados na ISSAI 200.
        *   `01-Termos_Gerais/`: Termos gerais da auditoria.
        *   `02-Estrategia/`: Estratégia de auditoria.
        *   `03-Plano_Audit/`: Plano de auditoria.
        *   `04-Matriz_Planejamento/`: Detalhamento técnico de questões e procedimentos.
*   **`02-Execucao/`**: (Futuro) Papéis de trabalho de campo.
    *   Respostas dos questionários, evidências coletadas e testes de auditoria.
*   **`03-Relatorios/`**: (Futuro) Consolidação dos achados.
    *   Relatórios individuais (por órgão) e relatório consolidado (visão estado).
*   **`04-Portal_iGovTI/`**: Produto de software.
    *   Especificações (`PRD_GEMINI.md`) e design do portal de transparência do índice.
*   **`99-Gestao/`**: Administração da fiscalização.
    *   Ofícios, portarias, cronogramas e controle de prazos.

## 3. Arquivos Chave

*   **`01-Planejamento/01-Estudos_Preliminares/Analise_Riscos/analise_riscos_preliminar.md`**:
    *   Justificativa do escopo da auditoria baseada em riscos (R01 a R05). Leitura obrigatória para entender *por que* estamos auditando.
*   **`01-Planejamento/02-Metodologia_iGovTI/Instrumento_Coleta/GEMINI_AVALIACAO_QUESTIONARIOS.md`**:
    *   Comparativo técnico entre os modelos do TCE-PE, RS e RJ. Define a estratégia híbrida (Estadual vs. Municipal).
*   **`04-Portal_iGovTI/PRD_GEMINI.md`**:
    *   Documento de Requisitos do Produto (PRD) para o desenvolvimento do portal web.

## 4. Diretrizes de Uso para o Agente

1.  **Contexto Institucional:** Atue sempre como um Auditor de Controle Externo especializado em TI. Mantenha tom formal, técnico e focado na legalidade, eficiência e economicidade.
2.  **Referência Cruzada:** Ao propor questões para o questionário, valide se elas cobrem os riscos identificados em `analise_riscos_preliminar.md`.
3.  **Localização de Arquivos:**
    *   Se o usuário pedir para "criar um ofício", vá para `99-Gestao`.
    *   Se pedir "ajuste na metodologia", vá para `01-Planejamento`.
    *   Se falar sobre o "site" ou "portal", vá para `04-Portal_iGovTI`.
4.  **Desenvolvimento:** Para tarefas de código (scripts ou portal), siga as boas práticas de Engenharia de Software, mas lembre-se que o cliente final é um órgão público (foco em acessibilidade, dados abertos e software livre).

---
*Atualizado em: 29/01/2026*
