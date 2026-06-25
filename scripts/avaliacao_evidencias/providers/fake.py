"""Provider fake: nao faz chamada de rede; retorna conclusao placeholder.

Usado para validar inventario, resolucao de arquivos, prompts, checkpoint e
relatorio sem gastar cota de IA.
"""
from __future__ import annotations

from typing import Any

from .base import GenericProvider, ProviderContext
from .response import validar_resultado_ia, valor_item


class FakeProvider(GenericProvider):
    name = "fake"
    supports_images = False
    needs_api_key = False

    def _build_content(self, ctx: ProviderContext) -> Any:
        return None

    def _call(self, ctx: ProviderContext, content: Any) -> Any:
        documentos = ctx.pacote.get("documentos", []) if isinstance(ctx.pacote, dict) else []
        referencias = [
            documento.get("nome")
            for documento in documentos
            if isinstance(documento, dict) and documento.get("nome")
        ]
        conclusoes = []
        for item in ctx.itens_afirmados:
            conclusoes.append(
                {
                    "item_codigo": valor_item(item, "codigo"),
                    "item_texto": valor_item(item, "texto"),
                    "afirmacao_auditado": valor_item(item, "afirmacao"),
                    "estado": "nao_conforme",
                    "justificativa": "Provider fake nao emite conclusao substantiva.",
                    "lacunas": ["Analise real de IA nao executada."],
                    "arquivos_referenciados": referencias,
                    "trechos_ou_elementos": [],
                    "paginas_ou_localizacao": [],
                    "coluna_evidencia": ctx.coluna_evidencia,
                }
            )
        return validar_resultado_ia({"status": "completed", "conclusoes": conclusoes})