{% set nome_achado = 'Capacidade institucional insuficiente para sustentar a gestão de TIC e segurança da informação' %}
{% set achado = auditado.get_achado_por_nome(nome_achado) %}
{% if achado %}
{% set situacao_forca = 'Ausência de força de trabalho dedicada à TIC ou à segurança da informação.' %}
{% set situacao_quantitativo = 'A organização não definiu o quantitativo necessário de pessoal de TIC e segurança da informação.' %}
{% set situacao_cargos = 'Ausência de cargos, funções, perfis ou ocupações específicas de TIC e segurança da informação.' %}
{% set situacao_perfis = 'Perfis profissionais de TIC e segurança da informação inexistentes, insuficientes ou não utilizados na escolha de gestores.' %}
{% set situacao_competencias = 'Lacunas de competências dos colaboradores e gestores de TIC e segurança da informação não são identificadas ou tratadas.' %}
{% set situacao_terceiros = 'Dependência externa relevante sem capacidade interna suficiente para coordenar e fiscalizar a TIC.' %}
{% set motivos_forca = auditado.get_motivos_situacao(nome_achado, situacao_forca) %}
{% set motivos_quantitativo = auditado.get_motivos_situacao(nome_achado, situacao_quantitativo) %}
{% set motivos_cargos = auditado.get_motivos_situacao(nome_achado, situacao_cargos) %}
{% set motivos_perfis = auditado.get_motivos_situacao(nome_achado, situacao_perfis) %}
{% set motivos_competencias = auditado.get_motivos_situacao(nome_achado, situacao_competencias) %}
{% set motivos_terceiros = auditado.get_motivos_situacao(nome_achado, situacao_terceiros) %}
{% set tem_forca = situacao_forca in achado.situacoes_encontradas and motivos_forca %}
{% set tem_quantitativo = situacao_quantitativo in achado.situacoes_encontradas and motivos_quantitativo %}
{% set tem_cargos = situacao_cargos in achado.situacoes_encontradas and motivos_cargos %}
{% set tem_perfis = situacao_perfis in achado.situacoes_encontradas and motivos_perfis %}
{% set tem_competencias = situacao_competencias in achado.situacoes_encontradas and motivos_competencias %}
{% set tem_terceiros = situacao_terceiros in achado.situacoes_encontradas and motivos_terceiros %}
{% set qtd_situacoes_exibidas = (1 if tem_forca else 0) + (1 if tem_quantitativo else 0) + (1 if tem_cargos else 0) + (1 if tem_perfis else 0) + (1 if tem_competencias else 0) + (1 if tem_terceiros else 0) %}

\newpage

## Achado {{ achado.numero }} – {{ achado.nome }}

### Critérios
{% if tem_cargos or tem_perfis %}
* COBIT 2019, APO01.05 - Estabelecer papéis e responsabilidades: definir, comunicar e manter papéis e responsabilidades relacionados à governança e gestão de TIC;
{% endif %}
{% if tem_forca or tem_quantitativo or tem_cargos or tem_perfis %}
* COBIT 2019, APO07.01 - Adquirir e manter pessoal adequado e apropriado: assegurar quantidade e perfil de profissionais compatíveis com as necessidades de TIC;
{% endif %}
{% if tem_cargos %}
* COBIT 2019, APO07.02 - Identificar pessoal-chave de TI: identificar funções e pessoas críticas para reduzir dependência individual, perda de conhecimento e descontinuidade;
{% endif %}
{% if tem_perfis or tem_competencias %}
* COBIT 2019, APO07.03 - Manter habilidades e competências do pessoal: identificar, desenvolver e manter competências necessárias à execução das responsabilidades de TIC;
{% endif %}
{% if tem_forca or tem_quantitativo %}
* COBIT 2019, APO07.05 - Planejar e monitorar o uso de recursos humanos de TI e de negócio: planejar, alocar e acompanhar capacidade de pessoal para iniciativas, operações e serviços de TIC;
{% endif %}
{% if tem_terceiros %}
* COBIT 2019, APO07.06 - Gerenciar pessoal contratado: controlar o uso de pessoal terceirizado ou externo, preservando responsabilização, supervisão e retenção de conhecimento;
* COBIT 2019, APO10.04 - Gerenciar risco de fornecedores: identificar e tratar riscos decorrentes de fornecedores, contratos e dependências externas relevantes para TIC;
* COBIT 2019, DSS01.02 - Gerenciar serviços de TI terceirizados: assegurar que serviços terceirizados sejam supervisionados, medidos e integrados aos controles da organização;
{% endif %}
{% if tem_forca or tem_perfis or tem_competencias %}
* ABNT NBR ISO/IEC 27001:2022, cláusulas 5.3 e 7.2: definir responsabilidades e autoridades para segurança da informação e assegurar competências necessárias às funções atribuídas;
{% endif %}
{% if tem_perfis or tem_competencias %}
* ABNT NBR ISO/IEC 27002:2022, controles 5.2 e 6.3: definir papéis e responsabilidades de segurança da informação e promover conscientização, educação e treinamento em segurança.
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

A capacidade institucional de TIC e segurança da informação pressupõe dispor de recursos humanos, competências, perfis profissionais, funções e vínculos contratuais adequados para planejar, coordenar, gerir, proteger, contratar, fiscalizar e sustentar o ambiente tecnológico. Sob a perspectiva de controle e governança, a estruturação formal de uma unidade de tecnologia deve ser acompanhada de capacidade técnica compatível para exercer a supervisão de suas atribuições estratégicas.

Os critérios de boas práticas indicam que a organização deve formalizar a designação de papéis e responsabilidades, assegurar o dimensionamento apropriado do quadro de pessoal, mapear funções críticas, capacitar periodicamente a equipe e supervisionar de forma estrita a atuação de prestadores de serviços externos[^explica_capacidade_tic].

Com base na análise das respostas aos itens 0101, 0105, 2701, 2702, 2703, 2704, 2705, 2706, 2708, 2801 e 2804 do questionário aplicado e da avaliação das evidências documentais anexadas, não foi demonstrada capacidade institucional suficiente para sustentar a gestão de TIC e segurança da informação. A Equipe de Auditoria identificou fragilidades nos seguintes aspectos:

{% if tem_forca %}
* **Força de trabalho dedicada**: a ausência de força de trabalho dedicada não demonstra aderência aos critérios de pessoal adequado, planejamento de recursos humanos e competências de segurança da informação (COBIT 2019, APO07.01/APO07.05 e ABNT NBR ISO/IEC 27001:2022, cláusulas 5.3 e 7.2), podendo comprometer a execução rotineira das atividades de planejamento, governança e sustentação operacional.
{% endif %}
{% if tem_quantitativo %}
* **Dimensionamento de pessoal**: a ausência de definição de parâmetros de pessoal não demonstra aderência aos critérios de planejamento de recursos humanos (COBIT 2019, APO07.01), elevando o risco de subdimensionamento ou má alocação da equipe técnica.
{% endif %}
{% if tem_cargos %}
* **Cargos e carreiras específicas**: a ausência de cargos, funções ou perfis técnicos estruturados não demonstra aderência às boas práticas de atração e retenção de pessoal (COBIT 2019, APO07.01), podendo reduzir a responsabilização e a continuidade da gestão tecnológica.
{% endif %}
{% if tem_perfis %}
* **Perfis profissionais**: a ausência ou inobservância de perfis profissionais mínimos para a escolha de gestores e técnicos não demonstra aderência às diretrizes de manutenção de competências (COBIT 2019, APO07.01/APO07.03 e ISO/IEC 27002:2022, 5.2/6.3), reduzindo a segurança de que os responsáveis possuam qualificação compatível com as funções exercidas.
{% endif %}
{% if tem_competencias %}
* **Lacunas de competência**: a ausência de identificação ou tratamento de lacunas de treinamento não demonstra aderência às recomendações de capacitação técnica (COBIT 2019, APO07.03 e ISO/IEC 27002:2022, 6.3), podendo fragilizar a operação de segurança e o gerenciamento de ativos de TIC.
{% endif %}
{% if tem_terceiros %}
* **Dependência externa**: a dependência externa relevante sem capacidade interna suficiente para coordenar e fiscalizar a TIC não demonstra aderência às boas práticas de gestão de pessoal contratado e terceirizações (COBIT 2019, APO07.06, APO10.04 e DSS01.02), elevando riscos à governabilidade técnica e à continuidade das atividades do órgão.
{% endif %}

{% if qtd_situacoes_exibidas == 1 %}
Essa situação ensejou o presente achado e será detalhada na subseção seguinte.
{% else %}
Essas situações ensejaram o presente achado e serão detalhadas nas subseções seguintes.
{% endif %}

[^explica_capacidade_tic]: Os critérios de capacidade institucional de TIC e segurança da informação concentram-se em pessoal adequado, competências, papéis, responsabilidades, retenção de conhecimento e supervisão de terceiros.

{% set situacao = situacao_forca %}
{% if tem_forca %}
#### Força de trabalho dedicada à TIC ou à segurança da informação

A organização deve dispor de força de trabalho dedicada à TIC e à segurança da informação, compatível com sua estrutura, porte, serviços prestados, sistemas mantidos, contratações e riscos relevantes.

O COBIT 2019, APO07.01 e APO07.05, orienta a manutenção de pessoal adequado e o planejamento e monitoramento da capacidade de recursos humanos. A ABNT NBR ISO/IEC 27001:2022, cláusulas 5.3 e 7.2, exige responsabilidades definidas e competências necessárias às funções atribuídas em segurança da informação.

Da análise das respostas ao item 0105 e da documentação apresentada, verificou-se que a existência de força de trabalho dedicada à TIC ou à segurança da informação compatível com as responsabilidades da organização não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
{% set refs_motivo = motivo.get('refs', []) -%}
* {{ motivo.texto.rstrip('.;') }}{% if refs_motivo %} ({{ refs_motivo | join(', ') }}){% endif %}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A inexistência ou insuficiência de profissionais dedicados, em quantitativo incompatível com a complexidade do ambiente tecnológico, pode comprometer a execução de rotinas essenciais de planejamento, gestão, segurança da informação, contratação, fiscalização contratual e sustentação das operações de TIC.

Diante disso, __será proposta recomendação para que a organização avalie sua força de trabalho dedicada à TIC e à segurança da informação e adote medidas proporcionais para assegurar capacidade de planejamento, gestão, proteção, contratação, fiscalização e sustentação da TIC.__

{% endif %}

{% set situacao = situacao_quantitativo %}
{% if tem_quantitativo %}
#### Quantitativo necessário de pessoal de TIC e segurança da informação

A definição do quantitativo necessário de pessoal permite avaliar se a força de trabalho disponível é compatível com as demandas, riscos e responsabilidades da organização.

O COBIT 2019, APO07.01 e APO07.05, exige que a organização assegure quantidade e perfil de profissionais compatíveis com as necessidades de TIC e planeje a alocação de recursos humanos para iniciativas, operações e serviços.

Da análise das respostas ao item 2703 e da documentação apresentada, verificou-se que a definição do quantitativo necessário de pessoal de TIC e segurança da informação com base em critério ou procedimento técnico não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
{% set refs_motivo = motivo.get('refs', []) -%}
* {{ motivo.texto.rstrip('.;') }}{% if refs_motivo %} ({{ refs_motivo | join(', ') }}){% endif %}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência de um dimensionamento técnico do quadro de pessoal priva a administração de bases objetivas para subsidiar decisões sobre contratações, provimentos, planos de capacitação ou o eventual compartilhamento de estruturas com outras organizações.

Diante disso, __será proposta recomendação para que a organização estime o quantitativo necessário de pessoal de TIC e segurança da informação, considerando porte, complexidade, serviços críticos, sistemas mantidos, contratações e riscos relevantes.__

{% endif %}

{% set situacao = situacao_cargos %}
{% if tem_cargos %}
#### Cargos, funções, perfis ou ocupações específicas de TIC e segurança da informação

Cargos, funções, gratificações, perfis ou ocupações específicas de TIC e segurança da informação ajudam a estruturar responsabilidades, atrair profissionais, definir requisitos mínimos e reduzir improvisação na alocação de pessoas.

O COBIT 2019, APO01.05, APO07.01 e APO07.02, orienta a definição de papéis e responsabilidades, a manutenção de pessoal adequado e a identificação de funções críticas de TI.

Da análise das respostas ao item 2708 e da documentação apresentada, verificou-se que a existência de cargos, funções, gratificações, perfis ou ocupações específicas de TIC e segurança da informação não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
{% set refs_motivo = motivo.get('refs', []) -%}
* {{ motivo.texto.rstrip('.;') }}{% if refs_motivo %} ({{ refs_motivo | join(', ') }}){% endif %}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A falta de estruturação e provimento de cargos públicos ou gratificações de representação técnica adequadas compromete a capacidade de atração, correta responsabilização e retenção de profissionais detentores de perfil compatível com as necessidades da área.

Diante disso, __será proposta recomendação para que a organização avalie a necessidade de instituir cargos, funções, gratificações, perfis ou ocupações específicas de TIC e segurança da informação, compatíveis com suas necessidades institucionais.__

{% endif %}

{% set situacao = situacao_perfis %}
{% if tem_perfis %}
#### Perfis profissionais de TIC e segurança da informação

A definição de perfis profissionais mínimos para gestores e colaboradores de TIC e segurança da informação é necessária para que as pessoas designadas possuam competências compatíveis com suas responsabilidades.

O COBIT 2019, APO01.05 e APO07.03, orienta a definição de papéis, responsabilidades e competências necessárias. A ABNT NBR ISO/IEC 27001:2022 também exige competências adequadas às funções atribuídas em segurança da informação.

Da análise das respostas aos itens 2701, 2702 e 2704 e da documentação apresentada, verificou-se que a definição ou utilização de perfis profissionais mínimos para gestores e colaboradores de TIC e segurança da informação não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
{% set refs_motivo = motivo.get('refs', []) -%}
* {{ motivo.texto.rstrip('.;') }}{% if refs_motivo %} ({{ refs_motivo | join(', ') }}){% endif %}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A designação de gestores ou técnicos sem a observância prévia de perfis profissionais bem delineados eleva o risco de indicação de colaboradores sem a qualificação requerida para conduzir atividades críticas da tecnologia da informação e da segurança cibernética.

Diante disso, __será proposta recomendação para que a organização defina perfis profissionais mínimos para gestores e colaboradores de TIC e segurança da informação e utilize esses perfis como referência para designação de responsáveis.__

{% endif %}

{% set situacao = situacao_competencias %}
{% if tem_competencias %}
#### Identificação e tratamento de lacunas de competências

A organização deve identificar periodicamente lacunas de competências dos gestores e colaboradores de TIC e segurança da informação e definir medidas de tratamento, como capacitação, realocação, provimento, apoio especializado, compartilhamento de estrutura ou contratação com transferência de conhecimento.

O COBIT 2019, APO07.03, orienta a manutenção de habilidades e competências necessárias à execução das responsabilidades de TIC. A ABNT NBR ISO/IEC 27002:2022, controles 5.2 e 6.3, reforça a definição de responsabilidades e a promoção de conscientização, educação e treinamento em segurança.

Da análise das respostas aos itens 2705 e 2706 e da documentação apresentada, verificou-se que a identificação ou o tratamento de lacunas de competências dos gestores e colaboradores de TIC e segurança da informação não se mostrou suficientemente demonstrado, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
{% set refs_motivo = motivo.get('refs', []) -%}
* {{ motivo.texto.rstrip('.;') }}{% if refs_motivo %} ({{ refs_motivo | join(', ') }}){% endif %}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

A ausência de diagnóstico regular sobre as competências internas e de planos para saneamento de lacunas operacionais impede que a equipe técnica acompanhe a evolução tecnológica e mitigue vulnerabilidades na administração de sistemas e infraestrutura.

Diante disso, __será proposta recomendação para que a organização realize diagnóstico periódico de lacunas de competências e estabeleça plano de tratamento, contemplando capacitação, realocação, provimento, apoio especializado, compartilhamento de estrutura ou contratação com transferência de conhecimento.__

{% endif %}

{% set situacao = situacao_terceiros %}
{% if tem_terceiros %}
#### Dependência externa e capacidade interna de coordenação e fiscalização

A utilização de terceiros ou de estrutura externa para execução de atividades de TIC não elimina a responsabilidade da organização pela coordenação, planejamento, aprovação técnica, fiscalização contratual e retenção de conhecimento.

O COBIT 2019, APO07.06, APO10.04 e DSS01.02, orienta o controle de pessoal contratado, a gestão de riscos de fornecedores e a supervisão de serviços terceirizados de TI, preservando responsabilização, medição, integração aos controles e retenção de conhecimento.

Da análise das respostas aos itens 0101 e 0105 e da documentação apresentada, verificou-se que a existência de capacidade interna para coordenar, planejar, fiscalizar e reter conhecimento quando a operação de TIC depende de terceiros ou de estrutura externa não se mostrou suficientemente demonstrada, em razão dos seguintes elementos identificados pela Equipe de Auditoria:

{% set motivos = auditado.get_motivos_situacao(nome_achado, situacao) -%}
{% if motivos %}

{% for motivo in motivos -%}
{% set refs_motivo = motivo.get('refs', []) -%}
* {{ motivo.texto.rstrip('.;') }}{% if refs_motivo %} ({{ refs_motivo | join(', ') }}){% endif %}{{ '.' if loop.last else ';' }}
{% endfor %}
{% endif %}

O estabelecimento de modelo operacional baseado predominantemente em recursos externos, sem capacidade interna suficiente de supervisão, pode reduzir a governabilidade técnica, a retenção de conhecimento e a continuidade das operações.

Diante disso, __será proposta recomendação para que a organização avalie seu modelo de operação de TIC e adote medidas proporcionais para assegurar capacidade interna suficiente de coordenação, planejamento, aprovação técnica, fiscalização contratual e retenção de conhecimento, especialmente quando a execução das atividades de TIC depender predominantemente de terceiros ou de estrutura externa.__

{% endif %}

#### Conclusão

As fragilidades identificadas na capacidade institucional de TIC e segurança da informação reduzem a segurança de que a organização disponha de pessoal, competências, papéis e mecanismos de supervisão suficientes para sustentar a gestão, a proteção, as contratações, a fiscalização e a continuidade dos serviços tecnológicos.

Diante do cenário efetivamente identificado, formula-se proposta de encaminhamento com vistas a recomendar à organização que promova a adequação de sua capacidade institucional de TIC e segurança da informação nas situações apontadas neste achado, conforme os critérios aplicáveis indicados nas seções anteriores.

### Propostas de Encaminhamento
{% for e in achado.encaminhamentos %}
* **Comunicação com {{ e.tipo }}** para que {{ e.encaminhamento }};
{% endfor %}

{# Final do Achado - Capacidade institucional de TIC e segurança da informação #}
{% endif %}
