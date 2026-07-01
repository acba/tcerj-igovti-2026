"""Consolidacao de pareceres por evidencia (refatorado).

Enxuto: apenas CLI, orquestracao do juiz e logs. Reutiliza
``evidence_processing.preparar_evidencia_para_provider`` (mesmo tratamento de
evidencias do pipeline) e ``providers.executar_provider``. A diferenca principal
e o prompt: este modulo age como juiz, decidindo a avaliacao final a partir
das avaliacoes preliminares dos modelos.

Os argumentos de entrada (argparse) sao identicos a ``consolidacao.py`` no
pacote original, mantendo compatibilidade com os orquestradores
(``run_consolida_avaliacoes_v2.py``) e os eventos de log JSONL esperados.
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
    carregar_registros_analise,
    gravar_registro_analise,
)
from .consolidation_core import (
    PROMPT_JUIZ_PADRAO,
    ChaveEvidencia,
    agrupar_opinioes_por_evidencia,
    avaliacoes_preliminares_para_juiz,
    carregar_opinioes_auditoria,
    carregar_registros_processamento,
    executar_juiz_fake,
    indices_chaves_logicas,
    itens_afirmados_do_grupo,
    localizar_evidencia,
    opiniao_auditoria_para_grupo,
    questoes_achado_de_prompts_dir,
    questoes_achado_de_registros,
    referencias_arquivos_do_grupo,
)
from .evidence_processing import (
    PacoteEvidencia,
    erro_tecnico_bloqueante_pacote,
    normalizar_evidencia,
    preparar_evidencia_para_provider,
)
from .providers import (
    REMOTE_PROVIDERS,
    conteudo_provider_textual,
    estimar_tokens_payload,
    executar_provider,
    limite_tokens_provider,
)
from .reporting import gerar_checkpoint_limpo_consolidado, gerar_relatorio_pareceres
from .utils import (
    RequestsPerMinuteLimiter,
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Consolida opinioes de modelos em um parecer por evidencia.")
    parser.add_argument("analyses", nargs="+", help="Arquivos analyses.jsonl gerados pelo processamento de evidencias.")
    parser.add_argument("--evidencias-root", default=None, help="Raiz de evidencias para reenviar a evidencia ao juiz.")
    parser.add_argument("--auditor-opinions", default=None, help="JSON/JSONL/CSV com opinioes opcionais da auditoria.")
    parser.add_argument("--judge-provider", default="fake")
    parser.add_argument("--judge-model", default="fake")
    parser.add_argument("--out-dir", default=".saida_analise")
    parser.add_argument("--prompt-version", default="juiz-v2")
    parser.add_argument("--rpm", type=validar_rpm, default=0)
    parser.add_argument("--skip-errors", action="store_true")
    parser.add_argument("--list-only", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument(
        "--reasoning",
        "--reasoning-effort",
        dest="reasoning_effort",
        choices=["low", "medium", "high"],
        default="",
        help="Nivel de reasoning a solicitar ao juiz quando suportado: low, medium ou high.",
    )
    parser.add_argument(
        "--store-prompts",
        action="store_true",
        help="Armazena o payload textual completo enviado ao juiz em cada registro JSONL.",
    )
    parser.add_argument(
        "--only-achados",
        action="store_true",
        help="Consolida somente grupos cuja questao-raiz enseja achado no mapa de verificacao. "
        "O conjunto de questoes-achado e obtido de --prompts-dir (marcadores gera_achado) ou, "
        "na ausencia deste, do campo gera_achado dos registros analyses.",
    )
    parser.add_argument(
        "--prompts-dir",
        default=None,
        help="Diretorio com prompts markdown usado para derivar o conjunto de questoes-achado "
        "quando --only-achados estiver ativo (fallback via marcadores no markdown).",
    )
    parser.add_argument(
        "--catalog",
        default=None,
        help="Caminho do catalogo YAML de prompts. Fonte primaria do conjunto de questoes-achado "
        "quando --only-achados esta ativo (le o atributo gera_achado do YAML).",
    )
    parser.add_argument(
        "--pdf2md",
        action="store_true",
        help="Converte PDFs para markdown+imagens com pymupdf4llm antes de enviar ao juiz.",
    )
    parser.add_argument(
        "--docx2html",
        action="store_true",
        help="Converte DOCX para HTML+imagens com mammoth antes de enviar ao juiz.",
    )
    parser.add_argument(
        "--pdf2md-dpi",
        type=int,
        default=150,
        help="DPI para extracao de imagens no pdf2md (default: 150).",
    )
    args = parser.parse_args(argv)

    log_event(
        "consolidation_started",
        "Inicio da consolidacao de pareceres por evidencia.",
        quiet=args.quiet,
        analyses=args.analyses,
        evidencias_root=args.evidencias_root or "",
        judge_provider=args.judge_provider,
        judge_model=args.judge_model,
        out_dir=args.out_dir,
        only_achados=args.only_achados,
        catalog=args.catalog or "",
        prompts_dir=args.prompts_dir or "",
    )
    registros_origem = carregar_registros_processamento(args.analyses)
    grupos = agrupar_opinioes_por_evidencia(registros_origem)
    if args.only_achados:
        if args.catalog or args.prompts_dir:
            achados_set = questoes_achado_de_prompts_dir(args.prompts_dir, args.catalog)
        else:
            achados_set = questoes_achado_de_registros(registros_origem)
        if not achados_set:
            parser.error(
                "--only-achados ativo, mas nenhum gera_achado encontrado no catalogo YAML "
                "(--catalog), nos marcadores dos prompts (--prompts-dir) ou nos registros analyses."
            )
        total_grupos_antes = len(grupos)
        grupos = [g for g in grupos if g.chave.questao in achados_set]
        log_event(
            "consolidation_filtered_achados",
            "Grupos filtrados para questoes que ensejam achado.",
            quiet=args.quiet,
            only_achados=True,
            catalog=args.catalog or "",
            prompts_dir=args.prompts_dir or "",
            questoes_achado=sorted(achados_set),
            total_grupos_antes=total_grupos_antes,
            total_grupos_depois=len(grupos),
        )
    if args.list_only:
        for grupo in grupos:
            print(
                __import__("json").dumps(
                    {
                        **grupo.chave.__dict__,
                        "opinioes": len(grupo.opinioes),
                        "modelos": [
                            {
                                "provider": opiniao.get("provider", ""),
                                "model": opiniao.get("model", ""),
                            }
                            for opiniao in grupo.opinioes
                        ],
                    },
                    ensure_ascii=False,
                )
            )
        return 0

    opinioes_auditoria = carregar_opinioes_auditoria(args.auditor_opinions)
    out_dir = Path(args.out_dir)
    checkpoint = out_dir / "consolidated.jsonl"
    registros_checkpoint = carregar_registros_analise(checkpoint)
    prompt_hash = hashlib.sha256(PROMPT_JUIZ_PADRAO.encode("utf-8")).hexdigest()
    rate_limiter = RequestsPerMinuteLimiter(args.rpm)
    total_processados = 0
    total_pulados = 0
    total_erros = 0
    total_concluidos = 0

    for index, grupo in enumerate(grupos, start=1):
        chave = grupo.chave
        consolidation_started_at = dt.datetime.now(dt.timezone.utc)

        # Filtrar opinioes validas e identificar erros
        opinioes_validas: list[dict[str, Any]] = []
        opinioes_erro: list[dict[str, Any]] = []
        for opiniao in grupo.opinioes:
            result_op = opiniao.get("result") if isinstance(opiniao.get("result"), dict) else {}
            if opiniao.get("status") != "completed" or result_op.get("status") != "completed":
                opinioes_erro.append(opiniao)
            else:
                conclusoes = result_op.get("conclusoes")
                if not isinstance(conclusoes, list):
                    opinioes_erro.append(opiniao)
                else:
                    opinioes_validas.append(opiniao)

        if opinioes_erro and opinioes_validas:
            erros_desc = []
            for op in opinioes_erro:
                res_op = op.get("result") if isinstance(op.get("result"), dict) else {}
                msg = op.get("error") or res_op.get("error") or "erro desconhecido"
                erros_desc.append(f"{op.get('provider')}/{op.get('model')}: {msg}")
            log_event(
                "consolidation_partial_errors",
                "Algumas avaliacoes de modelos falharam. Procedendo apenas com as validas.",
                level="warning",
                quiet=args.quiet,
                erros="; ".join(erros_desc),
                auditado=chave.auditado,
                questao=chave.questao,
                coluna_evidencia=chave.coluna_evidencia,
                evidencia=chave.evidencia,
            )

        itens = itens_afirmados_do_grupo(opinioes_validas)
        opiniao_auditoria = opiniao_auditoria_para_grupo(opinioes_auditoria, grupo)
        caminho_evidencia = (
            localizar_evidencia(
                args.evidencias_root,
                chave,
                referencias_arquivos=referencias_arquivos_do_grupo(opinioes_validas),
            )
            if args.evidencias_root
            else None
        )
        evidence_hash = hash_arquivo(caminho_evidencia) if caminho_evidencia else ""

        from .checkpoint import calcular_identidade_parecer
        identity = calcular_identidade_parecer(
            auditado=chave.auditado,
            questao=chave.questao,
            coluna_evidencia=chave.coluna_evidencia,
            evidencia=chave.evidencia,
            opinioes=opinioes_validas,
            judge_provider=args.judge_provider,
            judge_model=args.judge_model,
            prompt_hash=prompt_hash,
            prompt_version=args.prompt_version,
            evidence_hash=evidence_hash,
            opiniao_auditoria=opiniao_auditoria,
        )
        base_log = {
            "index": index,
            "total": len(grupos),
            "identity": identity,
            "auditado": chave.auditado,
            "questao": chave.questao,
            "coluna_evidencia": chave.coluna_evidencia,
            "evidencia": chave.evidencia,
            "opinioes": len(opinioes_validas),
        }
        # Dedup por chave logica
        chave_logica = (chave.auditado, chave.coluna_evidencia, chave.evidencia, args.judge_provider, args.judge_model)
        indices_logicos = indices_chaves_logicas(registros_checkpoint)
        identity_existente = indices_logicos.get(chave_logica)
        if identity_existente and registros_checkpoint[identity_existente].get("status") == "completed":
            total_pulados += 1
            log_event(
                "consolidation_skipped",
                "Parecer consolidado ignorado por checkpoint (chave logica).",
                quiet=args.quiet,
                **base_log,
            )
            continue

        pacote_evidencia: dict[str, Any] = {"documentos": [], "inventario": [], "erro": "evidencia nao informada para o juiz"}
        arquivos_upload: list[str] = []
        documentos_contexto: list[dict[str, Any]] = []
        inventario_contexto: list[str] = []
        documentos_contexto_vistos: set[str] = set()
        inventario_contexto_visto: set[str] = set()
        for opiniao in opinioes_validas:
            pacote_contexto = opiniao.get("pacote_contexto_consolidacao")
            if not isinstance(pacote_contexto, dict):
                continue
            documentos = pacote_contexto.get("documentos")
            if isinstance(documentos, list):
                for doc in documentos:
                    if not isinstance(doc, dict):
                        continue
                    chave_doc = json.dumps(doc, ensure_ascii=False, sort_keys=True, default=str)
                    if chave_doc in documentos_contexto_vistos:
                        continue
                    documentos_contexto_vistos.add(chave_doc)
                    documentos_contexto.append(doc)
            inventario = pacote_contexto.get("inventario")
            if isinstance(inventario, list):
                for item in inventario:
                    if item in (None, ""):
                        continue
                    item_str = str(item)
                    if item_str in inventario_contexto_visto:
                        continue
                    inventario_contexto_visto.add(item_str)
                    inventario_contexto.append(item_str)

        with tempfile.TemporaryDirectory() as upload_tmp:
            if caminho_evidencia:
                pacote, arquivos_upload, erro_preparo = preparar_evidencia_para_provider(
                    caminho_evidencia,
                    upload_tmp,
                    pdf2md=args.pdf2md,
                    docx2html=args.docx2html,
                    dpi=args.pdf2md_dpi,
                )
                log_event(
                    "evidence_normalized",
                    "Evidencia normalizada para envio ao juiz.",
                    quiet=args.quiet,
                    level="warning" if pacote.erro else "info",
                    tipo=pacote.tipo,
                    documentos=len(pacote.documentos),
                    inventario=len(pacote.inventario),
                    error=pacote.erro,
                    **base_log,
                )
                if erro_preparo:
                    log_event(
                        "upload_prepare_error",
                        "Erro ao preparar evidencia para upload ao juiz.",
                        quiet=args.quiet,
                        level="error",
                        error=erro_preparo,
                        **base_log,
                    )
                pacote_evidencia = {
                    "documentos": documentos_contexto + pacote.documentos,
                    "inventario": inventario_contexto + pacote.inventario,
                    "erro": pacote.erro,
                    "arquivos_upload": arquivos_upload,
                }
            elif documentos_contexto and not chave.evidencia:
                pacote_evidencia = {
                    "documentos": documentos_contexto,
                    "inventario": inventario_contexto,
                    "erro": "",
                    "arquivos_upload": [],
                }
            elif args.evidencias_root:
                pacote_evidencia["erro"] = "evidencia nao localizada na raiz informada"

            payload_pacote = {
                **pacote_evidencia,
                "avaliacoes_preliminares": avaliacoes_preliminares_para_juiz(opinioes_validas),
                "opiniao_auditoria": opiniao_auditoria,
                "papel_do_resultado": "parecer consolidado revisavel pela equipe de auditoria",
            }

            # Determinar erro bloqueante antes da chamada
            erro_ativo: str | None = None
            if not opinioes_validas:
                erros_desc = []
                for op in opinioes_erro:
                    res_op = op.get("result") if isinstance(op.get("result"), dict) else {}
                    msg = op.get("error") or res_op.get("error") or "erro desconhecido"
                    erros_desc.append(f"{op.get('provider')}/{op.get('model')}: {msg}")
                erro_ativo = "nenhuma avaliacao valida disponivel para o juiz. erros: " + "; ".join(erros_desc)
                log_event(
                    "consolidation_no_valid_opinions",
                    f"Erro de consolidacao: {erro_ativo}",
                    level="error",
                    quiet=args.quiet,
                    **base_log,
                )
            elif args.evidencias_root:
                pacote_obj = PacoteEvidencia(
                    caminho=caminho_evidencia or Path("."),
                    tipo=caminho_evidencia.suffix.lstrip(".") if caminho_evidencia else "",
                    documentos=pacote_evidencia.get("documentos", []),
                    inventario=pacote_evidencia.get("inventario", []),
                    erro=pacote_evidencia.get("erro", ""),
                )
                erro_atual = erro_tecnico_bloqueante_pacote(pacote_obj, arquivos_upload)
                if erro_atual and erro_atual != "evidencia nao informada para o juiz":
                    erro_ativo = erro_atual

            if erro_ativo:
                result = {"status": "error", "error": erro_ativo}
            elif args.judge_provider == "fake":
                result = executar_juiz_fake(chave, opinioes_validas, itens)
            else:
                api_key = _api_key_para(args.judge_provider)
                if args.judge_provider in REMOTE_PROVIDERS and (api_key or args.judge_provider == "openai"):
                    wait_seconds = rate_limiter.wait_seconds()
                    if wait_seconds > 0:
                        log_event(
                            "consolidation_rate_limit_wait",
                            "Aguardando limite de requests por minuto antes da chamada ao juiz.",
                            quiet=args.quiet,
                            wait_seconds=round(wait_seconds, 3),
                            rpm=args.rpm,
                            **base_log,
                        )
                    rate_limiter.wait_and_mark(wait_seconds)

                def on_judge_event(event: str, fields: dict[str, Any]) -> None:
                    log_event(
                        event,
                        "Evento do juiz durante a chamada.",
                        quiet=args.quiet,
                        level="warning",
                        provider=args.judge_provider,
                        model=args.judge_model,
                        **base_log,
                        **fields,
                    )

                tokens_info = estimar_tokens_payload(
                    prompt=PROMPT_JUIZ_PADRAO,
                    auditado=chave.auditado,
                    questao_base=chave.questao,
                    coluna_evidencia=chave.coluna_evidencia,
                    itens_afirmados=itens,
                    pacote=payload_pacote,
                    provider=args.judge_provider,
                )
                limite_tokens = limite_tokens_provider(args.judge_provider, args.judge_model)
                if limite_tokens and args.judge_provider != "gemini" and tokens_info["tokens_total"] > limite_tokens:
                    result = {
                        "status": "error",
                        "error": (
                            f"payload excede limite de tokens do juiz: "
                            f"{tokens_info['tokens_total']:,} > {limite_tokens:,}"
                        ),
                    }
                    log_event(
                        "payload_tokens_exceeded",
                        "Payload bloqueado por exceder limite de tokens do juiz.",
                        quiet=args.quiet,
                        level="warning",
                        tokens_total=tokens_info["tokens_total"],
                        limite=limite_tokens,
                        provider=args.judge_provider,
                        model=args.judge_model,
                        **base_log,
                    )
                else:
                    result = executar_provider(
                        provider=args.judge_provider,
                        model=args.judge_model,
                        api_key=api_key,
                        prompt=PROMPT_JUIZ_PADRAO,
                        auditado=chave.auditado,
                        questao_base=chave.questao,
                        coluna_evidencia=chave.coluna_evidencia,
                        itens_afirmados=itens,
                        pacote=payload_pacote,
                        reasoning_effort=args.reasoning_effort,
                        on_event=on_judge_event,
                    )

            # Rotação: todas as chaves exauridas
            if isinstance(result, dict) and result.get("all_keys_exhausted"):
                wait_secs = float(result.get("retry_after_seconds", 60))
                log_event(
                    "all_keys_exhausted",
                    f"Todas as chaves {args.judge_provider} exauridas. Registrando erro e passando para o proximo grupo.",
                    quiet=args.quiet,
                    level="warning",
                    provider=args.judge_provider,
                    model=args.judge_model,
                    retry_after_seconds=round(wait_secs, 1),
                    **base_log,
                )
                result = {
                    "status": "error",
                    "error": f"todas as chaves {args.judge_provider} exauridas (retry_after {wait_secs:.0f}s)",
                }

        status = result.get("status", "error") if isinstance(result, dict) else "error"
        finished_at = dt.datetime.now(dt.timezone.utc)
        registro: dict[str, Any] = {
            "identity": identity,
            "status": status,
            "auditado": chave.auditado,
            "questao": chave.questao,
            "coluna_evidencia": chave.coluna_evidencia,
            "evidencia": chave.evidencia,
            "judge_provider": args.judge_provider,
            "judge_model": args.judge_model,
            "opinion_count": len(opinioes_validas),
            "opinion_sources": [
                {
                    "identity": opiniao.get("identity", ""),
                    "provider": opiniao.get("provider", ""),
                    "model": opiniao.get("model", ""),
                    "source": opiniao.get("_source", ""),
                }
                for opiniao in opinioes_validas
            ],
            "opiniao_auditoria": opiniao_auditoria,
            "evidence_path": str(caminho_evidencia) if caminho_evidencia else "",
            "evidence_hash": evidence_hash,
            "gera_achado": any(op.get("gera_achado") for op in grupo.opinioes),
            "result": result,
            "error": result.get("error", "") if isinstance(result, dict) else "resultado invalido",
            "started_at": consolidation_started_at.isoformat(),
            "finished_at": finished_at.isoformat(),
            "duration_seconds": round((finished_at - consolidation_started_at).total_seconds(), 3),
            "reasoning_effort": args.reasoning_effort,
        }
        if args.store_prompts:
            registro["prompt_payload"] = conteudo_provider_textual(
                prompt=PROMPT_JUIZ_PADRAO,
                auditado=chave.auditado,
                questao_base=chave.questao,
                coluna_evidencia=chave.coluna_evidencia,
                itens_afirmados=itens,
                pacote={k: v for k, v in payload_pacote.items() if k != "arquivos_upload"},
            )
        gravar_registro_analise(checkpoint, registro)
        registros_checkpoint[identity] = registro
        total_processados += 1
        if status == "completed":
            total_concluidos += 1
        else:
            total_erros += 1
        log_event(
            "consolidation_recorded",
            "Parecer consolidado gravado.",
            quiet=args.quiet,
            level="error" if status == "error" else "info",
            status=status,
            error=registro["error"],
            **base_log,
        )

    relatorio = out_dir / "pareceres_consolidados.xlsx"
    linhas = gerar_relatorio_pareceres(checkpoint, relatorio)
    checkpoint_limpo = out_dir / "consolidated_clean.jsonl"
    registros_limpos = gerar_checkpoint_limpo_consolidado(checkpoint, checkpoint_limpo)
    log_event(
        "clean_checkpoint_generated",
        "Checkpoint limpo (somente completed) gerado.",
        quiet=args.quiet,
        checkpoint_limpo=str(checkpoint_limpo),
        registros=registros_limpos,
    )
    log_event(
        "consolidation_finished",
        "Consolidacao de pareceres finalizada.",
        quiet=args.quiet,
        grupos=len(grupos),
        processados=total_processados,
        pulados=total_pulados,
        concluidos=total_concluidos,
        erros=total_erros,
        checkpoint=str(checkpoint),
        checkpoint_limpo=str(checkpoint_limpo),
        relatorio=str(relatorio),
        linhas=linhas,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
