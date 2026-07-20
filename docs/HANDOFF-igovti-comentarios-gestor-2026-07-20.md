# Handoff — integridade dos comentários do gestor e relatório final iGovTI 2026

## Objetivo da próxima sessão

Retomar com segurança o reparo dirigido das avaliações dos comentários do gestor, validar a integridade de dados e pareceres, regenerar os produtos pós-contraditório e revisar os relatórios finais — especialmente o AN08 e o Capítulo 5 do relatório consolidado — antes da geração dos DOCX definitivos.

Repositório: `/home/acba/workspace/fiscalizacoes/202601-igovti`

Antes de agir, leia `AGENTS.md`. O worktree já estava amplamente modificado pelo usuário e por trabalhos anteriores; preserve alterações não relacionadas e não reverta arquivos em bloco.

## Contexto do incidente

Foi investigada uma inconsistência grave na avaliação dos comentários do gestor: no caso `UERJ / A5G20`, uma opinião individual devolveu corretamente `A5G20`, mas também introduziu uma conclusão externa sobre `q2708`. A consolidação e o mapeamento de ajustes aceitavam a união dos códigos retornados pelos avaliadores. Isso permitiu que a conclusão externa gerasse ajustes em respostas sem vínculo com `A5G20`, removendo indevidamente uma situação do resultado final.

O preflight e o arquivo `resumo-secao-2.json` apenas tornavam o efeito visível; não eram a origem do erro. A origem era combinada:

1. ausência de validação de pertencimento da resposta ao caso;
2. construção do escopo do juiz pela união das conclusões dos modelos;
3. mapeamento da seção 1 pelo estado temporal global, sem exigir que o motivo específico estivesse `afastado`;
4. ausência de uma porta de integridade antes da aplicação dos ajustes.

A inspeção mais ampla encontrou casos com códigos externos, motivos ausentes ou externos, estados temporais incompatíveis com os estados dos motivos e duas decisões antigas classificadas como `inconclusiva`. O usuário determinou que não exista classificação inconclusiva: insuficiência de elementos deve resultar em manutenção da situação, com não acolhimento ou acolhimento parcial conforme os motivos efetivamente afastados.

## Decisões substantivas já tomadas

- Ajustes da seção 1 devem ser aplicados por motivo, e somente quando o motivo ativo correspondente estiver classificado como `afastado`.
- Uma situação `mantida` pode gerar ajustes parciais se parte dos motivos tiver sido afastada.
- `afastada_na_data_base` e `corrigida_posteriormente` só são coerentes quando todos os motivos ativos tiverem sido afastados.
- Ausência ou insuficiência de prova mantém a situação; não usar `inconclusiva` nem `inconclusivo` no perfil temporal dos comentários do gestor.
- O juiz deve receber os itens autoritativos do caso, nunca a união de códigos sugeridos pelos avaliadores.
- Um caso pode ser consolidado com o quórum configurado de três avaliações válidas. A ausência de um avaliador opcional não invalida o caso; avaliação inválida conta como aviso e só exige reparo quando derruba o quórum ou quando o parecer consolidado é inválido.
- O reparo deve alcançar somente os casos afetados, mas usar todos os avaliadores atualmente habilitados. A configuração atual tem cinco avaliadores habilitados, inclusive `qwen3.7-plus`; o usuário aceitou o reparo dirigido com os avaliadores configurados, não uma reavaliação completa do universo pelo Qwen.
- Caso UERJ `A4G13`: restaurar `q2708[A] = Sim` e `q2708[B] = Sim`; manter `q2708[C] = Não` e `q2708[D] = Não`. A situação `A4G13` permanece caracterizada pelo fundamento relativo à segurança da informação. A legislação e o Manual de Cargos apresentados bastam para comprovar os cargos/funções de TIC.
- Não gerar ajustes, resultados ou relatórios definitivos enquanto a validação de integridade não estiver `conforme` e sem casos de reprocessamento.

## Implementação realizada nesta sessão

### Contrato de escopo e coerência

Criado `scripts/avaliacao_evidencias/scope_validation.py`, com validação determinística de:

- conjunto exato e cardinalidade dos `item_codigo`;
- duplicidade e códigos externos;
- conjunto exato dos motivos ativos;
- estados temporais permitidos;
- estados dos motivos permitidos;
- coerência entre estado temporal e estados dos motivos.

Integrações principais:

- `scripts/comentarios_gestor_pipeline.py` rejeita respostas individuais e pareceres do juiz fora do escopo;
- checkpoints inválidos não são tratados como avaliações utilizáveis;
- `scripts/avaliacao_evidencias/consolidation_core.py` prefere itens autoritativos gravados no caso; para checkpoints legados, só aceita fallback quando todas as opiniões possuem exatamente o mesmo conjunto de códigos;
- o juiz dos comentários recebe itens autoritativos, não a união das conclusões.

### Nova versão do prompt temporal

Criado:

`scripts/avaliacao_evidencias/prompt_catalogs/igovti_2026_comentarios_gestor_atual_v3.yml`

O catálogo exige preservação exata de `item_codigo` e `id_motivo`, elimina `inconclusiva` e manda manter a situação quando a prova for insuficiente.

O default foi atualizado em:

- `scripts/comentarios_gestor_pipeline.py`;
- `scripts/gerar_pacote_relatorios_igovti.py`.

Também foram removidos os estados temporais/motivos inconclusivos de:

- `scripts/avaliacao_evidencias/providers/response.py`;
- `scripts/avaliacao_evidencias/providers/base.py`;
- `scripts/avaliacao_evidencias/providers/fake.py`.

### Mapeamento dos ajustes por motivo

`mapear_ajustes_secao1` foi alterado para:

- validar o parecer antes do mapeamento;
- exigir que a conclusão pertença ao código da situação;
- correlacionar `id_motivo` do parecer com os motivos ativos do contexto;
- gerar ajustes somente para ações de motivos `afastado`;
- aceitar ajustes parciais de situações `mantida`;
- registrar justificativa e estado do motivo no papel de trabalho.

O caso contaminado `UERJ / A5G20` deixou de gerar qualquer ajuste em `q2708`.

### Revisão técnica reprodutível da UERJ

Criado:

`02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor/revisoes_respostas.yml`

Ele registra de forma declarativa e aprovada os ajustes `q2708[A]` e `q2708[B]` para `Sim`, vinculados ao caso `UERJ / A4G13`, ao `case_id` vigente e às referências documentais. `carregar_revisoes_respostas` materializa essas decisões e recusa revisões sem correspondência com o parecer vigente.

Antes da interrupção, uma leitura sem escrita confirmou:

- `q2708[B] = Sim` pelo motivo `MR048` afastado;
- `q2708[A] = Sim` pela revisão técnica documentada;
- `q2708[B] = Sim` também garantido pela revisão técnica;
- nenhum ajuste de `UERJ / A5G20` em `q2708`.

### Validação e reparo dirigido no CLI

Criado `scripts/comentarios_gestor_integridade.py`.

Adicionadas ações em `scripts/run_comentarios_gestor.py`:

- `validar-integridade`;
- `reparar-integridade`.

Artefatos produzidos:

- `02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor/preflight/validacao-integridade.json`;
- `.../validacao-integridade.xlsx`;
- `.../casos-reprocessamento.json`.

`reparar-integridade`:

1. prepara os casos autoritativos;
2. lê o manifesto de reparo;
3. reavalia somente os casos afetados com todos os avaliadores habilitados;
4. reconsolida somente os pareceres afetados;
5. preserva os demais registros;
6. valida novamente o conjunto.

`gerar-ajustes` e a ação `completo` agora bloqueiam a aplicação dos ajustes quando a integridade estiver reprovada.

As novas rotinas foram expostas em `scripts/argos_cli.py`. O orquestrador principal passou a aceitar `--revisoes-respostas` e usar o catálogo v3.

### Testes

Última execução local:

```bash
scripts/.venv/bin/python -m unittest discover -s scripts/tests -p 'test_*.py'
```

Resultado: 71 testes aprovados.

## Estado atual dos dados

Última validação completa, antes da tentativa de reparo:

- status: `reparo_necessario`;
- seção 1: 65 casos no manifesto;
- seção 2: 16 casos no manifesto;
- total: 81 casos.

O arquivo autoritativo para conferir esses números é:

`02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor/preflight/validacao-integridade.json`

Há centenas de avisos sobre avaliações individuais antigas inválidas, mas um caso só entra no reparo quando o quórum fica abaixo de três ou quando o parecer consolidado vigente viola o contrato. Não transformar todo aviso isolado em reprocessamento integral.

## Execução interrompida

Foi iniciado `reparar-integridade`, mas o usuário pediu para parar. Não há processo ativo; isso foi confirmado com `ps`.

A tentativa acrescentou registros de erro aos checkpoints históricos de três avaliadores, sem apagar resultados anteriores:

- Gemini 3.1;
- Gemini 3.5;
- GPT Luna.

Erros observados: `Temporary failure in name resolution`, inclusive durante upload Gemini. Os checkpoints são append-only. Não apague esses registros: a retomada, com `skip_errors=False`, repetirá as identidades que terminaram em erro. Não há evidência de chamadas bem-sucedidas ou consolidações novas nessa tentativa curta.

O `resumo-execucao.json` não representa a tentativa abortada; consulte os checkpoints e refaça a validação.

## Próximos passos obrigatórios

### 1. Garantir rede e executar novamente os testes

Não exponha o conteúdo de `.env`. Carregue-o no shell apenas para a execução:

```bash
cd /home/acba/workspace/fiscalizacoes/202601-igovti
scripts/.venv/bin/python -m unittest discover -s scripts/tests -p 'test_*.py'
set -a
source .env
set +a
```

### 2. Retomar o reparo dirigido

```bash
scripts/.venv/bin/python scripts/run_comentarios_gestor.py reparar-integridade \
  --respostas-comentarios 02-Execucao/05-Comentarios_Gestor/01-Coleta_LimeSurvey/20260716-respostas-bruto.xlsx \
  --evidencias-comentarios-root 02-Execucao/05-Comentarios_Gestor/01-Coleta_LimeSurvey/Evidencias_Coletadas/evidencias_extraidas \
  --out-dir 02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor
```

Não execute `completo`: com a versão nova do prompt, isso pode disparar reavaliação desnecessária do universo completo. O comando correto é `reparar-integridade`.

### 3. Validar novamente

```bash
scripts/.venv/bin/python scripts/run_comentarios_gestor.py validar-integridade \
  --respostas-comentarios 02-Execucao/05-Comentarios_Gestor/01-Coleta_LimeSurvey/20260716-respostas-bruto.xlsx \
  --evidencias-comentarios-root 02-Execucao/05-Comentarios_Gestor/01-Coleta_LimeSurvey/Evidencias_Coletadas/evidencias_extraidas \
  --out-dir 02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor
```

Porta obrigatória:

- `status = conforme`;
- zero casos de reprocessamento nas duas seções;
- nenhum parecer temporal inconclusivo;
- nenhum código ou motivo externo;
- pelo menos três avaliações válidas por caso.

Se falhar, não gerar ajustes. Investigue os casos remanescentes e repita o reparo.

### 4. Gerar e revisar os ajustes

Execute `gerar-ajustes` com os mesmos caminhos e com:

`--revisoes-respostas 02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor/revisoes_respostas.yml`

O comando possui porta de integridade. Depois, revise todas as linhas de `Ajustes` e `Pendências` em:

`02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor/ajustes_respostas_questionario_pos_comentarios_gestor.xlsx`

Pendências materiais devem ser resolvidas por decisão técnica explícita e reprodutível em `revisoes_respostas.yml`; não inventar valores.

Confirme especialmente os quatro itens `q2708` da UERJ e a permanência de `A4G13`.

### 5. Gerar produtos e cenários finais

A sequência completa, já detalhada na resposta anterior ao usuário, é:

1. `gerar_produtos_pos_comentarios_gestor.py` — somente os três produtos básicos;
2. orquestrador `gerar_pacote_relatorios_igovti.py`, etapas 19 a 21 — iGovTI corrente, auditoria pós-comentários e impactos;
3. `03-Relatorios/99-Avaliacao_Comentarios_Gestor/calcular_dados_comentarios_gestor.py` com avaliação final, ajustes e impactos;
4. revisão manual do AN08 e do Capítulo 5;
5. geração do DOCX do AN08;
6. etapas 22 e 23 — gráficos e relatórios individuais finais;
7. etapas 24 e 25 — relatório consolidado e validação final.

Use `--force-stage` nas etapas 19 a 25 para não adotar produtos antigos como definitivos. Não retome pela etapa 17 depois do reparo dirigido.

## Controles de qualidade antes da assinatura

O próximo agente deve verificar, a partir dos produtos finais e não de números antigos do Markdown:

- coerência entre base pós-comentários, iGovTI, auditoria, impactos, relatórios individuais, AN08 e relatório consolidado;
- ausência de `inconclusiva` em produtos e narrativa institucional;
- tabela manifestação do gestor × decisão técnica;
- concordâncias com situação ajustada apenas quando algum motivo tiver sido efetivamente afastado;
- justificativa de não acolhimento ou acolhimento parcial;
- totais de respondentes, não respondentes, manifestações, anexos e itens reavaliados;
- redução de situações e achados;
- variação do iGovTI;
- permanência de achados sustentados por motivos não afastados;
- nomes dos DOCX iguais à lista de anexos;
- inexistência de referências institucionais a providers, modelos, juiz de IA ou automação decisória;
- linguagem formal, simples, objetiva, imparcial e impessoal;
- recursos gráficos incorporados e nenhuma advertência de mídia ausente;
- `02-Execucao/00-Controle_Execucao/validacao-final.json` aprovado.

O script estatístico não edita `anexo-avaliacao-comentarios-gestor.md`; a atualização do texto do AN08 é atividade técnica/editorial manual baseada na memória de cálculo validada.

## Arquivos centrais para inspeção

- `scripts/avaliacao_evidencias/scope_validation.py`
- `scripts/comentarios_gestor_integridade.py`
- `scripts/comentarios_gestor_pipeline.py`
- `scripts/run_comentarios_gestor.py`
- `scripts/comentarios_gestor_produtos.py`
- `scripts/avaliacao_evidencias/consolidation_core.py`
- `scripts/avaliacao_evidencias/prompt_catalogs/igovti_2026_comentarios_gestor_atual_v3.yml`
- `scripts/avaliacao_evidencias/configs/comentarios_gestor_models_v1.json`
- `02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor/revisoes_respostas.yml`
- `02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor/revisoes_pareceres.yml`
- `02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor/preflight/validacao-integridade.json`
- `03-Relatorios/99-Avaliacao_Comentarios_Gestor/anexo-avaliacao-comentarios-gestor.md`
- `03-Relatorios/01-Relatorio_Consolidado/Relatório_altaresolucao_novo.md`

## Suggested skills

- `escrever-relatorio-auditoria`: usar na revisão do AN08, do Capítulo 5 e do relatório consolidado, depois que os dados finais estiverem estabilizados.
- `handoff`: usar novamente se a execução precisar ser interrompida antes da validação final.

Não é necessário usar uma skill de matriz de planejamento para esta continuação, salvo se a investigação revelar erro no mapa de verificação ou na lógica dos achados.
