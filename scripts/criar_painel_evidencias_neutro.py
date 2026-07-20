#!/usr/bin/env python3
"""Cria a fonte vazia usada no cenário anterior à avaliação de evidências."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from gerar_fonte_ajustes_evidencias_auditoria import itens_do_mapa


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--mapa", type=Path, required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    colunas = ["Auditado", *sorted(itens_do_mapa(args.mapa))]
    pd.DataFrame(columns=colunas).to_excel(
        args.output, sheet_name="Ajustes Evidencias Auditoria", index=False
    )
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
