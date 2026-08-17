# Revisão crítica da matriz de planejamento e do mapa de verificação de achados

## Identificação

| Campo | Informação |
|---|---|
| Fiscalização | TCE-RJ nº 18/2026 — iGovTI 2026 |
| Objeto | Matriz de planejamento e mapa de verificação de achados |
| Data da análise | 14/08/2026 |
| Modelo responsável pela análise | GPT-5.6 Sol |
| Natureza | Minuta técnica sujeita à revisão e aprovação da Equipe de Auditoria |

## 1. Parecer executivo

A matriz e o mapa precisam de revisão antes da consolidação definitiva dos achados e dos relatórios finais.

Os seis temas são relevantes, mas parte da lógica transforma práticas de maturidade elevada em requisitos mínimos universais. O principal indício é a incidência pós-comentários: entre 113 organizações avaliadas, os Achados 4 e 5 alcançaram 100% da população; os Achados 2, 3 e 6 ficaram entre 94,7% e 98,2%.

A revisão concluiu que:

- as questões 1, 2, 3 e 5 devem ser mantidas, com ajustes de escopo e lógica;
- o Achado 4 deve ser substancialmente reformulado;
- a Questão e o Achado 6 devem ser limitados à governança técnica da fase preparatória;
- algumas situações devem ser removidas como achado e preservadas apenas como indicadores de maturidade ou risco;
- há fundamento para converter em determinação a instituição de Comitê de TIC ou instância equivalente e a instituição formal de processo/PDTI;
- fragilidades qualitativas em controles já existentes devem permanecer como recomendações; e
- o mapa é estruturalmente válido, mas contém 41 ações que não participam de nenhuma lógica de achado ou motivo do relatório.

Foram examinados:

- `01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/matriz_planejamento.md`;
- `02-Execucao/03-Execucao_Procedimentos/01-Insumos/mapa-verificacao-achados.xlsx`;
- `01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md`;
- os resultados da auditoria pós-comentários do gestor;
- a planilha de verificação de evidências;
- o catálogo ativo de prompts de avaliação de evidências; e
- os Acórdãos TCE-RJ nº 44.490/2024-PLEN e TCU nº 1.411/2014-Plenário armazenados no repositório.

## 2. Diagnóstico dos resultados atuais

| Achado | Organizações | Incidência |
|---|---:|---:|
| A1 — Estrutura de TIC | 68 | 60,2% |
| A2 — Governança e Comitê | 107 | 94,7% |
| A3 — Planejamento de TIC | 108 | 95,6% |
| A4 — Capacidade institucional | 113 | 100,0% |
| A5 — Gestão de serviços | 113 | 100,0% |
| A6 — Contratações de TIC | 111 | 98,2% |

Fonte: `02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/03-pos-comentarios-gestor/resultado_auditoria.json`.

A alta incidência não invalida automaticamente os achados, mas reduz sua capacidade discriminatória. Nos Achados 4, 5 e 6, ela está associada principalmente a regras em que a ausência de qualquer subitem, isoladamente, caracteriza insuficiência ampla.

## 3. Revisão por questão e situação

### 3.1. Q1 — Estrutura de TIC

Manter a questão e o achado, com ajustes.

#### S1.1 — Ausência de estrutura formal

Manter. É uma deficiência institucional básica, mas o encaminhamento deve continuar como recomendação, pois os critérios citados são predominantemente referenciais técnicos.

#### S1.2 — Atribuições formais insuficientes

Dividir em duas situações:

1. inexistência de qualquer atribuição formal, com severidade alta; e
2. ausência de atribuições formais de governança, planejamento ou gestão, com severidade média.

A redação atual menciona planejamento, coordenação, gestão, execução, monitoramento e controle, mas a ação principal `q0103[D]` testa apenas governança, planejamento ou gestão.

#### S1.3 — Posicionamento inadequado

Ajustar. A matriz considera a alternativa `q0102 == B` inadequada, enquanto o mapa corretamente não a considera. A alternativa B representa vinculação a estrutura de nível estratégico e deve ser aceita.

Recomenda-se também retirar a alternativa C como gatilho automático. Subordinação a área administrativa ou financeira não prova, isoladamente, ausência de interlocução com a alta administração. A situação deveria ser caracterizada apenas pelas alternativas D e E ou por evidência adicional de baixa participação decisória.

Há ainda um erro latente no catálogo ativo `scripts/avaliacao_evidencias/prompt_catalogs/igovti_2026_achados_binario_v1.yml`: os critérios de `q0102[B]`, `q0102[C]` e `q0102[D]` exigem que a área se reporte diretamente ao dirigente máximo, alterando o significado das próprias alternativas. O prompt deve apenas verificar se a evidência confirma a posição declarada. A correção deve ser feita no YAML e seguida da regeneração dos prompts.

### 3.2. Q2 — Governança e Comitê de TIC

Manter a questão e o achado, mas separar seus componentes.

#### S2.1 — Modelo básico de governança

A lógica atual exige simultaneamente papéis, objetivos, indicadores, metas, rotina de monitoramento e indicadores implantados. Recomenda-se dividir em:

- ausência de elementos básicos de direção: `q1001ext[C]` ou `q1001ext[H]` não demonstrados; e
- ausência de monitoramento: situação caracterizada quando tanto a rotina quanto a implantação de indicadores não estiverem demonstradas, evitando que uma fragilidade isolada gere o título amplo.

#### S2.2 — Comitê não instituído

Manter e converter em determinação.

#### S2.3 — Comitê sem atuação efetiva

Manter como recomendação, mas corrigir a lógica.

A lógica atual aceita `AV90`, que significa evidência não conforme da instituição do comitê, como se fosse prova de que o comitê existe. Isso permite que a mesma organização seja apontada simultaneamente por “comitê não instituído” e “comitê sem atuação”.

Lógica sugerida:

```text
~(AV11 | AV89) & (AV13 | AV91)
```

Assim, a atuação somente será testada quando a instituição formal não tiver sido considerada inconforme.

### 3.3. Q3 — Planejamento de TIC

Manter a questão e o achado. É o bloco com maior suporte jurisprudencial, mas a lógica deve distinguir inexistência de imaturidade.

#### S3.1 — Processo de planejamento

Separar em:

- ausência de processo formal, baseada em `q2101ext[D]`: determinação; e
- processo existente, mas sem participação ou critérios de priorização: recomendação.

Retirar `q2101ext[C]` como gatilho universal. Análises de benefícios, custos e riscos devem ser proporcionais à materialidade das iniciativas, não obrigatórias com a mesma profundidade em todos os casos.

#### S3.2 — Aprovação do plano

Ajustar a descrição para “Plano de TIC inexistente, não demonstrado ou sem aprovação formal” e converter o encaminhamento em determinação.

#### S3.4 — Alinhamento institucional

Manter como recomendação quando houver plano existente, porém deficiente.

#### S3.5 — Vínculo com orçamento e contratações

Restringir a `q2102ext[C]` e à respectiva avaliação documental. As ações sobre `q2802ext[C]`, `q2802ext[D]` e `q2804[B]` medem o PCA ou contratações concretas e geram duplicidade com o Achado 6.

#### S3.6 — Acompanhamento e revisão

Manter como recomendação para planos existentes.

### 3.4. Q4 — Capacidade institucional de TIC e segurança

Recomenda-se alterar o título do achado para:

> Fragilidades no planejamento da força de trabalho e das competências de TIC e segurança da informação.

A formulação atual afirma insuficiência material de capacidade, mas o questionário não mede produtividade, criticidade das atividades, qualidade da fiscalização, suficiência real da equipe ou capacidade de estruturas compartilhadas.

Recomendações:

- **S4.1:** retirar `total_SI == 0`. O questionário manda registrar o profissional que atua em TI e segurança somente na área predominante. Zero em SI não prova ausência da função.
- Redigir S4.1 como “A organização não informou profissionais que atuem predominantemente em TIC” e reduzir a severidade para média.
- **S4.2:** manter como fragilidade de planejamento da força de trabalho, com severidade média.
- **S4.3 — Cargos ou funções específicas:** remover como situação inconforme. Cargos genéricos, designações, estruturas compartilhadas e prestação externa podem ser soluções legítimas.
- **S4.4 — Perfis profissionais:** retirar do achado e manter como indicador de maturidade. A negativa não prova inadequação das pessoas designadas.
- **S4.5 — Lacunas de competências:** restringir a `q2705ext[C]` e `q2705ext[D]`, referentes às competências técnicas de TIC e segurança. A ausência de plano de capacitação não prova ausência de tratamento, que também pode ocorrer por realocação, recrutamento ou apoio especializado.
- **S4.6 — Dependência externa:** remover como achado. Predominância numérica de terceiros não demonstra incapacidade de coordenação ou fiscalização.

Lógica recomendada para o PA04:

```text
AV25
|
(
  (AV29 | AV103)
  &
  (
    (AV40 | AV114)
    |
    (AV41 | AV115)
  )
)
```

Nenhum encaminhamento do Achado 4 deve ser convertido em determinação com a fundamentação atual.

### 3.5. Q5 — Gestão de serviços de TIC

Manter a questão, mas reduzir o nível de prescrição uniforme.

#### S5.1 — Catálogo

Retirar `q2201ext[B]`, que depende de compatibilidade com ANS e duplica S5.2. Recomenda-se também retirar `q2201ext[A]` da situação de catálogo e tratá-lo no bloco de níveis de serviço. A situação passaria a medir existência e disponibilidade do catálogo por `q2201ext[C]`.

#### S5.2 — Níveis de serviço

Manter como recomendação aplicável aos serviços relevantes. Aceitar metas de atendimento ou compromissos equivalentes, sem exigir necessariamente ANS bilateral formal para todo serviço.

#### S5.3 — Inventário

Retirar `q2203ext[A]`, que mede base de configuração e relacionamentos. Usar as ações de inventário de ativos da informação, dispositivos e softwares: `AV60/AV130`, `AV62/AV132` e `AV63/AV133`.

#### S5.4 — Gestão de configuração

Tratar como prática de maturidade ou limitar a serviços críticos. Uma base completa de relacionamentos próxima a uma CMDB não é mínimo universal para organizações pequenas.

#### S5.5 — Incidentes

Dividir em:

- processo de incidentes de serviços: priorização, escalamento e formalização; e
- tratamento de incidentes de segurança: procedimentos, responsabilidades e comunicação.

Isso evita que a ausência de um componente produza encaminhamento abrangente sobre ambos.

As práticas de catálogo, configuração, incidentes e níveis de serviço foram tratadas como recomendações no Acórdão TCE-RJ nº 44.490/2024-PLEN, não como determinações. Devem permanecer nessa categoria.

### 3.6. Q6 — Contratações de TIC

A questão atual alcança planejamento, contratação, fiscalização e gestão, mas os testes mais defensáveis concentram-se na fase preparatória. Sugere-se reformular a questão para:

> A organização adota controles mínimos na fase preparatória das contratações de TIC, com processo definido e análise técnica pela unidade competente?

Ajustes:

- **S6.1:** manter apenas `q2801ext[A]`, relativo ao planejamento da contratação. Os demais subitens alcançam seleção, gestão contratual e aderência genérica a normas, extrapolando o título do achado.
- **S6.2:** manter como recomendação, com a redação “A organização não demonstrou possuir regra geral que assegure análise prévia das contratações de TIC pela área técnica competente”.
- **S6.3:** retirar do Achado 6. As ações avaliam principalmente o plano de TIC e o PCA, já tratados no Achado 3, e não permitem concluir que uma contratação concreta foi desalinhada.
- **S6.4:** retirar. A resposta não distingue ausência de contratação, contratação centralizada, contratação simples ou de baixo valor. A composição específica de equipe com integrante requisitante e técnico não é obrigação universal para todos os jurisdicionados.

Lógica recomendada:

```text
(AV73 | AV143) | (AV78 | AV148)
```

A Lei nº 14.133/2021 permite determinação para restabelecer o planejamento obrigatório da fase preparatória e sua compatibilidade com o PCA, quando elaborado, e com as leis orçamentárias. Contudo, essa determinação deve decorrer de exame de processos concretos. O questionário, isoladamente, não é suficiente para concluir descumprimento legal.

## 4. Encaminhamentos passíveis de determinação

O Acórdão TCE-RJ nº 44.490/2024-PLEN adotou determinações para a instituição de Comitê de TI e de processo estruturado/PDTI em Rio das Ostras e Saquarema. Para controles existentes, porém incompletos, adotou recomendações. Essa distinção deve orientar a matriz.

| Situação | Classificação proposta |
|---|---|
| Ausência de Comitê de TIC ou instância equivalente | **Determinação** |
| Ausência de processo formal de planejamento de TIC | **Determinação** |
| Inexistência de plano de TIC/PDTI formalmente aprovado | **Determinação** |
| Comitê existente, mas com atuação insuficiente | Recomendação |
| PDTI existente, mas com conteúdo, alinhamento ou monitoramento incompleto | Recomendação |
| Ausência de planejamento legal da fase preparatória comprovada em contratação concreta | **Determinação** |
| Catálogo, ANS, configuração, incidentes, força de trabalho e perfis | Recomendação |

Redações sugeridas:

> Institua formalmente Comitê de TIC ou instância equivalente, compatível com a estrutura decisória da organização, com participação das áreas relevantes e competências para alinhamento, priorização e monitoramento da TIC.

> Estabeleça processo estruturado para elaborar, aprovar, manter e revisar periodicamente plano de TIC ou instrumento equivalente, compatível com o porte da organização e aprovado pela alta administração.

Quando a determinação representar orientação nova ou ampliar dever extraído de norma indeterminada, deve-se motivar a aplicabilidade, considerar as dificuldades reais do jurisdicionado e, quando necessário, prever transição, conforme os arts. 20, 22 e 23 da Lei de Introdução às Normas do Direito Brasileiro.

## 5. Ajustes técnicos no mapa e nos artefatos associados

### 5.1. Prioridade alta

1. Corrigir a lógica de S2.3 para evitar dupla imputação de comitê inexistente e inativo.
2. Corrigir o critério de `q0102` no catálogo YAML.
3. Harmonizar S1.3: a matriz inclui a alternativa B; o mapa não.
4. Remover a duplicidade entre S3.5 e S6.3.
5. Aplicar a revisão substantiva dos Achados 4, 5 e 6.

### 5.2. Prioridade média

- Das 151 ações existentes, somente 110 são utilizadas na lógica dos procedimentos e nos motivos do relatório. As outras 41 não têm efeito.
- Incorporar as ações úteis atualmente inativas, como `AV114`, `AV115`, `AV60` e `AV130`.
- Excluir as demais ou identificá-las expressamente como ações contextuais, fora da composição dos achados.
- Uniformizar o encaminhamento de S6.2: o mapa acrescenta segurança da informação, mas a matriz não.
- Corrigir textos com problemas de codificação, como “avalia??o” e “Inexist?ncia”.

A planilha `01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/matriz_verificaca_evidencias.xlsx` está estruturalmente consolidada em uma aba, mas usa numeração antiga: governança ainda aparece como Q1, planejamento como Q2, capacidade como Q3 e serviços como Q4. Deve ser sincronizada com a matriz atual ou formalmente arquivada como artefato histórico.

## 6. Conclusão

A oportunidade de melhoria mais importante é substituir a lógica “qualquer subitem ausente gera achado amplo” por uma régua em três níveis:

1. **Controle essencial inexistente:** situação inconforme, normalmente de severidade alta ou média; determinação quando houver obrigação legal ou precedente diretamente aplicável.
2. **Controle existente, mas incompleto:** situação de melhoria; recomendação proporcional.
3. **Prática de maior maturidade:** indicador diagnóstico, sem achado automático.

Essa revisão preservará os temas relevantes do iGovTI, reduzirá falsos positivos e produzirá encaminhamentos mais defensáveis perante os jurisdicionados e o Plenário.

As propostas constituem minuta técnica elaborada pelo modelo **GPT-5.6 Sol**, sujeita à avaliação e à aprovação da Equipe de Auditoria. Caso sejam acolhidas, deverão ser atualizados de forma coordenada a matriz de planejamento, o mapa de verificação de achados, o catálogo YAML, os relatórios, as tabelas e os gráficos, seguida de nova execução da auditoria em diretório temporário e comparação dos impactos.
