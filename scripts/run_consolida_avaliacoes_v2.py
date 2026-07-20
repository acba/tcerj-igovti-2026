#!/usr/bin/env python3
"""Orquestra a consolidação de avaliações de evidências por juiz IA com barras de progresso.

Versão v2: aponta para o pacote refatorado ``scripts.avaliacao_evidencias``
(provider genérico especializado, evidence_processing compartilhado com o pipeline,
consolidacao reusa preparar_evidencia_para_provider). Mantém a mesma CLI e os mesmos
eventos de log JSONL do orquestrador anterior (``run_consolida_avaliacoes_v2.py``).
"""

from __future__ import annotations

import argparse
import datetime as dt
import glob
import json
import os
import signal
import subprocess
import sys
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path

from rich.console import Console, Group
from rich.live import Live
from rich.progress import (
    BarColumn,
    Progress,
    ProgressColumn,
    TaskProgressColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.table import Table
from rich.text import Text as RichText

class CustomNameColumn(ProgressColumn):
    def render(self, task):
        is_hdr = task.fields.get("is_header")
        name = task.fields.get("name", "")
        if is_hdr:
            return RichText(name, style="bold dim")
        return RichText(name, style="bold cyan")

class CustomBarColumn(BarColumn):
    def render(self, task):
        if task.fields.get("is_header"):
            width = self.bar_width
            return RichText("Progresso".center(width), style="bold dim")
        return super().render(task)

class CustomProgressColumn(TaskProgressColumn):
    def render(self, task):
        if task.fields.get("is_header"):
            return RichText("%", style="bold dim")
        return super().render(task)

class CustomCountColumn(ProgressColumn):
    def render(self, task):
        if task.fields.get("is_header"):
            return RichText("Concl/Total", style="bold dim")
        return RichText(f"{task.completed}/{task.total}")

class CustomErrorColumn(ProgressColumn):
    def render(self, task):
        if task.fields.get("is_header"):
            return RichText("Erros", style="bold dim red")
        errs = task.fields.get("errors", 0)
        return RichText(f"x {errs}", style="red")

class CustomSkipColumn(ProgressColumn):
    def render(self, task):
        if task.fields.get("is_header"):
            return RichText("Pul", style="bold dim yellow")
        skips = task.fields.get("skipped", 0)
        return RichText(f"> {skips}", style="yellow")

class CustomTimeElapsedColumn(TimeElapsedColumn):
    def render(self, task):
        if task.fields.get("is_header"):
            return RichText("Tempo", style="bold dim")
        return super().render(task)

class CustomTimeRemainingColumn(TimeRemainingColumn):
    def render(self, task):
        if task.fields.get("is_header"):
            return RichText("ETA", style="bold dim")
        return super().render(task)

class CustomStartedColumn(ProgressColumn):
    def render(self, task):
        if task.fields.get("is_header"):
            return RichText("Início", style="bold dim")
        return RichText(task.fields.get("started_wall", ""))

class CustomCurrentColumn(ProgressColumn):
    def render(self, task):
        if task.fields.get("is_header"):
            return RichText("Auditado / Evidência", style="bold dim")
        return RichText(task.fields.get("current", ""), style="dim")

class CustomStatusColumn(ProgressColumn):
    def render(self, task):
        if task.fields.get("is_header"):
            return RichText("St", style="bold dim")
        return RichText(task.fields.get("status_icon", ""))

# ─── CONFIGURAÇÃO ───────────────────────────────────────────────────────────

REPO = Path(__file__).resolve().parent.parent
if sys.platform == "win32":
    VENV_PYTHON = str(REPO / "scripts" / ".venv" / "Scripts" / "python.exe")
else:
    VENV_PYTHON = str(REPO / "scripts" / ".venv" / "bin" / "python")

BASE_OUT = "02-Execucao/03-Execucao_Procedimentos/99-Avaliacao_Evidencias/individuais"
EVIDENCIAS_ROOT_DEFAULT = "02-Execucao/01-Questionario/01-Coleta_LimeSurvey/Evidencias_Coletadas/evidencias_extraidas"
PROMPTS_DIR = "scripts/avaliacao_evidencias/prompts/igovti_2026_achados_binario_v1"
CATALOG = "scripts/avaliacao_evidencias/prompt_catalogs/igovti_2026_achados_binario_v1.yml"

# Padrão glob para encontrar os arquivos analyses*.jsonl de entrada.
ANALYSES_GLOB = f"{BASE_OUT}/analyses_clean*.jsonl"
CONSOLIDATED_OUT = f"{BASE_OUT}/consolidado"
MIN_OPINIONS = 1

# Lista de juízes para executar em paralelo.
# Cada juiz consolida todos os analyses*.jsonl em pareceres.
# Para desativar um juiz, mudar "enabled" para False.
# Para adicionar um juiz, copiar um bloco e ajustar judge_provider/judge_model.
JUDGES: list[dict] = [
    {
        "name": "gemini-3.1-flash-lite",
        "judge_provider": "gemini",
        "judge_model": "gemini-3.1-flash-lite",
        "rpm": 0,
        "reasoning": "high",
        "pdf2md": False,
        "docx2html": True,
        "store_prompts": False,
        "enabled": True,
    },
    # ── Juízes desativados (mudar "enabled" para True para ativar) ───────────
    {
        "name": "gpt-5.4-mini",
        "judge_provider": "openai",
        "judge_model": "gpt-5.4-mini",
        "rpm": 0,
        "reasoning": "high",
        "store_prompts": False,
        "enabled": False,
    },
    {
        "name": "minimax-m3",
        "judge_provider": "opencodego",
        "judge_model": "minimax-m3",
        "rpm": 0,
        "reasoning": "high",
        "store_prompts": False,
        "enabled": False,
    },
    {
        "name": "openrouter-gpt-5.4-mini",
        "judge_provider": "openrouter",
        "judge_model": "openai/gpt-5.4-mini",
        "rpm": 0,
        "reasoning": "high",
        "store_prompts": False,
        "enabled": False,
    },
]

# ─── ESTADO POR JUIZ ────────────────────────────────────────────────────────


@dataclass
class JudgeProgress:
    name: str
    judge_provider: str
    judge_model: str
    total: int = 0
    completed: int = 0
    errors: int = 0
    skipped: int = 0
    status: str = "pending"  # pending | running | paused | done | failed | killed
    paused_message: str = ""
    started_at: float = 0.0
    finished_at: float = 0.0
    started_wall: str = ""  # hora de inicio em GMT-3 (string HH:MM:SS)
    current_auditado: str = ""
    current_evidencia: str = ""
    proc: subprocess.Popen | None = None
    errors_map: dict[str, dict] = field(default_factory=dict)
    lock: threading.Lock = field(default_factory=threading.Lock)

    @property
    def processed(self) -> int:
        return self.completed + self.errors + self.skipped

    @property
    def pending(self) -> int:
        return max(0, self.total - self.processed)

    @property
    def elapsed(self) -> float:
        end = self.finished_at if self.finished_at else time.monotonic()
        return max(0.0, end - self.started_at) if self.started_at else 0.0

    @property
    def eta_seconds(self) -> float:
        if self.processed == 0 or self.pending == 0:
            return 0.0
        rate = self.processed / self.elapsed if self.elapsed > 0 else 0
        if rate <= 0:
            return 0.0
        return self.pending / rate

    @property
    def display_name(self) -> str:
        return f"{self.judge_provider}/{self.name}"


# ─── CONSTRUÇÃO DE COMANDO ──────────────────────────────────────────────────


def resolve_analyses_files() -> list[str]:
    files = sorted(glob.glob(ANALYSES_GLOB))
    if not files:
        return []
    resolved: list[str] = []
    for value in files:
        path = Path(value)
        if path.is_absolute():
            try:
                resolved.append(str(path.relative_to(REPO)))
            except ValueError:
                resolved.append(str(path))
        else:
            resolved.append(value)
    return resolved


def build_command(cfg: dict, analyses_files: list[str], evidencias_root: str = EVIDENCIAS_ROOT_DEFAULT, only_achados: bool = True) -> list[str]:
    out_dir = CONSOLIDATED_OUT
    cmd = [
        VENV_PYTHON,
        "-m",
        "scripts.avaliacao_evidencias.consolidacao",
        *analyses_files,
        "--evidencias-root",
        evidencias_root,
        "--catalog",
        CATALOG,
        "--judge-provider",
        cfg["judge_provider"],
        "--judge-model",
        cfg["judge_model"],
        "--out-dir",
        out_dir,
    ]
    if only_achados or cfg.get("only_achados"):
        cmd.append("--only-achados")
    cmd += ["--min-opinions", str(MIN_OPINIONS)]
    rpm = cfg.get("rpm", 0)
    if rpm:
        cmd += ["--rpm", str(rpm)]
    reasoning = cfg.get("reasoning", "")
    if reasoning:
        cmd += ["--reasoning", reasoning]
    if cfg.get("store_prompts"):
        cmd.append("--store-prompts")
    if cfg.get("pdf2md"):
        cmd.append("--pdf2md")
    if cfg.get("docx2html"):
        cmd.append("--docx2html")
    return cmd


def env_for_judge(cfg: dict) -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    return env


# ─── LEITOR DE STDOUT ───────────────────────────────────────────────────────


def reader_thread(proc: subprocess.Popen, jp: JudgeProgress) -> None:
    assert proc.stdout is not None
    for raw_line in iter(proc.stdout.readline, ""):
        line = raw_line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except (json.JSONDecodeError, ValueError):
            continue
        evt = event.get("event", "")
        with jp.lock:
            if evt == "consolidation_started":
                ts = event.get("ts", "")
                if ts:
                    try:
                        utc = dt.datetime.fromisoformat(ts.replace("Z", "+00:00"))
                        local = utc.astimezone(dt.timezone(dt.timedelta(hours=-3)))
                        jp.started_wall = local.strftime("%H:%M:%S")
                    except (ValueError, TypeError):
                        jp.started_wall = ""
            elif evt == "consolidation_skipped":
                if not jp.total and event.get("total"):
                    jp.total = int(event["total"])
                jp.completed += 1
                jp.current_auditado = str(event.get("auditado", ""))
                jp.current_evidencia = str(event.get("evidencia", ""))
            elif evt == "consolidation_recorded":
                if not jp.total and event.get("total"):
                    jp.total = int(event["total"])
                status = event.get("status", "")
                if status == "error":
                    jp.errors += 1
                    identity = event.get("identity") or f"{event.get('auditado', 'D')}_{event.get('coluna_evidencia', 'C')}"
                    jp.errors_map[identity] = {
                        "auditado": event.get("auditado", "Desconhecido"),
                        "coluna_evidencia": event.get("coluna_evidencia", "Desconhecido"),
                        "error": event.get("error", "Erro de consolidação desconhecido"),
                    }
                else:
                    jp.completed += 1
                jp.current_auditado = str(event.get("auditado", ""))
                jp.current_evidencia = str(event.get("evidencia", ""))
            elif evt == "all_keys_exhausted":
                jp.status = "paused"
                wait_s = event.get("retry_after_seconds", 60)
                jp.paused_message = (
                    f"Todas as chaves {event.get('provider', '?')} exauridas — "
                    f"pausado por {wait_s:.0f}s"
                )
            elif evt == "consolidation_recorded" and jp.status == "paused":
                jp.status = "running"
                jp.paused_message = ""
            elif evt == "consolidation_finished":
                jp.status = "done"
                jp.finished_at = time.monotonic()
    with jp.lock:
        if jp.status in ("running", "pending"):
            jp.status = "done" if proc.poll() == 0 else "failed"
            jp.finished_at = time.monotonic()


# ─── FALLBACK: CONTAR LINHAS DO CHECKPOINT ──────────────────────────────────


def checkpoint_path(cfg: dict) -> Path:
    return REPO / CONSOLIDATED_OUT / "consolidated.jsonl"


# A thread fallback_count_thread foi desativada pois causava leituras
# cegas de cache fora do escopo de execução atual.
def fallback_count_thread(jp: JudgeProgress, cfg: dict) -> None:
    pass


# ─── ORQUESTRADOR ───────────────────────────────────────────────────────────

console = Console()


def _format_current(jp: JudgeProgress) -> str:
    """Compacta auditado + evidencia para a coluna 'Atual' da barra."""
    if not jp.current_auditado and not jp.current_evidencia:
        return ""
    ev = jp.current_evidencia
    if len(ev) > 26:
        ev = ev[:23] + "..."
    return f"{jp.current_auditado} | {ev}"


def run() -> int:
    global ANALYSES_GLOB, CONSOLIDATED_OUT, CATALOG, JUDGES, MIN_OPINIONS
    parser = argparse.ArgumentParser(
        description="Orquestra a consolidação de avaliações de evidências por juiz IA (v2 — refatorado)."
    )
    parser.add_argument(
        "--evidencias",
        default=EVIDENCIAS_ROOT_DEFAULT,
        help=f"Diretório raiz das evidências extraídas (default: {EVIDENCIAS_ROOT_DEFAULT})",
    )
    parser.add_argument(
        "--only-achados",
        action="store_true",
        help="Consolida apenas os itens que geram achados (default: todos os itens).",
    )
    parser.add_argument("--analyses-glob", default=ANALYSES_GLOB, help="Glob dos JSONL dos avaliadores.")
    parser.add_argument("--out-dir", default=CONSOLIDATED_OUT, help="Diretório da consolidação.")
    parser.add_argument("--catalog", default=CATALOG)
    parser.add_argument("--min-opinions", type=int, default=MIN_OPINIONS, help="Quórum mínimo de avaliações válidas por evidência.")
    parser.add_argument(
        "--judges-config",
        type=Path,
        help="JSON opcional com lista em 'judges'; substitui a configuração embutida.",
    )
    args = parser.parse_args()

    ANALYSES_GLOB = args.analyses_glob
    CONSOLIDATED_OUT = args.out_dir
    CATALOG = args.catalog
    MIN_OPINIONS = args.min_opinions
    if args.judges_config:
        payload = json.loads(args.judges_config.read_text(encoding="utf-8"))
        configured = payload.get("judges")
        if not isinstance(configured, list):
            parser.error("--judges-config deve conter uma lista em 'judges'.")
        JUDGES = configured

    analyses_files = resolve_analyses_files()
    if not analyses_files:
        console.print(f"[red]Nenhum arquivo encontrado em {ANALYSES_GLOB}.[/red]")
        console.print("[dim]Execute o pipeline de avaliação de evidências primeiro.[/dim]")
        return 1

    active = [j for j in JUDGES if j.get("enabled")]
    if not active:
        console.print("[red]Nenhum juiz ativado. Edite a lista JUDGES no script.[/red]")
        return 1

    only_achados = args.only_achados
    console.print(f"[bold green]Iniciando consolidação com {len(active)} juiz(es)...[/bold green]")
    console.print(f"[dim]Evidências: {args.evidencias}[/dim]")
    console.print(f"[dim]Escopo: {'apenas itens que geram achados' if only_achados else 'todos os itens'}[/dim]")
    console.print(f"[dim]Arquivos de entrada ({len(analyses_files)}):[/dim]")
    for f in analyses_files:
        console.print(f"[dim]  • {f}[/dim]")
    console.print()

    progress_list: list[JudgeProgress] = []
    threads: list[threading.Thread] = []
    fallback_threads: list[threading.Thread] = []

    for cfg in active:
        jp = JudgeProgress(
            name=cfg["name"],
            judge_provider=cfg["judge_provider"],
            judge_model=cfg["judge_model"],
        )
        jp.status = "running"
        jp.started_at = time.monotonic()
        cmd = build_command(cfg, analyses_files, args.evidencias, only_achados)
        env = env_for_judge(cfg)
        try:
            proc = subprocess.Popen(
                cmd,
                cwd=str(REPO),
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
        except FileNotFoundError as exc:
            console.print(f"[red]Erro ao iniciar {cfg['name']}: {exc}[/red]")
            jp.status = "failed"
            jp.finished_at = time.monotonic()
            progress_list.append(jp)
            continue

        jp.proc = proc
        progress_list.append(jp)

        t = threading.Thread(target=reader_thread, args=(proc, jp), daemon=True)
        t.start()
        threads.append(t)

        fb = threading.Thread(target=fallback_count_thread, args=(jp, cfg), daemon=True)
        fb.start()
        fallback_threads.append(fb)

    progress = Progress(
        CustomNameColumn(),
        CustomBarColumn(bar_width=22, complete_style="green", finished_style="green", pulse_style="blue"),
        CustomProgressColumn(),
        CustomCountColumn(),
        CustomErrorColumn(),
        CustomSkipColumn(),
        CustomTimeElapsedColumn(),
        CustomTimeRemainingColumn(),
        CustomStartedColumn(),
        CustomCurrentColumn(),
        CustomStatusColumn(),
        console=console,
        expand=False,
    )

    # Adiciona a tarefa de cabeçalho na primeira linha
    progress.add_task(
        description="",
        is_header=True,
        name="Juiz (Provider/Modelo)",
        total=1,
        completed=0,
        errors=0,
        skipped=0,
        started_wall="",
        current="",
        status_icon="",
    )

    task_ids: list[int] = []
    for jp in progress_list:
        tid = progress.add_task(
            description="",
            name=jp.display_name,
            total=jp.total or 1,
            completed=jp.completed,
            errors=jp.errors,
            skipped=jp.skipped,
            started_wall=jp.started_wall or "--:--:--",
            current="",
            status_icon="⏳",
        )
        task_ids.append(tid)

    shutdown = threading.Event()

    def handle_sigint(signum, frame):
        shutdown.set()
        for jp in progress_list:
            if jp.proc and jp.proc.poll() is None:
                jp.status = "killed"
                jp.proc.terminate()
        console.print("\n[yellow]Interrompendo subprocesses... (Ctrl+C novamente para forçar)[/yellow]")

    signal.signal(signal.SIGINT, handle_sigint)

    def build_alert() -> RichText | None:
        paused = [(jp.display_name, jp.paused_message) for jp in progress_list if jp.status == "paused"]
        if not paused:
            return None
        lines = [f"⚠ ALERTA: {msg} [{name}]" for name, msg in paused]
        return RichText("\n".join(lines), style="bold yellow")

    live_display = Group(progress)

    def update_loop():
        last_alert_printed = False
        while not shutdown.is_set():
            all_done = all(jp.status in ("done", "failed", "killed") for jp in progress_list)
            paused_now = any(jp.status == "paused" for jp in progress_list)
            if paused_now and not last_alert_printed:
                alert = build_alert()
                if alert:
                    console.print(alert)
                last_alert_printed = True
            elif not paused_now and last_alert_printed:
                last_alert_printed = False
            for i, jp in enumerate(progress_list):
                with jp.lock:
                    total = jp.total or 1
                    progress.update(
                        task_ids[i],
                        total=total,
                        completed=jp.completed,
                        name=jp.display_name,
                        errors=jp.errors,
                        skipped=jp.skipped,
                        started_wall=jp.started_wall or "--:--:--",
                        current=_format_current(jp),
                        status_icon={
                            "running": "⏳",
                            "paused": "[yellow blink]⏸[/yellow blink]",
                            "done": "[green]✓[/green]",
                            "failed": "[red]✗[/red]",
                            "killed": "[yellow]⚠[/yellow]",
                            "pending": "…",
                        }.get(jp.status, "…"),
                    )
            if all_done:
                break
            time.sleep(0.3)

    with Live(live_display, console=console, refresh_per_second=4, screen=False):
        update_thread = threading.Thread(target=update_loop, daemon=True)
        update_thread.start()
        for jp in progress_list:
            if jp.proc:
                jp.proc.wait()
        for t in threads:
            t.join(timeout=5)
        update_thread.join(timeout=5)

    console.print()
    table = Table(title="Resumo da consolidação", show_lines=False)
    table.add_column("Juiz (Provider/Modelo)", style="bold cyan")
    table.add_column("Total", justify="right")
    table.add_column("Concluídos", justify="right", style="green")
    table.add_column("Erros", justify="right", style="red")
    table.add_column("Pulados", justify="right", style="yellow")
    table.add_column("Tempo", justify="right")
    table.add_column("Status", justify="center")

    fail = 0
    for jp in progress_list:
        elapsed_str = f"{int(jp.elapsed // 60)}m{int(jp.elapsed % 60):02d}s"
        status_str = {
            "done": "[green]✓ Sucesso[/green]",
            "failed": "[red]✗ Falha[/red]",
            "killed": "[yellow]⚠ Interrompido[/yellow]",
            "running": "[blue]⏳ Em execução[/blue]",
            "paused": "[yellow]⏸ Chaves exauridas[/yellow]",
        }.get(jp.status, jp.status)
        if jp.status in ("failed", "killed"):
            fail = 1
        table.add_row(
            jp.display_name,
            str(jp.total),
            str(jp.completed),
            str(jp.errors),
            str(jp.skipped),
            elapsed_str,
            status_str,
        )

    console.print(table)
    console.print()

    has_any_errors = any(len(jp.errors_map) > 0 for jp in progress_list)
    if has_any_errors:
        from rich.tree import Tree
        error_tree = Tree("[bold red]Detalhamento de Erros por Juiz[/bold red]")
        for jp in progress_list:
            if jp.errors_map:
                judge_node = error_tree.add(f"[bold cyan]{jp.display_name}[/bold cyan] ({len(jp.errors_map)} erro(s))")
                sorted_errors = sorted(
                    jp.errors_map.values(),
                    key=lambda x: (x.get("auditado", ""), x.get("coluna_evidencia", ""))
                )
                for err_info in sorted_errors:
                    auditado = err_info.get("auditado", "Desconhecido")
                    coluna = err_info.get("coluna_evidencia", "Desconhecido")
                    desc = str(err_info.get("error", "Erro de consolidação desconhecido")).strip().replace("\n", " ")
                    judge_node.add(f"[bold yellow]{auditado}[/bold yellow] | [bold magenta]{coluna}[/bold magenta]: {desc}")
        console.print(error_tree)
        console.print()

    if fail == 0:
        console.print("[bold green]Todos os juízes finalizaram com sucesso.[/bold green]")
    else:
        console.print("[bold red]Um ou mais juízes falharam ou foram interrompidos.[/bold red]")
    return fail


if __name__ == "__main__":
    sys.exit(run())
