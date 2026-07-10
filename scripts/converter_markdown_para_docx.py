#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Converte arquivos Markdown em DOCX usando o template de estilos do Argos."""

from __future__ import annotations

import argparse
import glob
import logging
import os
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REFERENCE_DOCX = ROOT / "scripts/resources/template-base-estilos-sigiloso.docx"
DEFAULT_OUTPUT_DIR = Path(tempfile.gettempdir()) / "tcerj-igovti-2026/conversoes-docx"
TOC_MARKER_FILTER = ROOT / "scripts/resources/toc-marker.lua"

sys.path.insert(0, str(ROOT / "scripts/resources"))
from argos_utils import (  # noqa: E402
    aplicar_estilo_tabelas,
    cross_ref_figuras,
    cross_ref_tabelas,
    evitar_quebra_elementos,
    inserir_campo_sumario_docx,
    marcar_atualizacao_campos_docx,
    processar_quebras_pagina,
    substituir_underline_pandoc,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

try:
    import pypandoc
except ImportError:
    logger.error(
        "pypandoc não está instalado neste ambiente Python. Execute com: "
        "scripts/.venv/bin/python scripts/converter_markdown_para_docx.py"
    )
    sys.exit(1)

try:
    import docx  # noqa: F401
except ImportError:
    logger.error(
        "python-docx não está instalado neste ambiente Python. Execute com: "
        "scripts/.venv/bin/python scripts/converter_markdown_para_docx.py"
    )
    sys.exit(1)


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg"}


def resolve_path(path: str | Path) -> Path:
    candidate = Path(path).expanduser()
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


def expand_inputs(inputs: list[str], input_flag: str | None) -> list[Path]:
    raw_inputs = [*inputs]
    if input_flag:
        raw_inputs.append(input_flag)
    if not raw_inputs:
        raise ValueError("Informe ao menos um arquivo Markdown por argumento posicional ou --input.")

    md_paths: list[Path] = []
    for raw_input in raw_inputs:
        matches = glob.glob(str(resolve_path(raw_input)))
        if matches:
            md_paths.extend(Path(match) for match in sorted(matches))
        else:
            md_paths.append(resolve_path(raw_input))
    return md_paths


def expand_resource_paths(resources: list[str]) -> list[Path]:
    resolved: list[Path] = []
    for resource in resources:
        matches = glob.glob(str(resolve_path(resource)), recursive=True)
        if matches:
            resolved.extend(Path(match) for match in sorted(matches))
        else:
            resolved.append(resolve_path(resource))
    return resolved


def copy_image(src: Path, dest_dir: Path) -> None:
    if src.suffix.lower() not in IMAGE_EXTENSIONS:
        return
    dest = dest_dir / src.name
    if not dest.exists():
        shutil.copy2(src, dest)


def collect_resources(resources: list[str], temp_resources_dir: Path) -> list[Path]:
    temp_img_dir = temp_resources_dir / "img"
    temp_img_dir.mkdir(parents=True, exist_ok=True)
    resource_paths = expand_resource_paths(resources)

    for resource in resource_paths:
        if not resource.exists():
            logger.warning("Recurso não encontrado: %s", resource)
            continue
        if resource.is_dir():
            for child in resource.rglob("*"):
                if child.is_file():
                    copy_image(child, temp_img_dir)
        elif resource.suffix.lower() == ".zip":
            try:
                with tempfile.TemporaryDirectory() as unzip_tmp:
                    with zipfile.ZipFile(resource, "r") as zip_ref:
                        zip_ref.extractall(unzip_tmp)
                    for child in Path(unzip_tmp).rglob("*"):
                        if child.is_file():
                            copy_image(child, temp_img_dir)
            except Exception as exc:
                logger.error("Erro ao extrair ZIP de recursos %s: %s", resource, exc)
        else:
            copy_image(resource, temp_img_dir)

    for child in temp_img_dir.rglob("*"):
        if child.is_file():
            copy_image(child, temp_resources_dir)

    return resource_paths


def preprocess_markdown(input_path: Path) -> str:
    content = input_path.read_text(encoding="utf-8")
    content = cross_ref_figuras(content)
    content = cross_ref_tabelas(content)
    content = inserir_campo_sumario_docx(content)
    content = processar_quebras_pagina(content)
    return substituir_underline_pandoc(content)


def convert_one(input_path: Path, output_path: Path, reference_docx: Path, resource_files: list[str]) -> None:
    if not input_path.exists():
        raise FileNotFoundError(f"Arquivo Markdown de entrada não encontrado: {input_path}")
    if input_path.suffix.lower() != ".md":
        raise ValueError(f"Arquivo de entrada não é Markdown (.md): {input_path}")
    if not reference_docx.exists():
        raise FileNotFoundError(f"DOCX de referência não encontrado: {reference_docx}")

    logger.info("Lendo Markdown: %s", input_path)
    processed_markdown = preprocess_markdown(input_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", encoding="utf-8", delete=False) as temp_md:
        temp_md.write(processed_markdown)
        temp_md_path = Path(temp_md.name)

    try:
        with tempfile.TemporaryDirectory() as temp_resources:
            temp_resources_dir = Path(temp_resources)
            collect_resources(resource_files, temp_resources_dir)
            resource_paths = [
                ROOT,
                temp_resources_dir,
                input_path.parent,
                reference_docx.parent,
            ]
            resource_path_arg = "--resource-path=" + os.pathsep.join(str(path) for path in resource_paths)
            extra_args = [
                "--figure-caption-position=above",
                "--reference-doc=" + str(reference_docx),
                resource_path_arg,
            ]
            if TOC_MARKER_FILTER.exists():
                extra_args.append("--lua-filter=" + str(TOC_MARKER_FILTER))

            logger.info("Convertendo para DOCX: %s", output_path)
            pypandoc.convert_file(
                str(temp_md_path),
                to="docx",
                outputfile=str(output_path),
                extra_args=extra_args,
            )

        logger.info("Aplicando estilos de tabela no DOCX...")
        aplicar_estilo_tabelas(str(output_path))
        logger.info("Ajustando quebras de figuras, tabelas e fontes...")
        evitar_quebra_elementos(str(output_path))
        logger.info("Marcando campos do DOCX para atualização ao abrir no Word...")
        marcar_atualizacao_campos_docx(str(output_path))
        logger.info("DOCX gerado: %s", output_path)
    finally:
        temp_md_path.unlink(missing_ok=True)


def output_path_for(input_path: Path, output: str | None, output_dir: Path, multiple_inputs: bool) -> Path:
    if output:
        if multiple_inputs:
            raise ValueError("--output só pode ser usado com um único arquivo de entrada.")
        return resolve_path(output)
    return output_dir / input_path.with_suffix(".docx").name


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="*", help="Arquivos Markdown de entrada. Aceita padrões glob.")
    parser.add_argument("--input", default=None, help="Arquivo Markdown de entrada alternativo.")
    parser.add_argument("--output", default=None, help="Arquivo DOCX de saída. Use apenas com uma entrada.")
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help=f"Diretório de saída quando --output não é informado (padrão: {DEFAULT_OUTPUT_DIR}).",
    )
    parser.add_argument(
        "--reference-docx",
        default=str(DEFAULT_REFERENCE_DOCX),
        help="DOCX de referência de estilos.",
    )
    parser.add_argument(
        "--resource-files",
        "--resource-dirs",
        nargs="*",
        default=[],
        dest="resource_files",
        help="Arquivos, diretórios ou padrões glob com imagens usadas pelo Markdown.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        input_paths = expand_inputs(args.inputs, args.input)
        output_dir = resolve_path(args.output_dir)
        reference_docx = resolve_path(args.reference_docx)
        multiple_inputs = len(input_paths) > 1

        for input_path in input_paths:
            output_path = output_path_for(input_path, args.output, output_dir, multiple_inputs)
            convert_one(input_path, output_path, reference_docx, args.resource_files)
        return 0
    except Exception as exc:
        logger.error("%s", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
