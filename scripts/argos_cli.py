#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Argos CLI: orquestrador interativo das rotinas do projeto iGovTI."""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Iterable

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table
from rich.text import Text


ROOT = Path(__file__).resolve().parents[1]
PYTHON = Path(sys.executable)
TMP_ROOT = Path(tempfile.gettempdir())
OUTPUT_ROOT = ROOT
OUTPUT_LATEST = ROOT
STATE_DIR = ROOT / ".argos-cli"
STATE_FILE = STATE_DIR / "state.json"
LOG_DIR = STATE_DIR / "logs"
DEFAULT_DOCX_WORKERS = max(1, min(8, os.cpu_count() or 1))

console = Console()

LOG_LINE_RE = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} - (DEBUG|INFO|WARNING|ERROR|CRITICAL) - .+")
ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")


def log_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]


def strip_ansi(value: str) -> str:
    return ANSI_RE.sub("", value).replace("\r", "").rstrip("\n")


def infer_log_level(message: str, *, returncode: int | None = None) -> str:
    lowered = message.lower()
    if returncode is not None and returncode != 0:
        return "ERROR"
    if any(token in lowered for token in ["traceback", "exception", "erro", "error", "falha", "failed"]):
        return "ERROR"
    if any(token in lowered for token in ["warning", "aviso", "deprecationwarning"]):
        return "WARNING"
    if "debug" in lowered:
        return "DEBUG"
    return "INFO"


def format_log_message(message: str, *, level: str | None = None, returncode: int | None = None) -> str:
    cleaned = strip_ansi(message)
    if LOG_LINE_RE.match(cleaned):
        return cleaned
    resolved_level = level or infer_log_level(cleaned, returncode=returncode)
    return f"{log_timestamp()} - {resolved_level} - {cleaned}"


def emit_log(log_file, message: str, *, level: str | None = None, returncode: int | None = None) -> None:
    formatted = format_log_message(message, level=level, returncode=returncode)
    print(formatted, flush=True)
    log_file.write(formatted + "\n")
    log_file.flush()


@dataclass(frozen=True)
class Param:
    name: str
    flag: str
    default: str | bool
    help: str
    is_bool: bool = False
    is_list: bool = False
    repeat_flag: bool = False


@dataclass(frozen=True)
class Routine:
    key: str
    name: str
    description: str
    script: Path
    params: list[Param] = field(default_factory=list)
    positional: list[str] = field(default_factory=list)
    fixed_args: list[str] = field(default_factory=list)
    group: str = "Geral"
    scenarios: tuple[str, ...] = ()


def p(path: str | Path) -> str:
    return str(path)


ROUTINES: list[Routine] = [
    Routine(
        key="ajustar-respostas",
        name="Ajustar respostas",
        description="Aplica ajustes registrados sobre a base de respostas do questionario.",
        script=ROOT / "scripts/ajustar_respostas_questionario.py",
        params=[
            Param(
                "respostas",
                "--respostas",
                "02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario-01-pos-ajuste-inicial.xlsx",
                "Planilha de respostas original.",
            ),
            Param(
                "ajustes",
                "--ajustes",
                "02-Execucao/01-Questionario/02-Ajustes_Respostas/ajustes_respostas_questionario_pos_avaliacao_evidencias.xlsx",
                "Planilha de ajustes.",
            ),
            Param(
                "output",
                "--output",
                p(OUTPUT_ROOT / "02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario-02-pos-avaliacao-evidencias.xlsx"),
                "Planilha ajustada de saida.",
            ),
        ],
        group="Questionário e respostas",
        scenarios=("01-pos-ajuste-inicial", "02-pos-avaliacao-evidencias", "03-pos-comentarios-gestor"),
    ),
    Routine(
        key="avaliar-evidencias",
        name="Avaliar evidencias",
        description="Executa os avaliadores paralelos configurados para evidencias.",
        script=ROOT / "scripts/run_avaliacao_evidencias_v2.py",
        params=[
            Param("evidencias", "--evidencias", p(OUTPUT_ROOT / "evidencias_extraidas"), "Diretorio raiz das evidencias extraidas."),
            Param("respostas", "--respostas", "02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario-01-pos-ajuste-inicial.xlsx", "Base do cenário 01."),
            Param("out_dir", "--out-dir", "02-Execucao/03-Execucao_Procedimentos/99-Avaliacao_Evidencias/individuais", "Diretório dos checkpoints."),
            Param("models_config", "--models-config", "", "Configuração JSON opcional dos avaliadores."),
            Param("only_achados", "--only-achados", True, "Processa apenas itens que geram achados.", is_bool=True),
        ],
        group="Avaliação de evidências",
    ),
    Routine(
        key="consolidar-avaliacoes",
        name="Consolidar avaliacoes",
        description="Executa os juizes configurados para consolidar avaliacoes de evidencias.",
        script=ROOT / "scripts/run_consolida_avaliacoes_v2.py",
        params=[
            Param("evidencias", "--evidencias", p(OUTPUT_ROOT / "evidencias_extraidas"), "Diretorio raiz das evidencias extraidas."),
            Param("analyses_glob", "--analyses-glob", "02-Execucao/03-Execucao_Procedimentos/99-Avaliacao_Evidencias/individuais/analyses_clean*.jsonl", "Glob das avaliações individuais."),
            Param("out_dir", "--out-dir", "02-Execucao/03-Execucao_Procedimentos/99-Avaliacao_Evidencias/consolidado", "Diretório da consolidação."),
            Param("judges_config", "--judges-config", "", "Configuração JSON opcional dos juízes."),
            Param("min_opinions", "--min-opinions", "3", "Quórum mínimo de avaliações válidas."),
            Param("only_achados", "--only-achados", True, "Consolida apenas itens que geram achados.", is_bool=True),
        ],
        group="Avaliação de evidências",
    ),
    Routine(
        key="calcular-igovti",
        name="Calcular iGovTI",
        description="Gera resultados, comparacao longitudinal e contexto estatistico do iGovTI.",
        script=ROOT / "scripts/gerar_artefatos_igovti.py",
        params=[
            Param("respostas", "--respostas", "02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario-02-pos-avaliacao-evidencias.xlsx", "Planilha de respostas."),
            Param("prefixo", "--prefixo", "20260621", "Prefixo AAAAMMDD dos artefatos."),
            Param("output_dir", "--output-dir", p(OUTPUT_ROOT / "02-Execucao"), "Diretorio base dos artefatos."),
            Param("resultados_dir", "--resultados-dir", "", "Diretório explícito do cenário."),
            Param("comparacao_dir", "--comparacao-dir", "", "Diretório explícito da comparação longitudinal."),
        ],
        group="Cálculos e auditoria",
        scenarios=("01-pos-ajuste-inicial", "02-pos-avaliacao-evidencias", "03-pos-comentarios-gestor"),
    ),
    Routine(
        key="executar-auditoria",
        name="Executar auditoria",
        description="Executa procedimentos de auditoria e gera JSON/XLSX/anexos/relatorios de procedimentos.",
        script=ROOT / "scripts/executa_auditoria.py",
        params=[
            Param("auditados", "--auditados", "02-Execucao/03-Execucao_Procedimentos/01-Insumos/bd_auditados.xlsx", "Base de auditados."),
            Param("mapa", "--mapa", "02-Execucao/03-Execucao_Procedimentos/01-Insumos/mapa-verificacao-achados-pos-comentarios-gestor.xlsx", "Mapa de verificacao e achados."),
            Param(
                "matriz",
                "--matriz",
                "01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/matriz_planejamento-pos-comentarios-gestor.md",
                "Matriz de planejamento usada na validação Matriz × Mapa × Auditados.",
            ),
            Param(
                "fontes",
                "--fontes",
                f"{OUTPUT_ROOT}/02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario-02-pos-avaliacao-evidencias.xlsx "
                "02-Execucao/03-Execucao_Procedimentos/99-Avaliacao_Evidencias/painel-avaliacao-evidencias.xlsx",
                "Fontes de informacao separadas por espaco.",
                is_list=True,
            ),
            Param("fonte", "--fonte", "", "Mapeamentos ID=CAMINHO separados por espaço.", is_list=True, repeat_flag=True),
            Param("resultado", "--resultado-json", p(OUTPUT_ROOT / "02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/resultado_auditoria.json"), "JSON compacto de auditoria."),
            Param("resultado_detalhado", "--resultado-detalhado-json", "", "JSON detalhado opcional da auditoria."),
            Param("tabelas", "--tabelas-xlsx", p(OUTPUT_ROOT / "02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/tabelas_consolidadas_auditoria.xlsx"), "XLSX consolidado da auditoria."),
            Param("relatorios_procedimentos_zip", "--relatorios-procedimentos-zip", p(OUTPUT_ROOT / "02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/relatorios_procedimentos.zip"), "ZIP de relatorios de procedimentos."),
            Param("anexo_evidencias", "--anexo-evidencias-docx", p(OUTPUT_ROOT / "02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/anexo_evidencias.docx"), "DOCX do anexo de evidencias."),
            Param("jobs_relatorios_procedimentos", "--jobs-relatorios-procedimentos", str(DEFAULT_DOCX_WORKERS), "Workers para renderizar relatorios de procedimentos."),
            Param("somente_dados", "--somente-dados", False, "Gera apenas JSON/XLSX da auditoria.", is_bool=True),
            Param("skip_relatorios_procedimentos", "--skip-relatorios-procedimentos", False, "Nao gera relatorios de procedimentos.", is_bool=True),
            Param("skip_anexo_evidencias", "--skip-anexo-evidencias", False, "Nao gera o anexo de evidencias.", is_bool=True),
        ],
        group="Cálculos e auditoria",
        scenarios=("01-pos-ajuste-inicial", "02-pos-avaliacao-evidencias", "03-pos-comentarios-gestor"),
    ),
    Routine(
        key="gerar-comentarios-gestor",
        name="Gerar comentarios do gestor",
        description="Gera LSS do LimeSurvey e ZIP de anexos DOCX a partir do resultado da auditoria.",
        script=ROOT / "scripts/gerar_comentarios_gestor.py",
        params=[
            Param("resultado_auditoria", "--resultado-auditoria-json", p(OUTPUT_ROOT / "02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/resultado_auditoria.json"), "Resultado da auditoria JSON."),
            Param("comentarios_gestor_lss", "--comentarios-gestor-lss", p(OUTPUT_ROOT / "02-Execucao/05-Comentarios_Gestor/questionario_comentarios_gestor.lss"), "LSS de comentarios do gestor."),
            Param("comentarios_gestor_anexos_zip", "--comentarios-gestor-anexos-zip", p(OUTPUT_ROOT / "02-Execucao/05-Comentarios_Gestor/anexos_docx_comentarios.zip"), "ZIP de anexos de comentarios."),
            Param("jobs_comentarios_gestor_anexos", "--jobs-comentarios-gestor-anexos", str(DEFAULT_DOCX_WORKERS), "Workers para renderizar anexos de comentarios."),
            Param("data_final", "--data-final-preenchimento-comentarios-gestor", "06/07/2026", "Data final dos comentarios do gestor."),
            Param("email", "--email-contato-comentarios-gestor", "auditoriati@tcerj.tc.br", "E-mail de contato."),
            Param("admin", "--admin-responsavel-comentarios-gestor", "CAD-TI", "Administrador responsavel pelos comentarios do gestor."),
            Param("numero", "--numero-fiscalizacao-comentarios-gestor", "18/2026", "Numero da fiscalizacao."),
            Param("nome", "--nome-fiscalizacao-comentarios-gestor", "iGovTI 2026", "Nome da fiscalizacao."),
            Param("ajustes_evidencias", "--ajustes-evidencias-comentarios-gestor", "", "Planilha de ajustes de evidencias para reavaliacao."),
            Param("skip_comentarios_gestor_lss", "--skip-comentarios-gestor-lss", False, "Nao gera o LSS de comentarios.", is_bool=True),
            Param("skip_comentarios_gestor_anexos", "--skip-comentarios-gestor-anexos", False, "Nao gera anexos de comentarios.", is_bool=True),
        ],
    ),
    Routine(
        key="gerar-graficos",
        name="Gerar graficos",
        description="Gera graficos consolidados e individuais para os relatorios.",
        script=ROOT / "scripts/gerar_graficos_relatorios_consolidado_individuais_igovti.py",
        params=[
            Param("output_root", "--output-root", p(OUTPUT_ROOT), "Raiz dos artefatos."),
            Param("resultados_2026", "--resultados-2026", p(OUTPUT_ROOT / "02-Execucao/01-Questionario/04-Resultados_iGovTI/20260621-iGovTI-2026.xlsx"), "Resultados oficiais 2026."),
            Param("respostas_2026", "--respostas-2026", p(OUTPUT_ROOT / "02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario-02-pos-avaliacao-evidencias.xlsx"), "Respostas 2026."),
            Param("comparavel_2026", "--comparavel-2026", p(OUTPUT_ROOT / "02-Execucao/01-Questionario/04-Resultados_iGovTI/20260621-iGovTI-2026-Ajustado-Comparavel.xlsx"), "Resultado comparavel 2026."),
            Param("jobs", "--jobs", "1", "Processos paralelos. Use 1 em sandbox."),
            Param("dpi", "--dpi", "300", "Resolucao dos PNG."),
            Param("skip_existing", "--skip-existing", False, "Pula PNG ja existentes.", is_bool=True),
        ],
        group="Cálculos e auditoria",
    ),
    Routine(
        key="gerar-relatorios-individuais",
        name="Gerar relatorios individuais",
        description="Gera os DOCX individuais a partir do resultado da auditoria e do contexto iGovTI.",
        script=ROOT / "scripts/gerar_relatorios_individuais.py",
        params=[
            Param("auditados", "--auditados", p(OUTPUT_ROOT / "02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/resultado_auditoria.json"), "Resultado da auditoria JSON."),
            Param("templates", "--templates", "03-Relatorios/02-Relatorios_Individuais_Preliminares/relatorio-individual-preliminar-template.md", "Template(s) Markdown.", is_list=True),
            Param("context_files", "--context-files", p(OUTPUT_ROOT / "02-Execucao/01-Questionario/04-Resultados_iGovTI/20260621-contexto-relatorios-igovti-2026.xlsx"), "Planilhas de contexto.", is_list=True),
            Param("ajustes", "--ajustes-respostas", "02-Execucao/01-Questionario/02-Ajustes_Respostas/ajustes_respostas_questionario_pos_avaliacao_evidencias.xlsx", "Planilha de ajustes para Apendice B."),
            Param(
                "resources",
                "--resource-files",
                f"{OUTPUT_ROOT}/relatorios-individuais/img/**/* 03-Relatorios/02-Relatorios_Individuais_Preliminares/img/igovti_2026_composicao_infografico.png",
                "Recursos e imagens separados por espaco.",
                is_list=True,
            ),
            Param("output_dir", "--output-dir", p(OUTPUT_ROOT / "relatorios-individuais"), "Diretorio de saida."),
            Param("reference", "--reference-docx", "scripts/resources/template-base-estilos-sigiloso.docx", "DOCX de referencia."),
            Param("nome_base", "--nome-base-docx", "Relatório Individual Preliminar", "Nome base dos DOCX."),
        ],
        group="Relatórios",
        scenarios=("02-pos-avaliacao-evidencias",),
    ),
    Routine(
        key="gerar-relatorio-consolidado",
        name="Gerar relatorio consolidado",
        description="Converte o Markdown consolidado para DOCX com contexto, graficos e estilos.",
        script=ROOT / "scripts/gerar_relatorio_consolidado.py",
        params=[
            Param("input", "--input", "03-Relatorios/01-Relatorio_Consolidado/Relatório_altaresolucao_novo.md", "Markdown consolidado."),
            Param("output", "--output", p(OUTPUT_ROOT / "validacao/Relatório_altaresolucao_novo.docx"), "DOCX de saida."),
            Param("reference", "--reference-docx", "scripts/resources/template-base-estilos.docx", "DOCX de referencia."),
            Param(
                "resources",
                "--resource-files",
                "03-Relatorios/01-Relatorio_Consolidado/img "
                "relatorio-consolidado/img "
                "03-Relatorios/99-Avaliacao_IgovTi_Achados/img",
                "Recursos graficos.",
                is_list=True,
            ),
            Param("resultados_2026", "--resultados-2026", "02-Execucao/01-Questionario/04-Resultados_iGovTI/20260621-iGovTI-2026.xlsx", "Resultados iGovTI 2026."),
            Param("respostas_2026", "--respostas-2026", "02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario-02-pos-avaliacao-evidencias.xlsx", "Respostas 2026."),
            Param("comparavel_2026", "--comparavel-2026", "02-Execucao/01-Questionario/04-Resultados_iGovTI/20260621-iGovTI-2026-Ajustado-Comparavel.xlsx", "Comparavel 2026."),
            Param("setic_2023", "--setic-2023", "02-Execucao/02-Questionario iGovTI 2023/iGovTI-2023-SETIC-Ajustado-Comparavel.xlsx", "Comparavel SETIC 2023."),
            Param("municipios_2023", "--municipios-2023", "02-Execucao/02-Questionario iGovTI 2023/iGovTI-2023-Municipios-Ajustado-Comparavel.xlsx", "Comparavel municipios 2023."),
            Param("auditados_xlsx", "--auditados-xlsx", "02-Execucao/03-Execucao_Procedimentos/01-Insumos/bd_auditados.xlsx", "Base de auditados."),
            Param("resultado_auditoria", "--resultado-auditoria-json", "02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/resultado_auditoria.json", "Resultado da auditoria JSON."),
        ],
        group="Relatórios",
        scenarios=("03-pos-comentarios-gestor",),
    ),
    Routine(
        key="converter-md-docx",
        name="Converter Markdown para DOCX",
        description="Converte arquivos Markdown para DOCX usando o template de estilos do Argos.",
        script=ROOT / "scripts/converter_markdown_para_docx.py",
        params=[
            Param("input", "--input", "README.md", "Arquivo Markdown de entrada."),
            Param("output_dir", "--output-dir", p(OUTPUT_ROOT / "conversoes-docx"), "Diretorio de saida quando --output nao for informado."),
            Param("output", "--output", "", "Arquivo DOCX de saida opcional para conversao de arquivo unico."),
            Param("reference", "--reference-docx", "scripts/resources/template-base-estilos-sigiloso.docx", "DOCX de referencia."),
            Param("resources", "--resource-files", "", "Arquivos, diretorios ou globs de imagens usados pelo Markdown.", is_list=True),
        ],
        group="Utilitários",
    ),
    Routine(
        key="execucao-completa",
        name="Execucao completa",
        description="Executa ou retoma todas as etapas rastreáveis da auditoria.",
        script=ROOT / "scripts/gerar_pacote_relatorios_igovti.py",
        params=[
            Param("respostas_bruto", "--respostas-bruto", "02-Execucao/01-Questionario/01-Coleta_LimeSurvey/20260621-respostas-questionario-bruto.xlsx", "Exportacao bruta LimeSurvey."),
            Param("output_root", "--output-root", p(OUTPUT_LATEST), "Raiz dos papéis de trabalho."),
            Param("evidencias_root", "--evidencias-root", "02-Execucao/01-Questionario/01-Coleta_LimeSurvey/Evidencias_Coletadas/evidencias_extraidas", "Evidências extraídas do questionário."),
            Param("avaliadores_config", "--avaliadores-config", "", "JSON opcional dos avaliadores de evidências."),
            Param("juizes_config", "--juizes-config", "", "JSON opcional dos juízes de evidências."),
            Param("respostas_comentarios", "--respostas-comentarios", "", "XLSX opcional dos comentários; sem ele o fluxo aguarda após o survey."),
            Param("evidencias_comentarios", "--evidencias-comentarios-root", "", "Diretório opcional das evidências dos comentários."),
            Param("data_referencia", "--data-referencia-comentarios", "18/07/2026", "Data da posição pós-comentários."),
            Param("revisoes", "--revisoes-pareceres", "02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor/revisoes_pareceres.yml", "YAML declarativo de revisões institucionais."),
            Param("from_stage", "--from-stage", "", "Primeira etapa a executar."),
            Param("until_stage", "--until-stage", "", "Última etapa a executar."),
            Param("graficos_jobs", "--graficos-jobs", "8", "Processos paralelos para graficos."),
            Param("auditoria_jobs_relatorios_procedimentos", "--auditoria-jobs-relatorios-procedimentos", str(DEFAULT_DOCX_WORKERS), "Workers para relatorios de procedimentos na auditoria."),
            Param("auditoria_jobs_comentarios_gestor_anexos", "--auditoria-jobs-comentarios-gestor-anexos", str(DEFAULT_DOCX_WORKERS), "Workers para anexos de comentarios."),
            Param("data_final", "--data-final-preenchimento-comentarios-gestor", "06/07/2026", "Data final dos comentarios do gestor."),
            Param("email", "--email-contato-comentarios-gestor", "auditoriati@tcerj.tc.br", "E-mail de contato."),
            Param("numero", "--numero-fiscalizacao-comentarios-gestor", "18/2026", "Numero da fiscalizacao."),
            Param("nome", "--nome-fiscalizacao-comentarios-gestor", "iGovTI 2026", "Nome da fiscalizacao."),
            Param(
                "ajustes_evidencias_comentarios_gestor",
                "--ajustes-evidencias-comentarios-gestor",
                "02-Execucao/01-Questionario/02-Ajustes_Respostas/ajustes_respostas_questionario_pos_avaliacao_evidencias.xlsx",
                "Planilha de ajustes de evidencias para gerar a secao de reavaliacao nos comentarios do gestor.",
            ),
            Param("skip_existing", "--graficos-skip-existing", False, "Pula graficos existentes.", is_bool=True),
            Param("skip_relatorios_procedimentos", "--skip-relatorios-procedimentos", False, "Pula o ZIP de relatorios de procedimentos.", is_bool=True),
            Param("dry_run", "--dry-run", False, "Exibe todas as etapas sem executá-las.", is_bool=True),
            Param("adopt_existing", "--adopt-existing", False, "Adota produtos legados sem sobrescrevê-los.", is_bool=True),
        ],
        group="Execução integrada",
    ),
    Routine(
        key="status-pipeline",
        name="Status do pipeline",
        description="Exibe o manifesto e as etapas concluídas ou pendentes.",
        script=ROOT / "scripts/gerar_pacote_relatorios_igovti.py",
        fixed_args=["--status-only"],
        params=[Param("output_root", "--output-root", p(ROOT), "Raiz dos papéis de trabalho.")],
        group="Execução integrada",
    ),
    Routine(
        key="validar-pipeline",
        name="Validar pipeline",
        description="Monta e valida estruturalmente todas as etapas sem executá-las.",
        script=ROOT / "scripts/gerar_pacote_relatorios_igovti.py",
        fixed_args=["--dry-run"],
        params=[
            Param("respostas_bruto", "--respostas-bruto", "02-Execucao/01-Questionario/01-Coleta_LimeSurvey/20260621-respostas-questionario-bruto.xlsx", "Exportação bruta."),
            Param("output_root", "--output-root", p(ROOT), "Raiz dos papéis de trabalho."),
        ],
        group="Execução integrada",
    ),
    Routine(
        key="gerar-ajustes-evidencias",
        name="Gerar ajustes pós-evidências",
        description="Converte pareceres consolidados em minuta de ajustes.",
        script=ROOT / "scripts/gerar_ajustes_pos_avaliacao_evidencias.py",
        params=[
            Param("pareceres", "--pareceres", "02-Execucao/03-Execucao_Procedimentos/99-Avaliacao_Evidencias/consolidado/pareceres_consolidados.xlsx", "Pareceres consolidados."),
            Param("output", "--output", "02-Execucao/03-Execucao_Procedimentos/99-Avaliacao_Evidencias/ajustes_respostas_questionario_pos_avaliacao_evidencias.xlsx", "Minuta XLSX."),
        ],
        group="Avaliação de evidências",
    ),
    Routine(
        key="gerar-painel-evidencias",
        name="Gerar painel de evidências",
        description="Gera a fonte larga usada pela auditoria.",
        script=ROOT / "scripts/gerar_fonte_ajustes_evidencias_auditoria.py",
        params=[
            Param("ajustes", "--ajustes", "02-Execucao/03-Execucao_Procedimentos/99-Avaliacao_Evidencias/ajustes_respostas_questionario_pos_avaliacao_evidencias.xlsx", "Minuta revisada de ajustes."),
            Param("mapa", "--mapa", "02-Execucao/03-Execucao_Procedimentos/01-Insumos/mapa-verificacao-achados-pos-comentarios-gestor.xlsx", "Mapa de auditoria."),
            Param("output", "--output", "02-Execucao/03-Execucao_Procedimentos/99-Avaliacao_Evidencias/painel-avaliacao-evidencias.xlsx", "Painel de saída."),
        ],
        group="Avaliação de evidências",
    ),
    Routine(
        key="calcular-estatisticas-comentarios",
        name="Calcular estatísticas dos comentários",
        description="Gera memória, resumo e gráficos da participação dos gestores.",
        script=ROOT / "03-Relatorios/99-Avaliacao_Comentarios_Gestor/calcular_dados_comentarios_gestor.py",
        params=[
            Param("respostas", "--respostas", "02-Execucao/05-Comentarios_Gestor/01-Coleta_LimeSurvey/20260716-respostas-bruto.xlsx", "Respostas do survey."),
            Param("output_dir", "--output-dir", "03-Relatorios/99-Avaliacao_Comentarios_Gestor", "Diretório dos produtos."),
        ],
        group="Comentários do gestor",
    ),
    Routine(
        key="gerar-produtos-pos-comentarios",
        name="Gerar produtos pós-comentários",
        description="Gera somente a base ajustada, pareceres e contexto dos relatórios.",
        script=ROOT / "scripts/gerar_produtos_pos_comentarios_gestor.py",
        params=[
            Param("data_referencia", "--data-referencia", "18/07/2026", "Data da posição corrente."),
            Param("respostas_base", "--respostas-base", "02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario-02-pos-avaliacao-evidencias.xlsx", "Base do cenário 02."),
            Param("respostas_comentarios", "--respostas-comentarios", "02-Execucao/05-Comentarios_Gestor/01-Coleta_LimeSurvey/20260716-respostas-bruto.xlsx", "Respostas dos comentários."),
            Param("avaliacao_dir", "--avaliacao-comentarios-dir", "02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor", "Avaliações consolidadas."),
            Param("revisoes", "--revisoes-pareceres", "02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor/revisoes_pareceres.yml", "YAML opcional de revisões."),
            Param("output_root", "--output-root", p(ROOT), "Raiz dos produtos."),
        ],
        group="Comentários do gestor",
    ),
    Routine(
        key="calcular-impacto-comentarios",
        name="Calcular impacto dos comentários",
        description="Compara auditoria e iGovTI dos cenários 02 e 03.",
        script=ROOT / "scripts/calcular_impactos_comentarios_gestor.py",
        params=[
            Param("auditoria_anterior", "--auditoria-anterior", "02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/02-pos-avaliacao-evidencias/resultado_auditoria.json", "Auditoria do cenário 02."),
            Param("auditoria_atual", "--auditoria-atual", "02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/03-pos-comentarios-gestor/resultado_auditoria.json", "Auditoria do cenário 03."),
            Param("contexto_anterior", "--contexto-igovti-anterior", "02-Execucao/01-Questionario/04-Resultados_iGovTI/02-pos-avaliacao-evidencias/20260621-contexto-relatorios-igovti-2026.xlsx", "Contexto do cenário 02."),
            Param("contexto_atual", "--contexto-igovti-atual", "02-Execucao/01-Questionario/04-Resultados_iGovTI/03-pos-comentarios-gestor/20260621-contexto-relatorios-igovti-2026.xlsx", "Contexto do cenário 03."),
            Param("output_json", "--output-json", "02-Execucao/05-Comentarios_Gestor/03-Produtos_Pos_Comentarios/impactos-comentarios-gestor.json", "Impactos JSON."),
            Param("output_xlsx", "--output-xlsx", "02-Execucao/05-Comentarios_Gestor/03-Produtos_Pos_Comentarios/impactos-comentarios-gestor.xlsx", "Impactos XLSX."),
        ],
        group="Comentários do gestor",
    ),
    Routine(
        key="calcular-impacto-evidencias",
        name="Calcular impacto das evidências",
        description="Compara respostas, iGovTI e auditoria dos cenários 01 e 02.",
        script=ROOT / "03-Relatorios/99-Impacto_Avaliacao_Evidencias/atualizar_dados_impacto_avaliacao_evidencias.py",
        params=[
            Param("igovti_pre", "--igovti-pre", "02-Execucao/01-Questionario/04-Resultados_iGovTI/01-pos-ajuste-inicial/20260621-iGovTI-2026.xlsx", "iGovTI do cenário 01."),
            Param("igovti_final", "--igovti-final", "02-Execucao/01-Questionario/04-Resultados_iGovTI/02-pos-avaliacao-evidencias/20260621-iGovTI-2026.xlsx", "iGovTI do cenário 02."),
            Param("auditoria_pre", "--auditoria-pre", "02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/01-pos-ajuste-inicial/resultado_auditoria.json", "Auditoria do cenário 01."),
            Param("auditoria_final", "--auditoria-final", "02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/02-pos-avaliacao-evidencias/resultado_auditoria.json", "Auditoria do cenário 02."),
            Param("output", "--output", "03-Relatorios/99-Impacto_Avaliacao_Evidencias/dados_impacto_avaliacao_evidencias.xlsx", "Memória de impacto."),
        ],
        group="Avaliação de evidências",
    ),
    Routine(
        key="gerar-relatorios-individuais-finais",
        name="Gerar relatórios individuais finais",
        description="Gera os DOCX finais com comentários e impactos separados.",
        script=ROOT / "scripts/gerar_relatorios_individuais.py",
        params=[
            Param("auditados", "--auditados", "02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/03-pos-comentarios-gestor/resultado_auditoria.json", "Auditoria do cenário 03."),
            Param("templates", "--templates", "03-Relatorios/03-Relatorios_Individuais_Finais/relatorio-individual-template.md", "Template final.", is_list=True),
            Param("context_files", "--context-files", "02-Execucao/01-Questionario/04-Resultados_iGovTI/03-pos-comentarios-gestor/20260621-contexto-relatorios-igovti-2026.xlsx", "Contexto iGovTI.", is_list=True),
            Param("ajustes", "--ajustes-respostas", "02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor/ajustes_respostas_questionario_pos_comentarios_gestor.xlsx", "Ajustes aplicados no cenário 03."),
            Param("contexto_comentarios", "--contexto-comentarios-gestor", "02-Execucao/05-Comentarios_Gestor/03-Produtos_Pos_Comentarios/contexto-relatorios-comentarios-gestor.json", "Contexto dos comentários."),
            Param("impactos", "--impactos-comentarios-gestor", "02-Execucao/05-Comentarios_Gestor/03-Produtos_Pos_Comentarios/impactos-comentarios-gestor.json", "Impactos dos comentários."),
            Param("resources", "--resource-files", "relatorios-individuais/img/**/* 03-Relatorios/02-Relatorios_Individuais_Preliminares/img/igovti_2026_composicao_infografico.png", "Recursos gráficos.", is_list=True),
            Param("output_dir", "--output-dir", "03-Relatorios/03-Relatorios_Individuais_Finais/gerados", "Diretório de saída."),
            Param("reference", "--reference-docx", "scripts/resources/template-base-estilos-sigiloso.docx", "DOCX de referência."),
            Param("nome_base", "--nome-base-docx", "Relatório Individual", "Nome base dos DOCX."),
        ],
        group="Relatórios",
        scenarios=("03-pos-comentarios-gestor",),
    ),
    Routine(
        key="exportar-respostas-comentarios-pdf",
        name="Exportar respostas dos comentários em PDF",
        description="Baixa os PDFs dinâmicos do LimeSurvey para preservação como fonte.",
        script=ROOT / "scripts/exportar_respostas_comentarios_gestor_pdf.py",
        params=[
            Param("lss", "--lss", "02-Execucao/05-Comentarios_Gestor/questionario_comentarios_gestor.lss", "Survey LSS."),
            Param("participantes", "--participantes", "02-Execucao/05-Comentarios_Gestor/01-Coleta_LimeSurvey/20260716-respostas-bruto.xlsx", "Exportação de participantes."),
            Param("output_dir", "--output-dir", "02-Execucao/05-Comentarios_Gestor/01-Coleta_LimeSurvey/PDF_Respostas", "Diretório dos PDFs."),
            Param("dry_run", "--dry-run", False, "Valida seleção sem acessar o LimeSurvey.", is_bool=True),
        ],
        group="Comentários do gestor",
    ),
]

_COMPLETE_ROUTINE = next(routine for routine in ROUTINES if routine.key == "execucao-completa")
ROUTINES.append(
    Routine(
        key="continuar-execucao",
        name="Continuar execução",
        description="Retoma a execução completa a partir da primeira etapa incompleta.",
        script=_COMPLETE_ROUTINE.script,
        params=_COMPLETE_ROUTINE.params,
        group="Execução integrada",
    )
)

COMMENTS_OUT = OUTPUT_ROOT / "02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor"
COMMENTS_INPUT = OUTPUT_ROOT / "02-Execucao/05-Comentarios_Gestor/01-Coleta_LimeSurvey/20260716-respostas-bruto.xlsx"
COMMENTS_EVIDENCE = OUTPUT_ROOT / "02-Execucao/05-Comentarios_Gestor/01-Coleta_LimeSurvey/Evidencias_Coletadas/evidencias_extraidas"
COMMENTS_MODELS_CONFIG = ROOT / "scripts/avaliacao_evidencias/configs/comentarios_gestor_models_v1.json"


def comments_params() -> list[Param]:
    return [
        Param("respostas_comentarios", "--respostas-comentarios", p(COMMENTS_INPUT), "Exportação XLSX do survey de comentários."),
        Param("evidencias_comentarios", "--evidencias-comentarios-root", p(COMMENTS_EVIDENCE), "Raiz dos anexos já extraídos por organização."),
        Param("lss", "--lss", "02-Execucao/05-Comentarios_Gestor/questionario_comentarios_gestor.lss", "LSS que originou o survey."),
        Param("resultado_auditoria", "--resultado-auditoria", "02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/resultado_auditoria.json", "Resultado compacto da auditoria."),
        Param("mapa", "--mapa", "02-Execucao/03-Execucao_Procedimentos/01-Insumos/mapa-verificacao-achados-pos-comentarios-gestor.xlsx", "Mapa de verificação e achados."),
        Param("ajustes", "--ajustes-pos-avaliacao-evidencias", "02-Execucao/01-Questionario/02-Ajustes_Respostas/ajustes_respostas_questionario_pos_avaliacao_evidencias.xlsx", "Avaliação consolidada anterior e itens elegíveis."),
        Param("respostas_base", "--respostas-questionario-base", "02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario-02-pos-avaliacao-evidencias.xlsx", "Base pós-avaliação de evidências sobre a qual serão propostos ajustes."),
        Param("painel_evidencias", "--painel-avaliacao-evidencias", "02-Execucao/03-Execucao_Procedimentos/99-Avaliacao_Evidencias/painel-avaliacao-evidencias.xlsx", "Painel de evidências que será saneado para a auditoria final."),
        Param("revisoes_respostas", "--revisoes-respostas", "02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor/revisoes_respostas.yml", "Decisões técnicas humanas, aprovadas e reprodutíveis, sobre valores de resposta."),
        Param("models_config", "--models-config", p(COMMENTS_MODELS_CONFIG), "JSON com avaliadores, juiz, quórum e paralelismo."),
        Param("out_dir", "--out-dir", p(COMMENTS_OUT), "Diretório temporário dos checkpoints e pareceres."),
        Param("auditados", "--auditados", "", "Filtro opcional de siglas separadas por vírgula."),
        Param("fake", "--fake", False, "Substitui os modelos configurados por providers fake.", is_bool=True),
        Param("preflight_only", "--preflight-only", False, "Valida entradas e anexos sem chamar modelos.", is_bool=True),
    ]


COMMENTS_ROUTINES = [
    Routine(
        key="avaliar-comentarios-gestor-secao-1",
        name="Avaliar seção 1",
        description="Avalia manifestações sobre situações inconformes com os modelos do JSON configurado.",
        script=ROOT / "scripts/run_comentarios_gestor.py",
        fixed_args=["avaliar", "--secao", "1"],
        params=comments_params(),
        group="Comentários do gestor",
    ),
    Routine(
        key="avaliar-comentarios-gestor-secao-2",
        name="Avaliar seção 2",
        description="Reavalia afirmações não conformes com comentários e novos anexos.",
        script=ROOT / "scripts/run_comentarios_gestor.py",
        fixed_args=["avaliar", "--secao", "2"],
        params=comments_params(),
        group="Comentários do gestor",
    ),
    Routine(
        key="consolidar-comentarios-gestor",
        name="Consolidar avaliações",
        description="Consolida as duas seções com o juiz e o quórum definidos no JSON.",
        script=ROOT / "scripts/run_comentarios_gestor.py",
        fixed_args=["consolidar", "--secao", "ambas"],
        params=comments_params(),
        group="Comentários do gestor",
    ),
    Routine(
        key="pipeline-comentarios-gestor",
        name="Executar pipeline completo",
        description="Executa preflight, avaliações configuradas, juiz e minuta de ajustes reversos.",
        script=ROOT / "scripts/run_comentarios_gestor.py",
        fixed_args=["completo"],
        params=comments_params(),
        group="Comentários do gestor",
    ),
    Routine(
        key="validar-integridade-comentarios-gestor",
        name="Validar integridade",
        description="Verifica escopo, motivos, coerência temporal e quórum; gera o manifesto de reparo.",
        script=ROOT / "scripts/run_comentarios_gestor.py",
        fixed_args=["validar-integridade"],
        params=comments_params(),
        group="Comentários do gestor",
    ),
    Routine(
        key="reparar-integridade-comentarios-gestor",
        name="Reparar casos afetados",
        description="Reavalia com os avaliadores habilitados e reconsolida somente os casos apontados no preflight.",
        script=ROOT / "scripts/run_comentarios_gestor.py",
        fixed_args=["reparar-integridade"],
        params=comments_params(),
        group="Comentários do gestor",
    ),
    Routine(
        key="gerar-ajustes-comentarios-gestor",
        name="Gerar ajustes combinados",
        description="Combina os saneamentos das seções 1 e 2 e gera a minuta e o painel de evidências final.",
        script=ROOT / "scripts/run_comentarios_gestor.py",
        fixed_args=["gerar-ajustes"],
        params=comments_params(),
        group="Comentários do gestor",
    ),
]

COMMENTS_GROUP = Routine(
    key="grupo-avaliacao-comentarios-gestor",
    name="Avaliação de comentários do gestor",
    description="Abre as rotinas das seções 1 e 2, consolidação, ajustes e pipeline completo.",
    script=ROOT / "scripts/run_comentarios_gestor.py",
)
HOME_ROUTINES = [*ROUTINES, COMMENTS_GROUP]
ALL_RUNNABLE_ROUTINES = [*ROUTINES, *COMMENTS_ROUTINES]
ROUTINE_BY_KEY = {routine.key: routine for routine in ALL_RUNNABLE_ROUTINES}


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def format_dt(value: str | None) -> str:
    if not value:
        return "-"
    try:
        return datetime.fromisoformat(value).strftime("%d/%m/%Y %H:%M:%S")
    except ValueError:
        return value


def load_state() -> dict:
    if not STATE_FILE.exists():
        return {"routines": {}}
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"routines": {}}


def save_state(state: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def duration_text(seconds: float | int | None) -> str:
    if seconds is None:
        return "-"
    seconds = int(seconds)
    minutes, sec = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}h {minutes:02d}min {sec:02d}s"
    if minutes:
        return f"{minutes}min {sec:02d}s"
    return f"{sec}s"


def read_key() -> str:
    """Read one navigation key from the terminal, supporting Windows and POSIX."""
    if os.name == "nt":
        import msvcrt

        ch = msvcrt.getwch()
        if ch in ("\x00", "\xe0"):
            code = msvcrt.getwch()
            return {"H": "up", "P": "down", "K": "left", "M": "right"}.get(code, "")
        return {
            "\r": "enter",
            "\n": "enter",
            "\x1b": "escape",
        }.get(ch, ch)

    import termios
    import tty

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == "\x1b":
            seq = sys.stdin.read(2)
            return {"[A": "up", "[B": "down", "[D": "left", "[C": "right"}.get(seq, "escape")
        return {
            "\r": "enter",
            "\n": "enter",
            "\x03": "ctrl-c",
            "\x04": "ctrl-d",
        }.get(ch, ch)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def ensure_interactive_tty() -> bool:
    if sys.stdin.isatty() and sys.stdout.isatty():
        return True
    console.print("[red]O modo interativo exige um terminal TTY.[/red]")
    console.print("[dim]Use --list para listar rotinas ou --run <rotina> para execucao nao interativa.[/dim]")
    return False


def selectable_loop(
    item_count: int,
    render: Callable[[int], None],
    *,
    initial_index: int = 0,
    extra_keys: set[str] | None = None,
) -> tuple[str, int]:
    selected = min(max(initial_index, 0), max(item_count - 1, 0))
    keys = extra_keys or set()
    while True:
        render(selected)
        key = read_key()
        menu_key = key.lower() if len(key) == 1 else key
        if menu_key == "up" and item_count:
            selected = (selected - 1) % item_count
        elif menu_key == "down" and item_count:
            selected = (selected + 1) % item_count
        elif menu_key in {"enter", "q", "escape", "ctrl-c", "ctrl-d"} or menu_key in keys:
            return menu_key, selected


def render_home(state: dict, selected_index: int) -> None:
    console.clear()
    console.print(
        Panel(
            Text.from_markup(
                "[bold cyan]Argos CLI[/bold cyan]\n"
                "Orquestrador local das rotinas iGovTI 2026\n"
                f"[dim]Raiz: {ROOT}[/dim]\n"
                f"[dim]Saida temporaria padrao: {OUTPUT_ROOT}[/dim]"
            ),
            box=box.ROUNDED,
            border_style="cyan",
        )
    )
    table = Table(box=box.SIMPLE_HEAVY, show_lines=False)
    table.add_column("", justify="center", no_wrap=True)
    table.add_column("Grupo", style="dim")
    table.add_column("Rotina", style="bold")
    table.add_column("Descricao")
    table.add_column("Status", justify="center")
    table.add_column("Ultima execucao")
    table.add_column("Duracao")
    for index, routine in enumerate(HOME_ROUTINES):
        if routine.key == COMMENTS_GROUP.key:
            children = [state.get("routines", {}).get(child.key, {}) for child in COMMENTS_ROUTINES]
            children = [item for item in children if item.get("finished_at")]
            data = max(children, key=lambda item: item.get("finished_at", ""), default={})
        else:
            data = state.get("routines", {}).get(routine.key, {})
        status = data.get("status")
        if status == "success":
            marker = "[green]✓[/green]"
        elif status == "partial":
            marker = "[yellow]![/yellow]"
        elif status in {"awaiting_input", "awaiting_review"}:
            marker = "[yellow]⏸[/yellow]"
        elif status == "failed":
            marker = "[red]✗[/red]"
        else:
            marker = "[dim]-[/dim]"
        selected = index == selected_index
        table.add_row(
            ">" if selected else "",
            routine.group,
            routine.name,
            routine.description,
            marker,
            format_dt(data.get("finished_at")),
            duration_text(data.get("duration_seconds")),
            style="reverse" if selected else None,
        )
    console.print(table)
    console.print(
        "[bold]Opcoes:[/bold] [cyan]↑/↓[/cyan] mover | [cyan]Enter[/cyan] executar | "
        "[cyan]l[/cyan] logs | [cyan]c[/cyan] limpar historico | [cyan]q[/cyan] sair"
    )


def param_values(routine: Routine) -> dict[str, str | bool]:
    return {param.name: param.default for param in routine.params}


def param_type(param: Param) -> str:
    if param.is_bool:
        return "booleano"
    if param.is_list:
        return "lista"
    return "texto"


def display_value(value: str | bool) -> str:
    if isinstance(value, bool):
        return "Sim" if value else "Nao"
    text = str(value)
    if len(text) > 92:
        return text[:89] + "..."
    return text


@dataclass
class CompletionState:
    start: int
    original_prefix: str
    candidates: list[str]
    index: int = -1


@dataclass
class FileSearchState:
    start: int
    token: str
    candidates: list[str]
    selected: int = 0


def split_current_token(line: str) -> tuple[int, str]:
    quote: str | None = None
    token_start = 0
    for index, char in enumerate(line):
        if quote:
            if char == quote:
                quote = None
            continue
        if char in {"'", '"'}:
            quote = char
        elif char.isspace():
            token_start = index + 1
    return token_start, line[token_start:]


def unquote_token(token: str) -> str:
    if len(token) >= 2 and token[0] in {"'", '"'} and token[-1] == token[0]:
        return token[1:-1]
    if token[:1] in {"'", '"'}:
        return token[1:]
    return token


def path_separator_for(token: str) -> str:
    if os.name == "nt" and "\\" in token:
        return "\\"
    return "/"


def quote_completion(value: str) -> str:
    if not value or not any(char.isspace() for char in value):
        return value
    if os.name == "nt":
        return '"' + value.replace('"', '\\"') + '"'
    return shlex.quote(value)


def path_completion_candidates(token: str) -> list[str]:
    raw = unquote_token(token)
    sep = path_separator_for(raw)
    expanded = os.path.expanduser(raw)
    dir_part, base = os.path.split(expanded)
    original_dir, _ = os.path.split(raw)

    if raw.endswith(("/", "\\")):
        dir_part = expanded.rstrip("/\\") or expanded
        original_dir = raw.rstrip("/\\")
        base = ""

    if dir_part:
        search_dir = Path(dir_part) if os.path.isabs(dir_part) else ROOT / dir_part
    else:
        search_dir = ROOT

    if not search_dir.exists() or not search_dir.is_dir():
        return []

    candidates: list[str] = []
    try:
        entries = sorted(search_dir.iterdir(), key=lambda item: (not item.is_dir(), item.name.lower()))
    except OSError:
        return []

    for entry in entries:
        if not base.startswith(".") and entry.name.startswith("."):
            continue
        if not entry.name.lower().startswith(base.lower()):
            continue
        if original_dir:
            candidate = original_dir + sep + entry.name
        else:
            candidate = entry.name
        if entry.is_dir():
            candidate += sep
        candidates.append(quote_completion(candidate))
    return candidates


def should_skip_search_dir(path: Path) -> bool:
    return path.name in {".git", "__pycache__"} or path.name.startswith(".")


def filename_search_candidates(token: str, *, limit: int = 200) -> list[str]:
    raw = unquote_token(token)
    if not raw.startswith("@"):
        return []
    query = raw[1:].strip().lower()
    if not query:
        return []

    root = Path.cwd()
    candidates: list[str] = []
    for current_root, dirs, files in os.walk(root):
        current_path = Path(current_root)
        dirs[:] = [
            dirname
            for dirname in dirs
            if not should_skip_search_dir(current_path / dirname)
        ]
        for filename in sorted(files, key=str.lower):
            if query not in filename.lower():
                continue
            path = current_path / filename
            try:
                relative_path = path.relative_to(root)
            except ValueError:
                relative_path = path
            candidates.append(quote_completion(str(relative_path)))
            if len(candidates) >= limit:
                return candidates
    return candidates


def current_file_search(value: str, previous: FileSearchState | None = None) -> FileSearchState | None:
    start, token = split_current_token(value)
    raw = unquote_token(token)
    if not raw.startswith("@"):
        return None
    if previous and previous.start == start and previous.token == token:
        return previous
    candidates = filename_search_candidates(token)
    return FileSearchState(start=start, token=token, candidates=candidates, selected=0)


def apply_completion(line: str, state: CompletionState) -> str:
    _, current_token = split_current_token(line)
    if not state.candidates:
        return line
    state.index = (state.index + 1) % len(state.candidates)
    return line[: state.start] + state.candidates[state.index]


def apply_file_search_selection(line: str, state: FileSearchState) -> str:
    if not state.candidates:
        return line
    return line[: state.start] + state.candidates[state.selected]


def render_line_editor(
    title: str,
    help_text: str,
    value: str,
    suggestions: list[str],
    *,
    message: str = "",
    search_mode: bool = False,
    selected_index: int = 0,
) -> None:
    console.clear()
    console.print(Panel(help_text, title=title, border_style="cyan"))
    console.print("[bold]Valor:[/bold]")
    console.print(Panel(value or "[dim](vazio)[/dim]", border_style="yellow"))
    if search_mode:
        console.print("[dim]↑/↓ seleciona | Enter insere | Ctrl+U limpa | Esc cancela | Backspace apaga[/dim]")
    else:
        console.print("[dim]TAB completa/cicla | Ctrl+U limpa | Enter confirma | Esc cancela | Backspace apaga[/dim]")
    if message:
        console.print(f"[yellow]{message}[/yellow]")
    if suggestions:
        table = Table(title="Sugestoes", box=box.SIMPLE, show_header=False)
        table.add_column("", justify="center", no_wrap=True)
        table.add_column("Path")
        start = 0
        if search_mode and selected_index >= 12:
            start = selected_index - 11
        for offset, candidate in enumerate(suggestions[start : start + 12]):
            index = start + offset
            table.add_row(">" if search_mode and index == selected_index else "", candidate)
        console.print(table)


def line_input_with_path_completion(title: str, help_text: str, default: str) -> str | None:
    value = default
    completion: CompletionState | None = None
    suggestions: list[str] = []
    search: FileSearchState | None = None
    message = ""
    while True:
        search = current_file_search(value, search)
        active_suggestions = search.candidates if search else suggestions
        render_line_editor(
            title,
            help_text,
            value,
            active_suggestions,
            message=message,
            search_mode=search is not None,
            selected_index=search.selected if search else 0,
        )
        key = read_key()
        message = ""
        if key == "enter":
            if search and search.candidates:
                value = apply_file_search_selection(value, search)
                completion = None
                suggestions = []
                search = None
                continue
            return value
        if key in {"escape", "ctrl-c", "ctrl-d"}:
            return None
        if key == "\x15":
            value = ""
            completion = None
            suggestions = []
            search = None
            continue
        if key == "up" and search and search.candidates:
            search.selected = (search.selected - 1) % len(search.candidates)
            continue
        if key == "down" and search and search.candidates:
            search.selected = (search.selected + 1) % len(search.candidates)
            continue
        if key in {"\x7f", "\b"}:
            value = value[:-1]
            completion = None
            suggestions = []
            continue
        if key == "\t":
            if search:
                if search.candidates:
                    value = apply_file_search_selection(value, search)
                    completion = None
                    suggestions = []
                    search = None
                else:
                    message = "Nenhum arquivo encontrado para a busca @."
                continue
            start, token = split_current_token(value)
            raw_prefix = unquote_token(token)
            if completion and completion.start == start:
                value = apply_completion(value, completion)
            else:
                candidates = path_completion_candidates(token)
                completion = CompletionState(start=start, original_prefix=raw_prefix, candidates=candidates)
                suggestions = candidates
                if candidates:
                    value = apply_completion(value, completion)
                else:
                    message = "Nenhuma opcao de autocomplete encontrada."
            continue
        if len(key) == 1 and key >= " ":
            value += key
            completion = None
            suggestions = []


def render_params_screen(
    routine: Routine,
    values: dict[str, str | bool],
    extra_args: str,
    selected_index: int,
) -> None:
    console.clear()
    console.print(
        Panel(
            f"[bold cyan]{routine.name}[/bold cyan]\n{routine.description}",
            title="Parametros da rotina",
            border_style="cyan",
        )
    )
    table = Table(box=box.SIMPLE_HEAVY, show_lines=False)
    table.add_column("", justify="center", no_wrap=True)
    table.add_column("Parametro", no_wrap=True)
    table.add_column("Flag", no_wrap=True)
    table.add_column("Tipo", no_wrap=True)
    table.add_column("Valor atual")
    table.add_column("Descricao")
    for index, param in enumerate(routine.params):
        selected = index == selected_index
        table.add_row(
            ">" if selected else "",
            param.name,
            param.flag,
            param_type(param),
            display_value(values[param.name]),
            param.help,
            style="reverse" if selected else None,
        )

    extra_index = len(routine.params)
    selected = selected_index == extra_index
    table.add_row(
        ">" if selected else "",
        "args_extras",
        "(livre)",
        "lista",
        display_value(extra_args),
        "Argumentos avancados repassados diretamente a rotina.",
        style="reverse" if selected else None,
    )
    console.print(table)
    console.print(
        "[bold]Opcoes:[/bold] [cyan]↑/↓[/cyan] mover | [cyan]Enter[/cyan] editar | "
        "[cyan]t[/cyan] alternar booleano | [cyan]r[/cyan] restaurar default | "
        "[cyan]e[/cyan] args extras | [cyan]x[/cyan] revisar/executar | [cyan]q[/cyan] cancelar"
    )


def edit_param_value(param: Param, values: dict[str, str | bool]) -> None:
    current = values[param.name]
    if param.is_bool:
        values[param.name] = not bool(current)
        return
    new_value = line_input_with_path_completion(
        title=f"{param.name} {param.flag}",
        help_text=param.help,
        default=str(current),
    )
    if new_value is not None:
        values[param.name] = new_value


def edit_extra_args(extra_args: str) -> str:
    new_value = line_input_with_path_completion(
        title="Argumentos extras avancados",
        help_text="Argumentos repassados diretamente a rotina. Use TAB para completar paths no token atual.",
        default=extra_args,
    )
    return extra_args if new_value is None else new_value


def confirm_command(routine: Routine, values: dict[str, str | bool], extra_args: str) -> list[str] | None:
    cmd = build_command(routine, values, extra_args)
    console.clear()
    console.print(Panel(shlex.join(cmd), title="Comando final", border_style="yellow"))
    if Confirm.ask("Executar esta rotina agora?", default=True):
        return cmd
    return None


def configure_params(routine: Routine) -> tuple[dict[str, str | bool], str, list[str]] | None:
    values = param_values(routine)
    extra_args = ""
    selected_index = 0
    item_count = len(routine.params) + 1
    while True:
        key, selected_index = selectable_loop(
            item_count,
            lambda index: render_params_screen(routine, values, extra_args, index),
            initial_index=selected_index,
            extra_keys={"t", "r", "e", "x"},
        )
        if key in {"q", "escape", "ctrl-c", "ctrl-d"}:
            return None
        if selected_index == len(routine.params):
            if key in {"enter", "e"}:
                extra_args = edit_extra_args(extra_args)
            elif key == "r":
                extra_args = ""
            elif key == "x":
                cmd = confirm_command(routine, values, extra_args)
                if cmd:
                    return values, extra_args, cmd
            continue

        param = routine.params[selected_index]
        if key in {"enter", "t"}:
            if key == "t" and not param.is_bool:
                continue
            edit_param_value(param, values)
        elif key == "r":
            values[param.name] = param.default
        elif key == "e":
            extra_args = edit_extra_args(extra_args)
        elif key == "x":
            cmd = confirm_command(routine, values, extra_args)
            if cmd:
                return values, extra_args, cmd


def split_list(value: str | bool) -> list[str]:
    if isinstance(value, bool):
        return []
    return shlex.split(str(value))


def build_command(routine: Routine, values: dict[str, str | bool], extra_args: str = "") -> list[str]:
    cmd = [str(PYTHON), str(routine.script)]
    cmd.extend(routine.fixed_args)
    cmd.extend(routine.positional)
    for param in routine.params:
        value = values[param.name]
        if param.is_bool:
            if value:
                cmd.append(param.flag)
            continue
        if value is None or str(value).strip() == "":
            continue
        cmd.append(param.flag)
        if param.is_list:
            items = split_list(value)
            if param.repeat_flag:
                cmd.pop()
                for item in items:
                    cmd.extend([param.flag, item])
            else:
                cmd.extend(items)
        else:
            cmd.append(str(value))
    if extra_args.strip():
        cmd.extend(shlex.split(extra_args))
    return cmd


def log_path_for(routine: Routine) -> Path:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return LOG_DIR / f"{stamp}-{routine.key}.log"


def run_command(routine: Routine, cmd: list[str]) -> dict:
    log_path = log_path_for(routine)
    started = now_iso()
    started_monotonic = time.monotonic()

    env = os.environ.copy()
    env.setdefault("PYTHONUNBUFFERED", "1")
    awaiting_input = False
    awaiting_review = False
    with log_path.open("w", encoding="utf-8") as log:
        emit_log(log, f"Iniciando rotina: {routine.name}")
        emit_log(log, f"Comando: {shlex.join(cmd)}")
        emit_log(log, f"Arquivo de log: {log_path}")
        try:
            proc = subprocess.Popen(
                cmd,
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                env=env,
            )
        except OSError as exc:
            message = f"Erro ao iniciar processo: {exc}"
            emit_log(log, message, level="ERROR")
            return {
                "status": "failed",
                "started_at": started,
                "finished_at": now_iso(),
                "duration_seconds": round(time.monotonic() - started_monotonic, 2),
                "returncode": -1,
                "command": cmd,
                "log_path": str(log_path),
            }
        assert proc.stdout is not None
        for line in proc.stdout:
            cleaned = strip_ansi(line)
            if cleaned:
                if "aguardando comentários" in cleaned.casefold() or "awaiting_input" in cleaned.casefold():
                    awaiting_input = True
                if "awaiting_review" in cleaned.casefold() or "aguardando revisão humana" in cleaned.casefold():
                    awaiting_review = True
                emit_log(log, cleaned)
        returncode = proc.wait()
        duration = round(time.monotonic() - started_monotonic, 2)
        if returncode == 0:
            emit_log(log, f"Rotina finalizada com sucesso em {duration_text(duration)}.")
        elif returncode == 2:
            label = "aguardando insumos" if awaiting_input else "parcialmente"
            emit_log(log, f"Rotina finalizada {label} em {duration_text(duration)}.", level="WARNING")
        elif returncode == 3 and awaiting_review:
            emit_log(log, f"Rotina aguardando revisão humana em {duration_text(duration)}.", level="WARNING")
        else:
            emit_log(log, f"Rotina finalizada com erro: código {returncode} em {duration_text(duration)}.", level="ERROR")

    finished = now_iso()
    duration = round(time.monotonic() - started_monotonic, 2)
    status = (
        "success" if returncode == 0
        else "awaiting_input" if returncode == 2 and awaiting_input
        else "awaiting_review" if returncode == 3 and awaiting_review
        else "partial" if returncode == 2
        else "failed"
    )
    return {
        "status": status,
        "started_at": started,
        "finished_at": finished,
        "duration_seconds": duration,
        "returncode": returncode,
        "command": cmd,
        "log_path": str(log_path),
    }


def update_routine_state(state: dict, routine: Routine, result: dict) -> None:
    state.setdefault("routines", {})[routine.key] = result
    save_state(state)


def show_last_log(state: dict) -> None:
    rows = []
    for routine in ALL_RUNNABLE_ROUTINES:
        data = state.get("routines", {}).get(routine.key)
        if data:
            rows.append((routine, data))
    if not rows:
        console.print("[yellow]Nenhuma rotina foi executada ainda.[/yellow]")
        return

    def render_logs(selected_index: int) -> None:
        console.clear()
        table = Table(title="Ultimos logs", box=box.SIMPLE_HEAVY)
        table.add_column("", justify="center", no_wrap=True)
        table.add_column("Rotina")
        table.add_column("Status")
        table.add_column("Ultima execucao")
        table.add_column("Log")
        for index, (routine, data) in enumerate(rows):
            selected = index == selected_index
            table.add_row(
                ">" if selected else "",
                routine.name,
                str(data.get("status", "-")),
                format_dt(data.get("finished_at")),
                str(data.get("log_path", "-")),
                style="reverse" if selected else None,
            )
        console.print(table)
        console.print("[bold]Opcoes:[/bold] [cyan]↑/↓[/cyan] mover | [cyan]Enter[/cyan] abrir | [cyan]q[/cyan] voltar")

    key, selected = selectable_loop(len(rows), render_logs)
    if key not in {"enter"}:
        return
    routine, data = rows[selected]
    console.clear()
    console.print(Panel(shlex.join(data.get("command", [])), title=f"Comando: {routine.name}", border_style="cyan"))
    log_path = Path(data.get("log_path", ""))
    if not log_path.exists():
        console.print("[red]Arquivo de log nao encontrado.[/red]")
        return
    lines = log_path.read_text(encoding="utf-8", errors="replace").splitlines()
    tail = "\n".join(lines[-80:])
    console.print(Panel(tail or "(log vazio)", title=f"Ultimas linhas: {log_path}", border_style="dim"))


def run_routine_interactive(routine: Routine, state: dict) -> None:
    configured = configure_params(routine)
    if configured is None:
        return
    _, _, cmd = configured
    result = run_command(routine, cmd)
    update_routine_state(state, routine, result)
    Prompt.ask("Pressione Enter para voltar a tela inicial", default="")


def run_comments_group_interactive(state: dict) -> None:
    selected_index = 0

    def render_group(index_selected: int) -> None:
        console.clear()
        console.print(Panel("Selecione uma etapa do pipeline.", title="Avaliação de comentários do gestor", border_style="cyan"))
        table = Table(box=box.SIMPLE_HEAVY)
        table.add_column("")
        table.add_column("Rotina")
        table.add_column("Descrição")
        table.add_column("Status")
        for index, routine in enumerate(COMMENTS_ROUTINES):
            data = state.get("routines", {}).get(routine.key, {})
            marker = {
                "success": "[green]✓[/green]", "partial": "[yellow]![/yellow]",
                "awaiting_input": "[yellow]⏸[/yellow]", "awaiting_review": "[yellow]⏸[/yellow]",
                "failed": "[red]✗[/red]",
            }.get(data.get("status"), "[dim]-[/dim]")
            table.add_row(">" if index == index_selected else "", routine.name, routine.description, marker, style="reverse" if index == index_selected else None)
        console.print(table)
        console.print("[bold]Opções:[/bold] [cyan]↑/↓[/cyan] mover | [cyan]Enter[/cyan] configurar | [cyan]q[/cyan] voltar")

    while True:
        key, selected_index = selectable_loop(len(COMMENTS_ROUTINES), render_group, initial_index=selected_index)
        if key in {"q", "escape", "ctrl-c", "ctrl-d"}:
            return
        run_routine_interactive(COMMENTS_ROUTINES[selected_index], state)
        state.clear()
        state.update(load_state())


def interactive() -> int:
    if not ensure_interactive_tty():
        return 2
    state = load_state()
    selected_index = 0
    while True:
        key, selected_index = selectable_loop(
            len(HOME_ROUTINES),
            lambda index: render_home(state, index),
            initial_index=selected_index,
            extra_keys={"l", "c"},
        )
        if key in {"q", "escape", "ctrl-c", "ctrl-d"}:
            return 0
        if key == "l":
            show_last_log(state)
            Prompt.ask("Pressione Enter para voltar", default="")
            continue
        if key == "c":
            if Confirm.ask("Limpar historico local do Argos CLI?", default=False):
                state = {"routines": {}}
                save_state(state)
            continue
        routine = HOME_ROUTINES[selected_index]
        if routine.key == COMMENTS_GROUP.key:
            run_comments_group_interactive(state)
        else:
            run_routine_interactive(routine, state)
        state = load_state()


def list_routines() -> None:
    table = Table(title="Rotinas Argos CLI", box=box.SIMPLE)
    table.add_column("Chave")
    table.add_column("Grupo")
    table.add_column("Cenários")
    table.add_column("Nome")
    table.add_column("Descricao")
    for routine in ALL_RUNNABLE_ROUTINES:
        table.add_row(routine.key, routine.group, ", ".join(routine.scenarios) or "-", routine.name, routine.description)
    console.print(table)


def parse_bool(value: str) -> bool:
    normalized = value.strip().casefold()
    if normalized in {"1", "true", "sim", "yes", "y"}:
        return True
    if normalized in {"0", "false", "não", "nao", "no", "n"}:
        return False
    raise ValueError(f"valor booleano inválido: {value}")


def apply_named_params(routine: Routine, values: dict[str, str | bool], assignments: list[str]) -> None:
    params = {param.name: param for param in routine.params}
    for assignment in assignments:
        if "=" not in assignment:
            raise ValueError(f"--param exige nome=valor: {assignment}")
        name, value = assignment.split("=", 1)
        if name not in params:
            raise ValueError(f"parâmetro desconhecido para {routine.key}: {name}")
        values[name] = parse_bool(value) if params[name].is_bool else value


def apply_scenario(routine: Routine, values: dict[str, str | bool], scenario: str | None) -> None:
    if not scenario:
        return
    if scenario not in routine.scenarios:
        raise ValueError(f"a rotina {routine.key} não aceita o cenário {scenario}")
    prefix = "20260718" if scenario == "03-pos-comentarios-gestor" else "20260621"
    responses = {
        "01-pos-ajuste-inicial": f"{prefix}-respostas-questionario-01-pos-ajuste-inicial.xlsx",
        "02-pos-avaliacao-evidencias": f"{prefix}-respostas-questionario-02-pos-avaliacao-evidencias.xlsx",
        "03-pos-comentarios-gestor": f"{prefix}-respostas-questionario-pos-comentarios-gestor.xlsx",
    }
    response_path = ROOT / "02-Execucao/01-Questionario/03-Respostas_Processadas" / responses[scenario]
    results_dir = ROOT / "02-Execucao/01-Questionario/04-Resultados_iGovTI" / scenario
    audit_dir = ROOT / "02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria" / scenario
    if scenario == "01-pos-ajuste-inicial":
        panel = ROOT / "02-Execucao/03-Execucao_Procedimentos/99-Avaliacao_Evidencias/painel-avaliacao-evidencias-neutro.xlsx"
    elif scenario == "02-pos-avaliacao-evidencias":
        panel = ROOT / "02-Execucao/03-Execucao_Procedimentos/99-Avaliacao_Evidencias/painel-avaliacao-evidencias.xlsx"
    else:
        panel = ROOT / "02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor/fontes-auditoria-pos-comentarios/painel-avaliacao-evidencias.xlsx"
    replacements = {
        "respostas": str(response_path),
        "resultados_dir": str(results_dir),
        "comparacao_dir": str(results_dir / "comparacao-2023-2026"),
        "resultado": str(audit_dir / "resultado_auditoria.json"),
        "tabelas": str(audit_dir / "tabelas_consolidadas_auditoria.xlsx"),
        "relatorios_procedimentos_zip": str(audit_dir / "relatorios_procedimentos.zip"),
        "anexo_evidencias": str(audit_dir / "anexo_evidencias.docx"),
        "fontes": "",
        "fonte": f"questionario={response_path} avaliacao_evidencias_ajustes={panel.resolve()}",
    }
    for name, value in replacements.items():
        if name in values:
            values[name] = value
    if routine.key in {"gerar-relatorios-individuais", "gerar-relatorios-individuais-finais"}:
        values["auditados"] = str(audit_dir / "resultado_auditoria.json")
        values["context_files"] = str(results_dir / f"{prefix}-contexto-relatorios-igovti-2026.xlsx")
    if routine.key == "gerar-relatorio-consolidado":
        values["resultados_2026"] = str(results_dir / f"{prefix}-iGovTI-2026.xlsx")
        values["respostas_2026"] = str(response_path)
        values["comparavel_2026"] = str(results_dir / f"{prefix}-iGovTI-2026-Ajustado-Comparavel.xlsx")
        values["resultado_auditoria"] = str(audit_dir / "resultado_auditoria.json")


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="Lista rotinas disponiveis e sai.")
    parser.add_argument("--run", choices=sorted(ROUTINE_BY_KEY), help="Executa uma rotina sem abrir o menu interativo.")
    parser.add_argument("--yes", action="store_true", help="Nao pede confirmacao no modo --run.")
    parser.add_argument("--extra", default="", help="Argumentos extras repassados a rotina usada com --run.")
    parser.add_argument("--param", action="append", default=[], metavar="NOME=VALOR", help="Sobrescreve um parâmetro declarado; pode ser repetido.")
    parser.add_argument("--cenario", choices=["01-pos-ajuste-inicial", "02-pos-avaliacao-evidencias", "03-pos-comentarios-gestor"], help="Aplica os caminhos padrão de um cenário compatível.")
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    if args.list:
        list_routines()
        return 0
    if args.run:
        routine = ROUTINE_BY_KEY[args.run]
        values = param_values(routine)
        try:
            apply_scenario(routine, values, args.cenario)
            apply_named_params(routine, values, args.param)
        except ValueError as exc:
            console.print(f"[red]{exc}[/red]")
            return 2
        cmd = build_command(routine, values, args.extra)
        if not args.yes:
            console.print(Panel(shlex.join(cmd), title="Comando", border_style="yellow"))
            if not Confirm.ask("Executar esta rotina agora?", default=True):
                return 0
        state = load_state()
        result = run_command(routine, cmd)
        update_routine_state(state, routine, result)
        return int(result.get("returncode", 1))
    return interactive()


if __name__ == "__main__":
    raise SystemExit(main())
