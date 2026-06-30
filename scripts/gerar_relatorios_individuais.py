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
    evitar_quebra_elementos,
    processar_quebras_pagina,
    substituir_underline_pandoc
)

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

    args = parser.parse_args()

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
    logger.info(f"Variáveis encontradas no template: {sorted(list(vars_template))}")

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
        for sigla in siglas_selecionadas:
            auditado_obj = auditados[sigla]
            logger.info(f"Gerando relatório para: {sigla} - {auditado_obj.nome}")

            # Context dictionary building
            contexto = auditado_obj.to_dict()
            contexto['sigla'] = sigla
            contexto['data_hoje_abnt'] = data_hoje_abnt()
            contexto['data_hoje'] = data_hoje()
            contexto['auditado'] = auditado_obj

            if df_contexto_extra is not None and sigla in df_contexto_extra.index:
                contexto.update(df_contexto_extra.loc[sigla].to_dict())

            ajustes_respostas = ajustes_respostas_por_auditado.get(sigla.upper(), [])
            contexto['ajustes_respostas'] = ajustes_respostas
            contexto['teve_ajuste'] = bool(ajustes_respostas)

            # Fill missing variables in context with empty lists so Jinja rendering doesn't crash
            vars_faltantes = set(vars_template) - set(contexto.keys())
            if vars_faltantes:
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

                    template_content_local = cross_ref_figuras(template_content)
                    template_content_local = cross_ref_tabelas(template_content_local)
                    template_content_local = processar_quebras_pagina(template_content_local)
                    template_content_local = substituir_underline_pandoc(template_content_local)

                    template_md = env.from_string(template_content_local)
                    conteudo_final_md = template_md.render(contexto)

                    # Save intermediate MD report (useful for debugging)
                    md_filename = os.path.join(args.output_dir, f'Relatorio-{sigla}.md')
                    with open(md_filename, 'w', encoding='utf-8') as f:
                        f.write(conteudo_final_md)

                    # Build final Docx file using Pandoc
                    import pypandoc
                    docx_filename = os.path.join(args.output_dir, f'Relatorio-{sigla}.docx')

                    resource_paths = ['.', args.output_dir, unzip_dir, flat_resources_dir, os.path.dirname(args.templates[0])]
                    resource_path_arg = '--resource-path=' + os.pathsep.join(resource_paths)
                    args_docx = [
                        '--figure-caption-position=above',
                        '--reference-doc=' + args.reference_docx,
                        resource_path_arg
                    ]
                    
                    # Convert to Docx
                    pypandoc.convert_file(md_filename, to='docx', outputfile=docx_filename, extra_args=args_docx)
                    
                    # Apply styles to tables in Docx
                    aplicar_estilo_tabelas(docx_filename)
                    evitar_quebra_elementos(docx_filename)
                    logger.info(f"[{sigla}] Relatório Word gerado em: {docx_filename}")

                except Exception as e:
                    logger.error(f"[{sigla}] Falha ao processar relatório Markdown/Docx: {e}", exc_info=True)

            elif template_type == 'docx':
                try:
                    base_docx = DocxTemplate(template_content_path)
                    # Process images for Docx context
                    contexto, warnings = processa_imagens_contexto(contexto, context_files_path_map, 'docx', base_docx=base_docx)
                    if warnings:
                        for w in warnings:
                            logger.warning(f"[{sigla}] {w}")

                    base_docx.render(contexto)
                    docx_filename = os.path.join(args.output_dir, f'Relatorio-{sigla}.docx')
                    base_docx.save(docx_filename)
                    
                    # Apply styling to tables
                    aplicar_estilo_tabelas(docx_filename)
                    evitar_quebra_elementos(docx_filename)
                    logger.info(f"[{sigla}] Relatório Word (.docx) gerado em: {docx_filename}")
                except Exception as e:
                    logger.error(f"[{sigla}] Falha ao processar relatório DocxTemplate: {e}", exc_info=True)

    logger.info("Processamento concluído com sucesso!")

if __name__ == '__main__':
    main()
