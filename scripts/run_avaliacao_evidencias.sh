#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# CONFIGURAÇÃO
###############################################################################

OPENROUTER_API_KEY="${OPENROUTER_API_KEY:-}"
GEMINI_API_KEY="${GEMINI_API_KEY:-}"

BASE_OUT="02-Execucao/03-Execucao_Procedimentos/avaliacao_evidencias"

# Auditados específicos a serem avaliados (reprocessados/novos).
# O pipeline filtra pelo firstname do auditado; nomes com espaços são suportados.
# Lista de auditados separada por vírgula (suporta nomes com espaços).
AUDITADOS="RIO DAS OSTRAS" #,FS,MPERJ,PGE,PRODERJ,QUEIMADOS,SEDEC"

###############################################################################
# FUNÇÕES
###############################################################################

run_openrouter_com_preprocessamento() {
    local MODEL="$1"

    echo "[$(date '+%F %T')] Iniciando OpenRouter: $MODEL"

    OPENROUTER_API_KEY="$OPENROUTER_API_KEY" \
    scripts/.venv/bin/python -m scripts.avaliacao_evidencias \
        02-Execucao/01-Questionario/20260621-respostas-questionario.xlsx \
        02-Execucao/01-Questionario/Evidencias_Coletadas/evidencias_extraidas \
        --questionario 01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md \
        --prompts-dir scripts/avaliacao_evidencias/prompts/igovti_2026_achados_binario_v1 \
        --prompt-version igovti_2026_achados_binario_v1 \
        --catalog scripts/avaliacao_evidencias/prompt_catalogs/igovti_2026_achados_binario_v1.yml \
        --only-prompts-present \
        --only-achados \
        --provider openrouter \
        --model "$MODEL" \
        --reasoning high \
        --pdf2md \
        --docx2html \
        --auditados "$AUDITADOS" \
        --out-dir "$BASE_OUT" &

    PIDS+=($!)
    NAMES+=("openrouter:$MODEL")
}

run_openrouter() {
    local MODEL="$1"

    echo "[$(date '+%F %T')] Iniciando OpenRouter: $MODEL"

    OPENROUTER_API_KEY="$OPENROUTER_API_KEY" \
    scripts/.venv/bin/python -m scripts.avaliacao_evidencias \
        02-Execucao/01-Questionario/20260621-respostas-questionario.xlsx \
        02-Execucao/01-Questionario/Evidencias_Coletadas/evidencias_extraidas \
        --questionario 01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md \
        --prompts-dir scripts/avaliacao_evidencias/prompts/igovti_2026_achados_binario_v1 \
        --prompt-version igovti_2026_achados_binario_v1 \
        --catalog scripts/avaliacao_evidencias/prompt_catalogs/igovti_2026_achados_binario_v1.yml \
        --only-prompts-present \
        --only-achados \
        --provider openrouter \
        --model "$MODEL" \
        --reasoning high \
        --auditados "$AUDITADOS" \
        --out-dir "$BASE_OUT" &

    PIDS+=($!)
    NAMES+=("openrouter:$MODEL")
}

run_opencodego() {
    local MODEL="$1"

    echo "[$(date '+%F %T')] Iniciando OpenCode Go: $MODEL"

    OPENROUTER_API_KEY="$OPENROUTER_API_KEY" \
    scripts/.venv/bin/python -m scripts.avaliacao_evidencias \
        02-Execucao/01-Questionario/20260621-respostas-questionario.xlsx \
        02-Execucao/01-Questionario/Evidencias_Coletadas/evidencias_extraidas \
        --questionario 01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md \
        --prompts-dir scripts/avaliacao_evidencias/prompts/igovti_2026_achados_binario_v1 \
        --prompt-version igovti_2026_achados_binario_v1 \
        --catalog scripts/avaliacao_evidencias/prompt_catalogs/igovti_2026_achados_binario_v1.yml \
        --only-prompts-present \
        --only-achados \
        --provider opencodego \
        --model "$MODEL" \
        --pdf2md \
        --docx2html \
        --reasoning high \
        --auditados "$AUDITADOS" \
        --out-dir "$BASE_OUT" &

    PIDS+=($!)
    NAMES+=("openrouter:$MODEL")
}

run_gemini() {
    local MODEL="$1"

    echo "[$(date '+%F %T')] Iniciando Gemini: $MODEL"

    GEMINI_API_KEY="$GEMINI_API_KEY" \
    scripts/.venv/bin/python -m scripts.avaliacao_evidencias \
        02-Execucao/01-Questionario/20260621-respostas-questionario.xlsx \
        02-Execucao/01-Questionario/Evidencias_Coletadas/evidencias_extraidas \
        --questionario 01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md \
        --prompts-dir scripts/avaliacao_evidencias/prompts/igovti_2026_achados_binario_v1 \
        --prompt-version igovti_2026_achados_binario_v1 \
        --catalog scripts/avaliacao_evidencias/prompt_catalogs/igovti_2026_achados_binario_v1.yml \
        --only-prompts-present \
        --only-achados \
        --provider gemini \
        --model "$MODEL" \
        --rpm 12 \
        --reasoning high \
        --auditados "$AUDITADOS" \
        --out-dir "$BASE_OUT" &

    PIDS+=($!)
    NAMES+=("gemini:$MODEL")
}

run_openai() {
    local MODEL="$1"

    echo "[$(date '+%F %T')] Iniciando OpenAI: $MODEL"

    GEMINI_API_KEY="$GEMINI_API_KEY" \
    scripts/.venv/bin/python -m scripts.avaliacao_evidencias \
        02-Execucao/01-Questionario/20260621-respostas-questionario.xlsx \
        02-Execucao/01-Questionario/Evidencias_Coletadas/evidencias_extraidas \
        --questionario 01-Planejamento/02-Metodologia_iGovTI/igovti_2026.md \
        --prompts-dir scripts/avaliacao_evidencias/prompts/igovti_2026_achados_binario_v1 \
        --prompt-version igovti_2026_achados_binario_v1 \
        --catalog scripts/avaliacao_evidencias/prompt_catalogs/igovti_2026_achados_binario_v1.yml \
        --only-prompts-present \
        --only-achados \
        --provider openai \
        --model "$MODEL" \
        --rpm 12 \
        --reasoning high \
        --auditados "$AUDITADOS" \
        --out-dir "$BASE_OUT" &

    PIDS+=($!)
    NAMES+=("gemini:$MODEL")
}

###############################################################################
# EXECUÇÕES
###############################################################################

declare -a PIDS=()
declare -a NAMES=()

run_opencodego "minimax-m3"
# run_openai "gpt-5.4-mini"

# OpenRouter
# run_openrouter_com_preprocessamento "minimax/minimax-m3"
# run_openrouter_com_preprocessamento "qwen/qwen3.7-plus"
# run_openrouter "openai/gpt-5.4-mini"
# run_openrouter "google/gemma-4-31b-it:free"
# run_openrouter "openai/gpt-5.4-nano"

# Gemini
run_gemini "gemini-3.1-flash-lite"
# run_gemini "gemma-4-31b-it"

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