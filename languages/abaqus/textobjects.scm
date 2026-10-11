; Vim-mode text objects and motions.
;   ]] / [[  and  ac / ic : jump between or select whole sections
;   ]m / [m  and  af / if : jump between or select keyword blocks

(part) @class.around
(assembly) @class.around
(instance) @class.around
(step) @class.around

(keyword_block
  header: (keyword_line)
  (data_line)* @function.inside) @function.around

(comment)+ @comment.around
