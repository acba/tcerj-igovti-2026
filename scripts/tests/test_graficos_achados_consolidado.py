import tempfile
import unittest
from pathlib import Path

from openpyxl import Workbook

from scripts.gerar_graficos_achados_consolidado import parse_excel_spheres


class ParseExcelSpheresTest(unittest.TestCase):
    def test_le_celulas_inline_geradas_pelo_openpyxl(self):
        workbook = Workbook()
        sheet = workbook.active
        sheet.append(["sigla", "orgao", "esfera"])
        sheet.append(["DERRJ", "Departamento", "E"])
        sheet.append(["NITERÓI", "Prefeitura", "M"])
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "auditados.xlsx"
            workbook.save(path)
            self.assertEqual(
                parse_excel_spheres(path),
                {"DERRJ": "E", "NITERÓI": "M"},
            )


if __name__ == "__main__":
    unittest.main()
