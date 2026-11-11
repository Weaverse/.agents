# Weaverse .agents

A small first-party library for Claude Code, Codex, Cursor and OpenCode. Keep what a frontier model would
otherwise miss: team contracts, executable glue and platform-specific verification traps. No third-party skills
are vendored here. Repository instructions take precedence over the shared team defaults.

## Inside

| Path | Purpose |
| --- | --- |
| `rules/weaverse-team.md` | One short team file: commits, issue-first/single-spec work and coding exceptions |
| `skills/` | Four user-started workflows and eight focused engineering playbooks |
| `scripts/install.sh` | Safe symlink setup and migration; prints actions, never edits settings |
| `scripts/validate.sh`, `tests/` | Frontmatter, name collisions, size, shell/JSON checks and offline tool tests |
| `statusline.sh` | Duration, cost, tokens, context use, model, directory and Git state |
| `claude-code-notifier.sh` | Optional Notification-only hook; macOS fallback and Linux support |
| `claude-code-settings.example.json` | Attribution off, documented `statusLine` object and optional hook |

## Install per tool

Prerequisites: Git and Bash; jq for Claude Code glue. Review the scripts before running them.

```bash
git clone https://github.com/Weaverse/.agents.git "$HOME/.agents"
bash "$HOME/.agents/scripts/install.sh" --dry-run
bash "$HOME/.agents/scripts/install.sh"
```

Already using this clone? Pull the reviewed update and rerun the installer. It preserves personal files and
unrelated symlinks. Conflicts are printed, not overwritten. Dry run changes nothing, including dangling links.

- **Claude Code:** fresh setups get per-skill links in `$HOME/.claude/skills` and the team rule in
  `$HOME/.claude/rules`. Existing whole-directory skill/rule links keep working. Statusline and notifier links
  are created if absent. Manually merge the settings example into your existing settings; never replace the
  whole file. Keep the Notification hook only if the terminal's native notifications are insufficient.
- **Codex:** discovers `$HOME/.agents/skills` natively. The installer links the team file as
  `$HOME/.codex/AGENTS.md` only when absent; otherwise include it in your existing instructions yourself.
  Do not link this repository's contributor `AGENTS.md` as your global team instructions.
- **OpenCode:** discovers the shared skills natively. Add the installer-printed absolute team-file path to
  the `instructions` array in your global `opencode.json(c)`, preserving other entries. V2 honors
  `disable-model-invocation`; invoke a workflow explicitly with `@work`, `@fix-pr`, `@ship` or `@create-task`.
- **Cursor:** discovers the shared skills natively. Paste the team file into Customize > Rules > User Rules
  (or your approved Team Rules). Turn off Commit Attribution and PR Attribution; the CLI setting is
  `attribution.attributeCommitsToAgent: false`.

Claude Code and Cursor also honor `disable-model-invocation: true`. Codex behavior for that extension is not
verified here: the workflow bodies still require an explicit request. No skill grants permission to publish,
deploy, mutate data, spend or use a browser beyond the current task's authority.

### Skill catalogue

| Skill | Use when |
| --- | --- |
| [create-task](skills/create-task/SKILL.md) | Explicitly creating an issue, after open/closed duplicate search |
| [work](skills/work/SKILL.md) | Explicitly starting issue-governed implementation with one flat spec |
| [fix-pr](skills/fix-pr/SKILL.md) | Explicitly addressing live, original-commit-bound review findings |
| [ship](skills/ship/SKILL.md) | Explicitly preparing a release PR/draft for an already-bumped version |
| [debug-logs](skills/debug-logs/SKILL.md) | Capturing a bounded, non-sensitive browser reproduction timeline |
| [pr-merge-gates](skills/pr-merge-gates/SKILL.md) | Checking skipped CI, review cycles and merge identity |
| [release-verification](skills/release-verification/SKILL.md) | Proving serving versions, tags, schedules and queues |
| [production-debugging](skills/production-debugging/SKILL.md) | Discriminating opaque failures without leaking payloads |
| [database-migration-review](skills/database-migration-review/SKILL.md) | Reviewing live schema, history and atomicity boundaries |
| [reliability-review](skills/reliability-review/SKILL.md) | Testing real concurrency, retry and cache boundaries |
| [dependency-upgrades](skills/dependency-upgrades/SKILL.md) | Proving resolution, toolchain and artifact compatibility |
| [agent-work-verification](skills/agent-work-verification/SKILL.md) | Checking a coding agent's claims against independent evidence |

## What changed

- `commands/` is retired. `/create-task`, `/work`, `/fix-pr` and `/ship` keep their names as user-started skills.
- The old `$HOME/.claude/commands -> $HOME/.agents/commands` link now dangles. The installer removes only a
  recognized dangling legacy link; a real directory, working link or unrelated dangling link is preserved.
- `/review-changes`, `/review-code` and the personal `code-review` skill give way to built-in `/code-review`
  or `/review` in Claude Code, and `/review` in Codex/Cursor. The bundled Claude reviewer is no longer shadowed.
- `/debug` becomes `/debug-logs`; Claude Code's bundled `/debug` is restored. Logs go in Git-ignored `.debug/`,
  never specs, and contain no customer data, tokens or full URLs.
- `/explain` becomes `/output-style explanatory`; `/feature-plan` becomes `/plan` or plan mode.
  `/ultrathink` becomes `/effort` or the keyword in a normal prompt, not a slash command.
- `/handoff` becomes session `/compact` or `/resume` plus authorized PR/issue notes. `/format` uses the
  repository's own scripts. `/create-pr` is an ordinary request, and `/commit` conventions live in the team file.
- Six rules become `weaverse-team.md`. Specs are one flat dated file, not README/plan/work-log folders.
  A spec-only PR never closes the implementation issue. Version and changelog belong in the implementation.
- The copied `frontend-design` is removed. Use the licensed upstream version only where needed.
- `claude-code-hooks.json` becomes the settings example. Manually remove stale Stop/Session hooks and replace
  the unsupported `statusCommand` key with `statusLine`. Old notifier calls still reach the preserved script
  path but non-Notification events now do nothing. Windows uses text output rather than unsafe PowerShell interpolation.
- Whole-directory skill links still work, but per-skill links isolate future Claude installs better. `.gitignore`
  ignores non-team skill folders and installer locks; never force-add third-party content here. After a pull,
  validate in a clean checkout, not one containing ignored personal/third-party installs.

## Recommended upstream skills and tools

Install upstream, do not copy it into this library. Select only the skills needed. Pins below are reviewed
snapshots, not automatic updates. Run project installs in the relevant product repository, not this checkout.
`skills@1.7.6` needs Node >=22.20.0 and uses `#<commit>` for a source pin; `@<name>` selects a skill in that release.
Review the install preview and destination; no broad all-skills or auto-approval flags are needed.

### Onboarding first: Shopify telemetry opt-out

[Shopify AI Toolkit](https://github.com/Shopify/Shopify-AI-Toolkit) telemetry is on by default and can include
prompts and validation input. Before installing or activating it, create an **empty** opt-out file:

```bash
config_root="${XDG_CONFIG_HOME:-$HOME/.config}"
mkdir -p "$config_root/shopify-ai-toolkit"
: > "$config_root/shopify-ai-toolkit/opt-out"
```

An existing file containing `false`, `0`, `no` or `off` does not opt out. See upstream for Windows paths.
The team installer prints configuration guidance but does not perform this onboarding write for you.

### Adopt set (pinned)

1. **Shopify AI Toolkit / shopify** (MIT): live documentation/schema search and validation, rather than advice.
   User scope shown; select the agent(s) you use in the installer.

   ```bash
   npx skills@1.7.6 add 'Shopify/Shopify-AI-Toolkit#a3d20f8dc284a2e8ae25272fa79520888abb5dcb' --skill shopify -g
   ```

2. **[Hydrogen packaged skills](https://github.com/Shopify/hydrogen/tree/main/packages/hydrogen/skills)** (MIT):
   version-match to each storefront's frozen `@shopify/hydrogen` dependency (skills commands need >=2026.10.0).
   Add `skills:sync` / `skills:check` scripts using the installed `hydrogen skills sync` / `hydrogen skills check`.

   ```bash
   npm run skills:sync
   npm run skills:check
   ```

   Commit generated project skills in that storefront. CI runs **check**, never sync-before-check; the lockfile
   pins this source instead of a separate global skill version.
3. **[Weaverse Hydrogen skills](https://github.com/Weaverse/shopify-hydrogen-skills)**: product contracts and
   scripts. README claims MIT but the reviewed snapshot lacks LICENSE; confirm licensing before redistribution.

   ```bash
   npx skills@1.7.6 add 'Weaverse/shopify-hydrogen-skills#e20f3dad8418bc7113f36ca0b8ecb0f494fecb1b' --skill weaverse-hydrogen
   ```

4. **[Cloudflare skills](https://github.com/cloudflare/skills)** (Apache-2.0): current platform references.
   Start with the relevant skill, not the whole collection. A skill-only install does not configure its plugin's MCP.

   ```bash
   npx skills@1.7.6 add 'cloudflare/skills#6eb6c781aa9b6438e0c7307bd102788a75fe1a6d' --skill workers-best-practices
   ```

5. **[skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator)** (Apache-2.0):
   maintainers only, for trigger and behavior evaluations, not mass skill generation.

   ```bash
   npx skills@1.7.6 add 'anthropics/skills#2c5958ecac7cee2b583967a2c4981d0f4a75c579' --skill skill-creator -g
   ```

6. **[Next.js bundled docs](https://github.com/vercel/next.js)** (MIT): preserve the project's version-matched
   AGENTS.md docs index. If regeneration is needed, the reviewed generator is pinned (intentionally canary):

   ```bash
   npx @next/codemod@16.5.0-canary.46 agents-md
   ```

7. **[skills CLI](https://github.com/vercel-labs/skills)** (MIT): use the `npx skills@1.7.6` commands above.
   Review and commit the product repository's `skills-lock.json` for reproducibility. Never run an unreviewed
   update across every installed skill.
8. **[Agent Skills / skills-ref](https://github.com/agentskills/agentskills)** (Apache-2.0): pinned reference
   validator, installed by the validation commands below. Upstream labels it demonstrative; our stricter checks
   independently enforce portability, metadata types and budgets.

### Optional, not global defaults

- [Supabase](https://github.com/supabase/agent-skills) (MIT): trial vendor guidance in Supabase projects.
- [PlanetScale](https://github.com/planetscale/skills) (MIT): start with read-only reviews; live database changes
  retain their own approval gates.
- [Playwright CLI](https://github.com/microsoft/playwright-cli) (Apache-2.0): only in authorized browser-test scope.
- [Fly.io](https://github.com/superfly/skills) (MIT): for deployment owners, not every developer.
- [Official frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design) (Apache-2.0):
  opt-in prototypes, not automatic redesigns of existing themes.

Do not recommend `obra/superpowers` in Weaverse repositories: it overrides the team's process rules.

## Validation and maintenance

Prerequisites: Python >=3.11, ShellCheck and jq. Use Python 3.12 for CI parity. Install only into a dedicated venv:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-validation.txt
.venv/bin/python -m pip install --no-build-isolation --no-deps -r requirements-skills-ref.txt
PYTHON=.venv/bin/python bash scripts/validate.sh
.venv/bin/python -m unittest discover -s tests -v
```

Validation runs upstream `skills-ref` on standard frontmatter, excluding only the documented harness extensions
`disable-model-invocation` and `argument-hint` after checking their types. Unknown fields still fail.
Tests use disposable homes, a mocked read-only GitHub transport and notifier `--dry-run`; no notifications or
real tool-home installs occur. CI pins action releases by commit and runs the same validation and tests.

Review quarterly: retire new built-in overlaps, refresh the documented command-name snapshot and upstream pins,
and re-check license/telemetry changes. Before major changes or model/tool upgrades, run upstream skill-creator
with positive/near-miss trigger prompts and end-to-end cases; compare against no skill and report unrun evals.
See [AGENTS.md](AGENTS.md) for the frontier filter and public-repository privacy rules.

## License

[MIT](LICENSE), Copyright (c) 2026 Weaverse. Upstream recommendations retain their own licenses.
