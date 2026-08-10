from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

from scripts.pipeline_auditoria import Manifest, PipelineRunner, Stage


class PipelineAuditoriaTest(unittest.TestCase):
    def test_preserva_produto_e_retoma_por_hash(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            entrada = root / "entrada.txt"
            saida = root / "saida.txt"
            entrada.write_text("fonte", encoding="utf-8")
            stage = Stage(
                "01-teste",
                "Etapa de teste",
                (sys.executable, "-c", f"from pathlib import Path; Path({str(saida)!r}).write_text('produto')"),
                inputs=(entrada,),
                outputs=(saida,),
            )
            runner = PipelineRunner(Manifest(root / "controle"))
            self.assertEqual(runner.run(stage), "completed")
            self.assertEqual(runner.run(stage), "skipped")
            entrada.write_text("fonte alterada", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "não serão sobrescritos"):
                runner.run(stage)

    def test_entrada_opcional_produz_awaiting_input(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            missing = root / "comentarios.xlsx"
            manifest = Manifest(root / "controle")
            result = PipelineRunner(manifest).run(
                Stage("comentarios", "Comentários", optional_inputs=(missing,))
            )
            self.assertEqual(result, "awaiting_input")
            self.assertEqual(manifest.data["status"], "awaiting_input")

    def test_codigo_tres_produz_awaiting_review(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            review = root / "revisao.xlsx"
            manifest = Manifest(root / "controle")
            stage = Stage(
                "comentarios",
                "Comentários",
                (sys.executable, "-c", "raise SystemExit(3)"),
                metadata={"review_artifact": str(review)},
            )
            result = PipelineRunner(manifest).run(stage)
            self.assertEqual(result, "awaiting_review")
            self.assertEqual(manifest.data["status"], "awaiting_review")
            self.assertEqual(manifest.data["stages"]["comentarios"]["review_artifact"], str(review))

    def test_adota_produto_legado_sem_executar_comando(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            output = root / "legado.xlsx"
            output.write_text("legado", encoding="utf-8")
            stage = Stage("legado", "Produto legado", (sys.executable, "-c", "raise SystemExit(9)"), outputs=(output,))
            manifest = Manifest(root / "controle")
            result = PipelineRunner(manifest, adopt_existing=True).run(stage)
            self.assertEqual(result, "adopted")
            self.assertTrue(manifest.data["stages"]["legado"]["adopted_existing"])

    def test_adocao_remove_residuos_de_falha_anterior(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            output = root / "produto.xlsx"
            output.write_text("produto validado", encoding="utf-8")
            stage = Stage("comentarios", "Comentários", outputs=(output,))
            manifest = Manifest(root / "controle")
            manifest.data["stages"] = {
                "comentarios": {
                    "status": "failed",
                    "returncode": 2,
                    "error": "execução parcial",
                    "missing_inputs": ["entrada.xlsx"],
                    "review_artifact": "revisao.xlsx",
                }
            }

            result = PipelineRunner(manifest, adopt_existing=True).run(stage)
            record = manifest.data["stages"]["comentarios"]

            self.assertEqual(result, "adopted")
            self.assertEqual(record["status"], "completed")
            self.assertNotIn("returncode", record)
            self.assertNotIn("error", record)
            self.assertNotIn("missing_inputs", record)
            self.assertNotIn("review_artifact", record)


if __name__ == "__main__":
    unittest.main()
