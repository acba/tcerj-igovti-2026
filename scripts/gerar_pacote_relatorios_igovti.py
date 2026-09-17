#!/usr/bin/env python3
"""Executa, retoma e documenta o fluxo completo da auditoria iGovTI 2026."""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
import tempfile
from datetime import datetime
from pathlib import Path

try:
    from pipeline_auditoria import Manifest, PipelineRunner, Stage
except ModuleNotFoundError:  # Importação como módulo em testes e integrações.
    from scripts.pipeline_auditoria import Manifest, PipelineRunner, Stage


ROOT = Path(__file__).resolve().parents[1]
PYTHON = str(Path(sys.executable))
SCRIPTS = ROOT / "scripts"
DEFAULT_BRUTO = ROOT / "02-Execucao/01-Questionario/01-Coleta_LimeSurvey/20260621-respostas-questionario-bruto.xlsx"
DEFAULT_AJUSTES_INICIAIS = ROOT / "02-Execucao/01-Questionario/02-Ajustes_Respostas/ajustes_respostas_questionario_inicial.xlsx"
DEFAULT_EVIDENCIAS = ROOT / "02-Execucao/01-Questionario/01-Coleta_LimeSurvey/Evidencias_Coletadas/evidencias_extraidas"
DEFAULT_AJUSTES_EVIDENCIAS = ROOT / "02-Execucao/01-Questionario/02-Ajustes_Respostas/ajustes_respostas_questionario_pos_avaliacao_evidencias.xlsx"
DEFAULT_PAINEL_EVIDENCIAS = ROOT / "02-Execucao/03-Execucao_Procedimentos/99-Avaliacao_Evidencias/painel-avaliacao-evidencias.xlsx"
DEFAULT_AUDITADOS = ROOT / "02-Execucao/03-Execucao_Procedimentos/01-Insumos/bd_auditados.xlsx"
DEFAULT_MAPA = ROOT / "02-Execucao/03-Execucao_Procedimentos/01-Insumos/mapa-verificacao-achados-pos-comentarios-gestor.xlsx"
DEFAULT_MATRIZ = ROOT / "01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/matriz_planejamento-pos-comentarios-gestor.md"
DEFAULT_QUESTIONARIO = ROOT / "01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md"
DEFAULT_PROMPTS = ROOT / "scripts/avaliacao_evidencias/prompts/igovti_2026_achados_binario_v1"
DEFAULT_CATALOG = ROOT / "scripts/avaliacao_evidencias/prompt_catalogs/igovti_2026_achados_binario_v1.yml"
DEFAULT_CATALOG_COMENTARIOS = ROOT / "scripts/avaliacao_evidencias/prompt_catalogs/igovti_2026_comentarios_gestor_atual_v4.yml"
DEFAULT_MODELS_COMENTARIOS = ROOT / "scripts/avaliacao_evidencias/configs/comentarios_gestor_models_v1.json"
DEFAULT_MODELS_EVIDENCIAS = ROOT / "scripts/avaliacao_evidencias/configs/evidencias_models_v1.json"
DEFAULT_REVISOES_PARECERES = ROOT / "02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor/revisoes_pareceres.yml"
DEFAULT_REVISOES_RESPOSTAS = ROOT / "02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor/revisoes_respostas.yml"
DEFAULT_TEMPLATE_PRELIMINAR = ROOT / "03-Relatorios/02-Relatorios_Individuais_Preliminares/relatorio-individual-preliminar-template.md"
DEFAULT_TEMPLATE_FINAL = ROOT / "03-Relatorios/03-Relatorios_Individuais_Finais/relatorio-individual-template.md"
DEFAULT_RELATORIO_CONSOLIDADO = ROOT / "03-Relatorios/01-Relatorio_Consolidado/Relatório_altaresolucao_novo.md"
DEFAULT_REFERENCE = ROOT / "scripts/resources/template-base-estilos-sigiloso.docx"
DEFAULT_REFERENCE_CONSOLIDADO = ROOT / "scripts/resources/template-base-estilos.docx"
DEFAULT_MODELO_INSTITUCIONAL_CONSOLIDADO = (
    ROOT / "scripts/resources/template-relatorio-consolidado-institucional.docx"
)
DEFAULT_INFOGRAFICO = ROOT / "03-Relatorios/01-Relatorio_Consolidado/img/igovti_2026_composicao_infografico.png"
DEFAULT_WORKERS = max(1, min(8, os.cpu_count() or 1))


def infer_prefixo(path: Path) -> str:
    match = re.search(r"(\d{8})", path.name)
    if not match:
        raise ValueError(f"Não foi possível inferir AAAAMMDD de {path.name}; use --prefixo.")
    return match.group(1)


def cmd(script: Path, *args: object) -> tuple[str, ...]:
    return (PYTHON, str(script), *(str(item) for item in args))


def igovti_outputs(resultados: Path, prefixo: str) -> tuple[Path, ...]:
    return (
        resultados / f"{prefixo}-iGovTI-2026.xlsx",
        resultados / f"{prefixo}-iGovTI-2026-Ajustado-Comparavel.xlsx",
        resultados / f"{prefixo}-contexto-relatorios-igovti-2026.xlsx",
        resultados / f"{prefixo}-estatisticas-relatorios-igovti-2026.json",
    )


def auditoria_stage(
    key: str,
    title: str,
    scenario: str,
    args: argparse.Namespace,
    respostas: Path,
    painel: Path,
    out_dir: Path,
) -> Stage:
    resultado = out_dir / "resultado_auditoria.json"
    tabelas = out_dir / "tabelas_consolidadas_auditoria.xlsx"
    command = list(cmd(
        SCRIPTS / "executa_auditoria.py",
        "--auditados", args.auditados,
        "--mapa", args.mapa,
        "--matriz", args.matriz,
        "--fonte", f"questionario={respostas}",
        "--fonte", f"avaliacao_evidencias_ajustes={painel}",
        "--resultado-json", resultado,
        "--tabelas-xlsx", tabelas,
        "--somente-dados",
    ))
    return Stage(
        key, title, tuple(command),
        inputs=(args.auditados, args.mapa, args.matriz, respostas, painel),
        outputs=(resultado, tabelas), scenario=scenario,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--respostas-bruto", type=Path, default=DEFAULT_BRUTO)
    parser.add_argument("--ajustes-iniciais", type=Path, default=DEFAULT_AJUSTES_INICIAIS)
    parser.add_argument("--evidencias-root", type=Path, default=DEFAULT_EVIDENCIAS)
    parser.add_argument("--avaliadores-config", type=Path, default=DEFAULT_MODELS_EVIDENCIAS)
    parser.add_argument("--juizes-config", type=Path, default=DEFAULT_MODELS_EVIDENCIAS)
    parser.add_argument("--prefixo")
    parser.add_argument("--output-dir", "--output-root", dest="output_root", type=Path, default=ROOT)
    parser.add_argument("--auditados", type=Path, default=DEFAULT_AUDITADOS)
    parser.add_argument("--mapa", type=Path, default=DEFAULT_MAPA)
    parser.add_argument("--matriz", type=Path, default=DEFAULT_MATRIZ)
    parser.add_argument("--questionario", type=Path, default=DEFAULT_QUESTIONARIO)
    parser.add_argument("--prompts-dir", type=Path, default=DEFAULT_PROMPTS)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--respostas-comentarios", type=Path)
    parser.add_argument("--evidencias-comentarios-root", type=Path)
    parser.add_argument("--models-config-comentarios", type=Path, default=DEFAULT_MODELS_COMENTARIOS)
    parser.add_argument("--catalog-comentarios", type=Path, default=DEFAULT_CATALOG_COMENTARIOS)
    parser.add_argument("--revisoes-pareceres", type=Path, default=DEFAULT_REVISOES_PARECERES)
    parser.add_argument("--revisoes-respostas", type=Path, default=DEFAULT_REVISOES_RESPOSTAS)
    parser.add_argument("--data-referencia-comentarios", default=datetime.now().strftime("%d/%m/%Y"))
    parser.add_argument("--data-final-preenchimento-comentarios-gestor", default="")
    parser.add_argument("--email-contato-comentarios-gestor", default="auditoriati@tcerj.tc.br")
    parser.add_argument("--admin-responsavel-comentarios-gestor", default="CAD-TI")
    parser.add_argument("--numero-fiscalizacao-comentarios-gestor", default="18/2026")
    parser.add_argument("--nome-fiscalizacao-comentarios-gestor", default="iGovTI 2026")
    parser.add_argument("--template-preliminar", type=Path, default=DEFAULT_TEMPLATE_PRELIMINAR)
    parser.add_argument("--template-final", type=Path, default=DEFAULT_TEMPLATE_FINAL)
    parser.add_argument("--relatorio-consolidado-md", type=Path, default=DEFAULT_RELATORIO_CONSOLIDADO)
    parser.add_argument("--reference-docx", type=Path, default=DEFAULT_REFERENCE)
    parser.add_argument("--reference-docx-consolidado", type=Path, default=DEFAULT_REFERENCE_CONSOLIDADO)
    parser.add_argument(
        "--modelo-institucional-consolidado",
        type=Path,
        default=DEFAULT_MODELO_INSTITUCIONAL_CONSOLIDADO,
    )
    parser.add_argument("--auditados-select", nargs="*", default=[])
    parser.add_argument("--graficos-jobs", type=int, default=4)
    parser.add_argument("--graficos-dpi", type=int, default=300)
    parser.add_argument("--fake-comentarios", action="store_true")
    parser.add_argument("--from-stage")
    parser.add_argument("--until-stage")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--status-only", action="store_true")
    parser.add_argument("--adopt-existing", action="store_true", help="Registra produtos legados existentes no manifesto sem sobrescrevê-los.")
    parser.add_argument("--force-stage", action="append", default=[], help="Reexecuta uma etapa específica, inclusive após falha ou correção.")
    parser.add_argument("--skip-graficos", action="store_true")
    parser.add_argument("--skip-relatorios", action="store_true")
    parser.add_argument("--skip-relatorio-consolidado", action="store_true")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], default="INFO")
    # Compatibilidade com a interface anterior.
    parser.add_argument("--ajustes-evidencias", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--painel-avaliacao-evidencias", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--graficos-skip-existing", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--gerar-relatorios-procedimentos", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--skip-relatorios-procedimentos", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--auditoria-jobs-relatorios-procedimentos", type=int, default=DEFAULT_WORKERS, help=argparse.SUPPRESS)
    parser.add_argument("--auditoria-jobs-comentarios-gestor-anexos", type=int, default=DEFAULT_WORKERS, help=argparse.SUPPRESS)
    parser.add_argument("--ajustes-evidencias-comentarios-gestor", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--tipo-relatorio-individual", choices=["preliminar", "final"], help=argparse.SUPPRESS)
    return parser


def build_stages(args: argparse.Namespace) -> list[Stage]:
    root = args.output_root.expanduser().resolve()
    prefixo = args.prefixo or infer_prefixo(args.respostas_bruto)
    try:
        prefixo_atual = datetime.strptime(args.data_referencia_comentarios, "%d/%m/%Y").strftime("%Y%m%d")
    except ValueError as exc:
        raise ValueError("--data-referencia-comentarios deve usar DD/MM/AAAA") from exc
    respostas_root = root / "02-Execucao/01-Questionario/03-Respostas_Processadas"
    resultados_root = root / "02-Execucao/01-Questionario/04-Resultados_iGovTI"
    auditorias_root = root / "02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria"
    avaliacao_root = root / "02-Execucao/03-Execucao_Procedimentos/99-Avaliacao_Evidencias"
    comentarios_root = root / "02-Execucao/05-Comentarios_Gestor"
    relatorios_pre = root / "03-Relatorios/02-Relatorios_Individuais_Preliminares/gerados"
    relatorios_final = root / "03-Relatorios/03-Relatorios_Individuais_Finais/gerados"
    graficos_02 = root / "03-Relatorios/00-Recursos_Gerados/02-pos-avaliacao-evidencias"
    graficos_03 = root / "03-Relatorios/00-Recursos_Gerados/03-pos-comentarios-gestor"

    r1 = respostas_root / f"{prefixo}-respostas-questionario-01-pos-ajuste-inicial.xlsx"
    r2 = respostas_root / f"{prefixo}-respostas-questionario-02-pos-avaliacao-evidencias.xlsx"
    r3 = respostas_root / f"{prefixo_atual}-respostas-questionario-pos-comentarios-gestor.xlsx"
    i1, i2, i3 = (resultados_root / scenario for scenario in (
        "01-pos-ajuste-inicial", "02-pos-avaliacao-evidencias", "03-pos-comentarios-gestor"
    ))
    a1, a2, a3 = (auditorias_root / scenario for scenario in (
        "01-pos-ajuste-inicial", "02-pos-avaliacao-evidencias", "03-pos-comentarios-gestor"
    ))
    neutral = avaliacao_root / "painel-avaliacao-evidencias-neutro.xlsx"
    individuais = avaliacao_root / "individuais"
    consolidado = avaliacao_root / "consolidado"
    pareceres = consolidado / "pareceres_consolidados.xlsx"
    ajustes_evidencias = args.ajustes_evidencias or (
        DEFAULT_AJUSTES_EVIDENCIAS if root == ROOT and DEFAULT_AJUSTES_EVIDENCIAS.is_file()
        else avaliacao_root / "ajustes_respostas_questionario_pos_avaliacao_evidencias.xlsx"
    )
    painel_evidencias = args.painel_avaliacao_evidencias or (
        DEFAULT_PAINEL_EVIDENCIAS if root == ROOT and DEFAULT_PAINEL_EVIDENCIAS.is_file()
        else avaliacao_root / "painel-avaliacao-evidencias.xlsx"
    )
    comentarios_lss = comentarios_root / "questionario_comentarios_gestor.lss"
    comentarios_zip = comentarios_root / "anexos_docx_comentarios.zip"
    avaliacao_comentarios = comentarios_root / "02-Avaliacao_Comentarios_Gestor"
    ajustes_comentarios = avaliacao_comentarios / "ajustes_respostas_questionario_pos_comentarios_gestor.xlsx"
    painel_comentarios = avaliacao_comentarios / "fontes-auditoria-pos-comentarios/painel-avaliacao-evidencias.xlsx"
    produtos_comentarios = comentarios_root / "03-Produtos_Pos_Comentarios"
    pareceres_comentarios = produtos_comentarios / "avaliacao_comentarios_gestor.xlsx"
    contexto_comentarios = produtos_comentarios / "contexto-relatorios-comentarios-gestor.json"
    impactos_comentarios_json = produtos_comentarios / "impactos-comentarios-gestor.json"
    impactos_comentarios_xlsx = produtos_comentarios / "impactos-comentarios-gestor.xlsx"
    diagnostico_root = root / "03-Relatorios/01-Relatorio_Consolidado/dados"
    diagnostico_json = diagnostico_root / "diagnostico-transversal-igovti-2026.json"
    diagnostico_xlsx = diagnostico_root / "diagnostico-transversal-igovti-2026.xlsx"

    stages: list[Stage] = []
    cobertura_aplicabilidade = root / "02-Execucao/00-Controle_Execucao/cobertura-aplicabilidade-juridica.xlsx"
    stages.append(Stage(
        "00-validacao-aplicabilidade",
        "Validando aplicabilidade jurídica da matriz e do mapa",
        cmd(
            SCRIPTS / "validar_aplicabilidade_juridica.py",
            "--matriz", args.matriz,
            "--mapa", args.mapa,
            "--auditados", args.auditados,
            "--relatorio-xlsx", cobertura_aplicabilidade,
        ),
        inputs=(args.matriz, args.mapa, args.auditados),
        outputs=(cobertura_aplicabilidade,),
    ))
    stages.append(Stage(
        "01-ajustes-iniciais", "Aplicando ajustes iniciais", cmd(
            SCRIPTS / "ajustar_respostas_questionario.py", "--respostas", args.respostas_bruto,
            "--ajustes", args.ajustes_iniciais, "--output", r1,
        ), inputs=(args.respostas_bruto, args.ajustes_iniciais), outputs=(r1,), scenario="01-pos-ajuste-inicial",
    ))
    for n, respostas, resultados, scenario in ((2, r1, i1, "01-pos-ajuste-inicial"),):
        outputs = igovti_outputs(resultados, prefixo)
        stages.append(Stage(
            f"{n:02d}-igovti-{scenario}", f"Calculando iGovTI do cenário {scenario}", cmd(
                SCRIPTS / "gerar_artefatos_igovti.py", "--respostas", respostas, "--prefixo", prefixo,
                "--output-dir", root / "02-Execucao", "--resultados-dir", resultados,
                "--comparacao-dir", resultados / "comparacao-2023-2026",
            ), inputs=(respostas,), outputs=outputs, scenario=scenario,
        ))
    stages.append(Stage(
        "03-painel-neutro", "Criando painel neutro do cenário anterior às evidências",
        cmd(SCRIPTS / "criar_painel_evidencias_neutro.py", "--output", neutral, "--mapa", args.mapa),
        inputs=(args.mapa,), outputs=(neutral,), scenario="01-pos-ajuste-inicial",
    ))
    stages.append(auditoria_stage("04-auditoria-01", "Executando auditoria do cenário 01", "01-pos-ajuste-inicial", args, r1, neutral, a1))

    avaliacao_cmd = list(cmd(
        SCRIPTS / "run_avaliacao_evidencias_v2.py", "--respostas", r1, "--evidencias", args.evidencias_root,
        "--out-dir", individuais, "--questionario", args.questionario, "--prompts-dir", args.prompts_dir,
        "--prompt-version", "igovti_2026_achados_binario_v1", "--catalog", args.catalog, "--only-achados",
    ))
    if args.avaliadores_config:
        avaliacao_cmd.extend(["--models-config", str(args.avaliadores_config)])
    stages.append(Stage(
        "05-avaliar-evidencias", "Avaliando evidências do questionário", tuple(avaliacao_cmd),
        inputs=(r1, args.evidencias_root, args.questionario, args.catalog),
        outputs=(), metadata={"config": str(args.avaliadores_config or "embutida"), "output_dirs": [str(individuais)]},
    ))
    consolidar_cmd = list(cmd(
        SCRIPTS / "run_consolida_avaliacoes_v2.py", "--evidencias", args.evidencias_root,
        "--analyses-glob", individuais / "analyses_clean*.jsonl", "--out-dir", consolidado,
        "--catalog", args.catalog, "--only-achados", "--min-opinions", 3,
    ))
    if args.juizes_config:
        consolidar_cmd.extend(["--judges-config", str(args.juizes_config)])
    stages.append(Stage(
        "06-consolidar-evidencias", "Consolidando avaliações de evidências", tuple(consolidar_cmd),
        inputs=(args.evidencias_root, args.catalog), outputs=(consolidado / "consolidated.jsonl", pareceres),
        metadata={"config": str(args.juizes_config or "embutida")},
    ))
    stages.append(Stage(
        "07-ajustes-evidencias", "Gerando minuta de ajustes pós-evidências", cmd(
            SCRIPTS / "gerar_ajustes_pos_avaliacao_evidencias.py", "--pareceres", pareceres,
            "--output", ajustes_evidencias,
        ), inputs=(pareceres,), outputs=(ajustes_evidencias,), scenario="02-pos-avaliacao-evidencias",
    ))
    stages.append(Stage(
        "08-painel-evidencias", "Gerando painel pós-evidências", cmd(
            SCRIPTS / "gerar_fonte_ajustes_evidencias_auditoria.py", "--ajustes", ajustes_evidencias,
            "--mapa", args.mapa, "--output", painel_evidencias,
        ), inputs=(ajustes_evidencias, args.mapa), outputs=(painel_evidencias,), scenario="02-pos-avaliacao-evidencias",
    ))
    stages.append(Stage(
        "09-aplicar-ajustes-evidencias", "Aplicando ajustes pós-evidências", cmd(
            SCRIPTS / "ajustar_respostas_questionario.py", "--respostas", r1, "--ajustes", ajustes_evidencias,
            "--output", r2,
        ), inputs=(r1, ajustes_evidencias), outputs=(r2,), scenario="02-pos-avaliacao-evidencias",
    ))
    stages.append(Stage(
        "10-igovti-02", "Calculando iGovTI do cenário 02", cmd(
            SCRIPTS / "gerar_artefatos_igovti.py", "--respostas", r2, "--prefixo", prefixo,
            "--output-dir", root / "02-Execucao", "--resultados-dir", i2,
            "--comparacao-dir", i2 / "comparacao-2023-2026",
        ), inputs=(r2,), outputs=igovti_outputs(i2, prefixo), scenario="02-pos-avaliacao-evidencias",
    ))
    stages.append(auditoria_stage("11-auditoria-02", "Executando auditoria do cenário 02", "02-pos-avaliacao-evidencias", args, r2, painel_evidencias, a2))
    impacto_evidencias = root / "03-Relatorios/99-Impacto_Avaliacao_Evidencias/dados_impacto_avaliacao_evidencias.xlsx"
    stages.append(Stage(
        "12-impacto-evidencias", "Mensurando o impacto da avaliação de evidências", cmd(
            ROOT / "03-Relatorios/99-Impacto_Avaliacao_Evidencias/atualizar_dados_impacto_avaliacao_evidencias.py",
            "--igovti-pre", igovti_outputs(i1, prefixo)[0], "--igovti-final", igovti_outputs(i2, prefixo)[0],
            "--respostas-pre", r1, "--respostas-final", r2, "--ajustes", ajustes_evidencias,
            "--pareceres", pareceres, "--auditoria-pre", a1 / "resultado_auditoria.json",
            "--auditoria-final", a2 / "resultado_auditoria.json", "--universo-auditoria", args.auditados,
            "--output", impacto_evidencias,
        ), inputs=(igovti_outputs(i1, prefixo)[0], igovti_outputs(i2, prefixo)[0], r1, r2, ajustes_evidencias,
                   pareceres, a1 / "resultado_auditoria.json", a2 / "resultado_auditoria.json", args.auditados),
        outputs=(impacto_evidencias,),
    ))

    if not args.skip_graficos:
        stages.append(Stage(
            "13-graficos-preliminares", "Gerando gráficos preliminares", cmd(
                SCRIPTS / "gerar_graficos_relatorios_consolidado_individuais_igovti.py",
                "--output-root", graficos_02, "--resultados-2026", igovti_outputs(i2, prefixo)[0],
                "--respostas-2026", r2, "--comparavel-2026", igovti_outputs(i2, prefixo)[1],
                "--mapa", args.mapa,
                "--jobs", args.graficos_jobs, "--dpi", args.graficos_dpi,
            ), inputs=(igovti_outputs(i2, prefixo)[0], r2, igovti_outputs(i2, prefixo)[1], args.mapa), outputs=(),
            scenario="02-pos-avaliacao-evidencias",
            metadata={"output_dirs": [str(graficos_02 / "relatorios-individuais/img"), str(graficos_02 / "relatorio-consolidado/img")]},
        ))
    if not args.skip_relatorios:
        report_cmd = list(cmd(
            SCRIPTS / "gerar_relatorios_individuais.py", "--auditados", a2 / "resultado_auditoria.json",
            "--templates", args.template_preliminar, "--context-files", igovti_outputs(i2, prefixo)[2],
            "--ajustes-respostas", ajustes_evidencias, "--resource-files",
            str(graficos_02 / "relatorios-individuais/img/**/*"), DEFAULT_INFOGRAFICO,
            "--output-dir", relatorios_pre, "--reference-docx", args.reference_docx,
            "--nome-base-docx", "Relatório Individual Preliminar",
        ))
        if args.auditados_select:
            report_cmd.extend(["--auditados-select", *args.auditados_select])
        stages.append(Stage(
            "14-relatorios-preliminares", "Gerando relatórios individuais preliminares", tuple(report_cmd),
            inputs=(a2 / "resultado_auditoria.json", args.template_preliminar, igovti_outputs(i2, prefixo)[2]),
            outputs=(), scenario="02-pos-avaliacao-evidencias", metadata={"output_dirs": [str(relatorios_pre)]},
        ))

    comentarios_cmd = list(cmd(
        SCRIPTS / "gerar_comentarios_gestor.py", "--resultado-auditoria-json", a2 / "resultado_auditoria.json",
        "--comentarios-gestor-lss", comentarios_lss, "--comentarios-gestor-anexos-zip", comentarios_zip,
        "--jobs-comentarios-gestor-anexos", args.auditoria_jobs_comentarios_gestor_anexos,
        "--data-final-preenchimento-comentarios-gestor", args.data_final_preenchimento_comentarios_gestor,
        "--email-contato-comentarios-gestor", args.email_contato_comentarios_gestor,
        "--admin-responsavel-comentarios-gestor", args.admin_responsavel_comentarios_gestor,
        "--numero-fiscalizacao-comentarios-gestor", args.numero_fiscalizacao_comentarios_gestor,
        "--nome-fiscalizacao-comentarios-gestor", args.nome_fiscalizacao_comentarios_gestor,
        "--ajustes-evidencias-comentarios-gestor", ajustes_evidencias,
    ))
    stages.append(Stage(
        "15-survey-comentarios", "Gerando survey e anexos de comentários do gestor", tuple(comentarios_cmd),
        inputs=(a2 / "resultado_auditoria.json", ajustes_evidencias), outputs=(comentarios_lss, comentarios_zip),
    ))

    if args.respostas_comentarios:
        respostas_comentarios = args.respostas_comentarios
    else:
        coleta = comentarios_root / "01-Coleta_LimeSurvey"
        candidatas = sorted(coleta.glob("*-respostas-bruto.xlsx")) if coleta.is_dir() else []
        respostas_comentarios = candidatas[-1] if candidatas else coleta / "respostas-comentarios-gestor.xlsx"
    evidencias_comentarios = args.evidencias_comentarios_root or comentarios_root / "01-Coleta_LimeSurvey/Evidencias_Coletadas/evidencias_extraidas"
    stats_dir = root / "03-Relatorios/99-Avaliacao_Comentarios_Gestor"
    pipeline_comments = list(cmd(
        SCRIPTS / "run_comentarios_gestor.py", "completo", "--respostas-comentarios", respostas_comentarios,
        "--evidencias-comentarios-root", evidencias_comentarios, "--lss", comentarios_lss,
        "--resultado-auditoria", a2 / "resultado_auditoria.json", "--mapa", args.mapa,
        "--ajustes-pos-avaliacao-evidencias", ajustes_evidencias, "--questionario", args.questionario,
        "--respostas-questionario-base", r2, "--respostas-questionario-originais", args.respostas_bruto,
        "--painel-avaliacao-evidencias", painel_evidencias, "--catalog-comentarios", args.catalog_comentarios,
        "--revisoes-respostas", args.revisoes_respostas, "--revisoes-pareceres", args.revisoes_pareceres,
        "--models-config", args.models_config_comentarios, "--out-dir", avaliacao_comentarios,
    ))
    if args.fake_comentarios:
        pipeline_comments.append("--fake")
    stages.append(Stage(
        "17-avaliar-comentarios", "Avaliando e consolidando comentários do gestor", tuple(pipeline_comments),
        inputs=(respostas_comentarios, evidencias_comentarios, comentarios_lss, a2 / "resultado_auditoria.json",
                args.mapa, ajustes_evidencias, r2, painel_evidencias, args.models_config_comentarios,
                args.revisoes_respostas, args.revisoes_pareceres),
        outputs=(ajustes_comentarios, painel_comentarios), metadata={
            "output_dirs": [str(avaliacao_comentarios)],
            "review_artifact": str(avaliacao_comentarios / "revisao-humana-pareceres.xlsx"),
        },
    ))
    products_cmd = list(cmd(
        SCRIPTS / "gerar_produtos_pos_comentarios_gestor.py", "--data-referencia", args.data_referencia_comentarios,
        "--respostas-base", r2, "--respostas-comentarios", respostas_comentarios,
        "--avaliacao-comentarios-dir", avaliacao_comentarios, "--ajustes-comentarios", ajustes_comentarios,
        "--output-root", root, "--prefixo", prefixo_atual,
    ))
    if args.revisoes_pareceres:
        products_cmd.extend(["--revisoes-pareceres", str(args.revisoes_pareceres)])
    products_inputs = (r2, respostas_comentarios, ajustes_comentarios) + (
        (args.revisoes_pareceres,) if args.revisoes_pareceres else ()
    )
    stages.append(Stage(
        "18-produtos-pos-comentarios", "Gerando produtos básicos pós-comentários", tuple(products_cmd),
        inputs=products_inputs,
        outputs=(r3, pareceres_comentarios, contexto_comentarios), scenario="03-pos-comentarios-gestor",
    ))
    stages.append(Stage(
        "19-igovti-03", "Calculando iGovTI do cenário 03", cmd(
            SCRIPTS / "gerar_artefatos_igovti.py", "--respostas", r3, "--prefixo", prefixo_atual,
            "--output-dir", root / "02-Execucao", "--resultados-dir", i3,
            "--comparacao-dir", i3 / "comparacao-2023-2026",
        ), inputs=(r3,), outputs=igovti_outputs(i3, prefixo_atual), scenario="03-pos-comentarios-gestor",
    ))
    stages.append(auditoria_stage("20-auditoria-03", "Executando auditoria do cenário 03", "03-pos-comentarios-gestor", args, r3, painel_comentarios, a3))
    stages.append(Stage(
        "21-impacto-comentarios", "Mensurando impacto dos comentários do gestor", cmd(
            SCRIPTS / "calcular_impactos_comentarios_gestor.py",
            "--auditoria-anterior", a2 / "resultado_auditoria.json", "--auditoria-atual", a3 / "resultado_auditoria.json",
            "--contexto-igovti-anterior", igovti_outputs(i2, prefixo)[2],
            "--contexto-igovti-atual", igovti_outputs(i3, prefixo_atual)[2],
            "--output-json", impactos_comentarios_json, "--output-xlsx", impactos_comentarios_xlsx,
        ), inputs=(a2 / "resultado_auditoria.json", a3 / "resultado_auditoria.json",
                   igovti_outputs(i2, prefixo)[2], igovti_outputs(i3, prefixo_atual)[2]),
        outputs=(impactos_comentarios_json, impactos_comentarios_xlsx),
    ))
    stages.append(Stage(
        "22-estatisticas-comentarios", "Calculando estatísticas finais dos comentários do gestor", cmd(
            ROOT / "03-Relatorios/99-Avaliacao_Comentarios_Gestor/calcular_dados_comentarios_gestor.py",
            "--respostas", respostas_comentarios, "--lss", comentarios_lss,
            "--resultado-auditoria", a2 / "resultado_auditoria.json", "--ajustes-evidencias", ajustes_evidencias,
            "--avaliacao-final", pareceres_comentarios, "--ajustes-comentarios", ajustes_comentarios,
            "--impactos", impactos_comentarios_xlsx, "--output-dir", stats_dir,
        ), inputs=(
            respostas_comentarios, comentarios_lss, a2 / "resultado_auditoria.json", ajustes_evidencias,
            pareceres_comentarios, ajustes_comentarios, impactos_comentarios_xlsx,
        ), outputs=(stats_dir / "dados/resumo-execucao.json",),
    ))
    if not args.skip_graficos:
        stages.append(Stage(
            "23-graficos-finais", "Gerando gráficos finais", cmd(
                SCRIPTS / "gerar_graficos_relatorios_consolidado_individuais_igovti.py",
                "--output-root", graficos_03, "--resultados-2026", igovti_outputs(i3, prefixo_atual)[0],
                "--respostas-2026", r3, "--comparavel-2026", igovti_outputs(i3, prefixo_atual)[1],
                "--mapa", args.mapa,
                "--jobs", args.graficos_jobs, "--dpi", args.graficos_dpi,
            ), inputs=(igovti_outputs(i3, prefixo_atual)[0], r3, igovti_outputs(i3, prefixo_atual)[1], args.mapa),
            outputs=(), scenario="03-pos-comentarios-gestor",
            metadata={"output_dirs": [str(graficos_03 / "relatorios-individuais/img"), str(graficos_03 / "relatorio-consolidado/img")]},
        ))
    stages.append(Stage(
        "23b-diagnostico-transversal", "Consolidando o diagnóstico transversal do iGovTI 2026", cmd(
            SCRIPTS / "gerar_diagnostico_transversal_igovti.py",
            "--respostas", r3, "--resultados", igovti_outputs(i3, prefixo_atual)[0],
            "--auditados", args.auditados, "--questionario", args.questionario,
            "--output-json", diagnostico_json, "--output-xlsx", diagnostico_xlsx,
        ), inputs=(r3, igovti_outputs(i3, prefixo_atual)[0], args.auditados, args.questionario,
                   ROOT / "01-Planejamento/02-Metodologia_iGovTI/estrutura-igovti-2026.yaml"),
        outputs=(diagnostico_json, diagnostico_xlsx), scenario="03-pos-comentarios-gestor",
    ))
    if not args.skip_relatorios:
        final_cmd = list(cmd(
            SCRIPTS / "gerar_relatorios_individuais.py", "--auditados", a3 / "resultado_auditoria.json",
            "--templates", args.template_final, "--context-files", igovti_outputs(i3, prefixo_atual)[2],
            "--ajustes-respostas", ajustes_comentarios, "--contexto-comentarios-gestor", contexto_comentarios,
            "--impactos-comentarios-gestor", impactos_comentarios_json, "--resource-files",
            str(graficos_03 / "relatorios-individuais/img/**/*"), DEFAULT_INFOGRAFICO,
            "--output-dir", relatorios_final, "--reference-docx", args.reference_docx,
            "--nome-base-docx", "Relatório Individual",
        ))
        if args.auditados_select:
            final_cmd.extend(["--auditados-select", *args.auditados_select])
        stages.append(Stage(
            "24-relatorios-finais", "Gerando relatórios individuais finais", tuple(final_cmd),
            inputs=(a3 / "resultado_auditoria.json", args.template_final, igovti_outputs(i3, prefixo_atual)[2],
                    contexto_comentarios, impactos_comentarios_json), outputs=(), scenario="03-pos-comentarios-gestor",
            metadata={"output_dirs": [str(relatorios_final)]},
        ))
    if not args.skip_relatorio_consolidado:
        consolidado_docx = root / "03-Relatorios/01-Relatorio_Consolidado/gerados" / args.relatorio_consolidado_md.with_suffix(".docx").name
        stages.append(Stage(
            "25-relatorio-consolidado", "Gerando relatório consolidado final", cmd(
                SCRIPTS / "gerar_relatorio_consolidado.py", "--input", args.relatorio_consolidado_md,
                "--output", consolidado_docx, "--reference-docx", args.reference_docx_consolidado,
                "--modelo-institucional", args.modelo_institucional_consolidado,
                "--context-json", diagnostico_json,
                "--resource-files", root / "03-Relatorios/01-Relatorio_Consolidado/img",
                graficos_03 / "relatorio-consolidado/img", root / "03-Relatorios/99-Avaliacao_IgovTi_Achados/img",
                "--resultados-2026", igovti_outputs(i3, prefixo_atual)[0], "--respostas-2026", r3,
                "--comparavel-2026", igovti_outputs(i3, prefixo_atual)[1], "--auditados-xlsx", args.auditados,
                "--resultado-auditoria-json", a3 / "resultado_auditoria.json", "--mapa", args.mapa,
            ), inputs=(args.relatorio_consolidado_md, diagnostico_json, igovti_outputs(i3, prefixo_atual)[0], r3,
                       igovti_outputs(i3, prefixo_atual)[1], args.auditados, a3 / "resultado_auditoria.json",
                       args.mapa, args.modelo_institucional_consolidado),
            outputs=(consolidado_docx,), scenario="03-pos-comentarios-gestor",
        ))
    required_final = [
        r1, r2, r3,
        *igovti_outputs(i1, prefixo), *igovti_outputs(i2, prefixo), *igovti_outputs(i3, prefixo_atual),
        a1 / "resultado_auditoria.json", a2 / "resultado_auditoria.json", a3 / "resultado_auditoria.json",
        ajustes_evidencias, painel_evidencias, ajustes_comentarios, painel_comentarios,
        pareceres_comentarios, contexto_comentarios, impactos_comentarios_json, impactos_comentarios_xlsx,
        diagnostico_json, diagnostico_xlsx,
    ]
    report_dirs: list[Path] = [] if args.skip_relatorios else [relatorios_pre, relatorios_final]
    validation_output = root / "02-Execucao/00-Controle_Execucao/validacao-final.json"
    validation_cmd = list(cmd(
        SCRIPTS / "validar_produtos_pipeline.py", "--required", *required_final,
        "--logs-dir", root / "02-Execucao/00-Controle_Execucao/logs", "--output", validation_output,
        "--auditados-json", a3 / "resultado_auditoria.json",
    ))
    for directory in report_dirs:
        validation_cmd.extend(["--report-dir", str(directory)])
    stages.append(Stage(
        "26-validacao-final", "Validando produtos e recursos finais", tuple(validation_cmd),
        inputs=tuple(required_final), outputs=(validation_output,),
    ))
    return stages


def select_stages(stages: list[Stage], first: str | None, last: str | None) -> list[Stage]:
    keys = [stage.key for stage in stages]
    if first and first not in keys:
        raise ValueError(f"--from-stage desconhecida: {first}. Opções: {', '.join(keys)}")
    if last and last not in keys:
        raise ValueError(f"--until-stage desconhecida: {last}. Opções: {', '.join(keys)}")
    start = keys.index(first) if first else 0
    end = keys.index(last) + 1 if last else len(stages)
    if start >= end:
        raise ValueError("--from-stage deve anteceder --until-stage")
    return stages[start:end]


def main() -> int:
    args = build_parser().parse_args()
    logging.basicConfig(level=getattr(logging, args.log_level), format="%(asctime)s - %(levelname)s - %(message)s")
    args.output_root = args.output_root.expanduser().resolve()
    control = args.output_root / "02-Execucao/00-Controle_Execucao"
    if args.dry_run:
        with tempfile.TemporaryDirectory(prefix="igovti-pipeline-dry-") as temp:
            manifest = Manifest(Path(temp) / "controle")
            stages = select_stages(build_stages(args), args.from_stage, args.until_stage)
            runner = PipelineRunner(manifest, dry_run=True)
            for stage in stages:
                runner.run(stage)
        return 0
    if args.status_only and not (control / "manifesto-pipeline-auditoria.json").is_file():
        print(json.dumps({"status": "not_started", "manifest": str(control / "manifesto-pipeline-auditoria.json")}, ensure_ascii=False, indent=2))
        return 0
    manifest = Manifest(control)
    if args.status_only:
        print(json.dumps(manifest.data, ensure_ascii=False, indent=2))
        return 0
    stages = select_stages(build_stages(args), args.from_stage, args.until_stage)
    manifest.data["configuration"] = {
        "output_root": str(args.output_root),
        "prefixo": args.prefixo or infer_prefixo(args.respostas_bruto),
        "stages": [stage.key for stage in stages],
    }
    manifest.save()
    stage_keys = {stage.key for stage in build_stages(args)}
    force_stages = set(args.force_stage)
    desconhecidas = sorted(force_stages - stage_keys)
    if desconhecidas:
        raise ValueError("--force-stage desconhecida: " + ", ".join(desconhecidas))
    runner = PipelineRunner(manifest, adopt_existing=args.adopt_existing, force=force_stages)
    for stage in stages:
        result = runner.run(stage)
        if result == "awaiting_input":
            logging.warning("Pipeline aguardando comentários do gestor. Consulte %s", manifest.path)
            return 2
        if result == "awaiting_review":
            logging.warning("Pipeline aguardando revisão humana dos pareceres prioritários. Consulte %s", manifest.path)
            return 3
    if stages and stages[-1].key == build_stages(args)[-1].key:
        manifest.complete()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
