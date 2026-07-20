from __future__ import annotations

import io
import unittest
import urllib.error
from unittest.mock import patch

from scripts.avaliacao_evidencias.providers.base import ProviderContext
from scripts.avaliacao_evidencias.providers.opencodego import OpencodeGoProvider


class OpencodeGoHttpErrorsTests(unittest.TestCase):
    def test_http_400_registra_corpo_completo(self) -> None:
        corpo = '{"error":{"message":"' + ("detalhe-" * 600) + 'fim"}}'
        erro = urllib.error.HTTPError(
            "https://opencode.ai/zen/go/v1/chat/completions",
            400,
            "Bad Request",
            None,
            io.BytesIO(corpo.encode("utf-8")),
        )
        contexto = ProviderContext(
            provider="opencodego",
            model="qwen3.7-plus",
            api_key="teste",
            prompt="Analise.",
            auditado="ORG",
            questao_base="Q1",
            coluna_evidencia="Q1Evi",
            itens_afirmados=[],
            pacote={"documentos": [], "inventario": [], "erro": "", "arquivos_upload": []},
        )

        with patch("urllib.request.urlopen", side_effect=erro):
            resultado = OpencodeGoProvider("qwen3.7-plus")._call(contexto, "prompt")

        self.assertEqual(resultado["status"], "error")
        self.assertEqual(resultado["http_status"], 400)
        self.assertIn(corpo, resultado["error"])
        self.assertTrue(resultado["error"].endswith('fim"}}'))
        self.assertGreater(len(resultado["error"]), 2_000)


if __name__ == "__main__":
    unittest.main()
