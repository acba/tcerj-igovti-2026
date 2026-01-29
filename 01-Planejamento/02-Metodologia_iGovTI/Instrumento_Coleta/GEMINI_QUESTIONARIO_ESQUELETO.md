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

## 2. Esqueleto Detalhado e Rastreabilidade

A coluna "Origem" mapeia a questão para os questionários anteriores (**MUN**: Municípios/CAS-TI, **SETIC**: Estadual/SETIC) para garantir a série histórica.

### DOMÍNIO 1: GOVERNANÇA E ESTRATÉGIA DE TI
*Foco: Direção, Decisão e Alinhamento.*

#### [CORE] Práticas Comuns (Todos)
*   **1.1. Estruturas de Decisão**
    *   1.1.1. Existência e funcionamento efetivo do Comitê de TI (Multidisciplinar). `[Origem: MUN 1111 / SETIC 1111]`
    *   1.1.2. Existência e posicionamento hierárquico da unidade de TI. `[Origem: SETIC 1011 / MUN 2251]`
*   **1.2. Planejamento Estratégico (PDTI)**
    *   1.2.1. Existência de PDTI vigente, aprovado e publicado. `[Origem: MUN 2112 / SETIC 1022]`
    *   1.2.2. Monitoramento da execução do PDTI pela Alta Administração. `[Origem: MUN 1121 / SETIC 1121]`
*   **1.3. Gestão de Riscos de TI**
    *   1.3.1. Processo institucionalizado de gestão de riscos de TI. `[Origem: MUN 2140 / SETIC 2140]`

#### [MÓDULO ESTADUAL] Práticas Específicas
*   **1.E.1. Alinhamento Estratégico Vertical**
    *   *Pergunta Condicional:* O PDTI do órgão está alinhado à estratégia superior de TI da sua esfera? `[Origem: SETIC 1021 / 2113]`
        *   **(Executivo):** Alinhamento ao PGTIC/RJ e PEDTIC (Portaria 825/2021).
        *   **(Judiciário/MP/Leg):** Alinhamento à Estratégia Nacional (CNJ/CNMP) ou Institucional.

#### [MÓDULO MUNICIPAL] Práticas Específicas
*   **1.M.1. Governança Digital Local**
    *   1.M.1.1. Regulamentação local da Lei do Governo Digital. `[Origem: MUN 1141]`

---

### DOMÍNIO 2: GESTÃO DE SERVIÇOS E SISTEMAS
*Foco: Entrega de Valor e Processos.*

#### [CORE] Práticas Comuns (Todos)
*   **2.1. Gestão de Serviços (ITSM)**
    *   2.1.1. Catálogo de Serviços de TI atualizado e divulgado. `[Origem: MUN 2121 / SETIC 2121]`
    *   2.1.2. Gestão de Nível de Serviço (SLA) com áreas de negócio. `[Origem: MUN 2131 / SETIC 2131]`
    *   2.1.3. Processo formal de Gestão de Incidentes (Service Desk). `[Origem: MUN 2124 / SETIC 2124]`
*   **2.2. Gestão de Processos**
    *   2.2.1. Metodologia de Gestão de Projetos de TI implantada. `[Origem: MUN 2181 / SETIC 2181]`
    *   2.2.2. Processo de Software (Aquisição ou Desenvolvimento Seguro). `[Origem: MUN 2170 / SETIC 2170]`

#### [MÓDULO ESTADUAL] Práticas Específicas
*   **2.E.1. Interoperabilidade e Integração**
    *   **(Executivo):** Hospedagem em ambiente PRODERJ e uso de sistemas corporativos. `[Origem: SETIC 1025]`
    *   **(Autônomos):** Integração com sistemas nacionais de referência.

#### [MÓDULO MUNICIPAL] Práticas Específicas
*   **2.M.1. Conformidade Fiscal (SIAFIC)**
    *   2.M.1.1. O sistema contábil atende ao padrão SIAFIC (Decreto 10.540)? `[Origem: MUN 1145]`
    *   2.M.1.2. Integração automatizada com o PNCP e Proc. Adm. Eletrônico. `[Origem: MUN 1146 / 1144]`

---

### DOMÍNIO 3: SEGURANÇA DA INFORMAÇÃO E PRIVACIDADE
*Foco: Proteção e Conformidade. Crítico para todos os Poderes.*

#### [CORE] Práticas Comuns (Todos)
*   **3.1. Gestão de Segurança (GSI)**
    *   3.1.1. Política de Segurança (POSIC) formalizada e comunicada. `[Origem: MUN 2151 / SETIC 2151]`
    *   3.1.2. Gestor de Segurança (CISO) formalmente nomeado. `[Origem: MUN 2153 / SETIC 2153]`
*   **3.2. Resiliência Cibernética**
    *   3.2.1. Política de Backup: Existência de backup offline/imutável. `[Origem: MUN 2166 / SETIC 2166]`
    *   3.2.2. Testes periódicos de restauração (Restore). `[Refinamento de 2166]`
    *   3.2.3. Plano de Continuidade e Resposta a Incidentes. `[Origem: MUN 2142 / SETIC 2154]`
    *   3.2.4. Gestão de Acessos e Identidades. `[Origem: MUN 2162 / SETIC 2162]`
*   **3.3. Privacidade (LGPD)**
    *   3.3.1. Encarregado de Dados (DPO) nomeado e Inventário realizado. `[Novo/Aprofundamento]`

#### [MÓDULO ESTADUAL] Práticas Específicas
*   **3.E.1. Normatização Específica**
    *   **(Executivo):** Aderência à IN PRODERJ 02/2022. `[Origem: SETIC 1024]`
    *   **(Judiciário):** Aderência à Resolução CNJ 396/2021.

---

### DOMÍNIO 4: GESTÃO DE PESSOAS
*Foco: Capacidade Operacional.*

#### [CORE] Práticas Comuns (Todos)
*   **4.1. Força de Trabalho**
    *   4.1.1. Definição de perfis profissionais e competências. `[Origem: MUN 2211 / SETIC 2211]`
    *   4.1.2. Dimensionamento quantitativo da força de trabalho. `[Origem: MUN 2213 / SETIC 2213]`
*   **4.2. Capacitação**
    *   4.2.1. Ações de capacitação e treinamento. `[Origem: MUN 2231 / SETIC 2167]`

#### [MÓDULO MUNICIPAL] Práticas Específicas
*   **4.M.1. Profissionalização Mínima**
    *   4.M.1.1. Existência de profissional de TI com vínculo estável. `[Foco TCE-RS]`

#### [MÓDULO ESTADUAL] Práticas Específicas
*   **4.E.1. Capacitação Sistêmica**
    *   **(Executivo):** Utilização da Academia PRODERJ. `[Origem: SETIC 2233]`

---

### DOMÍNIO 5: CONTRATAÇÕES DE TI
*Foco: Legalidade e Economicidade.*

#### [CORE] Práticas Comuns (Todos)
*   **5.1. Planejamento da Contratação**
    *   5.1.1. Plano de Contratações Anual (PAC-TI) publicado. `[Origem: MUN 2331 / SETIC 2361]`
    *   5.1.2. Uso de Estudos Técnicos Preliminares (ETP) e Análise de Riscos. `[Origem: MUN 2341 / 2311]`
*   **5.2. Fiscalização**
    *   5.2.1. Monitoramento e fiscais capacitados. `[Origem: MUN 2343 / SETIC 2343]`
    *   5.2.2. Aderência às Notas Técnicas do TCE-RJ. `[Origem: MUN 2351 / SETIC 2351]`

#### [MÓDULO ESTADUAL] Práticas Específicas
*   **5.E.1. Otimização do Gasto Público**
    *   **(Executivo):** Consulta prévia ao PRODERJ e uso de ARPs. `[Origem: SETIC 1023 / 1037]`

---

### DOMÍNIO 6: INOVAÇÃO E CIDADÃO
*Foco: Sociedade.*

#### [CORE] Práticas Comuns (Todos)
*   **6.1. Transparência e Acesso**
    *   6.1.1. Carta de Serviços ao Usuário atualizada e digital. `[Origem: MUN 1143]`
    *   6.1.2. Participação do usuário e Pesquisa de Satisfação. `[Origem: MUN 1132 / 1133]`

---

## 3. Notas sobre o Mapeamento

1.  **Questões de Satisfação (Contexto):** Perguntas do questionário SETIC antigo focadas puramente em satisfação (ex: "Qual a satisfação com a comunicação do Diretor Geral?") foram movidas para uma seção de "Feedback" opcional no final do Módulo Estadual, pois não medem a maturidade do órgão auditado, mas sim a qualidade do serviço do órgão central.
2.  **Manutenção da Escala:** As questões do CORE mantêm a escala de resposta de 6 níveis (Não adota a Adota totalmente) para permitir a comparação direta com os dados de 2023.
