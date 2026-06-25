"""Pacote avaliacao_evidencias.

Reexporta a API publica principal para consumidores externos e mantem
compatibilidade com a surface de imports do pacote original.
"""
from __future__ import annotations

__all__ = [
    "AnaliseCandidata",
    "ItemAfirmado",
    "PacoteEvidencia",
    "inventariar_analises",
    "normalizar_evidencia",
    "arquivos_compativeis_upload",
    "verificar_integridade_pdf",
    "resolver_evidencia",
    "resolver_prompt",
    "carregar_achados_set",
    "executar_provider",
]


def __getattr__(name: str):
    # Imports lentos/tardios para evitar ciclos e custos desnecessarios.
    if name == "AnaliseCandidata" or name == "inventariar_analises" or name == "resolver_evidencia":
        from .inventory import AnaliseCandidata, inventariar_analises, resolver_evidencia
        return {
            "AnaliseCandidata": AnaliseCandidata,
            "inventariar_analises": inventariar_analises,
            "resolver_evidencia": resolver_evidencia,
        }[name]
    if name == "ItemAfirmado":
        from .questionnaire import ItemAfirmado
        return ItemAfirmado
    if name == "PacoteEvidencia" or name == "normalizar_evidencia" or name == "arquivos_compativeis_upload" or name == "verificar_integridade_pdf":
        from .evidence_processing import (
            PacoteEvidencia,
            arquivos_compativeis_upload,
            normalizar_evidencia,
            verificar_integridade_pdf,
        )
        return {
            "PacoteEvidencia": PacoteEvidencia,
            "normalizar_evidencia": normalizar_evidencia,
            "arquivos_compativeis_upload": arquivos_compativeis_upload,
            "verificar_integridade_pdf": verificar_integridade_pdf,
        }[name]
    if name == "resolver_prompt" or name == "carregar_achados_set":
        from .prompts import carregar_achados_set, resolver_prompt
        return {"resolver_prompt": resolver_prompt, "carregar_achados_set": carregar_achados_set}[name]
    if name == "executar_provider":
        from .providers import executar_provider
        return executar_provider
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")