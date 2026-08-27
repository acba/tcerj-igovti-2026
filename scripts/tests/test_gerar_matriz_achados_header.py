import unittest
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

from scripts.gerar_matriz_achados import atualizar_cabecalho
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


if __name__ == "__main__":
    unittest.main()
