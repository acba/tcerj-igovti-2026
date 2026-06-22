#!/usr/bin/env python3
"""Orquestra a consolidação de avaliações de evidências por juiz IA com barras de progresso.

Substitui scripts/run_consolida_avaliacoes.sh. Lança um ou mais juízes em paralelo,
cada um consolidando os analyses*.jsonl em pareceres consolidados. Mostra barras de
progresso empilhadas no terminal com rich.Progress.
"""

from __future__ import annotations

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
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.table import Table

# ─── CONFIGURAÇÃO ───────────────────────────────────────────────────────────

REPO = Path(__file__).resolve().parent.parent
VENV_PYTHON = str(REPO / "scripts" / ".venv" / "bin" / "python")

BASE_OUT = "02-Execucao/03-Execucao_Procedimentos/avaliacao_evidencias"
EVIDENCIAS_ROOT = "02-Execucao/01-Questionario/Evidencias_Coletadas/evidencias_extraidas"
PROMPTS_DIR = "scripts/avaliacao_evidencias/prompts/igovti_2026_achados_binario_v1"
CATALOG = "scripts/avaliacao_evidencias/prompt_catalogs/igovti_2026_achados_binario_v1.yml"

# Padrão glob para encontrar os arquivos analyses*.jsonl de entrada.
ANALYSES_GLOB = f"{BASE_OUT}/analyses*.jsonl"

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
    proc: subprocess.Popen | None = None
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
    return [str(Path(f).relative_to(REPO)) if Path(f).is_absolute() else f for f in files]


def build_command(cfg: dict, analyses_files: list[str]) -> list[str]:
    out_dir = f"{BASE_OUT}/consolidado"
    cmd = [
        VENV_PYTHON,
        "-m",
        "scripts.avaliacao_evidencias.consolidacao",
        *analyses_files,
        "--evidencias-root",
        EVIDENCIAS_ROOT,
        "--only-achados",
        "--catalog",
        CATALOG,
        "--judge-provider",
        cfg["judge_provider"],
        "--judge-model",
        cfg["judge_model"],
        "--out-dir",
        out_dir,
    ]
    rpm = cfg.get("rpm", 0)
    if rpm:
        cmd += ["--rpm", str(rpm)]
    reasoning = cfg.get("reasoning", "")
    if reasoning:
        cmd += ["--reasoning", reasoning]
    if cfg.get("store_prompts"):
        cmd.append("--store-prompts")
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
                pass
            elif evt == "consolidation_skipped":
                if not jp.total and event.get("total"):
                    jp.total = int(event["total"])
                jp.skipped += 1
            elif evt == "consolidation_recorded":
                if not jp.total and event.get("total"):
                    jp.total = int(event["total"])
                status = event.get("status", "")
                if status == "error":
                    jp.errors += 1
                else:
                    jp.completed += 1
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
    return REPO / BASE_OUT / "consolidado" / "consolidated.jsonl"


def fallback_count_thread(jp: JudgeProgress, cfg: dict) -> None:
    ckpt = checkpoint_path(cfg)
    while jp.status == "running":
        time.sleep(2.0)
        try:
            if ckpt.is_file():
                count = sum(1 for _ in ckpt.open(encoding="utf-8"))
                with jp.lock:
                    if count > jp.processed:
                        jp.completed = count
        except OSError:
            pass


# ─── ORQUESTRADOR ───────────────────────────────────────────────────────────

console = Console()


def run() -> int:
    analyses_files = resolve_analyses_files()
    if not analyses_files:
        console.print(f"[red]Nenhum arquivo encontrado em {ANALYSES_GLOB}.[/red]")
        console.print("[dim]Execute o pipeline de avaliação de evidências primeiro.[/dim]")
        return 1

    active = [j for j in JUDGES if j.get("enabled")]
    if not active:
        console.print("[red]Nenhum juiz ativado. Edite a lista JUDGES no script.[/red]")
        return 1

    console.print(f"[bold green]Iniciando consolidação com {len(active)} juiz(es)...[/bold green]")
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
        cmd = build_command(cfg, analyses_files)
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
        TextColumn("[bold cyan]{task.fields[name]:<36}"),
        BarColumn(bar_width=26, complete_style="green", finished_style="green", pulse_style="blue"),
        TaskProgressColumn(),
        TextColumn("{task.completed}/{task.total}"),
        TextColumn("[red]✗{task.fields[errors]:>4}[/red]"),
        TextColumn("[yellow]⏭{task.fields[skipped]:>3}[/yellow]"),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        TextColumn("{task.fields[status_icon]}"),
        console=console,
        expand=False,
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

    header_table = Table(show_header=False, box=None, padding=(0, 1), expand=False)
    header_table.add_column("hdr_name", width=38, style="bold dim", no_wrap=True)
    header_table.add_column("hdr_bar", width=28, style="bold dim", no_wrap=True)
    header_table.add_column("hdr_pct", width=6, style="bold dim", no_wrap=True)
    header_table.add_column("hdr_count", width=13, style="bold dim", no_wrap=True)
    header_table.add_column("hdr_err", width=6, style="bold dim red", no_wrap=True)
    header_table.add_column("hdr_skip", width=6, style="bold dim yellow", no_wrap=True)
    header_table.add_column("hdr_time", width=8, style="bold dim", no_wrap=True)
    header_table.add_column("hdr_eta", width=8, style="bold dim", no_wrap=True)
    header_table.add_column("hdr_st", width=3, style="bold dim", no_wrap=True)
    header_table.add_row(
        "Juiz (Provider/Modelo)",
        "Progresso",
        "%",
        "Concl/Total",
        "Erros",
        "Pul",
        "Tempo",
        "ETA",
        "St",
    )

    from rich.text import Text as RichText

    def build_alert() -> RichText | None:
        paused = [(jp.display_name, jp.paused_message) for jp in progress_list if jp.status == "paused"]
        if not paused:
            return None
        lines = [f"⚠ ALERTA: {msg} [{name}]" for name, msg in paused]
        return RichText("\n".join(lines), style="bold yellow")

    live_display = Group(header_table, progress)

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
    if fail == 0:
        console.print("[bold green]Todos os juízes finalizaram com sucesso.[/bold green]")
    else:
        console.print("[bold red]Um ou mais juízes falharam ou foram interrompidos.[/bold red]")
    return fail


if __name__ == "__main__":
    sys.exit(run())
