#!/usr/bin/env python3
"""Executa o fluxo completo de geração dos relatórios iGovTI 2026."""

from __future__ import annotations

import argparse
import logging
import os
import re
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BRUTO = ROOT / "02-Execucao/01-Questionario/01-Coleta_LimeSurvey/20260621-respostas-questionario-bruto.xlsx"
DEFAULT_AJUSTES_INICIAIS = ROOT / "02-Execucao/01-Questionario/02-Ajustes_Respostas/ajustes_respostas_questionario_inicial.xlsx"
DEFAULT_AJUSTES_EVIDENCIAS = ROOT / "02-Execucao/01-Questionario/02-Ajustes_Respostas/ajustes_respostas_questionario_pos_avaliacao_evidencias.xlsx"
DEFAULT_PAINEL_AVALIACAO_EVIDENCIAS = ROOT / "02-Execucao/03-Execucao_Procedimentos/99-Avaliacao_Evidencias/painel-avaliacao-evidencias.xlsx"
DEFAULT_AUDITADOS = ROOT / "02-Execucao/03-Execucao_Procedimentos/01-Insumos/bd_auditados.xlsx"
DEFAULT_MAPA = ROOT / "02-Execucao/03-Execucao_Procedimentos/01-Insumos/mapa-verificacao-achados.xlsx"
DEFAULT_TEMPLATE_INDIVIDUAL = ROOT / "03-Relatorios/02-Relatorios_Individuais_Preliminares/relatorio-individual-preliminar-template.md"
DEFAULT_INFOGRAFICO = ROOT / "03-Relatorios/02-Relatorios_Individuais_Preliminares/img/igovti_2026_composicao_infografico_v6.png"
DEFAULT_RELATORIO_CONSOLIDADO = ROOT / "03-Relatorios/01-Relatorio_Consolidado/Relatório_altaresolucao_novo.md"
DEFAULT_REFERENCE_DOCX = ROOT / "scripts/resources/template-base-estilos-sigiloso.docx"
DEFAULT_ADMIN_COMENTARIOS_GESTOR = "CAD-TI"
DEFAULT_EMAIL_COMENTARIOS_GESTOR = "auditoriati@tcerj.tc.br"
DEFAULT_NUMERO_FISCALIZACAO_COMENTARIOS_GESTOR = "18/2026"
DEFAULT_NOME_FISCALIZACAO_COMENTARIOS_GESTOR = "iGovTI 2026"

default_tmp_root = Path("C:/tmp") if sys.platform.startswith("win") else Path(tempfile.gettempdir())
DEFAULT_OUTPUT_DIR = default_tmp_root / "tcerj-igovti-2026-ultima-versao"


def infer_prefixo(path: Path) -> str:
    match = re.search(r"(\d{8})", path.name)
    if not match:
        raise ValueError(f"Não foi possível inferir o prefixo AAAAMMDD a partir de {path.name}. Use --prefixo.")
    return match.group(1)


def run_step(title: str, cmd: list[str], cwd: Path) -> None:
    logging.info("%s", title)
    logging.info("Comando: %s", shlex.join(str(part) for part in cmd))
    subprocess.run([str(part) for part in cmd], cwd=cwd, check=True)


def _ler_siglas_xlsx(path: Path, coluna: str) -> set[str]:
    df = pd.read_excel(path)
    if coluna not in df.columns:
        raise ValueError(f"Planilha {path} não possui a coluna obrigatória {coluna!r}.")
    return {str(valor).strip() for valor in df[coluna].dropna() if str(valor).strip()}


def validar_cadastro_respostas(auditados_xlsx: Path, respostas_xlsx: Path) -> None:
    siglas_cadastro = _ler_siglas_xlsx(auditados_xlsx, "sigla")
    siglas_respostas = _ler_siglas_xlsx(respostas_xlsx, "firstname")
    fora_cadastro = sorted(siglas_respostas - siglas_cadastro)
    if fora_cadastro:
        raise ValueError(
            "Há respondentes ausentes da base de auditados. Atualize bd_auditados.xlsx antes "
            f"de continuar: {', '.join(fora_cadastro)}"
        )


def validar_contexto_respondentes(respostas_xlsx: Path, contexto_xlsx: Path) -> None:
    siglas_respostas = _ler_siglas_xlsx(respostas_xlsx, "firstname")
    siglas_contexto = _ler_siglas_xlsx(contexto_xlsx, "sigla")
    sem_contexto = sorted(siglas_respostas - siglas_contexto)
    if sem_contexto:
        raise ValueError(
            "Há respondentes sem contexto iGovTI calculado. Refaça os artefatos iGovTI antes "
            f"de gerar relatórios: {', '.join(sem_contexto)}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--respostas-bruto", type=Path, default=DEFAULT_BRUTO, help="Planilha bruta exportada do LimeSurvey.")
    parser.add_argument("--ajustes-iniciais", type=Path, default=DEFAULT_AJUSTES_INICIAIS, help="Planilha de ajustes iniciais registrados pela equipe.")
    parser.add_argument("--ajustes-evidencias", type=Path, default=DEFAULT_AJUSTES_EVIDENCIAS, help="Planilha de ajustes pós-avaliação de evidências.")
    parser.add_argument("--painel-avaliacao-evidencias", type=Path, default=DEFAULT_PAINEL_AVALIACAO_EVIDENCIAS, help="Painel consolidado da avaliacao de evidencias usado como fonte pela execucao da auditoria.")
    parser.add_argument("--prefixo", default=None, help="Prefixo AAAAMMDD dos artefatos. Se omitido, é inferido do nome da planilha bruta.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Diretório base dos artefatos gerados.")
    parser.add_argument("--auditados", type=Path, default=DEFAULT_AUDITADOS, help="Base de auditados XLSX.")
    parser.add_argument("--mapa", type=Path, default=DEFAULT_MAPA, help="Mapa de verificação e achados XLSX.")
    parser.add_argument("--template-individual", type=Path, default=DEFAULT_TEMPLATE_INDIVIDUAL, help="Template Markdown dos relatórios individuais.")
    parser.add_argument("--relatorio-consolidado-md", type=Path, default=DEFAULT_RELATORIO_CONSOLIDADO, help="Markdown fonte do relatório consolidado.")
    parser.add_argument("--reference-docx", type=Path, default=DEFAULT_REFERENCE_DOCX, help="DOCX de referência de estilos.")
    parser.add_argument(
        "--email-contato-comentarios-gestor",
        default=DEFAULT_EMAIL_COMENTARIOS_GESTOR,
        help=f"E-mail de contato para o questionário de comentários do gestor (padrão: {DEFAULT_EMAIL_COMENTARIOS_GESTOR}).",
    )
    parser.add_argument(
        "--admin-responsavel-comentarios-gestor",
        default=DEFAULT_ADMIN_COMENTARIOS_GESTOR,
        help=f"Nome do administrador responsável pelo questionário de comentários do gestor (padrão: {DEFAULT_ADMIN_COMENTARIOS_GESTOR}).",
    )
    parser.add_argument(
        "--data-final-preenchimento-comentarios-gestor",
        default="",
        help="Data final de preenchimento dos comentários do gestor em DD/MM/AAAA (padrão: data atual + 15 dias).",
    )
    parser.add_argument(
        "--numero-fiscalizacao-comentarios-gestor",
        default=DEFAULT_NUMERO_FISCALIZACAO_COMENTARIOS_GESTOR,
        help=(
            "Número da fiscalização usado no questionário de comentários do gestor "
            f"(padrão: {DEFAULT_NUMERO_FISCALIZACAO_COMENTARIOS_GESTOR})."
        ),
    )
    parser.add_argument(
        "--nome-fiscalizacao-comentarios-gestor",
        default=DEFAULT_NOME_FISCALIZACAO_COMENTARIOS_GESTOR,
        help=(
            "Nome da fiscalização usado no questionário de comentários do gestor "
            f"(padrão: {DEFAULT_NOME_FISCALIZACAO_COMENTARIOS_GESTOR})."
        ),
    )
    parser.add_argument(
        "--ajustes-evidencias-comentarios-gestor",
        type=Path,
        default=None,
        help="Planilha de ajustes pós-avaliação de evidências usada para incluir seção opcional de reavaliação no survey de comentários do gestor.",
    )
    parser.add_argument("--auditados-select", nargs="*", default=[], help="Siglas de auditados para relatórios individuais. Se omitido, gera todos.")
    parser.add_argument(
        "--graficos-jobs",
        type=int,
        default=max(1, min(4, (os.cpu_count() or 2) - 1)),
        help="Quantidade de processos paralelos para gráficos individuais.",
    )
    parser.add_argument("--graficos-dpi", type=int, default=300, help="Resolução dos PNG gerados para relatórios.")
    parser.add_argument("--graficos-skip-existing", action="store_true", help="Pula PNG de relatórios já existentes no diretório de saída.")
    parser.add_argument("--skip-relatorios-procedimentos", action="store_true", help="Pula a geração do ZIP de relatórios de procedimentos individuais.")
    parser.add_argument(
        "--tipo-relatorio-individual",
        choices=["preliminar", "final"],
        default="preliminar",
        help="Define o nome dos DOCX individuais: preliminar inclui 'Preliminar'; final remove esse termo.",
    )
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"], help="Nível de log.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    logging.basicConfig(level=getattr(logging, args.log_level), format="%(asctime)s - %(levelname)s - %(message)s")

    prefixo = args.prefixo or infer_prefixo(args.respostas_bruto)
    output_dir = args.output_dir.expanduser().resolve()
    execucao_dir = output_dir / "02-Execucao"
    questionario_dir = execucao_dir / "01-Questionario"
    respostas_dir = questionario_dir / "03-Respostas_Processadas"
    resultados_igovti_dir = questionario_dir / "04-Resultados_iGovTI"
    auditoria_dir = execucao_dir / "03-Execucao_Procedimentos" / "02-Resultados_Auditoria"
    comentarios_dir = execucao_dir / "05-Comentarios_Gestor"
    relatorios_dir = output_dir / "relatorios-individuais"
    consolidado_dir = output_dir / "relatorio-consolidado"

    base_inicial = respostas_dir / f"{prefixo}-respostas-questionario.xlsx"
    base_final = respostas_dir / f"{prefixo}-respostas-questionario-pos-avaliacao-evidencias.xlsx"
    resultado_oficial = resultados_igovti_dir / f"{prefixo}-iGovTI-2026.xlsx"
    resultado_comparavel = resultados_igovti_dir / f"{prefixo}-iGovTI-2026-Ajustado-Comparavel.xlsx"
    contexto_relatorios = resultados_igovti_dir / f"{prefixo}-contexto-relatorios-igovti-2026.xlsx"
    resultado_auditoria = auditoria_dir / "resultado_auditoria.json"
    tabelas_auditoria = auditoria_dir / "tabelas_consolidadas_auditoria.xlsx"
    anexo_evidencias = auditoria_dir / "anexo_evidencias.docx"
    relatorios_procedimentos = auditoria_dir / "relatorios_procedimentos.zip"
    comentarios_lss = comentarios_dir / "questionario_comentarios_gestor.lss"
    comentarios_zip = comentarios_dir / "anexos_docx_comentarios.zip"
    relatorio_consolidado_docx = consolidado_dir / args.relatorio_consolidado_md.with_suffix(".docx").name

    for path in [respostas_dir, resultados_igovti_dir, auditoria_dir, comentarios_dir, relatorios_dir, consolidado_dir]:
        path.mkdir(parents=True, exist_ok=True)

    nome_base_relatorio_individual = "Relatório Individual Preliminar" if args.tipo_relatorio_individual == "preliminar" else "Relatório Individual"

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

    validar_cadastro_respostas(args.auditados, base_final)

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
            execucao_dir,
        ],
        ROOT,
    )

    validar_contexto_respondentes(base_final, contexto_relatorios)

    auditoria_cmd = [
        python,
        ROOT / "scripts/executa_auditoria.py",
        "--auditados",
        args.auditados,
        "--mapa",
        args.mapa,
        "--fontes",
        base_final,
        args.painel_avaliacao_evidencias,
        "--resultado-auditoria-json",
        resultado_auditoria,
        "--tabelas-auditoria-xlsx",
        tabelas_auditoria,
        "--out-proc-zip",
        relatorios_procedimentos,
        "--out-evidencias-docx",
        anexo_evidencias,
        "--out-lss",
        comentarios_lss,
        "--out-comentarios-zip",
        comentarios_zip,
        "--email-contato-comentarios-gestor",
        args.email_contato_comentarios_gestor,
        "--admin-responsavel-comentarios-gestor",
        args.admin_responsavel_comentarios_gestor,
        "--data-final-preenchimento-comentarios-gestor",
        args.data_final_preenchimento_comentarios_gestor,
        "--numero-fiscalizacao-comentarios-gestor",
        args.numero_fiscalizacao_comentarios_gestor,
        "--nome-fiscalizacao-comentarios-gestor",
        args.nome_fiscalizacao_comentarios_gestor,
    ]
    if args.ajustes_evidencias_comentarios_gestor:
        auditoria_cmd.extend([
            "--ajustes-evidencias-comentarios-gestor",
            args.ajustes_evidencias_comentarios_gestor,
        ])
    if args.skip_relatorios_procedimentos:
        auditoria_cmd.append("--skip-relatorios-procedimentos")

    run_step("4/7 Executando procedimentos de auditoria.", auditoria_cmd, ROOT)

    graficos_cmd = [
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
        "--jobs",
        args.graficos_jobs,
        "--dpi",
        args.graficos_dpi,
    ]
    if args.graficos_skip_existing:
        graficos_cmd.append("--skip-existing")
    if args.auditados_select:
        graficos_cmd.extend(["--auditados", *args.auditados_select])

    run_step("5/7 Gerando gráficos consolidados e individuais.", graficos_cmd, ROOT)

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
        "--nome-base-docx",
        nome_base_relatorio_individual,
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

    docx_count = len(list(relatorios_dir.glob(f"{nome_base_relatorio_individual} - *.docx")))
    logging.info("Pacote concluído.")
    logging.info("Relatórios individuais gerados: %s em %s", docx_count, relatorios_dir)
    logging.info("Relatório consolidado: %s", relatorio_consolidado_docx)
    logging.info("Resultado da auditoria: %s", resultado_auditoria)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
