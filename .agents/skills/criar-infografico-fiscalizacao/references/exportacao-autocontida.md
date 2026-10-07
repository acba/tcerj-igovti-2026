# Exportação autocontida de SVG para PNG

## Comando

A partir da pasta da skill:

```bash
python scripts/exportar_infografico.py pagina-1.svg pagina-2.svg --output-dir saida --dpi 600
```

A4 vertical a 600 dpi produz 4961 × 7016 pixels por página. A 300 dpi, produz 2480 × 3508 pixels. Outras resoluções de pelo menos 300 dpi são aceitas. Usar `--overwrite` para substituir resultados existentes. Mais de duas páginas exigem `--justificativa-paginas-extras`.

## Recursos incluídos

- Motor resvg_py 0.5.0 em arquivos wheel locais, com extensões nativas pré-compiladas.
- Fontes Cooper Hewitt e Open Sans, licenças e manifesto de hashes.
- Carregador e exportador feitos com a biblioteca padrão do Python.
- Licença do motor, SBOM fornecido pelo distribuidor e manifesto com versões, origens e hashes.

O carregador seleciona o motor pela plataforma, confere seu hash, extrai o pacote em uma pasta temporária e carrega a biblioteca dentro do processo Python. Não chama executáveis externos, não instala pacotes e não acessa a rede. O motor não carrega as fontes do sistema.

## Compatibilidade

Exige CPython 3.10 ou superior, convencional e de 64 bits. O pacote inclui motores para:

| Sistema | Arquiteturas | Base do motor |
|---|---|---|
| Linux | x86_64 e ARM64 | glibc ≥ 2.17 ou musl ≥ 1.2 |
| Windows | x64 e ARM64 | wheel nativo |
| macOS | Intel e Apple Silicon | macOS ≥ 10.12 em Intel e ≥ 11 em ARM64 |

Não inclui Python, PyPy, CPython sem GIL ou plataformas de 32 bits. O interpretador e os componentes básicos do sistema operacional continuam sendo necessários. Os oito motores são distribuídos no pacote. A exportação foi executada e inspecionada no Linux x86_64. Os motores de outras plataformas não foram executados neste ambiente.

## Qualidade e limites

A imagem é rasterizada diretamente do SVG, com precisão geométrica, antialiasing e carregamento das fontes do pacote. Não há ampliação de captura de tela. O script grava a densidade no PNG, verifica as dimensões e registra os hashes e o motor utilizado em `manifesto-exportacao.json`.

O padrão tipográfico da exportação é Open Sans nos textos e Cooper Hewitt Heavy normal nos cabeçalhos. Os arquivos originais dos OTF não são modificados. Para uma peça que exija outros estilos da Cooper Hewitt, adaptar a seleção explícita dos arquivos e conferir a aparência antes de entregar.

Usar SVG estático nativo. Recursos externos, scripts e `foreignObject` são rejeitados. Animações, JavaScript e layouts HTML não fazem parte deste fluxo. Recursos fora do padrão SVG suportado pelo resvg exigem inspeção visual e adaptação do SVG.

## Origem e licença

O motor é a distribuição oficial [resvg_py 0.5.0 no PyPI](https://pypi.org/project/resvg_py/0.5.0/), com licença MIT incluída nos wheels. [Documentação do motor](https://resvg-py.readthedocs.io/en/latest/api.html). Os wheels são preservados integralmente, inclusive licenças e metadados. `manifesto-renderizador.json` identifica cada arquivo e seu hash.

## Validação no Windows

No PowerShell, a partir da pasta da skill:

```powershell
py -3 scripts\validar_windows.py --output-dir "$env:TEMP\validacao-infografico"
```

Pode usar `python` no lugar de `py -3` quando o executável do Python estiver disponível. Escolher uma pasta nova para cada execução. O script conserva os registros anteriores e recusa sobrescrever um relatório existente.

O validador usa o próprio Python e o motor incluído. Verifica a leitura de SVG em UTF-8, a preservação de caracteres acentuados, caminhos com espaços e acentos, a incorporação das fontes, a geração de dois PNGs equivalentes, suas dimensões, densidade, CRCs e hashes. A execução desativa o modo UTF-8 automático do Python nos processos verificados e remove os programas externos do PATH. A codificação UTF-8 dos arquivos é explícita.

Os produtos são uma página sintética de validação, sua versão com fontes incorporadas, os PNGs a 600 dpi e `validacao-compatibilidade.json`. Abrir os PNGs para conferir a aparência dos acentos e das fontes. A validação automática não substitui a inspeção visual do infográfico real.

O relatório somente marca `validacao_windows: aprovada` se os procedimentos forem executados com sucesso no Windows. No Linux ou macOS, `--plataforma-atual` permite verificar o sistema real, conservando `validacao_windows: pendente`. Sem essa opção, o validador encerra com código 2 fora do Windows. Falhas de validação retornam código 1. Aprovação na plataforma executada retorna código 0.

Nesta revisão, a execução no Linux foi aprovada. O Windows não está disponível no ambiente de elaboração, portanto a execução nativa permanece pendente. Não apresentar a existência do motor Windows ou uma simulação de codificação como prova de execução nesse sistema.
