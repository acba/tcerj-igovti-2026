"""Relatorios de conformidade e pareceres consolidados em XLSX."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from openpyxl import Workbook

from .checkpoint import carregar_registros_analise
from .utils import join_value


def gerar_relatorio_conformidade(checkpoint: str | Path, destino: str | Path) -> int:
    registros = carregar_registros_analise(checkpoint)
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Conformidade"
    headers = [
        "auditado",
        "questao",
        "item",
        "afirmacao_auditado",
        "estado",
        "justificativa",
        "lacunas",
        "referencias",
        "evidencia",
        "provider",
        "model",
        "data_analise",
        "status_revisao_humana",
    ]
    sheet.append(headers)
    total_linhas = 0
    for registro in registros.values():
        result = registro.get("result") if isinstance(registro.get("result"), dict) else {}
        conclusoes = result.get("conclusoes") if isinstance(result, dict) else None
        if not conclusoes and registro.get("status") == "error":
            conclusoes = [
                {
                    "item_codigo": "",
                    "afirmacao_auditado": "",
                    "estado": "erro",
                    "justificativa": registro.get("error", "Erro de analise"),
                    "lacunas": [],
                    "arquivos_referenciados": [],
                }
            ]
        for conclusao in conclusoes or []:
            total_linhas += 1
            sheet.append(
                [
                    registro.get("auditado", ""),
                    registro.get("questao", ""),
                    conclusao.get("item_codigo", ""),
                    conclusao.get("afirmacao_auditado", ""),
                    conclusao.get("estado", ""),
                    conclusao.get("justificativa", ""),
                    join_value(conclusao.get("lacunas")),
                    join_value(conclusao.get("arquivos_referenciados")),
                    registro.get("evidencia", ""),
                    registro.get("provider", ""),
                    registro.get("model", ""),
                    registro.get("finished_at", ""),
                    None,
                ]
            )
    destino_path = Path(destino)
    destino_path.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(destino_path)
    return total_linhas


def _chave_parecer_logico(registro: dict[str, Any]) -> tuple[str, str, str, str, str, str]:
    return (
        str(registro.get("auditado") or ""),
        str(registro.get("questao") or ""),
        str(registro.get("coluna_evidencia") or ""),
        str(registro.get("evidencia") or ""),
        str(registro.get("judge_provider") or ""),
        str(registro.get("judge_model") or ""),
    )


def registros_pareceres_mais_recentes(registros: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    mais_recentes: dict[tuple[str, str, str, str, str, str], dict[str, Any]] = {}
    for registro in registros:
        chave = _chave_parecer_logico(registro)
        atual = mais_recentes.get(chave)
        if atual is None or str(registro.get("finished_at") or "") >= str(atual.get("finished_at") or ""):
            mais_recentes[chave] = registro
    return list(mais_recentes.values())


def gerar_relatorio_pareceres(checkpoint: str | Path, destino: str | Path) -> int:
    registros = carregar_registros_analise(checkpoint)
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Pareceres consolidados"
    sheet.append(
        [
            "auditado",
            "questao",
            "coluna_evidencia",
            "evidencia",
            "item",
            "afirmacao_auditado",
            "estado",
            "justificativa",
            "lacunas",
            "referencias",
            "judge_provider",
            "judge_model",
            "opinioes_modelos",
            "opiniao_auditoria",
            "data_parecer",
        ]
    )
    total = 0
    for registro in registros_pareceres_mais_recentes(registros.values()):
        result = registro.get("result") if isinstance(registro.get("result"), dict) else {}
        for conclusao in result.get("conclusoes") or []:
            if not isinstance(conclusao, dict):
                continue
            total += 1
            sheet.append(
                [
                    registro.get("auditado", ""),
                    registro.get("questao", ""),
                    registro.get("coluna_evidencia", ""),
                    registro.get("evidencia", ""),
                    conclusao.get("item_codigo", ""),
                    conclusao.get("afirmacao_auditado", ""),
                    conclusao.get("estado", ""),
                    conclusao.get("justificativa", ""),
                    "; ".join(str(item) for item in conclusao.get("lacunas") or []),
                    "; ".join(str(item) for item in conclusao.get("arquivos_referenciados") or []),
                    registro.get("judge_provider", ""),
                    registro.get("judge_model", ""),
                    registro.get("opinion_count", 0),
                    "sim" if registro.get("opiniao_auditoria") else "nao",
                    registro.get("finished_at", ""),
                ]
            )
    destino_path = Path(destino)
    destino_path.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(destino_path)
    return total


def gerar_checkpoint_limpo_consolidado(checkpoint: str | Path, destino: str | Path) -> int:
    """Copia para ``destino`` apenas os registros ``completed`` do checkpoint."""
    path = Path(checkpoint)
    if not path.is_file():
        return 0
    destino_path = Path(destino)
    destino_path.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    with path.open(encoding="utf-8") as f_in, destino_path.open("w", encoding="utf-8") as f_out:
        for linha in f_in:
            if not linha.strip():
                continue
            registro = json.loads(linha)
            if registro.get("status") == "completed":
                f_out.write(json.dumps(registro, ensure_ascii=False) + "\n")
                total += 1
    return total