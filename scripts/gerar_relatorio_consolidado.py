#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera o arquivo DOCX do Relatório Consolidado a partir do Markdown.

Este script processa o Markdown aplicando renderizações de template Jinja2,
referências cruzadas, quebras de página, substituição de underlines do Pandoc
e formatação de tabelas, utilizando o template de estilos do Argos.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path

# Configura path para importar utilitários da pasta resources
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "resources"))
from argos_utils import (
    cross_ref_figuras,
    processar_quebras_pagina,
    cross_ref_tabelas,
    substituir_underline_pandoc,
    aplicar_estilo_tabelas,
    evitar_quebra_elementos,
)

# Tenta importar as bibliotecas necessárias
try:
    import pypandoc
except ImportError:
    print(
        "Erro: pypandoc não está instalado neste ambiente Python.\n"
        "Execute o script utilizando o ambiente virtual do projeto:\n"
        "  scripts/.venv/bin/python scripts/gerar_relatorio_consolidado.py",
        file=sys.stderr
    )
    sys.exit(1)

try:
    import docx
except ImportError:
    print(
        "Erro: python-docx não está instalado neste ambiente Python.\n"
        "Execute o script utilizando o ambiente virtual do projeto:\n"
        "  scripts/.venv/bin/python scripts/gerar_relatorio_consolidado.py",
        file=sys.stderr
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
        default="scripts/resources/template-base-estilos-sigiloso.docx",
        help="Caminho para o documento de estilos do Word usado como referência."
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
    args = parser.parse_args()

    input_str = args.input_positional or args.input or "03-Relatorios/01-Relatorio_Consolidado/Relatório_altaresolucao_novo.md"
    input_path = Path(input_str)
    
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_suffix(".docx")

    ref_path = Path(args.reference_docx)

    if not input_path.exists():
        print(f"Erro: Arquivo de entrada não encontrado: {input_path}", file=sys.stderr)
        return 1

    if not ref_path.exists():
        print(f"Erro: Documento de referência de estilos não encontrado: {ref_path}", file=sys.stderr)
        return 1

    print(f"Lendo markdown: {input_path}")
    conteudo = input_path.read_text(encoding="utf-8")

    # 1. Resolve variáveis de contexto para renderização Jinja2
    contexto = {}
    if args.context_json:
        context_json_path = Path(args.context_json)
        if context_json_path.exists():
            print(f"Carregando variáveis do arquivo JSON: {context_json_path}")
            contexto.update(json.loads(context_json_path.read_text(encoding="utf-8")))
        else:
            print(f"Aviso: Arquivo JSON de contexto não encontrado: {context_json_path}", file=sys.stderr)

    if args.context_vars:
        for item in args.context_vars:
            if "=" in item:
                k, v = item.split("=", 1)
                contexto[k.strip()] = v.strip()

    # 2. Renderiza como Jinja2 se houver tags de template
    if "{{" in conteudo or "{%" in conteudo:
        print("Renderizando variáveis do template com Jinja2...")
        try:
            from jinja2 import Template
            template = Template(conteudo)
            conteudo = template.render(contexto)
        except Exception as e:
            print(f"Erro ao renderizar template Jinja2: {e}", file=sys.stderr)
            return 1

    # 3. Aplica os processamentos de marcação herdados do Argos
    conteudo_processado = cross_ref_figuras(conteudo)
    conteudo_processado = cross_ref_tabelas(conteudo_processado)
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
        print("Executando a geração de gráficos gerais consolidados no diretório temporário...")
        try:
            cmd_graficos_gerais = [sys.executable, script_gerais, "--somente-consolidados", "--output-root", temp_resources_dir]
            for option, value in [
                ("--resultados-2026", args.resultados_2026),
                ("--respostas-2026", args.respostas_2026),
                ("--comparavel-2026", args.comparavel_2026),
                ("--setic-2023", args.setic_2023),
                ("--municipios-2023", args.municipios_2023),
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
            print(f"Aviso: Erro ao gerar gráficos gerais: {e}", file=sys.stderr)

        # Executa a geração de gráficos de achados diretamente para a pasta temporária
        script_achados = os.path.join(os.path.dirname(__file__), "gerar_graficos_achados_consolidado.py")
        print("Executando a geração de gráficos de achados no diretório temporário...")
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
            print(f"Aviso: Erro ao gerar gráficos de achados: {e}", file=sys.stderr)
            
        # 5. Copia imagens de contexto de outros locais (se existirem / especificados) para consolidar na pasta temporária
        tmp_root = Path("C:/tmp") if sys.platform.startswith("win") else Path(tempfile.gettempdir())
        tmp_pkg = tmp_root / "tcerj-igovti-2026"
        tmp_consolidado_img = str(tmp_pkg / "relatorio-consolidado" / "img")
        tmp_individuais_img = str(tmp_pkg / "relatorios-individuais" / "img")
        
        resource_inputs = [tmp_consolidado_img, tmp_individuais_img]
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
                    print(f"Aviso: Nenhum recurso encontrado para o padrão: '{r_path}'", file=sys.stderr)
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
                    print(f"Erro ao extrair zip de recursos '{r_path}': {e}", file=sys.stderr)
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
            print(f"Compilando com Pandoc para DOCX usando template de referência: {ref_path}")
            
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

            # Executa conversão
            output_path.parent.mkdir(parents=True, exist_ok=True)
            pypandoc.convert_file(
                temp_md_name,
                to="docx",
                outputfile=str(output_path),
                extra_args=extra_args
            )

            print(f"Aplicando estilos de tabela pós-conversão no DOCX...")
            aplicar_estilo_tabelas(str(output_path))

            print(f"Ajustando layout para evitar quebras órfãs de figuras, tabelas e fontes...")
            evitar_quebra_elementos(str(output_path))

            print(f"[OK] Relatório DOCX gerado com sucesso em: {output_path}")
            return 0

        except Exception as e:
            print(f"Erro durante a geração do relatório: {e}", file=sys.stderr)
            return 1
        finally:
            if os.path.exists(temp_md_name):
                os.remove(temp_md_name)


if __name__ == "__main__":
    sys.exit(main())
