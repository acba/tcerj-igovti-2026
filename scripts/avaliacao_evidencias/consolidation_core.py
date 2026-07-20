"""Nucleo da consolidacao: agrupamento de opinioes, juiz fake e prompt juiz.

Estabelece as estruturas de agrupamento (ChaveEvidencia, GrupoEvidencia),
a leitura de opinioes de auditoria e o prompt padrao do juiz consolidador.
Este modulo nao chama providers nem grava checkpoint — essa orquestracao fica
em ``consolidacao.py`` (CLI), reutilizando ``evidence_processing`` e
``providers``.
"""
from __future__ import annotations

import csv
import json
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import unquote

from .inventory import _resolver_evidencia_exportada_limesurvey
from .questionnaire import ItemAfirmado
from .utils import caminho_is_file_safe, normalizar_nome


PROMPT_JUIZ_PADRAO = """Voce atua como equipe de auditoria governamental revisando avaliacoes preliminares de evidencias.

Sua tarefa e produzir um parecer consolidado de evidencia, revisavel pela equipe de auditoria, a partir de:
- a evidencia enviada pelo auditado, quando disponivel;
- avaliacoes preliminares;
- a opiniao da equipe de auditoria, quando fornecida.

Postura e linguagem:
- Use linguagem impessoal, imparcial, objetiva e simples.
- Nao trate o parecer consolidado como decisao final de auditoria.
- Nao use conhecimento externo para preencher lacunas da evidencia.
- Nao cite nomes de provedores ou modelos de IA, mesmo que aparecam nos dados recebidos.
- Nao escreva frases como "o modelo X avaliou", "todos os modelos analisados" ou equivalentes.
- Ao se referir a avaliacoes anteriores, use formulacoes institucionais e trate elas no singular: "A Equipe de Auditoria avalia que...", "A avaliacao da Equipe de Auditoria indica que..." ou "A avaliação realizada indica que...".

Regras de analise:
- Consolide a opinião majoritária apresentada nas avaliacoes recebidas.
- Se a opiniao da equipe de auditoria divergir das avaliacoes recebidas, explique criticamente o motivo da conclusao adotada.
- Fundamente cada conclusao com elementos da evidencia e/ou com a avaliacao critica das opinioes recebidas.
- Declare lacunas quando a evidencia ou as avaliacoes recebidas nao forem suficientes.

Padrao da justificativa:
- Escreva a justificativa como um paragrafo curto, preferencialmente com 3 a 5 frases.
- Siga esta ordem: conclusao objetiva; elementos da evidencia que sustentam a conclusao; análise crítica da suficiência da evidência; lacuna ou limitacao relevante, quando existir.
- Quando a evidencia for suficiente, indique o elemento verificavel utilizado, como trecho, pagina, tabela, ato, registro, imagem ou documento.
- Quando a evidencia for insuficiente, indique exatamente o elemento faltante.
- Nao inclua listas longas, digressoes, linguagem opinativa ou mencao a nomes de modelos.
- Não mencione avaliações recebidas, modelos, provedores, pluralidade de análises ou processo de consolidação.

Retorne somente JSON no schema solicitado.
"""


@dataclass(frozen=True)
class ChaveEvidencia:
    auditado: str
    questao: str
    coluna_evidencia: str
    evidencia: str


@dataclass(frozen=True)
class GrupoEvidencia:
    chave: ChaveEvidencia
    opinioes: list[dict[str, Any]]


def carregar_registros_processamento(caminhos: Iterable[str | Path]) -> list[dict[str, Any]]:
    registros_por_identidade: dict[str, dict[str, Any]] = {}
    sem_identidade: list[dict[str, Any]] = []
    for caminho in caminhos:
        path = Path(caminho)
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            registro = json.loads(line)
            registro["_source"] = str(path)
            registro["_line"] = line_number
            identidade = registro.get("identity")
            if isinstance(identidade, str) and identidade:
                registros_por_identidade[identidade] = registro
            else:
                sem_identidade.append(registro)
    return [*registros_por_identidade.values(), *sem_identidade]


def chave_evidencia(registro: dict[str, Any]) -> ChaveEvidencia:
    return ChaveEvidencia(
        auditado=str(registro.get("auditado") or ""),
        questao=str(registro.get("questao") or ""),
        coluna_evidencia=str(registro.get("coluna_evidencia") or ""),
        evidencia=str(registro.get("evidencia") or ""),
    )


def agrupar_opinioes_por_evidencia(registros: Iterable[dict[str, Any]]) -> list[GrupoEvidencia]:
    grupos: dict[ChaveEvidencia, list[dict[str, Any]]] = {}
    for registro in registros:
        chave = chave_evidencia(registro)
        grupos.setdefault(chave, []).append(registro)
    return [
        GrupoEvidencia(chave=chave, opinioes=opinioes)
        for chave, opinioes in sorted(
            grupos.items(),
            key=lambda item: (
                item[0].auditado,
                item[0].questao,
                item[0].coluna_evidencia,
                item[0].evidencia,
            ),
        )
    ]


def itens_afirmados_do_grupo(opinioes: list[dict[str, Any]]) -> list[ItemAfirmado]:
    """Obtém o escopo autoritativo do caso antes de recorrer a registros legados."""
    for opiniao in opinioes:
        itens_registro = opiniao.get("itens")
        if not isinstance(itens_registro, list) or not itens_registro:
            continue
        itens: list[ItemAfirmado] = []
        for item in itens_registro:
            if not isinstance(item, dict) or not str(item.get("codigo") or "").strip():
                continue
            itens.append(
                ItemAfirmado(
                    codigo=str(item.get("codigo") or ""),
                    texto=str(item.get("texto") or ""),
                    afirmacao=str(item.get("afirmacao") or ""),
                )
            )
        if itens:
            return itens

    for opiniao in opinioes:
        if str(opiniao.get("secao") or "") not in {"1", "situacoes"}:
            continue
        codigo = str(opiniao.get("codigo") or opiniao.get("questao") or "").strip()
        if codigo:
            return [ItemAfirmado(codigo=codigo, texto="", afirmacao="")]

    # Compatibilidade com checkpoints históricos da avaliação de evidências,
    # que ainda não gravavam os itens autoritativos no registro.
    por_codigo: dict[str, ItemAfirmado] = {}
    for opiniao in opinioes:
        result = opiniao.get("result") if isinstance(opiniao.get("result"), dict) else {}
        for conclusao in result.get("conclusoes") or []:
            if not isinstance(conclusao, dict):
                continue
            codigo = str(conclusao.get("item_codigo") or "")
            if not codigo or codigo in por_codigo:
                continue
            por_codigo[codigo] = ItemAfirmado(
                codigo=codigo,
                texto=str(conclusao.get("item_texto") or ""),
                afirmacao=str(conclusao.get("afirmacao_auditado") or ""),
            )
    return list(por_codigo.values())


def referencias_arquivos_do_grupo(opinioes: list[dict[str, Any]]) -> list[str]:
    referencias: list[str] = []
    for opiniao in opinioes:
        result = opiniao.get("result") if isinstance(opiniao.get("result"), dict) else {}
        for conclusao in result.get("conclusoes") or []:
            if not isinstance(conclusao, dict):
                continue
            for referencia in conclusao.get("arquivos_referenciados") or []:
                if isinstance(referencia, str) and referencia:
                    referencias.append(referencia)
    return referencias


def localizar_evidencia(
    raiz_evidencias: str | Path,
    chave: ChaveEvidencia,
    *,
    referencias_arquivos: Iterable[str] = (),
) -> Path | None:
    auditado_dir = Path(raiz_evidencias) / chave.auditado
    if not auditado_dir.is_dir():
        return None
    nomes = [unquote(chave.evidencia), chave.evidencia]
    for nome in nomes:
        caminho = auditado_dir / nome
        if caminho_is_file_safe(caminho):
            return caminho
    for referencia in referencias_arquivos:
        nome_referencia = Path(unquote(referencia)).name
        caminho = auditado_dir / nome_referencia
        if caminho_is_file_safe(caminho):
            return caminho
    exportado = _resolver_evidencia_exportada_limesurvey(auditado_dir, unquote(chave.evidencia))
    if exportado:
        return exportado
    alvo = normalizar_nome(unquote(chave.evidencia))
    try:
        candidatos = list(auditado_dir.iterdir())
    except OSError:
        return None
    for candidato in candidatos:
        if caminho_is_file_safe(candidato) and normalizar_nome(candidato.name) == alvo:
            return candidato
    return None


def _texto_opiniao_auditoria(registro: dict[str, Any]) -> str:
    for campo in ["opiniao_auditoria", "opiniao", "comentario", "justificativa", "parecer"]:
        valor = registro.get(campo)
        if valor not in (None, ""):
            return str(valor)
    return ""


def _chave_opiniao_auditoria(registro: dict[str, Any]) -> tuple[str, str, str, str]:
    return (
        str(registro.get("auditado") or ""),
        str(registro.get("questao") or ""),
        str(registro.get("coluna_evidencia") or ""),
        str(registro.get("evidencia") or ""),
    )


def carregar_opinioes_auditoria(caminho: str | Path | None) -> dict[tuple[str, str, str, str], str]:
    if not caminho:
        return {}
    path = Path(caminho)
    registros: list[dict[str, Any]] = []
    if path.suffix.lower() == ".jsonl":
        registros = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    elif path.suffix.lower() == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            registros = [item for item in payload if isinstance(item, dict)]
        elif isinstance(payload, dict):
            if isinstance(payload.get("opinioes"), list):
                registros = [item for item in payload["opinioes"] if isinstance(item, dict)]
            else:
                return {
                    tuple(str(part) for part in key.split("|", 3)): str(value)
                    for key, value in payload.items()
                    if isinstance(key, str) and key.count("|") == 3
                }
    elif path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            registros = list(csv.DictReader(file))
    return {
        _chave_opiniao_auditoria(registro): _texto_opiniao_auditoria(registro)
        for registro in registros
        if _texto_opiniao_auditoria(registro)
    }


def opiniao_auditoria_para_grupo(
    opinioes_auditoria: dict[tuple[str, str, str, str], str],
    grupo: GrupoEvidencia,
) -> str:
    chave = grupo.chave
    candidatos = [
        (chave.auditado, chave.questao, chave.coluna_evidencia, chave.evidencia),
        (chave.auditado, "", chave.coluna_evidencia, chave.evidencia),
        (chave.auditado, chave.questao, "", chave.evidencia),
        (chave.auditado, "", "", chave.evidencia),
    ]
    for candidato in candidatos:
        if candidato in opinioes_auditoria:
            return opinioes_auditoria[candidato]
    return ""


def avaliacoes_preliminares_para_juiz(opinioes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    avaliacoes: list[dict[str, Any]] = []
    for index, registro in enumerate(opinioes, start=1):
        result = registro.get("result") if isinstance(registro.get("result"), dict) else {}
        avaliacoes.append(
            {
                "avaliacao_id": f"avaliacao_{index}",
                "finished_at": registro.get("finished_at", ""),
                "conclusoes": result.get("conclusoes", []),
            }
        )
    return avaliacoes


def executar_juiz_fake(chave: ChaveEvidencia, opinioes: list[dict[str, Any]], itens: list[ItemAfirmado]) -> dict[str, Any]:
    modelos = sorted(
        {
            f"{opiniao.get('provider', '')}/{opiniao.get('model', '')}".strip("/")
            for opiniao in opinioes
        }
    )
    return {
        "status": "completed",
        "conclusoes": [
            {
                "item_codigo": item.codigo,
                "item_texto": item.texto,
                "afirmacao_auditado": item.afirmacao,
                "estado": "inconclusivo",
                "justificativa": "Juiz fake nao emite parecer substantivo.",
                "lacunas": ["Parecer consolidado real de IA nao executado."],
                "arquivos_referenciados": [chave.evidencia],
                "trechos_ou_elementos": modelos,
                "paginas_ou_localizacao": [],
            }
            for item in itens
        ],
    }


def questoes_achado_de_prompts_dir(
    prompts_dir: str | Path | None = None,
    catalog: str | Path | None = None,
) -> set[str]:
    from .prompts import carregar_achados_set
    return carregar_achados_set(prompts_dir, catalog)


def questoes_achado_de_registros(registros: Iterable[dict[str, Any]]) -> set[str]:
    questoes: set[str] = set()
    for registro in registros:
        if registro.get("gera_achado") and registro.get("questao"):
            questoes.add(str(registro["questao"]))
    return questoes


def _chave_logica_parecer(registro: dict[str, Any]) -> tuple[str, str, str, str, str]:
    """Chave logica de um parecer: (auditado, coluna, evidencia, judge_provider, judge_model)."""
    return (
        str(registro.get("auditado") or ""),
        str(registro.get("coluna_evidencia") or ""),
        str(registro.get("evidencia") or ""),
        str(registro.get("judge_provider") or ""),
        str(registro.get("judge_model") or ""),
    )


def indices_chaves_logicas(registros: dict[str, dict[str, Any]]) -> dict[tuple[str, str, str, str, str], str]:
    """Mapeia chave logica -> identity do registro mais recente."""
    resultado: dict[tuple[str, str, str, str, str], str] = {}
    for identity, registro in registros.items():
        chave = _chave_logica_parecer(registro)
        atual = resultado.get(chave)
        if atual is None or str(registro.get("finished_at") or "") >= str(registros[atual].get("finished_at") or ""):
            resultado[chave] = identity
    return resultado
