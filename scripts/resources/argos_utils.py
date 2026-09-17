import re
import os
import io
import tempfile
import zipfile
import pandas as pd
import jinja2
from jinja2 import Environment, BaseLoader, StrictUndefined
from google.genai import types
from docxtpl import InlineImage
from docx.shared import Mm, Pt
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import logging
from datetime import date

def detect_header(filepath, sheet_name=0, required_columns=None):
    """
    Detecta a linha de cabeçalho em um arquivo Excel procurando pelas colunas obrigatórias.
    Retorna o índice da linha (0-based) ou levanta ValueError se não encontrar.
    """
    if not required_columns:
        return 0 # Default to 0 if no columns specified

    # Read a sample of rows to search for header
    try:
        # Ler as primeiras 20 linhas sem cabeçalho para inspecionar
        df_sample = pd.read_excel(filepath, sheet_name=sheet_name, header=None, nrows=20)
    except Exception as e:
        filename = getattr(filepath, 'name', str(filepath))
        raise ValueError(f"Erro ao ler amostra do arquivo '{filename}' aba '{sheet_name}': {e}")

    required_set = set(c.lower().strip() for c in required_columns)

    for i, row in df_sample.iterrows():
        # Convert row values to strings, lowercased and stripped, filtering out NaNs
        row_values = set(str(val).lower().strip() for val in row.values if pd.notna(val))

        # Check if all required columns are present in this row
        if required_set.issubset(row_values):
            return i

    filename = getattr(filepath, 'name', str(filepath))
    raise ValueError(f"Não foi possível detectar o cabeçalho na aba '{sheet_name}' do arquivo '{filename}'. Colunas esperadas: {', '.join(required_columns)}")

def validar_schema(df, required_columns):
    """
    Valida se as colunas obrigatórias estão presentes no DataFrame.
    Lança ValueError se faltar alguma.
    """
    if not required_columns:
        return

    df_cols = set(c.lower().strip() for c in df.columns)
    req_cols = set(c.lower().strip() for c in required_columns)

    missing = req_cols - df_cols
    if missing:
        raise ValueError(f"Colunas obrigatórias ausentes: {', '.join(missing)}")

def carregar_dados(filepath, sheet_name=0, skiprows=None, required_columns=None):
    """
    Lê um arquivo Excel e retorna um DataFrame.

    Args:
        filepath: Caminho ou objeto do arquivo.
        sheet_name: Nome ou índice da aba.
        skiprows: (Opcional) Número de linhas para pular. Se None e required_columns for fornecido, tenta detectar.
        required_columns: (Opcional) Lista de nomes de colunas obrigatórias para detecção e validação.
    """
    try:
        # Se skiprows não for informado mas tivermos colunas obrigatórias, tenta detectar
        if skiprows is None and required_columns:
            skiprows = detect_header(filepath, sheet_name, required_columns)
        elif skiprows is None:
            skiprows = 0 # Default legacy behavior

        # Carrega o dataframe final
        na_values_sem_na = ['', '#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan',
                            '1.#IND', '1.#QNAN', '<NA>', 'NA', 'NULL', 'NaN', 'n/a', 'nan', 'null']
        df = pd.read_excel(filepath, sheet_name=sheet_name, skiprows=skiprows,
                           keep_default_na=False, na_values=na_values_sem_na)

        # Normaliza nomes das colunas para strip (remove espaços extras)
        df.columns = [str(c).strip() for c in df.columns]

        # Aplica map apenas nas células de string
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

        # Valida schema se solicitado
        if required_columns:
            # A validação aqui é case-insensitive por segurança,
            # mas idealmente os nomes devem bater exato ou normalizarmos tudo.
            # Para garantir robustez, vamos validar contra os nomes normalizados (strip).
            # A função validar_schema já faz lower().strip() para comparar.
            validar_schema(df, required_columns)

        return df

    except Exception as e:
        filename = getattr(filepath, 'name', str(filepath))
        raise ValueError(f"Erro ao carregar a planilha '{sheet_name}' do arquivo '{filename}': {e}")


def aplicar_variaveis_temporarias(fontes, variaveis):
    """Materializa colunas derivadas nas fontes apenas durante o processamento."""
    if variaveis is None or variaveis.empty:
        return fontes

    required = {'id', 'id_fonte_informacao', 'nome', 'expressao'}
    missing = required - set(variaveis.columns)
    if missing:
        raise ValueError(
            "Colunas obrigatórias ausentes em Variáveis Temporárias: "
            + ", ".join(sorted(missing))
        )

    nomes_criados = set()
    colunas_por_fonte = {}
    for _, row in variaveis.iterrows():
        variable_id = str(row['id']).strip()
        source_id = str(row['id_fonte_informacao']).strip()
        name = str(row['nome']).strip()
        expression = str(row['expressao']).strip()
        source = fontes.get(source_id)

        if source is None:
            raise ValueError(
                f"Variável temporária {variable_id} refere-se à fonte inexistente {source_id!r}."
            )
        if source.info is None:
            raise ValueError(
                f"A fonte {source_id!r} não foi carregada para calcular a variável {variable_id}."
            )
        if not name or name.lower() == 'nan':
            raise ValueError(f"Variável temporária {variable_id} sem nome.")
        if name in nomes_criados or name in source.info.columns:
            raise ValueError(f"Nome de variável temporária duplicado ou já existente: {name!r}.")

        colunas_fonte = colunas_por_fonte.setdefault(source_id, {})
        contexto = pd.concat([source.info, pd.DataFrame(colunas_fonte, index=source.info.index)], axis=1)
        prepared = expression
        for column in sorted(contexto.columns, key=lambda value: len(str(value)), reverse=True):
            column = str(column)
            if not re.fullmatch(r"[A-Za-z_]\w*", column):
                prepared = prepared.replace(column, f"`{column}`")

        try:
            colunas_fonte[name] = contexto.eval(prepared, engine='python')
        except Exception as exc:
            raise ValueError(
                f"Não foi possível calcular a variável temporária {variable_id} ({name}): {exc}"
            ) from exc
        nomes_criados.add(name)

    for source_id, colunas in colunas_por_fonte.items():
        if colunas:
            source = fontes[source_id]
            source.info = pd.concat([source.info, pd.DataFrame(colunas, index=source.info.index)], axis=1)

    return fontes

def get_variaveis_template(template_md_content):
    """Coleta as variáveis presentes em um template Jinja2."""
    if not template_md_content:
        return set()
    env = Environment(loader=BaseLoader())
    ast = env.parse(template_md_content)
    return jinja2.meta.find_undeclared_variables(ast)

class StreamlitLogHandler(logging.Handler):
    """Handler de logging customizado para exibir logs do pypandoc no Streamlit."""
    def __init__(self, container):
        super().__init__()
        self.container = container
        self.records = []

    def emit(self, record):
        self.records.append(record)
        msg = self.format(record)
        self.container.warning(msg)


def parse_expression(expression):
    tokens = []
    current_token = ''

    for char in expression:
        if char in {'|', '&', '~', '(', ')'}:
            if current_token:
                tokens.append(current_token.strip())
                current_token = ''
            tokens.append(char)
        else:
            current_token += char

    if current_token:
        tokens.append(current_token.strip())

    # Remove empty tokens that might result from spaces like "A | B" -> "A", "", "|", "", "B"
    return [t for t in tokens if t]

def infix_to_rpn(tokens):
    precedence = {'~': 3, '&': 2, '|': 1}
    output = []
    stack = []

    for token in tokens:
        if token == '(':
            # Abre parêntese
            stack.append(token)
        elif token == ')':
            # Fecha parêntese
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # Remove o '('
        elif token in precedence:
            # Operador
            while stack and stack[-1] in precedence and precedence[stack[-1]] >= precedence[token]:
                output.append(stack.pop())
            stack.append(token)
        else:
            output.append(token)

    while stack:
        output.append(stack.pop())

    return list(filter(lambda x: x != '', output))

def safe_compare(value, condition):
    """
    Compara um valor com uma condição de forma segura (sem eval).
    Suporta: >, <, >=, <=, ==, != e igualdade implícita.
    """
    condition = str(condition).strip()
    value_str = str(value).strip()

    # Operadores suportados
    operators = {
        '>=': lambda x, y: x >= y,
        '<=': lambda x, y: x <= y,
        '!=': lambda x, y: x != y,
        '==': lambda x, y: x == y,
        '>': lambda x, y: x > y,
        '<': lambda x, y: x < y
    }

    # Tenta encontrar um operador no início da condição
    # Ordenamos chaves pelo tamanho decrescente para pegar >= antes de >
    for op_symbol in sorted(operators.keys(), key=len, reverse=True):
        if condition.startswith(op_symbol):
            target_str = condition[len(op_symbol):].strip()
            # Remove quotes if user added them for a number (e.g. > '5')
            target_clean = target_str.strip("'\"")

            # Tenta comparação numérica
            try:
                val_num = float(value)
                target_num = float(target_clean) # Convert cleaned target
                return operators[op_symbol](val_num, target_num)
            except ValueError:
                # Comparação de strings (remove aspas se houver)
                # target_clean já está limpo
                return operators[op_symbol](value_str, target_clean)

    # Se não houver operador, assume igualdade (==)
    # Remove aspas se o usuário tiver colocado (ex: 'Sim')
    target_clean = condition.strip("'\"")
    # Tenta comparar como número se ambos forem numéricos e a condição for apenas um número
    try:
        val_num = float(value)
        target_num = float(target_clean)
        return val_num == target_num
    except ValueError:
        pass

    return value_str == target_clean

def avalia_logica(expressao, contexto):
    """
    Avalia uma expressão lógica (ex: 'AV01 & AV02') dado um contexto
    (dicionário de resultados { 'AV01': True, ... }).
    """
    if not expressao:
        return False

    tokens = parse_expression(str(expressao))
    rpn = infix_to_rpn(tokens)

    pilha = []

    for token in rpn:
        if token == '|':
            if len(pilha) < 2: raise ValueError("Expressão mal formada (operador |)")
            y = pilha.pop()
            x = pilha.pop()
            pilha.append(x or y)
        elif token == '&':
            if len(pilha) < 2: raise ValueError("Expressão mal formada (operador &)")
            y = pilha.pop()
            x = pilha.pop()
            pilha.append(x and y)
        elif token == '~':
            if len(pilha) < 1: raise ValueError("Expressão mal formada (operador ~)")
            x = pilha.pop()
            pilha.append(not x)
        else:
            # Token é uma chave no contexto (ex: AV01)
            val = contexto.get(token, False) # Default False se não achar
            pilha.append(val)

    if len(pilha) == 1:
        return pilha[0]
    else:
        # Se sobrou mais de um item, expressão pode estar incompleta, mas retornamos o topo
        return pilha[0]

def avalia_expressao(expressao_achado, situacao_encontrada, debug=False):
    expressao_achado = str(expressao_achado)
    # situacao_encontrada pode ser int/float/str, mantemos o tipo original para safe_compare tentar converter

    # Alternativas exportadas pelo LimeSurvey podem conter marcadores como
    # "f)" e outros parênteses que fazem parte do valor literal. Nesse caso,
    # somente operadores separados por espaços e os delimitadores externos
    # são estruturais; a pontuação interna deve permanecer na comparação.
    if re.search(r"(?:^|[~(])\s*[a-z]\)\s", expressao_achado, flags=re.IGNORECASE):
        def avaliar_alternativa(expressao):
            expressao = expressao.strip()
            if expressao.startswith('~(') and expressao.endswith(')'):
                return not avaliar_alternativa(expressao[2:-1])
            if (
                expressao.startswith('(')
                and expressao.endswith(')')
                and (' | ' in expressao or ' & ' in expressao)
            ):
                expressao = expressao[1:-1].strip()
            if ' | ' in expressao:
                return any(avaliar_alternativa(item) for item in expressao.split(' | '))
            if ' & ' in expressao:
                return all(avaliar_alternativa(item) for item in expressao.split(' & '))
            if expressao.startswith('~'):
                return not avaliar_alternativa(expressao[1:])
            return safe_compare(situacao_encontrada, expressao)

        resultado = avaliar_alternativa(expressao_achado)
        if debug:
            print(f"Avalia alternativa literal: '{expressao_achado}' vs '{situacao_encontrada}' -> {resultado}")
        return resultado

    parsed_tokens = parse_expression(expressao_achado)
    tokens = infix_to_rpn(parsed_tokens)

    if debug:
        print(f"Avalia Expressão: '{expressao_achado}' vs '{situacao_encontrada}'")
        print(f"Tokens RPN: {tokens}")

    pilha = []

    for token in tokens:
        if token == '|':
            if len(pilha) < 2: raise ValueError("Expressão mal formada (operador |)")
            y = pilha.pop()
            x = pilha.pop()
            pilha.append(x or y)
        elif token == '&':
            if len(pilha) < 2: raise ValueError("Expressão mal formada (operador &)")
            y = pilha.pop()
            x = pilha.pop()
            pilha.append(x and y)
        elif token == '~':
            if len(pilha) < 1: raise ValueError("Expressão mal formada (operador ~)")
            x = pilha.pop()
            pilha.append(not x)
        else:
            # O token é uma condição simples (ex: "> 10" ou "Sim")
            # Removemos o '.' no final que às vezes vem da planilha
            condition = re.sub(r'\.$', '', token)

            # Usamos safe_compare para validar
            resultado = safe_compare(situacao_encontrada, condition)

            if debug:
                print(f"    Comparando: Val='{situacao_encontrada}' Cond='{condition}' -> {resultado}")

            pilha.append(resultado)

    if len(pilha) >= 1:
        if debug:
            print('        Resultado Final:', pilha[0])
        return pilha[0]
    else:
        raise ValueError("Expressão lógica inválida ou vazia")

def processa_imagens_contexto(contexto, context_files_path_map, template_type, base_docx=None):
    """
    Substitui nomes de arquivos de imagem no contexto pelos caminhos ou objetos de imagem apropriados.

    Returns:
        tuple: (contexto_atualizado, lista_de_avisos)
    """
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
    warnings = []

    # Itera sobre uma cópia dos itens para permitir a modificação do dicionário
    for key, value in list(contexto.items()):
        if isinstance(value, str) and value.lower().endswith(image_extensions):
            if value in context_files_path_map:
                image_path = context_files_path_map[value]
                if template_type == 'docx':
                    if base_docx is None:
                        raise ValueError("O objeto base_docx é necessário para processar imagens em templates .docx")
                    # Para docx, substitui pelo objeto InlineImage
                    contexto[key] = InlineImage(base_docx, image_path, width=Mm(160))
                elif template_type == 'md':
                    # Para markdown, substitui pelo caminho do arquivo
                    contexto[key] = image_path
            else:
                warnings.append(f"Arquivo de imagem '{value}' para a variável '{key}' não encontrado. A imagem não será inserida.")
                contexto[key] = f"[Imagem '{value}' não encontrada]"

    return contexto, warnings

def cross_ref_figuras(template_str: str) -> str:
    """
    Processa um template de texto para numerar automaticamente as referências
    de figuras e modificar as legendas das imagens, preservando os
    atributos de formatação do Pandoc (ex: {width=10cm}).

    A função opera em duas passadas:

    1. Mapeamento:
       Encontra todas as declarações ({#fig:ID#}) e referências ([@fig:ID])
       na ordem em que aparecem para criar um mapa de numeração
       (ex: {'fig_01': 1, 'fig_02': 2}).

    2. Substituição:
       - Substitui referências de texto (ex: [@fig:fig_01] -> "Figura 1").
       - Encontra as linhas de imagem (ex: ![Texto]({{path}}){attrs}{#fig:ID#})
         e as substitui por "![Figura 1 - Texto]({{path}}){attrs}".
    """

    # --- Passa 1: Mapeamento ---

    figura_map = {}
    contador = 1

    # Regex combinada (NÃO MUDA)
    regex_combinado = r"(?:\{#fig:([^#]+)#\}|\[@fig:([^\]]+)\])"

    for match in re.finditer(regex_combinado, template_str):
        id_declaracao = match.group(1)
        id_referencia = match.group(2)
        fig_id = id_declaracao if id_declaracao else id_referencia

        if fig_id and fig_id not in figura_map:
            figura_map[fig_id] = contador
            contador += 1

    if not figura_map:
        return template_str

    # --- Passa 2: Substituições ---

    texto_processado = template_str

    # 1. Substituir referências de TEXTO (NÃO MUDA)
    regex_ref_texto = r"\[@fig:([^\]]+)\]"

    def substituir_ref_texto(match):
        fig_id = match.group(1)
        if fig_id in figura_map:
            return f"Figura {figura_map[fig_id]}"
        return match.group(0)

    texto_processado = re.sub(regex_ref_texto, substituir_ref_texto, texto_processado)

    # 2. Modificar linhas de IMAGEM e remover tags de declaração (MODIFICADO)

    # Regex ATUALIZADA:
    # Grupo 1: ![ (alt text) ]
    # Grupo 2: (path)
    # Grupo 3: (bloco de atributos opcional, ex: {width=10cm})
    # Grupo 4: {#fig: (ID) #}
    regex_imagem_decl = r"!\[([^\]]*)\](\([^)]*\))\s*(\{[^}]*\})?\s*\{#fig:([^#]+)#\}"

    def modificar_legenda_imagem(match):
        alt_text = match.group(1)
        path = match.group(2)
        attributes = match.group(3)  # O bloco {width=10cm}
        fig_id = match.group(4)

        if fig_id in figura_map:
            numero = figura_map[fig_id]

            # Se o grupo de atributos não for encontrado (None),
            # o transformamos em uma string vazia.
            attr_str = attributes if attributes else ""

            # Reconstrói a string: ![Figura X - Texto](path){atributos}
            return f"![Figura {numero} - {alt_text}]{path}{attr_str}"

        return match.group(0) # Failsafe

    texto_processado = re.sub(regex_imagem_decl, modificar_legenda_imagem, texto_processado)

    return texto_processado

def processar_quebras_pagina(template_str: str) -> str:
    """
    Substitui o comando LaTeX \newpage por um bloco Raw OpenXML
    que o Pandoc entende e converte corretamente para quebra de página no Word.
    """
    # Bloco nativo do OpenXML para quebra de página
    pagebreak_openxml = "\n```{=openxml}\n<w:p><w:r><w:br w:type=\"page\"/></w:r></w:p>\n```\n"

    # Regex para encontrar \newpage (aceitando espaços extras ou chaves vazias opcionais)
    regex_newpage = r"\\newpage(?:\{\})?"

    return re.sub(regex_newpage, pagebreak_openxml, template_str)

def inserir_campo_sumario_docx(template_str: str, titulo: str = "SUMÁRIO", profundidade: int = 3) -> str:
    """
    Substitui o bloco Markdown ``::: {.toc}`` por um campo TOC nativo do Word.

    O Pandoc trata ``::: {.toc}`` como um Div comum e não como marcador de
    posição do sumário em DOCX. Este pré-processamento materializa o sumário
    no ponto indicado usando Raw OpenXML.
    """
    marcador_toc = r"(?ms)^:::\s*\{\.toc\}\s*\n\s*:::\s*$"
    if not re.search(marcador_toc, template_str):
        return template_str

    depth_match = re.search(r"(?m)^toc-depth:\s*(\d+)\s*$", template_str)
    if depth_match:
        profundidade = int(depth_match.group(1))

    # Evita que o Pandoc gere um segundo sumário no início do DOCX.
    template_str = re.sub(r"(?m)^toc:\s*true\s*\n", "", template_str)
    template_str = re.sub(r"(?m)^table-of-contents:\s*true\s*\n", "", template_str)

    toc_openxml = f"""
```{{=openxml}}
<w:p>
  <w:pPr>
    <w:pStyle w:val="TOCHeading"/>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="Cambria" w:hAnsi="Cambria" w:eastAsia="Cambria" w:cs="Cambria"/>
      <w:b/>
      <w:bCs/>
      <w:color w:val="2F5496"/>
      <w:sz w:val="32"/>
      <w:szCs w:val="32"/>
    </w:rPr>
    <w:t>{titulo}</w:t>
  </w:r>
</w:p>
<w:p>
  <w:r>
    <w:fldChar w:fldCharType="begin" w:dirty="true"/>
  </w:r>
  <w:r>
    <w:instrText xml:space="preserve">TOC \\o "1-{profundidade}" \\h \\z \\u</w:instrText>
  </w:r>
  <w:r>
    <w:fldChar w:fldCharType="separate"/>
  </w:r>
  <w:r>
    <w:t>O sumário será atualizado ao abrir o documento no Word.</w:t>
  </w:r>
  <w:r>
    <w:fldChar w:fldCharType="end"/>
  </w:r>
</w:p>
```
""".strip()

    return re.sub(
        marcador_toc,
        lambda _: toc_openxml,
        template_str,
    )

def _marcar_atualizacao_campos_entries(entries: dict[str, bytes]) -> dict[str, bytes]:
    settings_name = "word/settings.xml"
    if settings_name in entries:
        settings_text = entries[settings_name].decode("utf-8")
    else:
        settings_text = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            '</w:settings>'
        )

    update_fields = '<w:updateFields w:val="true"/>'
    if "<w:updateFields" in settings_text:
        settings_text = re.sub(
            r'<w:updateFields\b[^>]*/>',
            update_fields,
            settings_text,
            count=1,
        )
        settings_text = re.sub(
            r'<w:updateFields\b[^>]*>.*?</w:updateFields>',
            update_fields,
            settings_text,
            count=1,
            flags=re.DOTALL,
        )
    elif "</w:settings>" in settings_text:
        settings_text = settings_text.replace("</w:settings>", update_fields + "</w:settings>", 1)
    else:
        raise ValueError(f"settings.xml inválido em {docx_path}: elemento </w:settings> ausente")

    entries[settings_name] = settings_text.encode("utf-8")
    return entries

def marcar_atualizacao_campos_docx_bytes(docx_bytes: bytes) -> bytes:
    """
    Retorna bytes de um DOCX com ``w:updateFields`` marcado.
    """
    with zipfile.ZipFile(io.BytesIO(docx_bytes), "r") as source:
        entries = {name: source.read(name) for name in source.namelist()}

    entries = _marcar_atualizacao_campos_entries(entries)

    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as target:
        for name, data in entries.items():
            target.writestr(name, data)
    return output.getvalue()

def marcar_atualizacao_campos_docx(docx_path: str) -> None:
    """
    Adiciona ``w:updateFields`` ao DOCX para o Word atualizar campos ao abrir.

    O Pandoc não calcula a paginação final do Word; páginas do sumário dependem
    do mecanismo de layout do editor. Esta marcação orienta o Word a atualizar
    o campo TOC quando o arquivo for aberto.
    """
    with zipfile.ZipFile(docx_path, "r") as source:
        entries = {name: source.read(name) for name in source.namelist()}

    entries = _marcar_atualizacao_campos_entries(entries)

    fd, tmp_name = tempfile.mkstemp(suffix=".docx", dir=os.path.dirname(docx_path) or None)
    os.close(fd)
    try:
        with zipfile.ZipFile(tmp_name, "w", compression=zipfile.ZIP_DEFLATED) as target:
            for name, data in entries.items():
                target.writestr(name, data)
        os.replace(tmp_name, docx_path)
    finally:
        if os.path.exists(tmp_name):
            os.remove(tmp_name)

def cross_ref_tabelas(template_str: str) -> str:
    """
    Processa um template de texto para numerar automaticamente as referências
    de tabelas e modificar as legendas das tabelas, seguindo o padrão de
    cross_ref_figuras.
    """

    # --- Passa 1: Mapeamento ---

    tabela_map = {}
    contador = 1

    # Regex combinada para encontrar declarações e referências
    regex_combinado = r"(?:\{#tbl:([^#]+)#\}|\[@tbl:([^\]]+)\])"

    for match in re.finditer(regex_combinado, template_str):
        id_declaracao = match.group(1)
        id_referencia = match.group(2)
        tbl_id = id_declaracao if id_declaracao else id_referencia

        if tbl_id and tbl_id not in tabela_map:
            tabela_map[tbl_id] = contador
            contador += 1

    if not tabela_map:
        return template_str

    # --- Passa 2: Substituições ---

    texto_processado = template_str

    # 1. Substituir referências de TEXTO
    regex_ref_texto = r"\[@tbl:([^\]]+)\]"

    def substituir_ref_texto(match):
        tbl_id = match.group(1)
        if tbl_id in tabela_map:
            return f"Tabela {tabela_map[tbl_id]}"
        return match.group(0)

    texto_processado = re.sub(regex_ref_texto, substituir_ref_texto, texto_processado)

    # 2. Modificar legendas de Tabela
    # Padrão esperado: ": Legenda da Tabela {#tbl:ID#}" OU "Table: Legenda..."
    # (?m) habilita multiline para ^ coincidir com início da linha
    regex_legenda = r"(?m)^([ \t]*)(:|Table:)\s*(.*?)\s*\{#tbl:([^#]+)#\}"

    def modificar_legenda_tabela(match):
        indentacao = match.group(1)
        prefix = match.group(2) # ":" ou "Table:"
        caption = match.group(3)
        tbl_id = match.group(4)

        if tbl_id in tabela_map:
            numero = tabela_map[tbl_id]
            return f"{indentacao}{prefix} Tabela {numero} - {caption}"

        return match.group(0)

    texto_processado = re.sub(regex_legenda, modificar_legenda_tabela, texto_processado)

    return texto_processado


def substituir_underline_preview(text: str) -> str:
    """
    Substitui texto envolvido por __ pela sintaxe de underline HTML:
    __texto__ -> <u>texto</u>
    """
    return re.sub(r"__(.+?)__", r"<u>\1</u>", text)


def substituir_underline_pandoc(text: str) -> str:
    """
    Substitui texto envolvido por __ pela sintaxe de underline do Pandoc:
    __texto__ -> [texto]{.underline}
    """
    return re.sub(r"__(.+?)__", r"[\1]{.underline}", text)


def avalia_gemini(client, prompt_text: str, modelo, temperature, response_format_choice, file_objects = []):
    """
    Chama a API do Gemini com a configuração apropriada.
    Retorna a resposta do modelo e uma mensagem de erro (se houver).
    """
    try:
        contents = [prompt_text] + file_objects
        # st.info(f'Avaliando com o modelo {modelo}...') # Comentado para evitar chamadas Streamlit em utils

        generation_config = types.GenerateContentConfig(
            max_output_tokens=65536, # Usando o valor sugerido de 65536
            temperature=temperature,
        )

        if response_format_choice in ('Estruturada', 'JSON'):
            generation_config.response_mime_type = 'application/json'

        # Cria o conteúdo para a API
        response = client.models.generate_content(
            model=modelo,
            contents=contents,
            config=generation_config
        )

        return response, None

    except Exception as e:
        return None, f"Erro ao chamar a API Gemini: {e}"

def data_hoje_abnt():
    hoje = date.today()

    # Lista de meses ABNT (Jan. Fev. Mar. Abr. Maio Jun. Jul. Ago. Set. Out. Nov. Dez.)
    # Note que 'maio' não tem ponto e é minúsculo na citação direta,
    # mas aqui usaremos minúsculo padrão.
    meses_abnt = {
        1: 'jan.', 2: 'fev.', 3: 'mar.', 4: 'abr.', 5: 'maio', 6: 'jun.',
        7: 'jul.', 8: 'ago.', 9: 'set.', 10: 'out.', 11: 'nov.', 12: 'dez.'
    }

    dia = hoje.day
    mes = meses_abnt[hoje.month]
    ano = hoje.year

    return f"{dia} {mes} {ano}"

def data_hoje():
    return date.today().strftime("%d/%m/%Y")

def is_tabela_plano_acao(table) -> bool:
    """Verifica estruturalmente se a tabela é a tabela do Plano de Ação pelo cabeçalho."""
    if len(table.rows) == 0:
        return False
    row0_texts = [cell.text.strip().lower() for cell in table.rows[0].cells]
    return any("medida proposta" in t for t in row0_texts) or (
        any("achado" in t for t in row0_texts) and any("tipo" in t for t in row0_texts) and any("quem" in t for t in row0_texts)
    )


def configurar_tabela_plano_acao(table, total_width_dxa=9072):
    """
    Aplica layout fixo e larguras otimizadas por coluna para a tabela do Plano de Ação.
    Proporções calibradas (total 16,00 cm = 9072 dxa):
    - Achado: 10% (1,60 cm / 907 dxa)
    - Tipo: 15% (2,40 cm / 1361 dxa)
    - Medida proposta: 38% (6,08 cm / 3448 dxa)
    - Avaliação de viabilidade: 15% (2,40 cm / 1361 dxa)
    - Quem?: 11% (1,76 cm / 998 dxa)
    - Quando?: 11% (1,76 cm / 997 dxa)
    """
    from docx.shared import Cm
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    col_dxas = [907, 1361, 3448, 1361, 998, 997]
    col_widths = [Cm(1.60), Cm(2.40), Cm(6.08), Cm(2.40), Cm(1.76), Cm(1.76)]

    table.autofit = False

    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        for l in tblPr[0].xpath('w:tblLayout'):
            tblPr[0].remove(l)
        layout = OxmlElement('w:tblLayout')
        layout.set(qn('w:type'), 'fixed')
        tblPr[0].append(layout)

        for w in tblPr[0].xpath('w:tblW'):
            tblPr[0].remove(w)
        tblW = OxmlElement('w:tblW')
        tblW.set(qn('w:type'), 'dxa')
        tblW.set(qn('w:w'), str(total_width_dxa))
        tblPr[0].append(tblW)

    tblGrid = table._element.xpath('w:tblGrid')
    if tblGrid:
        table._element.remove(tblGrid[0])
    new_grid = OxmlElement('w:tblGrid')
    for dxa in col_dxas:
        gc = OxmlElement('w:gridCol')
        gc.set(qn('w:w'), str(dxa))
        new_grid.append(gc)
    if tblPr:
        table._element.insert(table._element.index(tblPr[0]) + 1, new_grid)

    for row in table.rows:
        for i, cell in enumerate(row.cells):
            if i < len(col_widths):
                cell.width = col_widths[i]
                tcPr = cell._element.get_or_add_tcPr()
                for w in tcPr.xpath('w:tcW'):
                    tcPr.remove(w)
                tcW = OxmlElement('w:tcW')
                tcW.set(qn('w:type'), 'dxa')
                tcW.set(qn('w:w'), str(col_dxas[i]))
                tcPr.append(tcW)


def aplicar_estilo_tabelas(docx_path, font_name='Calibri', header_size=10, body_size=9):
    """
    Aplica estilos específicos às tabelas de um arquivo DOCX:
    - Cabeçalho: Fonte parametrizada (padrão Calibri), tamanho parametrizado (padrão 10)
    - Corpo: Fonte parametrizada (padrão Calibri), tamanho parametrizado (padrão 9)
    - Alinhamento: Justificado para todo o conteúdo
    - Plano de Ação: Layout fixo com larguras otimizadas (não submete a autofit)
    - Demais tabelas: autofit = True
    """
    from docx.enum.table import WD_TABLE_ALIGNMENT
    doc = Document(docx_path)
    for table in doc.tables:
        table.alignment = WD_TABLE_ALIGNMENT.CENTER

        if is_tabela_plano_acao(table):
            configurar_tabela_plano_acao(table)
        else:
            table.autofit = True

        for i, row in enumerate(table.rows):
            is_header = (i == 0)
            font_size = Pt(header_size) if is_header else Pt(body_size)

            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
                    for run in paragraph.runs:
                        run.font.name = font_name
                        run.font.size = font_size

    doc.save(docx_path)


def aplicar_fonte_justificativas_avaliacao(docx_path, tamanho=8):
    """Aplica fonte reduzida somente aos subitens de justificativa das evidências."""
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    def paragrafos_tabela(tabela):
        for linha in tabela.rows:
            for celula in linha.cells:
                yield from celula.paragraphs
                for tabela_interna in celula.tables:
                    yield from paragrafos_tabela(tabela_interna)

    documento = Document(docx_path)
    paragrafos = list(documento.paragraphs)
    for tabela in documento.tables:
        paragrafos.extend(paragrafos_tabela(tabela))

    tamanho_meios_pontos = str(int(tamanho * 2))
    for paragrafo in paragrafos:
        if not paragrafo.text.strip().startswith("Justificativa da avaliação:"):
            continue

        for trecho in paragrafo.runs:
            trecho.font.size = Pt(tamanho)

        propriedades = paragrafo._p.get_or_add_pPr()
        propriedades_execucao = propriedades.find(qn("w:rPr"))
        if propriedades_execucao is None:
            propriedades_execucao = OxmlElement("w:rPr")
            propriedades.append(propriedades_execucao)
        for nome in ("w:sz", "w:szCs"):
            elemento = propriedades_execucao.find(qn(nome))
            if elemento is None:
                elemento = OxmlElement(nome)
                propriedades_execucao.append(elemento)
            elemento.set(qn("w:val"), tamanho_meios_pontos)

    documento.save(docx_path)


def configurar_paginacao_headings(doc):
    """Configura keep_with_next nos títulos e widowControl no texto regular."""
    for p in doc.paragraphs:
        style_name = p.style.name or ''
        is_heading = (
            style_name.startswith(('Heading', 'heading', 'Título', 'Title', 'Subtitle')) or
            bool(p._element.xpath('./w:pPr/w:outlineLvl'))
        )
        if is_heading:
            p.paragraph_format.keep_with_next = True
        else:
            p.paragraph_format.widow_control = True


def configurar_figuras_e_fontes(doc):
    """
    Garante o agrupamento estrutural Legenda + Imagem + Fonte:
    - Legenda (parágrafo anterior à imagem): keep_with_next = True
    - Imagem: keep_with_next = True quando seguida de Fonte
    - Fonte: keep_with_next = False (não prende o parágrafo seguinte)
    - Limite genérico de altura de imagem (~21 cm = 7.560.000 EMUs) para caber na página útil.
    """
    paragraphs = doc.paragraphs
    for idx, p in enumerate(paragraphs):
        has_drawing = bool(p._element.xpath('.//w:drawing') or p._element.xpath('.//w:graphic'))
        if not has_drawing:
            continue

        # Legenda acima da imagem
        if idx > 0:
            prev_p = paragraphs[idx - 1]
            prev_style = prev_p.style.name or ''
            prev_text = prev_p.text.strip()
            if 'Caption' in prev_style or 'Legenda' in prev_style or prev_text.startswith('Figura '):
                prev_p.paragraph_format.keep_with_next = True

        # Fonte abaixo da imagem
        if idx < len(paragraphs) - 1:
            next_p = paragraphs[idx + 1]
            next_style = next_p.style.name or ''
            next_text = next_p.text.strip()
            if 'FonteImagem' in next_style or next_text.startswith('(Fonte:'):
                p.paragraph_format.keep_with_next = True
                next_p.paragraph_format.keep_with_next = False

        # Altura máxima da imagem para caber na página útil
        extents = p._element.xpath('.//wp:extent')
        for ext in extents:
            cy = int(ext.get('cy', 0))
            max_cy = 7560000  # 21 cm em EMUs
            if cy > max_cy:
                cx = int(ext.get('cx', 0))
                ratio = max_cy / cy
                ext.set('cy', str(max_cy))
                ext.set('cx', str(int(cx * ratio)))


def configurar_tabelas_e_quebras(doc):
    """
    Configura paginação de tabelas:
    - Legenda imediatamente anterior vinculada à tabela (keepNext)
    - Cabeçalho repetido na primeira linha (tblHeader) e indivisível (cantSplit)
    - Política inteligente de quebra: linhas curtas mantidas inteiras (cantSplit);
      linhas longas (manifestações, justificativas) podem dividir entre páginas.
    - Tabela e fonte: fonte não prende parágrafo posterior; última linha curta vinculada à fonte.
    """
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    for tbl in doc.tables:
        if len(tbl.rows) == 0:
            continue

        # Legenda anterior vinculada à tabela
        tbl_el = tbl._element
        prev_el = tbl_el.getprevious()
        if prev_el is not None and prev_el.tag.endswith('p'):
            pPr = prev_el.get_or_add_pPr()
            if not pPr.xpath('w:keepNext'):
                pPr.append(OxmlElement('w:keepNext'))

        # Cabeçalho repetido na linha 0
        trPr0 = tbl.rows[0]._element.get_or_add_trPr()
        if not trPr0.xpath('w:tblHeader'):
            trPr0.append(OxmlElement('w:tblHeader'))
        if not trPr0.xpath('w:cantSplit'):
            trPr0.append(OxmlElement('w:cantSplit'))

        # Política de quebra de linhas do corpo da tabela
        for r_idx, row in enumerate(tbl.rows):
            if r_idx == 0:
                continue
            trPr = row._element.get_or_add_trPr()
            total_chars = sum(len(c.text.strip()) for c in row.cells)
            total_paras = sum(len(c.paragraphs) for c in row.cells)
            is_long = (total_chars > 250 or total_paras > 3)

            cant_splits = trPr.xpath('w:cantSplit')
            if is_long:
                for cs in cant_splits:
                    trPr.remove(cs)
            else:
                if not cant_splits:
                    trPr.append(OxmlElement('w:cantSplit'))

        # Fonte posterior vinculada à tabela
        next_el = tbl_el.getnext()
        if next_el is not None and next_el.tag.endswith('p'):
            style_els = next_el.xpath('.//w:pStyle')
            style_val = style_els[0].get(qn('w:val')) if style_els else ''
            text_nodes = next_el.xpath('.//w:t')
            text_content = ''.join(node.text for node in text_nodes).strip()
            is_source = ('FonteImagem' in style_val or text_content.startswith('(Fonte:'))
            if is_source:
                pPr_next = next_el.get_or_add_pPr()
                for kn in pPr_next.xpath('w:keepNext'):
                    pPr_next.remove(kn)

                last_row = tbl.rows[-1]
                last_row_chars = sum(len(c.text.strip()) for c in last_row.cells)
                if last_row_chars <= 200:
                    for cell in last_row.cells:
                        for p_cell in cell.paragraphs:
                            p_cell.paragraph_format.keep_with_next = True


def remover_paragrafos_vazios_residuais(doc):
    """
    Remove parágrafos vazios ou quebras residuais que criam páginas em branco ou espaçamento inútil:
    - Converte parágrafos vazios contendo apenas <w:br w:type="page"/> em page_break_before no parágrafo seguinte.
    - Remove parágrafos vazios residuais entre legenda e figura/tabela, ou entre figura/tabela e fonte.
    """
    paras = list(doc.paragraphs)
    for i, p in enumerate(paras):
        brs = p._element.xpath('.//w:br[@w:type="page"]')
        if brs and not p.text.strip():
            if i + 1 < len(paras):
                next_p = paras[i + 1]
                next_p.paragraph_format.page_break_before = True
                p._element.getparent().remove(p._element)

    i = 0
    while i < len(doc.paragraphs) - 1:
        p_curr = doc.paragraphs[i]
        if not p_curr.text.strip() and not p_curr._element.xpath('.//w:drawing'):
            prev_p = doc.paragraphs[i - 1] if i > 0 else None
            if prev_p and ('Caption' in (prev_p.style.name or '') or prev_p.text.strip().startswith(('Figura ', 'Tabela '))):
                p_curr._element.getparent().remove(p_curr._element)
                continue
        i += 1


def otimizar_paginacao_relatorio(docx_path):
    """
    Coordenador genérico de otimização editorial e de paginação do relatório DOCX:
    1. Configura keep_with_next em títulos e widowControl no texto regular.
    2. Agrupa e dimensiona Figuras, Legendas e Fontes.
    3. Configura paginação de tabelas (repetição de cabeçalhos, quebra inteligente de linhas).
    4. Aplica layout fixo e larguras proporcionais à tabela do Plano de Ação.
    5. Remove parágrafos vazios seguros e quebras de página vazias que geram páginas em branco.
    Função totalmente idempotente.
    """
    doc = Document(docx_path)

    configurar_paginacao_headings(doc)
    configurar_figuras_e_fontes(doc)
    configurar_tabelas_e_quebras(doc)

    for tbl in doc.tables:
        if is_tabela_plano_acao(tbl):
            configurar_tabela_plano_acao(tbl)

    remover_paragrafos_vazios_residuais(doc)

    doc.save(docx_path)


def evitar_quebra_elementos(docx_path):
    """
    Pós-processa o arquivo Word (.docx) para evitar que elementos visuais
    se separem de suas legendas, títulos ou fontes nas quebras de página.
    Delega para a rotina completa e idempotente otimizar_paginacao_relatorio.
    """
    otimizar_paginacao_relatorio(docx_path)

def apply_custom_style():
    """
    Aplica estilos CSS customizados para tornar a interface mais moderna e profissional.
    Deve ser chamado no início de cada página Streamlit.
    """
    import streamlit as st

    st.markdown("""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

        /*
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }*/

        /* Títulos */
        h1 {
            color: #004e92;
            font-weight: 700 !important;
            letter-spacing: -0.5px;
        }
        h2, h3 {
            color: #2c3e50;
            font-weight: 600 !important;
        }

        /* Sidebar Styling */
        /*section[data-testid="stSidebar"] {
            background-color: #f8f9fa;
            border-right: 1px solid #e9ecef;
        }*/

        /* Cards customizados (Simulação com markdown) */
        .card {
            background-color: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            margin-bottom: 1rem;
            border: 1px solid #e9ecef;
            transition: transform 0.2s ease;
        }
        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
        }
        .card h4 {
            color: #0068C9;
            margin-top: 0;
            font-weight: 600;
        }
        .card p {
            color: #6c757d;
            font-size: 0.95rem;
            margin-bottom: 0;
        }

        /* Botões */
        div.stButton > button {
            background-color: #0068C9;
            color: white;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            border: none;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: all 0.2s;
        }
        div.stButton > button:hover {
            background-color: #0056b3;
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        div.stButton > button:active {
            background-color: #004494;
        }

        /* File Uploader */
        section[data-testid="stFileUploader"] {
            border-radius: 10px;
            padding: 1rem;
            border: 1px dashed #ced4da;
            background-color: #fdfdfe;
        }

        /* Expander */
        .streamlit-expanderHeader {
            font-weight: 600;
            color: #495057;
            background-color: white;
            border-radius: 8px;
        }

        /* Mensagens de Sucesso/Info/Erro */
        .stAlert {
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }

        </style>
    """, unsafe_allow_html=True)

def create_card(title, content, icon=None):
    """Retorna o HTML para um card estilizado."""
    icon_html = f'<div style="font-size: 1.5rem; margin-bottom: 0.5rem;">{icon}</div>' if icon else ''
    return f"""
    <div class="card">
        {icon_html}
        <h4>{title}</h4>
        <p>{content}</p>
    </div>
    """
