#!/usr/bin/env python3
"""Calculadora iGovTI em Python.

Replica a lógica do front-end ``scripts/calcula-igovti.html`` para permitir
a regeneração dos resultados do índice a partir de uma nova planilha de
respostas via linha de comando.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import yaml


class ErroCalculadoraIgovti(Exception):
    """Erro controlado durante o cálculo do iGovTI."""


# --------------------------------------------------------------------------- #
# Normalização de identificadores
# --------------------------------------------------------------------------- #


def normalizar_coluna(nome: str) -> str:
    """Remove pontos e espaços extras dos nomes de coluna."""
    return str(nome).replace(".", "").strip()


def eh_coluna_questao(nome: str) -> bool:
    """Colunas que representam questões contêm 4 dígitos e não são metadados."""
    nome_limpo = normalizar_coluna(nome)
    return bool(re.search(r"\d{4}", nome_limpo)) and not bool(
        re.search(r"lei|est|evi|nsa|raz|SQ", nome_limpo, re.IGNORECASE)
    )


def normalizar_id_questao(nome: str) -> str:
    """Garante que o identificador comece com 'q' minúsculo."""
    limpo = str(nome).strip()
    if limpo.lower().startswith("q"):
        return f"q{limpo[1:]}"
    return f"q{limpo}"


def aliases_id_questao(question_id: str) -> list[str]:
    """Gera aliases equivalentes para identificadores de detalhamento."""
    value = normalizar_id_questao(question_id)
    aliases = [value]

    ext_match = re.match(r"^q(\d{4})ext\[([^\]]+)\]$", value, re.IGNORECASE)
    if ext_match:
        aliases.append(f"q{ext_match.group(1)}{ext_match.group(2)}")

    bracket_match = re.match(r"^q(\d{4})\[([^\]]+)\]$", value, re.IGNORECASE)
    if bracket_match:
        aliases.append(f"q{bracket_match.group(1)}{bracket_match.group(2)}")

    compact_match = re.match(r"^q(\d{4})([A-Za-z])$", value)
    if compact_match:
        aliases.append(f"q{compact_match.group(1)}[{compact_match.group(2)}]")
        aliases.append(f"q{compact_match.group(1)}ext[{compact_match.group(2)}]")

    return list(dict.fromkeys(aliases))


# --------------------------------------------------------------------------- #
# Referências com seleção de itens (ex: q2201{A,B,C})
# --------------------------------------------------------------------------- #


def parse_referencia_questao(valor: str) -> dict[str, Any]:
    """Interpreta referências como ``q2201{A,B,C}`` ou ``q1003ext[A]``."""
    referencia = str(valor or "").strip()
    if "{" not in referencia and "[" not in referencia:
        return {
            "referencia": referencia,
            "questao_id": referencia,
            "codigos": None,
            "erro": None,
        }

    match = re.match(r"^(q\d{4})\s*\{([^{}]*)\}$", referencia, re.IGNORECASE)
    if not match:
        return {
            "referencia": referencia,
            "questao_id": None,
            "codigos": None,
            "erro": "use o formato qNNNN{A, C, D}",
        }

    codigos = [c.strip() for c in match.group(2).split(",") if c.strip()]
    if not codigos:
        return {
            "referencia": referencia,
            "questao_id": f"q{match.group(1)[1:]}",
            "codigos": None,
            "erro": "informe ao menos um item de detalhamento",
        }

    invalido = next((c for c in codigos if not re.match(r"^[A-Za-z0-9_-]+$", c)), None)
    if invalido:
        return {
            "referencia": referencia,
            "questao_id": f"q{match.group(1)[1:]}",
            "codigos": None,
            "erro": f"item de detalhamento inválido \"{invalido}\"",
        }

    return {
        "referencia": referencia,
        "questao_id": normalizar_id_questao(match.group(1)),
        "codigos": codigos,
        "erro": None,
    }


def codigo_detalhe_de_id(questao_id: str, detalhe_id: str) -> str | None:
    """Extrai o código de detalhe de um identificador completo."""
    base = re.escape(str(questao_id))
    valor = str(detalhe_id)
    padroes = [
        re.compile(rf"^{base}ext\[([^\]]+)\]$"),
        re.compile(rf"^{base}\[([^\]]+)\]$"),
        re.compile(rf"^{base}([A-Za-z0-9_-]+)$"),
    ]
    for padrao in padroes:
        match = valor.match(padrao)
        if match:
            return match.group(1)
    return None


def encontrar_id_detalhe(questao_id: str, codigo: str, ids_disponiveis: set[str]) -> str | None:
    """Encontra a coluna de detalhe que corresponde ao código informado."""
    candidatos = [
        f"{questao_id}ext[{codigo}]",
        f"{questao_id}[{codigo}]",
        f"{questao_id}{codigo}",
    ]
    for candidato in candidatos:
        if candidato in ids_disponiveis:
            return candidato
    for detalhe_id in ids_disponiveis:
        if codigo_detalhe_de_id(questao_id, detalhe_id) == codigo:
            return detalhe_id
    return None


# --------------------------------------------------------------------------- #
# Conversão e cálculo de respostas
# --------------------------------------------------------------------------- #


def normalizar_texto_resposta(valor: object) -> str:
    """Remove ponto final de strings de resposta."""
    if valor is None or (isinstance(valor, float) and np.isnan(valor)):
        return ""
    raw = str(valor).strip()
    return raw[:-1] if raw.endswith(".") else raw


def para_numero(valor: object, padrao: float = 0.0) -> float:
    """Converte valor para float, trocando vírgula por ponto."""
    if isinstance(valor, (int, float)) and not (isinstance(valor, float) and np.isnan(valor)):
        return float(valor)
    try:
        numero = float(str(valor).replace(",", "."))
        return numero if np.isfinite(numero) else padrao
    except (ValueError, TypeError):
        return padrao


def normalizar_resposta(valor: object, categorias: dict[str, float]) -> float | str:
    """Mapeia respostas categóricas ou converte para número."""
    if valor is None or (isinstance(valor, float) and np.isnan(valor)) or str(valor).strip() == "":
        return 0
    if isinstance(valor, (int, float)) and not (isinstance(valor, float) and np.isnan(valor)):
        return float(valor)

    raw = str(valor).strip()
    clean = raw[:-1] if raw.endswith(".") else raw
    if raw in categorias:
        return float(categorias[raw])
    if clean in categorias:
        return float(categorias[clean])
    return para_numero(raw, raw)


def calcular_questao(texto_base: str, valor_base: float, detalhes: list[float]) -> float:
    """Aplica desconto proporcional quando há detalhamentos afirmados."""
    base = para_numero(valor_base, 0.0)
    texto = str(texto_base).strip()
    if texto.endswith("."):
        texto = texto[:-1]

    adota_total = texto in {"admai", "Adota em maior parte ou totalmente", "Adota"}
    adota_parcial = texto in {"adpar", "Adota parcialmente"}

    if not detalhes or (not adota_total and not adota_parcial):
        return base

    desconto_maximo = 0.85 if adota_total else 0.35
    faltantes = sum(1.0 - para_numero(v, 0.0) for v in detalhes)
    return float(np.clip(base - ((faltantes * desconto_maximo) / len(detalhes)), 0.0, 1.0))


# --------------------------------------------------------------------------- #
# Configuração e cálculo do índice
# --------------------------------------------------------------------------- #


def carregar_configuracao_yaml(caminho: Path) -> dict[str, Any]:
    """Carrega e valida a estrutura do índice."""
    with open(caminho, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    if not config or not isinstance(config, dict):
        raise ErroCalculadoraIgovti("documento YAML vazio")
    if not config.get("metadata", {}).get("raiz"):
        raise ErroCalculadoraIgovti("metadata.raiz é obrigatório")
    if not config.get("categorias") or not isinstance(config["categorias"], dict):
        raise ErroCalculadoraIgovti("categorias é obrigatório")
    if not isinstance(config.get("niveis_maturidade"), list):
        raise ErroCalculadoraIgovti("niveis_maturidade deve ser uma lista")
    if not config.get("agregados") or not isinstance(config["agregados"], dict):
        raise ErroCalculadoraIgovti("agregados é obrigatório")

    return config


def classificar_maturidade(valor: float, niveis: list[dict[str, Any]]) -> str:
    """Classifica o valor do índice em um nível de maturidade."""
    for nivel in niveis:
        minimo = float(nivel["min"])
        maximo = float(nivel["max"])
        inclui_min = nivel.get("inclui_min", True)
        inclui_max = nivel.get("inclui_max", False)

        min_ok = valor > minimo if inclui_min is False else valor >= minimo
        max_ok = valor <= maximo if inclui_max is True else valor < maximo
        if min_ok and max_ok:
            return str(nivel["nome"])
    return "Sem classificação"


def _componentes_normalizados(spec: dict[str, Any]) -> list[dict[str, Any]]:
    """Extrai a lista de componentes de um agregado."""
    return [
        {"id": str(c["id"]).strip(), "peso": float(c["peso"])}
        for c in spec.get("componentes", [])
    ]


def _coletar_seletores_configurados(config: dict[str, Any]) -> list[dict[str, Any]]:
    """Retorna os seletores de detalhes declarados nos agregados."""
    seletores = {}
    for spec in config.get("agregados", {}).values():
        for componente in spec.get("componentes", []):
            parse = parse_referencia_questao(componente["id"])
            if parse["codigos"] and not parse["erro"]:
                seletores[parse["referencia"]] = parse
    return list(seletores.values())


def processar_respostas(
    df: pd.DataFrame,
    config: dict[str, Any],
    coluna_id: str | None = None,
) -> tuple[list[dict[str, Any]], str | None]:
    """Processa a planilha de respostas e retorna as linhas calculáveis."""
    if df.empty:
        return [], None

    colunas = [str(c) for c in df.columns]
    coluna_id = coluna_id or _escolher_coluna_id(colunas)

    categorias = config["categorias"]
    seletores = _coletar_seletores_configurados(config)

    linhas = []
    for idx, row in df.iterrows():
        normalizado: dict[str, float] = {}
        respostas_texto: dict[str, str] = {}

        for nome_coluna in colunas:
            nome_limpo = normalizar_coluna(nome_coluna)
            if not eh_coluna_questao(nome_limpo):
                continue
            qid = normalizar_id_questao(nome_limpo)
            normalizado[qid] = normalizar_resposta(row[nome_coluna], categorias)
            respostas_texto[qid] = normalizar_texto_resposta(row[nome_coluna])

        scores: dict[str, float] = {qid: para_numero(v, 0.0) for qid, v in normalizado.items()}

        # Questões base com todos os detalhamentos disponíveis
        questoes_base = [qid for qid in normalizado if re.match(r"^q\d{4}$", qid, re.IGNORECASE)]
        for base in questoes_base:
            detalhes = [normalizado[c] for c in normalizado if c != base and c.startswith(base)]
            scores[base] = calcular_questao(respostas_texto[base], normalizado[base], detalhes)

        # Seletores configurados nos agregados
        for seletor in seletores:
            qid_base = seletor["questao_id"]
            if qid_base not in normalizado:
                continue
            ids_detalhes_disponiveis = {c for c in normalizado if c != qid_base and c.startswith(qid_base)}
            ids_selecionados = [
                encontrar_id_detalhe(qid_base, codigo, ids_detalhes_disponiveis)
                for codigo in seletor["codigos"]
            ]
            if any(d is None for d in ids_selecionados):
                continue
            scores[seletor["referencia"]] = calcular_questao(
                respostas_texto[qid_base],
                normalizado[qid_base],
                [normalizado[d] for d in ids_selecionados],  # type: ignore[arg-type]
            )

        # Aliases para compatibilidade
        for qid, valor in normalizado.items():
            for alias in aliases_id_questao(qid):
                if alias not in scores:
                    scores[alias] = para_numero(valor, 0.0)

        identificador = str(row[coluna_id]) if coluna_id and coluna_id in row else f"Registro {idx + 1}"
        linhas.append(
            {
                "_id": identificador,
                "_raw": row.to_dict(),
                "_scores": scores,
            }
        )

    return linhas, coluna_id


def _escolher_coluna_id(colunas: list[str], coluna_solicitada: str = "") -> str | None:
    """Escolhe a coluna identificadora mais adequada."""
    disponiveis = [str(c) for c in colunas]
    if coluna_solicitada and coluna_solicitada in disponiveis:
        return coluna_solicitada

    candidatos = ["firstname", "attribute_1", "orgao", "órgão", "entidade", "auditado", "name", "id"]
    lower = {c.lower(): c for c in disponiveis}
    for candidato in candidatos:
        if candidato.lower() in lower:
            return lower[candidato.lower()]
    return disponiveis[0] if disponiveis else None


def calcular_indices(
    linhas: list[dict[str, Any]],
    config: dict[str, Any],
) -> list[dict[str, Any]]:
    """Calcula os agregados para cada linha processada."""
    raiz = config["metadata"]["raiz"]
    agregados = config["agregados"]
    niveis = config["niveis_maturidade"]

    resultados = []
    for linha in linhas:
        valores = dict(linha["_scores"])
        memoria: dict[str, list[dict[str, Any]]] = {}
        visitando: set[str] = set()

        def visitar(no_id: str) -> float:
            if no_id.startswith("q"):
                return para_numero(valores.get(no_id, 0.0), 0.0)
            if no_id in valores:
                return float(valores[no_id])
            if no_id in visitando:
                raise ErroCalculadoraIgovti(f"ciclo detectado em {no_id}")
            spec = agregados.get(no_id)
            if spec is None:
                return 0.0

            visitando.add(no_id)
            partes = []
            for comp in _componentes_normalizados(spec):
                valor_componente = visitar(comp["id"])
                partes.append(
                    {
                        "id": comp["id"],
                        "peso": comp["peso"],
                        "valor": valor_componente,
                        "contribuicao": valor_componente * comp["peso"],
                    }
                )
            visitando.discard(no_id)

            total = sum(p["contribuicao"] for p in partes)
            valores[no_id] = float(np.clip(total, 0.0, 1.0))
            memoria[no_id] = partes
            return valores[no_id]

        visitar(raiz)
        for agregado_id in agregados:
            visitar(agregado_id)

        resultados.append(
            {
                "id": linha["_id"],
                "indice": raiz,
                "valor": valores[raiz],
                "nivel_maturidade": classificar_maturidade(valores[raiz], niveis),
                "valores": valores,
                "memoria": memoria,
                "raw": linha["_raw"],
            }
        )

    return resultados


# --------------------------------------------------------------------------- #
# Exportação
# --------------------------------------------------------------------------- #


def exportar_resultados_xlsx(
    resultados: list[dict[str, Any]],
    config: dict[str, Any],
    caminho_saida: Path,
    mapeamento_id: dict[str, str] | None = None,
) -> None:
    """Exporta os resultados no mesmo formato do ``calcula-igovti.html``."""
    raiz = config["metadata"]["raiz"]
    ids_agregados = [a for a in config["agregados"] if a != raiz]
    colunas = ["id", raiz, "nivel_maturidade", *ids_agregados]

    linhas = []
    for resultado in resultados:
        identificador = resultado["id"]
        if mapeamento_id and identificador in mapeamento_id:
            identificador = mapeamento_id[identificador]
        linha = {"id": identificador}
        for col in colunas[1:]:
            if col == "nivel_maturidade":
                linha[col] = resultado["nivel_maturidade"]
            elif col == raiz:
                linha[col] = resultado["valor"]
            else:
                linha[col] = resultado["valores"].get(col)
        linhas.append(linha)

    df = pd.DataFrame(linhas, columns=colunas)
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(caminho_saida, sheet_name="resultados", index=False)


def calcular_igovti(
    caminho_respostas: Path,
    caminho_yaml: Path,
    caminho_saida: Path,
    coluna_id: str | None = None,
    mapeamento_id: dict[str, str] | None = None,
) -> pd.DataFrame:
    """Executa o pipeline completo de cálculo e exportação."""
    config = carregar_configuracao_yaml(caminho_yaml)
    df = pd.read_excel(caminho_respostas)
    linhas, coluna_id_usada = processar_respostas(df, config, coluna_id=coluna_id)
    resultados = calcular_indices(linhas, config)
    exportar_resultados_xlsx(resultados, config, caminho_saida, mapeamento_id)
    return pd.DataFrame(
        [{"id": r["id"], "indice": r["indice"], "valor": r["valor"], "nivel_maturidade": r["nivel_maturidade"]} for r in resultados]
    )
