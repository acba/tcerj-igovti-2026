#!/usr/bin/env python3
"""Converte documentos Word de uma pasta para PDF.

O script aceita arquivos .docx e .doc, cria uma subpasta ``pdf`` por padrao e
pula arquivos ja convertidos, salvo quando ``--overwrite`` for informado.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


WORD_EXTENSIONS = {".docx", ".doc"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir", type=Path, help="Pasta com arquivos .docx/.doc a converter.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Pasta de saida dos PDFs. Se omitida, usa a subpasta 'pdf' da pasta de entrada.",
    )
    parser.add_argument("--overwrite", action="store_true", help="Sobrescreve PDFs existentes.")
    parser.add_argument("--recursive", action="store_true", help="Busca documentos Word em subpastas.")
    parser.add_argument("--docx-only", action="store_true", help="Converte apenas arquivos .docx.")
    parser.add_argument(
        "--converter",
        choices=["auto", "libreoffice", "word", "onlyoffice"],
        default="auto",
        help="Conversor a usar. 'auto' utiliza LibreOffice no Linux e Microsoft Word no Windows.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Lista as conversoes sem gerar PDFs.")
    return parser.parse_args()


def iter_word_files(input_dir: Path, *, recursive: bool, docx_only: bool) -> list[Path]:
    extensions = {".docx"} if docx_only else WORD_EXTENSIONS
    pattern_iter = input_dir.rglob("*") if recursive else input_dir.iterdir()
    files = [
        path
        for path in pattern_iter
        if path.is_file()
        and path.suffix.casefold() in extensions
        and not path.name.startswith("~$")
    ]
    return sorted(files, key=lambda path: str(path).casefold())


def relative_pdf_path(source: Path, input_dir: Path, output_dir: Path, *, recursive: bool) -> Path:
    if not recursive:
        return output_dir / f"{source.stem}.pdf"
    relative_parent = source.relative_to(input_dir).parent
    return output_dir / relative_parent / f"{source.stem}.pdf"


def converter_com_libreoffice(source: Path, target: Path) -> tuple[bool, str]:
    executable = shutil.which("soffice") or shutil.which("libreoffice")
    if not executable:
        return False, "LibreOffice/soffice nao encontrado"

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        safe_source = tmp_path / f"document{source.suffix.lower()}"
        shutil.copyfile(source, safe_source)
        try:
            result = subprocess.run(
                [
                    executable,
                    "--headless",
                    "--convert-to",
                    "pdf",
                    "--outdir",
                    str(tmp_path),
                    str(safe_source),
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=180,
            )
        except subprocess.TimeoutExpired:
            return False, "timeout ao converter com LibreOffice/soffice"
        except OSError as exc:
            return False, f"erro ao executar LibreOffice/soffice: {exc}"

        if result.returncode != 0:
            detail = (result.stderr or result.stdout or "").strip()
            return False, f"LibreOffice/soffice retornou erro: {detail or result.returncode}"

        converted = tmp_path / f"{safe_source.stem}.pdf"
        if not converted.is_file():
            candidates = sorted(tmp_path.glob("*.pdf"))
            if not candidates:
                return False, "LibreOffice/soffice nao gerou arquivo PDF"
            converted = candidates[0]

        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(converted, target)
        return True, ""


def converter_com_word(source: Path, target: Path) -> tuple[bool, str]:
    if os.name != "nt":
        return False, "Microsoft Word COM disponivel apenas no Windows"
    if not shutil.which("powershell.exe"):
        return False, "powershell.exe nao encontrado para acionar Microsoft Word"

    script = r"""
param([string]$Source, [string]$Target)
$ErrorActionPreference = 'Stop'
$word = $null
$doc = $null
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $sourcePath = (Resolve-Path -LiteralPath $Source).Path
    $doc = $word.Documents.Open([ref]$sourcePath, [ref]$false, [ref]$true, [ref]$false)
    if ($null -eq $doc) {
        $doc = $word.ActiveDocument
    }
    if ($null -eq $doc) {
        throw 'Microsoft Word nao abriu o documento'
    }
    $doc.ExportAsFixedFormat($Target, 17)
} finally {
    if ($null -ne $doc) {
        $doc.Close($false) | Out-Null
        [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($doc) | Out-Null
    }
    if ($null -ne $word) {
        $word.Quit() | Out-Null
        [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($word) | Out-Null
    }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
"""

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        local_source = tmp_path / f"source{source.suffix.lower()}"
        local_target = tmp_path / "converted.pdf"
        script_path = tmp_path / "convert-word-to-pdf.ps1"
        try:
            shutil.copyfile(source, local_source)
            script_path.write_text(script, encoding="utf-8")
            result = subprocess.run(
                [
                    "powershell.exe",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(script_path),
                    "-Source",
                    str(local_source),
                    "-Target",
                    str(local_target),
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=240,
            )
        except subprocess.TimeoutExpired:
            return False, "timeout ao converter com Microsoft Word"
        except OSError as exc:
            return False, f"erro ao acionar Microsoft Word: {exc}"

        if result.returncode != 0:
            detail = (result.stderr or result.stdout or "").strip()
            return False, f"Microsoft Word retornou erro: {detail or result.returncode}"
        if not local_target.is_file():
            return False, "Microsoft Word nao gerou arquivo PDF"

        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(local_target, target)
        return True, ""


def converter_com_onlyoffice(source: Path, target: Path) -> tuple[bool, str]:
    x2t_system = Path("/opt/onlyoffice/desktopeditors/converter/x2t")
    if not x2t_system.is_file():
        return False, "x2t do ONLYOFFICE nao encontrado em /opt/onlyoffice/desktopeditors/converter/x2t"

    user_fonts = Path.home() / ".local/share/onlyoffice/desktopeditors/data/fonts/AllFonts.js"
    if not user_fonts.is_file():
        return False, (
            "Cache de fontes do ONLYOFFICE nao encontrado em "
            f"{user_fonts}. "
            "Abra o ONLYOFFICE DesktopEditors ao menos uma vez no ambiente grafico "
            "para inicializar o cache de fontes, ou use '--converter libreoffice'."
        )

    oo_runtime = Path(tempfile.gettempdir()) / "onlyoffice_converter_runtime"
    converter_dir = oo_runtime / "converter"
    editors_dir = oo_runtime / "editors"
    common_dir = editors_dir / "sdkjs/common"

    if not (converter_dir / "x2t").exists() or not (common_dir / "AllFonts.js").exists():
        converter_dir.mkdir(parents=True, exist_ok=True)
        common_dir.mkdir(parents=True, exist_ok=True)
        (oo_runtime / "dictionaries").mkdir(parents=True, exist_ok=True)

        for item in Path("/opt/onlyoffice/desktopeditors/converter").glob("*"):
            link = converter_dir / item.name
            if not link.exists():
                link.symlink_to(item)

        for item in Path("/opt/onlyoffice/desktopeditors/editors").glob("*"):
            link = editors_dir / item.name
            if item.name != "sdkjs" and not link.exists():
                link.symlink_to(item)

        for item in Path("/opt/onlyoffice/desktopeditors/editors/sdkjs").glob("*"):
            link = editors_dir / "sdkjs" / item.name
            if item.name != "common" and not link.exists():
                link.symlink_to(item)

        for item in Path("/opt/onlyoffice/desktopeditors/editors/sdkjs/common").glob("*"):
            link = common_dir / item.name
            if not link.exists():
                link.symlink_to(item)

        for item in Path("/opt/onlyoffice/desktopeditors/dictionaries").glob("*"):
            link = oo_runtime / "dictionaries" / item.name
            if not link.exists():
                link.symlink_to(item)

        shutil.copyfile(user_fonts, common_dir / "AllFonts.js")
    elif user_fonts.stat().st_mtime > (common_dir / "AllFonts.js").stat().st_mtime:
        shutil.copyfile(user_fonts, common_dir / "AllFonts.js")

    target.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    curr_ld = env.get("LD_LIBRARY_PATH", "")
    env["LD_LIBRARY_PATH"] = f"{converter_dir}:{curr_ld}"

    try:
        result = subprocess.run(
            [str(converter_dir / "x2t"), str(source.resolve()), str(target.resolve())],
            cwd=str(converter_dir),
            env=env,
            capture_output=True,
            text=True,
            timeout=180,
        )
    except subprocess.TimeoutExpired:
        return False, "timeout ao converter com ONLYOFFICE x2t"
    except OSError as exc:
        return False, f"erro ao executar ONLYOFFICE x2t: {exc}"

    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()
        return False, f"ONLYOFFICE x2t retornou codigo {result.returncode}: {detail}"

    if not target.is_file() or target.stat().st_size == 0:
        return False, "ONLYOFFICE x2t nao gerou arquivo PDF valido"

    return True, ""


def converter_documento(source: Path, target: Path, converter: str) -> tuple[bool, str]:
    if converter == "libreoffice":
        return converter_com_libreoffice(source, target)
    if converter == "word":
        return converter_com_word(source, target)
    if converter == "onlyoffice":
        print(
            "[AVISO] O motor headless do ONLYOFFICE (x2t) no Linux pode apresentar inconsistências "
            "de codificação de fontes TrueType em alguns visualizadores. Recomenda-se LibreOffice.",
            file=sys.stderr,
        )
        return converter_com_onlyoffice(source, target)

    # Modo "auto": no Windows prioriza Word COM; no Linux prioriza LibreOffice (estável e com fontes do sistema)
    if os.name == "nt":
        ok, error = converter_com_word(source, target)
        if ok:
            return True, ""
        lo_ok, lo_error = converter_com_libreoffice(source, target)
        if lo_ok:
            return True, ""
        return False, f"Word: {error}; LibreOffice: {lo_error}"

    ok, error = converter_com_libreoffice(source, target)
    if ok:
        return True, ""

    fallback_ok, fallback_error = converter_com_word(source, target)
    if fallback_ok:
        return True, ""
    return False, f"{error}; fallback Microsoft Word: {fallback_error}"


def main() -> int:
    args = parse_args()
    input_dir = args.input_dir.expanduser().resolve()
    if not input_dir.is_dir():
        print(f"ERRO: pasta de entrada nao encontrada: {input_dir}", file=sys.stderr)
        return 1

    output_dir = (args.output_dir or (input_dir / "pdf")).expanduser().resolve()
    files = iter_word_files(input_dir, recursive=args.recursive, docx_only=args.docx_only)
    converted = 0
    skipped = 0
    errors = 0

    print(f"Pasta de entrada: {input_dir}")
    print(f"Pasta de saida: {output_dir}")
    print(f"Arquivos encontrados: {len(files)}")

    for source in files:
        target = relative_pdf_path(source, input_dir, output_dir, recursive=args.recursive)
        if target.exists() and not args.overwrite:
            print(f"[SKIP] {source.name} -> {target}")
            skipped += 1
            continue

        print(f"[RUN] {source} -> {target}")
        if args.dry_run:
            continue

        ok, error = converter_documento(source, target, args.converter)
        if ok:
            print(f"[OK] {target}")
            converted += 1
        else:
            print(f"[ERRO] {source}: {error}", file=sys.stderr)
            errors += 1

    print(
        "Resumo: "
        f"encontrados={len(files)}, convertidos={converted}, pulados={skipped}, erros={errors}"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
