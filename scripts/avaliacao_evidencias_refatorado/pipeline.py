"""Pipeline de avaliacao de evidencias (refatorado).

Enxuto: apenas CLI, orquestracao do fluxo e logs estruturados. Toda a logica
de processamento de evidencias, providers de IA, contexto do questionario,
inventario, prompts, checkpoint e relatorios esta em modulos dedicados.

Os argumentos de entrada (argparse) sao identicos ao pipeline original em
``scripts/avaliacao_evidencias/pipeline.py``, mantendo compatibilidade total
com os orquestradores (``run_avaliacao_evidencias.py``) e os eventos de log
JSONL esperados.

Correcoes de performance:
- A planilha de respostas e lida uma unica vez e indexada por id em
  ``rows_by_id`` (dict), evitando releitura O(n^2) a cada analise.
- Contexto do questionario carregado uma unica vez.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any

from .checkpoint import (
    calcular_identidade_analise,
    carregar_registros_analise,
    deve_processar_identidade,
    gerar_checkpoint_limpo,
    gravar_registro_analise,
    identidade_para_erro_inventario,
    montar_registro_analise,
    nome_checkpoint_padrao,
    resolver_checkpoint_saida,
)
from .evidence_processing import (
    PacoteEvidencia,
    erro_tecnico_bloqueante_pacote,
    normalizar_evidencia,
    preparar_evidencia_para_provider,
    resultado_evidencia_ausente,
    resultado_indica_erro_tecnico,
)
from .inventory import (
    inventariar_analises,
    resolver_evidencia,
    rows_by_id,
)
from .prompts import (
    carregar_achados_set,
    colunas_com_prompt,
    filtrar_itens_por_prompt,
    preparar_itens_para_prompt,
    prompt_gera_achado,
    resolver_prompt,
)
from .providers import (
    REMOTE_PROVIDERS,
    conteudo_provider_textual,
    estimar_tokens_payload,
    executar_provider,
    limite_tokens_provider,
)
from .questionnaire import (
    carregar_contexto_questionario,
    selecionar_itens_afirmados,
)
from .reporting import gerar_relatorio_conformidade
from .utils import (
    RequestsPerMinuteLimiter,
    componente_nome_arquivo,
    hash_arquivo,
    log_event,
    validar_rpm,
)


ENV_PROVIDER_KEYS = {
    "gemini": "GEMINI_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
    "opencodego": "OPENCODEGO_API_KEY",
    "openai": "OPENAI_API_KEY",
}


def _api_key_para(provider: str) -> str:
    env_key = ENV_PROVIDER_KEYS.get(provider, "")
    return os.environ.get(env_key, "") if env_key else ""


def testar_conexao_provider(provider: str, model: str, api_key: str, reasoning_effort: str = "") -> bool:
    print(f"=== Testando conexao com provider: {provider} | modelo: {model} ===")
    env_key = ENV_PROVIDER_KEYS.get(provider, "")
    if provider in REMOTE_PROVIDERS and provider != "openai" and not api_key:
        print(f"[ERRO] A chave de API ({env_key}) nao esta configurada no ambiente!")
        return False

    prompt = "Teste de conexao de IA. Valide que voce recebeu esta mensagem."
    itens = [
        {
            "codigo": "test_01",
            "texto": "Teste de conexao",
            "afirmacao": "Mensagem de teste de conexao",
        }
    ]
    pacote = {
        "documentos": [],
        "inventario": [],
        "erro": "",
        "arquivos_upload": [],
    }
    try:
        resultado = executar_provider(
            provider=provider,
            model=model,
            api_key=api_key,
            prompt=prompt,
            auditado="TESTE",
            questao_base="qtest",
            coluna_evidencia="qtestevi",
            itens_afirmados=itens,
            pacote=pacote,
            reasoning_effort=reasoning_effort,
        )
        print("Resultado da chamada:")
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
        if isinstance(resultado, dict) and resultado.get("status") == "completed":
            print("\n[OK] Conexao e comunicacao com o modelo funcionando com sucesso!")
            return True
        print("\n[ERRO] O provider retornou um status inesperado ou erro.")
        return False
    except Exception as exc:
        print(f"\n[FALHA] Erro ao tentar se comunicar com o provider: {exc}")
        return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Pre-analisa evidencias enviadas por auditados.")
    parser.add_argument("respostas", nargs="?", default=None)
    parser.add_argument("evidencias", nargs="?", default=None)
    parser.add_argument("--questionario", default=None)
    parser.add_argument("--provider", default="fake")
    parser.add_argument("--model", default="fake")
    parser.add_argument(
        "--reasoning",
        "--reasoning-effort",
        dest="reasoning_effort",
        choices=["low", "medium", "high"],
        default="",
        help="Nivel de reasoning a solicitar ao provider quando suportado: low, medium ou high.",
    )
    parser.add_argument("--test-connection", action="store_true", help="Testa a conexao com o provider e modelo configurados e encerra.")
    parser.add_argument("--prompts-dir", default=None, help="Diretorio com Prompts de analise por questao.")
    parser.add_argument("--checklists-dir", default=None, help="Alias legado para --prompts-dir.")
    parser.add_argument("--out-dir", default=".saida_analise")
    parser.add_argument(
        "--out-file",
        default=None,
        help="Nome ou caminho do JSONL incremental de saida. Padrao: analyses_<provider>_<model>.jsonl dentro de --out-dir.",
    )
    parser.add_argument("--prompt-version", default="v1")
    parser.add_argument(
        "--only-prompts-present",
        action="store_true",
        help="Processa somente colunas de evidencia com prompt existente e registra item afirmado sem anexo como nao_conforme.",
    )
    parser.add_argument(
        "--only-achados",
        action="store_true",
        help="Processa somente colunas de evidencia cujo prompt esteja marcado como gera_achado: sim "
        "(questoes que ensejam achado no mapa de verificacao). Implicita o comportamento de "
        "--only-prompts-present e registra item afirmado sem anexo como nao_conforme.",
    )
    parser.add_argument(
        "--catalog",
        default=None,
        help="Caminho do catalogo YAML de prompts. Usado para derivar o conjunto de questoes-achado "
        "quando --only-achados esta ativo (le o atributo gera_achado do YAML).",
    )
    parser.add_argument(
        "--rpm",
        type=validar_rpm,
        default=12,
        help="Limita requests por minuto para providers remotos; padrao 12, 0 desativa.",
    )
    parser.add_argument("--skip-errors", action="store_true")
    parser.add_argument(
        "--include-unsubmitted",
        action="store_true",
        help="Inclui respostas sem submitdate. Por padrao, somente respostas submetidas sao analisadas.",
    )
    parser.add_argument("--list-only", action="store_true")
    parser.add_argument("--quiet", action="store_true", help="Nao emite logs estruturados durante a execucao.")
    parser.add_argument("--store-prompts", action="store_true", help="Armazena o payload textual completo enviado ao provider em cada registro JSONL.")
    parser.add_argument(
        "--pdf2md",
        "--pdf-markdown-images",
        dest="pdf2md",
        action="store_true",
        help="Para evidencias PDF, extrai Markdown e imagens com pymupdf4llm e envia esses artefatos ao modelo em vez do PDF original.",
    )
    parser.add_argument(
        "--pdf2md-dpi",
        "--pdf-markdown-images-dpi",
        dest="pdf2md_dpi",
        type=int,
        default=150,
        help="DPI usado nas imagens extraidas de PDF quando --pdf2md estiver ativo. Padrao: 150.",
    )
    parser.add_argument(
        "--docx2html",
        action="store_true",
        help="Para evidencias DOCX, extrai HTML e imagens com Mammoth e envia esses artefatos ao modelo em vez de converter o DOCX para PDF.",
    )
    parser.add_argument(
        "--auditados",
        nargs="+",
        default=None,
        help="Nomes de auditados (firstname) específicos para avaliar.",
    )
    args = parser.parse_args(argv)

    if args.auditados:
        auditados_flat = []
        for item in args.auditados:
            auditados_flat.extend([a.strip() for a in item.split(",") if a.strip()])
        args.auditados = auditados_flat

    if args.test_connection:
        api_key = _api_key_para(args.provider)
        sucesso = testar_conexao_provider(args.provider, args.model, api_key, args.reasoning_effort)
        return 0 if sucesso else 1

    if not args.respostas or not args.evidencias or not args.questionario:
        parser.error("Os argumentos respostas, evidencias e --questionario sao obrigatorios quando nao for --test-connection")
    if args.pdf2md_dpi <= 0:
        parser.error("--pdf2md-dpi deve ser maior que zero")

    prompts_dir = args.prompts_dir or args.checklists_dir or "checklists"
    modos_processamento = []
    if args.pdf2md:
        modos_processamento.append("pdf2md")
    if args.docx2html:
        modos_processamento.append("docx2html")
    evidence_processing_mode = "+".join(modos_processamento)
    filtrar_por_prompt = args.only_prompts_present or args.only_achados
    colunas_permitidas = (
        colunas_com_prompt(
            prompts_dir,
            args.questionario,
            only_achados=args.only_achados,
            catalog=args.catalog,
        )
        if filtrar_por_prompt
        else None
    )
    achados_set = carregar_achados_set(prompts_dir, args.catalog)
    rate_limiter = RequestsPerMinuteLimiter(args.rpm)
    log_event(
        "pipeline_started",
        "Inicio da avaliacao de evidencias.",
        quiet=args.quiet,
        respostas=args.respostas,
        evidencias=args.evidencias,
        questionario=args.questionario,
        prompts_dir=prompts_dir,
        provider=args.provider,
        model=args.model,
        reasoning_effort=args.reasoning_effort,
        out_dir=args.out_dir,
        out_file=args.out_file or nome_checkpoint_padrao(args.provider, args.model),
        prompt_version=args.prompt_version,
        rpm=args.rpm,
        include_unsubmitted=args.include_unsubmitted,
        skip_errors=args.skip_errors,
        list_only=args.list_only,
        store_prompts=args.store_prompts,
        pdf2md=args.pdf2md,
        pdf2md_dpi=args.pdf2md_dpi,
        docx2html=args.docx2html,
        auditados=args.auditados,
        only_prompts_present=args.only_prompts_present,
        only_achados=args.only_achados,
        colunas_com_prompt=sorted(colunas_permitidas or []),
    )
    analises = inventariar_analises(
        args.respostas,
        args.evidencias,
        args.questionario,
        include_unsubmitted=args.include_unsubmitted,
        colunas_evidencia_permitidas=colunas_permitidas,
        include_missing_evidence=filtrar_por_prompt,
    )
    if args.auditados:
        auditados_selecionados = {str(a).strip().upper() for a in args.auditados}
        analises = [a for a in analises if str(a.auditado).strip().upper() in auditados_selecionados]
    log_event(
        "inventory_completed",
        "Inventario de evidencias concluido.",
        quiet=args.quiet,
        total_analises=len(analises),
        analises_com_erro=sum(1 for analise in analises if analise.erro),
        auditados=sorted({analise.auditado for analise in analises if analise.auditado}),
    )
    if args.list_only:
        log_event(
            "list_only_started",
            "Listando analises candidatas sem processar evidencias.",
            quiet=args.quiet,
            total_analises=len(analises),
        )
        for analise in analises:
            print(json.dumps(analise.__dict__, ensure_ascii=False, default=str))
        log_event(
            "pipeline_finished",
            "Execucao finalizada em modo list-only.",
            quiet=args.quiet,
            total_analises=len(analises),
        )
        return 0

    # Performance: carregar contexto e rows_by_id uma unica vez.
    contexto = carregar_contexto_questionario(args.questionario)
    respostas_por_id = rows_by_id(args.respostas)

    checkpoint = resolver_checkpoint_saida(args.out_dir, args.out_file, args.provider, args.model)
    out_dir = checkpoint.parent
    registros = carregar_registros_analise(checkpoint)
    log_event(
        "checkpoint_loaded",
        "Checkpoint carregado para deduplicacao.",
        quiet=args.quiet,
        checkpoint=str(checkpoint),
        registros=len(registros),
    )
    total_processadas = 0
    total_puladas = 0
    total_erros = 0
    total_concluidas = 0
    for index, analise in enumerate(analises, start=1):
        analysis_started_at = dt.datetime.now(dt.timezone.utc)

        # Resolver prompt e questao base
        from .questionnaire import base_coluna_evidencia
        questao_base, _ = base_coluna_evidencia(analise.coluna_evidencia)
        base_log = {
            "index": index,
            "total": len(analises),
            "auditado": analise.auditado,
            "questao": questao_base,
            "coluna_evidencia": analise.coluna_evidencia,
            "evidencia": analise.nome_original_evidencia,
        }
        log_event("analysis_started", "Analise candidata iniciada.", quiet=args.quiet, **base_log)
        prompt = resolver_prompt(prompts_dir, analise.coluna_evidencia)
        gera_achado = (
            questao_base in achados_set
            if achados_set
            else (prompt_gera_achado(prompt.conteudo) if prompt.caminho else False)
        )

        # Erro de inventario
        if analise.erro:
            identity = identidade_para_erro_inventario(analise)
            if not deve_processar_identidade(registros, identity, skip_errors=args.skip_errors):
                total_puladas += 1
                log_event(
                    "analysis_skipped",
                    "Analise com erro de inventario ignorada por checkpoint.",
                    quiet=args.quiet,
                    identity=identity,
                    reason="checkpoint",
                    **base_log,
                )
            else:
                gravar_registro_analise(
                    checkpoint,
                    montar_registro_analise(
                        identity=identity,
                        status="error",
                        auditado=analise.auditado,
                        questao_base=questao_base,
                        coluna_evidencia=analise.coluna_evidencia,
                        evidencia=analise.nome_original_evidencia,
                        provider=args.provider,
                        model=args.model,
                        started_at=analysis_started_at,
                        reasoning_effort=args.reasoning_effort,
                        evidence_processing_mode=evidence_processing_mode,
                        gera_achado=gera_achado,
                        error=analise.erro,
                    ),
                )
                registros[identity] = {"identity": identity, "status": "error"}
                total_processadas += 1
                total_erros += 1
                log_event(
                    "analysis_recorded_error",
                    "Erro de inventario registrado no checkpoint.",
                    quiet=args.quiet,
                    level="error",
                    identity=identity,
                    error=analise.erro,
                    **base_log,
                )
            continue

        log_event(
            "prompt_resolved",
            "Resolucao do prompt de analise concluida.",
            quiet=args.quiet,
            level="error" if prompt.erro else "info",
            prompt=prompt.nome,
            prompt_hash=prompt.hash_conteudo,
            error=prompt.erro,
            **base_log,
        )

        # Resolver evidencia (se aplicavel)
        hash_conteudo = "" if analise.evidencia_ausente else None
        resolucao = None
        if hash_conteudo is None and not prompt.erro:
            resolucao = resolver_evidencia(
                analise.auditado,
                args.evidencias,
                analise.upload,
                resposta_id=analise.resposta_id,
                evidence_index=analise.evidence_index,
            )
            log_event(
                "evidence_resolved",
                "Resolucao do arquivo de evidencia concluida.",
                quiet=args.quiet,
                level="error" if resolucao.erro else "info",
                caminho=str(resolucao.caminho) if resolucao.caminho else "",
                nome_decodificado=resolucao.nome_decodificado,
                error=resolucao.erro,
                **base_log,
            )
            hash_conteudo = "" if resolucao.erro else hash_arquivo(resolucao.caminho)

        identity = calcular_identidade_analise(
            auditado=analise.auditado,
            coluna_evidencia=analise.coluna_evidencia,
            nome_original_evidencia=analise.nome_original_evidencia,
            hash_conteudo=hash_conteudo or "",
            provider=args.provider,
            model=args.model,
            prompt_hash=prompt.hash_conteudo,
            prompt_version=args.prompt_version,
            reasoning_effort=args.reasoning_effort,
            evidence_processing_mode=evidence_processing_mode,
        )
        if not deve_processar_identidade(registros, identity, skip_errors=args.skip_errors):
            total_puladas += 1
            log_event(
                "analysis_skipped",
                "Analise ignorada por ja existir no checkpoint.",
                quiet=args.quiet,
                identity=identity,
                reason="checkpoint",
                **base_log,
            )
            continue

        erro = prompt.erro or (resolucao.erro if resolucao else "")
        if erro:
            gravar_registro_analise(
                checkpoint,
                montar_registro_analise(
                    identity=identity,
                    status="error",
                    auditado=analise.auditado,
                    questao_base=questao_base,
                    coluna_evidencia=analise.coluna_evidencia,
                    evidencia=analise.nome_original_evidencia,
                    provider=args.provider,
                    model=args.model,
                    started_at=analysis_started_at,
                    reasoning_effort=args.reasoning_effort,
                    evidence_processing_mode=evidence_processing_mode,
                    gera_achado=gera_achado,
                    error=erro,
                ),
            )
            registros[identity] = {"identity": identity, "status": "error"}
            total_processadas += 1
            total_erros += 1
            log_event(
                "analysis_recorded_error",
                "Erro antes da chamada ao provider registrado no checkpoint.",
                quiet=args.quiet,
                level="error",
                identity=identity,
                error=erro,
                **base_log,
            )
            continue

        # Selecionar itens afirmados (usando rows_by_id — O(1) ao inves de O(n))
        resposta = respostas_por_id.get(analise.resposta_id, {})
        itens = selecionar_itens_afirmados(contexto, analise.coluna_evidencia, resposta)
        itens = filtrar_itens_por_prompt(itens, prompt)
        itens_provider = preparar_itens_para_prompt(itens, prompt)
        log_event(
            "items_selected",
            "Itens afirmados pelo auditado selecionados para avaliacao.",
            quiet=args.quiet,
            identity=identity,
            total_itens=len(itens),
            itens=[item.codigo for item in itens],
            textos_itens_visiveis=prompt_exibe_texto_itens_inline(prompt.conteudo),
            evidencia_ausente=analise.evidencia_ausente,
            **base_log,
        )

        if analise.evidencia_ausente and not itens:
            total_puladas += 1
            log_event(
                "analysis_skipped_missing_evidence_not_applicable",
                "Analise sem anexo ignorada porque nenhum item avaliavel foi afirmado.",
                quiet=args.quiet,
                identity=identity,
                **base_log,
            )
            continue

        if not itens:
            result = {"status": "completed", "conclusoes": [], "skip_reason": "nenhum_item_afirmado"}
            prompt_payload = conteudo_provider_textual(
                prompt=prompt.conteudo,
                auditado=analise.auditado,
                questao_base=questao_base,
                coluna_evidencia=analise.coluna_evidencia,
                itens_afirmados=itens_provider,
                pacote={"documentos": [], "inventario": [], "erro": "", "arquivos_upload": []},
            )
            gravar_registro_analise(
                checkpoint,
                montar_registro_analise(
                    identity=identity,
                    status=result["status"],
                    auditado=analise.auditado,
                    questao_base=questao_base,
                    coluna_evidencia=analise.coluna_evidencia,
                    evidencia=analise.nome_original_evidencia,
                    provider=args.provider,
                    model=args.model,
                    started_at=analysis_started_at,
                    reasoning_effort=args.reasoning_effort,
                    evidence_processing_mode=evidence_processing_mode,
                    gera_achado=gera_achado,
                    result=result,
                    error="",
                    prompt_payload=prompt_payload if args.store_prompts else None,
                ),
            )
            registros[identity] = {"identity": identity, "status": result["status"]}
            total_processadas += 1
            total_concluidas += 1
            log_event(
                "analysis_skipped_no_items",
                "Analise concluida sem chamada ao provider porque nenhum item foi afirmado.",
                quiet=args.quiet,
                identity=identity,
                checkpoint=str(checkpoint),
                **base_log,
            )
            continue

        if analise.evidencia_ausente:
            result = resultado_evidencia_ausente(itens_provider)
            prompt_payload = conteudo_provider_textual(
                prompt=prompt.conteudo,
                auditado=analise.auditado,
                questao_base=questao_base,
                coluna_evidencia=analise.coluna_evidencia,
                itens_afirmados=itens_provider,
                pacote={"documentos": [], "inventario": [], "erro": "evidencia ausente", "arquivos_upload": []},
            )
            gravar_registro_analise(
                checkpoint,
                montar_registro_analise(
                    identity=identity,
                    status=result["status"],
                    auditado=analise.auditado,
                    questao_base=questao_base,
                    coluna_evidencia=analise.coluna_evidencia,
                    evidencia=analise.nome_original_evidencia,
                    provider=args.provider,
                    model=args.model,
                    started_at=analysis_started_at,
                    reasoning_effort=args.reasoning_effort,
                    evidence_processing_mode=evidence_processing_mode,
                    gera_achado=gera_achado,
                    result=result,
                    error="",
                    prompt_payload=prompt_payload if args.store_prompts else None,
                ),
            )
            registros[identity] = {"identity": identity, "status": result["status"]}
            total_processadas += 1
            total_concluidas += 1
            log_event(
                "analysis_recorded_missing_evidence",
                "Item afirmado sem evidencia registrado como nao_conforme.",
                quiet=args.quiet,
                identity=identity,
                checkpoint=str(checkpoint),
                conclusoes=len(result["conclusoes"]),
                **base_log,
            )
            continue

        if resolucao is None or resolucao.caminho is None:
            raise RuntimeError("resolucao de evidencia ausente em analise com anexo")

        # Preparar evidencia para o provider (logica unificada em evidence_processing)
        with tempfile.TemporaryDirectory() as upload_tmp:
            pacote, arquivos_upload, erro_preparo = preparar_evidencia_para_provider(
                resolucao.caminho,
                upload_tmp,
                pdf2md=args.pdf2md,
                docx2html=args.docx2html,
                dpi=args.pdf2md_dpi,
            )
            if erro_preparo:
                log_event(
                    "upload_prepare_error",
                    "Erro ao preparar evidencia para upload ao provider.",
                    quiet=args.quiet,
                    level="error",
                    identity=identity,
                    error=erro_preparo,
                    **base_log,
                )
                gravar_registro_analise(
                    checkpoint,
                    montar_registro_analise(
                        identity=identity,
                        status="error",
                        auditado=analise.auditado,
                        questao_base=questao_base,
                        coluna_evidencia=analise.coluna_evidencia,
                        evidencia=analise.nome_original_evidencia,
                        provider=args.provider,
                        model=args.model,
                        started_at=analysis_started_at,
                        reasoning_effort=args.reasoning_effort,
                        evidence_processing_mode=evidence_processing_mode,
                        gera_achado=gera_achado,
                        result={"status": "error", "error": f"erro ao preparar evidencia para upload: {erro_preparo}"},
                        error=f"erro ao preparar evidencia para upload: {erro_preparo}",
                    ),
                )
                registros[identity] = {"identity": identity, "status": "error"}
                total_processadas += 1
                total_erros += 1
                continue

            log_event(
                "evidence_normalized",
                "Evidencia normalizada para envio ao provider.",
                quiet=args.quiet,
                level="warning" if pacote.erro else "info",
                identity=identity,
                tipo=pacote.tipo,
                documentos=len(pacote.documentos),
                inventario=len(pacote.inventario),
                duplicados_ignorados=list(pacote.duplicados_ignorados),
                error=pacote.erro,
                **base_log,
            )
            log_event(
                "upload_prepared",
                "Arquivos preparados para upload ao provider.",
                quiet=args.quiet,
                identity=identity,
                total_arquivos=len(arquivos_upload),
                arquivos=[Path(arquivo).name for arquivo in arquivos_upload],
                modo_processamento=evidence_processing_mode,
                **base_log,
            )
            erro_tecnico = erro_tecnico_bloqueante_pacote(pacote, arquivos_upload)
            if erro_tecnico:
                gravar_registro_analise(
                    checkpoint,
                    montar_registro_analise(
                        identity=identity,
                        status="error",
                        auditado=analise.auditado,
                        questao_base=questao_base,
                        coluna_evidencia=analise.coluna_evidencia,
                        evidencia=analise.nome_original_evidencia,
                        provider=args.provider,
                        model=args.model,
                        started_at=analysis_started_at,
                        reasoning_effort=args.reasoning_effort,
                        evidence_processing_mode=evidence_processing_mode,
                        gera_achado=gera_achado,
                        result={"status": "error", "error": f"erro tecnico ao processar evidencia: {erro_tecnico}"},
                        error=f"erro tecnico ao processar evidencia: {erro_tecnico}",
                    ),
                )
                registros[identity] = {"identity": identity, "status": "error"}
                total_processadas += 1
                total_erros += 1
                log_event(
                    "evidence_processing_error",
                    "Erro tecnico de processamento da evidencia registrado antes da chamada ao provider.",
                    quiet=args.quiet,
                    level="error",
                    identity=identity,
                    error=erro_tecnico,
                    **base_log,
                )
                continue

            api_key = _api_key_para(args.provider)
            tokens_info: dict[str, int] | None = None
            if args.provider in REMOTE_PROVIDERS and (api_key or args.provider == "openai"):
                wait_seconds = rate_limiter.wait_seconds()
                if wait_seconds > 0:
                    log_event(
                        "rate_limit_wait",
                        "Aguardando limite de requests por minuto antes da chamada ao provider.",
                        quiet=args.quiet,
                        identity=identity,
                        provider=args.provider,
                        model=args.model,
                        rpm=args.rpm,
                        wait_seconds=round(wait_seconds, 3),
                        resposta_id=analise.resposta_id,
                        itens=[item.codigo for item in itens],
                        **base_log,
                    )
                rate_limiter.wait_and_mark(wait_seconds)
            log_event(
                "provider_started",
                "Chamada ao provider iniciada.",
                quiet=args.quiet,
                identity=identity,
                provider=args.provider,
                model=args.model,
                **base_log,
            )
            pacote_provider = {
                "documentos": pacote.documentos,
                "inventario": pacote.inventario,
                "erro": pacote.erro,
                "arquivos_upload": arquivos_upload,
            }
            prompt_payload = conteudo_provider_textual(
                prompt=prompt.conteudo,
                auditado=analise.auditado,
                questao_base=questao_base,
                coluna_evidencia=analise.coluna_evidencia,
                itens_afirmados=itens_provider,
                pacote={k: v for k, v in pacote_provider.items() if k != "arquivos_upload"},
            )

            def on_provider_event(event: str, fields: dict[str, Any]) -> None:
                log_event(
                    event,
                    "Evento do provider durante a chamada.",
                    quiet=args.quiet,
                    level="warning",
                    provider=args.provider,
                    model=args.model,
                    identity=identity,
                    **base_log,
                    **fields,
                )

            tokens_info = estimar_tokens_payload(
                prompt=prompt.conteudo,
                auditado=analise.auditado,
                questao_base=questao_base,
                coluna_evidencia=analise.coluna_evidencia,
                itens_afirmados=itens_provider,
                pacote=pacote_provider,
                provider=args.provider,
            )
            log_event(
                "payload_tokens_estimated",
                "Tokens do payload estimados antes da chamada ao provider.",
                quiet=args.quiet,
                identity=identity,
                **tokens_info,
                **base_log,
            )
            limite_tokens = limite_tokens_provider(args.provider, args.model)
            if limite_tokens and args.provider != "gemini" and tokens_info["tokens_total"] > limite_tokens:
                result = {
                    "status": "error",
                    "error": (
                        f"payload excede limite de tokens do provider: "
                        f"{tokens_info['tokens_total']:,} > {limite_tokens:,} "
                        f"(texto={tokens_info['tokens_texto']:,}, "
                        f"pdfs={tokens_info['n_pdfs']}({tokens_info['tokens_pdfs']:,}), "
                        f"imagens={tokens_info['n_imagens']}({tokens_info['tokens_imagens']:,}))"
                    ),
                }
                log_event(
                    "payload_tokens_exceeded",
                    "Payload bloqueado por exceder limite de tokens do provider.",
                    quiet=args.quiet,
                    level="warning",
                    identity=identity,
                    tokens_total=tokens_info["tokens_total"],
                    limite=limite_tokens,
                    provider=args.provider,
                    model=args.model,
                    **base_log,
                )
            else:
                result = executar_provider(
                    provider=args.provider,
                    model=args.model,
                    api_key=api_key,
                    prompt=prompt.conteudo,
                    auditado=analise.auditado,
                    questao_base=questao_base,
                    coluna_evidencia=analise.coluna_evidencia,
                    itens_afirmados=itens_provider,
                    pacote=pacote_provider,
                    reasoning_effort=args.reasoning_effort,
                    on_event=on_provider_event,
                )
            if isinstance(result, dict) and result.get("all_keys_exhausted"):
                wait_seconds = float(result.get("retry_after_seconds", 60))
                log_event(
                    "all_keys_exhausted",
                    f"Todas as chaves {args.provider} exauridas. Registrando erro e passando para o proximo item.",
                    quiet=args.quiet,
                    level="warning",
                    provider=args.provider,
                    model=args.model,
                    retry_after_seconds=round(wait_seconds, 1),
                    available_keys=0,
                    **base_log,
                )
                result = {
                    "status": "error",
                    "error": f"todas as chaves {args.provider} exauridas (retry_after {wait_seconds:.0f}s)",
                }
            erro_tecnico_resultado = resultado_indica_erro_tecnico(result)
            if erro_tecnico_resultado:
                result = {
                    "status": "error",
                    "error": erro_tecnico_resultado,
                    "raw_completed_result": result,
                }

            conclusoes = result.get("conclusoes") if isinstance(result, dict) else None
            log_event(
                "provider_finished",
                "Chamada ao provider finalizada.",
                quiet=args.quiet,
                level="error" if (isinstance(result, dict) and result.get("status") == "error") else "info",
                identity=identity,
                provider=args.provider,
                model=args.model,
                status=result.get("status") if isinstance(result, dict) else None,
                conclusoes=len(conclusoes or []),
                error=result.get("error", "") if isinstance(result, dict) else "",
                **base_log,
            )
            status = result.get("status", "error") if isinstance(result, dict) else "error"
            gravar_registro_analise(
                checkpoint,
                montar_registro_analise(
                    identity=identity,
                    status=status,
                    auditado=analise.auditado,
                    questao_base=questao_base,
                    coluna_evidencia=analise.coluna_evidencia,
                    evidencia=analise.nome_original_evidencia,
                    provider=args.provider,
                    model=args.model,
                    started_at=analysis_started_at,
                    reasoning_effort=args.reasoning_effort,
                    evidence_processing_mode=evidence_processing_mode,
                    gera_achado=gera_achado,
                    result=result,
                    error=result.get("error", "") if isinstance(result, dict) else "resultado invalido",
                    prompt_payload=prompt_payload if args.store_prompts else None,
                    payload_tokens=tokens_info,
                ),
            )
            registros[identity] = {"identity": identity, "status": status}
            total_processadas += 1
            if status == "error":
                total_erros += 1
            else:
                total_concluidas += 1
            log_event(
                "analysis_recorded",
                "Resultado da analise gravado no checkpoint.",
                quiet=args.quiet,
                identity=identity,
                status=status,
                checkpoint=str(checkpoint),
                **base_log,
            )

    relatorio = out_dir / "relatorio_conformidade.xlsx"
    linhas_relatorio = gerar_relatorio_conformidade(checkpoint, relatorio)
    log_event(
        "report_generated",
        "Relatorio de conformidade gerado.",
        quiet=args.quiet,
        relatorio=str(relatorio),
        linhas=linhas_relatorio,
    )
    checkpoint_limpo = out_dir / f"analyses_clean_{componente_nome_arquivo(args.provider)}_{componente_nome_arquivo(args.model)}.jsonl"
    registros_limpos = gerar_checkpoint_limpo(checkpoint, checkpoint_limpo)
    log_event(
        "clean_checkpoint_generated",
        "Checkpoint limpo (somente completed) gerado.",
        quiet=args.quiet,
        checkpoint_limpo=str(checkpoint_limpo),
        registros=registros_limpos,
    )
    log_event(
        "pipeline_finished",
        "Execucao do pipeline finalizada.",
        quiet=args.quiet,
        total_analises=len(analises),
        processadas=total_processadas,
        puladas=total_puladas,
        concluidas=total_concluidas,
        erros=total_erros,
        checkpoint=str(checkpoint),
        checkpoint_limpo=str(checkpoint_limpo),
        relatorio=str(relatorio),
    )
    return 0


def prompt_exibe_texto_itens_inline(conteudo: str) -> bool:
    """Inline helper para log; espelha prompts.prompt_exibe_texto_itens."""
    from .prompts import prompt_exibe_texto_itens
    return prompt_exibe_texto_itens(conteudo)


if __name__ == "__main__":
    raise SystemExit(main())