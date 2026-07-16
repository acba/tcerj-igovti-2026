from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.avaliacao_evidencias.providers.response import (
    json_schema_response_format,
    validar_resultado_ia,
)
from scripts.avaliacao_evidencias.evidence_processing import _tentar_extrair_markdown_pdf
from scripts.avaliacao_evidencias.providers.base import (
    GenericProvider,
    conteudo_provider_textual,
    pacote_textual_sem_documentos_de_arquivos_nativos,
)
from scripts.comentarios_gestor_pipeline import (
    DEFAULT_AJUSTES,
    DEFAULT_CATALOG,
    DEFAULT_LSS,
    DEFAULT_MAPA,
    DEFAULT_RESPOSTAS_BASE,
    DEFAULT_RESULTADO,
    ItemAnterior,
    _agregar_propostas_ajuste,
    _identidade_logica_analise,
    _resolver_valor_positivo,
    _selecionar_situacao,
    avaliar_casos,
    carregar_rotas_catalogo,
    consolidar_casos,
    filtrar_itens_saneados_secao1,
    gerar_painel_evidencias_pos_comentarios,
    gravar_avaliacoes_modelos_xlsx,
    mapear_ajustes_secao1,
    materializar_checkpoint_limpo_modelo,
    parse_uploads,
)
from scripts.run_comentarios_gestor import DEFAULT_MODELS_CONFIG, carregar_configuracao_modelos, models


def opinion(case_id: str, provider: str, model: str) -> dict:
    return {
        "identity": f"{provider}-{model}",
        "case_id": case_id,
        "secao": "reavaliacao",
        "auditado": "ORG",
        "codigo": "q1001",
        "questao": "q1001",
        "coluna_evidencia": "q1001evi",
        "evidencia": "",
        "provider": provider,
        "model": model,
        "model_key": model,
        "status": "completed",
        "finished_at": "2026-07-13T10:00:00+00:00",
        "evidence_paths": [],
        "pacote_contexto_consolidacao": {"documentos": [], "inventario": [], "erro": ""},
        "result": {
            "status": "completed",
            "conclusoes": [
                {
                    "item_codigo": "q1001[A]",
                    "item_texto": "Prática",
                    "afirmacao_auditado": "Sim",
                    "estado": "nao_conforme",
                    "justificativa": "Teste",
                    "lacunas": [],
                    "arquivos_referenciados": [],
                    "trechos_ou_elementos": [],
                    "paginas_ou_localizacao": [],
                }
            ],
        },
    }


class ComentariosGestorPipelineTest(unittest.TestCase):
    def test_ajuste_corrente_nao_majora_item_sem_resposta_original_restauravel(self) -> None:
        valor, motivo = _resolver_valor_positivo(
            auditado="ORG", codigo="q1001ext[A]", fonte="questionario", ajustes_evidencias={},
        )
        self.assertEqual(valor, "")
        self.assertIn("originalmente afirmada", motivo)

    def test_checkpoint_limpo_exclui_identidade_de_prompt_anterior(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            checkpoint = root / "analyses_model_m.jsonl"
            registros = [
                {"identity": "antiga", "logical_identity": "antiga", "case_id": "c", "model_key": "m", "status": "completed"},
                {"identity": "nova", "logical_identity": "nova", "case_id": "c", "model_key": "m", "status": "completed"},
            ]
            checkpoint.write_text("\n".join(json.dumps(r) for r in registros) + "\n", encoding="utf-8")
            clean = materializar_checkpoint_limpo_modelo(
                root, model_key="m", routes=[], expected_identities={"nova"},
            )
            vigentes = [json.loads(line) for line in clean.read_text(encoding="utf-8").splitlines()]
        self.assertEqual([r["logical_identity"] for r in vigentes], ["nova"])

    def test_default_models_configuration_is_external_and_includes_glm(self) -> None:
        config = carregar_configuracao_modelos(DEFAULT_MODELS_CONFIG)
        pairs = {(item["provider"], item["model"]) for item in config["evaluators"]}
        self.assertIn(("openrouter", "z-ai/glm-5.2"), pairs)
        self.assertEqual(config["judge"]["min_valid_opinions"], 2)

    def test_models_configuration_rejects_duplicate_pairs(self) -> None:
        config = json.loads(DEFAULT_MODELS_CONFIG.read_text(encoding="utf-8"))
        config["evaluators"].append(dict(config["evaluators"][0], name="duplicado"))
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "models.json"
            path.write_text(json.dumps(config), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "provider/model duplicado"):
                carregar_configuracao_modelos(path)

    def test_models_configuration_filters_disabled_routes(self) -> None:
        config = json.loads(DEFAULT_MODELS_CONFIG.read_text(encoding="utf-8"))
        config["evaluators"][0]["enabled"] = False
        config["judge"]["min_valid_opinions"] = 1
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "models.json"
            path.write_text(json.dumps(config), encoding="utf-8")
            loaded = carregar_configuracao_modelos(path)
        self.assertEqual(
            len(models(loaded, False)),
            sum(item.get("enabled", True) for item in config["evaluators"]),
        )

    def test_models_configuration_defaults_enabled_and_model_key(self) -> None:
        config = json.loads(DEFAULT_MODELS_CONFIG.read_text(encoding="utf-8"))
        config["evaluators"][0].pop("enabled")
        config["evaluators"][0].pop("model_key")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "models.json"
            path.write_text(json.dumps(config), encoding="utf-8")
            loaded = carregar_configuracao_modelos(path)
        self.assertTrue(loaded["evaluators"][0]["enabled"])
        self.assertEqual(loaded["evaluators"][0]["model_key"], loaded["evaluators"][0]["model"])
        self.assertEqual(loaded["evaluators"][0]["pdf_detail"], "auto")
        self.assertEqual(loaded["judge"]["pdf_detail"], "auto")

    def test_models_configuration_rejects_invalid_pdf_detail(self) -> None:
        config = json.loads(DEFAULT_MODELS_CONFIG.read_text(encoding="utf-8"))
        config["evaluators"][0]["pdf_detail"] = "medium"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "models.json"
            path.write_text(json.dumps(config), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "pdf_detail"):
                carregar_configuracao_modelos(path)

    def test_models_configuration_allows_alternative_disabled_route(self) -> None:
        config = json.loads(DEFAULT_MODELS_CONFIG.read_text(encoding="utf-8"))
        first = config["evaluators"][0]
        config["evaluators"].append(
            {
                **first,
                "name": "gemini-alternativo",
                "provider": "openrouter",
                "model": "google/gemini-3.1-flash-lite",
                "enabled": False,
            }
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "models.json"
            path.write_text(json.dumps(config), encoding="utf-8")
            loaded = carregar_configuracao_modelos(path)
        self.assertEqual(
            len(models(loaded, False)),
            sum(item.get("enabled", True) for item in config["evaluators"]),
        )

    def test_models_configuration_rejects_two_active_routes_for_model_key(self) -> None:
        config = json.loads(DEFAULT_MODELS_CONFIG.read_text(encoding="utf-8"))
        first = config["evaluators"][0]
        config["evaluators"].append(
            {
                **first,
                "name": "gemini-alternativo",
                "provider": "openrouter",
                "model": "google/gemini-3.1-flash-lite",
                "enabled": True,
            }
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "models.json"
            path.write_text(json.dumps(config), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "uma rota.*model_key"):
                carregar_configuracao_modelos(path)

    def test_logical_identity_ignores_provider_but_tracks_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            evidence = Path(tmp) / "A.pdf"
            evidence.write_bytes(b"conteudo")
            kwargs = {
                "case_id_value": "case",
                "model_key": "gpt-5.4-mini",
                "prompt_hash": "prompt",
                "reasoning": "high",
                "pdf2md": False,
                "docx2html": False,
                "contexto": {"situacao": "A"},
                "evidence_paths": [evidence],
            }
            first = _identidade_logica_analise(**kwargs)
            second = _identidade_logica_analise(**kwargs)
            changed = _identidade_logica_analise(**{**kwargs, "pdf2md": True})
            changed_detail = _identidade_logica_analise(**{**kwargs, "pdf_detail": "low"})
        self.assertEqual(first, second)
        self.assertNotEqual(first, changed)
        self.assertNotEqual(first, changed_detail)

    def test_provider_switch_reuses_canonical_model_checkpoint(self) -> None:
        case = {
            "case_id": "case", "secao": "reavaliacao", "auditado": "ORG", "codigo": "q1",
            "coluna_evidencia": "q1evi", "prompt_hash": "prompt", "prompt_version": "v1",
            "contexto": {}, "evidence_paths": [], "evidencias": [], "documentos_contexto": [],
        }
        routes = [
            {"provider": "openai", "model": "gpt-5.4-mini", "model_key": "gpt-5.4-mini"},
            {"provider": "openrouter", "model": "openai/gpt-5.4-mini", "model_key": "gpt-5.4-mini"},
        ]

        def completed(caso, *, provider, model, **_):
            record = opinion(caso["case_id"], provider, model)
            record.update({"contexto": {}, "evidence_paths": [], "prompt_hash": "prompt"})
            return record

        with tempfile.TemporaryDirectory() as tmp, patch(
            "scripts.comentarios_gestor_pipeline.executar_caso", side_effect=completed
        ):
            out = Path(tmp)
            first = avaliar_casos(
                [case], provider="openai", model="gpt-5.4-mini", model_key="gpt-5.4-mini",
                out_dir=out, routes=routes, quiet=True,
            )
            second = avaliar_casos(
                [case], provider="openrouter", model="openai/gpt-5.4-mini", model_key="gpt-5.4-mini",
                out_dir=out, routes=routes, quiet=True,
            )
        self.assertEqual(first["processados"], 1)
        self.assertEqual(second["processados"], 0)
        self.assertEqual(second["pulados"], 1)

    def test_missing_evidence_hash_fails_only_its_case(self) -> None:
        def case(case_id: str, evidence_paths: list[Path]) -> dict:
            return {
                "case_id": case_id,
                "secao": "reavaliacao",
                "auditado": "ORG",
                "codigo": case_id,
                "coluna_evidencia": "q1evi",
                "prompt_hash": "prompt",
                "prompt_version": "v1",
                "contexto": {},
                "evidence_paths": evidence_paths,
                "evidencias": [],
                "documentos_contexto": [],
            }

        def completed(caso, *, provider, model, **_):
            record = opinion(caso["case_id"], provider, model)
            record.update({"contexto": {}, "evidence_paths": [], "prompt_hash": "prompt"})
            return record

        with tempfile.TemporaryDirectory() as tmp, patch(
            "scripts.comentarios_gestor_pipeline.executar_caso", side_effect=completed
        ) as execute:
            root = Path(tmp)
            result = avaliar_casos(
                [case("ausente", [root / "nao-existe.pdf"]), case("valido", [])],
                provider="fake",
                model="fake",
                model_key="fake",
                out_dir=root / "out",
                quiet=True,
            )
        self.assertEqual(result["processados"], 2)
        self.assertEqual(result["erros"], 1)
        self.assertEqual(result["concluidos"], 1)
        self.assertEqual(execute.call_count, 1)

    def test_pdf2md_does_not_change_process_working_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "origem.pdf"
            source.write_bytes(b"pdf sintetico")
            images = root / "saida" / "img"
            images.mkdir(parents=True)
            cwd_before = Path.cwd()
            absolute_image = (images / "pagina.png").resolve().as_posix()
            with patch(
                "pymupdf4llm.to_markdown",
                return_value=f"![imagem]({absolute_image})",
            ) as convert:
                markdown, error = _tentar_extrair_markdown_pdf(
                    source,
                    images.parent,
                    images,
                    "origem",
                    150,
                )
            self.assertEqual(Path.cwd(), cwd_before)
            self.assertEqual(error, "")
            self.assertEqual(markdown, "![imagem](img/pagina.png)")
            self.assertTrue(Path(convert.call_args.kwargs["image_path"]).is_absolute())

    def test_provider_switch_reuses_legacy_provider_checkpoint(self) -> None:
        case = {
            "case_id": "case", "secao": "reavaliacao", "auditado": "ORG", "codigo": "q1",
            "coluna_evidencia": "q1evi", "prompt_hash": "prompt", "prompt_version": "v1",
            "contexto": {}, "evidence_paths": [], "evidencias": [], "documentos_contexto": [],
        }
        routes = [
            {"provider": "openai", "model": "gpt-5.4-mini", "model_key": "gpt-5.4-mini"},
            {"provider": "openrouter", "model": "openai/gpt-5.4-mini", "model_key": "gpt-5.4-mini"},
        ]
        legacy = opinion("case", "openai", "gpt-5.4-mini")
        legacy.pop("model_key")
        legacy.update(
            {
                "identity": "identidade-antiga-com-provider",
                "contexto": {}, "evidence_paths": [], "prompt_hash": "prompt",
                "reasoning_effort": "high", "evidence_processing_mode": "",
            }
        )
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            (out / "analyses_openai_gpt-5.4-mini.jsonl").write_text(
                json.dumps(legacy) + "\n", encoding="utf-8"
            )
            with patch("scripts.comentarios_gestor_pipeline.executar_caso") as execute:
                result = avaliar_casos(
                    [case], provider="openrouter", model="openai/gpt-5.4-mini",
                    model_key="gpt-5.4-mini", out_dir=out, routes=routes, quiet=True,
                )
            clean = [
                json.loads(line)
                for line in (out / "analyses_clean_model_gpt-5.4-mini.jsonl").read_text().splitlines()
            ]
        execute.assert_not_called()
        self.assertEqual(result["pulados"], 1)
        self.assertEqual(clean[0]["source_identity"], "identidade-antiga-com-provider")
        self.assertEqual(clean[0]["model_key"], "gpt-5.4-mini")

    def test_empty_limesurvey_upload_is_absence(self) -> None:
        self.assertEqual(parse_uploads("[]"), [])

    def test_section_one_selection_rule(self) -> None:
        self.assertFalse(_selecionar_situacao("Concorda, mas ainda não adotou nenhuma medida", "", "", []))
        self.assertTrue(_selecionar_situacao("Discorda da sinalização", "Justificativa", "", []))
        self.assertTrue(_selecionar_situacao("Concorda e já está atendendo", "", "", []))

    def test_q2804_uses_specific_evidence_route(self) -> None:
        routes = carregar_rotas_catalogo(DEFAULT_CATALOG)
        self.assertEqual(routes["q2804"][0]["coluna_evidencia"], "q2804eviA")

    def test_temporal_schema_requires_temporal_fields(self) -> None:
        schema = json_schema_response_format(response_profile="manager_comments_temporal")
        properties = schema["json_schema"]["schema"]["properties"]["conclusoes"]["items"]["properties"]
        self.assertIn("estado_temporal", properties)
        result = opinion("case", "fake", "m")["result"]
        with self.assertRaises(ValueError):
            validar_resultado_ia(result, response_profile="manager_comments_temporal")

    def test_temporal_reason_accepts_extras_and_normalizes_safe_aliases(self) -> None:
        result = opinion("case", "fake", "m")["result"]
        conclusion = result["conclusoes"][0]
        conclusion.update({
            "estado_temporal": "mantida",
            "conclusoes_motivos": [{
                "motivo_id": "MR001",
                "estado": "mantido",
                "justificativa_motivo": "A manifestação não afasta o motivo.",
                "evidencias_consideradas": ["anexo.pdf"],
            }],
            "providencias_informadas": [],
            "comentarios_encaminhamento": "",
            "consequencias_praticas": [],
            "alternativas_propostas": [],
        })

        validated = validar_resultado_ia(result, response_profile="manager_comments_temporal")
        reason = validated["conclusoes"][0]["conclusoes_motivos"][0]
        self.assertEqual(reason["id_motivo"], "MR001")
        self.assertEqual(reason["estado_motivo"], "mantido")
        self.assertEqual(reason["justificativa"], "A manifestação não afasta o motivo.")
        self.assertEqual(reason["evidencias_consideradas"], ["anexo.pdf"])
        self.assertIn("avisos_estrutura_motivos", validated["conclusoes"][0])

    def test_temporal_reason_reports_the_specific_missing_fields(self) -> None:
        result = opinion("case", "fake", "m")["result"]
        conclusion = result["conclusoes"][0]
        conclusion.update({
            "estado_temporal": "mantida",
            "conclusoes_motivos": [{"id_motivo": "MR001"}],
            "providencias_informadas": [],
            "comentarios_encaminhamento": "",
            "consequencias_praticas": [],
            "alternativas_propostas": [],
        })

        with self.assertRaisesRegex(
            ValueError,
            r"motivo 0 sem campos: estado_motivo, justificativa",
        ):
            validar_resultado_ia(result, response_profile="manager_comments_temporal")

    def test_invalid_provider_response_preserves_raw_content(self) -> None:
        raw = '{"status":"completed","conclusoes":[{}]}'
        parsed = GenericProvider("modelo")._interpretar_resposta(
            raw,
            response_profile="manager_comments_temporal",
        )
        self.assertEqual(parsed["status"], "error")
        self.assertEqual(parsed["raw_response"], raw)
        self.assertIn("conclusao 0 sem campos", parsed["error"])

    def test_temporal_prompt_contains_reason_object_example(self) -> None:
        payload = json.loads(conteudo_provider_textual(
            prompt="Avalie.",
            auditado="ORG",
            questao_base="A1G1",
            coluna_evidencia="comentario",
            itens_afirmados=[],
            pacote={},
            response_profile="manager_comments_temporal",
        ))
        reason = payload["saida_obrigatoria"]["conclusoes"][0]["conclusoes_motivos"][0]
        self.assertEqual(set(reason), {"id_motivo", "estado_motivo", "justificativa"})

    def test_native_upload_filter_preserves_manager_context(self) -> None:
        package = {
            "arquivos_upload": ["/tmp/nova-evidencia.pdf"],
            "documentos": [
                {"nome": "nova-evidencia.pdf", "texto": "conteúdo extraído"},
                {"nome": "comentario-gestor", "texto": "esclarecimento do auditado"},
            ],
        }
        filtered = pacote_textual_sem_documentos_de_arquivos_nativos(package, {".pdf"})
        self.assertEqual([doc["nome"] for doc in filtered["documentos"]], ["comentario-gestor"])

    def test_section_one_maps_binary_adjustment_and_flags_derived_field(self) -> None:
        def record(case: str, code: str, item: str, source: str) -> dict:
            return {
                "identity": f"id-{case}", "case_id": case, "secao": "situacoes",
                "auditado": "AGERIO", "codigo": code, "status": "completed",
                "finished_at": "2026-07-14T10:00:00+00:00",
                "contexto": {
                    "achado": 2, "situacao": f"Situação {code}",
                    "motivos": [{
                        "id": f"MR-{code}",
                        "acoes": [{
                            "id": f"AV-{code}", "informacao_requerida": item,
                            "id_fonte_informacao": source,
                        }],
                    }],
                },
                "result": {"status": "completed", "error": "", "conclusoes": [{
                    "item_codigo": code, "item_texto": f"Situação {code}",
                    "afirmacao_auditado": "Discorda", "estado": "nao_conforme",
                    "estado_temporal": "corrigida_posteriormente", "justificativa": "Sanada.",
                }]},
            }

        with tempfile.TemporaryDirectory() as tmp:
            consolidated = Path(tmp) / "consolidated_clean.jsonl"
            consolidated.write_text(
                "\n".join([
                    json.dumps(record("c1", "A2G4", "q1001ext[E]", "avaliacao_evidencias_ajustes")),
                    json.dumps(record("c2", "A4G12", "total_SI", "questionario")),
                ]) + "\n",
                encoding="utf-8",
            )
            ajustes, pendencias = mapear_ajustes_secao1(
                consolidado=consolidated,
                resultado_auditoria=DEFAULT_RESULTADO,
                mapa=DEFAULT_MAPA,
                lss=DEFAULT_LSS,
                ajustes_pos_avaliacao_evidencias=DEFAULT_AJUSTES,
                respostas_base=DEFAULT_RESPOSTAS_BASE,
            )
        self.assertEqual([(a["Código do item avaliado"], a["Resposta ajustada"]) for a in ajustes], [("q1001ext[E]", "Sim")])
        self.assertEqual(pendencias[0]["Código do item avaliado"], "total_SI")

    def test_section_two_filter_removes_only_sane_item_from_base_group(self) -> None:
        first = ItemAnterior("ORG", "q1001ext[E]", "q1001", "Sim", "Não conforme", "", "E")
        second = ItemAnterior("ORG", "q1001ext[F]", "q1001", "Sim", "Não conforme", "", "F")
        saneamento = {("ORG", "q1001ext[E]"): {"Auditado": "ORG", "Código do item avaliado": "q1001ext[E]", "Resposta ajustada": "Sim"}}
        restantes, excluidos = filtrar_itens_saneados_secao1({("ORG", "q1001"): [first, second]}, saneamento)
        self.assertEqual([item.codigo for item in restantes[("ORG", "q1001")]], ["q1001ext[F]"])
        self.assertEqual(excluidos[0]["Código do item avaliado"], "q1001ext[E]")

    def test_conflicting_adjustments_become_pending(self) -> None:
        base = {"Auditado": "ORG", "Código do item avaliado": "q1001ext[A]"}
        finais, pendencias = _agregar_propostas_ajuste(
            [{**base, "Resposta ajustada": "Sim"}, {**base, "Resposta ajustada": "Não"}], []
        )
        self.assertEqual(finais, [])
        self.assertIn("conflitantes", pendencias[0]["Motivo da pendência"])

    def test_individual_evaluations_workbook_has_human_readable_sheets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            checkpoint = root / "analyses.jsonl"
            checkpoint.write_text(json.dumps(opinion("case", "provider", "model")) + "\n", encoding="utf-8")
            output = root / "avaliacoes_modelos.xlsx"
            gravar_avaliacoes_modelos_xlsx(
                output, [checkpoint], expected_models=["model"], expected_case_ids={"case"},
            )
            from openpyxl import load_workbook
            wb = load_workbook(output, read_only=True)
            sheets = wb.sheetnames
            wb.close()
        self.assertEqual(sheets, ["Avaliações", "Motivos", "Erros e ausências", "Escopo seção 2"])

    def test_revised_evidence_panel_blanks_sane_item_and_keeps_schema(self) -> None:
        from openpyxl import Workbook, load_workbook
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "painel.xlsx"
            output = root / "painel-final.xlsx"
            wb = Workbook()
            ws = wb.active
            ws.append(["Auditado", "q1001ext[E]", "q1001ext[E]__justificativa"])
            ws.append(["ORG", "Não conforme", "Lacuna"])
            wb.save(source)
            count = gerar_painel_evidencias_pos_comentarios(
                painel_origem=source,
                output=output,
                ajustes=[{"Auditado": "ORG", "Código do item avaliado": "q1001ext[E]"}],
            )
            result = load_workbook(output, data_only=True)
            values = list(result.active.iter_rows(values_only=True))
            result.close()
        self.assertEqual(count, 1)
        self.assertEqual(values[0], ("Auditado", "q1001ext[E]", "q1001ext[E]__justificativa"))
        self.assertEqual(values[1], ("ORG", None, None))

    def test_reconsolidates_when_third_and_fourth_opinions_arrive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = []
            pairs = [("p1", "m1"), ("p2", "m2"), ("p3", "m3"), ("p4", "m4")]
            for provider, model in pairs:
                path = root / f"{provider}.jsonl"
                path.write_text(json.dumps(opinion("case", provider, model)) + "\n", encoding="utf-8")
                paths.append(path)
            first = consolidar_casos(
                analyses_files=paths[:2], out_dir=root / "out", secao="2",
                expected_models=[model for _, model in pairs],
                judge_provider="fake", judge_model="judge", min_opinions=2, quiet=True,
            )
            second = consolidar_casos(
                analyses_files=paths[:3], out_dir=root / "out", secao="2",
                expected_models=[model for _, model in pairs],
                judge_provider="fake", judge_model="judge", min_opinions=2, quiet=True,
            )
            third = consolidar_casos(
                analyses_files=paths, out_dir=root / "out", secao="2",
                expected_models=[model for _, model in pairs],
                judge_provider="fake", judge_model="judge", min_opinions=2, quiet=True,
            )
            raw = [json.loads(line) for line in (root / "out/consolidated.jsonl").read_text().splitlines()]
            clean = [json.loads(line) for line in (root / "out/consolidated_clean.jsonl").read_text().splitlines()]
            self.assertEqual(first["concluidos"], 1)
            self.assertEqual(second["concluidos"], 1)
            self.assertEqual(third["concluidos"], 1)
            self.assertEqual([r["opinioes_validas"] for r in raw], [2, 3, 4])
            self.assertEqual(len(clean), 1)
            self.assertEqual(clean[0]["opinioes_validas"], 4)
            self.assertTrue(clean[0]["supersedes_identity"])

    def test_consolidation_counts_one_opinion_per_model_key(self) -> None:
        first = opinion("case", "openai", "gpt-5.4-mini")
        first["model_key"] = "gpt-5.4-mini"
        first["identity"] = "logical-identity"
        second = opinion("case", "openrouter", "openai/gpt-5.4-mini")
        second["model_key"] = "gpt-5.4-mini"
        second["identity"] = "logical-identity"
        second["finished_at"] = "2026-07-13T11:00:00+00:00"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = [root / "openai.jsonl", root / "openrouter.jsonl"]
            paths[0].write_text(json.dumps(first) + "\n", encoding="utf-8")
            paths[1].write_text(json.dumps(second) + "\n", encoding="utf-8")
            result = consolidar_casos(
                analyses_files=paths,
                out_dir=root / "out",
                secao="2",
                expected_models=["gpt-5.4-mini"],
                judge_provider="fake",
                judge_model="judge",
                min_opinions=1,
                quiet=True,
            )
            clean = [json.loads(line) for line in (root / "out/consolidated_clean.jsonl").read_text().splitlines()]
        self.assertEqual(result["concluidos"], 1)
        self.assertEqual(clean[0]["opinioes_validas"], 1)
        self.assertEqual(clean[0]["opinioes"][0]["provider"], "openrouter")


if __name__ == "__main__":
    unittest.main()
