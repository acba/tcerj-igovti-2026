#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# CONFIGURAÇÃO
###############################################################################

OPENROUTER_API_KEY="${OPENROUTER_API_KEY:-}"
GEMINI_API_KEY="${GEMINI_API_KEY:-}"

BASE_OUT="02-Execucao/03-Execucao_Procedimentos/avaliacao_evidencias"

###############################################################################
# FUNÇÕES
###############################################################################

run_gemini() {
    local MODEL="$1"

    echo "[$(date '+%F %T')] Iniciando Gemini: $MODEL"

    GEMINI_API_KEY="$GEMINI_API_KEY" \
    scripts/.venv/bin/python -m scripts.avaliacao_evidencias_refatorado.consolidacao \
        $BASE_OUT/analyses_clean*.jsonl \
        --evidencias-root 02-Execucao/01-Questionario/Evidencias_Coletadas/evidencias_extraidas \
        --judge-provider gemini \
        --judge-model "$MODEL" \
        --out-dir "$BASE_OUT"/consolidado

    PIDS+=($!)
    NAMES+=("gemini:$MODEL")
}

###############################################################################
# EXECUÇÕES
###############################################################################

declare -a PIDS=()
declare -a NAMES=()

# run_opencodego "minimax-m3"

# OpenRouter
# run_openrouter "openai/gpt-5.4-mini"

# Gemini
run_gemini "gemini-3.1-flash-lite"

###############################################################################
# AGUARDA E VERIFICA RESULTADOS
###############################################################################

echo
echo "Aguardando ${#PIDS[@]} processos..."
echo

FAIL=0

for i in "${!PIDS[@]}"; do
    PID="${PIDS[$i]}"
    NAME="${NAMES[$i]}"

    if wait "$PID"; then
        echo "✅ SUCESSO: $NAME"
    else
        echo "❌ FALHA:   $NAME"
        FAIL=1
    fi
done

echo

if [ "$FAIL" -eq 0 ]; then
    echo "Todos os processos finalizaram com sucesso."
else
    echo "Um ou mais processos falharam."
    exit 1
fi