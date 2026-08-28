import unittest
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

from scripts.gerar_matriz_achados import (
    atualizar_cabecalho,
    atualizar_documento,
    montar_dados,
)
from scripts.gerar_matriz_planejamento import (
    AUDITED_ENTITIES_HEADER,
    AUDIT_OBJECTIVE_HEADER,
    W,
)


MATRIX_PATH = Path("02-Execucao/04-Matriz_Achados/AN06 – Matriz de achados.docx")


class MatrizAchadosHeaderTest(unittest.TestCase):
    def test_cabecalho_usa_escopo_e_objetivo_padronizados(self):
        with ZipFile(MATRIX_PATH) as archive:
            updated = atualizar_cabecalho(archive.read("word/header1.xml"))
        root = ET.fromstring(updated)
        text = "".join(element.text or "" for element in root.iter(f"{W}t"))

        self.assertIn(f"JURISDICIONADOS: {AUDITED_ENTITIES_HEADER}", text)
        self.assertIn(f"OBJETIVO DA AUDITORIA: {AUDIT_OBJECTIVE_HEADER}", text)


class MatrizAchadosConteudoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dados = montar_dados(Path(".").resolve())

    def test_criterios_usam_ids_sequenciais_da_visao_da_matriz(self):
        achado = self.dados[0]

        self.assertEqual(
            [item["id_exibicao"] for item in achado["criterios"]],
            ["C1", "C2", "C3", "C4", "C5"],
        )
        self.assertEqual(
            {
                publico: [item["id_exibicao"] for item in criterios]
                for publico, criterios in achado["criterios_especificos"].items()
            },
            {
                "Poder Executivo Estadual": ["C6"],
                "Poder Judiciário Estadual": ["C7"],
                "Ministério Público Estadual": ["C8"],
            },
        )

    def test_evidencias_sao_agrupadas_por_situacao(self):
        evidencias = self.dados[0]["evidencias"]

        self.assertEqual(
            evidencias[0]["situacao"],
            "S1.1 - Ausência de área, unidade, setor ou função de TIC formalmente instituída",
        )
        self.assertEqual(evidencias[0]["itens"], ["alternativa f) em q0101"])

    def test_variantes_comuns_sao_agrupadas_com_seus_criterios(self):
        grupos = self.dados[0]["encaminhamentos"][0]["grupos"]

        self.assertEqual(grupos[0]["publico"], "Demais jurisdicionados")
        self.assertEqual(grupos[0]["criterios"], ["C1", "C5"])
        self.assertEqual(
            grupos[1]["publico"],
            "Poder Executivo Estadual, Poder Judiciário Estadual e Ministério Público Estadual",
        )
        self.assertEqual(grupos[1]["criterios"], ["C1", "C6", "C7", "C8"])

    def test_todos_os_encaminhamentos_referenciam_criterios_exibidos(self):
        for achado in self.dados:
            exibidos = {item["id_exibicao"] for item in achado["criterios"]}
            exibidos.update(
                item["id_exibicao"]
                for criterios in achado["criterios_especificos"].values()
                for item in criterios
            )
            for situacao in achado["encaminhamentos"]:
                for grupo in situacao["grupos"]:
                    self.assertTrue(grupo["criterios"])
                    self.assertTrue(set(grupo["criterios"]).issubset(exibidos))

    def test_documento_exibe_dispositivo_em_negrito_e_vinculos(self):
        with ZipFile(MATRIX_PATH) as archive:
            updated = atualizar_documento(archive.read("word/document.xml"), self.dados)
        root = ET.fromstring(updated)
        namespace = {"w": W.removesuffix("}").removeprefix("{")}
        first_row = root.findall(".//w:tbl", namespace)[0].findall("w:tr", namespace)[1]
        cells = first_row.findall("w:tc", namespace)

        criterion_runs = cells[1].findall(".//w:r", namespace)
        bold_text = [
            "".join(node.text or "" for node in run.findall("w:t", namespace))
            for run in criterion_runs
            if run.find("w:rPr/w:b", namespace) is not None
        ]
        evidence_text = "".join(node.text or "" for node in cells[2].iter(f"{W}t"))
        referral_text = "".join(node.text or "" for node in cells[5].iter(f"{W}t"))

        self.assertIn("C1: COBIT 2019, APO01.04", bold_text)
        self.assertIn("C6: Decreto Estadual nº 47.278/2020 (alterado pelo Decreto nº 48.997/2024), arts. 4º e 6º, I a XI, e Portaria PRODERJ/PRE nº 825/2021, Anexo A, arts. 1º, IX, 8º e 9º", bold_text)
        self.assertIn("S1.1 - Ausência de área", evidence_text)
        self.assertIn("• alternativa f) em q0101.", evidence_text)
        self.assertIn(
            "Poder Executivo Estadual, Poder Judiciário Estadual e Ministério Público Estadual",
            referral_text,
        )
        self.assertIn("[S1.1, C1, C6, C7, C8]", referral_text)

    def test_colunas_achado_e_encaminhamento_seguem_composicao_visual(self):
        with ZipFile(MATRIX_PATH) as archive:
            updated = atualizar_documento(archive.read("word/document.xml"), self.dados)
        root = ET.fromstring(updated)
        namespace = {"w": W.removesuffix("}").removeprefix("{")}
        first_row = root.findall(".//w:tbl", namespace)[0].findall("w:tr", namespace)[1]
        cells = first_row.findall("w:tc", namespace)
        finding_paragraphs = [
            "".join(node.text or "" for node in paragraph.iter(f"{W}t"))
            for paragraph in cells[0].findall("w:p", namespace)
        ]
        referral_paragraphs = [
            "".join(node.text or "" for node in paragraph.iter(f"{W}t"))
            for paragraph in cells[5].findall("w:p", namespace)
        ]

        self.assertIn(
            "Achado composto pela ocorrência de alguma dessas situações:",
            finding_paragraphs,
        )
        self.assertIn(
            "• S1.1 - Ausência de área, unidade, setor ou função de TIC formalmente instituída",
            finding_paragraphs,
        )
        self.assertIn(
            "Ausência de área, unidade, setor ou função de TIC formalmente instituída",
            referral_paragraphs,
        )
        self.assertTrue(any(paragraph.startswith("• Comunicação com Recomendação")
                            for paragraph in referral_paragraphs))
        self.assertTrue(any("[S1.1, C1, C5]" in paragraph for paragraph in referral_paragraphs))
        self.assertNotIn("Demais jurisdicionados", referral_paragraphs)
        self.assertNotIn("Todos os jurisdicionados", referral_paragraphs)
        self.assertNotIn(
            "S1.1 - Ausência de área, unidade, setor ou função de TIC formalmente instituída",
            referral_paragraphs,
        )

    def test_achados_segundo_ao_sexto_comecam_em_nova_pagina(self):
        with ZipFile(MATRIX_PATH) as archive:
            updated = atualizar_documento(archive.read("word/document.xml"), self.dados)
        root = ET.fromstring(updated)
        namespace = {"w": W.removesuffix("}").removeprefix("{")}
        body = root.find("w:body", namespace)
        children = list(body)
        tables = body.findall("w:tbl", namespace)

        self.assertEqual(len(tables), 6)
        for table in tables[1:]:
            position = children.index(table)
            self.assertGreater(position, 0)
            previous = children[position - 1]
            self.assertEqual(previous.tag, f"{W}p")
            self.assertIsNotNone(
                previous.find(".//w:br[@w:type='page']", namespace),
                "Cada achado posterior ao primeiro deve ter uma quebra de página estrutural.",
            )


if __name__ == "__main__":
    unittest.main()
