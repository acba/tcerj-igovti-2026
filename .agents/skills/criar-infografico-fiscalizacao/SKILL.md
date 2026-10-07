---
name: criar-infografico-fiscalizacao
description: Sintetizar auditorias, levantamentos e outras fiscalizações em infográficos institucionais de até duas páginas A4, com template padronizado, SVG editável e PNG de alta resolução. Use quando solicitado um infográfico ou resumo visual dos principais resultados de uma fiscalização, em qualquer área temática.
---

# Criar infográfico de fiscalização

## Produto

Produzir uma síntese visual que responda, na primeira leitura, **o que foi fiscalizado** e **o que foi encontrado**. Identificar os auditados, o objetivo, a abrangência, o período e os principais resultados. Apresentar os benefícios estimados e os encaminhamentos sustentados pelo trabalho, preservando o caráter esperado desses benefícios.

Aplicar o padrão institucional dos exemplos: **fundo cinza `#A6A6A6`, marca completa do TCE-RJ no cabeçalho, caixas azul-escuro, Open Sans nos textos e Cooper Hewitt nos cabeçalhos**. Justificar os parágrafos nas caixas de texto, alinhando as linhas às duas margens internas. Preservar a identificação das fontes dos dados. A peça combina contexto lateral desenvolvido com análises gráficas. O padrão se aplica também a saúde, educação, obras, finanças e outras áreas. Não impor índices, níveis de maturidade ou achados normativos a trabalhos que não os tenham.

A síntese deve preservar a riqueza analítica do modelo fornecido. Além dos indicadores gerais, apresentar as dimensões, os grupos, a distribuição, a evolução ou os recortes que melhor expliquem as conclusões. Selecionar visualizações complementares, evitando reduzir toda a fiscalização a poucos cartões. Preferir gráficos diretamente sobre o fundo cinza, como nos exemplos, sem substituir a composição por grandes painéis brancos.

Entregar **um SVG e um PNG por página**, em A4 vertical. Usar uma ou duas páginas. Páginas adicionais são excepcionais: primeiro reduzir repetições e detalhes, depois justificar a extensão por conteúdo essencial que perderia legibilidade. Não reduzir as fontes para fazer o material caber.

## Preparação e síntese

1. Ler o relatório, seus resultados finais e as fontes dos números selecionados. Usar imagens de referência para identificar o estilo, nunca como fonte definitiva dos resultados.
2. Identificar modalidade, tema, estágio processual, auditados, abrangência, período, benefícios estimados e conclusão principal. Distinguir organizações abrangidas e efetivamente avaliadas. Se houver muitos auditados, apresentar os grupos por esfera, poder, natureza ou território, com sua composição, sem preencher duas páginas com uma relação extensa de nomes. Se o usuário pedir a relação nominal, incorporá-la ou propor sua apresentação complementar.
3. Selecionar poucos indicadores que expliquem o trabalho e os resultados. Distinguir população abrangida, organizações avaliadas, objetos examinados, temas de achado e ocorrências. Registrar para cada número a unidade, o denominador, o período e a fonte em `dados-e-fontes.json`, na pasta de saída.
4. Consultar [síntese e visualizações](references/sintese-e-visualizacoes.md) para decidir o conteúdo e o gráfico adequado. Não transformar o infográfico em relatório completo ou lista de todos os auditados.
5. Aplicar [identidade visual e composição](references/identidade-visual.md). Copiar e adaptar os templates de [página 1](assets/template-pagina-1.svg) e [página 2](assets/template-pagina-2.svg). Usar a [marca vetorial do TCE-RJ](assets/tcerj-logo.svg) incorporada nos templates. Os campos e espaços de gráficos são substituídos pelo conteúdo real. Remover módulos sem conteúdo útil. Os templates são pontos de partida, não diagramas rígidos.

## Redação e precisão

- Usar linguagem simples, formal, impessoal, imparcial e objetiva. Preferir títulos que expressem a informação principal. Explicar siglas indispensáveis e evitar códigos dos sistemas internos.
- Preservar a distinção entre prática declarada, comprovação documental e funcionamento efetivo. Uma declaração ou a falta de comprovação não autoriza afirmar que o controle funciona ou inexiste.
- Diferenciar constatação, risco, efeito comprovado e benefício esperado. Não apresentar correlação como causa ou ausência de significância estatística como igualdade.
- Não converter propostas em decisões. Usar **O que foi proposto?** para minutas e encaminhamentos sugeridos. Usar **O que foi decidido?** somente quando houver decisão confirmada, com sua identificação.
- Para percentuais, identificar a população. Para comparações, utilizar períodos e grupos compatíveis. Conservar ressalvas que mudem a interpretação, junto do gráfico correspondente.
- Quando não houver números suficientes, usar sínteses qualitativas, fluxos ou quadros comparativos. Não inventar números para preencher cartões ou gráficos.

## Construção dos arquivos

- Criar SVG nativo, com textos, formas, gráficos e mapas vetoriais. Não envolver a imagem inteira de uma página em um SVG e apresentá-la como produto vetorial.
- Usar `width="210mm"`, `height="297mm"` e `viewBox="0 0 1190 1683"`. Manter os dois arquivos separados quando houver duas páginas.
- Incorporar as fontes no SVG final com `scripts/incorporar_fontes_svg.py`, conforme [fontes incluídas](references/fontes-incluidas.md). Manter texto selecionável no SVG. Incorporar logos oficiais ou imagens indispensáveis no próprio arquivo, sem dependências de caminhos locais ou da rede. Não redesenhar o brasão ou o logotipo por aproximação. Nas peças do TCE-RJ, manter a marca completa, sem substituí-la apenas pela sigla.
- Usar as fontes incluídas em `assets/fonts`: Open Sans nos textos e Cooper Hewitt nos cabeçalhos. O motor incluído carrega esses arquivos diretamente, sem fontes do sistema, Fontconfig, download ou instalação. O padrão de cabeçalhos usa Cooper Hewitt Heavy normal, com peso CSS 900. Para instalar no Linux, incorporar fontes no SVG ou conferir as licenças, consultar [fontes incluídas](references/fontes-incluidas.md). Guardar as famílias e os pesos utilizados no registro da geração. Para outra fonte solicitada, verificar sua disponibilidade e informar qualquer substituição.
- Justificar todos os parágrafos nas caixas de texto, inclusive na coluna lateral e nos quadros de encaminhamentos. As linhas completas devem atingir as duas margens internas, respeitando o espaço entre o texto e a borda. Manter a última linha de cada parágrafo alinhada à esquerda. Aplicar a justificação ao SVG antes da exportação, distribuindo o espaço entre palavras e preservando os caracteres. Seguir [alinhamento dos parágrafos](references/identidade-visual.md#alinhamento-dos-parágrafos).
- Gerar gráficos a partir dos dados, com ferramentas determinísticas. Pode usar SVG escrito diretamente ou gráficos exportados por uma biblioteca disponível. Preferir vetores para gráficos e mapas. Não depender de geração de imagens por IA para representar valores, rótulos ou geometria cartográfica.
- Exportar PNG diretamente do SVG a **600 dpi**: **4961 × 7016 px** por página A4. Não ampliar uma captura de baixa resolução. O script permite outra resolução quando solicitada, mantendo a proporção A4.

```bash
python scripts/exportar_infografico.py \
  /caminho/infografico-pagina-1.svg /caminho/infografico-pagina-2.svg \
  --output-dir /caminho/saida --dpi 600
```

O comando é executado a partir da pasta desta skill. Usar CPython 3.10 ou superior, de 64 bits. O exportador utiliza o motor `resvg_py` incluído em `assets/renderizador`, carregado em uma pasta temporária. Não exige programas gráficos, bibliotecas Python instaladas, pip, Fontconfig ou acesso à rede. Há motores incluídos para Linux, Windows e macOS, em x86_64 e ARM64. Consultar [exportação autocontida](references/exportacao-autocontida.md) para compatibilidade e limites. Não baixar ou instalar dependências automaticamente em plataformas sem motor incluído.

## Validação no Windows

Quando a execução ocorrer no Windows, rodar `python scripts/validar_windows.py --output-dir /caminho/validacao` antes de declarar compatibilidade confirmada. O validador verifica o motor nativo, as fontes, os acentos em UTF-8, caminhos com espaços e a exportação A4 a 600 dpi. O relatório `validacao-compatibilidade.json` registra o sistema real. Fora do Windows, a opção `--plataforma-atual` valida somente esse sistema e mantém a validação Windows como pendente. Consultar [exportação autocontida](references/exportacao-autocontida.md#validação-no-windows).

## Conferência e entrega

- Conferir valores, somas, percentuais, denominadores, legendas, unidades, períodos, nomes e estágio dos encaminhamentos contra as fontes. Não reutilizar os números dos exemplos.
- Renderizar cada SVG e inspecionar visualmente a página completa e os gráficos em detalhe. Verificar cortes, sobreposições, rótulos omitidos, contraste e legibilidade no tamanho A4. A validade do XML não garante qualidade visual.
- Comparar o produto com o modelo fornecido, considerando cabeçalho, fundo, tipografia, identificação dos auditados, benefícios estimados e riqueza das análises. Recalcular a posição do próximo bloco após quebrar linhas de um parágrafo. Não manter alturas fixas que produzam sobreposição na coluna lateral.
- Conferir a justificação dos parágrafos no SVG e no PNG. Verificar as duas margens internas, a última linha, os espaços entre palavras e a ausência de letras deformadas. Títulos, números, legendas e rótulos seguem o alinhamento próprio de cada componente.
- Conferir as dimensões e a resolução dos PNG. Manter o SVG e o PNG com o mesmo conteúdo. O exportador registra dimensões, resolução e hashes em `manifesto-exportacao.json`, sem substituir a conferência dos dados ou a inspeção visual.
- Entregar os links dos SVG e PNG e indicar quantidade de páginas, resolução e limites materiais. Na falta de destino solicitado, usar a pasta temporária definida pelo projeto ou `/tmp/infografico-fiscalizacao`.
- Não alterar o relatório de origem, publicar, fazer deploy ou commit apenas porque o infográfico foi solicitado.
