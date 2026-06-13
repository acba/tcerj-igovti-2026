{% set nome_achado = 'Capacidade institucional insuficiente para sustentar a gestão de TIC e segurança da informação' %}
{% set achado = auditado.get_achado_por_nome(nome_achado) %}
{% if achado %}

\newpage

## Achado {{ achado.numero }} – {{ achado.nome }}

### Critérios
* COBIT 2019, APO01.05 - Estabelecer papéis e responsabilidades: definir, comunicar e manter papéis e responsabilidades relacionados à governança e gestão de TIC;
* COBIT 2019, APO07.01 - Adquirir e manter pessoal adequado e apropriado: assegurar quantidade e perfil de profissionais compatíveis com as necessidades de TIC;
* COBIT 2019, APO07.02 - Identificar pessoal-chave de TI: identificar funções e pessoas críticas para reduzir dependência individual, perda de conhecimento e descontinuidade;
* COBIT 2019, APO07.03 - Manter habilidades e competências do pessoal: identificar, desenvolver e manter competências necessárias à execução das responsabilidades de TIC;
* COBIT 2019, APO07.05 - Planejar e monitorar o uso de recursos humanos de TI e de negócio: planejar, alocar e acompanhar capacidade de pessoal para iniciativas, operações e serviços de TIC;
* COBIT 2019, APO07.06 - Gerenciar pessoal contratado: controlar o uso de pessoal terceirizado ou externo, preservando responsabilização, supervisão e retenção de conhecimento;
* COBIT 2019, APO10.04 - Gerenciar risco de fornecedores: identificar e tratar riscos decorrentes de fornecedores, contratos e dependências externas relevantes para TIC;
* COBIT 2019, DSS01.02 - Gerenciar serviços de TI terceirizados: assegurar que serviços terceirizados sejam supervisionados, medidos e integrados aos controles da organização;
* ABNT NBR ISO/IEC 27001:2022, cláusulas 5.3 e 7.2: definir responsabilidades e autoridades para segurança da informação e assegurar competências necessárias às funções atribuídas;
* ABNT NBR ISO/IEC 27002:2022, controles 5.2 e 6.3: definir papéis e responsabilidades de segurança da informação e promover conscientização, educação e treinamento em segurança.

### Evidências
{% for evidencia in achado.evidencias %}
* {{ evidencia }};
{% endfor %}

### Situação encontrada

A capacidade institucional de TIC e segurança da informação pressupõe dispor de recursos humanos, competências, perfis profissionais, funções e vínculos contratuais adequados para planejar, coordenar, gerir, proteger, contratar, fiscalizar e sustentar o ambiente tecnológico. Sob a perspectiva de controle e governança, a mera estruturação formal de uma unidade de tecnologia não supre a necessidade de equipe técnica interna minimamente dimensionada e capacitada para exercer a supervisão técnica de suas atribuições estratégicas.

Os critérios de boas práticas indicam que a organização deve formalizar a designação de papéis e responsabilidades, assegurar o dimensionamento apropriado do quadro de pessoal, mapear funções críticas, capacitar periodicamente a equipe e supervisionar de forma estrita a atuação de prestadores de serviços externos[^explica_capacidade_tic].

Com base na análise das respostas aos itens 0101, 0105, 2701, 2702, 2703, 2704, 2705, 2706, 2708, 2801 e 2804 do questionário aplicado e da avaliação das evidências documentais anexadas, constatou-se que a organização apresenta insuficiências na capacidade institucional requerida. A Equipe de Auditoria identificou fragilidades nos seguintes aspectos:

{% set situacao_forca = 'Ausência de força de trabalho mínima dedicada à TIC ou à segurança da informação.' %}
{% set situacao_quantitativo = 'A organização não definiu o quantitativo necessário de pessoal de TIC e segurança da informação.' %}
{% set situacao_cargos = 'Ausência de cargos, funções, perfis ou ocupações específicas de TIC e segurança da informação.' %}
{% set situacao_perfis = 'Perfis profissionais de TIC e segurança da informação inexistentes, insuficientes ou não utilizados na escolha de gestores.' %}
{% set situacao_competencias = 'Lacunas de competências dos colaboradores e gestores de TIC e segurança da informação não são identificadas ou tratadas.' %}
{% set situacao_terceiros = 'Modelo de operação de TIC predominantemente terceirizado ou externo, sem capacidade interna mínima declarada para coordenação, planejamento, aprovação técnica ou fiscalização das atividades críticas de TIC.' %}

{% if situacao_forca in achado.situacoes_encontradas %}
* **Força de trabalho dedicada**: a ausência de força de trabalho mínima contraria os critérios de pessoal adequado, planejamento de recursos humanos e competências de segurança da informação (COBIT 2019, APO07.01/APO07.05 e ABNT NBR ISO/IEC 27001:2022, cláusulas 5.3 e 7.2), inviabilizando a execução rotineira das atividades de planejamento, governança e sustentação operacional.
{% endif %}
{% if situacao_quantitativo in achado.situacoes_encontradas %}
* **Dimensionamento de pessoal**: a ausência de definição de parâmetros de pessoal contraria os critérios de planejamento de recursos humanos (COBIT 2019, APO07.01), acarretando subdimensionamento crônico ou má alocação da equipe técnica.
{% endif %}
{% if situacao_cargos in achado.situacoes_encontradas %}
* **Cargos e carreiras específicas**: a ausência de cargos técnicos estruturados contraria as boas práticas de atração e retenção de pessoal (COBIT 2019, APO07.01), reduzindo a responsabilização e a continuidade da gestão tecnológica.
{% endif %}
{% if situacao_perfis in achado.situacoes_encontradas %}
* **Perfis profissionais**: a ausência ou inobservância de perfis profissionais mínimos para a escolha de gestores e técnicos contraria as diretrizes de manutenção de competências (COBIT 2019, APO07.01/APO07.03 e ISO/IEC 27002:2022, 5.2/6.3), abrindo margem para a indicação de responsáveis sem a qualificação requerida.
{% endif %}
{% if situacao_competencias in achado.situacoes_encontradas %}
* **Lacunas de competência**: a ausência de identificação ou tratamento de lacunas de treinamento contraria as recomendações de capacitação técnica (COBIT 2019, APO07.03 e ISO/IEC 27002:2022, 6.3), fragilizando a operação de segurança e o gerenciamento de ativos de TIC.
{% endif %}
{% if situacao_terceiros in achado.situacoes_encontradas %}
* **Dependência de terceiros**: a execução predominantemente externa sem capacidade interna de supervisão contraria as boas práticas de gestão de pessoal contratado e terceirizações (COBIT 2019, APO07.06, APO10.04 e DSS01.02), resultando em perda de governabilidade técnica e riscos à continuidade das atividades do órgão.
{% endif %}

Essas situações ensejaram o presente achado e serão detalhadas nas seções subsequentes.

[^explica_capacidade_tic]: Os critérios de capacidade institucional de TIC e segurança da informação concentram-se em pessoal adequado, competências, papéis, responsabilidades, retenção de conhecimento e supervisão de terceiros.

{% set situacao = 'Ausência de força de trabalho mínima dedicada à TIC ou à segurança da informação.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Força de trabalho mínima dedicada à TIC ou à segurança da informação

A organização deve dispor de força de trabalho mínima dedicada à TIC e à segurança da informação, compatível com sua estrutura, porte, serviços prestados, sistemas mantidos, contratações e riscos relevantes.

O COBIT 2019, APO07.01 e APO07.05, orienta a manutenção de pessoal adequado e o planejamento e monitoramento da capacidade de recursos humanos. A ABNT NBR ISO/IEC 27001:2022, cláusulas 5.3 e 7.2, exige responsabilidades definidas e competências necessárias às funções atribuídas em segurança da informação.

A inexistência ou insuficiência de profissionais dedicados, em quantitativo incompatível com a complexidade do ambiente tecnológico, inviabiliza a execução de rotinas essenciais de planejamento, gestão, segurança da informação, contratação, fiscalização contratual e sustentação das operações de TIC.

Diante disso, __será proposta recomendação para que a organização avalie sua força de trabalho dedicada à TIC e à segurança da informação e adote medidas proporcionais para assegurar capacidade mínima de planejamento, gestão, proteção, contratação, fiscalização e sustentação da TIC.__

{% endif %}

{% set situacao = 'A organização não definiu o quantitativo necessário de pessoal de TIC e segurança da informação.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Quantitativo necessário de pessoal de TIC e segurança da informação

A definição do quantitativo necessário de pessoal permite avaliar se a força de trabalho disponível é compatível com as demandas, riscos e responsabilidades da organização.

O COBIT 2019, APO07.01 e APO07.05, exige que a organização assegure quantidade e perfil de profissionais compatíveis com as necessidades de TIC e planeje a alocação de recursos humanos para iniciativas, operações e serviços.

A ausência de um dimensionamento técnico do quadro de pessoal priva a administração de bases objetivas para subsidiar decisões sobre contratações, provimentos, planos de capacitação ou o eventual compartilhamento de estruturas com outras organizações.

Diante disso, __será proposta recomendação para que a organização estime o quantitativo mínimo necessário de pessoal de TIC e segurança da informação, considerando porte, complexidade, serviços críticos, sistemas mantidos, contratações e riscos relevantes.__

{% endif %}

{% set situacao = 'Ausência de cargos, funções, perfis ou ocupações específicas de TIC e segurança da informação.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Cargos, funções, perfis ou ocupações específicas de TIC e segurança da informação

Cargos, funções, gratificações, perfis ou ocupações específicas de TIC e segurança da informação ajudam a estruturar responsabilidades, atrair profissionais, definir requisitos mínimos e reduzir improvisação na alocação de pessoas.

O COBIT 2019, APO01.05, APO07.01 e APO07.02, orienta a definição de papéis e responsabilidades, a manutenção de pessoal adequado e a identificação de funções críticas de TI.

A falta de estruturação e provimento de cargos públicos ou gratificações de representação técnica adequadas compromete a capacidade de atração, correta responsabilização e retenção de profissionais detentores de perfil compatível com as necessidades da área.

Diante disso, __será proposta recomendação para que a organização avalie a necessidade de instituir cargos, funções, gratificações, perfis ou ocupações específicas de TIC e segurança da informação, compatíveis com suas necessidades institucionais.__

{% endif %}

{% set situacao = 'Perfis profissionais de TIC e segurança da informação inexistentes, insuficientes ou não utilizados na escolha de gestores.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Perfis profissionais de TIC e segurança da informação

A definição de perfis profissionais mínimos para gestores e colaboradores de TIC e segurança da informação é necessária para que as pessoas designadas possuam competências compatíveis com suas responsabilidades.

O COBIT 2019, APO01.05 e APO07.03, orienta a definição de papéis, responsabilidades e competências necessárias. A ABNT NBR ISO/IEC 27001:2022 também exige competências adequadas às funções atribuídas em segurança da informação.

A designação de gestores ou técnicos sem a observância prévia de perfis profissionais bem delineados eleva o risco de indicação de colaboradores sem a qualificação requerida para conduzir atividades críticas da tecnologia da informação e da segurança cibernética.

Diante disso, __será proposta recomendação para que a organização defina perfis profissionais mínimos para gestores e colaboradores de TIC e segurança da informação e utilize esses perfis como referência para designação de responsáveis.__

{% endif %}

{% set situacao = 'Lacunas de competências dos colaboradores e gestores de TIC e segurança da informação não são identificadas ou tratadas.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Identificação e tratamento de lacunas de competências

A organização deve identificar periodicamente lacunas de competências dos gestores e colaboradores de TIC e segurança da informação e definir medidas de tratamento, como capacitação, realocação, provimento, apoio especializado, compartilhamento de estrutura ou contratação com transferência de conhecimento.

O COBIT 2019, APO07.03, orienta a manutenção de habilidades e competências necessárias à execução das responsabilidades de TIC. A ABNT NBR ISO/IEC 27002:2022, controles 5.2 e 6.3, reforça a definição de responsabilidades e a promoção de conscientização, educação e treinamento em segurança.

A ausência de diagnóstico regular sobre as competências internas e de planos para saneamento de lacunas operacionais impede que a equipe técnica acompanhe a evolução tecnológica e mitigue vulnerabilidades na administração de sistemas e infraestrutura.

Diante disso, __será proposta recomendação para que a organização realize diagnóstico periódico de lacunas de competências e estabeleça plano de tratamento, contemplando capacitação, realocação, provimento, apoio especializado, compartilhamento de estrutura ou contratação com transferência de conhecimento.__

{% endif %}

{% set situacao = 'Modelo de operação de TIC predominantemente terceirizado ou externo, sem capacidade interna mínima declarada para coordenação, planejamento, aprovação técnica ou fiscalização das atividades críticas de TIC.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Capacidade interna mínima em modelo terceirizado ou externo

A utilização de terceiros ou de estrutura externa para execução de atividades de TIC não elimina a responsabilidade da organização pela coordenação, planejamento, aprovação técnica, fiscalização, tomada de decisão e retenção de conhecimento.

O COBIT 2019, APO07.06, APO10.04 e DSS01.02, orienta o controle de pessoal contratado, a gestão de riscos de fornecedores e a supervisão de serviços terceirizados de TI, preservando responsabilização, medição, integração aos controles e retenção de conhecimento.

O estabelecimento de modelo operacional baseado predominantemente em recursos externos, desprovido de capacidade interna de supervisão, transfere o controle de atividades críticas ao setor privado, acarretando perda de governabilidade técnica, fuga do conhecimento corporativo e risco à continuidade das operações.

Diante disso, __será proposta recomendação para que a organização avalie seu modelo de operação de TIC e adote medidas para assegurar capacidade interna mínima de coordenação, planejamento, aprovação técnica, fiscalização contratual, tomada de decisão e retenção de conhecimento, especialmente quando a execução das atividades de TIC depender predominantemente de terceiros ou de estrutura externa.__

{% endif %}

#### Conclusão

As fragilidades identificadas na capacidade institucional de TIC e segurança da informação comprometem a sustentabilidade da gestão, da proteção, das contratações, da fiscalização e da continuidade dos serviços tecnológicos da organização.

Diante do cenário exposto, formula-se proposta de encaminhamento com vistas a recomendar à organização que promova a adequação de sua capacidade institucional de TIC e segurança da informação, em alinhamento aos critérios normativos previstos no COBIT 2019 e nas diretrizes das normas ABNT NBR ISO/IEC 27001:2022 e ABNT NBR ISO/IEC 27002:2022.

### Propostas de Encaminhamento
{% for e in achado.encaminhamentos %}
* **Comunicação com {{ e.tipo }}** para que {{ e.encaminhamento }};
{% endfor %}

{# Final do Achado - Capacidade institucional de TIC e segurança da informação #}
{% endif %}
