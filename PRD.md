Projeto: Página iGovTI — índice de governança e gestão de TI

Visão geral

Este documento descreve o Product Requirements Document (PRD) para uma página web pública que hospedará os arquivos da auditoria realizada pelo TCE-RJ nos municípios e órgãos estaduais do Rio de Janeiro. O objetivo é avaliar e divulgar a adoção de práticas de gestão e governança de TI por meio do índice chamado iGovTI. O design informacional e funcionalidades seguirão referências do TCE-PE e do TCU:

- TCE-PE: https://www.tcepe.tc.br/internet/index.php/indice-de-governanca-e-de-gestao-de-tecnologia-da-informacao-em-pernambuco-igovti-tce-pe
- TCU: https://iesgo.tcu.gov.br/

Objetivos

- Tornar públicos e pesquisáveis os resultados da auditoria e seus arquivos.
- Explicar de forma transparente o questionário e a metodologia do iGovTI.
- Facilitar uso por gestores, pesquisadores e sociedade civil.

Público-alvo

- Gestores públicos (municípios e estado)
- Auditores e equipe técnica do TCE-RJ
- Pesquisadores e consultores
- Cidadãos, imprensa e organizações de controle social

Escopo funcional

Páginas e conteúdos essenciais:

- Home: resumo do índice, destaques e acesso rápido a municípios/órgãos.
- Questionário: apresentação item a item com explicações, versão para download.
- Metodologia: descrição técnica e resumo para leigos, fórmulas e exemplo de cálculo.
- Glossário: termos e definições.
- FAQ: dúvidas frequentes sobre o índice e uso dos dados.
- Repositório de documentos: listagem pesquisável e filtrável, previews e downloads.
- Dados abertos/API: endpoints e arquivos CSV/JSON para reuso.
- Página por município/órgão: resultados, gráficos, documentos vinculados.

Requisitos funcionais (resumido)

- Exibir questionário com agrupamentos e metadados.
- Publicar metodologia com fórmula do índice e exemplos.
- Repositório pesquisável com filtros (município/órgão, ano, domínio, tipo de arquivo).
- Downloads individuais e em lote; preview quando possível.
- API pública para extração de dados agregados e por entidade.

Requisitos não-funcionais (resumido)

- Acessibilidade WCAG 2.1 AA.
- Responsividade e compatibilidade com navegadores modernos.
- Performance com paginação e lazy-loading de previews.
- Segurança: site público apenas leitura; uploads via intranet controlada.

Metadados mínimos por documento

- id, título, descrição, tipo de arquivo, município/órgão, ano, domínios relacionados, tags, data de publicação, link de download, checksum.

Descrição do cálculo do iGovTI (diretrizes)

- Listar domínios e questões com pesos.
- Definir escala de normalização (por exemplo 0–100 por questão).
- Incluir fórmula matemática para agregação de itens e domínios e tratamento de faltantes.
- Fornecer um exemplo de cálculo passo a passo com valores fictícios.

UX e UI (principais decisões)

- Barra de busca global com filtros rápidos.
- Filtros persistentes no repositório.
- Página de entidade com gráficos (radar, séries temporais) e lista de documentos.
- Comparação entre entidades (seleção múltipla).

Busca e descoberta

- Busca full-text com destaque, ordenação por relevância/data/pontuação.
- Filtros por domínio, ano, município/órgão e tipo de arquivo.

Políticas de publicação e privacidade

- Workflow: upload interno → revisão → aprovação → publicação.
- Redaction de dados sensíveis antes da publicação.
- Declaração de uso de dados e termos legais visíveis no rodapé.

Infraestrutura sugerida

- Site estático (ex.: gerador estático) combinado com uma pequena API para dados dinâmicos, hospedagem em infraestrutura do tribunal ou nuvem governamental com CDN.

Monitoramento e analytics

- Implantar Matomo ou similar para métricas; coletar estatísticas de download e páginas mais acessadas.

Critérios de aceite

- Conteúdos (questionário, metodologia, glossário, FAQ, repositório) publicados e navegáveis.
- Busca e filtros funcionais.
- APIs retornando dados conforme especificação.
- Checklist de acessibilidade (WCAG AA) aprovado em testes básicos.

Riscos e mitigações

- Falta de clareza na metodologia → workshop técnico e notas metodológicas detalhadas.
- Publicação de dados sensíveis → processo de revisão e redaction.

Cronograma proposto

- Semana 1: alinhamento, coleta de arquivos e questionários.
- Semana 2: redação final do PRD e conteúdo (metodologia/questionário).
- Semana 3: implementação inicial do repositório e importação de documentos.
- Semana 4: testes, acessibilidade e publicação.

Próximos passos

- Validar este PRD com a equipe do TCE-RJ.
- Receber amostra dos questionários e documentos para modelagem de metadados.
- Definir responsável técnico para implantação.

Contato

Comissão de Auditoria de TI — TCE-RJ (incluir responsáveis e contatos).