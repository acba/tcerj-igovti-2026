from __future__ import annotations

import json
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.avaliacao_evidencias.key_pool import (
    ExclusiveApiKeyPool,
    cooldown_429,
    normalizar_chaves,
)
from scripts.comentarios_gestor_pipeline import consolidar_casos
from scripts.run_comentarios_gestor import DEFAULT_MODELS_CONFIG, carregar_configuracao_modelos
from scripts.tests.test_comentarios_gestor_pipeline import opinion


class ExclusiveApiKeyPoolTest(unittest.TestCase):
    def test_normaliza_chaves_sem_repetir_a_mesma_credencial(self) -> None:
        self.assertEqual(
            normalizar_chaves(" chave-a, chave-b, chave-a, ,chave-b "),
            ["chave-a", "chave-b"],
        )

    def test_chave_em_uso_nao_e_entregue_a_outra_thread(self) -> None:
        pool = ExclusiveApiKeyPool("chave-a,chave-b")
        first = pool.acquire()
        second = pool.acquire()
        acquired: list[str] = []
        finished = threading.Event()

        def acquire_third() -> None:
            lease = pool.acquire()
            acquired.append(lease.key)
            lease.release()
            finished.set()

        thread = threading.Thread(target=acquire_third)
        thread.start()
        self.assertFalse(finished.wait(0.05))
        first.release()
        self.assertTrue(finished.wait(1.0))
        second.release()
        thread.join(timeout=1.0)
        self.assertEqual(acquired, ["chave-a"])

    def test_429_nao_entrega_chave_em_cooldown_quando_outra_fica_livre(self) -> None:
        pool = ExclusiveApiKeyPool("chave-a,chave-b")
        first = pool.acquire()
        second = pool.acquire()
        first.release(cooldown_seconds=0.3)
        acquired: list[str] = []

        def acquire_waiting() -> None:
            lease = pool.acquire()
            acquired.append(lease.key)
            lease.release()

        thread = threading.Thread(target=acquire_waiting)
        thread.start()
        time.sleep(0.05)
        self.assertEqual(acquired, [])
        second.release()
        thread.join(timeout=1.0)
        self.assertEqual(acquired, ["chave-b"])

    def test_reserva_maior_que_tpm_falha_sem_aguardar(self) -> None:
        pool = ExclusiveApiKeyPool("chave-a", tpm=100)
        with self.assertRaisesRegex(ValueError, "excede o TPM"):
            pool.acquire(tokens=101)

    def test_cooldown_429_aplica_fallback_e_limite(self) -> None:
        self.assertEqual(cooldown_429({}), 60.0)
        self.assertEqual(cooldown_429({"retry_after_seconds": 9999}), 180.0)


class CommentConsolidationParallelTest(unittest.TestCase):
    @staticmethod
    def _write_opinions(root: Path, total: int) -> list[Path]:
        records = []
        for index in range(total):
            record = opinion(f"case-{index}", "provider", "model-key")
            record["identity"] = f"opinion-{index}"
            records.append(record)
        path = root / "analyses.jsonl"
        path.write_text(
            "\n".join(json.dumps(record) for record in records) + "\n",
            encoding="utf-8",
        )
        return [path]

    @staticmethod
    def _completed_result() -> dict:
        return {
            "status": "completed",
            "conclusoes": [{"item_codigo": "q1001[A]", "estado": "nao_conforme"}],
        }

    def test_consolidacao_limita_concorrencia_ao_numero_de_chaves(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            analyses = self._write_opinions(root, 3)
            lock = threading.Lock()
            active_keys: set[str] = set()
            duplicate_use: list[str] = []
            max_active = 0

            def provider_call(**kwargs):
                nonlocal max_active
                key = kwargs["api_key"]
                with lock:
                    if key in active_keys:
                        duplicate_use.append(key)
                    active_keys.add(key)
                    max_active = max(max_active, len(active_keys))
                time.sleep(0.05)
                with lock:
                    active_keys.remove(key)
                return self._completed_result()

            with patch.dict("os.environ", {"GEMINI_API_KEY": "segredo-chave-a,segredo-chave-b"}), patch(
                "scripts.comentarios_gestor_pipeline.executar_provider",
                side_effect=provider_call,
            ), patch(
                "scripts.comentarios_gestor_pipeline.validar_resultado_no_escopo",
                return_value=[],
            ), patch(
                "scripts.comentarios_gestor_pipeline.validar_justificativa_publicavel",
                return_value=[],
            ):
                result = consolidar_casos(
                    analyses_files=analyses,
                    out_dir=root / "out",
                    secao="2",
                    expected_models=["model-key"],
                    judge_provider="gemini",
                    judge_model="judge",
                    min_opinions=1,
                    max_parallel=3,
                    quiet=True,
                )

        self.assertEqual(result["concluidos"], 3)
        self.assertEqual(result["effective_workers"], 2)
        self.assertEqual(result["gemini_keys"], 2)
        self.assertEqual(max_active, 2)
        self.assertEqual(duplicate_use, [])

    def test_429_troca_para_chave_livre_sem_gravar_erro(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            analyses = self._write_opinions(root, 1)
            called_keys: list[str] = []

            def provider_call(**kwargs):
                called_keys.append(kwargs["api_key"])
                if len(called_keys) == 1:
                    return {
                        "status": "error",
                        "error": "rate limit",
                        "http_status": 429,
                        "retry_after_seconds": 30,
                    }
                return self._completed_result()

            with patch.dict("os.environ", {"GEMINI_API_KEY": "segredo-chave-a,segredo-chave-b"}), patch(
                "scripts.comentarios_gestor_pipeline.executar_provider",
                side_effect=provider_call,
            ), patch(
                "scripts.comentarios_gestor_pipeline.validar_resultado_no_escopo",
                return_value=[],
            ), patch(
                "scripts.comentarios_gestor_pipeline.validar_justificativa_publicavel",
                return_value=[],
            ), patch(
                "scripts.comentarios_gestor_pipeline.log_event",
            ) as event_log:
                result = consolidar_casos(
                    analyses_files=analyses,
                    out_dir=root / "out",
                    secao="2",
                    expected_models=["model-key"],
                    judge_provider="gemini",
                    judge_model="judge",
                    min_opinions=1,
                    max_parallel=2,
                    quiet=False,
                    verbose=True,
                )
            checkpoint = [
                json.loads(line)
                for line in (root / "out/consolidated.jsonl").read_text(encoding="utf-8").splitlines()
            ]

        self.assertEqual(called_keys, ["segredo-chave-a", "segredo-chave-b"])
        self.assertEqual(result["concluidos"], 1)
        self.assertEqual(result["erros"], 0)
        self.assertEqual([record["status"] for record in checkpoint], ["completed"])
        event_names = [call.args[0] for call in event_log.call_args_list]
        self.assertIn("comment_judge_key_acquired", event_names)
        self.assertIn("comment_judge_key_cooldown", event_names)
        self.assertIn("comment_judge_key_released", event_names)

    def test_eventos_detalhados_de_chave_ficam_ocultos_por_padrao(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            analyses = self._write_opinions(root, 1)
            with patch.dict("os.environ", {"GEMINI_API_KEY": "segredo-chave-a"}), patch(
                "scripts.comentarios_gestor_pipeline.executar_provider",
                return_value=self._completed_result(),
            ), patch(
                "scripts.comentarios_gestor_pipeline.validar_resultado_no_escopo",
                return_value=[],
            ), patch(
                "scripts.comentarios_gestor_pipeline.validar_justificativa_publicavel",
                return_value=[],
            ), patch(
                "scripts.comentarios_gestor_pipeline.log_event",
            ) as event_log:
                consolidar_casos(
                    analyses_files=analyses,
                    out_dir=root / "out",
                    secao="2",
                    expected_models=["model-key"],
                    judge_provider="gemini",
                    judge_model="judge",
                    min_opinions=1,
                    max_parallel=1,
                    quiet=False,
                )

        event_names = [call.args[0] for call in event_log.call_args_list]
        self.assertIn("comment_consolidation_parallel_started", event_names)
        self.assertIn("comment_consolidation_recorded", event_names)
        self.assertFalse(any(name.startswith("comment_judge_key_") for name in event_names))

    def test_configuracao_carrega_limites_do_juiz(self) -> None:
        raw = json.loads(DEFAULT_MODELS_CONFIG.read_text(encoding="utf-8"))
        config = carregar_configuracao_modelos(DEFAULT_MODELS_CONFIG)
        self.assertEqual(config["judge"]["max_parallel"], raw["judge"]["max_parallel"])
        self.assertEqual(config["judge"]["tpm"], raw["judge"]["tpm"])

    def test_configuracao_antiga_recebe_defaults_sequenciais(self) -> None:
        config = json.loads(DEFAULT_MODELS_CONFIG.read_text(encoding="utf-8"))
        config["judge"].pop("max_parallel")
        config["judge"].pop("tpm")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "models.json"
            path.write_text(json.dumps(config), encoding="utf-8")
            loaded = carregar_configuracao_modelos(path)
        self.assertEqual(loaded["judge"]["max_parallel"], 1)
        self.assertEqual(loaded["judge"]["tpm"], 0)

    def test_configuracao_rejeita_limites_invalidos(self) -> None:
        config = json.loads(DEFAULT_MODELS_CONFIG.read_text(encoding="utf-8"))
        config["judge"]["max_parallel"] = 0
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "models.json"
            path.write_text(json.dumps(config), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "max_parallel"):
                carregar_configuracao_modelos(path)


if __name__ == "__main__":
    unittest.main()
