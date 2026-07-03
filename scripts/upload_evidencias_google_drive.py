#!/usr/bin/env python3
"""Envia evidencias coletadas ao Google Drive e gera tabela de links publicos.

Requer um arquivo OAuth 2.0 Client ID do tipo "Desktop app" baixado do Google
Cloud Console. No primeiro uso, o script abre o navegador para autorizacao e
armazena um token de atualizacao para execucoes posteriores.
"""

from __future__ import annotations

import argparse
import csv
import json
import mimetypes
import os
import sys
import time
import urllib.parse
import webbrowser
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any

import requests


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_DIR = (
    REPO_ROOT
    / "02-Execucao/01-Questionario/01-Coleta_LimeSurvey/"
    "Evidencias_Coletadas/evidencias"
)
DEFAULT_OUTPUT_XLSX = (
    DEFAULT_INPUT_DIR.parent / "evidencias_links_google_drive.xlsx"
)
DEFAULT_OUTPUT_CSV = DEFAULT_INPUT_DIR.parent / "evidencias_links_google_drive.csv"
DEFAULT_DRIVE_FOLDER = "Meu Drive/workspace/2026-Fiscalizacao-18-iGovTI2026"
DEFAULT_TOKEN_PATH = (
    Path.home() / ".config/tcerj-igovti/google-drive-oauth-token.json"
)
DEFAULT_DRIVE_SCOPE = "https://www.googleapis.com/auth/drive"
TOKEN_URL = "https://oauth2.googleapis.com/token"
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
DRIVE_API = "https://www.googleapis.com/drive/v3"
DRIVE_UPLOAD_API = "https://www.googleapis.com/upload/drive/v3"
FOLDER_MIME = "application/vnd.google-apps.folder"


class OAuthError(RuntimeError):
    pass


class DriveApiError(RuntimeError):
    pass


@dataclass
class OAuthClient:
    client_id: str
    client_secret: str


class TokenStore:
    def __init__(
        self,
        client: OAuthClient,
        token_path: Path,
        *,
        port: int,
        no_browser: bool,
        scope: str,
    ) -> None:
        self.client = client
        self.token_path = token_path
        self.port = port
        self.no_browser = no_browser
        self.scope = scope
        self.token: dict[str, Any] = self._load_token()

    def access_token(self) -> str:
        if self._token_valid():
            return str(self.token["access_token"])
        if self.token.get("refresh_token"):
            self._refresh_token()
            return str(self.token["access_token"])
        self._authorize()
        return str(self.token["access_token"])

    def _load_token(self) -> dict[str, Any]:
        if not self.token_path.exists():
            return {}
        with self.token_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def _save_token(self, token: dict[str, Any]) -> None:
        if "expires_in" in token:
            token["expires_at"] = int(time.time()) + int(token["expires_in"]) - 60
        if self.token.get("refresh_token") and "refresh_token" not in token:
            token["refresh_token"] = self.token["refresh_token"]
        self.token_path.parent.mkdir(parents=True, exist_ok=True)
        with self.token_path.open("w", encoding="utf-8") as handle:
            json.dump(token, handle, indent=2, ensure_ascii=False)
        self.token = token

    def _token_valid(self) -> bool:
        return bool(
            self.token.get("access_token")
            and int(self.token.get("expires_at", 0)) > int(time.time())
        )

    def _refresh_token(self) -> None:
        response = requests.post(
            TOKEN_URL,
            data={
                "client_id": self.client.client_id,
                "client_secret": self.client.client_secret,
                "refresh_token": self.token["refresh_token"],
                "grant_type": "refresh_token",
            },
            timeout=60,
        )
        if not response.ok:
            raise OAuthError(
                f"Falha ao atualizar token OAuth: {response.status_code} {response.text}"
            )
        self._save_token(response.json())

    def _authorize(self) -> None:
        redirect_uri = f"http://localhost:{self.port}/oauth2callback"
        params = {
            "client_id": self.client.client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": self.scope,
            "access_type": "offline",
            "prompt": "consent",
        }
        auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
        print("Abra a URL de autorizacao no navegador:")
        print(auth_url)
        if not self.no_browser:
            webbrowser.open(auth_url)
        code = receive_oauth_code(self.port)
        response = requests.post(
            TOKEN_URL,
            data={
                "code": code,
                "client_id": self.client.client_id,
                "client_secret": self.client.client_secret,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code",
            },
            timeout=60,
        )
        if not response.ok:
            raise OAuthError(
                f"Falha ao obter token OAuth: {response.status_code} {response.text}"
            )
        self._save_token(response.json())


def receive_oauth_code(port: int) -> str:
    result: dict[str, str] = {}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)
            if "error" in params:
                result["error"] = params["error"][0]
            if "code" in params:
                result["code"] = params["code"][0]
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(
                "Autorizacao recebida. Voce pode fechar esta janela.\n".encode(
                    "utf-8"
                )
            )

        def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
            return

    with HTTPServer(("localhost", port), Handler) as server:
        print(f"Aguardando autorizacao OAuth em http://localhost:{port}/oauth2callback")
        server.handle_request()
    if result.get("error"):
        raise OAuthError(f"Autorizacao recusada: {result['error']}")
    if not result.get("code"):
        raise OAuthError("Codigo OAuth nao recebido.")
    return result["code"]


def load_oauth_client(path: Path) -> OAuthClient:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    payload = data.get("installed") or data.get("web") or data
    client_id = payload.get("client_id")
    client_secret = payload.get("client_secret")
    if not client_id or not client_secret:
        raise OAuthError(
            "Arquivo client_secret invalido: client_id/client_secret nao encontrados."
        )
    return OAuthClient(client_id=client_id, client_secret=client_secret)


class DriveClient:
    def __init__(self, token_store: TokenStore) -> None:
        self.token_store = token_store

    def request(
        self,
        method: str,
        url: str,
        *,
        expected: tuple[int, ...] = (200,),
        **kwargs: Any,
    ) -> dict[str, Any]:
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self.token_store.access_token()}"
        response = requests.request(method, url, headers=headers, timeout=120, **kwargs)
        if response.status_code not in expected:
            raise DriveApiError(
                f"Erro na API do Drive ({method} {url}): "
                f"{response.status_code} {response.text}"
            )
        if not response.text:
            return {}
        return response.json()

    def list_files(self, query: str, fields: str) -> list[dict[str, Any]]:
        files: list[dict[str, Any]] = []
        page_token: str | None = None
        while True:
            params = {
                "q": query,
                "fields": f"nextPageToken,files({fields})",
                "pageSize": 1000,
                "supportsAllDrives": "false",
            }
            if page_token:
                params["pageToken"] = page_token
            payload = self.request("GET", f"{DRIVE_API}/files", params=params)
            files.extend(payload.get("files", []))
            page_token = payload.get("nextPageToken")
            if not page_token:
                return files

    def create_folder(self, name: str, parent_id: str) -> dict[str, Any]:
        metadata: dict[str, Any] = {"name": name, "mimeType": FOLDER_MIME}
        if parent_id:
            metadata["parents"] = [parent_id]
        return self.request(
            "POST",
            f"{DRIVE_API}/files",
            params={"fields": "id,name,webViewLink"},
            json=metadata,
        )

    def ensure_folder_path(self, drive_path: str, create: bool) -> str:
        parent_id = "root"
        parts = normalize_drive_path(drive_path)
        for part in parts:
            query = (
                f"name = '{drive_query_value(part)}' and "
                f"mimeType = '{FOLDER_MIME}' and "
                f"'{drive_query_value(parent_id)}' in parents and trashed = false"
            )
            matches = self.list_files(query, "id,name")
            if matches:
                parent_id = matches[0]["id"]
                continue
            if not create:
                raise DriveApiError(f"Pasta nao encontrada no Drive: {part}")
            folder = self.create_folder(part, parent_id)
            parent_id = folder["id"]
        return parent_id

    def find_existing_file(self, name: str, parent_id: str) -> dict[str, Any] | None:
        query = (
            f"name = '{drive_query_value(name)}' and "
            f"'{drive_query_value(parent_id)}' in parents and trashed = false"
        )
        matches = self.list_files(
            query, "id,name,webViewLink,webContentLink,size,md5Checksum"
        )
        return matches[0] if matches else None

    def upload_file(self, path: Path, parent_id: str) -> dict[str, Any]:
        mime_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        metadata = {"name": path.name, "parents": [parent_id]}
        session = requests.post(
            f"{DRIVE_UPLOAD_API}/files",
            headers={
                "Authorization": f"Bearer {self.token_store.access_token()}",
                "Content-Type": "application/json; charset=UTF-8",
                "X-Upload-Content-Type": mime_type,
                "X-Upload-Content-Length": str(path.stat().st_size),
            },
            params={"uploadType": "resumable", "fields": "id,name,webViewLink"},
            json=metadata,
            timeout=120,
        )
        if session.status_code != 200:
            raise DriveApiError(
                f"Falha ao iniciar upload de {path.name}: "
                f"{session.status_code} {session.text}"
            )
        upload_url = session.headers["Location"]
        with path.open("rb") as handle:
            response = requests.put(
                upload_url,
                headers={"Content-Type": mime_type},
                data=handle,
                timeout=600,
            )
        if response.status_code not in (200, 201):
            raise DriveApiError(
                f"Falha no upload de {path.name}: "
                f"{response.status_code} {response.text}"
            )
        return response.json()

    def ensure_public(self, file_id: str) -> None:
        permissions = self.request(
            "GET",
            f"{DRIVE_API}/files/{file_id}/permissions",
            params={"fields": "permissions(id,type,role)"},
        ).get("permissions", [])
        if any(
            permission.get("type") == "anyone"
            and permission.get("role") in {"reader", "commenter", "writer"}
            for permission in permissions
        ):
            return
        self.request(
            "POST",
            f"{DRIVE_API}/files/{file_id}/permissions",
            expected=(200,),
            params={"sendNotificationEmail": "false", "fields": "id"},
            json={"type": "anyone", "role": "reader"},
        )

    def get_file(self, file_id: str) -> dict[str, Any]:
        return self.request(
            "GET",
            f"{DRIVE_API}/files/{file_id}",
            params={
                "fields": "id,name,webViewLink,webContentLink,size,md5Checksum"
            },
        )


def drive_query_value(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\\'")


def normalize_drive_path(drive_path: str) -> list[str]:
    parts = [part.strip() for part in drive_path.replace("\\", "/").split("/")]
    parts = [part for part in parts if part]
    if parts and parts[0].casefold() in {"meu drive", "my drive"}:
        parts = parts[1:]
    return parts


def extract_sigla(path: Path) -> str:
    return path.name.split("_", 1)[0].strip()


def inventory(input_dir: Path, limit: int | None) -> list[Path]:
    if not input_dir.exists():
        raise FileNotFoundError(f"Pasta de evidencias nao encontrada: {input_dir}")
    files = sorted([path for path in input_dir.iterdir() if path.is_file()])
    return files[:limit] if limit else files


def build_dry_run_rows(files: list[Path], drive_folder: str) -> list[dict[str, Any]]:
    return [
        {
            "Sigla": extract_sigla(path),
            "Arquivo": path.name,
            "Caminho local": str(path),
            "Tamanho (bytes)": path.stat().st_size,
            "Pasta Google Drive": drive_folder,
            "Google Drive folder id": "",
            "Google Drive file id": "",
            "Link de acesso": "",
            "Link de download": "",
            "Status": "dry_run",
            "Mensagem": "Simulacao: nenhum upload ou permissao foi executado.",
        }
        for path in files
    ]


def upload_files(
    client: DriveClient,
    files: list[Path],
    *,
    drive_folder: str,
    create_folders: bool,
    upload_duplicates: bool,
) -> list[dict[str, Any]]:
    folder_id = client.ensure_folder_path(drive_folder, create=create_folders)
    rows: list[dict[str, Any]] = []
    for index, path in enumerate(files, start=1):
        print(f"[{index}/{len(files)}] Processando {path.name}")
        row = {
            "Sigla": extract_sigla(path),
            "Arquivo": path.name,
            "Caminho local": str(path),
            "Tamanho (bytes)": path.stat().st_size,
            "Pasta Google Drive": drive_folder,
            "Google Drive folder id": folder_id,
            "Google Drive file id": "",
            "Link de acesso": "",
            "Link de download": "",
            "Status": "",
            "Mensagem": "",
        }
        try:
            existing = None if upload_duplicates else client.find_existing_file(path.name, folder_id)
            if existing:
                file_info = existing
                row["Status"] = "existing"
                row["Mensagem"] = "Arquivo ja existia na pasta; permissao publica verificada."
            else:
                file_info = client.upload_file(path, folder_id)
                row["Status"] = "uploaded"
                row["Mensagem"] = "Arquivo enviado e permissao publica aplicada."
            file_id = file_info["id"]
            client.ensure_public(file_id)
            file_info = client.get_file(file_id)
            row["Google Drive file id"] = file_id
            row["Link de acesso"] = file_info.get(
                "webViewLink", f"https://drive.google.com/file/d/{file_id}/view"
            )
            row["Link de download"] = file_info.get("webContentLink", "")
        except Exception as exc:  # noqa: BLE001
            row["Status"] = "error"
            row["Mensagem"] = str(exc)
        rows.append(row)
    return rows


def write_table(
    rows: list[dict[str, Any]],
    *,
    output_xlsx: Path | None,
    output_csv: Path | None,
) -> None:
    if output_xlsx:
        output_xlsx.parent.mkdir(parents=True, exist_ok=True)
        try:
            import pandas as pd

            pd.DataFrame(rows).to_excel(output_xlsx, index=False)
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(f"Falha ao gravar XLSX {output_xlsx}: {exc}") from exc
    if output_csv:
        output_csv.parent.mkdir(parents=True, exist_ok=True)
        with output_csv.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Faz upload das evidencias coletadas ao Google Drive, torna os "
            "arquivos publicos e registra os links individuais em tabela."
        )
    )
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT_DIR)
    parser.add_argument("--drive-folder", default=DEFAULT_DRIVE_FOLDER)
    parser.add_argument("--client-secrets", type=Path)
    parser.add_argument("--token-path", type=Path, default=DEFAULT_TOKEN_PATH)
    parser.add_argument("--output-xlsx", type=Path, default=DEFAULT_OUTPUT_XLSX)
    parser.add_argument("--output-csv", type=Path, default=DEFAULT_OUTPUT_CSV)
    parser.add_argument("--oauth-port", type=int, default=8765)
    parser.add_argument(
        "--scope",
        default=DEFAULT_DRIVE_SCOPE,
        help=(
            "Escopo OAuth do Google Drive. Use o padrao para acessar uma pasta "
            "existente; como alternativa de menor permissao, teste "
            "https://www.googleapis.com/auth/drive.file."
        ),
    )
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--no-create-folders",
        action="store_true",
        help="Falha se a pasta de destino nao existir, em vez de cria-la.",
    )
    parser.add_argument(
        "--upload-duplicates",
        action="store_true",
        help="Envia nova copia mesmo quando ja existe arquivo com o mesmo nome.",
    )
    parser.add_argument("--limit", type=int, help="Limita a quantidade de arquivos.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    files = inventory(args.input_dir, args.limit)
    if not files:
        print(f"Nenhum arquivo encontrado em {args.input_dir}", file=sys.stderr)
        return 1

    if args.dry_run:
        rows = build_dry_run_rows(files, args.drive_folder)
    else:
        if not args.client_secrets:
            print(
                "Informe --client-secrets com o JSON OAuth 2.0 Client ID "
                "do tipo Desktop app.",
                file=sys.stderr,
            )
            return 2
        client = load_oauth_client(args.client_secrets)
        token_store = TokenStore(
            client,
            args.token_path,
            port=args.oauth_port,
            no_browser=args.no_browser,
            scope=args.scope,
        )
        drive = DriveClient(token_store)
        rows = upload_files(
            drive,
            files,
            drive_folder=args.drive_folder,
            create_folders=not args.no_create_folders,
            upload_duplicates=args.upload_duplicates,
        )

    output_xlsx = args.output_xlsx if args.output_xlsx else None
    output_csv = args.output_csv if args.output_csv else None
    write_table(rows, output_xlsx=output_xlsx, output_csv=output_csv)
    if output_xlsx:
        print(f"Tabela XLSX: {output_xlsx}")
    if output_csv:
        print(f"Tabela CSV: {output_csv}")
    errors = sum(1 for row in rows if row["Status"] == "error")
    print(f"Arquivos processados: {len(rows)}; erros: {errors}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
