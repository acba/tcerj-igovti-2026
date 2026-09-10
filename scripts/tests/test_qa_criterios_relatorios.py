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
    """Objeto auxiliar restrito estritamente aos métodos autorizados nos templates Jinja."""
    def get_achado_por_id(self, id_achado):
        class DummyAchado:
            pass
        a = DummyAchado()
        a.id_achado = id_achado
        a.numero = id_achado.replace("Q", "") if str(id_achado).startswith("Q") else "1"
        a.nome = f"Achado {a.numero}"
        a.situacoes_encontradas = []
        a.encaminhamentos = []
        return a

    def get_situacao(self, id_achado, id_situacao):
        from argos_classes import SituacaoAchado
        return SituacaoAchado(id_situacao=id_situacao, descricao="", ativa=False)

    def get_criterios_achado(self, id_achado):
        return []

    def get_evidencias_numeradas(self, id_achado):
        return []


ACHADOS_MAP = [
    ("achado_questao_1_estrutura_tic.md", "Q1"),
    ("achado_questao_2_governanca_comite_tic.md", "Q2"),
    ("achado_questao_3_planejamento_tic.md", "Q3"),
    ("achado_questao_4_capacidade_institucional_tic_si.md", "Q4"),
    ("achado_questao_5_gestao_servicos_tic.md", "Q5"),
    ("achado_questao_6_contratacoes_tic.md", "Q6"),
]


def extrair_dicionarios_templates(env):
    """Extrai os dicionários narrativa_criterios de cada template."""
    dicionarios = {}
    dummy = DummyAuditado()
    for tpl_name, q_prefix in ACHADOS_MAP:
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

    assert total_matriz > 0, "Nenhum critério encontrado na matriz para Q1-Q6"
    assert total_matriz == total_templates, (
        f"Contagem total divergente: {total_matriz} critérios na matriz vs {total_templates} nos templates"
    )
    print(f"test_cobertura_criterios_templates: OK! (100% de cobertura nos {total_templates} critérios)")


def test_qa_ids_estaveis_templates():
    """Valida ausência de dependência textual e conformidade dos IDs estáveis nos 6 templates."""
    import re

    matriz_path = (
        REPO_ROOT
        / "01-Planejamento"
        / "03-Estrategia_e_Plano"
        / "04-Matriz_Planejamento"
        / "matriz_planejamento-pos-comentarios-gestor.md"
    )
    matriz = parse_matrix(matriz_path.read_text(encoding="utf-8"))
    matriz_situacoes_por_q = {}
    for q in matriz.questions:
        matriz_situacoes_por_q[q.id] = {s.id for achado in q.achados for s in achado.situacoes}

    templates_dir = REPO_ROOT / "03-Relatorios" / "03-Relatorios_Individuais_Finais"

    for tpl_name, q_prefix in ACHADOS_MAP:
        tpl_path = templates_dir / tpl_name
        content = tpl_path.read_text(encoding="utf-8")

        # 1. Todo template possui declaração de id_achado
        match_achado = re.search(r"\{%\s*set\s+id_achado\s*=\s*['\"]([^'\"]+)['\"]\s*%\}", content)
        assert match_achado, f"Template {tpl_name} não declara id_achado"
        assert match_achado.group(1) == q_prefix, f"id_achado em {tpl_name} é {match_achado.group(1)}, esperado {q_prefix}"

        # 2. Nenhum template usa get_achado_por_nome
        assert "get_achado_por_nome" not in content, f"Template {tpl_name} ainda chama get_achado_por_nome"

        # 3. Nenhum template usa métodos antigos baseados em descrição
        assert "get_criterios_situacao" not in content, f"Template {tpl_name} ainda chama get_criterios_situacao"
        assert "get_motivos_situacao" not in content, f"Template {tpl_name} ainda chama get_motivos_situacao"
        assert "in achado.situacoes_encontradas" not in content, f"Template {tpl_name} verifica achado.situacoes_encontradas diretamente"

        # 4. Todos os Sx.y referenciados existem na matriz e são únicos
        sids_invocados = re.findall(r"get_situacao\s*\(\s*id_achado\s*,\s*['\"]([^'\"]+)['\"]\s*\)", content)
        assert sids_invocados, f"Template {tpl_name} não possui chamadas get_situacao(id_achado, ...)"
        assert len(sids_invocados) == len(set(sids_invocados)), f"IDs de situação duplicados no template {tpl_name}: {sids_invocados}"

        for sid in sids_invocados:
            assert sid in matriz_situacoes_por_q[q_prefix], (
                f"Situação {sid} referenciada no template {tpl_name} não existe na matriz para {q_prefix}"
            )

    print("test_qa_ids_estaveis_templates: OK! (IDs únicos, sem métodos legados, 100% alinhados à matriz)")


def test_alteracao_editorial_titulo_achado():
    """Valida que alteração no título do achado não quebra resolução nem renderização."""
    dados = carregar_dados_auditoria()
    env = obter_jinja_env()
    aud = Auditado.from_dict(dados["SEEL"])

    achado1 = aud.get_achado_por_id("Q1")
    assert achado1 is not None
    achado1.nome = "TÍTULO MUTADO ARBITRARIAMENTE PARA TESTE DE RESILIÊNCIA"

    # get_achado_por_id deve continuar encontrando o achado
    achado_resolvido = aud.get_achado_por_id("Q1")
    assert achado_resolvido is achado1
    assert achado_resolvido.nome == "TÍTULO MUTADO ARBITRARIAMENTE PARA TESTE DE RESILIÊNCIA"

    # Renderização deve ocorrer sem erros
    tpl = env.get_template("achado_questao_1_estrutura_tic.md")
    rendered = tpl.render(auditado=aud)
    assert "TÍTULO MUTADO ARBITRARIAMENTE PARA TESTE DE RESILIÊNCIA" in rendered
    print("test_alteracao_editorial_titulo_achado: OK!")


def test_alteracao_editorial_descricao_situacao():
    """Valida que alteração na descrição textual da situação não quebra resolução nem critérios/motivos."""
    dados = carregar_dados_auditoria()
    env = obter_jinja_env()
    aud = Auditado.from_dict(dados["SEEL"])

    achado1 = aud.get_achado_por_id("Q1")
    assert achado1 is not None

    # Localiza S1.2 por ID estrutural (nunca por posição arbitrária)
    sd12 = next(s for s in achado1.situacoes_detalhadas if s.get("id_situacao") == "S1.2")
    desc_orig12 = sd12["descricao"]
    try:
        # Altera apenas a descrição editorial da situação detalhada (sem alterar situacoes_encontradas)
        sd12["descricao"] = "DESCRIÇÃO TOTALMENTE MUTADA PARA TESTE DE RESILIÊNCIA"

        s12 = aud.get_situacao("Q1", "S1.2")
        assert s12.ativa is True, "S1.2 deve permanecer ativa mesmo com descrição mutada"
        assert len(s12.criterios) > 0, "Critérios devem continuar disponíveis"
        assert len(s12.motivos) > 0, "Motivos devem continuar disponíveis"

        tpl = env.get_template("achado_questao_1_estrutura_tic.md")
        rendered = tpl.render(auditado=aud)
        assert "Atribuições formais da área de TIC" in rendered
    finally:
        sd12["descricao"] = desc_orig12

    # Validação cruzada adicional com outra organização e situação: TJRJ Q3 S3.5
    aud_tjrj = Auditado.from_dict(dados["TJRJ"])
    achado3 = aud_tjrj.get_achado_por_id("Q3")
    if achado3:
        sd35 = next((s for s in achado3.situacoes_detalhadas if s.get("id_situacao") == "S3.5"), None)
        if sd35:
            desc_orig35 = sd35["descricao"]
            try:
                sd35["descricao"] = "DESCRIÇÃO EDITORIAL MUTADA S3.5"
                s35 = aud_tjrj.get_situacao("Q3", "S3.5")
                assert s35.ativa is True, "S3.5 deve permanecer ativa com descrição mutada"
                assert len(s35.criterios) > 0, "Critérios de S3.5 devem continuar disponíveis"
                assert len(s35.motivos) > 0, "Motivos de S3.5 devem continuar disponíveis"
            finally:
                sd35["descricao"] = desc_orig35

    print("test_alteracao_editorial_descricao_situacao: OK! (Resiliência de S1.2 e S3.5 comprovada)")


def test_semantica_situacao_ativa_independente_de_motivos():
    """Valida que situação ativa não depende de motivos (identidade != completude dos dados)."""
    dados = carregar_dados_auditoria()
    aud = Auditado.from_dict(dados["SEEL"])
    achado1 = aud.get_achado_por_id("Q1")
    assert achado1 is not None

    # Verifica situação real ativa
    s12_original = aud.get_situacao("Q1", "S1.2")
    assert s12_original.ativa is True
    assert len(s12_original.motivos) > 0

    # Simula temporariamente ausência de motivos para verificar separação de conceitos
    motivos_bkp = dict(achado1.motivos_situacoes)
    try:
        achado1.motivos_situacoes.clear()
        s12_sem_motivos = aud.get_situacao("Q1", "S1.2")

        # 1. A situação continua ATIVA (pois foi identificada pelo procedimento de auditoria)
        assert s12_sem_motivos.ativa is True, "Situação deve permanecer ativa mesmo sem motivos"
        # 2. Porém sua lista de motivos está vazia
        assert len(s12_sem_motivos.motivos) == 0, "Lista de motivos deve estar vazia nesta simulação"

        # 3. O teste de QA de completude deve acusar erro ao encontrar situação ativa sem motivos
        falha_detectada = False
        try:
            if s12_sem_motivos.ativa:
                assert s12_sem_motivos.motivos, (
                    f"Situação ativa S1.2 sem motivos no auditado 'SEEL' (Q1)"
                )
        except AssertionError as e:
            falha_detectada = True
            assert "S1.2" in str(e)
            assert "SEEL" in str(e)
            assert "Q1" in str(e)

        assert falha_detectada, "QA deveria ter acusado erro de completude para situação ativa sem motivos"
    finally:
        achado1.motivos_situacoes = motivos_bkp

    print("test_semantica_situacao_ativa_independente_de_motivos: OK! (Identidade != completude comprovada)")


def test_ids_invalidos():
    """Valida que IDs inexistentes ou inválidos não resolvem achados nem situações."""
    dados = carregar_dados_auditoria()
    aud = Auditado.from_dict(dados["SEEL"])

    # Achado inexistente
    assert aud.get_achado_por_id("Q99") is None
    assert aud.get_achado_por_id(None) is None
    assert aud.get_achado_por_id("INVALIDO") is None

    # Situação inexistente em achado existente
    s_invalida = aud.get_situacao("Q1", "S1.99")
    assert s_invalida.ativa is False
    assert s_invalida.motivos == []
    assert s_invalida.criterios == []
    assert s_invalida.id_situacao == "S1.99"

    # Situação em achado inexistente
    s_achado_invalido = aud.get_situacao("Q99", "S1.2")
    assert s_achado_invalido.ativa is False
    assert s_achado_invalido.motivos == []
    assert s_achado_invalido.criterios == []

    # Não deve resolver situação passando descrição textual como ID (fallback por texto removido)
    s_por_desc = aud.get_situacao("Q1", "Área de TIC sem atribuições formalmente definidas ou sem atribuições formais de gestão de TIC.")
    assert s_por_desc.ativa is False

    print("test_ids_invalidos: OK! (IDs inválidos/inexistentes e busca por descrição rejeitados corretamente)")


def test_identidade_independente_descricoes_duplicadas():
    """Valida que situações com a mesma descrição textual mantêm identidades independentes por ID."""
    dados = carregar_dados_auditoria()
    aud = Auditado.from_dict(dados["TJRJ"])
    achado5 = aud.get_achado_por_id("Q5")
    assert achado5 is not None
    assert len(achado5.situacoes_detalhadas) >= 2

    sd1 = achado5.situacoes_detalhadas[0]
    sd2 = achado5.situacoes_detalhadas[1]
    sid1 = sd1["id_situacao"]
    sid2 = sd2["id_situacao"]

    desc_compartilhada = "Descrição genérica idêntica compartilhada para teste de colisão"
    orig_desc1 = sd1["descricao"]
    orig_desc2 = sd2["descricao"]

    try:
        sd1["descricao"] = desc_compartilhada
        sd2["descricao"] = desc_compartilhada

        s1 = aud.get_situacao("Q5", sid1)
        s2 = aud.get_situacao("Q5", sid2)

        assert s1.id_situacao == sid1
        assert s2.id_situacao == sid2
        assert s1.descricao == desc_compartilhada
        assert s2.descricao == desc_compartilhada
        # Não há colisão nem confusão de instâncias
        assert s1 is not s2
        assert s1.ativa is True
        assert s2.ativa is True
        assert len(s1.criterios) > 0
        assert len(s2.criterios) > 0
    finally:
        sd1["descricao"] = orig_desc1
        sd2["descricao"] = orig_desc2

    print(f"test_identidade_independente_descricoes_duplicadas: OK! ({sid1} e {sid2} preservam identidades sob descrição idêntica)")


def test_situacoes_ativas_possuem_motivos_e_criterios():
    """Valida que toda situação ativa em toda a base de auditados possui motivos e critérios."""
    dados = carregar_dados_auditoria()
    total_ativas = 0

    for sigla, org in dados.items():
        if not org.get("tem_achados"):
            continue
        aud = Auditado.from_dict(org)
        for tpl_name, q_prefix in ACHADOS_MAP:
            achado = aud.get_achado_por_id(q_prefix)
            if not achado:
                continue
            for sd in getattr(achado, "situacoes_detalhadas", []) or []:
                sid = sd.get("id_situacao")
                s = aud.get_situacao(q_prefix, sid)
                if s.ativa:
                    total_ativas += 1
                    assert s.motivos, f"Situação ativa {sid} sem motivos no auditado '{sigla}' ({q_prefix})"
                    assert s.criterios, f"Situação ativa {sid} sem critérios no auditado '{sigla}' ({q_prefix})"

    assert total_ativas > 0
    print(f"test_situacoes_ativas_possuem_motivos_e_criterios: OK! ({total_ativas} situações ativas verificadas)")


def test_consistencia_criterios_seel():
    """Valida consistência das diretrizes editoriais no relatório de SEEL."""
    dados = carregar_dados_auditoria()
    env = obter_jinja_env()
    auditado = Auditado.from_dict(dados["SEEL"])

    for tpl_name, _ in ACHADOS_MAP:
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

        for tpl_name, q_prefix in ACHADOS_MAP:
            achado = auditado.get_achado_por_id(q_prefix)
            if not achado:
                continue

            tpl = env.get_template(tpl_name)
            rendered = tpl.render(auditado=auditado)

            for situacao in getattr(achado, "situacoes_detalhadas", []):
                id_sit = situacao["id_situacao"]
                s = auditado.get_situacao(q_prefix, id_sit)
                if not s.ativa:
                    continue
                for c in s.criterios:
                    cid = c["id"] if isinstance(c, dict) else c.id
                    texto_esperado = dicionarios[q_prefix][cid]
                    assert texto_esperado in rendered, (
                        f"Critério {cid} ({id_sit}) não encontrado no texto renderizado para {sigla} em {tpl_name}"
                    )

    print("test_todos_criterios_resolvidos_presentes: OK!")


def test_agrupamento_interno_por_id():
    """Valida que duas ações com mesmo id_situacao e descrições distintas geram 1 única situação detalhada."""
    from argos_classes import ProcedimentoAuditoria, AcaoVerificacao, FonteInformacao
    from aplicabilidade_juridica import carregar_catalogo_planilha

    proc = ProcedimentoAuditoria(
        descricao="Teste agrupamento por id",
        logica_achado="AV01 | AV02",
        numero_achado=5,
        nome_achado="Gestão de serviços de TIC",
        id="PA05",
    )
    fonte = FonteInformacao(descricao="Fonte teste", filepath="none", id="F01")

    # Criamos 2 ações com mesmo id_situacao 'S5.3' mas descrições divergentes
    acao1 = AcaoVerificacao(
        id="AV01",
        fonte_informacao=fonte,
        informacao_requerida="info 1",
        criterio="crit 1",
        descricao_evidencia="evidencia 1",
        situacao_inconforme="sit 1",
        tipo_encaminhamento="Recomendação",
        encaminhamento="enc 1",
        pre_encaminhamento="pre 1",
        descricao_situacao_inconforme="Descrição A para inventário de ativos",
        id_situacao="S5.3",
    )
    acao1.resultado = True

    acao2 = AcaoVerificacao(
        id="AV02",
        fonte_informacao=fonte,
        informacao_requerida="info 2",
        criterio="crit 2",
        descricao_evidencia="evidencia 2",
        situacao_inconforme="sit 2",
        tipo_encaminhamento="Recomendação",
        encaminhamento="enc 2",
        pre_encaminhamento="pre 2",
        descricao_situacao_inconforme="Descrição B para inventário de ativos divergente",
        id_situacao="S5.3",
    )
    acao2.resultado = True

    proc.adicionar_acao(acao1)
    proc.adicionar_acao(acao2)

    mapa_path = (
        REPO_ROOT
        / "02-Execucao"
        / "03-Execucao_Procedimentos"
        / "01-Insumos"
        / "mapa-verificacao-achados-pos-comentarios-gestor.xlsx"
    )
    resolvedor = carregar_catalogo_planilha(str(mapa_path))

    class DummyAuditadoExec:
        id = "TESTE"
        sigla = "TESTE"
        tipo_esfera = "Estadual"
        natureza_juridica = "Administração Direta"
        tipo_controle = "Estadual"

    auditado_exec = DummyAuditadoExec()

    from aplicabilidade_juridica import PerfilAuditado
    perfil = PerfilAuditado(sigla="TESTE", segmento_institucional="ESTADUAL")

    orig_executar = AcaoVerificacao.executar
    AcaoVerificacao.executar = lambda self, aud, debug=False: self
    try:
        resultado = proc.executar(
            auditado_exec,
            resolvedor_aplicabilidade=resolvedor,
            perfil_auditado=perfil,
        )
    finally:
        AcaoVerificacao.executar = orig_executar

    achado = resultado.achado
    assert achado is not None, "Achado deveria ter ocorrido"
    s53_list = [s for s in achado.situacoes_detalhadas if s["id_situacao"] == "S5.3"]
    assert len(s53_list) == 1, f"Esperava 1 única situação detalhada S5.3, encontrou {len(s53_list)}"
    assert s53_list[0]["ativa"] is True
    assert s53_list[0]["descricao"] == "Descrição A para inventário de ativos"
    print("test_agrupamento_interno_por_id: OK!")


def test_motivos_situacoes_por_id():
    """Verifica que nova execução indexa motivos_situacoes exclusivamente por id_situacao (Sx.y)."""
    from argos_classes import ProcedimentoAuditoria, AcaoVerificacao, FonteInformacao

    proc = ProcedimentoAuditoria(
        descricao="Teste chaves motivos",
        logica_achado="AV01",
        numero_achado=1,
        nome_achado="Estrutura de TIC",
        id="PA01",
    )
    fonte = FonteInformacao(descricao="Fonte teste", filepath="none", id="F01")
    acao = AcaoVerificacao(
        id="AV01",
        fonte_informacao=fonte,
        informacao_requerida="info",
        criterio="crit",
        descricao_evidencia="evidencia",
        situacao_inconforme="sit",
        tipo_encaminhamento="Recomendação",
        encaminhamento="enc",
        pre_encaminhamento="pre",
        descricao_situacao_inconforme="Área de TIC sem atribuições formais de gestão de TIC",
        id_situacao="S1.2",
    )
    acao.resultado = True
    proc.adicionar_acao(acao)

    orig_executar = AcaoVerificacao.executar
    AcaoVerificacao.executar = lambda self, aud, debug=False: self
    try:
        class DummyAuditadoExec:
            id = "TESTE"
        resultado = proc.executar(DummyAuditadoExec())
    finally:
        AcaoVerificacao.executar = orig_executar

    achado = resultado.achado
    assert achado is not None
    assert len(achado.motivos_situacoes) > 0
    for chave in achado.motivos_situacoes.keys():
        assert chave.startswith("S"), f"Chave de motivo não estrutural encontrada: '{chave}'"
        assert not chave.startswith("Área"), f"Chave textual legada detectada: '{chave}'"
    print("test_motivos_situacoes_por_id: OK!")


def test_compatibilidade_legada_motivos():
    """Valida normalização automática de JSON legado com chaves textuais para id_situacao."""
    from argos_classes import Achado

    dados_legados = {
        "numero": 1,
        "nome": "Estrutura de TIC",
        "situacoes_encontradas": ["Área de TIC sem atribuições formalmente definidas..."],
        "motivos_situacoes": {
            "Área de TIC sem atribuições formalmente definidas...": [
                {"id_acao": "AV01", "descricao": "Ausência de atribuições formais"}
            ]
        },
        "situacoes_detalhadas": [
            {
                "id_situacao": "S1.2",
                "descricao": "Área de TIC sem atribuições formalmente definidas...",
                "ativa": True,
                "criterios": [],
            }
        ],
    }

    achado = Achado.from_dict(dados_legados)
    assert "S1.2" in achado.motivos_situacoes, "S1.2 deveria estar em motivos_situacoes após normalização"
    assert "Área de TIC sem atribuições formalmente definidas..." not in achado.motivos_situacoes, (
        "Descrição textual legada não deveria permanecer como chave primária em motivos_situacoes"
    )
    assert len(achado.motivos_situacoes["S1.2"]) == 1
    assert achado.motivos_situacoes["S1.2"][0]["descricao"] == "Ausência de atribuições formais"
    print("test_compatibilidade_legada_motivos: OK!")


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
        for tpl_name, _ in ACHADOS_MAP:
            tpl = env.get_template(tpl_name)
            rendered = tpl.render(auditado=auditado)
            if rendered.strip():
                total_instancias += 1

    print(f"test_todos_auditados_renderizam_sem_erro: OK! ({total_auditados} auditados, {total_instancias} achados renderizados)")


if __name__ == "__main__":
    print("Iniciando bateria de testes de consistência de critérios e IDs estáveis...")
    test_cobertura_criterios_templates()
    test_qa_ids_estaveis_templates()
    test_alteracao_editorial_titulo_achado()
    test_alteracao_editorial_descricao_situacao()
    test_semantica_situacao_ativa_independente_de_motivos()
    test_ids_invalidos()
    test_identidade_independente_descricoes_duplicadas()
    test_situacoes_ativas_possuem_motivos_e_criterios()
    test_consistencia_criterios_seel()
    test_todos_criterios_resolvidos_presentes()
    test_agrupamento_interno_por_id()
    test_motivos_situacoes_por_id()
    test_compatibilidade_legada_motivos()
    test_todos_auditados_renderizam_sem_erro()
    print("Todos os testes passaram com 100% de sucesso!")
