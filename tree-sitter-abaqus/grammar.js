/**
 * Tree-sitter grammar for Abaqus input files (.inp, .inc, .incl).
 *
 * Abaqus input is line oriented:
 *   **  comment line
 *   *KEYWORD NAME, PARAM=value, FLAG      keyword line (continues on the next
 *                                         line when it ends with a comma)
 *   1, 0.0, 2.5e-3, Set-1                 data line
 *
 * Keyword names and parameters are case-insensitive. Every keyword line plus
 * the data lines after it form a `keyword_block`. The paired blocks
 * *Part/*End Part, *Assembly/*End Assembly, *Instance/*End Instance and
 * *Step/*End Step become nested sections, which gives Zed an outline and
 * text objects that follow the model structure.
 */

/** Case-insensitive regex for a (possibly multi-word) keyword. */
function ci(word) {
  const body = word
    .split('')
    .map((c) => (/[a-z]/i.test(c) ? `[${c.toLowerCase()}${c.toUpperCase()}]` : c === ' ' ? '[ \\t]+' : c))
    .join('');
  return new RegExp(body);
}

const NUMBER = /[+-]?(\d+\.?\d*|\.\d+)([eEdD][+-]?\d+)?/;

module.exports = grammar({
  name: 'abaqus',

  externals: ($) => [$._newline, $._eof, $._error_sentinel],

  // Comment lines are extras, so they may sit anywhere between other lines.
  // The token includes its line break.
  extras: ($) => [/[ \t]+/, $.comment],

  word: ($) => $.keyword_name,


  rules: {
    source_file: ($) => repeat($._top_item),

    _top_item: ($) =>
      choice($.part, $.assembly, $.step, $.keyword_block, $.data_line, $._newline),

    // ----------------------------------------------------------------- lines

    comment: (_) => token(prec(10, /\*\*[^\r\n]*(\r?\n)?/)),

    _eol: ($) => choice($._newline, $._eof),

    keyword_line: ($) => seq('*', field('name', $.keyword_name), optional($._parameters), $._eol),

    _parameters: ($) => repeat1(seq(',', optional($._newline), field('parameter', $.parameter))),

    keyword_name: (_) => /[A-Za-z]([A-Za-z0-9_ \t-]*[A-Za-z0-9_-])?/,

    parameter: ($) =>
      seq(field('name', $.parameter_name), optional(seq('=', field('value', $._parameter_value)))),

    parameter_name: (_) => /[A-Za-z_]([A-Za-z0-9_ \t-]*[A-Za-z0-9_-])?/,

    _parameter_value: ($) => choice($.number, $.string, $.parameter_ref, $.value),

    value: (_) => /[^,\s="<]([^,\r\n="]*[^,\s="])?/,

    data_line: ($) =>
      seq(
        choice(
          seq($._data_item, repeat(seq(',', optional($._data_item)))),
          seq(',', optional($._data_item), repeat(seq(',', optional($._data_item)))),
        ),
        $._eol,
      ),

    _data_item: ($) => choice($.number, $.string, $.parameter_ref, $.identifier),

    number: (_) => token(prec(2, NUMBER)),
    string: (_) => token(prec(2, /"[^"\r\n]*"/)),
    parameter_ref: (_) => token(prec(2, /<[A-Za-z_][A-Za-z0-9_]*>/)),
    identifier: (_) => /[^,\s*<"]([^,\r\n]*[^,\s])?/,

    // ---------------------------------------------------------------- blocks

    keyword_block: ($) =>
      prec.right(seq(field('header', $.keyword_line), repeat($.data_line))),

    // Paired sections. The opening keyword keeps its data lines (for example
    // the translation/rotation lines of *Instance).
    part: ($) => section($, 'Part', [$.keyword_block, $._newline]),
    assembly: ($) =>
      section($, 'Assembly', [$.instance, $.keyword_block, $._newline]),
    instance: ($) => section($, 'Instance', [$.keyword_block, $._newline]),
    step: ($) => section($, 'Step', [$.keyword_block, $._newline]),

    ...sectionRules('Part'),
    ...sectionRules('Assembly'),
    ...sectionRules('Instance'),
    ...sectionRules('Step'),
  },
});

function section($, word, body) {
  const w = word.toLowerCase();
  return seq(
    field('start', alias($[`_${w}_start`], $.keyword_block)),
    repeat(choice(...body)),
    field('end', alias($[`_${w}_end`], $.keyword_line)),
  );
}

/** Header/footer rules for one paired section, e.g. *Part ... *End Part. */
function sectionRules(word) {
  const w = word.toLowerCase();
  return {
    [`_kw_${w}`]: (_) => token(prec(3, ci(word))),
    [`_kw_end_${w}`]: (_) => token(prec(3, ci(`End ${word}`))),
    [`_${w}_start_line`]: ($) =>
      seq('*', field('name', alias($[`_kw_${w}`], $.keyword_name)), optional($._parameters), $._eol),
    [`_${w}_start`]: ($) =>
      prec.right(seq(field('header', alias($[`_${w}_start_line`], $.keyword_line)), repeat($.data_line))),
    [`_${w}_end`]: ($) =>
      seq('*', field('name', alias($[`_kw_end_${w}`], $.keyword_name)), optional($._parameters), $._eol),
  };
}
