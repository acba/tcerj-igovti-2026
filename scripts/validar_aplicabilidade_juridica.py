#!/usr/bin/env python3
"""Valida Matriz × Mapa × cadastro e resolve a cobertura por auditado."""

from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
for path in (ROOT / "scripts", ROOT / "scripts/resources"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from aplicabilidade_juridica import PerfilAuditado, carregar_catalogo_planilha  # noqa: E402
from matriz_aplicabilidade import carregar_catalogo_matriz  # noqa: E402


DEFAULT_MATRIZ = ROOT / "01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/matriz_planejamento-pos-comentarios-gestor.md"
DEFAULT_MAPA = ROOT / "02-Execucao/03-Execucao_Procedimentos/01-Insumos/mapa-verificacao-achados-pos-comentarios-gestor.xlsx"
DEFAULT_AUDITADOS = ROOT / "02-Execucao/03-Execucao_Procedimentos/01-Insumos/bd_auditados.xlsx"


def _normalizar_catalogo(criterios, variantes):
    return {
        "criterios": {item.id: asdict(item) for item in criterios},
        "variantes": {item.id: asdict(item) for item in variantes},
    }


def validar_consistencia(matriz: Path, mapa: Path, auditados: Path) -> pd.DataFrame:
    catalogo_matriz = carregar_catalogo_matriz(matriz)
    resolvedor_mapa = carregar_catalogo_planilha(str(mapa))
    variantes_mapa = [
        variante
        for variantes in resolvedor_mapa.variantes_por_situacao.values()
        for variante in variantes
    ]
    esperado = _normalizar_catalogo(catalogo_matriz.criterios, catalogo_matriz.variantes)
    encontrado = _normalizar_catalogo(list(resolvedor_mapa.criterios.values()), variantes_mapa)
    if esperado != encontrado:
        ids_criterios = sorted(set(esperado["criterios"]) ^ set(encontrado["criterios"]))
        ids_variantes = sorted(set(esperado["variantes"]) ^ set(encontrado["variantes"]))
        detalhe = []
        if ids_criterios:
            detalhe.append("critérios: " + ", ".join(ids_criterios))
        if ids_variantes:
            detalhe.append("variantes: " + ", ".join(ids_variantes))
        if not detalhe:
            detalhe.append("há divergência de conteúdo em critérios ou variantes de mesmo identificador")
        raise ValueError("Matriz e mapa não estão sincronizados: " + "; ".join(detalhe) + ".")

    acoes = pd.read_excel(
        mapa,
        sheet_name="Ações de Verificação",
        skiprows=2,
        keep_default_na=False,
    )
    colunas_acoes = {"id", "id_situacao", "descricao_situacao_inconforme"}
    faltantes_acoes = sorted(colunas_acoes - set(acoes.columns))
    if faltantes_acoes:
        raise ValueError(
            "Aba Ações de Verificação sem colunas de rastreabilidade: "
            + ", ".join(faltantes_acoes)
            + "."
        )
    ids_situacoes_matriz = set(catalogo_matriz.criar_resolvedor().variantes_por_situacao)
    ids_situacoes_mapa = {
        str(valor).strip() for valor in acoes["id_situacao"] if str(valor).strip()
    }
    ids_invalidos = sorted(ids_situacoes_mapa - ids_situacoes_matriz)
    ids_sem_acao = sorted(ids_situacoes_matriz - ids_situacoes_mapa)
    acoes_sem_situacao = sorted(
        str(row["id"]).strip()
        for _, row in acoes.iterrows()
        if str(row["descricao_situacao_inconforme"]).strip()
        and not str(row["id_situacao"]).strip()
    )
    descricoes_com_multiplos_ids = {}
    for descricao_bruta, grupo in acoes.groupby("descricao_situacao_inconforme", dropna=False):
        descricao = str(descricao_bruta).strip()
        ids = {str(valor).strip() for valor in grupo["id_situacao"] if str(valor).strip()}
        if descricao and len(ids) > 1:
            descricoes_com_multiplos_ids[descricao] = sorted(ids)
    erros_acoes = []
    if ids_invalidos:
        erros_acoes.append("identificadores inexistentes: " + ", ".join(ids_invalidos))
    if ids_sem_acao:
        erros_acoes.append("situações sem ação associada: " + ", ".join(ids_sem_acao))
    if acoes_sem_situacao:
        erros_acoes.append("ações sem id_situacao: " + ", ".join(acoes_sem_situacao))
    if descricoes_com_multiplos_ids:
        erros_acoes.append(
            "descrições associadas a mais de um identificador: "
            + "; ".join(
                f"{descricao} ({', '.join(ids)})"
                for descricao, ids in descricoes_com_multiplos_ids.items()
            )
        )
    if erros_acoes:
        raise ValueError("Inconsistência nas ações de verificação: " + "; ".join(erros_acoes) + ".")

    df = pd.read_excel(auditados, sheet_name="auditados", keep_default_na=False)
    obrigatorias = {
        "sigla", "segmento_institucional", "natureza_administrativa", "tags_aplicabilidade"
    }
    faltantes = sorted(obrigatorias - set(df.columns))
    if faltantes:
        raise ValueError("Cadastro sem colunas de aplicabilidade: " + ", ".join(faltantes) + ".")
    registros = []
    ids_situacoes = sorted(resolvedor_mapa.variantes_por_situacao)
    for _, row in df.iterrows():
        perfil = PerfilAuditado.from_mapping(row.to_dict())
        if not perfil.sigla:
            continue
        if not perfil.segmento_institucional:
            raise ValueError(f"{perfil.sigla}: segmento_institucional não informado.")
        if not perfil.natureza_administrativa:
            raise ValueError(f"{perfil.sigla}: natureza_administrativa não informada.")
        for id_situacao in ids_situacoes:
            resolvida = resolvedor_mapa.resolver(perfil, id_situacao)
            registros.append(
                {
                    "auditado": perfil.sigla,
                    "segmento_institucional": perfil.segmento_institucional,
                    "natureza_administrativa": perfil.natureza_administrativa,
                    "tags_aplicabilidade": ";".join(sorted(perfil.tags_aplicabilidade)),
                    "id_situacao": id_situacao,
                    "id_variante": resolvida.variante.id,
                    "publico": resolvida.variante.rotulo_publico,
                    "tipo_encaminhamento": resolvida.variante.tipo_encaminhamento,
                    "criterios": ";".join(criterio.id for criterio in resolvida.criterios),
                }
            )
    return pd.DataFrame(registros)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matriz", type=Path, default=DEFAULT_MATRIZ)
    parser.add_argument("--mapa", type=Path, default=DEFAULT_MAPA)
    parser.add_argument("--auditados", type=Path, default=DEFAULT_AUDITADOS)
    parser.add_argument("--relatorio-xlsx", type=Path)
    args = parser.parse_args()
    cobertura = validar_consistencia(args.matriz, args.mapa, args.auditados)
    if args.relatorio_xlsx:
        args.relatorio_xlsx.parent.mkdir(parents=True, exist_ok=True)
        cobertura.to_excel(args.relatorio_xlsx, index=False)
        print(args.relatorio_xlsx)
    print(f"Validação concluída: {len(cobertura)} combinações auditado/situação.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
