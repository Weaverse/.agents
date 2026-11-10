#!/bin/bash
# Link first-party files only. Existing personal configuration is never overwritten.
set -euo pipefail

dry_run=false
case "${1:-}" in
  --dry-run) dry_run=true; shift ;;
  --help) printf 'Usage: bash scripts/install.sh [--dry-run]\n'; exit 0 ;;
esac
if [ "$#" -ne 0 ]; then
  printf 'Unknown argument. Use --dry-run or --help.\n' >&2
  exit 2
fi
: "${HOME:?HOME must be set}"
repo=$(cd -- "$(dirname -- "$0")/.." && pwd -P)

function make_dir() {
  if [ -d "$1" ] && [ ! -L "$1" ]; then
    printf 'Keep directory: %s\n' "$1"
  elif [ -e "$1" ] || [ -L "$1" ]; then
    printf 'Preserve conflicting path: %s\n' "$1"
    return 1
  else
    printf 'Create directory: %s\n' "$1"
    if ! "$dry_run"; then mkdir -p -- "$1"; fi
  fi
}

function link_file() {
  if [ "$2" -ef "$1" ]; then
    printf 'Keep existing target: %s\n' "$2"
  elif [ -e "$2" ] || [ -L "$2" ]; then
    printf 'Preserve conflicting path: %s (wanted %s)\n' "$2" "$1"
  else
    printf 'Link: %s -> %s\n' "$2" "$1"
    if ! "$dry_run"; then ln -s -- "$1" "$2"; fi
  fi
}

printf 'Source: %s\nDry run: %s\n' "$repo" "$dry_run"
if [ ! "$HOME/.agents/skills" -ef "$repo/skills" ]; then
  printf 'Codex, Cursor and OpenCode need this checkout in your shared .agents directory for native discovery.\n'
  printf 'No shared-directory link is created automatically.\n'
fi

if make_dir "$HOME/.claude"; then
  commands="$HOME/.claude/commands"
  if [ -L "$commands" ] && [ ! -e "$commands" ]; then
    old_target=$(readlink "$commands")
    case "$old_target" in
      "$repo/commands"|"$HOME/.agents/commands"|../.agents/commands)
        printf 'Remove obsolete dangling commands link: %s\n' "$commands"
        if ! "$dry_run"; then rm -- "$commands"; fi ;;
      *) printf 'Preserve unrelated dangling commands link: %s\n' "$commands" ;;
    esac
  fi
  if [ "$HOME/.claude/skills" -ef "$repo/skills" ]; then
    printf 'Keep whole-directory skills link: %s\n' "$HOME/.claude/skills"
  elif make_dir "$HOME/.claude/skills"; then
    while IFS= read -r name; do
      link_file "$repo/skills/$name" "$HOME/.claude/skills/$name"
    done < <(sed -n 's|^!/skills/\([^/]*\)/$|\1|p' "$repo/.gitignore")
  fi
  if [ "$HOME/.claude/rules" -ef "$repo/rules" ]; then
    printf 'Keep whole-directory rules link: %s\n' "$HOME/.claude/rules"
  elif make_dir "$HOME/.claude/rules"; then
    link_file "$repo/rules/weaverse-team.md" "$HOME/.claude/rules/weaverse-team.md"
  fi
  link_file "$repo/statusline.sh" "$HOME/.claude/statusline.sh"
  link_file "$repo/claude-code-notifier.sh" "$HOME/.claude/claude-code-notifier.sh"
fi
if make_dir "$HOME/.codex"; then
  link_file "$repo/rules/weaverse-team.md" "$HOME/.codex/AGENTS.md"
fi

printf '\nManual configuration (no settings files were edited):\n'
printf 'Claude Code: merge the following example into your settings, preserving unrelated keys.\n'
cat "$repo/claude-code-settings.example.json"
printf '\nCodex: if AGENTS.md already exists, include the team file in your own instructions.\n'
printf 'OpenCode: add this absolute path to the instructions array in your global opencode.json(c):\n'
printf '  %s/rules/weaverse-team.md\n' "$repo"
printf 'Cursor: paste the team file into Customize > Rules > User Rules.\n'
printf 'Turn off Cursor Commit Attribution and PR Attribution; CLI: attribution.attributeCommitsToAgent=false.\n'
printf '\nTeam instructions for manual inclusion:\n'
cat "$repo/rules/weaverse-team.md"
