#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import json
import logging
import argparse
import zipfile
import io
import datetime
from pathlib import Path
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "resources"))

from argos_classes import FonteInformacao, AcaoVerificacao, ProcedimentoAuditoria, Auditado, \
    gerar_tabela_encaminhamentos, gerar_tabela_achados, gerar_tabela_situacoes_inconformes, \
    parse_bool_planilha, parse_lista_auditados, parse_lista_ids_acoes
from argos_utils import aplicar_variaveis_temporarias, carregar_dados, avalia_logica
from igovti_dados_utils import to_relative
from xlsx_utils import escrever_xlsx_se_diferente
from docxtpl import DocxTemplate
from limesurvey_generator import (
    DEFAULT_ADMIN_EMAIL,
    DEFAULT_ADMIN_NAME,
    DEFAULT_FISCALIZACAO_NOME,
    DEFAULT_FISCALIZACAO_NUMERO,
    LimeSurveyGenerator,
)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_QUESTIONARIO_IGOVTI = ROOT / "01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md"
NAO_PARECER_REVISOR = {"", "nan", "none", "sem_parecer", "sem parecer", "não revisado", "nao revisado"}

class NpEncoder(json.JSONEncoder):
    """JSON Encoder that converts numpy/pandas types to python primitives."""
    def default(self, obj):
        import numpy as np
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj) if not pd.isna(obj) else None
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif pd.isna(obj):
            return None
        return super().default(obj)


def extrair_ids_acoes_logica(expressao):
    return [acao_id for acao_id in re.split(r'[\&\|\~\(\)\s]+', str(expressao)) if acao_id]


def validar_ids_unicos(df, coluna, nome):
    valores = df[coluna].dropna().astype(str).str.strip()
    duplicados = sorted(valores[valores.duplicated()].unique())
    if duplicados:
        raise ValueError(f"{nome} possui identificadores duplicados em '{coluna}': {', '.join(duplicados)}")


def texto_planilha(valor):
    if pd.isna(valor):
        return ""
    return str(valor).strip()


def validar_mapa_auditoria(df_procedimentos, df_acoes, df_fontes, df_variaveis, fontes, df_motivos_relatorio=None):
    erros = []
    avisos = []

    for df, coluna, nome in [
        (df_fontes, 'id', 'Fontes de Informação'),
        (df_acoes, 'id', 'Ações de Verificação'),
        (df_procedimentos, 'id', 'Procedimentos de Auditoria'),
    ]:
        try:
            validar_ids_unicos(df, coluna, nome)
        except ValueError as exc:
            erros.append(str(exc))

    fonte_ids = set(df_fontes['id'].dropna().astype(str).str.strip())
    fonte_carregada_ids = set(fontes.keys())
    acao_ids = set(df_acoes['id'].dropna().astype(str).str.strip())
    acoes_usadas = set()

    for _, row in df_acoes.iterrows():
        acao_id = str(row.get('id')).strip()
        fonte_id = str(row.get('id_fonte_informacao')).strip()
        if fonte_id not in fonte_ids:
            erros.append(f"Ação {acao_id} referencia fonte inexistente no mapa: {fonte_id!r}.")
            continue
        if fonte_id not in fonte_carregada_ids:
            erros.append(f"Ação {acao_id} referencia fonte não carregada: {fonte_id!r}.")
            continue

        try:
            parse_bool_planilha(row.get('auditado_inexistente_e_achado'), default=False, field_name=f"auditado_inexistente_e_achado da ação {acao_id}")
            parse_bool_planilha(row.get('situacao_encontrada_nan_e_achado'), default=False, field_name=f"situacao_encontrada_nan_e_achado da ação {acao_id}")
        except ValueError as exc:
            erros.append(str(exc))

        parse_lista_auditados(row.get('acao_exclusiva_auditados'))

        fonte = fontes.get(fonte_id)
        if fonte and fonte.info is not None:
            for coluna in str(row.get('informacao_requerida')).split('|'):
                coluna = coluna.strip()
                if coluna and coluna not in fonte.info.columns:
                    erros.append(
                        f"Ação {acao_id} busca coluna/variável inexistente {coluna!r} na fonte {fonte_id!r}."
                    )

    for _, row in df_procedimentos.iterrows():
        proc_id = str(row.get('id')).strip()
        ids_logica = extrair_ids_acoes_logica(row.get('logica_achado'))
        if not ids_logica:
            erros.append(f"Procedimento {proc_id} não possui ações na lógica do achado.")
            continue
        acoes_usadas.update(ids_logica)
        faltantes = sorted(set(ids_logica) - acao_ids)
        if faltantes:
            erros.append(f"Procedimento {proc_id} referencia ações inexistentes: {', '.join(faltantes)}.")
        try:
            avalia_logica(str(row.get('logica_achado')), {acao_id: False for acao_id in ids_logica})
        except Exception as exc:
            erros.append(f"Procedimento {proc_id} possui lógica de achado inválida: {exc}")

    acoes_orfas = sorted(acao_ids - acoes_usadas)
    if acoes_orfas:
        avisos.append(f"Ações de verificação não usadas em procedimentos: {', '.join(acoes_orfas)}.")

    if df_motivos_relatorio is not None and not df_motivos_relatorio.empty:
        procedimento_ids = set(df_procedimentos['id'].dropna().astype(str).str.strip())
        if 'id' in df_motivos_relatorio.columns:
            try:
                validar_ids_unicos(df_motivos_relatorio, 'id', 'Motivos do Relatório')
            except ValueError as exc:
                erros.append(str(exc))

        for _, row in df_motivos_relatorio.iterrows():
            motivo_id = texto_planilha(row.get('id'))
            proc_id = texto_planilha(row.get('id_procedimento'))
            if proc_id not in procedimento_ids:
                erros.append(f"Motivo do relatório {motivo_id} referencia procedimento inexistente: {proc_id!r}.")

            situacao = texto_planilha(row.get('descricao_situacao_inconforme'))
            if not situacao:
                erros.append(f"Motivo do relatório {motivo_id} não possui descricao_situacao_inconforme.")

            texto_motivo = texto_planilha(row.get('texto_motivo'))
            if not texto_motivo:
                erros.append(f"Motivo do relatório {motivo_id} não possui texto_motivo.")

            try:
                parse_bool_planilha(row.get('ativo'), default=True, field_name=f"ativo do motivo {motivo_id}")
            except ValueError as exc:
                erros.append(str(exc))

            condicao = texto_planilha(row.get('condicao_exibicao'))
            ids_condicao = extrair_ids_acoes_logica(condicao)
            if condicao:
                faltantes = sorted(set(ids_condicao) - acao_ids)
                if faltantes:
                    erros.append(
                        f"Motivo do relatório {motivo_id} possui condição com ações inexistentes: {', '.join(faltantes)}."
                    )
                try:
                    avalia_logica(condicao, {acao_id: False for acao_id in ids_condicao})
                except Exception as exc:
                    erros.append(f"Motivo do relatório {motivo_id} possui condicao_exibicao inválida: {exc}")

            refs_acoes = parse_lista_ids_acoes(row.get('acoes_referencia'))
            faltantes_refs = sorted(set(refs_acoes) - acao_ids)
            if faltantes_refs:
                erros.append(
                    f"Motivo do relatório {motivo_id} referencia ações inexistentes em acoes_referencia: {', '.join(faltantes_refs)}."
                )

    if avisos:
        for aviso in avisos:
            logger.warning(aviso)

    if erros:
        raise ValueError("Mapa de auditoria inválido:\n- " + "\n- ".join(erros))


def gerar_tabela_status_auditados(auditados):
    dados = []
    for auditado in auditados.values():
        dados.append({
            "Auditado": auditado.sigla,
            "Nome": auditado.nome,
            "Respondeu ao questionário": "Sim" if auditado.respondeu_questionario else "Não",
            "Status da avaliação": auditado.status_avaliacao,
            "Foi auditado": "Sim" if auditado.foi_auditado else "Não",
            "Tem achados": "Sim" if auditado.tem_achados else "Não",
            "Motivo da não avaliação": auditado.motivo_nao_avaliacao,
        })
    if not dados:
        return pd.DataFrame().rename_axis("Auditado")
    return pd.DataFrame(dados).set_index("Auditado")


def calcular_data_final_comentarios_gestor(data_informada):
    if data_informada:
        try:
            data_final = datetime.datetime.strptime(data_informada, "%d/%m/%Y").date()
        except ValueError as exc:
            raise ValueError(
                "Data final de preenchimento dos comentários do gestor inválida. "
                "Use o formato DD/MM/AAAA."
            ) from exc
    else:
        data_final = datetime.date.today() + datetime.timedelta(days=15)

    data_exibicao = data_final.strftime("%d/%m/%Y")
    data_limesurvey = f"{data_final.strftime('%Y-%m-%d')} 23:59:59"
    return data_exibicao, data_limesurvey


def normalizar_texto_comentarios_gestor(valor):
    if pd.isna(valor):
        return ""
    return str(valor).strip()


def normalizar_resultado_comentarios_gestor(valor):
    texto = normalizar_texto_comentarios_gestor(valor)
    if not texto:
        return ""
    texto = re.sub(r"\s+", " ", texto).lower()
    texto = (
        texto.replace("ã", "a")
        .replace("á", "a")
        .replace("à", "a")
        .replace("é", "e")
        .replace("ê", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ô", "o")
        .replace("õ", "o")
        .replace("ç", "c")
    )
    return texto.replace("-", "_").replace(" ", "_")


def resultado_final_evidencia_comentarios_gestor(row):
    avaliacao_revisor = normalizar_texto_comentarios_gestor(row.get("Avaliação do auditor revisor"))
    if avaliacao_revisor.lower() not in NAO_PARECER_REVISOR:
        return avaliacao_revisor, normalizar_texto_comentarios_gestor(row.get("Justificativa do auditor revisor"))
    return (
        normalizar_texto_comentarios_gestor(row.get("Resultado da avaliação do juiz")),
        normalizar_texto_comentarios_gestor(row.get("Justificativa do juiz")),
    )


def base_item_questionario(codigo):
    match = re.match(r"^(q\d{4})", normalizar_texto_comentarios_gestor(codigo), flags=re.IGNORECASE)
    return match.group(1).lower() if match else ""


def limpar_texto_questionario(texto):
    texto = normalizar_texto_comentarios_gestor(texto)
    texto = re.sub(r"^\*\*|\*\*$", "", texto).strip()
    return texto


def texto_sem_numero_questao(texto):
    return re.sub(r"^\d{4}\.\s*", "", limpar_texto_questionario(texto)).strip()


def rotulo_item_questionario(codigo, textos_itens):
    codigo = normalizar_texto_comentarios_gestor(codigo)
    texto = textos_itens.get(codigo.lower())
    if texto:
        return texto
    base = base_item_questionario(codigo)
    return f"{base.upper()} - {codigo}" if base else codigo


def carregar_textos_questionario(path=DEFAULT_QUESTIONARIO_IGOVTI):
    textos_base = {}
    textos_itens = {}
    current = ""
    if not Path(path).exists():
        logger.warning("Questionário iGovTI não encontrado para textos de reavaliação: %s", path)
        return textos_base, textos_itens

    with open(path, encoding="utf-8") as stream:
        for line in stream:
            stripped = line.strip()
            match = re.match(r"^###\s+(q\d{4})\b", stripped, flags=re.IGNORECASE)
            if match:
                current = match.group(1).lower()
                continue
            if current and stripped.startswith("question:"):
                texto = limpar_texto_questionario(stripped.split(":", 1)[1])
                textos_base[current] = texto
                textos_itens[current] = f"{current.upper()} - {texto_sem_numero_questao(texto)}"
                continue
            if current:
                option_match = re.match(r"^-\s*([A-Z])\s*\|\s*(.+)$", stripped)
                if option_match:
                    letra = option_match.group(1)
                    texto = limpar_texto_questionario(option_match.group(2))
                    rotulo = f"{current.upper()} - {texto}"
                    textos_itens[f"{current}[{letra}]".lower()] = rotulo
                    textos_itens[f"{current}ext[{letra}]".lower()] = rotulo
    return textos_base, textos_itens


def carregar_reavaliacao_evidencias_comentarios_gestor(path):
    if not path:
        return {}

    ajustes_path = Path(path)
    if not ajustes_path.exists():
        raise FileNotFoundError(f"Planilha de ajustes de evidências não encontrada: {ajustes_path}")

    df = pd.read_excel(ajustes_path)
    required = {
        "Auditado",
        "Código do item avaliado",
        "Resposta afirmada",
        "Resultado da avaliação do juiz",
        "Justificativa do juiz",
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(
            "Colunas ausentes na planilha de ajustes de evidências para comentários do gestor: "
            + ", ".join(sorted(missing))
        )

    textos_base, textos_itens = carregar_textos_questionario()
    registros = {}
    for _, row in df.iterrows():
        auditado = normalizar_texto_comentarios_gestor(row.get("Auditado")).upper()
        codigo = normalizar_texto_comentarios_gestor(row.get("Código do item avaliado"))
        base = base_item_questionario(codigo)
        if not auditado or not codigo or not base:
            continue

        resultado, justificativa = resultado_final_evidencia_comentarios_gestor(row)
        if normalizar_resultado_comentarios_gestor(resultado) != "nao_conforme":
            continue

        registro_base = registros.setdefault(
            base,
            {
                "base": base,
                "base_texto": textos_base.get(base, base),
                "auditados": set(),
                "itens_por_auditado": {},
            },
        )
        registro_base["auditados"].add(auditado)
        registro_base["itens_por_auditado"].setdefault(auditado, []).append(
            {
                "codigo": codigo,
                "rotulo": rotulo_item_questionario(codigo, textos_itens),
                "resposta_afirmada": normalizar_texto_comentarios_gestor(row.get("Resposta afirmada")),
                "resultado": resultado,
                "justificativa_nao_conformidade": justificativa,
            }
        )

    return [
        {
            "base": registro["base"],
            "base_texto": registro["base_texto"],
            "auditados": sorted(registro["auditados"]),
            "itens_por_auditado": {
                auditado: sorted(itens, key=lambda item: item["codigo"])
                for auditado, itens in sorted(registro["itens_por_auditado"].items())
            },
        }
        for _, registro in sorted(registros.items(), key=lambda item: int(item[0][1:]))
    ]

def main():
    parser = argparse.ArgumentParser(
        description='Executa os procedimentos de auditoria do Argos via Linha de Comando.'
    )
    parser.add_argument(
        '-a', '--auditados', required=True,
        help='Caminho para a base de auditados (.xlsx) (ex: bd_auditados.xlsx).'
    )
    parser.add_argument(
        '-m', '--mapa', required=True,
        help='Caminho para o mapa de verificação e achados (.xlsx) (ex: mapa-verificacao-achados.xlsx).'
    )
    parser.add_argument(
        '-f', '--fontes', nargs='+', required=True,
        help='Caminho para um ou mais arquivos de fontes de informação/respostas (.xlsx).'
    )
    parser.add_argument(
        '-j', '--resultado-auditoria-json', '--output-json',
        dest='resultado_auditoria_json',
        default='.output_reports/resultado_auditoria.json',
        help='Caminho para salvar o resultado compacto da auditoria em JSON (padrão: .output_reports/resultado_auditoria.json).'
    )
    parser.add_argument(
        '--resultado-auditoria-detalhado-json',
        default='',
        help='Caminho opcional para salvar o resultado detalhado da auditoria, incluindo todas as ações de verificação.'
    )
    parser.add_argument(
        '-x', '--tabelas-auditoria-xlsx', '--output-xlsx',
        dest='tabelas_auditoria_xlsx',
        default='.output_reports/tabelas_consolidadas_auditoria.xlsx',
        help='Caminho para salvar a planilha de tabelas consolidadas da auditoria (padrão: .output_reports/tabelas_consolidadas_auditoria.xlsx).'
    )
    parser.add_argument(
        '--email-contato-comentarios-gestor',
        default=DEFAULT_ADMIN_EMAIL,
        help=f'E-mail de contato para o questionário de comentários do gestor (padrão: {DEFAULT_ADMIN_EMAIL}).'
    )
    parser.add_argument(
        '--admin-responsavel-comentarios-gestor',
        default=DEFAULT_ADMIN_NAME,
        help=f'Nome do administrador responsável pelo questionário de comentários do gestor (padrão: {DEFAULT_ADMIN_NAME}).'
    )
    parser.add_argument(
        '--data-final-preenchimento-comentarios-gestor',
        default='',
        help='Data final de preenchimento dos comentários do gestor em DD/MM/AAAA (padrão: data atual + 15 dias).'
    )
    parser.add_argument(
        '--numero-fiscalizacao-comentarios-gestor',
        default=DEFAULT_FISCALIZACAO_NUMERO,
        help=f'Número da fiscalização usado no questionário de comentários do gestor (padrão: {DEFAULT_FISCALIZACAO_NUMERO}).'
    )
    parser.add_argument(
        '--nome-fiscalizacao-comentarios-gestor',
        default=DEFAULT_FISCALIZACAO_NOME,
        help=f'Nome da fiscalização usado no questionário de comentários do gestor (padrão: {DEFAULT_FISCALIZACAO_NOME}).'
    )
    parser.add_argument(
        '--ajustes-evidencias-comentarios-gestor',
        default='',
        help='Planilha de ajustes pós-avaliação de evidências usada para incluir seção opcional de reavaliação no survey de comentários do gestor.'
    )
    parser.add_argument(
        '--out-proc-zip', default='',
        help='Caminho para salvar o arquivo .zip com relatórios individuais de procedimentos.'
    )
    parser.add_argument(
        '--out-evidencias-docx', default='',
        help='Caminho para salvar o documento Word consolidado do anexo de evidências.'
    )
    parser.add_argument(
        '--out-lss', default='',
        help='Caminho para salvar o arquivo de questionário unificado (.lss) do LimeSurvey.'
    )
    parser.add_argument(
        '--out-comentarios-zip', default='',
        help='Caminho para salvar o arquivo .zip com os questionários de comentários em Word individuais.'
    )
    parser.add_argument(
        '--somente-dados', action='store_true',
        help='Gera apenas JSON/XLSX da auditoria, sem ZIP/DOCX/LSS acessórios.'
    )
    parser.add_argument(
        '--skip-relatorios-procedimentos', action='store_true',
        help='Não gera o ZIP com relatórios de procedimentos individuais.'
    )
    parser.add_argument(
        '--skip-anexo-evidencias', action='store_true',
        help='Não gera o documento Word consolidado do anexo de evidências.'
    )
    parser.add_argument(
        '--skip-comentarios-gestor', action='store_true',
        help='Não gera o questionário LimeSurvey nem os anexos Word de comentários do gestor.'
    )

    args = parser.parse_args()

    # 1. Valida caminhos de entrada
    if not os.path.exists(args.auditados):
        logger.error(f"Arquivo de auditados '{args.auditados}' não encontrado.")
        sys.exit(1)
    if not os.path.exists(args.mapa):
        logger.error(f"Mapa de verificação '{args.mapa}' não encontrado.")
        sys.exit(1)

    # 2. Carrega planilhas do mapa
    logger.info("Carregando tabelas do mapa de verificação e auditados...")
    cols_jurisdicionados = ['sigla', 'orgao']
    cols_procedimentos = ['id', 'descricao', 'logica_achado', 'numero_achado', 'nome_achado']
    cols_acoes = ['id', 'id_fonte_informacao', 'informacao_requerida', 'criterio', 'situacao_inconforme', 'tipo_encaminhamento']
    cols_fontes = ['id', 'descricao', 'filepath', 'chave_jurisdicionado']
    cols_variaveis = ['id', 'id_fonte_informacao', 'nome', 'expressao', 'descricao']
    cols_motivos_relatorio = [
        'id',
        'id_procedimento',
        'descricao_situacao_inconforme',
        'ordem',
        'condicao_exibicao',
        'acoes_referencia',
        'texto_motivo',
    ]

    try:
        df_jurisdicionados = carregar_dados(args.auditados, skiprows=None, required_columns=cols_jurisdicionados)
        df_procedimentos = carregar_dados(args.mapa, sheet_name='Procedimentos de Auditoria', skiprows=None, required_columns=cols_procedimentos)
        df_acoes_verificacao = carregar_dados(args.mapa, sheet_name='Ações de Verificação', skiprows=None, required_columns=cols_acoes)
        df_fontes = carregar_dados(args.mapa, sheet_name='Fontes de Informação', skiprows=None, required_columns=cols_fontes)
        
        xl_mapa = pd.ExcelFile(args.mapa)
        if 'Variáveis Temporárias' in xl_mapa.sheet_names:
            df_variaveis_temporarias = carregar_dados(args.mapa, sheet_name='Variáveis Temporárias', skiprows=None, required_columns=cols_variaveis)
        else:
            df_variaveis_temporarias = pd.DataFrame(columns=cols_variaveis)
        if 'Motivos do Relatório' in xl_mapa.sheet_names:
            df_motivos_relatorio = carregar_dados(args.mapa, sheet_name='Motivos do Relatório', skiprows=None, required_columns=cols_motivos_relatorio)
        else:
            df_motivos_relatorio = pd.DataFrame(columns=cols_motivos_relatorio + ['ativo'])
    except Exception as e:
        logger.error(f"Erro ao carregar arquivos de configuração da auditoria: {e}")
        sys.exit(1)

    # 3. Mapeia e carrega as fontes de informação
    logger.info("Carregando fontes de informação...")
    fontes_path_map = {os.path.basename(f): f for f in args.fontes}
    fontes = {}

    for _, row in df_fontes.iterrows():
        nome_arquivo_fonte = os.path.basename(row['filepath'])
        actual_path = fontes_path_map.get(nome_arquivo_fonte)
        
        if not actual_path:
            if len(args.fontes) == 1:
                actual_path = args.fontes[0]
                logger.warning(f"Mapeando fonte '{nome_arquivo_fonte}' para o único arquivo fornecido '{actual_path}'.")
            else:
                logger.error(f"Arquivo da fonte de informação '{nome_arquivo_fonte}' não foi encontrado nos arquivos fornecidos.")
                sys.exit(1)

        fonte = FonteInformacao(
            descricao=row['descricao'],
            filepath=to_relative(actual_path),
            chave_jurisdicionado=row['chave_jurisdicionado'],
            id=row['id']
        )
        try:
            fonte.read()
            fontes[fonte.id] = fonte
        except Exception as e:
            logger.error(f"Erro ao ler a fonte de informação '{fonte.descricao}' ('{actual_path}'): {e}")
            sys.exit(1)

    # 4. Aplica variáveis temporárias
    logger.info("Aplicando variáveis temporárias...")
    try:
        aplicar_variaveis_temporarias(fontes, df_variaveis_temporarias)
    except Exception as e:
        logger.error(f"Erro ao aplicar variáveis temporárias: {e}")
        sys.exit(1)

    logger.info("Validando mapa de auditoria...")
    try:
        validar_mapa_auditoria(
            df_procedimentos,
            df_acoes_verificacao,
            df_fontes,
            df_variaveis_temporarias,
            fontes,
            df_motivos_relatorio,
        )
    except Exception as e:
        logger.error(e)
        sys.exit(1)

    # 5. Inicializa as ações de verificação
    logger.info("Inicializando ações de verificação...")
    acoes = {}
    for _, row in df_acoes_verificacao.iterrows():
        fonte_informacao = fontes.get(row['id_fonte_informacao'])
        if not fonte_informacao:
            logger.error(f"Ação de verificação '{row['id']}' refere-se a uma fonte inexistente '{row['id_fonte_informacao']}'.")
            sys.exit(1)
        
        acao = AcaoVerificacao(
            fonte_informacao=fonte_informacao,
            informacao_requerida=row.get('informacao_requerida'),
            acao_exclusiva_auditados=row.get('acao_exclusiva_auditados'),
            criterio=row.get('criterio'),
            descricao_situacao_inconforme=row.get('descricao_situacao_inconforme'),
            descricao_evidencia=row.get('descricao_evidencia'),
            situacao_inconforme=row.get('situacao_inconforme'),
            situacao_encontrada_nan_e_achado=row.get('situacao_encontrada_nan_e_achado'),
            tipo_encaminhamento=row.get('tipo_encaminhamento'),
            encaminhamento=row.get('encaminhamento'),
            pre_encaminhamento=row.get('pre_encaminhamento'),
            auditado_inexistente_e_achado=row.get('auditado_inexistente_e_achado'),
            descricao_auditado_inexistente=row.get('descricao_auditado_inexistente'),
            id=row['id']
        )
        acoes[acao.id] = acao

    # 6. Inicializa os procedimentos de auditoria
    logger.info("Inicializando procedimentos de auditoria...")
    procedimentos = {}
    for _, row in df_procedimentos.iterrows():
        procedimento = ProcedimentoAuditoria(
            descricao=row['descricao'],
            logica_achado=row['logica_achado'],
            numero_achado=row['numero_achado'],
            nome_achado=row['nome_achado'],
            id=row['id']
        )
        # Parse logic to extract dependencies
        acao_ids = [acao_id for acao_id in re.split(r'[\&\|\~\(\)\s]+', procedimento.logica_achado.replace("(", "").replace(")", "")) if acao_id]
        for acao_id in acao_ids:
            acao = acoes.get(acao_id.strip())
            if acao:
                procedimento.adicionar_acao(acao)
        procedimentos[procedimento.id] = procedimento

    if not df_motivos_relatorio.empty:
        for _, row in df_motivos_relatorio.iterrows():
            proc_id = texto_planilha(row.get('id_procedimento'))
            procedimento = procedimentos.get(proc_id)
            if procedimento:
                procedimento.adicionar_motivo_relatorio(row.to_dict())

    # 7. Inicializa os auditados
    logger.info("Carregando lista de auditados...")
    auditados = {}
    for _, row in df_jurisdicionados.iterrows():
        auditado = Auditado(nome=row['orgao'], sigla=row['sigla'])
        auditados[auditado.sigla] = auditado

    fonte_questionario = fontes.get("questionario")
    if fonte_questionario is None or fonte_questionario.info is None:
        logger.error("Fonte de informação 'questionario' não foi carregada; não é possível identificar respondentes.")
        sys.exit(1)
    respondentes_questionario = {
        valor for valor in fonte_questionario.info.index.astype(str).str.strip()
        if valor
    }
    respondentes_fora_cadastro = sorted(respondentes_questionario - set(auditados.keys()))
    if respondentes_fora_cadastro:
        logger.error(
            "Há respondentes ausentes da base de auditados. Atualize o cadastro antes de executar "
            "a auditoria: %s",
            ", ".join(respondentes_fora_cadastro),
        )
        sys.exit(1)

    # 8. Executa a auditoria
    logger.info("Executando procedimentos de auditoria...")
    for auditado in auditados.values():
        if auditado.sigla not in respondentes_questionario:
            auditado.marcar_nao_respondente("Ausência de resposta válida ao questionário iGovTI 2026.")
            logger.warning(
                "Auditado %s consta no cadastro, mas não possui resposta válida ao questionário; "
                "procedimentos individualizados não serão executados.",
                auditado.sigla,
            )
            continue
        auditado.aplicar_procedimentos(procedimentos.values(), debug=False)

    logger.info("Auditoria executada com sucesso! Gerando relatórios de saída...")

    # 9. Consolida tabelas
    tabela_status = gerar_tabela_status_auditados(auditados)
    tabela_encaminhamentos = gerar_tabela_encaminhamentos(auditados)
    tabela_achados = gerar_tabela_achados(auditados)
    tabela_situacoes = gerar_tabela_situacoes_inconformes(auditados)

    # Ranking de Auditados (como em visualiza_resultados)
    situations_per_auditado = {}
    achados_per_auditado = {}
    for sigla, auditado in auditados.items():
        if auditado.foi_auditado:
            situacoes = auditado.get_situacoes_inconformes()
            situations_per_auditado[sigla] = len(situacoes)
            achados_per_auditado[sigla] = len(auditado.get_nomes_achados())

    df_rank_combined = pd.DataFrame()
    if situations_per_auditado and achados_per_auditado:
        df_rank_situacoes = pd.DataFrame.from_dict(situations_per_auditado, orient='index', columns=['Qtd. Situações Inconformes'])
        df_rank_achados = pd.DataFrame.from_dict(achados_per_auditado, orient='index', columns=['Qtd. Achados Distintos'])
        df_rank_combined = df_rank_achados.join(df_rank_situacoes).sort_values(by=['Qtd. Achados Distintos', 'Qtd. Situações Inconformes'], ascending=False)

    # 10. Salva em JSON
    try:
        os.makedirs(os.path.dirname(os.path.abspath(args.resultado_auditoria_json)), exist_ok=True)
        auditados_dict = {k: v.to_dict(compacto=True) for k, v in auditados.items()}
        with open(args.resultado_auditoria_json, 'w', encoding='utf-8') as f:
            json.dump(auditados_dict, f, indent=2, ensure_ascii=False, cls=NpEncoder)
        logger.info(f"Resultado compacto da auditoria salvo em: {args.resultado_auditoria_json}")

        if args.resultado_auditoria_detalhado_json:
            os.makedirs(os.path.dirname(os.path.abspath(args.resultado_auditoria_detalhado_json)), exist_ok=True)
            auditados_detalhado_dict = {k: v.to_dict(compacto=False) for k, v in auditados.items()}
            with open(args.resultado_auditoria_detalhado_json, 'w', encoding='utf-8') as f:
                json.dump(auditados_detalhado_dict, f, indent=2, ensure_ascii=False, cls=NpEncoder)
            logger.info(f"Resultado detalhado da auditoria salvo em: {args.resultado_auditoria_detalhado_json}")
    except Exception as e:
        logger.error(f"Erro ao salvar arquivo JSON de auditados: {e}")

    # 11. Salva em Excel
    try:
        def _writer(temp_path):
            with pd.ExcelWriter(temp_path, engine='xlsxwriter') as writer:
                tabela_status.to_excel(writer, sheet_name='Status dos Auditados')
                nao_respondentes = tabela_status[tabela_status["Status da avaliação"] == "nao_respondente"]
                if not nao_respondentes.empty:
                    nao_respondentes.to_excel(writer, sheet_name='Não Respondentes')
                tabela_achados.to_excel(writer, sheet_name='Achados por Auditado')
                tabela_encaminhamentos.to_excel(writer, sheet_name='Encaminhamentos por Auditado')
                tabela_situacoes.to_excel(writer, sheet_name='Situações Inconformes')
                if not df_rank_combined.empty:
                    df_rank_combined.to_excel(writer, sheet_name='Ranking de Auditados')

        escrever_xlsx_se_diferente(args.tabelas_auditoria_xlsx, _writer)
        logger.info(f"Tabelas consolidadas da auditoria salvas em: {args.tabelas_auditoria_xlsx}")
    except Exception as e:
        logger.error(f"Erro ao salvar tabelas em Excel: {e}")

    # 12. Geração de relatórios de procedimentos individuais (ZIP)
    if args.somente_dados or args.skip_relatorios_procedimentos:
        logger.info("Geração do ZIP de relatórios de procedimentos ignorada.")
    else:
        proc_zip_path = Path(args.out_proc_zip) if args.out_proc_zip else Path(args.resultado_auditoria_json).parent / "relatorios_procedimentos.zip"
        logger.info(f"Gerando relatórios de procedimentos individuais em ZIP: {proc_zip_path}")
        try:
            os.makedirs(proc_zip_path.parent, exist_ok=True)
            template_report = os.path.join(os.path.dirname(__file__), "resources", "template_report.docx")
            
            with zipfile.ZipFile(proc_zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_f:
                for sigla, auditado in auditados.items():
                    if auditado.foi_auditado:
                        doc = auditado.documenta_procedimentos(template_path=template_report)
                        bio = io.BytesIO()
                        doc.save(bio)
                        zip_f.writestr(f"{auditado.sigla} - Relatorio.docx", bio.getvalue())
            logger.info(f"Relatórios de procedimentos individuais ZIP gerado com sucesso!")
        except Exception as e:
            logger.error(f"Erro ao gerar ZIP de procedimentos: {e}")

    # 13. Geração do Anexo de Evidências (Word consolidado)
    if args.somente_dados or args.skip_anexo_evidencias:
        logger.info("Geração do anexo de evidências ignorada.")
    else:
        evidencias_docx_path = Path(args.out_evidencias_docx) if args.out_evidencias_docx else Path(args.resultado_auditoria_json).parent / "anexo_evidencias.docx"
        logger.info(f"Gerando anexo de evidências unificado: {evidencias_docx_path}")
        try:
            os.makedirs(evidencias_docx_path.parent, exist_ok=True)
            template_evidencias = os.path.join(os.path.dirname(__file__), "resources", "anexo-evidencias-base.docx")
            
            contexto_anexo = [
                {
                    'sigla_orgao': a.sigla, 
                    'nome_orgao': a.nome, 
                    'achados': list(a.get_achados().values())
                } 
                for a in auditados.values()
            ]
            
            doc_evidencias = DocxTemplate(template_evidencias)
            doc_evidencias.render({'dados': contexto_anexo})
            doc_evidencias.save(evidencias_docx_path)
            logger.info(f"Anexo de evidências gerado com sucesso!")
        except Exception as e:
            logger.error(f"Erro ao gerar anexo de evidências: {e}")

    # 14. Geração do Questionário do Gestor (.lss e anexos Word em ZIP)
    auditados_com_achados = [v for v in auditados.values() if v.tem_achados]
    auditados_nao_respondentes = [
        v for v in auditados.values()
        if getattr(v, "status_avaliacao", "") == "nao_respondente"
    ]
    if not (args.somente_dados or args.skip_comentarios_gestor):
        data_final_entrega, data_final_limesurvey = calcular_data_final_comentarios_gestor(
            args.data_final_preenchimento_comentarios_gestor
        )
        reavaliacao_evidencias = carregar_reavaliacao_evidencias_comentarios_gestor(
            args.ajustes_evidencias_comentarios_gestor
        )
        if reavaliacao_evidencias:
            total_auditados_reavaliacao = len({
                auditado
                for base in reavaliacao_evidencias
                for auditado in base.get("auditados", [])
            })
            logger.info(
                "Seção de reavaliação de evidências habilitada para %s auditado(s) e %s questão(ões)-base.",
                total_auditados_reavaliacao,
                len(reavaliacao_evidencias),
            )
    
    # 14.1 Arquivo .lss (LimeSurvey)
    if args.somente_dados or args.skip_comentarios_gestor:
        logger.info("Geração do questionário LimeSurvey de comentários ignorada.")
    else:
        lss_path = Path(args.out_lss) if args.out_lss else Path(args.resultado_auditoria_json).parent / "comentarios_gestor" / "questionario_comentarios_gestor.lss"
        logger.info(f"Gerando questionário LimeSurvey unificado (.lss): {lss_path}")
        try:
            os.makedirs(lss_path.parent, exist_ok=True)
            generator = LimeSurveyGenerator()
            xml_content = generator.generate_xml(
                auditados_com_achados,
                admin_name=args.admin_responsavel_comentarios_gestor,
                admin_email=args.email_contato_comentarios_gestor,
                expires=data_final_limesurvey,
                reavaliacao_evidencias=reavaliacao_evidencias,
                auditados_nao_respondentes=auditados_nao_respondentes,
                fiscalizacao_numero=args.numero_fiscalizacao_comentarios_gestor,
                fiscalizacao_nome=args.nome_fiscalizacao_comentarios_gestor,
            )
            
            with open(lss_path, 'w', encoding='utf-8') as f:
                f.write(xml_content)
            logger.info(f"Questionário LimeSurvey (.lss) gerado com sucesso!")
        except Exception as e:
            logger.error(f"Erro ao gerar questionário LSS: {e}")

    # 14.2 Anexos Word em ZIP
    if args.somente_dados or args.skip_comentarios_gestor:
        logger.info("Geração dos anexos Word de comentários ignorada.")
    else:
        comentarios_zip_path = Path(args.out_comentarios_zip) if args.out_comentarios_zip else Path(args.resultado_auditoria_json).parent / "comentarios_gestor" / "anexos_docx_comentarios.zip"
        logger.info(f"Gerando anexos de comentários do gestor individuais em ZIP: {comentarios_zip_path}")
        try:
            os.makedirs(comentarios_zip_path.parent, exist_ok=True)
            template_comentarios = os.path.join(os.path.dirname(__file__), "resources", "template-questionario-comentarios-gestor.docx")
            siglas_reavaliacao = {
                normalizar_texto_comentarios_gestor(sigla).upper()
                for item in reavaliacao_evidencias
                for sigla in item.get("auditados", [])
            }
            auditados_reavaliacao = [
                auditado for auditado in auditados.values()
                if normalizar_texto_comentarios_gestor(auditado.sigla).upper() in siglas_reavaliacao
            ]
            auditados_para_comentarios = {
                auditado.sigla: auditado
                for auditado in [*auditados_com_achados, *auditados_reavaliacao, *auditados_nao_respondentes]
            }
                
            with zipfile.ZipFile(comentarios_zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for auditado in auditados_para_comentarios.values():
                    doc = DocxTemplate(template_comentarios)
                    achados = [p.achado for p in auditado.procedimentos_executados if p.achado is not None]
                    auditado_sigla = normalizar_texto_comentarios_gestor(auditado.sigla).upper()
                    reavaliacao_evidencias_auditado = [
                        {
                            "base": item.get("base", ""),
                            "base_texto": item.get("base_texto", item.get("base", "")),
                            "itens": item.get("itens_por_auditado", {}).get(auditado_sigla, []),
                        }
                        for item in reavaliacao_evidencias
                        if auditado_sigla in {
                            normalizar_texto_comentarios_gestor(sigla).upper()
                            for sigla in item.get("auditados", [])
                        }
                    ]
                    
                    contexto = {
                        'auditado': auditado,
                        'achados': achados,
                        'data_final_entrega': data_final_entrega,
                        'email_contato': args.email_contato_comentarios_gestor,
                        'reavaliacao_evidencias': reavaliacao_evidencias_auditado,
                    }
                    doc.render(contexto)
                    
                    bio = io.BytesIO()
                    doc.save(bio)
                    zip_file.writestr(f"Anexo - Questionário Comentarios ({auditado.sigla}).docx", bio.getvalue())
            logger.info(f"Anexos de comentários individuais ZIP gerado com sucesso!")
        except Exception as e:
            logger.error(f"Erro ao gerar ZIP de comentários do gestor: {e}")

    logger.info("Auditoria finalizada!")

if __name__ == '__main__':
    main()
