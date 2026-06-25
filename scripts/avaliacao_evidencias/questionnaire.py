"""Contexto do questionario e selecao de itens afirmados.

Le o questionario em Markdown (via md2lss) e seleciona, para cada coluna de
evidencia, os itens afirmados pelo auditado a partir da linha de respostas.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from scripts import md2lss

from .utils import normalizar_texto_resposta


@dataclass(frozen=True)
class ItemAfirmado:
    codigo: str
    texto: str
    afirmacao: str


@dataclass(frozen=True)
class QuestaoContexto:
    codigo: str
    tipo: str
    texto: str
    itens: dict[str, str]


@dataclass(frozen=True)
class ContextoQuestionario:
    questoes: dict[str, QuestaoContexto]


ADOPTION_VALUES = {"naoad", "adfor", "admen", "adpar", "admai", "naoap"}
ADOPTION_VALUE_ALIASES = {
    "nao adota.": "naoad",
    "adota em menor parte.": "admen",
    "adota parcialmente.": "adpar",
    "adota em maior parte ou totalmente.": "admai",
    "nao se aplica.": "naoap",
}


def base_coluna_evidencia(coluna_evidencia: str) -> tuple[str, str | None]:
    marker = coluna_evidencia.find("evi")
    base = coluna_evidencia[:marker]
    suffix = coluna_evidencia[marker + 3:]
    return base, suffix or None


def carregar_contexto_questionario(caminho_questionario: str | Path) -> ContextoQuestionario:
    survey = md2lss.parse_markdown(Path(caminho_questionario))
    questoes: dict[str, QuestaoContexto] = {}
    for group in survey.groups:
        for question in group.questions:
            if question.type == "upload":
                continue
            itens = {option.code: option.text for option in (question.subquestions or question.alternatives)}
            questoes[question.code] = QuestaoContexto(
                codigo=question.code,
                tipo=question.type,
                texto=question.text(),
                itens=itens,
            )
    return ContextoQuestionario(questoes=questoes)


def _valor_afirmativo(valor: Any) -> bool:
    if isinstance(valor, str):
        return valor.strip().casefold() in {"sim", "y", "yes", "true", "1"}
    return valor is True or valor == 1


def _valor_adocao(valor: Any) -> str:
    raw = str(valor or "").strip()
    if raw in ADOPTION_VALUES:
        return raw
    return ADOPTION_VALUE_ALIASES.get(normalizar_texto_resposta(raw), raw)


def _codigo_resposta_unica(questao: QuestaoContexto, valor: Any) -> str:
    raw = str(valor or "").strip()
    if not raw:
        return ""
    if raw in questao.itens:
        return raw
    normalizado = normalizar_texto_resposta(raw)
    for codigo, texto in questao.itens.items():
        if normalizado == normalizar_texto_resposta(texto):
            return codigo
    match = re.match(r"^([A-Za-z])\)", raw.strip())
    if match and match.group(1).upper() in questao.itens:
        return match.group(1).upper()
    return raw


def selecionar_itens_afirmados(
    contexto: ContextoQuestionario,
    coluna_evidencia: str,
    resposta: dict[str, Any],
) -> list[ItemAfirmado]:
    base, item_especifico = base_coluna_evidencia(coluna_evidencia)
    questao = contexto.questoes.get(base)
    if not questao:
        return []

    if item_especifico:
        valor = resposta.get(f"{base}[{item_especifico}]")
        if _valor_afirmativo(valor):
            return [
                ItemAfirmado(
                    codigo=f"{base}[{item_especifico}]",
                    texto=questao.itens.get(item_especifico, item_especifico),
                    afirmacao=str(valor),
                )
            ]
        return []

    valor_base = resposta.get(base)
    valor_adocao = _valor_adocao(valor_base)
    if questao.tipo in {"single", "adoption"} and valor_adocao in {"adpar", "admai"}:
        itens = [ItemAfirmado(codigo=base, texto=questao.texto, afirmacao=str(valor_base))]
        prefixo_ext = f"{base}ext["
        detalhe = contexto.questoes.get(f"{base}ext")
        for chave, valor in resposta.items():
            if chave.startswith(prefixo_ext) and chave.endswith("]") and _valor_afirmativo(valor):
                codigo_item = chave[len(prefixo_ext):-1]
                itens.append(
                    ItemAfirmado(
                        codigo=chave,
                        texto=(detalhe.itens if detalhe else {}).get(codigo_item, codigo_item),
                        afirmacao="Y",
                    )
                )
        return itens

    if questao.tipo == "single" and valor_adocao in ADOPTION_VALUES:
        return []

    if questao.tipo == "single" and valor_base not in (None, ""):
        valor_codigo = _codigo_resposta_unica(questao, valor_base)
        return [
            ItemAfirmado(
                codigo=f"{base}[{valor_codigo}]",
                texto=questao.itens.get(valor_codigo, questao.texto),
                afirmacao=valor_codigo,
            )
        ]

    itens = []
    for codigo_item, texto in questao.itens.items():
        chave = f"{base}[{codigo_item}]"
        valor = resposta.get(chave)
        if _valor_afirmativo(valor):
            itens.append(ItemAfirmado(codigo=chave, texto=texto, afirmacao=str(valor)))
    return itens