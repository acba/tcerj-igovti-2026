import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

from scripts.gerar_matriz_planejamento import (
    DEFAULT_TEMPLATE,
    W,
    CellParagraph,
    compact_display_identifiers,
    format_criteria,
    format_findings_or_analysis,
    format_items,
    generate_docx,
    parse_matrix,
)


MATRIX_PATH = Path(
    "01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/"
    "matriz_planejamento-pos-comentarios-gestor.md"
)


class MatrizPlanejamentoDocxTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matrix = parse_matrix(MATRIX_PATH.read_text(encoding="utf-8"))

    def test_possiveis_achados_usam_hierarquia_sem_ids_visuais(self):
        question = next(item for item in self.matrix.questions if item.id == "Q1")
        paragraphs = format_findings_or_analysis(
            question, compact_display_identifiers(question)
        )
        texts = [item.text if isinstance(item, CellParagraph) else item for item in paragraphs]

        self.assertIn(
            "Estrutura de TIC insuficientemente formalizada, definida ou posicionada "
            "para gerir a tecnologia da informação.",
            texts,
        )
        self.assertIn(
            "Ausência de área, unidade, setor ou função de TIC formalmente instituída."
            "[R1.1, P1, E1, C1, C5];",
            texts,
        )
        self.assertIn("Tipo: Recomendação;", texts)
        self.assertFalse(any(text.startswith("A1:") or text.startswith("S1.1:") for text in texts))

    def test_variaveis_derivadas_nao_vazam_para_evidencias(self):
        question = next(item for item in self.matrix.questions if item.id == "Q4")
        evidence_text = "\n".join(item.raw for item in question.evidencias)

        self.assertIn("E7: Modelo de operação de TIC predominantemente terceirizado", evidence_text)
        self.assertNotIn("variaveis_derivadas", evidence_text)
        self.assertNotIn("nome: total_TI", evidence_text)

    def test_ids_sao_compactados_apenas_na_view_e_referencias_acompanham(self):
        question = next(item for item in self.matrix.questions if item.id == "Q1")
        mapping = compact_display_identifiers(question)

        self.assertEqual(mapping["C6"], "C4")
        self.assertEqual(mapping["C7"], "C5")
        self.assertEqual(question.criterios[-1].id, "C7")

        criteria = format_criteria(question, mapping)
        criteria_text = [item.text if isinstance(item, CellParagraph) else item for item in criteria]
        self.assertTrue(any(text.startswith("C4: Portaria SGD/ME") for text in criteria_text))
        self.assertTrue(any(text.startswith("C5: Constituição Federal") for text in criteria_text))

        findings = format_findings_or_analysis(question, mapping)
        finding_text = [item.text if isinstance(item, CellParagraph) else item for item in findings]
        self.assertTrue(any("[R1.1, P1, E1, C1, C5];" in text for text in finding_text))

        question_four = next(item for item in self.matrix.questions if item.id == "Q4")
        mapping_four = compact_display_identifiers(question_four)
        evidence_view = format_items(question_four.evidencias, mapping_four)
        self.assertTrue(any(text.startswith("E4: Modelo de operação") for text in evidence_view))
        self.assertTrue(any(text.endswith("[P4]") for text in evidence_view if text.startswith("E4:")))

    def test_questoes_comecam_em_nova_pagina_e_tabelas_sao_adjacentes(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "matriz.docx"
            generate_docx(DEFAULT_TEMPLATE, MATRIX_PATH, output)
            with ZipFile(output) as archive:
                root = ET.fromstring(archive.read("word/document.xml"))

        body = root.find(f"{W}body")
        self.assertIsNotNone(body)
        children = list(body)
        page_break_indexes = [
            index
            for index, child in enumerate(children)
            if child.tag == f"{W}p"
            and child.find(f".//{W}br[@{W}type='page']") is not None
        ]
        self.assertEqual(len(page_break_indexes), len(self.matrix.questions))
        for index in page_break_indexes:
            self.assertEqual(children[index + 1].tag, f"{W}tbl")
            self.assertEqual(children[index + 2].tag, f"{W}tbl")

        document_text = "".join(element.text or "" for element in root.iter(f"{W}t"))
        self.assertNotIn("JURISDICIONADOS:", document_text)


if __name__ == "__main__":
    unittest.main()
