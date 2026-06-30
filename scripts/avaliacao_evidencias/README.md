# Avaliacao de evidencias

Pipeline generico para pre-analise de evidencias enviadas por auditados em questionarios SurveyMD/LimeSurvey.

O pipeline e generico. Os prompts nao sao genericos: cada questionario deve ter seu proprio diretorio de prompts, com um arquivo por questao ou item especifico.

## Organizacao da camada de IA

A logica de providers de IA fica isolada em `avaliacao_evidencias/providers_ai_service.py`. Esse modulo nao importa `pipeline.py` nem depende das dataclasses do questionario: ele recebe itens afirmados por interface estrutural, como objetos com atributos `codigo`, `texto` e `afirmacao`, ou dicionarios equivalentes.

`pipeline.py` e `consolidacao.py` apenas preparam contexto, evidencias, checkpoint e controle de fluxo; a chamada a Gemini, OpenRouter, OpenAI-compatible local, provider fake, retry transiente, reparo de JSON e validacao da resposta ficam no servico de providers.

## O que o pipeline faz

1. Le a planilha de respostas `.xlsx`.
2. Processa somente linhas com `submitdate`, salvo quando `--include-unsubmitted` for informado.
3. Identifica colunas de evidencia, isto e, colunas cujo nome contem `evi` e que nao terminam em `[filecount]`.
4. Para cada evidencia, localiza o arquivo em `evidencias/<auditado>/<name>`, usando o atributo `name` do JSON de upload.
5. Resolve o prompt especifico da questao.
6. Monta o pacote de evidencia, incluindo texto extraido, inventario de ZIP e arquivos compativeis para upload no Gemini.
7. Se nenhum item foi afirmado pelo auditado, grava a analise como concluida sem chamar provider.
8. Chama o provider configurado: `fake`, `gemini`, `openrouter`, `opencodego` ou `openai`.
9. Repara e valida a resposta JSON do modelo com `json-repair`.
10. Grava checkpoint incremental em JSONL.
11. Gera `relatorio_conformidade.xlsx`.

## Estrutura esperada

Exemplo:

```text
respostas.xlsx
igovti_2026.md
evidencias/
  SEFAZ/
    q0101.zip
    fu_8ks.png
  SEEDUC/
    q0102.zip
avaliacao_evidencias/
  prompt_catalogs/
    igovti_2026_conservador_v2.yml
  prompts/
    igovti_2026_conservador_v2/
      q0101.md
      q1001.md
      q2804_A.md
```

O valor de `firstname` na planilha identifica o auditado e deve corresponder ao subdiretorio em `evidencias/<auditado>/`.

O arquivo fisico de evidencia e localizado primeiro pelo atributo `name` do objeto JSON existente na coluna de evidencia. O atributo `filename` do LimeSurvey nao e usado como chave de busca.

Quando o arquivo exportado pelo LimeSurvey nao preserva exatamente esse nome, o pipeline tambem procura variantes com o padrao de exportacao do LimeSurvey, por exemplo:

```text
name na planilha:
Resolu%C3%A7%C3%A3o%20SECTI%20159-2023%20Pol%C3%ADtica%20de%20Seguran%C3%A7a%20da%20Informa%C3%A7%C3%A3o.pdf

arquivo exportado:
00006_11_resolução-secti-159-2023-pol-tica-de-segurança-da-informação.pdf
```

Essa resolucao tenta, nesta ordem: nome exato decodificado, prefixo numerico inferido do id da resposta e da ordem da coluna de evidencia, e fallback por nome normalizado.

Cada coluna de evidencia deve conter exatamente um arquivo. Esse arquivo pode ser `.zip` ou `.rar`; nesse caso, o arquivo compactado pode conter varios arquivos internos. Arquivos `.zip` e `.rar` aninhados tambem sao extraidos recursivamente (ate um limite de profundidade). Os arquivos internos sao achatados em uma unica pasta temporaria: duplicados por hash de conteudo sao removidos e colisoes de nome com conteudo diferente sao renomeadas.

### Atalhos `.url`

Arquivos `.url` (atalhos do Windows) sao interpretados pelo pipeline. A URL contida no arquivo e lida e, se atender as restricoes de seguranca, o recurso e baixado temporariamente e processado como evidencia:

- Apenas URLs dos esquemas `http` e `https` sao aceitas.
- Apenas dominios terminados em `.gov.br` sao permitidos.
- URLs com credenciais embutidas, enderecos locais (`localhost`, `127.0.0.1`, `::1`) e IPs privados/reservados sao bloqueadas.
- O download e limitado a **10 MB** e a um timeout de **30 segundos**.
- Apenas MIME types conhecidos e seguros sao aceitos (PDF, DOC/DOCX, planilhas, imagens, texto, HTML).

Se o recurso for uma pagina HTML, o arquivo `.html` baixado e enviado diretamente ao provider. Se a URL nao for `.gov.br`, o download falhar, o tipo for nao permitido ou qualquer outra restricao de seguranca for violada, o atalho e descartado silenciosamente: nenhum texto com a URL e enviado ao modelo.

## Instalar dependencias

Na raiz do repositorio:

```bash
python -m venv .venv
.venv/bin/pip install -r scripts/requirements.txt
```

Se a venv ja existir:

```bash
.venv/bin/pip install -r scripts/requirements.txt
```

### Dependencia para arquivos `.rar`

A extracao de `.rar` usa a biblioteca `rarfile` (incluida em `requirements.txt`). Ela localiza automaticamente:

- **Windows:** `UnRAR.exe`, normalmente disponivel quando o WinRAR esta instalado.
- **Linux:** `unrar`, `unrar-free` ou `bsdtar`.

Se nenhuma dessas ferramentas estiver disponivel, o modulo tenta fallback com `7z`, mas o 7z open source pode nao suportar metodos de compressao de RARs recentes. Nesse caso, instale `unrar` non-free ou use um ambiente Windows com WinRAR.

## Gerar prompts

Para o iGovTI 2026, a versao recomendada e `igovti_2026_conservador_v2`.

Fonte de verdade:

```text
avaliacao_evidencias/prompt_catalogs/igovti_2026_conservador_v2.yml
```

Prompts gerados:

```text
avaliacao_evidencias/prompts/igovti_2026_conservador_v2/
```

Para regenerar:

```bash
.venv/bin/python -m avaliacao_evidencias.prompt_catalog build \
  avaliacao_evidencias/prompt_catalogs/igovti_2026_conservador_v2.yml \
  igovti_2026.md \
  avaliacao_evidencias/prompts/igovti_2026_conservador_v2
```

Edite o YAML, nao os Markdown gerados. O gerador e deterministico: se o YAML e o questionario nao mudarem, os Markdown gerados devem ser identicos.

### Gerar prompts binarios para achados

O conjunto `igovti_2026_achados_binario_v1` cobre somente colunas de evidencia associadas a situacoes encontradas e achados na matriz de procedimentos. Ele usa julgamento substantivo binario: `conforme` ou `nao_conforme`.

No catalogo binario, cada entrada deve declarar `arquivo`, `coluna_evidencia` e `itens_avaliaveis`. Use `criterios_pratica_principal` para a pratica base de questoes `adoption`, `criterios_comuns_itens` para criterios compartilhados por varias alternativas e `criterios_por_item` para criterios especificos. Quando alguns itens nao devem receber os criterios comuns, declare `excluir_criterios_comuns_itens`.

Para questoes em que a alternativa marcada serve apenas como codigo de rastreabilidade, use `exibir_texto_itens: false`. O Markdown gerado passa a listar somente o codigo e os criterios; o pipeline tambem mascara `itens_afirmados[].texto` antes de chamar o provider, impedindo que o modelo julgue pelo texto integral da alternativa. Em questoes `adoption` com detalhamentos, mantenha o texto visivel quando o detalhamento marcado for a propria afirmacao que precisa ser sustentada pela evidencia.

Fonte de verdade:

```text
avaliacao_evidencias/prompt_catalogs/igovti_2026_achados_binario_v1.yml
```

Prompts gerados:

```text
avaliacao_evidencias/prompts/igovti_2026_achados_binario_v1/
```

Para regenerar:

```bash
.venv/bin/python -m avaliacao_evidencias.prompt_catalog_achados build \
  avaliacao_evidencias/prompt_catalogs/igovti_2026_achados_binario_v1.yml \
  igovti_2026.md \
  avaliacao_evidencias/prompts/igovti_2026_achados_binario_v1
```

## Validar sem chamar IA

Use o provider `fake` para validar inventario, resolucao de arquivos, prompts, checkpoint e relatorio:

```bash
.venv/bin/python -m avaliacao_evidencias respostas.xlsx evidencias/ \
  --questionario igovti_2026.md \
  --prompts-dir avaliacao_evidencias/prompts/igovti_2026_conservador_v2 \
  --prompt-version v2 \
  --provider fake \
  --model fake \
  --out-dir .saida_analise
```

O provider `fake` nao faz julgamento substantivo. Ele retorna conclusoes `inconclusivo` para testar o fluxo sem rede.

## Processar respostas sem submitdate

Por padrao, o pipeline ignora respostas sem `submitdate`, porque elas normalmente representam respostas nao submetidas ou rascunhos.

Para incluir essas respostas mesmo assim, use `--include-unsubmitted`:

```bash
.venv/bin/python -m avaliacao_evidencias respostas.xlsx evidencias/ \
  --questionario igovti_2026.md \
  --prompts-dir avaliacao_evidencias/prompts/igovti_2026_conservador_v2 \
  --prompt-version v2 \
  --provider fake \
  --model fake \
  --out-dir .saida_analise \
  --include-unsubmitted
```

Essa flag afeta o inventario inicial de analises. A deduplicacao por checkpoint continua valendo normalmente.

## Executar com Gemini

Configure a chave:

```bash
export GEMINI_API_KEY="..."
```

Execute:

```bash
.venv/bin/python -m avaliacao_evidencias respostas.xlsx evidencias/ \
  --questionario igovti_2026.md \
  --prompts-dir avaliacao_evidencias/prompts/igovti_2026_conservador_v2 \
  --prompt-version v2 \
  --provider gemini \
  --model gemini-2.5-flash \
  --rpm 30 \
  --out-dir .saida_analise
```

O Gemini usa `google-genai`. Arquivos compativeis sao enviados pela Files API com nomes temporarios seguros em ASCII, para evitar falhas de upload por caracteres especiais no caminho/nome do arquivo. Evidencias ZIP sao validadas contra path traversal e arquivos internos compativeis sao extraidos temporariamente para upload. Arquivos `.xlsx` nao sao enviados diretamente ao Gemini: o pipeline extrai o texto com `markitdown`, gera um `.txt` temporario com nome seguro e envia esse texto para a API. Arquivos `.doc` e `.docx` tambem nao sao enviados diretamente: por padrao, o pipeline converte o documento para PDF com LibreOffice/`soffice` em modo headless e envia o PDF ao modelo, preservando imagens e layout. Em Windows, quando LibreOffice/`soffice` nao estiver disponivel ou falhar, o pipeline tenta converter pelo Microsoft Word instalado, via automacao COM acionada pelo PowerShell. Se nenhum conversor funcionar, a analise da evidencia e registrada como erro tecnico.

Para modelos Gemini com suporte a pensamento controlavel, use `--reasoning low`, `--reasoning medium` ou `--reasoning high`. O valor e enviado como `thinking_config.thinking_level` e tambem entra na identidade do checkpoint, permitindo comparar execucoes com niveis diferentes sem reaproveitar indevidamente resultados anteriores. O alias `--reasoning-effort` e equivalente.

Erros tecnicos de processamento da evidencia, como `markitdown` ausente para `.xlsx`, falha na conversao de `.doc`/`.docx` para PDF ou evidencia sem conteudo processavel, sao registrados com `status: error`. Esses casos nao devem ser convertidos pelo modelo em `nao_conforme`, pois nao representam juizo substantivo sobre a evidencia apresentada.

## Executar com OpenRouter

Configure a chave:

```bash
export OPENROUTER_API_KEY="..."
```

Execute:

```bash
.venv/bin/python -m avaliacao_evidencias respostas.xlsx evidencias/ \
  --questionario igovti_2026.md \
  --prompts-dir avaliacao_evidencias/prompts/igovti_2026_conservador_v2 \
  --prompt-version v2 \
  --provider openrouter \
  --model google/gemini-2.5-flash \
  --out-dir .saida_analise
```

O OpenRouter recebe o prompt e o pacote de evidencia normalizado em texto pela API de Chat Completions. O request inclui `response_format` com JSON schema quando suportado pelo modelo. Para PDFs, o pipeline extrai texto com `pypdf` e envia o conteudo textual normalizado; PDFs sem texto extraivel ficam registrados como lacuna tecnica no pacote.

Quando o provider `openrouter` usa modelos Google/Gemini ou OpenAI/ChatGPT, o pipeline tambem anexa os arquivos `.pdf` preparados em `messages[].content` como `type: "file"` com `file_data` em base64 e configura o plugin `file-parser` com engine `native`. Isso permite que modelos com suporte nativo a arquivos analisem o PDF diretamente. Para os demais modelos, o comportamento permanece textual: o OpenRouter recebe apenas o pacote normalizado de evidencia.

## Executar com OpenAI-compatible local

O provider `openai` usa, por padrao, o proxy local `openai-oauth` no endereco `http://127.0.0.1:10531/v1`, o mesmo usado por `scripts/test_openai_oauth_provider.py`. Ele chama `/v1/responses` em modo streaming e envia PDFs preparados como `input_file` com `file_data` em base64. O proxy local normalmente nao exige chave; se houver chave, informe `OPENAI_API_KEY`. Para trocar a base URL, defina `OPENAI_BASE_URL`.

Execute com o proxy local ja ativo:

```bash
scripts/.venv/bin/python -m scripts.avaliacao_evidencias \
  02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario.xlsx \
  02-Execucao/01-Questionario/01-Coleta_LimeSurvey/Evidencias_Coletadas/evidencias_extraidas \
  --questionario 01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md \
  --prompts-dir scripts/avaliacao_evidencias/prompts/igovti_2026_achados_binario_v1 \
  --prompt-version igovti_2026_achados_binario_v1 \
  --only-prompts-present \
  --provider openai \
  --model gpt-5.4-mini \
  --rpm 12 \
  --out-dir 02-Execucao/03-Execucao_Procedimentos/99-Avaliacao_Evidencias/individuais/achados_binario_openai_gpt-5.4-mini
```

Para testar apenas algumas organizacoes:

```bash
scripts/.venv/bin/python -m scripts.avaliacao_evidencias \
  02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario.xlsx \
  02-Execucao/01-Questionario/01-Coleta_LimeSurvey/Evidencias_Coletadas/evidencias_extraidas \
  --questionario 01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md \
  --prompts-dir scripts/avaliacao_evidencias/prompts/igovti_2026_achados_binario_v1 \
  --prompt-version igovti_2026_achados_binario_v1 \
  --only-prompts-present \
  --provider openai \
  --model gpt-5.4-mini \
  --auditados ALERJ AGENERSA \
  --rpm 12 \
  --out-dir 02-Execucao/03-Execucao_Procedimentos/99-Avaliacao_Evidencias/individuais/achados_binario_openai_gpt-5.4-mini
```

Para forcar a conversao de evidencias PDF em Markdown com imagens extraidas antes da chamada ao modelo, use `--pdf2md`. Quando o anexo de evidencia resolvido for um arquivo `.pdf`, o pipeline usa `pymupdf4llm` para gerar um documento Markdown e arquivos de imagem, inclui o Markdown em `pacote_evidencia.documentos` e envia os artefatos preparados ao provider. No OpenRouter, as imagens `.png`/`.jpg` extraidas sao anexadas como `image_url` em data URI; no provider `openai`, como `input_image`; no Gemini, os arquivos preparados seguem pela camada de upload do provider. O PDF original nao e enviado nesse modo. Use `--pdf2md-dpi N` para ajustar a resolucao das imagens extraidas; o padrao e `150`.

Para forcar a conversao de evidencias DOCX em HTML com imagens extraidas antes da chamada ao modelo, use `--docx2html`. Quando o anexo de evidencia resolvido for um arquivo `.docx`, o pipeline usa `mammoth` para gerar um documento HTML, inclui esse HTML em `pacote_evidencia.documentos` e envia as imagens `.png`/`.jpg`/`.jpeg` extraidas como anexos ao provider. O DOCX original nao e enviado nesse modo. Arquivos `.doc` continuam seguindo o fluxo padrao de conversao para PDF.

No provider `opencodego`, imagens preparadas por `--pdf2md` ou `--docx2html` tambem sao enviadas ao endpoint OpenAI-compatible como `image_url` com data URI base64. O conteudo textual do Markdown/HTML permanece no `pacote_evidencia.documentos`.

Para modelos OpenRouter com suporte a raciocinio controlavel, use `--reasoning low`, `--reasoning medium` ou `--reasoning high`. O valor e enviado como `reasoning.effort` e tambem entra na identidade do checkpoint, permitindo comparar execucoes com niveis diferentes sem reaproveitar indevidamente resultados anteriores. O alias `--reasoning-effort` e equivalente.

Cada registro gravado no JSONL de analises inclui metadados de execucao da avaliacao: `started_at`, `finished_at`, `duration_seconds` e `reasoning_effort`. Esses campos permitem auditar o tempo gasto por item e distinguir execucoes com diferentes niveis de reasoning.

Para inspecionar o payload textual completo enviado ao provider, use `--store-prompts`. O campo `prompt_payload` sera gravado no respectivo registro do JSONL de analises. Em chamadas com arquivos anexados, como PDFs enviados ao Gemini ou ao OpenRouter, esse campo representa a parte textual do request; os arquivos continuam sendo enviados por upload/anexo e aparecem no pacote como `arquivos_upload`.

## Controlar requests por minuto

Use `--rpm N` para limitar a taxa de chamadas aos providers remotos. Por exemplo, `--rpm 30` limita a execucao a no maximo 30 chamadas por minuto para `gemini` ou `openrouter`.

O valor padrao e `12`, equivalente a uma chamada a cada 5 segundos. Use `--rpm 0` para desativar o limite. O provider `fake` nao e limitado por RPM.

Quando o provider retorna erro transiente (`429`, `500`, `502`, `503` ou `504`), o pipeline tenta novamente antes de gravar erro no checkpoint. Se houver header `Retry-After`, esse tempo e respeitado; sem o header, sao usados intervalos de `30s`, `60s` e `120s`. Se todas as tentativas falharem, o item recebe `status = error` e o processamento segue para o proximo item.

## Listar analises sem processar

Para conferir quais evidencias seriam processadas:

```bash
.venv/bin/python -m avaliacao_evidencias respostas.xlsx evidencias/ \
  --questionario igovti_2026.md \
  --prompts-dir avaliacao_evidencias/prompts/igovti_2026_conservador_v2 \
  --list-only
```

Para um conjunto parcial de prompts, como `igovti_2026_achados_binario_v1`, use `--only-prompts-present`. Essa opcao processa somente colunas com prompt existente no diretorio informado. Quando houver item afirmado avaliavel e o anexo correspondente estiver ausente, o pipeline registra conclusao `nao_conforme` sem chamar o provider.

```bash
.venv/bin/python -m avaliacao_evidencias respostas.xlsx evidencias/ \
  --questionario igovti_2026.md \
  --prompts-dir avaliacao_evidencias/prompts/igovti_2026_achados_binario_v1 \
  --prompt-version igovti_2026_achados_binario_v1 \
  --only-prompts-present \
  --list-only
```

## Retomada e deduplicacao

O pipeline grava um checkpoint incremental no arquivo JSONL de saida. Por padrao, o nome e derivado do provider e do modelo:

```text
.saida_analise/analyses_<provider>_<model>.jsonl
```

Exemplo: `--provider openrouter --model openai/gpt-5.4-mini` grava `.saida_analise/analyses_openrouter_openai_gpt-5.4-mini.jsonl`. Caracteres inadequados para nome de arquivo, como `/`, sao normalizados para `_`.

Use `--out-file` para escolher outro nome ou caminho. Se o valor for relativo, ele sera resolvido dentro de `--out-dir`; se for absoluto, sera usado diretamente:

```bash
.venv/bin/python -m avaliacao_evidencias respostas.xlsx evidencias/ \
  --questionario igovti_2026.md \
  --prompts-dir avaliacao_evidencias/prompts/igovti_2026_conservador_v2 \
  --provider gemini \
  --model gemini-2.5-flash \
  --out-dir .saida_analise \
  --out-file analyses.jsonl
```

Uma analise com `status = completed` nao e reprocessada se a identidade for a mesma.

A identidade considera:

- auditado;
- coluna de evidencia;
- nome original da evidencia;
- hash do arquivo de evidencia;
- provider;
- model;
- hash do prompt;
- `prompt_version`.

Erros sao retentados por padrao. Use `--skip-errors` para pular erros ja registrados:

```bash
.venv/bin/python -m avaliacao_evidencias respostas.xlsx evidencias/ \
  --questionario igovti_2026.md \
  --prompts-dir avaliacao_evidencias/prompts/igovti_2026_conservador_v2 \
  --prompt-version v2 \
  --provider gemini \
  --model gemini-2.5-flash \
  --out-dir .saida_analise \
  --skip-errors
```

## Saidas

```text
.saida_analise/
  analyses_<provider>_<model>.jsonl
  relatorio_conformidade.xlsx
```

O JSONL de analises contem uma linha por analise tentada, incluindo metadados, provider, modelo, resultado e erro quando houver.

`relatorio_conformidade.xlsx` contem uma linha por conclusao de conformidade, com estado, justificativa, lacunas e referencias.

Estados possiveis:

- `conforme`: a evidencia suporta diretamente o item afirmado.
- `nao_conforme`: a evidencia nao comprova ou contradiz o item afirmado.
- `inconclusivo`: ha indicios, mas falta elemento essencial para concluir.
- `erro`: a analise nao pode ser realizada por falha tecnica.

## Consolidar opinioes de modelos

Depois de executar a pre-analise com mais de um provider/modelo, gere um parecer consolidado por evidencia com:

```bash
.venv/bin/python -m avaliacao_evidencias.consolidacao \
  .saida_analise/teste_gemini/analyses*.jsonl \
  .saida_analise/teste_openrouter/analyses*.jsonl \
  --evidencias-root evidencias \
  --judge-provider gemini \
  --judge-model gemini-2.5-flash \
  --out-dir .saida_analise/consolidado
```

A etapa le um ou mais JSONL de analises, agrupa os resultados por `auditado + questao + coluna_evidencia + evidencia`, coleta as conclusoes emitidas pelos modelos e chama um modelo juiz para produzir um `Parecer consolidado de evidencia`.

A evidencia e reenviada ao juiz quando `--evidencias-root` e informado. Sem essa opcao, o juiz recebe apenas as opinioes dos modelos e deve registrar a lacuna de evidencia direta.

A chamada ao juiz nao envia nomes de provedores ou modelos no pacote de avaliacoes preliminares. O prompt orienta linguagem impessoal e institucional, propria de equipe de auditoria governamental, e padroniza a justificativa em: conclusao objetiva; elementos da evidencia; convergencia, divergencia ou fragilidade das avaliacoes recebidas; lacuna ou limitacao relevante.

A consolidacao usa a mesma camada de provider do processamento principal, portanto tambem aplica retries para erros transientes antes de registrar erro em `consolidated.jsonl`.

Opcionalmente, informe uma opiniao da equipe de auditoria:

```bash
.venv/bin/python -m avaliacao_evidencias.consolidacao .saida_analise/*/analyses*.jsonl \
  --auditor-opinions opinioes_auditoria.jsonl \
  --judge-provider openrouter \
  --judge-model google/gemini-2.5-flash
```

`--auditor-opinions` aceita JSONL, JSON ou CSV com campos como `auditado`, `questao`, `coluna_evidencia`, `evidencia` e `opiniao_auditoria`.

Saidas:

```text
.saida_analise/
  consolidated.jsonl
  pareceres_consolidados.xlsx
```

O parecer consolidado continua sendo pre-analise de auditoria e deve ser revisado por auditor humano.

## Manutencao de prompts

Para melhorar prompts:

1. Edite `avaliacao_evidencias/prompt_catalogs/igovti_2026_conservador_v2.yml`.
2. Regenere os Markdown com `python -m avaliacao_evidencias.prompt_catalog build ...`.
3. Rode os testes.
4. Execute o pipeline com novo `--prompt-version` se quiser forcar reprocessamento mesmo quando os arquivos de evidencia nao mudaram.

Exemplo:

```bash
.venv/bin/python -m unittest tests.test_avaliacao_evidencias.PromptCatalogV2Tests
```

Para rodar todos os testes do pacote:

```bash
.venv/bin/python -m unittest tests.test_avaliacao_evidencias
```

## Observacoes de auditoria

O resultado e uma pre-analise automatizada. O relatorio deve ser tratado como insumo para revisao humana, nao como decisao final de auditoria.

Os prompts v2 adotam postura conservadora: na duvida entre `conforme` e `inconclusivo`, o modelo deve usar `inconclusivo`; na ausencia de suporte direto, deve usar `nao_conforme`.

## Logs de execucao

Durante a execucao, o pipeline emite logs estruturados no `stdout`, em formato JSON Lines. Cada linha possui, no minimo, `ts`, `level`, `event` e `message`, alem de campos de contexto como `auditado`, `questao`, `coluna_evidencia`, `provider`, `model`, `status` e `error` quando aplicavel.

Exemplos de eventos: `pipeline_started`, `inventory_completed`, `checkpoint_loaded`, `analysis_started`, `evidence_resolved`, `prompt_resolved`, `items_selected`, `evidence_normalized`, `upload_prepared`, `rate_limit_wait`, `provider_started`, `provider_finished`, `analysis_recorded`, `report_generated` e `pipeline_finished`.

Para suprimir os logs em automacoes, use:

```bash
.venv/bin/python -m avaliacao_evidencias respostas.xlsx evidencias/ \
  --questionario igovti_2026.md \
  --prompts-dir avaliacao_evidencias/prompts/igovti_2026_conservador_v2 \
  --provider fake \
  --model fake \
  --quiet
```
