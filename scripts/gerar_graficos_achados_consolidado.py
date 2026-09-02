#!/usr/bin/env python3
"""Gera gráficos consolidados de causa/situação inconforme por esfera para os achados de auditoria do iGovTI 2026."""

from __future__ import annotations

import json
import logging
import os
import zipfile
import xml.etree.ElementTree as ET
import textwrap
import sys
from pathlib import Path

# Configura matplotlib para rodar headless
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-igovti-achados")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent / "resources"))
from identidade_visual_graficos import (  # noqa: E402
    CORES,
    CORES_ESFERAS,
    aplicar_estilo,
    legenda_superior,
    salvar_figura,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_AUDITADOS_XLSX = ROOT / "02-Execucao/03-Execucao_Procedimentos/01-Insumos/bd_auditados.xlsx"
DEFAULT_RESULTADO_AUDITORIA_JSON = ROOT / "02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/03-pos-comentarios-gestor/resultado_auditoria.json"

# Cores institucionais do TCE-RJ/CIS do iGovTI 2026
COLOR_ESTADUAL = CORES_ESFERAS["Estadual"]
COLOR_MUNICIPAL = CORES_ESFERAS["Municipal"]
COLOR_GRID = CORES["neutro_claro"]
COLOR_TEXT = CORES["texto"]

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def iter_organizacoes(data):
    """Retorna pares (sigla, dados) aceitando os formatos JSON já usados pelo projeto."""
    if isinstance(data, dict):
        if isinstance(data.get("auditados"), list):
            for org in data["auditados"]:
                yield str(org.get("sigla") or org.get("id") or "").strip(), org
            return
        for sigla, org in data.items():
            if isinstance(org, dict):
                yield str(org.get("sigla") or sigla).strip(), org
        return

    if isinstance(data, list):
        for org in data:
            if isinstance(org, dict):
                yield str(org.get("sigla") or org.get("id") or "").strip(), org


def numero_achado(proc: dict) -> int | None:
    """Extrai o número do achado do procedimento executado."""
    for value in (proc.get("numero_achado"), (proc.get("achado") or {}).get("numero")):
        if value is None:
            continue
        try:
            return int(value)
        except (TypeError, ValueError):
            continue
    return None

def parse_excel_spheres(path: Path) -> dict[str, str]:
    """Parse do Excel bd_auditados.xlsx via zipfile/xml para evitar dependências de pandas no sandbox."""
    sigla_to_esfera = {}
    with zipfile.ZipFile(path, 'r') as zip_ref:
        namelist = zip_ref.namelist()
        shared_strings = []
        if "xl/sharedStrings.xml" in namelist:
            with zip_ref.open("xl/sharedStrings.xml") as f:
                tree = ET.parse(f)
                root = tree.getroot()
                ns = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                for si in root.findall('ns:si', ns):
                    t = si.find('ns:t', ns)
                    if t is not None:
                        shared_strings.append(t.text)
                    else:
                        r_texts = []
                        for r in si.findall('ns:r', ns):
                            rt = r.find('ns:t', ns)
                            if rt is not None and rt.text:
                                r_texts.append(rt.text)
                        shared_strings.append("".join(r_texts))
        
        sheet_path = "xl/worksheets/sheet1.xml"
        if sheet_path in namelist:
            with zip_ref.open(sheet_path) as f:
                tree = ET.parse(f)
                root = tree.getroot()
                ns = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                
                rows = []
                sheetData = root.find('ns:sheetData', ns)
                for r in sheetData.findall('ns:row', ns):
                    row_cells = {}
                    for c in r.findall('ns:c', ns):
                        r_attr = c.get('r')
                        t_attr = c.get('t')
                        v = c.find('ns:v', ns)
                        val = ""
                        if v is not None:
                            val = v.text
                            if t_attr == 's':
                                val = shared_strings[int(val)]
                        elif t_attr == 'inlineStr':
                            inline = c.find('ns:is', ns)
                            if inline is not None:
                                textos = [
                                    no.text or ""
                                    for no in inline.findall('.//ns:t', ns)
                                ]
                                val = "".join(textos)
                        row_cells[r_attr] = val
                    rows.append(row_cells)
                
                def split_ref(ref):
                    import re
                    match = re.match(r"([A-Z]+)([0-9]+)", ref)
                    return match.groups() if match else (ref, "")
                
                tabular_data = []
                for r in rows:
                    row_data = {}
                    row_num = None
                    for cell_ref, val in r.items():
                        col, row = split_ref(cell_ref)
                        row_num = row
                        row_data[col] = val
                    if row_num:
                        tabular_data.append((int(row_num), row_data))
                
                tabular_data.sort(key=lambda x: x[0])
                headers = tabular_data[0][1] if tabular_data else {}
                
                for r_num, r_data in tabular_data[1:]:
                    mapped_row = {headers[col]: val for col, val in r_data.items() if col in headers}
                    sig = mapped_row.get('sigla')
                    esf = mapped_row.get('esfera')
                    if sig and esf:
                        sigla_to_esfera[sig.strip().upper()] = esf.strip().upper()
    return sigla_to_esfera

def main(argv: list[str] | None = None):
    import argparse
    parser = argparse.ArgumentParser(description="Gera gráficos consolidados por esfera.")
    parser.add_argument(
        "--output-dir",
        default=str(ROOT / "03-Relatorios/01-Relatorio_Consolidado"),
        help="Diretório de saída para os gráficos gerados."
    )
    parser.add_argument(
        "--auditados",
        type=Path,
        default=DEFAULT_AUDITADOS_XLSX,
        help=f"Base de auditados XLSX usada para identificar a esfera (padrão: {DEFAULT_AUDITADOS_XLSX})."
    )
    parser.add_argument(
        "--resultado-auditoria-json",
        type=Path,
        default=DEFAULT_RESULTADO_AUDITORIA_JSON,
        help=f"Resultado estruturado da auditoria em JSON (padrão: {DEFAULT_RESULTADO_AUDITORIA_JSON})."
    )
    args = parser.parse_args(argv)
    output_dir = Path(args.output_dir)
    xlsx_path = args.auditados
    json_path = args.resultado_auditoria_json

    logger.info("Iniciando geração de gráficos dos achados...")
    
    # 1. Carrega mapeamento de esferas
    if not xlsx_path.exists():
        logger.error("Arquivo Excel não encontrado em %s", xlsx_path)
        return
    sigla_to_esfera = parse_excel_spheres(xlsx_path)
    
    # 2. Carrega resultados da auditoria
    if not json_path.exists():
        logger.error("Arquivo JSON não encontrado em %s", json_path)
        return
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # Assegura que o diretório de destino existe
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "img").mkdir(parents=True, exist_ok=True)

    # Configuração de estilos do Matplotlib
    aplicar_estilo(tamanho_fonte=10)

    organizacoes = list(iter_organizacoes(data))
    organizacoes_avaliadas = [
        (sigla, org)
        for sigla, org in organizacoes
        if org.get("procedimentos_executados")
    ]

    if not organizacoes_avaliadas:
        logger.warning("Nenhuma organização com procedimentos executados foi encontrada no JSON.")
        return

    desconhecidas = sorted(
        {
            sigla.strip().upper()
            for sigla, _ in organizacoes_avaliadas
            if sigla.strip().upper() not in sigla_to_esfera
        }
    )
    if desconhecidas:
        logger.warning("Organizações avaliadas sem esfera em bd_auditados.xlsx: %s", ", ".join(desconhecidas))

    # Denominador dos percentuais: somente organizações efetivamente avaliadas.
    # Não respondentes constam no JSON, mas não possuem procedimentos executados.
    total_e = sum(1 for sigla, _ in organizacoes_avaliadas if sigla_to_esfera.get(sigla.strip().upper()) == 'E')
    total_m = sum(1 for sigla, _ in organizacoes_avaliadas if sigla_to_esfera.get(sigla.strip().upper()) == 'M')
    total_geral = total_e + total_m

    for find_idx in range(6):
        num_find = find_idx + 1
        # Estrutura para contar as situações ocorridas por esfera
        counts = {} # sit -> {'E': int, 'M': int}
        
        for org_key, org in organizacoes_avaliadas:
            sigla_upper = org_key.strip().upper()
            esfera = sigla_to_esfera.get(sigla_upper, "UNKNOWN")

            proc = next(
                (
                    item
                    for item in org.get("procedimentos_executados", [])
                    if isinstance(item, dict) and numero_achado(item) == num_find
                ),
                None,
            )
            if not proc:
                continue

            achado = proc.get("achado")
            if proc.get("achado_ocorreu") and achado:
                for sit in achado.get("situacoes_encontradas", []):
                    if sit not in counts:
                        counts[sit] = {'E': 0, 'M': 0}
                    if esfera == 'E':
                        counts[sit]['E'] += 1
                    elif esfera == 'M':
                        counts[sit]['M'] += 1

        if not counts:
            logger.warning("Nenhuma ocorrência registrada para o Achado %s", num_find)
            continue

        # Ordena situações pelo total (decrescente)
        sorted_sits = sorted(counts.items(), key=lambda item: item[1]['E'] + item[1]['M'])
        
        situations_labels = [item[0] for item in sorted_sits]
        vals_e = np.array([item[1]['E'] for item in sorted_sits])
        vals_m = np.array([item[1]['M'] for item in sorted_sits])
        totals = vals_e + vals_m

        # Quebra texto das labels para caber no gráfico
        wrapped_labels = [textwrap.fill(lbl, width=50) for lbl in situations_labels]

        # Altura do gráfico proporcional ao número de barras (geralmente entre 3 e 6 situações)
        fig_height = max(4, len(situations_labels) * 1.25)
        fig, ax = plt.subplots(figsize=(11, fig_height))

        y_positions = np.arange(len(wrapped_labels))
        height = 0.55

        # Plota as barras horizontais empilhadas
        bars_e = ax.barh(y_positions, vals_e, height, label=f"Estadual (n={total_e})", color=COLOR_ESTADUAL)
        bars_m = ax.barh(y_positions, vals_m, height, left=vals_e, label=f"Municipal (n={total_m})", color=COLOR_MUNICIPAL)

        # Adiciona rótulos estatísticos dentro/fora das barras
        for idx, (y_pos, val_e, val_m, tot) in enumerate(zip(y_positions, vals_e, vals_m, totals)):
            # Rótulo Estadual
            if val_e > 5:
                ax.text(val_e / 2, y_pos, f"{val_e}", ha="center", va="center", color="white", fontweight="bold")
            # Rótulo Municipal
            if val_m > 3:
                ax.text(val_e + val_m / 2, y_pos, f"{val_m}", ha="center", va="center", color="white", fontweight="bold")
            
            # Rótulo total, relativo ao universo efetivamente avaliado.
            pct = (tot / total_geral) * 100
            ax.text(tot + 1.5, y_pos, f"{tot} ({pct:.1f}%)", ha="left", va="center", color=COLOR_TEXT, fontweight="bold")

        # Ajustes estéticos
        ax.set_yticks(y_positions)
        ax.set_yticklabels(wrapped_labels, fontsize=9.5)
        ax.set_xlabel("Quantidade de organizações com a ocorrência", fontsize=10, labelpad=8)
        ax.set_xlim(0, total_geral + 10)
        
        # Gridlines verticais
        ax.xaxis.grid(True, linestyle="--", alpha=0.5, color=COLOR_GRID, zorder=0)
        ax.set_axisbelow(True)

        # Remove bordas desnecessárias
        for spine in ["top", "right"]:
            ax.spines[spine].set_visible(False)
        ax.spines["left"].set_color(COLOR_GRID)
        ax.spines["bottom"].set_color(COLOR_GRID)

        # Faixa superior reservada à legenda, sem sobrepor totais ou percentuais.
        legenda_superior(ax, ncol=2, y=1.02, fontsize=9.5)
        
        plt.tight_layout()

        # Salva o gráfico em PNG
        filename = f"igovti_2026_achado{num_find}_esferas.png"
        
        # Salva na raiz do consolidado e na pasta img/
        save_path_root = output_dir / filename
        save_path_img = output_dir / "img" / filename
        
        salvar_figura(fig, save_path_root, fechar=False)
        salvar_figura(fig, save_path_img)
        
        logger.info("Gráfico gerado com sucesso: %s", filename)

if __name__ == "__main__":
    main()
