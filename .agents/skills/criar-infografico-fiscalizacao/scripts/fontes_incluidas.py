"""Confere os arquivos de fonte incluídos no pacote, sem instalação ou rede."""
import hashlib
import json
from pathlib import Path

FONTES = Path(__file__).resolve().parents[1] / 'assets/fonts'


def conferir_fontes():
    manifest = json.loads((FONTES / 'manifesto-fontes.json').read_text(encoding="utf-8"))
    for item in manifest['fontes']:
        path = FONTES / item['arquivo']
        if hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
            raise ValueError(f'Fonte ausente ou divergente: {path}')
    return manifest
