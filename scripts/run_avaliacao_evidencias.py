#!/usr/bin/env python3
"""Orquestra pipelines de avaliação de evidências em paralelo com barras de progresso.

Substitui scripts/run_avaliacao_evidencias.sh com visibilidade de progresso por modelo
usando rich.Progress. Cada modelo rodando em paralelo tem sua própria barra empilhada
no terminal, mostrando concluídas, erros, puladas, % e ETA.
"""

from __future__ import annotations

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
QUESTIONARIO = "01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md"
PROMPTS_DIR = "scripts/avaliacao_evidencias/prompts/igovti_2026_achados_binario_v1"
PROMPT_VERSION = "igovti_2026_achados_binario_v1"
CATALOG = "scripts/avaliacao_evidencias/prompt_catalogs/igovti_2026_achados_binario_v1.yml"
RESPOSTAS = "02-Execucao/01-Questionario/20260621-respostas-questionario.xlsx"
EVIDENCIAS = "02-Execucao/01-Questionario/Evidencias_Coletadas/evidencias_extraidas"

# Lista de modelos para executar em paralelo.
# Para desativar um modelo, mudar "enabled" para False.
# Para adicionar um modelo, copiar um bloco e ajustar provider/model/flags.
MODELS: list[dict] = [
    {
        "name": "gemini-3.1-flash-lite",
        "provider": "gemini",
        "model": "gemini-3.1-flash-lite",
        "rpm": 12,
        "reasoning": "high",
        "pdf2md": False,
        "docx2html": False,
        "store_prompts": False,
        "enabled": True,
    },
    {
        "name": "minimax-m3",
        "provider": "opencodego",
        "model": "minimax-m3",
        "rpm": 0,
        "reasoning": "high",
        "pdf2md": True,
        "docx2html": True,
        "store_prompts": False,
        "enabled": True,
    },
    # ── Modelos desativados (mudar "enabled" para True para ativar) ──────────
    {
        "name": "gpt-5.4-mini",
        "provider": "openai",
        "model": "gpt-5.4-mini",
        "rpm": 12,
        "reasoning": "high",
        "pdf2md": False,
        "docx2html": False,
        "store_prompts": False,
        "enabled": False,
    },
    {
        "name": "openrouter-minimax-m3",
        "provider": "openrouter",
        "model": "minimax/minimax-m3",
        "rpm": 0,
        "reasoning": "high",
        "pdf2md": True,
        "docx2html": True,
        "store_prompts": False,
        "enabled": False,
    },
    {
        "name": "openrouter-qwen3.7-plus",
        "provider": "openrouter",
        "model": "qwen/qwen3.7-plus",
        "rpm": 0,
        "reasoning": "high",
        "pdf2md": True,
        "docx2html": True,
        "store_prompts": False,
        "enabled": False,
    },
    {
        "name": "openrouter-gpt-5.4-mini",
        "provider": "openrouter",
        "model": "openai/gpt-5.4-mini",
        "rpm": 0,
        "reasoning": "high",
        "pdf2md": False,
        "docx2html": False,
        "store_prompts": False,
        "enabled": False,
    },
    {
        "name": "openrouter-gemma-4-31b-it-free",
        "provider": "openrouter",
        "model": "google/gemma-4-31b-it:free",
        "rpm": 0,
        "reasoning": "high",
        "pdf2md": False,
        "docx2html": False,
        "store_prompts": False,
        "enabled": False,
    },
    {
        "name": "openrouter-gpt-5.4-nano",
        "provider": "openrouter",
        "model": "openai/gpt-5.4-nano",
        "rpm": 0,
        "reasoning": "high",
        "pdf2md": False,
        "docx2html": False,
        "store_prompts": False,
        "enabled": False,
    },
    {
        "name": "gemma-4-31b-it",
        "provider": "gemini",
        "model": "gemma-4-31b-it",
        "rpm": 12,
        "reasoning": "high",
        "pdf2md": False,
        "docx2html": False,
        "store_prompts": False,
        "enabled": False,
    },
]

# ─── ESTADO POR MODELO ──────────────────────────────────────────────────────


@dataclass
class ModelProgress:
    name: str
    provider: str
    model: str
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
        if self.completed == 0 or self.pending == 0:
            return 0.0
        rate = self.processed / self.elapsed if self.elapsed > 0 else 0
        if rate <= 0:
            return 0.0
        return self.pending / rate

    @property
    def display_name(self) -> str:
        return f"{self.provider}/{self.name}"


# ─── CONSTRUÇÃO DE COMANDO ──────────────────────────────────────────────────


def build_command(cfg: dict) -> list[str]:
    cmd = [
        VENV_PYTHON,
        "-m",
        "scripts.avaliacao_evidencias",
        RESPOSTAS,
        EVIDENCIAS,
        "--questionario",
        QUESTIONARIO,
        "--prompts-dir",
        PROMPTS_DIR,
        "--prompt-version",
        PROMPT_VERSION,
        "--only-prompts-present",
        "--only-achados",
        "--catalog",
        CATALOG,
        "--provider",
        cfg["provider"],
        "--model",
        cfg["model"],
        "--out-dir",
        BASE_OUT,
    ]
    reasoning = cfg.get("reasoning", "")
    if reasoning:
        cmd += ["--reasoning", reasoning]
    rpm = cfg.get("rpm", 0)
    if rpm:
        cmd += ["--rpm", str(rpm)]
    if cfg.get("pdf2md"):
        cmd.append("--pdf2md")
    if cfg.get("docx2html"):
        cmd.append("--docx2html")
    if cfg.get("store_prompts"):
        cmd.append("--store-prompts")
    return cmd


def env_for_model(cfg: dict) -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    return env


# ─── LEITOR DE STDOUT ───────────────────────────────────────────────────────


def reader_thread(proc: subprocess.Popen, mp: ModelProgress) -> None:
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
        with mp.lock:
            if evt == "inventory_completed":
                mp.total = int(event.get("total_analises", 0))
            elif evt == "analysis_recorded":
                status = event.get("status", "")
                if not mp.total and event.get("total"):
                    mp.total = int(event["total"])
                if status == "error":
                    mp.errors += 1
                else:
                    mp.completed += 1
            elif evt == "analysis_skipped":
                mp.skipped += 1
            elif evt == "all_keys_exhausted":
                mp.status = "paused"
                wait_s = event.get("retry_after_seconds", 60)
                mp.paused_message = (
                    f"Todas as chaves {event.get('provider', '?')} exauridas — "
                    f"pausado por {wait_s:.0f}s"
                )
            elif evt == "provider_started":
                if mp.status == "paused":
                    mp.status = "running"
                    mp.paused_message = ""
            elif evt == "pipeline_finished":
                mp.status = "done" if event.get("erros", 0) == 0 or mp.completed > 0 else "done"
                mp.finished_at = time.monotonic()
    with mp.lock:
        if mp.status in ("running", "pending"):
            mp.status = "done" if proc.poll() == 0 else "failed"
            mp.finished_at = time.monotonic()


# ─── FALLBACK: CONTAR LINHAS DO CHECKPOINT ──────────────────────────────────


def checkpoint_path(cfg: dict) -> Path:
    provider = cfg["provider"].replace("/", "_")
    model = cfg["model"].replace("/", "_")
    return REPO / BASE_OUT / f"analyses_{provider}_{model}.jsonl"


def fallback_count_thread(mp: ModelProgress, cfg: dict) -> None:
    ckpt = checkpoint_path(cfg)
    while mp.status == "running":
        time.sleep(2.0)
        try:
            if ckpt.is_file():
                count = sum(1 for _ in ckpt.open(encoding="utf-8"))
                with mp.lock:
                    if count > mp.processed:
                        mp.completed = count
        except OSError:
            pass


# ─── ORQUESTRADOR ───────────────────────────────────────────────────────────

console = Console()


def run() -> int:
    active = [m for m in MODELS if m.get("enabled")]
    if not active:
        console.print("[red]Nenhum modelo ativado. Edite a lista MODELS no script.[/red]")
        return 1

    console.print(f"[bold green]Iniciando {len(active)} pipeline(s) de avaliação de evidências...[/bold green]")
    console.print()

    progress_list: list[ModelProgress] = []
    threads: list[threading.Thread] = []
    fallback_threads: list[threading.Thread] = []

    for cfg in active:
        mp = ModelProgress(name=cfg["name"], provider=cfg["provider"], model=cfg["model"])
        mp.status = "running"
        mp.started_at = time.monotonic()
        cmd = build_command(cfg)
        env = env_for_model(cfg)
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
            mp.status = "failed"
            mp.finished_at = time.monotonic()
            progress_list.append(mp)
            continue

        mp.proc = proc
        progress_list.append(mp)

        t = threading.Thread(target=reader_thread, args=(proc, mp), daemon=True)
        t.start()
        threads.append(t)

        fb = threading.Thread(target=fallback_count_thread, args=(mp, cfg), daemon=True)
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
    for mp in progress_list:
        tid = progress.add_task(
            description="",
            name=mp.display_name,
            total=mp.total or 1,
            completed=mp.completed,
            errors=mp.errors,
            skipped=mp.skipped,
            status_icon="⏳",
        )
        task_ids.append(tid)

    shutdown = threading.Event()

    def handle_sigint(signum, frame):
        shutdown.set()
        for mp in progress_list:
            if mp.proc and mp.proc.poll() is None:
                mp.status = "killed"
                mp.proc.terminate()
        console.print("\n[yellow]Interrompendo subprocesses... (Ctrl+C novamente para forçar)[/yellow]")

    signal.signal(signal.SIGINT, handle_sigint)

    def update_loop():
        last_alert_printed = False
        while not shutdown.is_set():
            all_done = all(mp.status in ("done", "failed", "killed") for mp in progress_list)
            paused_now = any(mp.status == "paused" for mp in progress_list)
            if paused_now and not last_alert_printed:
                alert = build_alert()
                if alert:
                    console.print(alert)
                last_alert_printed = True
            elif not paused_now and last_alert_printed:
                last_alert_printed = False
            for i, mp in enumerate(progress_list):
                with mp.lock:
                    total = mp.total or 1
                    progress.update(
                        task_ids[i],
                        total=total,
                        completed=mp.completed,
                        name=mp.display_name,
                        errors=mp.errors,
                        skipped=mp.skipped,
                        status_icon={
                            "running": "⏳",
                            "paused": "[yellow blink]⏸[/yellow blink]",
                            "done": "[green]✓[/green]",
                            "failed": "[red]✗[/red]",
                            "killed": "[yellow]⚠[/yellow]",
                            "pending": "…",
                        }.get(mp.status, "…"),
                    )
            if all_done:
                break
            time.sleep(0.3)

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
        "Provider/Modelo",
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
        """Constrói texto de alerta se algum modelo estiver pausado."""
        paused = [(mp.display_name, mp.paused_message) for mp in progress_list if mp.status == "paused"]
        if not paused:
            return None
        lines = []
        for name, msg in paused:
            lines.append(f"⚠ ALERTA: {msg} [{name}]")
        return RichText("\n".join(lines), style="bold yellow")

    live_display = Group(header_table, progress)

    with Live(live_display, console=console, refresh_per_second=4, screen=False):
        update_thread = threading.Thread(target=update_loop, daemon=True)
        update_thread.start()
        for mp in progress_list:
            if mp.proc:
                mp.proc.wait()
        for t in threads:
            t.join(timeout=5)
        update_thread.join(timeout=5)

    console.print()
    table = Table(title="Resumo da avaliação de evidências", show_lines=False)
    table.add_column("Provider/Modelo", style="bold cyan")
    table.add_column("Total", justify="right")
    table.add_column("Concluídas", justify="right", style="green")
    table.add_column("Erros", justify="right", style="red")
    table.add_column("Puladas", justify="right", style="yellow")
    table.add_column("Tempo", justify="right")
    table.add_column("Status", justify="center")

    fail = 0
    for mp in progress_list:
        elapsed_str = f"{int(mp.elapsed // 60)}m{int(mp.elapsed % 60):02d}s"
        status_str = {
            "done": "[green]✓ Sucesso[/green]",
            "failed": "[red]✗ Falha[/red]",
            "killed": "[yellow]⚠ Interrompido[/yellow]",
            "running": "[blue]⏳ Em execução[/blue]",
            "paused": "[yellow]⏸ Chaves exauridas[/yellow]",
        }.get(mp.status, mp.status)
        if mp.status in ("failed", "killed"):
            fail = 1
        table.add_row(
            mp.display_name,
            str(mp.total),
            str(mp.completed),
            str(mp.errors),
            str(mp.skipped),
            elapsed_str,
            status_str,
        )

    console.print(table)
    console.print()
    if fail == 0:
        console.print("[bold green]Todos os pipelines finalizaram com sucesso.[/bold green]")
    else:
        console.print("[bold red]Um ou mais pipelines falharam ou foram interrompidos.[/bold red]")
    return fail


if __name__ == "__main__":
    sys.exit(run())
