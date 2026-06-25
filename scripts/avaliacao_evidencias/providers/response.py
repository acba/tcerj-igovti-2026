"""Tratamento de resposta dos modelos: extracao de JSON, reparo e validacao.

Independente de provider; opera sobre o texto bruto retornado pelo modelo.
"""
from __future__ import annotations

import dataclasses
import json
import re
from typing import Any, Mapping


ESTADOS_CONFORMIDADE = {"conforme", "nao_conforme", "erro"}
CONCLUSAO_CAMPOS_OBRIGATORIOS = {
    "item_codigo",
    "item_texto",
    "afirmacao_auditado",
    "estado",
    "justificativa",
    "lacunas",
    "arquivos_referenciados",
    "trechos_ou_elementos",
    "paginas_ou_localizacao",
}


def item_para_dict(item: Any) -> dict[str, Any]:
    if dataclasses.is_dataclass(item):
        return dataclasses.asdict(item)
    if isinstance(item, Mapping):
        return dict(item)
    if hasattr(item, "__dict__"):
        return dict(item.__dict__)
    raise TypeError(f"item afirmado nao serializavel: {type(item).__name__}")


def valor_item(item: Any, campo: str) -> Any:
    if isinstance(item, Mapping):
        return item.get(campo)
    return getattr(item, campo)


def _extrair_bloco_json(texto: str | None) -> str:
    if not isinstance(texto, str) or not texto.strip():
        return ""
    match = re.search(r"```(?:json)?\s*(.*?)```", texto, flags=re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return texto.strip()


def carregar_json_modelo(texto: str | None) -> dict[str, Any]:
    if not isinstance(texto, str) or not texto.strip():
        raise ValueError("resposta do modelo vazia ou nula")
    try:
        from json_repair import repair_json
    except ModuleNotFoundError as exc:
        raise ValueError("json-repair nao instalado para reparar respostas JSON") from exc

    bruto = _extrair_bloco_json(texto)
    reparado = repair_json(bruto)
    if not isinstance(reparado, str) or not reparado.strip():
        raise ValueError("resposta do modelo nao contem JSON reparavel")
    try:
        resultado = json.loads(reparado)
    except json.JSONDecodeError as exc:
        raise ValueError(f"resposta do modelo nao contem JSON reparavel: {exc.msg}") from exc
    if not isinstance(resultado, dict):
        raise ValueError("resposta do modelo precisa ser objeto JSON")
    return resultado


def validar_resultado_ia(resultado: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(resultado, dict):
        raise ValueError("resultado de IA deve ser objeto JSON")
    status = resultado.get("status", "completed")
    if status not in {"completed", "error"}:
        raise ValueError(f"status invalido: {status}")
    if status == "error":
        if not resultado.get("error"):
            raise ValueError("resultado error precisa de campo error")
        return resultado
    conclusoes = resultado.get("conclusoes")
    if not isinstance(conclusoes, list):
        raise ValueError("resultado completed precisa de lista conclusoes")
    for idx, conclusao in enumerate(conclusoes):
        if not isinstance(conclusao, dict):
            raise ValueError(f"conclusao {idx} deve ser objeto")
        faltantes = CONCLUSAO_CAMPOS_OBRIGATORIOS.difference(conclusao)
        if faltantes:
            raise ValueError(f"conclusao {idx} sem campos: {', '.join(sorted(faltantes))}")
        if conclusao["estado"] not in ESTADOS_CONFORMIDADE:
            raise ValueError(f"estado invalido: {conclusao['estado']}")
        for campo in ["lacunas", "arquivos_referenciados", "trechos_ou_elementos", "paginas_ou_localizacao"]:
            if not isinstance(conclusao[campo], list):
                raise ValueError(f"campo {campo} deve ser lista")
    resultado["status"] = status
    return resultado


def json_schema_response_format() -> dict[str, Any]:
    """Schema JSON para uso em response_format (chat completions / openai responses)."""
    properties = {
        "item_codigo": {"type": "string"},
        "item_texto": {"type": "string"},
        "afirmacao_auditado": {"type": "string"},
        "estado": {"type": "string", "enum": sorted(ESTADOS_CONFORMIDADE)},
        "justificativa": {"type": "string"},
        "lacunas": {"type": "array", "items": {"type": "string"}},
        "arquivos_referenciados": {"type": "array", "items": {"type": "string"}},
        "trechos_ou_elementos": {"type": "array", "items": {"type": "string"}},
        "paginas_ou_localizacao": {"type": "array", "items": {"type": "string"}},
    }
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "resultado_avaliacao_evidencia",
            "strict": True,
            "schema": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "status": {"type": "string", "enum": ["completed", "error"]},
                    "conclusoes": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "properties": properties,
                            "required": sorted(CONCLUSAO_CAMPOS_OBRIGATORIOS),
                        },
                    },
                    "error": {"type": "string"},
                },
                "required": ["status", "conclusoes", "error"],
            },
        },
    }


def json_schema_responses_format() -> dict[str, Any]:
    chat_format = json_schema_response_format()["json_schema"]
    return {
        "format": {
            "type": "json_schema",
            "name": chat_format["name"],
            "strict": chat_format["strict"],
            "schema": chat_format["schema"],
        }
    }