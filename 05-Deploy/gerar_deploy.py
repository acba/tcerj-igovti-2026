#!/usr/bin/env python3
"""Monta o pacote de anexos para o deploy da Fiscalização 18/2026.

O pacote segue a lista de anexos do relatório consolidado. Cada ZIP individual
contém somente documentos da organização destinatária. Insumos obrigatórios
ausentes recebem um marcador de texto dentro do pacote e são registrados nos
manifestos geral e individual.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import unicodedata
import zipfile
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "05-Deploy" / "gerados"
DEFAULT_RESULTADO = (
    ROOT
    / "02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria"
    / "03-pos-comentarios-gestor/resultado_auditoria.json"
)
DEFAULT_TSID_ROOT = ROOT / "99-Gestao/02-TSIDs"
QUESTIONARIO_PDF_ROOT = ROOT / "02-Execucao/01-Questionario/01-Coleta_LimeSurvey/Respostas_PDF"
QUESTIONARIO_EVIDENCIAS_ROOT = (
    ROOT
    / "02-Execucao/01-Questionario/01-Coleta_LimeSurvey/Evidencias_Coletadas"
    / "evidencias_extraidas"
)
COMENTARIOS_PDF_ROOT = ROOT / "02-Execucao/05-Comentarios_Gestor/01-Coleta_LimeSurvey/PDF_Respostas"
COMENTARIOS_EVIDENCIAS_ROOT = (
    ROOT
    / "02-Execucao/05-Comentarios_Gestor/01-Coleta_LimeSurvey/Evidencias_Coletadas"
    / "evidencias_extraidas"
)
RELATORIOS_INDIVIDUAIS_ROOT = ROOT / "03-Relatorios/03-Relatorios_Individuais_Finais/gerados"
RELATORIO_CONSOLIDADO_ROOT = ROOT / "03-Relatorios/01-Relatorio_Consolidado/gerados"
MAX_ZIP_BYTES = 100_000_000
TARGET_ZIP_BYTES = 90_000_000

ANEXOS_FIXOS = {
    "AN02 – Matriz de planejamento.docx": (
        ROOT / "01-Planejamento/03-Estrategia_e_Plano/04-Matriz_Planejamento/AN02 – Matriz de planejamento.docx"
    ),
    "AN04 – Evidências dos achados.docx": (
        ROOT / "02-Execucao/03-Execucao_Procedimentos/02-Resultados_Auditoria/AN04 – Evidências dos achados.docx"
    ),
    "AN06 – Matriz de achados.docx": ROOT / "02-Execucao/04-Matriz_Achados/AN06 – Matriz de achados.docx",
    "AN07 – Impacto da avaliação das evidências.docx": (
        ROOT / "03-Relatorios/99-Impacto_Avaliacao_Evidencias/AN07 – Impacto da avaliação das evidências.docx"
    ),
    "AN08 – Avaliação dos comentários do gestor.docx": (
        ROOT / "03-Relatorios/99-Avaliacao_Comentarios_Gestor/AN08 – Avaliação dos comentários do gestor.docx"
    ),
    "AN09 – Cenário de utilização de IA no ERJ.docx": (
        ROOT / "03-Relatorios/99-Avaliacao_IA/AN09 – Cenário de utilização de IA no ERJ.docx"
    ),
    "AN10 – Comunicações da fiscalização e registros de ciência dos não respondentes.zip": (
        ROOT / "99-Gestao/02-TSIDs/AN10 – Comunicações da fiscalização e registros de ciência dos não respondentes.zip"
    ),
    "AN11 – Análise longitudinal do iGovTI 2023–2026.docx": (
        ROOT / "03-Relatorios/99-Analise_Longitudinal/AN11 – Análise longitudinal do iGovTI 2023–2026.docx"
    ),
}

AN03_FONTES = [
    ROOT / "01-Planejamento/02-Metodologia_iGovTI/igovti_2026.pdf",
    ROOT / "01-Planejamento/02-Metodologia_iGovTI/igovti_2026.docx",
    ROOT / "01-Planejamento/02-Metodologia_iGovTI/igovti_2026.lss",
    ROOT / "01-Planejamento/02-Metodologia_iGovTI/metodologia-calculo.md",
    ROOT / "01-Planejamento/02-Metodologia_iGovTI/estrutura-igovti-2026.yaml",
    ROOT / "02-Execucao/01-Questionario/04-Resultados_iGovTI/03-pos-comentarios-gestor/20260716-iGovTI-2026.xlsx",
    ROOT
    / "02-Execucao/01-Questionario/04-Resultados_iGovTI/03-pos-comentarios-gestor"
    / "20260716-iGovTI-2026-Ajustado-Comparavel.xlsx",
    ROOT
    / "02-Execucao/01-Questionario/04-Resultados_iGovTI/03-pos-comentarios-gestor"
    / "20260716-estatisticas-relatorios-igovti-2026.json",
]

AN05_FONTES = [
    ROOT / "02-Execucao/01-Questionario/01-Coleta_LimeSurvey/20260621-respostas-questionario-bruto.xlsx",
    ROOT
    / "02-Execucao/01-Questionario/03-Respostas_Processadas"
    / "20260716-respostas-questionario-pos-comentarios-gestor.xlsx",
    ROOT / "02-Execucao/01-Questionario/02-Ajustes_Respostas/ajustes_respostas_questionario_inicial.xlsx",
    ROOT
    / "02-Execucao/01-Questionario/02-Ajustes_Respostas"
    / "ajustes_respostas_questionario_pos_avaliacao_evidencias.xlsx",
    ROOT / "02-Execucao/05-Comentarios_Gestor/01-Coleta_LimeSurvey/20260716-respostas-bruto.xlsx",
    ROOT
    / "02-Execucao/05-Comentarios_Gestor/02-Avaliacao_Comentarios_Gestor"
    / "ajustes_respostas_questionario_pos_comentarios_gestor.xlsx",
]


@dataclass
class Registro:
    anexo: str
    tipo: str
    auditado: str = ""
    caminho: str = ""
    status: str = "ok"
    faltantes: list[str] = field(default_factory=list)
    sha256: str = ""
    tamanho_bytes: int = 0


def chave(texto: object) -> str:
    valor = unicodedata.normalize("NFKD", str(texto or ""))
    valor = "".join(c for c in valor if not unicodedata.combining(c))
    return re.sub(r"[^A-Z0-9]+", "", valor.upper())


def texto_busca(texto: object) -> str:
    valor = unicodedata.normalize("NFKD", str(texto or ""))
    valor = "".join(c for c in valor if not unicodedata.combining(c)).upper()
    return " ".join(re.sub(r"[^A-Z0-9]+", " ", valor).split())


def nome_seguro(nome: str) -> str:
    return re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", nome).strip().rstrip(".")


def caminho_zip_seguro(caminho: str) -> str:
    return "/".join(nome_seguro(parte) for parte in caminho.replace("\\", "/").split("/") if parte)


def arquivos_em(pasta: Path | None) -> list[Path]:
    if pasta is None or not pasta.is_dir():
        return []
    return sorted(p for p in pasta.rglob("*") if p.is_file() and p.name != ".gitkeep")


def indice_por_chave(pasta: Path, extrator) -> dict[str, Path]:
    resultado: dict[str, Path] = {}
    if not pasta.is_dir():
        return resultado
    for item in sorted(pasta.iterdir()):
        identificador = extrator(item)
        if identificador:
            identificador_key = chave(identificador)
            anterior = resultado.get(identificador_key)
            if anterior is not None and anterior != item:
                raise ValueError(f"Identificador duplicado {identificador!r}: {anterior} e {item}")
            resultado[identificador_key] = item
    return resultado


def hash_arquivo(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for bloco in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(bloco)
    return digest.hexdigest()


def adicionar_arquivo(zf: zipfile.ZipFile, origem: Path, destino: str) -> None:
    zf.write(origem, caminho_zip_seguro(destino))


def adicionar_arvore(zf: zipfile.ZipFile, origem: Path, destino: str) -> int:
    quantidade = 0
    for arquivo in arquivos_em(origem):
        relativo = arquivo.relative_to(origem).as_posix()
        adicionar_arquivo(zf, arquivo, f"{destino}/{relativo}")
        quantidade += 1
    return quantidade


def adicionar_marcador(zf: zipfile.ZipFile, destino: str, mensagem: str) -> None:
    zf.writestr(destino, mensagem.rstrip() + "\n")


def localizar_tsids(tsids_root: Path, sigla: str) -> dict[str, list[Path]]:
    encontrados = {f"TSID0{numero}": [] for numero in range(1, 4)}
    if not tsids_root.is_dir():
        return encontrados
    sigla_key = chave(sigla)
    sigla_busca = texto_busca(sigla)
    for path in sorted(tsids_root.rglob("*")):
        if not path.is_file() or path.name == ".gitkeep" or path.name.startswith("AN10 "):
            continue
        partes = [chave(parte) for parte in path.relative_to(tsids_root).parts]
        stem_busca = texto_busca(path.stem)
        corresponde_nome_plano = re.search(rf"(?:^| ){re.escape(sigla_busca)}(?: |$)", stem_busca) is not None
        if sigla_key not in partes and not corresponde_nome_plano:
            continue
        texto = " ".join(path.relative_to(tsids_root).parts)
        match = re.search(r"TSID\s*0?([123])", texto, re.IGNORECASE)
        if match:
            encontrados[f"TSID0{match.group(1)}"].append(path)
    return encontrados


def carregar_auditados(resultado: Path) -> list[dict]:
    dados = json.loads(resultado.read_text(encoding="utf-8"))
    if not isinstance(dados, dict):
        raise ValueError("O resultado de auditoria deve ser um objeto indexado por sigla.")
    auditados = []
    for sigla, item in dados.items():
        if isinstance(item, dict) and item.get("foi_auditado") and item.get("respondeu_questionario"):
            auditados.append({"sigla": str(item.get("sigla") or sigla).strip(), "nome": str(item.get("nome") or "").strip()})
    if len(auditados) != 113:
        raise ValueError(f"Esperados 113 auditados avaliados; encontrados {len(auditados)} em {resultado}.")
    return auditados


def criar_zip_fontes(destino: Path, fontes: Iterable[Path], prefixo: str) -> list[str]:
    faltantes: list[str] = []
    with zipfile.ZipFile(destino, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=1, allowZip64=True) as zf:
        for fonte in fontes:
            if fonte.is_file():
                adicionar_arquivo(zf, fonte, f"{prefixo}/{fonte.name}")
            else:
                faltantes.append(str(fonte.relative_to(ROOT)))
        if faltantes:
            adicionar_marcador(
                zf,
                "ARQUIVOS_FALTANTES.txt",
                "Não foram localizados os seguintes insumos:\n" + "\n".join(f"- {p}" for p in faltantes),
            )
    return faltantes


def dividir_zip(path: Path, max_bytes: int = MAX_ZIP_BYTES) -> list[Path]:
    """Transforma um ZIP grande em vários ZIPs válidos de até ``max_bytes``."""
    if path.stat().st_size <= max_bytes:
        return [path]

    with zipfile.ZipFile(path) as origem:
        infos = [info for info in origem.infolist() if not info.is_dir()]
        grupos: list[list[zipfile.ZipInfo]] = []
        atual: list[zipfile.ZipInfo] = []
        tamanho_estimado = 0
        for info in infos:
            custo = info.compress_size + len(info.filename.encode("utf-8")) + 256
            if atual and tamanho_estimado + custo > TARGET_ZIP_BYTES:
                grupos.append(atual)
                atual = []
                tamanho_estimado = 0
            atual.append(info)
            tamanho_estimado += custo
        if atual:
            grupos.append(atual)

        partes: list[Path] = []
        total = len(grupos)
        for numero, grupo in enumerate(grupos, 1):
            parte = path.with_name(f"{path.stem}-parte{numero}{path.suffix}")
            with zipfile.ZipFile(parte, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=1, allowZip64=True) as destino:
                destino.writestr(
                    "LEIA-ME_PARTES.txt",
                    f"Este é o arquivo {numero} de {total} que compõem {path.name}.\n"
                    "Todos os arquivos -parteN.zip devem ser considerados em conjunto.\n",
                )
                for info in grupo:
                    dados = origem.read(info)
                    destino.writestr(info, dados, compress_type=zipfile.ZIP_DEFLATED, compresslevel=1)
            if parte.stat().st_size > max_bytes:
                raise ValueError(
                    f"Não foi possível respeitar o limite de {max_bytes} bytes: "
                    f"{parte.name} possui {parte.stat().st_size} bytes."
                )
            partes.append(parte)

    path.unlink()
    return partes


def aplicar_limite_zips(pasta: Path, registros: list[Registro]) -> list[Registro]:
    resultado: list[Registro] = []
    for registro in registros:
        path = pasta / registro.caminho
        if path.suffix.lower() != ".zip" or not path.is_file():
            resultado.append(registro)
            continue
        partes = dividir_zip(path)
        for indice, parte in enumerate(partes):
            resultado.append(
                replace(
                    registro,
                    caminho=parte.name,
                    faltantes=list(registro.faltantes) if indice == 0 else [],
                )
            )
    return resultado


def criar_an01(destino: Path) -> list[str]:
    fonte = ROOT / "99-Gestao/01-Oficios_Apresentacao"
    arquivos = arquivos_em(fonte)
    faltantes: list[str] = []
    with zipfile.ZipFile(destino, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=1) as zf:
        if arquivos:
            for arquivo in arquivos:
                adicionar_arquivo(zf, arquivo, arquivo.relative_to(fonte).as_posix())
        else:
            faltantes.append("99-Gestao/01-Oficios_Apresentacao")
            adicionar_marcador(
                zf,
                "OFICIOS_DE_APRESENTACAO_FALTANTES.txt",
                "Nenhum ofício de apresentação foi localizado no diretório esperado.",
            )
    return faltantes


def criar_zip_auditado(
    destino: Path,
    sigla: str,
    tsids_root: Path,
    questionarios: dict[str, Path],
    evidencias_questionario: dict[str, Path],
    comentarios: dict[str, Path],
    evidencias_comentarios: dict[str, Path],
    relatorios: dict[str, Path],
) -> list[str]:
    faltantes: list[str] = []
    sigla_key = chave(sigla)
    tsids = localizar_tsids(tsids_root, sigla)
    with zipfile.ZipFile(destino, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=1, allowZip64=True) as zf:
        for tsid, arquivos in tsids.items():
            if arquivos:
                for indice, arquivo in enumerate(arquivos, 1):
                    sufixo = "" if len(arquivos) == 1 else f"_{indice:02d}"
                    adicionar_arquivo(zf, arquivo, f"{tsid}/{arquivo.stem}{sufixo}{arquivo.suffix}")
            else:
                faltantes.append(tsid)
                adicionar_marcador(
                    zf,
                    f"{tsid}/ARQUIVO_FALTANTE.txt",
                    f"Não foi localizado arquivo do {tsid} enviado a {sigla}.",
                )

        resposta = questionarios.get(sigla_key)
        if resposta:
            adicionar_arquivo(zf, resposta, f"Questionário iGovTI/{resposta.name}")
        else:
            faltantes.append("Resposta ao questionário iGovTI")
            adicionar_marcador(
                zf,
                "Questionário iGovTI/RESPOSTA_FALTANTE.txt",
                f"Não foi localizado o PDF de respostas ao questionário iGovTI de {sigla}.",
            )

        evidencia_q = evidencias_questionario.get(sigla_key)
        if adicionar_arvore(zf, evidencia_q, "Questionário iGovTI/Evidências") == 0:
            adicionar_marcador(
                zf,
                "Questionário iGovTI/Evidências/NENHUMA_EVIDENCIA_ENVIADA.txt",
                "Não há evidência anexada ao questionário para esta organização.",
            )

        comentario = comentarios.get(sigla_key)
        evidencia_c = evidencias_comentarios.get(sigla_key)
        quantidade_evidencias_c = len(arquivos_em(evidencia_c))
        if comentario:
            adicionar_arquivo(zf, comentario, f"Comentários do Gestor/{comentario.name}")
            if quantidade_evidencias_c:
                adicionar_arvore(zf, evidencia_c, "Comentários do Gestor/Evidências")
            else:
                adicionar_marcador(
                    zf,
                    "Comentários do Gestor/Evidências/NENHUMA_EVIDENCIA_ENVIADA.txt",
                    "A manifestação não possui evidência anexada.",
                )
        elif quantidade_evidencias_c:
            faltantes.append("PDF de respostas aos comentários do gestor")
            adicionar_marcador(
                zf,
                "Comentários do Gestor/RESPOSTA_PDF_FALTANTE.txt",
                "Foram localizadas evidências de comentários, mas não o PDF da manifestação.",
            )
            adicionar_arvore(zf, evidencia_c, "Comentários do Gestor/Evidências")
        else:
            adicionar_marcador(
                zf,
                "Comentários do Gestor/NAO_HOUVE_MANIFESTACAO.txt",
                "Não foi localizada manifestação do gestor nem evidência complementar para esta organização.",
            )

        relatorio = relatorios.get(sigla_key)
        if relatorio:
            adicionar_arquivo(zf, relatorio, relatorio.name)
        else:
            faltantes.append("Relatório individual final em PDF")
            adicionar_marcador(
                zf,
                "RELATORIO_INDIVIDUAL_FINAL_FALTANTE.txt",
                f"Não foi localizado o relatório individual final em PDF de {sigla}.",
            )

        resumo = [
            f"Organização: {sigla}",
            "Pacote de acesso exclusivo da organização destinatária.",
            "",
            "Itens obrigatórios não localizados:" if faltantes else "Todos os itens obrigatórios foram localizados.",
        ]
        resumo.extend(f"- {item}" for item in faltantes)
        adicionar_marcador(zf, "MANIFESTO_DO_PACOTE.txt", "\n".join(resumo))
    return faltantes


def copiar_ou_marcar(destino: Path, origem: Path, registros: list[Registro]) -> None:
    if origem.is_file():
        shutil.copy2(origem, destino)
        registros.append(Registro(destino.name[:4], "anexo_geral", caminho=destino.name))
        return
    marcador = destino.with_name(f"{destino.stem} [FALTANTE].txt")
    marcador.write_text(f"Arquivo não localizado: {origem.relative_to(ROOT)}\n", encoding="utf-8")
    registros.append(
        Registro(destino.name[:4], "anexo_geral", caminho=marcador.name, status="faltante", faltantes=[str(origem.relative_to(ROOT))])
    )


def finalizar_registros(pasta: Path, registros: list[Registro]) -> None:
    for registro in registros:
        path = pasta / registro.caminho
        if path.is_file():
            registro.tamanho_bytes = path.stat().st_size
            registro.sha256 = hash_arquivo(path)


def escrever_manifestos(pasta: Path, registros: list[Registro]) -> None:
    gerado_em = datetime.now(timezone.utc).isoformat()
    conteudo = {
        "fiscalizacao": "18/2026",
        "nome": "iGovTI 2026",
        "gerado_em_utc": gerado_em,
        "quantidade_anexos": len(registros),
        "quantidade_faltantes": sum(len(r.faltantes) for r in registros),
        "registros": [r.__dict__ for r in registros],
    }
    (pasta / "manifesto-deploy.json").write_text(
        json.dumps(conteudo, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    with (pasta / "manifesto-deploy.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream, delimiter=";")
        writer.writerow(["anexo", "tipo", "auditado", "arquivo", "status", "faltantes", "tamanho_bytes", "sha256"])
        for registro in registros:
            writer.writerow(
                [
                    registro.anexo,
                    registro.tipo,
                    registro.auditado,
                    registro.caminho,
                    registro.status,
                    " | ".join(registro.faltantes),
                    registro.tamanho_bytes,
                    registro.sha256,
                ]
            )
    faltantes = [r for r in registros if r.faltantes]
    linhas = ["# Arquivos faltantes no deploy", ""]
    if not faltantes:
        linhas.append("Nenhum arquivo obrigatório está faltando.")
    else:
        linhas.append(f"Foram identificadas {sum(len(r.faltantes) for r in faltantes)} ausências em {len(faltantes)} anexos.")
        linhas.append("")
        for registro in faltantes:
            alvo = f" — {registro.auditado}" if registro.auditado else ""
            linhas.append(f"## {registro.anexo}{alvo}")
            linhas.extend(f"- {item}" for item in registro.faltantes)
            linhas.append("")
    (pasta / "FALTANTES.md").write_text("\n".join(linhas).rstrip() + "\n", encoding="utf-8")


def gerar(args: argparse.Namespace) -> Path:
    output = args.output_dir.resolve()
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(f"O diretório de saída não está vazio: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    auditados = carregar_auditados(args.resultado_auditoria)

    questionarios = indice_por_chave(QUESTIONARIO_PDF_ROOT, lambda p: re.sub(r"^Respostas Questionário\s*-\s*", "", p.stem, flags=re.I) if p.is_file() and p.suffix.lower() == ".pdf" else "")
    evidencias_questionario = indice_por_chave(QUESTIONARIO_EVIDENCIAS_ROOT, lambda p: p.name if p.is_dir() else "")
    comentarios = indice_por_chave(COMENTARIOS_PDF_ROOT, lambda p: p.name.split("_id", 1)[0] if p.is_file() and p.suffix.lower() == ".pdf" else "")
    evidencias_comentarios = indice_por_chave(COMENTARIOS_EVIDENCIAS_ROOT, lambda p: p.name if p.is_dir() else "")
    relatorios = indice_por_chave(RELATORIOS_INDIVIDUAIS_ROOT, lambda p: re.sub(r"^Relatório Individual\s*-\s*", "", p.stem, flags=re.I) if p.is_file() and p.suffix.lower() == ".pdf" else "")

    temp = Path(tempfile.mkdtemp(prefix="deploy-igovti-", dir=output.parent))
    registros: list[Registro] = []
    try:
        for extensao in ("docx", "pdf"):
            origem = RELATORIO_CONSOLIDADO_ROOT / f"Relatório_altaresolucao_novo.{extensao}"
            destino = temp / f"Relatório consolidado - iGovTI 2026.{extensao}"
            copiar_ou_marcar(destino, origem, registros)
            registros[-1].anexo = "RELATORIO"
            registros[-1].tipo = "relatorio_consolidado"

        an01 = temp / "AN01 – Ofícios de apresentação.zip"
        faltantes = criar_an01(an01)
        registros.append(Registro("AN01", "anexo_geral", caminho=an01.name, status="incompleto" if faltantes else "ok", faltantes=faltantes))

        for nome, origem in ANEXOS_FIXOS.items():
            copiar_ou_marcar(temp / nome, origem, registros)

        an03 = temp / "AN03 – Questionário iGovTI 2026, metodologia e resultados.zip"
        faltantes = criar_zip_fontes(an03, AN03_FONTES, "AN03")
        registros.append(Registro("AN03", "anexo_geral", caminho=an03.name, status="incompleto" if faltantes else "ok", faltantes=faltantes))

        an05 = temp / "AN05 – Respostas aos questionários e ajustes.zip"
        faltantes = criar_zip_fontes(an05, AN05_FONTES, "AN05")
        registros.append(Registro("AN05", "anexo_geral", caminho=an05.name, status="incompleto" if faltantes else "ok", faltantes=faltantes))

        for numero, auditado in enumerate(auditados, 12):
            sigla = auditado["sigla"]
            anexo = f"AN{numero:02d}"
            nome = f"{anexo} – {nome_seguro(sigla)}.zip"
            faltantes = criar_zip_auditado(
                temp / nome,
                sigla,
                args.tsids_root,
                questionarios,
                evidencias_questionario,
                comentarios,
                evidencias_comentarios,
                relatorios,
            )
            registros.append(
                Registro(
                    anexo,
                    "anexo_individual_reservado",
                    auditado=sigla,
                    caminho=nome,
                    status="incompleto" if faltantes else "ok",
                    faltantes=faltantes,
                )
            )
            print(f"[{anexo}] {sigla}: {'incompleto' if faltantes else 'ok'}", flush=True)

        registros = aplicar_limite_zips(temp, registros)

        def ordem(registro: Registro) -> tuple[int, str]:
            match = re.fullmatch(r"AN(\d+)", registro.anexo)
            return (int(match.group(1)) if match else 0, registro.caminho)

        registros.sort(key=ordem)
        finalizar_registros(temp, registros)
        escrever_manifestos(temp, registros)
        if output.exists():
            output.rmdir()
        os.replace(temp, output)
        return output
    except Exception:
        shutil.rmtree(temp, ignore_errors=True)
        raise


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT, help="Diretório vazio ou inexistente para os arquivos finais.")
    parser.add_argument("--resultado-auditoria", type=Path, default=DEFAULT_RESULTADO, help="Resultado final que define os 113 auditados e a ordem de AN12 a AN124.")
    parser.add_argument("--tsids-root", type=Path, default=DEFAULT_TSID_ROOT, help="Raiz dos TSID01, TSID02 e TSID03 por organização.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(argv)
        destino = gerar(args)
    except Exception as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1
    print(f"Deploy gerado em: {destino}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
