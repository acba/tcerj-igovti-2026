#!/usr/bin/env python3
"""Coleta, via EWS somente leitura, as comunicações que compõem o AN10.

O script usa o provedor OAuth2 do projeto AudCom. A consulta inicial traz apenas
metadados; corpos e anexos são buscados depois, somente para os candidatos.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from zoneinfo import ZoneInfo


BRASILIA = ZoneInfo("America/Sao_Paulo")
UTC = timezone.utc
INICIO = datetime(2026, 1, 1, tzinfo=UTC)
FIM = datetime.now(UTC)
CAIXA = "auditoriati@tcerj.tc.br"

ORGAOS = {
    "CEHAB": {
        "dominios": ("cehab.rj.gov.br",),
        "termos": ("CEHAB", "Companhia Estadual de Habitação do Rio de Janeiro"),
    },
    "EMOP": {
        "dominios": ("emop.rj.gov.br",),
        "termos": ("EMOP", "Empresa de Obras Públicas do Estado do Rio de Janeiro"),
    },
    "PESAGRO": {
        "dominios": ("pesagro.rj.gov.br",),
        "termos": ("PESAGRO", "Empresa de Pesquisa Agropecuária do Estado do Rio de Janeiro"),
    },
    "SEDCON": {
        "dominios": ("sedcon.rj.gov.br",),
        "termos": ("SEDCON", "Secretaria de Estado de Defesa do Consumidor"),
    },
    "SEPOL": {
        "dominios": ("pcivil.rj.gov.br",),
        "termos": ("SEPOL", "Secretaria de Estado de Polícia Civil"),
    },
    "SESP": {
        "dominios": ("sesp.rj.gov.br",),
        "termos": ("SESP", "Secretaria de Estado de Segurança Pública"),
    },
}

PASTAS = (
    ("Caixa de entrada", "datetime_received"),
    ("Mensagens enviadas", "datetime_sent"),
    ("2026_Audit_iGovTI", "datetime_received"),
)

CAMPOS_LEVES = (
    "subject",
    "datetime_received",
    "datetime_sent",
    "author",
    "sender",
    "to_recipients",
    "cc_recipients",
    "has_attachments",
    "internet_message_id_hdr",
)

CAMPOS_COMPLETOS = CAMPOS_LEVES + ("body", "text_body", "attachments")


def argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audcom-backend", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--listar", action="store_true", help="Somente lista os candidatos")
    parser.add_argument("--tentativas", type=int, default=3)
    parser.add_argument("--espera-busy", type=int, default=75)
    return parser.parse_args()


def carregar_audcom(backend: Path):
    backend = backend.resolve()
    sys.path.insert(0, str(backend))
    from app.ews_provider import EwsProvider  # noqa: PLC0415
    from app.ews_token import token_valido  # noqa: PLC0415
    from exchangelib import FileAttachment, Q  # noqa: PLC0415

    ok, diagnostico = token_valido()
    if not ok:
        raise RuntimeError(f"Token EWS inválido: {diagnostico}")
    return EwsProvider()._account(), FileAttachment, Q


def repetir_busy(func, tentativas: int, espera: int):
    for numero in range(1, tentativas + 1):
        try:
            return func()
        except Exception as exc:  # noqa: BLE001
            nome = type(exc).__name__
            texto = str(exc)
            if "ServerBusy" not in nome and "server busy" not in texto.lower():
                raise
            if numero == tentativas:
                raise
            print(f"EWS ocupado; nova tentativa em {espera}s ({numero}/{tentativas}).", flush=True)
            time.sleep(espera)
    raise AssertionError("laço de tentativas terminou inesperadamente")


def localizar_pastas(conta) -> dict[str, Any]:
    por_nome = {pasta.name: pasta for pasta in conta.root.walk()}
    ausentes = [nome for nome, _ in PASTAS if nome not in por_nome]
    if ausentes:
        raise RuntimeError(f"Pastas EWS não localizadas: {', '.join(ausentes)}")
    return {nome: por_nome[nome] for nome, _ in PASTAS}


def endereco(mailbox: Any) -> str:
    return ((getattr(mailbox, "email_address", "") or "").strip()) if mailbox else ""


def caixa_postal(mailbox: Any) -> str:
    if not mailbox:
        return ""
    nome = (getattr(mailbox, "name", "") or "").strip()
    email_ = endereco(mailbox)
    if nome and email_:
        return f"{nome} <{email_}>"
    return nome or email_


def caixas_postais(mailboxes: Iterable[Any] | None) -> str:
    return "; ".join(filter(None, (caixa_postal(item) for item in (mailboxes or []))))


def texto_metadados(item: Any) -> str:
    partes = [
        item.subject or "",
        endereco(item.author),
        endereco(item.sender),
        caixas_postais(item.to_recipients),
        caixas_postais(item.cc_recipients),
    ]
    return "\n".join(partes)


def orgaos_do_texto(texto: str) -> list[str]:
    resultado: list[str] = []
    minusculo = texto.casefold()
    for orgao, regra in ORGAOS.items():
        por_dominio = any(dominio.casefold() in minusculo for dominio in regra["dominios"])
        por_termo = any(
            re.search(rf"(?<![A-Z0-9]){re.escape(termo)}(?![A-Z0-9])", texto, re.IGNORECASE)
            for termo in regra["termos"]
        )
        if por_dominio or por_termo:
            resultado.append(orgao)
    return resultado


def relevante_metadados(item: Any) -> bool:
    assunto = item.subject or ""
    if re.search(r"17\s*/\s*2025", assunto, re.IGNORECASE):
        return False
    # O número 18/2026, isoladamente, identifica toda a fiscalização e não
    # associa o item a uma das seis organizações do AN10.
    return bool(orgaos_do_texto(texto_metadados(item)))


def chave_item(item: Any) -> str:
    message_id = (getattr(item, "internet_message_id_hdr", "") or "").strip().casefold()
    if message_id:
        return f"id:{message_id}"
    data = data_padrao(data_item(item), UTC).isoformat() if data_item(item) else ""
    base = "|".join((item.subject or "", data, endereco(item.author))).encode("utf-8")
    return "md5:" + hashlib.md5(base).hexdigest()  # noqa: S324 - chave de deduplicação, não criptografia


def data_item(item: Any) -> datetime | None:
    autor = endereco(item.author).casefold()
    enviado_pela_equipe = autor == CAIXA or autor.endswith("@tcerj.tc.br")
    data = item.datetime_sent if enviado_pela_equipe else item.datetime_received
    return data or item.datetime_received or item.datetime_sent


def data_padrao(data: datetime, fuso) -> datetime:
    """Converte EWSDateTime em datetime padrão sem exigir EWSTimeZone."""
    return datetime.fromtimestamp(data.timestamp(), tz=fuso)


def listar_candidatos(conta, pastas: dict[str, Any], Q, tentativas: int, espera: int):
    candidatos: dict[str, tuple[Any, str]] = {}
    estatisticas: dict[str, dict[str, int]] = {}
    termos_corpo = ("CEHAB", "EMOP", "PESAGRO", "SEDCON", "SEPOL", "SESP")

    for nome, campo_data in PASTAS:
        pasta = pastas[nome]
        filtro_data = {f"{campo_data}__gte": INICIO, f"{campo_data}__lte": FIM}

        def obter_leves():
            return list(pasta.filter(**filtro_data).only(*CAMPOS_LEVES))

        leves = repetir_busy(obter_leves, tentativas, espera)
        ids_corpo: set[str] = set()
        consulta_corpo_ok = True
        try:
            q_corpo = Q(body__icontains=termos_corpo[0])
            for termo in termos_corpo[1:]:
                q_corpo |= Q(body__icontains=termo)

            def obter_ids_corpo():
                return list(pasta.filter(q_corpo, **filtro_data).only("subject"))

            ids_corpo = {str(item.id) for item in repetir_busy(obter_ids_corpo, tentativas, espera)}
        except Exception as exc:  # noqa: BLE001
            consulta_corpo_ok = False
            print(f"AVISO: busca EWS no corpo falhou em {nome}: {type(exc).__name__}: {exc}", flush=True)

        selecionados = [item for item in leves if relevante_metadados(item) or str(item.id) in ids_corpo]
        excluidos_17 = sum(
            bool(re.search(r"17\s*/\s*2025", item.subject or "", re.IGNORECASE)) for item in selecionados
        )
        selecionados = [
            item for item in selecionados
            if not re.search(r"17\s*/\s*2025", item.subject or "", re.IGNORECASE)
        ]
        for item in selecionados:
            chave = chave_item(item)
            if chave not in candidatos:
                candidatos[chave] = (item, nome)
        estatisticas[nome] = {
            "listados": len(leves),
            "candidatos": len(selecionados),
            "excluidos_17_2025": excluidos_17,
            "busca_corpo_ok": int(consulta_corpo_ok),
        }
    return candidatos, estatisticas


def buscar_completos(conta, candidatos, pastas, tentativas: int, espera: int):
    por_pasta: dict[str, list[tuple[str, Any]]] = defaultdict(list)
    for chave, (item, nome) in candidatos.items():
        por_pasta[nome].append((chave, item))

    completos: list[tuple[Any, str]] = []
    for nome, pares in por_pasta.items():
        pasta = pastas[nome]
        for inicio in range(0, len(pares), 15):
            lote = pares[inicio:inicio + 15]

            def obter_lote():
                return list(conta.fetch(
                    ids=[item for _, item in lote],
                    folder=pasta,
                    only_fields=CAMPOS_COMPLETOS,
                    chunk_size=15,
                ))

            itens = repetir_busy(obter_lote, tentativas, espera)
            completos.extend((item, nome) for item in itens)
            print(f"{nome}: {min(inicio + len(lote), len(pares))}/{len(pares)} itens completos", flush=True)
    return completos


def corpo_textual(item: Any) -> str:
    if item.body:
        return str(item.body)
    if item.text_body:
        return str(item.text_body)
    return ""


def tsid_do_item(item: Any) -> tuple[str, bool]:
    assunto = item.subject or ""
    correspondencia = re.search(r"TSID\s*[-–—]?\s*0?([123])", assunto, re.IGNORECASE)
    if correspondencia:
        return f"TSID0{correspondencia.group(1)}", False
    if re.search(r"Of[ií]cio de Apresenta[cç][aã]o|Atendimento\s+TSID\s*0?1|Indica[cç][aã]o de empregado|Of\.SEPOL/ATA\s*N?[º°]?\s*251", assunto, re.IGNORECASE):
        return "TSID01", False
    return "TSID01", True


def tipo_do_item(item: Any) -> str:
    assunto = (item.subject or "").strip()
    autor = endereco(item.author).casefold()
    equipe = autor == CAIXA or autor.endswith("@tcerj.tc.br")
    if re.match(r"^(read|lida|read-receipt)\s*:", assunto, re.IGNORECASE):
        return "Ciencia-Confirmacao-Leitura"
    if not equipe:
        if re.match(r"^(fwd|enc)\s*:", assunto, re.IGNORECASE):
            return "Ciencia-Encaminhamento-Orgao"
        if re.search(r"Atendimento\s+TSID\s*0?1|Indica[cç][aã]o de empregado|Of\.SEPOL/ATA\s*N?[º°]?\s*251", assunto, re.IGNORECASE):
            return "Ciencia-Indicacao-Ponto-Focal"
        return "Ciencia-Responda-Orgao"
    if re.match(r"^(re|res)\s*:", assunto, re.IGNORECASE):
        return "Envio-Resposta-Equipe"
    if re.search(r"Termo de Reitera[cç][aã]o|Reitera[cç][aã]o", assunto, re.IGNORECASE):
        return "Envio-Termo-Reiteracao"
    if re.search(r"Lembrete", assunto, re.IGNORECASE):
        return "Envio-Lembrete"
    tsid, _ = tsid_do_item(item)
    if tsid == "TSID03":
        return "Envio-TSID03"
    if tsid == "TSID02":
        return "Envio-TSID02"
    return "Envio-TSID01-Oficio-Apresentacao"


def html_email(item: Any, data_brasil: datetime, anexos: list[str]) -> str:
    campos = (
        ("Assunto", item.subject or ""),
        ("De", caixa_postal(item.author)),
        ("Para", caixas_postais(item.to_recipients)),
        ("Cc", caixas_postais(item.cc_recipients)),
        ("Data", data_brasil.strftime("%d/%m/%Y %H:%M:%S %z")),
    )
    linhas = [f"<div><strong>{rotulo}:</strong> {html.escape(valor)}</div>" for rotulo, valor in campos]
    if anexos:
        lista = "".join(f"<li>{html.escape(nome)}</li>" for nome in anexos)
        linhas.append(f"<div><strong>Anexos:</strong><ul>{lista}</ul></div>")
    else:
        linhas.append("<div><strong>Anexos:</strong></div>")
    linhas.append(corpo_textual(item))
    return "\n".join(linhas)


def salvar_anexos(item: Any, pasta: Path, FileAttachment) -> tuple[list[str], list[str]]:
    nomes: list[str] = []
    falhas: list[str] = []
    anexos = list(item.attachments or [])
    if item.has_attachments or anexos:
        pasta.mkdir(parents=True, exist_ok=True)
    ids_vistos: set[str] = set()
    for anexo in anexos:
        nome_original = anexo.name or ""
        nome = re.sub(r'[\\/:*?"<>|\r\n]+', "_", nome_original).strip(" .") or "anexo"
        if not isinstance(anexo, FileAttachment):
            # Confirmações de leitura podem conter um ItemAttachment interno,
            # que não é um arquivo anexado pelo remetente.
            continue
        attachment_id = getattr(getattr(anexo, "attachment_id", None), "id", "") or ""
        if attachment_id and attachment_id in ids_vistos:
            continue
        ids_vistos.add(attachment_id)
        try:
            conteudo = anexo.content or b""
            destino = pasta / nome
            if destino.exists():
                if destino.read_bytes() == conteudo:
                    continue
                contador = 2
                while True:
                    candidato = pasta / f"{destino.stem} ({contador}){destino.suffix}"
                    if not candidato.exists():
                        destino = candidato
                        break
                    contador += 1
            destino.write_bytes(conteudo)
            nomes.append(destino.name)
        except Exception as exc:  # noqa: BLE001
            falhas.append(f"{nome_original}: {type(exc).__name__}: {exc}")
    return nomes, falhas


def gerar_saida(completos, output: Path, FileAttachment, estatisticas) -> tuple[list[dict[str, Any]], list[str]]:
    output.mkdir(parents=True, exist_ok=False)
    registros: list[dict[str, Any]] = []
    falhas: list[str] = []
    ambiguos: list[str] = []

    for item, pasta_origem in completos:
        assunto = item.subject or ""
        if re.search(r"17\s*/\s*2025", assunto, re.IGNORECASE):
            continue
        texto = texto_metadados(item) + "\n" + corpo_textual(item)
        orgaos = orgaos_do_texto(texto)
        if not orgaos:
            continue
        if len(orgaos) > 1:
            falhas.append(f"Organização ambígua ({', '.join(orgaos)}): {assunto}")
            continue
        orgao = orgaos[0]
        tsid, ambiguo = tsid_do_item(item)
        tipo = tipo_do_item(item)
        data = data_item(item)
        if data is None:
            falhas.append(f"Data ausente: {assunto}")
            continue
        data_utc = data_padrao(data, UTC)
        data_brasil = data_padrao(data, BRASILIA)
        base = f"{data_brasil:%Y-%m-%d_%H-%M-%S}_{orgao}_{tipo}"
        pasta_tsid = output / orgao / tsid
        pasta_tsid.mkdir(parents=True, exist_ok=True)
        arquivo = pasta_tsid / f"{base}.html"
        if arquivo.exists():
            falhas.append(f"Colisão de nome de arquivo: {arquivo.relative_to(output)}")
            continue
        pasta_anexos = pasta_tsid / f"{base}_anexos"
        anexos, erros_anexos = salvar_anexos(item, pasta_anexos, FileAttachment)
        falhas.extend(f"{arquivo.relative_to(output)} — {erro}" for erro in erros_anexos)
        arquivo.write_text(html_email(item, data_brasil, anexos), encoding="utf-8")
        relativo = arquivo.relative_to(output).as_posix()
        if ambiguo:
            ambiguos.append(relativo)
        registros.append({
            "arquivo": relativo,
            "org": orgao,
            "TSID": tsid,
            "tipo": tipo,
            "data_brasil": data_brasil.isoformat(),
            "data_utc": data_utc.isoformat().replace("+00:00", "Z"),
            "de_email": endereco(item.author),
            "para": "; ".join(endereco(x) for x in (item.to_recipients or []) if endereco(x)),
            "cc": "; ".join(endereco(x) for x in (item.cc_recipients or []) if endereco(x)),
            "assunto": assunto,
            "message_id": (getattr(item, "internet_message_id_hdr", "") or "").strip(),
            "pasta_origem": pasta_origem,
            "anexos": anexos,
            "item_original_has_attachments": bool(item.has_attachments),
        })

    registros.sort(key=lambda r: (r["org"], r["TSID"], r["data_utc"], r["arquivo"]))
    (output / "indice.json").write_text(json.dumps(registros, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    colunas = [
        "arquivo", "org", "TSID", "tipo", "data_brasil", "data_utc", "de_email", "para", "cc",
        "assunto", "message_id", "pasta_origem", "anexos", "item_original_has_attachments",
    ]
    with (output / "indice.csv").open("w", encoding="utf-8-sig", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=colunas)
        writer.writeheader()
        for registro in registros:
            linha = dict(registro)
            linha["anexos"] = "; ".join(registro["anexos"])
            writer.writerow(linha)
    escrever_leia_me(output, registros, ambiguos, falhas, estatisticas)
    return registros, falhas


def escrever_leia_me(output: Path, registros, ambiguos, falhas, estatisticas) -> None:
    contagens = Counter((r["org"], r["TSID"]) for r in registros)
    linhas = [
        "# AN10 — Comunicações das organizações não respondentes",
        "",
        "Coleção de mensagens da Fiscalização TCE-RJ nº 18/2026 (iGovTI 2026), extraídas em modo somente leitura da caixa `auditoriati@tcerj.tc.br`.",
        "",
        "## Estrutura e método",
        "",
        "Cada e-mail corresponde a um arquivo HTML. Quando o item original informa anexos, estes ficam na pasta de mesmo nome acrescida de `_anexos`. Os mapeamentos de organização, TSID e tipo constam apenas no nome do arquivo e nos índices.",
        "",
        "Foram varridas, de janeiro de 2026 até a data da extração, as pastas `Caixa de entrada`, `2026_Audit_iGovTI` e `Mensagens enviadas`. A listagem inicial consultou somente metadados; corpos e anexos foram obtidos apenas para candidatos. Itens repetidos foram deduplicados pelo cabeçalho Message-ID e, quando ausente, por MD5 de assunto, data e autor. As mensagens da Fiscalização de Contratações SETIC do exercício anterior foram excluídas.",
        "",
        "Os horários dos nomes de arquivo e do campo `data_brasil` estão em America/Sao_Paulo (UTC-03 no período). O índice também registra a data UTC. Os documentos HTML não contêm UTC nem texto de contextualização: somente os campos e o corpo do próprio e-mail.",
        "",
        "## Quantitativo",
        "",
        "| Organização | TSID01 | TSID02 | TSID03 | Total |",
        "|---|---:|---:|---:|---:|",
    ]
    for orgao in ORGAOS:
        valores = [contagens[(orgao, f"TSID0{n}")] for n in (1, 2, 3)]
        linhas.append(f"| {orgao} | {valores[0]} | {valores[1]} | {valores[2]} | {sum(valores)} |")
    linhas.extend(("", f"Total: **{len(registros)} e-mails**.", "", "## Limitações conhecidas", ""))
    linhas.append("O envio original do TSID01 de CEHAB, EMOP, PESAGRO e SEPOL não foi localizado nas três pastas consultadas; sua recuperação depende das caixas pessoais da equipe ou do SEI.")
    linhas.extend((
        "",
        "A referência preliminar indicava 49 mensagens. A varredura encontrou ainda dez itens que atendem aos critérios definidos: seis respostas recebidas no TSID01 (duas da CEHAB, uma da EMOP, uma da SEDCON e duas da SESP) e quatro confirmações iniciais de leitura do TSID02 (CEHAB, EMOP, SEPOL e SESP). Eles foram mantidos para preservar a completude da coleção.",
    ))
    if ambiguos:
        linhas.extend(("", "Mensagens sem referência explícita a TSID, classificadas como TSID01 conforme a regra de coleta:", ""))
        linhas.extend(f"- `{arquivo}`" for arquivo in ambiguos)
    else:
        linhas.extend(("", "Não houve mensagem classificada pela regra residual de TSID01."))
    if falhas:
        linhas.extend(("", "## Falhas que exigem conferência", ""))
        linhas.extend(f"- {falha}" for falha in falhas)
    linhas.extend(("", "## Diagnóstico da varredura", ""))
    for nome, dados in estatisticas.items():
        linhas.append(
            f"- {nome}: {dados['listados']} itens no período; {dados['candidatos']} candidatos; "
            f"busca no corpo={'ok' if dados['busca_corpo_ok'] else 'falhou'}; "
            f"exclusões explícitas da fiscalização SETIC anterior={dados['excluidos_17_2025']}."
        )
    (output / "LEIA-ME.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")


def main() -> int:
    args = argumentos()
    if not args.listar and args.output_dir is None:
        raise SystemExit("Informe --output-dir ou use --listar")
    if args.output_dir and args.output_dir.exists():
        raise SystemExit(f"O destino já existe: {args.output_dir}")
    conta, FileAttachment, Q = carregar_audcom(args.audcom_backend)
    pastas = localizar_pastas(conta)
    candidatos, estatisticas = listar_candidatos(
        conta, pastas, Q, args.tentativas, args.espera_busy,
    )
    print(json.dumps(estatisticas, ensure_ascii=False, indent=2), flush=True)
    print(f"Candidatos deduplicados: {len(candidatos)}", flush=True)
    if args.listar:
        for item, pasta in sorted(candidatos.values(), key=lambda par: data_item(par[0]) or INICIO):
            print(f"{data_item(item)} | {pasta} | {endereco(item.author)} | {item.subject}")
        return 0
    completos = buscar_completos(
        conta, candidatos, pastas, args.tentativas, args.espera_busy,
    )
    registros, falhas = gerar_saida(completos, args.output_dir.resolve(), FileAttachment, estatisticas)
    print(f"Registros gerados: {len(registros)}", flush=True)
    print(f"Falhas: {len(falhas)}", flush=True)
    return 2 if falhas else 0


if __name__ == "__main__":
    raise SystemExit(main())
