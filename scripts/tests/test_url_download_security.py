from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from scripts.avaliacao_evidencias.evidence_processing import baixar_recurso_url


class _Response:
    def __init__(
        self,
        *,
        headers: dict[str, str] | None = None,
        body: bytes = b"",
        redirect: bool = False,
    ) -> None:
        self.headers = headers or {}
        self.body = body
        self.is_redirect = redirect
        self.is_permanent_redirect = False
        self.closed = False

    def close(self) -> None:
        self.closed = True

    def raise_for_status(self) -> None:
        return None

    def iter_content(self, *, chunk_size: int):
        del chunk_size
        yield self.body

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        self.close()


class UrlDownloadSecurityTest(unittest.TestCase):
    def test_download_segue_redirecionamento_relativo_e_preserva_url_final(self) -> None:
        redirect = _Response(headers={"Location": "/documentos/ato.pdf"}, redirect=True)
        final = _Response(
            headers={"Content-Type": "application/pdf", "Content-Length": "4"},
            body=b"%PDF",
        )
        session = Mock()
        session.get.side_effect = [redirect, final]
        dns_publico = [(2, 1, 6, "", ("200.0.0.10", 443))]

        with tempfile.TemporaryDirectory() as tmp, patch(
            "requests.Session", return_value=session
        ), patch(
            "scripts.avaliacao_evidencias.evidence_processing.socket.getaddrinfo",
            return_value=dns_publico,
        ):
            caminho, erro, metadados = baixar_recurso_url(
                "https://www.rj.gov.br/inicio",
                Path(tmp),
            )

            self.assertEqual(erro, "")
            self.assertIsNotNone(caminho)
            self.assertEqual(caminho.read_bytes(), b"%PDF")

        self.assertEqual(session.get.call_count, 2)
        self.assertEqual(
            session.get.call_args_list[1].args[0],
            "https://www.rj.gov.br/documentos/ato.pdf",
        )
        self.assertEqual(metadados["url_final"], "https://www.rj.gov.br/documentos/ato.pdf")

    def test_download_bloqueia_hostname_que_resolve_para_ip_privado(self) -> None:
        session = Mock()
        dns_privado = [(2, 1, 6, "", ("10.0.0.10", 443))]

        with tempfile.TemporaryDirectory() as tmp, patch(
            "requests.Session", return_value=session
        ), patch(
            "scripts.avaliacao_evidencias.evidence_processing.socket.getaddrinfo",
            return_value=dns_privado,
        ):
            caminho, erro, metadados = baixar_recurso_url(
                "https://www.rj.gov.br/ato.pdf",
                Path(tmp),
            )

        self.assertIsNone(caminho)
        self.assertIn("endereço privado/reservado", erro)
        self.assertEqual(metadados, {})
        session.get.assert_not_called()

    def test_download_informa_falha_de_resolucao_dns(self) -> None:
        session = Mock()

        with tempfile.TemporaryDirectory() as tmp, patch(
            "requests.Session", return_value=session
        ), patch(
            "scripts.avaliacao_evidencias.evidence_processing.socket.getaddrinfo",
            side_effect=OSError("DNS indisponível"),
        ):
            caminho, erro, metadados = baixar_recurso_url(
                "https://www.rj.gov.br/ato.pdf",
                Path(tmp),
            )

        self.assertIsNone(caminho)
        self.assertIn("hostname não resolvido", erro)
        self.assertEqual(metadados, {})
        session.get.assert_not_called()


if __name__ == "__main__":
    unittest.main()
