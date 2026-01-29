# Avaliação Comparativa de Instrumentos de Diagnóstico de TI (TCEs)

Este documento consolida a análise dos instrumentos de avaliação de Governança e Gestão de TI utilizados pelo TCE-PE, TCE-RS e TCE-RJ (vertentes Municípios e Estadual/SETIC).

## 1. Visão Geral dos Instrumentos

### 1.1 TCE-PE (Questionário 2025)
*   **Perfil:** Vanguarda tecnológica.
*   **Destaques:** Inclui temas emergentes como Inteligência Artificial e Sustentabilidade Ambiental (TI Verde). Foco forte na transformação digital e na perspectiva do cidadão.
*   **Estrutura:** Baseada no iGovTI/TCU, muito bem estruturada em processos.

### 1.2 TCE-RS (Diagnóstico)
*   **Perfil:** Realidade estrutural básica ("Chão de fábrica").
*   **Destaques:** Focado em identificar a existência mínima de estrutura (formalização da área) e a composição da força de trabalho (vínculos precários vs. efetivos).
*   **Uso:** Ideal para diagnósticos em entes com baixa maturidade para identificar riscos de continuidade.

### 1.3 TCE-RJ (Municípios - CAS-TI)
*   **Perfil:** Conformidade Legal e Regulatória.
*   **Destaques:** Verifica aderência a leis críticas para municípios (SIAFIC, Lei do Governo Digital, PNCP). Seção robusta de contratações baseada em Notas Técnicas do Tribunal.
*   **Uso:** Auditoria de conformidade e legalidade em entes municipais.

### 1.4 TCE-RJ (Estadual - SETIC)
*   **Perfil:** Governança Sistêmica e Corporativa.
*   **Contexto:** Aplicado às organizações que compõem o Sistema Estadual de Tecnologia da Informação e Comunicação (SETIC), regido pelo Decreto Estadual nº 47.278/2020.
*   **Destaques:**
    *   **Visão Sistêmica:** Não avalia o órgão isoladamente, mas sua inserção no sistema estadual (Relação Órgão Setorial vs. Órgão Central/PRODERJ).
    *   **Compliance Específico:** Verifica o atendimento a normativos estaduais estritos, como a Portaria PRODERJ nº 825/2021 (PGTIC/RJ e PEDTIC) e Instruções Normativas de Segurança (02/2022) e Hospedagem (03/2022).
    *   **Avaliação de Serviços Centrais:** Inclui a avaliação da satisfação do gestor setorial com os serviços e orientações prestados pelo PRODERJ.

---

## 2. Análise Comparativa Integrada

### Semelhanças
*   **Base Metodológica:** Todos derivam dos frameworks consagrados (COBIT, ITIL) e do modelo federal (iGovTI/iGG do TCU).
*   **Escala de Maturidade:** TCE-PE e as duas vertentes do TCE-RJ utilizam a mesma escala de 6 níveis (Não adota a Adota totalmente), permitindo comparabilidade de dados.
*   **Tripé Clássico:** Todos cobrem Planejamento (PDTI/PEDTIC), Estrutura (Comitês/Setores) e Pessoas.

### Diferenças Críticas

| Característica | TCE-PE | TCE-RS | TCE-RJ (Municípios) | TCE-RJ (Estado/SETIC) |
| :--- | :--- | :--- | :--- | :--- |
| **Foco Principal** | Inovação e Digital | Estrutura Básica | Legalidade Municipal | Governança Sistêmica |
| **Nível de Detalhe** | Alto (inclui IA/Verde) | Baixo (foco em existência) | Médio/Alto (foco em leis) | Alto (normas estaduais) |
| **Público-Alvo** | Geral | Pequenos Municípios | Municípios RJ | Órgãos Estaduais RJ |
| **Diferencial** | Temas Futuros | Raio-X da Precariedade | SIAFIC/PNCP | Relação com PRODERJ |

---

## 3. Recomendações para Fiscalização no Rio de Janeiro

Considerando o cenário heterogêneo do Rio de Janeiro, recomenda-se uma abordagem bifurcada:

### 3.1 Para o Âmbito ESTADUAL (Órgãos do SETIC)
A fiscalização deve priorizar a **Governança Sistêmica** e a **Segurança Corporativa**.

*   **Prioridade 1: Alinhamento ao PEDTIC e PGTIC (Q.1021, Q.1022 do Questionário SETIC):**
    *   Verificar se o órgão possui seu Plano Estratégico (PEDTIC) alinhado à estratégia estadual. Sem isso, os órgãos remam em direções opostas, desperdiçando recursos estaduais.
*   **Prioridade 2: Segurança da Informação e Conformidade com IN 02/2022 (Q.1024, Q.2160):**
    *   O estado é um alvo grande. A adesão às normas centrais de segurança do PRODERJ é vital para evitar vulnerabilidades que afetem a rede de governo (GovNet).
*   **Prioridade 3: Gestão de Contratos Centralizados vs. Descentralizados:**
    *   Avaliar se o órgão utiliza as Atas de Registro de Preços do PRODERJ (papel integrador) ou se realiza contratações próprias redundantes/ineficientes (Q.1037, Q.2300).

### 3.2 Para o Âmbito MUNICIPAL
A fiscalização deve priorizar a **Legalidade Financeira** e a **Sobrevivência Operacional**.

*   **Prioridade 1: Conformidade SIAFIC e PNCP (Modelo TCE-RJ Municípios):**
    *   É o "piso" da legalidade. Municípios fora desses padrões operam irregularmente.
*   **Prioridade 2: Profissionalização Mínima (Modelo TCE-RS):**
    *   Verificar se existe *algum* servidor efetivo responsável pela TI. A terceirização total da "inteligência" e das "senhas" é um risco soberano para o município.
*   **Prioridade 3: Serviços ao Cidadão (Lei Governo Digital):**
    *   Existência e atualização da Carta de Serviços.

---

## 4. O que pode ser "Deixado de Lado" (Depriorizado) no momento

Para garantir foco e efetividade nas auditorias atuais:

1.  **Desenvolvimento de Software Interno (Fábrica de Software):** Tanto no Estado quanto nos Municípios, a tendência é contratação de serviços (SaaS) ou uso de sistemas prontos. Avaliar maturidade de desenvolvimento (CMMI/MPS.BR) é pouco produtivo para a maioria. O foco deve ser na **Gestão do Contrato** de software.
2.  **Tecnologias Emergentes em Municípios Pequenos:** Cobrar IA ou Blockchain de municípios que ainda lutam com backup e conectividade básica desvia o foco dos riscos reais.
3.  **Burocracia Excessiva em Gestão de Projetos:** Para órgãos menores, cobrar metodologias complexas (PMBOK completo) pode paralisar a TI. O foco deve ser em "Entregas" e "Resultados" (Gerir com base em desempenho - item 2320 do questionário SETIC) mais do que em artefatos documentais de projeto.
