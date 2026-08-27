"""Resolução explícita de critérios e encaminhamentos por público auditado.

O módulo não infere o tipo do encaminhamento. A matriz declara as variantes e
seus seletores; o resolvedor limita-se a escolher a única variante aplicável.
Campos ausentes ou listas vazias no seletor não restringem o público.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Iterable, Mapping, Sequence


def _normalizar_codigo(valor: object) -> str:
    return str(valor or "").strip().upper()


def _normalizar_lista(valores: object) -> tuple[str, ...]:
    if valores is None:
        return ()
    if isinstance(valores, str):
        partes = re.split(r"[,;\n]+", valores)
    elif isinstance(valores, Iterable):
        partes = list(valores)
    else:
        partes = [valores]
    return tuple(dict.fromkeys(codigo for item in partes if (codigo := _normalizar_codigo(item))))


@dataclass(frozen=True)
class PerfilAuditado:
    sigla: str
    segmento_institucional: str
    natureza_administrativa: str = ""
    tags_aplicabilidade: frozenset[str] = field(default_factory=frozenset)

    @classmethod
    def from_mapping(cls, dados: Mapping[str, object]) -> "PerfilAuditado":
        return cls(
            sigla=_normalizar_codigo(dados.get("sigla")),
            segmento_institucional=_normalizar_codigo(dados.get("segmento_institucional")),
            natureza_administrativa=_normalizar_codigo(dados.get("natureza_administrativa")),
            tags_aplicabilidade=frozenset(_normalizar_lista(dados.get("tags_aplicabilidade"))),
        )


@dataclass(frozen=True)
class SeletorAplicabilidade:
    segmentos: tuple[str, ...] = ()
    naturezas: tuple[str, ...] = ()
    tags_todas: tuple[str, ...] = ()
    tags_alguma: tuple[str, ...] = ()
    tags_excluidas: tuple[str, ...] = ()

    @classmethod
    def from_mapping(cls, dados: Mapping[str, object] | None) -> "SeletorAplicabilidade":
        dados = dados or {}
        return cls(
            segmentos=_normalizar_lista(dados.get("segmentos")),
            naturezas=_normalizar_lista(dados.get("naturezas")),
            tags_todas=_normalizar_lista(dados.get("tags_todas")),
            tags_alguma=_normalizar_lista(dados.get("tags_alguma")),
            tags_excluidas=_normalizar_lista(dados.get("tags_excluidas")),
        )

    @property
    def vazio(self) -> bool:
        return not any((self.segmentos, self.naturezas, self.tags_todas, self.tags_alguma, self.tags_excluidas))

    def corresponde(self, perfil: PerfilAuditado) -> bool:
        """Aplica OR dentro de cada lista e AND entre dimensões preenchidas."""
        if self.segmentos and perfil.segmento_institucional not in self.segmentos:
            return False
        if self.naturezas and perfil.natureza_administrativa not in self.naturezas:
            return False
        if self.tags_todas and not set(self.tags_todas).issubset(perfil.tags_aplicabilidade):
            return False
        if self.tags_alguma and perfil.tags_aplicabilidade.isdisjoint(self.tags_alguma):
            return False
        if self.tags_excluidas and not perfil.tags_aplicabilidade.isdisjoint(self.tags_excluidas):
            return False
        return True


@dataclass(frozen=True)
class CriterioAuditoria:
    id: str
    descricao: str
    natureza_fundamento: str
    apto_a_fundamentar_determinacao: bool
    seletor: SeletorAplicabilidade = field(default_factory=SeletorAplicabilidade)
    rotulo_publico: str = ""


@dataclass(frozen=True)
class VarianteEncaminhamento:
    id: str
    id_situacao: str
    geral: bool
    criterios: tuple[str, ...]
    tipo_encaminhamento: str
    encaminhamento: str
    seletor: SeletorAplicabilidade = field(default_factory=SeletorAplicabilidade)
    rotulo_publico: str = ""


@dataclass(frozen=True)
class VarianteResolvida:
    variante: VarianteEncaminhamento
    criterios: tuple[CriterioAuditoria, ...]


class ErroAplicabilidade(ValueError):
    """Erro determinístico de consistência ou resolução da camada jurídica."""


class ResolverAplicabilidade:
    def __init__(
        self,
        criterios: Sequence[CriterioAuditoria],
        variantes: Sequence[VarianteEncaminhamento],
    ) -> None:
        self.criterios = {criterio.id: criterio for criterio in criterios}
        if len(self.criterios) != len(criterios):
            raise ErroAplicabilidade("Há identificadores de critérios duplicados.")
        self.variantes_por_situacao: dict[str, list[VarianteEncaminhamento]] = {}
        for variante in variantes:
            self.variantes_por_situacao.setdefault(variante.id_situacao, []).append(variante)
        self._validar_catalogo()

    def _validar_catalogo(self) -> None:
        for criterio in self.criterios.values():
            if not criterio.descricao.strip():
                raise ErroAplicabilidade(f"{criterio.id}: critério sem descrição.")
            if not criterio.natureza_fundamento.strip():
                raise ErroAplicabilidade(f"{criterio.id}: natureza_fundamento não informada.")
        ids_variantes: set[str] = set()
        for id_situacao, variantes in self.variantes_por_situacao.items():
            gerais = [variante for variante in variantes if variante.geral]
            if len(gerais) != 1:
                raise ErroAplicabilidade(
                    f"{id_situacao}: deve existir exatamente uma variante geral; encontradas {len(gerais)}."
                )
            for variante in variantes:
                if variante.id in ids_variantes:
                    raise ErroAplicabilidade(f"Identificador de variante duplicado: {variante.id}.")
                ids_variantes.add(variante.id)
                if variante.geral and not variante.seletor.vazio:
                    raise ErroAplicabilidade(f"{variante.id}: a variante geral não pode restringir o público.")
                if not variante.geral and variante.seletor.vazio:
                    raise ErroAplicabilidade(f"{variante.id}: variante específica sem seletor preenchido.")
                if not variante.criterios:
                    raise ErroAplicabilidade(f"{variante.id}: variante sem critérios.")
                if variante.tipo_encaminhamento.strip().lower() not in {
                    "recomendação",
                    "determinação",
                }:
                    raise ErroAplicabilidade(
                        f"{variante.id}: tipo_encaminhamento deve ser Recomendação ou Determinação."
                    )
                if not variante.encaminhamento.strip():
                    raise ErroAplicabilidade(f"{variante.id}: encaminhamento não informado.")
                ausentes = [criterio for criterio in variante.criterios if criterio not in self.criterios]
                if ausentes:
                    raise ErroAplicabilidade(
                        f"{variante.id}: critérios inexistentes: {', '.join(ausentes)}."
                    )

    def resolver(self, perfil: PerfilAuditado, id_situacao: str) -> VarianteResolvida:
        variantes = self.variantes_por_situacao.get(id_situacao, [])
        if not variantes:
            raise ErroAplicabilidade(f"{id_situacao}: situação sem variantes de encaminhamento.")
        geral = next(variante for variante in variantes if variante.geral)
        especificas = [
            variante
            for variante in variantes
            if not variante.geral and variante.seletor.corresponde(perfil)
        ]
        if len(especificas) > 1:
            ids = ", ".join(variante.id for variante in especificas)
            raise ErroAplicabilidade(
                f"{perfil.sigla}/{id_situacao}: mais de uma variante específica aplicável: {ids}."
            )
        selecionada = especificas[0] if especificas else geral
        criterios = tuple(self.criterios[id_criterio] for id_criterio in selecionada.criterios)
        incompativeis = [
            criterio.id for criterio in criterios if not criterio.seletor.corresponde(perfil)
        ]
        if incompativeis:
            raise ErroAplicabilidade(
                f"{perfil.sigla}/{selecionada.id}: critérios fora do público aplicável: "
                + ", ".join(incompativeis)
                + "."
            )
        if selecionada.tipo_encaminhamento.strip().lower() == "determinação" and not any(
            criterio.apto_a_fundamentar_determinacao for criterio in criterios
        ):
            raise ErroAplicabilidade(
                f"{perfil.sigla}/{selecionada.id}: determinação sem critério aplicável "
                "marcado como apto a fundamentá-la."
            )
        return VarianteResolvida(selecionada, criterios)


def carregar_catalogo_planilha(caminho: str):
    """Carrega o resolvedor das abas jurídicas sincronizadas do mapa XLSX."""
    import pandas as pd

    def ler(aba: str):
        return pd.read_excel(caminho, sheet_name=aba, skiprows=2, keep_default_na=False)

    def seletor(row) -> SeletorAplicabilidade:
        return SeletorAplicabilidade.from_mapping(
            {
                "segmentos": row.get("segmentos"),
                "naturezas": row.get("naturezas"),
                "tags_todas": row.get("tags_todas"),
                "tags_alguma": row.get("tags_alguma"),
                "tags_excluidas": row.get("tags_excluidas"),
            }
        )

    criterios = []
    for _, row in ler("Critérios de Auditoria").iterrows():
        apto = row.get("apto_a_fundamentar_determinacao")
        if not isinstance(apto, bool):
            if str(apto).strip().lower() in {"true", "1", "sim"}:
                apto = True
            elif str(apto).strip().lower() in {"false", "0", "não", "nao"}:
                apto = False
            else:
                raise ErroAplicabilidade(
                    f"{row.get('id_criterio')}: apto_a_fundamentar_determinacao inválido."
                )
        criterios.append(
            CriterioAuditoria(
                id=str(row.get("id_criterio") or "").strip(),
                descricao=str(row.get("descricao") or "").strip(),
                natureza_fundamento=str(row.get("natureza_fundamento") or "").strip(),
                apto_a_fundamentar_determinacao=apto,
                seletor=seletor(row),
                rotulo_publico=str(row.get("publico") or "").strip(),
            )
        )
    variantes = []
    for _, row in ler("Variantes de Encaminhamento").iterrows():
        geral_texto = str(row.get("geral") or "").strip().lower()
        if isinstance(row.get("geral"), bool):
            geral = bool(row.get("geral"))
        elif geral_texto in {"true", "1", "sim"}:
            geral = True
        elif geral_texto in {"false", "0", "não", "nao"}:
            geral = False
        else:
            raise ErroAplicabilidade(f"{row.get('id_variante')}: valor geral inválido.")
        variantes.append(
            VarianteEncaminhamento(
                id=str(row.get("id_variante") or "").strip(),
                id_situacao=str(row.get("id_situacao") or "").strip(),
                geral=geral,
                criterios=_normalizar_lista(row.get("criterios")),
                tipo_encaminhamento=str(row.get("tipo_encaminhamento") or "").strip(),
                encaminhamento=str(row.get("encaminhamento") or "").strip(),
                seletor=seletor(row),
                rotulo_publico=str(row.get("publico") or "").strip(),
            )
        )
    return ResolverAplicabilidade(criterios, variantes)
