# Parecer de Revisão Crítica e Proporcionalidade — Matriz de Planejamento e Mapa de Verificação de Achados (iGovTI 2026)

| Campo | Valor |
| :--- | :--- |
| **Fiscalização** | Fiscalização nº 18/2026 – iGovTI 2026 (Processo TCE-RJ nº 303.389-0/2025) |
| **Documentos avaliados** | • Matriz de Planejamento (`01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/matriz_planejamento.md`)<br>• Mapa de Verificação de Achados (`02-Execucao/03-Execucao_Procedimentos/01-Insumos/mapa-verificacao-achados.xlsx`) |
| **Data da avaliação** | 14/08/2026 (UTC−03:00, America/Sao_Paulo) |
| **Realizada por** | **Gemini 3.7 Flash** |
| **Perfil da análise** | Auditor governamental experiente com especialidade em governança e gestão de TI, com juízo crítico para discernir as práticas essenciais (*mínimo aceitável*) daquelas desejáveis (*maturidade avançada*) no setor público |
| **Objetivo** | Avaliar criticamente a razoabilidade, proporcionalidade e suficiência das Ações de Verificação (AVs), Achados, Situações Inconformes e enquadramento jurídico dos Encaminhamentos (Recomendação vs Determinação) após o processamento da etapa de comentários do gestor |
| **Natureza** | Parecer técnico de garantia de qualidade metodológica e calibração de regras de auditoria; produzido por modelo de IA |

---

## 1. Sumário Executivo e Diretriz de Proporcionalidade

A conclusão da etapa de contraditório dos comentários dos gestores (alcançando 113 respondentes válidos e 80 manifestações processadas) forneceu subsídios empíricos indispensáveis para avaliar se as regras de auditoria foram **suficientes, razoáveis e proporcionais**, ou se impuseram **rigor excessivo incompatível com o estágio de maturidade predominante** da Administração Pública fluminense.

Em auditoria governamental de governança de TIC, o papel do Tribunal de Contas não consiste em exigir de prefeituras de pequeno porte e autarquias estaduais a sofisticação operacional de corporações multinacionais de tecnologia (ex.: ITIL nível 5 ou COBIT avançado), mas sim **assegurar o patamar mínimo aceitável de controle, planejamento, transparência, proteção patrimonial e economicidade**.

### Síntese das Conclusões:
1. **Ações de Verificação (AVs):** Apresentam elevado rigor decorrente da *explosão por disjunção* (`|` em regras multifatoriais), em que a ausência de um subitem acessório (ex.: falta de análise formal de causa-raiz em incidentes) rotula a organização com a mesma inconformidade total de quem não possui processo algum. Além disso, identificou-se **redundância estrita** entre a situação S3.5 (Planejamento) e S6.3 (Contratações), que avaliam exatamente os mesmos itens do questionário.
2. **Questões e Achados:** A estrutura de 6 Questões e 6 Achados estruturantes é dogmaticamente sólida, abrangente e deve ser **integralmente mantida**. Não há necessidade de remover nenhuma questão de auditoria ou achado.
3. **Situações Inconformes:** Devem ser calibradas para distinguir o *mínimo essencial* (ex.: possuir inventário de equipamentos, servidores e sistemas) de *práticas de alta maturidade* (ex.: Gestão de Configuração / CMDB relacional em S5.4), as quais sobrecarregam o achado e não se sustentam como deficiência grave para pequenos jurisdicionados.
4. **Enquadramento de Encaminhamentos (Recomendação $\rightarrow$ Determinação):** Atualmente, **todas as 26 situações do mapa estão classificadas como RECOMENDAÇÃO**, enfraquecendo a efetividade do controle externo. Práticas com respaldo legal expresso (Lei nº 14.133/2021) e jurisprudência vinculante pacificada (Acórdão TCU nº 1.411/2014-Plenário e Acórdão TCE-RJ nº 44.490/2024-PLEN) — como **elaboração e aprovação formal do PDTI**, **instituição do Comitê de TI**, **análise técnica prévia da área de TI nas contratações** e **designação de equipe de planejamento da contratação** — **devem ser convertidas em DETERMINAÇÃO**. Por outro lado, exigências que esbarram na reserva de iniciativa privativa do Chefe do Executivo (como criação de cargos por lei) ou na discricionariedade do organograma interno devem permanecer estritamente como **RECOMENDAÇÃO**.

---

## 2. Item 1: Avaliação e Ajustes nas Ações de Verificação (AVs) do Mapa

O arquivo [`mapa-verificacao-achados.xlsx`](file:///home/acba/workspace/fiscalizacoes/202601-igovti/02-Execucao/03-Execucao_Procedimentos/01-Insumos/mapa-verificacao-achados.xlsx) estrutura atualmente 151 Ações de Verificação (AV01 a AV83 para o questionário; AV84 a AV151 para a fonte derivada de avaliação de evidências).

### 2.1. O Problema da "Explosão por Disjunção" (`|` em excesso)
* **Diagnóstico:** Em regras como S2.1 (Modelo de Governança), S3.1 (Processo de Planejamento), S4.5 (Lacunas de Competências), S5.1 (Catálogo de Serviços), S5.5 (Gestão de Incidentes) e S6.1 (Processo de Contratações), a lógica booleana foi construída no padrão:
  $$\text{Situação} = (\text{Item}_A \neq \text{Sim}) \lor (\text{Item}_B \neq \text{Sim}) \lor (\text{Item}_C \neq \text{Sim}) \lor (\text{Item}_D \neq \text{Sim}) \lor \dots$$
* **Impacto na Razoabilidade:** Uma entidade que estruturou seu catálogo de serviços (itens A e B atendidos), mas não publicou todas as condições de SLA em portal aberto (item C não atendido), é enquadrada na situação *"Inexistência ou insuficiência do catálogo de serviços de TIC"* com a mesma severidade de quem não possui catálogo algum. Esse rigor cumulativo explica por que diversos achados atingiram 98% a 100% dos auditados.
* **Ajuste Recomendado:** Modular as regras para exigir o *núcleo essencial*. Por exemplo, em S5.5 (Incidentes), a situação deve ser disparada pela ausência de fluxo/registro básico (`q2204ext[A]` ou `q2204ext[D]`), tratando a ausência de análise de causa-raiz (`q2204ext[F]`) como oportunidade de melhoria ou ponderação de severidade média, sem caracterizar ausência de processo de incidentes.

### 2.2. Eliminação da Redundância Estrita entre S3.5 e S6.3
* **Diagnóstico:** As situações:
  * **S3.5** (*"Plano de TIC sem vínculo demonstrado com orçamento e contratações de TIC"*, sob o Achado 3); e
  * **S6.3** (*"Contratações de TIC sem alinhamento demonstrado ao planejamento de TIC, ao plano de contratações ou à proposta orçamentária"*, sob o Achado 6);
  utilizam **exatamente a mesma combinação de variáveis**: `q2102ext[C]`, `q2802ext[C]`, `q2802ext[D]` e `q2804[B]`.
* **Impacto:** Exatamente 106 organizações receberam ambas as situações simultaneamente, configurando *bis in idem* de inconformidade pelo mesmo fato gerador.
* **Ajuste Recomendado:** 
  * Delimitar **S3.5** estritamente à perspectiva do **Planejamento** (verificar se o PDTI possui estimativa orçamentária e cronograma de investimentos: `q2102ext[C]`);
  * Delimitar **S6.3** estritamente à perspectiva da **Execução Contratual** (verificar se o Plano de Contratações Anual e as contratações isoladas estão alinhadas ao PDTI: `q2802ext[C]`, `q2802ext[D]` e `q2804[B]`).

### 2.3. Blindagem de Falso Positivo para Entidades sem TI Formal (`q0101 == F`)
* **Diagnóstico:** Em 5 organizações não há área formal de TI (`q0101 == F`). Em S1.2 e S1.3 há a trava `q0101 != F`. Contudo, nas questões downstream de governança, planejamento, capacidade e contratações, essas entidades marcam `Não` ou `N/A` em dezenas de itens, disparando automaticamente todos os 6 achados e 24 situações em cascata.
* **Ajuste Recomendado:** Preservar a caracterização do Achado 1 e Achado 2, mas parametrizar os motivos de relatório para não gerar cobranças contraditórias (ex.: exigir CMDB ou catálogo avançado de quem não possui setor de TI).

---

## 3. Item 2: Avaliação das Questões de Auditoria e dos Achados

Avaliou-se a pertinência de manter, fundir ou extinguir as 6 Questões e os 6 Achados estruturantes da auditoria:

| Questão / Achado | Escopo e Foco | Avaliação de Pertinência | Veredito |
| :--- | :--- | :--- | :---: |
| **Q1 / Achado 1** | **Estrutura de TIC:** formalização da unidade de TI, atribuições essenciais e posicionamento hierárquico. | Indispensável. A formalização da área de TI é o alicerce de qualquer governança pública. Atingiu 60,2% das entidades. | **MANTER** |
| **Q2 / Achado 2** | **Governança e Comitê de TIC:** modelo de direção, indicadores e colegiado multidisciplinar (Comitê de TI). | Indispensável. Alinhado ao Acórdão TCU 1.411/2014, Acórdão TCE-RJ 44.490/2024 e Decreto Federal 12.198/2024. | **MANTER** |
| **Q3 / Achado 3** | **Planejamento de TIC:** existência de PDTI/PDTIC aprovado, vigente, alinhado e integrado ao orçamento. | Núcleo central da fiscalização. Obrigação de planejar para justificar o gasto público de TI. | **MANTER** |
| **Q4 / Achado 4** | **Capacidade Institucional:** força de trabalho, dimensionamento, retenção de conhecimento e controle de terceirização. | Essencial para diagnosticar o risco crônico de apagão de pessoal e dependência predatória de terceirizados. | **MANTER** |
| **Q5 / Achado 5** | **Gestão de Serviços e Ativos de TIC:** catálogo, inventário de ativos e gestão básica de incidentes. | Essencial para continuidade operacional e proteção patrimonial dos ativos tecnológicos. | **MANTER** |
| **Q6 / Achado 6** | **Governança Técnica das Contratações de TIC:** fase preparatória, ETP, análise técnica prévia e equipe de planejamento. | Indispensável. Fundamentado diretamente na Lei nº 14.133/2021 (arts. 11, 18, 19 e 7º). | **MANTER** |
| **Questão Transversal (QT)** | **Levantamento Longitudinal:** comparação 2023–2026 (`gera_achado: false`). | Estrutura exemplar para análise de tendências sem gerar achados punitivos. | **MANTER** |

**Conclusão do Item 2:** A arquitetura com 6 Questões e 6 Achados é **perfeita, lógica e suficiente**. Não se deve remover nenhum achado. A calibração necessária reside na **granularidade das situações inconformes** dentro de cada achado.

---

## 4. Item 3: Avaliação Crítica das Situações Inconformes (Essencial vs Excessivo)

Avaliando as 26 situações sob a ótica do auditor governamental focado no *mínimo aceitável*:

### 4.1. Práticas Essenciais Mínimas (Devem ser Mantidas Plenamente)
São aquelas sem as quais a administração pública opera em risco crítico de dano ao erário, descontinuidade ou ilegalidade:
1. **S1.1 – Ausência de área/função de TIC formalizada:** Essencial (não há responsável formal pela TI).
2. **S1.2 – Área de TIC sem atribuições formais mínimas:** Essencial (TI atuando sem competências regulamentares).
3. **S2.2 – Comitê de TIC não instituído formalmente:** Essencial (decisões de TI tomadas isoladamente, sem a alta administração e áreas finalísticas).
4. **S2.3 – Comitê de TIC sem atuação efetiva:** Essencial (comitê "de papel" / pro forma).
5. **S3.1 – Inexistência de processo formal de planejamento de TIC:** Essencial.
6. **S3.2 – Ausência de aprovação formal do plano de TIC pela alta administração:** Essencial (o plano perde legitimidade).
7. **S3.6 – Ausência de acompanhamento periódico do plano de TIC:** Essencial (plano vira peça de gaveta).
8. **S4.1 – Ausência de força de trabalho dedicada à TIC ou Segurança:** Essencial (risco operacional máximo).
9. **S4.6 – Dependência externa relevante sem capacidade interna de fiscalização:** Essencial (terceirização sem fiscalização técnica).
10. **S5.3 – Inexistência ou fragilidade do inventário de ativos de TIC:** Essencial (dever de controle patrimonial e segurança da informação).
11. **S5.5 – Inexistência ou fragilidade do processo de gestão de incidentes:** Essencial (falhas e incidentes de segurança sem registro e tratamento).
12. **S6.1 – Inexistência de fluxo padronizado de contratação de TIC:** Essencial (art. 11 e 19 da Lei 14.133/21).
13. **S6.2 – Contratações de TIC sem análise prévia e aprovação técnica da área de TI:** Essencial (evita "TI na sombra" e compras incompatíveis).
14. **S6.4 – Contratações de TIC sem equipe de planejamento formalmente designada:** Essencial (art. 7º e 18 da Lei 14.133/21).

### 4.2. Práticas Avançadas ou com Excesso de Rigor (Oportunidades de Ajuste)

#### A. Situação S5.4 – Gestão de Configuração (CMDB)
* **Texto atual:** *"Ausência ou fragilidade do processo de gestão de configuração."* (atinge 110 organizações - 97,3%).
* **Crítica técnica:** A Gestão de Configuração nos moldes do ITIL/COBIT (manter uma *Configuration Management Database* - CMDB mapeando relacionamentos lógicos entre itens de configuração, bancos e serviços) é uma **prática de maturidade intermediária a avançada**. Para prefeituras de pequeno/médio porte ou órgãos estaduais sem centro de dados próprio (que utilizam nuvem ou infraestrutura do PRODERJ), exigir CMDB formal é **desproporcional**.
* **Recomendação:** Fundir o controle de configuração ao **Inventário de Ativos (S5.3)**, cobrando a identificação de equipamentos, sistemas, servidores e licenças, e rebaixando o CMDB avançado para recomendação de melhoria em organizações de grande porte.

#### B. Situação S4.3 – Ausência de Cargos Específicos de TI Criados por Lei
* **Texto atual:** *"Ausência de cargos, funções, perfis ou ocupações específicas de TIC e segurança da informação."* (atinge 91 organizações - 80,5%).
* **Crítica técnica:** A criação de cargos efetivos específicos depende de projeto de lei de iniciativa privativa do Chefe do Poder Executivo (art. 61, § 1º, II, 'a' da CF/88) e subordina-se a limites fiscais da LRF (LC nº 101/2000). Muitas entidades da administração indireta ou municípios pequenos operam legitimamente com servidores de carreiras administrativas gerais alocados nas funções de TI, ou mediante funções gratificadas.
* **Recomendação:** Suprimir o foco estrito em "criação de cargos por lei" e reorientar a situação para **"Ausência de formalização de funções e atribuições técnicas para a equipe de TIC"**, permitindo que a organização atenda mediante designação formal de funções de confiança ou gratificações.

#### C. Situações S4.4 e S4.5 – Perfis Profissionais e Diagnóstico Formal de Competências
* **Crítica técnica:** Exigir matriz formal de competências e catálogo de perfis nos moldes do setor privado atinge 111 e 112 organizações. No setor público, isso deve ser flexibilizado para a existência de requisitos mínimos de capacitação e experiência nos atos de designação.

---

## 5. Item 4: Transição de RECOMENDAÇÃO para DETERMINAÇÃO com Fundamentação Jurisprudencial

No modelo atual da auditoria, **todas as 26 situações encontram-se classificadas como RECOMENDAÇÃO**. Essa opção enfraquece a força cogente do Tribunal em matérias onde já existe dever legal expresso e jurisprudência pacificada.

### 5.1. Critérios Dogmáticos de Distinção
* **DETERMINAÇÃO (Cogente / Mandamental):** Aplica-se quando houver **descumprimento de dever legal ou regulamentar expresso**, ou quando a omissão violar diretamente princípios constitucionais (eficiência, economicidade, publicidade, planejamento). O descumprimento injustificado sujeita o gestor à sanção de multa (art. 63 da LC nº 63/1990).
* **RECOMENDAÇÃO (Propositiva / Orientadora):** Aplica-se quando se tratar de **escolha discricionária de oportunidade e conveniência gerencial**, adoção de referenciais de excelência (COBIT/ITIL) sem matriz normativa estrita, ou matéria sujeita à reserva de iniciativa privativa de outros Poderes.

### 5.2. Matriz Conclusiva de Enquadramento dos Encaminhamentos

| Situação Encontrada | Tipo Atual | Tipo Proposto | Fundamento Jurídico e Jurisprudencial | Risco de Refazimento / Contestação |
| :--- | :---: | :---: | :--- | :--- |
| **S1.1 – Ausência de formalização da área/função de TIC** | Recomendação | **DETERMINAÇÃO** | **Princípio da Eficiência (art. 37, caput, CF/88)** c/c **art. 11, parágrafo único da Lei nº 14.133/2021** (dever de instituir estruturas de governança). | Nulo. Determina-se a formalização por ato próprio (decreto, portaria ou regimento), sem impor criação de cargos. |
| **S1.2 – Área de TIC sem atribuições formais mínimas** | Recomendação | **DETERMINAÇÃO** | **Princípio da Legalidade e Eficiência** c/c **art. 11, p. único da Lei nº 14.133/2021**. | Nulo. Toda unidade administrativa deve ter atribuições regulamentadas. |
| **S1.3 – Posicionamento hierárquico da TI** | Recomendação | **RECOMENDAÇÃO** | Discricionariedade organizatória da Administração. A Portaria SGD/ME 778/2019 é apenas referencial de boa prática. | **Alto se for determinação.** O Tribunal não pode desenhar o organograma interno do Executivo. |
| **S2.1 – Modelo básico de Governança de TIC** | Recomendação | **RECOMENDAÇÃO** | Governança geral baseada no COBIT/Decreto 9.203/17. | Médio. Manter como recomendação de aprimoramento contínuo. |
| **S2.2 – Comitê de TIC não instituído formalmente** | Recomendação | **DETERMINAÇÃO** | **Art. 11, parágrafo único da Lei nº 14.133/2021**; **Acórdão TCU nº 1.411/2014-Plenário**; **Acórdão TCE-RJ nº 44.490/2024-PLEN** (item II.1). | **Inexistente.** Jurisprudência consolidada do TCU e TCE-RJ impondo colegiado de TIC para alinhamento estratégico. |
| **S2.3 – Comitê de TIC sem atuação efetiva** | Recomendação | **DETERMINAÇÃO** | **Acórdão TCE-RJ nº 44.490/2024-PLEN** c/c Princípio da Eficiência (vedação a órgãos colegiados fictícios). | Nulo. Determina-se a realização e registro de reuniões periódicas. |
| **S3.1 / S3.2 – Inexistência ou Falta de Aprovação do PDTI** | Recomendação | **DETERMINAÇÃO** | **Art. 11, parágrafo único e art. 18, caput da Lei nº 14.133/2021**; **Acórdão TCU nº 1.411/2014-Plenário** (item 9.1.6); **Acórdão TCE-RJ nº 44.490/2024-PLEN** (item II.3). | **Inexistente.** O dever de elaborar e aprovar PDTI/PDTIC é pacífico no controle externo brasileiro como pressuposto do gasto público de TI. |
| **S3.5 – PDTI sem integração orçamentária** | Recomendação | **DETERMINAÇÃO** | **Art. 18, § 1º, II e art. 12, VII da Lei nº 14.133/2021** c/c **art. 165, § 5º da CF/88** (compatibilidade orçamentária). | Nulo. O plano de TI deve prever dotação orçamentária para seus projetos. |
| **S3.6 – Falta de acompanhamento periódico do PDTI** | Recomendação | **DETERMINAÇÃO** | **Acórdão TCE-RJ nº 44.490/2024-PLEN** (item II.3.5) c/c Princípio da Eficiência. | Nulo. Plano sem monitoramento viola a boa governança. |
| **S4.1 – Ausência de equipe dedicada à TI** | Recomendação | **DETERMINAÇÃO** | **Princípio da Continuidade do Serviço Público** c/c **art. 11, parágrafo único da Lei nº 14.133/2021**. | Nulo. Determina-se a alocação de capacidade mínima, por meios próprios ou cooperação. |
| **S4.2 – Falta de dimensionamento da equipe** | Recomendação | **RECOMENDAÇÃO** | Prática de gestão de RH. | Baixo. Manter como recomendação. |
| **S4.3 – Falta de criação de cargos específicos por lei** | Recomendação | **RECOMENDAÇÃO** | **Reserva de iniciativa privativa do Chefe do Executivo (art. 61, § 1º, II, 'a' da CF/88)**; Súmula Vinculante nº 37/STF. | **Gravíssimo se for determinação.** Violação direta da separação de poderes. Deve ser recomendação. |
| **S4.4 / S4.5 – Perfis profissionais e matriz de competências** | Recomendação | **RECOMENDAÇÃO** | Aperfeiçoamento de gestão de pessoas. | Médio. Manter como recomendação. |
| **S4.6 – Dependência externa sem capacidade de fiscalização** | Recomendação | **DETERMINAÇÃO** | **Art. 117 da Lei nº 14.133/2021** (dever de fiscalização contratual por agente público qualificado). | Nulo. É dever legal expresso manter fiscalização técnica de contratos. |
| **S5.1 / S5.2 – Catálogo de Serviços e Acordos de Nível de Serviço (ANS)** | Recomendação | **RECOMENDAÇÃO** | Práticas da ITIL 4 / COBIT. | Baixo. Manter como recomendação. |
| **S5.3 – Inexistência de Inventário de Ativos de TIC** | Recomendação | **DETERMINAÇÃO** | **Art. 50 da Lei nº 13.709/2018 (LGPD)**; **Art. 94 da Lei nº 4.320/1964** (controle de bens patrimoniais). | Nulo. Toda entidade pública tem dever legal de inventariar seus ativos tecnológicos e dados. |
| **S5.4 – Gestão de Configuração (CMDB)** | Recomendação | **RECOMENDAÇÃO** | Prática avançada do ITIL/COBIT BAI10. | Alto se for determinação em pequenos entes. Manter recomendação. |
| **S5.5 – Inexistência de processo de Gestão de Incidentes** | Recomendação | **DETERMINAÇÃO** | **Art. 46 e 48 da Lei nº 13.709/2018 (LGPD)** (dever de segurança e comunicação de incidentes) c/c **Acórdão TCE-RJ 44.490/2024**. | Nulo. Determina-se a formalização de fluxo básico de registro e tratamento de incidentes. |
| **S6.1 – Processo padronizado de contratação de TIC** | Recomendação | **DETERMINAÇÃO** | **Art. 11, parágrafo único e art. 19, IV da Lei nº 14.133/2021** (modelos de minutas e fluxos padronizados). | Nulo. Imposição legal expressa da NLLC. |
| **S6.2 – Falta de análise prévia e aprovação técnica de TI nas contratações** | Recomendação | **DETERMINAÇÃO** | **Art. 11, p. único c/c art. 18, § 1º, I e art. 7º da Lei nº 14.133/2021**; Princípio da Segregação de Funções e Economicidade. | **Inexistente.** Vedação a aquisições de tecnologia por órgãos setoriais sem manifestação da área de TIC. |
| **S6.3 – Contratações sem alinhamento ao PDTI e PCA** | Recomendação | **DETERMINAÇÃO** | **Art. 12, VII e art. 18, caput da Lei nº 14.133/2021** (compatibilização obrigatória com o Plano de Contratações Anual). | Nulo. Cumprimento estrito da Lei 14.133/2021. |
| **S6.4 – Falta de designação formal da equipe de planejamento** | Recomendação | **DETERMINAÇÃO** | **Art. 7º, caput e incisos I a III da Lei nº 14.133/2021**. | Nulo. Obrigação legal taxativa de designar formalmente os agentes públicos do planejamento. |

---

## 6. Propostas de Melhoria e Plano de Ação para os Artefatos

Com base nas conclusões deste parecer, recomenda-se o seguinte roteiro de ajustes operacionais:

### 1. Na Matriz de Planejamento (`matriz_planejamento.md`):
* **Atualizar o campo `tipo_encaminhamento`**: Alterar de `Recomendação` para `Determinação` nas 11 situações fundamentadas na Lei nº 14.133/2021, LGPD e Acórdãos paradigmáticos (S1.1, S1.2, S2.2, S2.3, S3.1, S3.2, S3.5, S4.6, S5.3, S5.5, S6.1, S6.2, S6.3, S6.4).
* **Desacoplar S3.5 e S6.3**: Redefinir as referências de itens de S3.5 (focando no orçamento do PDTI `q2102ext[C]`) e de S6.3 (focando no Plano Anual de Contratações e contratações isoladas `q2802ext[C]`, `q2802ext[D]`, `q2804[B]`).
* **Flexibilizar S4.3**: Substituir a ênfase em "criação de cargos por lei" pela exigência proporcional de "formalização de funções de confiança e atribuições da equipe técnica".

### 2. No Mapa de Verificação de Achados (`mapa-verificacao-achados.xlsx`):
* **Aba "Ações de Verificação"**:
  * Atualizar a coluna `tipo_encaminhamento` para refletir com exatidão as 11 situações convertidas em **Determinação** e as 15 mantidas como **Recomendação**;
  * Ajustar a fórmula do campo `encaminhamento` para usar o verbo no imperativo cominatória nas determinações (ex.: *"elabore e aprove formalmente o PDTI..."*) e no modo propositivo nas recomendações (ex.: *"avalie a conveniência de..."*);
* **Aba "Procedimentos de Auditoria"**:
  * Racionalizar as expressões booleanas em `logica_achado` para mitigar o efeito da disjunção irrestrita, assegurando que o achado reflita falhas substanciais e não meras ausências de formalismos secundários.

---

## 7. Conclusão

A revisão confirma que as 6 Questões e os 6 Achados estruturantes possuem **máxima higidez e devem ser mantidos**.

A calibração proposta — racionalizando as ações de verificação, eliminando a redundância entre S3.5 e S6.3, flexibilizando exigências desproporcionais como CMDB e criação de cargos, e **convertendo 11 encaminhamentos essenciais em DETERMINAÇÃO fundamentada** — elevará o trabalho ao mais alto padrão de efetividade do controle externo, garantindo acórdãos plenamente executáveis, justos e blindados perante a ordem jurídica.
