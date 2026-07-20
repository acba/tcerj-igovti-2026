from __future__ import annotations

import io
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

from scripts.avaliacao_evidencias.providers import (
    estimar_tokens_payload,
    limite_tokens_provider,
)
from scripts.avaliacao_evidencias.providers.base import ProviderContext
from scripts.avaliacao_evidencias.providers.http_utils import formatar_erro_http
from scripts.avaliacao_evidencias.providers.openai import OpenAIProvider


class OpenAIPdfInputsTests(unittest.TestCase):
    def _contexto(self, pdf: Path, *, pdf_detail: str = "auto") -> ProviderContext:
        return ProviderContext(
            provider="openai",
            model="gpt-5.6-luna",
            api_key="",
            prompt="Analise a evidencia.",
            auditado="ORG",
            questao_base="Q1",
            coluna_evidencia="Q1Evi",
            itens_afirmados=[],
            pacote={
                "documentos": [
                    {"nome": pdf.name, "tipo": "pdf", "texto": "texto extraido duplicado" * 500}
                ],
                "inventario": [pdf.name],
                "erro": "",
                "arquivos_upload": [str(pdf)],
            },
            pdf_detail=pdf_detail,
        )

    def test_pdf_e_enviado_com_detail_auto_por_padrao(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pdf = Path(tmp) / "evidencia.pdf"
            pdf.write_bytes(b"%PDF-1.7\nconteudo")
            content = OpenAIProvider("gpt-5.6-luna")._build_content(self._contexto(pdf))

        arquivo = next(item for item in content if item["type"] == "input_file")
        self.assertEqual(arquivo["detail"], "auto")
        self.assertTrue(arquivo["file_data"].startswith("data:application/pdf;base64,"))
        self.assertNotIn(arquivo["file_data"], next(item["text"] for item in content if item["type"] == "input_text"))

    def test_pdf_detail_configuravel(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pdf = Path(tmp) / "evidencia.pdf"
            pdf.write_bytes(b"%PDF-1.7\nconteudo")
            content = OpenAIProvider("gpt-5.6-luna")._build_content(
                self._contexto(pdf, pdf_detail="low")
            )

        arquivo = next(item for item in content if item["type"] == "input_file")
        self.assertEqual(arquivo["detail"], "low")

    def test_estimativa_openai_nao_tokeniza_base64_nem_texto_pdf_duplicado(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pdf = Path(tmp) / "evidencia.pdf"
            pdf.write_bytes(b"x" * 1_000_000)
            contexto = self._contexto(pdf)
            estimativa = estimar_tokens_payload(
                prompt=contexto.prompt,
                auditado=contexto.auditado,
                questao_base=contexto.questao_base,
                coluna_evidencia=contexto.coluna_evidencia,
                itens_afirmados=contexto.itens_afirmados,
                pacote=contexto.pacote,
                provider="openai",
            )

        self.assertEqual(estimativa["n_pdfs"], 1)
        self.assertEqual(estimativa["tokens_pdfs"], 0)
        self.assertLess(estimativa["tokens_total"], 10_000)

    def test_http_413_repete_chamada_com_texto_extraido_sem_pdf_inline(self) -> None:
        eventos: list[tuple[str, dict]] = []
        with tempfile.TemporaryDirectory() as tmp:
            pdf = Path(tmp) / "evidencia.pdf"
            pdf.write_bytes(b"%PDF-1.7\nconteudo")
            contexto = self._contexto(pdf)
            contexto.on_event = lambda nome, dados: eventos.append((nome, dados))
            provider = OpenAIProvider("gpt-5.6-luna")
            content = provider._build_content(contexto)
            erro_413 = urllib.error.HTTPError(
                "http://127.0.0.1:8787/v1/responses",
                413,
                "Payload Too Large",
                None,
                io.BytesIO(b'{"error":{"message":"Request body is too large"}}'),
            )
            with patch(
                "scripts.avaliacao_evidencias.providers.openai._request_openai_responses_stream",
                side_effect=[erro_413, {"output_text": "{}", "response": None, "events": []}],
            ) as request:
                result = provider._call(contexto, content)

        self.assertEqual(result, "{}")
        self.assertEqual(request.call_count, 2)
        fallback_content = request.call_args_list[1].kwargs["body"]["input"][0]["content"]
        self.assertTrue(all(item["type"] == "input_text" for item in fallback_content))
        self.assertIn("texto extraido duplicado", fallback_content[0]["text"])
        self.assertNotIn("file_data", fallback_content[0])
        self.assertEqual(eventos[0][0], "openai_pdf_text_fallback")
        self.assertEqual(eventos[0][1]["reason"], "http_413_payload_too_large")

    def test_http_502_context_window_repete_com_texto_sem_retry_transiente(self) -> None:
        eventos: list[tuple[str, dict]] = []
        with tempfile.TemporaryDirectory() as tmp:
            pdf = Path(tmp) / "evidencia.pdf"
            pdf.write_bytes(b"%PDF-1.7\nconteudo")
            contexto = self._contexto(pdf)
            contexto.on_event = lambda nome, dados: eventos.append((nome, dados))
            provider = OpenAIProvider("gpt-5.6-luna")
            content = provider._build_content(contexto)
            erro_502 = urllib.error.HTTPError(
                "http://127.0.0.1:10531/v1/responses",
                502,
                "Bad Gateway",
                None,
                io.BytesIO(
                    b'{"error":{"message":"Your input exceeds the context window of this model."}}'
                ),
            )
            with patch(
                "scripts.avaliacao_evidencias.providers.openai._request_openai_responses_stream",
                side_effect=[erro_502, {"output_text": "{}", "response": None, "events": []}],
            ) as request:
                result = provider._call(contexto, content)

        self.assertEqual(result, "{}")
        self.assertEqual(request.call_count, 2)
        fallback_content = request.call_args_list[1].kwargs["body"]["input"][0]["content"]
        self.assertTrue(all(item["type"] == "input_text" for item in fallback_content))
        self.assertIn("texto extraido duplicado", fallback_content[0]["text"])
        self.assertEqual(eventos, [
            (
                "openai_pdf_text_fallback",
                {
                    "provider": "openai",
                    "model": "gpt-5.6-luna",
                    "reason": "context_window_exceeded",
                },
            )
        ])

    def test_limite_gpt_5_6_corresponde_a_janela_documentada(self) -> None:
        self.assertEqual(limite_tokens_provider("openai", "gpt-5.6-luna"), 1_048_576)

    def test_formatacao_http_preserva_corpo_apos_primeira_leitura(self) -> None:
        erro = urllib.error.HTTPError(
            "http://127.0.0.1:10531/v1/responses",
            502,
            "Bad Gateway",
            None,
            io.BytesIO(b'{"error":{"message":"diagnostico upstream"}}'),
        )

        primeira = formatar_erro_http(erro)
        segunda = formatar_erro_http(erro)

        self.assertEqual(segunda, primeira)
        self.assertIn("diagnostico upstream", segunda)


if __name__ == "__main__":
    unittest.main()
