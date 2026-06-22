"""Migra um checkpoint analyses_*.jsonl para um novo provider/model.

Re-resolve cada evidencia e prompt para obter ``hash_conteudo`` e ``prompt_hash``
corretos, recalcula o ``identity`` com o novo provider/model e os parametros que
o pipeline usara em runtime (prompt_version, reasoning_effort,
evidence_processing_mode), e grava um novo checkpoint. Assim o pipeline
reconhece os registros ``completed`` (skip por dedup) e reprocessa apenas os
``error``.

IMPORTANTE: passe os mesmos parametros que o pipeline usara em runtime
(--prompt-version, --reasoning, --pdf2md, --docx2html). Se os valores diferirem,
o ``identity`` calculado pelo pipeline nao batera com o migrado, e tudo sera
reprocessado do zero.

Uso:
    scripts/.venv/bin/python scripts/migrar_checkpoint_provider.py \
        --input 02-Execucao/03-Execucao_Procedimentos/avaliacao_evidencias/analyses_openai_gpt-5.4-mini.jsonl \
        --evidencias 02-Execucao/01-Questionario/Evidencias_Coletadas/evidencias_extraidas \
        --prompts-dir scripts/avaliacao_evidencias/prompts/igovti_2026_achados_binario_v1 \
        --new-provider openrouter \
        --new-model openai/gpt-5.4-mini \
        --prompt-version igovti_2026_achados_binario_v1 \
        --reasoning high
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.avaliacao_evidencias.pipeline import (
    calcular_identidade_analise,
    hash_arquivo,
    nome_checkpoint_padrao,
    resolver_evidencia,
    resolver_prompt,
)


def migrar(
    input_path: Path,
    evidencias_root: str | Path,
    prompts_dir: str | Path,
    new_provider: str,
    new_model: str,
    prompt_version: str,
    reasoning_effort: str,
    evidence_processing_mode: str,
    output_path: Path | None,
) -> Path:
    if not input_path.is_file():
        raise FileNotFoundError(f"checkpoint nao encontrado: {input_path}")

    if output_path is None:
        output_path = input_path.parent / nome_checkpoint_padrao(new_provider, new_model)

    total = completed = errors = 0
    nao_resolvidos = 0
    with input_path.open(encoding="utf-8") as f_in, output_path.open("w", encoding="utf-8") as f_out:
        for linha in f_in:
            if not linha.strip():
                continue
            total += 1
            registro = json.loads(linha)
            old_provider = registro.get("provider", "")
            old_model = registro.get("model", "")
            nome_evidencia = registro.get("evidencia", "")

            # Re-resolve evidence file
            hash_conteudo = ""
            if nome_evidencia:
                upload = {"name": nome_evidencia}
                resolucao = resolver_evidencia(
                    registro.get("auditado", ""),
                    evidencias_root,
                    upload,
                )
                if resolucao.caminho and not resolucao.erro:
                    hash_conteudo = hash_arquivo(resolucao.caminho)
                else:
                    nao_resolvidos += 1

            # Re-resolve prompt
            prompt = resolver_prompt(prompts_dir, registro.get("coluna_evidencia", ""))
            prompt_hash = prompt.hash_conteudo

            novo_identity = calcular_identidade_analise(
                auditado=registro.get("auditado", ""),
                coluna_evidencia=registro.get("coluna_evidencia", ""),
                nome_original_evidencia=nome_evidencia,
                hash_conteudo=hash_conteudo,
                provider=new_provider,
                model=new_model,
                prompt_hash=prompt_hash,
                prompt_version=prompt_version,
                reasoning_effort=reasoning_effort,
                evidence_processing_mode=evidence_processing_mode,
            )

            registro["provider"] = new_provider
            registro["model"] = new_model
            registro["identity"] = novo_identity
            registro["prompt_version"] = prompt_version
            registro["reasoning_effort"] = reasoning_effort
            registro["evidence_processing_mode"] = evidence_processing_mode

            if registro.get("status") == "completed":
                completed += 1
            else:
                errors += 1

            f_out.write(json.dumps(registro, ensure_ascii=False) + "\n")

    print(f"Migracao: {input_path.name} -> {output_path.name}")
    print(f"  provider: {old_provider} -> {new_provider}")
    print(f"  model:    {old_model} -> {new_model}")
    print(f"  prompt_version: {prompt_version!r}")
    print(f"  reasoning_effort: {reasoning_effort!r}")
    print(f"  evidence_processing_mode: {evidence_processing_mode!r}")
    print(f"  total: {total} | completed (preservados): {completed} | error (serao reprocessados): {errors}")
    if nao_resolvidos:
        print(f"  evidencias nao resolvidas: {nao_resolvidos} (serao reprocessadas)")
    return output_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Migra checkpoint analyses para novo provider/model.")
    parser.add_argument("--input", required=True, help="Caminho do analyses_*.jsonl original.")
    parser.add_argument("--evidencias", required=True, help="Raiz das evidencias extraidas.")
    parser.add_argument("--prompts-dir", required=True, help="Diretorio de prompts.")
    parser.add_argument("--new-provider", required=True, help="Novo provider (ex: openrouter).")
    parser.add_argument("--new-model", required=True, help="Novo model (ex: openai/gpt-5.4-mini).")
    parser.add_argument(
        "--prompt-version",
        default="igovti_2026_achados_binario_v1",
        help="Versao do prompt que o pipeline usara em runtime (deve bater com --prompt-version do shell script).",
    )
    parser.add_argument(
        "--reasoning",
        default="high",
        help="Nivel de reasoning que o pipeline usara (ex: high).",
    )
    parser.add_argument(
        "--pdf2md",
        action="store_true",
        help="Define evidence_processing_mode=pdf2md (deve bater com a flag do pipeline).",
    )
    parser.add_argument(
        "--docx2html",
        action="store_true",
        help="Define evidence_processing_mode com docx2html (deve bater com a flag do pipeline).",
    )
    parser.add_argument("--output", default=None, help="Caminho de saida (padrao: analyses_<provider>_<model>.jsonl no mesmo dir).")
    args = parser.parse_args(argv)

    modos = []
    if args.pdf2md:
        modos.append("pdf2md")
    if args.docx2html:
        modos.append("docx2html")
    evidence_processing_mode = "+".join(modos)

    output = migrar(
        Path(args.input),
        args.evidencias,
        args.prompts_dir,
        args.new_provider,
        args.new_model,
        args.prompt_version,
        args.reasoning,
        evidence_processing_mode,
        Path(args.output) if args.output else None,
    )
    print(f"\nCheckpoint migrado: {output}")
    print(f"\nProximo passo:")
    print(f"  Rodar o pipeline com os MESMOS parametros:")
    print(f"    --prompt-version {args.prompt_version}")
    print(f"    --reasoning {args.reasoning}")
    if args.pdf2md:
        print(f"    --pdf2md")
    if args.docx2html:
        print(f"    --docx2html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
