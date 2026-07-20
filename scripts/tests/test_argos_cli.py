from __future__ import annotations

import unittest

from scripts.argos_cli import ROUTINE_BY_KEY, apply_named_params, apply_scenario, build_command, param_values


class ArgosCliTest(unittest.TestCase):
    def test_parametro_nomeado_e_validado(self) -> None:
        routine = ROUTINE_BY_KEY["calcular-igovti"]
        values = param_values(routine)
        apply_named_params(routine, values, ["prefixo=20260718"])
        self.assertEqual(values["prefixo"], "20260718")
        with self.assertRaisesRegex(ValueError, "desconhecido"):
            apply_named_params(routine, values, ["inexistente=x"])

    def test_cenario_define_caminhos_independentes(self) -> None:
        routine = ROUTINE_BY_KEY["calcular-igovti"]
        values = param_values(routine)
        apply_scenario(routine, values, "03-pos-comentarios-gestor")
        command = build_command(routine, values)
        self.assertIn("03-pos-comentarios-gestor", " ".join(command))
        self.assertIn("--resultados-dir", command)

    def test_fonte_repetida_gera_uma_flag_por_mapeamento(self) -> None:
        routine = ROUTINE_BY_KEY["executar-auditoria"]
        values = param_values(routine)
        values["fontes"] = ""
        values["fonte"] = "questionario=a.xlsx avaliacao_evidencias_ajustes=b.xlsx"
        command = build_command(routine, values)
        self.assertEqual(command.count("--fonte"), 2)


if __name__ == "__main__":
    unittest.main()
