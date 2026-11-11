# Weaverse team instructions

A repository's own AGENTS.md, CLAUDE.md or rules win where they differ from this file.

## Working style
- A question asks for an answer or a proposal. Change files only when asked to act.
- Do not stage, commit or push unless asked in the current conversation.

## Commits and pull requests
- Use plain English commit sentences, such as "Add pagination to reviews", without feat: or fix: prefixes.
- When asked to commit, group related changes into logical commits.
- No AI attribution in commits or PR descriptions: no Co-Authored-By or "Generated with" lines.
- Run the repository's own format, lint, typecheck and required tests before committing.
- PR claims need observed evidence; correct the description when a finding disproves it.
- Merged to a development branch is not released. Report merge and production delivery separately.
- Version bumps and changelog ship in the implementation change before final review and CI.
- Never create a separate version-bump branch or PR; retain any normal production release PR.

## Issues, specs and handoffs
- New substantive implementation starts from a matching issue. Search open and closed issues and reuse a real match.
- Create issues with assignee, labels, milestone, type and project fields when available; do not invent metadata.
- Review, verification and release support reuse the existing PR or issue, without ceremonial tracking files.
- Use one flat YYYY-MM-DD-what-update.md in the existing spec root; keep its creation-date path stable.
- Builder and SDK use .specs/; Pilot uses .weaverse/specs/. Reuse the closest canonical contract.
- Include Outcome; Scope and non-goals; Acceptance; Approach; Verification. Small fixes use the issue as the spec.
- Issue owns tracking; PR owns observed evidence. No plan, work-log or handoff files unless requested.
- Use "Closes #n" only for full resolution in a PR targeting the default branch, never for a spec-only PR.
- For a non-default target, use a supported explicit Development link and read it back; do not retarget just to link.
- Handoff notes go in the PR or issue, within publication authority.

## TypeScript and React (unless the repository says otherwise)
- Use function declarations, except where a framework convention needs an arrow function.
- Use named exports; default exports only where required, such as routes or Weaverse sections.
- Use let for variables; const only for ALL_CAPS module constants.
- Use the repository's cn() helper for conditional classes, never template strings; use cva for variants.
- Use kebab-case file names and no barrel index files.
- Skip useMemo and useCallback only in repositories that actually enable React Compiler.
