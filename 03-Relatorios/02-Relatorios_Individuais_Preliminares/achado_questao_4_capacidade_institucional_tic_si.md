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
{% set situacao_forca = 'Ausência de força de trabalho mínima dedicada à TIC ou à segurança da informação.' %}
{% set situacao_quantitativo = 'A organização não definiu o quantitativo necessário de pessoal de TIC e segurança da informação.' %}
{% set situacao_cargos = 'Ausência de cargos, funções, perfis ou ocupações específicas de TIC e segurança da informação.' %}
{% set situacao_perfis = 'Perfis profissionais de TIC e segurança da informação inexistentes, insuficientes ou não utilizados na escolha de gestores.' %}
{% set situacao_competencias = 'Lacunas de competências dos colaboradores e gestores de TIC e segurança da informação não são identificadas ou tratadas.' %}
{% set situacao_terceiros = 'Modelo de operação de TIC predominantemente terceirizado ou externo, sem capacidade interna mínima declarada para coordenação, planejamento, aprovação técnica ou fiscalização das atividades críticas de TIC.' %}
A partir da análise das informações fornecidas, verificou-se que a organização não demonstrou dispor de capacidade institucional mínima, em termos de força de trabalho, perfis profissionais, competências, funções e vínculos, para planejar, gerir, proteger, contratar, fiscalizar e sustentar a TIC e a segurança da informação de forma adequada às suas necessidades institucionais, pois a Equipe de Auditoria identificou fragilidades nos seguintes aspectos:{% if situacao_forca in achado.situacoes_encontradas %} força de trabalho mínima dedicada à TIC ou à segurança da informação;{% endif %}{% if situacao_quantitativo in achado.situacoes_encontradas %} definição do quantitativo necessário de pessoal;{% endif %}{% if situacao_cargos in achado.situacoes_encontradas %} cargos, funções, perfis ou ocupações específicas;{% endif %}{% if situacao_perfis in achado.situacoes_encontradas %} perfis profissionais e sua utilização na escolha de gestores;{% endif %}{% if situacao_competencias in achado.situacoes_encontradas %} identificação e tratamento de lacunas de competências;{% endif %}{% if situacao_terceiros in achado.situacoes_encontradas %} capacidade interna mínima diante de modelo terceirizado ou externo;{% endif %}.{% if situacao_forca in achado.situacoes_encontradas %} A ausência de força de trabalho mínima contraria os critérios de pessoal adequado, planejamento de recursos humanos e competências em segurança da informação, previstos no COBIT 2019, APO07.01 e APO07.05, e na ABNT NBR ISO/IEC 27001:2022, cláusulas 5.3 e 7.2, podendo inviabilizar o planejamento, a gestão, a proteção, a contratação, a fiscalização e a sustentação da TIC.{% endif %}{% if situacao_quantitativo in achado.situacoes_encontradas %} A ausência de definição do quantitativo necessário contraria os critérios de aquisição, manutenção, planejamento e monitoramento de pessoal de TIC, podendo causar subdimensionamento ou alocação inadequada da equipe.{% endif %}{% if situacao_cargos in achado.situacoes_encontradas %} A ausência de cargos, funções, perfis ou ocupações específicas contraria os critérios de papéis, responsabilidades, pessoal adequado e identificação de pessoal-chave, podendo reduzir a capacidade de atração, alocação, responsabilização e retenção de profissionais.{% endif %}{% if situacao_perfis in achado.situacoes_encontradas %} A inexistência, insuficiência ou não utilização de perfis profissionais contraria os critérios de definição de papéis, manutenção de competências e responsabilidades de segurança da informação, podendo levar à designação de gestores e colaboradores sem competências compatíveis com suas responsabilidades.{% endif %}{% if situacao_competencias in achado.situacoes_encontradas %} A ausência de identificação ou tratamento de lacunas de competências contraria os critérios de manutenção de habilidades e competências, responsabilidades de segurança da informação e educação e treinamento, podendo comprometer a execução de práticas mínimas de planejamento, gestão, segurança, contratação, fiscalização e sustentação de TIC.{% endif %}{% if situacao_terceiros in achado.situacoes_encontradas %} A dependência de terceiros sem capacidade interna mínima contraria os critérios de gestão de pessoal contratado, risco de fornecedores e serviços terceirizados de TI, podendo gerar perda de conhecimento, baixa governabilidade e risco de descontinuidade dos serviços.{% endif %}

A capacidade institucional de TIC e segurança da informação envolve a existência de pessoas, competências, perfis, funções e vínculos suficientes para sustentar atividades críticas de planejamento, gestão, proteção, contratação, fiscalização e operação. A mera existência formal de área de TIC não é suficiente quando a organização não dispõe de capacidade mínima para coordenar e supervisionar suas responsabilidades.

A organização deve conhecer sua força de trabalho, definir o quantitativo necessário, possuir cargos ou funções compatíveis, estabelecer perfis profissionais, identificar e tratar lacunas de competências e manter capacidade interna mínima mesmo quando utiliza terceiros ou estrutura externa.

Os critérios adotados indicam que a organização deve definir papéis e responsabilidades, assegurar quantidade e perfil adequados de pessoal, identificar pessoal-chave, manter habilidades e competências, planejar recursos humanos, controlar pessoal contratado e tratar riscos decorrentes de fornecedores e dependências externas[^explica_capacidade_tic].

Com base na análise das respostas aos itens 0101, 0105, 2701, 2702, 2703, 2704, 2705, 2706, 2708, 2801 e 2804 do questionário aplicado e da avaliação das evidências anexadas, conforme apontado na seção de Evidências, a Equipe de Auditoria constatou as seguintes deficiências na capacidade institucional de TIC e segurança da informação:

{% for situacao in achado.situacoes_encontradas %}
* **{{ situacao }}**
{% endfor %}

Essas situações ensejaram o presente achado e serão detalhadas nas seções subsequentes.

[^explica_capacidade_tic]: Os critérios de capacidade institucional de TIC e segurança da informação concentram-se em pessoal adequado, competências, papéis, responsabilidades, retenção de conhecimento e supervisão de terceiros.

{% set situacao = 'Ausência de força de trabalho mínima dedicada à TIC ou à segurança da informação.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Força de trabalho mínima dedicada à TIC ou à segurança da informação

A organização deve dispor de força de trabalho mínima dedicada à TIC e à segurança da informação, compatível com sua estrutura, porte, serviços prestados, sistemas mantidos, contratações e riscos relevantes.

O COBIT 2019, APO07.01 e APO07.05, orienta a manutenção de pessoal adequado e o planejamento e monitoramento da capacidade de recursos humanos. A ABNT NBR ISO/IEC 27001:2022, cláusulas 5.3 e 7.2, exige responsabilidades definidas e competências necessárias às funções atribuídas em segurança da informação.

A ausência de profissionais dedicados, ou quantitativo incompatível com a estrutura declarada, pode impedir a execução mínima de atividades de planejamento, gestão, proteção, contratação, fiscalização e sustentação da TIC.

Diante disso, __será proposta recomendação para que a organização avalie sua força de trabalho dedicada à TIC e à segurança da informação e adote medidas proporcionais para assegurar capacidade mínima de planejamento, gestão, proteção, contratação, fiscalização e sustentação da TIC.__

{% endif %}

{% set situacao = 'A organização não definiu o quantitativo necessário de pessoal de TIC e segurança da informação.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Quantitativo necessário de pessoal de TIC e segurança da informação

A definição do quantitativo necessário de pessoal permite avaliar se a força de trabalho disponível é compatível com as demandas, riscos e responsabilidades da organização.

O COBIT 2019, APO07.01 e APO07.05, exige que a organização assegure quantidade e perfil de profissionais compatíveis com as necessidades de TIC e planeje a alocação de recursos humanos para iniciativas, operações e serviços.

Sem estimativa do quantitativo mínimo necessário, a organização fica sem base objetiva para dimensionamento, alocação, contratação, capacitação ou compartilhamento de estrutura.

Diante disso, __será proposta recomendação para que a organização estime o quantitativo mínimo necessário de pessoal de TIC e segurança da informação, considerando porte, complexidade, serviços críticos, sistemas mantidos, contratações e riscos relevantes.__

{% endif %}

{% set situacao = 'Ausência de cargos, funções, perfis ou ocupações específicas de TIC e segurança da informação.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Cargos, funções, perfis ou ocupações específicas de TIC e segurança da informação

Cargos, funções, gratificações, perfis ou ocupações específicas de TIC e segurança da informação ajudam a estruturar responsabilidades, atrair profissionais, definir requisitos mínimos e reduzir improvisação na alocação de pessoas.

O COBIT 2019, APO01.05, APO07.01 e APO07.02, orienta a definição de papéis e responsabilidades, a manutenção de pessoal adequado e a identificação de funções críticas de TI.

A ausência desses instrumentos pode reduzir a capacidade de atração, alocação, responsabilização e retenção de profissionais com perfil compatível com as necessidades institucionais.

Diante disso, __será proposta recomendação para que a organização avalie a necessidade de instituir cargos, funções, gratificações, perfis ou ocupações específicas de TIC e segurança da informação, compatíveis com suas necessidades institucionais.__

{% endif %}

{% set situacao = 'Perfis profissionais de TIC e segurança da informação inexistentes, insuficientes ou não utilizados na escolha de gestores.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Perfis profissionais de TIC e segurança da informação

A definição de perfis profissionais mínimos para gestores e colaboradores de TIC e segurança da informação é necessária para que as pessoas designadas possuam competências compatíveis com suas responsabilidades.

O COBIT 2019, APO01.05 e APO07.03, orienta a definição de papéis, responsabilidades e competências necessárias. A ABNT NBR ISO/IEC 27001:2022 também exige competências adequadas às funções atribuídas em segurança da informação.

Quando perfis profissionais são inexistentes, insuficientes ou não utilizados na escolha de gestores, aumenta o risco de designação de responsáveis sem qualificação compatível com atividades críticas de TIC e segurança da informação.

Diante disso, __será proposta recomendação para que a organização defina perfis profissionais mínimos para gestores e colaboradores de TIC e segurança da informação e utilize esses perfis como referência para designação de responsáveis.__

{% endif %}

{% set situacao = 'Lacunas de competências dos colaboradores e gestores de TIC e segurança da informação não são identificadas ou tratadas.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Identificação e tratamento de lacunas de competências

A organização deve identificar periodicamente lacunas de competências dos gestores e colaboradores de TIC e segurança da informação e definir medidas de tratamento, como capacitação, realocação, provimento, apoio especializado, compartilhamento de estrutura ou contratação com transferência de conhecimento.

O COBIT 2019, APO07.03, orienta a manutenção de habilidades e competências necessárias à execução das responsabilidades de TIC. A ABNT NBR ISO/IEC 27002:2022, controles 5.2 e 6.3, reforça a definição de responsabilidades e a promoção de conscientização, educação e treinamento em segurança.

Sem diagnóstico e tratamento de lacunas, a organização pode não possuir competências suficientes para executar práticas mínimas de planejamento, gestão, segurança, contratação, fiscalização e sustentação de TIC.

Diante disso, __será proposta recomendação para que a organização realize diagnóstico periódico de lacunas de competências e estabeleça plano de tratamento, contemplando capacitação, realocação, provimento, apoio especializado, compartilhamento de estrutura ou contratação com transferência de conhecimento.__

{% endif %}

{% set situacao = 'Modelo de operação de TIC predominantemente terceirizado ou externo, sem capacidade interna mínima declarada para coordenação, planejamento, aprovação técnica ou fiscalização das atividades críticas de TIC.' %}
{% if situacao in achado.situacoes_encontradas %}
#### Capacidade interna mínima em modelo terceirizado ou externo

A utilização de terceiros ou de estrutura externa para execução de atividades de TIC não elimina a responsabilidade da organização pela coordenação, planejamento, aprovação técnica, fiscalização, tomada de decisão e retenção de conhecimento.

O COBIT 2019, APO07.06, APO10.04 e DSS01.02, orienta o controle de pessoal contratado, a gestão de riscos de fornecedores e a supervisão de serviços terceirizados de TI, preservando responsabilização, medição, integração aos controles e retenção de conhecimento.

Quando o modelo de operação é predominantemente terceirizado ou externo sem capacidade interna mínima declarada, a organização fica exposta à perda de conhecimento, baixa governabilidade, dependência excessiva e risco de descontinuidade dos serviços.

Diante disso, __será proposta recomendação para que a organização avalie seu modelo de operação de TIC e adote medidas para assegurar capacidade interna mínima de coordenação, planejamento, aprovação técnica, fiscalização contratual, tomada de decisão e retenção de conhecimento, especialmente quando a execução das atividades de TIC depender predominantemente de terceiros ou de estrutura externa.__

{% endif %}

#### Conclusão

As fragilidades identificadas na capacidade institucional de TIC e segurança da informação comprometem a sustentabilidade da gestão, da proteção, das contratações, da fiscalização e da continuidade dos serviços tecnológicos da organização.

Diante das situações apresentadas, será sugerida proposta de encaminhamento à organização para que promova a adequação de sua capacidade institucional de TIC e segurança da informação, alinhando-a aos critérios previstos no COBIT 2019 e nas normas ABNT NBR ISO/IEC 27001:2022 e ABNT NBR ISO/IEC 27002:2022.

### Propostas de Encaminhamento
{% for e in achado.encaminhamentos %}
* **Comunicação com {{ e.tipo }}** para que {{ e.encaminhamento }};
{% endfor %}

{# Final do Achado - Capacidade institucional de TIC e segurança da informação #}
{% endif %}
