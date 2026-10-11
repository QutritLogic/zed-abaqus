; Abaqus input file highlighting.
; Patterns are kept mutually exclusive so the result does not depend on
; whether an editor lets the first or the last matching pattern win.

(comment) @comment

; Ordinary *Keyword lines (the asterisk is coloured with the keyword).
(keyword_line
  "*" @keyword
  name: (keyword_name) @keyword @_kw
  (#not-match? @_kw "^(?i)(end[ \t]+)?(part|assembly|instance|step)$"))

; Structural keywords: *Part, *Assembly, *Instance, *Step and their *End.
; Zed tries @tag first and falls back to @keyword if the theme lacks @tag.
(keyword_line
  "*" @keyword @tag
  name: (keyword_name) @keyword @tag @_kw
  (#match? @_kw "^(?i)(end[ \t]+)?(part|assembly|instance|step)$"))

; Parameters:  NAME=value  or a bare flag such as GENERATE
(parameter_name) @property
"=" @operator

((value) @boolean
  (#match? @boolean "^(?i)(yes|no|true|false|on|off)$"))
((value) @constant
  (#not-match? @constant "^(?i)(yes|no|true|false|on|off)$"))

; Values and data
(number) @number
(string) @string
(parameter_ref) @variable.special
(data_line (identifier) @variable)

"," @punctuation.delimiter
