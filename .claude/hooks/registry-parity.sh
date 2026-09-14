#!/usr/bin/env bash
# PostToolUse (Write|Edit): enforce the Base UI <-> Radix registry parity rule.
#
# apps/v4/registry/bases/base and .../radix are parallel trees; a change to one
# side is expected on the other unless the APIs genuinely differ. That rule
# lives in .cursor/rules/registry-bases-parity.mdc, which only reaches Cursor
# and only as advice. This reports the mirrored path back into the session so
# the omission is visible while the change is still in progress.
set -uo pipefail

file="$(jq -r '.tool_response.filePath // .tool_input.file_path // empty')"
[ -n "$file" ] || exit 0

root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$root" || exit 0
rel="${file#"$root"/}"

case "$rel" in
  apps/v4/registry/bases/base/*)  other="${rel/bases\/base\//bases/radix/}" ;;
  apps/v4/registry/bases/radix/*) other="${rel/bases\/radix\//bases/base/}" ;;
  *) exit 0 ;;
esac

if [ ! -e "$other" ]; then
  msg="Registry parity: edited ${rel}, but its counterpart ${other} does not exist. If this component exists for one base only, that is fine — otherwise create the mirror."
else
  # Did this session touch the other side too?
  if git diff --name-only -- "$other" | grep -q . || git diff --cached --name-only -- "$other" | grep -q .; then
    exit 0
  fi
  msg="Registry parity: edited ${rel} but ${other} is unchanged. Per .cursor/rules/registry-bases-parity.mdc the trees stay in sync — apply the same behavioural and visual change there, or state why this side diverges."
fi

jq -nc --arg m "$msg" \
  '{hookSpecificOutput:{hookEventName:"PostToolUse", additionalContext:$m}}'
exit 0
