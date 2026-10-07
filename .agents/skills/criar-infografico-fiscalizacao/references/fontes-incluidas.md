# Fontes incluídas

A skill contém 14 estilos OpenType da Cooper Hewitt e 10 estilos TrueType da Open Sans. Os arquivos originais, as licenças SIL Open Font License 1.1 e o manifesto de versões e hashes ficam em `assets/fonts`.

## Origem e licença

- Cooper Hewitt: [distribuição oficial do museu](https://www.cooperhewitt.org/open-source-at-cooper-hewitt/cooper-hewitt-the-typeface-by-chester-jenkins/), arquivo `CooperHewitt-OTF-public.zip`.
- Open Sans: versão 3.003 do pacote local `ttf-opensans`, projeto [googlefonts/opensans](https://github.com/googlefonts/opensans).

As fontes podem ser redistribuídas junto da skill, conservando os avisos de direitos autorais e as licenças. Não vender os arquivos isoladamente. Não modificar os arquivos nem seus nomes internos neste fluxo.

## Exportar sem instalação

Executar `scripts/exportar_infografico.py` normalmente. O motor resvg_py incluído carrega diretamente os arquivos da skill e ignora as fontes do sistema. Não exige Fontconfig, aplicativos gráficos ou acesso à rede. Ler [exportação autocontida](exportacao-autocontida.md) para os sistemas suportados.

O padrão usa Cooper Hewitt Heavy normal nos cabeçalhos, com peso CSS 900, e Open Sans nos textos. O exportador carrega explicitamente o OTF Heavy normal para evitar que os pesos e as flags dos OTF originais selecionem o itálico. Os demais estilos da Cooper Hewitt permanecem no pacote para edição e instalação, mas a exportação padrão dos cabeçalhos usa Heavy normal.

`60-cooper-hewitt-pesos.conf` ajusta os pesos apenas na instalação opcional para aplicativos Linux. Não participa da exportação autocontida.

## Incorporar no SVG final

```bash
python scripts/incorporar_fontes_svg.py pagina-1.svg --output pagina-1-com-fontes.svg
```

O script incorpora os estilos com `@font-face` e URLs `data:`. Os textos continuam selecionáveis e editáveis. Navegadores compatíveis podem apresentar a tipografia sem fontes instaladas. Alguns editores e visualizadores ignoram fontes incorporadas no SVG. Nesses casos, instalar as fontes do pacote. O PNG conserva a aparência em qualquer visualizador. O exportador carrega os arquivos de fonte diretamente porque o motor não depende do suporte a `@font-face` do visualizador.

## Instalar no Linux, inclusive Arch

A partir da pasta da skill:

```bash
python scripts/instalar_fontes.py
```

O comando copia as fontes para `~/.local/share/fonts/infografico-fiscalizacao`, conserva as licenças, instala a configuração de pesos em `~/.config/fontconfig/conf.d` e executa `fc-cache`. Não usa sudo, AUR ou downloads. Recusa sobrescrever arquivos divergentes. Reabrir os aplicativos após a instalação.

Para conferir:

```bash
fc-match 'Cooper Hewitt:style=Heavy'
fc-match 'Open Sans:style=Regular'
```

Para outro destino, usar `--dest` e `--fontconfig-dir`. Em ambiente protegido, entregar a skill e o comando para execução pelo usuário, sem declarar instalação realizada.

## Windows e macOS

Selecionar os `.otf` e `.ttf` em `assets/fonts` e instalar pelo gerenciador de fontes do sistema. Essa instalação é opcional para edição em outros aplicativos. A exportação da skill usa as fontes incluídas diretamente, com motores para Linux, Windows e macOS. A execução foi validada no Linux. Os motores dos demais sistemas estão incluídos, mas não foram executados neste ambiente.
