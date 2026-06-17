# iGovTI 2026

Vocabulário compartilhado para avaliação de evidências e achados do questionário iGovTI 2026.

## Language

**Coluna de evidência**:
Campo do questionário em que o auditado anexa evidência documental para uma questão ou subitem específico.
_Avoid_: arquivo de evidência, upload, checklist

**Ação de verificação**:
Teste definido na matriz de procedimentos para avaliar uma informação requerida e identificar eventual situação encontrada ou achado.
_Avoid_: prompt, questão, coluna

**Prompt de avaliação de evidência**:
Instrução de análise usada para julgar se a evidência sustenta as afirmações do auditado associadas a uma coluna de evidência.
_Avoid_: checklist, ação de verificação

**Item afirmado**:
Alternativa, subitem ou prática declarada pelo auditado que deve ser confrontada com a evidência correspondente; itens não declarados não são positivados por inferência a partir da evidência.
_Avoid_: resposta bruta, achado

**Coluna candidata a prompt de achado**:
Coluna de evidência incluída no conjunto de prompts por estar associada, pela matriz de procedimentos, a uma ou mais informações requeridas que podem ensejar situação encontrada ou achado. A matriz seleciona a coluna; dentro dela, avaliam-se todos os itens afirmados pelo auditado que o pipeline enviar.
_Avoid_: ação candidata, subitem obrigatório

**Conjunto parcial de prompts**:
Conjunto de prompts que cobre apenas colunas de evidência selecionadas por critério de auditoria, sem representar a totalidade das evidências do questionário.
_Avoid_: catálogo incompleto, erro de prompt ausente

**Catálogo versionado de prompts**:
Artefato explícito que define quais colunas de evidência serão avaliadas e quais critérios de conformidade serão aplicados. A matriz de procedimentos orienta sua criação e conferência, mas não altera automaticamente seu conteúdo.
_Avoid_: geração implícita pela matriz, lista dinâmica

**Catálogo enxuto de prompts**:
Catálogo versionado de prompts que registra apenas a regra comum, os critérios da prática principal, os critérios por alternativa ou item detalhado e o formato de saída esperado.
_Avoid_: checklist extenso, matriz duplicada

**Julgamento binário de evidência**:
Regra de avaliação em que uma afirmação do auditado é classificada apenas como `conforme` ou `nao_conforme`, salvo falha técnica externa à evidência.
_Avoid_: inconclusivo, parcialmente conforme

**Conclusão de evidência**:
Registro JSON compatível com o pipeline que expressa o julgamento de um item afirmado, sua justificativa e os elementos de rastreabilidade usados na análise.
_Avoid_: resposta livre, parecer textual

**Linha do dashboard de avaliação**:
Representação visual de uma conclusão de evidência individual, enriquecida com metadados do processamento que a produziu.
_Avoid_: registro bruto, linha do JSONL

**Resposta avaliada no dashboard**:
Afirmação do auditado que foi efetivamente avaliada pelo pipeline e aparece em uma conclusão de evidência; não representa todas as respostas do questionário.
_Avoid_: resposta completa do questionário, base LimeSurvey

**Prática principal**:
Afirmação de adoção declarada na questão-base, distinta dos detalhamentos marcados pelo auditado. Sua conformidade depende de critérios próprios definidos para a questão, e não da soma automática dos subitens conformes.
_Avoid_: resumo dos detalhamentos, média dos subitens

**Critério da prática principal**:
Condição substantiva, definida por questão, para julgar a conformidade da afirmação de adoção da prática principal.
_Avoid_: critério automático, contagem de subitens

**Critério do item detalhado**:
Condição substantiva para julgar a conformidade de um subitem, alternativa ou detalhamento específico afirmado pelo auditado.
_Avoid_: critério geral da questão

**Suficiência documental mínima**:
Exigência comum de que a evidência sustente diretamente o item afirmado e contenha elemento verificável citável, como trecho, página, aba, linha, imagem, ato, ata, relatório, registro ou equivalente.
_Avoid_: plausibilidade, inferência ampla

**Alternativa declarada**:
Opção de resposta selecionada pelo auditado em uma questão de alternativa única; sua conformidade é julgada por critério específico da própria alternativa.
_Avoid_: prática principal, resposta textual

**Item sem exigência de evidência**:
Resposta ou subitem que pode compor achado pela regra da matriz, mas não deve gerar julgamento de evidência porque o questionário não solicita upload para essa condição.
_Avoid_: evidência negativa, prompt de ausência

**Item avaliável por evidência**:
Resposta, alternativa ou subitem que pode chegar ao pipeline porque aciona uma coluna de evidência no questionário; somente esses itens recebem critérios no prompt de avaliação de evidência.
_Avoid_: item de achado, item da matriz

**Evidência ausente**:
Condição em que o auditado afirma item avaliável por evidência, mas não envia o anexo esperado. Deve produzir julgamento `nao_conforme` para o item afirmado, em vez de simples ausência de análise.
_Avoid_: item ignorado, sem escopo

**Dashboard de avaliação de evidências**:
Artefato estático de visualização usado para explorar conclusões de evidência, estados de conformidade, auditados, questões, colunas de evidência e justificativas produzidas pelo pipeline.
_Avoid_: sistema de auditoria, fonte de verdade

**Grupo de comparação de modelos**:
Conjunto de conclusões de evidência referentes ao mesmo auditado, item afirmado e evidência, produzido por um ou mais modelos de avaliação para apoiar a revisão comparativa pelo analista.
_Avoid_: linha do JSONL, média dos modelos

**Consenso entre modelos**:
Situação em que dois ou mais modelos atribuem o mesmo estado substantivo a um grupo de comparação de modelos. Divergência ocorre quando há estados substantivos diferentes para o mesmo grupo.
_Avoid_: conclusão final de auditoria, decisão automática

**Arquivo estático de dashboard**:
Dashboard de avaliação de evidências distribuído como um único HTML, com dados iniciais embutidos e possibilidade de carregar outro `analyses.jsonl` local para exploração.
_Avoid_: aplicação web, backend
