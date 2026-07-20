"""Validação determinística do escopo lógico das avaliações de IA.

O esquema JSON garante apenas a forma da resposta. Este módulo garante que a
resposta pertença ao caso submetido: mesmos itens, mesmos motivos e estados
temporais coerentes. A validação é deliberadamente fechada para evitar que uma
conclusão válida de outro caso contamine ajustes ou produtos de auditoria.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable


ESTADOS_TEMPORAIS_FINAIS = {
    "mantida",
    "afastada_na_data_base",
    "corrigida_posteriormente",
}
ESTADOS_MOTIVO_FINAIS = {"mantido", "afastado"}


@dataclass(frozen=True)
class ViolacaoEscopo:
    codigo: str
    mensagem: str


def _codigo_item(item: Any) -> str:
    if isinstance(item, dict):
        return str(item.get("codigo") or item.get("item_codigo") or "").strip()
    return str(getattr(item, "codigo", "") or "").strip()


def itens_esperados_registro(registro: dict[str, Any]) -> list[str]:
    """Obtém os itens autoritativos do caso sem inferi-los da resposta do modelo."""
    itens = [_codigo_item(item) for item in registro.get("itens", [])]
    itens = [codigo for codigo in itens if codigo]
    if itens:
        return itens

    secao = str(registro.get("secao", "")).strip()
    codigo = str(registro.get("codigo", "")).strip()
    if secao == "1" and codigo:
        return [codigo]

    contexto = registro.get("contexto") if isinstance(registro.get("contexto"), dict) else {}
    anterior = contexto.get("avaliacao_anterior") if isinstance(contexto.get("avaliacao_anterior"), dict) else {}
    conclusoes = anterior.get("conclusoes") if isinstance(anterior.get("conclusoes"), list) else []
    codigos = [str(c.get("item_codigo") or "").strip() for c in conclusoes if isinstance(c, dict)]
    return [item for item in codigos if item]


def motivos_ativos_registro(registro: dict[str, Any]) -> list[str]:
    contexto = registro.get("contexto") if isinstance(registro.get("contexto"), dict) else {}
    motivos = contexto.get("motivos_ativos")
    if not isinstance(motivos, list):
        motivos = contexto.get("motivos") if isinstance(contexto.get("motivos"), list) else []
    resultado: list[str] = []
    for motivo in motivos:
        if not isinstance(motivo, dict):
            continue
        codigo = str(motivo.get("id_motivo") or motivo.get("id") or motivo.get("codigo") or "").strip()
        if codigo:
            resultado.append(codigo)
    return resultado


def _duplicados(valores: Iterable[str]) -> set[str]:
    vistos: set[str] = set()
    repetidos: set[str] = set()
    for valor in valores:
        if valor in vistos:
            repetidos.add(valor)
        vistos.add(valor)
    return repetidos


def validar_resultado_no_escopo(
    registro: dict[str, Any],
    resultado: dict[str, Any] | None = None,
    *,
    validar_temporal: bool = False,
) -> list[ViolacaoEscopo]:
    """Retorna violações de pertencimento e coerência; lista vazia significa válido."""
    resultado = resultado if resultado is not None else registro.get("resultado")
    if not isinstance(resultado, dict):
        return [ViolacaoEscopo("resultado_ausente", "resultado não é um objeto")]
    if resultado.get("status", "completed") != "completed":
        return [ViolacaoEscopo("status_invalido", "resultado não está concluído")]
    conclusoes = resultado.get("conclusoes")
    if not isinstance(conclusoes, list) or not conclusoes:
        return [ViolacaoEscopo("conclusoes_ausentes", "resultado não contém conclusões")]

    esperados = itens_esperados_registro(registro)
    recebidos = [
        str(conclusao.get("item_codigo") or "").strip()
        for conclusao in conclusoes
        if isinstance(conclusao, dict)
    ]
    violacoes: list[ViolacaoEscopo] = []
    if len(recebidos) != len(conclusoes) or any(not codigo for codigo in recebidos):
        violacoes.append(ViolacaoEscopo("codigo_item_ausente", "há conclusão sem item_codigo"))
    repetidos = _duplicados(recebidos)
    if repetidos:
        violacoes.append(
            ViolacaoEscopo("codigo_item_duplicado", f"itens duplicados: {', '.join(sorted(repetidos))}")
        )
    if esperados and (len(recebidos) != len(esperados) or set(recebidos) != set(esperados)):
        violacoes.append(
            ViolacaoEscopo(
                "escopo_itens",
                f"itens esperados={esperados}; recebidos={recebidos}",
            )
        )

    if not validar_temporal:
        return violacoes

    motivos_esperados = motivos_ativos_registro(registro)
    for indice, conclusao in enumerate(conclusoes):
        if not isinstance(conclusao, dict):
            violacoes.append(ViolacaoEscopo("conclusao_invalida", f"conclusão {indice} não é objeto"))
            continue
        estado = str(conclusao.get("estado_temporal") or "").strip()
        if estado not in ESTADOS_TEMPORAIS_FINAIS:
            violacoes.append(
                ViolacaoEscopo("estado_temporal", f"estado temporal inválido na conclusão {indice}: {estado!r}")
            )
        motivos = conclusao.get("conclusoes_motivos")
        if not isinstance(motivos, list):
            violacoes.append(ViolacaoEscopo("motivos_ausentes", f"conclusão {indice} sem lista de motivos"))
            continue
        ids = [str(m.get("id_motivo") or "").strip() for m in motivos if isinstance(m, dict)]
        if motivos_esperados and (len(ids) != len(motivos_esperados) or set(ids) != set(motivos_esperados)):
            violacoes.append(
                ViolacaoEscopo(
                    "escopo_motivos",
                    f"motivos esperados={motivos_esperados}; recebidos={ids}",
                )
            )
        if _duplicados(ids):
            violacoes.append(ViolacaoEscopo("motivo_duplicado", f"motivos duplicados na conclusão {indice}"))
        estados_motivos = [
            str(m.get("estado_motivo") or "").strip() for m in motivos if isinstance(m, dict)
        ]
        invalidos = sorted(set(estados_motivos).difference(ESTADOS_MOTIVO_FINAIS))
        if invalidos:
            violacoes.append(
                ViolacaoEscopo("estado_motivo", f"estados de motivo inválidos: {', '.join(invalidos)}")
            )
        if estado in {"afastada_na_data_base", "corrigida_posteriormente"} and any(
            valor != "afastado" for valor in estados_motivos
        ):
            violacoes.append(
                ViolacaoEscopo("coerencia_temporal", f"{estado} exige todos os motivos afastados")
            )
        if estado == "mantida" and motivos_esperados and "mantido" not in estados_motivos:
            violacoes.append(
                ViolacaoEscopo("coerencia_temporal", "situação mantida exige ao menos um motivo mantido")
            )
    return violacoes


def formatar_violacoes(violacoes: Iterable[ViolacaoEscopo]) -> str:
    return "; ".join(f"{item.codigo}: {item.mensagem}" for item in violacoes)
