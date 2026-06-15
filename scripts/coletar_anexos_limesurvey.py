from pathlib import Path
from urllib.parse import urljoin
import re
import requests
import pandas as pd

repo_root = Path(__file__).resolve().parent.parent
PLANILHA = repo_root / "02-Execucao/01-Questionario/Evidencias_Coletadas/urls_anexos_limesurvey_consolidado.xlsx"
PASTA_RAIZ = repo_root / "02-Execucao/01-Questionario/Evidencias_Coletadas/evidencias"

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
}

COOKIES = {
    "cookieconsent_status": "allow",
    "PHPSESSID": "jkvnhn5e3uge0ficdakbimh2g8",
    "YII_CSRF_TOKEN": "bTdPdXhRdTNRa2Z5R0hmQnRHczBwOEcwM3ZoRjN4V3HWX2dIjdVvEm08dsQMiwao4xz6iKJ5ti8UPSXgOG1DxQ==",
}

def limpar_texto(texto: str) -> str:
    texto = "" if pd.isna(texto) else str(texto).strip()
    texto = re.sub(r'[\\/:*?"<>|]', "_", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto or "SEM_VALOR"

def limpar_datestamp(datestamp: str) -> str:
    datestamp = "" if pd.isna(datestamp) else str(datestamp).strip()
    datestamp = datestamp.replace(".", "-")
    datestamp = datestamp.replace(":", "")
    datestamp = re.sub(r"\s+", "_", datestamp)
    datestamp = re.sub(r'[\\/:*?"<>|]', "_", datestamp)
    return datestamp or "SEM_DATA"

def nome_destino(orgao, datestamp, id_resposta) -> Path:
    orgao_limpo = limpar_texto(orgao)
    data_limpa = limpar_datestamp(datestamp)
    id_limpo = limpar_texto(id_resposta)

    return PASTA_RAIZ / f"{orgao_limpo}_{data_limpa}_id{id_limpo}.zip"

def baixar_arquivo(session, url, destino):
    with session.get(url, stream=True, timeout=180, allow_redirects=True) as resp:
        resp.raise_for_status()

        content_type = resp.headers.get("Content-Type", "").lower()

        if "text/html" in content_type:
            texto = resp.text[:5000].lower()

            if "login" in texto or "username" in texto or "password" in texto:
                raise RuntimeError("Sessão expirada. Atualize PHPSESSID/YII_CSRF_TOKEN.")

            raise RuntimeError("Resposta HTML recebida em vez de arquivo ZIP.")

        with open(destino, "wb") as f:
            for chunk in resp.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

def main():
    PASTA_RAIZ.mkdir(exist_ok=True)

    df = pd.read_excel(PLANILHA)

    colunas_obrigatorias = {"id", "orgao", "datestamp", "url"}
    faltantes = colunas_obrigatorias - set(df.columns)

    if faltantes:
        raise ValueError(f"Colunas ausentes na planilha: {faltantes}")

    session = requests.Session()
    session.headers.update(HEADERS)
    session.cookies.update(COOKIES)

    total = len(df)

    for i, row in df.iterrows():
        id_resposta = row["id"]
        orgao = row["orgao"]
        datestamp = row["datestamp"]
        url = str(row["url"]).strip()

        destino = nome_destino(orgao, datestamp, id_resposta)

        print(f"[{i + 1}/{total}] {orgao} -> {destino.name}")

        if destino.exists() and destino.stat().st_size > 0:
            print("  PULANDO -> arquivo já existe")
            continue

        try:
            baixar_arquivo(session, url, destino)
            print("  OK")

        except Exception as e:
            print(f"  ERRO -> {e}")

    print("\nConcluído.")

if __name__ == "__main__":
    main()