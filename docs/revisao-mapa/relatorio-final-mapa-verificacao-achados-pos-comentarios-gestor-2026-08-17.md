# Relatório final de revisão do mapa de verificação de achados — versão pós-comentários do gestor

Data de referência: 17/08/2026  
Objeto: consolidação das revisões críticas, avaliação das propostas adicionais e implementação de versão sincronizada do mapa de verificação de achados e da matriz de planejamento.

## 1. Conclusão executiva

O mapa exigia ajustes materiais nas ações de verificação, nas regras das situações encontradas, na aba de motivos do relatório, nas variáveis temporárias e na correspondência com a matriz de planejamento. As alterações foram aplicadas em uma nova versão, sem substituição do mapa vigente.

O resultado consolidado é o seguinte:

- 24 situações encontradas permanecem configuradas; S4.4 e S4.5 foram retiradas do achado;
- 12 situações foram classificadas como `Determinação` e 12 como `Recomendação`;
- o mapa passou de 151 ações cadastradas, das quais 41 já estavam órfãs, para 72 ações, todas utilizadas nas fórmulas;
- S1.2 e S2.1 foram separados: S1.2 verifica as atribuições formalizadas da área de TIC por `q0103`; S2.1 verifica exclusivamente objetivos, indicadores e metas estabelecidos pela alta administração;
- as regras de S2.2/S2.3 foram recalibradas, mantendo `AV11 | AV89` em S2.2 e condicionando S2.3 à declaração de existência do Comitê; S3.5/S6.3 e S5.3/S5.4 foram desacopladas;
- S4.1 passou a exigir simultaneamente existência de estrutura formal e ausência de profissionais de TIC, sem inferência baseada no quantitativo de segurança da informação;
- o enunciado de Q6 e as situações S1.2, S4.1, S6.1, S6.2 e S6.4 foram harmonizados com os critérios efetivamente testados;
- a matriz de planejamento foi sincronizada em arquivo próprio;
- o painel pós-comentários vigente foi ampliado para materializar `q2801ext[B]`, sem duplicação de arquivo e sem gerar nova avaliação por IA.

As saídas continuam sendo minutas técnicas sujeitas à aprovação da equipe de auditoria, especialmente quanto à proporcionalidade, à competência do destinatário e à redação final de cada determinação.

## 2. Contradições identificadas e decisão adotada

| Tema | Propostas em tensão | Decisão aplicada | Motivação |
|---|---|---|---|
| S1.2 × S2.1 | S1.2 já verificava atribuições formais de governança, planejamento e gestão por `q0103`, enquanto S2.1 também utilizava `q1001ext[C]` para responsabilidades da área | S1.2 mantida com `q0103`; S2.1 restrita a `AV08 \| AV86`, correspondentes a `q1001ext[H]` e sua evidência | Elimina sobreposição material. A primeira situação trata do desenho e das competências da unidade; a segunda, do direcionamento e da mensuração da gestão de TIC. |
| S2.2 | Proposta anterior de restringir a situação a `AV11` versus orientação da equipe para preservar a verificação documental | `AV11 \| AV89` | Mantém como gatilhos alternativos a negativa declarada e a evidência insuficiente para comprovar a instituição formal do Comitê ou instância equivalente. |
| S4.1 | `AV26 & (AV25 \| AV27)` versus instrução posterior para retirar `total_SI` e usar `AV26 & AV25` | `AV26 & AV25` | Prevaleceu a instrução posterior e específica. O preenchimento na área predominante impede concluir que `total_SI = 0` significa ausência da função de segurança. |
| S6.3 | Menção inicial a `q2802ext[C-D]` e `q2804[B]` versus fórmula final `AV82 \| (AV80 \| AV150)` | `AV82 \| (AV80 \| AV150)` | Prevaleceu a fórmula final expressa. `q2802ext[D]` foi excluído. |
| S4.6 | Determinação por incapacidade de fiscalização versus gatilho isolado por predomínio de terceiros | `AV45 & AV46`, com AV45 restrita a `q0101 = B` | Predomínio de terceiros não comprova falta de fiscalização; o modelo C pode representar estrutura compartilhada legítima. |
| S6.1 | Inclusão de `q2801ext[B]` versus ausência dessa coluna no painel pós-comentários vigente | Incorporação de B e seus metadados ao próprio painel vigente | O catálogo já avaliava B. Foram reaproveitados 21 resultados não conformes existentes; nenhuma conclusão foi criada ou reavaliada. |
| Determinações | Dever jurídico de resultado versus ausência de norma que imponha literalmente “PDTI”, “Comitê” ou “inventário” em todos os contextos | Determinação com equivalência funcional e proporcionalidade | Evita impor modelo organizacional único quando o dever pode ser cumprido por estrutura ou instrumento equivalente. |

## 3. Alterações no mapa e na matriz de planejamento

| Objeto | DE | PARA | Motivação/justificativa |
|---|---|---|---|
| Fontes de Informação | Respostas pós-evidências e painel com descrição corrompida | Respostas e painel pós-comentários, com acentuação corrigida | Mantém o mapa no mesmo estado temporal dos dados reexecutados. |
| PA01/S1.1 | Recomendação | Determinação | Formalização mínima e responsabilização foram vinculadas aos princípios do art. 37 da CF e à governança prevista no art. 11 da Lei nº 14.133/2021, admitida estrutura equivalente. |
| PA01/S1.2 | “Área de TIC sem atribuições formais suficientes...” e Recomendação | “Área de TIC sem atribuições formalmente definidas ou sem atribuições formais de governança, planejamento ou gestão de TIC” e Determinação | Alinha a descrição aos itens `q0103` efetivamente testados e ao dever de atribuição de responsabilidades. |
| PA01/S1.3 | `q0102 = B, C, D ou E` | `q0102 = C, D ou E` | A subordinação estratégica de B é aceitável; a Portaria SGD/ME nº 778/2019 usa formulação preferencial, não absoluta. |
| PA02/S2.1 | “Modelo básico de governança e gestão de TIC”; quatro requisitos e oito ações: C, H, q1002A e q1002C | “Ausência de objetivos, indicadores ou metas para a gestão de TIC”; `AV08 \| AV86` | Retira `q1001ext[C]`/`AV07`/`AV85`, já abrangidos materialmente por S1.2, e reserva S2.1 ao direcionamento e à mensuração definidos pela alta administração. |
| PA02/S2.2 | Consolidação anterior previa apenas `AV11` | `AV11 \| AV89`; itens `q1001ext[E]` e `q1001evi` | Preserva tanto a resposta negativa quanto a insuficiência da evidência de instituição formal. O motivo documental `MR017` também foi restaurado. |
| PA02/S2.3 | `(AV12 \| AV90) & (AV13 \| AV91)` | `AV12 & (AV13 \| AV91)` | A inatividade só é imputável a quem declarou possuir Comitê. Os motivos foram condicionados à mesma regra composta. |
| PA03/S3.1 | A, B, C e D como requisitos cumulativos | `(AV17 \| AV95) \| ((AV14 \| AV92) \| (AV15 \| AV93))` | Mantém formalização, participação dos demandantes e priorização; retira análise de benefícios, custos e riscos como gatilho autônomo. |
| PA03/S3.2 | Recomendação | Determinação | Aprovação formal do plano pela instância competente, com fundamento consolidado em governança, planejamento e precedentes. |
| PA03/S3.5 | q2102C, q2802C, q2802D e q2804B; “vínculo com orçamento e contratações” | `AV20 \| AV98`; “Plano de TIC sem previsão orçamentária demonstrada” | Elimina o bis in idem com o achado de contratações e reserva S3.5 à perspectiva orçamentária do plano de TIC. |
| PA03/S3.6 | Recomendação | Determinação | O Acórdão TCE-RJ nº 44.490/2024, item II.3.5, contém precedente de monitoramento do PDTI em comando mandamental. |
| PA04/S4.1 | `AV25 \| AV27`; “TIC ou segurança da informação” | `AV26 & AV25`; “Ausência de força de trabalho dedicada à TIC” | Elimina falsa inferência baseada em `total_SI` e impede dupla punição de quem já está em S1.1. |
| PA04/S4.4 | Situação geradora de achado | Retirada do achado | A resposta negativa sobre perfis não comprova inadequação das pessoas designadas. Os temas permanecem disponíveis como indicadores de maturidade na matriz. |
| PA04/S4.5 | Situação geradora de achado | Retirada do achado | Identificação e tratamento de lacunas são boas práticas sem suporte suficiente para imputação automática. |
| PA04/S4.6 | Modelo B ou C com zero interno, ou predomínio de terceiros | Apenas modelo B com zero interno: `AV45 & AV46` | Modelo C pode ser legítimo e predomínio de terceiros não prova incapacidade. O tipo passou a Determinação, ligado ao dever de fiscalização contratual. |
| PA05/S5.1 | q2201A, B e C | q2201B e C | q2201A trata de metas por serviço, e não da existência/atualização/disponibilidade do catálogo. |
| PA05/S5.2 | q2201D e E | q2201A, D e E | Reúne metas, pactuação e monitoramento no bloco de níveis de serviço. |
| PA05/S5.3 | Recomendação | Determinação | O inventário foi tratado como meio de demonstrar medidas de segurança e governança previstas nos arts. 46 e 50 da LGPD, admitida solução equivalente. |
| PA05/S5.4 | q2203A e C | Apenas q2203C | Separa inventário/base consolidada da formalização do processo de configuração. |
| PA05/S5.5 | Recomendação | Determinação | Os arts. 46 e 48 da LGPD sustentam segurança e comunicação de incidentes relevantes. |
| Q6 | Questão ampla sobre planejamento, contratação, fiscalização e gestão | “A organização adota controles mínimos na fase preparatória das contratações de TIC, com processo definido e análise técnica pela unidade competente?” | O enunciado passa a refletir o escopo das situações testadas. |
| PA06/S6.1 | q2801 A, C, D, E e G; Recomendação | q2801 A e B; `AV73 \| AV143 \| AV152 \| AV153`; Determinação | Foca processo e artefatos padronizados da fase preparatória, em correspondência com os arts. 11 e 19, IV, da Lei nº 14.133/2021. |
| PA06/S6.2 | “...aprovação técnica obrigatória...” | “Contratações de TIC sem análise prévia e aprovação técnica da área de TIC” | Retira qualificação absoluta e preserva análise proporcional à complexidade e ao risco. |
| PA06/S6.3 | q2102C, q2802C, q2802D e q2804B; Recomendação | `AV82 \| (AV80 \| AV150)`; Determinação | Reserva a situação ao alinhamento da execução das contratações com os instrumentos de planejamento e com o PCA. |
| PA06/S6.4 | “...equipe formalmente designada e com participação técnica...” | “Contratações de TIC sem designação de Equipe de Planejamento com integrante técnico da área de TIC” | Explicita o núcleo da situação testada. |
| Ações de Verificação | 151 ações; 41 órfãs antes da revisão | 72 ações; zero órfãs | Remove ações sem efeito, preserva AV89 em S2.2 e mantém AV07/AV85 fora dos achados. A lista completa está na planilha de ajustes. |
| Motivos do Relatório | Condições e textos das regras anteriores | 71 motivos sincronizados, incluindo MR017 e os motivos de q2801B | Evita que gates positivos sejam apresentados isoladamente como situação encontrada e remove referências a ações excluídas. |
| Variáveis Temporárias | VT01 a VT05 | VT01 (`total_TI`) e VT03 (`total_TI_interno`) | `total_SI`, `total_TI_terceiros` e `predominio_terceiros` deixaram de ser usados. |
| Matriz de Planejamento | Regras, itens, descrições, critérios e tipos anteriores | Nova versão pós-comentários sincronizada | Garante rastreabilidade entre planejamento e execução. |
| Painel de evidências | Sem `q2801ext[B]` por filtragem do mapa antigo | Mesmo arquivo ampliado com B e três colunas de metadados | Viabiliza AV153 com resultados de avaliação já existentes, sem manter painel paralelo. |

A planilha de ajustes contém, além desta consolidação, a relação individual das 81 ações retiradas, a ordem de implementação, as ressalvas jurídicas e o impacto da reexecução.

## 4. Consolidação dos encaminhamentos convertidos em determinação

| Situação | Tipo final | Fundamento consolidado | Ressalva necessária na aplicação |
|---|---|---|---|
| S1.1 | Determinação | CF, art. 37; Lei nº 14.133/2021, art. 11, parágrafo único | Admitir estrutura equivalente e observar eventual reserva legal para criação de órgão ou cargo. |
| S1.2 | Determinação | CF, art. 37; Lei nº 14.133/2021, art. 11, parágrafo único | Exigir atribuições mínimas, sem impor desenho organizacional único. |
| S2.2 | Determinação | Lei nº 14.133/2021, art. 11; Acórdãos TCE-RJ nº 44.490/2024 e TCU nº 1.411/2014 | O precedente do TCE-RJ contém determinação; o item 9.1 do precedente do TCU contém recomendação. |
| S2.3 | Determinação | CF, art. 37; Acórdão TCE-RJ nº 44.490/2024 | Aplicar apenas a quem declarou possuir Comitê ou instância equivalente. |
| S3.1 | Determinação | Lei nº 14.133/2021, arts. 11 e 18; precedentes TCU/TCE-RJ | Admitir instrumento equivalente a PDTI/PEDTIC que satisfaça o resultado. |
| S3.2 | Determinação | Lei nº 14.133/2021, arts. 11 e 18; precedentes TCU/TCE-RJ | A aprovação deve ser da instância competente, sem colegiado obrigatório único. |
| S3.6 | Determinação | CF, art. 37; Acórdão TCE-RJ nº 44.490/2024, item II.3.5 | Vincular acompanhamento e revisão ao plano efetivamente adotado. |
| S4.6 | Determinação | Lei nº 14.133/2021, art. 117 | O artigo exige fiscalização, não quadro próprio de TIC; a regra calibrada exige terceirização predominante e ausência total de pessoal interno. |
| S5.3 | Determinação | LGPD, arts. 46 e 50 | A LGPD não nomeia inventário; o encaminhamento deve admitir controle equivalente que demonstre segurança e governança. |
| S5.5 | Determinação | LGPD, arts. 46 e 48 | A comunicação legal é exigível para incidente que possa acarretar risco ou dano relevante. |
| S6.1 | Determinação | Lei nº 14.133/2021, arts. 11 e 19, IV | O art. 19, IV, tem destinatário qualificado; demais unidades podem adotar modelos aplicáveis, próprios ou compartilhados. |
| S6.3 | Determinação | Lei nº 14.133/2021, arts. 12, VII, e 18 | A compatibilização com o PCA é exigível quando o plano tiver sido elaborado. |

O art. 63 da Lei Complementar estadual nº 63/1990 prevê multa, entre outras hipóteses, pelo não atendimento injustificado de decisão do Tribunal. Isso não dispensa a motivação individualizada, a definição clara do resultado esperado e a análise da competência de cada jurisdicionado.

Fontes jurídicas conferidas: [Constituição Federal, art. 37](https://www.planalto.gov.br/ccivil_03/constituicao/constituicaocompilado.htm), [Lei nº 14.133/2021](https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/lei/l14133.htm), [Lei nº 13.709/2018 — LGPD](https://planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/L13709.htm), [Lei Complementar estadual nº 63/1990](https://alerjln1.alerj.rj.gov.br/contlei.nsf/f25571cac4a61011032564fe0052c89c/4b2972bdc563e76603256652006b849b), [Acórdão TCE-RJ nº 44.490/2024-PLEN](../../01-Planejamento/01-Estudos_Preliminares/Antecedentes/Acordao_44490_2024.PDF) e [Acórdão TCU nº 1.411/2014-Plenário](<../../01-Planejamento/01-Estudos_Preliminares/Antecedentes/Acórdão 1411 de 2014 Plenário.pdf>).

## 5. Resultado da reexecução sobre a base pós-comentários

A execução comparativa usou a mesma base pós-comentários e variou apenas o mapa e o painel compatível.

| Indicador | Mapa anterior | Mapa revisado | Variação |
|---|---:|---:|---:|
| Auditados avaliados | 113 | 113 | 0 |
| Cadastros sem resposta válida | 6 | 6 | 0 |
| Ocorrências de situação encontrada | 2.096 | 1.727 | -369 (-17,6%) |
| Achados por combinação órgão × procedimento | 620 | 599 | -21 |
| Situações configuradas | 26 | 24 | -2 |
| Ações cadastradas | 151 | 72 | -79 em relação ao total; 81 IDs do cadastro de origem foram retirados e 2 novos foram incluídos |
| Ações órfãs | 41 | 0 | -41 |
| Organizações simultaneamente em S2.2 e S2.3 | 7 | 0 | -7 |

O total de 17 duplas imputações mencionado na proposta não se reproduziu na base pós-comentários de 16/07/2026. A reexecução encontrou sete organizações simultaneamente classificadas em S2.2 e S2.3 no mapa anterior, e nenhuma no mapa revisado. A diferença temporal ou de versão deve ser considerada antes de usar o número 17 em relatório.

Com a restauração de `AV89`, oito organizações acionaram essa verificação documental; em todas elas `AV11` também estava presente. Assim, S2.2 permaneceu com 75 ocorrências, sem alteração dos totais e sem nova concomitância com S2.3 na base atual.

Impactos relevantes observados:

| Situação | Antes | Depois | Leitura |
|---|---:|---:|---|
| S2.1 | 107 | 94 | Restrição a objetivos, indicadores e metas; responsabilidades da área permanecem exclusivamente em S1.2. |
| S2.2 | 75 | 75 | `AV89` foi mantida; suas oito ocorrências também acionaram `AV11`, sem aumento da situação na base atual. |
| S2.3 | 27 | 20 | Exclusão das sete duplas imputações efetivas na base atual. |
| S3.1 | 98 | 92 | Retirada de q2101C como gatilho autônomo. |
| S3.5 | 106 | 79 | Restrição à previsão orçamentária do plano de TIC. |
| S4.1 | 59 | 0 | Nenhuma entidade com estrutura declarada apresentou total de profissionais de TIC igual a zero na base atual. |
| S4.4 | 111 | 0 | Situação retirada do achado. |
| S4.5 | 112 | 0 | Situação retirada do achado. |
| S4.6 | 17 | 1 | Exclusão do modelo C e do predomínio de terceiros como provas autônomas. |
| S5.4 | 110 | 108 | Restrição à formalização do processo, q2203C. |
| S6.1 | 98 | 88 | Restrição à fase preparatória, itens A e B. |
| S6.3 | 106 | 100 | Restrição a q2802C e q2804B. |

Essas variações são efeito das novas regras, não conclusão de saneamento pelos jurisdicionados. A equipe deve revisar amostras limítrofes antes de substituir os produtos oficiais.

## 6. Ordem de implementação e validação

1. Congelar os insumos vigentes e trabalhar apenas em versões com sufixo pós-comentários.
2. Fixar as fórmulas canônicas e registrar a decisão sobre cada contradição.
3. Atualizar a aba Fontes de Informação para a base e o painel pós-comentários.
4. Calibrar as ações declaratórias e documentais, preservando pares apenas quando a evidência altera validamente a resposta.
5. Reescrever as seis fórmulas de achado e conferir todas as referências de ações.
6. Sincronizar a aba Motivos do Relatório, incluindo condições compostas para gates positivos.
7. Remover ações órfãs e variáveis temporárias não utilizadas.
8. Materializar `q2801ext[B]` no painel vigente a partir das avaliações existentes.
9. Atualizar a matriz de planejamento: questão, situação, itens, regra, critérios, referências e tipo de encaminhamento.
10. Executar o validador estrutural do mapa e exigir zero ação órfã, zero coluna ausente e zero fórmula inválida.
11. Reexecutar a auditoria em modo somente dados com a base e o painel pós-comentários.
12. Comparar situações e achados antes/depois, com atenção a S2.2/S2.3, S3.5/S6.3, S4.1 e S4.6.
13. Regenerar matriz de achados e relatórios somente após aprovação dos impactos.
14. Submeter as determinações à revisão humana final quanto a mérito, competência, proporcionalidade, prazo e resultado verificável.

## 7. Artefatos produzidos e validações

- `02-Execucao/03-Execucao_Procedimentos/01-Insumos/mapa-verificacao-achados-pos-comentarios-gestor.xlsx`;
- `01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/matriz_planejamento-pos-comentarios-gestor.md`;
- `02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor/fontes-auditoria-pos-comentarios/painel-avaliacao-evidencias.xlsx`;
- `docs/revisao-mapa/ajustes-mapa-verificacao-achados-pos-comentarios-gestor-2026-08-17.xlsx`;
- script reprodutível `scripts/gerar_revisao_mapa_pos_comentarios.py`.

Validações concluídas:

- mapa carregado e validado sem erro de fonte, coluna, booleano, identificador ou fórmula;
- 72 ações utilizadas e nenhuma ação órfã;
- 71 motivos sem referência a ação inexistente;
- somente VT01 e VT03 mantidas;
- auditoria pós-comentários executada com sucesso para 113 auditados;
- matriz revisada convertida em DOCX de validação sem erro;
- arquivos vigentes preservados.

Produtos temporários de validação:

- `/tmp/tcerj-igovti-2026/revisao-mapa/resultado-auditoria-mapa-revisado.json`;
- `/tmp/tcerj-igovti-2026/revisao-mapa/resultado-auditoria-mapa-revisado-detalhado.json`;
- `/tmp/tcerj-igovti-2026/revisao-mapa/tabelas-auditoria-mapa-revisado.xlsx`;
- `/tmp/tcerj-igovti-2026/revisao-mapa/matriz-planejamento-pos-comentarios-gestor.docx`.
