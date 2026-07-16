#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Avalia comentarios do gestor para reavaliar nao conformidades de evidencias.

O script e um adaptador da fase de comentarios do gestor para o formato do
pipeline de avaliacao de evidencias. Ele gera checkpoints ``analyses*.jsonl``
compativeis com ``scripts.avaliacao_evidencias.consolidacao`` e, apos a
consolidacao, gera um XLSX de ajustes reversos compatível com
``scripts/ajustar_respostas_questionario.py``.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.avaliacao_evidencias.checkpoint import (
    calcular_identidade_analise,
    carregar_registros_analise,
    deve_processar_identidade,
    gerar_checkpoint_limpo,
    gravar_registro_analise,
    montar_registro_analise,
    nome_checkpoint_padrao,
    resolver_checkpoint_saida,
)
from scripts.avaliacao_evidencias.evidence_processing import (
    erro_tecnico_bloqueante_pacote,
    preparar_evidencia_para_provider,
    resultado_indica_erro_tecnico,
)
from scripts.avaliacao_evidencias.inventory import resolver_evidencia, rows_from_xlsx
from scripts.avaliacao_evidencias.prompts import (
    carregar_achados_set,
    filtrar_itens_por_prompt,
    preparar_itens_para_prompt,
    prompt_gera_achado,
    resolver_prompt,
)
from scripts.avaliacao_evidencias.providers import (
    REMOTE_PROVIDERS,
    conteudo_provider_textual,
    estimar_tokens_payload,
    executar_provider,
    limite_tokens_provider,
)
from scripts.avaliacao_evidencias.questionnaire import (
    ContextoQuestionario,
    ItemAfirmado,
    carregar_contexto_questionario,
)
from scripts.avaliacao_evidencias.reporting import (
    gerar_relatorio_conformidade,
    registros_pareceres_mais_recentes,
)
from scripts.avaliacao_evidencias.utils import (
    RequestsPerMinuteLimiter,
    componente_nome_arquivo,
    hash_arquivo,
    log_event,
    validar_rpm,
)
from scripts.resources.xlsx_utils import dataframe_to_xlsx_se_diferente


DEFAULT_AJUSTES = ROOT / "02-Execucao/01-Questionario/02-Ajustes_Respostas/ajustes_respostas_questionario_pos_avaliacao_evidencias.xlsx"
DEFAULT_QUESTIONARIO = ROOT / "01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md"
DEFAULT_PROMPTS = ROOT / "scripts/avaliacao_evidencias/prompts/igovti_2026_achados_binario_v1"
DEFAULT_CATALOG = ROOT / "scripts/avaliacao_evidencias/prompt_catalogs/igovti_2026_achados_binario_v1.yml"
DEFAULT_OUT = Path("/tmp/tcerj-igovti-2026/02-Execucao/05-Comentarios_Gestor/99-Reavaliacao_Evidencias")

ENV_PROVIDER_KEYS = {
    "gemini": "GEMINI_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
    "opencodego": "OPENCODEGO_API_KEY",
    "openai": "OPENAI_API_KEY",
}

NAO_PARECER_REVISOR = {"", "nan", "none", "sem_parecer", "sem parecer", "não revisado", "nao revisado"}
ESTADOS_CONFORMES = {"conforme"}
REV_EVI_RE = re.compile(r"^REVQ(\d{4})Evi$", re.IGNORECASE)


@dataclass(frozen=True)
class ItemReavaliacao:
    auditado: str
    codigo: str
    base: str
    resposta_afirmada: str
    resultado_anterior: str
    justificativa_anterior: str
    texto: str


@dataclass(frozen=True)
class AnaliseComentario:
    auditado: str
    base: str
    coluna_evidencia_original: str
    coluna_evidencia_comentarios: str
    coluna_comentario: str
    comentario: str
    nome_original_evidencia: str
    upload: dict[str, Any]
    resposta_id: Any
    evidence_index: int | None
    itens: list[ItemReavaliacao]
    erro_upload: str = ""


def _api_key_para(provider: str) -> str:
    env_key = ENV_PROVIDER_KEYS.get(provider, "")
    return os.environ.get(env_key, "") if env_key else ""


def normalizar_texto(valor: Any) -> str:
    if pd.isna(valor):
        return ""
    return str(valor).strip()


def normalizar_resultado(valor: Any) -> str:
    texto = normalizar_texto(valor)
    if not texto:
        return ""
    texto = re.sub(r"\s+", " ", texto)
    texto_lower = texto.casefold().replace("nao", "não")
    if texto_lower == "não conforme":
        return "Não conforme"
    if texto_lower == "conforme":
        return "Conforme"
    if texto_lower == "inconclusivo":
        return "Inconclusivo"
    return texto


def resultado_final(row: pd.Series) -> tuple[str, str]:
    avaliacao_revisor = normalizar_texto(row.get("Avaliação do auditor revisor"))
    if avaliacao_revisor.casefold() not in NAO_PARECER_REVISOR:
        return normalizar_resultado(avaliacao_revisor), normalizar_texto(row.get("Justificativa do auditor revisor"))
    return normalizar_resultado(row.get("Resultado da avaliação do juiz")), normalizar_texto(row.get("Justificativa do juiz"))


def item_base(codigo: str) -> str:
    match = re.match(r"^(q\d{4})", codigo.strip(), flags=re.IGNORECASE)
    return match.group(1).lower() if match else codigo.strip().lower()


def coluna_evidencia_original(base: str) -> str:
    return f"{base}evi"


def texto_item(contexto: ContextoQuestionario, codigo: str) -> str:
    codigo = codigo.strip()
    if codigo in contexto.questoes:
        return contexto.questoes[codigo].texto
    match_ext = re.match(r"^(q\d{4}ext)\[([^\]]+)\]$", codigo, flags=re.IGNORECASE)
    if match_ext:
        questao = contexto.questoes.get(match_ext.group(1).lower())
        return (questao.itens if questao else {}).get(match_ext.group(2), codigo)
    match_item = re.match(r"^(q\d{4})\[([^\]]+)\]$", codigo, flags=re.IGNORECASE)
    if match_item:
        questao = contexto.questoes.get(match_item.group(1).lower())
        return (questao.itens if questao else {}).get(match_item.group(2), codigo)
    return codigo


def carregar_nao_conformes(ajustes: Path, contexto: ContextoQuestionario) -> dict[tuple[str, str], list[ItemReavaliacao]]:
    df = pd.read_excel(ajustes)
    required = {"Auditado", "Código do item avaliado", "Resposta afirmada", "Resultado da avaliação do juiz", "Justificativa do juiz"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Colunas ausentes na planilha de ajustes: {', '.join(sorted(missing))}")

    itens: dict[tuple[str, str], list[ItemReavaliacao]] = {}
    for _, row in df.iterrows():
        auditado = normalizar_texto(row.get("Auditado")).upper()
        codigo = normalizar_texto(row.get("Código do item avaliado"))
        if not auditado or not codigo:
            continue
        resultado, justificativa = resultado_final(row)
        if resultado != "Não conforme":
            continue
        base = item_base(codigo)
        item = ItemReavaliacao(
            auditado=auditado,
            codigo=codigo,
            base=base,
            resposta_afirmada=normalizar_texto(row.get("Resposta afirmada")),
            resultado_anterior=resultado,
            justificativa_anterior=justificativa,
            texto=texto_item(contexto, codigo),
        )
        itens.setdefault((auditado, base), []).append(item)
    return itens


def parse_upload(valor: Any) -> tuple[dict[str, Any], str]:
    if valor in (None, "") or pd.isna(valor):
        return {}, ""
    if isinstance(valor, str):
        try:
            parsed = json.loads(valor)
        except json.JSONDecodeError as exc:
            return {}, f"metadados de upload invalidos: {exc.msg}"
    else:
        parsed = valor
    if not isinstance(parsed, list):
        return {}, "metadados de upload devem ser uma lista"
    if len(parsed) != 1:
        return {}, "coluna de evidencia deve conter exatamente um arquivo"
    upload = parsed[0]
    if not isinstance(upload, dict):
        return {}, "metadado de upload deve ser um objeto"
    name = upload.get("name")
    if not isinstance(name, str) or not name:
        return {}, "metadado de upload sem atributo name"
    return upload, ""


def inventariar_comentarios(
    respostas_comentarios: Path,
    nao_conformes: dict[tuple[str, str], list[ItemReavaliacao]],
    *,
    include_unsubmitted: bool = False,
    auditados: set[str] | None = None,
) -> list[AnaliseComentario]:
    linhas = list(rows_from_xlsx(respostas_comentarios))
    if not linhas:
        return []
    colunas = list(linhas[0].keys())
    colunas_evidencia = []
    for idx, coluna in enumerate((col for col in colunas if REV_EVI_RE.match(col)), start=1):
        match = REV_EVI_RE.match(coluna)
        if match:
            colunas_evidencia.append((idx, coluna, f"q{match.group(1)}"))

    analises: list[AnaliseComentario] = []
    for linha in linhas:
        if not include_unsubmitted and not linha.get("submitdate"):
            continue
        auditado = normalizar_texto(linha.get("firstname")).upper()
        if not auditado or (auditados is not None and auditado not in auditados):
            continue
        for evidence_index, coluna_evi, base in colunas_evidencia:
            itens = nao_conformes.get((auditado, base), [])
            if not itens:
                continue
            coluna_com = f"REV{base.upper()}Com"
            comentario = normalizar_texto(linha.get(coluna_com))
            upload, erro_upload = parse_upload(linha.get(coluna_evi))
            if not comentario and not upload and not erro_upload:
                continue
            analises.append(
                AnaliseComentario(
                    auditado=auditado,
                    base=base,
                    coluna_evidencia_original=coluna_evidencia_original(base),
                    coluna_evidencia_comentarios=coluna_evi,
                    coluna_comentario=coluna_com,
                    comentario=comentario,
                    nome_original_evidencia=normalizar_texto(upload.get("name")) if upload else "",
                    upload=upload,
                    resposta_id=linha.get("id"),
                    evidence_index=evidence_index,
                    itens=itens,
                    erro_upload=erro_upload,
                )
            )
    return analises


def montar_documentos_contexto(analise: AnaliseComentario) -> list[dict[str, Any]]:
    docs: list[dict[str, Any]] = []
    docs.append(
        {
            "nome": "comentario_gestor.txt",
            "tipo": "comentario_gestor",
            "texto": analise.comentario or "(sem comentario textual informado)",
        }
    )
    docs.append(
        {
            "nome": "nao_conformidade_original.json",
            "tipo": "contexto_reavaliacao",
            "texto": json.dumps(
                [
                    {
                        "item_codigo": item.codigo,
                        "resposta_afirmada_original": item.resposta_afirmada,
                        "resultado_anterior": item.resultado_anterior,
                        "justificativa_anterior": item.justificativa_anterior,
                    }
                    for item in analise.itens
                ],
                ensure_ascii=False,
                indent=2,
            ),
        }
    )
    return docs


def pacote_contexto_consolidacao(analise: AnaliseComentario) -> dict[str, Any]:
    return {
        "documentos": montar_documentos_contexto(analise),
        "inventario": ["comentario_gestor", "nao_conformidade_original"],
        "erro": "",
    }


def hash_contexto(analise: AnaliseComentario, hash_evidencia: str) -> str:
    payload = {
        "hash_evidencia": hash_evidencia,
        "comentario": analise.comentario,
        "itens": [
            {
                "codigo": item.codigo,
                "resposta_afirmada": item.resposta_afirmada,
                "justificativa_anterior": item.justificativa_anterior,
            }
            for item in analise.itens
        ],
    }
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def item_para_afirmado(item: ItemReavaliacao) -> ItemAfirmado:
    return ItemAfirmado(codigo=item.codigo, texto=item.texto, afirmacao=item.resposta_afirmada)


def cmd_avaliar(args: argparse.Namespace) -> int:
    if args.pdf2md_dpi <= 0:
        raise ValueError("--pdf2md-dpi deve ser maior que zero")

    prompts_dir = args.prompts_dir
    modos_processamento = []
    if args.pdf2md:
        modos_processamento.append("pdf2md")
    if args.docx2html:
        modos_processamento.append("docx2html")
    evidence_processing_mode = "+".join(modos_processamento)
    contexto = carregar_contexto_questionario(args.questionario)
    nao_conformes = carregar_nao_conformes(args.ajustes_pos_avaliacao_evidencias, contexto)
    auditados = {a.strip().upper() for item in (args.auditados or []) for a in item.split(",") if a.strip()} or None
    analises = inventariar_comentarios(
        args.respostas_comentarios,
        nao_conformes,
        include_unsubmitted=args.include_unsubmitted,
        auditados=auditados,
    )
    achados_set = carregar_achados_set(prompts_dir, args.catalog)
    rate_limiter = RequestsPerMinuteLimiter(args.rpm)

    checkpoint = resolver_checkpoint_saida(args.out_dir, args.out_file, args.provider, args.model)
    registros = carregar_registros_analise(checkpoint)

    log_event(
        "comentarios_gestor_pipeline_started",
        "Inicio da reavaliacao de evidencias a partir dos comentarios do gestor.",
        quiet=args.quiet,
        respostas_comentarios=str(args.respostas_comentarios),
        evidencias_comentarios_root=str(args.evidencias_comentarios_root),
        ajustes_pos_avaliacao_evidencias=str(args.ajustes_pos_avaliacao_evidencias),
        questionario=str(args.questionario),
        prompts_dir=str(prompts_dir),
        provider=args.provider,
        model=args.model,
        out_dir=str(args.out_dir),
        total_nao_conformes=sum(len(v) for v in nao_conformes.values()),
        total_analises=len(analises),
    )

    total_processadas = 0
    total_puladas = 0
    total_erros = 0
    total_concluidas = 0

    for index, analise in enumerate(analises, start=1):
        started_at = dt.datetime.now(dt.timezone.utc)
        base_log = {
            "index": index,
            "total": len(analises),
            "auditado": analise.auditado,
            "questao": analise.base,
            "coluna_evidencia": analise.coluna_evidencia_original,
            "coluna_evidencia_comentarios": analise.coluna_evidencia_comentarios,
            "evidencia": analise.nome_original_evidencia,
        }
        prompt = resolver_prompt(prompts_dir, analise.coluna_evidencia_original)
        gera_achado = analise.base in achados_set if achados_set else (prompt_gera_achado(prompt.conteudo) if prompt.caminho else False)
        itens = [item_para_afirmado(item) for item in analise.itens]
        itens = filtrar_itens_por_prompt(itens, prompt)
        itens_provider = preparar_itens_para_prompt(itens, prompt)

        hash_evidencia = ""
        resolucao = None
        if analise.upload and not prompt.erro:
            resolucao = resolver_evidencia(
                analise.auditado,
                args.evidencias_comentarios_root,
                analise.upload,
                resposta_id=analise.resposta_id,
                evidence_index=analise.evidence_index,
            )
            if not resolucao.erro and resolucao.caminho:
                hash_evidencia = hash_arquivo(resolucao.caminho)

        identity = calcular_identidade_analise(
            auditado=analise.auditado,
            coluna_evidencia=analise.coluna_evidencia_original,
            nome_original_evidencia=analise.nome_original_evidencia,
            hash_conteudo=hash_contexto(analise, hash_evidencia),
            provider=args.provider,
            model=args.model,
            prompt_hash=prompt.hash_conteudo,
            prompt_version=args.prompt_version,
            reasoning_effort=args.reasoning_effort,
            evidence_processing_mode=evidence_processing_mode,
        )
        if not deve_processar_identidade(registros, identity, skip_errors=args.skip_errors):
            total_puladas += 1
            log_event("analysis_skipped", "Reavaliacao ignorada por checkpoint.", quiet=args.quiet, identity=identity, **base_log)
            continue

        erro = prompt.erro or analise.erro_upload or (resolucao.erro if resolucao else "")
        if erro:
            gravar_registro_analise(
                checkpoint,
                montar_registro_analise(
                    identity=identity,
                    status="error",
                    auditado=analise.auditado,
                    questao_base=analise.base,
                    coluna_evidencia=analise.coluna_evidencia_original,
                    evidencia=analise.nome_original_evidencia,
                    provider=args.provider,
                    model=args.model,
                    started_at=started_at,
                    reasoning_effort=args.reasoning_effort,
                    evidence_processing_mode=evidence_processing_mode,
                    gera_achado=gera_achado,
                    error=erro,
                ),
            )
            registros[identity] = {"identity": identity, "status": "error"}
            total_processadas += 1
            total_erros += 1
            log_event("analysis_recorded_error", "Erro de inventario/prompt registrado.", quiet=args.quiet, level="error", identity=identity, error=erro, **base_log)
            continue

        if not itens_provider:
            total_puladas += 1
            log_event("analysis_skipped_no_items", "Nenhum item nao conforme avaliavel pelo prompt.", quiet=args.quiet, identity=identity, **base_log)
            continue

        with tempfile.TemporaryDirectory() as upload_tmp:
            pacote_provider: dict[str, Any] = {
                "documentos": montar_documentos_contexto(analise),
                "inventario": [],
                "erro": "",
                "arquivos_upload": [],
            }
            if resolucao and resolucao.caminho:
                pacote, arquivos_upload, erro_preparo = preparar_evidencia_para_provider(
                    resolucao.caminho,
                    upload_tmp,
                    pdf2md=args.pdf2md,
                    docx2html=args.docx2html,
                    dpi=args.pdf2md_dpi,
                )
                if erro_preparo:
                    erro = f"erro ao preparar evidencia para upload: {erro_preparo}"
                    gravar_registro_analise(
                        checkpoint,
                        montar_registro_analise(
                            identity=identity,
                            status="error",
                            auditado=analise.auditado,
                            questao_base=analise.base,
                            coluna_evidencia=analise.coluna_evidencia_original,
                            evidencia=analise.nome_original_evidencia,
                            provider=args.provider,
                            model=args.model,
                            started_at=started_at,
                            reasoning_effort=args.reasoning_effort,
                            evidence_processing_mode=evidence_processing_mode,
                            gera_achado=gera_achado,
                            error=erro,
                            result={"status": "error", "error": erro},
                        ),
                    )
                    registros[identity] = {"identity": identity, "status": "error"}
                    total_processadas += 1
                    total_erros += 1
                    continue
                erro_tecnico = erro_tecnico_bloqueante_pacote(pacote, arquivos_upload)
                if erro_tecnico:
                    erro = f"erro tecnico ao processar evidencia: {erro_tecnico}"
                    gravar_registro_analise(
                        checkpoint,
                        montar_registro_analise(
                            identity=identity,
                            status="error",
                            auditado=analise.auditado,
                            questao_base=analise.base,
                            coluna_evidencia=analise.coluna_evidencia_original,
                            evidencia=analise.nome_original_evidencia,
                            provider=args.provider,
                            model=args.model,
                            started_at=started_at,
                            reasoning_effort=args.reasoning_effort,
                            evidence_processing_mode=evidence_processing_mode,
                            gera_achado=gera_achado,
                            error=erro,
                            result={"status": "error", "error": erro},
                        ),
                    )
                    registros[identity] = {"identity": identity, "status": "error"}
                    total_processadas += 1
                    total_erros += 1
                    continue
                pacote_provider = {
                    "documentos": montar_documentos_contexto(analise) + pacote.documentos,
                    "inventario": pacote.inventario,
                    "erro": pacote.erro,
                    "arquivos_upload": arquivos_upload,
                }

            api_key = _api_key_para(args.provider)
            if args.provider in REMOTE_PROVIDERS and (api_key or args.provider == "openai"):
                wait_seconds = rate_limiter.wait_seconds()
                if wait_seconds > 0:
                    log_event("rate_limit_wait", "Aguardando limite de requests por minuto.", quiet=args.quiet, identity=identity, wait_seconds=round(wait_seconds, 3), **base_log)
                rate_limiter.wait_and_mark(wait_seconds)

            tokens_info = estimar_tokens_payload(
                prompt=prompt.conteudo,
                auditado=analise.auditado,
                questao_base=analise.base,
                coluna_evidencia=analise.coluna_evidencia_original,
                itens_afirmados=itens_provider,
                pacote=pacote_provider,
                provider=args.provider,
            )
            limite_tokens = limite_tokens_provider(args.provider, args.model)
            if limite_tokens and args.provider != "gemini" and tokens_info["tokens_total"] > limite_tokens:
                result = {"status": "error", "error": f"payload excede limite de tokens do provider: {tokens_info['tokens_total']:,} > {limite_tokens:,}"}
            else:
                result = executar_provider(
                    provider=args.provider,
                    model=args.model,
                    api_key=api_key,
                    prompt=prompt.conteudo,
                    auditado=analise.auditado,
                    questao_base=analise.base,
                    coluna_evidencia=analise.coluna_evidencia_original,
                    itens_afirmados=itens_provider,
                    pacote=pacote_provider,
                    reasoning_effort=args.reasoning_effort,
                )
            erro_tecnico_resultado = resultado_indica_erro_tecnico(result)
            if erro_tecnico_resultado:
                result = {"status": "error", "error": erro_tecnico_resultado, "raw_completed_result": result}
            status = result.get("status", "error") if isinstance(result, dict) else "error"
            prompt_payload = conteudo_provider_textual(
                prompt=prompt.conteudo,
                auditado=analise.auditado,
                questao_base=analise.base,
                coluna_evidencia=analise.coluna_evidencia_original,
                itens_afirmados=itens_provider,
                pacote={k: v for k, v in pacote_provider.items() if k != "arquivos_upload"},
            )
            registro = montar_registro_analise(
                identity=identity,
                status=status,
                auditado=analise.auditado,
                questao_base=analise.base,
                coluna_evidencia=analise.coluna_evidencia_original,
                evidencia=analise.nome_original_evidencia,
                provider=args.provider,
                model=args.model,
                started_at=started_at,
                reasoning_effort=args.reasoning_effort,
                evidence_processing_mode=evidence_processing_mode,
                gera_achado=gera_achado,
                result=result,
                error=result.get("error", "") if isinstance(result, dict) else "resultado invalido",
                prompt_payload=prompt_payload if args.store_prompts else None,
                payload_tokens=tokens_info,
            )
            registro["fase"] = "comentarios_gestor"
            registro["pacote_contexto_consolidacao"] = pacote_contexto_consolidacao(analise)
            gravar_registro_analise(checkpoint, registro)
            registros[identity] = {"identity": identity, "status": status}
            total_processadas += 1
            if status == "error":
                total_erros += 1
            else:
                total_concluidas += 1
            log_event("analysis_recorded", "Resultado da reavaliacao gravado.", quiet=args.quiet, identity=identity, status=status, **base_log)

    relatorio = checkpoint.parent / "relatorio_conformidade.xlsx"
    linhas_relatorio = gerar_relatorio_conformidade(checkpoint, relatorio)
    checkpoint_limpo = checkpoint.parent / f"analyses_clean_{componente_nome_arquivo(args.provider)}_{componente_nome_arquivo(args.model)}.jsonl"
    registros_limpos = gerar_checkpoint_limpo(checkpoint, checkpoint_limpo)
    log_event(
        "comentarios_gestor_pipeline_finished",
        "Reavaliacao de comentarios do gestor finalizada.",
        quiet=args.quiet,
        checkpoint=str(checkpoint),
        checkpoint_limpo=str(checkpoint_limpo),
        relatorio=str(relatorio),
        linhas_relatorio=linhas_relatorio,
        registros_limpos=registros_limpos,
        processadas=total_processadas,
        puladas=total_puladas,
        concluidas=total_concluidas,
        erros=total_erros,
    )
    return 0


def _estado_conforme(valor: Any) -> bool:
    return normalizar_texto(valor).casefold().replace("nao", "não") in ESTADOS_CONFORMES


def cmd_gerar_ajustes(args: argparse.Namespace) -> int:
    contexto = carregar_contexto_questionario(args.questionario)
    nao_conformes = carregar_nao_conformes(args.ajustes_pos_avaliacao_evidencias, contexto)
    por_item = {(item.auditado, item.codigo): item for itens in nao_conformes.values() for item in itens}

    registros = carregar_registros_analise(args.consolidado)
    linhas: list[dict[str, Any]] = []
    vistos: set[tuple[str, str]] = set()
    for registro in registros_pareceres_mais_recentes(registros.values()):
        if registro.get("status") != "completed":
            continue
        auditado = normalizar_texto(registro.get("auditado")).upper()
        result = registro.get("result") if isinstance(registro.get("result"), dict) else {}
        for conclusao in result.get("conclusoes") or []:
            if not isinstance(conclusao, dict) or not _estado_conforme(conclusao.get("estado")):
                continue
            codigo = normalizar_texto(conclusao.get("item_codigo"))
            chave = (auditado, codigo)
            item = por_item.get(chave)
            if not item or chave in vistos:
                continue
            vistos.add(chave)
            linhas.append(
                {
                    "Auditado": auditado,
                    "Código do item avaliado": codigo,
                    "Resposta afirmada": item.resposta_afirmada,
                    "Resposta ajustada": item.resposta_afirmada if item.resposta_afirmada else "Vazio",
                    "Resultado da avaliação do juiz": normalizar_resultado(conclusao.get("estado")),
                    "Justificativa do juiz": normalizar_texto(conclusao.get("justificativa")),
                    "Avaliação do auditor revisor": "",
                    "Justificativa do auditor revisor": "",
                    "Justificativa": (
                        "Retificacao pós-comentários do gestor: comentário e/ou nova evidência considerados "
                        "suficientes na consolidação da reavaliação."
                    ),
                    "observacao": normalizar_texto(conclusao.get("justificativa")),
                    "Fonte": "comentarios_gestor",
                    "Case ID": normalizar_texto(registro.get("case_id")),
                    "Identidade do parecer": normalizar_texto(registro.get("identity")),
                    "Opiniões válidas": registro.get("opinioes_validas", ""),
                    "Avaliadores ausentes": "; ".join(registro.get("avaliadores_ausentes") or []),
                    "Data do parecer": normalizar_texto(registro.get("finished_at")),
                }
            )

    df = pd.DataFrame(
        linhas,
        columns=[
            "Auditado",
            "Código do item avaliado",
            "Resposta afirmada",
            "Resposta ajustada",
            "Resultado da avaliação do juiz",
            "Justificativa do juiz",
            "Avaliação do auditor revisor",
            "Justificativa do auditor revisor",
            "Justificativa",
            "observacao",
            "Fonte",
            "Case ID",
            "Identidade do parecer",
            "Opiniões válidas",
            "Avaliadores ausentes",
            "Data do parecer",
        ],
    )
    dataframe_to_xlsx_se_diferente(
        df,
        args.output,
        index=False,
        sheet_name="Ajustes Comentarios Gestor",
    )
    print(f"OK: {len(df)} ajustes reversos gerados em {args.output}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    avaliar = sub.add_parser("avaliar", help="Gera analyses*.jsonl para reavaliacao dos comentarios do gestor.")
    avaliar.add_argument("--respostas-comentarios", type=Path, required=True, help="Exportacao XLSX do LimeSurvey de comentarios do gestor.")
    avaliar.add_argument("--evidencias-comentarios-root", type=Path, required=True, help="Pasta com anexos dos comentarios do gestor ja extraidos por auditado.")
    avaliar.add_argument("--ajustes-pos-avaliacao-evidencias", type=Path, default=DEFAULT_AJUSTES)
    avaliar.add_argument("--questionario", type=Path, default=DEFAULT_QUESTIONARIO)
    avaliar.add_argument("--prompts-dir", type=Path, default=DEFAULT_PROMPTS)
    avaliar.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    avaliar.add_argument("--provider", default="fake")
    avaliar.add_argument("--model", default="fake")
    avaliar.add_argument("--reasoning", "--reasoning-effort", dest="reasoning_effort", choices=["low", "medium", "high"], default="")
    avaliar.add_argument("--prompt-version", default="igovti_2026_comentarios_gestor_v1")
    avaliar.add_argument("--out-dir", type=Path, default=DEFAULT_OUT / "individuais")
    avaliar.add_argument("--out-file", default=None, help="Nome ou caminho do checkpoint JSONL. Padrao: analyses_<provider>_<model>.jsonl.")
    avaliar.add_argument("--rpm", type=validar_rpm, default=12)
    avaliar.add_argument("--skip-errors", action="store_true")
    avaliar.add_argument("--include-unsubmitted", action="store_true")
    avaliar.add_argument("--quiet", action="store_true")
    avaliar.add_argument("--store-prompts", action="store_true")
    avaliar.add_argument("--pdf2md", action="store_true")
    avaliar.add_argument("--pdf2md-dpi", type=int, default=150)
    avaliar.add_argument("--docx2html", action="store_true")
    avaliar.add_argument("--auditados", nargs="+", default=None)
    avaliar.set_defaults(func=cmd_avaliar)

    ajustes = sub.add_parser("gerar-ajustes", help="Gera XLSX de ajustes reversos a partir do consolidated.jsonl.")
    ajustes.add_argument("--consolidado", type=Path, required=True, help="Checkpoint consolidated.jsonl gerado pela consolidacao.")
    ajustes.add_argument("--ajustes-pos-avaliacao-evidencias", type=Path, default=DEFAULT_AJUSTES)
    ajustes.add_argument("--questionario", type=Path, default=DEFAULT_QUESTIONARIO)
    ajustes.add_argument("--output", type=Path, default=DEFAULT_OUT / "ajustes_respostas_questionario_pos_comentarios_gestor.xlsx")
    ajustes.set_defaults(func=cmd_gerar_ajustes)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
