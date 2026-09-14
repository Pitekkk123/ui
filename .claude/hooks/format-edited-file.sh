#!/usr/bin/env bash
# PostToolUse (Write|Edit): format the file Claude just wrote.
#
# The repo formats in CI (`pnpm format:check`) but nothing formatted during an
# AI session, so edits landed unformatted and the mismatch only surfaced later.
# Prettier here loads the repo config, including the import-sort and tailwind
# plugins, so a session edit matches what CI expects.
set -uo pipefail

file="$(jq -r '.tool_response.filePath // .tool_input.file_path // empty')"
[ -n "$file" ] || exit 0
[ -f "$file" ] || exit 0

case "$file" in
  *.ts|*.tsx|*.js|*.jsx|*.mjs|*.cjs|*.mts|*.cts|*.json|*.jsonc|*.css|*.md|*.mdx|*.yml|*.yaml) ;;
  *) exit 0 ;;
esac

root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$root" || exit 0

err="$(pnpm exec prettier --write --ignore-unknown --log-level warn "$file" 2>&1 >/dev/null)"
status=$?
[ $status -eq 0 ] && exit 0

# prettier-plugin-tailwindcss resolves `shadcn/tailwind.css` through the
# shadcn package's exports, which only exist once that package is built. On a
# fresh clone this fails for every file, and a silent no-op would leave the
# hook looking installed while doing nothing. A parse error, by contrast, is
# expected mid-edit and stays quiet.
case "$err" in
  *"Can't resolve"*|*"Cannot find module"*|*"Cannot find package"*)
    jq -nc --arg s "Formatting hook inactive: prettier cannot load its plugins ($(printf '%s' "$err" | head -1 | cut -c1-160)). Run \`pnpm --filter=shadcn build\` once, then formatting resumes automatically." \
      '{systemMessage:$s}'
    ;;
esac
exit 0
