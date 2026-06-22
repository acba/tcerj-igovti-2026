from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import tempfile
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import unquote

from openpyxl import Workbook

from .pipeline import (
    REMOTE_PROVIDERS,
    ItemAfirmado,
    PacoteEvidencia,
    RequestsPerMinuteLimiter,
    _resolver_evidencia_exportada_limesurvey,
    arquivos_compativeis_upload,
    carregar_achados_set,
    carregar_registros_analise,
    deve_processar_identidade,
    erro_tecnico_bloqueante_pacote,
    gravar_registro_analise,
    hash_arquivo,
    log_event,
    normalizar_evidencia,
    validar_rpm,
    _extrair_pdf_markdown_imagens,
    _extrair_docx_html_imagens,
    _processar_zip_com_preprocessamento,
)
from .providers_ai_service import executar_provider, estimar_tokens_payload

PROMPT_JUIZ_PADRAO = """Voce atua como equipe de auditoria governamental revisando avaliacoes preliminares de evidencias.

Sua tarefa e produzir um parecer consolidado de evidencia, revisavel pela equipe de auditoria, a partir de:
- a evidencia enviada pelo auditado, quando disponivel;
- avaliacoes preliminares;
- a opiniao da equipe de auditoria, quando fornecida.

Postura e linguagem:
- Use linguagem impessoal, imparcial, objetiva e simples.
- Nao trate o parecer consolidado como decisao final de auditoria.
- Nao use conhecimento externo para preencher lacunas da evidencia.
- Nao cite nomes de provedores ou modelos de IA, mesmo que aparecam nos dados recebidos.
- Nao escreva frases como "o modelo X avaliou", "todos os modelos analisados" ou equivalentes.
- Ao se referir a avaliacoes anteriores, use formulacoes institucionais e trate elas no singular: "A Equipe de Auditoria avalia que...", "A avaliacao da Equipe de Auditoria indica que..." ou "A avaliação realizada indica que...".

Regras de analise:
- Consolide a opinião majoritária apresentada nas avaliacoes recebidas.
- Se a opiniao da equipe de auditoria divergir das avaliacoes recebidas, explique criticamente o motivo da conclusao adotada.
- Fundamente cada conclusao com elementos da evidencia e/ou com a avaliacao critica das opinioes recebidas.
- Declare lacunas quando a evidencia ou as avaliacoes recebidas nao forem suficientes.

Padrao da justificativa:
- Escreva a justificativa como um paragrafo curto, preferencialmente com 3 a 5 frases.
- Siga esta ordem: conclusao objetiva; elementos da evidencia que sustentam a conclusao; análise crítica da suficiência da evidência; lacuna ou limitacao relevante, quando existir.
- Quando a evidencia for suficiente, indique o elemento verificavel utilizado, como trecho, pagina, tabela, ato, registro, imagem ou documento.
- Quando a evidencia for insuficiente, indique exatamente o elemento faltante.
- Nao inclua listas longas, digressoes, linguagem opinativa ou mencao a nomes de modelos.
- Não mencione avaliações recebidas, modelos, provedores, pluralidade de análises ou processo de consolidação.

Retorne somente JSON no schema solicitado.
"""


@dataclass(frozen=True)
class ChaveEvidencia:
    auditado: str
    questao: str
    coluna_evidencia: str
    evidencia: str


@dataclass(frozen=True)
class GrupoEvidencia:
    chave: ChaveEvidencia
    opinioes: list[dict[str, Any]]


def carregar_registros_processamento(caminhos: Iterable[str | Path]) -> list[dict[str, Any]]:
    registros_por_identidade: dict[str, dict[str, Any]] = {}
    sem_identidade: list[dict[str, Any]] = []
    for caminho in caminhos:
        path = Path(caminho)
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            registro = json.loads(line)
            registro["_source"] = str(path)
            registro["_line"] = line_number
            identidade = registro.get("identity")
            if isinstance(identidade, str) and identidade:
                registros_por_identidade[identidade] = registro
            else:
                sem_identidade.append(registro)
    return [*registros_por_identidade.values(), *sem_identidade]


def chave_evidencia(registro: dict[str, Any]) -> ChaveEvidencia:
    return ChaveEvidencia(
        auditado=str(registro.get("auditado") or ""),
        questao=str(registro.get("questao") or ""),
        coluna_evidencia=str(registro.get("coluna_evidencia") or ""),
        evidencia=str(registro.get("evidencia") or ""),
    )


def agrupar_opinioes_por_evidencia(registros: Iterable[dict[str, Any]]) -> list[GrupoEvidencia]:
    grupos: dict[ChaveEvidencia, list[dict[str, Any]]] = {}
    for registro in registros:
        chave = chave_evidencia(registro)
        grupos.setdefault(chave, []).append(registro)
    return [
        GrupoEvidencia(chave=chave, opinioes=opinioes)
        for chave, opinioes in sorted(
            grupos.items(),
            key=lambda item: (
                item[0].auditado,
                item[0].questao,
                item[0].coluna_evidencia,
                item[0].evidencia,
            ),
        )
    ]


def itens_afirmados_do_grupo(opinioes: list[dict[str, Any]]) -> list[ItemAfirmado]:
    por_codigo: dict[str, ItemAfirmado] = {}
    for opiniao in opinioes:
        result = opiniao.get("result") if isinstance(opiniao.get("result"), dict) else {}
        for conclusao in result.get("conclusoes") or []:
            if not isinstance(conclusao, dict):
                continue
            codigo = str(conclusao.get("item_codigo") or "")
            if not codigo or codigo in por_codigo:
                continue
            por_codigo[codigo] = ItemAfirmado(
                codigo=codigo,
                texto=str(conclusao.get("item_texto") or ""),
                afirmacao=str(conclusao.get("afirmacao_auditado") or ""),
            )
    return list(por_codigo.values())


def _opiniao_modelo(registro: dict[str, Any]) -> dict[str, Any]:
    result = registro.get("result") if isinstance(registro.get("result"), dict) else {}
    return {
        "identity": registro.get("identity", ""),
        "provider": registro.get("provider", ""),
        "model": registro.get("model", ""),
        "finished_at": registro.get("finished_at", ""),
        "source": registro.get("_source", ""),
        "conclusoes": result.get("conclusoes", []),
    }


def opinioes_modelos_do_grupo(opinioes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [_opiniao_modelo(registro) for registro in opinioes]


def avaliacoes_preliminares_para_juiz(opinioes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    avaliacoes: list[dict[str, Any]] = []
    for index, registro in enumerate(opinioes, start=1):
        result = registro.get("result") if isinstance(registro.get("result"), dict) else {}
        avaliacoes.append(
            {
                "avaliacao_id": f"avaliacao_{index}",
                "finished_at": registro.get("finished_at", ""),
                "conclusoes": result.get("conclusoes", []),
            }
        )
    return avaliacoes


def _hash_json(payload: Any) -> str:
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def calcular_identidade_parecer(
    *,
    chave: ChaveEvidencia,
    opinioes: list[dict[str, Any]],
    judge_provider: str,
    judge_model: str,
    prompt_hash: str,
    prompt_version: str,
    evidence_hash: str = "",
    opiniao_auditoria: str = "",
) -> str:
    opinioes_para_identidade = [
        {
            "identity": registro.get("identity", ""),
            "provider": registro.get("provider", ""),
            "model": registro.get("model", ""),
            "result": registro.get("result", {}),
        }
        for registro in opinioes
    ]
    payload = {
        "auditado": chave.auditado,
        "questao": chave.questao,
        "coluna_evidencia": chave.coluna_evidencia,
        "evidencia": chave.evidencia,
        "opinioes_hash": _hash_json(opinioes_para_identidade),
        "opiniao_auditoria_hash": hashlib.sha256(opiniao_auditoria.encode("utf-8")).hexdigest(),
        "evidence_hash": evidence_hash,
        "judge_provider": judge_provider,
        "judge_model": judge_model,
        "prompt_hash": prompt_hash,
        "prompt_version": prompt_version,
    }
    return _hash_json(payload)


def _normalizar_nome(valor: str) -> str:
    sem_acentos = unicodedata.normalize("NFKD", valor).encode("ascii", "ignore").decode("ascii")
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in sem_acentos).strip("-")


def referencias_arquivos_do_grupo(opinioes: list[dict[str, Any]]) -> list[str]:
    referencias: list[str] = []
    for opiniao in opinioes:
        result = opiniao.get("result") if isinstance(opiniao.get("result"), dict) else {}
        for conclusao in result.get("conclusoes") or []:
            if not isinstance(conclusao, dict):
                continue
            for referencia in conclusao.get("arquivos_referenciados") or []:
                if isinstance(referencia, str) and referencia:
                    referencias.append(referencia)
    return referencias


def localizar_evidencia(
    raiz_evidencias: str | Path,
    chave: ChaveEvidencia,
    *,
    referencias_arquivos: Iterable[str] = (),
) -> Path | None:
    auditado_dir = Path(raiz_evidencias) / chave.auditado
    if not auditado_dir.is_dir():
        return None
    nomes = [unquote(chave.evidencia), chave.evidencia]
    for nome in nomes:
        caminho = auditado_dir / nome
        if caminho.is_file():
            return caminho
    for referencia in referencias_arquivos:
        nome_referencia = Path(unquote(referencia)).name
        caminho = auditado_dir / nome_referencia
        if caminho.is_file():
            return caminho
    exportado = _resolver_evidencia_exportada_limesurvey(auditado_dir, unquote(chave.evidencia))
    if exportado:
        return exportado
    alvo = _normalizar_nome(unquote(chave.evidencia))
    for candidato in auditado_dir.iterdir():
        if candidato.is_file() and _normalizar_nome(candidato.name) == alvo:
            return candidato
    return None


def _texto_opiniao_auditoria(registro: dict[str, Any]) -> str:
    for campo in ["opiniao_auditoria", "opiniao", "comentario", "justificativa", "parecer"]:
        valor = registro.get(campo)
        if valor not in (None, ""):
            return str(valor)
    return ""


def _chave_opiniao_auditoria(registro: dict[str, Any]) -> tuple[str, str, str, str]:
    return (
        str(registro.get("auditado") or ""),
        str(registro.get("questao") or ""),
        str(registro.get("coluna_evidencia") or ""),
        str(registro.get("evidencia") or ""),
    )


def carregar_opinioes_auditoria(caminho: str | Path | None) -> dict[tuple[str, str, str, str], str]:
    if not caminho:
        return {}
    path = Path(caminho)
    registros: list[dict[str, Any]] = []
    if path.suffix.lower() == ".jsonl":
        registros = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    elif path.suffix.lower() == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            registros = [item for item in payload if isinstance(item, dict)]
        elif isinstance(payload, dict):
            if isinstance(payload.get("opinioes"), list):
                registros = [item for item in payload["opinioes"] if isinstance(item, dict)]
            else:
                return {
                    tuple(str(part) for part in key.split("|", 3)): str(value)
                    for key, value in payload.items()
                    if isinstance(key, str) and key.count("|") == 3
                }
    elif path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            registros = list(csv.DictReader(file))
    return {
        _chave_opiniao_auditoria(registro): _texto_opiniao_auditoria(registro)
        for registro in registros
        if _texto_opiniao_auditoria(registro)
    }


def opiniao_auditoria_para_grupo(
    opinioes_auditoria: dict[tuple[str, str, str, str], str],
    grupo: GrupoEvidencia,
) -> str:
    chave = grupo.chave
    candidatos = [
        (chave.auditado, chave.questao, chave.coluna_evidencia, chave.evidencia),
        (chave.auditado, "", chave.coluna_evidencia, chave.evidencia),
        (chave.auditado, chave.questao, "", chave.evidencia),
        (chave.auditado, "", "", chave.evidencia),
    ]
    for candidato in candidatos:
        if candidato in opinioes_auditoria:
            return opinioes_auditoria[candidato]
    return ""


def executar_juiz_fake(chave: ChaveEvidencia, opinioes: list[dict[str, Any]], itens: list[ItemAfirmado]) -> dict[str, Any]:
    modelos = sorted(
        {
            f"{opiniao.get('provider', '')}/{opiniao.get('model', '')}".strip("/")
            for opiniao in opinioes
        }
    )
    return {
        "status": "completed",
        "conclusoes": [
            {
                "item_codigo": item.codigo,
                "item_texto": item.texto,
                "afirmacao_auditado": item.afirmacao,
                "estado": "inconclusivo",
                "justificativa": "Juiz fake nao emite parecer substantivo.",
                "lacunas": ["Parecer consolidado real de IA nao executado."],
                "arquivos_referenciados": [chave.evidencia],
                "trechos_ou_elementos": modelos,
                "paginas_ou_localizacao": [],
            }
            for item in itens
        ],
    }


def _chave_parecer_logico(registro: dict[str, Any]) -> tuple[str, str, str, str, str, str]:
    return (
        str(registro.get("auditado") or ""),
        str(registro.get("questao") or ""),
        str(registro.get("coluna_evidencia") or ""),
        str(registro.get("evidencia") or ""),
        str(registro.get("judge_provider") or ""),
        str(registro.get("judge_model") or ""),
    )


def registros_pareceres_mais_recentes(registros: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    mais_recentes: dict[tuple[str, str, str, str, str, str], dict[str, Any]] = {}
    for registro in registros:
        chave = _chave_parecer_logico(registro)
        atual = mais_recentes.get(chave)
        if atual is None or str(registro.get("finished_at") or "") >= str(atual.get("finished_at") or ""):
            mais_recentes[chave] = registro
    return list(mais_recentes.values())


def gerar_relatorio_pareceres(checkpoint: str | Path, destino: str | Path) -> int:
    registros = carregar_registros_analise(checkpoint)
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Pareceres consolidados"
    sheet.append(
        [
            "auditado",
            "questao",
            "coluna_evidencia",
            "evidencia",
            "item",
            "afirmacao_auditado",
            "estado",
            "justificativa",
            "lacunas",
            "referencias",
            "judge_provider",
            "judge_model",
            "opinioes_modelos",
            "opiniao_auditoria",
            "data_parecer",
        ]
    )
    total = 0
    for registro in registros_pareceres_mais_recentes(registros.values()):
        result = registro.get("result") if isinstance(registro.get("result"), dict) else {}
        for conclusao in result.get("conclusoes") or []:
            if not isinstance(conclusao, dict):
                continue
            total += 1
            sheet.append(
                [
                    registro.get("auditado", ""),
                    registro.get("questao", ""),
                    registro.get("coluna_evidencia", ""),
                    registro.get("evidencia", ""),
                    conclusao.get("item_codigo", ""),
                    conclusao.get("afirmacao_auditado", ""),
                    conclusao.get("estado", ""),
                    conclusao.get("justificativa", ""),
                    "; ".join(str(item) for item in conclusao.get("lacunas") or []),
                    "; ".join(str(item) for item in conclusao.get("arquivos_referenciados") or []),
                    registro.get("judge_provider", ""),
                    registro.get("judge_model", ""),
                    registro.get("opinion_count", 0),
                    "sim" if registro.get("opiniao_auditoria") else "nao",
                    registro.get("finished_at", ""),
                ]
            )
    destino_path = Path(destino)
    destino_path.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(destino_path)
    return total


def questoes_achado_de_prompts_dir(
    prompts_dir: str | Path | None = None,
    catalog: str | Path | None = None,
) -> set[str]:
    return carregar_achados_set(prompts_dir, catalog)


def questoes_achado_de_registros(registros: Iterable[dict[str, Any]]) -> set[str]:
    questoes: set[str] = set()
    for registro in registros:
        if registro.get("gera_achado") and registro.get("questao"):
            questoes.add(str(registro["questao"]))
    return questoes


def _chave_logica_parecer(registro: dict[str, Any]) -> tuple[str, str, str, str, str]:
    """Chave logica de um parecer: (auditado, coluna, evidencia, judge_provider, judge_model)."""
    return (
        str(registro.get("auditado") or ""),
        str(registro.get("coluna_evidencia") or ""),
        str(registro.get("evidencia") or ""),
        str(registro.get("judge_provider") or ""),
        str(registro.get("judge_model") or ""),
    )


def _indices_chaves_logicas(registros: dict[str, dict[str, Any]]) -> dict[tuple[str, str, str, str, str], str]:
    """Mapeia chave logica -> identity do registro mais recente."""
    resultado: dict[tuple[str, str, str, str, str], str] = {}
    for identity, registro in registros.items():
        chave = _chave_logica_parecer(registro)
        atual = resultado.get(chave)
        if atual is None or str(registro.get("finished_at") or "") >= str(registros[atual].get("finished_at") or ""):
            resultado[chave] = identity
    return resultado


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Consolida opinioes de modelos em um parecer por evidencia.")
    parser.add_argument("analyses", nargs="+", help="Arquivos analyses.jsonl gerados pelo processamento de evidencias.")
    parser.add_argument("--evidencias-root", default=None, help="Raiz de evidencias para reenviar a evidencia ao juiz.")
    parser.add_argument("--auditor-opinions", default=None, help="JSON/JSONL/CSV com opinioes opcionais da auditoria.")
    parser.add_argument("--judge-provider", default="fake")
    parser.add_argument("--judge-model", default="fake")
    parser.add_argument("--out-dir", default=".saida_analise")
    parser.add_argument("--prompt-version", default="juiz-v2")
    parser.add_argument("--rpm", type=validar_rpm, default=0)
    parser.add_argument("--skip-errors", action="store_true")
    parser.add_argument("--list-only", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument(
        "--reasoning",
        "--reasoning-effort",
        dest="reasoning_effort",
        choices=["low", "medium", "high"],
        default="",
        help="Nivel de reasoning a solicitar ao juiz quando suportado: low, medium ou high.",
    )
    parser.add_argument(
        "--store-prompts",
        action="store_true",
        help="Armazena o payload textual completo enviado ao juiz em cada registro JSONL.",
    )
    parser.add_argument(
        "--only-achados",
        action="store_true",
        help="Consolida somente grupos cuja questao-raiz enseja achado no mapa de verificacao. "
        "O conjunto de questoes-achado e obtido de --prompts-dir (marcadores gera_achado) ou, "
        "na ausencia deste, do campo gera_achado dos registros analyses.",
    )
    parser.add_argument(
        "--prompts-dir",
        default=None,
        help="Diretorio com prompts markdown usado para derivar o conjunto de questoes-achado "
        "quando --only-achados estiver ativo (fallback via marcadores no markdown).",
    )
    parser.add_argument(
        "--catalog",
        default=None,
        help="Caminho do catalogo YAML de prompts. Fonte primaria do conjunto de questoes-achado "
        "quando --only-achados esta ativo (le o atributo gera_achado do YAML).",
    )
    parser.add_argument(
        "--pdf2md",
        action="store_true",
        help="Converte PDFs para markdown+imagens com pymupdf4llm antes de enviar ao juiz.",
    )
    parser.add_argument(
        "--docx2html",
        action="store_true",
        help="Converte DOCX para HTML+imagens com mammoth antes de enviar ao juiz.",
    )
    parser.add_argument(
        "--pdf2md-dpi",
        type=int,
        default=150,
        help="DPI para extracao de imagens no pdf2md (default: 150).",
    )
    args = parser.parse_args(argv)

    log_event(
        "consolidation_started",
        "Inicio da consolidacao de pareceres por evidencia.",
        quiet=args.quiet,
        analyses=args.analyses,
        evidencias_root=args.evidencias_root or "",
        judge_provider=args.judge_provider,
        judge_model=args.judge_model,
        out_dir=args.out_dir,
        only_achados=args.only_achados,
        catalog=args.catalog or "",
        prompts_dir=args.prompts_dir or "",
    )
    registros_origem = carregar_registros_processamento(args.analyses)
    grupos = agrupar_opinioes_por_evidencia(registros_origem)
    if args.only_achados:
        if args.catalog or args.prompts_dir:
            achados_set = questoes_achado_de_prompts_dir(args.prompts_dir, args.catalog)
        else:
            achados_set = questoes_achado_de_registros(registros_origem)
        if not achados_set:
            parser.error(
                "--only-achados ativo, mas nenhum gera_achado encontrado no catalogo YAML "
                "(--catalog), nos marcadores dos prompts (--prompts-dir) ou nos registros analyses."
            )
        total_grupos_antes = len(grupos)
        grupos = [g for g in grupos if g.chave.questao in achados_set]
        log_event(
            "consolidation_filtered_achados",
            "Grupos filtrados para questoes que ensejam achado.",
            quiet=args.quiet,
            only_achados=True,
            catalog=args.catalog or "",
            prompts_dir=args.prompts_dir or "",
            questoes_achado=sorted(achados_set),
            total_grupos_antes=total_grupos_antes,
            total_grupos_depois=len(grupos),
        )
    if args.list_only:
        for grupo in grupos:
            print(
                json.dumps(
                    {
                        **grupo.chave.__dict__,
                        "opinioes": len(grupo.opinioes),
                        "modelos": [
                            {
                                "provider": opiniao.get("provider", ""),
                                "model": opiniao.get("model", ""),
                            }
                            for opiniao in grupo.opinioes
                        ],
                    },
                    ensure_ascii=False,
                )
            )
        return 0

    opinioes_auditoria = carregar_opinioes_auditoria(args.auditor_opinions)
    out_dir = Path(args.out_dir)
    checkpoint = out_dir / "consolidated.jsonl"
    registros_checkpoint = carregar_registros_analise(checkpoint)
    prompt_hash = hashlib.sha256(PROMPT_JUIZ_PADRAO.encode("utf-8")).hexdigest()
    rate_limiter = RequestsPerMinuteLimiter(args.rpm)
    total_processados = 0
    total_pulados = 0
    total_erros = 0
    total_concluidos = 0

    for index, grupo in enumerate(grupos, start=1):
        chave = grupo.chave
        consolidation_started_at = dt.datetime.now(dt.timezone.utc)
        
        # Filtrar opinioes validas e identificar erros
        opinioes_validas = []
        opinioes_erro = []
        for opiniao in grupo.opinioes:
            result_op = opiniao.get("result") if isinstance(opiniao.get("result"), dict) else {}
            if opiniao.get("status") != "completed" or result_op.get("status") != "completed":
                opinioes_erro.append(opiniao)
            else:
                conclusoes = result_op.get("conclusoes")
                if not isinstance(conclusoes, list):
                    opinioes_erro.append(opiniao)
                else:
                    opinioes_validas.append(opiniao)

        if opinioes_erro and opinioes_validas:
            erros_desc = []
            for op in opinioes_erro:
                res_op = op.get("result") if isinstance(op.get("result"), dict) else {}
                msg = op.get("error") or res_op.get("error") or "erro desconhecido"
                erros_desc.append(f"{op.get('provider')}/{op.get('model')}: {msg}")
            log_event(
                "consolidation_partial_errors",
                "Algumas avaliacoes de modelos falharam. Procedendo apenas com as validas.",
                level="warning",
                quiet=args.quiet,
                erros="; ".join(erros_desc),
                auditado=chave.auditado,
                questao=chave.questao,
                coluna_evidencia=chave.coluna_evidencia,
                evidencia=chave.evidencia,
            )

        itens = itens_afirmados_do_grupo(opinioes_validas)
        opiniao_auditoria = opiniao_auditoria_para_grupo(opinioes_auditoria, grupo)
        caminho_evidencia = (
            localizar_evidencia(
                args.evidencias_root,
                chave,
                referencias_arquivos=referencias_arquivos_do_grupo(opinioes_validas),
            )
            if args.evidencias_root
            else None
        )
        evidence_hash = hash_arquivo(caminho_evidencia) if caminho_evidencia else ""
        identity = calcular_identidade_parecer(
            chave=chave,
            opinioes=opinioes_validas,
            judge_provider=args.judge_provider,
            judge_model=args.judge_model,
            prompt_hash=prompt_hash,
            prompt_version=args.prompt_version,
            evidence_hash=evidence_hash,
            opiniao_auditoria=opiniao_auditoria,
        )
        base_log = {
            "index": index,
            "total": len(grupos),
            "identity": identity,
            "auditado": chave.auditado,
            "questao": chave.questao,
            "coluna_evidencia": chave.coluna_evidencia,
            "evidencia": chave.evidencia,
            "opinioes": len(opinioes_validas),
        }
        # Dedup por chave logica (auditado, coluna, evidencia, juiz) em vez de identity
        chave_logica = (chave.auditado, chave.coluna_evidencia, chave.evidencia, args.judge_provider, args.judge_model)
        indices_logicos = _indices_chaves_logicas(registros_checkpoint)
        identity_existente = indices_logicos.get(chave_logica)
        if identity_existente and registros_checkpoint[identity_existente].get("status") == "completed":
            total_pulados += 1
            log_event(
                "consolidation_skipped",
                "Parecer consolidado ignorado por checkpoint (chave logica).",
                quiet=args.quiet,
                **base_log,
            )
            continue
        pacote_evidencia = {"documentos": [], "inventario": [], "erro": "evidencia nao informada para o juiz"}
        arquivos_upload: list[str] = []
        with tempfile.TemporaryDirectory() as upload_tmp:
            if caminho_evidencia:
                pacote = normalizar_evidencia(caminho_evidencia)
                log_event(
                    "evidence_normalized",
                    "Evidencia normalizada para envio ao juiz.",
                    quiet=args.quiet,
                    level="warning" if pacote.erro else "info",
                    tipo=pacote.tipo,
                    documentos=len(pacote.documentos),
                    inventario=len(pacote.inventario),
                    error=pacote.erro,
                    **base_log,
                )
                try:
                    suffix_evidencia = caminho_evidencia.suffix.lower()
                    if args.pdf2md and suffix_evidencia == ".pdf":
                        pacote_extraido, arquivos_upload, erro_extracao = _extrair_pdf_markdown_imagens(
                            caminho_evidencia,
                            Path(upload_tmp),
                            caminho_evidencia.name,
                            dpi=args.pdf2md_dpi,
                        )
                        if erro_extracao:
                            raise RuntimeError(erro_extracao)
                        if pacote_extraido is not None:
                            pacote = pacote_extraido
                    elif args.docx2html and suffix_evidencia == ".docx":
                        pacote_extraido, arquivos_upload, erro_extracao = _extrair_docx_html_imagens(
                            caminho_evidencia,
                            Path(upload_tmp),
                            caminho_evidencia.name,
                        )
                        if erro_extracao:
                            raise RuntimeError(erro_extracao)
                        if pacote_extraido is not None:
                            pacote = pacote_extraido
                    elif suffix_evidencia == ".zip" and (args.pdf2md or args.docx2html):
                        pacote_extraido, arquivos_upload, erro_extracao = _processar_zip_com_preprocessamento(
                            caminho_evidencia,
                            Path(upload_tmp),
                            pdf2md=args.pdf2md,
                            docx2html=args.docx2html,
                            dpi=args.pdf2md_dpi,
                        )
                        if erro_extracao:
                            raise RuntimeError(erro_extracao)
                        if pacote_extraido is not None:
                            pacote = pacote_extraido
                    else:
                        arquivos_upload = arquivos_compativeis_upload(caminho_evidencia, upload_tmp)
                except RuntimeError as exc:
                    pacote = PacoteEvidencia(
                        caminho=caminho_evidencia,
                        tipo=suffix_evidencia.lstrip("."),
                        documentos=[],
                        inventario=[],
                        erro=f"erro ao preparar evidencia para o juiz: {exc}",
                    )
                    arquivos_upload = []
                    log_event(
                        "upload_prepare_error",
                        "Erro ao preparar evidencia para upload ao juiz.",
                        quiet=args.quiet,
                        level="error",
                        error=str(exc),
                        **base_log,
                    )
                pacote_evidencia = {
                    "documentos": pacote.documentos,
                    "inventario": pacote.inventario,
                    "erro": pacote.erro,
                    "arquivos_upload": arquivos_upload,
                }
            elif args.evidencias_root:
                pacote_evidencia["erro"] = "evidencia nao localizada na raiz informada"

            payload_pacote = {
                **pacote_evidencia,
                "avaliacoes_preliminares": avaliacoes_preliminares_para_juiz(opinioes_validas),
                "opiniao_auditoria": opiniao_auditoria,
                "papel_do_resultado": "parecer consolidado revisavel pela equipe de auditoria",
            }
            erro_ativo = None
            if not opinioes_validas:
                erros_desc = []
                for op in opinioes_erro:
                    res_op = op.get("result") if isinstance(op.get("result"), dict) else {}
                    msg = op.get("error") or res_op.get("error") or "erro desconhecido"
                    erros_desc.append(f"{op.get('provider')}/{op.get('model')}: {msg}")
                erro_ativo = "nenhuma avaliacao valida disponivel para o juiz. erros: " + "; ".join(erros_desc)
                log_event(
                    "consolidation_no_valid_opinions",
                    f"Erro de consolidacao: {erro_ativo}",
                    level="error",
                    quiet=args.quiet,
                    **base_log,
                )
            elif args.evidencias_root:
                pacote_obj = PacoteEvidencia(
                    caminho=caminho_evidencia or Path("."),
                    tipo=caminho_evidencia.suffix.lstrip(".") if caminho_evidencia else "",
                    documentos=pacote_evidencia.get("documentos", []),
                    inventario=pacote_evidencia.get("inventario", []),
                    erro=pacote_evidencia.get("erro", ""),
                )
                erro_atual = erro_tecnico_bloqueante_pacote(pacote_obj, arquivos_upload)
                if erro_atual and erro_atual != "evidencia nao informada para o juiz":
                    erro_ativo = erro_atual

            if erro_ativo:
                result = {
                    "status": "error",
                    "error": erro_ativo,
                }
            elif args.judge_provider == "fake":
                result = executar_juiz_fake(chave, opinioes_validas, itens)
            else:
                env_key = {"gemini": "GEMINI_API_KEY", "openrouter": "OPENROUTER_API_KEY", "opencodego": "OPENCODEGO_API_KEY", "openai": "OPENAI_API_KEY"}.get(args.judge_provider, "")
                api_key = os.environ.get(env_key, "") if env_key else ""
                if args.judge_provider in REMOTE_PROVIDERS and (api_key or args.judge_provider == "openai"):
                    wait_seconds = rate_limiter.wait_seconds()
                    if wait_seconds > 0:
                        log_event(
                            "consolidation_rate_limit_wait",
                            "Aguardando limite de requests por minuto antes da chamada ao juiz.",
                            quiet=args.quiet,
                            wait_seconds=round(wait_seconds, 3),
                            rpm=args.rpm,
                            **base_log,
                        )
                    rate_limiter.wait_and_mark(wait_seconds)

                def on_judge_event(event: str, fields: dict[str, Any]) -> None:
                    log_event(
                        event,
                        "Evento do juiz durante a chamada.",
                        quiet=args.quiet,
                        level="warning",
                        provider=args.judge_provider,
                        model=args.judge_model,
                        **base_log,
                        **fields,
                    )

                # Bloquear payload que excede limite de tokens do juiz
                from .pipeline import _limite_tokens_provider

                tokens_info = estimar_tokens_payload(
                    prompt=PROMPT_JUIZ_PADRAO,
                    auditado=chave.auditado,
                    questao_base=chave.questao,
                    coluna_evidencia=chave.coluna_evidencia,
                    itens_afirmados=itens,
                    pacote=payload_pacote,
                    provider=args.judge_provider,
                )
                limite_tokens = _limite_tokens_provider(args.judge_provider, args.judge_model)
                # Gemini: pular bloqueio da estimativa — a contagem exata e feita
                # via client.models.count_tokens dentro do executar_julgamento_gemini_genai
                if limite_tokens and args.judge_provider != "gemini" and tokens_info["tokens_total"] > limite_tokens:
                    result = {
                        "status": "error",
                        "error": (
                            f"payload excede limite de tokens do juiz: "
                            f"{tokens_info['tokens_total']:,} > {limite_tokens:,}"
                        ),
                    }
                    log_event(
                        "payload_tokens_exceeded",
                        "Payload bloqueado por exceder limite de tokens do juiz.",
                        quiet=args.quiet,
                        level="warning",
                        tokens_total=tokens_info["tokens_total"],
                        limite=limite_tokens,
                        provider=args.judge_provider,
                        model=args.judge_model,
                        **base_log,
                    )
                else:
                    result = executar_provider(
                        provider=args.judge_provider,
                        model=args.judge_model,
                        api_key=api_key,
                        prompt=PROMPT_JUIZ_PADRAO,
                        auditado=chave.auditado,
                        questao_base=chave.questao,
                        coluna_evidencia=chave.coluna_evidencia,
                        itens_afirmados=itens,
                        pacote=payload_pacote,
                        reasoning_effort=args.reasoning_effort,
                        on_event=on_judge_event,
                    )
            # Rotação: todas as chaves exauridas - registrar erro e passar para o proximo grupo
            if isinstance(result, dict) and result.get("all_keys_exhausted"):
                wait_secs = float(result.get("retry_after_seconds", 60))
                log_event(
                    "all_keys_exhausted",
                    f"Todas as chaves {args.judge_provider} exauridas. Registrando erro e passando para o proximo grupo.",
                    quiet=args.quiet,
                    level="warning",
                    provider=args.judge_provider,
                    model=args.judge_model,
                    retry_after_seconds=round(wait_secs, 1),
                    **base_log,
                )
                result = {
                    "status": "error",
                    "error": f"todas as chaves {args.judge_provider} exauridas (retry_after {wait_secs:.0f}s)",
                }


        status = result.get("status", "error") if isinstance(result, dict) else "error"
        finished_at = dt.datetime.now(dt.timezone.utc)
        registro = {
            "identity": identity,
            "status": status,
            "auditado": chave.auditado,
            "questao": chave.questao,
            "coluna_evidencia": chave.coluna_evidencia,
            "evidencia": chave.evidencia,
            "judge_provider": args.judge_provider,
            "judge_model": args.judge_model,
            "opinion_count": len(opinioes_validas),
            "opinion_sources": [
                {
                    "identity": opiniao.get("identity", ""),
                    "provider": opiniao.get("provider", ""),
                    "model": opiniao.get("model", ""),
                    "source": opiniao.get("_source", ""),
                }
                for opiniao in opinioes_validas
            ],
            "opiniao_auditoria": opiniao_auditoria,
            "evidence_path": str(caminho_evidencia) if caminho_evidencia else "",
            "evidence_hash": evidence_hash,
            "gera_achado": any(op.get("gera_achado") for op in grupo.opinioes),
            "result": result,
            "error": result.get("error", "") if isinstance(result, dict) else "resultado invalido",
            "started_at": consolidation_started_at.isoformat(),
            "finished_at": finished_at.isoformat(),
            "duration_seconds": round((finished_at - consolidation_started_at).total_seconds(), 3),
            "reasoning_effort": args.reasoning_effort,
        }
        if args.store_prompts:
            from .providers_ai_service import _conteudo_provider_textual
            registro["prompt_payload"] = _conteudo_provider_textual(
                prompt=PROMPT_JUIZ_PADRAO,
                auditado=chave.auditado,
                questao_base=chave.questao,
                coluna_evidencia=chave.coluna_evidencia,
                itens_afirmados=itens,
                pacote={k: v for k, v in payload_pacote.items() if k != "arquivos_upload"},
            )
        gravar_registro_analise(checkpoint, registro)
        registros_checkpoint[identity] = registro
        total_processados += 1
        if status == "completed":
            total_concluidos += 1
        else:
            total_erros += 1
        log_event(
            "consolidation_recorded",
            "Parecer consolidado gravado.",
            quiet=args.quiet,
            level="error" if status == "error" else "info",
            status=status,
            error=registro["error"],
            **base_log,
        )

    relatorio = out_dir / "pareceres_consolidados.xlsx"
    linhas = gerar_relatorio_pareceres(checkpoint, relatorio)
    checkpoint_limpo = out_dir / "consolidated_clean.jsonl"
    registros_limpos = _gerar_checkpoint_limpo(checkpoint, checkpoint_limpo)
    log_event(
        "clean_checkpoint_generated",
        "Checkpoint limpo (somente completed) gerado.",
        quiet=args.quiet,
        checkpoint_limpo=str(checkpoint_limpo),
        registros=registros_limpos,
    )
    log_event(
        "consolidation_finished",
        "Consolidacao de pareceres finalizada.",
        quiet=args.quiet,
        grupos=len(grupos),
        processados=total_processados,
        pulados=total_pulados,
        concluidos=total_concluidos,
        erros=total_erros,
        checkpoint=str(checkpoint),
        checkpoint_limpo=str(checkpoint_limpo),
        relatorio=str(relatorio),
        linhas=linhas,
    )
    return 0


def _gerar_checkpoint_limpo(checkpoint: str | Path, destino: str | Path) -> int:
    """Copia para ``destino`` apenas os registros ``completed`` do checkpoint."""
    path = Path(checkpoint)
    if not path.is_file():
        return 0
    destino_path = Path(destino)
    destino_path.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    with path.open(encoding="utf-8") as f_in, destino_path.open("w", encoding="utf-8") as f_out:
        for linha in f_in:
            if not linha.strip():
                continue
            registro = json.loads(linha)
            if registro.get("status") == "completed":
                f_out.write(json.dumps(registro, ensure_ascii=False) + "\n")
                total += 1
    return total


if __name__ == "__main__":
    raise SystemExit(main())
