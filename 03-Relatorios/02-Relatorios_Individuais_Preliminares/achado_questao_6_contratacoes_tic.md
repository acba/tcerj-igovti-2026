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
* COBIT 2019, APO10.05 - Monitorar desempenho e conformidade de fornecedores: acompanhar desempenho, conformidade, qualidade e resultados pactuados com fornecedores.

### Evidências
{% for evidencia in achado.evidencias %}
* {{ evidencia }};
{% endfor %}

### Situação encontrada
{% set situacao_processo = 'Inexistência ou fragilidade de processo formal e padronizado para contratações de TIC.' %}
{% set situacao_aprovacao = 'Contratações de TIC sem análise prévia e aprovação técnica obrigatória da área de TIC.' %}
{% set situacao_aderencia = 'Contratações de TIC sem aderência ao plano de TIC, ao plano de contratações ou à proposta orçamentária.' %}
{% set situacao_equipe = 'Contratações de TIC sem equipe de planejamento formalmente designada e com participação técnica de TIC.' %}
{% set situacao_artefatos = 'Artefatos de planejamento das contratações de TIC sem requisitos técnicos, análise de riscos, segurança da informação, proteção de dados ou critérios objetivos de aceite.' %}
{% set situacao_niveis = 'Contratações de TIC sem níveis mínimos de serviço, métricas de desempenho ou critérios objetivos de fiscalização e recebimento.' %}
Conclui-se que o(a) {{ auditado.sigla }} não demonstrou adotar processo formal e padronizado para planejamento, contratação, fiscalização e gestão de soluções de TIC, com participação técnica da área de TIC, alinhamento ao planejamento, requisitos de segurança e critérios objetivos de entrega e desempenho, pois a Equipe de Auditoria identificou fragilidades nos seguintes aspectos:{% if situacao_processo in achado.situacoes_encontradas %} processo formal e padronizado para contratações de TIC;{% endif %}{% if situacao_aprovacao in achado.situacoes_encontradas %} análise prévia e aprovação técnica da área de TIC;{% endif %}{% if situacao_aderencia in achado.situacoes_encontradas %} aderência ao plano de TIC, ao plano de contratações ou à proposta orçamentária;{% endif %}{% if situacao_equipe in achado.situacoes_encontradas %} equipe de planejamento formalmente designada e com participação técnica de TIC;{% endif %}{% if situacao_artefatos in achado.situacoes_encontradas %} requisitos técnicos, análise de riscos, segurança da informação, proteção de dados ou critérios objetivos de aceite nos artefatos de planejamento;{% endif %}{% if situacao_niveis in achado.situacoes_encontradas %} níveis mínimos de serviço, métricas de desempenho ou critérios objetivos de fiscalização e recebimento;{% endif %}.{% if situacao_processo in achado.situacoes_encontradas %} A inexistência ou fragilidade de processo formal contraria a governança das contratações prevista no art. 11 da Lei 14.133/2021, a padronização documental do art. 19, inciso IV, e o COBIT 2019, APO01.09, podendo gerar falta de clareza quanto a etapas, instâncias decisórias e critérios de aprovação.{% endif %}{% if situacao_aprovacao in achado.situacoes_encontradas %} A ausência de análise prévia e aprovação técnica da área de TIC contraria a governança das contratações, a aprovação formal de requisitos da solução prevista no COBIT 2019, BAI02.04, e a definição de papéis e responsabilidades do COBIT 2019, APO01.05, podendo resultar em soluções incompatíveis com padrões técnicos, segurança ou prioridades institucionais.{% endif %}{% if situacao_aderencia in achado.situacoes_encontradas %} A falta de aderência ao planejamento, ao plano de contratações ou à proposta orçamentária contraria os arts. 11 e 18 da Lei 14.133/2021, podendo gerar contratações reativas, desalinhadas ou sem compatibilidade com prioridades e disponibilidade orçamentária.{% endif %}{% if situacao_equipe in achado.situacoes_encontradas %} A ausência de equipe de planejamento formalmente designada e com participação técnica de TIC contraria a governança das contratações, o art. 7º da Lei 14.133/2021 e a definição de papéis e responsabilidades do COBIT 2019, APO01.05, podendo fragilizar a instrução e a avaliação técnica da contratação.{% endif %}{% if situacao_artefatos in achado.situacoes_encontradas %} A insuficiência dos artefatos de planejamento contraria os arts. 18 e 6º, inciso XXIII, da Lei 14.133/2021 e o art. 46 da LGPD, podendo levar a contratações sem requisitos técnicos, riscos, segurança, proteção de dados ou critérios objetivos de aceite.{% endif %}{% if situacao_niveis in achado.situacoes_encontradas %} A ausência de níveis mínimos de serviço, métricas de desempenho ou critérios objetivos de fiscalização e recebimento contraria o art. 6º, inciso XXIII, da Lei 14.133/2021 e o COBIT 2019, APO10.03 e APO10.05, podendo gerar pagamento desvinculado da entrega de resultados, qualidade ou desempenho.{% endif %}

As contratações de TIC exigem governança técnica, planejamento adequado, participação da área de TIC e mecanismos objetivos de fiscalização e mensuração de resultados. A complexidade das soluções tecnológicas, os riscos de segurança da informação e a dependência operacional dos serviços tornam insuficiente uma instrução contratual genérica ou sem análise técnica especializada.

Sob a perspectiva da Questão 6 da matriz de planejamento, a organização deve possuir processo formal e padronizado para contratações de TIC, definir papéis e responsabilidades, utilizar modelos e orientações, submeter contratações à análise técnica da área de TIC, assegurar alinhamento ao planejamento e ao orçamento, designar equipe de planejamento, prever requisitos técnicos e de segurança e estabelecer níveis de serviço e critérios objetivos de fiscalização e recebimento.

Os critérios adotados pela matriz indicam que a alta administração é responsável pela governança das contratações, que a fase preparatória deve conter planejamento compatível com o plano de contratações e elementos mínimos do estudo técnico preliminar, que os termos de referência devem prever requisitos, modelo de execução, modelo de gestão e critérios de medição e pagamento, e que a gestão de TIC deve aprovar requisitos, definir papéis e acompanhar contratos e desempenho de fornecedores[^explica_contratacoes_tic].

Com base na análise das respostas aos itens q2801, q2801ext[A], q2801ext[B], q2801ext[C], q2801ext[D], q2801ext[E], q2801ext[F], q2801ext[G], q2804[A], q2804[B], q2804[C], q2804[D], q2804[E], q2102ext[C], q2802ext[C] e q2802ext[D] do questionário aplicado e da avaliação das evidências anexadas aos itens q2801evi, q2804eviA, q2102evi e q2802evi, conforme apontado na seção de Evidências, a Equipe de Auditoria constatou as seguintes deficiências nas contratações de TIC da organização:

{% for situacao in achado.situacoes_encontradas %}
* **{{ situacao }}**
{% endfor %}

Essas situações ensejaram o presente achado e serão detalhadas nas seções subsequentes.

[^explica_contratacoes_tic]: Os critérios de contratações de TIC adotados pela matriz combinam requisitos legais da Lei 14.133/2021, requisitos de segurança e proteção de dados da LGPD e boas práticas do COBIT 2019 sobre requisitos, papéis, procedimentos, contratos e desempenho de fornecedores.

{% set situacao = 'Inexistência ou fragilidade de processo formal e padronizado para contratações de TIC.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Processo formal e padronizado para contratações de TIC

O processo de contratação de TIC deve estabelecer fluxo, etapas, papéis, responsabilidades, modelos mínimos de artefatos, manuais, checklists ou orientações internas. Esses elementos reduzem improvisação, aumentam padronização e permitem controle sobre a qualidade da instrução processual.

O art. 11, parágrafo único, da Lei 14.133/2021 atribui à alta administração responsabilidade pela governança das contratações, com processos, estruturas, gestão de riscos e controles internos. O art. 19, inciso IV, prevê a instituição de modelos de documentos padronizados, e o COBIT 2019, APO01.09, orienta a definição e comunicação de políticas e procedimentos.

Sem processo formal e padronizado, pode não haver clareza quanto às etapas, instâncias decisórias, critérios de aprovação e artefatos mínimos das contratações de TIC.

Diante disso, __será proposta recomendação para que a organização formalize processo de contratação de TIC, contemplando fluxo, etapas, papéis, responsabilidades, modelos mínimos de artefatos, manuais, checklists ou orientações internas.__

{% endif %}

{% set situacao = 'Contratações de TIC sem análise prévia e aprovação técnica obrigatória da área de TIC.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Análise prévia e aprovação técnica da área de TIC

As contratações de TIC devem ser submetidas à análise prévia e aprovação técnica da área de TIC, inclusive quando demandadas por outras áreas da organização. Essa análise é necessária para verificar compatibilidade técnica, segurança, integração com o ambiente existente, riscos e aderência a padrões institucionais.

O COBIT 2019, BAI02.04, orienta a obtenção de aprovação formal dos requisitos funcionais, técnicos, de segurança e de conformidade antes de prosseguir com a solução. O COBIT 2019, APO01.05, reforça a definição de papéis e responsabilidades relacionados à informação e à tecnologia.

Sem análise e aprovação técnica obrigatória, a organização pode contratar soluções incompatíveis com padrões técnicos, requisitos institucionais, segurança ou prioridades definidas.

Diante disso, __será proposta recomendação para que as contratações de TIC sejam submetidas à análise prévia e aprovação técnica da área de TIC, inclusive quando demandadas por outras áreas da organização.__

{% endif %}

{% set situacao = 'Contratações de TIC sem aderência ao plano de TIC, ao plano de contratações ou à proposta orçamentária.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Aderência ao planejamento, plano de contratações e proposta orçamentária

As contratações de TIC devem estar vinculadas ao planejamento de TIC, ao plano de contratações e à proposta orçamentária. Essa vinculação demonstra que a contratação decorre de prioridade definida, possui respaldo orçamentário e contribui para objetivos institucionais.

O art. 18 da Lei 14.133/2021 prevê a compatibilização da contratação com o plano de contratações anual e o planejamento da Administração. O art. 11 também reforça a responsabilidade da alta administração pela governança das contratações.

A ausência de aderência ao planejamento, ao plano de contratações ou à proposta orçamentária aumenta o risco de aquisições reativas, desalinhadas, não priorizadas ou sem justificativa adequada.

Diante disso, __será proposta recomendação para que a organização condicione as contratações de TIC à vinculação com o planejamento de TIC, com o plano de contratações e com a proposta orçamentária, ressalvadas situações excepcionais devidamente justificadas.__

{% endif %}

{% set situacao = 'Contratações de TIC sem equipe de planejamento formalmente designada e com participação técnica de TIC.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Equipe de planejamento da contratação de TIC

As contratações de TIC devem contar com equipe de planejamento formalmente designada, com participação da área requisitante, da área técnica de TIC e das demais áreas necessárias. A designação formal favorece responsabilização, segregação de funções e qualidade técnica da instrução.

O art. 7º da Lei 14.133/2021 trata da designação de agentes públicos para funções essenciais, observadas atribuições, formação e segregação de funções. O COBIT 2019, APO01.05, orienta a definição e comunicação de papéis e responsabilidades.

Sem equipe formalmente designada e com participação técnica de TIC, os artefatos de planejamento podem ser incompletos ou tecnicamente frágeis.

Diante disso, __será proposta recomendação para que a organização designe formalmente equipe de planejamento da contratação de TIC, com participação da área requisitante, área técnica de TIC e demais áreas necessárias.__

{% endif %}

{% set situacao = 'Artefatos de planejamento das contratações de TIC sem requisitos técnicos, análise de riscos, segurança da informação, proteção de dados ou critérios objetivos de aceite.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Artefatos de planejamento das contratações de TIC

Os artefatos de planejamento das contratações de TIC devem contemplar requisitos técnicos, análise de riscos, requisitos de segurança da informação, proteção de dados pessoais quando aplicável e critérios objetivos de aceite.

O art. 18 da Lei 14.133/2021 define elementos mínimos da fase preparatória, e o art. 6º, inciso XXIII, prevê que o termo de referência contenha requisitos da contratação, modelo de execução, modelo de gestão contratual e critérios de medição e pagamento. O art. 46 da LGPD exige medidas técnicas e administrativas de segurança desde a concepção do produto ou serviço até sua execução.

Sem esses elementos, a contratação pode resultar em solução inadequada, riscos não tratados, baixa segurança, problemas de proteção de dados e dificuldade de verificar se a entrega atende às necessidades da Administração.

Diante disso, __será proposta recomendação para que os artefatos de planejamento das contratações de TIC contemplem requisitos técnicos, análise de riscos, requisitos de segurança da informação, proteção de dados pessoais quando aplicável e critérios objetivos de aceite.__

{% endif %}

{% set situacao = 'Contratações de TIC sem níveis mínimos de serviço, métricas de desempenho ou critérios objetivos de fiscalização e recebimento.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Níveis de serviço, métricas de desempenho e critérios de fiscalização

Os instrumentos de contratação de TIC devem estabelecer níveis mínimos de serviço, indicadores, critérios de medição, critérios de recebimento e vinculação do pagamento à efetiva entrega de resultados ou níveis de qualidade.

O art. 6º, inciso XXIII, da Lei 14.133/2021 exige modelo de gestão contratual e critérios de medição e pagamento no termo de referência. O COBIT 2019, APO10.03 e APO10.05, orienta o estabelecimento e acompanhamento de contratos, responsabilidades, níveis de serviço, desempenho, conformidade, qualidade e resultados pactuados com fornecedores.

Sem níveis mínimos de serviço, métricas de desempenho ou critérios objetivos de fiscalização e recebimento, a organização fica exposta ao pagamento desvinculado da qualidade, desempenho ou resultado efetivamente entregue.

Diante disso, __será proposta recomendação para que os TRs, projetos básicos, contratos ou instrumentos equivalentes de TIC estabeleçam níveis mínimos de serviço, indicadores, critérios de medição, critérios de recebimento e vinculação do pagamento à efetiva entrega de resultados ou níveis de qualidade.__

{% endif %}

#### Conclusão

As fragilidades identificadas nas contratações de TIC comprometem a governança técnica, o alinhamento ao planejamento, a qualidade dos artefatos, a gestão de riscos, a segurança da informação e o controle de resultados.

Diante das situações apresentadas, será sugerida proposta de encaminhamento à organização para que promova a adequação de seu processo de contratação de TIC, alinhando-o aos critérios previstos na Lei 14.133/2021, na Lei 13.709/2018 e no COBIT 2019.

### Propostas de Encaminhamento
{% for e in achado.encaminhamentos %}
* **Comunicação com {{ e.tipo }}** para que {{ e.encaminhamento }};
{% endfor %}

{# Final do Achado - Contratações de TIC #}
{% endif %}
