"""Testes automatizados de invariantes numéricas e estruturais da auditoria iGovTI 2026.

Verifica a consistência estrita de dados entre:
- bd_auditados.xlsx
- resultado_auditoria.json (pos-comentarios-gestor, pos-avaliacao-evidencias, pos-ajuste-inicial)
- resumo-execucao.json
- resumo-testes-pareados-igovti-2023-2026.json
- Relatório_altaresolucao_novo.md
"""

import json
import unittest
from pathlib import Path
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]


class TestInvariantesAuditoria(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path_bd_auditados = (
            REPO_ROOT
            / "02-Execucao"
            / "03-Execucao_Procedimentos"
            / "01-Insumos"
            / "bd_auditados.xlsx"
        )
        cls.path_res_final = (
            REPO_ROOT
            / "02-Execucao"
            / "03-Execucao_Procedimentos"
            / "02-Resultados_Auditoria"
            / "03-pos-comentarios-gestor"
            / "resultado_auditoria.json"
        )
        cls.path_res_evid = (
            REPO_ROOT
            / "02-Execucao"
            / "03-Execucao_Procedimentos"
            / "02-Resultados_Auditoria"
            / "02-pos-avaliacao-evidencias"
            / "resultado_auditoria.json"
        )
        cls.path_res_base = (
            REPO_ROOT
            / "02-Execucao"
            / "03-Execucao_Procedimentos"
            / "02-Resultados_Auditoria"
            / "01-pos-ajuste-inicial"
            / "resultado_auditoria.json"
        )
        cls.path_resumo_exec = (
            REPO_ROOT
            / "03-Relatorios"
            / "99-Avaliacao_Comentarios_Gestor"
            / "dados"
            / "resumo-execucao.json"
        )
        cls.path_longitudinal = (
            REPO_ROOT
            / "03-Relatorios"
            / "99-Analise_Longitudinal"
            / "dados"
            / "resumo-testes-pareados-igovti-2023-2026.json"
        )
        cls.path_consolidado_md = (
            REPO_ROOT
            / "03-Relatorios"
            / "01-Relatorio_Consolidado"
            / "Relatório_altaresolucao_novo.md"
        )

        with open(cls.path_res_final, encoding="utf-8") as f:
            cls.res_final = json.load(f)
        with open(cls.path_res_evid, encoding="utf-8") as f:
            cls.res_evid = json.load(f)
        with open(cls.path_res_base, encoding="utf-8") as f:
            cls.res_base = json.load(f)
        with open(cls.path_resumo_exec, encoding="utf-8") as f:
            cls.resumo_exec = json.load(f)
        with open(cls.path_longitudinal, encoding="utf-8") as f:
            cls.longitudinal = json.load(f)
        with open(cls.path_consolidado_md, encoding="utf-8") as f:
            cls.consolidado_md = f.read()

        df_auditados = pd.read_excel(cls.path_bd_auditados)
        cls.total_universo = len(df_auditados)

    def test_universo_e_respondentes(self):
        """Verifica universo de 119 organizações, 113 válidas avaliadas e 6 não respondentes."""
        self.assertEqual(self.total_universo, 119, "Total do universo deve ser 119")
        self.assertEqual(len(self.res_final), 119, "resultado_auditoria.json deve conter 119 organizações")

        avaliados = [k for k, v in self.res_final.items() if v.get("status_avaliacao") == "avaliado"]
        nao_respondentes = [k for k, v in self.res_final.items() if v.get("status_avaliacao") == "nao_respondente"]

        self.assertEqual(len(avaliados), 113, "Devem ser exatamente 113 avaliados")
        self.assertEqual(len(nao_respondentes), 6, "Devem ser exatamente 6 não respondentes")
        self.assertEqual(sorted(nao_respondentes), ["CEHAB", "EMOP", "PESAGRO", "SEDCON", "SEPOL", "SESP"])

    def test_invariantes_achados_final(self):
        """Verifica totais de achados por questão no cenário final (pós-comentários)."""
        totais_esperados_achados = {
            1: 66,
            2: 101,
            3: 99,
            4: 109,
            5: 113,
            6: 103,
        }
        total_geral_achados = sum(totais_esperados_achados.values())
        self.assertEqual(total_geral_achados, 591, "Total de achados final deve ser 591")

        contagem_achados = {i: 0 for i in range(1, 7)}
        total_encontrado = 0
        for org in self.res_final.values():
            for p in org.get("procedimentos_executados", []):
                if p.get("achado_ocorreu"):
                    num = p.get("numero_achado")
                    contagem_achados[num] += 1
                    total_encontrado += 1

        self.assertEqual(total_encontrado, 591)
        self.assertEqual(contagem_achados, totais_esperados_achados)

    def test_invariantes_situacoes_final(self):
        """Verifica totais de situações por código no cenário final (pós-comentários)."""
        totais_esperados_situacoes = {
            "S1.1": 5, "S1.2": 55, "S1.3": 18,
            "S2.1": 94, "S2.2": 75, "S2.3": 27,
            "S3.1": 88, "S3.2": 25, "S3.4": 17, "S3.5": 20, "S3.6": 31,
            "S4.2": 107, "S4.3": 91, "S4.6": 1,
            "S5.1": 108, "S5.2": 111, "S5.3": 86, "S5.4": 110, "S5.5": 102,
            "S6.1": 87, "S6.2": 83, "S6.3": 33, "S6.4": 45,
        }
        total_geral_situacoes = sum(totais_esperados_situacoes.values())
        self.assertEqual(total_geral_situacoes, 1419, "Total de situações final deve ser 1419")

        contagem_situacoes = {k: 0 for k in totais_esperados_situacoes}
        total_encontrado = 0
        for org in self.res_final.values():
            for p in org.get("procedimentos_executados", []):
                if p.get("achado_ocorreu"):
                    for sit in p["achado"].get("situacoes_detalhadas", []):
                        cod = sit["id_situacao"]
                        self.assertIn(cod, contagem_situacoes, f"Situação desconhecida encontrada: {cod}")
                        contagem_situacoes[cod] += 1
                        total_encontrado += 1

        self.assertEqual(total_encontrado, 1419)
        self.assertEqual(contagem_situacoes, totais_esperados_situacoes)

    def test_evolucao_tres_cenarios(self):
        """Verifica a evolução nos 3 cenários (Base -> Pós-Evidências -> Pós-Comentários)."""
        def contar(res):
            total_ach = sum(
                1 for org in res.values()
                for p in org.get("procedimentos_executados", [])
                if p.get("achado_ocorreu")
            )
            total_sit = sum(
                len(p["achado"].get("situacoes_detalhadas", []))
                for org in res.values()
                for p in org.get("procedimentos_executados", [])
                if p.get("achado_ocorreu")
            )
            return total_ach, total_sit

        base_ach, base_sit = contar(self.res_base)
        evid_ach, evid_sit = contar(self.res_evid)
        final_ach, final_sit = contar(self.res_final)

        self.assertEqual((base_ach, base_sit), (565, 1252), "Cenário 1 deve ter 565 achados e 1252 situações")
        self.assertEqual((evid_ach, evid_sit), (602, 1458), "Cenário 2 deve ter 602 achados e 1458 situações")
        self.assertEqual((final_ach, final_sit), (591, 1419), "Cenário 3 deve ter 591 achados e 1419 situações")

    def test_metricas_contraditorio(self):
        """Verifica números do contraditório e impacto dos comentários do gestor."""
        r = self.resumo_exec
        self.assertEqual(r["manifestacoes_situacoes"], 1471)
        self.assertEqual(r["discordancias"], 236)
        self.assertEqual(r["manifestacoes_submetidas_decisao_individualizada"], 261)

        secao1 = r["avaliacao_secao_1"]
        self.assertEqual(secao1["Acolhida"], 46)
        self.assertEqual(secao1["Parcialmente acolhida"], 6)
        self.assertEqual(secao1["Não acolhida"], 209)

        secao2 = r["avaliacao_secao_2"]
        self.assertEqual(secao2["Acolhida"], 22)
        self.assertEqual(secao2["Parcialmente acolhida"], 24)
        self.assertEqual(secao2["Não acolhida"], 291)

        impacto = r["impactos"]
        self.assertEqual(impacto["situacoes_removidas"], 47)
        self.assertEqual(impacto["achados_removidos"], 11)
        self.assertEqual(impacto["organizacoes_com_igovti_aumentado"], 23)
        self.assertEqual(impacto["organizacoes_com_igovti_reduzido"], 0)

    def test_comparacao_longitudinal(self):
        """Verifica dados do pareamento longitudinal 2023-2026."""
        pareados = self.longitudinal["n_pares"]
        self.assertEqual(pareados, 68, "Devem ser 68 organizações pareadas")

        # Localizar indicador iGovTI
        final_igovti = next(item for item in self.longitudinal["resultados"]["final"] if item["indicador"] == "iGovTI")
        base_igovti = next(item for item in self.longitudinal["resultados"]["base"] if item["indicador"] == "iGovTI")

        self.assertAlmostEqual(final_igovti["media_2023"], 0.180, places=2)
        self.assertAlmostEqual(base_igovti["media_2026"], 0.248, places=2)
        self.assertAlmostEqual(final_igovti["media_2026"], 0.189, places=2)

        self.assertEqual(base_igovti["avancos"], 43)
        self.assertEqual(base_igovti["regressoes"], 25)

        self.assertEqual(final_igovti["avancos"], 32)
        self.assertEqual(final_igovti["regressoes"], 36)

    def test_ajustes_editoriais_consolidado_md(self):
        """Verifica a presença dos ajustes pontuais e ausência de termos vedados no texto."""
        # 5.1: ausência de pontuação
        self.assertIn(
            "ausência de pontuação nas práticas mensuradas pelo modelo após a avaliação realizada",
            self.consolidado_md,
        )
        self.assertNotIn("possível ausência de práticas de TIC", self.consolidado_md)

        # 5.2: fragilidades recorrentes
        self.assertIn("fragilidades recorrentes", self.consolidado_md)
        self.assertNotIn("fragilidades sistemáticas", self.consolidado_md)

        # 5.4: advertência sancionatória vinculada a descumprimento do plano de ação
        self.assertIn(
            "descumprimento injustificado da determinação ora expedida quanto à elaboração e ao registro do plano de ação",
            self.consolidado_md,
        )

        # 5.5: processo apartado para não respondentes
        self.assertIn(
            "ABERTURA DE PROCESSOS APARTADOS PARA APURAÇÃO INDIVIDUALIZADA DA AUSÊNCIA DE RESPOSTA VÁLIDA",
            self.consolidado_md,
        )

        # 5.6: caráter reservado
        self.assertIn(
            "caráter reservado dos anexos individuais",
            self.consolidado_md,
        )


if __name__ == "__main__":
    unittest.main()
