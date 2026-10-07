#!/usr/bin/env python3
"""Incorpora fontes como @font-face no SVG, mantendo os textos editáveis."""
import argparse
import base64
from pathlib import Path
from xml.etree import ElementTree as ET
from fontes_incluidas import FONTES, conferir_fontes

SVG_NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG_NS)
PESOS = {'Thin': 100, 'Light': 300, 'Book': 400, 'Medium': 500, 'Semibold': 600, 'SemiBold': 600, 'Bold': 700, 'ExtraBold': 800, 'Heavy': 900, 'Regular': 400, 'Italic': 400}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('svg', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    manifest = conferir_fontes()
    raw = args.svg.read_text(encoding="utf-8")
    if '<!DOCTYPE' in raw.upper() or '<!ENTITY' in raw.upper():
        raise ValueError('SVG com entidades externas não é aceito.')
    root = ET.fromstring(raw)
    if root.tag != f'{{{SVG_NS}}}svg':
        raise ValueError('Raiz SVG inválida.')
    for node in list(root):
        if node.get('id') == 'fontes-incluidas': root.remove(node)
    rules = []
    for item in manifest['fontes']:
        path = FONTES / item['arquivo']
        style = path.stem.split('-', 1)[1]
        italic = 'Italic' in style
        weight = PESOS[style.replace('Italic', '') or 'Italic']
        family = 'Cooper Hewitt' if path.suffix == '.otf' else 'Open Sans'
        mime, fmt = ('font/otf', 'opentype') if path.suffix == '.otf' else ('font/ttf', 'truetype')
        encoded = base64.b64encode(path.read_bytes()).decode('ascii')
        rules.append(f"@font-face{{font-family:'{family}';font-style:{'italic' if italic else 'normal'};font-weight:{weight};src:url(data:{mime};base64,{encoded}) format('{fmt}');}}")
    node = ET.Element(f'{{{SVG_NS}}}style', {'id': 'fontes-incluidas', 'type': 'text/css'})
    node.text = '\n'.join(rules)
    root.insert(0, node)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(args.output, encoding='utf-8', xml_declaration=True)
    print(f'SVG com fontes incorporadas: {args.output}')


if __name__ == '__main__':
    main()
