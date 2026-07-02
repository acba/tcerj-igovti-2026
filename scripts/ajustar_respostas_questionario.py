#!/usr/bin/env python3
"""
Script para ajustar as respostas do questionário iGovTI-2026 com base nas
avaliações consolidadas / revisadas do painel de evidências.

Aplica as seguintes regras para itens com avaliação final "não conforme":
1. Itens de extensão / caixas de seleção (contêm 'ext' ou '['):
   - Se a resposta original for 'Y' ou 'y', remove o valor (célula vazia / NaN).
   - Se a resposta original for 'Sim', altera para 'Não'.
2. Itens base de adoção (formato qXXXX, ex: q1001):
   - Altera a resposta para 'Não adota.' (ou 'Não adota', mantendo o padrão de ponto final da coluna).
"""

import argparse
import sys
import re
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent / "resources"))

from xlsx_utils import dataframe_to_xlsx_se_diferente

NA_VALUES_PRESERVANDO_NA = [
    "",
    "#N/A",
    "#N/A N/A",
    "#NA",
    "-1.#IND",
    "-1.#QNAN",
    "-NaN",
    "-nan",
    "1.#IND",
    "1.#QNAN",
    "<NA>",
    "NA",
    "NULL",
    "NaN",
    "n/a",
    "nan",
    "null",
]


def read_excel_preservando_na(path: Path) -> pd.DataFrame:
    """Lê XLSX preservando o texto literal "N/A".

    No pandas, "N/A" faz parte da lista padrão de valores ausentes. Para as
    respostas LimeSurvey deste trabalho, porém, "N/A" tem significado
    substantivo: item não disponibilizado ao auditado. Por isso ele não pode
    ser convertido para NaN durante os ajustes.
    """
    return pd.read_excel(path, keep_default_na=False, na_values=NA_VALUES_PRESERVANDO_NA)


def normalize_text(val):
    if pd.isna(val):
        return ""
    # Transforma em minúsculas, remove espaços extras e acentos comuns
    s = str(val).strip().lower()
    s = s.replace("ã", "a").replace("õ", "o").replace("é", "e").replace("á", "a").replace("í", "i")
    return s

def is_nao_conforme(val):
    s = normalize_text(val)
    return s in ("nao conforme", "nao_conforme", "nao-conforme")

def get_nao_adota_value(df, col):
    # Verifica se algum valor não nulo na coluna termina com ponto final
    non_null_vals = df[col].dropna().astype(str)
    if non_null_vals.str.endswith(".").any():
        return "Não adota."
    return "Não adota"

def main():
    parser = argparse.ArgumentParser(
        description="Aplica ajustes de 'Não Conforme' na planilha de respostas do questionário."
    )
    parser.add_argument(
        "--respostas",
        type=Path,
        default=Path("02-Execucao/01-Questionario/03-Respostas_Processadas/20260621-respostas-questionario.xlsx"),
        help="Caminho da planilha de respostas original (XLSX)."
    )
    parser.add_argument(
        "--ajustes",
        type=Path,
        default=Path("ajustes_respostas_questionario_pos_avaliacao_evidencias.xlsx"),
        help="Caminho da planilha de ajustes exportada pelo painel (XLSX)."
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Caminho de saída do XLSX ajustado. Se omitido, usará o nome de --respostas com sufixo '_pos_ajustes_avaliacao_evidencias'."
    )

    args = parser.parse_args()

    # Validação dos arquivos de entrada
    for path_name, path in [("respostas", args.respostas), ("ajustes", args.ajustes)]:
        if not path.exists():
            print(f"Erro: O arquivo de {path_name} em '{path}' não existe.", file=sys.stderr)
            sys.exit(1)

    # Definir arquivo de saída
    if args.output:
        output_path = args.output
    else:
        suffix = "_pos_ajustes_avaliacao_evidencias"
        output_path = args.respostas.parent / f"{args.respostas.stem}{suffix}.xlsx"

    print(f"Lendo respostas de: {args.respostas}")
    df_respostas = read_excel_preservando_na(args.respostas)

    # Garantir que a coluna 'firstname' exista
    if "firstname" not in df_respostas.columns:
        print("Erro: A coluna 'firstname' (com o nome do auditado) não foi encontrada na planilha de respostas.", file=sys.stderr)
        sys.exit(1)

    print(f"Lendo ajustes de: {args.ajustes}")
    df_ajustes = read_excel_preservando_na(args.ajustes)

    # Ordenar por auditado e depois por item (ordem alfabética case-insensitive)
    col_item_ajustes = None
    if "Código do item" in df_ajustes.columns:
        col_item_ajustes = "Código do item"
    elif "Código do item avaliado" in df_ajustes.columns:
        col_item_ajustes = "Código do item avaliado"

    if col_item_ajustes and "Auditado" in df_ajustes.columns:
        df_ajustes["_sort_auditado"] = df_ajustes["Auditado"].fillna("").astype(str).str.upper()
        df_ajustes["_sort_item"] = df_ajustes[col_item_ajustes].fillna("").astype(str).str.upper()
        df_ajustes = df_ajustes.sort_values(by=["_sort_auditado", "_sort_item"]).drop(columns=["_sort_auditado", "_sort_item"])

    # Estatísticas e lista de mudanças
    total_lidos = len(df_ajustes)
    total_nao_conforme = 0
    total_ajustes_aplicados = 0
    orgaos_afetados = set()
    changes = []

    print("\nProcessando ajustes...")
    for idx, row in df_ajustes.iterrows():
        auditado = row.get("Auditado")
        
        # Suporte a "Código do item" ou "Código do item avaliado"
        item_codigo = row.get("Código do item")
        if pd.isna(item_codigo):
            item_codigo = row.get("Código do item avaliado")

        if pd.isna(auditado) or pd.isna(item_codigo):
            continue

        auditado = str(auditado).strip()
        item_codigo = str(item_codigo).strip()

        # Encontrar a linha correspondente do órgão comparando com a coluna 'firstname'
        rows_mask = df_respostas["firstname"].astype(str).str.strip().str.upper() == auditado.upper()
        if not rows_mask.any():
            print(f"Aviso: Órgão '{auditado}' não encontrado na coluna 'firstname' das respostas.")
            continue

        # Verificar se o item código está na planilha
        col_name = None
        if item_codigo in df_respostas.columns:
            col_name = item_codigo
        else:
            matching_cols = [c for c in df_respostas.columns if c.lower() == item_codigo.lower()]
            if matching_cols:
                col_name = matching_cols[0]

        has_resposta_ajustada = "Resposta ajustada" in df_ajustes.columns

        if has_resposta_ajustada:
            # Caso seja o ajuste inicial com valor pré-definido
            resposta_ajustada = row.get("Resposta ajustada")
            if pd.isna(resposta_ajustada) or str(resposta_ajustada).strip() == "" or str(resposta_ajustada).lower() in ("nan", "none", "vazio"):
                new_val = None
            else:
                new_val = resposta_ajustada

            justificativa_final = row.get("observacao")
            if pd.isna(justificativa_final):
                justificativa_final = row.get("Justificativa")

            # Mapeamento especial para itens base com colchetes no código do item (ex: q0104[D])
            if col_name is None:
                match = re.match(r"^q(\d{4})\[([A-Z])\]$", item_codigo, re.IGNORECASE)
                if match:
                    base_col = f"q{match.group(1)}"
                    opt_letter = match.group(2).lower()
                    if base_col in df_respostas.columns:
                        col_name = base_col
                        unique_opts = df_respostas[base_col].dropna().unique()
                        matched_opt = None
                        for opt in unique_opts:
                            opt_str = str(opt).strip().lower()
                            if opt_str.startswith(f"{opt_letter})") or opt_str.startswith(f"{opt_letter} "):
                                matched_opt = opt
                                break
                        if matched_opt:
                            new_val = matched_opt

            if col_name is None:
                print(f"Aviso: Coluna '{item_codigo}' não encontrada nas respostas para '{auditado}'.")
                continue

            old_val = df_respostas.loc[rows_mask, col_name].values[0]
            
            def values_equal(v1, v2):
                if pd.isna(v1) and pd.isna(v2):
                    return True
                return str(v1).strip() == str(v2).strip()

            if values_equal(old_val, new_val):
                mudado = False
            else:
                df_respostas.loc[rows_mask, col_name] = new_val
                mudado = True

        else:
            # Caso seja o fluxo normal de "Não Conforme" do painel de revisões
            if col_name is None:
                print(f"Aviso: Coluna '{item_codigo}' não encontrada nas respostas para '{auditado}'.")
                continue

            revisor_val = row.get("Avaliação do auditor revisor")
            juiz_val = row.get("Resultado da avaliação do juiz")

            # Determinar resultado final da avaliação (revisor prevalece sobre juiz)
            is_revisor = pd.notna(revisor_val) and str(revisor_val).strip() != "" and normalize_text(revisor_val) != "sem_parecer"
            
            if is_revisor:
                resultado_final = revisor_val
                justificativa_final = row.get("Justificativa do auditor revisor")
            else:
                resultado_final = juiz_val
                justificativa_final = row.get("Justificativa do juiz")

            if not is_nao_conforme(resultado_final):
                continue

            total_nao_conforme += 1
            old_val = df_respostas.loc[rows_mask, col_name].values[0]
            new_val = None
            mudado = False

            # 1. Regra para itens de extensão / caixas de seleção
            if "ext" in col_name.lower() or "[" in col_name:
                if pd.isna(old_val):
                    continue
                old_val_str = str(old_val).strip().lower()
                if old_val_str == "y":
                    new_val = None  # Remove valor (célula vazia)
                    df_respostas.loc[rows_mask, col_name] = new_val
                    mudado = True
                elif old_val_str == "sim":
                    new_val = "Não"
                    df_respostas.loc[rows_mask, col_name] = new_val
                    mudado = True

            # 2. Regra para itens base de adoção (ex: q1001, q2302)
            elif re.match(r"^q\d{4}$", col_name.lower()):
                if col_name.lower() == "q0101":
                    new_val = "F"
                elif col_name.lower() in ("q0102", "q0104"):
                    new_val = "E"
                else:
                    new_val = get_nao_adota_value(df_respostas, col_name)
                if str(old_val).strip().lower() != str(new_val).strip().lower():
                    df_respostas.loc[rows_mask, col_name] = new_val
                    mudado = True

        # Registrar a mudança se houve alteração de valor
        if mudado:
            total_ajustes_aplicados += 1
            orgaos_afetados.add(auditado)
            
            antes_str = "Vazio" if pd.isna(old_val) or str(old_val).strip() == "" else str(old_val)
            depois_str = "Vazio" if pd.isna(new_val) or str(new_val).strip() == "" else str(new_val)
            just_str = str(justificativa_final).strip() if pd.notna(justificativa_final) and str(justificativa_final).strip() != "" else "Sem justificativa registrada"
            
            changes.append({
                "auditado": auditado,
                "item": col_name,
                "antes": antes_str,
                "ajustado": depois_str,
                "justificativa": just_str
            })

    # Imprimir a tabela de alterações se houver mudanças
    if changes:
        try:
            from rich.console import Console
            from rich.table import Table
            from rich.box import ROUNDED

            console = Console()
            table = Table(
                title="[bold cyan]Alterações Realizadas nas Respostas[/bold cyan]",
                title_justify="left",
                box=ROUNDED,
                show_header=True,
                header_style="bold magenta"
            )
            table.add_column("Auditado", style="cyan", width=15)
            table.add_column("Item", style="yellow", width=15)
            table.add_column("Antes", style="green", width=20)
            table.add_column("Ajustado", style="red", width=20)
            table.add_column("Justificativa", style="white", max_width=100)

            for c in changes:
                antes_display = c["antes"]
                if len(antes_display) > 20:
                    antes_display = antes_display[:17] + "..."

                just_display = c["justificativa"].replace("\n", " ").replace("\r", " ").replace("  ", " ")
                if len(just_display) > 97:
                    just_display = just_display[:97] + "..."
                table.add_row(c["auditado"], c["item"], antes_display, c["ajustado"], just_display)

            console.print("\n")
            console.print(table)
        except ImportError:
            # Fallback clássico se rich não estiver instalado
            print("\nAlterações Realizadas:")
            print("=" * 168)
            print(f"{'Auditado':<15} | {'Item':<15} | {'Antes':<15} | {'Ajustado':<15} | {'Justificativa':<100}")
            print("-" * 168)
            for c in changes:
                if len(c["justificativa"]) > 97:
                    just_display = c["justificativa"][:97] + "..."
                else:
                    just_display = c["justificativa"]
                just_display = just_display.replace("\n", " ").replace("\r", " ").replace("  ", " ")
                print(f"{c['auditado']:<15} | {c['item']:<15} | {c['antes']:<15} | {c['ajustado']:<15} | {just_display:<100}")
            print("=" * 168)
    else:
        print("\nNenhuma alteração foi realizada nas respostas.")

    # Salvar resultado final
    print(f"\nSalvando resultado ajustado em: {output_path}")
    dataframe_to_xlsx_se_diferente(df_respostas, output_path, index=False)

    print("\n--- Resumo de Execução ---")
    print(f"Total de itens avaliados no arquivo de ajustes: {total_lidos}")
    print(f"Total de itens identificados como 'Não Conforme': {total_nao_conforme}")
    print(f"Total de células ajustadas com sucesso: {total_ajustes_aplicados}")
    print(f"Total de órgãos impactados: {len(orgaos_afetados)} ({', '.join(sorted(orgaos_afetados)) if orgaos_afetados else 'Nenhum'})")
    print("--------------------------")

if __name__ == "__main__":
    main()
