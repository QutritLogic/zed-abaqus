#!/usr/bin/env bash
# Prepares this folder for Zed's "install dev extension".
#
# Zed loads Tree-sitter grammars from a git commit. This script makes sure
# the grammar is committed in this repository, then writes the repository
# path and commit into extension.toml. Run it again after changing the
# grammar, then press Rebuild on the Abaqus entry in Zed's Extensions page.
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$root"
command -v git >/dev/null || { echo "git is required" >&2; exit 1; }

[ -d .git ] || git init -q -b main

# Zed reads the grammar from the commit, so uncommitted grammar changes
# would be ignored. Commit the grammar folder if it has changed.
git add tree-sitter-abaqus
if ! git rev-parse -q --verify HEAD >/dev/null || ! git diff --cached --quiet -- tree-sitter-abaqus; then
  git commit -q -m "Update Abaqus grammar" -- tree-sitter-abaqus
  echo "Committed changes in tree-sitter-abaqus/."
fi
rev="$(git rev-parse HEAD)"

sed -i.bak \
  -e "s|^repository = .*|repository = \"file://$root\"|" \
  -e "s|^rev = .*|rev = \"$rev\"|" \
  extension.toml
rm -f extension.toml.bak

echo "Grammar commit: $rev"
echo
echo "In Zed: command palette -> 'zed: install dev extension' -> choose $root"
