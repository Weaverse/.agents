# .claude

> Production-ready configuration for [Claude Code](https://claude.ai/download) - Specialized agents, workflow commands, and skills used by the Weaverse team.

This repository contains everything you need to supercharge your Claude Code setup: reusable agents, workflow automation commands, specialized skills, and system hooks.

## 📦 What's Inside

```
.claude/
├── agents/          # 7 specialized AI agents for specific tasks
├── commands/        # 8 workflow automation commands
├── skills/          # 2 domain-specific skills (code-review, frontend-design)
├── settings.json    # Hook configuration for notifications
└── claude-code-notifier.sh  # Cross-platform notification script
```

## 🚀 Quick Start

### Option 1: Clone Entire Setup
```bash
# Clone into your home directory
cd ~
git clone https://github.com/Weaverse/.claude.git

# Or symlink specific items
ln -s ~/path/to/.claude/agents ~/.claude/agents
```

### Option 2: Copy Individual Items
1. Browse the `agents/`, `commands/`, or `skills/` folders
2. Copy the files you want into your `~/.claude/` directory
3. Restart Claude Code (if needed)

## 🤖 Available Agents

Production-tested agents used daily by the Weaverse development team:

| Agent | Purpose | Best For |
|-------|---------|----------|
| **[code-review-specialist](agents/code-review-specialist.md)** | Expert code reviews with security & performance analysis | PR reviews, quality assessment |
| **[debug-specialist](agents/debug-specialist.md)** | Systematic debugging and issue diagnosis | Runtime errors, test failures, build issues |
| **[solution-architect](agents/solution-architect.md)** | Strategic guidance with pros/cons analysis | Architecture decisions, complex problems |
| **[docs-writer](agents/docs-writer.md)** | Clear, simple technical documentation | READMEs, API docs, guides |
| **[code-explainer](agents/code-explainer.md)** | Break down complex code concepts | Code walkthroughs, onboarding |
| **[feature-architecture-reviewer](agents/feature-architecture-reviewer.md)** | Review feature implementations | Scalability assessment, design validation |
| **[pr-review-analyst](agents/pr-review-analyst.md)** | Deep PR analysis with impact assessment | Change reviews, regression prevention |

[View detailed agent descriptions →](agents/README.md)

## ⚡ Workflow Commands

Automation commands for common development tasks:

- **[commit](commands/commit.md)** - Auto-generate conventional commit messages
- **[create-pr](commands/create-pr.md)** - Create pull requests with AI-generated descriptions
- **[fix-pr](commands/fix-pr.md)** - Fix issues from PR reviews
- **[format](commands/format.md)** - Auto-format code and fix TypeScript issues
- **[review-changes](commands/review-changes.md)** - Review uncommitted changes
- **[review-code](commands/review-code.md)** - In-depth code quality analysis
- **[handoff](commands/handoff.md)** - Generate context for team handoffs
- **[ultrathink](commands/ultrathink.md)** - Deep reasoning for complex problems

## 🎯 Specialized Skills

Domain-specific procedures for complex tasks:

- **[code-review](skills/code-review/)** - Comprehensive code audits (dead code, duplications, patterns, bugs)
- **[frontend-design](skills/frontend-design/)** - Create distinctive, production-grade UI components

## 🔔 System Hooks

The included `settings.json` and `claude-code-notifier.sh` enable system notifications for:
- Session start/end
- Task completion
- Custom alerts

Cross-platform support: macOS, Linux, Windows (PowerShell).

## 🛠️ Development

See [AGENTS.md](AGENTS.md) for:
- Validation commands
- Code style guidelines
- Frontmatter requirements
- Quality checklist

## 🤝 Contributing

Contributions welcome! When adding new agents/commands/skills:

1. Follow the naming convention: `kebab-case.md`
2. Include proper YAML frontmatter
3. Add 2-3 realistic examples with `<commentary>` tags
4. Test manually in Claude Code
5. Update relevant README sections

## 📝 License

MIT

---

**Built by [Weaverse](https://weaverse.io)** - Empowering developers with AI-enhanced workflows.
