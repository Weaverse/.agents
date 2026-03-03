# Agent Guidelines for .agents

This repository contains agent definitions, command workflows, skill definitions, and coding rules for AI-powered coding tools. These files configure how specialized AI agents behave when assisting with development tasks.

## Repository Structure

```
.
├── agents/          # Specialized agent personas (code review, debugging, docs, etc.)
├── commands/        # Workflow templates (create-pr, format, review, etc.)
├── skills/          # Domain-specific procedures (code-review, feature-plan, frontend-design, commit)
├── rules/           # Coding convention rules (coding, commit, spec-driven-development)
├── claude-code-hooks.json   # Hook configuration (Claude Code specific)
└── claude-code-notifier.sh  # Cross-platform notification script
```

## Build, Lint & Test Commands

This is a configuration repository with no build step. Validate changes with:

### Validation Commands
```bash
# Validate JSON configuration
cat claude-code-hooks.json | jq . > /dev/null

# Validate shell script syntax
bash -n claude-code-notifier.sh

# Check Markdown frontmatter structure (manual check)
# Ensure all .md files have valid YAML frontmatter between --- markers
```

### Testing Agents & Commands
No automated tests. Manual verification required:
1. Copy agent/command/skill to your AI tool's config directory
2. Trigger the appropriate scenario in your AI coding tool
3. Verify the agent follows the expected behavior from examples

## Code Style Guidelines

### File Organization
- **Naming**: Use `kebab-case` for all files and directories
  - ✅ `code-review-specialist.md`
  - ❌ `CodeReviewSpecialist.md`, `code_review_specialist.md`
- **Location**: Keep related files in proper directories
  - Agents → `agents/`
  - Commands → `commands/`
  - Skills → `skills/<skill-name>/SKILL.md`
  - Rules → `rules/`

### Markdown Formatting
- Use ATX-style headers (`#`, `##`, `###`)
- Code blocks must specify language (```bash, ```markdown, ```text)
- Keep lines under 120 characters when possible
- Use numbered lists for sequential steps, bullets for unordered items

### Frontmatter Requirements

**Agents** (`agents/*.md`):
```yaml
---
name: agent-identifier          # kebab-case, unique
description: Detailed description with usage examples and triggers
color: green|blue|red|purple   # Visual identifier
model: haiku|sonnet|opus       # Optional: specify model preference
---
```

**Commands** (`commands/*.md`):
```yaml
---
description: Short, concise summary of what this command does
---
```

**Skills** (`skills/**/SKILL.md`):
```yaml
---
name: skill-identifier
description: What it does and when to invoke it
argument-hint: [expected input format]
allowed-tools: Read, Grep, Glob  # Comma-separated tool names
---
```

### Agent/Command Content Structure

1. **Role Definition** (agents only)
   - Start with "You are an expert..." establishing persona
   - Define core mission and specialization

2. **Core Responsibilities/Priorities**
   - Numbered list (1-5 items max)
   - Each item has a bold title and explanation

3. **Process/Workflow**
   - Step-by-step instructions for the agent
   - Use numbered lists for sequential tasks

4. **Output Format** (when applicable)
   - Provide exact template using code blocks
   - Include formatting rules (e.g., emoji usage, numbering scheme)

5. **Examples** (required for agents)
   - Use `<example>` tags with `user:`, `assistant:`, and `<commentary>` blocks
   - Show realistic scenarios that trigger the agent
   - Demonstrate edge cases and error handling

### Writing Style

- **Tone**: Professional, direct, concise
- **Voice**: Second person ("You will...") for agent instructions
- **Tense**: Present tense for actions ("You analyze...", not "You will analyze...")
- **Clarity**: Prefer simple words over jargon
- **Specificity**: Reference exact file patterns, tool names, and technologies

### Shell Script Conventions

```bash
#!/bin/bash

# Use consistent header comment blocks
#==============================================================================
# Script Name
# Description of what it does
#==============================================================================

# Check dependencies before using them
if ! command -v jq &> /dev/null; then
    echo "jq is required but not installed"
    exit 1
fi

# Support macOS, Linux, and Windows (Git Bash)
case "$(uname -s)" in
    Darwin*)  # macOS specific
        ;;
    Linux*)   # Linux specific
        ;;
    CYGWIN*|MINGW*|MSYS*)  # Windows specific
        ;;
esac
```

## Naming Conventions

- **Variables**: `snake_case` in bash scripts, `camelCase` in JSON
- **Files**: `kebab-case.md` for all markdown files
- **Agents**: Descriptive role-based names (e.g., `debug-specialist`, `solution-architect`)
- **Commands**: Verb-based names (e.g., `commit`, `create-pr`, `review-changes`)
- **Skills**: Domain-based names (e.g., `code-review`, `frontend-design`)

## Error Handling & Edge Cases

### Agent Examples Must Cover:
- ✅ Happy path (when to use the agent)
- ✅ Edge cases (when NOT to use the agent)
- ✅ Error scenarios (missing context, unclear requirements)

### Commands Should:
- Verify prerequisites (e.g., git repo exists, config files present)
- Fail gracefully with clear error messages
- Provide fallback behavior when tools aren't available

### Skills Should:
- List `allowed-tools` explicitly in frontmatter
- Specify exact output format with examples
- Define what to do when no findings/results

## Common Patterns

### Git Commands in Workflows
```bash
# Always check git status first
git status --porcelain

# Show uncommitted changes
git diff HEAD

# Show staged changes
git diff --cached
```

### Conditional Tool Detection
```bash
# Check for package.json
if [ -f "package.json" ]; then
    npm run format
fi

# Check for specific commands
if command -v biome &> /dev/null; then
    biome check --apply
fi
```

### Agent Invocation Pattern (in descriptions)
```text
Use this agent when [scenario]. Examples:

<example>
Context: [Situation description]
user: "[User message]"
assistant: "[Initial response]"
<commentary>
[Why this agent should be invoked]
</commentary>
assistant: "[Agent invocation]"
</example>
```

## Quality Checklist

Before committing new agents/commands/skills:

- [ ] Frontmatter is valid YAML with all required fields
- [ ] File uses `kebab-case` naming
- [ ] Contains at least 2-3 realistic examples
- [ ] Examples include `<commentary>` explaining why to use the agent
- [ ] Output format is clearly specified
- [ ] No generic placeholders (fill in actual tool names, file patterns)
- [ ] Tone is professional and direct
- [ ] Tested manually in your AI coding tool (if applicable)
