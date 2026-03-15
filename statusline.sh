#!/bin/bash
input=$(cat)

MODEL_RAW=$(echo "$input" | jq -r '.model.display_name // "Claude"')
DIR=$(echo "$input" | jq -r '.workspace.current_dir // "."')
DURATION_MS=$(echo "$input" | jq -r '.cost.total_duration_ms // 0' | awk '{printf "%d", $1}')
COST=$(echo "$input" | jq -r '.cost.total_cost_usd // 0')
TOKENS=$(echo "$input" | jq -r '.context_window.total_input_tokens // 0' | awk '{printf "%d", $1}')

# Shorten model name: "claude-sonnet-4-5" or "Claude Sonnet 4.5" -> "Sonnet 4.5"
MODEL=$(echo "$MODEL_RAW" \
  | sed 's/[Cc]laude[- ]//g' \
  | sed 's/\([0-9]\)-\([0-9]\)/\1.\2/g' \
  | sed 's/-/ /g' \
  | sed 's/  */ /g' \
  | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2); print}')

# Colors for light background
BLACK='\033[30m'
DARK_GRAY='\033[90m'
GREEN='\033[32m'
RED='\033[31m'
RESET='\033[0m'

SEP=" ${DARK_GRAY}|${RESET} "
DOT=" ${DARK_GRAY}·${RESET} "

# Format duration: ms -> "2m34s" or "1h13m6s"
TOTAL_SECS=$((DURATION_MS / 1000))
HOURS=$((TOTAL_SECS / 3600))
MINS=$(((TOTAL_SECS % 3600) / 60))
SECS=$((TOTAL_SECS % 60))
if [ "$HOURS" -gt 0 ]; then
  DURATION_FMT="${HOURS}h${MINS}m${SECS}s"
else
  DURATION_FMT="${MINS}m${SECS}s"
fi

# Format cost: "$0.42"
COST_FMT=$(printf '$%.2f' "$COST")

# Format tokens: "12k token" or "512 token"
if [ "$TOKENS" -ge 1000 ]; then
  TOKENS_FMT=$(awk "BEGIN {printf \"%dk\", $TOKENS/1000}")
else
  TOKENS_FMT="${TOKENS}"
fi

# Stats block
STATS="${DARK_GRAY}[${RESET}${DURATION_FMT}${DOT}${COST_FMT}${DOT}${TOKENS_FMT} token${DARK_GRAY}]${RESET}"

# Short dir: last two path segments
SHORT_DIR=$(echo "$DIR" | awk -F'/' '{if(NF>=2) print $(NF-1)"/"$NF; else print $NF}')

# Git branch + dirty status (inline with dir)
GIT_PART=""
if git -C "$DIR" rev-parse --git-dir > /dev/null 2>&1; then
  BRANCH=$(git -C "$DIR" branch --show-current 2>/dev/null)
  if [ -n "$BRANCH" ]; then
    if git -C "$DIR" diff --quiet 2>/dev/null && git -C "$DIR" diff --cached --quiet 2>/dev/null; then
      DIRTY="${GREEN}✓${RESET}"
    else
      DIRTY="${RED}✗${RESET}"
    fi
    GIT_PART=" ${DARK_GRAY}(${RESET}${GREEN}⎇ ${BRANCH}${RESET} ${DIRTY}${DARK_GRAY})${RESET}"
  fi
fi

echo -e "${STATS}${SEP}${BLACK}${MODEL}${RESET}${SEP}${SHORT_DIR}${GIT_PART}"
