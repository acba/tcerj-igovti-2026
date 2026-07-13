#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Exporta um PDF LimeSurvey por auditado com apenas os grupos aplicáveis.

O conjunto de colunas é derivado das expressões ``grelevance`` do LSS. No
questionário de comentários do gestor, essas expressões associam cada grupo ao
órgão armazenado em ``TOKEN:FIRSTNAME``.

A autenticação não é gravada no script. A sessão pode ser informada pela
variável ``LIMESURVEY_COOKIE``, por ``--cookie-file`` ou, se ambos forem
omitidos, em um prompt sem eco no terminal.
"""

from __future__ import annotations

import argparse
import datetime
import getpass
import html
import os
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit

import openpyxl
import requests


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = Path("C:/tmp/tcerj-igovti-2026/02-Execucao/05-Comentarios_Gestor/PDF_Respostas")
METADATA_FIELDS = [
    "id",
    "submitdate",
    "lastpage",
    "startlanguage",
    "seed",
    "token",
    "startdate",
    "datestamp",
]
PARTICIPANT_FIELDS = ["first_name", "last_name", "email_address"]
TOKEN_COMPARISON_RE = re.compile(r'TOKEN:FIRSTNAME\s*==\s*"((?:[^"\\]|\\.)*)"', re.IGNORECASE)
INVALID_FILENAME_RE = re.compile(r'[\\/:*?"<>|]')


@dataclass(frozen=True)
class Grupo:
    gid: str
    nome: str
    ordem: int
    relevancia: str


@dataclass(frozen=True)
class Questao:
    qid: str
    parent_qid: str
    gid: str
    tipo: str
    codigo: str
    ordem: int


@dataclass(frozen=True)
class Survey:
    sid: str
    grupos: tuple[Grupo, ...]
    questoes: tuple[Questao, ...]


@dataclass(frozen=True)
class Resposta:
    response_id: str
    orgao: str
    datestamp: str
    completed: str


def texto_normalizado(valor: object) -> str:
    texto = "" if valor is None else str(valor)
    texto = unicodedata.normalize("NFC", html.unescape(texto))
    return re.sub(r"\s+", " ", texto).strip()


def chave_orgao(valor: object) -> str:
    return texto_normalizado(valor).casefold()


def inteiro_seguro(valor: str, padrao: int = 0) -> int:
    try:
        return int(valor)
    except (TypeError, ValueError):
        return padrao


def row_xml(row: ET.Element) -> dict[str, str]:
    return {child.tag: child.text or "" for child in row}


def carregar_survey(path: Path) -> Survey:
    root = ET.parse(path).getroot()
    if (root.findtext("LimeSurveyDocType") or "").strip() != "Survey":
        raise ValueError(f"O arquivo não é um survey LimeSurvey válido: {path}")

    grupos_node = root.find("groups/rows")
    questoes_node = root.find("questions/rows")
    if grupos_node is None or questoes_node is None:
        raise ValueError("O LSS não contém as tabelas de grupos e questões esperadas.")

    grupos: list[Grupo] = []
    sids: set[str] = set()
    for node in grupos_node.findall("row"):
        row = row_xml(node)
        sids.add(row["sid"])
        grupos.append(
            Grupo(
                gid=row["gid"],
                nome=texto_normalizado(row["group_name"]),
                ordem=inteiro_seguro(row["group_order"]),
                relevancia=texto_normalizado(row["grelevance"]),
            )
        )

    questoes: list[Questao] = []
    for node in questoes_node.findall("row"):
        row = row_xml(node)
        sids.add(row["sid"])
        questoes.append(
            Questao(
                qid=row["qid"],
                parent_qid=row["parent_qid"] or "0",
                gid=row["gid"],
                tipo=row["type"],
                codigo=row["title"],
                ordem=inteiro_seguro(row["question_order"]),
            )
        )

    sids.discard("")
    if len(sids) != 1:
        raise ValueError(f"Esperado exatamente um survey id no LSS; encontrados: {sorted(sids)}")

    return Survey(
        sid=sids.pop(),
        grupos=tuple(sorted(grupos, key=lambda item: item.ordem)),
        questoes=tuple(sorted(questoes, key=lambda item: (item.gid, item.ordem))),
    )


def nomes_da_relevancia(expressao: str) -> set[str] | None:
    """Retorna os órgãos citados ou ``None`` para um grupo incondicional."""
    if not expressao or expressao == "1":
        return None

    nomes = TOKEN_COMPARISON_RE.findall(expressao)
    resto = TOKEN_COMPARISON_RE.sub("", expressao)
    resto = re.sub(r"\bOR\b|[()\s]", "", resto, flags=re.IGNORECASE)
    if not nomes or resto:
        raise ValueError(
            "Expressão de relevância de grupo não suportada. Esperava somente "
            f"comparações TOKEN:FIRSTNAME unidas por OR: {expressao!r}"
        )
    return {chave_orgao(nome.replace(r'\"', '"').replace(r"\\", "\\")) for nome in nomes}


def grupos_do_orgao(survey: Survey, orgao: str) -> list[Grupo]:
    chave = chave_orgao(orgao)
    selecionados: list[Grupo] = []
    for grupo in survey.grupos:
        nomes = nomes_da_relevancia(grupo.relevancia)
        if nomes is None or chave in nomes:
            selecionados.append(grupo)
    return selecionados


def nome_campo_limesurvey(sid: str, questao: Questao) -> str:
    if questao.parent_qid != "0":
        return f"{sid}X{questao.gid}X{questao.parent_qid}{questao.codigo}"
    return f"{sid}X{questao.gid}X{questao.qid}"


def campos_do_orgao(survey: Survey, grupos: list[Grupo]) -> list[str]:
    gids = {grupo.gid for grupo in grupos}
    campos = list(METADATA_FIELDS)
    for questao in survey.questoes:
        if questao.gid not in gids:
            continue
        campo = nome_campo_limesurvey(survey.sid, questao)
        campos.append(campo)
        if questao.tipo == "|":
            campos.append(f"{campo}_filecount")
    return campos


def carregar_respostas(path: Path) -> list[Resposta]:
    workbook = openpyxl.load_workbook(path, read_only=True, data_only=True)
    sheet = workbook.active
    rows = sheet.iter_rows(values_only=True)
    try:
        headers = [texto_normalizado(value).casefold() for value in next(rows)]
    except StopIteration as exc:
        raise ValueError(f"A planilha está vazia: {path}") from exc

    obrigatorias = {"id", "orgao", "datestamp", "completed"}
    faltantes = obrigatorias - set(headers)
    if faltantes:
        raise ValueError(f"Colunas ausentes na planilha: {', '.join(sorted(faltantes))}")
    indices = {nome: headers.index(nome) for nome in obrigatorias}

    respostas: list[Resposta] = []
    for row in rows:
        response_id = texto_normalizado(row[indices["id"]])
        orgao = texto_normalizado(row[indices["orgao"]])
        if not response_id and not orgao:
            continue
        respostas.append(
            Resposta(
                response_id=response_id,
                orgao=orgao,
                datestamp=texto_normalizado(row[indices["datestamp"]]),
                completed=texto_normalizado(row[indices["completed"]]),
            )
        )
    return respostas


def filtrar_respostas(respostas: list[Resposta], args: argparse.Namespace) -> list[Resposta]:
    selecionadas = [
        resposta
        for resposta in respostas
        if (args.include_incomplete or resposta.completed.casefold() in {"sim", "yes", "y", "1", "true"})
        and (not args.orgao or chave_orgao(resposta.orgao) in {chave_orgao(item) for item in args.orgao})
        and (not args.response_id or resposta.response_id in set(args.response_id))
    ]
    if args.latest_only:
        ultimas: dict[str, tuple[tuple[datetime.datetime, int], Resposta]] = {}
        for resposta in selecionadas:
            data = datetime.datetime.min
            for formato in ("%d/%m/%Y %H:%M:%S", "%d.%m.%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S"):
                try:
                    data = datetime.datetime.strptime(resposta.datestamp, formato)
                    break
                except ValueError:
                    pass
            criterio = (data, inteiro_seguro(resposta.response_id, -1))
            chave = chave_orgao(resposta.orgao)
            if chave not in ultimas or criterio > ultimas[chave][0]:
                ultimas[chave] = (criterio, resposta)
        selecionadas = [item[1] for item in ultimas.values()]
    return selecionadas


def ler_cookie(args: argparse.Namespace) -> str:
    if args.cookie_file:
        cookie = args.cookie_file.read_text(encoding="utf-8").strip()
    else:
        cookie = os.environ.get("LIMESURVEY_COOKIE", "").strip()
    if not cookie and not args.dry_run:
        cookie = getpass.getpass("Cole o cabeçalho Cookie da sessão LimeSurvey: ").strip()
    return cookie.removeprefix("Cookie:").strip()


def obter_csrf_token(cookie: str, args: argparse.Namespace) -> str:
    token = args.csrf_token or os.environ.get("LIMESURVEY_CSRF_TOKEN", "")
    if not token:
        match = re.search(r"(?:^|;\s*)YII_CSRF_TOKEN=([^;]+)", cookie, flags=re.IGNORECASE)
        if match:
            token = match.group(1)
    token = unquote(token.strip())
    if not token and not args.dry_run:
        token = getpass.getpass("YII_CSRF_TOKEN: ").strip()
    return token


def nome_arquivo(resposta: Resposta) -> str:
    orgao = INVALID_FILENAME_RE.sub("_", resposta.orgao)
    orgao = re.sub(r"\s+", " ", orgao).strip().rstrip(".") or "SEM_ORGAO"
    return f"{orgao}_id{resposta.response_id}_comentarios_gestor.pdf"


def payload_exportacao(
    survey: Survey,
    resposta: Resposta,
    campos: list[str],
    csrf_token: str,
    maior_response_id: int,
) -> list[tuple[str, str]]:
    dados = [
        ("YII_CSRF_TOKEN", csrf_token),
        ("type", "pdf"),
        ("csvfieldseparator", ","),
        ("completionstate", "complete"),
        ("exportlang", "pt-BR"),
        ("export_from", "1"),
        ("export_to", str(max(1, maior_response_id))),
        ("answers", "long"),
        ("convertyto", "1"),
        ("convertnto", "2"),
        ("maskequations", "Y"),
        ("headstyle", "full"),
        ("striphtmlcode", "1"),
        ("headspacetounderscores", "0"),
        ("abbreviatedtext", "0"),
        ("emcode", "0"),
        ("abbreviatedtextto", "15"),
        ("codetextseparator", ". "),
        ("sid", survey.sid),
        ("response_id", resposta.response_id),
    ]
    dados.extend(("colselect[]", campo) for campo in campos)
    dados.extend(("attribute_select[]", campo) for campo in PARTICIPANT_FIELDS)
    return dados


def validar_pdf(response: requests.Response) -> None:
    content_type = response.headers.get("Content-Type", "").casefold()
    inicio = response.content[:512].lstrip()
    if response.history and any("login" in item.url.casefold() for item in response.history):
        raise RuntimeError("Sessão expirada: o LimeSurvey redirecionou para a página de login.")
    if not inicio.startswith(b"%PDF"):
        trecho = inicio.decode("utf-8", errors="replace").replace("\n", " ")[:240]
        raise RuntimeError(
            f"O LimeSurvey não retornou um PDF (HTTP {response.status_code}, "
            f"Content-Type {content_type!r}). Início da resposta: {trecho!r}"
        )


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Exporta um PDF de respostas por auditado, selecionando no LSS apenas os grupos aplicáveis."
    )
    parser.add_argument("--lss", type=Path, required=True, help="Survey LimeSurvey .lss exportado.")
    parser.add_argument("--participantes", type=Path, required=True, help="XLSX com id, orgao, datestamp e completed.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--base-url",
        default="https://www.tcerj.tc.br/limesurvey-novo",
        help="URL base da instalação LimeSurvey.",
    )
    parser.add_argument("--survey-id", help="Sobrescreve/valida o survey id extraído do LSS.")
    parser.add_argument("--cookie-file", type=Path, help="Arquivo fora do repositório contendo o cabeçalho Cookie.")
    parser.add_argument("--csrf-token", help="CSRF explícito; normalmente é extraído do cookie.")
    parser.add_argument("--orgao", action="append", help="Processa somente este órgão; pode ser repetido.")
    parser.add_argument("--response-id", action="append", help="Processa somente este id; pode ser repetido.")
    parser.add_argument("--include-incomplete", action="store_true", help="Inclui respostas não concluídas.")
    parser.set_defaults(latest_only=True)
    parser.add_argument(
        "--all-responses",
        action="store_false",
        dest="latest_only",
        help="Exporta todas as respostas, em vez de somente a mais recente de cada órgão.",
    )
    parser.add_argument(
        "--include-unmatched",
        action="store_true",
        help="Inclui órgãos sem nenhum grupo condicional no LSS (útil para respostas de teste).",
    )
    parser.add_argument("--overwrite", action="store_true", help="Sobrescreve PDFs existentes.")
    parser.add_argument("--dry-run", action="store_true", help="Mostra grupos/campos sem acessar o LimeSurvey.")
    parser.add_argument("--timeout", type=int, default=180, help="Timeout de cada download, em segundos.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = criar_parser().parse_args(argv)
    survey = carregar_survey(args.lss)
    if args.survey_id and args.survey_id != survey.sid:
        raise ValueError(f"--survey-id {args.survey_id} diverge do id {survey.sid} contido no LSS.")

    respostas = filtrar_respostas(carregar_respostas(args.participantes), args)
    sem_grupo = [
        resposta
        for resposta in respostas
        if not any(nomes_da_relevancia(grupo.relevancia) is not None for grupo in grupos_do_orgao(survey, resposta.orgao))
    ]
    if sem_grupo and not args.include_unmatched:
        for resposta in sem_grupo:
            print(
                f"AVISO: ignorando {resposta.orgao!r} (id {resposta.response_id}): "
                "nenhum grupo condicional do LSS corresponde ao órgão.",
                file=sys.stderr,
            )
        ids_sem_grupo = {id(resposta) for resposta in sem_grupo}
        respostas = [resposta for resposta in respostas if id(resposta) not in ids_sem_grupo]
    if not respostas:
        raise ValueError("Nenhuma resposta corresponde aos filtros informados.")
    maior_response_id = max((inteiro_seguro(item.response_id, 1) for item in respostas), default=1)

    cookie = ler_cookie(args)
    csrf_token = obter_csrf_token(cookie, args)
    if not args.dry_run and (not cookie or not csrf_token):
        raise ValueError("Cookie e YII_CSRF_TOKEN são obrigatórios para o download.")

    session = requests.Session()
    session.headers.update(
        {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/150 Safari/537.36",
            "Cookie": cookie,
        }
    )
    endpoint = f"{args.base_url.rstrip('/')}/index.php/admin/export/sa/exportresults/surveyid/{survey.sid}"
    referer = f"{endpoint}/id/1"
    partes_url = urlsplit(args.base_url)
    origin = f"{partes_url.scheme}://{partes_url.netloc}"

    args.output_dir.mkdir(parents=True, exist_ok=True) if not args.dry_run else None
    falhas = 0
    total = len(respostas)
    for indice, resposta in enumerate(respostas, start=1):
        grupos = grupos_do_orgao(survey, resposta.orgao)
        campos = campos_do_orgao(survey, grupos)
        grupos_condicionais = [grupo for grupo in grupos if nomes_da_relevancia(grupo.relevancia) is not None]
        destino = args.output_dir / nome_arquivo(resposta)
        print(
            f"[{indice}/{total}] {resposta.orgao} (id {resposta.response_id}): "
            f"{len(grupos_condicionais)} grupos condicionais, {len(campos)} campos"
        )
        if args.dry_run:
            print("  " + "; ".join(f"{grupo.gid} - {grupo.nome}" for grupo in grupos_condicionais))
            continue
        if destino.exists() and destino.stat().st_size > 0 and not args.overwrite:
            print(f"  PULANDO: já existe {destino}")
            continue

        dados = payload_exportacao(survey, resposta, campos, csrf_token, maior_response_id)
        try:
            response = session.post(
                endpoint,
                data=dados,
                headers={"Origin": origin, "Referer": referer},
                timeout=args.timeout,
                allow_redirects=True,
            )
            response.raise_for_status()
            validar_pdf(response)
            temporario = destino.with_suffix(destino.suffix + ".part")
            temporario.write_bytes(response.content)
            temporario.replace(destino)
            print(f"  OK: {destino} ({len(response.content):,} bytes)")
        except Exception as exc:
            falhas += 1
            print(f"  ERRO: {exc}", file=sys.stderr)

    if args.dry_run:
        print(f"Validação concluída: {total} resposta(s); nenhum acesso de rede realizado.")
    elif falhas:
        print(f"Concluído com {falhas} falha(s) em {total} resposta(s).", file=sys.stderr)
    else:
        print(f"Concluído: {total} resposta(s) processada(s). PDFs em {args.output_dir}")
    return 1 if falhas else 0


if __name__ == "__main__":
    raise SystemExit(main())
