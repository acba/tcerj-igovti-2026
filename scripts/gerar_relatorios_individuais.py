#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import io
import json
import zipfile
import tempfile
import ast
import logging
import argparse
import glob
import shutil
import pandas as pd
import docx
from docxtpl import DocxTemplate
from jinja2 import Environment, BaseLoader, StrictUndefined

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "resources"))

from argos_classes import Auditado, ProcedimentoAuditoria
from argos_utils import (
    get_variaveis_template,
    processa_imagens_contexto,
    cross_ref_figuras,
    cross_ref_tabelas,
    data_hoje_abnt,
    data_hoje,
    aplicar_estilo_tabelas,
    aplicar_fonte_justificativas_avaliacao,
    evitar_quebra_elementos,
    inserir_campo_sumario_docx,
    marcar_atualizacao_campos_docx,
    processar_quebras_pagina,
    substituir_underline_pandoc
)

TOC_MARKER_FILTER = os.path.join(os.path.dirname(__file__), "resources", "toc-marker.lua")

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def normalizar_texto_ajuste(val):
    if pd.isna(val):
        return ""
    s = str(val).strip().lower()
    return s.replace("ã", "a").replace("õ", "o").replace("é", "e").replace("á", "a").replace("í", "i")

def is_nao_conforme_ajuste(val):
    return normalizar_texto_ajuste(val) in ("nao conforme", "nao_conforme", "nao-conforme")

def valor_texto(val, vazio=""):
    if pd.isna(val) or str(val).strip() == "" or str(val).strip().lower() in ("nan", "none"):
        return vazio
    return str(val).strip()

def justificativa_pos_comentarios_exibicao(valor):
    """Remove da comunicação final digressões sobre a antiga data-base."""
    texto_original = valor_texto(valor)
    frases = re.split(r"(?<=[.!?])\s+", texto_original)
    marca_historica = re.compile(
        r"data[- ]base|período da auditoria|época da auditoria|correç(?:ão|ao) posterior|regulariza(?:ção|cao) após",
        re.IGNORECASE,
    )
    limpas = [frase for frase in frases if not marca_historica.search(frase)]
    resultado = " ".join(limpas).strip()
    resultado = re.sub(r"^Ajuste pós-comentários do gestor:\s*situação\s+\S+\.\s*", "", resultado, flags=re.I)
    return resultado or "Ajuste decorrente da avaliação dos comentários e evidências apresentados pelo gestor."

def normalizar_valor_contexto(val):
    if isinstance(val, (list, tuple, dict, set)):
        return val
    if pd.isna(val):
        return ""
    return val

def resposta_ajustada_exibicao(item_codigo, resposta_afirmada, resposta_ajustada=None):
    if resposta_ajustada is not None and not pd.isna(resposta_ajustada):
        text = str(resposta_ajustada).strip()
        if text and text.lower() not in ("nan", "none", "vazio"):
            return text
        if text.lower() == "vazio":
            return ""

    item = str(item_codigo or "").strip()
    afirmada = valor_texto(resposta_afirmada)
    if "ext" in item.lower() or "[" in item:
        if afirmada.lower() in ("sim", "y"):
            return "Não" if afirmada.lower() == "sim" else ""
        return ""
    if re.match(r"^q\d{4}$", item.lower()):
        return "Não adota." if afirmada.endswith(".") else "Não adota"
    return ""

def carregar_ajustes_respostas(path):
    if not path:
        return {}
    if not os.path.exists(path):
        logger.warning(f"Planilha de ajustes de respostas '{path}' não encontrada. Apêndice B não será preenchido.")
        return {}

    try:
        df = pd.read_excel(path)
    except Exception as e:
        logger.error(f"Erro ao ler planilha de ajustes de respostas '{path}': {e}")
        return {}

    ajustes_por_auditado = {}
    for _, row in df.iterrows():
        auditado = row.get("Auditado")
        item_codigo = row.get("Código do item")
        if pd.isna(item_codigo):
            item_codigo = row.get("Código do item avaliado")
        if pd.isna(auditado) or pd.isna(item_codigo):
            continue

        resposta_ajustada_planilha = row.get("Resposta ajustada") if "Resposta ajustada" in df.columns else None

        if "Resposta ajustada" not in df.columns:
            revisor_val = row.get("Avaliação do auditor revisor")
            juiz_val = row.get("Resultado da avaliação do juiz")
            tem_revisor = pd.notna(revisor_val) and str(revisor_val).strip() != "" and normalizar_texto_ajuste(revisor_val) != "sem_parecer"
            resultado_final = revisor_val if tem_revisor else juiz_val
            if not is_nao_conforme_ajuste(resultado_final):
                continue
            justificativa = row.get("Justificativa do auditor revisor") if tem_revisor else row.get("Justificativa do juiz")
        else:
            justificativa = row.get("Justificativa")
            if pd.isna(justificativa):
                justificativa = row.get("observacao")
            if valor_texto(row.get("Origem")).startswith("secao_"):
                justificativa = justificativa_pos_comentarios_exibicao(justificativa)

        resposta_afirmada = row.get("Resposta afirmada")
        ajuste = {
            "codigo_questao": str(item_codigo).strip(),
            "de": valor_texto(resposta_afirmada, vazio="Vazio"),
            "para": valor_texto(
                resposta_ajustada_exibicao(item_codigo, resposta_afirmada, resposta_ajustada_planilha),
                vazio="Vazio",
            ),
            "justificativa": valor_texto(justificativa, vazio="Sem justificativa registrada"),
        }
        ajustes_por_auditado.setdefault(str(auditado).strip().upper(), []).append(ajuste)

    logger.info(f"Carregados ajustes de respostas para {len(ajustes_por_auditado)} auditado(s) a partir de '{path}'.")
    return ajustes_por_auditado

def carregar_contexto_comentarios_gestor(path):
    """Carrega o produto de comunicação pós-comentários indexado pela sigla."""
    if not path:
        return {}
    if not os.path.exists(path):
        logger.warning("Contexto de comentários do gestor '%s' não encontrado.", path)
        return {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except Exception as e:
        logger.error("Erro ao ler contexto de comentários do gestor '%s': %s", path, e)
        return {}
    if not isinstance(dados, dict):
        logger.error("Contexto de comentários do gestor deve ser um objeto indexado por sigla.")
        return {}
    return {str(k).strip().upper(): v for k, v in dados.items() if isinstance(v, dict)}

def consolidar_templates(base_content, all_files_content, template_paths, processed_files=None):
    """
    Consolidates templates by replacing {% include 'filename' %} with the file's content,
    searching both in the provided files and in the directories of the template paths.
    """
    if processed_files is None:
        processed_files = set()

    pattern = re.compile(r"\{%-?\s*include\s+['\"](.+?)['\"]\s*-?%\}")

    def replace_match(match):
        filename = match.group(1)

        # If not already loaded, try to load it from the directories of the supplied templates
        if filename not in all_files_content:
            for t_path in template_paths:
                dir_path = os.path.dirname(t_path)
                full_path = os.path.join(dir_path, filename)
                if os.path.exists(full_path):
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            all_files_content[filename] = f.read()
                        break
                    except Exception as e:
                        logger.warning(f"Failed to read included file '{full_path}': {e}")

        if filename in all_files_content:
            if filename in processed_files:
                return f"<!-- ERRO: Ciclo de inclusão detectado para '{filename}' -->"

            new_processed = processed_files.copy()
            new_processed.add(filename)

            return consolidar_templates(all_files_content[filename], all_files_content, template_paths, new_processed)
        else:
            return f"<!-- ERRO: Arquivo '{filename}' não encontrado -->"

    return pattern.sub(replace_match, base_content)

def get_variaveis_definidas_no_template(template_content):
    """Coleta nomes declarados em blocos Jinja, para não tratá-los como contexto externo."""
    if not template_content:
        return set()

    definidas = set()
    for match in re.finditer(r"\{%-?\s*set\s+([A-Za-z_]\w*)\s*=", template_content):
        definidas.add(match.group(1))

    for match in re.finditer(r"\{%-?\s*for\s+(.+?)\s+in\s+.+?%}", template_content):
        targets = match.group(1).strip()
        for target in targets.split(","):
            target = target.strip()
            if re.fullmatch(r"[A-Za-z_]\w*", target):
                definidas.add(target)

    return definidas

def main():
    parser = argparse.ArgumentParser(
        description='Gerador de Relatórios Individuais do Argos via Linha de Comando.'
    )
    parser.add_argument(
        '--auditados', required=True,
        help='Caminho para o arquivo JSON contendo o contexto dos auditados (ex: resultado_auditoria.json).'
    )
    parser.add_argument(
        '--templates', nargs='+', required=True,
        help='Caminho para um ou mais arquivos de template (.md, .jinja, ou .docx).'
    )
    parser.add_argument(
        '--context-files', nargs='*', default=[],
        help='Caminho para planilhas Excel (.xlsx) contendo variáveis adicionais indexadas por "sigla".'
    )
    parser.add_argument(
        '--resource-files', nargs='*', default=[],
        help='Caminho para arquivos/diretórios de recursos (ex: imagens ou arquivos ZIP) referenciados no contexto.'
    )
    parser.add_argument(
        '--auditados-select', nargs='*', default=[],
        help='Lista de siglas dos auditados a serem processados. Se omitido, processa todos do JSON.'
    )
    parser.add_argument(
        '--output-dir', default='.output_reports',
        help='Diretório onde os relatórios gerados serão salvos (padrão: .output_reports).'
    )
    parser.add_argument(
        '--reference-docx', default='scripts/resources/template-base-estilos-sigiloso.docx',
        help='Modelo de referência Word (.docx) usado pelo Pandoc para os estilos (padrão: scripts/resources/template-base-estilos-sigiloso.docx).'
    )
    parser.add_argument(
        '--ajustes-respostas',
        default=None,
        help='Planilha XLSX de ajustes aplicados às respostas para preencher o Apêndice B.'
    )
    parser.add_argument(
        '--contexto-comentarios-gestor',
        default=None,
        help='JSON pós-comentários indexado por sigla, usado na seção de manifestações do relatório final.'
    )
    parser.add_argument(
        '--impactos-comentarios-gestor',
        default=None,
        help='JSON de impactos 02×03 indexado por sigla; obrigatório para preencher o resumo de impacto final.'
    )
    parser.add_argument(
        '--nome-base-docx',
        default='Relatório Individual Preliminar',
        help='Nome base dos arquivos DOCX gerados, antes da sigla do auditado.'
    )
    args = parser.parse_args()
    if args.contexto_comentarios_gestor:
        if not args.impactos_comentarios_gestor:
            parser.error("--impactos-comentarios-gestor é obrigatório com --contexto-comentarios-gestor")
        for label, path in (
            ("contexto", args.contexto_comentarios_gestor),
            ("impactos", args.impactos_comentarios_gestor),
        ):
            if not os.path.isfile(path):
                parser.error(f"JSON de {label} dos comentários não encontrado: {path}")
    contexto_comentarios_por_auditado = carregar_contexto_comentarios_gestor(args.contexto_comentarios_gestor)
    impactos_comentarios_por_auditado = carregar_contexto_comentarios_gestor(args.impactos_comentarios_gestor)
    datas_referencia = {
        str(item.get('data_referencia')).strip()
        for item in contexto_comentarios_por_auditado.values()
        if item.get('data_referencia')
    }
    data_referencia_padrao = next(iter(datas_referencia)) if len(datas_referencia) == 1 else 'não informada'
    for sigla, impacto in impactos_comentarios_por_auditado.items():
        contexto = contexto_comentarios_por_auditado.setdefault(sigla, {
            'data_referencia': data_referencia_padrao,
            'status_produto': 'minuta para revisão final da equipe de auditoria',
            'respondeu': False,
            'situacoes': [],
            'itens_questionario': [],
            'resumo_impacto': {},
        })
        contexto.setdefault('data_referencia', data_referencia_padrao)
        contexto.setdefault('respondeu', False)
        contexto.setdefault('situacoes', [])
        contexto.setdefault('itens_questionario', [])
        contexto['resumo_impacto'] = impacto

    # 1. Load auditados from JSON
    if not os.path.exists(args.auditados):
        logger.error(f"Arquivo de auditados '{args.auditados}' não encontrado.")
        sys.exit(1)

    try:
        with open(args.auditados, 'r', encoding='utf-8') as f:
            auditados_dict = json.load(f)
        auditados = {k: Auditado.from_dict(v) for k, v in auditados_dict.items()}
        logger.info(f"Carregados {len(auditados)} auditados do arquivo JSON.")
    except Exception as e:
        logger.error(f"Erro ao carregar o arquivo JSON de auditados: {e}")
        sys.exit(1)

    # 2. Parse Context Spreadsheets
    df_contexto_extra = None
    if args.context_files:
        dfs_contexto = []
        for path in args.context_files:
            if not os.path.exists(path):
                logger.warning(f"Planilha de contexto '{path}' não encontrada. Ignorando.")
                continue
            try:
                df_temp = pd.read_excel(path)
                if 'sigla' in df_temp.columns:
                    df_temp = df_temp.set_index('sigla')
                    df_temp.columns = [col.strip() for col in df_temp.columns]

                    # Process special columns ending in '*'
                    for col in df_temp.columns:
                        if col.endswith('*'):
                            try:
                                df_temp[col] = df_temp[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
                                df_temp.rename(columns={col: col.rstrip('*')}, inplace=True)
                            except Exception:
                                try:
                                    df_temp[col] = df_temp[col].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
                                    df_temp.rename(columns={col: col.rstrip('*')}, inplace=True)
                                except Exception as e:
                                    logger.warning(f"Falha ao converter coluna especial '{col}' na planilha '{path}': {e}")
                    dfs_contexto.append(df_temp)
                else:
                    logger.warning(f"Planilha '{path}' ignorada: Coluna 'sigla' não encontrada.")
            except Exception as e:
                logger.error(f"Erro ao ler planilha de contexto '{path}': {e}")

    if dfs_contexto:
            df_contexto_extra = pd.concat(dfs_contexto).groupby(level=0).first()
            logger.info("Planilhas de contexto consolidadas com sucesso.")

    ajustes_respostas_por_auditado = carregar_ajustes_respostas(args.ajustes_respostas)

    # 3. Read and Consolidate Templates
    template_content = None
    template_type = None
    template_paths = args.templates

    # Check template extension (take first to determine type)
    first_template_ext = os.path.splitext(template_paths[0])[1].lower()

    if first_template_ext in ('.md', '.jinja', '.txt'):
        template_type = 'md'
        template_files = {}
        for path in template_paths:
            if not os.path.exists(path):
                logger.error(f"Template '{path}' não encontrado.")
                sys.exit(1)
            name = os.path.basename(path)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    template_files[name] = f.read()
            except Exception as e:
                logger.error(f"Erro ao ler template '{path}': {e}")
                sys.exit(1)

        # Detect base file (the one with the most includes, or the first one)
        if len(template_files) > 1:
            include_pattern = re.compile(r"\{%-?\s*include\s+['\"](.+?)['\"]\s*-?%\}")
            base_filename = max(template_files, key=lambda k: len(include_pattern.findall(template_files[k])))
        else:
            base_filename = list(template_files.keys())[0]

        try:
            template_content = consolidar_templates(template_files[base_filename], template_files, template_paths)
            logger.info(f"Templates consolidados usando base: '{base_filename}'")
        except RecursionError:
            logger.error("Erro: Loop de inclusão cíclico detectado nos templates.")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Erro na consolidação de templates: {e}")
            sys.exit(1)

    elif first_template_ext == '.docx':
        template_type = 'docx'
        # docxtpl template path will be passed to rendering engine directly per auditado
        template_content_path = template_paths[0]
        if not os.path.exists(template_content_path):
            logger.error(f"Template Word '{template_content_path}' não encontrado.")
            sys.exit(1)

        # Try reading template text just to get variables
        try:
            doc_sample = docx.Document(template_content_path)
            template_content = "\n".join([para.text for para in doc_sample.paragraphs])
            template_content = template_content.replace("%p", "%").replace('‘', "'").replace('’', "'").replace('“', "'").replace('”', "'")
        except Exception as e:
            logger.warning(f"Não foi possível inspecionar as variáveis do template Word: {e}")
            template_content = ""
    else:
        logger.error("Formato de template não suportado. Utilize .md, .jinja ou .docx.")
        sys.exit(1)

    # 4. Extract variables from template
    vars_template = get_variaveis_template(template_content)
    vars_definidas_template = get_variaveis_definidas_no_template(template_content)
    vars_contexto_template = vars_template - vars_definidas_template
    logger.info(f"Variáveis de contexto encontradas no template: {sorted(list(vars_contexto_template))}")
    if vars_definidas_template:
        logger.debug(f"Variáveis definidas internamente no template: {sorted(list(vars_definidas_template))}")

    # 5. Filter auditados to process
    siglas_selecionadas = args.auditados_select
    if not siglas_selecionadas:
        siglas_selecionadas = list(auditados.keys())

    # Ensure they exist in the loaded JSON
    siglas_selecionadas = [s for s in siglas_selecionadas if s in auditados]
    if not siglas_selecionadas:
        logger.error("Nenhum auditado válido selecionado para processamento.")
        sys.exit(1)

    logger.info(f"Processando relatórios para os auditados: {siglas_selecionadas}")

    # 6. Create Output Directory
    os.makedirs(args.output_dir, exist_ok=True)

    # 7. Set up environment for generation
    env = Environment(loader=BaseLoader(), undefined=StrictUndefined)

    # Prepare resource paths
    with tempfile.TemporaryDirectory() as tmp_dir:
        flat_resources_dir = os.path.join(tmp_dir, "flat_resources")
        os.makedirs(flat_resources_dir, exist_ok=True)

        unzip_dir = os.path.join(tmp_dir, "unzipped_context")
        os.makedirs(unzip_dir, exist_ok=True)

        context_files_path_map = {}

        # Resolve wildcards/globs first
        resolved_paths = []
        for r_path in args.resource_files:
            if any(char in r_path for char in ['*', '?', '[']):
                expanded = glob.glob(r_path, recursive=True)
                if expanded:
                    resolved_paths.extend([p for p in expanded if os.path.isfile(p)])
                else:
                    logger.warning(f"Nenhum arquivo encontrado para o padrão '{r_path}'")
            else:
                resolved_paths.append(r_path)

        for r_path in resolved_paths:
            if not os.path.exists(r_path):
                logger.warning(f"Recurso '{r_path}' não encontrado.")
                continue

            if os.path.isdir(r_path):
                for root, _, files in os.walk(r_path):
                    for filename in files:
                        src_file = os.path.join(root, filename)
                        dest_file = os.path.join(flat_resources_dir, filename)
                        try:
                            if os.path.exists(dest_file):
                                logger.warning(f"Conflito de nome detectado para '{filename}' na pasta temporária. Sobrescrevendo.")
                            shutil.copy2(src_file, dest_file)
                            context_files_path_map[filename] = dest_file
                        except Exception as e:
                            logger.error(f"Erro ao copiar '{src_file}' para pasta plana: {e}")
            elif r_path.lower().endswith('.zip'):
                try:
                    with zipfile.ZipFile(r_path, 'r') as zip_ref:
                        zip_ref.extractall(unzip_dir)
                    for root, _, files in os.walk(unzip_dir):
                        for filename in files:
                            src_file = os.path.join(root, filename)
                            dest_file = os.path.join(flat_resources_dir, filename)
                            try:
                                if os.path.exists(dest_file):
                                    logger.warning(f"Conflito de nome detectado para '{filename}' da extração ZIP. Sobrescrevendo.")
                                shutil.copy2(src_file, dest_file)
                                context_files_path_map[filename] = dest_file
                            except Exception as e:
                                logger.error(f"Erro ao copiar arquivo ZIP extraído '{src_file}': {e}")
                except Exception as e:
                    logger.error(f"Erro ao extrair arquivo ZIP '{r_path}': {e}")
            else:
                filename = os.path.basename(r_path)
                dest_file = os.path.join(flat_resources_dir, filename)
                try:
                    if os.path.exists(dest_file):
                        logger.warning(f"Conflito de nome detectado para '{filename}'. Sobrescrevendo.")
                    shutil.copy2(r_path, dest_file)
                    context_files_path_map[filename] = dest_file
                except Exception as e:
                    logger.error(f"Erro ao copiar '{r_path}' para pasta plana: {e}")

        # 8. Generation Loop
        falhas_relatorios = []
        for sigla in siglas_selecionadas:
            auditado_obj = auditados[sigla]
            logger.info(f"Gerando relatório para: {sigla} - {auditado_obj.nome}")

            # Context dictionary building
            contexto = auditado_obj.to_dict()
            contexto['sigla'] = sigla
            contexto['data_hoje_abnt'] = data_hoje_abnt()
            contexto['data_hoje'] = data_hoje()
            contexto['auditado'] = auditado_obj

            tem_contexto_extra = df_contexto_extra is not None and sigla in df_contexto_extra.index
            if tem_contexto_extra:
                contexto.update(
                    {
                        chave: normalizar_valor_contexto(valor)
                        for chave, valor in df_contexto_extra.loc[sigla].to_dict().items()
                    }
                )
            elif df_contexto_extra is not None and auditado_obj.status_avaliacao != "nao_respondente":
                logger.error(
                    "[%s] Contexto estatístico/iGovTI não encontrado para auditado avaliado; "
                    "relatório normal não será gerado.",
                    sigla,
                )
                sys.exit(1)

            ajustes_respostas = ajustes_respostas_por_auditado.get(sigla.upper(), [])
            contexto['ajustes_respostas'] = ajustes_respostas
            contexto['teve_ajuste'] = bool(ajustes_respostas)
            contexto['comentarios_gestor'] = contexto_comentarios_por_auditado.get(sigla, {
                'data_referencia': 'não informada',
                'respondeu': False,
                'situacoes': [],
                'itens_questionario': [],
                'resumo_impacto': {},
            })
            contexto['teve_comentarios_gestor'] = bool(contexto['comentarios_gestor'].get('respondeu'))

            # Fill missing variables in context with empty lists so Jinja rendering doesn't crash
            vars_faltantes = set(vars_contexto_template) - set(contexto.keys())
            if vars_faltantes:
                if auditado_obj.status_avaliacao == "nao_respondente":
                    logger.info(
                        "[%s] Relatório de não respondente sem contexto iGovTI; %d variáveis de ramos não renderizados serão preenchidas com vazio.",
                        sigla,
                        len(vars_faltantes),
                    )
                else:
                    logger.warning(f"[{sigla}] Variáveis ausentes no contexto: {vars_faltantes}. Preenchendo com valores vazios.")
                for var in vars_faltantes:
                    contexto[var] = []

            # Generate Report based on template type
            if template_type == 'md':
                try:
                    # Process images for Markdown context
                    contexto, warnings = processa_imagens_contexto(contexto, context_files_path_map, 'md')
                    if warnings:
                        for w in warnings:
                            logger.warning(f"[{sigla}] {w}")

                    # A sintaxe das declarações de referência do Argos
                    # ({#fig:...#} e {#tbl:...#}) coincide com a de comentários
                    # do Jinja. Proteja essas declarações durante a renderização
                    # para que somente as presentes nos ramos efetivamente
                    # renderizados sejam restauradas e numeradas.
                    declaracoes_crossref = {}

                    def proteger_declaracao_crossref(match):
                        marcador = f"@@ARGOS_CROSSREF_{len(declaracoes_crossref)}@@"
                        declaracoes_crossref[marcador] = match.group(0)
                        return marcador

                    template_content_jinja = re.sub(
                        r"\{#(?:fig|tbl):[^#]+#\}",
                        proteger_declaracao_crossref,
                        template_content,
                    )
                    template_md = env.from_string(template_content_jinja)
                    conteudo_final_md = template_md.render(contexto)
                    for marcador, declaracao in declaracoes_crossref.items():
                        conteudo_final_md = conteudo_final_md.replace(marcador, declaracao)
                    # Numere apenas as figuras e tabelas que permaneceram após
                    # a avaliação dos blocos condicionais do template. Isso
                    # evita lacunas em relatórios sem seções opcionais.
                    conteudo_final_md = cross_ref_figuras(conteudo_final_md)
                    conteudo_final_md = cross_ref_tabelas(conteudo_final_md)
                    conteudo_final_md = inserir_campo_sumario_docx(conteudo_final_md)
                    conteudo_final_md = processar_quebras_pagina(conteudo_final_md)
                    conteudo_final_md = substituir_underline_pandoc(conteudo_final_md)

                    # Save intermediate MD report (useful for debugging)
                    nome_relatorio = f'{args.nome_base_docx} - {sigla}'
                    md_filename = os.path.join(args.output_dir, f'{nome_relatorio}.md')
                    with open(md_filename, 'w', encoding='utf-8') as f:
                        f.write(conteudo_final_md)

                    # Build final Docx file using Pandoc
                    import pypandoc
                    docx_filename = os.path.join(args.output_dir, f'{nome_relatorio}.docx')

                    resource_paths = ['.', args.output_dir, unzip_dir, flat_resources_dir, os.path.dirname(args.templates[0])]
                    resource_path_arg = '--resource-path=' + os.pathsep.join(resource_paths)
                    args_docx = [
                        '--figure-caption-position=above',
                        '--reference-doc=' + args.reference_docx,
                        resource_path_arg
                    ]
                    if os.path.exists(TOC_MARKER_FILTER):
                        args_docx.append('--lua-filter=' + TOC_MARKER_FILTER)

                    # Convert to Docx
                    pypandoc.convert_file(md_filename, to='docx', outputfile=docx_filename, extra_args=args_docx)

                    # Apply styles to tables in Docx
                    aplicar_estilo_tabelas(docx_filename)
                    aplicar_fonte_justificativas_avaliacao(docx_filename)
                    evitar_quebra_elementos(docx_filename)
                    marcar_atualizacao_campos_docx(docx_filename)
                    logger.info(f"[{sigla}] Relatório Word gerado em: {docx_filename}")

                except Exception as e:
                    logger.error(f"[{sigla}] Falha ao processar relatório Markdown/Docx: {e}", exc_info=True)
                    falhas_relatorios.append(sigla)

            elif template_type == 'docx':
                try:
                    base_docx = DocxTemplate(template_content_path)
                    # Process images for Docx context
                    contexto, warnings = processa_imagens_contexto(contexto, context_files_path_map, 'docx', base_docx=base_docx)
                    if warnings:
                        for w in warnings:
                            logger.warning(f"[{sigla}] {w}")

                    base_docx.render(contexto)
                    docx_filename = os.path.join(args.output_dir, f'{args.nome_base_docx} - {sigla}.docx')
                    base_docx.save(docx_filename)

                    # Apply styling to tables
                    aplicar_estilo_tabelas(docx_filename)
                    aplicar_fonte_justificativas_avaliacao(docx_filename)
                    evitar_quebra_elementos(docx_filename)
                    marcar_atualizacao_campos_docx(docx_filename)
                    logger.info(f"[{sigla}] Relatório Word (.docx) gerado em: {docx_filename}")
                except Exception as e:
                    logger.error(f"[{sigla}] Falha ao processar relatório DocxTemplate: {e}", exc_info=True)
                    falhas_relatorios.append(sigla)

    if falhas_relatorios:
        logger.error(
            "Falha na geração de %d relatório(s): %s",
            len(falhas_relatorios),
            ", ".join(falhas_relatorios),
        )
        raise SystemExit(1)
    logger.info("Processamento concluído com sucesso!")

if __name__ == '__main__':
    main()
