#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."

if [[ -z "${OPENROUTER_API_KEY:-}" ]]; then
  echo "Erro: defina OPENROUTER_API_KEY antes de executar." >&2
  exit 1
fi

RPM="${RPM:-12}"
MODEL="${MODEL:-openai/gpt-5.4}"
REASONING="${REASONING:-medium}"
OUT_DIR="${OUT_DIR:-02-Execucao/03-Execucao_Procedimentos/avaliacao_evidencias/achados_binario_openrouter_gpt-5.4}"

args=(
  02-Execucao/01-Questionario/20260611-respostas-questionario.xlsx
  02-Execucao/01-Questionario/Evidencias_Coletadas/evidencias_extraidas
  --questionario 01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md
  --prompts-dir scripts/avaliacao_evidencias/prompts/igovti_2026_achados_binario_v1
  --prompt-version igovti_2026_achados_binario_v1
  --only-prompts-present
  --provider openrouter
  --model "$MODEL"
  --rpm "$RPM"
  --out-dir "$OUT_DIR"
)

if [[ -n "$REASONING" ]]; then
  args+=(--reasoning "$REASONING")
fi

scripts/.venv/bin/python -m scripts.avaliacao_evidencias "${args[@]}"
