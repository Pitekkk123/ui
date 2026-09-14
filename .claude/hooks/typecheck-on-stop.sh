#!/usr/bin/env bash
# Stop: typecheck the workspace once the turn ends.
#
# CI runs `turbo run typecheck`, but during a session nothing did, so a type
# error introduced by an edit stayed invisible until push. Running it per edit
# would be far too slow on a turborepo this size; once per turn is the cheap
# point, and turbo's cache makes a clean run near-instant.
#
# Reports rather than blocks: a turn that ends mid-refactor is legitimately
# un-typecheckable, and a Stop hook that refuses to let the turn finish would
# be worse than the error it reports.
set -uo pipefail

root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$root" || exit 0

out="$(pnpm typecheck 2>&1)"
status=$?

if [ $status -eq 0 ]; then
  exit 0
fi

# Keep the message short; the full log is reproducible with the same command.
summary="$(printf '%s\n' "$out" | grep -E "error TS[0-9]+" | head -5)"
[ -n "$summary" ] || summary="$(printf '%s\n' "$out" | tail -5)"
count="$(printf '%s\n' "$out" | grep -cE "error TS[0-9]+" || true)"

jq -nc --arg s "$(printf 'typecheck failed (%s type errors). Run `pnpm typecheck` for the full output.\n%s' "$count" "$summary")" \
  '{systemMessage:$s}'
exit 0
