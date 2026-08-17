# Ordem de implementação e validação — mapa de verificação de achados pós-comentários do gestor

**Fiscalização TCE-RJ nº 18/2026 — iGovTI 2026**
**Data:** 17/08/2026
**Natureza:** roteiro executivo para assegurar integridade e sincronia entre mapa, matriz, painel de evidências e produtos da auditoria.

## 1. Artefatos de referência

| Artefato | Caminho | Status |
|---|---|---|
| Mapa original (produção, preservado) | `02-Execucao/03-Execucao_Procedimentos/01-Insumos/mapa-verificacao-achados.xlsx` | Intacto |
| **Mapa novo pós-comentários** | `02-Execucao/03-Execucao_Procedimentos/01-Insumos/mapa-verificacao-achados-pos-comentarios-gestor.xlsx` | Gerado e validado |
| Planilha de ajustes (DE→PARA, contradições, encaminhamentos, impacto) | `docs/revisao-mapa/ajustes-mapa-verificacao-achados-pos-comentarios-gestor-2026-08-17.xlsx` | Gerada |
| Painel de evidências pós-comentários (com q2801ext[B]) | `02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor/fontes-auditoria-pos-comentarios/painel-avaliacao-evidencias.xlsx` | Atualizado no arquivo vigente |
| Base de respostas pós-comentários | `02-Execucao/01-Questionario/03-Respostas_Processadas/20260716-respostas-questionario-pos-comentarios-gestor.xlsx` | Referência do mapa novo |
| Matriz de planejamento | `01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/matriz_planejamento-pos-comentarios-gestor.md` | Sincronizada em 17/08/2026 |
| Relatório final de consolidação | `docs/revisao-mapa/relatorio-final-mapa-verificacao-achados-pos-comentarios-gestor-2026-08-17.md` | Registro da consolidação |

## 2. Ordem de implementação (executada em 17/08/2026)

| # | Etapa | Produto/controle | Critério de aceite | Status |
|---|---|---|---|---|
| 1 | Congelar o mapa vigente e criar a versão pós-comentários em arquivo novo | Mapa novo nomeado `...pos-comentarios-gestor.xlsx` | Mapa vigente preservado; painel atualizado em etapa própria | ✅ |
| 2 | Resolver as contradições do conjunto de propostas e fixar uma regra única por situação | Aba `Contradições resolvidas` da planilha de ajustes | Uma regra por situação, com precedência documentada | ✅ |
| 3 | Atualizar as fontes temporais do mapa (base e painel pós-comentários) | Aba `Fontes de Informação` | Base `20260716-...` e `painel-avaliacao-evidencias.xlsx` referenciados | ✅ |
| 4 | Calibrar ações: religar AV26 (gate de S4.1), criar AV152/AV153 (q2801ext[B]), restringir AV45 (q0101 B), manter AV89 e remover órfãs | Aba `Ações de Verificação` (151 → 72 ações) | Toda coluna existe na fonte; zero ações órfãs | ✅ |
| 5 | Reescrever as fórmulas PA02–PA06 (PA01 mantida) | Aba `Procedimentos de Auditoria` | Fórmulas parseáveis, sem ações inexistentes | ✅ |
| 6 | Ajustar Motivos do Relatório (condições, ordens, renames, remoções; MR111/MR112 novos) | Aba `Motivos do Relatório` | Condições e referências usam apenas ações existentes | ✅ |
| 7 | Converter 12 situações para Determinação e acrescentar fundamento jurídico aos critérios | Aba `Ações de Verificação` (41 ações) | Fundamentos registrados (CF/88; Lei 14.133/2021; LGPD; Acórdãos TCU 1.411/2014 e TCE-RJ 44.490/2024) | ✅ |
| 8 | Renomear situações (S1.2, S2.1, S2.3, S3.5, S4.1, S6.1, S6.2, S6.3, S6.4) e a questão Q6 | Ações + Motivos + PA06 | Textos idênticos nos três locais | ✅ |
| 9 | Remover variáveis sem consumidor (VT02, VT04, VT05) e corrigir encoding da fonte | Abas `Variáveis Temporárias` e `Fontes de Informação` | Sem variáveis órfãs | ✅ |
| 10 | Incorporar q2801ext[B] ao painel de evidências vigente | `painel-avaliacao-evidencias.xlsx` | Colunas de todos os itens consumidos presentes; nenhum painel paralelo | ✅ |
| 11 | Sincronizar a matriz de planejamento (regras, itens, descrições, tipos, Q6, exclusão de S4.4/S4.5 do achado) | `matriz_planejamento-pos-comentarios-gestor.md` | 24 situações (12 Determinação + 12 Recomendação); regras idênticas às fórmulas do mapa | ✅ |
| 12 | Validar a execução com `executa_auditoria.py --somente-dados` | Resultado em `.scratch/validacao-pos-comentarios/` | Execução sem erros; 113 auditados avaliados | ✅ |
| 13 | Comparar impacto antes × depois por achado e situação | Aba `Impacto da reexecução` da planilha de ajustes | Toda diferença explicável por ajuste aprovado | ✅ |
| 14 | Revisão jurídica das determinações e deliberação da Equipe | Minuta para deliberação | Aprovação expressa antes de substituir o mapa de produção | ⏳ pendente |
| 15 | Regenerar produtos finais (matriz de achados, relatórios individuais, consolidado, tabelas e gráficos) com o mapa aprovado | `gerar_matriz_achados.py`, geradores de relatório | Sem recursos ausentes; Determinações exibidas como tal | ⏳ pendente |

## 3. Validação executada (17/08/2026)

```text
executa_auditoria.py --somente-dados
  --mapa mapa-verificacao-achados-pos-comentarios-gestor.xlsx
  --fontes 20260716-respostas-questionario-pos-comentarios-gestor.xlsx
           painel-avaliacao-evidencias.xlsx
```

- **Estrutura do mapa:** aprovada (validação de fontes/ações/colunas/lógicas/motivos sem erro).
- **Ações órfãs:** zero (72 ações, todas referenciadas).
- **Execução:** 113 auditados avaliados; 6 cadastros sem resposta válida ao questionário (CEHAB, EMOP, PESAGRO, SEDCON, SEPOL, SESP) — mesmo comportamento da execução anterior.

### Impacto por achado (antes → depois)

| Achado | Antes (pós-comentários) | Depois (mapa revisado) | Variação |
|---|---:|---:|---:|
| A1 — Estrutura de TIC | 68 | 68 | 0 |
| A2 — Governança e Comitê | 107 | 101 | −6 |
| A3 — Planejamento de TIC | 108 | 100 | −8 |
| A4 — Capacidade institucional | 113 | 109 | −4 |
| A5 — Gestão de serviços | 113 | 113 | 0 |
| A6 — Contratações de TIC | 111 | 108 | −3 |

### Impacto por situação (principais variações)

| Situação | Antes | Depois |
|---|---:|---:|
| S2.1 (objetivos, indicadores e metas) | 107 | 94 |
| S2.3 (atuação do comitê) | 27 | 20 |
| S3.1 (processo de planejamento) | 98 | 92 |
| S3.5 (previsão orçamentária do plano) | 106 | 79 |
| S4.1 (força de trabalho de TIC) | 59 | 0 |
| S4.6 (modelo B sem pessoal interno) | 17 | 1 |
| S5.4 (formalização da configuração) | 110 | 108 |
| S6.1 (planejamento das contratações) | 98 | 88 |
| S6.3 (alinhamento ao PCA) | 106 | 100 |
| S4.4/S4.5 (perfis/lacunas) | 111/112 | removidas do achado |

## 4. Ressalvas registradas para deliberação da Equipe

1. **S2.2 = AV11 (exclusiva declaração):** declaração de comitê com evidência insuficiente de instituição não gera S2.2 nem bloqueia S2.3.
2. **AV26 mantém `q0101 != F`:** organização em modelo C (Centralizada Externa) com zero pessoal interno de TI pode ser apontada em S4.1 (na execução atual não houve caso).
3. **S6.1 com q2801ext[B]:** subitem B sem avaliação documental no painel original; a versão revisada materializou a coluna (AV153). Confirmar a suficiência dos registros materializados.
4. **Fundamentos jurídicos:** art. 19, IV (dirige-se a órgãos com competência regulamentar) e art. 18 (ressalva "sempre que elaborado") exigem redação cuidadosa nas determinações de S6.1 e S6.3; a natureza jurídica foi registrada com "equivalência funcional" para Comitê/PDTI/inventário.
5. **S4.6 — redação:** encaminhamento inicia com "avalie o modelo de operação..."; para determinação, recomenda-se comando objetivo ("assegure capacidade interna... formalmente designada").
6. **S5.5 unificada (serviços + segurança):** fundamento LGPD (arts. 46/48) é robusto para o ramo de segurança; para incidentes de serviço, avaliar redação no relatório.
7. **Revisão humana obrigatória:** mapa, matriz, painel e resultados são minuta técnica; a substituição do mapa de produção depende de aprovação expressa da Equipe.

## 5. Sincronia entre artefatos

- A matriz de planejamento foi atualizada em 17/08/2026 para refletir exatamente as 24 situações, as regras (equivalente às fórmulas PA01–PA06), as descrições renomeadas, a questão Q6 renomeada e os 12 tipos Determinação do mapa novo.
- O mapa novo aponta para a base de respostas pós-comentários (`20260716-...`) e para o painel de evidências do mapa revisado.
- A planilha de ajustes registra todo o DE→PARA com motivação, as contradições resolvidas e o impacto da reexecução.
