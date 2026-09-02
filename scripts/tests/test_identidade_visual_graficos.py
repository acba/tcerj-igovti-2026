import unittest
import os
from pathlib import Path
from tempfile import TemporaryDirectory

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-igovti-testes")

import matplotlib.pyplot as plt
from PIL import Image

from scripts.resources.identidade_visual_graficos import (
    CORES,
    CORES_MATURIDADE,
    DPI_PADRAO,
    FAMILIA_TIPOGRAFICA,
    aplicar_estilo,
    cor_texto_contraste,
    salvar_figura,
)


ROOT = Path(__file__).resolve().parents[2]
GERADORES = (
    ROOT / "scripts/gerar_graficos_relatorios_consolidado_individuais_igovti.py",
    ROOT / "scripts/gerar_graficos_achados_consolidado.py",
    ROOT / "scripts/gerar_graficos_igovti_comparavel.py",
    ROOT / "scripts/analisar_achados_igovti_2026.py",
    ROOT / "03-Relatorios/99-Analise_Longitudinal/calcular_analise_longitudinal.py",
    ROOT / "03-Relatorios/99-Avaliacao_Comentarios_Gestor/calcular_dados_comentarios_gestor.py",
    ROOT / "03-Relatorios/99-Avaliacao_IA/gerar_grafico_institucionalizacao_ia.py",
)


class IdentidadeVisualGraficosTest(unittest.TestCase):
    def test_todos_os_geradores_usam_a_identidade_compartilhada(self):
        for caminho in GERADORES:
            with self.subTest(caminho=caminho):
                fonte = caminho.read_text(encoding="utf-8")
                self.assertIn("identidade_visual_graficos", fonte)

    def test_estilo_define_familia_tipografica_e_resolucao(self):
        aplicar_estilo(tamanho_fonte=10)
        self.assertEqual(plt.rcParams["font.family"][0], FAMILIA_TIPOGRAFICA)
        self.assertEqual(plt.rcParams["savefig.dpi"], DPI_PADRAO)

    def test_paleta_semantica_reutiliza_cores_canonicas(self):
        self.assertEqual(CORES_MATURIDADE["Inexpressivo"], "#B33A3A")
        self.assertEqual(CORES_MATURIDADE["Iniciando"], "#FFA500")
        self.assertEqual(CORES_MATURIDADE["Intermediário"], "#9ACD32")
        self.assertEqual(CORES_MATURIDADE["Aprimorado"], "#228B22")
        self.assertNotIn("azul_petroleo", CORES)
        self.assertNotIn("grade", CORES)
        self.assertNotIn("borda", CORES)

    def test_contraste_escolhe_texto_claro_em_cores_escuras(self):
        self.assertEqual(cor_texto_contraste(CORES["negativo"]), "#FFFFFF")
        self.assertEqual(cor_texto_contraste(CORES["positivo"]), "#FFFFFF")
        self.assertEqual(cor_texto_contraste(CORES["laranja"]), CORES["texto"])

    def test_salvamento_png_usa_trezentos_dpi(self):
        with TemporaryDirectory() as diretorio:
            destino = Path(diretorio) / "grafico.png"
            fig, ax = plt.subplots(figsize=(2, 1))
            ax.plot([0, 1], [0, 1])
            salvar_figura(fig, destino)
            with Image.open(destino) as imagem:
                dpi = imagem.info["dpi"]
            self.assertGreaterEqual(min(dpi), 299)


if __name__ == "__main__":
    unittest.main()
