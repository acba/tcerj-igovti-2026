from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from scripts import md2lss


@dataclass(frozen=True)
class PromptContext:
    arquivo: str
    coluna_evidencia: str
    questao_base: str
    item_especifico: str
    grupo: str
    texto_questao: str
    solicitacao_evidencia: str
    itens_possiveis: dict[str, str]


def load_catalog(caminho: str | Path) -> dict[str, Any]:
    with Path(caminho).open(encoding="utf-8") as file:
        data = yaml.safe_load(file)
    if not isinstance(data, dict):
        raise ValueError("catalogo de prompts deve ser um objeto YAML")
    if not isinstance(data.get("prompts"), list):
        raise ValueError("catalogo de prompts deve conter lista prompts")
    return data


def build_prompt_set(catalogo_path: str | Path, questionario: str | Path, destino: str | Path) -> None:
    catalogo = load_catalog(catalogo_path)
    erros = validate_catalog(catalogo, questionario)
    if erros:
        raise ValueError("catalogo de prompts invalido:\n" + "\n".join(erros))

    destino_path = Path(destino)
    destino_path.mkdir(parents=True, exist_ok=True)
    contextos = {contexto.arquivo: contexto for contexto in _prompt_contexts(questionario)}
    for entrada in sorted(catalogo["prompts"], key=lambda item: item["arquivo"]):
        contexto = contextos[entrada["arquivo"]]
        texto = render_prompt(catalogo, entrada, contexto)
        (destino_path / entrada["arquivo"]).write_text(texto, encoding="utf-8")


def validate_catalog(catalogo: dict[str, Any], questionario: str | Path) -> list[str]:
    erros: list[str] = []
    contextos = {contexto.arquivo: contexto for contexto in _prompt_contexts(questionario)}
    vistos: set[str] = set()
    regra = catalogo.get("regra_comum")
    if not isinstance(regra, dict):
        erros.append("regra_comum deve ser objeto")
    else:
        for campo in ["conformidade", "nao_conformidade"]:
            valor = regra.get(campo)
            if not isinstance(valor, list) or not all(isinstance(item, str) and item.strip() for item in valor):
                erros.append(f"regra_comum.{campo} deve ser lista de textos")

    for idx, entrada in enumerate(catalogo.get("prompts", [])):
        if not isinstance(entrada, dict):
            erros.append(f"prompts[{idx}] deve ser objeto")
            continue
        arquivo = entrada.get("arquivo")
        coluna = entrada.get("coluna_evidencia")
        if not isinstance(arquivo, str) or not arquivo:
            erros.append(f"prompts[{idx}] sem arquivo")
            continue
        if arquivo in vistos:
            erros.append(f"prompt duplicado: {arquivo}")
        vistos.add(arquivo)
        contexto = contextos.get(arquivo)
        if contexto is None:
            erros.append(f"prompt inesperado: {arquivo}")
            continue
        if coluna != contexto.coluna_evidencia:
            erros.append(f"{arquivo} com coluna_evidencia divergente")
        itens = entrada.get("itens_avaliaveis")
        if not isinstance(itens, list) or not itens or not all(isinstance(item, str) and item.strip() for item in itens):
            erros.append(f"{arquivo} deve declarar lista nao vazia itens_avaliaveis")
        elif set(itens) - set(contexto.itens_possiveis):
            extras = ", ".join(sorted(set(itens) - set(contexto.itens_possiveis)))
            erros.append(f"{arquivo} contem itens_avaliaveis inexistentes: {extras}")
        criterios = entrada.get("criterios_por_item")
        if criterios is not None and not isinstance(criterios, dict):
            erros.append(f"{arquivo} criterios_por_item deve ser objeto")
        excluir_regra = entrada.get("excluir_regra_comum_conformidade")
        if excluir_regra is not None and (
            not isinstance(excluir_regra, list) or not all(isinstance(item, str) and item.strip() for item in excluir_regra)
        ):
            erros.append(f"{arquivo} excluir_regra_comum_conformidade deve ser lista de textos")
        pratica = entrada.get("criterios_pratica_principal")
        if pratica is not None and (not isinstance(pratica, list) or not all(isinstance(item, str) and item.strip() for item in pratica)):
            erros.append(f"{arquivo} criterios_pratica_principal deve ser lista de textos")
    return erros


def render_prompt(catalogo: dict[str, Any], entrada: dict[str, Any], contexto: PromptContext) -> str:
    meta = catalogo.get("meta", {}) if isinstance(catalogo.get("meta"), dict) else {}
    regra = catalogo.get("regra_comum", {}) if isinstance(catalogo.get("regra_comum"), dict) else {}
    titulo = entrada.get("titulo") or f"{contexto.arquivo[:-3]} - {contexto.texto_questao}"
    itens_avaliaveis = [str(item) for item in entrada["itens_avaliaveis"]]
    criterios_por_item = entrada.get("criterios_por_item", {}) if isinstance(entrada.get("criterios_por_item"), dict) else {}
    excluir_conformidade = set(entrada.get("excluir_regra_comum_conformidade") or [])
    regra_conformidade = [
        item
        for item in regra.get("conformidade", [])
        if item not in excluir_conformidade
    ]
    linhas: list[str] = [
        f"# {titulo}",
        "",
        "<!-- Gerado a partir do catalogo YAML. Edite o catalogo, nao este arquivo. -->",
        f"<!-- itens_avaliaveis: {', '.join(itens_avaliaveis)} -->",
        "",
        "## Identidade da analise",
        f"- Prompt set: {meta.get('nome', 'igovti_2026_achados_binario')}",
        f"- Versao: {meta.get('versao', 'v1')}",
        "- Postura de julgamento: auditoria objetiva, binaria e conservadora",
        f"- Grupo do questionario: {contexto.grupo}",
        f"- Questao base: {contexto.texto_questao}",
        f"- Coluna de evidencia: {contexto.coluna_evidencia}",
        f"- Solicitacao de evidencia ao auditado: {contexto.solicitacao_evidencia}",
        "",
        "## Escopo",
        "- Avalie somente os itens afirmados recebidos em `itens_afirmados` pelo pipeline.",
        "- Nao crie conclusoes para itens nao afirmados, ainda que a evidencia sugira sua ocorrencia.",
        "- Nao avalie item sem criterio listado neste prompt.",
        "",
        "## Regra comum de conformidade",
    ]
    linhas.extend(_bullet_list(regra_conformidade))
    linhas.extend(["", "## Regra comum de nao conformidade"])
    linhas.extend(_bullet_list(regra.get("nao_conformidade", [])))

    pratica = entrada.get("criterios_pratica_principal")
    if pratica:
        linhas.extend(["", "## Criterios da pratica principal"])
        linhas.extend(_bullet_list(pratica))

    linhas.extend(["", "## Criterios por item"])
    for codigo in itens_avaliaveis:
        texto_item = contexto.itens_possiveis[codigo]
        linhas.append(f"- {codigo}: {texto_item}")
        criterios = criterios_por_item.get(codigo) or (pratica if codigo == contexto.questao_base else None) or [_criterio_padrao_item(texto_item)]
        for criterio in criterios:
            linhas.append(f"  - {criterio}")

    linhas.extend(
        [
            "",
            "## Regras de decisao",
            "- Use `conforme` somente quando a evidencia atender ao criterio especifico do item e a regra comum de conformidade.",
            "- Use `nao_conforme` quando a evidencia nao sustentar diretamente o item, nao trouxer elemento citavel, for declaracao isolada do respondente, for arquivo sem conteudo util ou pertencer a outra organizacao.",
            "- Nao use `inconclusivo` para julgamento substantivo.",
            "- Use `erro` apenas quando falha tecnica registrada no pacote impedir a avaliacao.",
            "",
            "## Saida obrigatoria",
            "- Responda somente com JSON valido.",
            "- O objeto raiz deve conter `status` com `completed` ou `error`.",
            "- Quando `status` for `completed`, inclua `conclusoes`, uma lista com uma conclusao por item afirmado avaliavel.",
            "- Cada conclusao deve conter exatamente estes campos: `item_codigo`, `item_texto`, `afirmacao_auditado`, `estado`, `justificativa`, `lacunas`, `arquivos_referenciados`, `trechos_ou_elementos`, `paginas_ou_localizacao`.",
            "- Para julgamento substantivo, `estado` deve ser `conforme` ou `nao_conforme`.",
            "- `lacunas`, `arquivos_referenciados`, `trechos_ou_elementos` e `paginas_ou_localizacao` devem ser listas.",
            "",
        ]
    )
    return "\n".join(linhas)


def _prompt_contexts(questionario: str | Path) -> list[PromptContext]:
    survey = md2lss.parse_markdown(Path(questionario))
    contextos: list[PromptContext] = []
    for group in survey.groups:
        questoes = {question.code: question for question in group.questions}
        for question in group.questions:
            if question.type != "upload" or "evi" not in question.code:
                continue
            questao_base, item_especifico = _base_coluna_evidencia(question.code)
            base = questoes[questao_base]
            arquivo = f"{questao_base}_{item_especifico}.md" if item_especifico else f"{questao_base}.md"
            contextos.append(
                PromptContext(
                    arquivo=arquivo,
                    coluna_evidencia=question.code,
                    questao_base=questao_base,
                    item_especifico=item_especifico,
                    grupo=group.title,
                    texto_questao=_clean(base.text()),
                    solicitacao_evidencia=_clean(question.text()),
                    itens_possiveis=_itens_possiveis(base, item_especifico, questoes),
                )
            )
    return contextos


def _base_coluna_evidencia(coluna: str) -> tuple[str, str]:
    marker = coluna.find("evi")
    return coluna[:marker], coluna[marker + 3 :]


def _itens_possiveis(question: Any, item_especifico: str, questoes: dict[str, Any]) -> dict[str, str]:
    if item_especifico:
        for item in question.subquestions:
            if item.code == item_especifico:
                return {f"{question.code}[{item.code}]": item.text}
        return {f"{question.code}[{item_especifico}]": item_especifico}
    detail = questoes.get(f"{question.code}ext")
    itens: dict[str, str] = {}
    if detail and detail.subquestions:
        itens[question.code] = _clean(question.text())
        itens.update({f"{detail.code}[{item.code}]": item.text for item in detail.subquestions})
        return itens
    if question.subquestions:
        return {f"{question.code}[{item.code}]": item.text for item in question.subquestions}
    if question.alternatives:
        return {f"{question.code}[{item.code}]": item.text for item in question.alternatives}
    return {question.code: _clean(question.text())}


def _criterio_padrao_item(texto_item: str) -> str:
    return f"A evidência demonstra diretamente a ocorrência da afirmação: {texto_item}"


def _clean(texto: str) -> str:
    return " ".join(texto.replace("**", "").split())


def _bullet_list(items: list[str]) -> list[str]:
    return [f"- {item}" for item in items]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Gera prompts binarios de achados a partir de catalogo YAML enxuto.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    build = subparsers.add_parser("build")
    build.add_argument("catalogo")
    build.add_argument("questionario")
    build.add_argument("destino")
    args = parser.parse_args(argv)
    if args.command == "build":
        build_prompt_set(args.catalogo, args.questionario, args.destino)
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
