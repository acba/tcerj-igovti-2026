RELATÓRIO DE REVISÃO — Matriz de Planejamento e Mapa de Verificação de Achados (iGovTI 2026)

Análise realizada sobre matriz_planejamento.md (734 linhas) e mapa-verificacao-achados.xlsx (5 abas, 151 ações de verificação, 6 procedimentos, 113 motivos), confrontados com o questionário igovti_2026.md. Verificadas a razoabilidade das práticas exigidas, a lógica dos procedimentos (PA01–PA06), os gatilhos de cada situação e o tipo de encaminhamento.

1. Conclusão geral
O desenho é, em geral, técnico, rastreável e proporcional: os critérios citam normas e referenciais específicos (COBIT/ITIL/ISO com item, acórdãos com item e subitem), as situações são objetivamente verificáveis e os encaminhamentos trazem cláusulas de proporcionalidade ("compatível com o porte..."). Nenhuma questão de auditoria e nenhum achado devem ser removidos.
Foram identificados, porém: (i) 41 ações de verificação órfãs no mapa (sem efeito na lógica de achado nem na narrativa), (ii) 4 divergências entre matriz e mapa — o mapa já é, em dois pontos, mais razoável que a matriz —, (iii) sobreposições de gatilhos entre situações e entre achados, (iv) 3 situações cujo gatilho é mais exigente que o "mínimo aceitável" para organizações pequenas e merecem recalibragem, e (v) um conjunto de encaminhamentos com jurisprudência consolidada que suporta elevação a DETERMINAÇÃO.

2. Ajustes necessários nas ações de verificação do mapa
2.1 Ações órfãs (41 linhas sem efeito)
Não constam das lógicas PA01–PA06 nem são referenciadas em "Motivos do Relatório": AV26, AV28, AV30, AV32, AV35, AV37, AV43, AV44, AV47–AV52, AV60, AV61, AV65, AV68, AV69, AV72, AV102, AV104, AV106, AV109, AV111, AV113–AV115, AV117–AV123, AV130, AV131, AV135, AV138, AV139, AV142.
- AV26 (q0101 ≠ F, situação S4.1) — provavelmente era condição pretendida para "tem área de TI, mas sem força de trabalho". Recomendo religar: PA04 passaria a (AV26 & (AV25 | AV27)), evitando que organização sem área de TI (S1.1) receba simultaneamente S4.1 — hoje há dupla contagem.
- AV35/AV37 (q2701extC, q2702extC) — devem substituir AV34/AV36 no gatilho de S4.4 (ver item 4.3).
- AV113–AV115 (evidência "Não conforme" de q2705extB/C/D) — inconsistência: a rejeição da evidência desses itens não gera situação, mas a de q2706extA (AV116) gera. Religar junto a AV39–AV41 ou documentar a razão.
- As demais (AV28, AV30, AV32, AV43, AV44, AV47–AV52, AV60, AV61, AV65, AV68, AV69, AV72, AV102, AV104, AV106, AV109, AV111, AV117–AV123, AV130, AV131, AV135, AV138, AV139, AV142) devem ser removidas — não contribuem para achado nem para motivo, e criam risco de questionamento de rastreabilidade.
2.2 Divergências matriz × mapa (harmonizar no sentido do mapa)
Ponto	Matriz	Mapa	Análise
S1.3 (posicionamento)	inclui q0102 == B (subordinada a secretaria/subsecretaria de nível estratégico)	exclui B (usa C, D, E)	Mapa mais razoável: subordinação a estrutura de nível estratégico não é posicionamento inadequado; a Portaria SGD 778/2019 exige apenas vinculação preferencial à alta administração. Ajustar a matriz (retirar B) e manter severidade média.
S4.6 (dependência externa)	((q0101 == B) | (q0101 == C)) & (interno == 0)	apenas q0101 == B	Mapa mais razoável: no modelo C (Centralizada Externa, ex.: PRODERJ/empresa pública), zero pessoal interno é desenho institucional legítimo. Ajustar a matriz (retirar C).
2.3 Sobreposição de gatilhos (dupla contagem)
- S5.3 e S5.4 compartilham q2203ext[A] (base consolidada de configuração): a mesma ausência gera "inventário" e "gestão de configuração" na mesma organização (reflete-se nos 97 e 110 casos do consolidado). Recomendo: manter q2203ext[A] apenas em S5.3; S5.4 passa a (q2203ext[C] != Sim) — o item da formalização do processo.
- S3.5 e S6.3 compartilham 4 itens (q2102extC, q2802extC, q2802extD, q2804B) entre o Achado 3 e o Achado 6. Trata-se de lentes distintas e defensáveis, mas recomendo nota metodológica explícita (matriz de achados/consolidado) para antecipar alegação de dupla punição pelo mesmo fato.
2.4 Numeração com lacunas na matriz (Q3)
Faltam R3.3, IR6, P6, E6 e S3.3 (provavelmente "plano vigente" suprimido). Sem efeito funcional, mas renumerar para eliminar aparência de item omitido.

3. Questões de auditoria e achados: nada a remover
- Q1 a Q6 são essenciais e respondíveis; os seis achados correspondem fielmente às questões e são sustentados por critérios específicos.
- QT (longitudinal) está corretamente marcada como levantamento, sem achado.
- Único ajuste recomendado: no Achado 4, reforçar na matriz a cláusula de proporcionalidade ("adequada às suas necessidades institucionais" da Q4) na narrativa das situações, pois é o achado com 100% de incidência e o mais exposto a contestação.

4. Situações inconformes: ajustes de proporcionalidade
Situação	Regra atual	Problema
S4.1 (força de trabalho, severidade alta)	total_TI == 0 | total_SI == 0	(i) organização de modelo C (Centralizada Externa) com zero pessoal interno é apontada com severidade alta; (ii) organização com 1–2 técnicos de TI que acumulam SI é apontada por total_SI == 0
S4.3 (cargos específicos, média)	(q2708[B] != Sim) | (q2708[D] != Sim) (OR)	Org com funções formais de TI, mas sem funções formais de SI, é apontada
S4.4 (perfis profissionais, média)	(q2701ext[A] != Sim) | (q2702ext[A] != Sim) | (q2704ext[B] != Sim)	Os itens "A" exigem perfis "definidos, documentados e publicados" — o requisito de transparência ativa eleva a barra para órgãos pequenos sem agregar essência
S5.3/S5.4	compartilham q2203ext[A]	dupla contagem
S2.1 (modelo básico, alta)	OR de 4 itens, incluindo q1002ext[C] "indicadores implantados (há coleta e análise)"	item mais exigente dos quatro
S3.1 (processo de planejamento, alta)	OR de 4 subitens (participação, critérios, custo/benefício/risco, formalização)	exigente para municípios pequenos

5. RECOMENDAÇÃO → DETERMINAÇÃO (análise por fundamento)
Critérios utilizados: (i) existência de norma vinculante aplicável ao grupo do jurisdicionado; (ii) jurisprudência consolidada e específica do TCE-RJ ou do TCU sobre a matéria; (iii) verificabilidade objetiva da determinação.
Tier 1 — elevação com segurança (jurisprudência + norma aplicável)
Situação	Fundamentos
S2.2 — Comitê de TIC ou instância equivalente	Acórdão TCE-RJ 44.490/2024-PLEN (item II.1: Comitê de TI com participação de áreas relevantes, priorização e monitoramento por indicadores); Acórdão TCU 1.411/2014-Plenário (item 9.1.1)
S3.2 — Aprovação formal do PDTI/PEDTIC	TCU 1.411/2014 (item 9.1.6 e subitens); TCE-RJ 44.490/2024 (item II.3: aprovação pela autoridade máxima); Resolução CNJ 370/2021 (PDTIC obrigatório — vinculante para TJRJ); Decreto Estadual 48.997/2024 (SETIC — confirmar obrigatoriedade dos planos setoriais para o Executivo estadual)
S3.1 — Processo formal de planejamento de TIC	TCE-RJ 44.490/2024 (item II.3: processo estruturado, com participação das secretarias, para elaborar, manter e revisar o PDTI)
S6.3 — Alinhamento das contratações ao planejamento/PCA/orçamento	Lei 14.133/2021: art. 11, parágrafo único (governança das contratações), art. 12, VII (plano de contratações), art. 18, §1º, I (compatibilização com o plano de contratações anual)
S3.5 — Vínculo do plano com orçamento e contratações	TCU 1.411/2014 (9.1.6.4: vinculação das ações priorizadas ao orçamento de TI); TCE-RJ 44.490/2024 (II.3.4: alocação de recursos)
Tier 2 — elevação avaliável, com cautela redacional
Situação	Fundamentos	Cautela
S2.1 — Modelo básico de governança (papéis, objetivos, indicadores, metas)	TCE-RJ 44.490/2024 (item II.1: estrutura de governança com indicadores e metas); TCU 1.411/2014	Determinar "modelo básico" é menos objetivo que instituir comitê/plano; recomendo determinar o núcleo (papéis + objetivos/indicadores/metas da TIC) com prazo maior
S6.1 — Processo formal e padronizado de contratações de TIC	Lei 14.133/2021, art. 11, parágrafo único ("implementar processos e estruturas") e art. 19, IV (modelos de minutas/TR)	Determinar fluxo proporcional ao porte, preservando a cláusula de fluxos simplificados
S6.2 — Análise prévia e aprovação técnica da área de TIC	Jurisprudência consolidada do TCU (1.411/2014 e sucessivas); IN SGD/ME 94/2022 como referencial; Notas Técnicas TCE-RJ	Manter a ressalva de fluxo simplificado para baixo valor/complexidade; para municípios sem área de TIC formal (S1.1), a determinação deve ser condicionada à instituição da área
Tier 3 — manter RECOMENDAÇÃO
- S1.1, S1.2, S1.3 (formalização, atribuições, posicionamento): base é Portaria SGD 778/2019 (federal, não vinculante) + COBIT/ISO 38500. Recomendação, podendo citar o acórdão como reforço argumentativo.
- Achado 4 (S4.1–S4.6): APO07/ISO 27001 — sem jurisprudência específica suficiente; determinar dimensionamento de pessoal seria indevida ingerência. Manter recomendação.
- Achado 5 (S5.1–S5.5): ITIL/COBIT — manutenção de recomendação.
- S6.4 (equipe de planejamento da contratação): IN federal; manter recomendação.
Condicionantes para o upgrade
1. Preservar em todas as determinações a cláusula de proporcionalidade ("compatível com o porte, a complexidade e a estrutura decisória") — a redação atual dos encaminhamentos já a contém.
2. Diferenciar o grupo do jurisdicionado na fundamentação (TJRJ: CNJ 370/2021; Executivo estadual: Decreto 48.997/2024, se confirmado; municípios: jurisprudência TCU/TCE-RJ).
3. Coordenar com o capítulo 7 do consolidado: o item 2 comina sanção do art. 63 da LCE 63/1990 — com determinações no relatório individual, o alerta sancionatório passa a ter destinatário certo; ajustar a redação para separar determinação (cumprimento obrigatório) de recomendação (aderência motivada), evitando a fusão hoje criticada.
4. O mapa tem coluna tipo_encaminhamento por linha de ação; a mudança deve ser idêntica em todas as linhas da mesma situação (matriz e mapa) e exige regeneração dos relatórios individuais, da matriz de achados e do consolidado.

6. Severidades
Todas as situações possuem severidade preenchida na matriz — adequado. Ajustes recomendados: S4.1 ramo total_SI == 0 (alta → média, quando total_TI > 0); demais severidades estão proporcionais (alta para estrutura, governança, planejamento e contratações; média para atributos complementares).

7. Plano de ação sugerido
1. Mapa: religar AV26 e AV35/AV37 em PA04; decidir sobre AV113–AV115; excluir as demais 38 linhas órfãs.
2. Matriz: alinhar S1.3 (retirar B) e S4.6 (retirar C) ao mapa; reavaliar S4.1/S4.3/S4.4; renumerar Q3.
3. Upgrade de encaminhamento: Tier 1 (S2.2, S3.1, S3.2, S3.5, S6.3) → DETERMINAÇÃO; Tier 2 (S2.1, S6.1, S6.2) a critério da equipe; Tier 3 permanece RECOMENDAÇÃO.
4. Regenerar produtos e revisar capítulo 7 do consolidado à luz do novo regime.