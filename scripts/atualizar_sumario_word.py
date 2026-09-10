"""Atualiza o sumário (TOC) e todos os campos de um documento DOCX usando o Word via COM.

Permite opcionalmente salvar como PDF.
Verifica se o placeholder 'O sumário será atualizado ao abrir o documento no Word'
foi devidamente eliminado do XML do documento.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import zipfile
from pathlib import Path


def atualizar_sumario_word(docx_path: Path, exportar_pdf: bool = True) -> tuple[bool, Path | None]:
    docx_path = docx_path.resolve()
    if not docx_path.exists():
        print(f"Erro: Arquivo não encontrado: {docx_path}")
        return False, None

    pdf_path = docx_path.with_suffix(".pdf") if exportar_pdf else None

    # Script PowerShell para invocar o Word COM
    export_cmd = f"$doc.ExportAsFixedFormat('{pdf_path}', 17)" if pdf_path else ""
    ps_code = f"""
$ErrorActionPreference = 'Stop'
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0

try {{
    $doc = $word.Documents.Open('{docx_path}')
    if ($doc.TablesOfContents.Count -ge 1) {{
        $doc.TablesOfContents.Item(1).Update()
    }}
    $doc.Fields.Update()
    $doc.Save()
    {export_cmd}
    $pageCount = $doc.ComputeStatistics(2) # 2 = wdStatisticPages
    Write-Output "SUCCESS: Paginas=$pageCount"
}}
catch {{
    Write-Error $_.Exception.Message
    exit 1
}}
finally {{
    if ($doc) {{ $doc.Close([ref]$false) }}
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}}
"""
    result = subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_code],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"Erro ao atualizar via Word COM: {result.stderr.strip()}")
        return False, None

    print(result.stdout.strip())

    # Verifica se o placeholder ainda existe no document.xml
    with zipfile.ZipFile(docx_path, "r") as z:
        doc_xml = z.read("word/document.xml").decode("utf-8")
        if "O sumário será atualizado ao abrir o documento no Word" in doc_xml:
            print("AVISO: O texto de placeholder do sumário ainda permanece no XML!")
            return False, pdf_path
        else:
            print("OK: Placeholder do sumário eliminado com sucesso. Sumário materializado no DOCX.")

    return True, pdf_path


def main():
    parser = argparse.ArgumentParser(description="Atualiza sumário do DOCX via Word COM e exporta PDF.")
    parser.add_argument("docx", help="Caminho do arquivo DOCX")
    parser.add_argument("--no-pdf", action="store_true", help="Não exportar para PDF")
    args = parser.parse_args()

    sucesso, pdf_path = atualizar_sumario_word(Path(args.docx), exportar_pdf=not args.no_pdf)
    if not sucesso:
        sys.exit(1)
    if pdf_path and pdf_path.exists():
        print(f"PDF exportado com sucesso: {pdf_path}")
    sys.exit(0)


if __name__ == "__main__":
    main()
