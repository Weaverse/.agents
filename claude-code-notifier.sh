#!/bin/bash
# Optional Notification-only hook. Tests use --dry-run and never notify the desktop.
set -euo pipefail
case "${1:-}" in
  '') dry_run=false ;;
  --dry-run) dry_run=true ;;
  *) printf 'Usage: bash claude-code-notifier.sh [--dry-run]\n' >&2; exit 2 ;;
esac
if [ "$#" -gt 1 ]; then exit 2; fi
command -v jq >/dev/null || { printf 'jq is required\n' >&2; exit 1; }
input=$(cat)
event=$(printf '%s' "$input" | jq -er '.hook_event_name | select(type == "string")') || exit 1
[ "$event" = Notification ] || exit 0
message=$(printf '%s' "$input" | jq -r '.message | if type == "string" then . else "Needs attention" end') || exit 1
if "$dry_run"; then printf 'Claude Code: %s\n' "$message"; exit 0; fi
case "$(uname -s)" in
  Darwin*)
    if command -v terminal-notifier >/dev/null; then
      terminal-notifier -title 'Claude Code' -message "$message"
    else
      osascript - "$message" <<'APPLESCRIPT'
on run argv
  display notification (item 1 of argv) with title "Claude Code"
end run
APPLESCRIPT
    fi ;;
  Linux*)
    if command -v notify-send >/dev/null; then notify-send -- 'Claude Code' "$message"
    else printf 'Claude Code: %s\n' "$message"; fi ;;
  *) printf 'Claude Code: %s\n' "$message" ;;
esac
