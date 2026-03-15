# .agents

> Skills, commands, and rules for AI-powered coding tools — used daily to supercharge development productivity.

This repository contains workflow commands, specialized skills, coding rules, and system hooks that work with any AI coding assistant that supports markdown-based configuration.

## 📦 What's Inside

```
.agents/
├── commands/        # 9 workflow automation commands
├── skills/          # 4 domain-specific skills
├── rules/           # 5 coding convention rules
└── claude-code-hooks.json   # Hook configuration (Claude Code specific)
```

## 🚀 Quick Start

### Option 1: Clone Entire Setup
```bash
cd ~
git clone git@github.com:Weaverse/.agents.git

# Symlink into your AI tool's config directory
# For Claude Code:
ln -s ~/.agents/commands ~/.claude/commands
ln -s ~/.agents/skills ~/.claude/skills
ln -s ~/.agents/rules ~/.claude/rules
```

### Option 2: Copy Individual Items
1. Browse the `commands/`, `skills/`, or `rules/` folders
2. Copy the files you need into your AI tool's config directory

## ⚡ Workflow Commands

Automation commands for common development tasks:

| Command | Description |
|---------|-------------|
| **[work](commands/work.md)** | Pick up a GitHub issue — fetch context, create branch, generate spec plan, and optionally open a draft PR |
| **[create-task](commands/create-task.md)** | Create a GitHub issue with full metadata and optional project board integration |
| **[create-pr](commands/create-pr.md)** | Create pull requests with AI-generated descriptions |
| **[fix-pr](commands/fix-pr.md)** | Fix issues raised in PR reviews |
| **[review-changes](commands/review-changes.md)** | Review uncommitted changes before pushing |
| **[review-code](commands/review-code.md)** | In-depth code quality analysis |
| **[format](commands/format.md)** | Auto-format code and fix TypeScript issues |
| **[handoff](commands/handoff.md)** | Generate context summaries for team handoffs |
| **[ultrathink](commands/ultrathink.md)** | Deep reasoning mode for complex problems |

## 🎯 Specialized Skills

Domain-specific procedures for complex tasks:

| Skill | Description |
|-------|-------------|
| **[commit](skills/commit/)** | Commit changes with well-crafted messages, grouping related files into separate commits |
| **[code-review](skills/code-review/)** | Comprehensive code audits — dead code, duplications, patterns, bugs |
| **[feature-plan](skills/feature-plan/)** | Detailed implementation planning before writing code |
| **[frontend-design](skills/frontend-design/)** | Create distinctive, production-grade UI components |

## 📏 Coding Rules

Opinionated conventions enforced across the team:

| Rule | Description |
|------|-------------|
| **[coding](rules/coding.md)** | Naming, styling, and general coding standards |
| **[commit](rules/commit.md)** | Commit message conventions |
| **[communication](rules/communication.md)** | How AI should handle questions vs statements |
| **[never-auto-commit](rules/never-auto-commit.md)** | Prevent AI tools from auto-committing |
| **[spec-driven-development](rules/spec-driven-development.md)** | Write specs before code |

## 🔔 System Hooks

The included `claude-code-hooks.json` and `claude-code-notifier.sh` enable system notifications for:
- Session start/end
- Task completion
- Custom alerts

Cross-platform support: macOS, Linux, Windows (PowerShell).

> **Note:** Hooks are currently Claude Code specific. Contributions for other tools welcome.

## 🛠️ Development

See [AGENTS.md](AGENTS.md) for:
- Validation commands
- Code style guidelines
- Frontmatter requirements
- Quality checklist

## 🤝 Contributing

Contributions welcome! When adding new commands/skills:

1. Follow the naming convention: `kebab-case.md`
2. Include proper YAML frontmatter
3. Add 2-3 realistic usage examples
4. Test manually in your AI coding tool
5. Update relevant README sections

## 📝 License

MIT

---

**Built by [Weaverse](https://weaverse.io)** — Empowering developers with AI-enhanced workflows.
