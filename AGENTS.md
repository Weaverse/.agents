# Contributing to .agents

This public repository holds Weaverse's team rules, first-party skills and optional Claude Code glue.
The shared instructions live in `rules/weaverse-team.md`; follow them when changing this repository.

## Add a skill
- Put it in `skills/<lowercase-hyphen-name>/SKILL.md` and add its folder to the `.gitignore` allowlist.
- Match `name` to the folder (1 to 64 ASCII lowercase letters, digits and single hyphens).
- Set a string `description` of at most 1024 characters, including a specific "Use when" trigger.
- Keep `metadata` a string-to-string map; use `allowed-tools` for tool hints, not `metadata.tools`.
- Set `disable-model-invocation: true` for workflows that only a person should initiate.
- Avoid built-in command names; `scripts/claude-commands.json` records the checked collision list.
- Keep each skill under 150 lines where practical; 500 lines is the validation ceiling.

## Apply the frontier filter
- Keep only team contracts, executable helpers, current platform traps or verification a model would miss.
- Cut generic advice and incident narratives. Explain the non-obvious failure, not textbook practice.
- Reference maintained upstream skills with pinned sources. Do not copy third-party skills here.
- Keep customer data, personal names, private paths, identifiers and credentials out of every public file.

## Verify and maintain
- Install the pinned validation dependencies as described in `README.md`, then run `bash scripts/validate.sh`.
- Test installer changes only with a throwaway `HOME`; use `--dry-run` before any real installation.
- Test notifications with `--dry-run`; never send a desktop notification from a test.
- Keep shell files compatible with Bash 3.2 and check them with ShellCheck.
- Update the README catalogue and migration notes with behavior changes.
- Review quarterly; use upstream skill-creator evaluations before major skill changes or model/tool upgrades.
