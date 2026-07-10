-- Converte o bloco Markdown
--
--   ::: {.toc}
--   :::
--
-- em um campo de sumario nativo do Word no ponto exato do documento.
-- Use com DOCX:
--
--   pandoc entrada.md -o saida.docx \
--     --reference-doc=scripts/resources/template-base-estilos-sigiloso.docx \
--     --lua-filter=scripts/resources/toc-marker.lua

local toc_depth = "3"
local toc_title = "SUMÁRIO"

local function stringify(value)
  if value == nil then
    return nil
  end
  return pandoc.utils.stringify(value)
end

local function escape_xml(text)
  text = text:gsub("&", "&amp;")
  text = text:gsub("<", "&lt;")
  text = text:gsub(">", "&gt;")
  text = text:gsub('"', "&quot;")
  text = text:gsub("'", "&apos;")
  return text
end

local function configure_from_meta(meta, has_toc_marker)
  local depth = stringify(meta["toc-depth"])
  if depth ~= nil and depth ~= "" then
    toc_depth = depth
  end

  local title = stringify(meta["toc-title"])
  if title ~= nil and title ~= "" then
    toc_title = title
  end

  if has_toc_marker then
    -- Evita duplicidade quando o Markdown contem "toc: true".
    -- Para uso com marcador local, nao passe --toc na linha de comando.
    meta["toc"] = nil
    meta["table-of-contents"] = nil
  end
  return meta
end

local function convert_toc_div(el)
  if not el.classes:includes("toc") then
    return nil
  end

  if FORMAT ~= "docx" then
    return el
  end

  local openxml = string.format([[
<w:p>
  <w:pPr>
    <w:pStyle w:val="TOCHeading"/>
  </w:pPr>
  <w:r>
    <w:t>%s</w:t>
  </w:r>
</w:p>
<w:p>
  <w:r>
    <w:fldChar w:fldCharType="begin" w:dirty="true"/>
  </w:r>
  <w:r>
    <w:instrText xml:space="preserve">TOC \o "1-%s" \h \z \u</w:instrText>
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
]], escape_xml(toc_title), escape_xml(toc_depth))

  return pandoc.RawBlock("openxml", openxml)
end

function Pandoc(doc)
  local has_toc_marker = false
  doc:walk({
    Div = function(el)
      if el.classes:includes("toc") then
        has_toc_marker = true
      end
      return nil
    end
  })

  doc.meta = configure_from_meta(doc.meta, has_toc_marker)
  return doc:walk({ Div = convert_toc_div })
end
