|  |
| --- |
| **P****rocesso:** 101.088-0/26  **Origem:** SIGILOSO  **Natureza:** RELATÓRIO DE AUDITORIA GOVERNAMENTAL - AUDITORIA DE CONFORMIDADE  **Observação:** Verificar a adoção de controles e sua aderência às boas práticas de segurança da informação e segurança cibernética a fim de mitigar os principais riscos às informações e sistemas das organizações no âmbito da Administração Pública Estadual, por meio de uma auditoria de conformidade com contornos operacionais. |

**RELATÓRIO DE AUDITORIA GOVERNAMENTAL**

**DADOS DA FISCALIZAÇÃO**

|  |  |
| --- | --- |
| Número da fiscalização: | 18/2026 |
| Modalidade: | AUDITORIA DE CONFORMIDADE |
| Forma de autorização: | ORDINÁRIA |
| Ato originário: | PROCESSO TCE-RJ nº 303.389-0/2025 |
| Jurisdicionados: | AGENERSA, AGERIO, AGETRANSP, CEASA, CECIERJ, CEDAE, CEHAB, CENTRAL, CEPERJ, CODERTE, CODIN, CGE, DEGASE, DERRJ, DETRAN, DETRO, DPGE, DRM, EMATER, EMOP, FAETEC, FAPERJ, FIA, FIPERJ, FLXIII, FMIS, FS, FSC, FTM, FUNARJ, GSI, IEEA, INEA, IRM, IO, IPEM, ITERJ, IVB, JUCERJA, LOTERJ, MPE, PESAGRO, PGE, PMAR, PMA, PMAB, PMAC, PMBP, PMBR, PMCF, PMCG, PMCA, PMDC, PMG, PMI, PMJ, PMM, PMM, PMM, PMM, PMN, PMNF, PMNI, PMP, PMP, PMPR, PMQ, PMQ, PMQ, PMRO, PMSJB, PMSJM, PMSPA, PMS, PMS, PMSG, PMT, PMVR, PROCON, PRODERJ, RIOTRILHOS, RJ PREV, SEAP, SEAPA, SECTI, SECEC, SECC, SECID, SEDEC, SEDCON, SEDEICS, SEDSODH, SEEDUC, SEENEMAR, SEENVS, SEELJE, SEFAZ, SEGOV, SEHIS, SEIOP, SEPLAG, SEPOL, SEPM, SES, SETD, SETRANS, SETUR, SUDERJ, TCE, TJERJ, TURISRIO, UENF, UERJ. |
| Objetivo da fiscalização: | Avaliar o grau de adoção dos jurisdicionados às boas práticas de governança e gestão de TI. |
| Ofícios de apresentação: | AUD/SGE/GAP 3232/25 a 3241/25, 3243/25 a 3268/25 todos de 06/08/2025. |
| Período abrangido: | janeiro/24 a julho/26 |
| Período de execução: | 02/02/26 à 03/07/26 |
| Equipe: | Augusto César Benvenuto de Almeida, mat. 02/4823  João Paulo de Freitas Ramirez, mat. 02/4820 |
| Supervisão: | Bruno Mattos Souza de Souza Melo, mat. 02/4258 |

![](data:image/png;base64...)

# SUMÁRIO

[SUMÁRIO 3](#_Toc216981879)

[LISTA DE ANEXOS 5](#_Toc216981880)

[1. RESUMO 6](#_Toc216981881)

[2. INTRODUÇÃO 8](#_Toc216981882)

[2.1 Antecedentes 8](#_Toc216981883)

[2.2 Objetivo e escopo 9](#_Toc216981884)

[2.3 Limitações 9](#_Toc216981885)

[2.4 Critérios aplicados 9](#_Toc216981886)

[2.5 Metodologia utilizada 10](#_Toc216981887)

[2.6 Benefícios estimados 11](#_Toc216981888)

[3. VISÃO GERAL DO OBJETO 12](#_Toc216981889)

[2.1. Família ISO 27000 13](#_Toc216981890)

[2.2. Controles CIS 13](#_Toc216981891)

[2.3. Base legal (Normativos aplicáveis) 14](#_Toc216981892)

[2.3. Primeira fase da fiscalização de segurança cibernética 15](#_Toc216981893)

[4. RESULTADOS DA AUDITORIA 16](#_Toc216981894)

[4.1. Avaliação dos planos de ação elaborados em atendimento a fase 1 da fiscalização 16](#_Toc216981895)

[4.1.1. Visão geral 17](#_Toc216981896)

[4.2. Índice de segurança cibernética básica (iSegCiber) 21](#_Toc216981897)

[4.2.1. Controles com maior aderência 23](#_Toc216981898)

[4.2.2. Maiores riscos 24](#_Toc216981899)

[4.2.3 Análise de Dados 26](#_Toc216981900)

[4.2.4 Desafios e Deficiências em Segurança da Informação 27](#_Toc216981901)

[4.3. Achados de Auditoria 28](#_Toc216981902)

[4.3.1 Achado 1 – Medidas básicas de segurança cibernética insuficientes na gestão de vulnerabilidades 28](#_Toc216981903)

[4.3.2. Achado 2 – Medidas básicas de segurança cibernética insuficientes na gestão de registros de auditoria (logs) 34](#_Toc216981904)

[4.3.3. Achado 3 – Medidas básicas de segurança cibernética insuficientes nas proteções de *e-mail* e navegador *web* 40](#_Toc216981905)

[4.3.4. Achado 4 – Medidas básicas de segurança cibernética insuficientes nas defesas contra malware 45](#_Toc216981906)

[4.3.5. Achado 5 – Medidas básicas de segurança cibernética insuficientes no processo de recuperação de dados 50](#_Toc216981907)

[4.3.6. Achado 6 – Medidas básicas de segurança cibernética insuficientes na gestão da infraestrutura de rede 55](#_Toc216981908)

[4.3.7. Achado 7 – Medidas básicas de segurança cibernética insuficientes no programa de conscientização e treinamento em segurança 59](#_Toc216981909)

[4.3.8. Achado 8 – Medidas básicas de segurança cibernética insuficientes na gestão de provedores de serviços 66](#_Toc216981910)

[4.3.9. Achado 9 – Medidas básicas de segurança cibernética insuficientes na gestão de respostas a incidentes 70](#_Toc216981911)

[5. COMENTÁRIOS DO GESTOR E ANÁLISE DA EQUIPE 75](#_Toc216981912)

[5.1. Achado 1 - Medidas básicas de segurança cibernética insuficientes na gestão de vulnerabilidades 76](#_Toc216981913)

[5.2. Achado 2 - Medidas básicas de segurança cibernética insuficientes na gestão de registros de auditoria (*logs*) 77](#_Toc216981914)

[5.3. Achado 3 - Medidas básicas de segurança cibernética insuficientes nas proteções de *e-mail* e navegador *web* 78](#_Toc216981915)

[5.4. Achado 4 – Medidas básicas de segurança cibernética insuficientes nas defesas contra malware 80](#_Toc216981916)

[5.5. Achado 5 – Medidas básicas de segurança cibernética insuficientes no processo de recuperação de dados 81](#_Toc216981917)

[5.6. Achado 6 – Medidas básicas de segurança cibernética insuficientes na gestão da infraestrutura de rede 82](#_Toc216981918)

[5.7. Achado 7 – Medidas básicas de segurança cibernética insuficientes no programa de conscientização e treinamento em segurança 83](#_Toc216981919)

[5.8. Achado 8 – Medidas básicas de segurança cibernética insuficientes na gestão de provedores de serviços 84](#_Toc216981920)

[5.9. Achado 9 – Medidas básicas de segurança cibernética insuficientes na gestão de respostas a incidentes 85](#_Toc216981921)

[5.10. Avaliação dos gestores sobre a fiscalização 87](#_Toc216981922)

[6. CONSIDERAÇÕES FINAIS 88](#_Toc216981923)

[7. PROPOSTA DE ENCAMINHAMENTO 89](#_Toc216981924)

# LISTA DE ANEXOS

| **ANEXOS** | |
| --- | --- |
| **Documento nº** | **Descrição** |
| AN01 | **Ofícios de Apresentação**  (arquivo digital “*AN01 - Ofícios de Apresentação.zip*”) |
| AN02 | **Matriz de Planejamento**  (arquivo digital “AN02 - Matriz de Planejamento.pdf”) |
| AN03 | **Questionário iSegCiber, metodologia e resultado**  (arquivo digital “AN03 – Questionário iSegCiber e informações.zip”) |
| AN04 | **Evidências** (arquivo digital “AN04 – Evidências dos achados.pdf”) |
| AN05 | **Respostas aos Questionários (avaliação de medidas de segurança e comentários do gestor) e planilhas de ajustes**  (arquivo digital “*AN05 – Respostas aos questionários e ajustes.zip*”) |
| AN06 | Matriz de Achados  (arquivo digital “AN06 – Matriz de Achados.pdf”) |
| AN07 | Relatório Público  (arquivo digital “AN07 – Relatório Público.pdf”) |
| AN08 | **Informações das organizações (TSIDs, Respostas e evidências enviadas, Relatório Individual)**  *(arquivos digitais “ANXX – [ORGANIZAÇÃO].zip”)*  *\* Os anexos 08 a 43 consolidam as informações de cada organização auditada, seus TSIDs, respostas, evidências encaminhadas, comentários do gestor e relatórios individuais.* |
| AN44 | Planos de Ação  (arquivo digital “AN44 –Planos de Ação.zip”) |

# 1. RESUMO

**O que o TCE-RJ fiscalizou?**

O Tribunal de Contas do Estado do Rio de Janeiro realizou auditoria de conformidade, com contornos operacionais, para verificar a adoção de controles de segurança da informação e segurança cibernética nas organizações da Administração Pública Estadual. Trata-se da segunda fase da fiscalização em segurança da informação, motivada pelo baixo nível de maturidade das organizações no tema e pela ampliação na oferta de serviços públicos digitais.

O objeto compreendeu as medidas básicas de segurança do *framework* CIS Controls v8.1(IG1), abrangendo 29 medidas remanescentes[[1]](#footnote-2) e requisitos da ABNT NBR ISO/IEC 27001/27002. Adicionalmente, foi realizada avaliação dos planos de ação elaborados em atendimento à fase 1 (processo TCE-RJ nº 105.895-5/2024).

A auditoria abrangeu 36 organizações da Administração Pública Estadual, incluindo órgãos dos poderes Executivo, Legislativo e Judiciário, Ministério Público, Defensoria Pública e Tribunal de Contas. O período do trabalho ocorreu entre agosto e dezembro de 2025.

A metodologia combinou (i) questionário de autoavaliação, (ii) análise documental das evidências apresentadas (políticas, normas e registros técnicos), (iii) verificação do status dos prazos e metas dos planos de ação monitorados e (iv) consolidação comparativa por meio do Índice de Segurança Cibernética (iSegCiber), calculado a partir das respostas e validação de evidências, com classificação em quatro níveis de maturidade (Inexpressivo, Inicial, Intermediário e Aprimorado). Ao final, o Tribunal encaminhou relatórios individuais preliminares para contraditório e analisou as manifestações recebidas.

**O que o TCE-RJ encontrou?**

A auditoria constatou um cenário de maturidade predominantemente incipiente na segurança cibernética das organizações estaduais. O iSegCiber indicou que 63,9% dos jurisdicionados situam-se nos níveis “Inexpressivo” ou “Inicial”.

Em razão da sensibilidade das informações tratadas e visando preservar a segurança institucional, os resultados são apresentados de forma agregada e descaracterizada, sem identificação nominal das vulnerabilidades ou das manifestações de cada jurisdicionado.

A avaliação dos planos de ação elaborados em resposta à primeira fase da fiscalização demonstrou predominância de planejamento, com baixa execução. Dos 645 encaminhamentos avaliados, mais de dois terços encontram-se nas categorias “Planejados” ou “Em Andamento”, e apenas 14% como “Atendidos”. A análise dos prazos aponta que 31,4% das ações têm previsão de conclusão até o fim de 2025, mantendo-se janela de exposição a riscos no curto prazo.

Registraram-se 9 achados em 29 situações encontradas. Destacam-se: ausência de programas de conscientização em segurança da informação; baixa adoção de processos de gestão e remediação de vulnerabilidades; e insuficiência na gestão de *logs* e de inventário de provedores de serviço – situações encontradas em praticamente todas as organizações.

A análise dos comentários dos gestores revelou convergência com o diagnóstico da auditoria em 82,6% dos casos. Os gestores apontaram como principais obstáculos a escassez crítica de recursos financeiros e humanos, a obsolescência tecnológica, a dificuldade de retenção de talentos técnicos e a necessidade de conciliar a operação diária com a formalização de processos. Das 99 discordâncias apresentadas, apenas 13,1% foram acatadas, ocorrendo nos casos em que foram apresentadas evidências que comprovavam controles eficazes.

**Qual é a proposta de encaminhamento?**

Propõe-se um conjunto articulado de determinações e recomendações para induzir o fortalecimento da governança e da gestão de segurança da informação nas organizações estaduais, com foco na adoção adequada das medidas básicas identificadas como inconformes. A proposta central é a estruturação de plano de ação para implementação dessas medidas, conforme detalhamento constante dos relatórios individuais.

Para as organizações em situação crítica quanto ao cumprimento dos encaminhamentos da primeira fase da fiscalização, será expedida determinação para que ajustem seus planos de ação, assegurando tratamento explícito e adequado das medidas apontadas. Às duas organizações que não enviaram plano de ação será reiterada uma determinação de planejamento e cumprimento dos controles cibernéticos.

Propõe-se ainda recomendação transversal às organizações para que priorizem a consolidação dos controles fundamentais da primeira fase da fiscalização: a estrutura de segurança e os inventários de ativos e *softwares*, que constituem pré-requisitos para a eficácia dos demais controles.

Os benefícios esperados incluem o fortalecimento da governança, o aprimoramento na gestão de riscos cibernéticos, a elevação do nível de maturidade e da resiliência contra ataques, bem como a promoção de cultura organizacional que valorize a proteção de dados críticos do Estado e dados pessoais dos cidadãos.

**Quais os próximos passos?**

O Tribunal acompanhará a implementação por meio de monitoramento e de avaliações futuras, nos termos da Resolução TCE-RJ nº 422/2023, com foco na execução dos planos de ação registrados no SEI e na evidência de institucionalização dos processos e controles recomendados.

# 2. INTRODUÇÃO

Trata-se de auditoria de conformidade autorizada no âmbito do processo TCE-RJ nº 303.389-0/2025 que tem por objeto as práticas de governança e gestão de TI adotadas pelas organizações da Administração Pública Estadual e Municipal.

Os trabalhos foram conduzidos em conformidade com as Normas Brasileiras de Auditoria do Setor Público (NBASP) e de acordo com os padrões estabelecidos no Manual de Auditoria deste Tribunal de Contas do Estado do Rio de Janeiro (TCE-RJ).

## 2.1 Antecedentes

A presente fiscalização insere-se em um conjunto de atuações planejadas do Tribunal de Contas do Estado do Rio de Janeiro (TCE-RJ) para avaliar a maturidade da governança e gestão de TI no âmbito estadual e municipal.

Inicialmente, levantamento no processo TCE-RJ nº 105.096-3/2020 verificou aspectos chaves de governança de TI dos principais entes que fazem uso de tecnologia da informação da esfera estadual, mensurando o indicador de governança de TI (iGovTI).

Posteriormente, auditoria desta Coordenadoria (processo TCE-RJ nº 205.089-9/2023) analisou aspectos das políticas de Governança e Gestão de TI enquanto norteadores das contratações de Tecnologia da Informação no âmbito dos municípios. Nessa ocasião, as prefeituras de Maricá, Rio das Ostras, Saquarema e Volta Redonda tiveram suas práticas medidas pelo iGovTI.

Finalmente, esta CAD-TI avaliou as práticas de Governança e Gestão de TI nas organizações do Sistema Estadual de Tecnologia da Informação e Comunicação - SETIC. Naquela oportunidade, o iGovTI foi utilizado como medidor de tais práticas.

## 2.2 Objetivo e escopo

O objeto do presente trabalho são as práticas de Governança e Gestão de Tecnologia da Informação (TI) em 126 jurisdicionados estaduais e municipais do Rio de Janeiro.

O objetivo do trabalho consiste em:

• Realizar a avaliação do índice de maturidade de governança de TI (iGovTI) em todos os jurisdicionados e consolidar os resultados em relatório até julho de 2026;

• Comparar os indicadores de governança de TI levantados em 2026 com os resultados de 2023, apresentando análise detalhada da evolução até julho de 2026;

• Emitir recomendações individualizadas e consolidadas para induzir a adoção de boas práticas de gestão e governança de TI.

O escopo da auditoria abrangeu 120 (cento e vinte) organizações das Administrações Públicas Estadual e Municipal. O período de realização dos trabalhos de campo ocorreu entre fevereiro e julho de 2026.

## 2.3 Limitações

As limitações estão relacionadas com a metodologia do questionário utilizada nessa auditoria, dado que as informações são obtidas através de questionário eletrônico e, portanto, possuem caráter auto declaratório.

Para endereçar o caráter declaratório das respostas fornecidas, foi solicitado o envio de algumas das evidências que ensejaram seu preenchimento.

Ressalta-se que tais limitações não impediram o pleno atingimento do objetivo proposto deste trabalho.

## 2.4 Critérios aplicados

Os principais critérios de auditoria utilizados para a análise da conformidade incluíram os *frameworks* COBIT 2019 e ITIL 4, bem como jurisprudência desta Corte de Contas.

## 2.5 Metodologia utilizada

A metodologia empregada envolveu a elaboração e a aplicação de questionário de autoavaliação nos questionários do iGovTI do TCU dos anos de 2021 e 2024.

A partir das respostas ao Questionário calculou-se o índice iGovTI e seus diversos agregadores, possibilitando, assim, mensurar quais práticas estão sendo adotadas, e em que grau, permitindo, assim, a comparabilidade entre as organizações.

A ferramenta escolhida para enviar as perguntas aos jurisdicionados e coletar suas respostas foi o LimeSurvey, um software livre que permite a aplicação de questionários online com uma gama de funcionalidades, amplamente adotado pelo Tribunal de Contas do Estado do Rio de Janeiro em suas auditorias.

Ao final da fase de execução, buscando fortalecer o caráter dialógico da fiscalização, permitindo o esclarecimento de pontos obscuros, a correção de informações imprecisas ou inconsistentes, e o aperfeiçoamento das medidas propostas, foi encaminhado um relatório individual preliminar[[2]](#footnote-3) para cada jurisdicionado contendo os achados da auditoria, com suas situações encontradas específicas e as propostas de encaminhamento sugeridas pela Equipe, bem como as respostas ajustadas em função da análise documental, permitindo que as organizações apresentassem suas considerações sobre os apontamentos.

Assim, os comentários remetidos pelos gestores foram avaliados para consolidação do resultado da fiscalização.

Na fase de elaboração do relatório, a Equipe de Auditoria produziu o presente relatório, bem como 120 relatórios individuais, contemplando uma visão geral do iGovTI de cada organização, os achados, as situações encontradas, as propostas de encaminhamento e um plano de ação específico para cada entidade.

## 2.6 Benefícios estimados

Espera-se que esta fiscalização induza o fortalecimento da governança e da gestão de Tecnologia da informação nas organizações auditadas. Os principais benefícios estimados incluem o aprimoramento na estrutura organizacional da TI, no planejamento de TI, na gestão de serviços de TI, na gestão de recursos humanos de TI e nas contratações de TI

Além disso, a auditoria desempenha um papel fundamental na promoção de uma cultura organizacional que atribui à tecnologia da informação valor estratégico para as entidades, contribuindo diretamente para o cumprimento de suas políticas públicas.

# 3. VISÃO GERAL DO OBJETO

O uso de tecnologia da informação é capaz de impulsionar de forma significativa os resultados das organizações. A governança de TI cumpre papel fundamental para garantir que os recursos digitais tragam os melhores benefício.

Nesse sentido, a governança é responsável por garantir que as necessidades das partes interessadas sejam avaliadas para determinar objetivos empresariais equilibrados e acordados. Além disso, a governança define a direção por meio de priorizações e tomadas de decisão, monitorando o desempenho e a conformidade em relação à direção definida.

A ISO-IEC 38501:2015 estabelece o modelo de governança de TI, ilustrado na Figura 1, que apresenta as três atividades da governança: avaliar, dirigir e monitorar. Avaliar consiste em estabelecer o ambiente interno e externo e determinar como a organização é atualmente apoiada e habilitada por meio do uso de TI. Dirigir significa definir como a organização deve ser apoiada e habilitada por meio do uso adequado da TI. Por fim, monitorar é a atividade que verifica se o que foi planejado e direcionado está realmente sendo executado.

Figura 1 - Modelo de Governança de TI

![](data:image/png;base64...)

(Fonte: Adaptado de ISO-IEC 38501:2015)

## 3.1. O Papel e os Mecanismos da Governança de TI

A governança no setor público baseia-se na teoria da agência, visando reduzir a assimetria de informação entre a sociedade (o principal) e os gestores públicos (os agentes). Ela opera através de três mecanismos fundamentais:

• Liderança: Compreende práticas de integridade, competência, responsabilidade e motivação exercidas pela alta administração para assegurar a boa governança;

• Estratégia: Envolve a definição de objetivos, diretrizes e planos, além do alinhamento entre as partes interessadas para o alcance dos resultados;

• Controle: Consiste em processos estruturados para gerenciar riscos e garantir a execução eficiente, eficaz e ética das atividades.

A alta administração é a principal responsável pela governança, cabendo a ela estabelecer políticas, objetivos e conduzir a estratégia institucional. Na área de TI, o estabelecimento de um Comitê Gestor Multidisciplinar é uma prática essencial para priorizar investimentos e garantir que a TI suporte efetivamente os objetivos de negócio.

## 3.2. 2 Princípios e Responsabilidades na Governança Pública

Para assegurar a legitimidade e a eficácia, a governança deve pautar-se por princípios fundamentais, conforme estabelecido pelo Decreto Federal nº 9.203/2017 e referendado pelo Tribunal de Contas da União (TCU):

• Capacidade de resposta: Responder de forma tempestiva e inovadora às demandas da sociedade;

• Integridade: Priorizar o interesse público sobre os privados, sustentando padrões éticos;

• Confiabilidade: Minimizar incertezas e manter consistência com a missão institucional;

• Melhoria regulatória: Elaborar políticas baseadas em evidências e consultas públicas;

• Prestação de contas e responsabilidade (*Accountability*): Agentes públicos devem responder por seus atos e omissões de forma clara e transparente;

• Transparência: Disponibilizar informações sobre decisões e desempenho além do que exige a lei;

• Equidade e participação: Tratar todas as partes interessadas de forma justa e participativa.

## 3.3. Gestão de TI

A gestão é a função encarregada de planejar, construir, executar e monitorar as atividades em alinhamento com a direção estabelecida pelo órgão de governança para atingir os objetivos da organização. Enquanto a governança avalia e direciona, a gestão executa as operações diárias de tecnologia e informação.

As instâncias de gestão podem ser táticas (coordenando áreas setoriais como a TI) ou operacionais (executando processos de apoio ou finalísticos).

As funções típicas da gestão de TI incluem o gerenciamento de serviços, a segurança da informação, a gestão de riscos e a continuidade dos serviços. A gestão deve operar em um ciclo de melhoria contínua (como o modelo PDCA), garantindo a conformidade com as normas e o reporte sistemático do progresso em relação aos objetivos estratégicos.

## 3.4. Instrumentos de Integração: PETI e PDTI

A integração entre governança e gestão materializa-se em instrumentos de planejamento. O Plano Estratégico de TI (PETI) e o Plano Diretor de TI (PDTI) são os principais documentos que vinculam a alocação de recursos de tecnologia aos objetivos organizacionais.

O PDTI, aprovado pela alta administração, deve conter o inventário de necessidades, planos de metas, ações, orçamento e gestão de riscos. É através desses instrumentos que a governança exerce seu papel de direcionamento, enquanto a gestão utiliza-os como guia para a execução eficiente das soluções de TIC.

## 3.5 Modelos de governança e gestão de TI dos auditados

Os auditados deste trabalho seguem modelos distintos de governança e gestão de TI. É notório que as organizações estaduais exibam maior maturidade nessa seara em comparação àquelas municipais. Nesse sentido, destacamos a estruturação do Poder Executivo e Judiciários do Estado do Rio de Janeiro.

O Decreto Estadual nº 48.997/2024 é o normativo que define o atual modelo de gestão e governança de TI no âmbito do Poder Executivo do Estado do Rio de Janeiro.

Esse normativo estabelece que o Sistema Estadual de Tecnologia da Informação e Comunicação - SETIC é composto pelo conjunto de recursos humanos, tecnológicos e de equipamentos voltados para o estabelecimento e a implementação de políticas para a informação e a comunicação pública, organizando-se em dois níveis: Direção Geral, sob competência do PRODERJ; e nível setorial, representado pelas assessorias de informática, ou setores equivalentes, de todos os órgãos da administração direta e indireta do estado do Rio de Janeiro.

O modelo do SETIC atribuiu ao PRODERJ competências relevantes, como a coordenação e supervisão do Sistema, a normatização de aspectos de TI, a elaboração e disponibilização de atas de registro de preço para contratação de bens e serviços de TI, e a avaliação e consolidação dos planos de TI dos órgãos do nível setorial do sistema.

No Poder Judiciário, a Resolução CNJ nº 370/2021, que estabelece a Estratégia Nacional de Tecnologia da Informação e Comunicação do Poder Judiciário (ENTIC-JUD), dispõe no art. 6º que cada órgão elabore e mantenha o Plano Diretor de Tecnologia da Informação e Comunicação (PDTIC), “o qual deverá elencar as ações que estarão alinhadas ao Planejamento Estratégico Institucional, ao Planejamento Estratégico Nacional do Poder Judiciário e à Estratégia Nacional de Tecnologia da Informação e Comunicação do Poder Judiciário”.

## 3.6. Mensuração da governança e gestão da TI pelos Tribunais de Contas

Desde 2010, o TCU avalia a governança e gestão de TI na administração federal por meio do iGovTI, índice baseado nas respostas das organizações a um questionário específico sobre o tema.

Atualmente, o iGovTI compõe o iESGo, índice que aborda os temas Liderança, Estratégia, Controle, Gestão de Pessoas, Gestão de Tecnologia da Informação e da Segurança da Informação, Gestão de Contratações, Gestão Orçamentária, Sustentabilidade Ambiental, Sustentabilidade Social.

O Tribunal de Contas de Pernambuco adotou o iGovTI oficialmente através da Resolução TC nº 207 de 2023, que dispõe da apuração do índice a cada dois anos. A edição de 2025 utilizou o mesmo questionário aplicado no pelo TCU em 2021, mas com algumas adaptações para tornar algumas questões que tratam de mais de uma temática mais focadas na área de tecnologia da informação.

No Tribunal de Contas do Rio de Janeiro, as últimas mensurações do iGovTI foram nas auditorias dos processos TCE-RJ 205.089-9/2023, que teve quatro prefeituras municipais auditadas, e TCE-RJ 109.009-4/2023, que teve os órgãos estaduais do Sistema Estadual de Tecnologia da Informação e Comunicação (SETIC) como auditados. Em ambas as fiscalizações, utilizou-se o questionário de 2021 do TCU com adaptações.

No contexto do Índice de Efetividade dea Gestão Municipal (IEGM) também existe um índice chamado iGovTI. O IEGM foi concebido em 2015 pelo Tribunal de Contas do Estado de São Paulo e disponibilizado aos demais Tribunais de Contas através do Instituto Rui Barbosa (IRB). O iGovTI do IEGM é baseado em um questionário que não se confunde com aquele aplicado nos demais trabalhos supracitados.

# 4. RESULTADOS DA AUDITORIA

Devido à sensibilidade dos dados tratados e visando preservar a segurança das instituições, as informações, comentários e opiniões oferecidos pelas organizações nas fases de coleta não serão explicitados de forma nominal.

Diante disso, os dados serão apresentados de maneira agregada ou descaracterizada, focando na análise sistêmica dos problemas e nas soluções transversais para a Administração Pública, sem expor individualmente as vulnerabilidades ou manifestações de cada jurisdicionado.

## 4.1. Avaliação dos planos de ação elaborados em atendimento a fase 1 da fiscalização

A presente avaliação insere-se no monitoramento preliminar das determinações exaradas durante a primeira fase da fiscalização de segurança cibernética (Processo TCE-RJ nº 105.895-5/2024). Naquela etapa inicial, que verificou a existência de uma estrutura básica de segurança da informação e a aderência aos Controles CIS 1 a 6, o diagnóstico revelou um cenário de fragilidade sistêmica na Administração Pública estadual: 66,7% das organizações encontravam-se em níveis de maturidade Inexpressivo ou Inicial.

Em resposta a esse cenário crítico, foram expedidos até 27 encaminhamentos por organização, com a determinação expressa para a elaboração de Planos de Ação visando sanar as inconformidades descritas.

A decisão plenária contendo as determinações foi exarada em 26/05/2025, concedendo às organizações um prazo de até 60 dias para a elaboração e registro de seus respectivos planos de ação.

Visando aferir o cumprimento tempestivo dessa obrigação, a Equipe de Auditoria, solicitou aos auditados o envio dos planos consolidados em meados de setembro de 2025. Portanto, a presente avaliação considera o status e planejamento das organizações neste marco específico, momento em que o prazo regulamentar para planejamento já se encontrava expirado.

Para a aferição do atendimento dos encaminhamentos, a Equipe analisou 33 planos[[3]](#footnote-4) submetidos pelas organizações auditadas. A metodologia consistiu no confronto direto entre cada encaminhamento proposto e a respectiva resposta do gestor, classificando-as segundo sua materialidade e tempestividade:

* **Atendido / Em Andamento:** Ações concluídas e iniciadas.
* **Planejado:** Ações futuras com prazo definido (promessas de execução).
* **Resposta insuficiente quanto ao objeto:** Respostas vagas, genéricas ou condicionadas a eventos incertos (ex: "aguardando reestruturação"), sem detalhamento técnico.
* **Item não endereçado:** Omissão completa do encaminhamento no plano de ação.

A partir dessa classificação, calculou-se o grau de cobertura dos encaminhamentos (percentual de encaminhamentos propostos que foram endereçados pelo plano).

Ressalta-se que o escopo desta avaliação se limitou à análise das informações prestadas nos planos apresentados. Nesta etapa as informações não foram validadas por meio de testes pela Equipe.

### 4.1.1. Visão geral

A análise dos planos de ação encaminhados revela um cenário de alta capacidade de planejamento, porém ainda com um baixo grau de execução das ações propostas. Identificou-se que, dos 645 encaminhamentos avaliados, mais de dois terços (70,2%) encontra-se nas categorias "Planejados" ou "Em Andamento". O percentual de itens efetivamente "Atendidos" (concluídos) ainda é baixo, de apenas 14%, conforme detalhado na Figura 5.

Figura 2 – Status consolidado dos encaminhamentos

![Gráfico  O conteúdo gerado por IA pode estar incorreto.](data:image/png;base64...)

(Fonte: elaboração própria)

Dos encaminhamentos classificados como “Resposta insuficiente quanto ao objeto” observa-se uma confusão entre ferramentas e processos. Diversas organizações responderam à necessidade de se estabelecer um processo com a aquisição ou implementação de ferramentas. Ignora-se que a tecnologia sem o rito processual de formalização, fluxo e responsabilização não atende ao controle.

Ainda nessa classe, identificou-se o uso recorrente de reestruturações organizacionais ou ausência de setores formais como justificativa para não executar controles operacionais básicos, paralisando a segurança à espera de uma burocracia ideal. Também foi observada a transferência de responsabilidade para o provedor central de TI do Poder Executivo, o que mesmo quando cabível, não exime as organizações da responsabilidade de assegurar a adequada adoção das práticas apontadas.

Da análise dos itens classificados como "Item Não Endereçado", observou-se que controles técnicos essenciais não estão sendo adequadamente tratados, como os relacionados a governança da segurança (Gestão de riscos e Política de Segurança da Informação), o inventário de ativos/*software* e a utilização de autenticação multifator (MFA).

Por fim, a avaliação, apresentada na Figura 6, entre o índice de cobertura (grau de encaminhamentos propostos que foram endereçados pela organização) e o índice de atendimento aos encaminhamentos aponta para uma disparidade preocupante entre as organizações. Destaca-se o grupo dos “ágeis”, que demonstrou capacidade de resposta imediata. Em contrapartida, observa-se uma "cauda crítica" de entidades que falharam tanto em planejar quanto em executar. No meio termo encontra-se o grupo dos “latentes”, que apresenta uma capacidade de planejamento, mas cujos controles de segurança ainda não se manifestaram efetivamente no ambiente operacional.

Figura 3 – Matriz de cumprimento (Planejamento vs. Execução)

![Gráfico, Gráfico de dispersão  O conteúdo gerado por IA pode estar incorreto.](data:image/png;base64...)

(Fonte: elaboração própria)

A análise de 398 prazos válidos apresentados para os encaminhamentos pendentes de conclusão (classificados como "Em Andamento" ou "Planejados") revela uma larga janela temporal de vulnerabilidade. Os dados apontam para uma concentração de esforços apenas a partir de 2026, com uma parcela alarmante de previsão de cumprimento para o médio e longo prazo.

Da avaliação, apenas 31,4% das ações serão concluídas até o fim de 2025. A maior concentração de entregas (41,2%) está prevista para o ano de 2026 e identificou-se que 27,4% das ações foram empurradas para um horizonte distante a partir de 2027, com destaque negativo a partir do ano de 2029 (21,1% das entregas previstas).

Esse cenário implica que a Administração operará, pelos próximos 12 a 48 meses, ciente das vulnerabilidades (riscos conhecidos), mas sem os controles mitigadores ativos.

Em complemento à análise documental dos planos, a Equipe de Auditoria coletou, via questionário enviado com o TSID2, a percepção dos gestores quanto aos obstáculos enfrentados para a materialização das ações de segurança. O confronto entre a realidade verificada (baixo índice de execução) e a visão interna das organizações revela gargalos estruturais críticos.

A análise das justificativas aponta a insuficiência de Recursos Humanos (Item A2.b do questionário) como o impedimento mais severo e transversal na Administração Pública. Diversas organizações sinalizaram que sua equipe técnica é insuficiente em número ou carece da capacitação necessária para implementar os controles do CIS v8.

Relatou-se explicitamente a dificuldade em "conciliar a execução diária das medidas de segurança com o tempo necessário para formalizar os procedimentos e normas", indicando que a rotina de "apagar incêndios" impede a maturação da governança.

A forma como a alta gestão acompanha o progresso do plano de ação (Item A3) correlaciona-se com a qualidade e agilidade dos planos. Organizações que relataram que o progresso é acompanhado de forma *"interna e informal" ou “não houve acompanhamento formalmente estabelecido”* apresentam um baixo índice de cobertura e execução do plano. Em contrapartida, entidades que reportaram monitoramento formal tendem a apresentar ações mais estruturadas e consciência dos riscos.

Apesar dos atrasos, as organizações que iniciaram a execução relatam ganhos tangíveis imediatos (Item A4) na segurança da informação da organização, validando a eficácia dos controles propostos, como exemplo:

* **Mudança Cultural:** Relatou-se maior engajamento dos usuários no reporte proativo de *e-mails* suspeitos (*phishing*). Outra entidade destaca a sinergia amplificada entre os setores de serviços e aumento da maturidade dos técnicos envolvidos no projeto. Também foi apontado um aumento no engajamento dos usuários e destaque para uma postura mais proativa, gerando mais visibilidade de seu ambiente e reduzindo os riscos.
* **Controle de Ativos e *Shadow IT*:** Houve apontamento sobre o desenvolvimento de mecanismos específicos para "controlar programas instalados no parque com base em um *baseline* definido", e a consolidação da elaboração consistente de inventário de ativos e *softwares*, atacando a raiz dos problemas de *softwares* não autorizados.
* **Proteção de Identidade:** Foi destacada a mitigação de riscos de acesso não autorizado através do bloqueio automático de tela e implementação de duplo fator de autenticação.
* **Elevação Estratégica da Segurança:** Relatou-se que a formalização da governança (Criação de Comitê e aprovação da PSI) gerou o benefício intangível, porém vital, de "elevar a segurança da informação à pauta estratégica da alta gestão".

Diante do cenário de risco apresentado será proposta **DETERMINAÇÃO** às organizações auditadas em situação crítica para que ajustem seu plano de ação a fim de que as ações presentes nele tratem explicita e adequadamente dos encaminhamentos apontados no item III do Acórdão nº 12.947/2025 referente à decisão plenária do Processo TCE-RJ nº 105.895-5/2024.

Diante do não envio do plano de ação por 2 organizações em atendimento ao TSID1 será proposta **DETERMINAÇÃO** reiterando a necessidade de se planejar e avaliar as medidas suficientes para cumprimento dos controles cibernéticos apontados no Processo TCE-RJ nº 105.895-5/2024.

## 4.2. Índice de segurança cibernética básica (iSegCiber)

A avaliação da maturidade em segurança da informação, realizada junto a 36 organizações jurisdicionadas, revela um cenário predominantemente incipiente e marcado por fragilidades estruturais. A análise do Índice de Segurança Cibernética Básica (iSegCiber) demonstra uma concentração de organizações com avaliações baixas, evidenciando que a estratégia de segurança vigente na maioria dos entes é reativa e carece de processos formalizados.

A distribuição de frequência das notas (Figura 9) apresenta uma curva deslocada para a esquerda, o que denota uma maior densidade de organizações nas faixas de pontuação inferior (entre 0,10 e 0,40).

Figura 4 – Histograma apresentando a distribuição das notas do índice iSegCiber

![](data:image/png;base64...)

(Fonte: elaboração própria)

Ao classificar os índices calculados nos níveis de maturidade estabelecidos pela metodologia, confirma-se o diagnóstico de vulnerabilidade: 63,9% das organizações (23 de 36) situam-se nos estratos inferiores (“Inexpressivo” ou “Inicial”). Apenas uma organização auditada (2,8%) atingiu o nível “Aprimorado”, conforme detalhado na Figura 8.

Figura 5 - Níveis de maturidade das organizações às medidas básicas de segurança cibernética

![Gráfico, Gráfico de barras  O conteúdo gerado por IA pode estar incorreto.](data:image/png;base64...)

(Fonte: elaboração própria)

A falta de homogeneidade na aplicação dos controles é visível no mapa de calor abaixo (Figura 9). Observa-se uma predominância de tonalidades quentes (vermelho e laranja), indicando baixa aderência na maioria dos requisitos avaliados, salvo exceções pontuais em controles específicos.

Figura 6 - Matriz de calor evidenciando a concentração de organizações (eixo Y) com baixos níveis de implementação na maioria dos controles (eixo X)

![Gráfico de mapa de árvore  O conteúdo gerado por IA pode estar incorreto.](data:image/png;base64...)

(Fonte: elaboração própria)

Em síntese, a média global de aderência situa-se abaixo de 0,40, denotando que os requisitos essenciais de segurança são atendidos, em média, de forma parcial e não estruturada.

### 4.2.1. Controles com maior aderência

A análise setorizada aponta que os controles com melhores índices de desempenho são aqueles frequentemente associados a soluções tecnológicas de mercado (“*commodities*” de segurança) ou necessidades operacionais básicas. O gráfico abaixo destaca os controles que atingiram os maiores percentuais de classificação nos níveis “Largamente Atingido” ou “Plenamente Atingido”.

Figura 7 - Percentual de organizações que atingiram níveis satisfatórios de conformidade (“Largamente” ou “Plenamente”) por controle

![Gráfico, Gráfico de dispersão  O conteúdo gerado por IA pode estar incorreto.](data:image/png;base64...)

(Fonte: elaboração própria)

Destacam-se neste grupo:

* **Controle 09 – Proteções de *e-mail* e navegador (Nota média: 0,46)**: Apresenta o maior índice de sucesso relativo, com 61,1% das organizações situadas nos níveis superiores de maturidade. O desempenho sugere que as organizações se beneficiam de camadas de segurança nativas providas por serviços de correio eletrônico e navegação contratados, garantindo uma proteção perimetral mínima.
* **Controle 10 – Defesas contra *malware* (Nota média: 0,59)**: Apresenta a segunda melhor adoção de controles, com 58,3% das organizações situadas nos níveis superiores de maturidade. Este resultado sugere que a aquisição de ferramentas de antivírus/*antimalware* é uma das medidas de segurança mais disseminada.
* **Controle 05 – Gestão de contas (Nota média: 0,49)**: A posição de destaque deste controle reflete a necessidade operacional básica de criação e manutenção de credenciais de acesso. Contudo, a aderência é predominantemente “Parcial” ou “Larga”, indicando que, embora as contas sejam criadas, processos de revisão e revogação podem não estar totalmente maduros.

### 4.2.2. Maiores riscos

Os controles com desempenho crítico revelam lacunas severas na gestão de ativos, infraestrutura e proteção da informação. O gráfico de barras empilhadas a seguir detalha a composição dos níveis de aderência, evidenciando a predominância das classificações “Não Atingido” (vermelho) e “Parcialmente Atingido” (laranja) nestes quesitos.

Figura 8 - Distribuição detalhada dos níveis de aderência por controle

![Gráfico, Gráfico de barras  O conteúdo gerado por IA pode estar incorreto.](data:image/png;base64...)

(Fonte: elaboração própria)

A análise detalhada destes *gaps* aponta riscos iminentes:

* **Controle 03 – Proteção de dados (Nota média: 0,21)**: Identificado como a maior vulnerabilidade do escopo auditado. Observa-se que 91,7% das organizações não atingiram níveis satisfatórios de implementação. A ausência de processos robustos de identificação e classificação de dados torna ineficazes medidas avançadas de proteção, expondo os entes a riscos elevados de desconformidade com a LGPD e vazamento de informações sensíveis.
* **Controle 12 – Gestão da infraestrutura de rede (Nota média: 0,25)**: Com aproximadamente 83,4% das organizações em níveis críticos, constata-se deficiência na manutenção adequada dos ativos de rede, comprometendo a resiliência a vulnerabilidades conhecidas.
* **Controle 6 – Gestão do controle de acesso (Nota média: 0,32)**: Também com 83,4% das organizações em níveis insuficientes (abaixo do “Intermediário”), constatam-se problemas no controle de acesso das organizações, com medidas insuficientes para concessão e revogação de acesso, bem como a utilização de MFA para acesso às aplicações da organização.
* **Controle 8 – Gestão de *logs* (registros de auditoria) (Nota média: 0,27)**: Ainda com 83,4% das organizações em níveis insuficientes (abaixo do “Intermediário”), verificam-se deficiências na definição de um processo de gestão de logs, com consequente coleta dos registros e armazenamento adequado.

### 4.2.3 Análise de Dados

A análise estatística da correlação dos dados coletados permitiu identificar dependências lógicas que explicam a baixa maturidade geral. Destacam-se os seguintes achados analíticos:

* **A importância do controle estruturante**: O Controle 00 (Estrutura em Segurança da Informação) possui a maior correlação com o índice geral de segurança (iSegCiber). Isso demonstra que o estabelecimento formal de comitês, políticas e normas é o maior preditor de sucesso para a implementação dos demais controles técnicos. Organizações sem governança formal tendem a ter desempenho técnico inferior em todas as outras áreas.
* **Inconsistência na ordem de implementação**: Observou-se que controles mais operacionais (Controles 09 e 10) possuem notas superiores a controles de base, como Inventário de Ativos (Controle 01 e 02) e Proteção de Dados (Controle 03). Essa inversão sugere um investimento em ferramentas pontuais sem a consolidação dos fundamentos de segurança, reduzindo a eficácia do gasto público em tecnologia.

A avaliação conclui que o ambiente auditado opera sob risco cibernético, caracterizado pela falta de visibilidade sobre os próprios ativos e dados. A estratégia de segurança vigente aparenta ser reativa e dependente de ferramentas isoladas, carecendo de uma abordagem baseada em riscos e processos integrados.

É primordial que as ações de remediação sejam priorizadas pelo fortalecimento da Higiene Cibernética Básica com ênfase em estabelecer e manter uma estrutura de segurança (Controle 00), a fim de institucionalizar a segurança da informação para assegurar a autoridade e recursos necessários, e em mapear os ativos e dados da organização (Controles 01, 02 e 03), com objetivo de aumentar o grau de aderência desses controles que são pré-requisitos obrigatórios para a eficácia de quaisquer outros controles de proteção ou recuperação.

Diante disso, será sugerida proposta de **RECOMENDAÇÃO** às organizações para que, no âmbito da fase 1 da fiscalização (qual seja Processo TCE-RJ nº 105.895-5/2024), priorizem a consolidação dos controles fundamentais para mitigação dos riscos cibernéticos: o Controle 0 de Estrutura de Segurança e os Controles 1 e 2 de Inventário de Ativos e *Softwares*, uma vez que estes constituem pré-requisitos estruturais para a eficácia e efetividade dos demais controles de proteção.

### 4.2.4 Desafios e Deficiências em Segurança da Informação

Com base nas declarações prestadas pelos gestores na seção de encerramento do questionário eletrônico enviado mediante TSID2, coletou-se subsídios fundamentais para a compreensão das possíveis causas raízes das lacunas de conformidade identificadas.

Predomina nas respostas a escassez crítica de recursos financeiros e humanos, resultando em obsolescência tecnológica, ausência de ferramentas de segurança corporativas e dificuldade na retenção de talentos técnicos. Esse cenário impõe às equipes de TI um modelo operacional eminentemente reativo, focado na continuidade do serviço em detrimento da formalização de processos e da gestão proativa de riscos.

Adicionalmente, barreiras culturais, como a baixa conscientização dos usuários, e a complexidade operacional em ambientes com grande dispersão geográfica e volume massivo de usuários dificultam a padronização dos controles e o alinhamento com normativos estaduais. Depreende-se que as deficiências de conformidade não provêm apenas de falhas gerenciais, mas de um déficit estrutural de capacidade de execução.

A superação dessas vulnerabilidades exige que a segurança da informação transcenda a esfera técnica, consolidando-se como pilar de governança corporativa com garantia de recursos e patrocínio efetivo da Alta Administração para a transição de uma postura reativa para um modelo de gestão de riscos formalizado e auditável.

## 4.3. Achados de Auditoria

O *Center for Internet Security* (CIS) define as medidas de segurança do Grupo de Implementação 1 (IG1) como a “Higiene Cibernética Essencial”. Este referencial constitui o padrão técnico mínimo de segurança que deve ser adotado por qualquer organização para garantir a confidencialidade, integridade e disponibilidade das informações.

Sob esse prisma, a Equipe de Auditoria considera que a adoção dessas salvaguardas básicas é condição indispensável para o atendimento aos deveres legais de segurança impostos à Administração Pública.

A falha em implementar esse nível mínimo de proteção configura, por consequência, inobservância aos requisitos estabelecidos nos incisos II e III do art. 6º da Lei de Acesso à Informação (Lei nº 12.527/2011) e nos deveres de segurança e prevenção previstos no inciso VII do art. 6º e nos arts. 46 e 47 da Lei Geral de Proteção de Dados Pessoais (Lei nº 13.709/2018).

Nesse contexto, os exames e procedimentos aplicados revelaram fragilidades nos controles das organizações auditadas. As situações encontradas, detalhadas nos achados a seguir, evidenciam lacunas na aplicação dessas medidas essenciais, expondo as informações custodiadas a riscos operacionais e legais.

### 4.3.1 Achado 1 – Medidas básicas de segurança cibernética insuficientes na gestão de vulnerabilidades

#### 4.3.1.1. Critérios

* Lei Federal nº 12.527/2011 (LAI), art. 6º, incisos II e III (Dever da Administração de proteger a confidencialidade, integridade e disponibilidade das informações sob sua custódia);
* Lei Federal nº 13.709/2018 (LGPD), art. 6º, inciso VII, art. 46 e art. 47 (Dever da Administração de atender ao princípio da segurança nas atividades de tratamento de dados pessoais, por meio da utilização de medidas técnicas e administrativas na proteção dos dados);
* Controles CIS versão 8.1, medidas de segurança 7.1 (Estabelecer e manter um processo de gestão de vulnerabilidade), 7.2 (Estabelecer e manter um processo de remediação), 7.3 (Executar a gestão automatizada de *patches* do sistema operacional) e 7.4 (Executar a gestão automatizada de *patches* de aplicações);
* Norma Técnica ABNT NBR ISO/IEC 27002:2022, item 8.8 (Gestão de vulnerabilidades).

#### 4.3.1.2. Evidências

As evidências que embasam este achado estão consolidadas no Anexo AN04 e encontram-se individualizadas em cada um dos relatórios individuais (AN08 a AN43) das organizações auditadas.

#### 4.3.1.3. Situação encontrada

A gestão contínua de vulnerabilidades é um processo essencial para a segurança da informação, permitindo que a organização identifique, priorize e corrija falhas de segurança em seus ativos antes que elas sejam exploradas por agentes maliciosos. A ausência ou a ineficiência desse processo amplia significativamente a superfície de ataque e o risco de comprometimento da confidencialidade, integridade e disponibilidade dos dados e serviços.

O ciclo de vida da gestão de vulnerabilidades compreende, fundamentalmente, as etapas de avaliação (*assess*), priorização (*prioritize*), remediação (*remediate*) e monitoramento (*monitor*). Para operacionalizar esse ciclo, é imprescindível que a organização utilize fontes fidedignas de inteligência de ameaças e mantenha processos formalizados e ferramentas adequadas para varredura e correção.

A legislação vigente, notadamente o art. 6º, incisos II e III, da Lei de Acesso à Informação (LAI) e os artigos 46 e 47 da Lei Geral de Proteção de Dados (LGPD), impõem à Administração o dever de implementar medidas técnicas de segurança aptas a proteger as informações sob sua custódia.

No contexto da gestão de vulnerabilidades, o cumprimento desses requisitos legais materializa-se na adoção de práticas consagradas, como o item 8.8 da ABNT NBR ISO/IEC 27002:2022[[4]](#footnote-5) e as medidas de higiene cibernética do Controle 07 dos Controles CIS v8.1[[5]](#footnote-6).

O tema já foi incorporado, sob diferentes aspectos, a normativos e diretrizes governamentais específicos. O Programa de Privacidade e Segurança da Informação (PPSI) do Governo Federal, por exemplo, disponibiliza o Guia de Gerenciamento de Vulnerabilidades[[6]](#footnote-7), que orienta a adoção dessas medidas no âmbito do Poder Executivo Federal.

Para assegurar uma gestão eficaz e conforme, a organização deve adotar, minimamente, as medidas básicas (de higiene cibernética) do Controle 07 dos Controles CIS versão 8.1: (1) o estabelecimento de um processo formal de gestão de vulnerabilidades, (2) a definição de um processo de remediação baseado em riscos, (3) a execução automatizada de atualizações (*patches*) em sistemas operacionais e (4) a execução automatizada de atualizações em aplicações.

Com base na análise dos itens 0701, 0702, 0703 e 0704 do questionário aplicado, da avaliação dos documentos encaminhados e dos comentários do gestor, a Equipe de Auditoria constatou as seguintes deficiências nas organizações auditadas:

Figura 9 – Distribuição das situações da gestão de vulnerabilidades

![Gráfico, Gráfico de barras  O conteúdo gerado por IA pode estar incorreto.](data:image/png;base64...)

(Fonte: elaboração própria)

Essas situações ensejaram o presente achado e serão detalhadas nas seções subsequentes.

##### Processo de gestão de vulnerabilidade

A governança eficaz exige que a organização possua um processo formal, documentado e padronizado para gerir o ciclo de vida das vulnerabilidades.

A Medida 7.1 dos Controles CIS v8.1 requer a documentação desse processo, incluindo revisões anuais ou, quando houver, mudanças significativas no ambiente.

Em complemento, o item 8.8 da ABNT NBR ISO/IEC 27002:2022 dispõe que a organização deve definir e estabelecer responsabilidades claras para a gestão de vulnerabilidades técnicas, abrangendo desde o monitoramento e a avaliação de riscos até a correção e o rastreamento dos ativos.

Para garantir a efetividade do controle, e em consonância com o *Vulnerability Management Policy Template*[[7]](#footnote-8) do CIS, o processo deve definir claramente o escopo (quais ativos corporativos são aplicáveis), estabelecer os papéis envolvidos e detalhar as etapas de identificação, priorização, remediação e monitoramento. É imprescindível, ainda, que o processo formalize a monitoria constante de fontes de informação sobre novas ameaças e anúncios de vulnerabilidades aplicáveis ao inventário da organização.

Da análise das respostas ao item 0701 do questionário submetido pelo TSID02, a documentação remetida como anexo à resposta e os comentários do gestor, conforme ilustrado na Figura 12, verificou-se que 31 (86,1%) das 36 organizações auditadas não estabelecem e mantêm adequadamente um processo de gestão de vulnerabilidades.

Diante disso, será sugerida proposta de recomendação às organizações nessa situação para que estabeleçam, mantenham e revisem periodicamente seu processo de gestão de vulnerabilidades.

##### Processo de remediação de vulnerabilidade

Identificar vulnerabilidades é apenas a primeira etapa do processo. Uma vez identificadas é crucial remediá-las de forma tempestiva e priorizada.

A Medida 7.2 dos Controles CIS v8.1 exige o estabelecimento de uma estratégia de remediação baseada em riscos, com revisões mensais ou mais frequentes.

O processo deve incluir critérios claros para priorização (como a criticidade do ativo e a severidade da falha), procedimentos para tratamento de exceções (quando a correção não é viável) e mecanismos de escalonamento para a alta gestão em caso de não mitigação nos prazos definidos.

Da análise das respostas ao item 0702 do questionário submetido pelo TSID02, a documentação remetida como anexo à resposta e os comentários do gestor, conforme ilustrado na Figura 12, verificou-se que 35 (97,2%) das 36 organizações auditadas não estabelecem e mantêm um processo adequado de remediação de vulnerabilidades.

Diante disso, será sugerida proposta de recomendação às organizações nessa situação para que estabeleçam, mantenham e revisem periodicamente um processo de remediação de vulnerabilidades baseado em riscos.

##### Gestão automatizada de *patches* do sistema operacional e de aplicações

A aplicação de correções de segurança (*patches*) é a medida técnica mais direta para mitigar vulnerabilidades conhecidas. Dada a complexidade e a volumetria dos ambientes modernos, a automação é indispensável para garantir a consistência e a celeridade necessárias.

As Medidas 7.3 e 7.4 dos Controles CIS v8.1 determinam a execução automatizada de atualizações em sistemas operacionais e aplicações, respectivamente, com periodicidade mínima mensal. Em consonância com o *Vulnerability Management Policy Template* do CIS, o processo deve contemplar a verificação de sucesso da instalação para garantir a efetividade da correção. Adicionalmente, para assegurar a continuidade operacional, recomenda-se a realização de testes prévios em ambientes de homologação antes da distribuição em larga escala, visando mitigar riscos de instabilidade no ambiente de produção.

Da análise das respostas aos itens 0703 e 0704 do questionário submetido pelo TSID02, a documentação remetida como anexo à resposta e os comentários do gestor, conforme ilustrado na Figura 12, verificou-se que 23 (63,9%) das 36 organizações auditadas não executam uma gestão automatizada de *patches* em sistemas operacionais e 28 (77,8%) delas não fazem em aplicações.

Diante disso, será sugerida proposta de recomendação às organizações nessa situação para que implementem a gestão automatizada de *patches* para sistemas operacionais e aplicações, assegurando periodicidade adequada e validação das correções.

##### Conclusão

Com base nas situações avaliadas, verificou-se que nenhuma das organizações auditadas possuem medidas suficientes para realizar uma gestão contínua de vulnerabilidades.

Figura 10 – Quantitativo de organizações contidas no achado 1

![Gráfico  O conteúdo gerado por IA pode estar incorreto.](data:image/png;base64...)

(Fonte: elaboração própria)

As fragilidades identificadas nesse achado comprometem a postura de segurança da organização, facilitando a exploração de falhas conhecidas por atacantes.

Diante das situações apresentadas, serão sugeridas propostas de encaminhamento às organizações para que promovam a adequação de seus controles, alinhando-se às práticas da ABNT NBR ISO/IEC 27002:2022 e do CIS Controls v8.1.

#### 4.3.1.4. Causas

* Não investigadas.

#### 4.3.1.5. Efeitos

* Maior exposição ao risco nos ativos: Aumento significativo da probabilidade de ativos corporativos serem comprometidos, pois atacantes exploram ativamente as vulnerabilidades conhecidas para obter acesso;
* Possível perda ou exposição de dados: Risco de infecção por *malware* ou acesso não autorizado que pode resultar na leitura, modificação ou destruição de dados sensíveis da organização;
* Potencial interrupção de serviços: Paralisação de operações e serviços essenciais devido a ataques bem-sucedidos (como *ransomware*) que exploram falhas de segurança não corrigidas, resultando em perdas financeiras e de reputação.

#### 4.3.1.6. Propostas de Encaminhamento

Ressalta-se que as propostas de encaminhamento individualizadas para cada organização auditada constam no bojo dos relatórios individuais presentes nos conjuntos de anexos AN08 a AN43. Dessa forma, seguem as sugestões gerais propostas pela Equipe de Auditoria:

* **Comunicação com Recomendação** às organizações que não possuem um processo estabelecido de gestão de vulnerabilidades para que adotem integralmente a medida de segurança 7.1 (Estabelecer e manter um processo de gestão de vulnerabilidade) prevista nos Controles CIS v8.1, atentando-se, minimamente, em estabelecer, manter e revisar, com frequência mínima anual, um processo de gestão de vulnerabilidades que seja documentado, aprovado, definindo o escopo, as etapas, as responsabilidades e os papéis;
* **Comunicação com Recomendação** às organizações que não possuem um processo estabelecido de remediação de vulnerabilidades para que adote integralmente a medida de segurança 7.2 (Estabelecer e manter um processo de remediação) prevista nos Controles CIS v8.1, atentando-se, minimamente, em estabelecer e manter um processo documentado de remediação de vulnerabilidades, alinhado ou parte do processo de gestão de vulnerabilidades e que defina uma estratégia de remediação baseada em risco, a qual deve ser revisada com frequência mínima mensal;
* **Comunicação com Recomendação** às organizações que não executam gestão automatizada de gestão de patches em sistemas operacionais para que adotem integralmente a medida de segurança 7.3 (Executar a gestão automatizada de patches do sistema operacional) prevista nos Controles CIS v8.1, atentando-se, minimamente, em assegurar a aplicação automatizada de atualizações nos sistemas operacionais dos ativos corporativos, com frequência mínima mensal;
* **Comunicação com Recomendação** às organizações que não executam gestão automatizada de gestão de patches em aplicações para que adotem integralmente a medida de segurança 7.4 (Executar a gestão automatizada de patches de aplicações) prevista nos Controles CIS v8.1, atentando-se, minimamente, em assegurar a aplicação automatizada de atualizações nas aplicações dos ativos corporativos, com frequência mínima mensal;

# 5. COMENTÁRIOS DO GESTOR E ANÁLISE DA EQUIPE

Visando fortalecer o caráter dialógico da fiscalização e assegurar o contraditório, foram encaminhados[[8]](#footnote-9) relatórios individuais preliminares para cada organização auditada. Ao final do prazo, foram recebidas 27 respostas (77% dos 35 relatórios enviados). Considerando que o escopo da auditoria abrangeu a verificação de 29 situações inconformes distintas (agrupadas em 9 achados), o somatório das manifestações resultou em um universo de aproximadamente 570 avaliações individuais processadas pela Equipe.

Essa etapa permitiu o esclarecimento de pontos obscuros, a correção de informações imprecisas ou inconsistentes e o aperfeiçoamento das medidas propostas.

O panorama geral das respostas revela alta convergência entre o diagnóstico da auditoria e a visão dos gestores. Conforme ilustrado na Figura 30, em aproximadamente 82,6% dos casos, os auditados reconheceram as fragilidades apontadas.

Figura 27 – Cenário das manifestações dos gestores quanto às situações encontradas apontadas no Relatório Individual Preliminar

![Gráfico, Gráfico de barras, Gráfico de cascata  O conteúdo gerado por IA pode estar incorreto.](data:image/png;base64...)

(Fonte: elaboração própria)

A predominância de concordâncias ratifica a materialidade dos achados, indicando que o levantamento reflete a realidade das organizações e que a atuação da auditoria já motivou o início do atendimento às propostas, demonstrando o benefício imediato do controle e evidenciando a oportunidade e a necessidade da atuação deste Tribunal para induzir melhorias.

No que tange às 99 sinalizações de discordância (17,4% do total), a Equipe empreendeu uma revisão técnica minuciosa. O procedimento consistiu no confronto entre as justificativas e evidências apresentadas nos comentários dos gestores e o conjunto probatório coletado durante a fase de execução.

O objetivo foi verificar se os argumentos trazidos eram suficientes para elidir a irregularidade ou justificar a situação encontrada. O resultado dessa reanálise encontra-se consolidado na Figura 31.

Figura 28 – Resultado da análise técnica das discordâncias apresentadas

![Tabela  O conteúdo gerado por IA pode estar incorreto.](data:image/png;base64...)

(Fonte: elaboração própria)

Apenas 13,13% das discordâncias foram acatadas (total ou parcialmente), ocorrendo nos casos em que foram apresentadas novas evidências que comprovavam a regularidade da situação ou a existência de controles compensatórios eficazes.

Nas subseções a seguir, apresenta-se uma visão detalhada da avaliação dos comentários dos gestores segregada por cada um dos achados de auditoria, apresentando os principais comentários e justificativas.

## 5.1. Achado 1 - Medidas básicas de segurança cibernética insuficientes na gestão de vulnerabilidades

Este achado trata da avaliação da maturidade das organizações quanto ao estabelecimento de processos formais para identificar, remediar e corrigir vulnerabilidades em seus ativos de TIC. A Figura 32 consolida as manifestações.

Figura 29 - Comentários dos gestores sobre as situações encontradas do Achado 1

![Gráfico, Gráfico de barras  O conteúdo gerado por IA pode estar incorreto.](data:image/png;base64...)

(Fonte: elaboração própria)

A maioria das organizações reconhece a fragilidade em seus processos de gestão de vulnerabilidades, citando limitações orçamentárias e sistemas legados como barreiras para a correção. Na análise das discordâncias (Figura 33), a equipe rejeitou 100% dos argumentos. Constatou-se que a mera existência de ferramentas (antivírus, *firewalls*) não substitui um processo formal de gestão de vulnerabilidades com análise de risco e SLAs definidos. Ferramentas inadequadas para a finalidade, como repositórios de código, também foram citadas erroneamente como soluções de gestão de *patches*.

Figura 30 - Resultado da análise das discordâncias do Achado 1

![Tabela  O conteúdo gerado por IA pode estar incorreto.](data:image/png;base64...)

(Fonte: elaboração própria)

Conclui-se, portanto, pela manutenção integral dos apontamentos deste achado. Embora seja positivo que diversas organizações tenham informado o início de planos de ação para 2026, a contratação de consultorias para adequação à ISO 27001 e a busca por novas soluções de *Unified Endpoint Management* (UEM), a realidade atual permanece de alto risco. A ausência de formalização dos processos e a dependência de execuções manuais ou "empíricas" deixam a administração pública exposta a ameaças cibernéticas conhecidas.

## 5.10. Avaliação dos gestores sobre a fiscalização

Como parte do processo de melhoria contínua do controle externo, foi solicitado aos gestores que avaliassem a qualidade e a condução da fiscalização. Os resultados demonstram uma ampla aprovação da metodologia adotada. Houve unanimidade quanto à clareza do escopo e ao profissionalismo da equipe de auditoria. A relevância do trabalho foi reconhecida pela quase totalidade dos gestores, que destacaram o valor agregado à segurança do setor e demandaram fortemente (77%) por capacitação e materiais orientativos, reforçando um caráter pedagógico do controle externo.

Figura 47 - Avaliação dos gestores quanto à qualidade e condução da fiscalização

![Gráfico, Gráfico de barras  O conteúdo gerado por IA pode estar incorreto.](data:image/png;base64...)

(Fonte: elaboração própria)

Apesar dos resultados positivos (vide Figura 50), foram apontadas oportunidades de melhoria, principalmente quanto à exiguidade dos prazos para resposta e envio de evidências (objeto de 5 discordâncias). Também foram registradas observações sobre a necessidade de calibrar as exigências à realidade estrutural de órgãos menores e de maior clareza na solicitação de evidências técnicas específicas. Tais *feedbacks* serão incorporados ao planejamento de futuras fiscalizações, visando aprimorar o equilíbrio entre rigor técnico e viabilidade operacional.

# 6. CONSIDERAÇÕES FINAIS

A presente fiscalização verificou a adoção de controles e medidas de segurança alinhadas às boas práticas de segurança da informação pelos órgãos e entidades da Administração Pública do Estado do Rio de Janeiro, tendo como referência as normas ABNT NBR ISO/IEC 27001:2022 e 27002:2022, bem como as medidas básicas do Grupo de Implementação 1 (IG1) dos Controles 7 a 17 do *framework* Controles CIS versão 8.1.

Adicionalmente, foram analisados os planos de ação oriundos dos encaminhamentos da primeira fase da auditoria (Processo TCE-RJ nº 105.895-5/2024).

A adoção das medidas supracitadas é imprescindível para o cumprimento de normativos estaduais — como a Instrução Normativa PRODERJ/PRE nº 07/2025 e a Resolução TJ/OE nº 28/2022 — e para assegurar a proteção das informações custodiadas e dos dados pessoais, em conformidade com os incisos II e III, do art. 6º, da Lei de Acesso à Informação (LAI) e com os arts. 46 e 47 da Lei Geral de Proteção de Dados Pessoais (LGPD).

Em linhas gerais, a fiscalização aponta um cenário de maturidade incipiente. Verificou-se que 23 dos 36 jurisdicionados (63,9%) se encontram nos níveis de maturidade "Inexpressivo" ou "Inicial". Dentre as fragilidades identificadas nesta segunda fase, destacam-se a ausência de programas de conscientização em segurança, a baixa adoção de processos de remediação de vulnerabilidades, a gestão insuficiente de *logs* de auditoria e de inventários de provedores de serviço.

Quanto à avaliação dos planos de ação da primeira fase, a análise indicou um descompasso entre a capacidade de planejamento e a efetiva execução, a existência de uma janela de vulnerabilidades e a existência de planos que não atendem aos encaminhamentos propostos.

A etapa de comentários do gestor revelou alta convergência (82,6%) entre o diagnóstico da auditoria e a visão dos gestores. Os principais entraves citados à adoção das medidas foram restrições orçamentárias, escassez de pessoal e obsolescência tecnológica.

Para alcançar mais efetividade à fiscalização e acelerar o processo de adequação às práticas de segurança, a Equipe, exercendo seu papel orientativo, desenvolveu relatórios individualizados aos jurisdicionados, com encaminhamentos específicos às suas situações. Nesse sentido, foram propostas até 27 medidas específicas por auditado, desenhadas para mitigar as lacunas identificadas em cada realidade organizacional.

Dessa forma, contata-se o caráter indutor e orientador desta auditoria que, em conjunto com as determinações e recomendações comunicadas, ensejará uma melhora significativa na higiene cibernética e no fortalecimento da governança de segurança das organizações fiscalizadas.

# 7. PROPOSTA DE ENCAMINHAMENTO

**CONSIDERANDO** o pleno atendimento ao objetivo proposto pela auditoria, qual seja, o de verificar a adoção de controles e sua aderência às boas práticas de segurança da informação;

**CONSIDERANDO** que o foco do presente trabalho é induzir os jurisdicionados a uma maior adoção de medidas de higiene cibernética;

**CONSIDERANDO** que a higiene cibernética não se esgota nos controles abordados nessa auditoria, e que deve ser encarada como um processo de melhoria contínua, norteado por um sistema de segurança da informação centrado na gestão de riscos e no uso de boas práticas consolidadas;

**CONSIDERANDO** o caráter orientador e dialógico do presente trabalho, assim como o alinhamento à diretriz de incremento de eficiência e efetividade na gestão administrativa;

**CONSIDERANDO** as informações sensíveis à segurança de informação dos jurisdicionados presentes nos autos do processo;

**CONSIDERANDO** que os resultados decorrentes das ações previstas no Plano de Ação poderão ser objeto de avaliação futura por meio de Monitoramento, considerando os preceitos definidos na Resolução TCE-RJ nº 422/2023;

**CONSIDERANDO** que a metodologia empregada neste trabalho não abordou as causas específicas dos problemas identificados e que as recomendações focam na implementação de medidas estabelecidas pelos controles CIS e pelas normas ABNT, conforme observado durante o processo de auditoria.

Sugere-se ao Egrégio Plenário desta Corte de Contas a adoção das seguintes propostas:

1. **MANUTENÇÃO DO CARÁTER SIGILOSO** do presente processo, classificando-o como informação reservada, nos termos do inciso I, § 3º, art. 8º c/c incisos IV, V, VIII do art. 9º da Resolução TCE-RJ nº 433/2023, pelo caráter sensível das análises e informações que constam no relatório e seus anexos;
2. **COMUNICAÇÃO COM DETERMINAÇÃO** à Secretaria Geral da Presidência, por meio da sua coordenadoria competente, para que adote as medidas necessárias para **CLASSIFICAR COMO INFORMAÇÃO PÚBLICA** o anexo AN07 nos termos do art. 4º c/c § 1º, do art. 8º, da Resolução TCE-RJ nº 433/2023, para conferir informação ao público geral sobre a natureza da fiscalização empreendida;
3. **COMUNICAÇÃO COM DETERMINAÇÃO** à Secretaria Geral da Presidência, por meio da sua coordenadoria competente, para que encaminhe, em anexo aos ofícios de comunicação da decisão, cópia do Acórdão proferido e dos respectivos relatórios individuais (AN08 a AN43) a cada organização auditada, de forma a garantir a ciência efetiva aos jurisdicionados acerca da decisão proferida por esta Corte, **tendo em vista o caráter sigiloso do processo, em que cada jurisdicionado só deve ter acesso ao seu relatório individual**;
4. **COMUNICAÇÃO  COM DETERMINAÇÃO** aos órgãos fiscalizados nesta auditoria, nos termos do artigo 15, inciso I, do Regimento Interno deste Tribunal, para que **promovam a atualização do plano de ação estruturado na fase anterior da fiscalização (Fiscalização nº 49/2024 acostada sob o Processo TCE-RJ nº 105.895-5/24), no prazo máximo de 60 (sessenta) dias a contar da ciência da decisão plenária**, formalizando essa atualização do plano em processo administrativo eletrônico para futuro monitoramento, e incorporando as medidas necessárias para que cumpram as **DETERMINAÇÕES** e considerem a adoção das **RECOMENDAÇÕES** dispostas nos seus respectivos **RELATÓRIOS INDIVIDUAIS anexos (AN08 a AN43)**, alertando-os de que o não atendimento injustificado os sujeita às sanções previstas no art. 63 da Lei Complementar Estadual n.º 63/1990, sendo desnecessário o encaminhamento de comprovação ou esclarecimentos nos autos deste processo, já que a verificação quanto ao atendimento poderá ser realizada em auditoria futura desta Corte de Contas.

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| **Plano de Ação** | | | | |
| **Determinação / Recomendação** | **O que fazer** | **Como fazer** | **Quem vai fazer** | **Quando fazer** |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

1. **COMUNICAÇÃO às Unidades de Controle Interno dos órgãos jurisdicionados desta fiscalização,** nos termos do artigo 15, inciso I, do Regimento Interno deste Tribunal, para que tomem **CIÊNCIA** do inteiro teor do presente Relatório de Auditoria Governamental, bem como do respectivo Relatório Individual de seu órgão (AN08 a AN43), e acompanhem a elaboração e execução do plano de ação desenvolvido a fim de assegurar seu efetivo cumprimento;
2. **ARQUIVAMENTO** do presente processo.

O presente relatório foi objeto de supervisão conforme as disposições da Portaria SGE n° 05/2019, no Manual de Auditoria Governamental do TCE-RJ, aprovado pela Resolução nº 373, de 16/06/21 e em material armazenado nos assentamentos internos desta Coordenadoria, estando, portanto, **APROVADO** por esta supervisão e encaminhado à sua apreciação para adoção das medidas cabíveis.

**CAD-TI, 03/06/2026**

|  |  |  |
| --- | --- | --- |
| **AUGUSTO CÉSAR BENVENUTO DE ALMEIDA**  **Matrícula 02/004823** | Auditor de Controle Externo | Equipe de Auditoria |
| **JOÃO PAULO DE FREITAS RAMIREZ**  **Matrícula 02/004820** | Auditor de Controle Externo | Equipe de Auditoria |
| **BRUNO MATTOS SOUZA DE SOUZA MELO**  **Matrícula 02/004258** | Auditor de Controle Externo | Supervisor |

**DE ACORDO**.

À **SUB-CIDADANIA**, em prosseguimento.

**CAD-TI, 03/06/2026**

**ALBERTO DE FONTES TAVARES NETO**

**Coordenador-Geral**

**Matrícula 02/004260**

1. Refere-se às salvaguardas do Grupo de Implementação 1 (IG1) não auditadas na primeira fase da fiscalização, abrangendo agora os Controles 7, 8, 9, 10, 11, 12, 14, 15 e 17 do *framework* CIS Controls v8.1. [↑](#footnote-ref-2)
2. Os relatórios preliminares individuais enviados aos jurisdicionados encontram-se presentes no TSID03 de cada anexo das organizações auditadas (AN08 a AN43). [↑](#footnote-ref-3)
3. Destaca-se a ausência de 2 planos na avaliação, uma vez que não foram enviados tempestivamente à equipe de fiscalização, e que o plano da RJPREV não foi avaliado dado que parte significativa de seus controles tecnológicos foi considerada no escopo da avaliação da SEFAZ, dada a dependência de gestão. Planos avaliados estão no AN44. [↑](#footnote-ref-4)
4. O item 8.8 da ISO/IEC 27002:2022 (Gestão de vulnerabilidades) estabelece que as informações sobre vulnerabilidades técnicas dos sistemas em uso devem ser obtidas, a exposição da organização avaliada e as medidas apropriadas tomadas. [↑](#footnote-ref-5)
5. As medidas básicas do Controle 07 (Gestão contínua de vulnerabilidades) dos Controles CIS versão 8.1 representam o conjunto mínimo de medidas para estabelecer e manter o processo de gerenciamento de vulnerabilidades da organização. [↑](#footnote-ref-6)
6. BRASIL. Ministério da Gestão e da Inovação em Serviços Públicos. Secretaria de Governo Digital. Programa de Privacidade e Segurança da Informação (PPSI): Guia de Gerenciamento de Vulnerabilidades. 2023. Disponível em: <https://www.gov.br/governodigital/pt-br/privacidade-e-seguranca/ppsi/guia_gerenciamento_vulnerabilidades.pdf>. Acesso em: 1 dez. 2025. [↑](#footnote-ref-7)
7. CENTER FOR INTERNET SECURITY (CIS). CIS Controls v8.1 Vulnerability Management Policy Template. CIS, 2025. Disponível em: <https://www.cisecurity.org/insights/white-papers/controls-v8-1-vulnerability-management-policy-template>. Acesso em: 1 dez. 2025. [↑](#footnote-ref-8)
8. Os relatórios individuais preliminares encontram-se presentes nos anexos individuais de cada auditado, AN08 a AN43. [↑](#footnote-ref-9)