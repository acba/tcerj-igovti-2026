from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.comentarios_gestor_integridade import validar_integridade_comentarios


def _registro(*, status: str, finished_at: str, item_codigo: str = "q1001[A]") -> dict:
    registro = {
        "case_id": "case-1",
        "secao": "2",
        "auditado": "ORG",
        "codigo": "q1001",
        "provider": "provider",
        "model": "model",
        "model_key": "model",
        "status": status,
        "finished_at": finished_at,
    }
    if status == "completed":
        registro["result"] = {
            "status": "completed",
            "conclusoes": [{"item_codigo": item_codigo}],
        }
    else:
        registro["error"] = "falha transitoria"
    return registro


class ComentariosGestorIntegridadeTest(unittest.TestCase):
    def _validar(self, individual_novo: dict, consolidado_novo: dict) -> dict:
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp)
            individual = out_dir / "individuais/secao-2/analyses_model_model.jsonl"
            individual.parent.mkdir(parents=True)
            individual.write_text(
                "\n".join(
                    json.dumps(item)
                    for item in [
                        _registro(status="completed", finished_at="2026-07-20T10:00:00+00:00"),
                        individual_novo,
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            consolidado = out_dir / "consolidado/secao-2/consolidated.jsonl"
            consolidado.parent.mkdir(parents=True)
            consolidado.write_text(
                "\n".join(
                    json.dumps(item)
                    for item in [
                        _registro(status="completed", finished_at="2026-07-20T10:00:00+00:00"),
                        consolidado_novo,
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            return validar_integridade_comentarios(
                out_dir=out_dir,
                casos_por_secao={
                    "1": [],
                    "2": [{
                        "case_id": "case-1",
                        "secao": "2",
                        "auditado": "ORG",
                        "codigo": "q1001",
                        "itens": [{"codigo": "q1001[A]"}],
                    }],
                },
                deterministicos_por_secao={"1": [], "2": []},
                modelos_esperados=["model"],
                quorum=1,
            )

    def test_preserva_registros_validos_diante_de_erros_posteriores(self) -> None:
        resultado = self._validar(
            _registro(status="error", finished_at="2026-07-20T11:00:00+00:00"),
            _registro(status="error", finished_at="2026-07-20T11:00:00+00:00"),
        )

        self.assertEqual(resultado["status"], "conforme")
        self.assertEqual(resultado["casos_reprocessamento_secao_2"], 0)
        self.assertEqual(resultado["avisos_avaliacoes_individuais"], 0)

    def test_preserva_registros_validos_diante_de_respostas_externas_posteriores(self) -> None:
        resultado = self._validar(
            _registro(status="completed", finished_at="2026-07-20T11:00:00+00:00", item_codigo="q9999[A]"),
            _registro(status="completed", finished_at="2026-07-20T11:00:00+00:00", item_codigo="q9999[A]"),
        )

        self.assertEqual(resultado["status"], "conforme")
        self.assertEqual(resultado["casos_reprocessamento_secao_2"], 0)
        self.assertEqual(resultado["avisos_avaliacoes_individuais"], 0)


if __name__ == "__main__":
    unittest.main()