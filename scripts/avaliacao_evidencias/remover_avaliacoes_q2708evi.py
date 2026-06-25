#!/usr/bin/env python3
import os
import json
import shutil
import pandas as pd
from pathlib import Path

def main():
    respostas_bruto_path = Path("02-Execucao/01-Questionario/20260621-respostas-questionario-bruto.xlsx")
    evidencias_dir = Path("02-Execucao/03-Execucao_Procedimentos/avaliacao_evidencias")

    if not respostas_bruto_path.exists():
        print(f"Erro: Planilha bruta não encontrada em '{respostas_bruto_path}'")
        return

    # 1. Identificar dinamicamente os auditados que responderam "Não" a todas as opções da q2708
    print(f"Lendo respostas brutas de: {respostas_bruto_path}")
    df_bruto = pd.read_excel(respostas_bruto_path)
    mask_q2708 = (
        (df_bruto["q2708[A]"] == "Não") &
        (df_bruto["q2708[B]"] == "Não") &
        (df_bruto["q2708[C]"] == "Não") &
        (df_bruto["q2708[D]"] == "Não")
    )
    auditados_alvo = set(df_bruto.loc[mask_q2708, "firstname"].astype(str).str.strip().str.upper())
    print(f"Total de {len(auditados_alvo)} auditados identificados para remoção: {sorted(list(auditados_alvo))}")

    # 2. Localizar arquivos .jsonl recursivamente no diretório de avaliação de evidências
    if not evidencias_dir.exists():
        print(f"Erro: Diretório de avaliações não existe em '{evidencias_dir}'")
        return

    jsonl_files = list(evidencias_dir.glob("**/*.jsonl"))
    print(f"Encontrados {len(jsonl_files)} arquivos .jsonl para verificação.")

    total_removido_geral = 0

    for jsonl_path in jsonl_files:
        linhas_mantidas = []
        linhas_removidas = 0

        # Ler o arquivo JSONL linha por linha
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                line_stripped = line.strip()
                if not line_stripped:
                    continue
                try:
                    record = json.loads(line_stripped)
                    auditado = str(record.get("auditado", "")).strip().upper()
                    col_evidencia = str(record.get("coluna_evidencia", "")).strip().lower()

                    # Condição de remoção:
                    # - coluna_evidencia == "q2708evi"
                    # - auditado é um dos 27 identificados
                    if col_evidencia == "q2708evi" and auditado in auditados_alvo:
                        linhas_removidas += 1
                    else:
                        linhas_mantidas.append(line_stripped)
                except Exception as e:
                    # Em caso de erro de parsing, mantém a linha intacta por segurança
                    linhas_mantidas.append(line_stripped)

        # Se houver linhas removidas, gera o backup .bak e sobrescreve o arquivo com segurança
        if linhas_removidas > 0:
            backup_path = jsonl_path.with_name(jsonl_path.name + ".bak")
            print(f"Criando backup em: '{backup_path}'")
            try:
                shutil.copy2(jsonl_path, backup_path)
            except Exception as e:
                print(f"Aviso: Não foi possível criar backup para '{jsonl_path}': {e}. Prosseguindo...")

            print(f"Removendo {linhas_removidas} registros de '{jsonl_path}'...")
            
            # Escrever em um arquivo temporário primeiro e depois substituir
            temp_path = jsonl_path.with_suffix(".tmp")
            with open(temp_path, "w", encoding="utf-8") as f_out:
                for line in linhas_mantidas:
                    f_out.write(line + "\n")
            
            os.replace(temp_path, jsonl_path)
            total_removido_geral += linhas_removidas

    print("\n--- Resumo de Remoção ---")
    print(f"Total de registros removidos em todos os arquivos .jsonl: {total_removido_geral}")
    print("-------------------------")

if __name__ == "__main__":
    main()
