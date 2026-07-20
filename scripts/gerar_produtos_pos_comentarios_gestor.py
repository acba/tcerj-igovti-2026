#!/usr/bin/env python3
"""Materializa somente os três produtos básicos pós-comentários do gestor."""
from __future__ import annotations

import argparse
import logging
import re
import shlex
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = Path(sys.executable)
DEFAULT_COMENTARIOS = ROOT / "02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor"


def run_step(titulo: str, command: list[object]) -> None:
    logging.info("%s", titulo)
    logging.info("Comando: %s", shlex.join(str(item) for item in command))
    subprocess.run([str(item) for item in command], cwd=ROOT, check=True)


def prefixo_data(data: str) -> str:
    match = re.fullmatch(r"(\d{2})/(\d{2})/(\d{4})", data.strip())
    if not match:
        raise ValueError("--data-referencia deve estar no formato DD/MM/AAAA")
    return f"{match.group(3)}{match.group(2)}{match.group(1)}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-referencia", required=True, help="Data da posição corrente, em DD/MM/AAAA.")
    parser.add_argument("--respostas-base", type=Path, required=True, help="Base pós-avaliação de evidências.")
    parser.add_argument("--respostas-comentarios", type=Path, required=True, help="Exportação XLSX do survey de comentários.")
    parser.add_argument("--avaliacao-comentarios-dir", type=Path, default=DEFAULT_COMENTARIOS)
    parser.add_argument("--ajustes-comentarios", type=Path)
    parser.add_argument("--revisoes-pareceres", type=Path, help="YAML declarativo ou XLSX legado de pareceres revisados.")
    parser.add_argument("--output-root", type=Path, default=ROOT)
    parser.add_argument("--prefixo", help="Prefixo AAAAMMDD; por padrão usa a data de referência.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    prefixo = args.prefixo or prefixo_data(args.data_referencia)
    comentarios = args.avaliacao_comentarios_dir
    ajustes = args.ajustes_comentarios or comentarios / "ajustes_respostas_questionario_pos_comentarios_gestor.xlsx"
    execucao = args.output_root / "02-Execucao"
    respostas_dir = execucao / "01-Questionario/03-Respostas_Processadas"
    produto_dir = execucao / "05-Comentarios_Gestor/03-Produtos_Pos_Comentarios"
    respostas_atual = respostas_dir / f"{prefixo}-respostas-questionario-pos-comentarios-gestor.xlsx"
    pareceres_xlsx = produto_dir / "avaliacao_comentarios_gestor.xlsx"
    contexto_json = produto_dir / "contexto-relatorios-comentarios-gestor.json"
    for path in (respostas_dir, produto_dir):
        path.mkdir(parents=True, exist_ok=True)

    for entrada in (args.respostas_base, args.respostas_comentarios, ajustes):
        if not entrada.is_file():
            raise FileNotFoundError(f"entrada obrigatória não encontrada: {entrada}")

    run_step("1/2 Aplicando ajustes acolhidos nos comentários do gestor.", [
        PYTHON, ROOT / "scripts/ajustar_respostas_questionario.py", "--respostas", args.respostas_base,
        "--ajustes", ajustes, "--output", respostas_atual,
    ])
    materializar_cmd: list[object] = [
        PYTHON, ROOT / "scripts/comentarios_gestor_produtos.py",
        "--respostas-comentarios", args.respostas_comentarios,
        "--consolidado-secao1", comentarios / "consolidado/secao-1/consolidated_clean.jsonl",
        "--consolidado-secao2", comentarios / "consolidado/secao-2/consolidated_clean.jsonl",
        "--data-referencia", args.data_referencia, "--output-xlsx", pareceres_xlsx,
        "--output-json", contexto_json,
    ]
    if args.revisoes_pareceres:
        flag = "--revisoes-yaml" if args.revisoes_pareceres.suffix.lower() in {".yml", ".yaml"} else "--revisoes-xlsx"
        materializar_cmd.extend([flag, args.revisoes_pareceres])
    run_step("2/2 Materializando pareceres e contexto dos relatórios.", materializar_cmd)

    logging.info("Base corrente: %s", respostas_atual)
    logging.info("Pareceres revisáveis: %s", pareceres_xlsx)
    logging.info("Contexto dos relatórios: %s", contexto_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
