"""Testes automatizados de consistência e cobertura de critérios nos templates de achados."""

import json
import os
import sys
from pathlib import Path
import jinja2

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "scripts" / "resources"))

from argos_classes import Auditado
from gerar_matriz_planejamento import parse_matrix


def carregar_dados_auditoria():
    json_path = (
        REPO_ROOT
        / "02-Execucao"
        / "03-Execucao_Procedimentos"
        / "02-Resultados_Auditoria"
        / "03-pos-comentarios-gestor"
        / "resultado_auditoria.json"
    )
    with open(json_path, encoding="utf-8") as f:
        return json.load(f)


def obter_jinja_env():
    templates_dir = REPO_ROOT / "03-Relatorios" / "03-Relatorios_Individuais_Finais"
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(templates_dir)),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
        undefined=jinja2.StrictUndefined,
    )


class DummyAuditado:
    """Objeto auxiliar para extrair variáveis exportadas pelos templates Jinja."""
    def get_achado_por_nome(self, nome):
        class DummyAchado:
            pass
        a = DummyAchado()
        a.numero = "1"
        a.nome = nome
        a.situacoes_encontradas = []
        a.encaminhamentos = []
        return a

    def get_criterios_achado(self, nome):
        return []

    def get_enquadramentos_especificos_achado(self, nome):
        return []

    def get_evidencias_numeradas(self, nome):
        return []

    def get_motivos_situacao(self, nome, sit):
        return []

    def get_criterios_situacao(self, nome, sit):
        return []


ACHADOS_MAP = [
    ("achado_questao_1_estrutura_tic.md", "Q1", "Estrutura de TIC insuficientemente formalizada, definida ou posicionada para gerir a tecnologia da informação."),
    ("achado_questao_2_governanca_comite_tic.md", "Q2", "Governança de TIC insuficiente para avaliar, dirigir e monitorar a tecnologia da informação."),
    ("achado_questao_3_planejamento_tic.md", "Q3", "Planejamento de TIC insuficiente para orientar a gestão, o orçamento e as contratações de TIC"),
    ("achado_questao_4_capacidade_institucional_tic_si.md", "Q4", "Capacidade institucional de pessoal de TIC e segurança da informação insuficientemente estruturada ou dimensionada"),
    ("achado_questao_5_gestao_servicos_tic.md", "Q5", "Gestão de serviços de TIC insuficiente para assegurar controle sobre serviços, ativos e incidentes"),
    ("achado_questao_6_contratacoes_tic.md", "Q6", "Fragilidades na governança técnica da fase preparatória das contratações de TIC"),
]


def extrair_dicionarios_templates(env):
    """Extrai os dicionários narrativa_criterios de cada template."""
    dicionarios = {}
    dummy = DummyAuditado()
    for tpl_name, q_prefix, _ in ACHADOS_MAP:
        tpl = env.get_template(tpl_name)
        mod = tpl.make_module({"auditado": dummy})
        narrativa = getattr(mod, "narrativa_criterios", {})
        dicionarios[q_prefix] = dict(narrativa)
    return dicionarios


def test_cobertura_criterios_templates():
    """Valida 100% de cobertura entre critérios da matriz e narrativa_criterios nos templates."""
    matriz_path = (
        REPO_ROOT
        / "01-Planejamento"
        / "03-Estrategia_e_Plano"
        / "04-Matriz_Planejamento"
        / "matriz_planejamento-pos-comentarios-gestor.md"
    )
    matriz = parse_matrix(matriz_path.read_text(encoding="utf-8"))
    env = obter_jinja_env()
    dicionarios = extrair_dicionarios_templates(env)

    total_matriz = 0
    total_templates = 0

    for q in matriz.questions:
        if q.id not in dicionarios:
            continue
        # IDs da matriz no formato Qx.Cy
        matriz_cids = set()
        for c in q.criterios:
            cid = c.id if c.id.startswith(q.id + ".") else f"{q.id}.{c.id}"
            matriz_cids.add(cid)

        template_cids = set(dicionarios[q.id].keys())

        # 1. Todos os critérios da matriz devem estar no template
        faltando = matriz_cids - template_cids
        assert not faltando, f"Critérios da matriz sem narrativa no template de {q.id}: {faltando}"

        # 2. Nenhum critério desconhecido no template
        sobbrando = template_cids - matriz_cids
        assert not sobbrando, f"Critérios no template de {q.id} sem correspondência na matriz: {sobbrando}"

        # 3. Nenhum texto vazio
        for cid, texto in dicionarios[q.id].items():
            assert texto and texto.strip(), f"Narrativa vazia para o critério {cid} em {q.id}"

        total_matriz += len(matriz_cids)
        total_templates += len(template_cids)

    assert total_matriz == 76, f"Esperado 76 critérios na matriz para Q1-Q6, encontrado {total_matriz}"
    assert total_templates == 76, f"Esperado 76 critérios nos templates para Q1-Q6, encontrado {total_templates}"
    print(f"test_cobertura_criterios_templates: OK! (100% de cobertura nos {total_templates} critérios)")


def test_consistencia_criterios_seel():
    """Valida consistência das diretrizes editoriais no relatório de SEEL."""
    dados = carregar_dados_auditoria()
    env = obter_jinja_env()
    auditado = Auditado.from_dict(dados["SEEL"])

    for tpl_name, _, _ in ACHADOS_MAP:
        tpl = env.get_template(tpl_name)
        rendered = tpl.render(auditado=auditado)
        if not rendered.strip():
            continue

        # Verifica que nenhum dos termos banidos aparece
        assert "governabilidade financeira" not in rendered, f"Termo 'governabilidade financeira' encontrado em {tpl_name}"
        assert "[^explica_" not in rendered, f"Nota de rodapé [^explica_ encontrada em {tpl_name}"

        # Se for Achado 1:
        if "achado_questao_1" in tpl_name:
            assert "Decreto Estadual nº 48.997/2024" in rendered
            assert "art. 37, caput, da Constituição Federal" not in rendered
            assert "Constituição Federal, art. 37" not in rendered

        # Se for Achado 2:
        if "achado_questao_2" in tpl_name:
            assert "Portaria PRODERJ/PRE nº 825/2021" in rendered
            assert "Decreto federal nº 12.198/2024" not in rendered
            assert "Decreto nº 12.198/2024" not in rendered

        # Se for Achado 4:
        if "achado_questao_4" in tpl_name:
            if "Cargos ou funções" in rendered:
                assert "segurança da informação" in rendered

        # Se for Achado 5:
        if "achado_questao_5" in tpl_name:
            assert "controle de custos" in rendered
            assert "podendo reduzir" in rendered

        # Se for Achado 6:
        if "achado_questao_6" in tpl_name:
            assert "Para esta situação, foram aplicados os critérios apresentados na seção Critérios" not in rendered
            assert "IN PRODERJ/PRE nº 5/2024" in rendered

    print("test_consistencia_criterios_seel: OK!")


def test_todos_criterios_resolvidos_presentes():
    """Valida que todos os critérios resolvidos para SEEL, TJRJ, MPERJ e DUQUE DE CAXIAS estão no texto."""
    dados = carregar_dados_auditoria()
    env = obter_jinja_env()
    dicionarios = extrair_dicionarios_templates(env)

    for sigla in ["SEEL", "TJRJ", "MPERJ", "DUQUE DE CAXIAS"]:
        if sigla not in dados:
            continue
        auditado = Auditado.from_dict(dados[sigla])

        for tpl_name, q_prefix, achado_nome in ACHADOS_MAP:
            achado = auditado.get_achado_por_nome(achado_nome)
            if not achado:
                continue

            tpl = env.get_template(tpl_name)
            rendered = tpl.render(auditado=auditado)

            for situacao in getattr(achado, "situacoes_detalhadas", []):
                id_sit = situacao["id_situacao"]
                criterios = auditado.get_criterios_situacao(achado_nome, id_sit)
                for c in criterios:
                    cid = c["id"]
                    texto_esperado = dicionarios[q_prefix][cid]
                    assert texto_esperado in rendered, (
                        f"Critério {cid} ({id_sit}) não encontrado no texto renderizado para {sigla} em {tpl_name}"
                    )

    print("test_todos_criterios_resolvidos_presentes: OK!")


def test_todos_auditados_renderizam_sem_erro():
    """Valida renderização com StrictUndefined para todas as organizações auditadas."""
    dados = carregar_dados_auditoria()
    env = obter_jinja_env()

    total_auditados = 0
    total_instancias = 0

    for sigla, org in dados.items():
        if not org.get("tem_achados"):
            continue
        auditado = Auditado.from_dict(org)
        total_auditados += 1
        for tpl_name, _, _ in ACHADOS_MAP:
            tpl = env.get_template(tpl_name)
            rendered = tpl.render(auditado=auditado)
            if rendered.strip():
                total_instancias += 1

    print(f"test_todos_auditados_renderizam_sem_erro: OK! ({total_auditados} auditados, {total_instancias} achados renderizados)")


if __name__ == "__main__":
    print("Iniciando bateria de testes de consistência de critérios...")
    test_cobertura_criterios_templates()
    test_consistencia_criterios_seel()
    test_todos_criterios_resolvidos_presentes()
    test_todos_auditados_renderizam_sem_erro()
    print("Todos os testes passaram com 100% de sucesso!")
