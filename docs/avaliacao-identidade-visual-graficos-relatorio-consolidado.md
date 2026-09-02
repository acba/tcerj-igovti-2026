# Avaliação da identidade visual dos gráficos do relatório consolidado

## 1. Objetivo e escopo

Esta avaliação examina a identidade visual, a consistência e a legibilidade dos gráficos e diagramas utilizados no relatório consolidado da Fiscalização nº 18/2026 — iGovTI 2026.

Foram considerados o relatório consolidado em Markdown, o DOCX gerado e os recursos gráficos efetivamente empregados no diagnóstico do iGovTI, na comparação longitudinal, nos achados de auditoria, na análise da utilização institucional de inteligência artificial e na avaliação dos comentários dos gestores.

O diagnóstico foi inicialmente produzido com natureza avaliativa. Em 1º de setembro de 2026, as oportunidades aprovadas foram incorporadas aos geradores e aos gráficos utilizados pelo relatório e por seus anexos.

## 1.1 Ajustes implementados

- adoção de identidade visual central compartilhada entre os geradores Matplotlib;
- uso do estilo `seaborn-v0_8-whitegrid`, com fundo branco e grades restritas ao eixo quantitativo;
- definição explícita da família DejaVu Sans e resolução de 300 dpi;
- reposicionamento das legendas dos achados e dos comentários para faixas superiores;
- dimensionamento dinâmico dos gráficos de comentários;
- identificação das cores de fundo como faixas de maturidade;
- padronização de capitalização e terminologia;
- substituição dos verdes dos cenários de 2026 por tons de azul, com laranja para 2023.

A paleta foi posteriormente simplificada para reduzir variações desnecessárias. As cores semânticas centrais passaram a reutilizar vermelho `#B33A3A`, laranja `#FFA500`, verde-claro `#9ACD32`, verde `#228B22`, os azuis institucional, médio e claro e os neutros claro e médio. O azul-petróleo e as variações alternativas de vermelho, laranja e verde foram eliminados.

## 2. Conclusão executiva

Os gráficos estão satisfatoriamente alinhados e apresentam identidade profissional. Há consistência no uso de fundo branco, tipografia sem serifa, textos em cinza-escuro, grades discretas, legendas pouco intrusivas e apresentação dos valores junto aos elementos gráficos.

O conjunto, entretanto, ainda não constitui um sistema visual completamente unificado. O relatório combina quatro subsistemas, adequados às respectivas finalidades:

- maturidade do iGovTI: vermelho, laranja e verdes;
- comparação entre esferas: azul e azul-petróleo;
- comentários dos gestores: verde, amarelo, laranja, vermelho e cinza;
- diagramas metodológicos: azul-marinho e verde-petróleo.

A diferenciação é, em grande parte, apropriada, porque as cores representam conceitos distintos. Não se recomenda impor a mesma paleta a todos os gráficos. A principal oportunidade consiste em estabelecer uma gramática visual comum, com cores, tipografia, posicionamento de legendas, dimensões e recursos de acessibilidade definidos conforme a função semântica de cada elemento.

Não foi identificado problema visual que comprometa a credibilidade do relatório ou determine seu refazimento. As principais oportunidades concentram-se na sobreposição de legendas em gráficos dos achados, na densidade dos gráficos de comentários dos gestores e na centralização das regras visuais utilizadas pelos diferentes geradores.

## 3. Pontos fortes

- As figuras do diagnóstico do iGovTI apresentam identidade consistente e utilizam a mesma ordem cromática para os níveis Inexpressivo, Iniciando, Intermediário e Aprimorado.
- Os gráficos dos seis achados mantêm cores estáveis para as esferas estadual e municipal.
- O gráfico longitudinal diferencia as referências por cor e formato dos marcadores, o que facilita a leitura e reduz a dependência exclusiva da percepção cromática.
- A utilização de cinza para a categoria “Não adota” no gráfico de inteligência artificial é adequada, pois evita representar a não adoção de IA como inconformidade.
- As imagens apresentam resolução suficiente para utilização no DOCX e não demonstram perda relevante de nitidez.
- Na maior parte dos casos, os títulos são apresentados como legendas formais no relatório, evitando repetição dentro dos gráficos.
- O uso de fundo branco, grades discretas e textos em tonalidade escura favorece a leitura e a impressão.

## 4. Oportunidades de melhoria

| Prioridade | Oportunidade | Avaliação e ajuste sugerido |
|:---:|:---|:---|
| Alta | Reposicionar as legendas dos gráficos dos Achados 1 a 6 | Em alguns gráficos, especialmente nos Achados 2, 4 e 5, a legenda posicionada no canto superior direito se sobrepõe aos totais e percentuais. Recomenda-se colocá-la acima da área de dados, em faixa reservada, seguindo o padrão adotado no gráfico longitudinal. |
| Alta | Melhorar a legibilidade dos gráficos das situações comentadas | Os gráficos das situações dos Achados 1 a 6 possuem descrições extensas, muitas categorias e legendas pequenas. Recomenda-se ajustar dinamicamente a altura conforme o número de situações, reservar espaço superior para a legenda e assegurar tamanho mínimo de fonte adequado à largura efetiva no DOCX. |
| Média | Instituir paleta central compartilhada | Funções semânticas semelhantes utilizam tonalidades distintas entre os geradores. O vermelho, por exemplo, varia entre os gráficos de maturidade, manifestações e decisões. Recomenda-se definir um catálogo central de cores institucionais, de maturidade, de situação, de esfera e de etapa metodológica. |
| Média | Reduzir a dependência das combinações vermelho e verde | A paleta é convencional, mas pode limitar a compreensão por pessoas com deficiência de visão cromática e em impressões monocromáticas. Recomenda-se complementar as cores com rótulos, formatos, contornos, padrões ou ordem fixa das categorias. |
| Média | Esclarecer a legenda da distribuição dos componentes | No gráfico de distribuição do iGovTI, Governança de TIC e Gestão de TIC, a legenda colorida representa as faixas sombreadas de maturidade, enquanto as caixas utilizam cores próprias. Recomenda-se identificar expressamente a legenda como “Faixas de maturidade” ou rotular diretamente as faixas. |
| Média | Harmonizar capitalização e terminologia | Há variações como “Gestão de Serviços” e “Gestão de serviços”, “TI” e “TIC”, além de eixos grafados em estilo de título. Recomenda-se padronizar a terminologia do relatório e empregar caixa de frase, a exemplo de “Quantidade de organizações com a ocorrência”. |
| Baixa | Declarar explicitamente a família tipográfica | A maior parte dos gráficos utiliza DejaVu Sans, enquanto o gerador dos achados declara apenas uma família genérica sem serifa. Recomenda-se explicitar a mesma família nos diferentes geradores. |
| Baixa | Evitar títulos internos redundantes | O diagrama do modelo de governança contém título dentro da própria imagem e também recebe legenda no relatório. A duplicidade não prejudica a compreensão, mas pode ser eliminada em futura revisão. |
| Baixa | Uniformizar a resolução nominal | Os geradores utilizam resoluções nominais distintas. Embora a resolução efetiva atual seja suficiente, recomenda-se adotar padrão único, preferencialmente 300 dpi, para simplificar a validação e assegurar qualidade uniforme. |

## 5. Avaliação por família visual

### 5.1. Diagnóstico do iGovTI

É a família visual mais consistente do relatório. A paleta de maturidade é utilizada de maneira estável nos gráficos de distribuição, histograma e dimensões. As faixas de fundo auxiliam a leitura da escala de 0 a 1, e os valores apresentados junto às barras reduzem ambiguidades.

Como oportunidade específica, a legenda das faixas de maturidade deve ser distinguida das cores utilizadas para as séries ou caixas quando ambas aparecem no mesmo gráfico.

### 5.2. Comparação longitudinal

O gráfico utiliza laranja para 2023, azul-claro para o cenário-base de 2026 e azul-escuro para o cenário final. Círculo, triângulo e quadrado complementam a diferenciação por cor, e a legenda posicionada acima da área de dados não interfere nos resultados. Essa solução evita associar o cenário final a uma melhora meramente pela utilização do verde.

### 5.3. Achados de auditoria

Os gráficos apresentam boa consistência interna: azul para organizações estaduais, azul-petróleo para municipais, mesma escala horizontal e valores dentro e fora das barras. Essa estabilidade permite comparar os achados.

A legenda passou a ocupar faixa superior reservada e não cobre percentuais ou totais. A apresentação dos valores dentro das barras complementa a diferenciação cromática entre as esferas.

### 5.4. Comentários dos gestores

Os gráficos utilizam uma lógica semântica compreensível: verdes para medidas atendidas ou em atendimento, laranja para ausência de medida, vermelho para discordância e cinza para situação inexistente. A ordem das categorias e os rótulos numéricos ajudam a interpretação.

As figuras com várias situações passaram a utilizar altura dinâmica, maior área para os rótulos e faixa superior reservada à legenda. Os valores permanecem associados diretamente aos segmentos, preservando a leitura no DOCX.

### 5.5. Inteligência artificial

A paleta é deliberadamente mais neutra que a escala de maturidade. Essa opção é adequada porque a análise tem natureza descritiva e não trata a ausência de adoção de IA como deficiência. O gráfico é simples, legível e compatível com sua função no relatório.

### 5.6. Diagramas metodológicos e conceituais

Os diagramas utilizam predominantemente azul-marinho, azul e verde-petróleo, cores compatíveis com a identidade institucional e com os gráficos comparativos. A diferença de estilo em relação aos gráficos estatísticos é aceitável, pois se trata de outra categoria de visualização.

Em revisão futura, podem ser uniformizados tipografia, espessura das linhas, sombras, raios dos cantos e presença de títulos internos.

## 6. Ordem recomendada de aprimoramento

1. Remover a sobreposição das legendas nos gráficos dos achados.
2. Aumentar a legibilidade dos gráficos de comentários dos gestores.
3. Criar configuração visual compartilhada pelos geradores de gráficos.
4. Padronizar terminologia, capitalização, tipografia e resolução.
5. Reforçar a acessibilidade para leitura com deficiência de visão cromática e impressão monocromática.
6. Harmonizar, em etapa posterior, os detalhes gráficos dos diagramas conceituais.

## 7. Fontes examinadas

- `03-Relatorios/01-Relatorio_Consolidado/Relatório_altaresolucao_novo.md`;
- `03-Relatorios/01-Relatorio_Consolidado/gerados/Relatório_altaresolucao_novo.docx`;
- `scripts/gerar_graficos_relatorios_consolidado_individuais_igovti.py`;
- `scripts/gerar_graficos_achados_consolidado.py`;
- `03-Relatorios/99-Analise_Longitudinal/calcular_analise_longitudinal.py`;
- `03-Relatorios/99-Avaliacao_Comentarios_Gestor/calcular_dados_comentarios_gestor.py`;
- `03-Relatorios/99-Avaliacao_IA/gerar_grafico_institucionalizacao_ia.py`;
- imagens utilizadas nas pastas de recursos do relatório consolidado e dos anexos técnicos.
