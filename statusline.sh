#!/bin/bash
# Read Claude Code's status JSON; do not evaluate any of its strings as shell code.
set -euo pipefail
command -v jq >/dev/null || { printf 'jq is required\n' >&2; exit 1; }
input=$(cat)
fields=$(printf '%s' "$input" | jq -er '
  def clean: gsub("[\u0000-\u001f\u007f-\u009f]"; "");
  [(.model.display_name // "Claude" | tostring | clean),
   (.workspace.current_dir // "." | tostring | clean),
   (.cost.total_duration_ms // 0 | tonumber | floor | tostring),
   (.cost.total_cost_usd // 0 | tonumber | tostring),
   (.context_window.total_input_tokens // 0 | tonumber | floor | tostring),
   (.context_window.used_percentage // 0 | tonumber | floor | tostring)] | .[]') || exit 1
{
  IFS= read -r model
  IFS= read -r dir
  IFS= read -r duration_ms
  IFS= read -r cost
  IFS= read -r tokens
  IFS= read -r used
} <<< "$fields"
total_seconds=$((duration_ms / 1000))
printf -v duration '%dh%dm%ds' "$((total_seconds / 3600))" "$(((total_seconds % 3600) / 60))" \
  "$((total_seconds % 60))"
short_dir=$(printf '%s' "$dir" | awk -F/ '{if(NF>1) print $(NF-1)"/"$NF; else print $NF}')
printf '[%s | $%.2f | %s tokens | %s%% context] | %s | %s' "$duration" "$cost" "$tokens" "$used" \
  "$model" "$short_dir"
if git -C "$dir" rev-parse --git-dir >/dev/null 2>&1; then
  branch=$(git -C "$dir" branch --show-current 2>/dev/null)
  if [ -z "$branch" ]; then branch=$(git -C "$dir" rev-parse --short HEAD); fi
  branch=$(printf '%s' "$branch" | tr -d '\000-\037\177')
  dirty=$(git -C "$dir" status --porcelain --untracked-files=normal 2>/dev/null)
  state=clean
  if [ -n "$dirty" ]; then state=dirty; fi
  printf ' | %s (%s)' "$branch" "$state"
fi
printf '\n'
