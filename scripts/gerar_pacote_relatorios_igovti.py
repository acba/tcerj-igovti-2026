#!/usr/bin/env python3
"""Executa o fluxo completo de geração dos relatórios iGovTI 2026."""

from __future__ import annotations

import argparse
import logging
import re
import shlex
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BRUTO = ROOT / "02-Execucao/01-Questionario/20260621-respostas-questionario-bruto.xlsx"
DEFAULT_AJUSTES_INICIAIS = ROOT / "02-Execucao/01-Questionario/Ajustes/ajustes_respostas_questionario_inicial.xlsx"
DEFAULT_AJUSTES_EVIDENCIAS = ROOT / "02-Execucao/01-Questionario/Ajustes/ajustes_respostas_questionario_pos_avaliacao_evidencias.xlsx"
DEFAULT_AUDITADOS = ROOT / "02-Execucao/03-Execucao_Procedimentos/bd_auditados.xlsx"
DEFAULT_MAPA = ROOT / "02-Execucao/03-Execucao_Procedimentos/mapa-verificacao-achados.xlsx"
DEFAULT_TEMPLATE_INDIVIDUAL = ROOT / "03-Relatorios/02-Relatorios_Individuais_Preliminares/relatorio-individual-preliminar-template.md"
DEFAULT_INFOGRAFICO = ROOT / "03-Relatorios/02-Relatorios_Individuais_Preliminares/img/igovti_2026_composicao_infografico_v6.png"
DEFAULT_RELATORIO_CONSOLIDADO = ROOT / "03-Relatorios/01-Relatorio_Consolidado/Relatório_altaresolucao_novo.md"
DEFAULT_REFERENCE_DOCX = ROOT / "scripts/resources/template-base-estilos-sigiloso.docx"
DEFAULT_OUTPUT_DIR = Path("/tmp/tcerj-igovti-2026-ultima-versao")


def infer_prefixo(path: Path) -> str:
    match = re.search(r"(\d{8})", path.name)
    if not match:
        raise ValueError(f"Não foi possível inferir o prefixo AAAAMMDD a partir de {path.name}. Use --prefixo.")
    return match.group(1)


def run_step(title: str, cmd: list[str], cwd: Path) -> None:
    logging.info("%s", title)
    logging.info("Comando: %s", shlex.join(str(part) for part in cmd))
    subprocess.run([str(part) for part in cmd], cwd=cwd, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--respostas-bruto", type=Path, default=DEFAULT_BRUTO, help="Planilha bruta exportada do LimeSurvey.")
    parser.add_argument("--ajustes-iniciais", type=Path, default=DEFAULT_AJUSTES_INICIAIS, help="Planilha de ajustes iniciais registrados pela equipe.")
    parser.add_argument("--ajustes-evidencias", type=Path, default=DEFAULT_AJUSTES_EVIDENCIAS, help="Planilha de ajustes pós-avaliação de evidências.")
    parser.add_argument("--prefixo", default=None, help="Prefixo AAAAMMDD dos artefatos. Se omitido, é inferido do nome da planilha bruta.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Diretório base dos artefatos gerados.")
    parser.add_argument("--auditados", type=Path, default=DEFAULT_AUDITADOS, help="Base de auditados XLSX.")
    parser.add_argument("--mapa", type=Path, default=DEFAULT_MAPA, help="Mapa de verificação e achados XLSX.")
    parser.add_argument("--template-individual", type=Path, default=DEFAULT_TEMPLATE_INDIVIDUAL, help="Template Markdown dos relatórios individuais.")
    parser.add_argument("--relatorio-consolidado-md", type=Path, default=DEFAULT_RELATORIO_CONSOLIDADO, help="Markdown fonte do relatório consolidado.")
    parser.add_argument("--reference-docx", type=Path, default=DEFAULT_REFERENCE_DOCX, help="DOCX de referência de estilos.")
    parser.add_argument("--auditados-select", nargs="*", default=[], help="Siglas de auditados para relatórios individuais. Se omitido, gera todos.")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"], help="Nível de log.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    logging.basicConfig(level=getattr(logging, args.log_level), format="%(asctime)s - %(levelname)s - %(message)s")

    prefixo = args.prefixo or infer_prefixo(args.respostas_bruto)
    output_dir = args.output_dir.expanduser().resolve()
    questionario_dir = output_dir / "01-Questionario"
    auditoria_dir = output_dir / "auditoria"
    relatorios_dir = output_dir / "relatorios-individuais"
    consolidado_dir = output_dir / "relatorio-consolidado"

    base_inicial = questionario_dir / f"{prefixo}-respostas-questionario.xlsx"
    base_final = questionario_dir / f"{prefixo}-respostas-questionario-pos-avaliacao-evidencias.xlsx"
    resultado_oficial = questionario_dir / f"{prefixo}-iGovTI-2026.xlsx"
    resultado_comparavel = questionario_dir / f"{prefixo}-iGovTI-2026-Ajustado-Comparavel.xlsx"
    contexto_relatorios = questionario_dir / f"{prefixo}-contexto-relatorios-igovti-2026.xlsx"
    resultado_auditoria = auditoria_dir / "resultado_auditoria.json"
    tabelas_auditoria = auditoria_dir / "tabelas_consolidadas_auditoria.xlsx"
    relatorio_consolidado_docx = consolidado_dir / args.relatorio_consolidado_md.with_suffix(".docx").name

    for path in [questionario_dir, auditoria_dir, relatorios_dir, consolidado_dir]:
        path.mkdir(parents=True, exist_ok=True)

    python = sys.executable
    logging.info("Iniciando geração do pacote de relatórios iGovTI 2026.")
    logging.info("Prefixo: %s", prefixo)
    logging.info("Diretório de saída: %s", output_dir)

    run_step(
        "1/7 Aplicando ajustes iniciais sobre a base bruta.",
        [
            python,
            ROOT / "scripts/ajustar_respostas_questionario.py",
            "--respostas",
            args.respostas_bruto,
            "--ajustes",
            args.ajustes_iniciais,
            "--output",
            base_inicial,
        ],
        ROOT,
    )

    run_step(
        "2/7 Aplicando ajustes pós-avaliação de evidências.",
        [
            python,
            ROOT / "scripts/ajustar_respostas_questionario.py",
            "--respostas",
            base_inicial,
            "--ajustes",
            args.ajustes_evidencias,
            "--output",
            base_final,
        ],
        ROOT,
    )

    run_step(
        "3/7 Gerando artefatos iGovTI, comparação longitudinal e contexto estatístico.",
        [
            python,
            ROOT / "scripts/gerar_artefatos_igovti.py",
            "--respostas",
            base_final,
            "--prefixo",
            prefixo,
            "--output-dir",
            output_dir,
        ],
        ROOT,
    )

    run_step(
        "4/7 Executando procedimentos de auditoria.",
        [
            python,
            ROOT / "scripts/executa_auditoria.py",
            "--auditados",
            args.auditados,
            "--mapa",
            args.mapa,
            "--fontes",
            base_final,
            "--resultado-auditoria-json",
            resultado_auditoria,
            "--tabelas-auditoria-xlsx",
            tabelas_auditoria,
        ],
        ROOT,
    )

    run_step(
        "5/7 Gerando gráficos consolidados e individuais.",
        [
            python,
            ROOT / "scripts/gerar_graficos_relatorios_consolidado_individuais_igovti.py",
            "--output-root",
            output_dir,
            "--resultados-2026",
            resultado_oficial,
            "--respostas-2026",
            base_final,
            "--comparavel-2026",
            resultado_comparavel,
        ],
        ROOT,
    )

    relatorios_cmd = [
        python,
        ROOT / "scripts/gerar_relatorios_individuais.py",
        "--auditados",
        resultado_auditoria,
        "--templates",
        args.template_individual,
        "--context-files",
        contexto_relatorios,
        "--ajustes-respostas",
        args.ajustes_evidencias,
        "--resource-files",
        str(output_dir / "relatorios-individuais/img/**/*"),
        DEFAULT_INFOGRAFICO,
        "--output-dir",
        relatorios_dir,
        "--reference-docx",
        args.reference_docx,
    ]
    if args.auditados_select:
        relatorios_cmd.extend(["--auditados-select", *args.auditados_select])

    run_step("6/7 Gerando relatórios individuais.", relatorios_cmd, ROOT)

    run_step(
        "7/7 Gerando relatório consolidado.",
        [
            python,
            ROOT / "scripts/gerar_relatorio_consolidado.py",
            "--input",
            args.relatorio_consolidado_md,
            "--output",
            relatorio_consolidado_docx,
            "--reference-docx",
            args.reference_docx,
            "--resource-files",
            str(output_dir / "relatorio-consolidado/img/**/*"),
            str(output_dir / "relatorios-individuais/img/**/*"),
            "--resultados-2026",
            resultado_oficial,
            "--respostas-2026",
            base_final,
            "--comparavel-2026",
            resultado_comparavel,
            "--auditados-xlsx",
            args.auditados,
            "--resultado-auditoria-json",
            resultado_auditoria,
        ],
        ROOT,
    )

    docx_count = len(list(relatorios_dir.glob("Relatorio-*.docx")))
    logging.info("Pacote concluído.")
    logging.info("Relatórios individuais gerados: %s em %s", docx_count, relatorios_dir)
    logging.info("Relatório consolidado: %s", relatorio_consolidado_docx)
    logging.info("Resultado da auditoria: %s", resultado_auditoria)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
