# Revisão da proporcionalidade das lógicas dos Achados 4, 5 e 6

## 1. Identificação e finalidade

Este papel de trabalho registra a revisão crítica das ações de verificação e das lógicas que ensejam os Achados 4, 5 e 6 no arquivo `02-Execucao/03-Execucao_Procedimentos/01-Insumos/mapa-verificacao-achados.xlsx`.

A revisão teve como objetivos:

* verificar se as situações inconformes são integralmente respondíveis pelos itens do questionário `01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md`;
* identificar conclusões que extrapolem o conteúdo das respostas ou evidências solicitadas;
* avaliar a razoabilidade e a proporcionalidade da régua aplicada a organizações de diferentes portes, estruturas e modelos de operação;
* reduzir o risco de falsos positivos, dupla contagem ou transformação de práticas de maior maturidade em requisitos mínimos universais;
* propor ajustes que aumentem a defensabilidade dos achados perante os auditados e o Plenário.

As propostas deste documento constituem **minuta técnica sujeita à avaliação e aprovação da Equipe de Auditoria**. Nenhuma alteração deve ser considerada incorporada à metodologia antes da atualização dos artefatos, da reexecução dos procedimentos e da revisão dos impactos resultantes.

## 2. Fontes examinadas

Foram examinados:

* `02-Execucao/03-Execucao_Procedimentos/01-Insumos/mapa-verificacao-achados.xlsx`;
* `01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/matriz_planejamento.md`;
* `01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md`.

A análise foi limitada ao que pode ser respondido ou comprovado pelos itens existentes no questionário. Não foram presumidas informações sobre contratos, pessoal, criticidade, materialidade, desempenho ou capacidade institucional que não possam ser obtidas desses itens.

## 3. Conclusão geral

Os temas dos três achados são relevantes. O principal risco metodológico está na combinação das ações: em diferentes situações, a ausência isolada de um elemento formal ou de uma prática de maior maturidade produz um título amplo de insuficiência institucional.

Recomenda-se:

* reformular substancialmente o Achado 4, removendo situações que não demonstram, por si sós, insuficiência de capacidade e combinando os testes remanescentes;
* manter o Achado 5, com ajustes para evitar dupla contagem e separar inventário de ativos de gestão de configuração;
* reformular substancialmente o Achado 6, limitando-o às situações que o questionário permite afirmar com segurança sobre a governança técnica da fase preparatória.

## 4. Achado 4 — Capacidade institucional de TIC e segurança da informação

### 4.1. Limites do que o questionário permite concluir

O questionário permite identificar:

* o quantitativo declarado de profissionais por área e tipo de vínculo (`q0105`);
* a existência de dimensionamento documentado (`q2703`);
* a existência de cargos ou funções específicas (`q2708`);
* a definição documental de perfis (`q2701` e `q2702`);
* a escolha de gestores segundo perfis (`q2704`);
* a identificação documentada de lacunas de competências (`q2705`);
* determinadas práticas de capacitação (`q2706`);
* o modelo predominante de operação (`q0101`);
* a predominância numérica de profissionais terceirizados, derivada de `q0105`.

O questionário não permite avaliar diretamente a suficiência material do quantitativo existente, a produtividade da equipe, a criticidade das atividades terceirizadas, a qualidade da fiscalização, a retenção efetiva de conhecimento ou a capacidade real de estruturas compartilhadas. Por isso, a expressão “capacidade institucional insuficiente” não deve decorrer da ausência isolada de qualquer prática formal.

### 4.2. Ausência de força de trabalho dedicada

Lógica vigente:

```text
AV25 | AV27
```

`AV25` identifica `total_TI = 0`. A ação pode ser mantida, pois permite afirmar que a organização não informou profissional que atue predominantemente em TIC.

`AV27` identifica `total_SI = 0` e deve ser removida como gatilho autônomo. A instrução de `q0105` determina que a pessoa que atua simultaneamente em TIC e segurança seja registrada apenas na área predominante. Assim, `total_SI = 0` não permite concluir que ninguém exerça responsabilidades de segurança da informação.

Proposta:

```text
AV25
```

Redação sugerida para a situação:

> A organização não informou profissionais que atuem predominantemente em tecnologia da informação.

### 4.3. Quantitativo necessário não definido

Lógica vigente:

```text
AV29 | AV103
```

A situação deve ser mantida. `q2703ext[C]` pergunta diretamente se foi definido, de maneira documentada, o quantitativo necessário de pessoal de TIC e segurança da informação. A situação não afirma que o quadro atual seja insuficiente, mas que a necessidade não foi definida documentalmente.

### 4.4. Ausência de cargos, funções ou ocupações específicas

Lógica vigente:

```text
(AV31 | AV105) | (AV33 | AV107)
```

Recomenda-se remover integralmente essa situação do achado. O questionário permite afirmar que não existem cargos ou funções formalmente atribuídos, mas não permite concluir que a capacidade seja insuficiente. A organização pode utilizar cargos genéricos, designações, funções acumuladas, estruturas compartilhadas, profissionais cedidos ou prestação externa.

O próprio encaminhamento manda avaliar a necessidade de instituir cargos ou funções. Se a necessidade ainda deve ser avaliada, sua inexistência não deve ser utilizada isoladamente como prova de insuficiência.

Ações a retirar da lógica do PA04:

```text
AV31
AV33
AV105
AV107
```

### 4.5. Perfis profissionais inexistentes ou não utilizados

Lógica vigente:

```text
(AV34 | AV108)
| (AV36 | AV110)
| (AV38 | AV112)
```

Recomenda-se remover integralmente essa situação do Achado 4.

`q2701ext[A]` e `q2702ext[A]` combinam, na mesma alternativa, responsabilidades definidas, documentadas e publicadas. Uma resposta negativa não permite saber qual desses elementos faltou. Portanto, não é seguro concluir que o perfil inexiste.

`q2704ext[B]` permite saber se a escolha dos gestores considerou perfil previamente definido, mas a resposta negativa não comprova que o gestor designado seja inadequado nem que haja insuficiência de capacidade institucional.

Ações a retirar:

```text
AV34
AV36
AV38
AV108
AV110
AV112
```

Os itens podem permanecer no diagnóstico de maturidade e no cálculo dos índices aplicáveis.

### 4.6. Lacunas de competências não identificadas ou tratadas

Lógica vigente:

```text
AV39 | AV40 | AV41 | (AV42 | AV116)
```

`AV42` e `AV116` avaliam especificamente a existência de plano de capacitação. Entretanto, o próprio questionário admite tratamento por capacitação, realocação, recrutamento, contratação ou apoio especializado. A ausência de plano de treinamento não permite concluir que as lacunas não sejam tratadas.

Recomenda-se retirar:

```text
AV42
AV116
```

Recomenda-se também retirar `AV39`, pois `q2705ext[B]` utiliza formulação abrangente sobre competências de liderança e gestão dos gestores da organização. Para manter aderência estrita às competências técnicas de TIC e segurança, devem ser utilizados `q2705ext[C]` e `q2705ext[D]`.

Proposta para a situação:

```text
(AV40 | AV114) | (AV41 | AV115)
```

`AV114` e `AV115` já existem na planilha e devem ser incorporadas para assegurar tratamento simétrico entre resposta negativa e resposta afirmativa não comprovada.

Nova descrição sugerida:

> A organização não identifica e documenta integralmente as lacunas de competências técnicas necessárias à atuação dos colaboradores de TIC e segurança da informação.

### 4.7. Dependência externa sem capacidade interna

Lógica vigente:

```text
(AV45 & AV46) | AV53
```

Recomenda-se remover integralmente essa situação do Achado 4.

`AV53` demonstra apenas que o número de terceirizados é superior ao de profissionais internos. Isso não comprova insuficiência da equipe interna para governar, coordenar ou fiscalizar os serviços.

`AV45` e `AV46`, em conjunto, demonstram modelo terceirizado ou externo sem profissionais internos informados, mas não permitem avaliar a capacidade de governança compartilhada, a atuação de órgão central, a fiscalização exercida por outra unidade ou a qualidade da supervisão.

Ações a retirar:

```text
AV45
AV46
AV53
```

O modelo de operação e a predominância de terceiros podem permanecer como indicadores de risco para seleção e aprofundamento em fiscalizações futuras.

### 4.8. Lógica proposta para o Achado 4

Recomenda-se que o achado ocorra quando não houver profissional declarado em TIC ou quando coexistirem ausência de dimensionamento e ausência de identificação de lacunas técnicas:

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

Título sugerido:

> Fragilidades no planejamento da força de trabalho e das competências de TIC e segurança da informação.

O título sugerido é mais aderente aos itens respondidos, que medem principalmente a formalização do planejamento da força de trabalho, e não a suficiência material da capacidade instalada.

## 5. Achado 5 — Gestão de serviços de TIC

### 5.1. Catálogo de serviços

Lógica vigente:

```text
(AV54 | AV124)
| (AV55 | AV125)
| (AV56 | AV126)
```

`q2201ext[B]`, avaliada por `AV55` e `AV125`, combina atualização do catálogo e compatibilidade com ANS. A resposta negativa pode decorrer apenas da inexistência de ANS, gerando simultaneamente situação de catálogo insuficiente e de níveis de serviço insuficientes.

Recomenda-se retirar:

```text
AV55
AV125
```

Proposta:

```text
(AV54 | AV124) | (AV56 | AV126)
```

### 5.2. Níveis de serviço

Lógica vigente:

```text
(AV57 | AV127) | (AV58 | AV128)
```

Recomenda-se manter. Os itens perguntam diretamente se há ANS formalizados e se os níveis estabelecidos são monitorados. A situação “ausência ou fragilidade na definição e no monitoramento” corresponde ao conteúdo respondido.

### 5.3. Inventário de ativos

Lógica vigente:

```text
(AV59 | AV129)
| (AV62 | AV132)
| (AV63 | AV133)
```

`q2203ext[A]`, avaliada por `AV59` e `AV129`, exige base consolidada de configurações e relacionamentos. Esse requisito pertence à gestão de configuração, não ao simples inventário. Seu uso nas duas situações produz dupla contagem.

Recomenda-se retirar:

```text
AV59
AV129
```

E incorporar as ações já existentes sobre inventário de ativos associados à informação:

```text
AV60
AV130
```

Proposta:

```text
(AV60 | AV130)
| (AV62 | AV132)
| (AV63 | AV133)
```

Nova descrição sugerida:

> Inexistência ou insuficiência dos inventários de ativos associados à informação, dispositivos ou softwares gerenciados pela organização.

### 5.4. Gestão de configuração

Lógica vigente:

```text
(AV64 | AV134) | (AV66 | AV136)
```

Recomenda-se manter. Os itens verificam diretamente a base de configuração, os relacionamentos e a formalização do processo.

Não se recomenda acrescentar `AV65` ou `AV135`, pois isso elevaria a régua sem ser necessário para caracterizar a fragilidade básica.

### 5.5. Gestão de incidentes

Lógica vigente:

```text
(AV67 | AV137)
| (AV70 | AV140)
| (AV71 | AV141)
```

Recomenda-se manter. As ações verificam priorização e escalamento, formalização e tratamento de incidentes de segurança. Esses elementos são diretamente respondíveis e constituem núcleo mínimo razoável.

Não se recomenda acrescentar base de conhecimento, integração com ANS ou análise de causa raiz como novos gatilhos do achado.

### 5.6. Lógica proposta para o Achado 5

```text
((AV54 | AV124) | (AV56 | AV126))
|
((AV57 | AV127) | (AV58 | AV128))
|
((AV60 | AV130) | (AV62 | AV132) | (AV63 | AV133))
|
((AV64 | AV134) | (AV66 | AV136))
|
((AV67 | AV137) | (AV70 | AV140) | (AV71 | AV141))
```

É defensável que qualquer uma das cinco situações gere o Achado 5, pois a questão de auditoria pergunta expressamente sobre práticas mínimas de catálogo, níveis de serviço, ativos, configuração e incidentes.

## 6. Achado 6 — Governança técnica das contratações de TIC

### 6.1. Limites do que o questionário permite concluir

O questionário não permite identificar se houve contratação de TIC no período, quantidade, valor ou risco das contratações, contratação emergencial, rito legitimamente simplificado, contratação centralizada ou justificativa para demanda superveniente.

Além disso, `q2804` é obrigatória e utiliza apenas “Sim” ou “Não”, sem alternativa para ausência de contratação ou inaplicabilidade. Essas limitações impedem conclusões seguras sobre casos concretos a partir de `q2804[B]` e `q2804[C]`.

### 6.2. Processo formal e padronizado

Lógica vigente:

```text
(AV73 | AV143)
| (AV74 | AV144)
| (AV75 | AV145)
| (AV76 | AV146)
| (AV77 | AV147)
```

O título do achado trata da fase preparatória, mas `AV74` e `AV75` alcançam seleção de fornecedores, `AV76` alcança gestão e fiscalização contratual e `AV77` abrange genericamente todas as fases.

Recomenda-se manter apenas:

```text
AV73 | AV143
```

`q2801ext[A]` pergunta diretamente se o planejamento das contratações contempla etapas, responsabilidades e artefatos.

Ações a retirar:

```text
AV74
AV75
AV76
AV77
AV144
AV145
AV146
AV147
```

Nova descrição sugerida:

> Inexistência ou fragilidade do processo formal de planejamento das contratações de TIC.

### 6.3. Análise prévia e aprovação técnica

Lógica vigente:

```text
AV78 | AV148
```

Recomenda-se manter. `q2804[A]` pergunta expressamente se existe submissão obrigatória à análise e aprovação técnica da área de TIC, e `q2804eviA` solicita norma e caso concreto.

Para não afirmar que uma contratação determinada ocorreu sem aprovação, sugere-se a seguinte redação:

> A organização não demonstrou possuir regra geral que assegure análise prévia e aprovação técnica das contratações de TIC pela área técnica competente.

### 6.4. Alinhamento das contratações ao planejamento

Lógica vigente:

```text
(AV79 | AV149)
| (AV80 | AV150)
| (AV81 | AV151)
| AV82
```

Recomenda-se remover integralmente essa situação do Achado 6.

`AV79` a `AV81` avaliam características gerais do plano de TIC e do PCA, não contratações concretas. Essas fragilidades já são tratadas no Achado 3. `AV82` não permite saber se houve contratação no exercício nem se existiu exceção justificada.

Ações a retirar:

```text
AV79
AV80
AV81
AV82
AV149
AV150
AV151
```

### 6.5. Equipe de planejamento formalmente designada

Lógica vigente:

```text
AV83
```

Recomenda-se remover integralmente essa situação do Achado 6.

A resposta negativa a `q2804[C]` não permite distinguir ausência de participação técnica, contratação simples, contratação centralizada, contratação de baixo valor, inexistência de contratação no exercício ou participação técnica documentada sem integração formal à equipe. O formato específico de equipe multidisciplinar também não constitui obrigação universal demonstrada para todos os jurisdicionados.

Ação a retirar:

```text
AV83
```

### 6.6. Lógica proposta para o Achado 6

```text
(AV73 | AV143) | (AV78 | AV148)
```

Situações mantidas:

1. inexistência ou fragilidade do processo formal de planejamento das contratações de TIC;
2. ausência de regra demonstrada de análise prévia e aprovação técnica das contratações de TIC.

O título “Fragilidades na governança técnica da fase preparatória das contratações de TIC” pode ser mantido.

## 7. Síntese das alterações propostas

### 7.1. Achado 4

Retirar da lógica:

```text
AV27
AV31
AV33
AV34
AV36
AV38
AV39
AV42
AV45
AV46
AV53
AV105
AV107
AV108
AV110
AV112
AV116
```

Incorporar os pares documentais já existentes:

```text
AV114
AV115
```

Lógica proposta:

```text
AV25 | ((AV29 | AV103) & ((AV40 | AV114) | (AV41 | AV115)))
```

### 7.2. Achado 5

Retirar:

```text
AV55
AV59
AV125
AV129
```

Incorporar:

```text
AV60
AV130
```

Lógica proposta:

```text
((AV54 | AV124) | (AV56 | AV126))
| ((AV57 | AV127) | (AV58 | AV128))
| ((AV60 | AV130) | (AV62 | AV132) | (AV63 | AV133))
| ((AV64 | AV134) | (AV66 | AV136))
| ((AV67 | AV137) | (AV70 | AV140) | (AV71 | AV141))
```

### 7.3. Achado 6

Retirar:

```text
AV74
AV75
AV76
AV77
AV79
AV80
AV81
AV82
AV83
AV144
AV145
AV146
AV147
AV149
AV150
AV151
```

Lógica proposta:

```text
(AV73 | AV143) | (AV78 | AV148)
```

## 8. Providências necessárias após decisão da Equipe de Auditoria

Caso as propostas sejam aprovadas, devem ser atualizados de forma coordenada:

1. a matriz de planejamento, incluindo situações, regras, severidades e encaminhamentos;
2. o arquivo `mapa-verificacao-achados.xlsx`;
3. eventuais planilhas de checklists ou catálogos de avaliação documental;
4. a matriz de achados e seus artefatos derivados;
5. os textos dos relatórios individuais e consolidado;
6. gráficos, tabelas e quantitativos associados aos achados.

Após as alterações, a auditoria deve ser reexecutada em diretório temporário. A validação deve comparar, antes e depois:

* organizações com cada achado;
* incidência de cada situação inconforme;
* organizações cujo achado decorria de uma única ação removida;
* distribuição por esfera e porte, quando disponível;
* organizações de maior iGovTI ainda alcançadas;
* consistência entre respostas negativas e avaliações documentais não conformes;
* duplicidades entre os Achados 3, 4, 5 e 6.

O resultado da reexecução e a decisão final da Equipe devem ser acrescentados a este papel de trabalho, distinguindo claramente propostas rejeitadas, parcialmente acolhidas e aprovadas.
