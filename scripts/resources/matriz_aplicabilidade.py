"""Leitura da camada jurídica declarada na matriz de planejamento."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

try:
    from .aplicabilidade_juridica import (
        CriterioAuditoria,
        ErroAplicabilidade,
        ResolverAplicabilidade,
        SeletorAplicabilidade,
        VarianteEncaminhamento,
    )
except ImportError:  # execução por scripts que adicionam resources ao sys.path
    from aplicabilidade_juridica import (  # type: ignore
        CriterioAuditoria,
        ErroAplicabilidade,
        ResolverAplicabilidade,
        SeletorAplicabilidade,
        VarianteEncaminhamento,
    )


@dataclass(frozen=True)
class CatalogoAplicabilidadeMatriz:
    criterios: tuple[CriterioAuditoria, ...]
    variantes: tuple[VarianteEncaminhamento, ...]

    def criar_resolvedor(self) -> ResolverAplicabilidade:
        return ResolverAplicabilidade(self.criterios, self.variantes)


def _qualificar(qid: str, criterio: object) -> str:
    codigo = str(criterio or "").strip().upper()
    if not codigo:
        raise ErroAplicabilidade(f"{qid}: identificador de critério vazio.")
    return codigo if "." in codigo else f"{qid}.{codigo}"


def carregar_catalogo_matriz(caminho: str | Path) -> CatalogoAplicabilidadeMatriz:
    # Importação local evita acoplar o resolvedor à geração DOCX.
    try:
        from scripts.gerar_matriz_planejamento import materialize_situation_variant, parse_matrix
    except ImportError:
        from gerar_matriz_planejamento import materialize_situation_variant, parse_matrix  # type: ignore

    matriz = parse_matrix(Path(caminho).read_text(encoding="utf-8"))

    criterios: list[CriterioAuditoria] = []
    variantes: list[VarianteEncaminhamento] = []
    for questao in matriz.questions:
        if not questao.gera_achado:
            continue
        for item in questao.criterios:
            cid = _qualificar(questao.id, item.id)
            seletor = SeletorAplicabilidade.from_mapping(item.aplica_se)
            criterios.append(
                CriterioAuditoria(
                    id=cid,
                    descricao=item.descricao,
                    natureza_fundamento=item.natureza_fundamento,
                    apto_a_fundamentar_determinacao=item.apto_a_fundamentar_determinacao,
                    seletor=seletor,
                    rotulo_publico=item.publico,
                )
            )

        for achado in questao.achados:
            for situacao in achado.situacoes:
                variantes.append(
                    VarianteEncaminhamento(
                        id=f"{situacao.id}.GERAL",
                        id_situacao=situacao.id,
                        geral=True,
                        criterios=tuple(_qualificar(questao.id, cid) for cid in situacao.criterios),
                        tipo_encaminhamento=situacao.tipo_encaminhamento,
                        encaminhamento=situacao.encaminhamento,
                        rotulo_publico="Geral",
                    )
                )
                for item in situacao.variantes:
                    identifier, criteria_ids, referral_type, referral = materialize_situation_variant(
                        situacao, item
                    )
                    variantes.append(
                        VarianteEncaminhamento(
                            id=identifier,
                            id_situacao=situacao.id,
                            geral=False,
                            criterios=tuple(_qualificar(questao.id, cid) for cid in criteria_ids),
                            tipo_encaminhamento=referral_type,
                            encaminhamento=referral,
                            seletor=SeletorAplicabilidade.from_mapping(item.aplica_se),
                            rotulo_publico=item.publico,
                        )
                    )

    catalogo = CatalogoAplicabilidadeMatriz(tuple(criterios), tuple(variantes))
    catalogo.criar_resolvedor()
    return catalogo
