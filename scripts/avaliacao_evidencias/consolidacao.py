from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import tempfile
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import unquote

from openpyxl import Workbook

from .pipeline import (
    REMOTE_PROVIDERS,
    ItemAfirmado,
    RequestsPerMinuteLimiter,
    _resolver_evidencia_exportada_limesurvey,
    arquivos_compativeis_upload,
    carregar_registros_analise,
    deve_processar_identidade,
    gravar_registro_analise,
    hash_arquivo,
    log_event,
    normalizar_evidencia,
    validar_rpm,
)
from .providers_ai_service import executar_provider


PROMPT_JUIZ_PADRAO = """Voce e um juiz avaliador de evidencias de auditoria.

Sua tarefa e produzir um parecer consolidado de evidencia, revisavel pela equipe de auditoria, a partir de:
- a evidencia enviada pelo auditado, quando disponivel;
- as opinioes ja emitidas por diferentes provedores/modelos;
- a opiniao da equipe de auditoria, quando fornecida.

Regras:
- Nao trate o parecer consolidado como decisao final de auditoria.
- Nao use conhecimento externo para preencher lacunas da evidencia.
- Analise convergencias, divergencias, fragilidades e excesso de inferencia nas opinioes dos modelos.
- Se a opiniao da equipe de auditoria divergir dos modelos, explique criticamente o motivo da conclusao adotada.
- Fundamente cada conclusao com elementos da evidencia e/ou com a avaliacao critica das opinioes recebidas.
- Declare lacunas quando a evidencia ou as opinioes nao forem suficientes.
- Na justificativa de cada conclusao, declare explicitamente quais modelos (provedor/modelo) foram a base para a avaliacao.
- Retorne somente JSON no schema solicitado.
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


def _opiniao_modelo(registro: dict[str, Any]) -> dict[str, Any]:
    result = registro.get("result") if isinstance(registro.get("result"), dict) else {}
    return {
        "identity": registro.get("identity", ""),
        "provider": registro.get("provider", ""),
        "model": registro.get("model", ""),
        "finished_at": registro.get("finished_at", ""),
        "source": registro.get("_source", ""),
        "conclusoes": result.get("conclusoes", []),
    }


def opinioes_modelos_do_grupo(opinioes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [_opiniao_modelo(registro) for registro in opinioes]


def _hash_json(payload: Any) -> str:
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def calcular_identidade_parecer(
    *,
    chave: ChaveEvidencia,
    opinioes: list[dict[str, Any]],
    judge_provider: str,
    judge_model: str,
    prompt_hash: str,
    prompt_version: str,
    evidence_hash: str = "",
    opiniao_auditoria: str = "",
) -> str:
    opinioes_para_identidade = [
        {
            "identity": registro.get("identity", ""),
            "provider": registro.get("provider", ""),
            "model": registro.get("model", ""),
            "result": registro.get("result", {}),
        }
        for registro in opinioes
    ]
    payload = {
        "auditado": chave.auditado,
        "questao": chave.questao,
        "coluna_evidencia": chave.coluna_evidencia,
        "evidencia": chave.evidencia,
        "opinioes_hash": _hash_json(opinioes_para_identidade),
        "opiniao_auditoria_hash": hashlib.sha256(opiniao_auditoria.encode("utf-8")).hexdigest(),
        "evidence_hash": evidence_hash,
        "judge_provider": judge_provider,
        "judge_model": judge_model,
        "prompt_hash": prompt_hash,
        "prompt_version": prompt_version,
    }
    return _hash_json(payload)


def _normalizar_nome(valor: str) -> str:
    sem_acentos = unicodedata.normalize("NFKD", valor).encode("ascii", "ignore").decode("ascii")
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in sem_acentos).strip("-")


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
        if caminho.is_file():
            return caminho
    for referencia in referencias_arquivos:
        nome_referencia = Path(unquote(referencia)).name
        caminho = auditado_dir / nome_referencia
        if caminho.is_file():
            return caminho
    exportado = _resolver_evidencia_exportada_limesurvey(auditado_dir, unquote(chave.evidencia))
    if exportado:
        return exportado
    alvo = _normalizar_nome(unquote(chave.evidencia))
    for candidato in auditado_dir.iterdir():
        if candidato.is_file() and _normalizar_nome(candidato.name) == alvo:
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Consolida opinioes de modelos em um parecer por evidencia.")
    parser.add_argument("analyses", nargs="+", help="Arquivos analyses.jsonl gerados pelo processamento de evidencias.")
    parser.add_argument("--evidencias-root", default=None, help="Raiz de evidencias para reenviar a evidencia ao juiz.")
    parser.add_argument("--auditor-opinions", default=None, help="JSON/JSONL/CSV com opinioes opcionais da auditoria.")
    parser.add_argument("--judge-provider", default="fake")
    parser.add_argument("--judge-model", default="fake")
    parser.add_argument("--out-dir", default=".saida_analise")
    parser.add_argument("--prompt-version", default="juiz-v1")
    parser.add_argument("--rpm", type=validar_rpm, default=0)
    parser.add_argument("--skip-errors", action="store_true")
    parser.add_argument("--list-only", action="store_true")
    parser.add_argument("--quiet", action="store_true")
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
    )
    registros_origem = carregar_registros_processamento(args.analyses)
    grupos = agrupar_opinioes_por_evidencia(registros_origem)
    if args.list_only:
        for grupo in grupos:
            print(
                json.dumps(
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
        
        # Filtrar opinioes validas e identificar erros
        opinioes_validas = []
        opinioes_erro = []
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
        identity = calcular_identidade_parecer(
            chave=chave,
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
        if not deve_processar_identidade(registros_checkpoint, identity, skip_errors=args.skip_errors):
            total_pulados += 1
            log_event(
                "consolidation_skipped",
                "Parecer consolidado ignorado por checkpoint.",
                quiet=args.quiet,
                **base_log,
            )
            continue
        pacote_evidencia = {"documentos": [], "inventario": [], "erro": "evidencia nao informada para o juiz"}
        arquivos_upload: list[str] = []
        with tempfile.TemporaryDirectory() as upload_tmp:
            if caminho_evidencia:
                pacote = normalizar_evidencia(caminho_evidencia)
                arquivos_upload = arquivos_compativeis_upload(caminho_evidencia, upload_tmp)
                pacote_evidencia = {
                    "documentos": pacote.documentos,
                    "inventario": pacote.inventario,
                    "erro": pacote.erro,
                    "arquivos_upload": arquivos_upload,
                }
            elif args.evidencias_root:
                pacote_evidencia["erro"] = "evidencia nao localizada na raiz informada"

            payload_pacote = {
                **pacote_evidencia,
                "opinioes_modelos": opinioes_modelos_do_grupo(opinioes_validas),
                "opiniao_auditoria": opiniao_auditoria,
                "papel_do_resultado": "parecer consolidado revisavel pela equipe de auditoria",
            }
            erro_ativo = None
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
                erro_atual = pacote_evidencia.get("erro")
                if erro_atual and erro_atual != "evidencia nao informada para o juiz":
                    erro_ativo = erro_atual

            if erro_ativo:
                result = {
                    "status": "error",
                    "error": erro_ativo,
                }
            elif args.judge_provider == "fake":
                result = executar_juiz_fake(chave, opinioes_validas, itens)
            else:
                env_key = {"gemini": "GEMINI_API_KEY", "openrouter": "OPENROUTER_API_KEY", "opencodego": "OPENCODEGO_API_KEY"}.get(args.judge_provider, "")
                api_key = os.environ.get(env_key, "") if env_key else ""
                if args.judge_provider in REMOTE_PROVIDERS and api_key:
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
                )


        status = result.get("status", "error") if isinstance(result, dict) else "error"
        registro = {
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
            "result": result,
            "error": result.get("error", "") if isinstance(result, dict) else "resultado invalido",
            "finished_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        }
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
        relatorio=str(relatorio),
        linhas=linhas,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
