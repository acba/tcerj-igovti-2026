#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import json
import argparse
import tempfile
from pathlib import Path
from typing import Any, List, Dict

# Ajustar PYTHONPATH para permitir imports da pasta raiz
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from scripts.avaliacao_evidencias.pipeline import normalizar_evidencia, arquivos_compativeis_upload, ItemAfirmado
except ImportError:
    from dataclasses import dataclass
    @dataclass(frozen=True)
    class ItemAfirmado:
        codigo: str
        texto: str
        afirmacao: str

from scripts.avaliacao_evidencias.providers_ai_service import executar_provider

# Provedores e modelos padrão para o benchmark
DEFAULT_MODELS = [
    ("gemini", "gemini-3.5-flash"),
    ("gemini", "gemini-3-flash-preview"),
    ("gemini", "gemini-3.1-flash-lite"),
    ("gemini", "gemma-4-26b-a4b-it"),
    ("opencodego", "minimax-m3"),
    ("opencodego", "kimi-k2.6"),
    ("opencodego", "mimo-v2.5-pro"),
    ("opencodego", "mimo-v2.5"),
    ("opencodego", "qwen3.7-max"),
    ("opencodego", "qwen3.7-plus"),
    ("opencodego", "deepssek-v4-pro"),
    ("opencodego", "deepssek-v4-flash"),
]


def benchmark_model(
    provider: str,
    model: str,
    prompt: str,
    itens: List[ItemAfirmado],
    caminho_evidencia: Path,
) -> Dict[str, Any]:
    print(f"Benchmarking: provider={provider:<12} | model={model} ...")
    
    # Resolver a chave de API correta
    env_key = {
        "gemini": "GEMINI_API_KEY",
        "openrouter": "OPENROUTER_API_KEY",
        "opencodego": "OPENCODEGO_API_KEY"
    }.get(provider, "")
    
    api_key = os.environ.get(env_key, "") if env_key else ""
    
    if provider != "fake" and not api_key:
        print(f"  [PULADO] Chave de API {env_key} nao configurada no ambiente.")
        return {
            "provider": provider,
            "model": model,
            "status": "skipped",
            "error": f"Chave {env_key} nao configurada",
            "duration_seconds": 999999.0,  # Fica no final da ordenação
            "estado": "N/A",
            "conclusoes": []
        }
        
    start_time = time.perf_counter()
    try:
        # Normalizar a evidência física
        pacote_evidencia = normalizar_evidencia(caminho_evidencia)
        
        # O upload temporário precisa ocorrer dentro do bloco para manter os arquivos válidos
        with tempfile.TemporaryDirectory() as upload_tmp:
            arquivos_upload = arquivos_compativeis_upload(caminho_evidencia, upload_tmp)
            pacote_dict = {
                "documentos": pacote_evidencia.documentos,
                "inventario": pacote_evidencia.inventario,
                "erro": pacote_evidencia.erro,
                "arquivos_upload": arquivos_upload,
            }
            
            result = executar_provider(
                provider=provider,
                model=model,
                api_key=api_key,
                prompt=prompt,
                auditado="ALERJ",
                questao_base="q0101",
                coluna_evidencia="q0101evi",
                itens_afirmados=itens,
                pacote=pacote_dict,
            )
            
        duration = time.perf_counter() - start_time
        status = result.get("status", "error") if isinstance(result, dict) else "error"
        conclusoes = result.get("conclusoes", []) if status == "completed" else []
        
        # Extrair o estado da primeira conclusão
        estado = "N/A"
        if conclusoes and isinstance(conclusoes, list) and isinstance(conclusoes[0], dict):
            estado = conclusoes[0].get("estado", "N/A")
            
        err_msg = result.get("error", "") if status == "error" else ""
        if status == "error":
            print(f"  [ERRO] {err_msg} | Tempo: {duration:.2f}s")
        else:
            print(f"  [OK] Concluido | Tempo: {duration:.2f}s | Estado: {estado}")
            
        return {
            "provider": provider,
            "model": model,
            "status": status,
            "error": err_msg,
            "duration_seconds": duration,
            "estado": estado,
            "conclusoes": conclusoes
        }
    except Exception as e:
        duration = time.perf_counter() - start_time
        print(f"  [FALHA] Execucao falhou com excecao: {e} | Tempo: {duration:.2f}s")
        return {
            "provider": provider,
            "model": model,
            "status": "error",
            "error": str(e),
            "duration_seconds": duration,
            "estado": "EXCECAO",
            "conclusoes": []
        }


def main():
    parser = argparse.ArgumentParser(description="Benchmark de velocidade de resposta de modelos de IA.")
    parser.add_argument(
        "--evidencia-path",
        default="/tmp/tcerj-igovti-2026/evidencias_extraidas/ALERJ/00001_01_organograma-alerj-versão-para-impressão.pdf",
        help="Caminho do PDF de evidencia a ser avaliado."
    )
    parser.add_argument(
        "--prompts-dir",
        default="scripts/avaliacao_evidencias/prompts/igovti_2026_conservador_v2",
        help="Diretorio com os prompts markdown gerados."
    )
    parser.add_argument(
        "--models",
        default=None,
        help="Lista de modelos formato provider/model separados por virgula. Ex: gemini/gemini-2.5-flash,openrouter/google/gemini-2.5-flash"
    )
    parser.add_argument(
        "--output-json",
        default="scripts/benchmark_results.json",
        help="Arquivo JSON onde todos os resultados serao salvos."
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=0,
        help="Numero maximo de retentativas para erros transientes como 429. Padrao e 0 (falha rapida)."
    )
    parser.add_argument(
        "--retry-delays",
        default="1.0,2.0,4.0",
        help="Tempos de espera (delays) entre retentativas para erros transientes."
    )
    args = parser.parse_args()

    os.environ["AI_MAX_RETRIES"] = str(args.max_retries)
    os.environ["AI_RETRY_DELAYS"] = args.retry_delays

    # 1. Resolver e validar o caminho da evidência
    caminho = Path(args.evidencia_path)
    if not caminho.is_file():
        # Tentar auto-resolucao no diretorio ALERJ
        alerj_dir = Path("/tmp/tcerj-igovti-2026/evidencias_extraidas/ALERJ")
        if alerj_dir.is_dir():
            for f in alerj_dir.iterdir():
                if "organograma" in f.name.lower() and f.suffix == ".pdf":
                    caminho = f
                    break
                    
    if not caminho.is_file():
        print(f"Erro: Arquivo de evidencia nao encontrado: {args.evidencia_path}")
        print("Certifique-se de extrair as evidencias usando 'python3 scripts/extrair_evidencias.py' antes de rodar o benchmark.")
        return 1

    print(f"Utilizando evidencia: {caminho.resolve()}")

    # 2. Carregar o prompt da q0101
    prompts_dir = Path(args.prompts_dir)
    prompt_path = prompts_dir / "q0101.md"
    if not prompt_path.is_file():
        # Fallback para o diretorio legado se houver
        prompts_dir = Path("scripts/avaliacao_evidencias/prompts/igovti_2026_conservador")
        prompt_path = prompts_dir / "q0101.md"

    if not prompt_path.is_file():
        print(f"Erro: Prompt q0101 nao encontrado em {args.prompts_dir} ou caminhos de fallback.")
        return 1

    print(f"Utilizando prompt: {prompt_path.resolve()}")
    prompt_content = prompt_path.read_text(encoding="utf-8")

    # 3. Configurar itens afirmados para q0101
    itens = [
        ItemAfirmado(
            codigo="q0101[a) Centralizada Interna: Há uma área de TI centralizada e formal que atende toda a organização, utilizando equipe técnica majoritariamente própria (servidores).]",
            texto="0101. Qual alternativa melhor descreve a formalização e o modelo de operação predominante da Tecnologia da Informação (TI) na organização?",
            afirmacao="a) Centralizada Interna: Há uma área de TI centralizada e formal que atende toda a organização, utilizando equipe técnica majoritariamente própria (servidores)."
        )
    ]

    # 4. Configurar lista de modelos a serem testados
    models_to_test = []
    if args.models:
        for item in args.models.split(","):
            if "/" in item:
                prov, mod = item.strip().split("/", 1)
                models_to_test.append((prov, mod))
            else:
                models_to_test.append(("gemini", item.strip()))
    else:
        models_to_test = DEFAULT_MODELS

    # 5. Executar os benchmarks
    benchmark_results = []
    print("\nIniciando o benchmark...")
    print("=" * 60)
    for provider, model in models_to_test:
        res = benchmark_model(
            provider=provider,
            model=model,
            prompt=prompt_content,
            itens=itens,
            caminho_evidencia=caminho,
        )
        benchmark_results.append(res)
    print("=" * 60)

    # 6. Salvar todos os resultados detalhados
    with open(args.output_json, "w", encoding="utf-8") as f:
        json.dump(benchmark_results, f, ensure_ascii=False, indent=2)
    print(f"\nResultados completos salvos em: {args.output_json}")

    # 7. Filtrar pulados e ordenar por tempo de execução
    valid_results = [r for r in benchmark_results if r["status"] != "skipped"]
    valid_results.sort(key=lambda x: x["duration_seconds"])

    skipped_results = [r for r in benchmark_results if r["status"] == "skipped"]

    # 8. Apresentar ranking
    print("\n" + "=" * 80)
    print(f"{'RANKING DE VELOCIDADE (Do mais rapido ao mais lento)':^80}")
    print("=" * 80)
    print(f"{'Rank':<6} | {'Provedor':<12} | {'Modelo':<35} | {'Tempo (s)':<10} | {'Status':<10} | {'Estado':<12}")
    print("-" * 88)
    
    for rank, res in enumerate(valid_results, start=1):
        dur_str = f"{res['duration_seconds']:.3f}s" if res['status'] == "completed" else "N/A"
        print(f"{rank:<6} | {res['provider']:<12} | {res['model']:<35} | {dur_str:<10} | {res['status']:<10} | {res['estado']:<12}")
        
    if skipped_results:
        print("\nModelos nao testados (Chaves de API ausentes):")
        for res in skipped_results:
            print(f"  - {res['provider']}/{res['model']} ({res['error']})")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(main())
