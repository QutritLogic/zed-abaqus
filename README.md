# Abaqus for Zed

Abaqus input file support (`.inp`, `.inc`, `.incl`) for the Zed editor, built on a new Tree-sitter grammar.

![Highlighting preview](docs/preview.png)

## Features

- **Syntax highlighting**
  - comments
  - `*Keywords`
  - parameter names and values
  - `YES`/`NO` flags
  - numbers, including Fortran-style `2.5D+1`
  - strings and `<parameter>` references
  - data lines
- **Structural keywords stand out.** `*Part`, `*Assembly`, `*Instance`, `*Step` and their `*End` lines get their own colour.
- **Outline** ("outline: toggle" for quick jump, "outline panel: toggle focus" for the panel):
  - parts, assemblies, instances and steps, nested
  - every named definition: materials, sets, surfaces, amplitudes …
- **Vim text objects and motions**:
  - `]]` / `[[` jump between parts, instances and steps; `ac` / `ic` select one
  - `]m` / `[m` jump between keyword blocks; `af` selects a whole block, `if` only its data lines
- **67 snippets.** Type `*`, then a keyword such as `node`, `material`, `static` or `contact pair`, and pick the snippet. Tab moves through the fields.
- **Comment toggling** with `Ctrl+/`, using `** `.
- **Large files.** A 28 MB / 550,000-line mesh parses in a few seconds in the background, and highlighting stays on.

## Install (Linux / macOS)

1. Run `bash install.sh` in this folder. Zed only loads grammars from a git commit, so the script commits `tree-sitter-abaqus/` if it has changed and writes this repository's path and that commit into `extension.toml`.
2. In Zed, open the command palette, run **zed: install dev extension**, and choose this folder. The first install compiles the grammar, which takes a moment. `zed: open log` shows any errors. If it complains about Rust, install it via rustup and try again.

Open an `.inp` file. The language indicator in the status bar should say **Abaqus**.

## Changing the grammar or queries

| What you change | What to do afterwards |
| --- | --- |
| Colours / captures | Edit `languages/abaqus/highlights.scm`, then **Rebuild** the extension on Zed's Extensions page. |
| Outline / text objects | Edit `outline.scm` / `textobjects.scm`, then Rebuild. |
| Snippets | Edit `make_snippets.py`, run `python3 make_snippets.py`, then Rebuild. |
| Grammar | Edit `tree-sitter-abaqus/grammar.js`, then run `tree-sitter generate` and `tree-sitter test` (needs `npm i -g tree-sitter-cli`). Run `bash install.sh` again and Rebuild. |

`tree-sitter-abaqus/queries/` holds a copy of the queries for Tree-sitter's own tools (`tree-sitter highlight`, Neovim, Helix). Keep it in sync if you use those.

### Recolouring without touching the extension

The captures used are:

- `keyword`, `tag` (structural keywords), `property` (parameter names)
- `constant` (parameter values), `boolean`, `number`, `string`
- `variable` (data identifiers), `variable.special` (`<param>`)
- `comment`

Override any of them in your Zed `settings.json`:

```json
"theme_overrides": {
  "One Dark": {
    "syntax": {
      "tag":      { "color": "#e5c07b", "font_weight": 700 },
      "property": { "color": "#61afef" }
    }
  }
}
```

## Known limits

- **Folding per keyword block isn't possible.** Zed folds by indentation and Abaqus decks aren't indented. Use the outline panel to jump instead, or select a block with `af` in Vim mode and run "editor: fold selected ranges".
- **No equivalent to the VS Code "run job" helper.** Running Abaqus works the same in Zed's terminal (`abaqus job=name input=name.inp cpus=4 interactive`). You could also add it as a Zed task.
- **File-type conflicts.** If another extension also claims `.inp` or `.inc`, set it explicitly in `settings.json`:
  ```json
  "file_types": { "Abaqus": ["inp", "inc", "incl"] }
  ```
- **Comment lines are not grouped into blocks.** Comments (`**`) sit between blocks in the syntax tree. A data line that follows a comment in the middle of a block still highlights correctly.

## Repository layout

| Path | Contents |
| --- | --- |
| `extension.toml`, `languages/`, `snippets/` | The Zed extension |
| `tree-sitter-abaqus/` | The grammar: `grammar.js`, the generated parser in `src/`, tests in `test/corpus/` |
| `install.sh` | Local development setup |
| `make_snippets.py` | Generates `snippets/abaqus.json` |

## Publishing (optional)

`install.sh` writes a local `file://` path into `extension.toml`, so don't push that version as-is if you want others to build from the repo. To list it in Zed's extension registry:

- Set `repository` in `extension.toml` to this repo's GitHub URL and `rev` to a pushed commit. Keep `path = "tree-sitter-abaqus"`.
- Add an open-source license; Zed's registry requires one.
- Follow https://zed.dev/docs/extensions/publishing/overview.html
