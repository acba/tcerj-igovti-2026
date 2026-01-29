# PRD - Página Web do Índice de Governança de TI (iGovTI) - TCE-RJ

## 1. Visão Geral do Produto
O projeto consiste na criação de uma página web institucional para o Tribunal de Contas do Estado do Rio de Janeiro (TCE-RJ) dedicada ao **iGovTI** (Índice de Governança e Gestão de Tecnologia da Informação). O objetivo central é hospedar e dar publicidade aos arquivos da auditoria realizada nos municípios e órgãos estaduais, além de fornecer informações detalhadas sobre a metodologia, o questionário aplicado e suporte aos jurisdicionados.

A página servirá como o ponto central de referência para transparência sobre a governança de TI no estado, permitindo não apenas o download de arquivos, mas a visualização dinâmica de dados e comparativos.

## 2. Público-Alvo
*   **Jurisdicionados (Gestores Públicos e TI):** Interessados em entender a metodologia, acessar o questionário e consultar seus próprios resultados ou comparativos.
*   **Cidadãos e Sociedade Civil:** Interessados em transparência e controle social sobre a gestão de TI pública.
*   **Pesquisadores e Acadêmicos:** Interessados nos dados brutos e metodologia para estudos.
*   **Auditores do TCE-RJ:** Para referência centralizada de documentos públicos.

## 3. Objetivos
*   **Centralizar Informações:** Reunir todos os documentos, manuais e dados referentes ao iGovTI em um único local.
*   **Transparência:** Publicar os resultados da auditoria e a metodologia de cálculo de forma clara.
*   **Orientação:** Facilitar o entendimento dos jurisdicionados através de FAQs e Glossários.
*   **Interatividade:** Permitir a comparação entre entidades e visualização de evolução histórica.

## 4. Funcionalidades e Seções da Página

### 4.1. Home / Apresentação do Índice
*   **Descrição:** Texto introdutório explicando o que é o iGovTI, sua importância para a administração pública e o contexto da auditoria do TCE-RJ.
*   **Destaques:** Gráficos ou cards resumidos com os principais resultados do último ciclo (ex: média geral do estado).
*   **Busca Rápida:** Barra de busca global para localizar rapidamente um município ou órgão.

### 4.2. O Questionário
*   **Visualização e Download:** Disponibilizar o questionário utilizado na auditoria para download (PDF/Excel) ou visualização direta (navegável item a item).
*   **Estrutura:** Explicar brevemente as dimensões avaliadas (ex: Governança, Gestão, Sistemas, etc.) com seus respectivos metadados.

### 4.3. Metodologia de Cálculo
*   **Explicação Técnica:** Detalhar como o índice é calculado.
*   **Fórmulas e Pesos:** Apresentar de forma didática os pesos atribuídos a cada questão ou dimensão.
*   **Exemplo Prático:** Fornecer um exemplo de cálculo passo a passo com valores fictícios para facilitar o entendimento.
*   **Níveis de Maturidade:** Explicar a escala de classificação (ex: Inicial, Básico, Intermediário, Aprimorado) e normalização (ex: 0-100).

### 4.4. Repositório de Arquivos (Audit Files)
*   **Objetivo:** Hospedar os arquivos resultantes da auditoria de forma pesquisável.
*   **Funcionalidade:**
    *   Listagem organizada com filtros por Ano, Domínio, Tipo de Arquivo e Município/Órgão.
    *   **Preview:** Visualização prévia do arquivo no navegador quando possível.
    *   **Downloads:** Opção de download individual ou em lote.
*   **Metadados Mínimos por Arquivo:** ID, título, descrição, tipo de arquivo, município/órgão vinculado, ano de referência, domínios relacionados, tags, data de publicação, link de download e checksum.

### 4.5. Página do Jurisdicionado (Município/Órgão)
*   **Perfil da Entidade:** Página dedicada a exibir os resultados de um órgão ou município específico.
*   **Visualização de Dados:**
    *   Gráficos de Radar (Spider Chart) comparando as dimensões avaliadas.
    *   Séries temporais mostrando a evolução do índice ao longo dos anos.
*   **Comparativo:** Funcionalidade para comparar os resultados da entidade com a média do estado ou com outras entidades selecionadas (seleção múltipla).

### 4.6. Dados Abertos e API
*   **Objetivo:** Permitir o reuso dos dados por pesquisadores e sistemas externos.
*   **Formatos:** Disponibilizar arquivos em CSV e JSON contendo dados brutos e agregados.
*   **API:** (Opcional) Endpoints públicos para consulta automatizada de resultados por entidade.

### 4.7. Glossário
*   **Objetivo:** Definir termos técnicos de TI e de controle externo.
*   **Formato:** Lista alfabética pesquisável (ex: "Governança de TI", "PDTI", "PETI").

### 4.8. Dúvidas Frequentes (FAQ)
*   **Objetivo:** Responder às dúvidas mais comuns.
*   **Tópicos:** Envio de informações, periodicidade, cálculo do índice, consequências da não participação.

## 5. Requisitos Não Funcionais
*   **Acessibilidade:** Padrões e-MAG e WCAG 2.1 AA (contraste, teclado, leitor de tela).
*   **Responsividade:** Layout adaptável a mobile, tablet e desktop.
*   **Performance:** Carregamento otimizado com paginação e *lazy-loading* para previews e listas longas.
*   **Identidade Visual:** Manual de identidade visual do TCE-RJ.

## 6. Políticas de Publicação e Segurança
*   **Workflow:** O sistema deve suportar um fluxo de aprovação: Upload Interno -> Revisão -> Aprovação -> Publicação.
*   **Proteção de Dados:** Processo de *redaction* (supressão) de dados sensíveis antes da publicação pública.
*   **Termos de Uso:** Declaração visível sobre o uso dos dados públicos e limitações legais.

## 7. Infraestrutura e Monitoramento
*   **Arquitetura:** Sugere-se site estático (ex: gerador estático) para alta performance e segurança, consumindo uma API leve para dados dinâmicos.
*   **Analytics:** Implementação de ferramenta de monitoramento (ex: Matomo) para métricas de acesso e downloads.

## 8. Referências e Inspirações
O desenvolvimento deve ter como referência visual e estrutural os seguintes portais:
1.  **TCE-PE (iGovTI-PE):** [Link](https://www.tcepe.tc.br/internet/index.php/indice-de-governanca-e-de-gestao-de-tecnologia-da-informacao-em-pernambuco-igovti-tce-pe) - *Referência para níveis de maturidade.*
2.  **TCU (iESGo/iGG):** [Link](https://iesgo.tcu.gov.br/) - *Referência para dados abertos e planilhas.*