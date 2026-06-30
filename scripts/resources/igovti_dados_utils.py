#!/usr/bin/env python3
"""Funcoes compartilhadas para leitura e comparacao dos resultados do iGovTI."""

from __future__ import annotations

import os
import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]


def to_relative(path: str | Path) -> str:
    """Retorna o caminho de um arquivo relativo ao ROOT do projeto se possivel."""
    try:
        p = Path(path).resolve()
        r = ROOT.resolve()
        return os.path.relpath(p, start=r)
    except Exception:
        return str(path)

RESULTADOS_2026 = ROOT / "02-Execucao/01-Questionario/04-Resultados_iGovTI/20260621-iGovTI-2026.xlsx"
RESPOSTAS_2026 = ROOT / "02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario.xlsx"
COMPARAVEL_2026 = ROOT / "02-Execucao/01-Questionario/04-Resultados_iGovTI/20260621-iGovTI-2026-Ajustado-Comparavel.xlsx"
COMPARAVEL_2023_SETIC = ROOT / "02-Execucao/02-Questionario iGovTI 2023/iGovTI-2023-SETIC-Ajustado-Comparavel.xlsx"
COMPARAVEL_2023_MUNICIPIOS = ROOT / "02-Execucao/02-Questionario iGovTI 2023/iGovTI-2023-Municipios-Ajustado-Comparavel.xlsx"

NIVEIS = ["Inexpressivo", "Iniciando", "Intermediário", "Aprimorado"]
ORDEM_NIVEIS = {nivel: indice for indice, nivel in enumerate(NIVEIS)}

# Correspondencias institucionais explicitamente validadas. Coincidencias apenas
# lexicais nao devem ser acrescentadas automaticamente a esta relacao.
ALIASES_2023_2026 = {
    "FIARJ": "FIA",
    "FTMRJ": "FTM",
    "IO": "IOERJ",
    "IPEMRJ": "IPEM",
    "RIOPREVI": "RIOPREVIDENCIA",
    "RIOTRILH": "RIOTRILHOS",
    "SEDSODH": "SEDSDH",
}

AGREGADOS_COMPARAVEIS = {
    "ModeloTI": "Modelo de gestão de TIC",
    "MonitorAvaliaTI": "Monitoramento e avaliação de TIC",
    "ResultadoTI": "Resultados de TIC",
    "PlanejamentoTI": "Planejamento de TIC",
    "PessoasTI": "Gestão de pessoas de TIC",
    "iGestServicosTI": "Gestão de serviços de TIC",
    "iGestNiveisServicoTI": "Gestão de níveis de serviço",
    "iGestRiscosTI": "Gestão de riscos de TIC",
    "EstruturaSegInfo": "Estrutura de segurança da informação",
    "ProcessoSegInfo": "Processos de segurança da informação",
    "ProcessoSoftware": "Processo de software",
    "iGestProjetosTI": "Gestão de projetos de TIC",
    "ProcessosContratacao": "Processos de contratação de TIC",
}

INDICADORES_COMPARAVEIS = {
    "iGovTI": "iGovTI ajustado comparável",
    "GovernancaTI": "Governança de TIC",
    "iGestTI": "Gestão de TIC",
    **AGREGADOS_COMPARAVEIS,
}


def normalizar_sigla(valor: object) -> str:
    texto = unicodedata.normalize("NFKD", str(valor or ""))
    texto = texto.encode("ascii", "ignore").decode().upper().strip()
    texto = re.sub(r"^PREFEITURA MUNICIPAL DE\s+", "", texto)
    return re.sub(r"[^A-Z0-9]", "", texto)


def classificar_maturidade(valor: float) -> str:
    if valor < 0.15:
        return "Inexpressivo"
    if valor < 0.40:
        return "Iniciando"
    if valor < 0.70:
        return "Intermediário"
    return "Aprimorado"


def carregar_resultados_2026(caminho: Path = RESULTADOS_2026) -> pd.DataFrame:
    dados = pd.read_excel(caminho, sheet_name="resultados")
    dados = dados.rename(columns={"id": "sigla", "nivel_maturidade": "iGovTI_maturidade"})
    obrigatorias = {
        "sigla", "iGovTI", "iGovTI_maturidade", "GovernancaTI", "iGestTI",
        "PlanejamentoTI", "ServicosTI", "RiscosTISegInfo", "EstruturaSegInfo",
        "ProcessoSegInfo", "GerirSoluçõesTI",
    }
    faltantes = obrigatorias - set(dados.columns)
    if faltantes:
        raise ValueError(f"Colunas ausentes em {caminho}: {sorted(faltantes)}")
    if dados["sigla"].isna().any() or dados["sigla"].duplicated().any():
        repetidas = dados.loc[dados["sigla"].duplicated(False), "sigla"].astype(str).tolist()
        raise ValueError(f"A base oficial de 2026 deve conter uma linha unica por sigla. Duplicadas: {repetidas}")
    dados["_key"] = dados["sigla"].map(normalizar_sigla)
    if dados["_key"].duplicated().any():
        repetidas = dados.loc[dados["_key"].duplicated(False), "sigla"].astype(str).tolist()
        raise ValueError(f"Siglas colidem apos normalizacao: {repetidas}")
    return dados


def carregar_comparavel(caminho: Path) -> pd.DataFrame:
    dados = pd.read_excel(caminho, sheet_name="resultados")
    obrigatorias = {"id", "nivel_maturidade", *INDICADORES_COMPARAVEIS}
    faltantes = obrigatorias - set(dados.columns)
    if faltantes:
        raise ValueError(f"Colunas ausentes em {caminho}: {sorted(faltantes)}")
    if dados["id"].isna().any() or dados["id"].duplicated().any():
        repetidas = dados.loc[dados["id"].duplicated(False), "id"].astype(str).tolist()
        raise ValueError(f"A base comparavel deve conter uma linha unica por organizacao. Duplicadas: {repetidas}")
    dados["_key"] = dados["id"].map(normalizar_sigla)
    return dados


def consolidar_pareamentos(
    caminho_2026: Path = COMPARAVEL_2026,
    caminho_setic_2023: Path = COMPARAVEL_2023_SETIC,
    caminho_municipios_2023: Path = COMPARAVEL_2023_MUNICIPIOS,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    atual = carregar_comparavel(caminho_2026)
    antigos = pd.concat(
        [
            carregar_comparavel(caminho_setic_2023).assign(grupo="Estaduais"),
            carregar_comparavel(caminho_municipios_2023).assign(grupo="Municípios"),
        ],
        ignore_index=True,
    )
    por_chave_2026 = atual.set_index("_key", drop=False)
    linhas = []
    usados_2026: set[str] = set()

    for _, antigo in antigos.iterrows():
        chave_2023 = antigo["_key"]
        if chave_2023 in por_chave_2026.index:
            chave_2026 = chave_2023
            tipo = "normalizado"
        else:
            chave_2026 = ALIASES_2023_2026.get(chave_2023)
            tipo = "alias validado" if chave_2026 in por_chave_2026.index else "sem correspondência"

        registro = {
            "grupo": antigo["grupo"],
            "sigla_2023": antigo["id"],
            "chave_2023": chave_2023,
            "sigla_2026": None,
            "chave_2026": chave_2026,
            "tipo_pareamento": tipo,
            "pareado": tipo != "sem correspondência",
        }
        if registro["pareado"]:
            if chave_2026 in usados_2026:
                raise ValueError(f"Mais de uma organizacao de 2023 foi associada a {chave_2026}.")
            usados_2026.add(chave_2026)
            novo = por_chave_2026.loc[chave_2026]
            registro["sigla_2026"] = novo["id"]
            registro["nivel_maturidade_2023"] = antigo["nivel_maturidade"]
            registro["nivel_maturidade_2026"] = novo["nivel_maturidade"]
            for indicador in INDICADORES_COMPARAVEIS:
                valor_2023 = float(antigo[indicador])
                valor_2026 = float(novo[indicador])
                registro[f"{indicador}_2023"] = valor_2023
                registro[f"{indicador}_2026"] = valor_2026
                registro[f"delta_{indicador}"] = valor_2026 - valor_2023
        linhas.append(registro)

    pareamentos = pd.DataFrame(linhas)
    pareados = pareamentos.loc[pareamentos["pareado"]].copy()
    nao_pareados_2026 = atual.loc[~atual["_key"].isin(usados_2026), ["id", "_key"]].copy()
    nao_pareados_2026 = nao_pareados_2026.rename(columns={"id": "sigla_2026", "_key": "chave_2026"})
    return pareamentos, pareados, nao_pareados_2026


def estatisticas_serie(serie: pd.Series) -> dict[str, float | int]:
    valores = pd.to_numeric(serie, errors="raise")
    return {
        "media": float(valores.mean()),
        "q1": float(valores.quantile(0.25)),
        "mediana": float(valores.median()),
        "q3": float(valores.quantile(0.75)),
        "minimo": float(valores.min()),
        "maximo": float(valores.max()),
        "zeros_n": int(np.isclose(valores, 0.0).sum()),
        "abaixo_040_n": int((valores < 0.40).sum()),
        "a_partir_040_n": int((valores >= 0.40).sum()),
    }


def direcao_variacao(delta: float, tolerancia: float = 1e-12) -> str:
    if delta > tolerancia:
        return "avanço"
    if delta < -tolerancia:
        return "regressão"
    return "estabilidade"


def formatar_lista_variacoes(registro: pd.Series, positivas: bool, limite: int = 3) -> str:
    variacoes = [
        (float(registro[f"delta_{campo}"]), rotulo)
        for campo, rotulo in AGREGADOS_COMPARAVEIS.items()
    ]
    if positivas:
        selecionadas = sorted((item for item in variacoes if item[0] > 1e-12), reverse=True)[:limite]
    else:
        selecionadas = sorted(item for item in variacoes if item[0] < -1e-12)[:limite]
    return "; ".join(f"{rotulo} ({delta:+.4f})" for delta, rotulo in selecionadas)
