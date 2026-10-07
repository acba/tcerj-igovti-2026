#!/usr/bin/env python3
"""Instala as fontes incluídas para o usuário Linux, sem sudo ou download."""
import argparse
import platform
from pathlib import Path
import shutil
import subprocess
from fontes_incluidas import FONTES, conferir_fontes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dest', type=Path, default=Path.home() / '.local/share/fonts/infografico-fiscalizacao')
    parser.add_argument('--fontconfig-dir', type=Path, default=Path.home() / '.config/fontconfig/conf.d')
    args = parser.parse_args()
    if platform.system() != 'Linux':
        parser.error('Este instalador é específico de Linux. No Windows e no macOS, instalar as fontes pelo gerenciador do sistema. A exportação da skill dispensa essa instalação.')
    manifest = conferir_fontes()
    pending = [(FONTES / item['arquivo'], args.dest / item['arquivo']) for item in manifest['fontes']]
    pending += [(p, args.dest / p.relative_to(FONTES)) for p in FONTES.rglob('OFL.txt')]
    pending += [(FONTES / 'cooper-hewitt/60-cooper-hewitt-pesos.conf', args.fontconfig_dir / '60-cooper-hewitt-pesos.conf')]
    for source, target in pending:
        if target.exists() and target.read_bytes() != source.read_bytes():
            raise ValueError(f'Arquivo divergente já existente: {target}')
    for source, target in pending:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    subprocess.run(['fc-cache', '-f', str(args.dest)], check=True)
    print(f'Fontes: {args.dest.resolve()}')
    print(f'Configuração de pesos: {args.fontconfig_dir.resolve()}')


if __name__ == '__main__':
    main()
