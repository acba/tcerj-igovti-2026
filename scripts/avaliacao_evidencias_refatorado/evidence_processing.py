"""Processamento de evidencias: normalizacao, recuperacao de PDF, conversao
de PDF/DOCX/XLSX/ODS, tratamento de ZIPs e preparacao de arquivos para envio
ao provider.

Planilhas OpenDocument (.ods) sao convertidas para .xlsx via LibreOffice
headless e em seguida processadas por ``_extrair_xlsx_abas_visiveis``, que
filtra abas ocultas via openpyxl. markitdown nao suporta .ods nativamente.

Este modulo e o nucleo compartilhado entre o pipeline de avaliacao e a
consolidacao (juiz). A funcao ``preparar_evidencia_para_provider`` substitui
a logica de preparacao que antes era duplicada entre os dois fluxos.
"""
from __future__ import annotations

import io
import mimetypes
import os
import re
import shutil
import subprocess
import tempfile
import zipfile
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from openpyxl import load_workbook

from .utils import (
    caminho_unico,
    copiar_upload_seguro,
    gravar_upload_texto,
    hash_arquivo,
    nome_upload_seguro,
    slug_ascii,
    suprimir_stderr,
    zip_member_safe,
)


@dataclass(frozen=True)
class PacoteEvidencia:
    caminho: Path
    tipo: str
    documentos: list[dict[str, Any]]
    inventario: list[str]
    erro: str = ""
    duplicados_ignorados: tuple[str, ...] = ()


EXTENSOES_UPLOAD_DIRETO = {".pdf", ".txt", ".md", ".csv", ".png", ".jpg", ".jpeg"}
EXTENSOES_WORD_PARA_PDF = {".doc", ".docx"}
EXTENSOES_ODS = {".ods"}
EXTENSOES_PLANILHAS = {".xlsx"} | EXTENSOES_ODS
EXTENSOES_UPLOAD_PREPARAVEIS = EXTENSOES_UPLOAD_DIRETO | EXTENSOES_WORD_PARA_PDF | EXTENSOES_PLANILHAS
EXTENSOES_COMPACTADOS = {".zip", ".rar"}

MAX_PAGINAS_PDF = 100
MAX_PROFUNDIDADE_RECURSIVIDADE = 5

# ---------------------------------------------------------------------------
# Tratamento de atalhos .url (download seguro de recursos .gov.br)
# ---------------------------------------------------------------------------

URL_DOWNLOAD_MAX_BYTES = 10 * 1024 * 1024  # 10 MB
URL_DOWNLOAD_TIMEOUT = 30  # segundos
URL_SCHEMES_PERMITIDOS = {"http", "https"}
URL_DOMINIOS_PERMITIDOS = {".gov.br"}

URL_MIME_TYPES_PERMITIDOS = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.oasis.opendocument.text",
    "application/vnd.oasis.opendocument.spreadsheet",
    "text/plain",
    "text/html",
    "text/markdown",
    "image/png",
    "image/jpeg",
}


# ---------------------------------------------------------------------------
# Extracao de arquivos compactados (.zip e .rar)
# ---------------------------------------------------------------------------


def _extrair_zip_para_pasta(path: Path, destino: Path) -> tuple[list[Path], str]:
    """Extrai um ZIP para destino, retornando lista de arquivos extraidos."""
    try:
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            for name in names:
                if not zip_member_safe(name):
                    return [], f"zip contem path traversal: {name}"
            archive.extractall(destino)
            return [
                (destino / name).resolve()
                for name in names
                if not name.endswith("/")
            ], ""
    except zipfile.BadZipFile as exc:
        return [], f"zip invalido: {exc}"


def _extrair_rar_com_7z(path: Path, destino: Path) -> tuple[list[Path], str]:
    """Fallback para extracao de RAR via 7z (Linux/Windows)."""
    executavel_7z = shutil.which("7z") or shutil.which("7za") or shutil.which("7zz")
    if not executavel_7z:
        return [], "rar sem ferramenta de extracao disponivel (rarfile/7z)"
    destino.mkdir(parents=True, exist_ok=True)
    try:
        result = subprocess.run(
            [executavel_7z, "x", str(path), f"-o{destino}", "-y"],
            check=False,
            capture_output=True,
            text=True,
            timeout=180,
        )
    except (subprocess.TimeoutExpired, OSError) as exc:
        return [], f"erro ao executar 7z para extrair rar: {exc}"
    saida = (result.stderr or result.stdout or "").casefold()
    if result.returncode != 0 or "unsupported method" in saida:
        if "unsupported method" in saida:
            return [], "rar usa metodo de compressao nao suportado pelo 7z open source; instale unrar non-free ou WinRAR"
        return [], f"7z falhou ao extrair rar: {(result.stderr or result.stdout or result.returncode)}"
    return [
        p.resolve()
        for p in destino.rglob("*")
        if p.is_file()
    ], ""


def _extrair_rar_para_pasta(path: Path, destino: Path) -> tuple[list[Path], str]:
    """Extrai um RAR para destino. Tenta rarfile (UnRAR.exe/WinRAR no Windows
    ou unrar no Linux); em falha, usa 7z como fallback.
    """
    try:
        import rarfile
    except ModuleNotFoundError:
        return _extrair_rar_com_7z(path, destino)

    try:
        ts = rarfile.tool_setup()
        if not ts or not ts.check():
            return _extrair_rar_com_7z(path, destino)
        with rarfile.RarFile(path) as archive:
            for info in archive.infolist():
                if not zip_member_safe(info.filename):
                    return [], f"rar contem path traversal: {info.filename}"
            archive.extractall(destino)
            return [
                p.resolve()
                for p in destino.rglob("*")
                if p.is_file()
            ], ""
    except Exception as exc:
        texto_erro = str(exc).casefold()
        if "unsupported method" in texto_erro or "not implemented" in texto_erro:
            return _extrair_rar_com_7z(path, destino)
        fallback_7z, erro_7z = _extrair_rar_com_7z(path, destino)
        if fallback_7z or not erro_7z:
            return fallback_7z, erro_7z
        return [], f"rar nao pode ser extraido. instale UnRAR/WinRAR ou unrar non-free. erro rarfile: {exc}; erro 7z: {erro_7z}"


# ---------------------------------------------------------------------------
# Utilidades para atalhos .url (download seguro)
# ---------------------------------------------------------------------------


def extrair_url_arquivo_url(caminho: Path) -> str | None:
    """Extrai a URL de um arquivo .url do Windows (formato INI)."""
    try:
        conteudo = caminho.read_text(encoding="utf-8", errors="ignore")
        for linha in conteudo.splitlines():
            linha_limpa = linha.strip()
            if linha_limpa.upper().startswith("URL="):
                return linha_limpa.split("=", 1)[1].strip()
    except Exception:
        pass
    return None


def _url_download_permitida(url: str) -> tuple[bool, str]:
    """Valida se uma URL pode ser baixada de forma segura.

    Permite apenas esquemas http/https, dominios .gov.br e bloqueia
    credenciais embutidas, enderecos locais e IPs privados/reservados.
    """
    from urllib.parse import urlparse
    import ipaddress

    parsed = urlparse(url)
    scheme = parsed.scheme.lower()
    if scheme not in URL_SCHEMES_PERMITIDOS:
        return False, f"esquema de URL nao permitido: {parsed.scheme}"

    if not parsed.hostname:
        return False, "URL sem hostname"

    hostname = parsed.hostname.lower()

    if "@" in parsed.netloc:
        return False, "URL com credenciais embutidas nao permitida"

    if hostname in {"localhost", "127.0.0.1", "::1"}:
        return False, "endereco local nao permitido"

    try:
        ip = ipaddress.ip_address(hostname)
        if ip.is_private or ip.is_reserved or ip.is_loopback:
            return False, "endereco IP privado/reservado nao permitido"
    except ValueError:
        pass  # hostname DNS, prossegue

    if not any(hostname.endswith(dom) for dom in URL_DOMINIOS_PERMITIDOS):
        return False, f"dominio nao permitido: {hostname}"

    return True, ""


def baixar_recurso_url(url: str, destino: Path) -> tuple[Path | None, str]:
    """Baixa um recurso .gov.br de forma segura e retorna o caminho local.

    Aplica limite de tamanho, timeout e validacao de Content-Type.
    """
    import urllib.request
    from urllib.parse import urlparse

    destino.mkdir(parents=True, exist_ok=True)
    parsed = urlparse(url)
    nome_sugerido = Path(parsed.path).name or "recurso"
    extensao = Path(nome_sugerido).suffix.lower()
    if extensao not in EXTENSOES_UPLOAD_DIRETO | EXTENSOES_WORD_PARA_PDF | EXTENSOES_PLANILHAS | {".html", ".htm"}:
        extensao = ".bin"
    nome_seguro = nome_upload_seguro(nome_sugerido, extensao)
    target = caminho_unico(destino, nome_seguro)

    request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})

    try:
        with urllib.request.urlopen(request, timeout=URL_DOWNLOAD_TIMEOUT) as resp:
            length = resp.headers.get("Content-Length")
            if length:
                try:
                    if int(length) > URL_DOWNLOAD_MAX_BYTES:
                        return None, f"recurso excede {URL_DOWNLOAD_MAX_BYTES} bytes"
                except ValueError:
                    pass
    except Exception:
        pass  # HEAD pode nao ser suportado; continua com GET

    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(request, timeout=URL_DOWNLOAD_TIMEOUT) as resp:
            dados = resp.read(URL_DOWNLOAD_MAX_BYTES + 1)
            if len(dados) > URL_DOWNLOAD_MAX_BYTES:
                return None, f"recurso excede {URL_DOWNLOAD_MAX_BYTES} bytes"

            content_type = resp.headers.get("Content-Type", "").split(";")[0].strip().lower()
            if content_type:
                if content_type not in URL_MIME_TYPES_PERMITIDOS:
                    return None, f"tipo de conteudo nao permitido: {content_type}"
            else:
                tipo_inferido, _ = mimetypes.guess_type(nome_sugerido)
                if not tipo_inferido or tipo_inferido not in URL_MIME_TYPES_PERMITIDOS:
                    return None, "tipo de conteudo nao identificado ou nao permitido"

            target.write_bytes(dados)
            return target, ""
    except Exception as exc:
        return None, f"erro ao baixar recurso: {exc}"


def _extrair_compactado_para_hierarquia(
    path: Path,
    destino: Path,
    *,
    profundidade: int = 0,
    max_profundidade: int = MAX_PROFUNDIDADE_RECURSIVIDADE,
) -> tuple[list[Path], list[str]]:
    """Extrai .zip/.rar recursivamente, mantendo hierarquia em destino."""
    if profundidade > max_profundidade:
        return [], [f"profundidade maxima atingida: {path.name}"]

    suffix = path.suffix.lower()
    pasta_nivel = destino / f"_nivel_{profundidade}_{slug_ascii(path.stem, fallback='arq')}"
    pasta_nivel.mkdir(parents=True, exist_ok=True)

    if suffix == ".zip":
        arquivos, erro = _extrair_zip_para_pasta(path, pasta_nivel)
    elif suffix == ".rar":
        arquivos, erro = _extrair_rar_para_pasta(path, pasta_nivel)
    else:
        return [], [f"tipo nao compactado: {path.name}"]

    if erro:
        return [], [erro]

    extraidos: list[Path] = []
    erros: list[str] = []
    for arquivo in arquivos:
        if not arquivo.is_file():
            continue
        if arquivo.suffix.lower() in EXTENSOES_COMPACTADOS:
            sub_extraidos, sub_erros = _extrair_compactado_para_hierarquia(
                arquivo,
                destino,
                profundidade=profundidade + 1,
                max_profundidade=max_profundidade,
            )
            extraidos.extend(sub_extraidos)
            erros.extend(sub_erros)
        else:
            extraidos.append(arquivo)

    return extraidos, erros


def _achatar_e_deduplicar(
    arquivos: list[Path],
    pasta_final: Path,
) -> tuple[list[Path], list[str], list[str]]:
    """Copia arquivos para pasta_final, achatando, deduplicando por hash e
    resolvendo colisoes de nome com hash diferente.
    """
    pasta_final.mkdir(parents=True, exist_ok=True)
    hashes_vistos: dict[str, Path] = {}
    duplicados_ignorados: list[str] = []
    resultado: list[Path] = []

    for arquivo in arquivos:
        h = hash_arquivo(arquivo)
        if h in hashes_vistos:
            duplicados_ignorados.append(arquivo.name)
            continue
        hashes_vistos[h] = arquivo

        destino = pasta_final / arquivo.name
        if destino.exists():
            destino = caminho_unico(pasta_final, arquivo.name)
        shutil.copy2(arquivo, destino)
        resultado.append(destino)

    return resultado, duplicados_ignorados, []


def extrair_arquivo_compactado(
    caminho: str | Path,
    pasta_final: str | Path,
    *,
    max_profundidade: int = MAX_PROFUNDIDADE_RECURSIVIDADE,
) -> tuple[list[Path], list[str], list[str]]:
    """Extrai .zip ou .rar para pasta_final, achatando e deduplicando.

    Retorna (arquivos_achatados, duplicados_ignorados, erros).
    """
    path = Path(caminho)
    pasta_final_path = Path(pasta_final)
    pasta_final_path.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        arquivos_brutos, erros = _extrair_compactado_para_hierarquia(
            path,
            tmp_path,
            profundidade=0,
            max_profundidade=max_profundidade,
        )
        arquivos_achatados, duplicados_ignorados, _ = _achatar_e_deduplicar(
            arquivos_brutos,
            pasta_final_path,
        )
        return arquivos_achatados, duplicados_ignorados, erros


# ---------------------------------------------------------------------------
# Normalizacao principal
# ---------------------------------------------------------------------------


def processar_arquivo_individual(
    caminho: Path,
    destino: Path,
    *,
    nome_exibicao: str | None = None,
    pdf2md: bool = False,
    docx2html: bool = False,
    dpi: int = 150,
) -> tuple[list[dict[str, Any]], list[str], str]:
    """Processa um arquivo avulso pelo mesmo fluxo usado para arquivos
    extraidos de .zip/.rar. Retorna (documentos, arquivos_upload, erro).
    """
    suffix = caminho.suffix.lower()
    nome = nome_exibicao or caminho.name
    documentos: list[dict[str, Any]] = []
    arquivos_upload: list[str] = []
    erro = ""

    if suffix in {".txt", ".md", ".csv"}:
        try:
            texto = caminho.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            texto = caminho.read_text(encoding="latin-1")
        documentos.append({"nome": nome, "texto": texto})
        arquivos_upload.append(str(caminho))

    elif suffix == ".pdf":
        caminho_pdf, info_rec, erro_rec = _preparar_pdf_com_recuperacao(caminho, destino)
        pdf_documento_base: dict[str, Any] = {"nome": nome}
        if info_rec.get("pdf_recuperado"):
            pdf_documento_base["pdf_recuperado"] = True
            pdf_documento_base["camada_recuperacao"] = info_rec["camada_recuperacao"]
        if info_rec.get("pdf_cortado"):
            pdf_documento_base["pdf_cortado"] = True
            pdf_documento_base["paginas_originais"] = info_rec["paginas_originais"]
            pdf_documento_base["paginas_cortadas"] = info_rec["paginas_cortadas"]
            pdf_documento_base["max_paginas"] = info_rec["max_paginas"]
        if erro_rec:
            # PDF nao integro e nao recuperavel: remove da avaliacao sem gerar
            # erro bloqueante. Apenas arquivos PDF integros seguem para o provider.
            return documentos, arquivos_upload, ""

        if pdf2md:
            pacote, upload, erro_pdf = extrair_pdf_markdown_imagens(
                caminho_pdf,
                destino,
                nome,
                dpi=dpi,
            )
            if erro_pdf:
                erro = erro_pdf
                documentos.append({**pdf_documento_base, "erro": erro_pdf})
            elif pacote is not None:
                # Propaga metadados de recuperacao para o documento markdown principal
                if pacote.documentos:
                    pacote.documentos[0] = {**pacote.documentos[0], **pdf_documento_base}
                documentos.extend(pacote.documentos)
                arquivos_upload.extend(upload)
        else:
            docs, erro_pdf = _extrair_texto_pdf(caminho_pdf)
            if docs:
                for doc in docs:
                    documentos.append({**pdf_documento_base, **doc})
            else:
                erro_msg = erro_pdf or "pdf sem texto extraivel"
                erro = erro_msg
                documentos.append({**pdf_documento_base, "erro": erro_msg})
            arquivos_upload.append(str(caminho_pdf))

    elif suffix in EXTENSOES_PLANILHAS:
        texto, erro_md = _extrair_texto_com_markitdown(caminho)
        if erro_md:
            erro = erro_md
        else:
            documentos.append({"nome": nome, "texto": texto})
        preparado = preparar_documento_para_upload(caminho, destino, nome)
        if preparado:
            arquivos_upload.append(str(preparado))

    elif suffix in EXTENSOES_WORD_PARA_PDF:
        if docx2html and suffix == ".docx":
            pacote, upload, erro_docx = extrair_docx_html_imagens(
                caminho,
                destino,
                nome,
            )
            if erro_docx:
                erro = erro_docx
            elif pacote is not None:
                documentos.extend(pacote.documentos)
                arquivos_upload.extend(upload)
        else:
            preparado, erro_conv = converter_word_para_pdf(caminho, destino, nome)
            if erro_conv:
                erro = erro_conv
            elif preparado:
                arquivos_upload.append(str(preparado))
            documentos.append(
                {
                    "nome": nome,
                    "tipo_convertido": "pdf",
                    "observacao": "Documento Word preservado para avaliacao visual por conversao para PDF no upload.",
                }
            )

    elif suffix in {".png", ".jpg", ".jpeg"}:
        arquivos_upload.append(str(caminho))

    elif suffix == ".url":
        # Atalho Windows: tenta baixar recurso .gov.br seguro. Em qualquer
        # falha (URL invalida, nao .gov.br, download falho, tipo nao permitido)
        # o arquivo e descartado silenciosamente, sem enviar texto ou URL.
        url = extrair_url_arquivo_url(caminho)
        if url:
            permitido, _ = _url_download_permitida(url)
            if permitido:
                pasta_download = destino / "_url_downloads"
                baixado, _ = baixar_recurso_url(url, pasta_download)
                if baixado:
                    docs, upload, erro_proc = processar_arquivo_individual(
                        baixado,
                        destino,
                        nome_exibicao=f"{nome} -> {baixado.name}",
                        pdf2md=pdf2md,
                        docx2html=docx2html,
                        dpi=dpi,
                    )
                    documentos.extend(docs)
                    arquivos_upload.extend(upload)
                    if erro_proc:
                        erro = erro_proc

    elif suffix in {".html", ".htm"}:
        # HTML e autocontido: envia o arquivo bruto ao provider.
        arquivos_upload.append(str(caminho))

    else:
        documentos.append({"nome": nome, "nao_suportado": True})

    return documentos, arquivos_upload, erro


def normalizar_evidencia(
    caminho: str | Path,
    *,
    pdf2md: bool = False,
    docx2html: bool = False,
    dpi: int = 150,
) -> PacoteEvidencia:
    path = Path(caminho)
    suffix = path.suffix.lower()

    if suffix in EXTENSOES_COMPACTADOS:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            arquivos, duplicados_ignorados, erros = extrair_arquivo_compactado(
                path,
                tmp_path,
            )
            if erros and not arquivos:
                return PacoteEvidencia(
                    caminho=path,
                    tipo=suffix.lstrip("."),
                    documentos=[],
                    inventario=[],
                    erro="; ".join(erros),
                )

            documentos: list[dict[str, Any]] = []
            inventario: list[str] = []
            for arquivo in arquivos:
                docs, _, erro_arq = processar_arquivo_individual(
                    arquivo,
                    tmp_path,
                    nome_exibicao=arquivo.name,
                    pdf2md=pdf2md,
                    docx2html=docx2html,
                    dpi=dpi,
                )
                if erro_arq:
                    documentos.append({"nome": arquivo.name, "erro": erro_arq})
                else:
                    documentos.extend(docs)
                inventario.append(arquivo.name)

            return PacoteEvidencia(
                caminho=path,
                tipo=suffix.lstrip("."),
                documentos=documentos,
                inventario=inventario,
                erro="; ".join(erros) if erros else "",
                duplicados_ignorados=tuple(duplicados_ignorados),
            )

    if suffix in {".txt", ".md", ".csv"}:
        try:
            texto = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            texto = path.read_text(encoding="latin-1")
        return PacoteEvidencia(
            caminho=path,
            tipo=suffix.lstrip("."),
            documentos=[{"nome": path.name, "texto": texto}],
            inventario=[path.name],
        )

    if suffix == ".pdf":
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            caminho_pdf, info_rec, erro_rec = _preparar_pdf_com_recuperacao(path, tmp_path)
            documentos, erro = _extrair_texto_pdf(caminho_pdf)
            if info_rec:
                def _enriquecer_doc(doc: Any) -> Any:
                    if not isinstance(doc, dict):
                        return doc
                    enriquecido = {
                        "nome": doc.get("nome", path.name),
                        "pagina": doc.get("pagina"),
                        "texto": doc.get("texto", ""),
                    }
                    if info_rec.get("pdf_recuperado"):
                        enriquecido["pdf_recuperado"] = True
                        enriquecido["camada_recuperacao"] = info_rec["camada_recuperacao"]
                    if info_rec.get("pdf_cortado"):
                        enriquecido["pdf_cortado"] = True
                        enriquecido["paginas_originais"] = info_rec["paginas_originais"]
                        enriquecido["paginas_cortadas"] = info_rec["paginas_cortadas"]
                        enriquecido["max_paginas"] = info_rec["max_paginas"]
                    return enriquecido

                documentos = [_enriquecer_doc(doc) for doc in documentos]
            if erro_rec and not documentos:
                erro = erro_rec
            return PacoteEvidencia(
                caminho=path,
                tipo="pdf",
                documentos=documentos,
                inventario=[path.name],
                erro=erro,
            )

    if suffix in EXTENSOES_PLANILHAS:
        texto, erro = _extrair_texto_com_markitdown(path)
        if erro:
            return PacoteEvidencia(
                caminho=path,
                tipo=suffix.lstrip("."),
                documentos=[],
                inventario=[path.name],
                erro=erro,
            )
        return PacoteEvidencia(
            caminho=path,
            tipo=suffix.lstrip("."),
            documentos=[{"nome": path.name, "texto": texto}],
            inventario=[path.name],
        )

    if suffix in EXTENSOES_WORD_PARA_PDF:
        return PacoteEvidencia(
            caminho=path,
            tipo=suffix.lstrip("."),
            documentos=[
                {
                    "nome": path.name,
                    "tipo_convertido": "pdf",
                    "observacao": "Documento Word preservado para avaliacao visual por conversao para PDF no upload.",
                }
            ],
            inventario=[path.name],
        )

    return PacoteEvidencia(
        caminho=path,
        tipo=suffix.lstrip(".") or "desconhecido",
        documentos=[],
        inventario=[path.name],
        erro=f"tipo de evidencia nao suportado: {suffix or path.name}",
    )


# ---------------------------------------------------------------------------
# Extracao de texto (markitdown / xlsx / pdf)
# ---------------------------------------------------------------------------


def _extrair_texto_com_markitdown(caminho: Path) -> tuple[str, str]:
    suffix = caminho.suffix.lower()
    if suffix == ".xlsx":
        return _extrair_xlsx_abas_visiveis(caminho)
    if suffix == ".ods":
        return _extrair_texto_ods(caminho)
    try:
        from markitdown import MarkItDown
    except ModuleNotFoundError:
        return "", "markitdown nao instalado no ambiente virtual"
    try:
        md = MarkItDown()
        result = md.convert(str(caminho))
        return result.text_content, ""
    except Exception as exc:
        return "", f"erro ao extrair texto com markitdown: {exc}"


def _converter_ods_para_xlsx(origem: Path, destino_dir: Path) -> Path | None:
    """Converte um arquivo .ods para .xlsx via LibreOffice/soffice headless.

    Retorna o caminho do .xlsx gerado ou None em caso de falha.
    """
    conversor = shutil.which("soffice") or shutil.which("libreoffice")
    if not conversor:
        return None
    destino_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        try:
            result = subprocess.run(
                [
                    conversor,
                    "--headless",
                    "--convert-to",
                    "xlsx",
                    "--outdir",
                    str(tmp_path),
                    str(origem),
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=120,
            )
        except (subprocess.TimeoutExpired, OSError):
            return None
        if result.returncode != 0:
            return None
        xlsx_convertido = tmp_path / f"{origem.stem}.xlsx"
        if not xlsx_convertido.is_file():
            candidatos = sorted(tmp_path.glob("*.xlsx"))
            if not candidatos:
                return None
            xlsx_convertido = candidatos[0]
        nome_xlsx = nome_upload_seguro(origem.name, ".xlsx")
        target = caminho_unico(destino_dir, nome_xlsx)
        shutil.copyfile(xlsx_convertido, target)
        return target


def _extrair_texto_ods(caminho: Path) -> tuple[str, str]:
    """Converte .ods para .xlsx (via soffice) e extrai apenas abas visiveis.

    markitdown nao suporta .ods nativamente (UnsupportedFormatException).
    Workaround: converter ODS -> XLSX com LibreOffice headless e entao usar
    _extrair_xlsx_abas_visiveis (que filtra abas ocultas via openpyxl).
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        xlsx_path = _converter_ods_para_xlsx(caminho, Path(tmp_dir))
        if xlsx_path is None:
            return "", "soffice/libreoffice nao disponivel ou falhou ao converter .ods para .xlsx"
        return _extrair_xlsx_abas_visiveis(xlsx_path)


def _extrair_xlsx_abas_visiveis(caminho: Path) -> tuple[str, str]:
    """Extrai markdown de um XLSX considerando apenas abas visiveis.

    Reproduz o formato do MarkItDown (## nome_aba + tabela em markdown), mas
    filtra abas ocultas (sheet_state != 'visible') usando openpyxl.
    """
    try:
        import pandas as pd
        from openpyxl import load_workbook as _lw
    except ModuleNotFoundError as exc:
        return "", f"dependencia para xlsx nao disponivel: {exc}"
    try:
        wb = _lw(caminho, read_only=True, data_only=True)
        abas_visiveis = [ws.title for ws in wb.worksheets if ws.sheet_state == "visible"]
        wb.close()
        if not abas_visiveis:
            return "", "xlsx sem abas visiveis"
        partes: list[str] = []
        for nome_aba in abas_visiveis:
            df = pd.read_excel(caminho, sheet_name=nome_aba, engine="openpyxl")
            partes.append(f"## {nome_aba}\n")
            partes.append(df.to_markdown(index=False))
            partes.append("\n\n")
        return "".join(partes).strip(), ""
    except Exception as exc:
        return "", f"erro ao extrair xlsx com abas visiveis: {exc}"


def verificar_integridade_pdf(caminho: str | Path) -> tuple[bool, str]:
    """Verifica rapidamente se um PDF esta integro.

    Tenta abrir com pypdf; em falha, usa PyMuPDF (fitz). Retorna (True, "")
    se o PDF possui pelo menos uma pagina; caso contrario, (False, erro).
    """
    path = Path(caminho)

    if not path.exists():
        return False, "arquivo nao existe"

    if path.stat().st_size == 0:
        return False, "arquivo vazio"

    try:
        from pypdf import PdfReader

        with suprimir_stderr():
            reader = PdfReader(path)

            if len(reader.pages) == 0:
                return False, "pdf nao possui paginas"

        return True, ""

    except Exception as exc_pypdf:
        try:
            import fitz

            doc = fitz.open(str(path))
            ok = doc.page_count > 0
            doc.close()

            if ok:
                return True, ""

            return False, "pdf nao possui paginas"

        except Exception:
            return False, f"pdf corrompido ou ilegivel: {exc_pypdf}"


def _cortar_pdf_para_max_paginas(
    caminho: Path,
    destino: Path,
    *,
    max_paginas: int = MAX_PAGINAS_PDF,
) -> tuple[Path, dict[str, Any]]:
    """Corta um PDF para no maximo ``max_paginas`` paginas.

    Salva o PDF cortado em um subdiretorio temporario de ``destino``.
    Retorna (caminho_efetivo, info_corte).
    """
    try:
        import fitz
    except ModuleNotFoundError:
        return caminho, {}

    try:
        doc = fitz.open(str(caminho))
        total = doc.page_count
        if total <= max_paginas:
            doc.close()
            return caminho, {}

        pasta_corte = destino / "_pdf_cortados"
        pasta_corte.mkdir(parents=True, exist_ok=True)
        nome_cortado = nome_upload_seguro(caminho.name, caminho.suffix)
        caminho_cortado = pasta_corte / nome_cortado

        novo_doc = fitz.open()
        novo_doc.insert_pdf(doc, from_page=0, to_page=max_paginas - 1)
        novo_doc.save(str(caminho_cortado))
        novo_doc.close()
        doc.close()

        return caminho_cortado, {
            "pdf_cortado": True,
            "paginas_originais": total,
            "paginas_cortadas": max_paginas,
            "max_paginas": max_paginas,
        }
    except Exception:
        return caminho, {}


def _preparar_pdf_com_recuperacao(
    caminho: Path,
    destino: Path,
) -> tuple[Path, dict[str, Any], str]:
    """Verifica integridade do PDF, recupera se corrompido e corta se tiver
    mais de MAX_PAGINAS_PDF paginas.

    Todos os arquivos intermediarios ficam em subdiretorios temporarios de
    ``destino`` (upload_tmp), sem alterar a pasta original de evidencias.
    Retorna (caminho_efetivo, info, erro).
    """
    info: dict[str, Any] = {}
    caminho_efetivo = caminho

    ok, erro_integ = verificar_integridade_pdf(caminho)
    if not ok:
        pasta_rec = destino / "_pdf_recuperados"
        pasta_rec.mkdir(parents=True, exist_ok=True)
        caminho_recuperado, camada, erro_rec = recuperar_pdf(caminho, pasta_rec)
        if caminho_recuperado is not None:
            caminho_efetivo = caminho_recuperado
            info["pdf_recuperado"] = True
            info["camada_recuperacao"] = camada
        else:
            return caminho, info, erro_rec or erro_integ

    caminho_cortado, info_corte = _cortar_pdf_para_max_paginas(
        caminho_efetivo,
        destino,
        max_paginas=MAX_PAGINAS_PDF,
    )
    if info_corte:
        info.update(info_corte)
        caminho_efetivo = caminho_cortado

    return caminho_efetivo, info, ""


def _extrair_texto_pdf_reader(nome: str, reader: Any) -> tuple[list[dict[str, Any]], str]:
    documentos: list[dict[str, Any]] = []
    total_paginas = len(reader.pages)
    limite = min(total_paginas, MAX_PAGINAS_PDF)
    for index, page in enumerate(reader.pages[:limite], start=1):
        texto = (page.extract_text() or "").strip()
        if texto:
            documentos.append({"nome": nome, "pagina": index, "texto": texto})
    if not documentos:
        return [], "pdf sem texto extraivel"
    return documentos, ""


def _extrair_texto_pdf(caminho: str | Path) -> tuple[list[dict[str, Any]], str]:
    try:
        from pypdf import PdfReader
    except ModuleNotFoundError:
        return [], "pypdf nao instalado para normalizar PDF"
    try:
        path = Path(caminho)
        with suprimir_stderr():
            return _extrair_texto_pdf_reader(path.name, PdfReader(path))
    except Exception as exc:
        return [], f"erro ao normalizar PDF: {exc}"


# ---------------------------------------------------------------------------
# Recuperacao de PDF corrompido (camadas)
# ---------------------------------------------------------------------------


def _pdf_tem_paginas(caminho: Path) -> bool:
    try:
        import fitz

        doc = fitz.open(str(caminho))
        n = doc.page_count
        doc.close()
        return n > 0
    except Exception:
        return False


def recuperar_pdf(caminho: Path, destino_dir: Path) -> tuple[Path | None, str, str]:
    """Aplica protocolo de recuperacao de PDF corrompido em camadas.

    Retorna (caminho_recuperado, camada_aplicada, erro). Se todas as camadas
    falharem, retorna (None, ultima_camada_tentada, erro).
    """
    data = caminho.read_bytes()
    ultima_camada = ""

    tem_eof = b"%%EOF" in data[-1024:]
    tem_startxref = b"startxref" in data[-1024:]
    header_ok = data[:5] == b"%PDF-"

    # Camada 1.1 — Adicionar %%EOF no final
    ultima_camada = "1.1_eof"
    if not tem_eof:
        recuperado = destino_dir / f"{caminho.stem}_rec_eof.pdf"
        recuperado.write_bytes(data + b"\n%%EOF\n")
        if _pdf_tem_paginas(recuperado):
            return recuperado, ultima_camada, ""

    # Camada 1.2 — PyMuPDF: abrir e re-salvar
    ultima_camada = "1.2_fitz_resave"
    recuperado = _tentar_recuperar_fitz(caminho, destino_dir)
    if recuperado is not None:
        return recuperado, ultima_camada, ""

    # Camada 1.3 — pikepdf com flags permissivas
    ultima_camada = "1.3_pikepdf"
    recuperado = _tentar_recuperar_pikepdf(caminho, destino_dir)
    if recuperado is not None:
        return recuperado, ultima_camada, ""

    # Camada 4 — Reconstrucao manual
    ultima_camada = "4_reconstrucao_manual"
    recuperado = _tentar_reconstrucao_manual(caminho, destino_dir, data)
    if recuperado is not None:
        return recuperado, ultima_camada, ""

    # Camada 5 — Reconstrucao a partir de imagens extraidas
    ultima_camada = "5_imagens_extraidas"
    recuperado = _tentar_reconstrucao_imagens(caminho, destino_dir, data)
    if recuperado is not None:
        return recuperado, ultima_camada, ""

    return None, ultima_camada, "todas as camadas de recuperacao falharam"


def _tentar_recuperar_fitz(caminho: Path, destino_dir: Path) -> Path | None:
    try:
        import fitz

        doc = fitz.open(str(caminho))
        if doc.page_count == 0:
            doc.close()
            return None
        recuperado = destino_dir / f"{caminho.stem}_rec_fitz.pdf"
        doc.save(str(recuperado), garbage=4, deflate=True, clean=True)
        doc.close()
        if _pdf_tem_paginas(recuperado):
            return recuperado
    except Exception:
        pass
    return None


def _tentar_recuperar_pikepdf(caminho: Path, destino_dir: Path) -> Path | None:
    try:
        import pikepdf

        recuperado = destino_dir / f"{caminho.stem}_rec_pikepdf.pdf"
        with pikepdf.open(str(caminho), ignore_xref_streams=True) as pdf:
            pdf.save(str(recuperado))
        if _pdf_tem_paginas(recuperado):
            return recuperado
    except Exception:
        pass
    return None


def _tentar_reconstrucao_manual(caminho: Path, destino_dir: Path, data: bytes) -> Path | None:
    """Camada 4: Reconstruir manualmente Catalog, Pages, xref e trailer."""
    try:
        objs = list(re.finditer(rb"(\d+)\s+(\d+)\s+obj\b", data))
        if not objs:
            return None
        page_objs: list[int] = []
        for m in objs:
            obj_num = int(m.group(1))
            trecho = data[m.end():m.end() + 200]
            if rb"/Type" in trecho and rb"/Page" in trecho and rb"/Pages" not in trecho:
                page_objs.append(obj_num)
        if not page_objs:
            return None
        nums_usados = {int(m.group(1)) for m in objs}
        catalog_num = 1 if 1 not in nums_usados else max(nums_usados) + 1
        pages_num = catalog_num + 1 if catalog_num + 1 not in nums_usados else max(nums_usados) + 2
        catalog_obj = (
            f"{catalog_num} 0 obj\n<< /Type /Catalog /Pages {pages_num} 0 R >>\nendobj\n"
        ).encode()
        kids = " ".join(f"{n} 0 R" for n in page_objs)
        pages_obj = (
            f"{pages_num} 0 obj\n<< /Type /Pages /Kids [ {kids} ] /Count {len(page_objs)} >>\nendobj\n"
        ).encode()
        output = bytearray()
        output.extend(b"%PDF-1.7\n%\xe2\xe3\xcf\xd3\n")
        offsets: dict[int, int] = {}
        offsets[catalog_num] = len(output)
        output.extend(catalog_obj)
        offsets[pages_num] = len(output)
        output.extend(pages_obj)
        for m in objs:
            obj_num = int(m.group(1))
            if obj_num in (catalog_num, pages_num):
                continue
            end = data.find(b"endobj", m.end())
            if end == -1:
                continue
            conteudo = data[m.start():end + 6] + b"\n"
            offsets[obj_num] = len(output)
            output.extend(conteudo)
        xref_offset = len(output)
        output.extend(b"xref\n")
        output.extend(f"0 {max(offsets.keys()) + 1}\n".encode())
        output.extend(b"0000000000 65535 f \n")
        for i in range(1, max(offsets.keys()) + 1):
            if i in offsets:
                output.extend(f"{offsets[i]:010d} 00000 n \n".encode())
            else:
                output.extend(b"0000000000 00000 f \n")
        output.extend(b"trailer\n")
        output.extend(f"<< /Size {max(offsets.keys()) + 1} /Root {catalog_num} 0 R >>\n".encode())
        output.extend(b"startxref\n")
        output.extend(f"{xref_offset}\n".encode())
        output.extend(b"%%EOF\n")
        recuperado = destino_dir / f"{caminho.stem}_rec_manual.pdf"
        recuperado.write_bytes(bytes(output))
        try:
            import fitz
            doc = fitz.open(str(recuperado))
            if doc.page_count > 0:
                otimizado = destino_dir / f"{caminho.stem}_rec_manual_opt.pdf"
                doc.save(str(otimizado), garbage=4, deflate=True, clean=True)
                doc.close()
                return otimizado
            doc.close()
        except Exception:
            pass
        if _pdf_tem_paginas(recuperado):
            return recuperado
    except Exception:
        pass
    return None


def _tentar_reconstrucao_imagens(caminho: Path, destino_dir: Path, data: bytes) -> Path | None:
    """Camada 5: Extrai imagens JPEG embarcadas e cria novo PDF."""
    try:
        import fitz
        from PIL import Image
    except ModuleNotFoundError:
        return None
    imagens: list[bytes] = []
    start = 0
    while True:
        pos = data.find(b"\xff\xd8\xff", start)
        if pos == -1:
            break
        end = data.find(b"\xff\xd9", pos)
        if end == -1:
            break
        imagens.append(data[pos:end + 2])
        start = end + 2
    if not imagens:
        return None
    recuperado = destino_dir / f"{caminho.stem}_rec_imagens.pdf"
    imagens_dir = destino_dir / f"{caminho.stem}_imgs"
    imagens_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open()
    for i, img_data in enumerate(imagens):
        img_path = imagens_dir / f"img_{i:03d}.jpg"
        img_path.write_bytes(img_data)
        try:
            img = Image.open(img_path)
            img.verify()
            img = Image.open(img_path)
            page = doc.new_page(width=img.width, height=img.height)
            page.insert_image(fitz.Rect(0, 0, img.width, img.height), filename=str(img_path))
        except Exception:
            continue
    if doc.page_count == 0:
        doc.close()
        return None
    doc.save(str(recuperado))
    doc.close()
    return recuperado


# ---------------------------------------------------------------------------
# Extracao PDF -> Markdown + imagens (pdf2md)
# ---------------------------------------------------------------------------


def _tentar_extrair_markdown_pdf(
    caminho: Path,
    raiz: Path,
    imagens_dir: Path,
    slug: str,
    dpi: int,
) -> tuple[str, str]:
    """Tenta extrair markdown de um PDF com pymupdf4llm. Retorna (markdown, erro)."""
    try:
        import pymupdf4llm
    except ModuleNotFoundError:
        return "", "pymupdf4llm nao instalado no ambiente virtual"
    try:
        import fitz

        doc = fitz.open(str(caminho))
        total_paginas = doc.page_count
        doc.close()
    except Exception:
        total_paginas = 0
    if total_paginas > 0:
        pages = list(range(0, min(total_paginas, MAX_PAGINAS_PDF)))
    else:
        pages = None
    caminho_absoluto = caminho.resolve()
    cwd = Path.cwd()
    try:
        os.chdir(raiz)
        kwargs: dict[str, Any] = {
            "write_images": True,
            "image_path": "img",
            "image_format": "png",
            "dpi": dpi,
        }
        if pages is not None:
            kwargs["pages"] = pages
        markdown = pymupdf4llm.to_markdown(str(caminho_absoluto), **kwargs)
        return markdown, ""
    except Exception as exc:
        return "", f"erro ao extrair PDF com pymupdf4llm: {exc}"
    finally:
        os.chdir(cwd)


def extrair_pdf_markdown_imagens(
    caminho: Path,
    destino: Path,
    nome_original: str | None = None,
    *,
    dpi: int = 150,
) -> tuple[PacoteEvidencia | None, list[str], str]:
    """Extrai Markdown + imagens de um PDF (modo --pdf2md).

    Em caso de falha inicial, tenta recuperar o PDF corrompido e repetir.
    Retorna (pacote, arquivos_upload, erro).
    """
    try:
        import pymupdf4llm  # noqa: F401
    except ModuleNotFoundError:
        return None, [], "pymupdf4llm nao instalado no ambiente virtual"

    destino.mkdir(parents=True, exist_ok=True)
    nome_base = nome_original or caminho.name
    slug = slug_ascii(Path(nome_base).stem, fallback="pdf")
    raiz = caminho_unico(destino, f"{slug}-md")
    raiz.mkdir(parents=True, exist_ok=True)
    imagens_dir = raiz / "img"
    imagens_dir.mkdir(parents=True, exist_ok=True)
    markdown_nome = f"{slug}.md"
    markdown_path = raiz / markdown_nome

    markdown, erro = _tentar_extrair_markdown_pdf(caminho, raiz, imagens_dir, slug, dpi)
    if erro:
        pdf_recuperado, camada, erro_rec = recuperar_pdf(caminho, destino)
        if pdf_recuperado is not None:
            markdown, erro = _tentar_extrair_markdown_pdf(
                pdf_recuperado, raiz, imagens_dir, slug, dpi
            )
            if erro:
                return None, [], f"erro ao extrair PDF com pymupdf4llm apos recuperacao (camada {camada}): {erro}"
        else:
            return None, [], f"erro ao extrair PDF com pymupdf4llm: {erro}. recuperacao tentada ate camada {camada} sem sucesso: {erro_rec}"

    markdown_path.write_text(markdown, encoding="utf-8")
    imagens = sorted(path for path in imagens_dir.glob("*") if path.is_file())

    # Dedup de imagens por hash de conteudo
    hashes_imagens: dict[str, Path] = {}
    dedup_map: dict[str, Path] = {}
    duplicadas_removidas: list[str] = []
    for img in imagens:
        h = hash_arquivo(img)
        if h in hashes_imagens:
            dedup_map[str(img)] = hashes_imagens[h]
            duplicadas_removidas.append(img.name)
        else:
            hashes_imagens[h] = img

    if dedup_map:
        texto_md = markdown_path.read_text(encoding="utf-8")
        for caminho_dup, caminho_orig in dedup_map.items():
            nome_dup = Path(caminho_dup).name
            nome_orig = caminho_orig.name
            texto_md = texto_md.replace(nome_dup, nome_orig)
        markdown_path.write_text(texto_md, encoding="utf-8")
        markdown = texto_md
        for img_dup in dedup_map:
            Path(img_dup).unlink()

    imagens_unicas = sorted(path for path in imagens_dir.glob("*") if path.is_file())
    imagens_relativas = [str(path.relative_to(raiz).as_posix()) for path in imagens_unicas]
    documentos = [
        {
            "nome": markdown_nome,
            "origem_pdf": nome_base,
            "tipo_extraido": "pdf_markdown_imagens",
            "texto": markdown,
            "imagens_extraidas": imagens_relativas,
            "duplicadas_removidas": duplicadas_removidas,
        }
    ]
    inventario = [nome_base, markdown_nome, *imagens_relativas]
    arquivos_upload = [str(markdown_path), *(str(path) for path in imagens_unicas)]
    pacote = PacoteEvidencia(
        caminho=caminho,
        tipo="pdf_markdown_imagens",
        documentos=documentos,
        inventario=inventario,
    )
    return pacote, arquivos_upload, ""


# ---------------------------------------------------------------------------
# Extracao DOCX -> HTML + imagens (docx2html)
# ---------------------------------------------------------------------------


def _extensao_imagem_mammoth(content_type: str) -> str:
    extensao = mimetypes.guess_extension(content_type.split(";")[0].strip())
    if extensao == ".jpe":
        return ".jpg"
    return extensao or ".bin"


def extrair_docx_html_imagens(
    caminho: Path,
    destino: Path,
    nome_original: str | None = None,
) -> tuple[PacoteEvidencia | None, list[str], str]:
    """Extrai HTML + imagens de um DOCX (modo --docx2html)."""
    try:
        import mammoth
    except ModuleNotFoundError:
        return None, [], "mammoth nao instalado no ambiente virtual"

    destino.mkdir(parents=True, exist_ok=True)
    nome_base = nome_original or caminho.name
    slug = slug_ascii(Path(nome_base).stem, fallback="docx")
    raiz = caminho_unico(destino, f"{slug}-html")
    raiz.mkdir(parents=True, exist_ok=True)
    imagens_dir = raiz / "img"
    imagens_dir.mkdir(parents=True, exist_ok=True)
    html_nome = f"{slug}.html"
    html_path = raiz / html_nome
    imagens: list[Path] = []
    contador = 0

    def salvar_imagem(image: Any) -> dict[str, str]:
        nonlocal contador
        contador += 1
        suffix = _extensao_imagem_mammoth(str(getattr(image, "content_type", "")))
        image_path = imagens_dir / f"img_{contador:03d}{suffix}"
        with image.open() as image_bytes:
            image_path.write_bytes(image_bytes.read())
        imagens.append(image_path)
        return {"src": f"img/{image_path.name}"}

    try:
        with caminho.open("rb") as handle:
            resultado = mammoth.convert_to_html(
                handle,
                convert_image=mammoth.images.img_element(salvar_imagem),
            )
    except Exception as exc:
        return None, [], f"erro ao extrair DOCX com mammoth: {exc}"

    html_path.write_text(resultado.value, encoding="utf-8")
    imagens = sorted(path for path in imagens if path.is_file())
    imagens_relativas = [str(path.relative_to(raiz).as_posix()) for path in imagens]
    avisos = [str(message) for message in getattr(resultado, "messages", [])]
    documentos = [
        {
            "nome": html_nome,
            "origem_docx": nome_base,
            "tipo_extraido": "docx_html_imagens",
            "formato": "html",
            "texto": resultado.value,
            "imagens_extraidas": imagens_relativas,
            "avisos_conversao": avisos,
        }
    ]
    inventario = [nome_base, html_nome, *imagens_relativas]
    imagens_upload = [path for path in imagens if path.suffix.casefold() in {".png", ".jpg", ".jpeg"}]
    arquivos_upload = [str(path) for path in imagens_upload]
    pacote = PacoteEvidencia(
        caminho=caminho,
        tipo="docx_html_imagens",
        documentos=documentos,
        inventario=inventario,
    )
    return pacote, arquivos_upload, ""


# ---------------------------------------------------------------------------
# Conversao Word -> PDF
# ---------------------------------------------------------------------------


def converter_word_para_pdf(origem: Path, destino: Path, nome_original: str | None = None) -> tuple[Path | None, str]:
    conversor = shutil.which("soffice") or shutil.which("libreoffice")
    if not conversor:
        return _converter_word_para_pdf_com_microsoft_word(origem, destino, nome_original)
    destino.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        try:
            result = subprocess.run(
                [
                    conversor,
                    "--headless",
                    "--convert-to",
                    "pdf",
                    "--outdir",
                    str(tmp_path),
                    str(origem),
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=120,
            )
        except subprocess.TimeoutExpired:
            convertido, erro_word = _converter_word_para_pdf_com_microsoft_word(origem, destino, nome_original)
            if convertido:
                return convertido, ""
            return None, f"timeout ao converter documento Word em PDF; fallback Microsoft Word: {erro_word}"
        except OSError as exc:
            convertido, erro_word = _converter_word_para_pdf_com_microsoft_word(origem, destino, nome_original)
            if convertido:
                return convertido, ""
            return None, f"erro ao executar conversor de documento Word para PDF: {exc}; fallback Microsoft Word: {erro_word}"
        if result.returncode != 0:
            detalhe = (result.stderr or result.stdout or "").strip()
            convertido, erro_word = _converter_word_para_pdf_com_microsoft_word(origem, destino, nome_original)
            if convertido:
                return convertido, ""
            return None, f"erro ao converter documento Word em PDF: {detalhe or result.returncode}; fallback Microsoft Word: {erro_word}"
        pdf_convertido = tmp_path / f"{origem.stem}.pdf"
        if not pdf_convertido.is_file():
            candidatos = sorted(tmp_path.glob("*.pdf"))
            if not candidatos:
                convertido, erro_word = _converter_word_para_pdf_com_microsoft_word(origem, destino, nome_original)
                if convertido:
                    return convertido, ""
                return None, f"conversor de documento Word para PDF nao gerou arquivo PDF; fallback Microsoft Word: {erro_word}"
            pdf_convertido = candidatos[0]
        nome_pdf = nome_upload_seguro(nome_original or origem.name, ".pdf")
        target = caminho_unico(destino, nome_pdf)
        shutil.copyfile(pdf_convertido, target)
        return target, ""


def _converter_word_para_pdf_com_microsoft_word(
    origem: Path,
    destino: Path,
    nome_original: str | None = None,
) -> tuple[Path | None, str]:
    if os.name != "nt":
        return None, "Microsoft Word COM disponivel apenas no Windows"
    if not shutil.which("powershell.exe"):
        return None, "powershell.exe nao encontrado para acionar Microsoft Word"
    destino.mkdir(parents=True, exist_ok=True)
    nome_pdf = nome_upload_seguro(nome_original or origem.name, ".pdf")
    target = caminho_unico(destino, nome_pdf)
    script = r"""
param([string]$Source, [string]$Target)
$ErrorActionPreference = 'Stop'
$word = $null
$doc = $null
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $sourcePath = (Resolve-Path -LiteralPath $Source).Path
    $doc = $word.Documents.Open([ref]$sourcePath, [ref]$false, [ref]$true, [ref]$false)
    if ($null -eq $doc) {
        $doc = $word.ActiveDocument
    }
    if ($null -eq $doc) {
        throw 'Microsoft Word nao abriu o documento'
    }
    $doc.ExportAsFixedFormat($Target, 17)
} finally {
    if ($null -ne $doc) {
        $doc.Close($false) | Out-Null
        [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($doc) | Out-Null
    }
    if ($null -ne $word) {
        $word.Quit() | Out-Null
        [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($word) | Out-Null
    }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
"""
    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            local_source = tmp_path / f"source{origem.suffix.lower()}"
            local_target = tmp_path / "converted.pdf"
            script_path = tmp_path / "convert-word-to-pdf.ps1"
            shutil.copyfile(origem, local_source)
            script_path.write_text(script, encoding="utf-8")
            result = subprocess.run(
                [
                    "powershell.exe",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(script_path),
                    "-Source",
                    str(local_source),
                    "-Target",
                    str(local_target),
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=180,
            )
            if result.returncode != 0:
                detalhe = (result.stderr or result.stdout or "").strip()
                return None, f"erro ao converter documento Word em PDF com Microsoft Word: {detalhe or result.returncode}"
            if not local_target.is_file():
                return None, "Microsoft Word nao gerou arquivo PDF"
            shutil.copyfile(local_target, target)
    except subprocess.TimeoutExpired:
        return None, "timeout ao converter documento Word em PDF com Microsoft Word"
    except OSError as exc:
        return None, f"erro ao acionar Microsoft Word para converter documento Word em PDF: {exc}"
    if not target.is_file():
        return None, "Microsoft Word nao gerou arquivo PDF"
    return target, ""


# ---------------------------------------------------------------------------
# Preparo de documento para upload (markitdown -> .txt)
# ---------------------------------------------------------------------------


def preparar_documento_para_upload(caminho: Path, destino: Path, nome_original: str | None = None) -> Path | None:
    texto, erro = _extrair_texto_com_markitdown(caminho)
    if erro:
        return None
    return gravar_upload_texto(destino, nome_original or caminho.name, texto)


# ---------------------------------------------------------------------------
# Processamento de ZIP com preprocessamento (pdf2md / docx2html)
# ---------------------------------------------------------------------------


def _processar_evidencia(
    caminho: Path,
    destino: Path,
    *,
    pdf2md: bool = False,
    docx2html: bool = False,
    dpi: int = 150,
) -> tuple[PacoteEvidencia, list[str]]:
    """Fluxo unico de processamento de evidencia (compactado ou avulso).

    Para .zip/.rar, extrai recursivamente, achata, deduplica e processa cada
    arquivo. Para arquivos avulsos, aplica o processamento individual.
    Retorna (pacote, arquivos_upload).
    """
    suffix = caminho.suffix.lower()
    destino.mkdir(parents=True, exist_ok=True)

    if suffix in EXTENSOES_COMPACTADOS:
        pasta_extraidos = destino / f"_extraidos_{slug_ascii(caminho.stem, fallback='compactado')}"
        pasta_extraidos.mkdir(parents=True, exist_ok=True)
        arquivos, duplicados_ignorados, erros = extrair_arquivo_compactado(
            caminho,
            pasta_extraidos,
        )
        if erros and not arquivos:
            return PacoteEvidencia(
                caminho=caminho,
                tipo=suffix.lstrip("."),
                documentos=[],
                inventario=[],
                erro="; ".join(erros),
            ), []

        documentos: list[dict[str, Any]] = []
        arquivos_upload: list[str] = []
        inventario: list[str] = []
        for arquivo in arquivos:
            docs, upload, erro_arq = processar_arquivo_individual(
                arquivo,
                destino,
                nome_exibicao=arquivo.name,
                pdf2md=pdf2md,
                docx2html=docx2html,
                dpi=dpi,
            )
            if erro_arq:
                documentos.append({"nome": arquivo.name, "erro": erro_arq})
            else:
                documentos.extend(docs)
            arquivos_upload.extend(upload)
            inventario.append(arquivo.name)

        return PacoteEvidencia(
            caminho=caminho,
            tipo=suffix.lstrip("."),
            documentos=documentos,
            inventario=inventario,
            erro="; ".join(erros) if erros else "",
            duplicados_ignorados=tuple(duplicados_ignorados),
        ), arquivos_upload

    docs, upload, erro = processar_arquivo_individual(
        caminho,
        destino,
        pdf2md=pdf2md,
        docx2html=docx2html,
        dpi=dpi,
    )
    return PacoteEvidencia(
        caminho=caminho,
        tipo=suffix.lstrip(".") or "desconhecido",
        documentos=docs,
        inventario=[caminho.name],
        erro=erro,
    ), upload


def _processar_evidencia_retornando_upload(
    caminho: Path,
    destino: Path,
    *,
    pdf2md: bool = False,
    docx2html: bool = False,
    dpi: int = 150,
) -> tuple[list[str], str]:
    """Wrapper de _processar_evidencia que retorna apenas upload e erro."""
    pacote, arquivos_upload = _processar_evidencia(
        caminho,
        destino,
        pdf2md=pdf2md,
        docx2html=docx2html,
        dpi=dpi,
    )
    return arquivos_upload, pacote.erro


def processar_compactado_com_preprocessamento(
    caminho_compactado: Path,
    destino: Path,
    *,
    pdf2md: bool = False,
    docx2html: bool = False,
    dpi: int = 150,
) -> tuple[PacoteEvidencia | None, list[str], str]:
    """Extrai arquivos de .zip/.rar aplicando pdf2md/docx2html a cada um.

    Retorna um PacoteEvidencia consolidado com os documentos extraidos e a
    lista de arquivos para upload. Delega para o fluxo unificado de
    processamento de arquivos individuais.
    """
    pacote, arquivos_upload = _processar_evidencia(
        caminho_compactado,
        destino,
        pdf2md=pdf2md,
        docx2html=docx2html,
        dpi=dpi,
    )
    return pacote, arquivos_upload, ""


# Alias legado para compatibilidade com chamadores anteriores.
processar_zip_com_preprocessamento = processar_compactado_com_preprocessamento


# ---------------------------------------------------------------------------
# Arquivos compativeis para upload (fluxo padrao, sem pdf2md/docx2html)
# ---------------------------------------------------------------------------


def arquivos_compativeis_upload(
    caminho: str | Path,
    destino_zip: str | Path | None = None,
    *,
    pdf2md: bool = False,
    docx2html: bool = False,
    dpi: int = 150,
) -> list[str]:
    path = Path(caminho)
    suffix = path.suffix.lower()

    if destino_zip is None:
        if suffix in EXTENSOES_UPLOAD_DIRETO:
            return [str(path)]
        return []

    destino = Path(destino_zip)
    if suffix in EXTENSOES_COMPACTADOS or suffix in EXTENSOES_UPLOAD_PREPARAVEIS:
        arquivos_upload, erro = _processar_evidencia_retornando_upload(
            path,
            destino,
            pdf2md=pdf2md,
            docx2html=docx2html,
            dpi=dpi,
        )
        if erro:
            raise RuntimeError(erro)
        return arquivos_upload

    return []


# ---------------------------------------------------------------------------
# Erros tecnicos / resultado evidence ausente
# ---------------------------------------------------------------------------


def _erros_documentos(pacote: PacoteEvidencia) -> list[str]:
    erros = []
    for documento in pacote.documentos:
        erro = documento.get("erro") if isinstance(documento, dict) else None
        nome = documento.get("nome") if isinstance(documento, dict) else ""
        if erro:
            erros.append(f"{nome}: {erro}" if nome else str(erro))
    return erros


def _erro_pdf_mitigado_por_upload(erro: str, arquivos_upload: list[str]) -> bool:
    texto = erro.casefold()
    return bool(arquivos_upload) and "pdf" in texto and (
        "sem texto extraivel" in texto
        or "normalizar pdf" in texto
        or "extrair texto" in texto
    )


def erro_tecnico_bloqueante_pacote(pacote: PacoteEvidencia, arquivos_upload: list[str]) -> str:
    if pacote.erro and not _erro_pdf_mitigado_por_upload(pacote.erro, arquivos_upload):
        return pacote.erro
    erros_bloqueantes = [
        erro for erro in _erros_documentos(pacote) if not _erro_pdf_mitigado_por_upload(erro, arquivos_upload)
    ]
    if erros_bloqueantes:
        return "; ".join(erros_bloqueantes)
    if not pacote.documentos and not arquivos_upload:
        return "evidencia sem conteudo processavel para avaliacao"
    if all(documento.get("nao_suportado") for documento in pacote.documentos) and not arquivos_upload:
        return "evidencia contem apenas arquivos de tipo nao suportado"
    return ""


def resultado_indica_erro_tecnico(resultado: dict[str, Any]) -> str:
    if resultado.get("status") != "completed":
        return ""
    termos = [
        "markitdown",
        "erro tecnico",
        "erro técnico",
        "nao possui acesso ao conteudo",
        "não possui acesso ao conteúdo",
        "conteudo do arquivo inacessivel",
        "conteúdo do arquivo inacessível",
    ]
    conclusoes = resultado.get("conclusoes")
    if not isinstance(conclusoes, list):
        return ""
    for conclusao in conclusoes:
        if not isinstance(conclusao, dict):
            continue
        campos = [
            conclusao.get("justificativa", ""),
            " ".join(str(valor) for valor in conclusao.get("lacunas", []) if valor is not None)
            if isinstance(conclusao.get("lacunas"), list)
            else str(conclusao.get("lacunas", "")),
        ]
        texto = " ".join(campos).casefold()
        if any(termo in texto for termo in termos):
            return "modelo indicou erro tecnico de acesso/processamento da evidencia"
    return ""


def resultado_evidencia_ausente(itens: list[Any]) -> dict[str, Any]:
    def _v(item: Any, campo: str) -> Any:
        return getattr(item, campo) if hasattr(item, campo) else item.get(campo)
    return {
        "status": "completed",
        "conclusoes": [
            {
                "item_codigo": _v(item, "codigo"),
                "item_texto": _v(item, "texto"),
                "afirmacao_auditado": _v(item, "afirmacao"),
                "estado": "nao_conforme",
                "justificativa": "O auditado afirmou o item, mas nao enviou evidencia para sustentar a afirmacao.",
                "lacunas": ["Evidencia nao enviada."],
                "arquivos_referenciados": [],
                "trechos_ou_elementos": [],
                "paginas_ou_localizacao": [],
            }
            for item in itens
        ],
    }


# ---------------------------------------------------------------------------
# Preparacao unificada de evidencia para envio ao provider (pipeline + juiz)
# ---------------------------------------------------------------------------


def preparar_evidencia_para_provider(
    caminho_evidencia: Path,
    upload_tmp: str | Path,
    *,
    pdf2md: bool,
    docx2html: bool,
    dpi: int,
) -> tuple[PacoteEvidencia, list[str], str | None]:
    """Prepara a evidencia para envio ao provider aplicando os modos de
    preprocessamento (pdf2md, docx2html) quando ativos.

    Retorna (pacote, arquivos_upload, erro). Em caso de erro, ``erro`` e nao
    nulo e o pacote retornado e um PacoteEvidencia de erro (sem documentos).
    Esta funcao elimina a duplicacao que existia entre o pipeline e a
    consolidacao.
    """
    upload_tmp_path = Path(upload_tmp)
    suffix_evidencia = caminho_evidencia.suffix.lower()
    try:
        pacote, arquivos_upload = _processar_evidencia(
            caminho_evidencia,
            upload_tmp_path,
            pdf2md=pdf2md,
            docx2html=docx2html,
            dpi=dpi,
        )
        if pacote.erro and not arquivos_upload:
            raise RuntimeError(pacote.erro)
        return pacote, arquivos_upload, None
    except RuntimeError as exc:
        pacote_erro = PacoteEvidencia(
            caminho=caminho_evidencia,
            tipo=suffix_evidencia.lstrip("."),
            documentos=[],
            inventario=[],
            erro=str(exc),
        )
        return pacote_erro, [], str(exc)