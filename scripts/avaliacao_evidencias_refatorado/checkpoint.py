"""Identidade, gravacao, deduplicacao e checkpoint limpo.

Centraliza o calculo de identidade (hash deterministico de uma analise ou
parecer), a gravacao incremental no JSONL, o carregamento para dedup e a
geracao do checkpoint limpo (somente ``completed``).
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Any

from .utils import componente_nome_arquivo


def calcular_identidade_analise(
    *,
    auditado: str,
    coluna_evidencia: str,
    nome_original_evidencia: str,
    hash_conteudo: str,
    provider: str,
    model: str,
    prompt_hash: str = "",
    checklist_hash: str = "",
    prompt_version: str,
    reasoning_effort: str = "",
    evidence_processing_mode: str = "",
) -> str:
    artifact_hash = prompt_hash or checklist_hash
    payload = {
        "auditado": auditado,
        "coluna_evidencia": coluna_evidencia,
        "nome_original_evidencia": nome_original_evidencia,
        "hash_conteudo": hash_conteudo,
        "provider": provider,
        "model": model,
        "prompt_hash": artifact_hash,
        "prompt_version": prompt_version,
        "reasoning_effort": reasoning_effort,
        "evidence_processing_mode": evidence_processing_mode,
    }
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def calcular_identidade_parecer(
    *,
    auditado: str,
    questao: str,
    coluna_evidencia: str,
    evidencia: str,
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
            "identity": r.get("identity", ""),
            "provider": r.get("provider", ""),
            "model": r.get("model", ""),
            "result": r.get("result", {}),
        }
        for r in opinioes
    ]
    payload = {
        "auditado": auditado,
        "questao": questao,
        "coluna_evidencia": coluna_evidencia,
        "evidencia": evidencia,
        "opinioes_hash": _hash_json(opinioes_para_identidade),
        "opiniao_auditoria_hash": hashlib.sha256(opiniao_auditoria.encode("utf-8")).hexdigest(),
        "evidence_hash": evidence_hash,
        "judge_provider": judge_provider,
        "judge_model": judge_model,
        "prompt_hash": prompt_hash,
        "prompt_version": prompt_version,
    }
    return _hash_json(payload)


def _hash_json(payload: Any) -> str:
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def gravar_registro_analise(checkpoint: str | Path, registro: dict[str, Any]) -> None:
    path = Path(checkpoint)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(registro, ensure_ascii=False, sort_keys=True, default=str))
        file.write("\n")


def carregar_registros_analise(checkpoint: str | Path) -> dict[str, dict[str, Any]]:
    path = Path(checkpoint)
    if not path.is_file():
        return {}
    registros: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        registro = json.loads(line)
        identity = registro.get("identity")
        if isinstance(identity, str):
            registros[identity] = registro
    return registros


def deve_processar_identidade(
    registros: dict[str, dict[str, Any]],
    identity: str,
    *,
    skip_errors: bool = False,
) -> bool:
    registro = registros.get(identity)
    if not registro:
        return True
    status = registro.get("status")
    if status == "completed":
        return False
    if status == "error" and skip_errors:
        return False
    return True


def nome_checkpoint_padrao(provider: str, model: str) -> str:
    return f"analyses_{componente_nome_arquivo(provider)}_{componente_nome_arquivo(model)}.jsonl"


def resolver_checkpoint_saida(out_dir: str | Path, out_file: str | Path | None, provider: str, model: str) -> Path:
    caminho = Path(out_file or nome_checkpoint_padrao(provider, model))
    if caminho.is_absolute():
        return caminho
    return Path(out_dir) / caminho


def montar_registro_analise(
    *,
    identity: str,
    status: str,
    auditado: str,
    questao_base: str,
    coluna_evidencia: str,
    evidencia: str,
    provider: str,
    model: str,
    started_at: dt.datetime,
    reasoning_effort: str = "",
    evidence_processing_mode: str = "",
    gera_achado: bool = False,
    result: dict[str, Any] | None = None,
    error: str = "",
    prompt_payload: str | None = None,
    payload_tokens: dict[str, int] | None = None,
) -> dict[str, Any]:
    finished_at = dt.datetime.now(dt.timezone.utc)
    registro: dict[str, Any] = {
        "identity": identity,
        "status": status,
        "auditado": auditado,
        "questao": questao_base,
        "coluna_evidencia": coluna_evidencia,
        "evidencia": evidencia,
        "provider": provider,
        "model": model,
        "started_at": started_at.isoformat(),
        "finished_at": finished_at.isoformat(),
        "duration_seconds": round((finished_at - started_at).total_seconds(), 3),
        "reasoning_effort": reasoning_effort,
        "evidence_processing_mode": evidence_processing_mode,
        "gera_achado": gera_achado,
        "error": error,
    }
    if result is not None:
        registro["result"] = result
    if prompt_payload is not None:
        registro["prompt_payload"] = prompt_payload
    if payload_tokens is not None:
        registro["payload_tokens"] = payload_tokens
    return registro


def gerar_checkpoint_limpo(checkpoint: str | Path, destino: str | Path) -> int:
    """Copia para ``destino`` apenas os registros ``completed`` do checkpoint."""
    path = Path(checkpoint)
    if not path.is_file():
        return 0
    destino_path = Path(destino)
    destino_path.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    with path.open(encoding="utf-8") as f_in, destino_path.open("w", encoding="utf-8") as f_out:
        for linha in f_in:
            if not linha.strip():
                continue
            registro = json.loads(linha)
            if registro.get("status") == "completed":
                f_out.write(json.dumps(registro, ensure_ascii=False) + "\n")
                total += 1
    return total


def identidade_para_erro_inventario(analise: Any) -> str:
    """Identidade auxiliar para analises com erro de inventario.

    Usa os campos estruturais da AnaliseCandidata via __dict__.
    """
    return hashlib.sha256(
        json.dumps(analise.__dict__, ensure_ascii=False, sort_keys=True, default=str).encode("utf-8")
    ).hexdigest()