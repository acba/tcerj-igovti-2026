"""Identidade visual compartilhada dos gráficos da Fiscalização iGovTI 2026."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb


ESTILO_MATPLOTLIB = "seaborn-v0_8-whitegrid"
FAMILIA_TIPOGRAFICA = "DejaVu Sans"
DPI_PADRAO = 300

CORES = {
    "texto": "#263238",
    "texto_secundario": "#52606D",
    "fundo": "#FFFFFF",
    "azul_institucional": "#1F4E79",
    "azul_medio": "#3B6EA8",
    "azul_claro": "#7FA9CF",
    "laranja": "#FFA500",
    "negativo": "#B33A3A",
    "positivo": "#228B22",
    "neutro": "#9AA3AA",
    "neutro_claro": "#D2D7DB",
}

CORES_MATURIDADE = {
    "Inexpressivo": CORES["negativo"],
    "Iniciando": CORES["laranja"],
    "Intermediário": "#9ACD32",
    "Aprimorado": CORES["positivo"],
}

CORES_ESFERAS = {
    "Estadual": CORES["azul_medio"],
    "Municipal": CORES["azul_institucional"],
}

CORES_LONGITUDINAL = {
    "2023": CORES["laranja"],
    "2026_base": CORES["azul_claro"],
    "2026_final": CORES["azul_institucional"],
}

CORES_COMENTARIOS = {
    "Concorda e ja atendeu": CORES["positivo"],
    "Concorda e esta atendendo": CORES_MATURIDADE["Intermediário"],
    "Concorda, sem medida adotada": CORES["laranja"],
    "Discorda": CORES["negativo"],
    "Situacao encontrada inexistente": CORES["neutro_claro"],
}

CORES_DECISOES = {
    "Acolhida": CORES["positivo"],
    "Parcialmente acolhida": CORES["laranja"],
    "Não acolhida": CORES["negativo"],
}

CORES_IA = {
    "Não adota": CORES["neutro"],
    "Planejamento ou adoção incipiente": CORES["laranja"],
    "Adoção parcial ou superior": CORES["positivo"],
    "Não se aplica": "#D9E1F2",
}

PALETA_CATEGORICA = (
    CORES["azul_medio"],
    "#7556A5",
    CORES["laranja"],
    CORES["azul_institucional"],
    CORES["negativo"],
    CORES["texto_secundario"],
)


def aplicar_estilo(*, tamanho_fonte: float = 10) -> None:
    """Aplica o estilo editorial comum sem impor grade em eixos inadequados."""
    plt.style.use(ESTILO_MATPLOTLIB)
    plt.rcParams.update(
        {
            "font.family": FAMILIA_TIPOGRAFICA,
            "font.size": tamanho_fonte,
            "axes.titlesize": tamanho_fonte + 1.5,
            "axes.titleweight": "bold",
            "axes.labelcolor": CORES["texto"],
            "axes.titlecolor": CORES["texto"],
            "axes.edgecolor": CORES["neutro"],
            "axes.facecolor": CORES["fundo"],
            "axes.grid": False,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "xtick.color": CORES["texto"],
            "ytick.color": CORES["texto"],
            "figure.facecolor": CORES["fundo"],
            "savefig.facecolor": CORES["fundo"],
            "savefig.dpi": DPI_PADRAO,
        }
    )


def legenda_superior(
    ax,
    *,
    ncol: int,
    titulo: str | None = None,
    y: float = 1.02,
    fontsize: float | None = None,
    handles=None,
):
    """Posiciona a legenda em faixa superior, fora da área dos dados."""
    kwargs = {
        "loc": "lower center",
        "bbox_to_anchor": (0.5, y),
        "ncol": ncol,
        "frameon": False,
        "borderaxespad": 0,
        "title": titulo,
    }
    if fontsize is not None:
        kwargs["fontsize"] = fontsize
    if handles is not None:
        kwargs["handles"] = handles
    return ax.legend(**kwargs)


def cor_texto_contraste(cor_fundo: str) -> str:
    """Escolhe texto claro ou escuro pelo maior contraste WCAG com o fundo."""

    def luminancia_relativa(cor: str) -> float:
        canais = []
        for canal in to_rgb(cor):
            canais.append(
                canal / 12.92
                if canal <= 0.04045
                else ((canal + 0.055) / 1.055) ** 2.4
            )
        return 0.2126 * canais[0] + 0.7152 * canais[1] + 0.0722 * canais[2]

    fundo = luminancia_relativa(cor_fundo)
    candidatos = (CORES["texto"], "#FFFFFF")

    def razao_contraste(cor: str) -> float:
        texto = luminancia_relativa(cor)
        mais_claro, mais_escuro = max(fundo, texto), min(fundo, texto)
        return (mais_claro + 0.05) / (mais_escuro + 0.05)

    return max(candidatos, key=razao_contraste)


def salvar_figura(
    fig,
    path: str | Path,
    *,
    fechar: bool = True,
    dpi: int = DPI_PADRAO,
    **kwargs,
) -> None:
    """Salva PNG em 300 dpi, com metadados e fundo uniformes."""
    destino = Path(path)
    destino.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        destino,
        dpi=dpi,
        bbox_inches="tight",
        facecolor=CORES["fundo"],
        metadata={"Software": "TCE-RJ iGovTI 2026"},
        **kwargs,
    )
    if fechar:
        plt.close(fig)
