; Outline panel: model structure plus every named definition.

; Paired sections, shown as e.g. "Part Bracket", "Step Load"
(part
  start: (keyword_block
    header: (keyword_line
      name: (keyword_name) @context
      parameter: (parameter
        name: (parameter_name) @_param
        value: (_) @name)))
  (#match? @_param "^(?i)name$")) @item

(assembly
  start: (keyword_block
    header: (keyword_line
      name: (keyword_name) @context
      parameter: (parameter
        name: (parameter_name) @_param
        value: (_) @name)))
  (#match? @_param "^(?i)name$")) @item

(instance
  start: (keyword_block
    header: (keyword_line
      name: (keyword_name) @context
      parameter: (parameter
        name: (parameter_name) @_param
        value: (_) @name)))
  (#match? @_param "^(?i)name$")) @item

(step
  start: (keyword_block
    header: (keyword_line
      name: (keyword_name) @context
      parameter: (parameter
        name: (parameter_name) @_param
        value: (_) @name)))
  (#match? @_param "^(?i)name$")) @item

; Any other keyword block that names something: *Material, *Nset, *Elset,
; *Surface, *Amplitude, *Surface Interaction, ...
(keyword_block
  header: (keyword_line
    name: (keyword_name) @context
    parameter: (parameter
      name: (parameter_name) @_param
      value: (_) @name))
  (#match? @_param "^(?i)(name|nset|elset)$")
  (#not-match? @context "^(?i)(part|assembly|instance|step)$")) @item
