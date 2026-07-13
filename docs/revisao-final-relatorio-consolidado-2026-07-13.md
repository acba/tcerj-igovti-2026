# Parecer de revisão final do Relatório Consolidado iGovTI 2026

**Relatório avaliado:** `03-Relatorios/01-Relatorio_Consolidado/Relatório_altaresolucao_novo.md`  
**Data e hora da avaliação:** 13/07/2026, às 11:10:20 (UTC−03:00, America/Sao_Paulo)  
**Escopo:** revisão integral do relatório, exceto o conteúdo da Seção 5, ainda mantida como template. Foram consideradas as repercussões da pendência dessa seção sobre as demais partes do documento.  
**Natureza:** parecer técnico de revisão; não substitui a deliberação da Equipe de Auditoria nem a revisão jurídica competente.

## Conclusão

O relatório ainda não está em condições de ser submetido à assinatura. A redação geral é organizada e os principais números do iGovTI reproduzem os artefatos estatísticos do repositório, mas há riscos metodológicos e probatórios capazes de provocar contestação dos auditados, refazimento dos resultados e perda de credibilidade perante o Plenário.

## Questões impeditivas à assinatura

### 1. Resultados baseados em pré-análise de IA sem revisão humana registrada — criticidade crítica

O relatório afirma que a Equipe analisou e validou as evidências, com alteração de 1.964 respostas e rebaixamento de 18 organizações (linhas 153 e 290-292). Entretanto:

* os 4.597 pareceres de `pareceres_consolidados.xlsx` estão marcados com `opiniao_auditoria = nao`;
* as 1.966 linhas da planilha `ajustes_respostas_questionario_pos_avaliacao_evidencias.xlsx` têm vazios os campos “Avaliação do auditor revisor” e “Justificativa do auditor revisor”;
* o manual da automação qualifica expressamente o resultado como pré-análise que deve ser revista por auditor humano.

Não é possível atribuir esses juízos à Equipe de Auditoria sem registro de revisão. Deve-se revisar e homologar os ajustes — sobretudo os que geram achado ou alteram nível de maturidade —, preencher os campos próprios, documentar a amostragem e a supervisão e informar no relatório o uso de IA, os controles aplicados e a responsabilidade humana pela conclusão.

### 2. Revisão metodológica substantiva não resolvida — criticidade crítica

O papel de trabalho `02-Execucao/03-Execucao_Procedimentos/04-Revisoes_Metodologicas/revisao-proporcionalidade-achados-4-5-6.md` recomenda reformular substancialmente os Achados 4 e 6 e ajustar o Achado 5, devido a riscos de falsos positivos, dupla contagem, falta de proporcionalidade e conclusões que o questionário não permite sustentar.

O mapa executado ainda contém integralmente as lógicas criticadas. As incidências de 100% no Achado 4, 100% no Achado 5 e 99,1% no Achado 6 não são defensáveis enquanto a Equipe não decidir formalmente sobre essa revisão. É necessário acolher ou rejeitar motivadamente cada proposta, atualizar o mapa e a matriz, reexecutar a auditoria e regenerar tabelas, gráficos, matriz de achados e relatórios.

### 3. Achado 4 extrapola o alcance do questionário — criticidade crítica

O relatório conclui que 113 organizações têm “capacidade institucional insuficiente” (linhas 495-506). O papel de trabalho registra que o questionário não permite avaliar suficiência material do quadro, produtividade, criticidade da terceirização, qualidade da fiscalização, retenção de conhecimento ou capacidade de estruturas compartilhadas.

O título e a conclusão transformam ausência de formalização em insuficiência material. Recomenda-se adotar título mais aderente — “Fragilidades no planejamento da força de trabalho e das competências de TIC e segurança da informação” — e recalcular a ocorrência com a lógica revisada.

### 4. Achado 6 afirma fatos sobre contratações concretas que não foram coletados — criticidade crítica

O relatório declara que houve contratações sem alinhamento, aprovação técnica ou equipe formal (linhas 521-532). A revisão metodológica demonstra que o questionário não identifica sequer se houve contratação no período, nem valor, risco, rito simplificado, contratação centralizada ou exceção justificada.

Devem-se substituir afirmações sobre contratações realizadas por formulações sobre regras e processos demonstrados, a exemplo de “a organização não demonstrou possuir regra geral que assegure...”. Também devem ser removidos os gatilhos sem suporte, com posterior reexecução do achado.

### 5. Contraditório pendente, mas tratado como concluído — criticidade crítica

O resumo emprega a formulação “Após o contraditório” (linha 90); a metodologia afirma que as manifestações “foram posteriormente apreciadas” (linha 170); e a Seção 4.6 relata manifestações já recebidas. A Seção 5, porém, ainda é um template.

Antes da assinatura, devem-se incorporar as manifestações e novas evidências, efetuar a reavaliação, aplicar os ajustes reversos aprovados, recalcular índices e achados e atualizar todas as estatísticas. Até isso ocorrer, o relatório deve empregar tempo futuro e identificar os resultados como anteriores aos comentários do gestor.

### 6. Geração do relatório não é reprodutível com os padrões atuais — criticidade crítica

A execução padrão de `scripts/gerar_relatorio_consolidado.py` falha porque `scripts/resources/igovti_dados_utils.py` aponta para `20260621-respostas-questionario.xlsx`, arquivo inexistente. Com o arquivo correto, a geração termina com três avisos de recursos ausentes:

* `achados_vs_igovti_2026.png`;
* `correlacao_achados_notas_igovti_2026.png`;
* `situacoes_mais_frequentes_igovti_2026.png`.

É necessário corrigir os caminhos padrão e incluir `03-Relatorios/99-Avaliacao_IgovTi_Achados/img` entre os recursos. O DOCX existente no repositório também está defasado e contém uma mídia de tamanho zero. O documento deve ser regenerado e todas as imagens incorporadas devem ser verificadas antes da assinatura.

## Riscos elevados de contestação

### 7. Comparação longitudinal interpretada como deterioração institucional

O texto reconhece que 2026 teve validação documental mais abrangente e que os índices não são diretamente comparáveis, mas conclui por “deterioração relevante” e destaca “regressões” (linhas 372-427). Isso excede o que os dados permitem.

Recomenda-se substituir “deterioração” por “redução nos indicadores ajustados”, esclarecendo que não é possível separar mudança institucional do efeito da validação documental e das alterações de respondente, contexto e instrumento.

### 8. Inexistência de limiar para classificar avanço e regressão

As 68 organizações foram divididas em 32 avanços e 36 regressões, sem casos estáveis. A menor variação absoluta é 0,000791. Com tolerância de 0,01, nove casos seriam estáveis; com tolerância de 0,05, seriam 24. A classificação atual transforma qualquer diferença numérica em evolução material.

Deve-se justificar um limiar de materialidade ou apresentar a variação de forma contínua, reservando “avanço” e “regressão” para mudanças de faixa ou diferenças superiores ao limiar definido.

### 9. Circularidade na Seção 4.4

O iGovTI e os achados derivam largamente das mesmas respostas ajustadas. A correlação negativa é, em parte, estrutural, e não uma validação independente. Não foram apresentados significância, intervalos de confiança, diagnóstico da distribuição ou controle dessa dependência (linhas 534-572).

A análise deve ser qualificada como exploratória e descritiva, com explicitação da fonte comum dos indicadores. Deve-se retirar a expressão “carga incompatível com a maturidade esperada”, pois não foi definido modelo de valor esperado.

### 10. “Materialidade” confundida com frequência

As linhas 251 e 742 tratam grande incidência como prova de materialidade. Frequência demonstra extensão; materialidade exige relevância, magnitude ou consequência.

Recomenda-se empregar “abrangência”, “recorrência” ou “incidência”. A materialidade somente deve ser afirmada quando houver critério e avaliação próprios.

### 11. Efetividade não testada

A limitação admite ausência de testes locais (linhas 126-132), mas o texto conclui sobre efetividade de mecanismos, atuação efetiva de comitês e operação reativa.

Devem-se empregar formulações como “não demonstrou documentalmente”, “não foram apresentados registros suficientes” e “não foi possível confirmar”, distinguindo desenho ou formalização, funcionamento documentado e efetividade operacional.

### 12. Afirmação inexata sobre evidências em “todos os itens”

A nota da linha 380 afirma que foram solicitadas e avaliadas evidências para todos os itens. O próprio questionário distingue itens com submissão obrigatória daqueles cujas evidências apenas deveriam permanecer disponíveis.

Redação sugerida: “Em 2026, a solicitação e a avaliação documental tiveram abrangência superior à do ciclo anterior, nos itens definidos pela metodologia.”

### 13. Objetivo declarado como plenamente atendido apesar de seis não respondentes

O objetivo menciona mensurar “todos os jurisdicionados”, e o considerando da linha 752 afirma “pleno atendimento”. Seis organizações não foram mensuradas.

Deve-se declarar atendimento parcial quanto à cobertura ou reformular o objetivo operacional como mensuração das organizações com resposta válida.

### 14. Destinatários dos encaminhamentos estão ambíguos

AN11 a AN123 representam 113 relatórios, mas os itens 2 e 4 dirigem-se genericamente aos “órgãos fiscalizados”, universo de 119 organizações. Os seis não respondentes não possuem relatório individual com achados ou plano de ação.

É necessário identificar expressamente as 113 organizações respondentes como destinatárias dos itens 1, 2 e 4 e tratar as seis restantes exclusivamente no item 3.

### 15. O texto menciona determinações inexistentes nos resultados individuais

O arquivo `resultado_auditoria.json` contém 2.140 encaminhamentos, todos classificados como “Recomendação”; não há determinação individual. O Capítulo 7 fala em “determinações e recomendações” constantes dos relatórios individuais.

O texto deve ser adequado ao conteúdo real, salvo se determinações forem posteriormente incluídas e individualizadas.

### 16. Apuração dos não respondentes exige maior precisão jurídica e factual

A Lei Complementar Estadual nº 63/1990 distingue “obstrução” (art. 63, V) de “sonegação de processo, documento ou informação” (art. 63, VI), e o art. 40 prevê prazo para apresentação antes da sanção. A redação atual agrega as duas hipóteses sob “possível obstrução”, sem resumir datas, prazos, recebimentos e conduta individual de cada organização.

Sugere-se a formulação “apuração de eventual ocorrência das hipóteses do art. 63, V e/ou VI”, acompanhada de quadro individual de comunicações, prazos, ciência, reiterações e justificativas.

Fonte oficial consultada: [Lei Complementar Estadual nº 63/1990 — ALERJ](https://www3.alerj.rj.gov.br/lotus_notes/default.asp?amp=&id=52&url=L2NvbnRsZWkubnNmLzU3M2FkMGIzNzJlYThjOTYwMzI1NjRmZjAwNjI5ZWFlLzRiMjk3MmJkYzU2M2U3NjYwMzI1NjY1MjAwNmI4NDliP09wZW5Eb2N1bWVudA%3D%3D).

### 17. Sigilo demanda validação jurídica específica

O considerando da linha 760 classifica genericamente todos os relatórios como reservados “pelo caráter sensível”. Deve-se confirmar competência classificatória, fundamento material, prazo, termo de classificação, autoridade e possibilidade de versões expurgadas.

Fonte oficial consultada: [Regimento Interno atual do TCE-RJ — Deliberação nº 338/2023](https://www.tcerj.tc.br/portalnovo/pagina/regimento_interno). A aplicação da Resolução TCE-RJ nº 433/2023 deve ser validada pela unidade jurídica competente.

## Oportunidades de melhoria de clareza, coerência e redação

1. A linha 63 diz que a avaliação cobriu seis temas, mas o questionário e o índice abrangem também riscos, segurança, continuidade, soluções, projetos e IA. Deve-se diferenciar o escopo do iGovTI das seis questões de auditoria que geram achados.
2. “As respostas foram validadas” é excessivo; recomenda-se “foram confrontadas com as evidências apresentadas”.
3. A afirmação de que índice zero indica ausência das práticas deve ser substituída por “indica que as respostas ajustadas não geraram pontuação no modelo”.
4. “Operam com fragilidades” deve ser substituído por “não demonstraram atendimento integral às práticas avaliadas”.
5. “Comparação longitudinal temporal” é pleonasmo.
6. A linha 452 contém texto de template — “quando gerados pelo fluxo de consolidação” — embora as figuras já estejam no relatório.
7. A tabela longitudinal apresenta `-0,000`; deve-se usar `0,000` ou “inferior a 0,001”.
8. Corrigir “grau de adoção dos jurisdicionados às boas práticas” para “grau de adoção, pelos jurisdicionados, das boas práticas” ou “grau de aderência dos jurisdicionados às boas práticas”.
9. Padronizar `TI` e `TIC`, “organização”, “entidade”, “jurisdicionado” e a capitalização dos títulos.
10. Substituir “desempenha um papel fundamental” e outras formulações promocionais por redação neutra.
11. A seção “Benefícios estimados” apresenta apenas expectativas qualitativas. Deve ser renomeada para “Benefícios esperados” ou complementada com indicadores mensuráveis.
12. As afirmações sobre IEGM, censo CAD-TI e experiências de outros Tribunais nas seções 3.5 e 3.6 precisam de referências identificáveis, datas e documentos.
13. Explicar que as situações de uma mesma organização não são mutuamente exclusivas e que basta uma delas, conforme a lógica vigente, para gerar o achado.

## Problemas de marcação e do produto final

1. A figura da linha 206 usa marcação inválida:

   ```markdown
   {#fig:modelo_governanca_ti_iso_38500 width=90%}
   ```

   Deve ser:

   ```markdown
   { width=90% }{#fig:modelo_governanca_ti_iso_38500#}
   ```

2. Três imagens da Seção 4.4 não são incorporadas pela geração padrão.
3. O DOCX do repositório está defasado e contém mídia vazia.
4. Há espaço não separável indevido em “COMUNICAÇÃO  COM DETERMINAÇÃO” e “À SUB-CIDADANIA”.
5. Deve-se padronizar `nº`, evitando alternância com `n.º` e `n°`.
6. Referências, sumário, notas, imagens, legendas e fontes devem ser validados novamente depois da consolidação dos comentários do gestor.

## Sequência mínima antes da assinatura

1. Decidir e documentar a revisão metodológica dos Achados 4 a 6.
2. Reexecutar a auditoria com as lógicas aprovadas.
3. Realizar e registrar a revisão humana dos pareceres de IA.
4. Incorporar os comentários do gestor e eventuais ajustes reversos.
5. Recalcular índices, achados, tabelas, gráficos e anexos.
6. Revisar integralmente as seções 1, 4, 6 e 7 com os resultados finais.
7. Submeter sigilo, não respondentes e encaminhamentos a revisão jurídica e processual.
8. Corrigir o gerador e produzir DOCX sem avisos nem recursos ausentes.

## Registro da validação técnica

Foi produzida cópia de validação em `/tmp/tcerj-igovti-2026/revisao-final/Relatório_altaresolucao_novo.docx`. A geração registrou ausência das três imagens indicadas neste parecer. Nenhum arquivo do relatório original foi alterado durante a avaliação.
