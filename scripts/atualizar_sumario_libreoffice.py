#!/usr/bin/env python3
"""Materializa o sumário de um DOCX usando o mecanismo de layout do LibreOffice."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import zipfile


PLACEHOLDER_SUMARIO = "O sumário será atualizado ao abrir o documento no Word."


def _localizar_program_dir() -> Path:
    configurado = os.environ.get("LIBREOFFICE_PROGRAM_DIR")
    candidatos = [
        Path(configurado) if configurado else None,
        Path("/usr/lib/libreoffice/program"),
        Path("/usr/lib64/libreoffice/program"),
    ]
    candidatos.extend(
        sorted((Path.home() / ".local/lib/libreoffice/opt").glob("libreoffice*/program"))
    )
    candidatos.extend(sorted(Path("/opt").glob("libreoffice*/program")))
    for candidato in candidatos:
        if candidato and (candidato / "uno.py").is_file():
            return candidato.resolve()
    raise RuntimeError(
        "Módulo UNO do LibreOffice não encontrado. Defina LIBREOFFICE_PROGRAM_DIR."
    )


def _porta_livre() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.bind(("127.0.0.1", 0))
        return int(servidor.getsockname()[1])


def _propriedade(uno, nome: str, valor):
    propriedade = uno.createUnoStruct("com.sun.star.beans.PropertyValue")
    propriedade.Name = nome
    propriedade.Value = valor
    return propriedade


def _validar_sumario_materializado(docx_path: Path) -> None:
    with zipfile.ZipFile(docx_path, "r") as arquivo:
        documento_xml = arquivo.read("word/document.xml").decode("utf-8")
    if PLACEHOLDER_SUMARIO in documento_xml:
        raise RuntimeError("O placeholder permaneceu no campo de sumário.")
    if "TOC1" not in documento_xml or "LISTA DE ANEXOS" not in documento_xml:
        raise RuntimeError("O LibreOffice não materializou as entradas do sumário.")


def atualizar_sumario_libreoffice(docx_path: Path, *, timeout: float = 30.0) -> int:
    """Atualiza os índices e sobrescreve ``docx_path`` somente após validação."""
    docx_path = docx_path.resolve()
    if not docx_path.is_file():
        raise FileNotFoundError(f"DOCX não encontrado: {docx_path}")
    executavel = shutil.which("libreoffice") or shutil.which("soffice")
    if not executavel:
        raise RuntimeError("Executável do LibreOffice não encontrado no PATH.")

    program_dir = _localizar_program_dir()
    sys.path.insert(0, str(program_dir))
    os.environ.setdefault(
        "URE_BOOTSTRAP",
        f"vnd.sun.star.pathname:{program_dir / 'fundamentalrc'}",
    )
    import uno

    porta = _porta_livre()
    processo = None
    desktop = None
    documento = None
    with tempfile.TemporaryDirectory(prefix="tcerj-sumario-") as diretorio:
        temporario = Path(diretorio)
        perfil = temporario / "perfil"
        perfil.mkdir()
        copia = temporario / "relatorio.docx"
        shutil.copy2(docx_path, copia)
        endereco = (
            f"socket,host=127.0.0.1,port={porta};urp;StarOffice.ServiceManager"
        )
        comando = [
            executavel,
            "--headless",
            f"--accept={endereco}",
            "--norestore",
            "--nodefault",
            "--nofirststartwizard",
            f"-env:UserInstallation={perfil.resolve().as_uri()}",
        ]

        try:
            contexto_local = uno.getComponentContext()
            resolvedor = contexto_local.ServiceManager.createInstanceWithContext(
                "com.sun.star.bridge.UnoUrlResolver",
                contexto_local,
            )
            limite = time.monotonic() + timeout
            ultima_excecao = None
            contexto = None
            for tentativa in range(2):
                processo = subprocess.Popen(
                    comando,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                while time.monotonic() < limite:
                    try:
                        contexto = resolvedor.resolve(
                            f"uno:socket,host=127.0.0.1,port={porta};urp;"
                            "StarOffice.ComponentContext"
                        )
                        break
                    except Exception as exc:  # pyuno expõe exceções dinâmicas
                        ultima_excecao = exc
                        if processo.poll() is not None:
                            break
                        time.sleep(0.1)
                else:
                    contexto = None
                if contexto is not None:
                    break
                if processo.poll() != 81 or tentativa == 1:
                    raise RuntimeError(
                        "Não foi possível conectar ao LibreOffice para atualizar o sumário."
                    ) from ultima_excecao
            else:
                raise RuntimeError("LibreOffice indisponível para atualizar o sumário.")

            desktop = contexto.ServiceManager.createInstanceWithContext(
                "com.sun.star.frame.Desktop",
                contexto,
            )
            documento = desktop.loadComponentFromURL(
                uno.systemPathToFileUrl(str(copia)),
                "_blank",
                0,
                (
                    _propriedade(uno, "Hidden", True),
                    _propriedade(uno, "UpdateDocMode", 3),
                ),
            )
            if documento is None:
                raise RuntimeError("O LibreOffice não conseguiu abrir o DOCX temporário.")
            indices = documento.getDocumentIndexes()
            quantidade = indices.getCount()
            if quantidade < 1:
                raise RuntimeError("Nenhum campo de sumário foi reconhecido no DOCX.")
            for indice in range(quantidade):
                indices.getByIndex(indice).update()
            documento.store()
            documento.close(True)
            documento = None
            _validar_sumario_materializado(copia)
            shutil.copy2(copia, docx_path)
            return quantidade
        finally:
            if documento is not None:
                try:
                    documento.close(True)
                except Exception:
                    pass
            if desktop is not None:
                try:
                    desktop.terminate()
                except Exception:
                    pass
            if processo is not None:
                try:
                    processo.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    processo.terminate()
                    try:
                        processo.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        processo.kill()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Materializa o sumário de um DOCX usando LibreOffice/UNO."
    )
    parser.add_argument("docx", type=Path)
    args = parser.parse_args()
    quantidade = atualizar_sumario_libreoffice(args.docx)
    print(f"Sumário materializado com sucesso ({quantidade} índice).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
