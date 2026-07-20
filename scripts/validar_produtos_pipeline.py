#!/usr/bin/env python3
"""Valida produtos essenciais e avisos de recursos ao final do pipeline."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


WARNINGS = ("recurso não encontrado", "resource not found", "missing resource", "imagem não encontrada")
FAILURES = ("falha ao processar relatório", "traceback (most recent call last)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--required", nargs="+", type=Path, required=True)
    parser.add_argument("--report-dir", action="append", type=Path, default=[])
    parser.add_argument("--auditados-json", type=Path, help="JSON da auditoria usado para exigir um relatório por auditado.")
    parser.add_argument("--logs-dir", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    missing = [str(path) for path in args.required if not path.is_file() or path.stat().st_size == 0]
    report_counts = {str(path): len(list(path.glob("*.docx"))) if path.is_dir() else 0 for path in args.report_dir}
    empty_reports = [path for path, count in report_counts.items() if count == 0]
    expected_report_count = None
    if args.auditados_json:
        with args.auditados_json.open(encoding="utf-8") as handle:
            auditados = json.load(handle)
        if not isinstance(auditados, dict):
            raise ValueError("--auditados-json deve conter um objeto indexado por auditado")
        expected_report_count = len(auditados)
    incomplete_reports = [
        path for path, count in report_counts.items()
        if expected_report_count is not None and count != expected_report_count
    ]
    warnings: list[dict[str, object]] = []
    failures: list[dict[str, object]] = []
    if args.logs_dir and args.logs_dir.is_dir():
        for log in sorted(args.logs_dir.glob("*.log")):
            for number, line in enumerate(log.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
                if any(marker in line.casefold() for marker in WARNINGS):
                    warnings.append({"log": str(log), "line": number, "message": line.strip()})
                if any(marker in line.casefold() for marker in FAILURES):
                    failures.append({"log": str(log), "line": number, "message": line.strip()})
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "ok" if not missing and not empty_reports and not incomplete_reports and not warnings and not failures else "error",
        "required_files": len(args.required),
        "missing_or_empty": missing,
        "report_counts": report_counts,
        "expected_report_count": expected_report_count,
        "empty_report_dirs": empty_reports,
        "incomplete_report_dirs": incomplete_reports,
        "resource_warnings": warnings,
        "execution_failures": failures,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
