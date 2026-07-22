from __future__ import annotations

import unittest
import tempfile
from pathlib import Path

from scripts.comentarios_gestor_produtos import (
    _campos_manifestacao_secao1,
    _decisao_secao1,
    _decisao_secao2,
    _limpar_fundamentacao,
    _carregar_revisoes,
    _texto_equipe_secao1,
    normalizar_data_referencia,
)


class ComentariosGestorProdutosTest(unittest.TestCase):
    def test_helper_legado_de_texto_secao1_mantem_inicio_e_fundamentacao(self) -> None:
        texto = _texto_equipe_secao1(
            "acolhida",
            "A documentação comprovou o atendimento.",
        )
        self.assertEqual(texto, "A manifestação foi acolhida. A documentação comprovou o atendimento.")

    def test_alternativa_e_textos_livres_da_secao1_ficam_separados(self) -> None:
        alternativa, comentario, justificativa = _campos_manifestacao_secao1(
            {
                "A2G4Conc": "Concorda, mas ainda não adotou nenhuma medida",
                "A2G4Com": "Comentário livre.",
                "A2G4Jus": "Justificativa complementar.",
            },
            "A2G4",
        )
        self.assertEqual(alternativa, "Concorda, mas ainda não adotou nenhuma medida")
        self.assertEqual(comentario, "Comentário livre.")
        self.assertEqual(justificativa, "Justificativa complementar.")

    def test_situacao_corrigida_e_acolhida_na_posicao_corrente(self) -> None:
        decisao, situacao = _decisao_secao1({"estado_temporal": "corrigida_posteriormente"})
        self.assertEqual(decisao, "acolhida")
        self.assertEqual(situacao, "Situação não existente")

    def test_secao2_parcial_quando_apenas_parte_dos_itens_e_conforme(self) -> None:
        decisao = _decisao_secao2([{"estado": "conforme"}, {"estado": "nao_conforme"}])
        self.assertEqual(decisao, "parcialmente acolhida")

    def test_insuficiencia_com_fundamento_afastado_e_parcialmente_acolhida(self) -> None:
        decisao, situacao = _decisao_secao1(
            {
                "estado_temporal": "mantida",
                "conclusoes_motivos": [
                    {"estado_motivo": "afastado"},
                    {"estado_motivo": "mantido"},
                ],
            }
        )
        self.assertEqual(decisao, "parcialmente acolhida")
        self.assertEqual(situacao, "Situação existente")

    def test_insuficiencia_sem_fundamento_afastado_e_nao_acolhida(self) -> None:
        decisao, situacao = _decisao_secao1(
            {
                "estado_temporal": "mantida",
                "conclusoes_motivos": [{"estado_motivo": "mantido"}],
            }
        )
        self.assertEqual(decisao, "não acolhida")
        self.assertEqual(situacao, "Situação existente")

    def test_secao2_insuficiente_sem_item_conforme_e_nao_acolhida(self) -> None:
        decisao = _decisao_secao2([{"estado": "inconclusivo"}, {"estado": "nao_conforme"}])
        self.assertEqual(decisao, "não acolhida")

    def test_fundamentacao_preserva_texto_do_juiz(self) -> None:
        texto = _limpar_fundamentacao(
            "O ato formal foi apresentado. A correção ocorreu após a data-base da auditoria. O requisito está atendido."
        )
        self.assertEqual(
            texto,
            "O ato formal foi apresentado. A correção ocorreu após a data-base da auditoria. O requisito está atendido.",
        )

    def test_fundamentacao_temporal_nao_e_reescrita_pelo_produto(self) -> None:
        fundamento = (
            "Os documentos são posteriores à data-base da auditoria. "
            "A inconformidade persistia no período auditado, caracterizando correção posterior."
        )
        self.assertEqual(_limpar_fundamentacao(fundamento), fundamento)

    def test_data_referencia_e_obrigatoriamente_ddmmyyyy(self) -> None:
        self.assertEqual(normalizar_data_referencia("16/07/2026"), "16/07/2026")
        with self.assertRaisesRegex(ValueError, "DD/MM/AAAA"):
            normalizar_data_referencia("2026-07-16")

    def test_revisoes_yaml_sao_indexadas_por_auditado_secao_codigo(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "revisoes.yml"
            path.write_text(
                "revisoes:\n"
                "  - auditado: SÃO JOÃO DE MERITI\n"
                "    secao: '1'\n"
                "    codigo: A4G14\n"
                "    decisao: acolhida\n"
                "    situacao_atual: Situação não caracterizada na data de referência\n"
                "    manifestacao_equipe: A lei comprova os cargos de SI.\n",
                encoding="utf-8",
            )
            revisoes = _carregar_revisoes(path)
            self.assertEqual(revisoes[("SÃO JOÃO DE MERITI", "1", "A4G14")]["decisao"], "acolhida")
            self.assertEqual(
                revisoes[("SÃO JOÃO DE MERITI", "1", "A4G14")]["situacao_atual"],
                "Situação não caracterizada na data de referência",
            )


if __name__ == "__main__":
    unittest.main()
