#!/usr/bin/env python3
"""Infraestrutura compartilhada do pipeline rastreável da auditoria iGovTI."""

from __future__ import annotations

import hashlib
import json
import logging
import shlex
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from openpyxl import Workbook


CENARIOS = (
    "01-pos-ajuste-inicial",
    "02-pos-avaliacao-evidencias",
    "03-pos-comentarios-gestor",
)


def agora() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def descrever_arquivo(path: Path) -> dict[str, object]:
    resolved = path.expanduser().resolve()
    if resolved.is_dir():
        digest = hashlib.sha256()
        count = 0
        size = 0
        for child in sorted(item for item in resolved.rglob("*") if item.is_file()):
            relative = child.relative_to(resolved).as_posix()
            digest.update(relative.encode("utf-8"))
            child_size = child.stat().st_size
            digest.update(str(child_size).encode("ascii"))
            digest.update(sha256(child).encode("ascii"))
            count += 1
            size += child_size
        return {
            "path": str(resolved), "exists": True, "kind": "directory",
            "files": count, "size": size, "sha256": digest.hexdigest(),
        }
    if not resolved.is_file():
        return {"path": str(resolved), "exists": False}
    stat = resolved.stat()
    return {
        "path": str(resolved),
        "exists": True,
        "size": stat.st_size,
        "sha256": sha256(resolved),
    }


@dataclass(frozen=True)
class Stage:
    key: str
    title: str
    command: tuple[str, ...] = ()
    inputs: tuple[Path, ...] = ()
    outputs: tuple[Path, ...] = ()
    scenario: str | None = None
    optional_inputs: tuple[Path, ...] = ()
    metadata: dict[str, object] = field(default_factory=dict)


class Manifest:
    """Manifesto persistente, sem identificador de run, com eventos append-only."""

    def __init__(self, control_dir: Path) -> None:
        self.control_dir = control_dir
        self.path = control_dir / "manifesto-pipeline-auditoria.json"
        self.events_path = control_dir / "eventos-pipeline-auditoria.jsonl"
        self.logs_dir = control_dir / "logs"
        control_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        if self.path.is_file():
            self.data = json.loads(self.path.read_text(encoding="utf-8"))
        else:
            self.data = {
                "schema_version": 1,
                "pipeline": "igovti-2026",
                "created_at": agora(),
                "updated_at": agora(),
                "status": "pending",
                "stages": {},
            }

    def save(self) -> None:
        self.data["updated_at"] = agora()
        temp = self.path.with_suffix(".tmp")
        temp.write_text(json.dumps(self.data, ensure_ascii=False, indent=2), encoding="utf-8")
        temp.replace(self.path)

    def event(self, event: str, **payload: object) -> None:
        record = {"ts": agora(), "event": event, **payload}
        with self.events_path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")

    def stage_record(self, stage: Stage) -> dict[str, object]:
        return self.data.setdefault("stages", {}).setdefault(
            stage.key,
            {"key": stage.key, "title": stage.title, "scenario": stage.scenario, "status": "pending"},
        )

    def outputs_match(self, stage: Stage) -> bool:
        record = self.stage_record(stage)
        expected = record.get("outputs") or []
        if record.get("status") != "completed":
            return False
        old_inputs = record.get("inputs") or []
        if len(old_inputs) != len(stage.inputs):
            return False
        current_inputs = [descrever_arquivo(path) for path in stage.inputs]
        for current, old in zip(current_inputs, old_inputs):
            if not current.get("exists") or current.get("kind") != old.get("kind"):
                return False
            if current.get("sha256") != old.get("sha256"):
                return False
        if not stage.outputs:
            output_dirs = [Path(str(path)) for path in stage.metadata.get("output_dirs", [])]
            if output_dirs:
                old_dirs = record.get("output_directories") or []
                current_dirs = [descrever_arquivo(path) for path in output_dirs]
                return len(old_dirs) == len(current_dirs) and all(
                    current.get("exists") and current.get("sha256") == old.get("sha256")
                    for current, old in zip(current_dirs, old_dirs)
                )
            return True
        if len(expected) != len(stage.outputs):
            return False
        current = [descrever_arquivo(path) for path in stage.outputs]
        return all(
            item.get("exists") and item.get("sha256") == old.get("sha256")
            for item, old in zip(current, expected)
        )

    def start(self, stage: Stage) -> Path:
        record = self.stage_record(stage)
        record.update(
            {
                "status": "running",
                "started_at": agora(),
                "command": list(stage.command),
                "inputs": [descrever_arquivo(path) for path in stage.inputs],
                "metadata": stage.metadata,
            }
        )
        log_path = self.logs_dir / f"{stage.key}.log"
        record["log"] = str(log_path)
        self.data["status"] = "running"
        self.save()
        self.event("stage_started", stage=stage.key, scenario=stage.scenario, command=list(stage.command))
        return log_path

    def finish(self, stage: Stage, returncode: int = 0) -> None:
        record = self.stage_record(stage)
        outputs = [descrever_arquivo(path) for path in stage.outputs]
        missing = [str(path) for path, item in zip(stage.outputs, outputs) if not item.get("exists")]
        if returncode == 0 and missing:
            raise RuntimeError(f"A etapa {stage.key} não produziu: {', '.join(missing)}")
        record.update(
            {
                "status": "completed" if returncode == 0 else "failed",
                "finished_at": agora(),
                "returncode": returncode,
                "outputs": outputs,
                "output_directories": [
                    descrever_arquivo(Path(str(path)))
                    for path in stage.metadata.get("output_dirs", [])
                ],
            }
        )
        self.save()
        self.event("stage_finished", stage=stage.key, scenario=stage.scenario, returncode=returncode)

    def awaiting(self, stage: Stage, missing: Iterable[Path]) -> None:
        record = self.stage_record(stage)
        record.update(
            {
                "status": "awaiting_input",
                "finished_at": agora(),
                "missing_inputs": [str(path) for path in missing],
            }
        )
        self.data["status"] = "awaiting_input"
        self.save()
        self.event("pipeline_awaiting_input", stage=stage.key, missing_inputs=record["missing_inputs"])

    def awaiting_review(self, stage: Stage) -> None:
        record = self.stage_record(stage)
        record.update(
            {
                "status": "awaiting_review",
                "finished_at": agora(),
                "review_artifact": str((stage.metadata or {}).get("review_artifact", "")),
            }
        )
        self.data["status"] = "awaiting_review"
        self.save()
        self.event(
            "pipeline_awaiting_review",
            stage=stage.key,
            review_artifact=record["review_artifact"],
        )

    def adopt(self, stage: Stage) -> None:
        record = self.stage_record(stage)
        for stale_key in ("returncode", "error", "missing_inputs", "review_artifact", "log"):
            record.pop(stale_key, None)
        record.update(
            {
                "status": "completed",
                "adopted_existing": True,
                "started_at": agora(),
                "finished_at": agora(),
                "command": list(stage.command),
                "inputs": [descrever_arquivo(path) for path in stage.inputs],
                "outputs": [descrever_arquivo(path) for path in stage.outputs],
                "output_directories": [
                    descrever_arquivo(Path(str(path)))
                    for path in stage.metadata.get("output_dirs", [])
                ],
                "metadata": stage.metadata,
            }
        )
        self.save()
        self.event("stage_adopted", stage=stage.key, scenario=stage.scenario)

    def complete(self) -> None:
        self.data["status"] = "completed"
        self.data["finished_at"] = agora()
        inventory: list[dict[str, object]] = []
        for stage_key, stage in self.data.get("stages", {}).items():
            for output in stage.get("outputs") or []:
                inventory.append(
                    {
                        "stage": stage_key,
                        "scenario": stage.get("scenario") or "",
                        **output,
                    }
                )
            for directory in (stage.get("metadata") or {}).get("output_dirs", []):
                output_dir = Path(str(directory))
                if not output_dir.is_dir():
                    continue
                for path in sorted(item for item in output_dir.rglob("*") if item.is_file()):
                    inventory.append(
                        {
                            "stage": stage_key,
                            "scenario": stage.get("scenario") or "",
                            **descrever_arquivo(path),
                        }
                    )
        inventory_json = self.control_dir / "inventario-artefatos.json"
        inventory_xlsx = self.control_dir / "inventario-artefatos.xlsx"
        inventory_json.write_text(json.dumps(inventory, ensure_ascii=False, indent=2), encoding="utf-8")
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Artefatos"
        headers = ["stage", "scenario", "path", "exists", "size", "sha256"]
        sheet.append(headers)
        for item in inventory:
            sheet.append([item.get(header, "") for header in headers])
        sheet.freeze_panes = "A2"
        workbook.save(inventory_xlsx)
        self.data["inventory"] = {"json": str(inventory_json), "xlsx": str(inventory_xlsx)}
        self.save()
        self.event("pipeline_finished", status="completed")


class PipelineRunner:
    def __init__(self, manifest: Manifest, *, dry_run: bool = False, force: set[str] | None = None, adopt_existing: bool = False) -> None:
        self.manifest = manifest
        self.dry_run = dry_run
        self.force = force or set()
        self.adopt_existing = adopt_existing

    def run(self, stage: Stage) -> str:
        if self.dry_run:
            logging.info("[DRY-RUN] %s", stage.title)
            logging.info("[DRY-RUN] Comando: %s", shlex.join(stage.command))
            return "planned"
        missing = [path for path in stage.inputs if not path.exists()]
        if missing:
            raise FileNotFoundError(f"Entradas ausentes em {stage.key}: {', '.join(map(str, missing))}")
        optional_missing = [path for path in stage.optional_inputs if not path.exists()]
        if optional_missing:
            self.manifest.awaiting(stage, optional_missing)
            return "awaiting_input"
        if stage.key not in self.force and self.manifest.outputs_match(stage):
            logging.info("Etapa já concluída e íntegra: %s", stage.title)
            self.manifest.event("stage_skipped", stage=stage.key, reason="matching_manifest")
            return "skipped"
        record = self.manifest.stage_record(stage)
        if not stage.outputs and record.get("status") == "completed" and stage.key not in self.force:
            raise RuntimeError(
                f"As entradas de {stage.key} mudaram desde a conclusão; a etapa não será reexecutada "
                "automaticamente porque seus produtos acessórios devem ser preservados."
            )
        existing = [path for path in stage.outputs if path.exists()]
        existing_dirs = [
            Path(str(path)) for path in stage.metadata.get("output_dirs", [])
            if Path(str(path)).is_dir() and any(Path(str(path)).iterdir())
        ]
        if self.adopt_existing and not stage.outputs and existing_dirs:
            logging.info("Adotando diretórios de produtos existentes: %s", stage.title)
            self.manifest.adopt(stage)
            return "adopted"
        if self.adopt_existing and stage.outputs and len(existing) == len(stage.outputs):
            logging.info("Adotando produtos existentes sem sobrescrevê-los: %s", stage.title)
            self.manifest.adopt(stage)
            return "adopted"
        retomando_revisao = record.get("status") == "awaiting_review"
        if existing and stage.key not in self.force and not retomando_revisao:
            raise RuntimeError(
                f"Produtos existentes sem correspondência íntegra no manifesto em {stage.key}; "
                "não serão sobrescritos: " + ", ".join(map(str, existing))
            )
        if existing_dirs and stage.key not in self.force and not retomando_revisao:
            raise RuntimeError(
                f"Diretórios de produtos existentes sem correspondência íntegra no manifesto em {stage.key}; "
                "não serão sobrescritos: " + ", ".join(map(str, existing_dirs))
            )
        logging.info("%s", stage.title)
        logging.info("Comando: %s", shlex.join(stage.command))
        for output in stage.outputs:
            output.parent.mkdir(parents=True, exist_ok=True)
        log_path = self.manifest.start(stage)
        with log_path.open("w", encoding="utf-8") as log:
            proc = subprocess.Popen(
                list(stage.command),
                cwd=Path(__file__).resolve().parents[1],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
            assert proc.stdout is not None
            for line in proc.stdout:
                print(line, end="", flush=True)
                log.write(line)
                log.flush()
            returncode = proc.wait()
            proc.stdout.close()
        if returncode == 3:
            self.manifest.awaiting_review(stage)
            return "awaiting_review"
        self.manifest.finish(stage, returncode)
        if returncode:
            raise subprocess.CalledProcessError(returncode, stage.command)
        return "completed"
