#!/usr/bin/env python3
"""Exporta páginas SVG A4 para PNG e registra resolução e hashes."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import tempfile
from xml.etree import ElementTree as ET
import zlib

from fontes_incluidas import conferir_fontes, FONTES
from renderizador_incluido import carregar_renderizador


SVG_NS = "http://www.w3.org/2000/svg"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def tamanho_mm(value: str) -> float:
    match = re.fullmatch(r"\s*([0-9]+(?:\.[0-9]+)?)\s*(mm|cm|in|pt)\s*", value)
    if not match:
        raise ValueError("Declarar largura e altura físicas, por exemplo 210mm e 297mm.")
    factor = {"mm": 1, "cm": 10, "in": 25.4, "pt": 25.4 / 72}[match[2]]
    return float(match[1]) * factor


def conferir_svg(path: Path) -> None:
    raw = path.read_text(encoding="utf-8")
    if "<!DOCTYPE" in raw.upper() or "<!ENTITY" in raw.upper():
        raise ValueError(f"{path.name}: usar SVG sem entidades externas.")
    root = ET.fromstring(raw)
    if root.tag != f"{{{SVG_NS}}}svg":
        raise ValueError(f"{path.name}: raiz SVG ou namespace inválido.")
    width = tamanho_mm(root.get("width", ""))
    height = tamanho_mm(root.get("height", ""))
    if abs(width - 210) > 0.05 or abs(height - 297) > 0.05:
        raise ValueError(f"{path.name}: a página deve medir 210 × 297 mm.")
    box = [float(v) for v in re.split(r"[\s,]+", root.get("viewBox", "").strip()) if v]
    if len(box) != 4 or box[2] <= 0 or box[3] <= 0:
        raise ValueError(f"{path.name}: viewBox ausente ou inválido.")
    if abs(box[2] / box[3] - 210 / 297) > 0.001:
        raise ValueError(f"{path.name}: proporção do viewBox diferente de A4.")
    if re.search(r"\{\{[^{}]+\}\}", raw):
        raise ValueError(f"{path.name}: substituir os campos do template antes de exportar.")
    for node in root.iter():
        tag = node.tag.rsplit("}", 1)[-1]
        if tag in {"script", "foreignObject"}:
            raise ValueError(f"{path.name}: usar elementos SVG nativos, sem {tag}.")
        for key, value in node.attrib.items():
            if key.rsplit("}", 1)[-1] == "href" and not value.startswith(("#", "data:")):
                raise ValueError(f"{path.name}: incorporar o recurso externo {value!r}.")
    for match in re.finditer(r"url\(\s*['\"]?([^)'\"]+)", raw):
        if not match[1].strip().startswith(("#", "data:")):
            raise ValueError(f"{path.name}: recurso CSS externo não incorporado.")
    if not any(n.tag == f"{{{SVG_NS}}}text" for n in root.iter()):
        raise ValueError(f"{path.name}: manter texto selecionável no SVG.")


def renderizar(source: Path, output: Path, width: int, height: int, motor, fontes) -> None:
    # OTF Cooper Hewitt tem flags e pesos que confundem a seleção automática.
    # Os cabeçalhos do padrão usam Heavy normal. Carregar esse estilo explicitamente.
    paths = [str(FONTES / item['arquivo']) for item in fontes['fontes']
             if item['arquivo'].startswith('open-sans/')
             or item['arquivo'] == 'cooper-hewitt/CooperHewitt-Heavy.otf']
    root = ET.fromstring(source.read_text(encoding='utf-8'))
    # Evita arredondamento de 1 px do motor ao ajustar dimensões em milímetros.
    # O SVG original continua em A4 e seu viewBox é preservado.
    root.set('width', str(width))
    root.set('height', str(height))
    output.write_bytes(motor.svg_to_bytes(
        svg_string=ET.tostring(root, encoding='unicode'),
        dpi=96.0, skip_system_fonts=True,
        font_files=paths, font_family='Open Sans', sans_serif_family='Open Sans',
        shape_rendering='geometric_precision', text_rendering='geometric_precision',
        image_rendering='optimize_quality',
    ))


def ajustar_densidade(path: Path, dpi: int, expected: tuple[int, int]) -> None:
    raw = path.read_bytes()
    if not raw.startswith(PNG_SIGNATURE):
        raise ValueError("O renderizador não produziu um PNG válido.")
    offset = len(PNG_SIGNATURE)
    result = bytearray(PNG_SIGNATURE)
    dimensions = None
    ended = False
    while offset < len(raw):
        if offset + 12 > len(raw):
            raise ValueError("PNG truncado.")
        size = struct.unpack(">I", raw[offset:offset + 4])[0]
        end = offset + size + 12
        if end > len(raw):
            raise ValueError("Bloco PNG truncado.")
        kind = raw[offset + 4:offset + 8]
        payload = raw[offset + 8:offset + 8 + size]
        crc = struct.unpack(">I", raw[end - 4:end])[0]
        if zlib.crc32(kind + payload) & 0xFFFFFFFF != crc:
            raise ValueError("CRC inválido no PNG.")
        if kind != b"pHYs":
            result.extend(raw[offset:end])
        if kind == b"IHDR":
            dimensions = struct.unpack(">II", payload[:8])
            ppm = round(dpi / 0.0254)
            density = struct.pack(">IIB", ppm, ppm, 1)
            result.extend(struct.pack(">I", len(density)) + b"pHYs" + density)
            result.extend(struct.pack(">I", zlib.crc32(b"pHYs" + density) & 0xFFFFFFFF))
        if kind == b"IEND":
            ended = True
            break
        offset = end
    if dimensions != expected or not ended:
        raise ValueError(f"Dimensões PNG inesperadas ou arquivo incompleto: {dimensions}, esperado {expected}.")
    path.write_bytes(result)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("svg", nargs="+", type=Path, help="Um SVG por página A4.")
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--dpi", type=int, default=600)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--justificativa-paginas-extras", help="Justificativa de conteúdo essencial para mais de duas páginas.")
    args = parser.parse_args()
    if args.dpi < 300:
        parser.error("Usar pelo menos 300 dpi. O padrão de alta qualidade é 600 dpi.")
    if len(args.svg) > 2 and not (args.justificativa_paginas_extras or "").strip():
        parser.error("Mais de duas páginas exigem --justificativa-paginas-extras.")
    sources = [p.resolve() for p in args.svg]
    if len({p.stem for p in sources}) != len(sources):
        parser.error("Os arquivos de entrada devem ter nomes distintos.")
    output_dir = args.output_dir.resolve()
    manifest_path = output_dir / "manifesto-exportacao.json"
    try:
        for source in sources:
            conferir_svg(source)
        targets = [output_dir / f"{source.stem}.png" for source in sources]
        for target in [*targets, manifest_path]:
            if target.exists() and not args.overwrite:
                raise ValueError(f"Arquivo existente: {target}. Usar --overwrite para substituí-lo.")
        fontes = conferir_fontes()
        width, height = round(210 / 25.4 * args.dpi), round(297 / 25.4 * args.dpi)
        output_dir.mkdir(parents=True, exist_ok=True)
        records = []
        with carregar_renderizador() as (motor, motor_info), tempfile.TemporaryDirectory(prefix="infografico-", dir=output_dir) as temp:
            pending = []
            for number, (source, target) in enumerate(zip(sources, targets), 1):
                temporary = Path(temp) / target.name
                renderizar(source, temporary, width, height, motor, fontes)
                ajustar_densidade(temporary, args.dpi, (width, height))
                records.append({"pagina": number, "svg": str(source), "png": str(target), "largura_px": width, "altura_px": height, "dpi": args.dpi, "tamanho_mm": [210, 297], "svg_sha256": hashlib.sha256(source.read_bytes()).hexdigest(), "png_sha256": hashlib.sha256(temporary.read_bytes()).hexdigest()})
                pending.append((temporary, target))
            for temporary, target in pending:
                temporary.replace(target)
        manifest = {"paginas": len(records), "renderizador": motor_info, "fontes_incluidas": fontes, "fontes_carregadas": [item["arquivo"] for item in fontes["fontes"] if item["arquivo"].startswith("open-sans/") or item["arquivo"] == "cooper-hewitt/CooperHewitt-Heavy.otf"], "justificativa_paginas_extras": args.justificativa_paginas_extras, "arquivos": records}
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        for target in targets:
            print(f"PNG: {target} ({width} × {height} px, {args.dpi} dpi)")
        print(f"Manifesto: {manifest_path}")
        return 0
    except (OSError, ValueError, ET.ParseError, RuntimeError, ImportError) as error:
        parser.exit(1, f"ERRO: {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
