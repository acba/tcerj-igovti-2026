# Relatório final de revisão do mapa de verificação de achados (v2 — consolidação validada)

**Fiscalização TCE-RJ nº 18/2026 — iGovTI 2026**
**Data de consolidação:** 14/08/2026 (v2)
**Natureza:** minuta técnica para deliberação da Equipe de Auditoria

> Esta versão consolida e **supersede** `relatorio-final-revisao-mapa-verificacao-achados-2026-08-14.md`. Foi validada item a item contra o estado atual dos artefatos (`mapa-verificacao-achados.xlsx`, 151 ações, e `matriz_planejamento.md`, 734 linhas) em 14/08/2026. As propostas não substituem o juízo profissional da Equipe de Auditoria e somente devem ser incorporadas aos artefatos de produção depois de validação metodológica e jurídica, execução em cópia de teste e análise dos impactos sobre os resultados.

## 1. Objetivo e fontes examinadas

Consolidar as alterações recomendadas para:

1. as ações e as lógicas do mapa de verificação de achados;
2. as questões de auditoria e os possíveis achados;
3. as situações inconformes; e
4. a classificação dos encaminhamentos como recomendação ou determinação.

Foram examinados e consolidados:

- os cinco arquivos de revisão crítica `docs/revisao-mapa/revisao-critica-mapa-verificacao-achados*.md` (Gemini 3.7 Flash, GPT-5.6 Sol, Claude 4.6, DeepSeek Pro, DeepSeek V4 Flash);
- os três arquivos de proposta de ajuste `docs/revisao-mapa/proposta-ajuste-mapa-verificacao-achados*.md` (Gemini 3.7 Flash, DeepSeek Flash, Claude 4.6);
- `02-Execucao/03-Execucao_Procedimentos/01-Insumos/mapa-verificacao-achados.xlsx` (verificado: 151 ações, 41 órfãs, 112 motivos de relatório, fórmulas PA01–PA06);
- `01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/matriz_planejamento.md`;
- `01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md`;
- `02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/03-pos-comentarios-gestor/resultado_auditoria.json`;
- Acórdão TCE-RJ nº 44.490/2024-PLEN e Acórdão TCU nº 1.411/2014-Plenário (arquivados no repositório);
- [Lei nº 14.133/2021](https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/lei/l14133.htm), especialmente arts. 7º, 11, 12, 18 e 19.

## 2. Conclusão executiva e respostas aos quatro quesitos

O mapa é tecnicamente aproveitável, mas deve ser revisto antes de nova execução definitiva. Não se recomenda eliminar nenhuma das questões Q1 a Q6, a questão transversal QT ou os achados A1 a A6. O problema principal não está na arquitetura temática, mas na correspondência entre o alcance dos títulos e o que os gatilhos efetivamente demonstram, na cumulatividade excessiva das regras (A4 e A5 atingem 100% da população) e em sobreposições de gatilhos que geram dupla imputação.

| Quesito | Conclusão consolidada |
|---|---|
| 1. Ajustar ações de verificação? | **Sim.** Das 151 ações, 41 são órfãs (não participam de `logica_achado` nem de `Motivos do Relatório`). A proposta religa 9 e remove 32; a recalibração das regras dispensa outras 37 hoje ativas. Saldo: **82 ações**, todas com função definida. Corrigir também as lógicas S2.2/S2.3, S3.5/S6.3, S4.1, S4.3 a S4.6, S5.1 a S5.5 e S6.1/S6.3, e os motivos de relatório correspondentes. |
| 2. Remover questão ou achado? | **Não.** Manter Q1–Q6, QT e A1–A6. Ajustar a redação de Q4/A4 e Q6 para que não afirmem capacidade material ou toda a gestão contratual quando os testes medem principalmente formalização, planejamento e controles da fase preparatória. |
| 3. Remover situação inconforme? | **Não é necessário suprimir tema inteiro.** Devem ser restringidas, renomeadas ou desdobradas várias situações (S2.1→S2.4; S3.1→S3.3; S5.5→S5.6; recalibração de S3.5, S4.x, S5.1–S5.4 e S6.x). Elementos avançados (CMDB relacional, causa-raiz universal, publicação de perfis, ANS bilateral para todo serviço) deixam de gerar inconformidade automática e permanecem como indicadores de maturidade. O mapa passa de 26 para **29 situações** — o acréscimo separa controles distintos, não amplia a régua. |
| 4. Converter recomendação em determinação? | **Sim, em três situações: S2.2, S3.1 e S3.2.** Comitê de TIC e processo/plano de TIC (PDTI/PEDTIC) são passíveis de determinação mesmo sem normativo explícito, porque há jurisprudência consolidada do TCE-RJ (Acórdão 44.490/2024-PLEN) que já determinou esses controles e reforço do TCU (1.411/2014) e da Lei nº 14.133/2021. As demais situações permanecem recomendações ou admitem determinação apenas após comprovação de ilegalidade em processo concreto. |

### 2.1 Oportunidades de melhoria priorizadas

| Prioridade | Oportunidade | Resultado esperado |
|---|---|---|
| Imediata | Corrigir S2.2/S2.3, S3.5/S6.3 e S5.3/S5.4 | Eliminar dupla imputação do mesmo fato (S2.2+S2.3 em 7 orgs; S3.5≡S6.3 em 106 orgs; S5.3+S5.4 em 95 orgs). |
| Imediata | Corrigir S4.1 (gate `AV26`) | Eliminar dupla contagem com S1.1 para organizações sem área de TIC (FTM, TURISRIO, São João da Barra). |
| Alta | Recalibrar regras multifatoriais e retirar práticas avançadas do achado automático | Reduzir a universalidade de A4/A5 (100%) e aproximar a régua do mínimo essencial sem perder o diagnóstico de maturidade. |
| Alta | Harmonizar matriz, mapa e motivos do relatório | Garantir que questão, regra, evidência, narrativa e encaminhamento expressem a mesma condição. |
| Alta | Converter S2.2, S3.1 e S3.2 em determinações objetivas | Dar força mandamental aos controles com precedente local direto, preservando proporcionalidade. |
| Média | Reduzir e sanear o conjunto de ações (151 → 82) | Eliminar ações e variáveis órfãs e risco de questionamento de rastreabilidade. |
| Média | Separar incidentes de serviços e incidentes de segurança | Produzir evidências e encaminhamentos específicos para naturezas de risco diferentes. |

## 3. Critério para recomendação e determinação

- **Determinação:** medida mandamental, objetiva e verificável, destinada a corrigir irregularidade, prevenir sua continuidade ou restabelecer dever jurídico suficientemente definido. A redação deve indicar providência concreta e, na decisão, prazo compatível.
- **Recomendação:** oportunidade de melhoria apoiada em referencial técnico ou em solução cuja forma de implementação comporte avaliação de conveniência, oportunidade, porte, complexidade e capacidade administrativa.

O Acórdão TCE-RJ nº 44.490/2024-PLEN é o precedente local mais aderente:

- itens II.1 e III.1: **determinou** a instituição de Comitê de TI quando inexistente;
- itens II.3 e III.3: **determinou** a instituição de processo estruturado destinado a elaborar, manter e revisar PDTI, com conteúdo mínimo e aprovação pela autoridade máxima (itens II.3.5/III.3.5);
- item I.10 (Maricá): tratou o aperfeiçoamento de controles já existentes (comitê, PDTI, ativos, configuração) como **recomendações** — distinção que deve orientar o mapa.

O Acórdão TCU nº 1.411/2014-Plenário reforça a relevância do planejamento de TIC, mas seus itens finais 9.1.5/9.1.6 estão no bloco iniciado por "recomendar". Deve ser citado como reforço argumentativo, não como se o item 9.1.6 fosse, por si só, uma determinação.

A Lei nº 14.133/2021 exige cautela: o art. 11, parágrafo único, impõe governança, processos e estruturas para as contratações; o art. 18 torna obrigatório o planejamento da fase preparatória e a compatibilidade com o PCA, **sempre que este for elaborado**, e com as leis orçamentárias; o art. 7º exige agentes para funções essenciais, mas não cria, de forma universal, a composição literal de q2804[C]; e o art. 19, IV, dirige a obrigação de modelos padronizados aos órgãos com competência regulamentar sobre licitações, não a todos os jurisdicionados.

## 4. Questões de auditoria e achados: DE → PARA

| Objeto | DE | PARA | Motivação/justificativa |
|---|---|---|---|
| Q1/A1 | Estrutura de TIC, sem alteração temática | **Manter** | Questão respondível; os três controles são pertinentes. Ajustar apenas S1.2 e S1.3. |
| Q2/A2 | Governança e Comitê de TIC em uma situação ampla de modelo/monitoramento | **Manter Q2/A2 e desdobrar S2.1**, criando S2.4 para monitoramento | Papéis/objetivos e monitoramento são controles distintos; a separação evita que a falta de um indicador isolado produza o título amplo de modelo inexistente. |
| Q3/A3 | Processo formal, plano, conteúdo, integração e monitoramento | **Manter Q3/A3 e criar S3.3** para participação/priorização | Reserva a determinação ao núcleo objetivo de formalização do processo/PDTI e mantém deficiências qualitativas como recomendação. Aproveita a lacuna histórica do identificador S3.3 sem renumerar os demais itens. |
| Q4 | "capacidade institucional mínima" | "planejamento e gestão da força de trabalho e das competências de TIC e segurança da informação" | O questionário não mede produtividade, suficiência real, qualidade da fiscalização ou capacidade entregue por estruturas compartilhadas; mede quantitativos declarados, formalização, perfis e práticas de planejamento de pessoas. |
| A4 | "Capacidade institucional insuficiente para sustentar..." | "Fragilidades no planejamento e na gestão da força de trabalho e das competências de TIC e segurança da informação" | Evita concluir insuficiência material de capacidade apenas por ausência de documentos ou subitens de maturidade. |
| Q5/A5 | Gestão de serviços, ativos, configuração e incidentes | **Manter**, com critérios mínimos separados de práticas avançadas | Catálogo, metas, inventário e incidentes são pertinentes. CMDB relacional, ANS bilateral e causa-raiz para todo incidente não devem funcionar como requisitos mínimos universais. |
| Q6 | "planejamento, contratação, fiscalização e gestão" | "controles mínimos da fase preparatória das contratações de TIC, com planejamento, alinhamento e participação técnica proporcional ao risco" | Os gatilhos mais defensáveis concentram-se na fase preparatória. q2801[C]/[D]/[E] alcançam seleção e gestão contratual e não devem ampliar automaticamente o achado A6. |
| A6 | "Fragilidades na governança técnica da fase preparatória..." | **Manter** | O título atual já é mais restrito e deve orientar a revisão de Q6, S6.1 e dos procedimentos. |
| QT | Levantamento longitudinal sem achado | **Manter sem alteração** | A natureza `levantamento` e `gera_achado: false` está coerente. |

Não se recomenda renumerar os identificadores estáveis apenas para eliminar lacunas (ex.: lacunas R3.3/IR6/P6/E6/S3.3 na Q3). A criação de S3.3 resolve a lacuna material; os demais IDs devem ser preservados para não romper rastreabilidade histórica.

## 5. Situações inconformes: alterações consolidadas (DE → PARA)

As expressões usam os IDs atuais das ações. A redação final das ações deve ser atualizada para a nova situação a que passarem a pertencer.

| Situação | DE | PARA | Motivação/justificativa |
|---|---|---|---|
| S1.2 | "Área de TIC sem atribuições formais suficientes para planejamento, coordenação, gestão, execução, monitoramento e controle"; regra testa q0103[G] ou q0103[D] | "Área de TIC sem atribuições formalmente definidas ou sem atribuições formais de governança, planejamento ou gestão de TIC"; manter a lógica atual | A descrição atual é mais ampla que o teste. q0103[D] não comprova todas as funções listadas no título. |
| S1.3 | Matriz: q0102 B/C/D/E; mapa: C/D/E | Matriz e mapa: somente q0102 D/E; AV06 deve excluir B e C | B é posição estratégica aceitável. C, isoladamente, não prova falta de interlocução com a alta administração. D e E demonstram, de forma direta, posição setorial sem alcance corporativo ou ausência de posição formal. |
| S2.1 | Papéis, objetivos, rotina e indicadores unidos por OR | "Elementos básicos de direção da TIC não estabelecidos", usando `(AV07\|AV85) \| (AV08\|AV86)` | Restringe S2.1 a papéis/responsabilidades e objetivos/indicadores/metas. |
| Nova S2.4 | Inexistente | "Monitoramento do desempenho da TIC não estruturado", severidade média, usando `(AV09\|AV87) & (AV10\|AV88)` | Só caracteriza ausência de monitoramento quando faltarem simultaneamente rotina e indicadores implantados. Fragilidade isolada não recebe o mesmo tratamento da inexistência do controle. |
| S2.2 | "Comitê não instituído"; `(AV11\|AV89)` | "Comitê de TIC ou instância equivalente não instituído ou não demonstrado formalmente"; manter `(AV11\|AV89)`; alterar para **Determinação** | AV89 demonstra insuficiência da prova, não inexistência factual. A nova descrição preserva a avaliação documental sem sobreafirmar. |
| S2.3 | `(AV12\|AV90) & (AV13\|AV91)` | `AV12 & ~AV89 & (AV13\|AV91)`; remover AV90 | Evidência insuficiente da instituição não pode servir de prova positiva de existência. A atuação só deve ser testada quando houver declaração afirmativa e comprovação suficiente da instituição. |
| S3.1 | q2101[A]/[B]/[C]/[D] em OR | "Processo de planejamento de TIC não formalizado", usando `(AV17\|AV95)`; alterar para **Determinação** | Reserva o comando mandamental ao núcleo objetivo de formalização. |
| Nova S3.3 | Inexistente | "Participação das áreas demandantes ou critérios de priorização insuficientes", severidade média, usando `(AV14\|AV92) \| (AV15\|AV93)`; **Recomendação** | Separa aperfeiçoamento qualitativo de inexistência do processo. q2101[C] permanece indicador de maturidade, sem achado automático. |
| S3.2 | "Ausência de aprovação formal do plano de TIC" | "Plano de TIC/PDTI/PEDTIC inexistente, não demonstrado ou sem aprovação formal"; `(AV18\|AV96)`; alterar para **Determinação** | O valor Não/N/A e a evidência não conforme podem decorrer de inexistência ou falta de aprovação; o precedente do TCE-RJ sustenta instituição e aprovação formal. |
| S3.5 | q2102[C], q2802[C], q2802[D] e q2804[B] | Somente q2102[C] e sua avaliação: `(AV20\|AV98)` | S3.5 deve avaliar se o plano de TIC fundamenta orçamento/PCA. Os testes de PCA e contratações executadas pertencem a S6.3. |
| S4.1 | `total_TI == 0 \| total_SI == 0` | "Ausência de força de trabalho predominantemente dedicada à TIC em organização com área própria de TIC"; `AV26 & AV25`; AV26 deve excluir q0101 C e F | q0105 manda registrar quem atua nas duas áreas apenas na área predominante; `total_SI == 0` não prova ausência da função. O gate evita duplicidade com S1.1 e falso positivo em modelo centralizado externo. |
| S4.2 | Severidade alta | Severidade **média**, mantendo `(AV29\|AV103)` | A falta de estimativa documentada é fragilidade de planejamento de pessoas; não comprova, sozinha, ausência material de capacidade. |
| S4.3 | Falta de B **ou** D; título inclui cargos, funções, perfis e ocupações | "Ausência simultânea de cargos ou funções formalmente atribuídos a TIC e a segurança da informação"; `((AV31\|AV105) & (AV33\|AV107))` | Não exigir cargo efetivo nem estrutura separada para SI. A situação deve ocorrer quando nenhuma das duas funções estiver formalmente atribuída. |
| S4.4 | q2701[A], q2702[A] e q2704[B] em OR | "Perfis profissionais de gestores e colaboradores de TIC sem competências e habilidades mínimas definidas"; `(AV35\|AV109) \| (AV37\|AV111)` | Os itens A exigem publicação; q2704[B] avalia seleção para nomeação. Os itens C medem diretamente competências e habilidades do perfil, sem impor transparência ativa ou forma de provimento. |
| S4.5 | Liderança, competências técnicas e plano de capacitação em OR | "Lacunas de competências técnicas de TIC ou segurança da informação não identificadas e documentadas"; `(AV40\|AV114) \| (AV41\|AV115)` | A falta de plano de capacitação não prova falta de tratamento, que pode ocorrer por realocação, recrutamento ou apoio especializado. Retiram-se liderança genérica e tratamento exclusivamente por plano. |
| S4.6 | `((q0101 B\|C) & total_TI_interno==0) \| predominio_terceiros` | "Modelo de TIC predominantemente terceirizado sem pessoal interno informado para coordenação e fiscalização"; `AV45 & AV46`; AV45 deve aceitar somente q0101 B | Modelo C pode representar estrutura compartilhada legítima. Predomínio numérico de terceiros, isoladamente, não comprova incapacidade de coordenação ou fiscalização. |
| S5.1 | q2201[A]/[B]/[C] em OR | "Catálogo de serviços de TIC inexistente ou não disponibilizado aos usuários"; `(AV56\|AV126)` | A e B misturam metas/ANS e duplicam S5.2. C é o subitem que pressupõe catálogo existente e disponível. |
| S5.2 | ANS formal e monitoramento, em OR; severidade média | "Ausência de metas ou níveis mínimos formalizados para os serviços de TIC mais relevantes"; `((AV54\|AV124) & (AV57\|AV127))`; severidade **baixa** | Aceita como núcleo mínimo tanto metas registradas no catálogo quanto ANS formal. Somente a ausência de ambos gera a situação; o monitoramento contínuo permanece indicador de maturidade. |
| S5.3 | q2203[A], q2504[A] e q2504[B] | q2501[A], q2504[A] e q2504[B]: `(AV60\|AV130) \| (AV62\|AV132) \| (AV63\|AV133)` | q2203[A] exige base de configuração com relacionamentos e duplicava S5.4. q2501[A] é o teste direto de inventário de ativos associados à informação. |
| S5.4 | q2203[A] ou q2203[C]; severidade média | "Processo de gestão de configuração e ativos não formalizado"; `(AV66\|AV136)`; severidade **baixa** | Elimina a dupla contagem com inventário e evita exigir CMDB relacional como mínimo universal. O encaminhamento deve ser proporcional e aplicável a serviços/ativos relevantes. |
| S5.5 | Incidentes de serviços e de segurança em uma situação | "Processo de gestão de incidentes de serviços de TIC inexistente ou frágil"; `(AV67\|AV137) \| (AV70\|AV140)` | Prioridade/escalamento e formalização do processo de serviços formam um núcleo coerente. |
| Nova S5.6 | Inexistente | "Procedimentos e responsabilidades para notificação e tratamento de incidentes de segurança da informação não definidos"; `(AV71\|AV141)`; severidade alta; **Recomendação** | Separa segurança da informação de incidentes de serviço e permite encaminhamento específico. Determinação deve depender de violação legal concretamente demonstrada. |
| S6.1 | q2801[A]/[C]/[D]/[E]/[G] em OR | "Processo de planejamento das contratações de TIC não formalizado"; `(AV73\|AV143)` | C, D e E alcançam seleção e gestão contratual; G é autodeclaração genérica de aderência. A mede diretamente a fase preparatória do título A6. |
| S6.2 | "aprovação técnica obrigatória"; severidade alta | "Regra geral de análise técnica prévia das contratações de TIC não demonstrada"; manter `(AV78\|AV148)`; severidade **média** | O questionário não testa todos os processos concretos e devem ser admitidos arranjos centralizados e fluxos proporcionais ao risco. |
| S6.3 | Repete os quatro itens de S3.5 | q2802[C], q2802[D] e q2804[B]: `(AV80\|AV150) \| (AV81\|AV151) \| AV82` | Elimina sobreposição total. S6.3 passa a tratar PCA/orçamento e contratações executadas; S3.5 trata o conteúdo do plano de TIC. |
| S6.4 | Equipe formal específica para toda contratação; severidade alta | Manter a situação, reduzir para severidade **média** e acrescentar "quando compatível com a complexidade e os riscos da contratação" ao encaminhamento | A Lei nº 14.133/2021 exige agentes qualificados, mas não impõe universalmente a composição literal de q2804[C]. |

Após os desdobramentos S2.4, S3.3 e S5.6, o mapa passará de 26 para 29 situações. A quantidade maior não representa ampliação da régua: os novos registros separam controles distintos e reduzem a imputação ampla causada por disjunções.

## 6. Alterações nas ações e fórmulas do mapa (DE → PARA)

### 6.1 Fórmulas `logica_achado` (aba "Procedimentos de Auditoria")

| Procedimento | DE | PARA | Motivação/justificativa |
|---|---|---|---|
| PA01 | `(AV01 \| (AV02 & (AV03 \| (AV04 \| AV84))) \| (AV05 & AV06))` | **Manter a fórmula**, alterando apenas o valor inconforme de AV06 para q0102 D/E | A estrutura lógica está adequada; o problema é o universo de valores de AV06. |
| PA02 | `(((AV07\|AV85)\|(AV08\|AV86)\|(AV09\|AV87)\|(AV10\|AV88)) \| (AV11\|AV89) \| ((AV12\|AV90)&(AV13\|AV91)))` | `((AV07\|AV85) \| (AV08\|AV86) \| ((AV09\|AV87)&(AV10\|AV88)) \| (AV11\|AV89) \| (AV12&~AV89&(AV13\|AV91)))` | Separa monitoramento (S2.4) e impede que evidência insuficiente da instituição seja usada como prova de existência do comitê. |
| PA03 | Quatro itens de q2101 e quatro itens repetidos em S3.5/S6.3 | `((AV17\|AV95) \| (AV14\|AV92) \| (AV15\|AV93) \| (AV18\|AV96) \| (AV19\|AV97) \| (AV20\|AV98) \| (AV24\|AV101))` | Separa formalização (S3.1) de qualidades do processo (S3.3) e elimina a duplicidade com S6.3. |
| PA04 | `((AV25\|AV27) \| (AV29\|AV103) \| ((AV31\|AV105)\|(AV33\|AV107)) \| ((AV34\|AV108)\|(AV36\|AV110)\|(AV38\|AV112)) \| (AV39\|AV40\|AV41\|(AV42\|AV116)) \| ((AV45&AV46)\|AV53))` | `((AV26&AV25) \| (AV29\|AV103) \| ((AV31\|AV105)&(AV33\|AV107)) \| ((AV35\|AV109)\|(AV37\|AV111)) \| ((AV40\|AV114)\|(AV41\|AV115)) \| (AV45&AV46))` | Corrige falsos positivos, substitui publicação por competências e retira predomínio numérico como prova autônoma de incapacidade. |
| PA05 | Catálogo, ANS, inventário/configuração e incidentes em disjunções amplas | `((AV56\|AV126) \| ((AV54\|AV124)&(AV57\|AV127)) \| (AV60\|AV130) \| (AV62\|AV132) \| (AV63\|AV133) \| (AV66\|AV136) \| (AV67\|AV137) \| (AV70\|AV140) \| (AV71\|AV141))` | Distingue catálogo, metas/ANS, inventário, formalização da configuração e dois tipos de incidente. |
| PA06 | Cinco subitens em S6.1 e quatro itens idênticos a S3.5 em S6.3 | `((AV73\|AV143) \| (AV78\|AV148) \| (AV80\|AV150) \| (AV81\|AV151) \| AV82 \| AV83)` | Restringe A6 à fase preparatória e elimina q2102[C] duplicado. |

### 6.2 Ações órfãs, ações religadas e ações removidas

O levantamento programático confirmou **110 ações atualmente utilizadas e 41 órfãs** (mesma relação apontada pelas cinco revisões). A solução não é remover indiscriminadamente todas as órfãs: nove são necessárias às regras recalibradas.

| Tratamento | Ações | DE | PARA | Motivação/justificativa |
|---|---|---|---|---|
| Religar | AV26 | Órfã | Gate de S4.1 | Impedir S4.1 para organização sem área de TIC ou com modelo centralizado externo. Ajustar a inconformidade de AV26 para excluir q0101 C/F. |
| Religar | AV35, AV37, AV109, AV111 | Órfãs | Núcleo de S4.4 | Testam competências/habilidades de perfis (q2701[C]/q2702[C]), sem exigir publicação ou forma de seleção. |
| Religar | AV114, AV115 | Órfãs | Espelhos documentais de AV40/AV41 em S4.5 | Corrigem a assimetria pela qual a declaração positiva sem prova escapava da situação. |
| Religar | AV60, AV130 | Órfãs | Inventário de ativos associados à informação em S5.3 | Substituem q2203[A], que mede configuração e relacionamentos. |
| Remover — órfãs sem função | AV28, AV30, AV32, AV43, AV44, AV47–AV52, AV61, AV65, AV68, AV69, AV72, AV102, AV104, AV106, AV113, AV117–AV123, AV131, AV135, AV138, AV139 e AV142 | Linhas sem efeito | Linhas excluídas | São 32 das 41 órfãs atuais e não compõem o núcleo das regras finais. |
| Remover — dispensadas pela recalibração | AV16, AV21–AV23, AV27, AV34, AV36, AV38, AV39, AV42, AV53, AV55, AV58, AV59, AV64, AV74–AV77, AV79, AV90, AV94, AV99, AV100, AV108, AV110, AV112, AV116, AV125, AV128, AV129, AV134, AV144–AV147 e AV149 | Linhas hoje ativas | Linhas excluídas | São 37 ações que deixam de ser necessárias após restringir os títulos e separar situações. |

O saldo proposto é de **82 ações de verificação**. Cada uma deve consultar uma única coluna ou variável e participar de ao menos uma fórmula ou motivo.

### 6.3 Mudança de situação associada às ações mantidas

| Ações | DE | PARA | Motivação/justificativa |
|---|---|---|---|
| AV09, AV10, AV87, AV88 | S2.1 | Nova S2.4 | Monitoramento deixa de integrar o título de modelo básico. |
| AV14, AV15, AV92, AV93 | S3.1 | Nova S3.3 | Participação e priorização são aperfeiçoamentos do processo, não prova de sua inexistência. |
| AV35, AV37, AV109, AV111 | Linhas órfãs de S4.4 | Núcleo de S4.4 | Substituem os itens de publicação e seleção. |
| AV40, AV41, AV114, AV115 | Parte de S4.5 | Núcleo completo de S4.5 | Restrição às lacunas técnicas e inclusão da avaliação documental. |
| AV54, AV124 | S5.1 | S5.2 | Metas no catálogo passam a ser forma alternativa de nível mínimo de serviço. |
| AV60, AV130 | Órfãs de S5.3 | Núcleo de S5.3 | Inventário de ativos associados à informação. |
| AV71, AV141 | S5.5 | Nova S5.6 | Incidentes de segurança recebem situação e encaminhamento próprios. |

### 6.4 Motivos do relatório (aba "Motivos do Relatório", 112 linhas atuais)

A aba deve ser ajustada em conjunto com as fórmulas. Não basta alterar `logica_achado`, pois motivos incompatíveis produziriam narrativas contraditórias.

| Linhas/IDs | DE | PARA | Motivação/justificativa |
|---|---|---|---|
| MR012–MR015 | S2.1, condições individuais | S2.4; cada motivo só aparece quando também falhar o outro componente do AND | Coerência com a nova S2.4. |
| MR016–MR021 | AV90 pode sustentar S2.3 | Atualizar S2.2 para "não instituído ou não demonstrado"; excluir MR019; usar AV12, `~AV89`, AV13 e AV91 em MR018/MR020/MR021 | Eliminar dupla imputação de comitê inexistente e inativo. |
| MR022–MR029 | Todos em S3.1 | MR022–MR025 passam a S3.3; excluir os motivos de q2101[C]; MR028/MR029 permanecem em S3.1 | Separar inexistência formal de qualidades do processo. |
| MR034–MR040 | Quatro gatilhos em S3.5 | Manter apenas os motivos de AV20/AV98; excluir os vinculados a q2802/q2804 | Os demais gatilhos permanecem apenas em S6.3. |
| MR043–MR044 | TI ou SI igual a zero | MR043 condicionado a AV26 & AV25; excluir MR044 | q0105 não permite inferir ausência da função SI a partir de `total_SI == 0`. |
| MR047–MR050 | Motivos independentes de B/D | Exibir somente quando ambas as famílias B e D estiverem inconformes | Coerência com o AND de S4.3. |
| MR051–MR056 | q2701[A], q2702[A], q2704[B] | Reaproveitar quatro linhas para AV35/AV109 e AV37/AV111; excluir as duas excedentes | Adequar aos novos testes de perfil. |
| MR057–MR061 | Liderança, técnica e plano | Reescrever quatro linhas para AV40/AV114 e AV41/AV115; excluir a linha excedente | Coerência com S4.5 restrita às competências técnicas. |
| MR062–MR064 | Modelo B/C ou predomínio de terceiros | Manter MR062/MR063 para q0101 B + zero interno; excluir MR064 | Predomínio numérico deixa de ser gatilho autônomo. |
| MR065–MR074 | Catálogo e ANS separados por OR | MR069/MR070 ficam em S5.1; MR065/MR066 e MR071/MR072 passam a S5.2 com gate recíproco; excluir os demais | S5.2 só ocorre quando faltarem tanto metas no catálogo quanto ANS. |
| MR075–MR080 | q2203[A] + q2504[A]/[B] | Reaproveitar MR075/MR076 para AV60/AV130 e manter os pares de q2504 | Substituir configuração por inventário de ativos associados à informação. |
| MR081–MR084 | q2203[A]/[C] | Excluir MR081/MR082; manter MR083/MR084 | S5.4 fica restrita à formalização. |
| MR085–MR090 | Uma situação de incidentes | MR085–MR088 permanecem em S5.5; MR089/MR090 passam a S5.6 | Separar incidentes de serviço e de segurança. |
| MR091–MR100 | Cinco gatilhos em S6.1 | Manter MR091/MR092 e excluir MR093–MR100 | S6.1 fica restrita ao planejamento da contratação. |
| MR103–MR109 | q2102 + q2802 + q2804 em S6.3 | Excluir MR103/MR104; manter MR105–MR109 | Eliminar repetição de q2102[C] com S3.5. |

### 6.5 Outras correções no XLSX

| Local | DE | PARA | Motivação/justificativa |
|---|---|---|---|
| `Fontes de Informação!B5` | `Painel consolidado da avalia??o de evid?ncias` | `Painel consolidado da avaliação de evidências` | Corrigir perda de codificação. |
| `Variáveis Temporárias` | VT02, VT04 e VT05 ativas | Remover VT02, VT04 e VT05 após excluir AV27 e AV53; manter VT01 e VT03 | Variáveis sem consumidor não devem permanecer no contrato operacional. |
| `Ações de Verificação`, S6.2 | Encaminhamento inclui "segurança da informação" (AV78); matriz não | Adotar a mesma redação nos dois artefatos | Eliminar divergência textual entre matriz e mapa. |

## 7. Alterações correspondentes na matriz de planejamento (DE → PARA)

As alterações do mapa somente são válidas se a matriz permanecer como fonte de verdade. Devem ser feitas, no mínimo, as seguintes mudanças coordenadas.

| Bloco/campo | DE | PARA | Motivação/justificativa | Status |
|---|---|---|---|---|
| Q1 — S1.3 | Regra q0102 B/C/D/E | Regra q0102 **D/E** (estado final, conforme § 5) | B é posição estratégica aceitável e C, isoladamente, não prova falta de interlocução com a alta administração. | 🔶 Parcialmente aplicado na cópia de trabalho (14/08/2026: B removido — regra atual C/D/E). Falta excluir C na matriz e ajustar AV06 no mapa para D/E. |
| Q1 — S1.2 | Descrição ampla de todas as funções de TIC | Descrição limitada a ausência geral de atribuições ou ausência de governança, planejamento e gestão | Alinhar o texto a q0103[G]/[D]. Ajustar E3/E4 e o encaminhamento na mesma direção. | Pendente |
| Q2 — riscos, procedimentos e evidências | R2.1/P1/P2/E1/E2 misturam direção e monitoramento | Separar o risco de falta de direção do risco de ausência de monitoramento; criar referências para S2.4 | Sustentar o desdobramento sem perda de rastreabilidade. | Pendente |
| Q2 — S2.1/S2.4 | Uma situação com quatro subitens em OR | S2.1 com q1001[C]/[H]; S2.4 com q1002[A] e [C] em AND | Mesma lógica do mapa. | Pendente |
| Q2 — S2.2 | "não instituído"; Recomendação | "não instituído ou não demonstrado formalmente"; **Determinação** | A matriz deve refletir tanto resposta negativa quanto avaliação documental insuficiente. | Pendente |
| Q2 — S2.3 | Apenas `(E == Sim) & (F != Sim)` | Exigir também comprovação suficiente da instituição e admitir avaliação não conforme da atuação | Evitar que evidência insuficiente da existência habilite teste de funcionamento. | Pendente |
| Q3 — R/IR/P/E/S3.1 | Processo formal e atributos qualitativos unidos | S3.1 restrita a q2101[D]; criar R3.3, IR6, P6, E6 e S3.3 para participação/priorização; q2101[C] fica fora do achado automático | Restabelecer rastreabilidade e proporcionalidade; preencher a lacuna histórica S3.3. | Pendente |
| Q3 — S3.1 | Recomendação genérica | **Determinação** para estabelecer processo estruturado destinado a elaborar, manter e revisar PDTI/PEDTIC ou equivalente | Precedente direto do TCE-RJ. | Pendente |
| Q3 — S3.2 | Ausência de aprovação; Recomendação | Inexistência/não demonstração/falta de aprovação; **Determinação** para elaborar/submeter/aprovar formalmente PDTI/PEDTIC ou equivalente | Precedente direto do TCE-RJ e redação aderente ao dado. | Pendente |
| Q3 — IR8/P8/E8/S3.5 | Incluem q2102, q2802 e q2804 | Restringir a q2102[C]/q2102evi | Os dados de PCA e contratação concreta ficam exclusivamente em Q6. | Pendente |
| Q4/A4 — títulos | Capacidade institucional insuficiente | Planejamento e gestão da força de trabalho e das competências | Evitar conclusão material não mensurada. | Pendente |
| Q4 — S4.1 | TI ou SI igual a zero | q0101 fora de C/F e total_TI igual a zero; retirar `total_SI` | Respeitar a instrução de preenchimento de q0105 e modelos compartilhados. | Pendente |
| Q4 — S4.2 | Severidade alta | Severidade média | Fragilidade de planejamento, não ausência material comprovada. | Pendente |
| Q4 — S4.3 | B ou D ausente; descrição inclui cargos efetivos | B e D simultaneamente ausentes; descrição limitada a função formal | Evitar ingerência sobre criação de cargos e admitir SI integrada. | Pendente |
| Q4 — IR4/IR5/IR6, P4/P5, E4/E5 e S4.4 | Publicação de perfis e seleção de gestores | Competências/habilidades dos perfis em q2701[C]/q2702[C]; retirar q2704 do achado | Publicação e forma de seleção permanecem no questionário como maturidade. | Pendente |
| Q4 — IR7/IR8, P6, E6 e S4.5 | Liderança, técnicas e plano de capacitação | Lacunas técnicas q2705[C]/[D] | Não confundir plano de treinamento com todas as formas de tratamento. | Pendente |
| Q4 — IR9/P7/E7/S4.6 | Modelos B/C ou predomínio de terceiros | Modelo B e ausência de pessoal interno | O teste final não deve afirmar incapacidade com base apenas em predominância numérica. | Pendente |
| Q5 — subquestões e IR/P/E | Catálogo/ANS/configuração tratados como requisitos uniformes | Distinguir catálogo disponível, metas ou ANS alternativos, inventário e formalização proporcional da configuração | Ajustar o desenho à heterogeneidade do universo. | Pendente |
| Q5 — S5.1/S5.2 | A/B/C e D/E em OR | S5.1 por q2201[C]; S5.2 por ausência simultânea de q2201[A] e q2201[D] | Eliminar sobreposição catálogo–ANS e aceitar solução equivalente. | Pendente |
| Q5 — S5.3/S5.4 | q2203[A] nas duas situações | S5.3 com q2501[A]/q2504[A]/[B]; S5.4 com q2203[C] | Eliminar dupla contagem e CMDB como mínimo universal. | Pendente |
| Q5 — S5.5 | Serviços e segurança juntos | S5.5 para incidentes de serviços e nova S5.6 para incidentes de segurança | Produzir encaminhamentos específicos e rastreáveis. | Pendente |
| Q6 — questão/subquestões/riscos | Planejamento, seleção, fiscalização e gestão | Controles mínimos da fase preparatória, alinhamento e participação técnica proporcional | Coerência com A6 e com os itens efetivamente mantidos. | Pendente |
| Q6 — IR1/IR2/IR3/P1/P2/E1/E2/S6.1 | q2801[A]/[C]/[D]/[E]/[G] | q2801[A] e respectiva evidência | Restringir S6.1 à fase preparatória. | Pendente |
| Q6 — S6.2 | Obrigatoriedade universal; severidade alta | Regra geral não demonstrada; severidade média; redação proporcional e alinhada à do mapa | O teste não substitui exame de processos concretos. | Pendente |
| Q6 — IR6/P4/E5/S6.3 | Inclui q2102[C] | Excluir q2102[C]; manter q2802[C]/[D], q2804[B] e evidências correspondentes | Separar planejamento de TIC de execução do PCA/contratações. | Pendente |
| Q6 — S6.4 | Severidade alta e equipe específica universal | Severidade média e cláusula de aplicabilidade conforme complexidade/risco | Art. 7º da Lei nº 14.133/2021 não impõe a composição literal de q2804[C] a toda contratação. | Pendente |
| Todas as situações alteradas | `tipo_encaminhamento` e textos atuais | Replicar exatamente o tipo e o texto aprovados no mapa | Evitar divergência entre fonte de planejamento e instrumento de execução. | Pendente |

## 8. Encaminhamentos: DE/PARA e fundamento

### 8.1 Converter agora para determinação

A jurisprudência do TCE-RJ (Acórdão 44.490/2024-PLEN) e do TCU (1.411/2014-Plenário) sustenta determinação para Comitê de TIC e PDTI/PEDTIC **mesmo sem normativo explícito aplicável a todos os jurisdicionados**, pois o conteúdo mínimo da governança de TIC já foi deliberado por essas Cortes, e a Lei nº 14.133/2021 (art. 11, parágrafo único, e art. 18) reforça o dever de governança e planejamento.

| Situação/ações remanescentes | DE | PARA | Motivação/justificativa | Redação proposta |
|---|---|---|---|---|
| S2.2 — AV11/AV89 | Recomendação | **Determinação** | Acórdão TCE-RJ nº 44.490/2024-PLEN, itens II.1 e III.1, determinou a instituição de Comitê de TI aos auditados em que a instância não existia. A redação admite instância equivalente e proporcional ao porte. | `institua formalmente Comitê de TIC ou instância equivalente, compatível com o porte e a estrutura decisória da organização, definindo composição, competências, periodicidade de reuniões, registro das deliberações e acompanhamento dos encaminhamentos` |
| S3.1 — AV17/AV95 | Recomendação | **Determinação** | Itens II.3 e III.3 do mesmo acórdão determinaram processo estruturado para elaborar, manter e revisar PDTI. A nova regra testa somente a inexistência/não demonstração da formalização. | `estabeleça formalmente processo estruturado, compatível com o porte da organização, destinado a elaborar, manter e revisar periodicamente PDTI, PEDTIC ou instrumento equivalente, com participação das áreas relevantes e definição de responsáveis` |
| S3.2 — AV18/AV96 | Recomendação | **Determinação** | Os itens II.3.5 e III.3.5 exigem aprovação do PDTI pela autoridade máxima. A situação deve abranger plano inexistente, não demonstrado ou não aprovado. | `elabore, submeta e mantenha formalmente aprovado pela alta administração PDTI, PEDTIC ou instrumento equivalente, preservando o ato de aprovação e a vigência do plano` |

As linhas de ação acima (inclusive espelhos de avaliação de evidências) devem receber a mesma classificação na planilha. Não se deve manter ações de uma mesma situação com tipos distintos.

### 8.2 Manter como recomendação

| Situações | Motivação/justificativa |
|---|---|
| S1.1–S1.3 | Estrutura, atribuições e posicionamento envolvem desenho organizacional e referenciais preferenciais. Não impor organograma específico nem criação de cargos. |
| S2.1, S2.3 e S2.4 | Tratam de conteúdo, funcionamento e monitoramento de mecanismos existentes. O Acórdão TCE-RJ nº 44.490/2024 tratou aperfeiçoamentos de controles existentes como recomendações (item I.10). |
| S3.3–S3.6 | Participação, priorização, alinhamento, integração e acompanhamento são atributos qualitativos. Em Maricá, o aperfeiçoamento de PDTI já existente foi objeto de recomendação. |
| S4.1–S4.6 | Gestão de pessoas, perfis, competências e modelo de operação exigem proporcionalidade e não autorizam ingerência automática em cargos ou quantitativos. |
| S5.1–S5.6 | Catálogo, metas/ANS, configuração e processos de serviço apoiam-se principalmente em ITIL/COBIT. Mesmo inventário e incidentes precisam de recorte fático específico antes de se afirmar violação legal. |
| S6.1–S6.4 | O questionário mede regras gerais e declarações, não substitui exame de processo licitatório concreto. Art. 7º não exige a equipe literal de q2804[C], e art. 19, IV, não se aplica indistintamente a todo órgão. |

### 8.3 Determinação possível apenas após teste concreto

| Tema | Condição para determinação | Por que não converter automaticamente no mapa |
|---|---|---|
| Contratação sem planejamento/alinhamento | Processo concreto demonstrar descumprimento do art. 18 da Lei nº 14.133/2021, inclusive incompatibilidade com PCA existente ou leis orçamentárias | S6.3 combina declarações sobre PCA e alinhamento; o art. 18 usa a ressalva "sempre que elaborado". |
| Ausência de análise técnica | Processo concreto demonstrar que considerações técnicas essenciais foram omitidas e que a unidade competente não participou quando necessária | A lei exige considerações técnicas, mas não contém regra universal de aprovação pela área de TIC para toda contratação. |
| Fiscalização de terceiros | Contrato concreto sem fiscal/gestor qualificado ou sem fiscalização exigida pelo art. 117 | Predomínio numérico de terceirizados não comprova ausência de fiscalização. |
| Inventário ou incidente de segurança | Evidência demonstrar violação específica de dever patrimonial, de segurança ou de comunicação previsto em norma aplicável | Os gatilhos atuais são mais amplos que os comandos legais e misturam boas práticas com deveres jurídicos. |

## 9. Propostas das revisões que não devem ser acolhidas sem ressalva

| Proposta encontrada (fonte) | Conclusão final | Justificativa |
|---|---|---|
| Converter 11 a 14 situações em determinação com base genérica em LGPD, Lei 4.320/1964, art. 7º/18/19 da Lei 14.133/2021 e itens "recomendar" do TCU 1.411/2014 (Gemini 3.7 Flash; parcialmente DeepSeek Pro/V4 Flash) | **Não acolher em bloco; converter apenas S2.2, S3.1 e S3.2** | O escopo dos gatilhos é mais amplo que o dever legal específico; o art. 7º não impõe a composição literal de q2804[C]; o art. 19, IV, não se aplica a todo jurisdicionado; o bloco final do TCU 1.411/2014 é de recomendações. Determinação depende de condição concreta e norma aplicável. |
| Converter S1.1/S1.2 em determinação com base apenas em eficiência e art. 11 da Lei nº 14.133/2021 (Gemini) | **Não acolher** | O art. 11 trata governança das contratações e não autoriza o Tribunal a desenhar toda a estrutura administrativa de TIC. |
| Converter S2.3 em determinação (Gemini) | **Não acolher automaticamente** | O precedente local determinou instituir comitê inexistente, mas recomendou aperfeiçoar funcionamento/monitoramento de comitê existente. |
| Converter S4.1/S4.6 em determinação (Gemini/DeepSeek Pro) | **Não acolher automaticamente** | Quantidade/predominância não prova incapacidade nem ausência de fiscalização contratual. |
| Remover S4.3, S4.6, S6.3 e S6.4 do achado (GPT-5.6 Sol; Claude 4.6 remove S4.3 e S5.2) | **Não remover em bloco; recalibrar** | Os temas permanecem relevantes; a recalibração (AND, gate, severidade e título) resolve a desproporcionalidade sem suprimir subquestões, que ficariam sem resposta direta no achado. |
| Tratar Acórdão TCU 1.411/2014, item 9.1.6, como determinação | **Corrigir** | No dispositivo final, o item 9.1 é expressamente um bloco de recomendações. |
| Manter S3.5 e S6.3 idênticas apenas com nota metodológica (DeepSeek Pro/V4 Flash) | **Não acolher** | A separação dos itens é simples, preserva as duas subquestões e elimina a aparência de dupla imputação. |
| Usar incidência de 100% como prova de erro (Claude 4.6) | **Não acolher como prova; usar como sinal de revisão** | Universalidade pode refletir baixa maturidade real. A decisão deve se apoiar na validade do gatilho, não apenas na frequência. |
| Manter as fórmulas PA01–PA06 intactas e tratar dupla contagem apenas com nota metodológica (propostas DeepSeek Flash/Gemini com premissa de lógica inalterada) | **Não acolher como solução final** | As propostas foram úteis para listar remoções de órfãs e conversões por linha, mas as correções de dupla contagem exigem editar `logica_achado` e `Motivos do Relatório`; as notas metodológicas ficam restritas aos efeitos residuais do ciclo já executado. |
| Afirmar que o mapa já exclui q0101 C em S4.6 | **Corrigir** | No arquivo vigente, AV45 contém as alternativas B **e C**. A exclusão de C ainda precisa ser feita. |
| Renumerar todos os IDs para eliminar lacunas (DeepSeek Pro) | **Não acolher no ciclo atual** | A estabilidade dos IDs é mais valiosa para rastreabilidade. Criar S3.3 e documentar eventuais lacunas restantes. |
| Ajustes no catálogo YAML de prompts (GPT-5.6 Sol: critérios de q0102[B]/[C]/[D] reescrevem as alternativas) | **Acolher, na etapa de implementação** | O prompt deve apenas verificar se a evidência confirma a posição declarada. Editar o YAML `igovti_2026_achados_binario_v1.yml` e regenerar os prompts. |

## 10. Ordem de implementação e validação

1. Editar primeiro `matriz_planejamento.md`, mantendo-a como fonte de verdade (o único ajuste já aplicado é S1.3/q0102).
2. Aplicar, em cópia do XLSX sob `/tmp/tcerj-igovti-2026`, as mudanças nas fontes, variáveis, ações, procedimentos e motivos (§§ 6.1 a 6.5).
3. Conferir que todas as ações remanescentes têm uma única `informacao_requerida`, fonte existente, situação, critério, tipo e encaminhamento.
4. Conferir que cada ação é referenciada por `logica_achado`, `condicao_exibicao` ou `acoes_referencia` e que nenhuma referência aponta para ação removida.
5. Atualizar o catálogo YAML de prompts (sem editar os Markdown gerados diretamente); manter apenas avaliações ainda consumidas pelo mapa e regenerar os prompts; validar com `--provider fake`.
6. Regenerar `painel-avaliacao-evidencias.xlsx` para refletir as ações mantidas.
7. Executar a validação estrutural do mapa e `executa_auditoria.py --somente-dados` em `/tmp`.
8. Comparar, por situação e auditado, o resultado anterior e o recalibrado. Toda saída deve ser explicável por uma alteração aprovada neste relatório.
9. Regenerar matriz de achados, relatórios individuais, relatório consolidado, tabelas e gráficos.
10. Ajustar os templates para distinguir determinação de recomendação, inclusive quanto a prazo, plano de ação e consequência do descumprimento (art. 63 da LC nº 63/1990).

## 11. Checklist de aceite

- [ ] Q1–Q6, QT e A1–A6 foram preservados.
- [ ] Q4/A4 e Q6 foram renomeados ou delimitados conforme o alcance dos testes.
- [ ] S2.2 e S2.3 não podem ocorrer pelo mesmo fato de inexistência/não comprovação do comitê.
- [ ] S3.5 e S6.3 não compartilham mais os mesmos gatilhos.
- [ ] `total_SI == 0` não gera S4.1.
- [ ] q0101 C e predomínio numérico de terceiros não geram S4.6 isoladamente.
- [ ] q2203[A] não gera simultaneamente S5.3 e S5.4.
- [ ] As 69 ações indicadas foram removidas e as 9 órfãs úteis foram religadas (saldo: 82 ações).
- [ ] Não existem ações ou variáveis temporárias órfãs.
- [ ] Os motivos do relatório refletem exatamente as novas fórmulas.
- [ ] Somente S2.2, S3.1 e S3.2 foram convertidas automaticamente em determinação.
- [ ] S6.1–S6.4 permanecem recomendações no mapa, sem impedir determinação baseada em processo concreto.
- [ ] Matriz e mapa têm textos, tipos de encaminhamento, severidades e critérios coerentes.
- [ ] A execução de teste não apresentou fontes, ações, colunas ou recursos ausentes.
- [ ] A Equipe de Auditoria aprovou expressamente as mudanças e seus impactos.

## 12. Conclusão

A revisão final preserva a cobertura temática do iGovTI 2026, mas substitui a lógica de "qualquer subitem ausente gera deficiência ampla" por testes que distinguem:

1. controle essencial inexistente ou não demonstrado;
2. controle existente, porém incompleto; e
3. prática de maior maturidade, sem achado automático.

Essa solução reduz falsos positivos e dupla imputação, melhora a aderência entre título, evidência e encaminhamento e fortalece as determinações que possuem precedente local direto — Comitê de TIC e processo/plano de TIC (PDTI/PEDTIC), passíveis de determinação ainda que sem normativo explícito, por força da jurisprudência consolidada do TCE-RJ e do TCU. O ganho de efetividade não virá de aumentar indiscriminadamente a força cogente dos encaminhamentos, mas de reservar a determinação para comandos objetivos e verificáveis e manter recomendações proporcionais para escolhas de aperfeiçoamento da gestão.
