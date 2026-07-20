#!/usr/bin/env python3
"""Orquestra avaliação e consolidação das seções 1 e 2 dos comentários do gestor."""
from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.comentarios_gestor_pipeline import (
    DEFAULT_AJUSTES,
    DEFAULT_CATALOG,
    DEFAULT_CATALOG_COMENTARIOS,
    DEFAULT_LSS,
    DEFAULT_MAPA,
    DEFAULT_PAINEL_EVIDENCIAS,
    DEFAULT_PROMPTS,
    DEFAULT_QUESTIONARIO,
    DEFAULT_RESPOSTAS_BASE,
    DEFAULT_RESPOSTAS_ORIGINAIS,
    DEFAULT_RESULTADO,
    DEFAULT_REVISOES_RESPOSTAS,
    _identidade_logica_analise,
    avaliar_casos,
    carregar_revisoes_respostas,
    consolidar_casos,
    gravar_deterministicos,
    gravar_ajustes_combinados_xlsx,
    gravar_avaliacoes_modelos_xlsx,
    gerar_painel_evidencias_pos_comentarios,
    mapear_ajustes_secao1,
    mapear_ajustes_secao2,
    materializar_checkpoint_limpo_modelo,
    preparar_casos_comentarios,
)
from scripts.comentarios_gestor_integridade import validar_integridade_comentarios

TMP_ROOT = Path("/tmp/tcerj-igovti-2026") if sys.platform != "win32" else Path("C:/tmp/tcerj-igovti-2026")
DEFAULT_OUT = TMP_ROOT / "02-Execucao/05-Comentarios_Gestor/99-Avaliacao_Comentarios_Gestor"
DEFAULT_RESPOSTAS = TMP_ROOT / "02-Execucao/05-Comentarios_Gestor/respostas-comentarios-gestor.xlsx"
DEFAULT_EVIDENCIAS = TMP_ROOT / "02-Execucao/05-Comentarios_Gestor/evidencias_extraidas"
DEFAULT_MODELS_CONFIG = ROOT / "scripts/avaliacao_evidencias/configs/comentarios_gestor_models_v1.json"


def carregar_configuracao_modelos(path: Path) -> dict[str, Any]:
    """Carrega e valida a configuração externa de avaliadores e juiz."""
    if not path.is_file():
        raise ValueError(f"configuração de modelos não encontrada: {path}")
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON inválido em {path}: linha {exc.lineno}, coluna {exc.colno}: {exc.msg}") from exc
    if not isinstance(config, dict):
        raise ValueError("a configuração de modelos deve ser um objeto JSON")
    evaluators = config.get("evaluators")
    judge = config.get("judge")
    if not isinstance(evaluators, list) or not evaluators:
        raise ValueError("a configuração deve conter uma lista não vazia 'evaluators'")
    if not isinstance(judge, dict):
        raise ValueError("a configuração deve conter o objeto 'judge'")

    required_evaluator = {"name", "provider", "model", "rpm", "reasoning", "pdf2md", "docx2html"}
    names: set[str] = set()
    pairs: set[tuple[str, str]] = set()
    for index, evaluator in enumerate(evaluators, start=1):
        if not isinstance(evaluator, dict):
            raise ValueError(f"evaluators[{index}] deve ser um objeto")
        missing = required_evaluator.difference(evaluator)
        if missing:
            raise ValueError(f"evaluators[{index}] sem campos: {', '.join(sorted(missing))}")
        name = str(evaluator["name"]).strip()
        provider = str(evaluator["provider"]).strip()
        model = str(evaluator["model"]).strip()
        enabled = evaluator.get("enabled", True)
        model_key = str(evaluator.get("model_key", model)).strip()
        if not name or not provider or not model:
            raise ValueError(f"evaluators[{index}] possui name/provider/model vazio")
        if not isinstance(enabled, bool):
            raise ValueError(f"evaluators[{index}].enabled deve ser booleano")
        if not model_key:
            raise ValueError(f"evaluators[{index}].model_key não pode ser vazio")
        if name in names:
            raise ValueError(f"nome de avaliador duplicado: {name}")
        if (provider, model) in pairs:
            raise ValueError(f"par provider/model duplicado: {provider}/{model}")
        if not isinstance(evaluator["rpm"], int) or evaluator["rpm"] < 0:
            raise ValueError(f"evaluators[{index}].rpm deve ser inteiro não negativo")
        if not isinstance(evaluator["reasoning"], str):
            raise ValueError(f"evaluators[{index}].reasoning deve ser string")
        if not isinstance(evaluator["pdf2md"], bool) or not isinstance(evaluator["docx2html"], bool):
            raise ValueError(f"evaluators[{index}].pdf2md e docx2html devem ser booleanos")
        pdf_detail = str(evaluator.get("pdf_detail", "auto")).strip().lower()
        if pdf_detail not in {"auto", "low", "high"}:
            raise ValueError(f"evaluators[{index}].pdf_detail deve ser auto, low ou high")
        names.add(name)
        pairs.add((provider, model))
        evaluator["enabled"] = enabled
        evaluator["model_key"] = model_key
        evaluator["pdf_detail"] = pdf_detail

    active = [evaluator for evaluator in evaluators if evaluator["enabled"]]
    if not active:
        raise ValueError("a configuração deve conter ao menos um avaliador habilitado")
    active_by_model: dict[str, list[str]] = {}
    for evaluator in active:
        active_by_model.setdefault(evaluator["model_key"], []).append(evaluator["name"])
    duplicated_active = {key: routes for key, routes in active_by_model.items() if len(routes) > 1}
    if duplicated_active:
        details = "; ".join(f"{key}: {', '.join(routes)}" for key, routes in sorted(duplicated_active.items()))
        raise ValueError(f"apenas uma rota pode estar habilitada por model_key: {details}")

    required_judge = {"provider", "model", "min_valid_opinions", "rpm", "reasoning", "pdf2md", "docx2html"}
    missing_judge = required_judge.difference(judge)
    if missing_judge:
        raise ValueError(f"judge sem campos: {', '.join(sorted(missing_judge))}")
    quorum = judge["min_valid_opinions"]
    if not isinstance(quorum, int) or not 1 <= quorum <= len(active_by_model):
        raise ValueError(f"judge.min_valid_opinions deve estar entre 1 e {len(active_by_model)}")
    if not isinstance(judge["rpm"], int) or judge["rpm"] < 0:
        raise ValueError("judge.rpm deve ser inteiro não negativo")
    if not str(judge["provider"]).strip() or not str(judge["model"]).strip():
        raise ValueError("judge.provider e judge.model não podem ser vazios")
    if not isinstance(judge["reasoning"], str):
        raise ValueError("judge.reasoning deve ser string")
    if not isinstance(judge["pdf2md"], bool) or not isinstance(judge["docx2html"], bool):
        raise ValueError("judge.pdf2md e judge.docx2html devem ser booleanos")
    judge_pdf_detail = str(judge.get("pdf_detail", "auto")).strip().lower()
    if judge_pdf_detail not in {"auto", "low", "high"}:
        raise ValueError("judge.pdf_detail deve ser auto, low ou high")
    judge["pdf_detail"] = judge_pdf_detail
    max_workers = config.get("max_parallel_evaluators", len(evaluators))
    if not isinstance(max_workers, int) or max_workers < 1:
        raise ValueError("max_parallel_evaluators deve ser inteiro positivo")
    config["max_parallel_evaluators"] = max_workers
    return config


def models(config: dict[str, Any], fake: bool) -> list[dict[str, Any]]:
    configured = [cfg for cfg in config["evaluators"] if cfg["enabled"]]
    if not fake:
        return configured
    return [
        {
            **cfg,
            "provider": "fake",
            "model": cfg["name"],
            "model_key": f"fake-{cfg['model_key']}",
            "rpm": 0,
        }
        for cfg in configured
    ]


def section_name(secao: str) -> str:
    return "secao-1" if secao == "1" else "secao-2"


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


def prepare(args: argparse.Namespace, secao: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    auditados = {x.strip().upper() for x in (args.auditados or "").split(",") if x.strip()} or None
    casos, deterministicos, excluidas, resumo = preparar_casos_comentarios(
        respostas=args.respostas_comentarios,
        evidencias_root=args.evidencias_comentarios_root,
        secao=secao,
        lss=args.lss,
        resultado_auditoria=args.resultado_auditoria,
        mapa=args.mapa,
        ajustes=args.ajustes_pos_avaliacao_evidencias,
        questionario=args.questionario,
        prompts_dir=args.prompts_dir,
        catalog=args.catalog,
        catalog_comentarios=args.catalog_comentarios,
        auditados=auditados,
        saneados_secao1=getattr(args, "saneados_secao1_runtime", {}) if secao == "2" else None,
    )
    preflight = args.out_dir / "preflight"
    _write_json(preflight / f"resumo-{section_name(secao)}.json", resumo)
    _write_json(
        preflight / "submissoes-excluidas.json",
        [
            {
                "id": r.get("id"), "token": r.get("token"), "auditado": r.get("firstname"),
                "submitdate": r.get("submitdate"), "motivo_exclusao": r.get("motivo_exclusao"),
            }
            for r in excluidas
        ],
    )
    print(json.dumps({"event": "comments_preflight_completed", **resumo}, ensure_ascii=False), flush=True)
    return casos, deterministicos, resumo


def evaluate_section(args: argparse.Namespace, secao: str) -> dict[str, Any]:
    casos, deterministicos, preflight = prepare(args, secao)
    casos_execucao = casos
    filtro_reparo = getattr(args, "repair_case_ids", {}).get(secao)
    if filtro_reparo is not None:
        casos_execucao = [caso for caso in casos if caso["case_id"] in filtro_reparo]
    individual_dir = args.out_dir / "individuais" / section_name(secao)
    manifesto = {
        "secao": secao,
        "casos_ia": [
            {"case_id": c["case_id"], "prompt_hash": c["prompt_hash"], "prompt_version": c["prompt_version"]}
            for c in casos
        ],
        "case_ids_ia": [c["case_id"] for c in casos],
        "case_ids_deterministicos": [r["case_id"] for r in deterministicos],
        "identidades_esperadas_por_modelo": {},
    }
    if secao == "1":
        gravar_deterministicos(deterministicos, individual_dir)
    configs = models(args.models_runtime_config, args.fake)
    for cfg in configs:
        identidades: list[str] = []
        for caso in casos:
            try:
                identidades.append(
                    _identidade_logica_analise(
                        case_id_value=caso["case_id"],
                        model_key=cfg["model_key"],
                        prompt_hash=caso["prompt_hash"],
                        reasoning=cfg["reasoning"],
                        pdf2md=cfg["pdf2md"],
                        docx2html=cfg["docx2html"],
                        pdf_detail=cfg["pdf_detail"],
                        contexto=caso.get("contexto", {}),
                        evidence_paths=caso["evidence_paths"],
                    )
                )
            except (OSError, ValueError):
                continue
        manifesto["identidades_esperadas_por_modelo"][cfg["model_key"]] = identidades
    if filtro_reparo is None:
        _write_json(individual_dir / "manifesto-casos.json", manifesto)
    if args.preflight_only:
        return {"secao": secao, "preflight": preflight, "modelos": []}
    resultados: list[dict[str, Any]] = []
    max_workers = min(args.models_runtime_config["max_parallel_evaluators"], len(configs))
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                avaliar_casos,
                casos_execucao,
                provider=cfg["provider"], model=cfg["model"], model_key=cfg["model_key"],
                out_dir=individual_dir, routes=args.models_runtime_config["evaluators"],
                reasoning=cfg["reasoning"], rpm=cfg["rpm"], pdf2md=cfg["pdf2md"],
                docx2html=cfg["docx2html"], pdf_detail=cfg["pdf_detail"], quiet=args.quiet,
            ): cfg
            for cfg in configs
        }
        for future in as_completed(futures):
            cfg = futures[future]
            try:
                resultado = future.result()
            except Exception as exc:
                resultado = {
                    "provider": cfg["provider"],
                    "model": cfg["model"],
                    "erros": 0,
                    "falha_global": True,
                    "casos_nao_processados": len(casos_execucao),
                    "error": str(exc),
                }
            resultados.append(resultado)
            print(json.dumps({"event": "comments_model_finished", "secao": secao, **resultado}, ensure_ascii=False), flush=True)
    checkpoints = [
        Path(resultado["clean"])
        for resultado in resultados
        if resultado.get("clean") and Path(resultado["clean"]).is_file()
    ]
    xlsx = individual_dir / "avaliacoes_modelos.xlsx"
    gravar_avaliacoes_modelos_xlsx(
        xlsx,
        checkpoints,
        expected_models=[cfg["model_key"] for cfg in configs],
        expected_case_ids={caso["case_id"] for caso in casos_execucao},
        itens_excluidos=preflight.get("itens_excluidos_secao1") or [],
    )
    return {"secao": secao, "preflight": preflight, "modelos": resultados, "xlsx": str(xlsx)}


def _analysis_files(args: argparse.Namespace, secao: str, *, ignore_manifest: bool = False) -> list[Path]:
    directory = args.out_dir / "individuais" / section_name(secao)
    configs = models(args.models_runtime_config, args.fake)
    manifesto_path = directory / "manifesto-casos.json"
    manifesto = json.loads(manifesto_path.read_text(encoding="utf-8")) if manifesto_path.is_file() else {}
    expected_by_model = {} if ignore_manifest else (manifesto.get("identidades_esperadas_por_modelo") or {})
    files = []
    for cfg in configs:
        files.append(
            materializar_checkpoint_limpo_modelo(
                directory,
                model_key=cfg["model_key"],
                routes=args.models_runtime_config["evaluators"],
                expected_identities=set(expected_by_model[cfg["model_key"]]) if cfg["model_key"] in expected_by_model else None,
            )
        )
    existentes = [path for path in files if path.is_file()]
    quorum = args.models_runtime_config["judge"]["min_valid_opinions"]
    if len(existentes) < quorum:
        raise ValueError(
            f"quórum impossível: encontrados {len(existentes)} de {len(configs)} checkpoints; "
            f"mínimo configurado={quorum}; diretório={directory}"
        )
    return existentes


def consolidate_section(
    args: argparse.Namespace,
    secao: str,
    *,
    selected_case_ids: set[str] | None = None,
    expected_case_ids: set[str] | None = None,
) -> dict[str, Any]:
    configs = models(args.models_runtime_config, args.fake)
    judge = args.models_runtime_config["judge"]
    judge_provider = "fake" if args.fake else judge["provider"]
    judge_model = judge["model"]
    manifesto_path = args.out_dir / "individuais" / section_name(secao) / "manifesto-casos.json"
    manifesto = json.loads(manifesto_path.read_text(encoding="utf-8")) if manifesto_path.is_file() else {}
    result = consolidar_casos(
        analyses_files=_analysis_files(args, secao, ignore_manifest=selected_case_ids is not None),
        out_dir=args.out_dir / "consolidado" / section_name(secao),
        secao=secao,
        expected_models=[c["model_key"] for c in configs],
        judge_provider=judge_provider,
        judge_model=judge_model,
        min_opinions=judge["min_valid_opinions"],
        reasoning=judge["reasoning"],
        rpm=judge["rpm"],
        pdf2md=judge["pdf2md"],
        docx2html=judge["docx2html"],
        pdf_detail=judge["pdf_detail"],
        catalog_comentarios=args.catalog_comentarios,
        deterministic_path=(args.out_dir / "individuais/secao-1/deterministicos.jsonl") if secao == "1" else None,
        expected_case_ids=expected_case_ids or set(manifesto.get("case_ids_ia") or []),
        selected_case_ids=selected_case_ids,
        quiet=args.quiet,
    )
    print(json.dumps({"event": "comments_consolidation_finished", **result}, ensure_ascii=False), flush=True)
    return result


def _carregar_saneados_secao1(
    args: argparse.Namespace,
) -> tuple[dict[tuple[str, str], dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    consolidated = args.out_dir / "consolidado/secao-1/consolidated_clean.jsonl"
    if not consolidated.is_file():
        return {}, [], []
    ajustes, pendencias = mapear_ajustes_secao1(
        consolidado=consolidated,
        resultado_auditoria=args.resultado_auditoria,
        mapa=args.mapa,
        lss=args.lss,
        ajustes_pos_avaliacao_evidencias=args.ajustes_pos_avaliacao_evidencias,
        respostas_base=args.respostas_questionario_base,
        respostas_originais=args.respostas_questionario_originais,
    )
    revisoes, pendencias_revisoes = carregar_revisoes_respostas(
        path=args.revisoes_respostas,
        consolidado_secao1=consolidated,
        respostas_base=args.respostas_questionario_base,
    )
    ajustes.extend(revisoes)
    pendencias.extend(pendencias_revisoes)
    saneados = {
        (str(item.get("Auditado", "")).strip().upper(), str(item.get("Código do item avaliado", "")).strip()): item
        for item in ajustes
        if item.get("Auditado") and item.get("Código do item avaliado") and item.get("Resposta ajustada")
    }
    return saneados, ajustes, pendencias


def generate_adjustments(args: argparse.Namespace) -> dict[str, Any]:
    saneados, ajustes_secao1, pendencias = _carregar_saneados_secao1(args)
    consolidated_secao2 = args.out_dir / "consolidado/secao-2/consolidated_clean.jsonl"
    ajustes_secao2 = (
        mapear_ajustes_secao2(
            consolidado=consolidated_secao2,
            ajustes_pos_avaliacao_evidencias=args.ajustes_pos_avaliacao_evidencias,
            questionario=args.questionario,
            saneados_secao1=set(saneados),
        )
        if consolidated_secao2.is_file()
        else []
    )
    output = args.out_dir / "ajustes_respostas_questionario_pos_comentarios_gestor.xlsx"
    finais, pendencias_finais = gravar_ajustes_combinados_xlsx(
        output,
        ajustes_secao1=ajustes_secao1,
        ajustes_secao2=ajustes_secao2,
        pendencias=pendencias,
    )
    painel_output = args.out_dir / "fontes-auditoria-pos-comentarios/painel-avaliacao-evidencias.xlsx"
    painel_alteracoes = gerar_painel_evidencias_pos_comentarios(
        painel_origem=args.painel_avaliacao_evidencias,
        output=painel_output,
        ajustes=finais,
    )
    return {
        "path": str(output),
        "ajustes": len(finais),
        "pendencias": len(pendencias_finais),
        "ajustes_secao1": len(ajustes_secao1),
        "ajustes_secao2": len(ajustes_secao2),
        "painel_evidencias": str(painel_output),
        "painel_celulas_saneadas": painel_alteracoes,
    }


def validate_integrity(args: argparse.Namespace) -> dict[str, Any]:
    casos_por_secao: dict[str, list[dict[str, Any]]] = {}
    deterministicos_por_secao: dict[str, list[dict[str, Any]]] = {}
    for secao in ("1", "2"):
        casos, deterministicos, _ = prepare(args, secao)
        casos_por_secao[secao] = casos
        deterministicos_por_secao[secao] = deterministicos
    configs = models(args.models_runtime_config, args.fake)
    return validar_integridade_comentarios(
        out_dir=args.out_dir,
        casos_por_secao=casos_por_secao,
        deterministicos_por_secao=deterministicos_por_secao,
        modelos_esperados=[item["model_key"] for item in configs],
        quorum=args.models_runtime_config["judge"]["min_valid_opinions"],
    )


def repair_integrity(args: argparse.Namespace) -> dict[str, Any]:
    validacao = validate_integrity(args)
    manifest_path = Path(validacao["manifesto_reparo"])
    manifesto = json.loads(manifest_path.read_text(encoding="utf-8"))
    filtros = {
        secao: {str(item["case_id"]) for item in manifesto.get("secoes", {}).get(secao, [])}
        for secao in ("1", "2")
    }
    args.repair_case_ids = filtros
    resultados: list[dict[str, Any]] = []
    for secao in ("1", "2"):
        if not filtros[secao]:
            continue
        casos, _, _ = prepare(args, secao)
        esperados = {str(caso["case_id"]) for caso in casos}
        resultados.append(evaluate_section(args, secao))
        resultados.append(
            consolidate_section(
                args,
                secao,
                selected_case_ids=filtros[secao],
                expected_case_ids=esperados,
            )
        )
    args.repair_case_ids = {}
    validacao_final = validate_integrity(args)
    return {
        "validacao_inicial": validacao,
        "casos_reprocessados": {secao: len(ids) for secao, ids in filtros.items()},
        "resultados": resultados,
        "validacao_final": validacao_final,
    }


def run(args: argparse.Namespace) -> int:
    resumo: dict[str, Any] = {"action": args.action, "fake": args.fake, "resultados": []}
    try:
        args.models_runtime_config = carregar_configuracao_modelos(args.models_config)
        resumo["models_config"] = str(args.models_config)
        resumo["models_config_version"] = args.models_runtime_config.get("version", "")
        _write_json(args.out_dir / "configuracao-modelos-efetiva.json", args.models_runtime_config)
        if args.action == "avaliar":
            secoes = [args.secao] if args.secao in {"1", "2"} else ["1", "2"]
            for secao in secoes:
                if secao == "2":
                    args.saneados_secao1_runtime, _, _ = _carregar_saneados_secao1(args)
                    if not args.saneados_secao1_runtime:
                        print(
                            json.dumps(
                                {
                                    "event": "comments_section1_saneados_unavailable",
                                    "message": "Seção 2 executada sem exclusões da seção 1.",
                                },
                                ensure_ascii=False,
                            ),
                            flush=True,
                        )
                resumo["resultados"].append(evaluate_section(args, secao))
        elif args.action == "consolidar":
            secoes = [args.secao] if args.secao in {"1", "2"} else ["1", "2"]
            resumo["resultados"].extend(consolidate_section(args, s) for s in secoes)
        elif args.action == "completo":
            resumo["resultados"].append(evaluate_section(args, "1"))
            if not args.preflight_only:
                resumo["resultados"].append(consolidate_section(args, "1"))
                args.saneados_secao1_runtime, _, _ = _carregar_saneados_secao1(args)
            resumo["resultados"].append(evaluate_section(args, "2"))
            if not args.preflight_only:
                resumo["resultados"].append(consolidate_section(args, "2"))
                resumo["integridade"] = validate_integrity(args)
                if resumo["integridade"]["status"] != "conforme":
                    raise ValueError(
                        "validação de integridade reprovada; execute 'reparar-integridade' antes de gerar ajustes"
                    )
                resumo["ajustes"] = generate_adjustments(args)
        elif args.action == "gerar-ajustes":
            resumo["integridade"] = validate_integrity(args)
            if resumo["integridade"]["status"] != "conforme":
                raise ValueError(
                    "validação de integridade reprovada; execute 'reparar-integridade' antes de gerar ajustes"
                )
            resumo["ajustes"] = generate_adjustments(args)
        elif args.action == "validar-integridade":
            resumo["integridade"] = validate_integrity(args)
        elif args.action == "reparar-integridade":
            resumo["reparo"] = repair_integrity(args)
        else:
            raise ValueError(f"ação desconhecida: {args.action}")
    except Exception as exc:
        resumo["status"] = "failed"
        resumo["error"] = str(exc)
        _write_json(args.out_dir / "resumo-execucao.json", resumo)
        print(json.dumps({"event": "comments_pipeline_failed", "error": str(exc)}, ensure_ascii=False), flush=True)
        return 1
    def has_partial(value: Any) -> bool:
        if isinstance(value, dict):
            if value.get("erros", 0) or value.get("pendentes_quorum", 0) or value.get("error"):
                return True
            return any(has_partial(v) for v in value.values())
        if isinstance(value, list):
            return any(has_partial(v) for v in value)
        return False

    parcial = has_partial(resumo["resultados"])
    resumo["status"] = "partial" if parcial else "success"
    _write_json(args.out_dir / "resumo-execucao.json", resumo)
    print(json.dumps({"event": "comments_pipeline_finished", "status": resumo["status"], "out_dir": str(args.out_dir)}, ensure_ascii=False), flush=True)
    return 2 if parcial else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "action",
        choices=["avaliar", "consolidar", "gerar-ajustes", "validar-integridade", "reparar-integridade", "completo"],
    )
    parser.add_argument("--secao", choices=["1", "2", "ambas"], default="ambas")
    parser.add_argument("--respostas-comentarios", type=Path, default=DEFAULT_RESPOSTAS)
    parser.add_argument("--evidencias-comentarios-root", type=Path, default=DEFAULT_EVIDENCIAS)
    parser.add_argument("--lss", type=Path, default=DEFAULT_LSS)
    parser.add_argument("--resultado-auditoria", type=Path, default=DEFAULT_RESULTADO)
    parser.add_argument("--mapa", type=Path, default=DEFAULT_MAPA)
    parser.add_argument("--ajustes-pos-avaliacao-evidencias", type=Path, default=DEFAULT_AJUSTES)
    parser.add_argument("--questionario", type=Path, default=DEFAULT_QUESTIONARIO)
    parser.add_argument("--respostas-questionario-base", type=Path, default=DEFAULT_RESPOSTAS_BASE)
    parser.add_argument("--respostas-questionario-originais", type=Path, default=DEFAULT_RESPOSTAS_ORIGINAIS)
    parser.add_argument("--painel-avaliacao-evidencias", type=Path, default=DEFAULT_PAINEL_EVIDENCIAS)
    parser.add_argument("--revisoes-respostas", type=Path, default=DEFAULT_REVISOES_RESPOSTAS)
    parser.add_argument("--prompts-dir", type=Path, default=DEFAULT_PROMPTS)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--catalog-comentarios", type=Path, default=DEFAULT_CATALOG_COMENTARIOS)
    parser.add_argument("--models-config", type=Path, default=DEFAULT_MODELS_CONFIG)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--auditados", default="", help="Siglas separadas por vírgula.")
    parser.add_argument("--fake", action="store_true", help="Substitui os avaliadores e o juiz configurados por providers fake.")
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    return parser


if __name__ == "__main__":
    raise SystemExit(run(build_parser().parse_args()))
