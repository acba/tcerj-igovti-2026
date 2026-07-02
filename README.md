# Fiscalização 18/2026 - iGovTI 2026

**Tribunal de Contas do Estado do Rio de Janeiro (TCE-RJ)**  
**Auditoria temática de governança e gestão de tecnologia da informação**

Este repositório reúne os papéis de trabalho digitais da Fiscalização nº 18/2026, voltada à avaliação da governança e da gestão de tecnologia da informação dos jurisdicionados estaduais e municipais do Rio de Janeiro.

O trabalho combina matriz de planejamento, questionário estruturado no LimeSurvey, cálculo do índice iGovTI 2026, avaliação de evidências, execução automatizada dos procedimentos de auditoria e geração de relatórios individuais e consolidado.

## Objetivo

Avaliar se as estruturas, práticas e controles de governança e gestão de TIC dos jurisdicionados são suficientes para apoiar o alinhamento estratégico, a conformidade normativa, a segurança da informação, a gestão de serviços, a gestão de contratações e a melhoria contínua da administração pública.

Os principais produtos do trabalho são:

- diagnóstico consolidado de maturidade em governança e gestão de TIC;
- índice iGovTI 2026, inclusive versão ajustada para comparação longitudinal;
- avaliação de conformidade das respostas e evidências apresentadas;
- achados, recomendações e determinações por organização auditada;
- relatórios individuais preliminares e relatório consolidado.

## Estrutura do Repositório

```text
.
├── 01-Planejamento/
│   ├── 01-Estudos_Preliminares/
│   ├── 02-Metodologia_iGovTI/
│   └── 03-Estrategia_e_Plano/
├── 02-Execucao/
│   ├── 01-Questionario/
│   ├── 02-Questionario iGovTI 2023/
│   ├── 03-Execucao_Procedimentos/
│   └── 04-Matriz_Achados/
├── 03-Relatorios/
│   ├── 01-Relatorio_Consolidado/
│   └── 02-Relatorios_Individuais_Preliminares/
├── 04-Portal_iGovTI/
└── scripts/
```

### Principais Artefatos

- `01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md`: questionário-fonte do iGovTI 2026.
- `01-Planejamento/02-Metodologia_iGovTI/igovti_2026.lss`: questionário importável no LimeSurvey.
- `01-Planejamento/02-Metodologia_iGovTI/estrutura-igovti-2026.yaml`: estrutura oficial de cálculo do iGovTI 2026.
- `01-Planejamento/02-Metodologia_iGovTI/estrutura-igovti-2026-ajustado-comparavel.yaml`: estrutura ajustada para comparação com 2023.
- `01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/matriz_planejamento.md`: matriz de planejamento em formato estruturado.
- `02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario.xlsx`: base de respostas tratada.
- `02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario-pos-avaliacao-evidencias.xlsx`: base após ajustes decorrentes da avaliação de evidências.
- `02-Execucao/03-Execucao_Procedimentos/01-Insumos/mapa-verificacao-achados.xlsx`: matriz que liga fontes, procedimentos, situações encontradas, achados e encaminhamentos.
- `02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/resultado_auditoria.json`: resultado compacto da execução dos procedimentos de auditoria.
- `03-Relatorios/01-Relatorio_Consolidado/Relatório_altaresolucao_novo.md`: fonte Markdown do relatório consolidado.
- `03-Relatorios/02-Relatorios_Individuais_Preliminares/relatorio-individual-preliminar-template.md`: template dos relatórios individuais.
- `scripts/calcula-igovti.html`: calculadora interativa para aplicar uma estrutura YAML de índice a uma fonte de informação e analisar resultados.
- `scripts/dashboard_avaliacao_evidencias.html`: dashboard para revisão humana das avaliações de evidências e exportação da consolidação por auditado e item.
- `scripts/montar_tabela_download_anexos_limesurvey.js`: script de apoio para gerar, a partir da tabela de respostas do LimeSurvey, a planilha com URLs de anexos e de respostas.
- `scripts/gerar_pacote_relatorios_igovti.py`: orquestrador do fluxo completo de geração dos artefatos, auditoria, gráficos e relatórios.

## Metodologia Sequencial

As etapas abaixo descrevem o fluxo operacional do trabalho, da concepção da auditoria à geração dos relatórios. Quando há automação disponível, o script correspondente é indicado.

### Fluxo completo em comando único

Para regenerar o pacote completo a partir da planilha bruta exportada do questionário eletrônico, use o orquestrador:

```bash
scripts/.venv/bin/python scripts/gerar_pacote_relatorios_igovti.py \
  --respostas-bruto 02-Execucao/01-Questionario/01-Coleta_LimeSurvey/20260621-respostas-questionario-bruto.xlsx \
  --data-final-preenchimento-comentarios-gestor 06/07/2026 \
  --email-contato-comentarios-gestor auditoriati@tcerj.tc.br \
  --numero-fiscalizacao-comentarios-gestor 18/2026 \
  --nome-fiscalizacao-comentarios-gestor "iGovTI 2026" \
  --output-dir C:/tmp/tcerj-igovti-2026-ultima-versao
```

O script infere o prefixo `20260621` a partir do nome da planilha bruta, aplica os ajustes registrados pela equipe, recalcula o iGovTI, executa a auditoria, gera gráficos, relatórios individuais e relatório consolidado. Cada etapa é exibida na tela com logs e o comando executado. Use `--auditados-select SIGLA...` para restringir a geração dos relatórios individuais a auditados específicos.

Os parâmetros `--email-contato-comentarios-gestor`, `--numero-fiscalizacao-comentarios-gestor` e `--nome-fiscalizacao-comentarios-gestor` são repassados ao gerador do questionário LimeSurvey de comentários do gestor e usados no texto de boas-vindas, encerramento, título, descrição e assunto do convite. Os padrões são `auditoriati@tcerj.tc.br`, `18/2026` e `iGovTI 2026`.

Principais sa?das no Windows:

```text
C:/tmp/tcerj-igovti-2026-ultima-versao/02-Execucao/01-Questionario/
C:/tmp/tcerj-igovti-2026-ultima-versao/02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/
C:/tmp/tcerj-igovti-2026-ultima-versao/02-Execucao/05-Comentarios_Gestor/
C:/tmp/tcerj-igovti-2026-ultima-versao/relatorios-individuais/
C:/tmp/tcerj-igovti-2026-ultima-versao/relatorio-consolidado/
```

Em Linux/macOS, o mesmo pacote ? gerado sob `/tmp/tcerj-igovti-2026-ultima-versao`.

### 1. Estudos preliminares e definição da abordagem

A equipe reúne antecedentes, referenciais externos e critérios de auditoria para definir escopo, riscos e questões de auditoria. As referências ficam principalmente em:

- `01-Planejamento/01-Estudos_Preliminares/`
- `01-Planejamento/01-Estudos_Preliminares/Referencias_Externas/`
- `01-Planejamento/01-Estudos_Preliminares/Analise_Riscos/`

Não há script único para esta etapa; trata-se de atividade analítica e documental.

### 2. Elaboração da matriz de planejamento

A matriz de planejamento organiza questões de auditoria, subquestões, riscos, fontes de informação, informações requeridas, critérios, procedimentos, evidências esperadas, possíveis achados e encaminhamentos.

Fonte principal:

```text
01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/matriz_planejamento.md
```

Geração do DOCX:

```bash
scripts/.venv/bin/python scripts/gerar_matriz_planejamento.py \
  01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/matriz_planejamento.md
```

### 3. Criação da metodologia e do índice iGovTI

A metodologia do iGovTI 2026 é definida a partir do questionário e das estruturas YAML de cálculo. A versão oficial calcula o índice do ciclo atual; a versão ajustada comparável permite análise longitudinal com 2023.

Fontes principais:

```text
01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md
01-Planejamento/02-Metodologia_iGovTI/metodologia-calculo.md
01-Planejamento/02-Metodologia_iGovTI/estrutura-igovti-2026.yaml
01-Planejamento/02-Metodologia_iGovTI/estrutura-igovti-2026-ajustado-comparavel.yaml
```

Cálculo dos resultados a partir das respostas:

```bash
scripts/.venv/bin/python scripts/gerar_igovti.py \
  --respostas 02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario.xlsx
```

Regeneração integrada dos artefatos do índice, comparação longitudinal e contexto estatístico:

```bash
scripts/.venv/bin/python scripts/gerar_artefatos_igovti.py \
  --respostas 02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario.xlsx \
  --prefixo 20260621 \
  --output-dir C:/tmp/tcerj-igovti-2026
```

Para simulações, validações metodológicas ou cálculo de um índice qualquer baseado em uma estrutura YAML, pode ser usada a página:

```text
scripts/calcula-igovti.html
```

Essa ferramenta permite carregar uma fonte de informação, aplicar a estrutura YAML de entrada, gerar resultados e visualizar estatísticas exploratórias do índice calculado.

### 4. Criação da matriz de procedimentos de auditoria

A matriz de procedimentos traduz a matriz de planejamento em verificações executáveis: fontes de informação, procedimentos, ações de verificação, lógica de achado, situações encontradas e encaminhamentos.

Artefato principal:

```text
02-Execucao/03-Execucao_Procedimentos/01-Insumos/mapa-verificacao-achados.xlsx
```

O repositório usa a skill local `preencher-matriz-procedimentos-auditoria` para apoiar essa geração a partir da matriz de planejamento. A matriz de achados em DOCX é gerada por:

```bash
scripts/.venv/bin/python scripts/gerar_matriz_achados.py
```

### 5. Construção do questionário e publicação no LimeSurvey

O questionário-fonte é mantido em Markdown estruturado e convertido para LimeSurvey quando necessário.

Fonte e saída:

```text
01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md
01-Planejamento/02-Metodologia_iGovTI/igovti_2026.lss
```

Conversão do Markdown para LSS:

```bash
scripts/.venv/bin/python scripts/resources/md2lss.py \
  01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md \
  01-Planejamento/02-Metodologia_iGovTI/igovti_2026.lss
```

A importação, ativação e configuração final do survey no LimeSurvey são etapas operacionais da plataforma, sem script dedicado neste repositório.

### 6. Comunicação aos auditados

Após a ativação do survey, cada auditado recebe comunicação formal com link individualizado de acesso ao questionário. A consolidação dos identificadores e links de anexos aparece nos artefatos de execução, especialmente:

```text
02-Execucao/01-Questionario/01-Coleta_LimeSurvey/urls_anexos_limesurvey_consolidado.xlsx
```

Não há script dedicado para expedição das comunicações formais. O envio e o controle de ciência são procedimentos administrativos externos ao repositório.

### 7. Coleta das respostas e dos anexos

As respostas do LimeSurvey são exportadas para XLSX e armazenadas em `02-Execucao/01-Questionario/`. Os anexos enviados pelos auditados são baixados e extraídos para análise.

Antes de rodar o coletor de anexos, a planilha com URLs de download pode ser montada a partir da página administrativa de respostas do LimeSurvey com:

```text
scripts/montar_tabela_download_anexos_limesurvey.js
```

O script deve ser executado no navegador, na tela de listagem das respostas do survey. Ele lê a tabela de respostas do LimeSurvey e gera `urls_anexos_limesurvey_consolidado.xlsx`, contendo identificadores, nomes dos auditados, URLs de download dos anexos e URLs dos PDFs de respostas. Essa planilha é usada pelo coletor Python.

Coleta dos anexos:

```bash
scripts/.venv/bin/python scripts/coletar_anexos_limesurvey.py
```

Extração dos ZIPs de evidências:

```bash
scripts/.venv/bin/python scripts/extrair_evidencias.py
```

Principais artefatos:

```text
02-Execucao/01-Questionario/01-Coleta_LimeSurvey/20260621-respostas-questionario-bruto.xlsx
02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario.xlsx
02-Execucao/01-Questionario/01-Coleta_LimeSurvey/urls_anexos_limesurvey_consolidado.xlsx
02-Execucao/01-Questionario/01-Coleta_LimeSurvey/Evidencias_Coletadas/evidencias/
02-Execucao/01-Questionario/01-Coleta_LimeSurvey/Evidencias_Coletadas/evidencias_extraidas/
```

### 8. Aplicação de ajustes iniciais nas respostas

Antes das avaliações finais, a equipe pode aplicar ajustes decorrentes de retificações, saneamento de inconsistências, correção de bugs identificados no survey ou padronização de respostas.

Artefato de controle:

```text
02-Execucao/01-Questionario/02-Ajustes_Respostas/ajustes_respostas_questionario_inicial.xlsx
```

Quando o ajuste segue a estrutura esperada pelo script de ajustes, ele pode ser aplicado por:

```bash
scripts/.venv/bin/python scripts/ajustar_respostas_questionario.py \
  --respostas 02-Execucao/01-Questionario/01-Coleta_LimeSurvey/20260621-respostas-questionario-bruto.xlsx \
  --ajustes 02-Execucao/01-Questionario/02-Ajustes_Respostas/ajustes_respostas_questionario_inicial.xlsx \
  --output 02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario.xlsx
```

### 9. Avaliação das respostas e evidências

A avaliação confronta as respostas afirmativas dos auditados com as evidências anexadas. O pipeline usa catálogos de prompts, processa arquivos PDF/DOCX quando necessário, registra avaliações em JSONL e permite consolidação posterior por juiz IA e revisão humana.

Catálogo principal para achados:

```text
scripts/avaliacao_evidencias/prompt_catalogs/igovti_2026_achados_binario_v1.yml
scripts/avaliacao_evidencias/prompts/igovti_2026_achados_binario_v1/
```

Regeneração dos prompts binários de achados:

```bash
scripts/.venv/bin/python -m scripts.avaliacao_evidencias.prompt_catalog_achados build \
  scripts/avaliacao_evidencias/prompt_catalogs/igovti_2026_achados_binario_v1.yml \
  01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md \
  scripts/avaliacao_evidencias/prompts/igovti_2026_achados_binario_v1
```

Validação local sem IA remota:

```bash
scripts/.venv/bin/python -m scripts.avaliacao_evidencias \
  02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario.xlsx \
  C:/tmp/tcerj-igovti-2026/evidencias_extraidas \
  --questionario 01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md \
  --prompts-dir scripts/avaliacao_evidencias/prompts/igovti_2026_achados_binario_v1 \
  --prompt-version igovti_2026_achados_binario_v1 \
  --only-prompts-present \
  --provider fake \
  --model fake \
  --out-dir C:/tmp/tcerj-igovti-2026/02-Execucao/03-Execucao_Procedimentos/99-Avaliacao_Evidencias/individuais/teste-achados-binario
```

Execução paralela dos modelos configurados:

```bash
scripts/.venv/bin/python scripts/run_avaliacao_evidencias_v2.py
```

Consolidação das avaliações por juiz IA:

```bash
scripts/.venv/bin/python scripts/run_consolida_avaliacoes_v2.py
```

Revisão humana das avaliações e dos pareceres consolidados:

```text
scripts/dashboard_avaliacao_evidencias.html
```

O dashboard permite que a equipe revise as avaliações das evidências, inclusive pareceres consolidados pelo juiz, filtre por auditado e item avaliado, e exporte planilha XLSX com a consolidação da revisão. Isso permite dividir o mesmo conjunto de dados entre revisores em paralelo e depois usar a planilha exportada como insumo para os ajustes pós-avaliação.

Agregação por item do questionário:

```bash
scripts/.venv/bin/python scripts/agregar_analyses_por_item.py \
  02-Execucao/03-Execucao_Procedimentos/99-Avaliacao_Evidencias/individuais/analyses*.jsonl \
  --output 02-Execucao/03-Execucao_Procedimentos/99-Avaliacao_Evidencias/consolidado/agregado_avaliacoes_por_item.xlsx
```

Documentação detalhada:

```text
scripts/avaliacao_evidencias/README.md
```

### 10. Ajustes pós-avaliação de evidências

Após a revisão das evidências, respostas afirmativas não comprovadas podem ser convertidas em respostas não conformes ou removidas, conforme o tipo de item.

Planilha de ajustes:

```text
02-Execucao/01-Questionario/02-Ajustes_Respostas/ajustes_respostas_questionario_pos_avaliacao_evidencias.xlsx
```

Aplicação dos ajustes:

```bash
scripts/.venv/bin/python scripts/ajustar_respostas_questionario.py \
  --respostas 02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario.xlsx \
  --ajustes 02-Execucao/01-Questionario/02-Ajustes_Respostas/ajustes_respostas_questionario_pos_avaliacao_evidencias.xlsx \
  --output 02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario-pos-avaliacao-evidencias.xlsx
```

Fonte derivada para uso nos procedimentos de auditoria:

```bash
scripts/.venv/bin/python scripts/gerar_fonte_ajustes_evidencias_auditoria.py
```

O script gera `02-Execucao/03-Execucao_Procedimentos/99-Avaliacao_Evidencias/painel-avaliacao-evidencias.xlsx`, em formato largo por auditado, contendo apenas itens já utilizados no mapa de verificação de achados. Essa fonte permite que a ocorrência de `Não conforme` na avaliação de evidências também componha a lógica dos achados, mantendo a justificativa do juiz ou do auditor revisor disponível para a descrição da evidência.

### 10.1. Reavaliação dos comentários do gestor e ajustes reversos

Quando o survey de comentários do gestor coletar comentários e novas evidências para itens avaliados como `Não conforme`, a reavaliação deve usar o mesmo conjunto de prompts da avaliação de evidências. O pipeline específico para essa fase lê a exportação XLSX do LimeSurvey de comentários, a pasta de anexos já extraídos e a planilha de ajustes pós-avaliação de evidências. Ele avalia apenas os itens originalmente não conformes para cada auditado e questão base.

Geração das avaliações individuais:

```bash
scripts/.venv/bin/python scripts/avaliar_comentarios_gestor.py avaliar \
  --respostas-comentarios C:/tmp/tcerj-igovti-2026/02-Execucao/05-Comentarios_Gestor/respostas-comentarios-gestor.xlsx \
  --evidencias-comentarios-root C:/tmp/tcerj-igovti-2026/02-Execucao/05-Comentarios_Gestor/evidencias_extraidas \
  --ajustes-pos-avaliacao-evidencias 02-Execucao/01-Questionario/02-Ajustes_Respostas/ajustes_respostas_questionario_pos_avaliacao_evidencias.xlsx \
  --questionario 01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md \
  --prompts-dir scripts/avaliacao_evidencias/prompts/igovti_2026_achados_binario_v1 \
  --prompt-version igovti_2026_comentarios_gestor_v1 \
  --provider fake \
  --model fake \
  --out-dir C:/tmp/tcerj-igovti-2026/02-Execucao/05-Comentarios_Gestor/99-Reavaliacao_Evidencias/individuais
```

Consolidação das avaliações por juiz IA:

```bash
scripts/.venv/bin/python -m scripts.avaliacao_evidencias.consolidacao \
  C:/tmp/tcerj-igovti-2026/02-Execucao/05-Comentarios_Gestor/99-Reavaliacao_Evidencias/individuais/analyses*.jsonl \
  --evidencias-root C:/tmp/tcerj-igovti-2026/02-Execucao/05-Comentarios_Gestor/evidencias_extraidas \
  --judge-provider fake \
  --judge-model fake \
  --out-dir C:/tmp/tcerj-igovti-2026/02-Execucao/05-Comentarios_Gestor/99-Reavaliacao_Evidencias/consolidado
```

Geração do arquivo de ajustes reversos:

```bash
scripts/.venv/bin/python scripts/avaliar_comentarios_gestor.py gerar-ajustes \
  --consolidado C:/tmp/tcerj-igovti-2026/02-Execucao/05-Comentarios_Gestor/99-Reavaliacao_Evidencias/consolidado/consolidated.jsonl \
  --ajustes-pos-avaliacao-evidencias 02-Execucao/01-Questionario/02-Ajustes_Respostas/ajustes_respostas_questionario_pos_avaliacao_evidencias.xlsx \
  --output C:/tmp/tcerj-igovti-2026/02-Execucao/05-Comentarios_Gestor/99-Reavaliacao_Evidencias/ajustes_respostas_questionario_pos_comentarios_gestor.xlsx
```

O arquivo gerado contém apenas itens que o parecer consolidado classificou como `Conforme`. Para esses casos, a coluna `Resposta ajustada` restaura a `Resposta afirmada` original, permitindo desfazer o ajuste negativo aplicado após a primeira avaliação de evidências.

Aplicação dos ajustes reversos sobre a base já ajustada por evidências:

```bash
scripts/.venv/bin/python scripts/ajustar_respostas_questionario.py \
  --respostas 02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario-pos-avaliacao-evidencias.xlsx \
  --ajustes C:/tmp/tcerj-igovti-2026/02-Execucao/05-Comentarios_Gestor/99-Reavaliacao_Evidencias/ajustes_respostas_questionario_pos_comentarios_gestor.xlsx \
  --output C:/tmp/tcerj-igovti-2026/02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario-pos-comentarios-gestor.xlsx
```

Em Linux/macOS, substitua `C:/tmp/tcerj-igovti-2026` por `/tmp/tcerj-igovti-2026`. Use `provider fake` e `judge-provider fake` apenas para validação estrutural; a reavaliação substantiva exige os provedores reais configurados.

### 11. Cálculo de estatísticas, índices e comparação longitudinal

Com a base ajustada, são recalculados os resultados do iGovTI, a versão comparável, os dados históricos 2023-2026 e o contexto usado nos relatórios.

Regeneração completa recomendada:

```bash
scripts/.venv/bin/python scripts/gerar_artefatos_igovti.py \
  --respostas 02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario-pos-avaliacao-evidencias.xlsx \
  --prefixo 20260621 \
  --output-dir C:/tmp/tcerj-igovti-2026
```

Execução manual das etapas estatísticas:

```bash
scripts/.venv/bin/python scripts/consolidar_dados_comparativos_igovti.py
scripts/.venv/bin/python scripts/calcular_contexto_relatorios_igovti.py
```

Geração de gráficos para relatórios:

```bash
scripts/.venv/bin/python scripts/gerar_graficos_relatorios_consolidado_individuais_igovti.py \
  --auditados FTM \
  --output-root C:/tmp/tcerj-igovti-2026
```

Geração de gráficos específicos da comparação harmonizada iGovTI 2023-2026:

```bash
scripts/.venv/bin/python scripts/gerar_graficos_igovti_comparavel.py
```

Geração de gráficos consolidados dos achados por esfera, a partir do banco de auditados e do resultado da auditoria:

```bash
scripts/.venv/bin/python scripts/gerar_graficos_achados_consolidado.py \
  --output-dir C:/tmp/tcerj-igovti-2026/relatorio-consolidado/img
```

### 12. Execução dos procedimentos de auditoria e consolidação de achados

A execução automatizada cruza o banco de auditados, a matriz de procedimentos e as fontes de informação para produzir achados, encaminhamentos, rankings e artefatos de suporte à manifestação dos gestores.

```bash
scripts/.venv/bin/python scripts/executa_auditoria.py \
  --auditados 02-Execucao/03-Execucao_Procedimentos/01-Insumos/bd_auditados.xlsx \
  --mapa 02-Execucao/03-Execucao_Procedimentos/01-Insumos/mapa-verificacao-achados.xlsx \
  --fontes \
    02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario-pos-avaliacao-evidencias.xlsx \
    02-Execucao/03-Execucao_Procedimentos/99-Avaliacao_Evidencias/painel-avaliacao-evidencias.xlsx \
  --resultado-auditoria-json C:/tmp/tcerj-igovti-2026/02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/resultado_auditoria.json \
  --tabelas-auditoria-xlsx C:/tmp/tcerj-igovti-2026/02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/tabelas_consolidadas_auditoria.xlsx \
  --data-final-preenchimento-comentarios-gestor 06/07/2026 \
  --email-contato-comentarios-gestor auditoriati@tcerj.tc.br \
  --numero-fiscalizacao-comentarios-gestor 18/2026 \
  --nome-fiscalizacao-comentarios-gestor "iGovTI 2026"
```

Saídas principais:

- `resultado_auditoria.json`: serialização compacta dos resultados, suficiente para gráficos, relatórios e plano de ação.
- `tabelas_consolidadas_auditoria.xlsx`: tabelas de achados, recomendações e ranking.
- `relatorios_procedimentos.zip`: relatórios de procedimentos por auditado.
- `anexo_evidencias.docx`: consolidação de evidências vinculadas aos achados.
- `comentarios_gestor/questionario_comentarios_gestor.lss`: survey para comentários dos gestores.
- `comentarios_gestor/anexos_docx_comentarios.zip`: modelos Word para manifestação dos gestores.

Para depuração da execução, incluindo todas as ações de verificação avaliadas, informe também `--resultado-auditoria-detalhado-json C:/tmp/tcerj-igovti-2026/02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/resultado_auditoria_detalhado.json`.

Antes da execução, o script valida o mapa de auditoria de forma bloqueante, incluindo referências a fontes, ações citadas na lógica, colunas das fontes, valores booleanos e expressões lógicas. Para uma execução leve, sem ZIP, DOCX ou LSS acessórios, use `--somente-dados`. Também é possível pular saídas específicas com `--skip-relatorios-procedimentos`, `--skip-anexo-evidencias` e `--skip-comentarios-gestor`.

### 13. Escrita dos relatórios individuais preliminares

Os relatórios individuais combinam o resultado da execução dos procedimentos, o contexto estatístico do iGovTI, gráficos e templates Markdown.

```bash
scripts/.venv/bin/python scripts/gerar_relatorios_individuais.py \
  --auditados C:/tmp/tcerj-igovti-2026/02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/resultado_auditoria.json \
  --templates 03-Relatorios/02-Relatorios_Individuais_Preliminares/relatorio-individual-preliminar-template.md \
  --context-files 02-Execucao/01-Questionario/04-Resultados_iGovTI/20260621-contexto-relatorios-igovti-2026.xlsx \
  --ajustes-respostas 02-Execucao/01-Questionario/02-Ajustes_Respostas/ajustes_respostas_questionario_pos_avaliacao_evidencias.xlsx \
  --resource-files "C:/tmp/tcerj-igovti-2026/relatorios-individuais/img/**/*" "03-Relatorios/02-Relatorios_Individuais_Preliminares/img/igovti_2026_composicao_infografico_v6.png" \
  --auditados-select FTM \
  --output-dir C:/tmp/tcerj-igovti-2026/relatorios-individuais/FTM \
  --reference-docx scripts/resources/template-base-estilos-sigiloso.docx
```

O argumento `--ajustes-respostas` alimenta o Apêndice B de cada relatório individual com os ajustes aplicados após a avaliação de evidências, incluindo item, resposta declarada, resposta ajustada e justificativa do juiz ou do auditor revisor, quando houver revisão humana.

### 14. Escrita do relatório consolidado

O relatório consolidado é mantido em Markdown e convertido para DOCX com aplicação de estilos, recursos gráficos e referências.

Fonte principal:

```text
03-Relatorios/01-Relatorio_Consolidado/Relatório_altaresolucao_novo.md
```

Geração do DOCX:

```bash
scripts/.venv/bin/python scripts/gerar_relatorio_consolidado.py \
  --input 03-Relatorios/01-Relatorio_Consolidado/Relatório_altaresolucao_novo.md \
  --output C:/tmp/tcerj-igovti-2026/relatorio-consolidado/Relatório_altaresolucao_novo.docx \
  --resource-files "C:/tmp/tcerj-igovti-2026/relatorio-consolidado/img/**/*" "C:/tmp/tcerj-igovti-2026/relatorios-individuais/img/**/*" \
  --resultados-2026 C:/tmp/tcerj-igovti-2026/02-Execucao/01-Questionario/04-Resultados_iGovTI/20260621-iGovTI-2026.xlsx \
  --respostas-2026 C:/tmp/tcerj-igovti-2026/02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario-pos-avaliacao-evidencias.xlsx \
  --comparavel-2026 C:/tmp/tcerj-igovti-2026/02-Execucao/01-Questionario/04-Resultados_iGovTI/20260621-iGovTI-2026-Ajustado-Comparavel.xlsx \
  --auditados-xlsx 02-Execucao/03-Execucao_Procedimentos/01-Insumos/bd_auditados.xlsx \
  --resultado-auditoria-json C:/tmp/tcerj-igovti-2026/02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/resultado_auditoria.json
```

O gerador do consolidado também recria, em diretório temporário interno, os gráficos gerais e os gráficos de achados usados pelo DOCX. Quando os argumentos acima são informados, esses gráficos são produzidos a partir dos artefatos recém-gerados, e não dos arquivos padrão do repositório.

### 15. Publicação e portal iGovTI

Os requisitos do portal ficam em:

```text
04-Portal_iGovTI/PRD.md
```

Essa etapa consolida a estratégia de transparência e comunicação dos resultados após a validação dos produtos de auditoria.

## Convenções de Execução

- Use preferencialmente o ambiente virtual do repositório: `scripts/.venv/bin/python`.
- Gere artefatos intermediários em `C:/tmp/tcerj-igovti-2026` quando estiver validando uma nova execução.
- Não edite diretamente prompts Markdown gerados em `scripts/avaliacao_evidencias/prompts/`; altere o catálogo YAML correspondente e regenere os prompts.
- Trate saídas de IA como minutas auxiliares. A conclusão de auditoria depende de revisão humana da equipe.
- Para documentação, preserve português do Brasil e os identificadores técnicos do questionário, como `q0101`, `evidence_text`, `visible_if` e códigos de alternativas.

## Comandos de Inspeção Úteis

```bash
rg --files -g '!**/.git/**'
find . -maxdepth 3 -type d | sort
rg -n "^## Grupo:|^### q|evidence_text:" 01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md
```

## Equipe Técnica

**Unidade técnica:** Coordenadoria de Auditoria de Tecnologia da Informação (CAD-TI/TCE-RJ)  
**Responsável:** Equipe de Auditoria

---

© 2026 Tribunal de Contas do Estado do Rio de Janeiro. Repositório de uso interno/restrito até a publicação do relatório final.
