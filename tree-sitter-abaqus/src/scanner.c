// External scanner: line endings for the Abaqus grammar.
//
// _newline  consumes "\n" or "\r\n".
// _eof      zero-width token at end of input, so the last line of a file
//           does not need a trailing newline. It is only offered where the
//           parser expects the end of a line, which keeps it from looping.
#include "tree_sitter/parser.h"

enum TokenType { NEWLINE, END_OF_FILE, ERROR_SENTINEL };

void *tree_sitter_abaqus_external_scanner_create(void) { return NULL; }
void tree_sitter_abaqus_external_scanner_destroy(void *payload) {}
unsigned tree_sitter_abaqus_external_scanner_serialize(void *payload, char *buffer) { return 0; }
void tree_sitter_abaqus_external_scanner_deserialize(void *payload, const char *buffer, unsigned length) {}

bool tree_sitter_abaqus_external_scanner_scan(void *payload, TSLexer *lexer, const bool *valid_symbols) {
  if (valid_symbols[ERROR_SENTINEL]) return false;

  while (lexer->lookahead == ' ' || lexer->lookahead == '\t') lexer->advance(lexer, true);

  if (valid_symbols[NEWLINE]) {
    if (lexer->lookahead == '\r') {
      lexer->advance(lexer, false);
      if (lexer->lookahead == '\n') lexer->advance(lexer, false);
      lexer->result_symbol = NEWLINE;
      return true;
    }
    if (lexer->lookahead == '\n') {
      lexer->advance(lexer, false);
      lexer->result_symbol = NEWLINE;
      return true;
    }
  }

  if (valid_symbols[END_OF_FILE] && lexer->eof(lexer)) {
    lexer->result_symbol = END_OF_FILE;
    return true;
  }
  return false;
}
