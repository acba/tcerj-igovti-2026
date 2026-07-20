import unittest
from io import StringIO
from unittest.mock import patch

from scripts.avaliacao_evidencias.providers.base import GenericProvider, ProviderContext
from scripts.avaliacao_evidencias.providers.gemini import (
    GeminiKeyRotationManager,
    resultado_adiar_item_todas_chaves_429,
)
from scripts.avaliacao_evidencias.providers.http_utils import (
    MAX_TRANSIENT_RETRY_DELAY_SECONDS,
    executar_com_retry_transiente,
)


class ProviderRetryPolicyTests(unittest.TestCase):
    def test_retry_after_enorme_e_limitado_a_tres_minutos(self):
        esperas = []
        chamadas = 0
        saida = StringIO()

        class TooManyRequests(Exception):
            code = 429
            headers = {"Retry-After": "505712"}

        def operacao():
            nonlocal chamadas
            chamadas += 1
            if chamadas == 1:
                raise TooManyRequests("Too Many Requests")
            return "ok"

        with patch("scripts.avaliacao_evidencias.providers.http_utils.sys.stderr", new=saida):
            resultado = executar_com_retry_transiente(
                operacao,
                max_retries=1,
                sleeper=esperas.append,
                provider="opencodego",
                model="qwen3.7-plus",
            )

        self.assertEqual(resultado, "ok")
        self.assertEqual(esperas, [MAX_TRANSIENT_RETRY_DELAY_SECONDS])
        self.assertEqual(MAX_TRANSIENT_RETRY_DELAY_SECONDS, 180.0)
        self.assertIn("Provedor [opencodego/qwen3.7-plus]", saida.getvalue())

    def test_gemini_rotaciona_todas_as_chaves_antes_de_adiar_item(self):
        manager = GeminiKeyRotationManager(["chave-1", "chave-2", "chave-3"])

        for chave in ["chave-1", "chave-2", "chave-3"]:
            selecionada, espera = manager.next_available_key()
            self.assertEqual((selecionada, espera), (chave, 0.0))
            manager.mark_exhausted(chave, 505712.0)

        self.assertTrue(manager.all_exhausted())
        self.assertEqual(manager.available_count(), 0)
        self.assertEqual(
            manager.next_available_key(),
            (None, 0.0),
        )

        manager.start_new_cycle()
        self.assertFalse(manager.all_exhausted())
        self.assertEqual(manager.available_count(), 3)
        self.assertEqual(manager.next_available_key(), ("chave-1", 0.0))

    def test_indisponibilidade_total_adia_item_sem_esperar_ou_reiniciar(self):
        manager = GeminiKeyRotationManager(["chave-1", "chave-2"])
        manager.mark_exhausted("chave-1", 505712.0)
        manager.mark_exhausted("chave-2", 505712.0)
        eventos = []
        saida = StringIO()

        resultado = resultado_adiar_item_todas_chaves_429(
            manager,
            emit=lambda evento, **campos: eventos.append((evento, campos)),
            key_rotations=[{"from_key": "chave-1"}, {"from_key": "chave-2"}],
            stream=saida,
        )

        self.assertIn("Todas as chaves Gemini estão indisponíveis por erro 429", saida.getvalue())
        self.assertIn("item atual será pulado", saida.getvalue())
        self.assertEqual(eventos[0][0], "gemini_all_keys_429_item_deferred")
        self.assertEqual(manager.available_count(), 0)
        self.assertEqual(resultado["status"], "error")
        self.assertEqual(resultado["http_status"], 429)
        self.assertTrue(resultado["retryable"])
        self.assertEqual(resultado["retry_after_seconds"], 505712.0)
        self.assertEqual(len(resultado["key_rotations"]), 2)

    def test_provider_generico_rotaciona_e_reinicia_apos_todas_429(self):
        class ProviderTeste(GenericProvider):
            name = "teste"
            rotate_comma_separated_keys = True

            def __init__(self):
                super().__init__("modelo")
                self.chamadas = []

            def _build_content(self, ctx):
                return "conteudo"

            def _call(self, ctx, content):
                self.chamadas.append(ctx.api_key)
                if len(self.chamadas) <= 2:
                    return {"status": "error", "error": "429", "http_status": 429}
                return {"status": "completed", "conclusoes": [], "error": ""}

        provider = ProviderTeste()
        contexto = ProviderContext(
            provider="teste", model="modelo", api_key="chave-1,chave-2",
            prompt="", auditado="ORG", questao_base="Q", coluna_evidencia="E",
            itens_afirmados=[], pacote={},
        )
        with patch("scripts.avaliacao_evidencias.providers.base.time.sleep") as sleep, patch(
            "scripts.avaliacao_evidencias.providers.base.sys.stderr", new=StringIO()
        ):
            resultado = provider.executar(contexto)

        self.assertEqual(resultado["status"], "completed")
        self.assertEqual(provider.chamadas, ["chave-1", "chave-2", "chave-1"])
        sleep.assert_called_once_with(180.0)


if __name__ == "__main__":
    unittest.main()
