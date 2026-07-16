#!/usr/bin/env python3
"""Aplica comentários do gestor, recalcula o iGovTI e reexecuta a auditoria."""
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
    parser.add_argument("--painel-pos-comentarios", type=Path)
    parser.add_argument("--resultado-auditoria-anterior", type=Path, default=ROOT / "02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/resultado_auditoria.json")
    parser.add_argument("--contexto-igovti-anterior", type=Path)
    parser.add_argument("--revisoes-pareceres", type=Path, help="Planilha de pareceres previamente revisada; evita nova chamada a modelos.")
    parser.add_argument("--output-root", type=Path, default=ROOT)
    parser.add_argument("--prefixo", help="Prefixo AAAAMMDD; por padrão usa a data de referência.")
    parser.add_argument("--auditados", type=Path, default=ROOT / "02-Execucao/03-Execucao_Procedimentos/01-Insumos/bd_auditados.xlsx")
    parser.add_argument("--mapa", type=Path, default=ROOT / "02-Execucao/03-Execucao_Procedimentos/01-Insumos/mapa-verificacao-achados.xlsx")
    parser.add_argument("--template-final", type=Path, default=ROOT / "03-Relatorios/03-Relatorios_Individuais_Finais/relatorio-individual-template.md")
    parser.add_argument("--reference-docx", type=Path, default=ROOT / "scripts/resources/template-base-estilos-sigiloso.docx")
    parser.add_argument("--auditados-select", nargs="*", default=[])
    parser.add_argument("--jobs-graficos", type=int, default=2)
    parser.add_argument("--skip-graficos", action="store_true")
    parser.add_argument("--skip-relatorios", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    prefixo = args.prefixo or prefixo_data(args.data_referencia)
    comentarios = args.avaliacao_comentarios_dir
    ajustes = args.ajustes_comentarios or comentarios / "ajustes_respostas_questionario_pos_comentarios_gestor.xlsx"
    painel = args.painel_pos_comentarios or comentarios / "fontes-auditoria-pos-comentarios/painel-avaliacao-evidencias.xlsx"
    execucao = args.output_root / "02-Execucao"
    respostas_dir = execucao / "01-Questionario/03-Respostas_Processadas"
    resultados_dir = execucao / "01-Questionario/04-Resultados_iGovTI"
    auditoria_dir = execucao / "03-Execucao_Procedimentos/02-Resultados_Auditoria-pos-comentarios"
    produto_dir = execucao / "05-Comentarios_Gestor/03-Produtos_Pos_Comentarios"
    relatorios_dir = args.output_root / "03-Relatorios/03-Relatorios_Individuais_Finais/gerados"
    respostas_atual = respostas_dir / f"{prefixo}-respostas-questionario-pos-comentarios-gestor.xlsx"
    resultado_atual = auditoria_dir / "resultado_auditoria.json"
    tabelas_atual = auditoria_dir / "tabelas_consolidadas_auditoria.xlsx"
    contexto_atual = resultados_dir / f"{prefixo}-contexto-relatorios-igovti-2026.xlsx"
    resultado_oficial = resultados_dir / f"{prefixo}-iGovTI-2026.xlsx"
    resultado_comparavel = resultados_dir / f"{prefixo}-iGovTI-2026-Ajustado-Comparavel.xlsx"
    pareceres_xlsx = produto_dir / "avaliacao_comentarios_gestor.xlsx"
    contexto_json = produto_dir / "contexto-relatorios-comentarios-gestor.json"
    for path in (respostas_dir, resultados_dir, auditoria_dir, produto_dir, relatorios_dir):
        path.mkdir(parents=True, exist_ok=True)

    for entrada in (args.respostas_base, args.respostas_comentarios, ajustes, painel, args.auditados, args.mapa):
        if not entrada.is_file():
            raise FileNotFoundError(f"entrada obrigatória não encontrada: {entrada}")

    run_step("1/6 Aplicando ajustes acolhidos nos comentários do gestor.", [
        PYTHON, ROOT / "scripts/ajustar_respostas_questionario.py", "--respostas", args.respostas_base,
        "--ajustes", ajustes, "--output", respostas_atual,
    ])
    run_step("2/6 Recalculando o iGovTI corrente.", [
        PYTHON, ROOT / "scripts/gerar_artefatos_igovti.py", "--respostas", respostas_atual,
        "--prefixo", prefixo, "--output-dir", execucao,
    ])
    run_step("3/6 Reexecutando a auditoria sobre as fontes saneadas.", [
        PYTHON, ROOT / "scripts/executa_auditoria.py", "--auditados", args.auditados, "--mapa", args.mapa,
        "--fontes", respostas_atual, painel, "--resultado-json", resultado_atual,
        "--tabelas-xlsx", tabelas_atual, "--somente-dados",
    ])
    materializar_cmd: list[object] = [
        PYTHON, ROOT / "scripts/comentarios_gestor_produtos.py",
        "--respostas-comentarios", args.respostas_comentarios,
        "--consolidado-secao1", comentarios / "consolidado/secao-1/consolidated_clean.jsonl",
        "--consolidado-secao2", comentarios / "consolidado/secao-2/consolidated_clean.jsonl",
        "--data-referencia", args.data_referencia, "--output-xlsx", pareceres_xlsx,
        "--output-json", contexto_json, "--auditoria-anterior", args.resultado_auditoria_anterior,
        "--auditoria-atual", resultado_atual, "--contexto-igovti-atual", contexto_atual,
    ]
    if args.contexto_igovti_anterior:
        materializar_cmd.extend(["--contexto-igovti-anterior", args.contexto_igovti_anterior])
    if args.revisoes_pareceres:
        materializar_cmd.extend(["--revisoes-xlsx", args.revisoes_pareceres])
    run_step("4/6 Materializando pareceres e impactos para revisão final.", materializar_cmd)

    if not args.skip_graficos:
        graficos: list[object] = [
            PYTHON, ROOT / "scripts/gerar_graficos_relatorios_consolidado_individuais_igovti.py",
            "--output-root", args.output_root, "--resultados-2026", resultado_oficial,
            "--respostas-2026", respostas_atual, "--comparavel-2026", resultado_comparavel,
            "--jobs", args.jobs_graficos,
        ]
        if args.auditados_select:
            graficos.extend(["--auditados", *args.auditados_select])
        run_step("5/6 Gerando gráficos com os índices correntes.", graficos)
    else:
        logging.info("5/6 Geração de gráficos ignorada por opção do usuário.")

    if not args.skip_relatorios:
        relatorios: list[object] = [
            PYTHON, ROOT / "scripts/gerar_relatorios_individuais.py", "--auditados", resultado_atual,
            "--templates", args.template_final, "--context-files", contexto_atual,
            "--ajustes-respostas", ajustes, "--contexto-comentarios-gestor", contexto_json,
            "--nome-base-docx", "Relatório Individual", "--resource-files",
            str(args.output_root / "relatorios-individuais/img/**/*"),
            ROOT / "03-Relatorios/02-Relatorios_Individuais_Preliminares/img/igovti_2026_composicao_infografico_v6.png",
            "--output-dir", relatorios_dir, "--reference-docx", args.reference_docx,
        ]
        if args.auditados_select:
            relatorios.extend(["--auditados-select", *args.auditados_select])
        run_step("6/6 Gerando relatórios individuais finais.", relatorios)
    else:
        logging.info("6/6 Geração de relatórios ignorada por opção do usuário.")

    logging.info("Base corrente: %s", respostas_atual)
    logging.info("Auditoria corrente: %s", resultado_atual)
    logging.info("Pareceres revisáveis: %s", pareceres_xlsx)
    logging.info("Contexto dos relatórios: %s", contexto_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
