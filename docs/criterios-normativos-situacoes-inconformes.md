---
title: "Critérios Normativos Específicos Aplicáveis às Situações Inconformes"
subtitle: "Fiscalização TCE-RJ nº 18/2026 — iGovTI 2026"
date: "27 de agosto de 2026"
author: "Equipe de Auditoria de TI — TCE-RJ"
lang: pt-BR
---

# Critérios Normativos Específicos Aplicáveis às Situações Inconformes

**Fiscalização:** TCE-RJ nº 18/2026 — iGovTI 2026  
**Data de corte da pesquisa:** 27/08/2026  
**Público-alvo:** Equipe de Auditoria de TI  
**Objeto:** Mapeamento aprofundado e fundamentação de critérios normativos específicos e vinculantes aplicáveis às 24 situações inconformes da matriz de planejamento aos entes auditados do Poder Executivo Estadual fluminense, do Tribunal de Justiça do Estado do Rio de Janeiro (TJRJ) e do Ministério Público do Estado do Rio de Janeiro (MPRJ).

---

## 1. Alertas Normativos e Status de Vigência

Antes da aplicação aos achados e relatórios, é fundamental observar a consolidação das normas em vigor e a revogação de atos anteriores:

1. **Poder Executivo Estadual / PRODERJ:**
   - **Contratações de TIC:** A *IN PRODERJ/PRE nº 01/2021* foi **revogada** expressamente pela **Instrução Normativa PRODERJ/PRE nº 05, de 20/03/2024**, que passa a ser o marco regulatório das contratações de TIC na Administração Direta e Indireta do Executivo estadual.
   - **Segurança da Informação:** A *IN PRODERJ/PRE nº 02/2022* foi **revogada** expressamente pela **Instrução Normativa PRODERJ/PRE nº 07, de 29/05/2025**, ato vigente que disciplina a segurança da informação, papéis e resposta a incidentes.
   - **Estrutura do SETIC / NSTIC:** O regime vigente foi consolidado pelo **Decreto Estadual nº 48.997/2024**, que reestruturou o SETIC e alterou as disposições do Decreto Estadual nº 47.278/2020.
   - **Regulamento Geral da Lei nº 14.133/2021 no ERJ:** O **Decreto Estadual nº 48.816/2023** regulamenta a governança das contratações e a equipe de planejamento da contratação no Poder Executivo estadual. O **Decreto Estadual nº 48.749/2023** regulamenta o Plano de Contratações Anual (PCA).

2. **Tribunal de Justiça do Estado do Rio de Janeiro (TJRJ) / CNJ:**
   - **Contratações de TIC:** A *Resolução CNJ nº 182/2013* foi **revogada** pela **Resolução CNJ nº 468, de 15/07/2022** (com redação consolidada pelas Resoluções nº 480/2022 e nº 616/2025).
   - **Governança e Estratégia de TIC:** A **Resolução CNJ nº 370/2021** (ENTIC-JUD 2021–2026) permanece vigente e é o marco orientador nacional de estrutura, governança, pessoal, serviços e planejamento.
   - **Normas Locais do TJRJ:** Aplicam-se a **Resolução TJ/OE nº 04/2021** (estrutura da SGTEC), o **Ato Normativo TJ nº 32/2023** (Política de Governança, Gestão e Infraestrutura de TIC), o **Ato Normativo TJ nº 27/2022** (CGTIC, PDTIC, orçamento e PAC) e o **Ato Normativo TJ nº 28/2022** (Gestão de Serviços de TIC, Catálogo, ANS e Incidentes). O *Ato Normativo TJ nº 16/2018* foi revogado.

3. **Ministério Público do Estado do Rio de Janeiro (MPRJ) / CNMP:**
   - **Contratações de TIC:** A *Resolução CNMP nº 102/2013* foi **revogada** pela **Resolução CNMP nº 283, de 05/02/2024**, novo marco obrigatório para contratações de TIC em todos os ramos do Ministério Público.
   - **Governança Nacional:** A **Resolução CNMP nº 171/2017** (Política Nacional de TI do MP) permanece vigente e estrutura os macroprocessos, PETI, PDTI, CETI e serviços.
   - **Normas Locais do MPRJ:** Aplicam-se a novel **Resolução GPGJ nº 2.785, de 06/05/2026** (Política de Governança e Gestão de TI do MPRJ), a **Resolução GPGJ nº 2.540/2023** (*consolidada pela Resolução GPGJ nº 2.738/2025* — instituição do CETI), a **Resolução GPGJ nº 2.675/2025** (estrutura da SGMTI e STIC vinculadas à PGJ) e a **Resolução GPGJ nº 2.757/2025** (acesso a recursos, ativos e incidentes de segurança).

---

## 2. Mapa Geral de Aderência por Situação Inconforme

Legenda de Aderência:
- **(D) Direto:** O normativo estabelece dever expresso, específico e coincidente com a situação auditada.
- **(P) Parcial / Reforço:** O normativo dá respaldo à matéria, mas não contém todos os elementos da situação (deve ser combinado com critérios gerais como COBIT, ITIL, ISO ou jurisprudência do TCE-RJ).
- **(L) Lacuna em norma específica:** Ausência de obrigação formal expressa e pública no ente; o tema deve ser tratado sob a ótica de boa prática, governança e risco (Recomendação).

| Código | Descrição da Situação Inconforme | Poder Executivo Estadual (Decretos e PRODERJ) | TJRJ (CNJ e TJRJ) | MPRJ (CNMP e MPRJ) |
| :--- | :--- | :--- | :--- | :--- |
| **S1.1** | Ausência de área, unidade, setor ou função de TIC formalmente instituída. | **(D)** Dec. Est. 48.997/2024 (arts. 2º e 4º); Port. PRODERJ 825/2021 (Anexo A, arts. 1º, IX, 8º e 9º). | **(D)** Res. CNJ 370/2021 (arts. 21 a 23); Res. TJ/OE 04/2021. | **(D)** Res. CNMP 171/2017 (arts. 9º e 16); Res. GPGJ 2.675/2025 (art. 1º); Res. GPGJ 2.785/2026 (arts. 7º a 10). |
| **S1.2** | Área de TIC sem atribuições formais definidas ou sem atribuições de gestão de TIC. | **(D)** Dec. Est. 48.997/2024 (art. 4º, I a XI); Port. PRODERJ 825/2021 (Anexo A). | **(D)** Res. CNJ 370/2021 (arts. 21 a 23); Ato Normativo TJ 32/2023 (arts. 8º a 10). | **(D)** Res. CNMP 171/2017 (arts. 16 e 18); Res. GPGJ 2.785/2026 (arts. 7º a 10 e 13). |
| **S1.3** | Posicionamento organizacional inadequado da área de TIC. | **(P)** O Dec. Est. 48.997/2024 institui e coordena o nível setorial, mas não define vínculo uniforme com a alta administração. (*Reforço: Port. SGD/ME 778/2019, art. 4º, § 1º*). | **(D)** Res. CNJ 370/2021 (arts. 22 e 23); Ato Normativo TJ 32/2023 (arts. 3º e 9º). | **(D)** Res. CNMP 171/2017 (art. 16, caput); Res. GPGJ 2.675/2025 (art. 1º); Res. GPGJ 2.785/2026 (art. 7º). |
| **S2.1** | Ausência de objetivos, indicadores ou metas para a gestão de TIC. | **(P/D)** Port. PRODERJ 825/2021 (Anexo C, arts. 2º, 13 e 14); Dec. Est. 46.644/2019 (arts. 3º e 4º). | **(D)** Res. CNJ 370/2021 (arts. 7º, I, 42, 46 e 48); Ato Normativo TJ 27/2022 (arts. 2º a 4º). | **(D)** Res. CNMP 171/2017 (arts. 11, 12 e 14); Res. GPGJ 2.540/2023 (art. 2º); Res. GPGJ 2.785/2026 (arts. 5º, 11 e 12). |
| **S2.2** | Comitê de TIC não instituído formalmente ou sem representação relevante. | **(D)** Port. PRODERJ 825/2021 (Anexo C, art. 5º – Comitê Permanente do PEDTIC). | **(D)** Res. CNJ 370/2021 (art. 7º); Ato Normativo TJ 27/2022 e Ato Normativo TJ 32/2023 (CGTIC). | **(D)** Res. CNMP 171/2017 (arts. 13 e 14); Res. GPGJ 2.540/2023 (arts. 1º e 3º – CETI). |
| **S2.3** | Comitê de TIC sem atuação efetiva comprovada. | **(P)** Port. PRODERJ 825/2021 (Anexo C, arts. 5º e 6º – atas em processo SEI/RJ). | **(D)** Res. CNJ 370/2021 (arts. 7º, 8º e 44); Ato Normativo TJ 27/2022 (arts. 2º e 3º). | **(D)** Res. CNMP 171/2017 (arts. 13 e 14); Res. GPGJ 2.540/2023 (arts. 2º, 4º e 5º – reuniões trimestrais e relatório anual). |
| **S3.1** | Inexistência ou insuficiência do processo de planejamento de TIC (PDTI/PEDTIC). | **(D)** Port. PRODERJ 825/2021 (arts. 2º a 5º e Anexo C); IN PRODERJ 05/2024 (arts. 5º e 6º). | **(D)** Res. CNJ 370/2021 (arts. 6º a 8º e 42); Ato Normativo TJ 32/2023 (arts. 10 e 11). | **(D)** Res. CNMP 171/2017 (arts. 9º, 11 e 12); Res. GPGJ 2.785/2026 (arts. 11 e 12). |
| **S3.2** | Ausência de aprovação formal do plano de TIC pela autoridade competente. | **(D)** Port. PRODERJ 825/2021 (Anexo C, arts. 3º, III e IV, e 11, parágrafo único). | **(D)** Res. CNJ 370/2021 (art. 7º, II); Ato Normativo TJ 32/2023 (art. 11, § 1º). | **(D)** Res. CNMP 171/2017 (arts. 12 e 14); Res. GPGJ 2.540/2023 (art. 2º, II); Res. GPGJ 2.785/2026 (art. 12, p. único). |
| **S3.4** | Plano de TIC sem alinhamento adequado ao planejamento institucional. | **(D)** Port. PRODERJ 825/2021 (arts. 1º, 3º e 4º; Anexo C, arts. 1º e 2º). | **(D)** Res. CNJ 370/2021 (arts. 6º e 42); Res. CNJ 325/2020; Ato Normativo TJ 27/2022 (art. 4º). | **(D)** Res. CNMP 171/2017 (arts. 11 e 12); Res. CNMP 204/2019; Res. GPGJ 2.785/2026 (arts. 5º, III, 11 e 12). |
| **S3.5** | Plano de TIC não utilizado na elaboração da proposta orçamentária e do PCA. | **(D)** Port. PRODERJ 825/2021 (art. 1º, V-VIII; arts. 4º e 5º); IN PRODERJ 05/2024 (art. 5º); Dec. Est. 48.749/2023. | **(D)** Res. CNJ 370/2021 (art. 6º); Res. CNJ 468/2022 (arts. 4º e 5º); Ato Normativo TJ 27/2022 (arts. 5º e 6º). | **(D)** Res. CNMP 283/2024 (arts. 4º a 6º); Res. GPGJ 2.540/2023 (art. 2º, II); Res. GPGJ 2.785/2026 (art. 13, III). |
| **S3.6** | Ausência de acompanhamento da execução do plano de TIC. | **(D)** Port. PRODERJ 825/2021 (Anexo C, arts. 3º, 7º, 11 e 13). | **(P/D)** Res. CNJ 370/2021 (arts. 8º, V, 46 e 48); Ato Normativo TJ 32/2023 (art. 11, § 2º). | **(D)** Res. CNMP 171/2017 (arts. 12, 14 e 16); Res. GPGJ 2.540/2023 (art. 2º, V); Res. GPGJ 2.785/2026 (arts. 5º e 13, I). |
| **S4.1** | Ausência de força de trabalho dedicada à TIC. | **(P)** Dec. Est. 48.997/2024 (art. 4º); IN PRODERJ 07/2025 (art. 11, VI e § 2º). | **(D)** Res. CNJ 370/2021 (art. 24, caput – quadro permanente exclusivo). | **(P)** Res. CNMP 171/2017 (arts. 16 e 33); Res. GPGJ 2.675/2025 e 2.785/2026. |
| **S4.2** | Quantitativo necessário de pessoal não definido documentadamente. | **(L/P)** Não há ato geral impositivo no Executivo. (*Reforço: COBIT 2019 APO07.01; Acórdão TCE-RJ 44.490/2024*). | **(D)** Res. CNJ 370/2021 (art. 24, §§ 1º a 3º – Guia de Dimensionamento do Judiciário). | **(L/P)** Res. CNMP 171/2017 (art. 8º, § 1º, "d"); Res. CNMP 283/2024 (art. 10, III, "b"). |
| **S4.3** | Ausência de cargos/funções formalmente atribuídos à TIC ou Segurança. | **(P/D)** IN PRODERJ 07/2025 (arts. 11, 17 e 18 – Gestor de Segurança e ETIR); Dec. Est. 48.997/2024 (art. 4º). | **(P)** Res. CNJ 370/2021 (arts. 23 e 24); Res. CNJ 396/2021 (art. 7º); Ato Normativo TJ 32/2023. | **(P)** Res. CNMP 171/2017 (arts. 16 e 33); Res. CNMP 294/2024; Res. GPGJ 2.675/2025 e 2.757/2025. |
| **S4.6** | Operação de TIC predominantemente terceirizada sem profissionais internos. | **(P)** Dec. Est. 48.997/2024 (art. 4º); IN PRODERJ 07/2025. (*Reforço: Acórdão TCE-RJ 44.490/2024, II.7*). | **(D)** Res. CNJ 370/2021 (art. 24, caput); Res. CNJ 468/2022 (art. 8º, § 1º – vedada terceirização de gestão). | **(D/P)** Res. CNMP 171/2017 (arts. 16 e 33); Res. CNMP 283/2024 (art. 9º, § 2º e art. 33). |
| **S5.1** | Inexistência ou insuficiência do catálogo de serviços de TIC. | **(L)** Sem norma geral no Executivo (*Reforço: ISO 20000-2 item 8.2.4; COBIT APO09.02; Acórdão TCE-RJ 44.490/2024*). | **(D)** Res. CNJ 370/2021 (art. 21, IV, "d"); Ato Normativo TJ 28/2022 (arts. 4º e 5º). | **(D)** Res. CNMP 171/2017 (arts. 14, V, e 23); Res. GPGJ 2.785/2026 (art. 13, IV); Res. GPGJ 2.675/2025 (art. 2º, VIII). |
| **S5.2** | Ausência ou fragilidade na definição e no monitoramento de ANS/SLA. | **(P)** IN PRODERJ 07/2025 (Anexo, item 8.9.2.1 – SLA contratual). (*Reforço: ITIL 4; Acórdão TCE-RJ 44.490/2024*). | **(D)** Res. CNJ 370/2021 (arts. 18 a 20 e 21, IV, "d"); Ato Normativo TJ 28/2022 e Anexo (tempos e metas). | **(D)** Res. CNMP 171/2017 (arts. 14, VI, e 23); Res. GPGJ 2.785/2026 (arts. 5º, IX, e 13, IV); Res. GPGJ 2.540/2023 (art. 2º, VIII). |
| **S5.3** | Inventário de ativos de TIC (hardware e software) inexistente ou insuficiente. | **(D)** Dec. Est. 48.997/2024 (art. 4º, V); IN PRODERJ 07/2025 (Anexo, itens 7.1 e 8.1). | **(D)** Res. CNJ 370/2021 (art. 21, IV, "c", art. 23 e art. 34, § 2º); Res. CNJ 396/2021 (art. 6º). | **(D)** Res. CNMP 171/2017 (art. 26, II); Res. GPGJ 2.785/2026 (art. 13, VI e VII); Res. GPGJ 2.757/2025. |
| **S5.4** | Ausência ou fragilidade do processo de gestão de configuração. | **(P)** IN PRODERJ 07/2025 (Anexo, itens 7.2.1.5, 8.1.1 e 8.10 – baseline seguro). (*Reforço: ISO 20000-2; COBIT BAI10.01*). | **(P)** Res. CNJ 370/2021 (arts. 19 e 21, IV, "c"). (*Reforço: ISO 20000-2 item 8.2.6; COBIT BAI10.01*). | **(D)** Res. CNMP 171/2017 (arts. 18, 19 e 26, II); Res. GPGJ 2.785/2026 (art. 13, VI, "b"). |
| **S5.5** | Inexistência ou fragilidade na gestão de incidentes de TIC. | **(P/D em Segurança)** IN PRODERJ 07/2025 (arts. 11 a 13, 17 e 18; Anexo item 8.14). (*Reforço em serviços: ISO 20000-2; ITIL 4*). | **(D)** Res. CNJ 370/2021 (art. 21, II, "a", e IV, "f"); Res. CNJ 396/2021 (arts. 7º e 8º); Ato Normativo TJ 28/2022 (art. 4º). | **(D)** Res. CNMP 171/2017 (arts. 23, 27 e 28); Res. CNMP 294/2024; Res. GPGJ 2.785/2026 (art. 13, IV e VII); Res. GPGJ 2.757/2025. |
| **S6.1** | Inexistência ou fragilidade de fluxo formal para planejamento de contratações. | **(D)** IN PRODERJ 05/2024 (arts. 1º, 4º a 7º, 11 e ss. – DOD, ETP, Riscos, TR); Dec. Est. 48.816/2023; Lei 14.133/2021. | **(D)** Res. CNJ 468/2022 (arts. 6º, 7º, 10, 11, 15 e 29); Ato Normativo TJ 27/2022 (arts. 5º e 6º); Lei 14.133/2021. | **(D)** Res. CNMP 283/2024 (arts. 2º, 6º, 8º a 10, 16, 17 e 20); Res. GPGJ 2.785/2026 (art. 13, III); Lei 14.133/2021. |
| **S6.2** | Contratações de TIC sem análise prévia e aprovação técnica da TIC. | **(D)** Dec. Est. 48.997/2024 (art. 5º); IN PRODERJ 05/2024 (arts. 4º, 7º, 8º e 28 – parecer/aprovação técnica setorial e PRODERJ). | **(D)** Res. CNJ 468/2022 (arts. 7º, 8º, 10, 14 e 15 – aprovação e assinatura obrigatória do Integrante Técnico nos artefatos). | **(D)** Res. CNMP 283/2024 (arts. 9º, 16, 20 e 33 – validação e subscrição técnica obrigatória dos artefatos). |
| **S6.3** | Contratações de TIC sem alinhamento ao Plano de TIC e ao PCA. | **(D)** IN PRODERJ 05/2024 (art. 5º – vedação expressa); Dec. Est. 48.749/2023; Lei 14.133/2021 (art. 12, VII e art. 18, § 1º, II). | **(D)** Res. CNJ 468/2022 (arts. 4º e 5º); Res. CNJ 370/2021 (art. 6º); Ato Normativo TJ 27/2022 (art. 5º); Lei 14.133/2021. | **(D)** Res. CNMP 283/2024 (arts. 4º a 6º); Res. GPGJ 2.540/2023 (art. 2º, II); Lei 14.133/2021. |
| **S6.4** | Ausência de equipe de planejamento com integrante técnico da área de TIC. | **(D/P)** Dec. Est. 48.816/2023 (arts. 6º a 8º); IN PRODERJ 05/2024 (arts. 6º e 7º); Lei 14.133/2021 (art. 7º). | **(D)** Res. CNJ 468/2022 (art. 7º, caput e incisos I a III, e art. 8º – designação formal de integrante demandante, técnico e administrativo). | **(D)** Res. CNMP 283/2024 (art. 8º, caput e incisos I a III, e art. 9º – designação formal com integrante técnico da área de TI). |

---

## 3. Detalhamento Temático por Questão de Auditoria

### Questão 01 — Estrutura de TIC

#### S1.1 — Ausência de área, unidade, setor ou função de TIC formalmente instituída
- **Poder Executivo Estadual:**
  * *Decreto Estadual nº 48.997/2024, arts. 2º e 4º:* Reestrutura o Sistema Estadual de TIC (SETIC) e estabelece os Níveis Setoriais de TIC (NSTIC/RJ) representados pelas Assessorias de Informática ou setores equivalentes em todos os órgãos e entidades da Administração Direta e Indireta.
  * *Portaria PRODERJ/PRE nº 825/2021, Anexo A, arts. 1º (IX), 8º e 9º:* Define o NSTIC como a unidade de TIC responsável pela coordenação técnica e execução das diretrizes no órgão setorial.
- **TJRJ / CNJ:**
  * *Resolução CNJ nº 370/2021, arts. 21 a 23:* Determina que os órgãos do Poder Judiciário devem dispor de estrutura organizacional de TIC formalizada para sustentar as estratégias institucionais.
  * *Resolução TJ/OE nº 04/2021 e Ato Normativo TJ nº 32/2023, arts. 3º e 8º:* Formaliza a Secretaria-Geral de Tecnologia da Informação (SGTEC) e departamentos especializados no TJRJ.
- **MPRJ / CNMP:**
  * *Resolução CNMP nº 171/2017, arts. 9º, 16 e 33:* Impõe a estruturação formal da unidade de TIC em cada Ministério Público.
  * *Resolução GPGJ nº 2.675/2025, art. 1º e Resolução GPGJ nº 2.785/2026, arts. 7º a 10:* Estrutura a Secretaria-Geral de Modernização e TIC (SGMTI) e a Secretaria de TIC (STIC) do MPRJ.

#### S1.2 — Área de TIC sem atribuições formais suficientes
- **Poder Executivo Estadual:**
  * *Decreto Estadual nº 48.997/2024, art. 4º, incisos I a XI:* Fixa expressamente o rol de competências mínimas dos setores de TIC (planejamento, segurança, governança, infraestrutura e gestão).
  * *Portaria PRODERJ/PRE nº 825/2021, Anexo A, arts. 8º e 9º:* Responsabilidades do gestor de TIC na condução do PEDTIC e governança setorial.
- **TJRJ / CNJ:**
  * *Resolução CNJ nº 370/2021, arts. 21 a 23:* Atribuições essenciais da área de TIC (planejamento, projetos, sustentação, segurança, dados e serviços).
  * *Ato Normativo TJ nº 32/2023, arts. 8º a 10:* Competências regimentais detalhadas da SGTEC e unidades subordinadas.
- **MPRJ / CNMP:**
  * *Resolução CNMP nº 171/2017, arts. 16 e 18:* Atribuições e macroprocessos obrigatórios de TIC.
  * *Resolução GPGJ nº 2.785/2026, arts. 7º a 10 e 13:* Competências formais da SGMTI e STIC para a gestão e sustentação dos serviços de tecnologia.

#### S1.3 — Posicionamento organizacional inadequado da área de TIC
- **Poder Executivo Estadual:**
  * *Decreto Estadual nº 48.997/2024, art. 4º, § 1º:* Estabelece a coordenação técnica dos setores equivalentes pelo PRODERJ, sem impor vínculo hierárquico uniforme com a alta administração. (*Critério complementar: Portaria SGD/ME nº 778/2019, art. 4º, § 1º e COBIT 2019 APO01.06*).
- **TJRJ / CNJ:**
  * *Resolução CNJ nº 370/2021, arts. 22 e 23:* Determina nível hierárquico estratégico e canal direto de interlocução com a cúpula do Tribunal.
  * *Ato Normativo TJ nº 32/2023, arts. 3º e 9º:* Posiciona a SGTEC como Secretaria-Geral vinculada à Presidência.
- **MPRJ / CNMP:**
  * *Resolução CNMP nº 171/2017, art. 16, caput:* Determina subordinação direta da área de TIC ao Procurador-Geral de Justiça ou à administração superior.
  * *Resolução GPGJ nº 2.675/2025, art. 1º e Resolução GPGJ nº 2.785/2026, art. 7º:* Vinculação direta da SGMTI ao Procurador-Geral de Justiça.

---

### Questão 02 — Governança e Comitê de TIC

#### S2.1 — Ausência de objetivos, indicadores ou metas para a gestão de TIC
- **Poder Executivo Estadual:**
  * *Portaria PRODERJ/PRE nº 825/2021, Anexo C, arts. 2º, 13 e 14:* Exige a fixação de metas, indicadores e monitoramento de desempenho no PEDTIC.
  * *Decreto Estadual nº 46.644/2019, arts. 3º e 4º:* Política de Governança Pública Estadual (estabelecimento de metas e indicadores).
- **TJRJ / CNJ:**
  * *Resolução CNJ nº 370/2021, arts. 7º (I), 42, 46 e 48:* Obrigatoriedade de indicadores e metas de TIC aprovados e acompanhados pelo Comitê de Governança.
  * *Ato Normativo TJ nº 27/2022, arts. 2º a 4º:* Disciplina os indicadores estratégicos de TIC e acompanhamento no PJERJ.
- **MPRJ / CNMP:**
  * *Resolução CNMP nº 171/2017, arts. 11, 12 e 14:* Fixação e monitoramento de indicadores e metas pelo Comitê Estratégico de TI.
  * *Resolução GPGJ nº 2.540/2023, art. 2º e Resolução GPGJ nº 2.785/2026, arts. 5º, 11 e 12:* Metas e acompanhamento estratégico no MPRJ.

#### S2.2 — Comitê de TIC não instituído ou sem representação relevante
- **Poder Executivo Estadual:**
  * *Portaria PRODERJ/PRE nº 825/2021, Anexo C, art. 5º:* Determina a instituição formal do **Comitê Permanente do PEDTIC** em todos os órgãos e entidades, com composição multidisciplinar mínima (Gestor de TIC / NSTIC como Presidente, Planejamento, Orçamento, Administração/Patrimônio, Área-Fim e Alta Administração).
- **TJRJ / CNJ:**
  * *Resolução CNJ nº 370/2021, art. 7º:* Obriga a criação do Comitê de Governança de TIC (CGTIC) multidisciplinar (magistrados, áreas finalísticas, administrativa e TIC).
  * *Ato Normativo TJ nº 27/2022 e Ato Normativo TJ nº 32/2023:* Formaliza a composição e funcionamento do CGTIC no PJERJ.
- **MPRJ / CNMP:**
  * *Resolução CNMP nº 171/2017, arts. 13 e 14:* Exige Comitê Estratégico de Tecnologia da Informação (CETI) com representação multidisciplinar.
  * *Resolução GPGJ nº 2.540/2023 (consolidada c/ Res. 2.738/2025), arts. 1º a 3º:* Institui o CETI no MPRJ com caráter permanente e deliberativo.

#### S2.3 — Comitê de TIC sem atuação efetiva comprovada
- **Poder Executivo Estadual:**
  * *Portaria PRODERJ/PRE nº 825/2021, Anexo C, arts. 5º e 6º:* Exige atuação contínua, deliberações em processo SEI/RJ e registros formais de atas.
- **TJRJ / CNJ:**
  * *Resolução CNJ nº 370/2021, arts. 7º, 8º e 44 e Ato Normativo TJ nº 27/2022, arts. 2º e 3º:* Periodicidade regular de reuniões, atas com registro de deliberação e acompanhamento de portfólio de projetos.
- **MPRJ / CNMP:**
  * *Resolução CNMP nº 171/2017, arts. 13 e 14 e Resolução GPGJ nº 2.540/2023, arts. 2º, 4º e 5º:* Exige reuniões com periodicidade mínima trimestral, atas publicadas e relatório anual consolidado de atividades.

---

### Questão 03 — Planejamento de TIC

#### S3.1 — Inexistência ou insuficiência do processo de planejamento de TIC
- **Poder Executivo Estadual:**
  * *Portaria PRODERJ/PRE nº 825/2021, arts. 2º a 5º e Anexo C:* Disciplina a obrigatoriedade, rito e conteúdo mínimo do Plano Estratégico e Diretor de TIC (PEDTIC).
  * *IN PRODERJ/PRE nº 05/2024, arts. 5º e 6º:* Condiciona os processos operacionais à existência e vigência do PEDTIC.
- **TJRJ / CNJ:**
  * *Resolução CNJ nº 370/2021, arts. 6º a 8º e 42:* Metodologia estruturada para elaboração do Plano Diretor de TIC (PDTIC).
  * *Ato Normativo TJ nº 32/2023, arts. 10 e 11 e Ato Normativo TJ nº 27/2022, arts. 4º a 6º:* Ciclo de planejamento do PDTIC no TJRJ.
- **MPRJ / CNMP:**
  * *Resolução CNMP nº 171/2017, arts. 9º, 11 e 12:* Obrigação de elaborar o PDTI e PETI.
  * *Resolução GPGJ nº 2.785/2026, arts. 11 e 12:* Regulamenta o planejamento de TIC e elaboração do PETI-MPRJ e PDTI-MPRJ.

#### S3.2 — Ausência de aprovação formal do plano de TIC
- **Poder Executivo Estadual:**
  * *Portaria PRODERJ/PRE nº 825/2021, Anexo C, arts. 3º (III e IV) e 11 (parágrafo único):* Exige ato formal de aprovação do PEDTIC pelo Dirigente Máximo do órgão/entidade e publicação no Diário Oficial.
- **TJRJ / CNJ:**
  * *Resolução CNJ nº 370/2021, art. 7º (II) e Ato Normativo TJ nº 32/2023, art. 11, § 1º:* Aprovação formal do PDTIC pelo Presidente do Tribunal após parecer do CGTIC.
- **MPRJ / CNMP:**
  * *Resolução CNMP nº 171/2017, arts. 12 e 14 (I) e Resolução GPGJ nº 2.785/2026, art. 12, p. único:* Aprovação formal do PETI/PDTI pelo Procurador-Geral de Justiça.

#### S3.4 — Plano de TIC sem alinhamento institucional
- **Poder Executivo Estadual:**
  * *Portaria PRODERJ/PRE nº 825/2021, arts. 1º, 3º e 4º e Anexo C, arts. 1º e 2º:* Alinhamento obrigatório do PEDTIC ao Planejamento Estratégico Institucional e à EGTIC/RJ.
- **TJRJ / CNJ:**
  * *Resolução CNJ nº 370/2021, arts. 6º e 42 c/c Resolução CNJ nº 325/2020 e Ato Normativo TJ nº 27/2022, art. 4º:* Desdobramento dos macrodesafios do Poder Judiciário no PDTIC.
- **MPRJ / CNMP:**
  * *Resolução CNMP nº 171/2017, arts. 11 e 12 c/c Resolução CNMP nº 204/2019 e Resolução GPGJ nº 2.785/2026, arts. 5º (III), 11 e 12:* Alinhamento do PDTI à Estratégia Nacional e ao Plano Estratégico do MPRJ.

#### S3.5 — Plano de TIC não utilizado na proposta orçamentária e no PCA
- **Poder Executivo Estadual:**
  * *Portaria PRODERJ/PRE nº 825/2021, art. 1º (V a VIII) e arts. 4º e 5º; IN PRODERJ/PRE nº 05/2024, art. 5º; Decreto Estadual nº 48.749/2023:* Proibição de contratações fora do PEDTIC e exigência de integração com o PCA e proposta orçamentária.
- **TJRJ / CNJ:**
  * *Resolução CNJ nº 370/2021, art. 6º; Resolução CNJ nº 468/2022, arts. 4º e 5º; Ato Normativo TJ nº 27/2022, arts. 5º e 6º:* Contratações e orçamento de TIC derivados compulsoriamente do PDTIC e registrados no PAC.
- **MPRJ / CNMP:**
  * *Resolução CNMP nº 283/2024, arts. 4º a 6º e Resolução GPGJ nº 2.540/2023, art. 2º (II):* Integração direta entre iniciativas do PDTI, Plano Anual de Contratações (PAC) e orçamento.

#### S3.6 — Ausência de acompanhamento da execução do plano de TIC
- **Poder Executivo Estadual:**
  * *Portaria PRODERJ/PRE nº 825/2021, Anexo C, arts. 3º, 7º, 11 e 13:* Rotinas obrigatórias de revisão anual, acompanhamento físico e registro de versões do PEDTIC em processo administrativo.
- **TJRJ / CNJ:**
  * *Resolução CNJ nº 370/2021, arts. 8º (V), 46 e 48 e Ato Normativo TJ nº 32/2023, art. 11, § 2º:* Monitoramento e prestação de contas periódica das metas do PDTIC ao CGTIC.
- **MPRJ / CNMP:**
  * *Resolução CNMP nº 171/2017, arts. 12, 14 e 16 e Resolução GPGJ nº 2.785/2026, arts. 5º e 13 (I):* Avaliação sistemática e relatórios de execução do PDTI.

---

### Questão 04 — Capacidade Institucional de TIC e Segurança da Informação

#### S4.1 — Ausência de força de trabalho dedicada à TIC
- **Poder Executivo Estadual:**
  * *Decreto Estadual nº 48.997/2024, art. 4º; IN PRODERJ nº 07/2025, art. 11, VI:* Previsão de estrutura setorial para sustentação das atribuições de TIC e de responsáveis pela gestão de segurança.
- **TJRJ / CNJ:**
  * *Resolução CNJ nº 370/2021, art. 24, caput:* Exige quadro permanente com servidores ocupantes de cargos efetivos com dedicação exclusiva à área de TIC.
- **MPRJ / CNMP:**
  * *Resolução CNMP nº 171/2017, arts. 16 e 33 e Resoluções GPGJ nº 2.675/2025 e 2.785/2026:* Estrutura funcional permanente para a área de TI.

#### S4.2 — Quantitativo necessário de pessoal não definido documentadamente
- **Poder Executivo Estadual:**
  * *Critério de Boas Práticas / Geral:* COBIT 2019 APO07.01 e APO07.05; Acórdão TCE-RJ nº 44.490/2024-PLEN, item II.7. (Ausência de regulamento estadual impositivo; formular como recomendação).
- **TJRJ / CNJ:**
  * *Resolução CNJ nº 370/2021, art. 24, §§ 1º a 3º:* Determina dimensionamento formal fundamentado em estudos técnicos e no "Guia de Dimensionamento da Força de Trabalho em TIC do Poder Judiciário".
- **MPRJ / CNMP:**
  * *Resolução CNMP nº 171/2017, art. 8º, § 1º, "d" e Resolução CNMP nº 283/2024, art. 10, III, "b":* Critérios nacionais de dimensionamento e avaliação de recursos humanos.

#### S4.3 — Ausência de cargos ou funções formalmente atribuídos à TIC ou Segurança
- **Poder Executivo Estadual:**
  * *IN PRODERJ/PRE nº 07/2025, arts. 11, 17 e 18:* Exige a designação formal do Gestor de Segurança da Informação e do responsável pela equipe de incidentes (ETIR). *Decreto nº 48.997/2024, art. 4º:* Estrutura o nível setorial do SETIC.
- **TJRJ / CNJ:**
  * *Resolução CNJ nº 370/2021, arts. 23 e 24 e Resolução CNJ nº 396/2021, art. 7º:* Formalização de papéis de liderança técnica, segurança e equipes de resposta a incidentes cibernéticos (ETIR/CSIRT).
- **MPRJ / CNMP:**
  * *Resolução CNMP nº 171/2017, arts. 16 e 33 e Resoluções GPGJ nº 2.675/2025 e nº 2.757/2025:* Formalização de cargos e funções de gestão de TIC e segurança.

#### S4.6 — Operação de TIC predominantemente terceirizada sem capacidade interna
- **Poder Executivo Estadual:**
  * *Decreto Estadual nº 48.997/2024, art. 4º, e IN PRODERJ nº 07/2025:* Retenção de competências de coordenação, gestão e fiscalização no órgão estatal. (*Reforço: Acórdão TCE-RJ nº 44.490/2024-PLEN*).
- **TJRJ / CNJ:**
  * *Resolução CNJ nº 370/2021, art. 24, caput e Resolução CNJ nº 468/2022, art. 8º, § 1º:* Veda expressamente a terceirização integral e a contratação de terceiros para a gestão/supervisão das soluções.
- **MPRJ / CNMP:**
  * *Resolução CNMP nº 171/2017, arts. 16 e 33 e Resolução CNMP nº 283/2024, art. 9º, § 2º e art. 33:* Gestão, planejamento e fiscalização técnica exercidas exclusivamente por servidores do quadro próprio.

---

### Questão 05 — Gestão de Serviços de TIC

#### S5.1 — Inexistência ou insuficiência do catálogo de serviços de TIC
- **Poder Executivo Estadual:**
  * *Critério Geral / Frameworks:* ABNT NBR ISO/IEC 20000-2:2021, item 8.2.4; COBIT 2019 APO09.02; ITIL 4; Acórdão TCE-RJ nº 44.490/2024-PLEN, item II.7.4.
- **TJRJ / CNJ:**
  * *Resolução CNJ nº 370/2021, art. 21, IV, "d" e Ato Normativo TJ nº 28/2022, arts. 4º e 5º:* Determina a estruturação, atualização e publicação do Catálogo de Serviços de TIC no TJRJ.
- **MPRJ / CNMP:**
  * *Resolução CNMP nº 171/2017, arts. 14 (V) e 23 e Resolução GPGJ nº 2.785/2026, art. 13 (IV):* Implantação e manutenção obrigatória do Catálogo de Serviços de TI no MPRJ.

#### S5.2 — Ausência ou fragilidade na definição e no monitoramento de ANS/SLA
- **Poder Executivo Estadual:**
  * *IN PRODERJ/PRE nº 07/2025, Anexo, item 8.9.2.1:* Exige ANS/SLA em contratações de serviços de TIC. (*Critério Geral: ITIL 4 e Acórdão TCE-RJ nº 44.490/2024-PLEN, item II.7.7*).
- **TJRJ / CNJ:**
  * *Resolução CNJ nº 370/2021, arts. 18 a 20 e Ato Normativo TJ nº 28/2022 (e Anexo):* Fixa parâmetros de níveis de serviço, metas e tempos operacionais de atendimento.
- **MPRJ / CNMP:**
  * *Resolução CNMP nº 171/2017, arts. 14 (VI) e 23 e Resolução GPGJ nº 2.785/2026, arts. 5º (IX) e 13 (IV):* Pactuação formal e monitoramento de Acordos de Nível de Serviço.

#### S5.3 — Inventário de ativos de TIC inexistente ou insuficiente
- **Poder Executivo Estadual:**
  * *Decreto Estadual nº 48.997/2024, art. 4º, inciso V; IN PRODERJ/PRE nº 07/2025, Anexo, itens 7.1 e 8.1:* Obrigação de informar o inventário permanente de equipamentos, licenças de software e ativos computacionais.
- **TJRJ / CNJ:**
  * *Resolução CNJ nº 370/2021, art. 21, IV, "c", art. 23 e art. 34, § 2º e Resolução CNJ nº 396/2021, art. 6º:* Inventário de ativos de tecnologia e segurança cibernética.
- **MPRJ / CNMP:**
  * *Resolução CNMP nº 171/2017, art. 26, II e Resoluções GPGJ nº 2.785/2026, art. 13 (VI/VII) e 2.757/2025:* Inventário e controle permanente de ativos de hardware e software.

#### S5.4 — Ausência ou fragilidade na gestão de configuração
- **Poder Executivo Estadual:**
  * *IN PRODERJ/PRE nº 07/2025, Anexo, itens 7.2.1.5, 8.1.1 e 8.10:* Baseline de configuração segura, controle de versões e gerenciamento de mudanças. (*Critério Geral: ISO 20000-2 item 8.2.6; COBIT BAI10.01*).
- **TJRJ / CNJ:**
  * *Resolução CNJ nº 370/2021, arts. 19 e 21, IV, "c":* Controle de configuração e mudanças. (*Critério Geral: ISO 20000-2; COBIT BAI10.01*).
- **MPRJ / CNMP:**
  * *Resolução CNMP nº 171/2017, arts. 18, 19 e 26, II e Resolução GPGJ nº 2.785/2026, art. 13, VI, "b":* Execução do macroprocesso de gestão de configuração e relacionamentos entre itens de configuração.

#### S5.5 — Inexistência ou fragilidade na gestão de incidentes de TIC
- **Poder Executivo Estadual:**
  * *IN PRODERJ/PRE nº 07/2025, arts. 11 a 13, 17 e 18 e Anexo, item 8.14:* Processo estruturado para registro, classificação, tratamento e resposta a incidentes de segurança. (*Critério Geral de Serviços: ISO 20000-2 item 8.6.1; ITIL 4*).
- **TJRJ / CNJ:**
  * *Resolução CNJ nº 370/2021, art. 21, II, "a" e IV, "f"; Resolução CNJ nº 396/2021, arts. 7º e 8º; Ato Normativo TJ nº 28/2022, art. 4º:* Fluxo de registro, atendimento e resposta a incidentes operacionais e cibernéticos.
- **MPRJ / CNMP:**
  * *Resolução CNMP nº 171/2017, arts. 23, 27 e 28; Resolução CNMP nº 294/2024; Resoluções GPGJ nº 2.785/2026, art. 13 (IV/VII) e 2.757/2025:* Fluxos estruturados de gestão de incidentes de serviços e segurança.

---

### Questão 06 — Contratações de TIC

#### S6.1 — Processo de contratações de TIC sem fluxo padronizado
- **Poder Executivo Estadual:**
  * *IN PRODERJ/PRE nº 05/2024, arts. 1º, 4º a 7º, 11 e seguintes:* Rito obrigatório de planejamento com DOD/DFD, ETP, Mapa de Gerenciamento de Riscos e Termo de Referência padronizados.
  * *Decreto Estadual nº 48.816/2023, arts. 6º a 20 c/c Lei Federal nº 14.133/2021, art. 11, p. único:* Governança das contratações públicas e padronização.
- **TJRJ / CNJ:**
  * *Resolução CNJ nº 468/2022, arts. 6º, 7º, 10, 11, 15 e 29:* Processo padronizado de planejamento da contratação de TIC no Poder Judiciário.
  * *Ato Normativo TJ nº 27/2022, arts. 5º e 6º c/c Lei nº 14.133/2021:* Rito de contratação de soluções de TIC no PJERJ.
- **MPRJ / CNMP:**
  * *Resolução CNMP nº 283/2024, arts. 2º, 6º, 8º a 10, 16, 17 e 20:* Procedimento padronizado com DOD, ETP, Riscos e TR.
  * *Resolução GPGJ nº 2.785/2026, art. 13, III c/c Lei nº 14.133/2021:* Macroprocesso de contratações de TIC no MPRJ.

#### S6.2 — Contratações de TIC sem análise prévia e aprovação técnica da área de TIC
- **Poder Executivo Estadual:**
  * *Decreto Estadual nº 48.997/2024, art. 5º:* Exige o envio e a anuência prévia do PRODERJ para a deflagração da fase externa ou a assinatura do instrumento, conforme o caso.
  * *IN PRODERJ/PRE nº 05/2024, arts. 4º, 7º, 8º e 28:* Obrigatoriedade de parecer técnico, aprovação pela área de TIC setorial (NSTIC) e encaminhamento para análise e anuência prévia do PRODERJ.
- **TJRJ / CNJ:**
  * *Resolução CNJ nº 468/2022, arts. 7º, 8º, 10, 14 e 15:* Análise técnica e subscrição obrigatória do Integrante Técnico da área de TIC nos artefatos (ETP, Riscos e TR).
- **MPRJ / CNMP:**
  * *Resolução CNMP nº 283/2024, arts. 9º, 16, 20 e 33:* Elaboração, validação e assinatura obrigatória do Integrante Técnico da área de TI em todos os artefatos de planejamento.

#### S6.3 — Contratações de TIC sem alinhamento ao Plano de TIC e ao PCA
- **Poder Executivo Estadual:**
  * *IN PRODERJ/PRE nº 05/2024, art. 5º:* Vedação expressa a contratações não contempladas no PEDTIC e no Plano de Contratações Anual (PCA).
  * *Decreto Estadual nº 48.749/2023 c/c Lei nº 14.133/2021, art. 12, VII e art. 18, § 1º, II:* Compatibilização com o PCA estadual.
- **TJRJ / CNJ:**
  * *Resolução CNJ nº 468/2022, arts. 4º e 5º e Resolução CNJ nº 370/2021, art. 6º:* Contratações compulsoriamente derivadas do PDTIC e inclusas no PAC.
  * *Ato Normativo TJ nº 27/2022, art. 5º c/c Lei nº 14.133/2021:* Alinhamento formal ao PDTIC e PAC do TJRJ.
- **MPRJ / CNMP:**
  * *Resolução CNMP nº 283/2024, arts. 4º a 6º e Resolução GPGJ nº 2.540/2023, art. 2º, II:* Previsão obrigatória no PDTI e no PAC do MPRJ.

#### S6.4 — Ausência de equipe de planejamento com integrante técnico da área de TIC
- **Poder Executivo Estadual:**
  * *Decreto Estadual nº 48.816/2023, arts. 6º a 8º c/c Lei nº 14.133/2021, art. 7º:* Designação formal dos agentes públicos responsáveis pela instrução da contratação.
  * *IN PRODERJ/PRE nº 05/2024, arts. 6º e 7º:* Atuação formal da área requisitante em conjunto com o setor de TIC (NSTIC).
- **TJRJ / CNJ:**
  * *Resolução CNJ nº 468/2022, art. 7º, caput e incisos I a III, e art. 8º:* Obrigatoriedade de designação formal da **Equipe de Planejamento da Contratação** composta necessariamente por: **I - Integrante Requisitante; II - Integrante Técnico (obrigatoriamente lotado na área de TIC); e III - Integrante Administrativo**.
- **MPRJ / CNMP:**
  * *Resolução CNMP nº 283/2024, art. 8º, caput e incisos I a III, e art. 9º:* Designação formal obrigatória de **Equipe de Planejamento da Contratação** com: **I - Integrante Requisitante; II - Integrante Técnico (servidor da área de TI); e III - Integrante Administrativo**.

---

## 4. Orientações Práticas para Relatórios e Matriz de Achados

1. **Adequação Subjetiva do Critério no Relatório Individual:**
   - Para auditados do **Poder Executivo Estadual**, cite expressamente o Decreto Estadual nº 48.997/2024 (ou 48.816/2023 para contratações) e as Instruções Normativas / Portarias do PRODERJ (Portaria nº 825/2021 para PEDTIC/Comitê; IN nº 05/2024 para Contratações; IN nº 07/2025 para Segurança/Ativos).
   - Para o **TJRJ**, cite expressamente as Resoluções CNJ nº 370/2021, 468/2022 e 396/2021, conjugadas com os Atos Normativos TJ nº 32/2023, 27/2022 e 28/2022.
   - Para o **MPRJ**, cite expressamente as Resoluções CNMP nº 171/2017, 283/2024 e 294/2024, conjugadas com as Resoluções GPGJ nº 2.785/2026, 2.540/2023 e 2.675/2025.

2. **Critérios de Encaminhamento (Deliberação TCE-RJ nº 346/2024):**
   - **Determinação:** Utilize para situações com aderência direta (**D**) em normas vinculantes aplicáveis ao ente (ex.: ausência de aprovação formal do PEDTIC no Executivo; ausência de designação de equipe de planejamento com integrante técnico no TJRJ/MPRJ; ausência de inventário de ativos).
   - **Recomendação:** Utilize quando o critério for apoiado em boas práticas internacionais, referencial de maturidade ou quando houver lacuna de norma local específica (**P** ou **L**) (ex.: dimensionamento documentado no Executivo, catálogo geral de serviços no Executivo ou modelo avançado de CMDB).
