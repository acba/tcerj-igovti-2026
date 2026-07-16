import unittest

import pandas as pd

from scripts.coletar_anexos_limesurvey import normalizar_url_download


class NormalizarUrlDownloadTests(unittest.TestCase):
    def test_valores_sem_anexo_resultam_em_vazio(self):
        for valor in (None, pd.NA, float("nan"), "", "  ", "nan", "None", "<NA>"):
            with self.subTest(valor=valor):
                self.assertEqual(normalizar_url_download(valor), "")

    def test_url_e_preservada_sem_espacos_externos(self):
        self.assertEqual(
            normalizar_url_download("  https://example.test/anexos/1  "),
            "https://example.test/anexos/1",
        )


if __name__ == "__main__":
    unittest.main()
