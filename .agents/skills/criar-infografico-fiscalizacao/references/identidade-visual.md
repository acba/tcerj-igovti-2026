# Identidade visual e composição

## Padrão extraído dos exemplos

Foram examinadas as nove páginas fornecidas: iGovTI 2026 (duas), SegInfo 2024 (uma), Contratações SETIC (duas) e Sistemas Críticos (quatro). Todas têm proporção A4 vertical, título de destaque, identificação do TCE-RJ, caixas azul-escuro e áreas para contexto e resultados. Aparecem gráficos de barras, barras empilhadas, comparações temporais, mapas e mapas de árvore.

O azul dominante das caixas é `#08306A`. O fundo das imagens é `#A6A6A6`. O padrão consolidado preserva o fundo cinza, o azul, a marca completa do TCE-RJ e a hierarquia dos exemplos. Os gráficos são apresentados diretamente sobre o fundo, com painéis apenas quando necessários. Esta é uma convenção derivada dos exemplos, não um manual oficial de marca.

Evitar grandes vazios entre módulos, rótulos cortados e muitos assuntos na mesma página. Ao justificar parágrafos em colunas estreitas, ajustar as quebras de linha para manter os espaços entre palavras regulares. Os exemplos de quatro páginas não estabelecem um mínimo de quatro páginas.

## Cores

| Papel | Cor | Aplicação |
|---|---|---|
| Azul principal | `#08306A` | Cabeçalhos, indicadores, títulos e encaminhamentos |
| Azul de apoio | `#1F4E79` | Barras e gráficos comparativos |
| Azul claro | `#7FA9CF` | Séries secundárias e elementos de contexto |
| Ciano | `#018DC6` | Destaque secundário e categorias |
| Verde da identidade | `#75B72E` | Acentos discretos, quando pertinentes |
| Texto | `#08306A` | Texto narrativo e rótulos sobre o cinza |
| Texto secundário | `#16365A` | Fontes, notas e explicações sobre o cinza |
| Fundo | `#A6A6A6` | Página, conforme os modelos fornecidos |
| Painel | `#08306A` | Indicadores e sínteses de encaminhamentos |
| Divisórias | `#D2D7DB` | Linhas e contornos discretos |

O fundo cinza é o padrão. Usar texto azul-escuro sobre ele, reservando branco para as caixas azuis. Um fundo claro só deve substituir esse padrão quando o usuário solicitar outra identidade visual.

Usar vermelho `#B33A3A`, laranja `#FFA500` e verde `#228B22` quando houver significado de risco ou avaliação. Em classificações de maturidade, preservar os nomes, limites e cores utilizados pelo trabalho, inclusive as cores já adotadas no relatório. Para categorias sem ordem, usar cores distintas sem sugerir bom ou ruim. Manter a mesma cor para o mesmo significado nas duas páginas. Não depender exclusivamente da cor: incluir rótulos ou legenda.

## Tipografia e dimensões

- A4 vertical: 210 × 297 mm. Grade dos templates: 1190 × 1683 unidades, aproximadamente duas unidades por ponto tipográfico.
- Textos, rótulos e fontes dos dados: **Open Sans**, regular e negrito conforme a hierarquia. Cabeçalhos: **Cooper Hewitt**, com peso forte no título principal. Essas famílias foram indicadas pelo autor dos modelos. Conferir os arquivos e os pesos disponíveis. Não trocar silenciosamente por DejaVu Sans ou Arial.
- Título principal: cerca de 46–64 unidades, 23–32 pt. Preferir duas linhas a reduzir o tamanho para acomodar um título longo.
- Títulos de seção: 26–32 unidades, 13–16 pt.
- Texto e rótulos: 20–24 unidades, 10–12 pt. Números de destaque: 34–48 unidades.
- Fontes e notas: 16–18 unidades, 8–9 pt. Não usar esse tamanho para conclusões ou ressalvas centrais.
- Margens aproximadas: 10 mm, equivalentes a 57 unidades. Nos templates, usar 60 unidades.
- Justificar os parágrafos narrativos dentro das caixas de texto. Entrelinha em torno de 1,3–1,45. As linhas completas alcançam as duas margens internas. A última linha de cada parágrafo fica alinhada à esquerda. Títulos, números de destaque, legendas e rótulos seguem o alinhamento definido para o componente.

Os tamanhos são referência de composição. Conferir a leitura no tamanho real da página, especialmente ao inserir gráficos exportados com escalas diferentes.

Uma imagem PNG não identifica com segurança a família tipográfica. Usar a informação fornecida pelo autor ou os nomes e arquivos incorporados em um PDF editável. A declaração de `font-family` no SVG não instala a fonte nem comprova que o renderizador a utilizou. Conferir a família e o peso disponíveis, por exemplo com Fontconfig em Linux. Um PDF fornecido pelo usuário pode permitir extrair a fonte com PyMuPDF, mantendo sua identificação. Registrar as substituições provisórias e adaptar novamente o espaçamento quando a fonte correta estiver disponível.

Nos templates, a marca completa ocupa cerca de 220 unidades antes do título. Preservar seu nome e símbolo, com proporção original e área livre ao redor. A coluna lateral dispõe de aproximadamente 250 unidades por linha. Medir a largura real do texto e recalcular a altura dos blocos após as quebras, antes de posicionar o próximo título.

## Alinhamento dos parágrafos

Justificar todos os parágrafos nas caixas de texto, inclusive na coluna lateral, nas sínteses de resultados e nos quadros de encaminhamentos. O limite de alinhamento é a largura útil do texto, descontado o espaço entre o texto e as bordas da caixa.

- Definir a margem esquerda, a margem direita e a largura útil antes de quebrar as linhas. Manter essas margens constantes dentro da mesma caixa.
- Medir as palavras com a fonte e o tamanho utilizados. Quebrar o parágrafo em linhas que caibam na largura útil.
- Nas linhas completas, distribuir igualmente o espaço restante entre as palavras, para que a primeira comece na margem esquerda e a última termine na margem direita. Manter a última linha alinhada à esquerda, com espaçamento normal. Parágrafos de uma única linha também usam espaçamento normal.
- Aplicar o ajuste entre palavras, preservando a forma e o tamanho das letras. Não alongar os caracteres, inserir sequências de espaços no conteúdo ou reduzir a fonte para preencher a caixa.
- Em SVG nativo, usar posições explícitas de palavras em elementos `tspan` ou outro recurso vetorial comprovado no motor incluído. Preservar os espaços simples e a ordem do texto para seleção e cópia. A declaração CSS `text-align: justify` isolada não estabelece o alinhamento de texto SVG comum.
- Se houver intervalos muito grandes, rever as quebras de linha e a largura da caixa, preservando o conteúdo e a justificação. Recalcular a altura do parágrafo e a posição do próximo bloco após as novas quebras.
- Conferir visualmente as margens e o espaçamento no PNG gerado pelo motor incluído. A caixa não precisa ter contorno visível para seguir essa regra.

Títulos, números, legendas, rótulos de gráficos e relações organizadas em linhas ou colunas mantêm seu alinhamento próprio. A justificação se aplica aos parágrafos de texto corrido.

## Template comum

### Página 1 — Objeto e diagnóstico

1. Cabeçalho com órgão, modalidade, tema e identificação curta da fiscalização.
2. Faixa com três ou quatro indicadores principais. Cada caixa apresenta valor e significado. Não inserir um quarto número irrelevante apenas para preencher o template.
3. Coluna lateral com **Organizações auditadas**, **Por que a fiscalização foi feita?** e **Benefícios estimados**, com explicação suficiente para compreender o contexto e a composição dos auditados.
4. Área principal com **O que foi encontrado?**, uma síntese e visualizações do resultado geral e de sua composição por dimensões, grupos ou território. No iGovTI, a distribuição de maturidade e as seis dimensões de gestão são análises complementares.
5. Rodapé com fonte, período ou data de referência e número da página.

### Página 2 — Resultados e encaminhamentos

1. Cabeçalho reduzido com o mesmo tema e identificação.
2. Comparação temporal e diferenças entre grupos, quando examinadas no relatório.
3. Resultados por tema de achado e outra análise complementar que acrescente informação relevante. Não repetir o mesmo resultado apenas em formato diferente.
4. **O que foi proposto?** ou **O que foi decidido?**, com duas a quatro medidas principais e destinatários quando necessários à compreensão.
5. Fonte e paginação consistentes com a primeira página.

Em uma única página, reunir resultados e encaminhamentos após reduzir detalhes. Pode substituir a coluna lateral por faixa horizontal se a composição ficar mais clara. Usar páginas adicionais somente para conteúdo essencial que não caiba com texto legível. Mapas ou dados de todas as organizações não justificam, por si sós, ampliar a peça.

## Componentes e espaço

- Os templates oferecem grupos com IDs para cabeçalho, indicadores, contexto, gráficos, encaminhamentos e fontes. Copiar, substituir os campos e adaptar os módulos ao conteúdo real.
- Os espaços de gráfico delimitam a área útil sobre o fundo cinza. Remover as orientações e inserir o grupo SVG do gráfico, respeitando título, legenda, rótulos e fonte.
- Para inserir outro SVG, ajustar `viewBox` ou usar `transform` no grupo importado. Renomear IDs de gradientes, marcadores e caminhos para evitar conflitos entre gráficos.
- Não preservar áreas vazias apenas porque fazem parte do template. Redistribuir os módulos.
- Logo: incorporar o arquivo vetorial disponibilizado, sem distorção. O ativo `assets/tcerj-logo.svg` usa os traçados da marca contidos na capa do Regimento Interno do TCE-RJ, fornecido localmente como `Regimento-Interno-e-Lei-Organica-20240430.pdf`, com as cores da referência apresentada. Seu símbolo e lettering são vetoriais. Para outro órgão, substituir pela marca correspondente. A falta do logo solicitado deve ser tratada como pendência, sem reduzir automaticamente o cabeçalho à sigla.
- Reservar o rodapé antes de compor o restante. Não deixar as referências de fonte sobrepostas aos gráficos.
- Reservar texto branco para fundos escuros com contraste suficiente. Usar azul-escuro ou preto nas barras laranja e verde-claro, conforme a legibilidade.

## Exportação

Manter elementos analíticos em vetor. Imagens indispensáveis, como logo raster fornecido, devem ter resolução suficiente e ser incorporadas por `data:`. Evitar filtros, sombras e transparências complexas que mudem entre renderizadores.

Exportar PNG diretamente do SVG. Em 600 dpi, as dimensões arredondadas de A4 são 4961 × 7016 px. Em 300 dpi, 2480 × 3508 px. Se o usuário solicitar qualidade máxima, preferir 600 dpi ou superior. A densidade não corrige texto pequeno ou fontes de dados incompletas.

## Fontes autocontidas

Open Sans e Cooper Hewitt estão incluídas em `assets/fonts`, com licenças OFL e manifesto de origem, versões e hashes. Usar esses arquivos na geração. Ler [fontes incluídas](fontes-incluidas.md) para exportação, incorporação e instalação. A Cooper Hewitt Heavy corresponde a peso CSS 900, Bold a 700 e Semibold a 600. A exportação carrega explicitamente Cooper Hewitt Heavy normal. A configuração Fontconfig dos pesos é usada apenas na instalação opcional para outros aplicativos Linux. Os arquivos originais não são modificados.
