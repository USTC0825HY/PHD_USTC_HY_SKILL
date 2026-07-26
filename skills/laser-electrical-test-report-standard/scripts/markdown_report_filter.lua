local first_h1_seen = false

function Header(element)
  if element.level == 1 and not first_h1_seen then
    first_h1_seen = true
    return {}
  end
  if element.level > 1 then
    element.level = element.level - 1
  end
  return element
end

function CodeBlock(element)
  local is_mermaid = false
  for _, class_name in ipairs(element.classes) do
    if class_name == "mermaid" then
      is_mermaid = true
      break
    end
  end
  if not is_mermaid then
    return nil
  end
  local image_path = os.getenv("MERMAID_PNG")
  if image_path == nil or image_path == "" then
    return nil
  end
  local alt = { pandoc.Str("100 MHz 参考与 DDS 输出链路") }
  return {
    pandoc.Para({ pandoc.Image(alt, image_path) }),
    pandoc.Para({ pandoc.Str("图 1 100 MHz 参考与 DDS 输出链路") }),
  }
end

local function flatten_list(items, ordered)
  local blocks = pandoc.List()
  for index, item in ipairs(items) do
    local marker = ordered and (tostring(index) .. ".") or "•"
    local first = item[1]
    if first ~= nil and (first.t == "Para" or first.t == "Plain") then
      first.content:insert(1, pandoc.Space())
      first.content:insert(1, pandoc.Str(marker))
    else
      item:insert(1, pandoc.Para({ pandoc.Str(marker) }))
    end
    blocks:extend(item)
  end
  return blocks
end

function OrderedList(element)
  return flatten_list(element.content, true)
end

function BulletList(element)
  return flatten_list(element.content, false)
end
