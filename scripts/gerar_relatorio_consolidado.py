#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera o arquivo DOCX do Relatório Consolidado a partir do Markdown.

Este script processa o Markdown aplicando renderizações de template Jinja2,
referências cruzadas, quebras de página, substituição de underlines do Pandoc
e formatação de tabelas, utilizando o template de estilos do Argos.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
import json
import logging
import os
import re
import sys
import tempfile
import zipfile
from pathlib import Path

from lxml import etree

# Configura path para importar utilitários da pasta resources
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "resources"))
from argos_utils import (
    cross_ref_figuras,
    processar_quebras_pagina,
    cross_ref_tabelas,
    substituir_underline_pandoc,
    aplicar_estilo_tabelas,
    evitar_quebra_elementos,
    inserir_campo_sumario_docx,
    marcar_atualizacao_campos_docx,
    data_hoje_abnt,
    data_hoje,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
TOC_MARKER_FILTER = Path(__file__).resolve().parent / "resources" / "toc-marker.lua"
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = f"{{{W_NS}}}"


def _texto_elemento_docx(elemento) -> str:
    return "".join(
        no.text or ""
        for no in elemento.iter()
        if no.tag.endswith("}t")
    )


def _localizar_ultimo_elemento_docx(documento, texto: str) -> int:
    correspondencias = [
        indice
        for indice, elemento in enumerate(documento.element.body)
        if _texto_elemento_docx(elemento).strip() == texto
    ]
    if not correspondencias:
        raise ValueError(f"Elemento {texto!r} não encontrado no DOCX.")
    return correspondencias[-1]


def _remover_corpo_antes_de(documento, texto: str) -> None:
    indice = _localizar_ultimo_elemento_docx(documento, texto)
    body = documento.element.body
    for elemento in list(body)[:indice]:
        body.remove(elemento)


def _remover_corpo_a_partir_de(documento, texto: str) -> None:
    from docx.oxml.ns import qn

    indice = _localizar_ultimo_elemento_docx(documento, texto)
    body = documento.element.body
    for elemento in list(body)[indice:]:
        if elemento.tag != qn("w:sectPr"):
            body.remove(elemento)


def _substituir_texto_paragrafo(paragrafo, texto: str, *, negrito_rotulo: str | None = None) -> None:
    for run in paragrafo.runs:
        run._element.getparent().remove(run._element)
    if negrito_rotulo and texto.startswith(negrito_rotulo):
        run_rotulo = paragrafo.add_run(negrito_rotulo)
        run_rotulo.bold = True
        paragrafo.add_run(texto[len(negrito_rotulo):])
    else:
        paragrafo.add_run(texto)


def _preencher_celula_com_paragrafos(celula, paragrafos_origem) -> None:
    for paragrafo in list(celula.paragraphs):
        paragrafo._element.getparent().remove(paragrafo._element)
    for paragrafo in paragrafos_origem:
        celula._tc.append(deepcopy(paragrafo._element))


def _atualizar_capa_modelo(modelo, conteudo) -> None:
    """Atualiza os dados variáveis da capa preservando o desenho institucional."""
    tabela_processo = modelo.tables[0]
    dados_processo = [
        ("Processo:", "101.088-0/2026"),
        ("Origem:", "SIGILOSO"),
        ("Natureza:", "RELATÓRIO DE AUDITORIA GOVERNAMENTAL - AUDITORIA DE CONFORMIDADE"),
        (
            "Observação:",
            "Avaliar o grau de adoção das organizações públicas jurisdicionadas às boas práticas "
            "de governança e gestão de tecnologia da informação e comunicação, por meio do iGovTI 2026.",
        ),
    ]
    celula_processo = tabela_processo.cell(0, 0)
    while len(celula_processo.paragraphs) < len(dados_processo):
        celula_processo.add_paragraph()
    for paragrafo, (rotulo, valor) in zip(celula_processo.paragraphs, dados_processo):
        _substituir_texto_paragrafo(
            paragrafo,
            f"{rotulo} {valor}",
            negrito_rotulo=rotulo,
        )

    tabela_modelo = modelo.tables[1]
    tabela_conteudo = conteudo.tables[0]
    if len(tabela_modelo.rows) != len(tabela_conteudo.rows):
        raise ValueError("A tabela de dados da fiscalização diverge da estrutura do modelo.")
    for linha_modelo, linha_conteudo in zip(tabela_modelo.rows, tabela_conteudo.rows):
        for celula_modelo, celula_conteudo in zip(linha_modelo.cells, linha_conteudo.cells):
            _preencher_celula_com_paragrafos(celula_modelo, celula_conteudo.paragraphs)

    # O cabeçalho do modelo inclui o número do processo em caixas de texto VML,
    # que não são expostas como runs pelo python-docx.
    for secao in modelo.sections:
        for no in secao.header._element.iter():
            if no.tag.endswith("}t") and no.text:
                no.text = no.text.replace("101.088-0/26", "101.088-0/2026")


def _mapear_estilos_equivalentes(documento_origem, documento_destino) -> dict[str, str]:
    """Mapeia IDs de estilos pelo nome, pois cada DOCX pode usar IDs distintos."""
    destino_por_nome = {
        estilo.name.casefold(): estilo.style_id
        for estilo in documento_destino.styles
        if estilo.name
    }
    return {
        estilo.style_id: destino_por_nome[estilo.name.casefold()]
        for estilo in documento_origem.styles
        if estilo.name and estilo.name.casefold() in destino_por_nome
    }


def _normalizar_estilos_notas_rodape(
    docx_path: Path,
    estilos_equivalentes: dict[str, str],
) -> None:
    """Reassocia estilos das notas após a composição com o modelo institucional.

    O docxcompose converte as referências no corpo, mas pode manter em
    ``footnotes.xml`` os IDs do documento anexado. Se esses IDs não existem no
    documento principal, o Word exibe a nota com a formatação padrão.
    """
    with zipfile.ZipFile(docx_path, "r") as entrada:
        footnotes = etree.fromstring(entrada.read("word/footnotes.xml"))
        alteracoes = 0
        for atributo_estilo in footnotes.findall(f".//{W}pStyle") + footnotes.findall(
            f".//{W}rStyle"
        ):
            estilo_origem = atributo_estilo.get(f"{W}val")
            estilo_destino = estilos_equivalentes.get(estilo_origem)
            if estilo_destino and estilo_destino != estilo_origem:
                atributo_estilo.set(f"{W}val", estilo_destino)
                alteracoes += 1

        if not alteracoes:
            return

        itens_docx = [
            (item, entrada.read(item.filename))
            for item in entrada.infolist()
        ]

    with tempfile.NamedTemporaryFile(
        suffix=".docx",
        dir=docx_path.parent,
        delete=False,
    ) as arquivo_temporario:
        caminho_temporario = Path(arquivo_temporario.name)

    try:
        with zipfile.ZipFile(caminho_temporario, "w") as saida:
            for item, dados in itens_docx:
                if item.filename == "word/footnotes.xml":
                    dados = etree.tostring(
                        footnotes,
                        xml_declaration=True,
                        encoding="UTF-8",
                        standalone=True,
                    )
                saida.writestr(item, dados)
        os.replace(caminho_temporario, docx_path)
    finally:
        if caminho_temporario.exists():
            caminho_temporario.unlink()


def _validar_estilos_notas_rodape(docx_path: Path) -> int:
    """Valida os estilos das notas efetivamente referenciadas no relatório."""
    with zipfile.ZipFile(docx_path, "r") as arquivo:
        estilos = etree.fromstring(arquivo.read("word/styles.xml"))
        documento = etree.fromstring(arquivo.read("word/document.xml"))
        footnotes = etree.fromstring(arquivo.read("word/footnotes.xml"))

    estilos_definidos = {
        estilo.get(f"{W}styleId") for estilo in estilos.findall(f"{W}style")
    }
    notas_referenciadas = {
        referencia.get(f"{W}id")
        for referencia in documento.findall(f".//{W}footnoteReference")
    }
    estilos_ausentes: set[tuple[str, str]] = set()
    notas_encontradas = 0
    for nota in footnotes.findall(f"{W}footnote"):
        nota_id = nota.get(f"{W}id")
        if nota_id not in notas_referenciadas:
            continue
        notas_encontradas += 1
        for no_estilo in nota.findall(f".//{W}pStyle") + nota.findall(f".//{W}rStyle"):
            estilo_id = no_estilo.get(f"{W}val")
            if estilo_id and estilo_id not in estilos_definidos:
                estilos_ausentes.add((nota_id, estilo_id))

    if notas_encontradas != len(notas_referenciadas):
        raise ValueError(
            "Há referências de nota de rodapé sem definição correspondente: "
            f"{len(notas_referenciadas) - notas_encontradas}."
        )
    if estilos_ausentes:
        detalhes = ", ".join(
            f"nota {nota_id}: {estilo_id}"
            for nota_id, estilo_id in sorted(estilos_ausentes)
        )
        raise ValueError(f"Notas de rodapé referenciam estilos inexistentes: {detalhes}")
    return notas_encontradas


def _configurar_faixas_horizontais_tabelas(documento) -> int:
    """Mantém faixas horizontais e desativa faixas verticais nas tabelas."""
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    atributos_bits = {
        "firstRow": 0x0020,
        "lastRow": 0x0040,
        "firstColumn": 0x0080,
        "lastColumn": 0x0100,
        "noHBand": 0x0200,
        "noVBand": 0x0400,
    }
    for tabela in documento.tables:
        propriedades = tabela._tbl.tblPr
        tbl_look = propriedades.find(qn("w:tblLook"))
        if tbl_look is None:
            tbl_look = OxmlElement("w:tblLook")
            propriedades.append(tbl_look)

        tbl_look.set(qn("w:noHBand"), "0")
        tbl_look.set(qn("w:noVBand"), "1")

        # w:val duplica os atributos individuais em uma máscara hexadecimal.
        # Mantê-los coerentes evita interpretações diferentes entre editores.
        mascara = 0
        for atributo, bit in atributos_bits.items():
            if tbl_look.get(qn(f"w:{atributo}"), "0") == "1":
                mascara |= bit
        tbl_look.set(qn("w:val"), f"{mascara:04X}")

    return len(documento.tables)


def _validar_faixas_horizontais_tabelas(
    docx_path: Path,
    quantidade_esperada: int,
) -> int:
    """Confirma que tabelas de relatório usam linhas, não colunas, alternadas."""
    with zipfile.ZipFile(docx_path, "r") as arquivo:
        estilos = etree.fromstring(arquivo.read("word/styles.xml"))
        documento = etree.fromstring(arquivo.read("word/document.xml"))

    estilos_tabela = set()
    for estilo in estilos.findall(f"{W}style"):
        nome = estilo.find(f"{W}name")
        if nome is not None and nome.get(f"{W}val", "").casefold() == "table":
            estilos_tabela.add(estilo.get(f"{W}styleId"))

    tabelas_relatorio = []
    configuracoes_incorretas = []
    for indice, tabela in enumerate(documento.findall(f".//{W}tbl")):
        estilo = tabela.find(f"./{W}tblPr/{W}tblStyle")
        if estilo is None or estilo.get(f"{W}val") not in estilos_tabela:
            continue
        tabelas_relatorio.append(indice)
        tbl_look = tabela.find(f"./{W}tblPr/{W}tblLook")
        if (
            tbl_look is None
            or tbl_look.get(f"{W}noHBand") != "0"
            or tbl_look.get(f"{W}noVBand") != "1"
        ):
            configuracoes_incorretas.append(indice)

    if len(tabelas_relatorio) != quantidade_esperada:
        raise ValueError(
            "Quantidade inesperada de tabelas do relatório após a composição: "
            f"esperadas {quantidade_esperada}, encontradas {len(tabelas_relatorio)}."
        )
    if configuracoes_incorretas:
        raise ValueError(
            "Há tabelas com faixas verticais habilitadas ou faixas horizontais "
            f"desabilitadas: {configuracoes_incorretas}."
        )
    return len(tabelas_relatorio)


def aplicar_paginas_institucionais(
    docx_gerado: Path,
    modelo_path: Path,
) -> None:
    """Compõe capa e sumário do modelo com lista de anexos e corpo atuais.

    O reference-docx do Pandoc transfere estilos, mas não o conteúdo pré-textual.
    Esta etapa preserva a capa e a página de sumário do modelo e incorpora, do
    documento recém-gerado, a lista de anexos e todo o relatório a partir dela.
    """
    try:
        from docxcompose.composer import Composer
    except ImportError as exc:
        raise RuntimeError(
            "docxcompose é necessário para aplicar as páginas institucionais do modelo."
        ) from exc

    if not modelo_path.exists():
        raise FileNotFoundError(f"Modelo institucional não encontrado: {modelo_path}")

    documento_modelo = docx.Document(str(modelo_path))
    documento_conteudo = docx.Document(str(docx_gerado))
    estilos_equivalentes = _mapear_estilos_equivalentes(
        documento_conteudo,
        documento_modelo,
    )
    _atualizar_capa_modelo(documento_modelo, documento_conteudo)

    # Mantém do modelo a capa e a página do sumário; a lista de anexos vem da
    # fonte Markdown atual para evitar que o modelo legado se torne fonte de dados.
    _remover_corpo_a_partir_de(documento_modelo, "LISTA DE ANEXOS")
    _remover_corpo_antes_de(documento_conteudo, "LISTA DE ANEXOS")
    total_tabelas = _configurar_faixas_horizontais_tabelas(documento_conteudo)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        modelo_recortado = temp_dir_path / "modelo-frontispicio.docx"
        conteudo_recortado = temp_dir_path / "conteudo-relatorio.docx"
        documento_modelo.save(modelo_recortado)
        documento_conteudo.save(conteudo_recortado)

        principal = docx.Document(str(modelo_recortado))
        compositor = Composer(principal)
        compositor.append(docx.Document(str(conteudo_recortado)))
        compositor.save(str(docx_gerado))

    _normalizar_estilos_notas_rodape(docx_gerado, estilos_equivalentes)
    total_notas = _validar_estilos_notas_rodape(docx_gerado)
    logger.info("Notas de rodapé validadas após a composição: %d", total_notas)
    total_tabelas = _validar_faixas_horizontais_tabelas(
        docx_gerado,
        total_tabelas,
    )
    logger.info(
        "Tabelas validadas com faixas somente horizontais: %d",
        total_tabelas,
    )
    marcar_atualizacao_campos_docx(str(docx_gerado))
REFERENCE_LABEL_RE = re.compile(r"\{#(?:fig|tbl):[^#\r\n]+#\}")


def proteger_rotulos_referencias(conteudo: str) -> tuple[str, dict[str, str]]:
    """Protege labels de figuras/tabelas para que o Jinja não os trate como comentários."""
    rotulos: dict[str, str] = {}

    def substituir(match: re.Match[str]) -> str:
        token = f"@@ARGOS_REFERENCE_LABEL_{len(rotulos)}@@"
        if token in conteudo:
            raise ValueError(f"Token interno de proteção já existe no Markdown: {token}")
        rotulos[token] = match.group(0)
        return token

    return REFERENCE_LABEL_RE.sub(substituir, conteudo), rotulos


def restaurar_rotulos_referencias(conteudo: str, rotulos: dict[str, str]) -> str:
    """Restaura os labels que permaneceram após a renderização Jinja."""
    for token, rotulo in rotulos.items():
        conteudo = conteudo.replace(token, rotulo)
    return conteudo

# Tenta importar as bibliotecas necessárias
try:
    import pypandoc
except ImportError:
    logger.error(
        "pypandoc não está instalado neste ambiente Python. Execute o script utilizando o ambiente virtual do projeto: "
        "  scripts/.venv/bin/python scripts/gerar_relatorio_consolidado.py"
    )
    sys.exit(1)

try:
    import docx
except ImportError:
    logger.error(
        "python-docx não está instalado neste ambiente Python. Execute o script utilizando o ambiente virtual do projeto: "
        "  scripts/.venv/bin/python scripts/gerar_relatorio_consolidado.py"
    )
    sys.exit(1)



def main() -> int:
    parser = argparse.ArgumentParser(
        description="Gera o arquivo DOCX do Relatório Consolidado a partir do Markdown."
    )
    parser.add_argument(
        "input_positional",
        nargs="?",
        default=None,
        help="Caminho do arquivo Markdown de entrada (posicional)."
    )
    parser.add_argument(
        "--input",
        default=None,
        help="Caminho do arquivo Markdown de entrada."
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Caminho do arquivo DOCX de saída gerado. Se omitido, usa o mesmo nome do arquivo de entrada com extensão .docx."
    )
    parser.add_argument(
        "--reference-docx",
        default="scripts/resources/template-base-estilos.docx",
        help="Caminho para o documento de estilos do Word usado como referência."
    )
    parser.add_argument(
        "--modelo-institucional",
        default=None,
        help=(
            "DOCX cuja capa e página de sumário serão aplicadas após a conversão. "
            "A lista de anexos e o corpo permanecem provenientes do Markdown atual."
        ),
    )
    parser.add_argument(
        "--resource-files", "--resource-dirs",
        nargs="*",
        default=[],
        dest="resource_files",
        help="Diretórios adicionais, arquivos ou padrões glob (wildcards) contendo recursos de contexto."
    )
    parser.add_argument(
        "--context-json",
        default=None,
        help="Caminho para um arquivo JSON contendo variáveis de contexto para renderização Jinja2."
    )
    parser.add_argument(
        "--context-vars",
        nargs="*",
        default=[],
        help="Parâmetros de contexto adicionais chave=valor (ex: sigla=FTM ano=2026)."
    )
    parser.add_argument("--resultados-2026", default=None, help="XLSX de resultados iGovTI 2026 usado para gerar gráficos do relatório consolidado.")
    parser.add_argument("--respostas-2026", default=None, help="XLSX de respostas do questionário usado para gerar gráficos do relatório consolidado.")
    parser.add_argument("--comparavel-2026", default=None, help="XLSX iGovTI 2026 ajustado comparável usado para gerar gráficos do relatório consolidado.")
    parser.add_argument("--setic-2023", default=None, help="XLSX comparável do SETIC 2023 usado para gerar gráficos do relatório consolidado.")
    parser.add_argument("--municipios-2023", default=None, help="XLSX comparável dos municípios 2023 usado para gerar gráficos do relatório consolidado.")
    parser.add_argument("--auditados-xlsx", default=None, help="Base de auditados XLSX usada para gerar gráficos consolidados de achados.")
    parser.add_argument("--resultado-auditoria-json", default=None, help="Resultado estruturado da auditoria em JSON usado para gerar gráficos consolidados de achados.")
    parser.add_argument("--mapa", default=None, help="Mapa de verificação revisado usado nos perfis das questões Q1 a Q6.")
    args = parser.parse_args()

    input_str = args.input_positional or args.input or "03-Relatorios/01-Relatorio_Consolidado/Relatório_altaresolucao_novo.md"
    input_path = Path(input_str)
    
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_suffix(".docx")

    ref_path = Path(args.reference_docx)

    if not input_path.exists():
        logger.error("Arquivo de entrada não encontrado: %s", input_path)
        return 1

    if not ref_path.exists():
        logger.error("Documento de referência de estilos não encontrado: %s", ref_path)
        return 1

    logger.info("Lendo markdown: %s", input_path)
    conteudo = input_path.read_text(encoding="utf-8")

    # 1. Resolve variáveis de contexto para renderização Jinja2
    contexto = {
        "data_hoje_abnt": data_hoje_abnt(),
        "data_hoje": data_hoje(),
    }
    if args.context_json:
        context_json_path = Path(args.context_json)
        if context_json_path.exists():
            logger.info("Carregando variáveis do arquivo JSON: %s", context_json_path)
            contexto.update(json.loads(context_json_path.read_text(encoding="utf-8")))
        else:
            logger.warning("Arquivo JSON de contexto não encontrado: %s", context_json_path)

    if args.context_vars:
        for item in args.context_vars:
            if "=" in item:
                k, v = item.split("=", 1)
                contexto[k.strip()] = v.strip()

    # 2. Renderiza como Jinja2 se houver tags de template. Os labels
    # {#fig:...#}/{#tbl:...#} precisam ser protegidos porque essa sintaxe
    # também representa comentários para o Jinja.
    if "{{" in conteudo or "{%" in conteudo:
        logger.info("Renderizando variáveis do template com Jinja2...")
        try:
            from jinja2 import Template
            conteudo_protegido, rotulos_referencias = proteger_rotulos_referencias(conteudo)
            template = Template(conteudo_protegido)
            conteudo = restaurar_rotulos_referencias(
                template.render(contexto),
                rotulos_referencias,
            )
        except Exception as e:
            logger.error("Erro ao renderizar template Jinja2: %s", e)
            return 1

    # 3. Aplica os processamentos de marcação herdados do Argos
    conteudo_processado = cross_ref_figuras(conteudo)
    conteudo_processado = cross_ref_tabelas(conteudo_processado)
    conteudo_processado = inserir_campo_sumario_docx(conteudo_processado)
    conteudo_processado = processar_quebras_pagina(conteudo_processado)
    conteudo_processado = substituir_underline_pandoc(conteudo_processado)

    # Cria arquivo temporário para o markdown intermediário
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", encoding="utf-8", delete=False) as temp_md:
        temp_md.write(conteudo_processado)
        temp_md_name = temp_md.name

    with tempfile.TemporaryDirectory() as temp_resources_dir:
        temp_img_dir = os.path.join(temp_resources_dir, "img")
        os.makedirs(temp_img_dir, exist_ok=True)
        
        # 4. Executa a geração de gráficos gerais consolidados na pasta temporária
        import subprocess
        import shutil
        
        script_gerais = os.path.join(os.path.dirname(__file__), "gerar_graficos_relatorios_consolidado_individuais_igovti.py")
        logger.info("Executando a geração de gráficos gerais consolidados no diretório temporário...")
        try:
            cmd_graficos_gerais = [sys.executable, script_gerais, "--somente-consolidados", "--output-root", temp_resources_dir]
            for option, value in [
                ("--resultados-2026", args.resultados_2026),
                ("--respostas-2026", args.respostas_2026),
                ("--comparavel-2026", args.comparavel_2026),
                ("--setic-2023", args.setic_2023),
                ("--municipios-2023", args.municipios_2023),
                ("--mapa", args.mapa),
            ]:
                if value:
                    cmd_graficos_gerais.extend([option, value])
            # Executa com o mesmo interpretador python
            subprocess.run(
                cmd_graficos_gerais,
                check=True,
                stdout=subprocess.DEVNULL
            )
        except Exception as e:
            logger.error("Erro ao gerar gráficos gerais: %s", e)
            return 1

        # Executa a geração de gráficos de achados diretamente para a pasta temporária
        script_achados = os.path.join(os.path.dirname(__file__), "gerar_graficos_achados_consolidado.py")
        logger.info("Executando a geração de gráficos de achados no diretório temporário...")
        try:
            cmd_graficos_achados = [sys.executable, script_achados, "--output-dir", temp_resources_dir]
            if args.auditados_xlsx:
                cmd_graficos_achados.extend(["--auditados", args.auditados_xlsx])
            if args.resultado_auditoria_json:
                cmd_graficos_achados.extend(["--resultado-auditoria-json", args.resultado_auditoria_json])
            subprocess.run(
                cmd_graficos_achados,
                check=True,
                stdout=subprocess.DEVNULL
            )
        except Exception as e:
            logger.error("Erro ao gerar gráficos de achados: %s", e)
            return 1
            
        # 5. Copia imagens de contexto de outros locais (se existirem / especificados) para consolidar na pasta temporária
        tmp_root = Path("C:/tmp") if sys.platform.startswith("win") else Path(tempfile.gettempdir())
        tmp_pkg = tmp_root / "tcerj-igovti-2026"
        tmp_consolidado_img = str(tmp_pkg / "relatorio-consolidado" / "img")
        tmp_individuais_img = str(tmp_pkg / "relatorios-individuais" / "img")
        
        resource_inputs = [
            tmp_consolidado_img,
            tmp_individuais_img,
            "03-Relatorios/01-Relatorio_Consolidado/img",
            "03-Relatorios/99-Avaliacao_IA/img",
        ]
        if args.resource_files:
            resource_inputs.extend(args.resource_files)
            
        # Resolve wildcards/globs primeiro
        import glob
        import zipfile
        
        resolved_paths = []
        for r_path in resource_inputs:
            if not r_path:
                continue
            # Verifica se contém caracteres wildcard
            if any(char in r_path for char in ['*', '?', '[']):
                expanded = glob.glob(r_path, recursive=True)
                if expanded:
                    resolved_paths.extend([p for p in expanded if os.path.exists(p)])
                else:
                    logger.warning("Nenhum recurso encontrado para o padrão: %r", r_path)
            else:
                resolved_paths.append(r_path)

        for r_path in resolved_paths:
            if not os.path.exists(r_path):
                continue

            if os.path.isdir(r_path):
                for root, _, files in os.walk(r_path):
                    for filename in files:
                        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                            src_file = os.path.join(root, filename)
                            dest_file = os.path.join(temp_img_dir, filename)
                            if not os.path.exists(dest_file):
                                shutil.copy2(src_file, dest_file)
            elif r_path.lower().endswith('.zip'):
                try:
                    with tempfile.TemporaryDirectory() as unzip_tmp:
                        with zipfile.ZipFile(r_path, 'r') as zip_ref:
                            zip_ref.extractall(unzip_tmp)
                        for root, _, files in os.walk(unzip_tmp):
                            for filename in files:
                                if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                                    src_file = os.path.join(root, filename)
                                    dest_file = os.path.join(temp_img_dir, filename)
                                    if not os.path.exists(dest_file):
                                        shutil.copy2(src_file, dest_file)
                except Exception as e:
                    logger.error("Erro ao extrair zip de recursos %r: %s", r_path, e)
            else:
                # Arquivo normal
                filename = os.path.basename(r_path)
                if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                    dest_file = os.path.join(temp_img_dir, filename)
                    if not os.path.exists(dest_file):
                        shutil.copy2(r_path, dest_file)

        # Planifica todas as imagens encontradas nas subpastas do diretório temporário
        # colocando-as também na raiz de temp_resources_dir para que o Pandoc as encontre
        # diretamente quando referenciadas por nome simples (sem prefixo de pasta)
        for root, _, files in os.walk(temp_resources_dir):
            if root == temp_resources_dir:
                continue
            for filename in files:
                if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                    src_file = os.path.join(root, filename)
                    dest_file_root = os.path.join(temp_resources_dir, filename)
                    if not os.path.exists(dest_file_root):
                        shutil.copy2(src_file, dest_file_root)


        try:
            logger.info("Compilando com Pandoc para DOCX usando template de referência: %s", ref_path)
            
            # Garante diretórios de recursos para o Pandoc
            resource_paths = [
                ".",
                temp_resources_dir,
                str(input_path.parent),
                os.path.dirname(args.reference_docx)
            ]
            resource_path_arg = '--resource-path=' + os.pathsep.join(resource_paths)
            
            extra_args = [
                '--figure-caption-position=above',
                '--reference-doc=' + str(ref_path),
                resource_path_arg
            ]
            if TOC_MARKER_FILTER.exists():
                extra_args.append('--lua-filter=' + str(TOC_MARKER_FILTER))

            # Executa conversão
            output_path.parent.mkdir(parents=True, exist_ok=True)
            pypandoc.convert_file(
                temp_md_name,
                to="docx",
                outputfile=str(output_path),
                extra_args=extra_args
            )

            logger.info("Aplicando estilos de tabela pós-conversão no DOCX...")
            aplicar_estilo_tabelas(str(output_path))

            logger.info("Ajustando layout para evitar quebras órfãs de figuras, tabelas e fontes...")
            evitar_quebra_elementos(str(output_path))

            logger.info("Marcando campos do DOCX para atualização ao abrir no Word...")
            marcar_atualizacao_campos_docx(str(output_path))

            if args.modelo_institucional:
                logger.info(
                    "Aplicando capa e sumário do modelo institucional: %s",
                    args.modelo_institucional,
                )
                aplicar_paginas_institucionais(
                    output_path,
                    Path(args.modelo_institucional),
                )

            logger.info("Relatório DOCX gerado com sucesso em: %s", output_path)
            return 0

        except Exception as e:
            logger.error("Erro durante a geração do relatório: %s", e)
            return 1
        finally:
            if os.path.exists(temp_md_name):
                os.remove(temp_md_name)


if __name__ == "__main__":
    sys.exit(main())
