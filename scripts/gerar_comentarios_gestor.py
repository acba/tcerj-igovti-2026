#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Gera questionário LimeSurvey e anexos DOCX dos comentários do gestor."""

from __future__ import annotations

import argparse
import datetime
import io
import json
import logging
import os
import re
import sys
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd
from docxtpl import DocxTemplate

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "resources"))

from argos_classes import Auditado  # noqa: E402
from argos_utils import marcar_atualizacao_campos_docx_bytes  # noqa: E402
from limesurvey_generator import (  # noqa: E402
    DEFAULT_ADMIN_EMAIL,
    DEFAULT_ADMIN_NAME,
    DEFAULT_FISCALIZACAO_NOME,
    DEFAULT_FISCALIZACAO_NUMERO,
    LimeSurveyGenerator,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_QUESTIONARIO_IGOVTI = ROOT / "01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md"
DEFAULT_DOCX_WORKERS = max(1, min(8, os.cpu_count() or 1))
NAO_PARECER_REVISOR = {"", "nan", "none", "sem_parecer", "sem parecer", "não revisado", "nao revisado"}


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


def normalizar_workers_docx(valor):
    try:
        workers = int(valor)
    except (TypeError, ValueError):
        return DEFAULT_DOCX_WORKERS
    return max(1, workers)


def renderizar_docx_em_paralelo(itens, render_fn, jobs, descricao):
    itens = list(itens)
    total = len(itens)
    if not total:
        logger.warning("Nenhum item encontrado para gerar %s.", descricao)
        return []

    workers = min(normalizar_workers_docx(jobs), total)
    logger.info("Renderizando %s DOCX de %s com %s worker(s)...", total, descricao, workers)

    resultados = [None] * total
    if workers == 1:
        for index, item in enumerate(itens, start=1):
            resultados[index - 1] = render_fn(item)
            if index == total or index % 10 == 0:
                logger.info("Renderizados %s/%s DOCX de %s.", index, total, descricao)
        return resultados

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(render_fn, item): index
            for index, item in enumerate(itens)
        }
        concluidos = 0
        for future in as_completed(futures):
            index = futures[future]
            resultados[index] = future.result()
            concluidos += 1
            if concluidos == total or concluidos % 10 == 0:
                logger.info("Renderizados %s/%s DOCX de %s.", concluidos, total, descricao)

    return resultados


def gravar_zip_docx(zip_path, entradas):
    os.makedirs(zip_path.parent, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_STORED) as zip_file:
        for filename, content in entradas:
            zip_file.writestr(filename, content)


def indexar_reavaliacao_evidencias_por_auditado(reavaliacao_evidencias):
    por_auditado = {}
    for item in reavaliacao_evidencias or []:
        itens_por_auditado = {
            normalizar_texto_comentarios_gestor(sigla).upper(): itens
            for sigla, itens in (item.get("itens_por_auditado") or {}).items()
        }
        for sigla in item.get("auditados", []):
            auditado_sigla = normalizar_texto_comentarios_gestor(sigla).upper()
            por_auditado.setdefault(auditado_sigla, []).append(
                {
                    "base": item.get("base", ""),
                    "base_texto": item.get("base_texto", item.get("base", "")),
                    "itens": itens_por_auditado.get(auditado_sigla, []),
                }
            )
    return por_auditado


def selecionar_auditados_para_comentarios(auditados, auditados_com_achados, auditados_nao_respondentes, reavaliacao_por_auditado):
    selecionados = {}
    for auditado in [*auditados_com_achados, *auditados_nao_respondentes]:
        selecionados[auditado.sigla] = auditado

    siglas_reavaliacao = set(reavaliacao_por_auditado.keys())
    for auditado in auditados.values():
        if normalizar_texto_comentarios_gestor(auditado.sigla).upper() in siglas_reavaliacao:
            selecionados[auditado.sigla] = auditado

    return sorted(selecionados.values(), key=lambda auditado: str(auditado.sigla))


def carregar_auditados_resultado(resultado_auditoria_json):
    path = Path(resultado_auditoria_json)
    if not path.exists():
        raise FileNotFoundError(f"Resultado de auditoria não encontrado: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("O resultado de auditoria deve ser um objeto JSON indexado por auditado.")
    return {sigla: Auditado.from_dict(item) for sigla, item in data.items()}


def gerar_zip_anexos_comentarios_gestor(
    auditados_para_comentarios,
    reavaliacao_por_auditado,
    zip_path,
    data_final_entrega,
    email_contato,
    jobs,
):
    template_comentarios = Path(__file__).resolve().parent / "resources/template-questionario-comentarios-gestor.docx"

    def render(auditado):
        doc = DocxTemplate(template_comentarios)
        achados = [p.achado for p in auditado.procedimentos_executados if p.achado is not None]
        auditado_sigla = normalizar_texto_comentarios_gestor(auditado.sigla).upper()
        contexto = {
            "auditado": auditado,
            "achados": achados,
            "data_final_entrega": data_final_entrega,
            "email_contato": email_contato,
            "reavaliacao_evidencias": reavaliacao_por_auditado.get(auditado_sigla, []),
        }
        doc.render(contexto)
        bio = io.BytesIO()
        doc.save(bio)
        return (
            f"Anexo - Questionário Comentarios ({auditado.sigla}).docx",
            marcar_atualizacao_campos_docx_bytes(bio.getvalue()),
        )

    entradas = renderizar_docx_em_paralelo(
        auditados_para_comentarios,
        render,
        jobs,
        "anexos de comentários do gestor",
    )
    gravar_zip_docx(zip_path, entradas)
    logger.info(
        "Anexos de comentários individuais ZIP gerado com sucesso: %s (%s arquivo(s)).",
        zip_path,
        len(entradas),
    )


def gerar_comentarios_gestor(args):
    resultado_path = Path(args.resultado_auditoria_json)
    auditados = carregar_auditados_resultado(resultado_path)
    auditados_com_achados = [v for v in auditados.values() if v.tem_achados]
    auditados_nao_respondentes = [
        v for v in auditados.values()
        if getattr(v, "status_avaliacao", "") == "nao_respondente"
    ]
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
    reavaliacao_por_auditado = indexar_reavaliacao_evidencias_por_auditado(reavaliacao_evidencias)

    if not args.skip_comentarios_gestor_lss:
        lss_path = (
            Path(args.comentarios_gestor_lss)
            if args.comentarios_gestor_lss
            else resultado_path.parent / "comentarios_gestor/questionario_comentarios_gestor.lss"
        )
        logger.info("Gerando questionário LimeSurvey unificado (.lss): %s", lss_path)
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
        lss_path.write_text(xml_content, encoding="utf-8")
        logger.info("Questionário LimeSurvey (.lss) gerado com sucesso.")

    if not args.skip_comentarios_gestor_anexos:
        comentarios_zip_path = (
            Path(args.comentarios_gestor_anexos_zip)
            if args.comentarios_gestor_anexos_zip
            else resultado_path.parent / "comentarios_gestor/anexos_docx_comentarios.zip"
        )
        logger.info("Gerando anexos de comentários do gestor individuais em ZIP: %s", comentarios_zip_path)
        auditados_para_comentarios = selecionar_auditados_para_comentarios(
            auditados,
            auditados_com_achados,
            auditados_nao_respondentes,
            reavaliacao_por_auditado,
        )
        gerar_zip_anexos_comentarios_gestor(
            auditados_para_comentarios,
            reavaliacao_por_auditado,
            comentarios_zip_path,
            data_final_entrega,
            args.email_contato_comentarios_gestor,
            args.jobs_comentarios_gestor_anexos,
        )


def parse_args():
    parser = argparse.ArgumentParser(
        description="Gera questionário LimeSurvey e anexos DOCX de comentários do gestor a partir do resultado da auditoria."
    )
    parser.add_argument(
        "--resultado-auditoria-json",
        required=True,
        help="Caminho do resultado_auditoria.json gerado por scripts/executa_auditoria.py.",
    )
    parser.add_argument(
        "--comentarios-gestor-lss",
        default="",
        help="Caminho para salvar o questionário unificado (.lss) do LimeSurvey. Se omitido, usa a pasta comentarios_gestor ao lado do resultado.",
    )
    parser.add_argument(
        "--comentarios-gestor-anexos-zip",
        default="",
        help="Caminho para salvar o ZIP com os anexos DOCX individuais. Se omitido, usa a pasta comentarios_gestor ao lado do resultado.",
    )
    parser.add_argument(
        "--email-contato-comentarios-gestor",
        default=DEFAULT_ADMIN_EMAIL,
        help=f"E-mail de contato para o questionário de comentários do gestor (padrão: {DEFAULT_ADMIN_EMAIL}).",
    )
    parser.add_argument(
        "--admin-responsavel-comentarios-gestor",
        default=DEFAULT_ADMIN_NAME,
        help=f"Nome do administrador responsável pelo questionário de comentários do gestor (padrão: {DEFAULT_ADMIN_NAME}).",
    )
    parser.add_argument(
        "--data-final-preenchimento-comentarios-gestor",
        default="",
        help="Data final de preenchimento dos comentários do gestor em DD/MM/AAAA (padrão: data atual + 15 dias).",
    )
    parser.add_argument(
        "--numero-fiscalizacao-comentarios-gestor",
        default=DEFAULT_FISCALIZACAO_NUMERO,
        help=f"Número da fiscalização usado no questionário de comentários do gestor (padrão: {DEFAULT_FISCALIZACAO_NUMERO}).",
    )
    parser.add_argument(
        "--nome-fiscalizacao-comentarios-gestor",
        default=DEFAULT_FISCALIZACAO_NOME,
        help=f"Nome da fiscalização usado no questionário de comentários do gestor (padrão: {DEFAULT_FISCALIZACAO_NOME}).",
    )
    parser.add_argument(
        "--ajustes-evidencias-comentarios-gestor",
        default="",
        help="Planilha de ajustes pós-avaliação de evidências usada para incluir seção opcional de reavaliação no survey.",
    )
    parser.add_argument(
        "--jobs-comentarios-gestor-anexos",
        type=int,
        default=DEFAULT_DOCX_WORKERS,
        help=f"Quantidade de workers para renderizar anexos DOCX (padrão: {DEFAULT_DOCX_WORKERS}).",
    )
    parser.add_argument(
        "--skip-comentarios-gestor-lss",
        action="store_true",
        help="Não gera o questionário LimeSurvey de comentários do gestor.",
    )
    parser.add_argument(
        "--skip-comentarios-gestor-anexos",
        action="store_true",
        help="Não gera os anexos DOCX de comentários do gestor.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        gerar_comentarios_gestor(args)
        logger.info("Geração de comentários do gestor finalizada.")
        return 0
    except Exception as exc:
        logger.error("Erro ao gerar comentários do gestor: %s", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
