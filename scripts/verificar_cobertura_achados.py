"""Verifica a cobertura das avaliacoes de evidencias para questoes que ensejam achado.

Calcula o universo esperado a partir das respostas do questionario (auditados que
afirmaram ao menos um item avaliavel em cada questao-achado) e compara com o que
esta nos arquivos analyses_*.jsonl, gerando um relatorio XLSX de cobertura.

Para cada (auditado, questao-achado) no universo:
- quantos modelos avaliaram (completed)
- status por modelo
- se ha lacuna (0 completed), cobertura parcial ou completa

Uso:
    scripts/.venv/bin/python scripts/verificar_cobertura_achados.py \
        --respostas 02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario.xlsx \
        --questionario 01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md \
        --analyses 02-Execucao/03-Execucao_Procedimentos/99-Avaliacao_Evidencias/individuais/analyses_*.jsonl \
        --catalog scripts/avaliacao_evidencias/prompt_catalogs/igovti_2026_achados_binario_v1.yml \
        --output C:/tmp/tcerj-igovti-2026/cobertura_achados.xlsx
"""

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.resources.xlsx_utils import escrever_xlsx_se_diferente


def carregar_questoes_achado(catalog_path: str | Path) -> dict[str, str]:
    """Retorna dict questao -> coluna_evidencia das questoes marcadas gera_achado."""
    with Path(catalog_path).open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    colunas: dict[str, str] = {}
    for entrada in data.get("prompts", []) or []:
        if not isinstance(entrada, dict) or not entrada.get("gera_achado"):
            continue
        match = re.match(r"(q\d{4})", str(entrada.get("arquivo", "")))
        if match:
            colunas[match.group(1)] = str(entrada.get("coluna_evidencia", ""))
    return colunas


def carregar_cobertura(
    analyses_paths: list[str | Path],
    achados_set: set[str],
) -> tuple[dict[str, dict[tuple[str, str], str]], set[tuple[str, str]], dict[str, set[tuple[str, str]]]]:
    """Cruza os JSONL com o universo de achados.

    Retorna:
    - modelo_status: modelo -> (auditado, questao) -> status (prioriza completed)
    - grupos_jsonl: grupos que aparecem em qualquer JSONL (qualquer status)
    - modelo_avaliou: modelo -> set de (auditado, questao) onde o modelo foi
      efetivamente chamado (status=completed E campo evidencia nao vazio),
      excluindo auto-registros de nao_conforme sem chamada ao provider.
    """
    modelo_status: dict[str, dict[tuple[str, str], str]] = defaultdict(lambda: defaultdict(str))
    grupos_jsonl: set[tuple[str, str]] = set()
    modelo_avaliou: dict[str, set[tuple[str, str]]] = defaultdict(set)
    for caminho in analyses_paths:
        path = Path(caminho)
        if not path.is_file():
            continue
        with path.open(encoding="utf-8") as f:
            for linha in f:
                if not linha.strip():
                    continue
                try:
                    registro = json.loads(linha)
                except json.JSONDecodeError:
                    continue
                questao = (registro.get("questao") or "").lower()
                if questao not in achados_set:
                    continue
                modelo = f"{registro.get('provider','')}/{registro.get('model','')}".strip("/")
                chave = (registro.get("auditado", ""), questao)
                status = registro.get("status", "?")
                tem_evidencia = bool(str(registro.get("evidencia") or "").strip())
                atual = modelo_status[modelo][chave]
                if status == "completed" or atual != "completed":
                    modelo_status[modelo][chave] = status
                grupos_jsonl.add(chave)
                if status == "completed" and tem_evidencia:
                    modelo_avaliou[modelo].add(chave)
    return dict(modelo_status), grupos_jsonl, dict(modelo_avaliou)


def carregar_universo(
    respostas_path: str | Path,
    questionario_path: str | Path,
    colunas_achado: dict[str, str],
    *,
    incluir_nao_submetidas: bool = False,
) -> set[tuple[str, str]]:
    """Universo esperado: (auditado, questao-achado) onde o auditado enviou evidencia.

    Conta apenas colunas de evidencia com anexo efetivamente enviado (upload presente
    na celula qNNNevi). Se o auditado afirmou a pratica mas nao enviou anexo, o pipeline
    registra nao_conforme automaticamente sem chamar modelo — logo nao entra no universo
    de evidencias a verificar por IA.
    """
    from scripts.avaliacao_evidencias.pipeline import (
        _parse_upload,
        _rows_from_xlsx,
    )

    universo: set[tuple[str, str]] = set()
    for linha in _rows_from_xlsx(Path(respostas_path)):
        if not incluir_nao_submetidas and not linha.get("submitdate"):
            continue
        auditado = str(linha.get("firstname") or "").strip()
        for questao, coluna in colunas_achado.items():
            upload, erro = _parse_upload(linha.get(coluna))
            if upload is not None and not erro:
                universo.add((auditado, questao))
    return universo


def gerar_relatorio(
    modelo_status: dict[str, dict[tuple[str, str], str]],
    universo: set[tuple[str, str]],
    grupos_jsonl: set[tuple[str, str]],
    modelo_avaliou: dict[str, set[tuple[str, str]]],
    colunas_achado: dict[str, str],
    output: str | Path,
) -> dict[str, int]:
    modelos = sorted(modelo_status.keys())
    wb = Workbook()

    # Aba 1: Resumo
    ws1 = wb.active
    ws1.title = "Resumo"
    cobertura_contagem = defaultdict(int)
    for grupo in universo:
        n = sum(1 for m in modelos if grupo in modelo_avaliou.get(m, set()))
        cobertura_contagem[n] += 1
    total_grupos = len(universo)
    ws1.append(["Métrica", "Valor"])
    ws1.append(["Questões-achado no catálogo", len(colunas_achado)])
    ws1.append(["Modelos com análises", len(modelos)])
    ws1.append(["Universo esperado (itens afirmados)", total_grupos])
    ws1.append(["Ao menos 1 registro no JSONL (qualquer status)", len(universo & grupos_jsonl)])
    ws1.append(["Nunca entrou no pipeline", len(universo - grupos_jsonl)])
    ws1.append([""])
    ws1.append(["Cobertura por nº de modelos completed", ""])
    for n in sorted(cobertura_contagem):
        if n == 0:
            rotulo = "  0 modelos (lacuna total)"
        else:
            rotulo = f"  {n} modelo(s)"
        ws1.append([rotulo, cobertura_contagem[n]])
    ws1.append([""])
    ws1.append(["Modelos", ""])
    for m in modelos:
        ws1.append([m, ""])

    # Aba 2: Detalhe por (auditado, questão)
    ws2 = wb.create_sheet("Cobertura detalhada")
    headers = ["Auditado", "Questão", "Nº modelos que avaliaram", "Cobertura", "No JSONL?"] + modelos
    ws2.append(headers)
    lacunas_total = 0
    parcial = 0
    completo = 0
    for auditado, questao in sorted(universo):
        n_avaliado = sum(1 for m in modelos if (auditado, questao) in modelo_avaliou.get(m, set()))
        no_jsonl = "Sim" if (auditado, questao) in grupos_jsonl else "Não"
        if n_avaliado == 0:
            cobertura = "LACUNA TOTAL (0 modelos)"
            lacunas_total += 1
        elif n_avaliado < len(modelos):
            cobertura = f"Parcial ({n_avaliado}/{len(modelos)})"
            parcial += 1
        else:
            cobertura = "Completo"
            completo += 1
        row = [auditado, questao, n_avaliado, cobertura, no_jsonl]
        for m in modelos:
            avaliou = (auditado, questao) in modelo_avaliou.get(m, set())
            status = modelo_status[m].get((auditado, questao), "—")
            row.append(f"{status}{' ✓' if avaliou else ''}")
        ws2.append(row)

    # Aba 3: Lacunas (0 modelos avaliaram)
    ws3 = wb.create_sheet("Lacunas")
    ws3.append(["Auditado", "Questão", "No JSONL?"] + modelos)
    for auditado, questao in sorted(universo):
        n_avaliado = sum(1 for m in modelos if (auditado, questao) in modelo_avaliou.get(m, set()))
        if n_avaliado > 0:
            continue
        no_jsonl = "Sim" if (auditado, questao) in grupos_jsonl else "Não"
        row = [auditado, questao, no_jsonl]
        for m in modelos:
            row.append(modelo_status[m].get((auditado, questao), "—"))
        ws3.append(row)

    # --- Aba 4: Nunca processado (não entrou no pipeline) ---
    ws4 = wb.create_sheet("Nunca processado")
    ws4.append(["Auditado", "Questão"])
    nunca = universo - grupos_jsonl
    for auditado, questao in sorted(nunca):
        ws4.append([auditado, questao])

    # Formatação comum
    for ws in [ws1, ws2, ws3, ws4]:
        fill = PatternFill("solid", fgColor="1F4E78")
        for celula in ws[1]:
            celula.fill = fill
            celula.font = Font(color="FFFFFF", bold=True)
            celula.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws.freeze_panes = "A2"
        for col_idx in range(1, ws.max_column + 1):
            max_len = max(
                (len(str(celula.value or "")) for celula in ws[get_column_letter(col_idx)]),
                default=10,
            )
            ws.column_dimensions[get_column_letter(col_idx)].width = min(max(max_len + 2, 12), 45)

    # Destaques na aba detalhada
    fill_lacuna = PatternFill("solid", fgColor="FFC7CE")
    fill_parcial = PatternFill("solid", fgColor="FFEB9C")
    for row_idx in range(2, ws2.max_row + 1):
        cobertura_val = ws2.cell(row=row_idx, column=4).value
        if cobertura_val and "LACUNA" in str(cobertura_val):
            ws2.cell(row=row_idx, column=4).fill = fill_lacuna
            ws2.cell(row=row_idx, column=5).fill = fill_lacuna
        elif "Parcial" in str(cobertura_val or ""):
            ws2.cell(row=row_idx, column=4).fill = fill_parcial

    out_path = Path(output)
    escrever_xlsx_se_diferente(out_path, wb.save)
    return {
        "universo": total_grupos,
        "no_jsonl": len(universo & grupos_jsonl),
        "nunca_processado": len(universo - grupos_jsonl),
        "lacunas_total": lacunas_total,
        "parcial": parcial,
        "completo": completo,
        "modelos": len(modelos),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verifica cobertura das avaliacoes para questoes-achado.")
    parser.add_argument(
        "--analyses",
        nargs="+",
        required=True,
        help="Arquivos analyses_*.jsonl (aceita glob expandido pelo shell).",
    )
    parser.add_argument(
        "--respostas",
        default="02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario.xlsx",
        help="Planilha de respostas do questionario (fonte do universo amostral).",
    )
    parser.add_argument(
        "--questionario",
        default="01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md",
        help="Questionario iGovTI em markdown.",
    )
    parser.add_argument(
        "--catalog",
        default="scripts/avaliacao_evidencias/prompt_catalogs/igovti_2026_achados_binario_v1.yml",
        help="Catálogo YAML com atributo gera_achado.",
    )
    parser.add_argument(
        "--output",
        default=str((Path("C:/tmp") if sys.platform.startswith("win") else Path(tempfile.gettempdir())) / "tcerj-igovti-2026" / "cobertura_achados.xlsx"),
        help="Arquivo XLSX de saída.",
    )
    parser.add_argument(
        "--incluir-nao-submetidas",
        action="store_true",
        help="Inclui respostas sem submitdate no universo (por padrao, só submetidas).",
    )
    args = parser.parse_args(argv)

    colunas_achado = carregar_questoes_achado(args.catalog)
    achados_set = set(colunas_achado.keys())
    print(f"Questões-achado no catálogo ({len(achados_set)}): {sorted(achados_set)}")

    universo = carregar_universo(
        args.respostas,
        args.questionario,
        colunas_achado,
        incluir_nao_submetidas=args.incluir_nao_submetidas,
    )
    print(f"Universo esperado (auditado × questão-achado com item afirmado): {len(universo)}")

    modelo_status, grupos_jsonl, modelo_avaliou = carregar_cobertura(args.analyses, achados_set)
    print(f"Modelos: {sorted(modelo_status.keys())}")
    print(f"Grupos no JSONL (qualquer status): {len(grupos_jsonl)}")
    print(f"Universo ao menos 1 registro: {len(universo & grupos_jsonl)}")
    print(f"Universo nunca processado: {len(universo - grupos_jsonl)}")

    resumo = gerar_relatorio(modelo_status, universo, grupos_jsonl, modelo_avaliou, colunas_achado, args.output)
    print(f"\nResumo (sobre universo de {resumo['universo']}):")
    print(f"  Lacunas totais (0 modelos completed): {resumo['lacunas_total']}")
    print(f"    - nunca processado: {resumo['nunca_processado']}")
    print(f"    - processado mas só error: {resumo['lacunas_total'] - resumo['nunca_processado']}")
    print(f"  Parcial (1 a {resumo['modelos']-1} modelos): {resumo['parcial']}")
    print(f"  Completo (todos os {resumo['modelos']} modelos): {resumo['completo']}")
    print(f"\nRelatório: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
