# Relatório de revisão crítica — Relatório consolidado iGovTI 2026

| Campo | Valor |
| --- | --- |
| **Documento avaliado** | `03-Relatorios/01-Relatorio_Consolidado/Relatório_altaresolucao_novo.md` |
| **Data e hora da avaliação** | 13/07/2026, às 11:15:11 (UTC−03:00, America/Sao_Paulo) |
| **Realizada por** | Grok 4.5 (xAI) |
| **Papel da revisão** | Último filtro antes de assinatura/apreciação superior (simulação de revisor final perante o Secretário-Geral de Controle Externo) |
| **Critério** | Risco de contestação pelo auditado, determinação de refazimento ou perda de credibilidade no Plenário |
| **Natureza** | Parecer técnico de revisão de clareza, coerência, coesão, linguagem e confiabilidade narrativa; não substitui deliberação da Equipe de Auditoria nem revisão jurídica competente |

**Parecer sintético:** o corpo analítico (capítulos 3–4 e 6) está, em geral, bem estruturado, com números internos coerentes e boa cautela metodológica na comparação longitudinal. **Contudo, o documento ainda não está pronto para assinatura.** Há trechos de rascunho, capítulos incompletos, inconsistências jurídicas entre consolidado e individuais, e formulações que expõem o Tribunal a contestação sistêmica.

---

## 1. Bloqueadores (impedem assinatura / geram risco de refazimento)

### 1.1 Capítulo 5 está em estado de esboço

Todo o capítulo *Comentários do Gestor e Análise da Equipe* permanece como modelo:

- “Figura XX”
- “*[Gráfico a ser inserido após consolidação dos comentários do gestor.]*”
- “*[Tabela a ser inserida após análise das discordâncias…]*”
- verbo no futuro: “a Equipe **deverá** verificar / registrar / indicar”

Isso é incompatível com um relatório final. Pior: **contraria a própria narrativa do documento**.

| Trecho | Afirmação | Problema |
| --- | --- | --- |
| §2.5 (linha ~170) | Manifestações dos gestores “foram apreciadas… e consideradas na consolidação” | Indica análise já concluída |
| Cap. 5 | “deverá indicar… a ser inserido” | Indica análise ainda por fazer |
| Resumo | “Após o contraditório…” | Sugere contraditório ainda pendente |

**Risco:** o Plenário ou o auditado pode alegar que o contraditório não foi materialmente apreciado no consolidado, ou que o relatório foi assinado incompleto.

**Ação:** ou (a) preencher o capítulo 5 com consolidação real (quantitativos, principais argumentos, decisões de manutenção/ajuste/afastamento), ou (b) reescrever a metodologia/resumo para delimitar com precisão o que já foi analisado e o que ainda pendia na data-base do consolidado — e **eliminar todo placeholder**.

### 1.2 Variáveis e marcadores de produção não resolvidos

- `{{ data_hoje }}` nas linhas de assinatura (equipe e coordenador)
- “Figura XX” repetido
- “quando gerados pelo fluxo de consolidação do relatório” (linha ~452) — linguagem de pipeline, não de relatório oficial

**Risco:** aparência de minuta; perda de solenidade e de credibilidade institucional.

### 1.3 Figuras citadas sem lastro confiável no pacote

O Markdown referencia dezenas de gráficos. Na pasta do consolidado (`03-Relatorios/01-Relatorio_Consolidado/img/`) há apenas 3 figuras de base; os gráficos de achados por esfera (`igovti_2026_achadoN_esferas.png`) **não foram encontrados no repositório**. No DOCX existe mídia com **tamanho 0 bytes** (`rId31.png`), indício de figura quebrada.

**Risco:** relatório assinado com “Figura X” sem conteúdo, ou com figuras ausentes — base clássica para questionamento formal.

**Ação:** validar, figura a figura, se cada referência está embutida no DOCX final; regenerar e reanexar o que faltar.

### 1.4 Inconsistência jurídica: DETERMINAÇÃO × RECOMENDAÇÃO

No consolidado (cap. 7):

- fala em **DETERMINAÇÕES e RECOMENDAÇÕES** dos relatórios individuais;
- determina elaboração de plano de ação sob **alerta de sanção do art. 63 da LCE 63/1990**.

No template dos relatórios individuais:

- encaminhamentos são tratados como **recomendações**;
- há citação expressa da **Deliberação TCE-RJ nº 346/2024** (conveniência/oportunidade da implementação, com motivação da não aderência).

**Risco alto:** o auditado pode alegar confusão entre regime de determinação (obrigatoriedade + sanção) e de recomendação (aderência motivada). O item 2 do encaminhamento mistura “cumprimento de determinações” e “avaliação da adoção de recomendações” sob o mesmo alerta sancionatório.

**Ação urgente:** alinhar terminologia entre consolidado e individuais; se nos individuais só há recomendações, **retirar “determinações” do texto do consolidado** (exceto comunicações/determinações processuais do cap. 7, se mantidas) e afastar sanção automática da mera não implementação de recomendação.

---

## 2. Riscos de contestação substantiva (mérito / proporcionalidade / critérios)

### 2.1 Achados com 100% de incidência (Achados 4 e 5)

Afirmar que **113/113** organizações têm fragilidades de capacidade institucional e de gestão de serviços, sem matização suficiente de:

- porte e natureza jurídica;
- capacidade mínima proporcional;
- o que se considerou “suficiente” para órgão pequeno vs. grande;
- se a regra de achado captura ausência de formalização documental ou ausência real de capacidade;

**Risco:** contestação de que o critério é inviável, de que a auditoria “já nasce com achado universal”, e de que a materialidade individual se dilui.

**Melhoria:** explicitar no consolidado (i) o desenho de materialização do achado (qualquer situação inconforme ⇒ achado), (ii) a distribuição de *intensidade* (quantidade de situações por órgão), e (iii) a lógica de proporcionalidade já usada nos encaminhamentos. O texto atual reconhece heterogeneidade no cap. 3, mas aplica o mesmo padrão sem ponte suficiente no cap. 4.3.

### 2.2 Critérios “de boa prática” apresentados como se bastassem para inconformidade

O relatório acerta ao dizer que decretos/portarias federais nem sempre vinculam (2.4 e 3.2). Porém, nos achados:

- Achado 1 cita Portaria SGD/ME nº 778/2019 para posicionamento da área de TIC;
- Achado 2 cita Decreto Federal nº 12.198/2024;
- Achado 6 cita IN SGD/ME nº 94/2022.

**Risco:** o auditado estadual/municipal contesta a força normativa do critério e a própria existência de “desconformidade”.

**Melhoria:** em cada achado, separar em duas camadas:

1. **critério vinculante** (quando houver — lei, regimento, acórdão aplicável);
2. **referencial técnico de maturidade/boa prática** (COBIT, ITIL, ISO, normas federais não vinculantes).

Evitar redigir como se o descumprimento de boa prática federal fosse, por si, desconformidade jurídica.

### 2.3 Escopo de Segurança da Informação: aparente contradição

- §2.1: SI/cibersegurança **não** é questão de auditoria autônoma (já fiscalizada em processos específicos).
- Metodologia e iGovTI: incluem dimensões e itens de SI.
- Achado 4: capacidade institucional de TIC **e SI**.

A distinção pode ser legítima (SI no índice ≠ SI como QA autônoma), mas **não está suficientemente cristalina** para o leitor médio nem para o gestor de SI.

**Risco:** alegação de reabertura indevida de tema já auditado, ou de surpresa no escopo.

**Melhoria:** parágrafo único, explícito: “SI entra apenas como componente de maturidade/capacidade; não se reavaliam controles CIS/ISO 27001 como questão autônoma.”

### 2.4 “Nível mínimo esperado de maturidade institucional” (linha ~279)

Expressão normativa **sem definição operacional**.

**Risco:** juízo subjetivo sem lastro no critério.

**Substituir por:** “nível Intermediário (iGovTI ≥ 0,40)” ou “patamar em que mecanismos básicos de direção e operação já se formalizam”, se for essa a intenção — ou remover a valoração.

### 2.5 Comparação longitudinal: Resumo “vende” regressões fora do iGovTI oficial

O corpo (4.2) explica bem que:

- estruturas 2023/2026 diferem;
- usa-se base ajustada de 68 órgãos;
- **pessoas e contratações não integram a árvore oficial do iGovTI 2026**.

Já o Resumo destaca, como “destaque negativo”, regressões em **Processos de Contratação de TIC** e **Gestão de Pessoas de TIC**, sem essa ressalva.

**Risco:** leitura enviesada no Plenário e contestação de que o consolidado usa métricas “não oficiais” para dramatizar retrocesso.

**Ação:** no Resumo, qualificar: “na estrutura ajustada comparável (não no índice oficial 2026)”.

### 2.6 Limitação metodológica subestimada

§2.3: “A limitação não obstou o atingimento dos objetivos propostos.”

Com CSA + análise documental remota, **sem testes locais**, e com achados de 94–100%, a frase é demasiado absoluta.

**Risco:** questionamento de suficiência de evidência para afirmações universais.

**Melhoria:** manter a limitação e declarar o que a auditoria *pode* e *não pode* concluir (ex.: não atesta inexistência absoluta de controles em campo; atesta inconsistência entre declaração e evidência documental apresentada).

### 2.7 Proposta de processos apartados por “possível obstrução”

O item 3 do encaminhamento nomeia CEHAB, EMOP, PESAGRO, SEDCON, SEPOL e SESP e fala em conduta passível de multa (art. 63, V e VI).

Pontos de cuidado:

- §4.6 admite que “algumas confirmaram que não participaram; outras não se manifestaram” — **não individualiza** quem confirmou, com qual justificativa, e se isso altera a qualificação de “obstrução”.
- Qualificar desde já como “possível obstrução” no pedido de abertura é aceitável se houver AN10 robusto; sem individualização no consolidado, o risco de defesa prévia forte aumenta.

**Ação:** no consolidado, quadro com: organização, comunicações, ciência, reiterações, eventual justificativa no TSID 3, e conclusão “sem resposta válida”. Separar faticamente “não respondeu” de “obstruiu”.

---

## 3. Coerência, coesão e clareza

### 3.1 O que funciona bem

- Estrutura geral alinhada a relatório de auditoria governamental (resumo → introdução → objeto → resultados → comentários → conclusões → encaminhamento).
- Explicação do iGovTI (coeficientes, pesos, faixas) em linguagem acessível.
- Comparação 2023–2026 com ressalvas metodológicas honestas (um dos pontos mais maduros do texto).
- Seção 4.4 (correlação índice × achados) com cautela de não causalidade e crítica ao “efeito teto” da contagem de achados.
- Considerações finais, no conjunto, bem amarradas aos resultados.

### 3.2 Problemas de clareza para o leitor médio

1. **TI × TIC** alternam sem regra; padronizar “TIC”, reservando “TI” só a nomes próprios/históricos (iGovTI, área de TI quando for citação).
2. **“Auditoria de conformidade, com contornos operacionais”** — jargão interno não definido. Explicar em uma frase o que isso significa (escopo, profundidade, tipo de teste).
3. **Resumo vs. metodologia de temas:** o Resumo lista 6 temas; a metodologia lista segurança, riscos, continuidade, IA, projetos etc. O leitor pode achar que o escopo mudou. Esclarecer: questionário amplo; achados de auditoria concentrados em 6 questões.
4. **Recomendações transversais em 5 eixos** (Resumo e cap. 7) **não aparecem como dispositivos autonômos** no encaminhamento; só como “leitura conjunta”. Ou formalize-as (ainda que como orientação), ou não prometa “notificação das recomendações transversais” no Resumo.
5. **Cap. 2.7** descreve o cap. 5 como consolidação das manifestações — hoje falso.
6. **Precisão excessiva** em médias de contagem: “5,531 achados”, “18,938 situações” — melhor “5,5” e “18,9”, ou “cerca de 5,5 / 18,9”.

### 3.3 Problemas de coesão narrativa

- Benefícios estimados (2.6) soam um pouco promocionais e pouco auditáveis (“papel fundamental na promoção de cultura organizacional…”). Em relatório de conformidade, preferir benefícios em termos de controle (rastreabilidade, previsibilidade orçamentária, redução de riscos contratuais).
- Nos achados, a estrutura é monótona e correta (critérios → quantificação → efeitos → recomendações), mas **faltam exemplos anonimizados ou tipologias** que mostrem diversidade de situações — o texto fica estatístico e pouco pedagógico para o Plenário.
- A frase “quando gerados pelo fluxo…” quebra o tom formal e revela incerteza sobre a própria existência dos gráficos de esfera.

### 3.4 Impessoalidade e formalidade

Em geral adequado (“Equipe de Auditoria”, voz passiva/impessoal).

Pontos a ajustar:

- evitar tom de certeza absoluta onde a base é documental remota;
- evitar “revela operação predominantemente reativa” sem qualificar “nas organizações com o achado / no conjunto avaliado”;
- no cap. 5, o futuro do verbo “deverá” soa como instrução interna de trabalho, não como análise concluída.

---

## 4. Conferência numérica (amostra)

Os percentuais principais batem com a base **n = 113**:

| Afirmação | Cálculo | Status |
| --- | --- | --- |
| 61 Inexpressivo (54,0%) | 61/113 ≈ 53,98% | OK (arredondamento) |
| 39 Iniciando (34,5%) | 34,51% | OK |
| 100 abaixo de 0,40 (88,5%) | 88,50% | OK |
| Achados 1–6 (62,8%…100%) | coerentes | OK |
| Matriz de transição 68 | linhas/colunas fecham; 13↑ / 16↓ / 39= | OK |
| 625 marcações / 113 ≈ 5,531 | OK |
| Pesos 47,8% + 52,2% e 0,4777 + 0,5223 | OK |

**Não se detectou inconsistência aritmética grave** nas tabelas centrais. O problema dominante não é conta errada; é **texto incompleto, enquadramento jurídico e robustez das generalizações**.

---

## 5. Encaminhamento (cap. 7) — pontos de atrito

1. **Item 1:** bom cuidado com sigilo e envio individualizado.
2. **Item 2:** prazo de 60 dias e plano de ação são claros; **revisar regime determinação/recomendação e o alcance da sanção**.
3. **Item 3:** nomear as 6 organizações é transparente; **fortalecer a base fática individualizada** e a linguagem (“apuração das circunstâncias da ausência de resposta”, em vez de concluir obstrução no dispositivo).
4. **Item 4:** comunicação ao controle interno — coerente.
5. **Item 5:** arquivamento do processo principal com abertura de apartados — ok, desde que a cadeia documental esteja pronta.
6. **CONSIDERANDO do sigilo:** ok, mas o consolidado em si contém dados agregados sensíveis de maturidade; confirmar se a classificação dos anexos e a publicidade do consolidado estão harmonizadas.

---

## 6. Oportunidades de melhoria redacional (checklist objetivo)

### Prioridade máxima

1. Completar ou reestruturar o **Capítulo 5**; eliminar “Figura XX” e “a ser inserido”.
2. Resolver `{{ data_hoje }}` e demais marcadores de produção.
3. Garantir **todas as figuras** no pacote final (especialmente achados por esfera e figuras da seção 4.4).
4. Alinhar **determinação × recomendação** com os individuais e com a Deliberação 346/2024.
5. Qualificar no **Resumo** as regressões de pessoas/contratações como resultado da **base ajustada**.

### Prioridade alta

6. Definir “contornos operacionais” e “nível mínimo esperado”.
7. Explicitar escopo de SI (componente vs. questão autônoma).
8. Reforçar proporcionalidade e desenho do achado nos casos de 100%.
9. Individualizar, no consolidado ou em anexo, a situação dos 6 não respondentes.
10. Remover linguagem de rascunho (“quando gerados pelo fluxo…”).

### Prioridade média

11. Padronizar TI/TIC.
12. Conciliar Resumo (5 eixos transversais notificados) com o dispositivo real do cap. 7.
13. Suavizar 2.3 e 2.6 (limitação e benefícios).
14. Reduzir casas decimais em médias de contagens.
15. Revisar espaços/NBSP anômalos (“COMUNICAÇÃO  COM DETERMINAÇÃO”) e o salto nos ofícios (3242 ausente — se intencional, explicar).

### Prioridade baixa (polimento)

16. Unificar estilo de numeração de seções (3.1. vs 4.1).
17. Evitar repetição quase literal das mesmas recomendações no fim de cada achado sem ganho informativo — ou condensar e remeter ao plano individual.
18. Conferir se “todos os poderes e esferas” no Resumo corresponde de fato ao universo (listar poderes cobertos se houver lacuna).

---

## 7. Juízo final de qualidade e confiabilidade

| Dimensão | Avaliação | Comentário |
| --- | --- | --- |
| Clareza | Média | Boa no iGovTI e longitudinal; fraca no escopo SI e no status do contraditório |
| Coerência | Insuficiente para assinatura | Cap. 5 vs. 2.5/Resumo; determinação vs. recomendação |
| Coesão | Boa no cap. 4 | Quebras graves no cap. 5 e em marcadores de produção |
| Linguagem formal/objetiva | Boa no geral | Trechos absolutos e de pipeline a corrigir |
| Imparcialidade | Adequada com ressalvas | Generalizações a 100% e “nível mínimo esperado” elevam risco de parcialidade aparente |
| Confiabilidade numérica | Boa | Amostra principal confere |
| Confiabilidade probatória narrativa | Condicionada | Depende de anexos, figuras e da análise real dos comentários do gestor |
| Prontidão para Plenário | **Não** | Há bloqueadores de minuta e risco jurídico-terminológico |

**Conclusão do revisor:**

Trata-se de um consolidado **analiticamente promissor**, com diagnóstico de maturidade e comparação longitudinal bem construídos, **mas ainda em condição de minuta avançada, não de peça pronta para assinatura do Secretário-Geral de Controle Externo**. Os três problemas que, isoladamente, já bastariam para devolver o texto à equipe são:

1. **Capítulo 5 incompleto com placeholders;**
2. **marcadores de produção e figuras não fechados;**
3. **desalinhamento determinação/recomendação entre consolidado e individuais.**

Recomenda-se **não encaminhar para assinatura** até a eliminação dos bloqueadores da seção 1 e a mitigação dos riscos da seção 2. Após isso, uma segunda passagem de revisão jurídica-redacional (focada só em encaminhamento, critérios e contraditório) seria prudente antes do rito superior.

---

*Avaliação registrada em 13/07/2026, às 11:15:11 (UTC−03:00), realizada pelo Grok 4.5 (xAI).*
