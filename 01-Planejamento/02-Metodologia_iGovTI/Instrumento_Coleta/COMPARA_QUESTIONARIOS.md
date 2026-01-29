# Comparacao de Instrumentos (Questionarios) de Governanca e Gestao de TI

Este documento compara os instrumentos aplicados por:

- TCE-PE: `docs/referencias/tcepe/questionario-igoviti-tcepe-atualizado2025.pdf`
- TCE-RJ (municipios): `docs/referencias/tcerj/municipios/CAS-TI - Questionário de Governança e Gestão de TI.pdf`
- TCE-RJ (organizacoes estaduais / SETIC): `docs/referencias/tcerj/setic/01-Questionário de Governança e Gestão de TI.pdf`
- TCE-RS (municipios): `docs/referencias/tcers/tce-rs-levantamento-ti-municipios.pdf`

E propoe como evoluir o instrumento do RJ preservando comparabilidade historica (manter o nucleo do questionario anterior) e acrescentar pontos atuais.

---

## 1) Leitura rapida (executivo)

- TCE-RJ (municipios e SETIC) e TCE-PE usam um modelo de maturidade por pratica (escala de adocao), muito alinhado a levantamentos do TCU (iGG/iGovTI). Esses instrumentos cobrem governanca, gestao (planejamento, servicos, riscos/continuidade), seguranca da informacao, software/projetos e contratacoes.
- O instrumento do TCE-RJ aplicado no Executivo Estadual (SETIC) preserva o nucleo de governanca/gestao, mas adiciona um bloco especifico do contexto estadual: aderencia a normativos do SETIC/PRODERJ e avaliacao (percepcao/satisfacao) da atuacao do Diretor Geral do SETIC como indutor e integrador.
- TCE-RS (2025) e um levantamento/diagnostico mais enxuto e orientado a capacidade basica: estrutura/equipe de TI e governanca (PDTI, comite, controle interno e alinhamento). Ele e bom para diagnosticar “causas-raiz” (ausencia de area formal, equipe insuficiente, baixa capacidade de controle interno), mas nao substitui um instrumento de controles (seguranca, continuidade, gestao de servicos, contratacoes).
- Para uma fiscalizacao atual no RJ (Estado + municipios), a recomendacao e:
  - manter o nucleo do questionario do RJ para comparacao temporal;
  - ajustar alguns itens para refletir realidade 2026 (nuvem, ciber, cadeia de suprimentos, identidade/acesso);
  - adicionar um “modulo novo” (pontuado separadamente ou como subindice) para maturidade cibernetica/continuidade e governanca de terceiros;
  - manter perguntas “diagnosticas” do estilo TCE-RS (estrutura/equipe, posicionamento, capacidade de controle interno) como condicionantes/explicadores do desempenho.

---

## 2) Como cada instrumento se organiza

### 2.1 TCE-PE (iGovTI TCE-PE)

Caracteristicas:

- Instrumento de maturidade por pratica, com:
  - respostas em escala (Nao adota; Ha decisao/plano; Adota em menor parte; Adota parcialmente; Adota em maior parte/totalmente; Nao se aplica);
  - campo de evidencias (especialmente para adocao parcial/maior parte);
  - itens de “multiplas escolhas” para qualificar a resposta.
- Declaracao explicita de alinhamento ao iGG/TCU: o questionario referencia correspondencia com iGG 2021.
- Estrutura ampla (governanca/gestao/seguranca/contratacoes etc.) e, adicionalmente, menciona perguntas novas (ex.: sustentabilidade em TI e inteligencia artificial) e perguntas de perfil organizacional, algumas sem impacto no resultado.

Ponto forte: abrangencia e padronizacao; comparabilidade com referencias (TCU/iGG).

### 2.2 TCE-RJ (questionario aplicado a municipios)

Caracteristicas:

- Muito proximo do modelo do TCE-PE (escala de adocao + evidencias + itens qualificadores).
- Organiza por dominios/itens numerados e inclui, alem dos eixos classicos, um bloco de “Conformidade Externa” com foco municipal:
  - recepcao da Lei 14.129/2021 (Governo Digital);
  - Carta de Servicos;
  - processo administrativo eletronico/digital;
  - requisitos minimos de TI do SIAFIC;
  - integracao de sistemas cabiveis ao PNCP.
- Inclui ainda um item de “aderencia as notas tecnicas do TCE-RJ” em contratacoes de TI.

Ponto forte: mantem a base de governanca/gestao e agrega conformidades e integracoes relevantes ao contexto do RJ.

### 2.3 TCE-RJ (questionario aplicado a organizacoes estaduais / SETIC)

Caracteristicas:

- Mantem o modelo de maturidade por pratica (escala de adocao de 6 pontos + evidencias + itens qualificadores), muito proximo de PE/RJ (municipios).
- Estrutura por dominios numerados (ex.: 1100 Governanca; 2100 Gestao; 2200 Pessoas; 2300 Contratacoes) e inclui controles operacionais detalhados, como:
  - gestao de servicos (catalogo, mudancas, configuracao/ativos, incidentes, nivel de servico/ANS);
  - riscos e continuidade (riscos de TI e institucionais, continuidade de TI e de negocio);
  - seguranca da informacao (politica, comite, responsaveis/ETIR, riscos, controle de acesso, ativos/classificacao, incidentes, infraestrutura incluindo nuvem, conscientizacao);
  - software e projetos (processo de software; gestao de projetos);
  - contratacoes (riscos, desempenho, planejamento, processos de trabalho por fase, transparencia).
- Diferencial do contexto estadual (SETIC): bloco especifico para mapear o nivel setorial, incluindo:
  - existencia/organizacao do Setor de TI (NSTIC/RJ) e dados do gestor;
  - conhecimento e aderencia a normativos do Diretor Geral do SETIC (PRODERJ) (ex.: Portaria PRODERJ/PRE no 825/2021; IN PRODERJ/PRE no 01/2021; IN PRODERJ/PRE no 02/2022; IN PRODERJ/PRE no 03/2022);
  - questoes de avaliacao/percepcao do suporte, comunicacao e atuacao do Diretor Geral do SETIC (inclusive como integrador de solucoes) e situacao de hospedagem de sites/portais no PRODERJ.

Ponto forte: combina instrumento de maturidade (controles/processos) com afericao de conformidade e efetividade do arranjo de governanca estadual (SETIC).

### 2.4 TCE-RS (levantamento 2025)

Caracteristicas:

- Instrumento/relatorio de diagnostico com indice e 4 niveis de maturidade (Inicial/Basico/Aprimorado/Otimizado).
- Foco em duas dimensoes:
  - Estrutura e Equipe de TI: formalizacao da area, quantidade/composicao da equipe, posicionamento no organograma.
  - Governanca de TI: formalizacao do PDTI, formalizacao e funcionamento de comite/conselho, capacidade tecnica do controle interno para avaliar TI, percepcao de alinhamento estrategico.
- O relatorio ressalta riscos sistemicos associados a:
  - baixa formalizacao (responsabilidades difusas);
  - alta dependencia de terceirizados/vinculos precarios (rotatividade, perda de conhecimento e dependencia de fornecedores);
  - baixa capacidade interna de fiscalizar contratos/tecnologia.

Ponto forte: evidencia “fundacoes” e causas-raiz. Limitacao: pouco detalhamento de controles e processos operacionais (seguranca, continuidade, gestao de servicos, contratacoes) quando comparado a PE/RJ.

---

## 3) Pontos semelhantes (convergencias)

### 3.1 Convergencia de conteudo (o que todos tentam medir)

- TI como funcao estrategica: existencia de instancia decisoria (comite), planejamento (PDTI/plano de TI), alinhamento com objetivos e monitoramento pela alta administracao.
- Institucionalizacao: estruturas formais, definicao de papeis/responsabilidades, normativos e evidencias.
- Capacidade minima: equipe e posicionamento (mais explicito no RS) como precondicoes para maturidade.

### 3.2 Convergencia metodologica (como medem)

- PE e RJ (municipios e SETIC): escala de adocao por pratica + evidencias e itens qualificadores.
- RS: indice de maturidade por dimensao (4 niveis), com leitura mais “diagnostica” e menos “controle a controle”.

---

## 4) Diferencas relevantes (o que muda de um para outro)

### 4.1 Abrangencia e granularidade

- TCE-PE e TCE-RJ (municipios e SETIC) sao instrumentos de controles e processos (mais granulares):
  - gestao de servicos (catalogo, ANS, incidentes, mudancas, configuracao/ativos);
  - gestao de riscos (TI e institucional) e continuidade (negocio e TI);
  - seguranca da informacao (governanca e controles tecnicos: inventario, vulnerabilidades, logs, backup/testes etc.);
  - contratacoes (planejamento, riscos, desempenho, transparencia);
  - software/projetos (ciclo de vida, qualidade, requisitos de seguranca/interoperabilidade/acessibilidade).

- TCE-RS e um instrumento de base (menos granularity):
  - estrutura/equipe e governanca (PDTI, comite, controle interno, alinhamento).
  - excelente para explicar por que um municipio nao consegue evoluir, mas insuficiente para qualificar maturidade operacional.

### 4.2 Enfoque “municipal” e conformidade externa

- TCE-RJ (municipios) incorpora explicitamente conformidades/integracoes do contexto brasileiro recente:
  - Governo Digital (Lei 14.129/2021) e medidas concretas;
  - processo administrativo digital;
  - SIAFIC (requisitos minimos de TI) e PNCP.

- TCE-RJ (SETIC) incorpora explicitamente conformidades do arranjo estadual (PRODERJ como Diretor Geral do SETIC), cobrando conhecimento e aderencia a atos/normas e a operacionalizacao associada (p. ex. PEDTIC, procedimentos de contratacao e seguranca), alem de medir percepcao/satisfacao quanto a comunicacao, apoio/orientacao e integracao de solucoes pelo PRODERJ.

- TCE-PE enfatiza comparabilidade com o iGG/TCU e sinaliza perguntas adicionais recentes (ex.: sustentabilidade em TI e IA).

- TCE-RS trabalha com recortes por porte populacional (IBGE) e usa isso para interpretar maturidade e desigualdades de capacidade.

### 4.3 Natureza do resultado

- PE/RJ (municipios e SETIC): pontuacao por pratica e potencial para subindices por dominio; facilita benchmark e plano de acao por processo.
- RS: pontuacao por dimensao “macro”; favorece narrativa de capacidade e definicao de politicas de apoio/orientacao.

---

## 5) O que priorizar numa fiscalizacao atual no RJ (Estado + municipios)

O criterio aqui e materialidade (impacto em servicos essenciais), exposicao (ameacas atuais), e capacidade de implementacao (controles basicos primeiro).

### 5.1 Prioridade 1: ciberseguranca operacional + resposta a incidentes

Justificativa:

- A ameaca mais provavel e mais danosa hoje (ransomware, vazamento, indisponibilidade) se materializa quando faltam controles basicos e governanca de resposta.
- Os questionarios do TCE-RJ (municipios e SETIC) ja contem muitos elementos (politica, riscos, incidentes, logs, vulnerabilidades, backup/testes), o que permite medir evolucao.

Componentes recomendados como foco (e evidencias tipicas):

- Inventario de ativos e software; controle de configuracoes.
- Gestao de vulnerabilidades e atualizacoes (processo, SLA interno, evidencia de ciclos).
- Logs e monitoramento (centralizacao, retencao, analise de eventos relevantes).
- Backup com testes de restauracao (incluindo protecao contra ransomware, segregacao e testes periodicos).
- Gestao de incidentes e ETIR/estrutura equivalente (ponto de contato, procedimentos, escalonamento, exercicios e lessons learned).

### 5.2 Prioridade 2: continuidade (negocio e TI) e gestao de riscos

Justificativa:

- Sem BIA/PCN/planos e testes, incidentes viram interrupcao prolongada de servicos criticos (saude, arrecadacao, folha, assistencia social, educacao).
- A governanca de riscos cria disciplina de priorizacao e tratamento.

Componentes:

- Politica e processo institucional de gestao de riscos (incluindo riscos criticos) + integracao com TI.
- Continuidade do negocio (BIA, PCN, testes e revisoes).
- Continuidade de servicos de TI (planos, testes, integracao com continuidade institucional).

### 5.3 Prioridade 3: contratacoes de TI (planejamento, riscos, desempenho e transparencia)

Justificativa:

- Grande parcela da entrega de TI no setor publico depende de terceiros; falhas em planejamento e gestao contratual geram desperdicio, dependencia tecnologica e servicos ruins.
- O TCE-RS destaca a dependencia de terceirizados e a baixa capacidade interna como vulnerabilidade.

Componentes:

- Gestao de riscos nas contratacoes (por contratacao e por servicos continuados).
- Criterios e metricas de desempenho (SLA/indicadores, vinculo a resultados quando aplicavel).
- Avaliacao de vantajosidade em prorrogacoes.
- Publicacao/transparencia de documentos do ciclo de contratacao (respeitado sigilo legal).

### 5.4 Prioridade 4: fundacoes (estrutura/equipe e governanca) como “causa-raiz”

Justificativa:

- O que o TCE-RS chama de “informalidade” e “dependencia de vinculos precarios” e um forte preditor de fragilidade em seguranca, continuidade e capacidade de fiscalizar contratos.
- No RJ, isso funciona como eixo explicativo para diferenciar incapacidade estrutural de falta de gestao.

Componentes:

- Area de TI formalmente instituida e posicionamento adequado no organograma.
- Quantidade e composicao minima do corpo tecnico (efetivos x terceirizados) e estrategia de retencao de conhecimento.
- PDTI/plano de TI vigente e conectado a orcamento e plano de contratacoes.
- Comite/conselho de TI funcionando (pautas, decisoes, acompanhamento).
- Capacidade do controle interno para auditar TI (competencias e rotinas).

### 5.5 Prioridade 5 (municipios): governo digital e integracoes nacionais

Justificativa:

- Sao temas normativos e de entrega ao cidadao; reduzem retrabalho, melhoram integridade de dados e transparência.

Componentes:

- Lei 14.129/2021 (governo digital): medidas locais e governanca.
- Carta de Servicos e qualidade do servico digital (interoperabilidade/usabilidade/acessibilidade).
- Processo administrativo digital.
- SIAFIC (requisitos minimos de TI) e integracao ao PNCP.

### 5.6 Prioridade 6 (Estado/SETIC): governanca do arranjo setorial e conformidade com normativos do Diretor Geral

Justificativa:

- No Executivo Estadual, o SETIC e um componente material do modelo de governanca: capacidade de induzir padroes, orientar setoriais e integrar solucoes.

Componentes:

- Conhecimento e atendimento a atos/normas do SETIC/PRODERJ (ex.: PGTIC/EGTIC/PEDTIC; procedimentos de contratacao e seguranca; regras de sites/portais quando aplicavel).
- Medidas de efetividade do arranjo (comunicacao, suporte/orientacao, integracao de solucoes, canais de atendimento) como variaveis explicativas de maturidade.

---

## 6) O que pode ser deixado em segundo plano (se precisar reduzir escopo)

Essa secao nao diz “nao fazer”; diz “nao colocar como eixo principal do ciclo”, especialmente quando controles basicos ainda estao ausentes.

- Sustentabilidade ambiental em TI (ex.: criterios verdes em aquisicao/descarte) como eixo principal: importante, mas tipicamente tem menor impacto imediato que ciber/continuidade/contratos.
- Inteligencia artificial (governanca de IA) como eixo principal: relevante, mas melhor como modulo adicional (com foco em uso real, riscos e privacidade), pois muitos entes ainda estao no basico de seguranca e continuidade.
- Itens muito finos de gestao de pessoas (ex.: avaliacao individual formal) como centro do indice: util para maturidade, mas raramente e o fator que derruba servicos ou causa dano material imediato.

---

## 7) Recomendacao para evoluir o questionario do RJ sem perder comparabilidade

Premissa do RJ: continuar na linha do instrumento anterior para permitir comparacao de evolucao.

### 7.1 Estrategia de versionamento (para comparacao ao longo do tempo)

Proposta:

1) Congelar um “Nucleo 1.0” (itens historicos) e manter as perguntas e regras de pontuacao sem mudancas relevantes.
2) Criar “Modulos 2.0” adicionados:
   - pontuados separadamente (subindice) OU
   - marcados como “nao impacta o indice historico” no primeiro ciclo, para amadurecer series.
3) Ao apresentar resultados publicos, exibir:
   - indice historico (comparavel com anos anteriores);
   - subindices novos (ciber/terceiros/nuvem etc.) e, quando houver serie, comparar neles.

Isso evita que a evolucao aparente seja “artefato” de mudanca de instrumento.

### 7.2 Ajustes recomendados no nucleo (sem mudar o conceito do item)

Objetivo: manter a essencia do que ja era medido, mas atualizar evidencias e linguagem.

- Seguranca (controles tecnicos): explicitar evidencias minimas atuais sem alterar o “que” se mede.
  - Ex.: backup “com teste de restauracao” (ja aparece) pode ganhar qualificadores como frequencia de teste, segregacao e protecao contra ransomware.
- Gestao de incidentes: reforcar exercicios e tempo de resposta/registro de lições aprendidas.
- Vulnerabilidades/logs: incluir “monitoramento e analise” como parte do “adota em maior parte”, evitando que apenas “tem ferramenta” conte como maturidade.
- Contratacoes: explicitar gestao de riscos em cadeia (fornecedores/subcontratados) e dependencia tecnologica, coerente com o item de “mitigar risco de dependencia”.

### 7.3 Novos pontos a acrescentar (modulos sugeridos)

#### Modulo A: Identidade e Acesso (IAM/PAM)

Por que: identidade e o novo perimetro; e onde muitos incidentes comecam.

Sugestoes de itens:

- MFA para acessos privilegiados e remotos.
- Gestao de privilegios administrativos (PAM ou controles compensatorios) e segregacao de funcoes.
- Processo de concessao/revogacao de acesso (onboarding/offboarding) e revisoes periodicas.

#### Modulo B: Nuvem e terceirizacao (governanca e risco)

Por que: migracao para nuvem e servicos gerenciados aumenta superficie de risco e dependencia.

Sugestoes:

- Inventario de servicos em nuvem e contratos associados; definicao de responsabilidades (shared responsibility).
- Requisitos minimos de seguranca para contratos em nuvem (logs, criptografia, backups, localizacao, continuidade).
- Avaliacao e monitoramento de risco de fornecedores criticos.

#### Modulo C: Observabilidade e resposta (deteccao)

Por que: sem deteccao, o ente so descobre incidente quando ja houve impacto.

Sugestoes:

- Centralizacao de logs de sistemas criticos e retencao minima.
- Procedimentos de triagem/analise e criterios de escalonamento.
- Exercicios de mesa e melhoria continua.

#### Modulo D: Governanca de dados (LGPD aplicada)

Por que: a gestao municipal/estadual e intensiva em dados pessoais sensiveis.

Sugestoes:

- Classificacao de informacoes/dados e rotulagem aplicada aos sistemas criticos.
- Processo de atendimento a incidentes envolvendo dados pessoais (interface com juridico/encarregado).
- Medidas minimas de protecao para bases sensiveis (saude/assistencia/folha).

#### Modulo E: Software e cadeia de suprimentos (seguranca no ciclo)

Por que: vulnerabilidades em software e dependencias (inclusive open source) sao vetor frequente.

Sugestoes:

- Requisitos de seguranca no ciclo de vida (S-SDLC/DevSecOps de forma proporcional).
- Gestao de dependencias e atualizacoes (SBOM quando aplicavel; ao menos inventario de componentes).

### 7.4 Incorporar “diagnosticos” do TCE-RS como variaveis explicativas

Mesmo mantendo o instrumento RJ como nucleo, vale adicionar (ou reforcar) perguntas curtas e objetivas que expliquem resultados:

- Formalizacao da area de TI e seu posicionamento (subordinacao e autonomia).
- Quantitativo e composicao do time (efetivos/terceirizados) e rotatividade.
- Capacidade do controle interno para auditar TI/contratos.

Essas variaveis ajudam a interpretar por que certos controles nao avancam e orientam a estrategia de apoio/orientacao (especialmente para municipios pequenos).

---

## 8) Observacoes para aplicacao RJ (Estado + municipios)

- Separar o que e “comum a todos” (nucleo) do que e “especifico de municipio” (Lei 14.129, Carta de Servicos, SIAFIC, PNCP) e do que e “especifico de Estado/SETIC” (conformidade com normativos do SETIC/PRODERJ e afericao da efetividade do Diretor Geral como indutor/integrador). Para o Estado, manter equivalentes (ex.: servicos digitais ao cidadao, processos digitais), mas ajustar a redacao e as referencias normativas.
- Manter o modelo de exigencia de evidencias e, quando possivel, orientar o tipo de evidencia aceitavel (ato normativo, plano aprovado, ata de comite, relatorio de teste de backup, evidencias de logs, etc.).
- Evitar transformar “existencia de ferramenta” em maturidade. Preferir itens que cobrem processo (rotina, criterio, revisao, evidencia de execucao).

---

## 9) Proximo passo (se quiser operacionalizar)

Eu posso elaborar uma proposta de “RJ vNext” em formato de diff, listando:

- itens do nucleo (inalterados);
- itens ajustados (mudancas pequenas de evidencias/qualificadores);
- itens novos (modulos A-E), com sugestao de:
  - se pontua no indice historico ou em subindice;
  - evidencias minimas;
  - aplicabilidade: Estado, Municipios, ou ambos.
