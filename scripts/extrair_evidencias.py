import os
import zipfile
from pathlib import Path

# Resolve repo root relative to the script location
repo_root = Path(__file__).resolve().parent.parent

src_dir = repo_root / "02-Execucao" / "01-Questionario" / "Evidencias_Coletadas" / "evidencias"
dest_dir = Path("/tmp/tcerj-igovti-2026/evidencias_extraidas")

if not src_dir.exists():
    print(f"Diretório de origem de evidências não encontrado: {src_dir}")
    exit(1)

dest_dir.mkdir(parents=True, exist_ok=True)

zip_files = list(src_dir.glob("*.zip"))
print(f"Encontrados {len(zip_files)} arquivos ZIP para extrair...")

for idx, zip_path in enumerate(zip_files):
    # The prefix before the first '_' identifies the audited organization (e.g. FTM, ALERJ)
    auditado = zip_path.name.split("_")[0]
    auditado_dir = dest_dir / auditado
    auditado_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"[{idx+1}/{len(zip_files)}] Extraindo {zip_path.name} para {auditado_dir}...")
    try:
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(auditado_dir)
    except Exception as e:
        print(f"Erro ao extrair {zip_path.name}: {e}")

print("Extração concluída com sucesso!")
