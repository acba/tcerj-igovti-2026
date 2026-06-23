"""Resolucao de prompts/checklists por questao e metadados embutidos nos
prompts markdown (itens_avaliaveis, exibir_texto_itens, gera_achado). Tambem
carrega o conjunto de questoes-achado a partir do catalogo YAML ou dos
marcadores markdown.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from scripts import md2lss

from .questionnaire import ItemAfirmado, base_coluna_evidencia


@dataclass(frozen=True)
class PromptResolvido:
    nome: str
    caminho: Path | None
    conteudo: str
    hash_conteudo: str
    erro: str = ""


@dataclass(frozen=True)
class ChecklistResolvido:
    nome: str
    caminho: Path | None
    conteudo: str
    hash_conteudo: str
    erro: str = ""


_NOME_PROMPT_ACHADO_RE = re.compile(r"^(q\d{4})(?:_[A-Z])?\.md$", re.IGNORECASE)


def resolver_prompt(prompts_dir: str | Path, coluna_evidencia: str) -> PromptResolvido:
    base, item_especifico = base_coluna_evidencia(coluna_evidencia)
    raiz = Path(prompts_dir)
    candidatos = []
    if item_especifico:
        candidatos.append(raiz / f"{base}_{item_especifico}.md")
    candidatos.append(raiz / f"{base}.md")
    for caminho in candidatos:
        if caminho.is_file():
            conteudo = caminho.read_text(encoding="utf-8")
            digest = hashlib.sha256(conteudo.encode("utf-8")).hexdigest()
            return PromptResolvido(
                nome=caminho.name,
                caminho=caminho,
                conteudo=conteudo,
                hash_conteudo=digest,
            )
    return PromptResolvido(
        nome="",
        caminho=None,
        conteudo="",
        hash_conteudo="",
        erro=f"prompt de analise nao encontrado para {coluna_evidencia}",
    )


def resolver_checklist(checklists_dir: str | Path, coluna_evidencia: str) -> ChecklistResolvido:
    base, item_especifico = base_coluna_evidencia(coluna_evidencia)
    raiz = Path(checklists_dir)
    candidatos = []
    if item_especifico:
        candidatos.append(raiz / f"{base}_{item_especifico}.md")
    candidatos.append(raiz / f"{base}.md")
    for caminho in candidatos:
        if caminho.is_file():
            conteudo = caminho.read_text(encoding="utf-8")
            digest = hashlib.sha256(conteudo.encode("utf-8")).hexdigest()
            return ChecklistResolvido(
                nome=caminho.name,
                caminho=caminho,
                conteudo=conteudo,
                hash_conteudo=digest,
            )
    return ChecklistResolvido(
        nome="",
        caminho=None,
        conteudo="",
        hash_conteudo="",
        erro=f"checklist de analise nao encontrado para {coluna_evidencia}",
    )


def colunas_com_prompt(
    prompts_dir: str | Path,
    caminho_questionario: str | Path,
    *,
    only_achados: bool = False,
    catalog: str | Path | None = None,
) -> set[str]:
    from .inventory import coluna_evidencia
    achados_set = carregar_achados_set(prompts_dir, catalog) if only_achados else set()
    survey = md2lss.parse_markdown(Path(caminho_questionario))
    colunas: set[str] = set()
    for group in survey.groups:
        for question in group.questions:
            if question.type == "upload" and coluna_evidencia(question.code):
                prompt = resolver_prompt(prompts_dir, question.code)
                if prompt.caminho is None:
                    continue
                if only_achados:
                    base, _ = base_coluna_evidencia(question.code)
                    if base not in achados_set:
                        continue
                colunas.add(question.code)
    return colunas


def itens_avaliaveis_prompt(conteudo: str) -> set[str]:
    match = re.search(r"<!--\s*itens_avaliaveis:\s*(.*?)\s*-->", conteudo)
    if not match:
        return set()
    return {item.strip() for item in match.group(1).split(",") if item.strip()}


def filtrar_itens_por_prompt(itens: list[ItemAfirmado], prompt: PromptResolvido) -> list[ItemAfirmado]:
    permitidos = itens_avaliaveis_prompt(prompt.conteudo)
    if not permitidos:
        return itens
    return [item for item in itens if item.codigo in permitidos]


def prompt_exibe_texto_itens(conteudo: str) -> bool:
    match = re.search(r"<!--\s*exibir_texto_itens:\s*(.*?)\s*-->", conteudo)
    if not match:
        return True
    valor = match.group(1).strip().lower()
    return valor not in {"nao", "não", "false", "0", "no"}


def prompt_gera_achado(conteudo: str) -> bool:
    match = re.search(r"<!--\s*gera_achado:\s*(.*?)\s*-->", conteudo)
    if not match:
        return False
    valor = match.group(1).strip().lower()
    return valor in {"sim", "true", "1", "yes"}


def carregar_achados_set(
    prompts_dir: str | Path | None = None,
    catalog: str | Path | None = None,
) -> set[str]:
    """Conjunto de questoes-raiz marcadas como gera_achado.

    Fonte primaria: catalogo YAML informado em ``catalog`` (le o atributo
    ``gera_achado`` de cada entrada de ``prompts``). Fallback: marcadores
    ``<!-- gera_achado: sim -->`` nos prompts markdown de ``prompts_dir``.
    """
    if catalog:
        return _achados_de_catalogo(catalog)
    if prompts_dir:
        return _achados_de_prompts_dir(prompts_dir)
    return set()


def _achados_de_catalogo(caminho: str | Path) -> set[str]:
    import yaml

    with Path(caminho).open(encoding="utf-8") as file:
        data = yaml.safe_load(file)
    if not isinstance(data, dict):
        return set()
    questoes: set[str] = set()
    for entrada in data.get("prompts", []) or []:
        if not isinstance(entrada, dict) or not entrada.get("gera_achado"):
            continue
        arquivo = str(entrada.get("arquivo") or "")
        match = _NOME_PROMPT_ACHADO_RE.match(arquivo)
        if match:
            questoes.add(match.group(1))
    return questoes


def _achados_de_prompts_dir(prompts_dir: str | Path) -> set[str]:
    raiz = Path(prompts_dir)
    questoes: set[str] = set()
    for caminho in raiz.glob("*.md"):
        match = _NOME_PROMPT_ACHADO_RE.match(caminho.name)
        if not match:
            continue
        try:
            conteudo = caminho.read_text(encoding="utf-8")
        except OSError:
            continue
        if prompt_gera_achado(conteudo):
            questoes.add(match.group(1))
    return questoes


def preparar_itens_para_prompt(itens: list[ItemAfirmado], prompt: PromptResolvido) -> list[ItemAfirmado]:
    if prompt_exibe_texto_itens(prompt.conteudo):
        return itens
    return [
        ItemAfirmado(
            codigo=item.codigo,
            texto=item.codigo,
            afirmacao=item.afirmacao,
        )
        for item in itens
    ]