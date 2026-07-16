"""Tratamento de resposta dos modelos: extracao de JSON, reparo e validacao.

Independente de provider; opera sobre o texto bruto retornado pelo modelo.
"""
from __future__ import annotations

import dataclasses
import json
import re
from typing import Any, Mapping


ESTADOS_CONFORMIDADE = {"conforme", "nao_conforme", "erro"}
ESTADOS_TEMPORAIS = {"mantida", "afastada_na_data_base", "corrigida_posteriormente", "inconclusiva"}
ESTADOS_MOTIVO = {"mantido", "afastado", "inconclusivo"}
CAMPOS_MOTIVO_OBRIGATORIOS = {"id_motivo", "estado_motivo", "justificativa"}
ALIASES_CAMPOS_MOTIVO = {
    "id_motivo": ("motivo_id",),
    "estado_motivo": ("estado",),
    "justificativa": ("justificativa_motivo",),
}
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


def validar_resultado_ia(resultado: dict[str, Any], *, response_profile: str = "evidence") -> dict[str, Any]:
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
        if response_profile == "manager_comments_temporal":
            _validar_conclusao_temporal(conclusao, idx)
    resultado["status"] = status
    return resultado


def _validar_conclusao_temporal(conclusao: dict[str, Any], idx: int) -> None:
    campos = {
        "estado_temporal",
        "conclusoes_motivos",
        "providencias_informadas",
        "comentarios_encaminhamento",
        "consequencias_praticas",
        "alternativas_propostas",
    }
    faltantes = campos.difference(conclusao)
    if faltantes:
        raise ValueError(f"conclusao temporal {idx} sem campos: {', '.join(sorted(faltantes))}")
    if conclusao["estado_temporal"] not in ESTADOS_TEMPORAIS:
        raise ValueError(f"estado_temporal invalido: {conclusao['estado_temporal']}")
    if not isinstance(conclusao["conclusoes_motivos"], list):
        raise ValueError("conclusoes_motivos deve ser lista")
    avisos = []
    for motivo_idx, motivo in enumerate(conclusao["conclusoes_motivos"]):
        if not isinstance(motivo, dict):
            raise ValueError(f"conclusao temporal {idx}, motivo {motivo_idx} deve ser objeto")
        normalizacoes = _normalizar_aliases_motivo(motivo)
        faltantes_motivo = CAMPOS_MOTIVO_OBRIGATORIOS.difference(motivo)
        if faltantes_motivo:
            raise ValueError(
                f"conclusao temporal {idx}, motivo {motivo_idx} sem campos: "
                f"{', '.join(sorted(faltantes_motivo))}"
            )
        extras = set(motivo).difference(CAMPOS_MOTIVO_OBRIGATORIOS)
        if normalizacoes or extras:
            aviso: dict[str, Any] = {
                "conclusao": idx,
                "motivo": motivo_idx,
            }
            if normalizacoes:
                aviso["aliases_normalizados"] = normalizacoes
            if extras:
                aviso["campos_adicionais"] = sorted(extras)
            avisos.append(aviso)
        if motivo["estado_motivo"] not in ESTADOS_MOTIVO:
            raise ValueError(
                f"conclusao temporal {idx}, motivo {motivo_idx}: "
                f"estado_motivo invalido: {motivo['estado_motivo']}"
            )
    if avisos:
        avisos_existentes = conclusao.get("avisos_estrutura_motivos")
        if not isinstance(avisos_existentes, list):
            avisos_existentes = []
            conclusao["avisos_estrutura_motivos"] = avisos_existentes
        avisos_existentes.extend(avisos)
    for campo in ["providencias_informadas", "consequencias_praticas", "alternativas_propostas"]:
        if not isinstance(conclusao[campo], list):
            raise ValueError(f"campo temporal {campo} deve ser lista")
    if not isinstance(conclusao["comentarios_encaminhamento"], str):
        raise ValueError("comentarios_encaminhamento deve ser string")


def _normalizar_aliases_motivo(motivo: dict[str, Any]) -> dict[str, str]:
    """Copia aliases inequívocos sem apagar a resposta original do modelo."""
    normalizacoes: dict[str, str] = {}
    for canonico, aliases in ALIASES_CAMPOS_MOTIVO.items():
        if canonico in motivo:
            continue
        encontrados = [alias for alias in aliases if alias in motivo]
        if len(encontrados) == 1:
            alias = encontrados[0]
            motivo[canonico] = motivo[alias]
            normalizacoes[alias] = canonico
    return normalizacoes


def _conclusion_properties(response_profile: str) -> dict[str, Any]:
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
    if response_profile == "manager_comments_temporal":
        properties.update(
            {
                "estado_temporal": {"type": "string", "enum": sorted(ESTADOS_TEMPORAIS)},
                "conclusoes_motivos": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "id_motivo": {"type": "string"},
                            "estado_motivo": {"type": "string", "enum": sorted(ESTADOS_MOTIVO)},
                            "justificativa": {"type": "string"},
                        },
                        "required": ["id_motivo", "estado_motivo", "justificativa"],
                    },
                },
                "providencias_informadas": {"type": "array", "items": {"type": "string"}},
                "comentarios_encaminhamento": {"type": "string"},
                "consequencias_praticas": {"type": "array", "items": {"type": "string"}},
                "alternativas_propostas": {"type": "array", "items": {"type": "string"}},
            }
        )
    return properties


def json_schema_response_format(*, response_profile: str = "evidence") -> dict[str, Any]:
    """Schema JSON para uso em response_format (chat completions / openai responses)."""
    properties = _conclusion_properties(response_profile)
    required = set(CONCLUSAO_CAMPOS_OBRIGATORIOS)
    if response_profile == "manager_comments_temporal":
        required.update(
            {
                "estado_temporal",
                "conclusoes_motivos",
                "providencias_informadas",
                "comentarios_encaminhamento",
                "consequencias_praticas",
                "alternativas_propostas",
            }
        )
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
                            "required": sorted(required),
                        },
                    },
                    "error": {"type": "string"},
                },
                "required": ["status", "conclusoes", "error"],
            },
        },
    }


def json_schema_responses_format(*, response_profile: str = "evidence") -> dict[str, Any]:
    chat_format = json_schema_response_format(response_profile=response_profile)["json_schema"]
    return {
        "format": {
            "type": "json_schema",
            "name": chat_format["name"],
            "strict": chat_format["strict"],
            "schema": chat_format["schema"],
        }
    }
