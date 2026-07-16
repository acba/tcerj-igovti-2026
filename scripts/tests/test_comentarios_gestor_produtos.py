from __future__ import annotations

import unittest

from scripts.comentarios_gestor_produtos import (
    _decisao_secao1,
    _decisao_secao2,
    _limpar_fundamentacao,
    normalizar_data_referencia,
)


class ComentariosGestorProdutosTest(unittest.TestCase):
    def test_situacao_corrigida_e_acolhida_na_posicao_corrente(self) -> None:
        decisao, situacao = _decisao_secao1({"estado_temporal": "corrigida_posteriormente"})
        self.assertEqual(decisao, "acolhida")
        self.assertEqual(situacao, "Situação não caracterizada na data de referência")

    def test_secao2_parcial_quando_apenas_parte_dos_itens_e_conforme(self) -> None:
        decisao = _decisao_secao2([{"estado": "conforme"}, {"estado": "nao_conforme"}])
        self.assertEqual(decisao, "parcialmente acolhida")

    def test_texto_externo_remove_discussao_historica(self) -> None:
        texto = _limpar_fundamentacao(
            "O ato formal foi apresentado. A correção ocorreu após a data-base da auditoria. O requisito está atendido."
        )
        self.assertEqual(texto, "O ato formal foi apresentado. O requisito está atendido.")

    def test_data_referencia_e_obrigatoriamente_ddmmyyyy(self) -> None:
        self.assertEqual(normalizar_data_referencia("16/07/2026"), "16/07/2026")
        with self.assertRaisesRegex(ValueError, "DD/MM/AAAA"):
            normalizar_data_referencia("2026-07-16")


if __name__ == "__main__":
    unittest.main()
