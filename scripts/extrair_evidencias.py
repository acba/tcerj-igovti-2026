import os
import re
import zipfile
from pathlib import Path, PurePosixPath

repo_root = Path(__file__).resolve().parent.parent
DEFAULT_SRC_DIR = (
    repo_root
    / "02-Execucao"
    / "01-Questionario"
    / "01-Coleta_LimeSurvey"
    / "Evidencias_Coletadas"
    / "evidencias"
)
DEFAULT_DEST_DIR = DEFAULT_SRC_DIR.parent / "evidencias_extraidas"

# Caracteres inválidos em nomes de arquivo Windows
_INVALID_CHARS = re.compile(r'[<>:"|?*\x00-\x1f]')
_MAX_NAME_LEN = 200  # limite conservador para evitar MAX_PATH


def sanitize_filename(name: str) -> str:
    """Normaliza o nome de arquivo para ser válido no Windows e no Python."""
    # Substitui separadores POSIX/Windows por underscore (evita subdiretórios inesperados)
    name = name.replace("/", "_").replace("\\", "_")
    # Remove caracteres de controle e inválidos
    name = _INVALID_CHARS.sub("_", name)
    # Remove espaços no início/fim e pontos no fim
    name = name.strip(" .")
    if not name:
        name = "arquivo"
    return name


def split_name(name: str) -> tuple[str, str]:
    """Separa o nome base da extensão final (após o último ponto)."""
    if "." in name[1:]:  # ignora ponto inicial
        idx = name.rfind(".")
        return name[:idx], name[idx:]
    return name, ""


def extract_zip(zip_path: Path, target_dir: Path) -> None:
    """Extrai o ZIP sanitizando nomes e limitando tamanho dos arquivos."""
    with zipfile.ZipFile(zip_path, "r") as z:
        for info in z.infolist():
            if info.is_dir():
                continue

            # Tenta decodificar o nome do arquivo dentro do ZIP
            raw_name = info.filename
            decoded_name = raw_name
            for enc in ("utf-8", "cp437", "cp1252", "latin-1"):
                try:
                    if isinstance(raw_name, bytes):
                        decoded_name = raw_name.decode(enc)
                    else:
                        decoded_name = raw_name.encode("cp437").decode(enc)
                    break
                except (UnicodeDecodeError, UnicodeEncodeError):
                    continue

            # Sanitiza o nome final
            safe_name = sanitize_filename(decoded_name)

            # Limita o tamanho do nome preservando apenas a extensão final
            stem, suffix = split_name(safe_name)
            suffix = suffix.lower()
            if len(stem) + len(suffix) > _MAX_NAME_LEN:
                stem = stem[: _MAX_NAME_LEN - len(suffix)]
            safe_name = stem + suffix

            dest_path = target_dir / safe_name
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            with z.open(info) as src, open(dest_path, "wb") as dst:
                dst.write(src.read())


def main(argv: list[str] | None = None) -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Extrai os ZIPs de evidências do LimeSurvey em uma pasta por auditado."
    )
    parser.add_argument(
        "--input-dir",
        "-i",
        type=Path,
        default=DEFAULT_SRC_DIR,
        help=f"Diretório com os ZIPs baixados (padrão: {DEFAULT_SRC_DIR}).",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        type=Path,
        default=DEFAULT_DEST_DIR,
        help=f"Diretório para as evidências extraídas (padrão: {DEFAULT_DEST_DIR}).",
    )
    args = parser.parse_args(argv)

    src_dir = args.input_dir
    dest_dir = args.output_dir
    if not src_dir.is_dir():
        parser.error(f"diretório de origem de evidências não encontrado: {src_dir}")

    dest_dir.mkdir(parents=True, exist_ok=True)
    zip_files = sorted(src_dir.glob("*.zip"))
    print(f"Encontrados {len(zip_files)} arquivos ZIP para extrair...")

    erros = 0
    for idx, zip_path in enumerate(zip_files):
        # O prefixo anterior ao primeiro '_' identifica o auditado.
        auditado = zip_path.name.split("_")[0]
        auditado_dir = dest_dir / auditado
        auditado_dir.mkdir(parents=True, exist_ok=True)

        print(f"[{idx + 1}/{len(zip_files)}] Extraindo {zip_path.name} para {auditado_dir}...")
        try:
            extract_zip(zip_path, auditado_dir)
        except Exception as exc:
            erros += 1
            print(f"Erro ao extrair {zip_path.name}: {exc}")

    if erros:
        raise SystemExit(f"Extração concluída com erro em {erros} arquivo(s).")
    print("Extração concluída com sucesso!")


if __name__ == "__main__":
    main()
