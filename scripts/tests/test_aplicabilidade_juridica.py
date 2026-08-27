import unittest
from pathlib import Path

from scripts.classificar_auditados_aplicabilidade import classificar
from scripts.gerar_matriz_planejamento import materialize_situation_variant, parse_matrix
from scripts.resources.aplicabilidade_juridica import (
    CriterioAuditoria,
    ErroAplicabilidade,
    PerfilAuditado,
    ResolverAplicabilidade,
    SeletorAplicabilidade,
    VarianteEncaminhamento,
)
from scripts.resources.matriz_aplicabilidade import carregar_catalogo_matriz


def _matriz_minima(criterios: str, complemento: str = "") -> str:
    return f"""\
## Questão 01 - Teste

questao: Q1. A organização atende ao critério?

criterios:
{criterios}

{complemento}
procedimentos:
- P1: Verificar o atendimento.
"""


class CriteriosMatrizTest(unittest.TestCase):
    def test_formato_unificado_aceita_criterio_geral_e_especifico(self):
        matriz = parse_matrix(
            _matriz_minima(
                """\
- id: C1
  descricao: >-
    Referencial geral: descrição com dois-pontos.
  natureza_fundamento: boa_pratica
  apto_a_fundamentar_determinacao: false
- id: C2
  descricao: Norma específica.
  natureza_fundamento: norma_regulamentar_vinculante
  apto_a_fundamentar_determinacao: true
  publico: Poder Executivo Estadual
  aplica_se:
    segmentos: [EXECUTIVO_ESTADUAL]"""
            )
        )
        geral, especifico = matriz.questions[0].criterios
        self.assertEqual(geral.id, "C1")
        self.assertEqual(geral.descricao, "Referencial geral: descrição com dois-pontos.")
        self.assertFalse(geral.especifico)
        self.assertEqual(especifico.aplica_se, {"segmentos": ["EXECUTIVO_ESTADUAL"]})
        self.assertTrue(especifico.especifico)

    def test_formato_legado_e_rejeitado(self):
        texto = _matriz_minima(
            """\
- id: C1
  descricao: Critério.
  natureza_fundamento: boa_pratica
  apto_a_fundamentar_determinacao: false""",
            """\
metadados_criterios:
- id: C1
  natureza_fundamento: boa_pratica
  apto_a_fundamentar_determinacao: false

""",
        )
        with self.assertRaisesRegex(ValueError, "blocos de critérios legados"):
            parse_matrix(texto)

    def test_booleano_de_aptidao_deve_ser_explicito(self):
        with self.assertRaisesRegex(ValueError, "explicitamente como true ou false"):
            parse_matrix(
                _matriz_minima(
                    """\
- id: C1
  descricao: Critério.
  natureza_fundamento: boa_pratica
  apto_a_fundamentar_determinacao: não"""
                )
            )

    def test_publico_e_seletor_devem_ser_declarados_em_conjunto(self):
        with self.assertRaisesRegex(ValueError, "publico exige aplica_se"):
            parse_matrix(
                _matriz_minima(
                    """\
- id: C1
  descricao: Critério.
  natureza_fundamento: boa_pratica
  apto_a_fundamentar_determinacao: false
  publico: Poder Executivo Estadual"""
                )
            )

    def test_estrutura_invalida_e_rejeitada(self):
        cases = (
            (
                "critério duplicado",
                """\
- id: C1
  descricao: Primeiro.
  natureza_fundamento: boa_pratica
  apto_a_fundamentar_determinacao: false
- id: C1
  descricao: Segundo.
  natureza_fundamento: boa_pratica
  apto_a_fundamentar_determinacao: false""",
                "critério duplicado",
            ),
            (
                "campo desconhecido",
                """\
- id: C1
  descricao: Critério.
  natureza_fundamento: boa_pratica
  apto_a_fundamentar_determinacao: false
  natureza: inválida""",
                "campos desconhecidos",
            ),
            (
                "descrição vazia",
                """\
- id: C1
  descricao: ''
  natureza_fundamento: boa_pratica
  apto_a_fundamentar_determinacao: false""",
                "descricao não pode ser vazia",
            ),
            (
                "seletor vazio",
                """\
- id: C1
  descricao: Critério.
  natureza_fundamento: boa_pratica
  apto_a_fundamentar_determinacao: false
  publico: Poder Executivo Estadual
  aplica_se:
    segmentos: []""",
                "sem seletor preenchido",
            ),
            (
                "seletor sem público",
                """\
- id: C1
  descricao: Critério.
  natureza_fundamento: boa_pratica
  apto_a_fundamentar_determinacao: false
  aplica_se:
    segmentos: [EXECUTIVO_ESTADUAL]""",
                "sem publico",
            ),
        )
        for label, criteria, message in cases:
            with self.subTest(label=label):
                with self.assertRaisesRegex(ValueError, message):
                    parse_matrix(_matriz_minima(criteria))

    def test_lista_antiga_de_criterios_e_rejeitada(self):
        with self.assertRaisesRegex(ValueError, "campos desconhecidos"):
            parse_matrix(_matriz_minima("- C1: Critério no formato antigo."))

    def test_catalogo_real_preserva_quantitativos_e_especificos(self):
        caminho = Path(
            "01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/"
            "matriz_planejamento-pos-comentarios-gestor.md"
        )
        catalogo = carregar_catalogo_matriz(caminho)
        gerais = [criterio for criterio in catalogo.criterios if criterio.seletor.vazio]
        especificos = [criterio for criterio in catalogo.criterios if not criterio.seletor.vazio]
        self.assertEqual(len(gerais), 40)
        self.assertEqual(len(especificos), 21)
        self.assertTrue(
            all(len(criterio.seletor.segmentos) == 1 for criterio in especificos)
        )


class VariantesAninhadasMatrizTest(unittest.TestCase):
    CRITERIOS = """\
- id: C1
  descricao: Critério geral.
  natureza_fundamento: boa_pratica
  apto_a_fundamentar_determinacao: false
- id: C2
  descricao: Critério específico.
  natureza_fundamento: norma_regulamentar_vinculante
  apto_a_fundamentar_determinacao: true
  publico: Poder Judiciário Estadual
  aplica_se:
    segmentos: [JUDICIARIO_ESTADUAL]"""

    def _parse(self, variants: str):
        text = _matriz_minima(
            self.CRITERIOS,
            f"""\
possiveis_achados:
- A1: Achado
  situacoes_encontradas:
  - S1.1:
      descricao: Situação geral.
      severidade: alta
      itens_questionario: [q0101]
      regra_de_identificacao:
      - (q0101 != Sim)
      referencias_matriz: [R1.1, P1, E1]
      criterios: [C1]
      tipo_encaminhamento: Recomendação
      encaminhamento: corrija a situação geral
      variantes:
{variants}

""",
        )
        return parse_matrix(text).questions[0].achados[0].situacoes[0]

    def test_campos_omitidos_sao_herdados_e_id_e_gerado(self):
        situation = self._parse(
            """\
      - publico: Poder Judiciário Estadual
        aplica_se:
          segmentos: [JUDICIARIO_ESTADUAL]
        criterios: [C2]"""
        )
        identifier, criteria, referral_type, referral = materialize_situation_variant(
            situation, situation.variantes[0]
        )
        self.assertEqual(identifier, "S1.1.JUDICIARIO_ESTADUAL")
        self.assertEqual(criteria, ["C2"])
        self.assertEqual(referral_type, "Recomendação")
        self.assertEqual(referral, "corrija a situação geral")

    def test_campos_declarados_substituem_os_gerais_sem_mesclagem(self):
        situation = self._parse(
            """\
      - publico: Poder Judiciário Estadual
        aplica_se:
          segmentos: [JUDICIARIO_ESTADUAL]
        criterios: [C2]
        tipo_encaminhamento: Determinação
        encaminhamento: cumpra a norma específica"""
        )
        _, criteria, referral_type, referral = materialize_situation_variant(
            situation, situation.variantes[0]
        )
        self.assertEqual(criteria, ["C2"])
        self.assertEqual(referral_type, "Determinação")
        self.assertEqual(referral, "cumpra a norma específica")

    def test_id_usa_publico_quando_nao_ha_segmento_unico(self):
        situation = self._parse(
            """\
      - publico: Órgãos integrantes do sistema
        aplica_se:
          tags_alguma: [SETIC]
        criterios: [C2]"""
        )
        identifier, *_ = materialize_situation_variant(situation, situation.variantes[0])
        self.assertEqual(identifier, "S1.1.ORGAOS_INTEGRANTES_DO_SISTEMA")

    def test_id_e_campos_factuais_nao_podem_ser_declarados(self):
        for field in ("id: S1.1.MANUAL", "descricao: Outra situação"):
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, "campos desconhecidos"):
                    self._parse(
                        f"""\
      - publico: Poder Judiciário Estadual
        aplica_se:
          segmentos: [JUDICIARIO_ESTADUAL]
        criterios: [C2]
        {field}"""
                    )

    def test_bloco_global_legado_e_rejeitado(self):
        text = _matriz_minima(
            self.CRITERIOS,
            """\
variantes_especificas:
- id: S1.1.JUDICIARIO_ESTADUAL
  id_situacao: S1.1

""",
        )
        with self.assertRaisesRegex(ValueError, "bloco global variantes_especificas"):
            parse_matrix(text)

    def test_catalogo_real_preserva_ids_das_variantes(self):
        caminho = Path(
            "01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/"
            "matriz_planejamento-pos-comentarios-gestor.md"
        )
        catalog = carregar_catalogo_matriz(caminho)
        specifics = {variant.id for variant in catalog.variantes if not variant.geral}
        self.assertEqual(len(specifics), 72)
        for variant in catalog.variantes:
            if not variant.geral:
                self.assertTrue(
                    any(
                        variant.id.endswith(sufixo)
                        for sufixo in (
                            "EXECUTIVO_ESTADUAL",
                            "JUDICIARIO_ESTADUAL",
                            "MINISTERIO_PUBLICO_ESTADUAL",
                        )
                    )
                )


class SeletorAplicabilidadeTest(unittest.TestCase):
    def setUp(self):
        self.perfil = PerfilAuditado(
            sigla="ORGAO",
            segmento_institucional="EXECUTIVO_ESTADUAL",
            natureza_administrativa="AUTARQUIA",
            tags_aplicabilidade=frozenset({"SETIC", "SISP_RJ"}),
        )

    def test_campos_ausentes_nao_restringem(self):
        self.assertTrue(SeletorAplicabilidade.from_mapping({}).corresponde(self.perfil))

    def test_listas_vazias_nao_restringem(self):
        seletor = SeletorAplicabilidade.from_mapping(
            {
                "segmentos": ["EXECUTIVO_ESTADUAL"],
                "naturezas": [],
                "tags_todas": [],
                "tags_alguma": [],
                "tags_excluidas": [],
            }
        )
        self.assertTrue(seletor.corresponde(self.perfil))

    def test_apenas_segmento_abrange_todas_as_naturezas_e_tags(self):
        seletor = SeletorAplicabilidade.from_mapping({"segmentos": ["EXECUTIVO_ESTADUAL"]})
        perfis = [
            self.perfil,
            PerfilAuditado("SEC", "EXECUTIVO_ESTADUAL", "ADMINISTRACAO_DIRETA"),
            PerfilAuditado("FUND", "EXECUTIVO_ESTADUAL", "FUNDACAO", frozenset({"OUTRA"})),
        ]
        self.assertTrue(all(seletor.corresponde(perfil) for perfil in perfis))
        self.assertFalse(seletor.corresponde(PerfilAuditado("TJRJ", "JUDICIARIO_ESTADUAL")))

    def test_filtros_adicionais_restringem_por_and(self):
        seletor = SeletorAplicabilidade.from_mapping(
            {
                "segmentos": ["EXECUTIVO_ESTADUAL"],
                "naturezas": ["AUTARQUIA", "FUNDACAO"],
                "tags_todas": ["SETIC"],
                "tags_alguma": ["SISP_RJ", "OUTRA"],
                "tags_excluidas": ["EXCLUIDA"],
            }
        )
        self.assertTrue(seletor.corresponde(self.perfil))
        self.assertFalse(
            seletor.corresponde(
                PerfilAuditado("X", "EXECUTIVO_ESTADUAL", "AUTARQUIA", frozenset({"SETIC", "EXCLUIDA"}))
            )
        )


class ResolverAplicabilidadeTest(unittest.TestCase):
    def _criterios(self):
        return [
            CriterioAuditoria("Q6.C1", "Geral", "boa_pratica", False),
            CriterioAuditoria(
                "Q6.C11",
                "Específico",
                "normativo_vinculante",
                True,
                SeletorAplicabilidade.from_mapping({"segmentos": ["EXECUTIVO_ESTADUAL"]}),
            ),
        ]

    def _variantes(self):
        return [
            VarianteEncaminhamento(
                "S6.4.GERAL", "S6.4", True, ("Q6.C1",), "Recomendação", "avalie"
            ),
            VarianteEncaminhamento(
                "S6.4.EXEC_EST", "S6.4", False, ("Q6.C11",), "Determinação", "designe",
                SeletorAplicabilidade.from_mapping({"segmentos": ["EXECUTIVO_ESTADUAL"]}),
            ),
        ]

    def test_variante_especifica_substitui_geral(self):
        resolvida = ResolverAplicabilidade(self._criterios(), self._variantes()).resolver(
            PerfilAuditado("AUT", "EXECUTIVO_ESTADUAL", "AUTARQUIA"), "S6.4"
        )
        self.assertEqual(resolvida.variante.id, "S6.4.EXEC_EST")
        self.assertEqual(resolvida.variante.tipo_encaminhamento, "Determinação")

    def test_geral_e_usada_sem_especifica(self):
        resolvida = ResolverAplicabilidade(self._criterios(), self._variantes()).resolver(
            PerfilAuditado("PREF", "EXECUTIVO_MUNICIPAL", "ADMINISTRACAO_DIRETA"), "S6.4"
        )
        self.assertEqual(resolvida.variante.id, "S6.4.GERAL")

    def test_conflito_entre_especificas_falha(self):
        variantes = self._variantes() + [
            VarianteEncaminhamento(
                "S6.4.SETIC", "S6.4", False, ("Q6.C11",), "Determinação", "designe",
                SeletorAplicabilidade.from_mapping({"tags_alguma": ["SETIC"]}),
            )
        ]
        with self.assertRaisesRegex(ErroAplicabilidade, "mais de uma variante específica"):
            ResolverAplicabilidade(self._criterios(), variantes).resolver(
                PerfilAuditado("AUT", "EXECUTIVO_ESTADUAL", "AUTARQUIA", frozenset({"SETIC"})), "S6.4"
            )

    def test_especifica_sem_filtro_falha(self):
        variantes = self._variantes() + [
            VarianteEncaminhamento("S6.4.INVALIDA", "S6.4", False, ("Q6.C1",), "Recomendação", "x")
        ]
        with self.assertRaisesRegex(ErroAplicabilidade, "sem seletor preenchido"):
            ResolverAplicabilidade(self._criterios(), variantes)

    def test_determinacao_sem_criterio_apto_falha(self):
        variantes = [
            VarianteEncaminhamento("S6.4.GERAL", "S6.4", True, ("Q6.C1",), "Determinação", "determine")
        ]
        with self.assertRaisesRegex(ErroAplicabilidade, "sem critério aplicável"):
            ResolverAplicabilidade(self._criterios(), variantes).resolver(
                PerfilAuditado("PREF", "EXECUTIVO_MUNICIPAL"), "S6.4"
            )

    def test_tipo_de_encaminhamento_deve_ser_explicito_e_valido(self):
        variantes = [
            VarianteEncaminhamento("S6.4.GERAL", "S6.4", True, ("Q6.C1",), "Aviso", "avalie")
        ]
        with self.assertRaisesRegex(ErroAplicabilidade, "Recomendação ou Determinação"):
            ResolverAplicabilidade(self._criterios(), variantes)


class ClassificacaoAuditadosTest(unittest.TestCase):
    def test_classificacao_conhecida_e_materializada(self):
        self.assertEqual(
            classificar("TJRJ", "E"),
            ("JUDICIARIO_ESTADUAL", "ORGAO_AUTONOMO", "CNJ"),
        )

    def test_organizacao_desconhecida_nao_e_inferida(self):
        with self.assertRaisesRegex(ValueError, "não declarada explicitamente"):
            classificar("ORGAO_NOVO", "E")


if __name__ == "__main__":
    unittest.main()
