from pathlib import Path
from urllib.parse import urljoin
import re
import requests
import pandas as pd

repo_root = Path(__file__).resolve().parent.parent

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
    "PHPSESSID": "b6clbglald2dru1r8dht1f52aq",
    "YII_CSRF_TOKEN": "WnRyaVhVbGhwOWZSVXp4cFY5aTM4RkhNNGc4akhsbXil6seQmZe43CRbHR39XHzh9Ju-k-_Kbt-FPdvF1bG30A%3D%3D",
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

def nome_destino(orgao, datestamp, id_resposta, pasta_raiz: Path) -> Path:
    orgao_limpo = limpar_texto(orgao)
    data_limpa = limpar_datestamp(datestamp)
    id_limpo = limpar_texto(id_resposta)

    return pasta_raiz / f"{orgao_limpo}_{data_limpa}_id{id_limpo}.zip"

def baixar_arquivo(session, url, destino):
    with session.get(url, stream=True, timeout=180, allow_redirects=True) as resp:
        resp.raise_for_status()

        content_type = resp.headers.get("Content-Type", "").lower()

        if "text/html" in content_type:
            # Pegamos o texto completo para buscar indicadores de expiração de sessão
            texto = resp.text.lower()

            if "login" in texto or "username" in texto or "password" in texto or "loginform" in texto:
                raise RuntimeError("Sessão expirada (LimeSurvey redirecionou para tela de login). Atualize PHPSESSID/YII_CSRF_TOKEN no script.")

            # Tenta capturar o título da página HTML para melhor debug
            title_match = re.search(r"<title>(.*?)</title>", resp.text, re.IGNORECASE | re.DOTALL)
            title = title_match.group(1).strip() if title_match else "Sem título"
            snippet = resp.text[:150].replace('\n', ' ').strip()
            raise RuntimeError(
                f"Resposta HTML recebida (HTTP {resp.status_code}, Content-Type: '{content_type}'). "
                f"Título: '{title}'. Início: '{snippet}...'"
            )

        with open(destino, "wb") as f:
            for chunk in resp.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

def main(argv: list[str] | None = None):
    import argparse
    
    parser = argparse.ArgumentParser(description="Baixa anexos de evidencias do LimeSurvey.")
    parser.add_argument(
        "--planilha", "-p",
        default=str(repo_root / "02-Execucao/01-Questionario/Evidencias_Coletadas/urls_anexos_limesurvey_consolidado.xlsx"),
        help="Caminho da planilha Excel de entrada com as URLs."
    )
    parser.add_argument(
        "--output-dir", "-o",
        default=str(repo_root / "02-Execucao/01-Questionario/Evidencias_Coletadas/evidencias"),
        help="Diretorio de destino para os downloads."
    )
    args = parser.parse_args(argv)

    planilha_path = Path(args.planilha)
    pasta_destino = Path(args.output_dir)
    pasta_destino.mkdir(parents=True, exist_ok=True)

    df = pd.read_excel(planilha_path)

    colunas_obrigatorias = {"id", "orgao", "datestamp", "url", "completed"}
    faltantes = colunas_obrigatorias - set(df.columns)

    if faltantes:
        raise ValueError(f"Colunas ausentes na planilha: {faltantes}")

    # Identificar o envio mais recente de cada órgão
    df["parsed_date"] = pd.to_datetime(df["datestamp"], format="%d.%m.%Y %H:%M:%S", errors="coerce")
    latest_idx_by_orgao = df.groupby("orgao")["parsed_date"].idxmax()
    latest_indices_set = set(latest_idx_by_orgao.values)

    session = requests.Session()
    session.headers.update(HEADERS)
    session.cookies.update(COOKIES)

    total = len(df)

    for i, row in df.iterrows():
        id_resposta = row["id"]
        orgao = row["orgao"]
        datestamp = row["datestamp"]
        completed = str(row["completed"]).strip().lower()
        url = str(row["url"]).strip()

        destino = nome_destino(orgao, datestamp, id_resposta, pasta_destino)

        print(f"[{i + 1}/{total}] {orgao} -> {destino.name}")

        # 1. Verificar se é o envio mais recente do órgão
        if i not in latest_indices_set:
            latest_idx = latest_idx_by_orgao[orgao]
            latest_row = df.loc[latest_idx]
            print(f"  PULANDO -> há um envio mais recente em {latest_row['datestamp']} (ID {latest_row['id']})")
            continue

        # 2. Verificar se o questionário está concluído
        if completed != "sim":
            print(f"  PULANDO -> questionário não concluído (completed = '{row['completed']}')")
            continue

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