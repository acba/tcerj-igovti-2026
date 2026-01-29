# Proposta de Arquitetura de Questionário: Core + Módulos (Revisão Todos os Poderes)

Este documento apresenta a estrutura atualizada para os questionários de Governança e Gestão de TI do TCE-RJ. A arquitetura **"Core Comum + Extensões"** foi ajustada para cobrir não apenas o Poder Executivo (SETIC), mas também **Judiciário, Legislativo, Ministério Público e Defensoria Pública**, respeitando suas autonomias e vinculações a conselhos nacionais (CNJ, CNMP, etc.).

## 1. Visão Geral da Arquitetura

*   **Módulo CORE (Universal):** Práticas fundamentais aplicáveis a **qualquer** organização pública (Prefeitura, Secretaria de Estado, Tribunal, Assembleia). É a base da comparação transversal.
*   **Módulo MUNICIPAL:** Foco em Prefeituras (SIAFIC, Governo Digital Local).
*   **Módulo ESTADUAL (Multisetorial):**
    *   **Práticas Transversais:** Aplicáveis a todos os órgãos estaduais (escala, complexidade).
    *   **Trilha Executivo (SETIC):** Perguntas específicas sobre PRODERJ/Decretos do Governador.
    *   **Trilha Órgãos Autônomos:** Perguntas sobre alinhamento a Conselhos Nacionais (CNJ, CNMP).

---

## 2. Esqueleto Detalhado dos Domínios e Práticas

### DOMÍNIO 1: GOVERNANÇA E ESTRATÉGIA DE TI
*Foco: Direção, Decisão e Alinhamento.*

#### [CORE] Práticas Comuns (Todos)
*   **1.1. Estruturas de Decisão**
    *   1.1.1. Existência e funcionamento efetivo do Comitê de TI (Multidisciplinar).
    *   1.1.2. Posicionamento hierárquico da unidade de TI (Reporta à Alta Administração?).
*   **1.2. Planejamento Estratégico (PDTI)**
    *   1.2.1. Existência de PDTI vigente, aprovado e publicado.
    *   1.2.2. O PDTI possui metas claras, indicadores e orçamento estimado?
*   **1.3. Gestão de Riscos de TI**
    *   1.3.1. Processo institucionalizado de gestão de riscos de TI.

#### [MÓDULO ESTADUAL] Práticas Específicas
*   **1.E.1. Alinhamento Estratégico Vertical (Strategy Alignment)**
    *   *Pergunta Condicional:* O PDTI do órgão está alinhado à estratégia superior de TI da sua esfera?
        *   **(Executivo):** Alinhamento ao PGTIC/RJ e PEDTIC (Portaria 825/2021).
        *   **(Judiciário):** Alinhamento à ENTIC-JUD (Resoluções CNJ).
        *   **(MP):** Alinhamento à Estratégia Nacional do CNMP.
        *   **(Legislativo/Outros):** Alinhamento ao Planejamento Estratégico Institucional.

#### [MÓDULO MUNICIPAL] Práticas Específicas
*   **1.M.1. Governança Digital Local**
    *   1.M.1.1. Regulamentação local da Lei do Governo Digital.

---

### DOMÍNIO 2: GESTÃO DE SERVIÇOS E SISTEMAS
*Foco: Entrega de Valor e Processos.*

#### [CORE] Práticas Comuns (Todos)
*   **2.1. Gestão de Serviços (ITSM)**
    *   2.1.1. Catálogo de Serviços de TI atualizado e divulgado.
    *   2.1.2. Gestão de Nível de Serviço (SLA) com áreas de negócio.
    *   2.1.3. Processo formal de Gestão de Incidentes (Service Desk).
*   **2.2. Gestão de Processos**
    *   2.2.1. Metodologia de Gestão de Projetos de TI implantada.

#### [MÓDULO ESTADUAL] Práticas Específicas
*   **2.E.1. Interoperabilidade e Integração**
    *   **(Executivo):** Hospedagem em ambiente PRODERJ (IN 03/2022) e uso do SEI-RJ.
    *   **(Autônomos):** Integração com sistemas nacionais (ex: PJe/E-Proc no Judiciário, sistemas do CNMP).

#### [MÓDULO MUNICIPAL] Práticas Específicas
*   **2.M.1. Conformidade Fiscal (SIAFIC)**
    *   2.M.1.1. O sistema contábil atende ao padrão SIAFIC (Decreto 10.540)?
    *   2.M.1.2. Integração automatizada com o PNCP.

---

### DOMÍNIO 3: SEGURANÇA DA INFORMAÇÃO E PRIVACIDADE
*Foco: Proteção e Conformidade. Crítico para todos os Poderes.*

#### [CORE] Práticas Comuns (Todos)
*   **3.1. Gestão de Segurança (GSI)**
    *   3.1.1. Política de Segurança (POSIC) formalizada e comunicada.
    *   3.1.2. Gestor de Segurança (CISO) formalmente nomeado.
*   **3.2. Resiliência Cibernética**
    *   3.2.1. Política de Backup: Existência de backup **offline/imutável** (Proteção contra Ransomware).
    *   3.2.2. Testes periódicos de restauração (Restore) realizados e documentados.
    *   3.2.3. Plano de Continuidade de Negócios (PCN) ou Resposta a Incidentes.
*   **3.3. Privacidade (LGPD)**
    *   3.3.1. Encarregado de Dados (DPO) nomeado.
    *   3.3.2. Inventário de Dados Pessoais realizado.

#### [MÓDULO ESTADUAL] Práticas Específicas
*   **3.E.1. Normatização Específica**
    *   **(Executivo):** Aderência à IN PRODERJ 02/2022.
    *   **(Judiciário):** Aderência à Resolução CNJ 396/2021 (Cibersegurança).

---

### DOMÍNIO 4: GESTÃO DE PESSOAS
*Foco: Capacidade Operacional.*

#### [CORE] Práticas Comuns (Todos)
*   **4.1. Força de Trabalho**
    *   4.1.1. O órgão possui quadro próprio de TI (Carreira de TI)?
    *   4.1.2. Proporção de Servidores Efetivos vs. Terceirizados/Comissionados.
    *   4.1.3. O Gestor de TI é do quadro efetivo ou livre nomeação?

#### [MÓDULO MUNICIPAL] Práticas Específicas
*   **4.M.1. Profissionalização**
    *   4.M.1.1. Existência de *pelo menos um* profissional de TI com vínculo estável (Mitigação de risco de descontinuidade administrativa).

---

### DOMÍNIO 5: CONTRATAÇÕES DE TI
*Foco: Legalidade e Economicidade.*

#### [CORE] Práticas Comuns (Todos)
*   **5.1. Planejamento da Contratação**
    *   5.1.1. Plano de Contratações Anual (PAC-TI) elaborado e alinhado ao Orçamento.
    *   5.1.2. Uso de Estudos Técnicos Preliminares (ETP) padronizados.
*   **5.2. Fiscalização**
    *   5.2.1. Fiscais de contrato tecnicamente capacitados para o objeto licitado.

#### [MÓDULO ESTADUAL] Práticas Específicas
*   **5.E.1. Otimização do Gasto Público**
    *   **(Executivo):** Consulta prévia ao PRODERJ (IN 01/2021) e uso de ARPs corporativas.
    *   **(Autônomos):** Adoção de práticas de compartilhamento de soluções (ex: Softwares Públicos do Judiciário).

---

### DOMÍNIO 6: INOVAÇÃO E CIDADÃO
*Foco: Sociedade.*

#### [CORE] Práticas Comuns (Todos)
*   **6.1. Transparência e Acesso**
    *   6.1.1. Carta de Serviços ao Usuário/Cidadão.
    *   6.1.2. Pesquisa de Satisfação dos serviços digitais.

---

## 3. Resumo da Estratégia de Aplicação

1.  **Questionário Único para o Estado:** Um único formulário digital que, na pergunta de perfil ("Qual seu Poder/Natureza Jurídica?"), habilita ou oculta as seções específicas (Executivo vs. Autônomos).
2.  **Questionário Único para Municípios:** Focado na realidade das Prefeituras (Core + Módulo Municipal).
3.  **Comparabilidade:** Os relatórios gerenciais poderão comparar o "Domínio 3 - Segurança" entre um Tribunal de Justiça e uma Prefeitura, pois as perguntas do CORE são idênticas.