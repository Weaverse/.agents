---
name: handoff
description: "Capture current work context for handoff to another agent/developer. Gathers git state, todos, and modified files into a structured handoff document saved to the related spec folder."
argument-hint: "[optional notes or context about the handoff]"
metadata:
  tools: [Read, Grep, Glob, Write, Bash, AskUserQuestion]
---

Generate a comprehensive handoff document capturing the current state of work for seamless continuation by another agent or developer.

## Workflow

### Step 1: Gather Context

Run these commands in parallel to understand the current state:
- `git status` — see all tracked/untracked files and staging state
- `git diff` — see unstaged changes
- `git log --oneline -10` — recent commits to understand work trajectory
- `git branch --show-current` — current branch name
- `git remote get-url origin` — repository name (if available)

Also check for active todos in the todo system.

### Step 2: Find the Related Spec Folder

Look for a matching spec folder in `.specs/`:
1. List all folders in `.specs/`
2. Match the current branch name, modified files, or recent commit messages to spec folder names
3. If multiple spec folders could match, pick the most relevant one
4. If a match is found, the handoff file will be saved inside that spec folder
5. If **no spec folder is found**, use `AskUserQuestion` to ask the user where to save the handoff file

### Step 3: Analyze Work State

1. **Work Completed** — analyze recent git commits, review completed todos, identify patterns in changes made
2. **Work In Progress** — active todo items, uncommitted changes, files currently being modified
3. **Work Remaining** — pending todo items, blockers, dependencies, priorities
4. **Context** — branch strategy, important decisions, known issues, relevant file paths with line numbers

### Step 4: Write the Handoff Document

Save the file as `handoff--{YYYY-MM-DD-HH:mm}.md` in the determined location.

Use this structure:

```markdown
# Handoff Context - {Date Time}

## Project
- Repository: {repo name if available}
- Branch: {current branch}
- Spec: {spec folder path if found}
- Last Updated: {timestamp}

## Current Status

### What's Been Done
{List completed work, recent commits, changes made}

### What's In Progress
{Current todo items, ongoing work}

### What's Next
{Pending tasks, blockers, priorities}

## Technical Context

### Modified Files
{List files changed with brief description}

### Key Decisions
{Important architectural or implementation decisions}

### Known Issues
{Bugs, blockers, or things to watch out for}

## Dependencies & Prerequisites
{External dependencies, required setup, environment notes}

## Additional Notes
{Any other relevant context for continuation}
```

### Step 5: Report

After saving, display:
- The full file path where the handoff was saved
- A brief summary of the current state

## User Arguments

$ARGUMENTS

## Important Notes

- Be concise but comprehensive — focus on actionable information
- Include specific file paths with line numbers where relevant
- Do NOT commit the handoff file automatically
- If the user provided notes via arguments, include them in the "Additional Notes" section
