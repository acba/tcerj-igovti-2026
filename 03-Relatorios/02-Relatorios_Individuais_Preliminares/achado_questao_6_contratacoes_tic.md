{% set nome_achado = 'Fragilidades na governança técnica da fase preparatória das contratações de TIC' %}
{% set achado = auditado.get_achado_por_nome(nome_achado) %}
{% if achado %}
{% set situacao_processo = 'Inexistência ou fragilidade de processo formal e padronizado para contratações de TIC.' %}
{% set situacao_aprovacao = 'Contratações de TIC sem análise prévia e aprovação técnica obrigatória da área de TIC.' %}
{% set situacao_aderencia = 'Contratações de TIC sem alinhamento demonstrado ao planejamento de TIC, ao plano de contratações ou à proposta orçamentária.' %}
{% set situacao_equipe = 'Contratações de TIC sem equipe de planejamento formalmente designada e com participação técnica de TIC.' %}
{% set situacao_artefatos = 'Artefatos de planejamento das contratações de TIC sem requisitos técnicos, análise de riscos, segurança da informação, proteção de dados ou critérios objetivos de aceite.' %}
{% set situacao_niveis = 'Contratações de TIC sem níveis mínimos de serviço, métricas de desempenho ou critérios objetivos de fiscalização e recebimento.' %}
{% set motivos_processo = auditado.get_motivos_situacao(nome_achado, situacao_processo) %}
{% set motivos_aprovacao = auditado.get_motivos_situacao(nome_achado, situacao_aprovacao) %}
{% set motivos_aderencia = auditado.get_motivos_situacao(nome_achado, situacao_aderencia) %}
{% set motivos_equipe = auditado.get_motivos_situacao(nome_achado, situacao_equipe) %}
{% set motivos_artefatos = auditado.get_motivos_situacao(nome_achado, situacao_artefatos) %}
{% set motivos_niveis = auditado.get_motivos_situacao(nome_achado, situacao_niveis) %}
{% set tem_processo = situacao_processo in achado.situacoes_encontradas and motivos_processo %}
{% set tem_aprovacao = situacao_aprovacao in achado.situacoes_encontradas and motivos_aprovacao %}
{% set tem_aderencia = situacao_aderencia in achado.situacoes_encontradas and motivos_aderencia %}
{% set tem_equipe = situacao_equipe in achado.situacoes_encontradas and motivos_equipe %}
{% set tem_artefatos = situacao_artefatos in achado.situacoes_encontradas and motivos_artefatos %}
{% set tem_niveis = situacao_niveis in achado.situacoes_encontradas and motivos_niveis %}
{% set qtd_situacoes_exibidas = (1 if tem_processo else 0) + (1 if tem_aprovacao else 0) + (1 if tem_aderencia else 0) + (1 if tem_equipe else 0) + (1 if tem_artefatos else 0) + (1 if tem_niveis else 0) %}

\newpage

## Achado {{ achado.numero }} – {{ achado.nome }}

### Critérios
{% if tem_processo or tem_aderencia %}
* Art. 11, parágrafo único, da Lei 14.133/2021: responsabilidade da alta administração pela governança das contratações, com processos, estruturas, gestão de riscos e controles internos;
{% endif %}
{% if tem_aderencia or tem_artefatos %}
* Art. 18, caput e §1º, incisos I, IV, V, VIII, IX, X e XIII, da Lei 14.133/2021: fase preparatória caracterizada pelo planejamento, compatibilização com o plano de contratações anual e elementos mínimos do estudo técnico preliminar;
{% endif %}
{% if tem_artefatos or tem_niveis %}
* Art. 6º, inciso XXIII, alíneas "d", "e", "f" e "g", da Lei 14.133/2021: termo de referência deve conter requisitos da contratação, modelo de execução, modelo de gestão contratual e critérios de medição e pagamento;
{% endif %}
{% if tem_processo %}
* Art. 19, inciso IV, da Lei 14.133/2021: instituição de modelos de minutas de editais, termos de referência, contratos padronizados e demais documentos;
{% endif %}
{% if tem_equipe %}
* Art. 7º, caput, incisos I a III e §1º, da Lei 14.133/2021: designação de agentes públicos para funções essenciais, observados atribuições, formação, segregação de funções e inexistência de vínculos que comprometam a atuação;
{% endif %}
{% if tem_artefatos %}
* Art. 46, caput e §2º, da Lei 13.709/2018: adoção de medidas de segurança, técnicas e administrativas, desde a concepção do produto ou serviço até sua execução;
{% endif %}
{% if tem_aprovacao or tem_artefatos %}
* COBIT 2019, BAI02.04 - Obter aprovação dos requisitos da solução: obter aprovação formal dos requisitos funcionais, técnicos, de segurança e de conformidade antes de prosseguir com a solução;
{% endif %}
{% if tem_aprovacao or tem_equipe %}
* COBIT 2019, APO01.05 - Estabelecer papéis e responsabilidades: definir e comunicar papéis e responsabilidades relacionados à informação e à tecnologia;
{% endif %}
{% if tem_processo %}
* COBIT 2019, APO01.09 - Definir e comunicar políticas e procedimentos: manter políticas, procedimentos e orientações para direcionar processos de gestão de TIC;
{% endif %}
{% if tem_niveis %}
* COBIT 2019, APO10.03 - Gerenciar relacionamentos e contratos com fornecedores: estabelecer e acompanhar contratos, responsabilidades, níveis de serviço e obrigações de fornecedores;
* COBIT 2019, APO10.05 - Monitorar desempenho e conformidade de fornecedores: acompanhar desempenho, conformidade, qualidade e resultados pactuados com fornecedores;
{% endif %}
{% if tem_aprovacao %}
* Instrução Normativa SGD/ME nº 94, de 23 de dezembro de 2022, art. 1º, § 1º: como referência de boa prática, a aplicação de ritos formais de contratação de TIC pode ser facultada para contratações diretas por dispensa em razão do valor (inciso II do art. 75 da Lei nº 14.133/2021), indicando a possibilidade de fluxos simplificados para aquisições de baixa complexidade ou valor.
{% endif %}

### Evidências
{% set evidencias = auditado.get_evidencias_numeradas(nome_achado) %}
{% for evidencia in evidencias %}
{% set complemento_evidencia = evidencia.get('complemento') %}
{% set descricao_evidencia = evidencia.descricao.rstrip('.;') %}
* **{{ evidencia.ref }}:** {{ descricao_evidencia }}{{ ';' if not loop.last or complemento_evidencia else '.' }}
{% if complemento_evidencia %}  * {{ complemento_evidencia.rstrip('.;') }}{{ ';' if not loop.last else '.' }}
{% endif %}
{% endfor %}

### Situação encontrada

As contratações de TIC devem observar governança técnica, planejamento prévio proporcional à complexidade do objeto, participação da área de tecnologia quando cabível e critérios objetivos para recebimento e mensuração de resultados. A complexidade dos ativos de tecnologia, as exigências de conformidade legal, incluindo LGPD quando aplicável, e a dependência das atividades finalísticas em relação aos serviços de TIC demandam controles compatíveis com a relevância, o risco e o valor da contratação.

Os critérios previstos na Lei 14.133/2021, na Lei 13.709/2018 (LGPD) e nos objetivos do COBIT 2019 disciplinam que a alta administração responde pela governança das contratações, que a fase preparatória deve ser instruída com planejamento compatível com o objeto e que os Termos de Referência (TR), projetos básicos, contratos ou instrumentos equivalentes devem conter requisitos, modelos de execução, critérios de medição e parâmetros de acompanhamento proporcionais à natureza da contratação[^explica_contratacoes_tic].

Com base na análise das respostas aos itens 2801, 2804, 2102 e 2802 do questionário aplicado e da avaliação das evidências documentais anexadas, não foi demonstrado atendimento suficiente das contratações de TIC da organização a essas diretrizes. A Equipe de Auditoria identificou fragilidades nos seguintes aspectos:

{% if tem_processo %}
* **Processo de contratação de TIC**: a fragilidade ou ausência de fluxo padronizado contraria a governança de contratações (Lei 14.133/2021, art. 11/art. 19, IV) e o COBIT 2019 (APO01.09), acarretando indefinição de papéis, ritos processuais e prazos internos.
{% endif %}
{% if tem_aprovacao %}
* **Aprovação técnica de TIC**: a falta de avaliação prévia pela área técnica, quando necessária, contraria a governança institucional (COBIT 2019, BAI02.04 e APO01.05), favorecendo aquisições de soluções desalinhadas do ambiente tecnológico existente.
{% endif %}
{% if tem_aderencia %}
* **Alinhamento ao planejamento**: a ausência de alinhamento demonstrado ao planejamento de TIC, ao plano de contratações ou à proposta orçamentária não demonstra aderência à Lei 14.133/2021 (arts. 11 e 18), podendo resultar em aquisições reativas ou sem lastro orçamentário adequado.
{% endif %}
{% if tem_equipe %}
* **Equipe de planejamento**: a ausência de portaria ou designação de equipe mista com representação técnica de TIC, quando aplicável, não demonstra aderência à governança pública e à Lei 14.133/2021 (art. 7º), podendo comprometer a qualidade e a imparcialidade das especificações técnicas.
{% endif %}
{% if tem_artefatos %}
* **Artefatos de planejamento (ETP/TR)**: a insuficiência de análise de riscos, requisitos de proteção de dados quando aplicáveis e requisitos técnicos detalhados não demonstra aderência à Lei 14.133/2021 (art. 18 e art. 6º, XXIII) e à LGPD (art. 46), elevando riscos de segurança da informação e de perdas contratuais.
{% endif %}
{% if tem_niveis %}
* **Níveis de serviço**: a ausência de indicadores objetivos de desempenho e qualidade não demonstra aderência à Lei 14.133/2021 (art. 6º, XXIII) e ao COBIT 2019 (APO10.03 e APO10.05), podendo dificultar a vinculação dos pagamentos à qualidade e aos resultados das entregas.
{% endif %}

{% if qtd_situacoes_exibidas == 1 %}
Essa situação ensejou o presente achado e será detalhada na subseção seguinte.
{% else %}
Essas situações ensejaram o presente achado e serão detalhadas nas subseções seguintes.
{% endif %}

[^explica_contratacoes_tic]: Os critérios de contratações de TIC combinam requisitos legais da Lei 14.133/2021, requisitos de segurança e proteção de dados da LGPD e boas práticas do COBIT 2019 sobre requisitos, papéis, procedimentos, contratos e desempenho de fornecedores.

{% set situacao = situacao_processo %}
{% if tem_processo %}
#### Processo formal e padronizado para contratações de TIC

O processo de contratação de TIC deve estabelecer fluxo, etapas, papéis, responsabilidades, modelos mínimos de artefatos, manuais, checklists ou orientações internas. Esses elementos reduzem improvisação, aumentam padronização e permitem controle sobre a qualidade da instrução processual.

O art. 11, parágrafo único, da Lei 14.133/2021 atribui à alta administração responsabilidade pela governança das contratações, com processos, estruturas, gestão de riscos e controles internos. O art. 19, inciso IV, prevê a instituição de modelos de documentos padronizados, e o COBIT 2019, APO01.09, orienta a definição e comunicação de políticas e procedimentos.

Da análise das respostas ao item 2801 e da documentação apresentada, verificou-se que a existência de processo formal e padronizado para contratações de TIC, com fluxo, etapas, papéis, responsabilidades, instâncias de aprovação e modelos de artefatos proporcionais ao porte e aos riscos das contratações, não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
{% set refs_motivo = motivo.get('refs', []) -%}
* {{ motivo.texto.rstrip('.;') }}{% if refs_motivo %} ({{ refs_motivo | join(', ') }}){% endif %}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência de fluxo processual regulamentado e de modelos padronizados reduz a segurança quanto à conformidade das contratações de TIC e eleva o risco de atrasos processuais, indefinição de papéis e inconsistências na elaboração dos documentos da fase preparatória.

{% endif %}

{% set situacao = situacao_aprovacao %}
{% if tem_aprovacao %}
#### Análise prévia e aprovação técnica da área de TIC

As contratações de TIC devem ser submetidas à análise prévia e aprovação técnica da área de TIC, inclusive quando demandadas por outras áreas da organização. Essa análise é necessária para verificar compatibilidade técnica, segurança, integração com o ambiente existente, riscos e aderência a padrões institucionais.

O COBIT 2019, BAI02.04, orienta a obtenção de aprovação formal dos requisitos funcionais, técnicos, de segurança e de conformidade antes de prosseguir com a solução. O COBIT 2019, APO01.05, reforça a definição de papéis e responsabilidades relacionados à informação e à tecnologia. De forma complementar, o art. 1º, § 1º, da Instrução Normativa SGD/ME nº 94/2022, adotado como referência de boa prática, aponta a possibilidade de facultar a aplicação de ritos formais para contratações diretas por dispensa em razão do valor (inciso II do art. 75 da Lei nº 14.133/2021), indicando que os controles e pareceres podem ser proporcionais à relevância estratégica, complexidade e valor da aquisição.

Da análise das respostas ao item 2804 e da documentação apresentada, verificou-se que a submissão das contratações de TIC à análise prévia ou aprovação técnica da área de TIC, inclusive quando demandadas por outras áreas, não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
{% set refs_motivo = motivo.get('refs', []) -%}
* {{ motivo.texto.rstrip('.;') }}{% if refs_motivo %} ({{ refs_motivo | join(', ') }}){% endif %}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência de análise prévia ou aprovação técnica da área de TIC reduz a segurança de que as soluções contratadas sejam compatíveis com o ambiente tecnológico existente, com os requisitos institucionais e com os controles mínimos de segurança da informação, observada a proporcionalidade em relação à complexidade, ao risco e ao valor da contratação.

{% endif %}

{% set situacao = situacao_aderencia %}
{% if tem_aderencia %}
#### Alinhamento ao planejamento, plano de contratações e proposta orçamentária

As contratações de TIC devem estar vinculadas ao planejamento de TIC, ao plano de contratações e à proposta orçamentária. Essa vinculação demonstra que a contratação decorre de prioridade definida, possui respaldo orçamentário e contribui para objetivos institucionais.

O art. 18 da Lei 14.133/2021 prevê a compatibilização da contratação com o plano de contratações anual e o planejamento da Administração. O art. 11 também reforça a responsabilidade da alta administração pela governança das contratações.

Da análise das respostas aos itens 2102, 2802 e 2804 e da documentação apresentada, verificou-se que o alinhamento das contratações de TIC ao planejamento de TIC, ao plano de contratações ou à proposta orçamentária não se mostrou suficientemente demonstrado, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
{% set refs_motivo = motivo.get('refs', []) -%}
* {{ motivo.texto.rstrip('.;') }}{% if refs_motivo %} ({{ refs_motivo | join(', ') }}){% endif %}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência de alinhamento das contratações de TIC ao planejamento de TIC, ao plano de contratações ou à proposta orçamentária eleva o risco de fragmentação de despesas, contratações reativas ou insuficientemente priorizadas e uso pouco eficiente dos recursos orçamentários.

{% endif %}

{% set situacao = situacao_equipe %}
{% if tem_equipe %}
#### Equipe de planejamento da contratação de TIC

As contratações de TIC devem contar com equipe de planejamento formalmente designada, com participação da área requisitante, da área técnica de TIC e das demais áreas necessárias. A designação formal favorece responsabilização, segregação de funções e qualidade técnica da instrução.

O art. 7º da Lei 14.133/2021 trata da designação de agentes públicos para funções essenciais, observadas atribuições, formação e segregação de funções. O COBIT 2019, APO01.05, orienta a definição e comunicação de papéis e responsabilidades.

Da análise das respostas ao item 2804 e da documentação apresentada, verificou-se que a designação formal de equipe de planejamento da contratação de TIC com participação da área requisitante, da área técnica de TIC e das demais áreas necessárias não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
{% set refs_motivo = motivo.get('refs', []) -%}
* {{ motivo.texto.rstrip('.;') }}{% if refs_motivo %} ({{ refs_motivo | join(', ') }}){% endif %}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência de designação formal da equipe de planejamento, com participação técnica de TIC quando aplicável, reduz a segurança quanto à qualidade técnica das estimativas de mercado, dos estudos de viabilidade e da especificação do objeto no ETP, no TR ou em instrumentos equivalentes.

{% endif %}

{% set situacao = situacao_artefatos %}
{% if tem_artefatos %}
#### Artefatos de planejamento das contratações de TIC

Os artefatos de planejamento das contratações de TIC devem contemplar requisitos técnicos, análise de riscos, requisitos de segurança da informação, proteção de dados pessoais quando aplicável e critérios objetivos de aceite.

O art. 18 da Lei 14.133/2021 define elementos mínimos da fase preparatória, e o art. 6º, inciso XXIII, prevê que o termo de referência contenha requisitos da contratação, modelo de execução, modelo de gestão contratual e critérios de medição e pagamento. O art. 46 da LGPD exige medidas técnicas e administrativas de segurança desde a concepção do produto ou serviço até sua execução.

Da análise das respostas ao item 2801 e da documentação apresentada, verificou-se que a inclusão de requisitos técnicos, análise de riscos, segurança da informação, proteção de dados pessoais quando aplicável ou critérios objetivos de aceite nos artefatos de planejamento das contratações de TIC não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
{% set refs_motivo = motivo.get('refs', []) -%}
* {{ motivo.texto.rstrip('.;') }}{% if refs_motivo %} ({{ refs_motivo | join(', ') }}){% endif %}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência ou insuficiência de requisitos técnicos, análise de riscos, requisitos de segurança da informação, regras de proteção de dados pessoais quando aplicáveis ou critérios objetivos de aceite nos artefatos preparatórios eleva o risco de contratações insuficientemente instruídas e pode dificultar a fiscalização das entregas.

{% endif %}

{% set situacao = situacao_niveis %}
{% if tem_niveis %}
#### Níveis de serviço, métricas de desempenho e critérios de fiscalização

Os instrumentos de contratação de TIC devem estabelecer níveis mínimos de serviço, indicadores, critérios de medição, critérios de recebimento e vinculação do pagamento à efetiva entrega de resultados ou níveis de qualidade.

O art. 6º, inciso XXIII, da Lei 14.133/2021 exige modelo de gestão contratual e critérios de medição e pagamento no termo de referência. O COBIT 2019, APO10.03 e APO10.05, orienta o estabelecimento e acompanhamento de contratos, responsabilidades, níveis de serviço, desempenho, conformidade, qualidade e resultados pactuados com fornecedores.

Da análise das respostas ao item 2801 e da documentação apresentada, verificou-se que a previsão de níveis mínimos de serviço, métricas de desempenho ou critérios objetivos de fiscalização, recebimento e pagamento nas contratações de TIC não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
{% set refs_motivo = motivo.get('refs', []) -%}
* {{ motivo.texto.rstrip('.;') }}{% if refs_motivo %} ({{ refs_motivo | join(', ') }}){% endif %}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência de demonstração de níveis mínimos de serviço, métricas de desempenho ou indicadores objetivos pode dificultar a vinculação do pagamento público a resultados, qualidade e conformidade das entregas.

{% endif %}

#### Conclusão

As fragilidades evidenciadas na fase preparatória das contratações de TIC reduzem a segurança de que a organização disponha de controles suficientes para assegurar, conforme aplicável ao caso concreto, processo formal de contratação, participação técnica da área de TIC, alinhamento ao planejamento e adequada instrução dos processos. Essas fragilidades elevam o risco de contratações insuficientemente fundamentadas, pouco rastreáveis ou desalinhadas às necessidades institucionais, à complexidade e aos riscos das soluções de TIC pretendidas.

Em razão das lacunas descritas, são propostas recomendações preliminares voltadas à estruturação e à adequação dos aspectos da fase preparatória das contratações de TIC efetivamente apontados neste achado, observados os critérios aplicáveis indicados nas seções anteriores.

### Propostas de Encaminhamento
{% for e in achado.encaminhamentos %}
* **Comunicação com {{ e.tipo }}** para que {{ e.encaminhamento.rstrip('.;') }}{{ '.' if loop.last else ';' }}
{% endfor %}

{# Final do Achado - Contratações de TIC #}
{% endif %}
