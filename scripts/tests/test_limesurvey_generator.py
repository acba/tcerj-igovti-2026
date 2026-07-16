import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


RESOURCES = Path(__file__).resolve().parents[1] / "resources"
sys.path.insert(0, str(RESOURCES))

from limesurvey_generator import LimeSurveyGenerator  # noqa: E402


class LimeSurveyGeneratorTest(unittest.TestCase):
    def test_uploads_de_achados_aceitam_apenas_pdf_ou_zip(self) -> None:
        generator = LimeSurveyGenerator()
        questions_xml, upload_qids, _, _ = generator._build_questions(
            [(1, "Achado de teste", "Situação de teste")],
            [],
            [],
            "iGovTI 2026",
        )
        attributes_xml = generator._build_question_attributes(upload_qids)

        questions = ET.fromstring(questions_xml)
        evidence_qid = next(
            row.findtext("qid")
            for row in questions.findall("./rows/row")
            if row.findtext("title") == "A1G1Evi"
        )
        attributes = ET.fromstring(attributes_xml)
        values = {
            row.findtext("attribute"): row.findtext("value")
            for row in attributes.findall("./rows/row")
            if row.findtext("qid") == evidence_qid
        }

        self.assertEqual(values["allowed_filetypes"], "pdf,zip")
        self.assertEqual(values["max_num_of_files"], "1")

    def test_grupo_de_ciencia_e_o_ultimo_e_exige_confirmacao(self) -> None:
        generator = LimeSurveyGenerator()
        sorted_keys = [(1, "Achado de teste", "Situação de teste")]
        groups = ET.fromstring(
            generator._build_groups(
                sorted_keys,
                sorted_keys and {sorted_keys[0]: {"ORG"}},
                sorted_keys and {sorted_keys[0]: set()},
                [],
                [],
                "iGovTI 2026",
            )
        )
        group_rows = groups.findall("./rows/row")
        self.assertEqual(group_rows[-1].findtext("group_name"), "Ciência")

        questions_xml, _, ciencia_qid, ciencia_gid = generator._build_questions(
            sorted_keys,
            [],
            [],
            "iGovTI 2026",
        )
        questions = ET.fromstring(questions_xml)
        ciencia = next(
            row
            for row in questions.findall("./rows/row")
            if row.findtext("qid") == str(ciencia_qid)
        )
        self.assertEqual(ciencia.findtext("gid"), str(ciencia_gid))
        self.assertEqual(ciencia.findtext("title"), "qciencia")
        self.assertEqual(ciencia.findtext("type"), "M")
        self.assertEqual(ciencia.findtext("mandatory"), "Y")

        subquestions = ET.fromstring(generator._build_subquestions(ciencia_qid, ciencia_gid))
        declaration = subquestions.find("./rows/row")
        self.assertIsNotNone(declaration)
        self.assertEqual(declaration.findtext("parent_qid"), str(ciencia_qid))
        self.assertIn("Declaro estar ciente", declaration.findtext("question"))


if __name__ == "__main__":
    unittest.main()
