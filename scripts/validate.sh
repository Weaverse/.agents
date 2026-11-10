#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "$0")/.."
python=${PYTHON:-python3}
for dependency in "$python" shellcheck jq; do
  command -v "$dependency" >/dev/null || { printf 'Missing dependency: %s\n' "$dependency" >&2; exit 1; }
done
"$python" scripts/validate.py
shellcheck --external-sources statusline.sh claude-code-notifier.sh scripts/*.sh
while IFS= read -r -d '' file; do
  jq empty "$file"
done < <(find . -name .git -prune -o -name .venv -prune -o -type f -name '*.json' -print0)
printf 'ShellCheck and JSON validation passed\n'
