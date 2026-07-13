#!/usr/bin/env python
"""Pipeline auditável das seções 1 e 2 dos comentários do gestor."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import os
import re
import tempfile
import unicodedata
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable
from xml.etree import ElementTree

import yaml
from openpyxl import Workbook, load_workbook
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parents[1]

from scripts.avaliacao_evidencias.evidence_processing import (
    erro_tecnico_bloqueante_pacote,
    preparar_evidencia_para_provider,
    resultado_indica_erro_tecnico,
)
from scripts.avaliacao_evidencias.inventory import resolver_evidencia
from scripts.avaliacao_evidencias.prompts import (
    filtrar_itens_por_prompt,
    preparar_itens_para_prompt,
    resolver_prompt,
)
from scripts.avaliacao_evidencias.providers import executar_provider
from scripts.avaliacao_evidencias.questionnaire import (
    ItemAfirmado,
    carregar_contexto_questionario,
)
from scripts.avaliacao_evidencias.utils import hash_arquivo


DEFAULT_LSS = ROOT / "02-Execucao/05-Comentarios_Gestor/questionario_comentarios_gestor.lss"
DEFAULT_RESULTADO = ROOT / "02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/resultado_auditoria.json"
DEFAULT_MAPA = ROOT / "02-Execucao/03-Execucao_Procedimentos/01-Insumos/mapa-verificacao-achados.xlsx"
DEFAULT_AJUSTES = ROOT / "02-Execucao/01-Questionario/02-Ajustes_Respostas/ajustes_respostas_questionario_pos_avaliacao_evidencias.xlsx"
DEFAULT_QUESTIONARIO = ROOT / "01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md"
DEFAULT_PROMPTS = ROOT / "scripts/avaliacao_evidencias/prompts/igovti_2026_achados_binario_v1"
DEFAULT_CATALOG = ROOT / "scripts/avaliacao_evidencias/prompt_catalogs/igovti_2026_achados_binario_v1.yml"
DEFAULT_CATALOG_COMENTARIOS = ROOT / "scripts/avaliacao_evidencias/prompt_catalogs/igovti_2026_comentarios_gestor_v1.yml"

ENV_PROVIDER_KEYS = {
    "gemini": "GEMINI_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
    "opencodego": "OPENCODEGO_API_KEY",
    "openai": "OPENAI_API_KEY",
}

ESTADOS_TEMPORAIS = {
    "mantida",
    "afastada_na_data_base",
    "corrigida_posteriormente",
    "inconclusiva",
}


@dataclass(frozen=True)
class SituacaoDef:
    codigo: str
    achado: int
    situacao: str


@dataclass(frozen=True)
class ItemAnterior:
    auditado: str
    codigo: str
    base: str
    resposta_afirmada: str
    resultado: str
    justificativa: str
    texto: str


def texto(valor: Any) -> str:
    return "" if valor is None else str(valor).strip()


def chave(valor: Any) -> str:
    bruto = unicodedata.normalize("NFKD", texto(valor).casefold())
    bruto = "".join(c for c in bruto if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", bruto).strip()


def base_item(codigo: str) -> str:
    match = re.match(r"^(q\d{4})", codigo, flags=re.I)
    return match.group(1).lower() if match else codigo.lower()


def ler_xlsx(path: Path) -> tuple[list[str], list[dict[str, Any]]]:
    wb = load_workbook(path, read_only=True, data_only=True)
    try:
        ws = wb.active
        rows = ws.iter_rows(values_only=True)
        headers = [texto(v) for v in next(rows)]
        dados = [dict(zip(headers, row)) for row in rows if any(v is not None for v in row)]
        return headers, dados
    finally:
        wb.close()


def consolidar_submissoes(rows: Iterable[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    validas: list[dict[str, Any]] = []
    excluidas: list[dict[str, Any]] = []
    for row in rows:
        if not row.get("submitdate"):
            excluidas.append({**row, "motivo_exclusao": "Submissão não concluída"})
        elif chave(row.get("firstname")) == "teste zip" or texto(row.get("token")) == "123":
            excluidas.append({**row, "motivo_exclusao": "Registro de teste"})
        else:
            validas.append(row)

    grupos: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in validas:
        identificador = texto(row.get("token")) or chave(row.get("firstname"))
        grupos[identificador].append(row)

    finais: list[dict[str, Any]] = []
    for grupo in grupos.values():
        ordenado = sorted(grupo, key=lambda r: texto(r.get("submitdate")))
        finais.append(ordenado[-1])
        for antiga in ordenado[:-1]:
            excluidas.append({**antiga, "motivo_exclusao": "Substituída por reenvio posterior do mesmo token"})
    finais.sort(key=lambda r: chave(r.get("firstname")))
    return finais, excluidas


def parse_uploads(valor: Any) -> list[dict[str, Any]]:
    if valor in (None, ""):
        return []
    parsed = json.loads(valor) if isinstance(valor, str) else valor
    if not isinstance(parsed, list):
        raise ValueError("metadados de upload devem ser uma lista")
    uploads: list[dict[str, Any]] = []
    for item in parsed:
        if not isinstance(item, dict) or not texto(item.get("name")):
            raise ValueError("metadado de upload inválido ou sem atributo name")
        uploads.append(item)
    return uploads


def indices_upload(headers: list[str]) -> dict[str, int]:
    colunas = [h for h in headers if "evi" in h.casefold() and not h.endswith("[filecount]")]
    return {coluna: idx for idx, coluna in enumerate(colunas, start=1)}


def limpar_html(valor: str) -> str:
    sem_tags = re.sub(r"<[^>]+>", " ", html.unescape(valor or ""))
    return re.sub(r"\s+", " ", sem_tags).strip()


def carregar_situacoes_lss(path: Path) -> dict[str, SituacaoDef]:
    root = ElementTree.parse(path).getroot()
    resultado: dict[str, SituacaoDef] = {}
    for row in root.findall("./questions/rows/row"):
        titulo = texto(row.findtext("title"))
        match = re.fullmatch(r"A(\d+)G(\d+)Conc", titulo, flags=re.I)
        if not match:
            continue
        pergunta_html = row.findtext("question") or ""
        strong = re.search(r"<strong>(.*?)</strong>", pergunta_html, flags=re.I | re.S)
        situacao = limpar_html(strong.group(1) if strong else pergunta_html)
        codigo = titulo[:-4]
        resultado[codigo] = SituacaoDef(codigo=codigo, achado=int(match.group(1)), situacao=situacao.rstrip("."))
    if not resultado:
        raise ValueError(f"nenhuma situação A#G# encontrada no LSS: {path}")
    return resultado


def carregar_acoes_mapa(path: Path) -> dict[str, dict[str, Any]]:
    wb = load_workbook(path, read_only=True, data_only=True)
    try:
        ws = wb["Ações de Verificação"]
        headers = [texto(v) for v in next(ws.iter_rows(min_row=3, max_row=3, values_only=True))]
        return {
            texto(row[0]): dict(zip(headers, row))
            for row in ws.iter_rows(min_row=4, values_only=True)
            if row and texto(row[0])
        }
    finally:
        wb.close()


def carregar_contextos_situacoes(resultado_path: Path, mapa_path: Path) -> dict[tuple[str, int, str], dict[str, Any]]:
    dados = json.loads(resultado_path.read_text(encoding="utf-8"))
    acoes = carregar_acoes_mapa(mapa_path)
    contextos: dict[tuple[str, int, str], dict[str, Any]] = {}
    for sigla, auditado in dados.items():
        for procedimento in auditado.get("procedimentos_executados", []):
            achado = procedimento.get("achado") or {}
            numero = int(achado.get("numero") or procedimento.get("numero_achado") or 0)
            for situacao in achado.get("situacoes_encontradas", []) or []:
                motivos = (achado.get("motivos_situacoes") or {}).get(situacao, []) or []
                motivos_enriquecidos = []
                for motivo in motivos:
                    refs = motivo.get("refs_acoes") or motivo.get("acoes_referencia") or []
                    if isinstance(refs, str):
                        refs = re.findall(r"AV\d+", refs)
                    motivos_enriquecidos.append(
                        {
                            **motivo,
                            "acoes": [acoes[ref] for ref in refs if ref in acoes],
                        }
                    )
                key = (texto(sigla).upper(), numero, chave(situacao.rstrip(".")))
                if key in contextos:
                    raise ValueError(f"situação duplicada no resultado de auditoria: {key}")
                contextos[key] = {
                    "achado": numero,
                    "nome_achado": achado.get("nome", ""),
                    "situacao": situacao,
                    "motivos": motivos_enriquecidos,
                    "evidencias": achado.get("evidencias_detalhadas") or achado.get("evidencias") or [],
                    "encaminhamentos": achado.get("encaminhamentos") or [],
                }
    return contextos


def resultado_anterior(row: dict[str, Any]) -> tuple[str, str]:
    revisao = texto(row.get("Avaliação do auditor revisor"))
    if chave(revisao) not in {"", "nan", "none", "sem parecer", "sem_parecer", "nao revisado"}:
        return revisao, texto(row.get("Justificativa do auditor revisor"))
    return texto(row.get("Resultado da avaliação do juiz")), texto(row.get("Justificativa do juiz"))


def carregar_itens_nao_conformes(path: Path, questionario: Path) -> dict[tuple[str, str], list[ItemAnterior]]:
    contexto = carregar_contexto_questionario(questionario)
    _, rows = ler_xlsx(path)
    itens: dict[tuple[str, str], list[ItemAnterior]] = defaultdict(list)
    for row in rows:
        auditado = texto(row.get("Auditado")).upper()
        codigo = texto(row.get("Código do item avaliado"))
        resultado, justificativa = resultado_anterior(row)
        if not auditado or not codigo or chave(resultado) != "nao conforme":
            continue
        base = base_item(codigo)
        item_texto = codigo
        questao = contexto.questoes.get(base)
        match = re.search(r"\[([^]]+)\]$", codigo)
        if questao and match:
            item_texto = questao.itens.get(match.group(1), codigo)
        elif questao:
            item_texto = questao.texto
        itens[(auditado, base)].append(
            ItemAnterior(
                auditado=auditado,
                codigo=codigo,
                base=base,
                resposta_afirmada=texto(row.get("Resposta afirmada")),
                resultado=resultado,
                justificativa=justificativa,
                texto=item_texto,
            )
        )
    return itens


def carregar_indice_consolidado(path: Path) -> dict[tuple[str, str], list[dict[str, Any]]]:
    indice: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for linha in path.read_text(encoding="utf-8").splitlines():
        if not linha.strip():
            continue
        registro = json.loads(linha)
        if registro.get("status") != "completed":
            continue
        auditado = texto(registro.get("auditado")).upper()
        result = registro.get("result") if isinstance(registro.get("result"), dict) else {}
        for conclusao in result.get("conclusoes") or []:
            codigo = texto(conclusao.get("item_codigo"))
            if codigo:
                indice[(auditado, codigo)].append(
                    {
                        "evidencia": registro.get("evidencia", ""),
                        "estado": conclusao.get("estado", ""),
                        "justificativa": conclusao.get("justificativa", ""),
                        "lacunas": conclusao.get("lacunas") or [],
                        "arquivos_referenciados": conclusao.get("arquivos_referenciados") or [],
                        "trechos_ou_elementos": conclusao.get("trechos_ou_elementos") or [],
                        "paginas_ou_localizacao": conclusao.get("paginas_ou_localizacao") or [],
                    }
                )
    return indice


def carregar_rotas_catalogo(path: Path) -> dict[str, list[dict[str, Any]]]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    rotas: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in data.get("prompts", []) or []:
        coluna = texto(entry.get("coluna_evidencia"))
        match = re.match(r"^(q\d{4})", coluna, flags=re.I)
        if not match:
            continue
        entry = dict(entry)
        entry["itens_avaliaveis"] = [texto(v) for v in entry.get("itens_avaliaveis", []) or []]
        rotas[match.group(1).lower()].append(entry)
    return rotas


def resolver_caminhos_upload(
    auditado: str,
    root: Path,
    uploads: list[dict[str, Any]],
    *,
    resposta_id: Any,
    evidence_index: int,
) -> list[Path]:
    caminhos: list[Path] = []
    for upload in uploads:
        resolucao = resolver_evidencia(
            auditado,
            root,
            upload,
            resposta_id=resposta_id,
            evidence_index=evidence_index,
        )
        if resolucao.erro or not resolucao.caminho:
            raise ValueError(resolucao.erro or f"arquivo não encontrado: {upload.get('name')}")
        caminhos.append(resolucao.caminho)
    return caminhos


def carregar_prompts_comentarios(path: Path) -> dict[str, str]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return {
        "situacoes": texto(data.get("prompt_situacoes")),
        "reavaliacao": texto(data.get("prompt_reavaliacao_prefixo")),
        "version": texto(data.get("version")),
    }


def api_key(provider: str) -> str:
    return os.environ.get(ENV_PROVIDER_KEYS.get(provider, ""), "")


def case_id(secao: str, auditado: str, codigo: str, resposta_id: Any, extra: str = "") -> str:
    bruto = json.dumps([secao, auditado, codigo, resposta_id, extra], ensure_ascii=False)
    return hashlib.sha256(bruto.encode("utf-8")).hexdigest()


def _resultado_fake_temporal(result: dict[str, Any], motivos: list[dict[str, Any]]) -> dict[str, Any]:
    for conclusao in result.get("conclusoes") or []:
        conclusao["estado_temporal"] = "inconclusiva"
        conclusao["conclusoes_motivos"] = [
            {
                "id_motivo": texto(m.get("id")),
                "estado_motivo": "inconclusivo",
                "justificativa": "Provider fake não emite conclusão substantiva.",
            }
            for m in motivos
        ]
        conclusao["providencias_informadas"] = []
        conclusao["comentarios_encaminhamento"] = ""
        conclusao["consequencias_praticas"] = []
        conclusao["alternativas_propostas"] = []
    return result


def executar_caso(
    caso: dict[str, Any],
    *,
    provider: str,
    model: str,
    reasoning: str,
    pdf2md: bool,
    docx2html: bool,
) -> dict[str, Any]:
    started = dt.datetime.now(dt.timezone.utc)
    with tempfile.TemporaryDirectory() as tmp:
        pacote = {
            "documentos": list(caso["documentos_contexto"]),
            "inventario": [d.get("nome", "") for d in caso["documentos_contexto"]],
            "erro": "",
            "arquivos_upload": [],
        }
        for caminho in caso["evidence_paths"]:
            preparado, arquivos, erro = preparar_evidencia_para_provider(
                Path(caminho), tmp, pdf2md=pdf2md, docx2html=docx2html, dpi=150
            )
            if erro:
                raise ValueError(f"erro ao preparar {caminho}: {erro}")
            bloqueante = erro_tecnico_bloqueante_pacote(preparado, arquivos)
            if bloqueante:
                raise ValueError(f"erro técnico ao processar {caminho}: {bloqueante}")
            pacote["documentos"].extend(preparado.documentos)
            pacote["inventario"].extend(preparado.inventario)
            pacote["arquivos_upload"].extend(arquivos)

        result = executar_provider(
            provider=provider,
            model=model,
            api_key=api_key(provider),
            prompt=caso["prompt"],
            auditado=caso["auditado"],
            questao_base=caso["codigo"],
            coluna_evidencia=caso["coluna_evidencia"],
            itens_afirmados=caso["itens"],
            pacote=pacote,
            reasoning_effort=reasoning,
        )
        erro_tecnico = resultado_indica_erro_tecnico(result)
        if erro_tecnico:
            result = {"status": "error", "error": erro_tecnico}
        if caso["secao"] == "situacoes" and provider == "fake" and result.get("status") == "completed":
            result = _resultado_fake_temporal(result, caso["contexto"].get("motivos", []))

    return {
        "identity": hashlib.sha256(
            json.dumps(
                [
                    caso["case_id"],
                    provider,
                    model,
                    caso["prompt_hash"],
                    [hash_arquivo(Path(p)) for p in caso["evidence_paths"]],
                ],
                sort_keys=True,
            ).encode("utf-8")
        ).hexdigest(),
        "case_id": caso["case_id"],
        "secao": caso["secao"],
        "auditado": caso["auditado"],
        "codigo": caso["codigo"],
        "coluna_evidencia": caso["coluna_evidencia"],
        "resposta_id": caso["resposta_id"],
        "provider": provider,
        "model": model,
        "started_at": started.isoformat(),
        "finished_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "status": result.get("status", "error"),
        "error": result.get("error", ""),
        "result": result,
        "contexto": caso["contexto"],
        "documentos_contexto": caso["documentos_contexto"],
        "evidence_paths": [str(p) for p in caso["evidence_paths"]],
        "evidencias": caso["evidencias"],
        "itens": [asdict(i) if hasattr(i, "__dataclass_fields__") else dict(i) for i in caso["itens"]],
        "prompt_hash": caso["prompt_hash"],
    }


def gravar_jsonl(path: Path, registros: Iterable[dict[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    registros = list(registros)
    with path.open("w", encoding="utf-8") as file:
        for registro in registros:
            file.write(json.dumps(registro, ensure_ascii=False, default=str) + "\n")
    return len(registros)

def _documento(nome: str, tipo: str, valor: Any) -> dict[str, Any]:
    conteudo = valor if isinstance(valor, str) else json.dumps(valor, ensure_ascii=False, indent=2, default=str)
    return {nome: nome, tipo: tipo, texto: conteudo}
