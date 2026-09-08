#!/usr/bin/env python3
"""Gera o papel de trabalho da Questão Transversal - Diagnóstico do iGovTI 2026."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent / "resources"))

from igovti_calculadora import calcular_indices, carregar_configuracao_yaml, processar_respostas


DIMENSOES = {
    "PlanejamentoTI": "Planejamento de TIC",
    "ServicosTI": "Gestão de serviços de TIC",
    "RiscosTISegInfo": "Riscos de TI e segurança da informação",
    "EstruturaSegInfo": "Estrutura de segurança da informação",
    "ProcessoSegInfo": "Processos de segurança da informação",
    "GerirSoluçõesTI": "Gestão de soluções de TIC",
}
INDICADORES = {"iGovTI": "iGovTI", "GovernancaTI": "Governança de TIC", "iGestTI": "Gestão de TIC", **DIMENSOES}
PRATICAS = [
    "q1001", "q1002", "q1003", "q1004", "q2101", "q2102", "q2201", "q2202", "q2203", "q2204",
    "q2301", "q2302", "q2303", "q2401", "q2402", "q2403", "_q4251(TCU)", "q2503", "q2504", "q2601", "q2602",
]
ROTULOS_PRATICAS_GOVERNANCA = {
    "q1001": "Modelo de gestão de TIC",
    "q1002": "Monitoramento do desempenho da gestão de TIC",
    "q1003": "Atuação da auditoria interna em apoio à governança de TIC",
    "q1004": "Simplificação dos serviços públicos",
}


def extrair_rotulos_questionario(path: Path) -> dict[str, str]:
    texto = path.read_text(encoding="utf-8")
    rotulos: dict[str, str] = {}
    blocos = re.split(r"(?=^### q\d{4}\s)", texto, flags=re.MULTILINE)
    for bloco in blocos:
        id_match = re.match(r"### (q\d{4})\s", bloco)
        pergunta = re.search(r"^question:\s*\*\*(.+?)\*\*\s*$", bloco, flags=re.MULTILINE)
        if id_match and pergunta:
            rotulos[id_match.group(1)] = pergunta.group(1).strip()
    rotulos["_q4251(TCU)"] = (
        "2501/2502. Gestão de ativos associados à informação e controle de acesso, "
        "conforme composição prevista na metodologia."
    )
    return rotulos


def classificar_esfera(valor: object) -> str:
    return {"E": "Organizações estaduais", "M": "Municípios"}.get(str(valor).strip().upper(), str(valor))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--respostas", type=Path, required=True)
    parser.add_argument("--resultados", type=Path, required=True)
    parser.add_argument("--auditados", type=Path, required=True)
    parser.add_argument("--metodologia", type=Path, default=ROOT / "01-Planejamento/02-Metodologia_iGovTI/estrutura-igovti-2026.yaml")
    parser.add_argument("--questionario", type=Path, default=ROOT / "01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md")
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-xlsx", type=Path, required=True)
    args = parser.parse_args()

    config = carregar_configuracao_yaml(args.metodologia)
    respostas = pd.read_excel(args.respostas)
    resultados = pd.read_excel(args.resultados, sheet_name="resultados")
    auditados = pd.read_excel(args.auditados)
    linhas, _ = processar_respostas(respostas, config, coluna_id="firstname")
    calculados = calcular_indices(linhas, config)
    valores = pd.DataFrame([{"sigla": item["id"], **item["valores"]} for item in calculados])

    base = resultados.rename(columns={"id": "sigla"}).merge(auditados[["sigla", "esfera"]], on="sigla", how="left", validate="one_to_one")
    if base["esfera"].isna().any():
        faltantes = base.loc[base["esfera"].isna(), "sigla"].tolist()
        raise ValueError(f"Organizações sem esfera no cadastro: {faltantes}")
    if len(base) != len(valores):
        raise ValueError("A base de resultados e a memória de cálculo não têm o mesmo universo.")

    segmentos = []
    linhas_segmentos = []
    for esfera, grupo in base.groupby("esfera", sort=True):
        item = {"segmento": classificar_esfera(esfera), "n": int(len(grupo))}
        for coluna, rotulo in INDICADORES.items():
            media = float(grupo[coluna].mean())
            mediana = float(grupo[coluna].median())
            item[f"{coluna}_media"] = media
            item[f"{coluna}_mediana"] = mediana
            linhas_segmentos.append({"segmento": item["segmento"], "n": item["n"], "indicador": rotulo, "media": media, "mediana": mediana})
        segmentos.append(item)

    rotulos = extrair_rotulos_questionario(args.questionario)
    respostas_por_sigla = respostas.set_index("firstname")
    valores_por_sigla = valores.set_index("sigla")
    ranking = []
    for pratica in PRATICAS:
        serie = pd.to_numeric(valores_por_sigla[pratica], errors="coerce")
        if pratica == "_q4251(TCU)":
            bases_na = respostas_por_sigla[["q2501", "q2502"]].apply(
                lambda coluna: coluna.astype(str).str.rstrip(".").eq("Não se aplica")
            )
            n_na = int(bases_na.any(axis=1).sum())
        else:
            n_na = int(respostas_por_sigla[pratica].astype(str).str.rstrip(".").eq("Não se aplica").sum())
        ranking.append({
            "id": pratica,
            "descricao": rotulos.get(pratica, pratica),
            "media": float(serie.mean()),
            "mediana": float(serie.median()),
            "respostas_validas": int(serie.notna().sum()),
            "nao_aplicavel": n_na,
        })
    ranking = sorted(ranking, key=lambda item: (item["media"], item["id"]))
    menores = ranking[:5]
    maiores = list(reversed(ranking[-5:]))

    pesos_governanca = {
        item["id"]: float(item["peso"])
        for item in config["agregados"]["GovernancaTI"]["componentes"]
    }
    praticas_governanca = []
    for pratica, rotulo in ROTULOS_PRATICAS_GOVERNANCA.items():
        serie = pd.to_numeric(valores_por_sigla[pratica], errors="coerce")
        praticas_governanca.append({
            "id": pratica,
            "descricao": rotulo,
            "peso": pesos_governanca[pratica],
            "media": float(serie.mean()),
            "mediana": float(serie.median()),
            "minimo": float(serie.min()),
            "maximo": float(serie.max()),
            "zeros_n": int(serie.eq(0).sum()),
            "zeros_pct": float(serie.eq(0).mean() * 100),
            "abaixo_040_n": int(serie.lt(0.40).sum()),
            "abaixo_040_pct": float(serie.lt(0.40).mean() * 100),
        })

    maturidade = (
        base["nivel_maturidade"].value_counts().rename_axis("nivel").reset_index(name="quantidade")
    )
    maturidade["percentual"] = maturidade["quantidade"] / len(base) * 100
    resumo = {
        "diagnostico_universo_n": int(len(base)),
        "diagnostico_igovti_media": float(base["iGovTI"].mean()),
        "diagnostico_igovti_mediana": float(base["iGovTI"].median()),
        "diagnostico_segmentos": segmentos,
        "diagnostico_praticas_governanca": praticas_governanca,
        "diagnostico_praticas_menor_adocao": menores,
        "diagnostico_praticas_maior_adocao": maiores,
        "diagnostico_nao_aplicavel_tratamento": "As respostas 'Não se aplica' recebem pontuação parcial (0,5), conforme a metodologia oficial.",
        "diagnostico_limitacoes": (
            "A comparação por segmento é descritiva e restrita à esfera estadual ou municipal, único atributo institucional disponível no cadastro. "
            "O índice mede adoção declarada, após os ajustes aplicáveis, e não comprova isoladamente efetividade ou conformidade jurídica."
        ),
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_xlsx.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(resumo, ensure_ascii=False, indent=2), encoding="utf-8")
    with pd.ExcelWriter(args.output_xlsx, engine="openpyxl") as writer:
        base[["sigla", "esfera", *INDICADORES]].to_excel(writer, sheet_name="Universo e índices", index=False)
        maturidade.to_excel(writer, sheet_name="Faixas de maturidade", index=False)
        pd.DataFrame(linhas_segmentos).to_excel(writer, sheet_name="Segmentos", index=False)
        pd.DataFrame(praticas_governanca).to_excel(writer, sheet_name="Governança de TIC", index=False)
        pd.DataFrame(ranking).to_excel(writer, sheet_name="Práticas", index=False)
        pd.DataFrame([
            {"verificacao": "Universo", "resultado": f"{len(base)} respostas válidas e índices calculados"},
            {"verificacao": "Completude do segmento", "resultado": "Sem valores ausentes"},
            {"verificacao": "Tratamento de N/A", "resultado": resumo["diagnostico_nao_aplicavel_tratamento"]},
            {"verificacao": "Limitações", "resultado": resumo["diagnostico_limitacoes"]},
        ]).to_excel(writer, sheet_name="Validações e limitações", index=False)
    print(f"Diagnóstico JSON: {args.output_json}")
    print(f"Papel de trabalho XLSX: {args.output_xlsx}")


if __name__ == "__main__":
    main()
