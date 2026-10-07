#!/usr/bin/env python3
"""Valida UTF-8, fontes e exportação PNG no Windows, sem programas gráficos."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import struct
import subprocess
import sys
from xml.etree import ElementTree as ET
import zlib

SCRIPTS = Path(__file__).resolve().parent
SVG_NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG_NS)


def exigir(condition, message):
    if not condition:
        raise ValueError(message)


def conferir_png(path):
    raw = path.read_bytes()
    exigir(raw[:8] == b'\x89PNG\r\n\x1a\n', 'Assinatura PNG inválida.')
    offset = 8
    dimensions = density = None
    ended = False
    while offset < len(raw):
        exigir(offset + 12 <= len(raw), 'Bloco PNG truncado.')
        length = struct.unpack('>I', raw[offset:offset + 4])[0]
        end = offset + length + 12
        exigir(end <= len(raw), 'Conteúdo PNG truncado.')
        kind = raw[offset + 4:offset + 8]
        payload = raw[offset + 8:end - 4]
        crc = struct.unpack('>I', raw[end - 4:end])[0]
        exigir(zlib.crc32(kind + payload) & 0xFFFFFFFF == crc, 'CRC PNG divergente.')
        if kind == b'IHDR': dimensions = struct.unpack('>II', payload[:8])
        if kind == b'pHYs': density = struct.unpack('>IIB', payload)
        if kind == b'IEND':
            ended = True
            break
        offset = end
    exigir(ended and dimensions == (4961, 7016), 'Dimensões diferentes de A4 a 600 dpi.')
    exigir(density == (round(600 / 0.0254), round(600 / 0.0254), 1), 'Densidade diferente de 600 dpi.')
    return {'arquivo': str(path), 'dimensoes': list(dimensions), 'dpi': 600, 'sha256': hashlib.sha256(raw).hexdigest()}


def executar(script, arguments, environment):
    result = subprocess.run([sys.executable, '-S', str(SCRIPTS / script), *map(str, arguments)], env=environment, capture_output=True, encoding='utf-8', errors='replace', timeout=240)
    if result.returncode:
        raise RuntimeError(f'{script}: {result.stderr.strip() or result.stdout.strip()}')
    return result.stdout.strip()


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(errors='backslashreplace')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', required=True, type=Path)
    parser.add_argument('--plataforma-atual', action='store_true', help='Executa em outro sistema e registra esse sistema, sem validar Windows.')
    args = parser.parse_args()
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    report_path = out / 'validacao-compatibilidade.json'
    if report_path.exists():
        parser.error('Relatório já existe. Escolher outra pasta de saída para conservar o registro anterior.')
    native_windows = sys.platform == 'win32' and platform.system() == 'Windows'
    report = {'gerado_em_utc': datetime.now(timezone.utc).isoformat(), 'sistema': platform.system(), 'arquitetura': platform.machine(), 'python': sys.version, 'executado_no_windows': native_windows, 'validacao_windows': 'pendente', 'status': 'iniciada', 'verificacoes': []}
    exit_code = 1
    try:
        if not native_windows and not args.plataforma_atual:
            report['status'] = 'nao_executada'
            report['motivo'] = 'Executar no Windows. --plataforma-atual verifica somente o sistema real em execução.'
            exit_code = 2
            return exit_code
        from fontes_incluidas import conferir_fontes
        from renderizador_incluido import carregar_renderizador
        manifest = conferir_fontes()
        with carregar_renderizador() as (engine, engine_info):
            report['renderizador'] = engine_info
            exigir(engine.__version__ == engine_info['versao'], 'Versão do motor divergente.')
            if native_windows:
                exigir('win_' in engine_info['wheel'], 'Motor de outra plataforma selecionado no Windows.')
        report['verificacoes'].append({'item': 'motor e hashes das fontes', 'status': 'aprovado', 'fontes_conferidas': len(manifest['fontes'])})
        folder = out / 'caminho com espaços e acentuação'
        folder.mkdir(exist_ok=True)
        original = folder / 'Fiscalização — São João.svg'
        embedded = folder / 'Fiscalização — fontes incorporadas.svg'
        texts = ['VALIDAÇÃO DO INFOGRÁFICO', 'Fiscalização — São João de Meriti, ação e governança.', 'Órgãos públicos, diretrizes, evidências e utilização de TIC.', 'ÁÉÍÓÚ áéíóú ÃÕ ãõ Çç — nº 18/2026.']
        root = ET.Element(f'{{{SVG_NS}}}svg', {'width': '210mm', 'height': '297mm', 'viewBox': '0 0 1190 1683'})
        ET.SubElement(root, f'{{{SVG_NS}}}rect', {'width': '1190', 'height': '1683', 'fill': '#A6A6A6'})
        for i, value in enumerate(texts):
            node = ET.SubElement(root, f'{{{SVG_NS}}}text', {'x': '60', 'y': str(100 + i * 70), 'font-family': 'Cooper Hewitt' if i == 0 else 'Open Sans', 'font-weight': '900' if i == 0 else '400', 'font-size': '40' if i == 0 else '27', 'fill': '#08306A'})
            node.text = value
        ET.ElementTree(root).write(original, encoding='utf-8', xml_declaration=True)
        env = dict(os.environ)
        env['PATH'] = str(out / 'sem-programas-externos')
        env['PYTHONUTF8'] = '0'
        env['PYTHONIOENCODING'] = 'utf-8'
        report['verificacoes'].append({'item': 'ambiente de validação', 'status': 'configurado', 'python_utf8_mode': False, 'programas_externos_no_path': False})
        executar('incorporar_fontes_svg.py', [original, '--output', embedded], env)
        incorporated = ET.parse(embedded).getroot()
        actual = [n.text for n in incorporated.iter(f'{{{SVG_NS}}}text')]
        exigir(actual == texts, 'A incorporação de fontes modificou os acentos ou o texto.')
        face = next(n for n in incorporated.iter(f'{{{SVG_NS}}}style') if n.get('id') == 'fontes-incluidas')
        exigir((face.text or '').count('@font-face') == len(manifest['fontes']), 'Fontes não incorporadas integralmente.')
        report['verificacoes'].append({'item': 'UTF-8, acentos e caminhos com espaços', 'status': 'aprovado', 'textos_preservados': texts})
        png_out = folder / 'PNG — alta resolução'
        executar('exportar_infografico.py', [original, embedded, '--output-dir', png_out, '--dpi', '600'], env)
        generated_manifest = json.loads((png_out / 'manifesto-exportacao.json').read_text(encoding='utf-8'))
        images = []
        for record in generated_manifest['arquivos']:
            for kind in ('svg', 'png'):
                exigir(hashlib.sha256(Path(record[kind]).read_bytes()).hexdigest() == record[kind + '_sha256'], 'Hash da exportação divergente.')
            images.append(conferir_png(Path(record['png'])))
        exigir(images[0]['sha256'] == images[1]['sha256'], 'O SVG original e o SVG com fontes incorporadas geraram imagens diferentes.')
        report['verificacoes'].append({'item': 'exportação A4 a 600 dpi, CRC, hashes e equivalência dos SVGs', 'status': 'aprovado', 'arquivos': images})
        report['status'] = 'aprovada'
        report['validacao_windows'] = 'aprovada' if native_windows else 'pendente'
        if not native_windows:
            report['limite'] = 'Validação aprovada apenas no sistema registrado. Não comprova execução no Windows.'
        exit_code = 0
    except (OSError, ValueError, RuntimeError, ImportError, subprocess.TimeoutExpired, StopIteration) as error:
        report['status'] = 'reprovada'
        report['erro'] = str(error)
        if native_windows: report['validacao_windows'] = 'reprovada'
    finally:
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'Relatório: {report_path}')
        print(f"Resultado nesta plataforma: {report['status']}. Validação Windows: {report['validacao_windows']}.")
    return exit_code


if __name__ == '__main__':
    raise SystemExit(main())
