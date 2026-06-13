{% set nome_achado = 'Contratações de TIC sem governança técnica e controle de resultados' %}
{% set achado = auditado.get_achado_por_nome(nome_achado) %}
{% if achado %}

\newpage

## Achado {{ achado.numero }} – {{ achado.nome }}

### Critérios
* Art. 11, parágrafo único, da Lei 14.133/2021: responsabilidade da alta administração pela governança das contratações, com processos, estruturas, gestão de riscos e controles internos;
* Art. 18, caput e §1º, incisos I, IV, V, VIII, IX, X e XIII, da Lei 14.133/2021: fase preparatória caracterizada pelo planejamento, compatibilização com o plano de contratações anual e elementos mínimos do estudo técnico preliminar;
* Art. 6º, inciso XXIII, alíneas "d", "e", "f" e "g", da Lei 14.133/2021: termo de referência deve conter requisitos da contratação, modelo de execução, modelo de gestão contratual e critérios de medição e pagamento;
* Art. 19, inciso IV, da Lei 14.133/2021: instituição de modelos de minutas de editais, termos de referência, contratos padronizados e demais documentos;
* Art. 7º, caput, incisos I a III e §1º, da Lei 14.133/2021: designação de agentes públicos para funções essenciais, observados atribuições, formação, segregação de funções e inexistência de vínculos que comprometam a atuação;
* Art. 46, caput e §2º, da Lei 13.709/2018: adoção de medidas de segurança, técnicas e administrativas, desde a concepção do produto ou serviço até sua execução;
* COBIT 2019, BAI02.04 - Obter aprovação dos requisitos da solução: obter aprovação formal dos requisitos funcionais, técnicos, de segurança e de conformidade antes de prosseguir com a solução;
* COBIT 2019, APO01.05 - Estabelecer papéis e responsabilidades: definir e comunicar papéis e responsabilidades relacionados à informação e à tecnologia;
* COBIT 2019, APO01.09 - Definir e comunicar políticas e procedimentos: manter políticas, procedimentos e orientações para direcionar processos de gestão de TIC;
* COBIT 2019, APO10.03 - Gerenciar relacionamentos e contratos com fornecedores: estabelecer e acompanhar contratos, responsabilidades, níveis de serviço e obrigações de fornecedores;
* COBIT 2019, APO10.05 - Monitorar desempenho e conformidade de fornecedores: acompanhar desempenho, conformidade, qualidade e resultados pactuados com fornecedores;
* Instrução Normativa SGD/ME nº 94, de 23 de dezembro de 2022, art. 1º, § 1º: como referência de boa prática, a aplicação de ritos formais de contratação de TIC pode ser facultada para contratações diretas por dispensa em razão do valor (inciso II do art. 75 da Lei nº 14.133/2021), indicando a possibilidade de fluxos simplificados para aquisições de baixa complexidade ou valor.

### Evidências
{% for evidencia in achado.evidencias %}
* {{ evidencia }};
{% endfor %}

### Situação encontrada

As contratações de TIC exigem governança técnica, planejamento prévio circunstanciado, efetiva participação da área de tecnologia e o estabelecimento de critérios objetivos para recebimento do objeto e mensuração de resultados. A alta complexidade dos ativos de tecnologia, as exigências de conformidade legal (incluindo LGPD) e a forte dependência das atividades finalísticas em relação aos serviços de TIC demandam um fluxo de contratação rigoroso, afastando a possibilidade de aquisições genéricas ou desprovidas de análise técnica especializada.

Os critérios previstos na Lei 14.133/2021, na Lei 13.709/2018 (LGPD) e nos objetivos do COBIT 2019 disciplinam que a alta administração responde pela governança das contratações, que a fase preparatória deve ser instruída com Estudo Técnico Preliminar (ETP) e matrizes de risco adequadas, e que os Termos de Referência (TR) devem conter modelos objetivos de execução, critérios objetivos de medição atrelados a níveis mínimos de serviço (ANS) e aprovação formal dos requisitos técnicos e de segurança[^explica_contratacoes_tic].

Com base na análise das respostas aos itens 2801, 2804, 2102 e 2802 do questionário aplicado e da avaliação das evidências documentais anexadas, constatou-se que as contratações de TIC da organização apresentam desconformidades em relação a essas diretrizes. A Equipe de Auditoria identificou fragilidades nos seguintes aspectos:

{% set situacao_processo = 'Inexistência ou fragilidade de processo formal e padronizado para contratações de TIC.' %}
{% set situacao_aprovacao = 'Contratações de TIC sem análise prévia e aprovação técnica obrigatória da área de TIC.' %}
{% set situacao_aderencia = 'Contratações de TIC sem aderência ao plano de TIC, ao plano de contratações ou à proposta orçamentária.' %}
{% set situacao_equipe = 'Contratações de TIC sem equipe de planejamento formalmente designada e com participação técnica de TIC.' %}
{% set situacao_artefatos = 'Artefatos de planejamento das contratações de TIC sem requisitos técnicos, análise de riscos, segurança da informação, proteção de dados ou critérios objetivos de aceite.' %}
{% set situacao_niveis = 'Contratações de TIC sem níveis mínimos de serviço, métricas de desempenho ou critérios objetivos de fiscalização e recebimento.' %}

{% if situacao_processo in achado.situacoes_encontradas %}
* **Processo de contratação de TIC**: a fragilidade ou ausência de fluxo padronizado contraria a governança de contratações (Lei 14.133/2021, art. 11/art. 19, IV) e o COBIT 2019 (APO01.09), acarretando indefinição de papéis, ritos processuais e prazos internos.
{% endif %}
{% if situacao_aprovacao in achado.situacoes_encontradas %}
* **Aprovação técnica de TIC**: a falta de avaliação prévia obrigatória pela área técnica contraria a governança institucional (COBIT 2019, BAI02.04 e APO01.05), favorecendo aquisições de soluções desalinhadas do ecossistema de infraestrutura existente.
{% endif %}
{% if situacao_aderencia in achado.situacoes_encontradas %}
* **Aderência ao planejamento**: a desconexão com o planejamento setorial de TIC e com o plano de contratações anual contraria a Lei 14.133/2021 (arts. 11 e 18), resultando em aquisições reativas, emergenciais ou sem lastro orçamentário adequado.
{% endif %}
{% if situacao_equipe in achado.situacoes_encontradas %}
* **Equipe de planejamento**: a ausência de portaria ou designação de equipe mista com representação técnica de TIC contraria a governança pública e a Lei 14.133/2021 (art. 7º), comprometendo a qualidade e a imparcialidade das especificações técnicas.
{% endif %}
{% if situacao_artefatos in achado.situacoes_encontradas %}
* **Artefatos de planejamento (ETP/TR)**: a insuficiência de análise de riscos, LGPD e requisitos técnicos detalhados contraria a Lei 14.133/2021 (art. 18 e art. 6º, XXIII) e a LGPD (art. 46), expondo o órgão a passivos de segurança da informação e perdas contratuais.
{% endif %}
{% if situacao_niveis in achado.situacoes_encontradas %}
* **Níveis de serviço (ANS)**: a ausência de indicadores objetivos de desempenho e qualidade contraria a Lei 14.133/2021 (art. 6º, XXIII) e o COBIT 2019 (APO10.03 e APO10.05), vinculando os pagamentos à mera disponibilização de esforço ou tempo, em detrimento da qualidade das entregas.
{% endif %}

Essas situações ensejaram o presente achado e serão detalhadas nas seções subsequentes.

[^explica_contratacoes_tic]: Os critérios de contratações de TIC combinam requisitos legais da Lei 14.133/2021, requisitos de segurança e proteção de dados da LGPD e boas práticas do COBIT 2019 sobre requisitos, papéis, procedimentos, contratos e desempenho de fornecedores.

{% set situacao = 'Inexistência ou fragilidade de processo formal e padronizado para contratações de TIC.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Processo formal e padronizado para contratações de TIC

O processo de contratação de TIC deve estabelecer fluxo, etapas, papéis, responsabilidades, modelos mínimos de artefatos, manuais, checklists ou orientações internas. Esses elementos reduzem improvisação, aumentam padronização e permitem controle sobre a qualidade da instrução processual.

O art. 11, parágrafo único, da Lei 14.133/2021 atribui à alta administração responsabilidade pela governança das contratações, com processos, estruturas, gestão de riscos e controles internos. O art. 19, inciso IV, prevê a instituição de modelos de documentos padronizados, e o COBIT 2019, APO01.09, orienta a definição e comunicação de políticas e procedimentos.

A ausência de um fluxo processual regulamentado e de modelos padronizados prejudica a conformidade das contratações de TIC, gerando atrasos processuais e inconsistências na elaboração dos documentos da fase preparatória.

Diante disso, __será proposta recomendação para que a organização formalize processo de contratação de TIC, contemplando fluxo, etapas, papéis, responsabilidades, modelos mínimos de artefatos, manuais, checklists ou orientações internas.__

{% endif %}

{% set situacao = 'Contratações de TIC sem análise prévia e aprovação técnica obrigatória da área de TIC.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Análise prévia e aprovação técnica da área de TIC

As contratações de TIC devem ser submetidas à análise prévia e aprovação técnica da área de TIC, inclusive quando demandadas por outras áreas da organização. Essa análise é necessária para verificar compatibilidade técnica, segurança, integração com o ambiente existente, riscos e aderência a padrões institucionais.

O COBIT 2019, BAI02.04, orienta a obtenção de aprovação formal dos requisitos funcionais, técnicos, de segurança e de conformidade antes de prosseguir com a solução. O COBIT 2019, APO01.05, reforça a definição de papéis e responsabilidades relacionados à informação e à tecnologia. De forma complementar, o art. 1º, § 1º, da Instrução Normativa SGD/ME nº 94/2022, adotado como referência de boa prática, aponta a possibilidade de facultar a aplicação de ritos formais para contratações diretas por dispensa em razão do valor (inciso II do art. 75 da Lei nº 14.133/2021), indicando que os controles e pareceres podem ser proporcionais à relevância estratégica, complexidade e valor da aquisição.

A realização de aquisições de tecnologia sem a validação técnica da área de TIC compromete a integridade do ambiente lógico do órgão, gerando riscos de incompatibilidade sistêmica, vulnerabilidades de segurança e ineficiência operacional.

Diante disso, __será proposta recomendação para que a organização estabeleça a submissão das contratações de TIC à análise prévia e à aprovação técnica da área de TIC, inclusive quando demandadas por outras áreas, facultando a adoção de fluxos simplificados ou a dispensa de parecer detalhado para contratações diretas por dispensa em razão do valor (baixo valor) ou de baixa complexidade técnica, mediante critérios objetivos ou catálogos de soluções padronizadas.__

{% endif %}

{% set situacao = 'Contratações de TIC sem aderência ao plano de TIC, ao plano de contratações ou à proposta orçamentária.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Aderência ao planejamento, plano de contratações e proposta orçamentária

As contratações de TIC devem estar vinculadas ao planejamento de TIC, ao plano de contratações e à proposta orçamentária. Essa vinculação demonstra que a contratação decorre de prioridade definida, possui respaldo orçamentário e contribui para objetivos institucionais.

O art. 18 da Lei 14.133/2021 prevê a compatibilização da contratação com o plano de contratações anual e o planejamento da Administração. O art. 11 também reforça a responsabilidade da alta administração pela governança das contratações.

A falta de conformidade das aquisições frente ao planejamento setorial de TIC e ao plano de contratações anual resulta na fragmentação de despesas, em contratações reativas e no desperdício de recursos orçamentários.

Diante disso, __será proposta recomendação para que a organização condicione as contratações de TIC à vinculação com o planejamento de TIC, com o plano de contratações e com a proposta orçamentária, ressalvadas situações excepcionais devidamente justificadas.__

{% endif %}

{% set situacao = 'Contratações de TIC sem equipe de planejamento formalmente designada e com participação técnica de TIC.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Equipe de planejamento da contratação de TIC

As contratações de TIC devem contar com equipe de planejamento formalmente designada, com participação da área requisitante, da área técnica de TIC e das demais áreas necessárias. A designação formal favorece responsabilização, segregação de funções e qualidade técnica da instrução.

O art. 7º da Lei 14.133/2021 trata da designação de agentes públicos para funções essenciais, observadas atribuições, formação e segregação de funções. O COBIT 2019, APO01.05, orienta a definição e comunicação de papéis e responsabilidades.

A falta de designação formal da equipe com a inclusão de especialistas de TIC compromete a qualidade técnica das estimativas de mercado, dos estudos de viabilidade e da especificação do objeto no ETP e no TR.

Diante disso, __será proposta recomendação para que a organização designe formalmente equipe de planejamento da contratação de TIC, com participação da área requisitante, área técnica de TIC e demais áreas necessárias.__

{% endif %}

{% set situacao = 'Artefatos de planejamento das contratações de TIC sem requisitos técnicos, análise de riscos, segurança da informação, proteção de dados ou critérios objetivos de aceite.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Artefatos de planejamento das contratações de TIC

Os artefatos de planejamento das contratações de TIC devem contemplar requisitos técnicos, análise de riscos, requisitos de segurança da informação, proteção de dados pessoais quando aplicável e critérios objetivos de aceite.

O art. 18 da Lei 14.133/2021 define elementos mínimos da fase preparatória, e o art. 6º, inciso XXIII, prevê que o termo de referência contenha requisitos da contratação, modelo de execução, modelo de gestão contratual e critérios de medição e pagamento. O art. 46 da LGPD exige medidas técnicas e administrativas de segurança desde a concepção do produto ou serviço até sua execução.

A omissão de requisitos técnicos claros, matrizes de risco, diretrizes de segurança da informação e regras de LGPD nos artefatos preparatórios expõe a administração a severos riscos operacionais e inviabiliza a fiscalização das entregas.

Diante disso, __será proposta recomendação para que os artefatos de planejamento das contratações de TIC contemplem requisitos técnicos, análise de riscos, requisitos de segurança da informação, proteção de dados pessoais quando aplicável e critérios objetivos de aceite.__

{% endif %}

{% set situacao = 'Contratações de TIC sem níveis mínimos de serviço, métricas de desempenho ou critérios objetivos de fiscalização e recebimento.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Níveis de serviço, métricas de desempenho e critérios de fiscalização

Os instrumentos de contratação de TIC devem estabelecer níveis mínimos de serviço, indicadores, critérios de medição, critérios de recebimento e vinculação do pagamento à efetiva entrega de resultados ou níveis de qualidade.

O art. 6º, inciso XXIII, da Lei 14.133/2021 exige modelo de gestão contratual e critérios de medição e pagamento no termo de referência. O COBIT 2019, APO10.03 e APO10.05, orienta o estabelecimento e acompanhamento de contratos, responsabilidades, níveis de serviço, desempenho, conformidade, qualidade e resultados pactuados com fornecedores.

A contratação desprovida de Acordos de Nível de Serviço (ANS) e indicadores objetivos vincula o pagamento público à mera presença física ou disponibilização de tempo de profissionais, impossibilitando a cobrança por resultados, qualidade e conformidade das entregas da contratada.

Diante disso, __será proposta recomendação para que os TRs, projetos básicos, contratos ou instrumentos equivalentes de TIC estabeleçam níveis mínimos de serviço, indicadores, critérios de medição, critérios de recebimento e vinculação do pagamento à efetiva entrega de resultados ou níveis de qualidade.__

{% endif %}

#### Conclusão

As fragilidades identificadas nas contratações de TIC comprometem a governança técnica, o alinhamento ao planejamento, a qualidade dos artefatos, a gestão de riscos, a segurança da informação e o controle de resultados.

Diante do cenário exposto, formula-se proposta de encaminhamento com vistas a recomendar à organização que promova a estruturação e a adequação de seus processos de contratação de TIC, em alinhamento aos critérios da Lei 14.133/2021, da Lei 13.709/2018 (LGPD) e do COBIT 2019.

### Propostas de Encaminhamento
{% for e in achado.encaminhamentos %}
* **Comunicação com {{ e.tipo }}** para que {{ e.encaminhamento }};
{% endfor %}

{# Final do Achado - Contratações de TIC #}
{% endif %}
