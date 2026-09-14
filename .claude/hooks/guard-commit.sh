#!/usr/bin/env bash
# PreToolUse (Bash, git commit): lint the message and refuse committed secrets.
#
# The repo runs commitlint on @commitlint/config-conventional, but only in CI,
# so a badly-shaped message was only rejected after the push. The secret check
# is the cheaper half: a credential in a staged diff is expensive to undo once
# it reaches the remote, and trivial to catch here.
set -uo pipefail

payload="$(cat)"
cmd="$(printf '%s' "$payload" | jq -r '.tool_input.command // empty')"
[ -n "$cmd" ] || exit 0
printf '%s' "$cmd" | grep -q "git commit" || exit 0

root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$root" || exit 0

deny() {
  jq -nc --arg r "$1" \
    '{hookSpecificOutput:{hookEventName:"PreToolUse", permissionDecision:"deny", permissionDecisionReason:$r}}'
  exit 0
}

# --- credential shapes in the staged diff -------------------------------------
staged="$(git diff --cached 2>/dev/null || true)"
if [ -n "$staged" ]; then
  hit="$(printf '%s' "$staged" | grep -nE \
    -e 'sk-(proj-)?[A-Za-z0-9_-]{20,}' \
    -e 'ghp_[A-Za-z0-9]{30,}' \
    -e 'github_pat_[A-Za-z0-9_]{30,}' \
    -e 'xox[baprs]-[A-Za-z0-9-]{10,}' \
    -e '-----BEGIN (RSA |EC )?PRIVATE KEY-----' \
    -e 'AKIA[0-9A-Z]{16}' \
    | head -1 || true)"
  if [ -n "$hit" ]; then
    deny "A staged line matches a credential shape. Nothing was committed. Remove the value, rotate it if it is real, and stage again. First match: $(printf '%s' "$hit" | cut -c1-120)"
  fi
fi

# --- conventional-commit message ---------------------------------------------
# Only -m is checked; -F, -c and an editor-opened message are left alone rather
# than guessed at.
msg="$(printf '%s' "$cmd" | sed -n 's/.*-m[[:space:]]*"\([^"]*\)".*/\1/p')"
[ -n "$msg" ] || msg="$(printf '%s' "$cmd" | sed -n "s/.*-m[[:space:]]*'\([^']*\)'.*/\1/p")"
[ -n "$msg" ] || exit 0

if ! printf '%s' "$msg" | pnpm exec commitlint >/dev/null 2>&1; then
  reason="$(printf '%s' "$msg" | pnpm exec commitlint 2>&1 | grep -E "^.?[[:space:]]*(✖|×|error)" | head -3)"
  [ -n "$reason" ] || reason="does not match @commitlint/config-conventional"
  deny "commitlint rejected the message, so nothing was committed: ${reason}. Expected conventional form, e.g. 'fix(v4): correct button focus ring'."
fi
exit 0
