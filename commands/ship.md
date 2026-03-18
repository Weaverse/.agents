---
description: Create a release PR to main with version bump and draft a GitHub release
argument-hint: "[optional version number or extra notes]"
---

# Ship

Create a pull request from the current working branch to `main`, ensure the version is bumped, and draft a GitHub release. The user will review, merge, and publish manually.

## Usage

- `/ship` — auto-detect versioning scheme and walk through the process
- `/ship 2.5.0` — use a specific version
- `/ship patch` — shorthand for semver bump type

## Process

### Step 1: Preflight checks

Run these commands in parallel to understand the current state:

```bash
git status
git branch --show-current
git log main..HEAD --oneline
gh auth status
```

Verify:
- There are no uncommitted changes. If there are, warn the user and stop.
- The current branch is NOT `main`. If it is, warn the user and stop.
- There is at least one commit ahead of `main`. If not, inform the user there is nothing to ship.
- `gh` CLI is authenticated. If not, inform the user and stop.

### Step 2: Collect all changes since main

```bash
git log main..HEAD --pretty=format:"%h %s (by @%an)" --no-merges
```

Also gather PR numbers if commits came from merged PRs:

```bash
git log main..HEAD --pretty=format:"%h %s" --no-merges
```

For each commit, check if it is associated with a PR:

```bash
gh api repos/{owner}/{repo}/commits/{sha}/pulls --jq '.[0].number' 2>/dev/null
```

Build a list of all changes with their authors and references (commit hash or PR number).

### Step 3: Check version and detect versioning scheme

Read the current version from `package.json`:

```bash
node -p "require('./package.json').version"
```

Detect the versioning scheme:

| Scheme | Pattern | Examples |
|--------|---------|---------|
| **Semver** | `MAJOR.MINOR.PATCH` | `2.5.0`, `1.0.3`, `0.9.1` |
| **Calendar versioning** | Contains year/month/date-like segments | `2026.3.18`, `25.03.1` |

**If `$ARGUMENTS` provides a version or bump type**, use it:
- Exact version (e.g., `2.5.0`) — use as-is
- Bump type (`major`, `minor`, `patch`) — calculate the next version from current

**If `$ARGUMENTS` does not specify a version**, check if the version was already bumped compared to `main`:

```bash
git show main:package.json | node -p "JSON.parse(require('fs').readFileSync('/dev/stdin','utf8')).version"
```

- If the version is **the same** as `main`, a bump is required — ask the user (see below).
- If the version is **already different** from `main`:
  - **Semver**: the version is already bumped. Use the current version and skip to Step 4.
  - **Calendar versioning**: the version may be stale (bumped days or weeks ago). Always ask the user to confirm — see the calver prompt below.

**For semver** (when bump is needed), present the options:

> Current version: `2.4.1`
>
> What version bump do you need?
> - **patch** -> `2.4.2` (bug fixes, small changes)
> - **minor** -> `2.5.0` (new features, backward compatible)
> - **major** -> `3.0.0` (breaking changes)

**For calendar versioning** (always ask, even if already different from main):

> Current version: `2025.12.3`
>
> Today's date version: `2026.3.18` (Recommended)
>
> Use today's date as the version, keep current (`2025.12.3`), or enter a custom one?

If the user picks today's date, update the version. If they choose to keep the current version, skip the bump. If they enter a custom version, use that.

### Step 4: Apply version bump

If a version bump is needed (version same as main, or calver and user chose a new version):

Update `package.json` with the new version. Use a precise edit — only change the `"version"` field.

Then re-install dependencies to update the lock file:

```bash
ni
```

Commit the version bump:

```bash
git add package.json
# Also stage the lock file (package-lock.json, pnpm-lock.yaml, yarn.lock, bun.lockb — whichever exists)
git add package-lock.json pnpm-lock.yaml yarn.lock bun.lockb 2>/dev/null
git commit -m "Bump version to <new-version>"
```

Push the branch:

```bash
git push -u origin $(git branch --show-current)
```

### Step 5: Create the PR to main

Build the PR title using the version and a summary of changes:

**Title format**: `v<version> - <short summary of changes>`

The short summary should capture the main themes from the changes (features, fixes, optimizations). Keep it under 72 characters total. Examples:
- `v2.5.0 - Add dark mode, fix cart calculation, optimize image loading`
- `v2026.3.18 - Redesign settings page, update dependencies`

Build the PR body by grouping changes into categories:

```markdown
## What's in this release

### New features
- Add dark mode toggle (#45)
- Add user onboarding flow (#52)

### Bug fixes
- Fix cart total when discount applied (#48)
- Fix null pointer in auth middleware (a1b2c3d)

### Improvements
- Optimize image loading for product pages (#50)
- Refactor payment utils for reusability (#51)

### Other
- Update dependencies (d4e5f6g)
```

**Grouping rules:**
- Scan each change's commit message or PR title to determine the category
- Features: new functionality, "add", "implement", "introduce"
- Bug fixes: "fix", "resolve", "correct", "patch"
- Improvements: "optimize", "refactor", "improve", "update", "enhance", "clean up"
- Other: anything that does not fit the above (config, docs, chore, deps)
- Skip empty categories
- Each item references either `#<PR-number>` or `<short-commit-hash>` depending on what is available

Create the PR:

```bash
gh pr create \
  --base main \
  --head "$(git branch --show-current)" \
  --title "v<version> - <short summary>" \
  --body "$(cat <<'EOF'
<the grouped changelog body from above>
EOF
)"
```

### Step 6: Draft a GitHub release

Create a draft release targeting `main` with tag `v<version>`.

Build the release body. List all changes, each in this format:

```
<description of change> by @<author> in #<PR-number>
```

or if no PR exists for that change:

```
<description of change> by @<author> at <commit-hash>
```

**Rules for the release body:**
- Use simple English, no emojis
- Remove duplicate entries (same change appearing in multiple commits)
- Skip trivial changes (typo fixes, formatting-only, merge commits)
- Group by category (same groups as the PR body) if there are more than 10 items
- If 10 or fewer items, a flat list is fine
- Each line starts with a capital letter
- Add a "New Contributors" section at the end if there are first-time contributors to the repo (check with `gh api`)

```bash
gh release create "v<version>" \
  --target main \
  --title "v<version>" \
  --draft \
  --notes "$(cat <<'EOF'
## What's Changed

- Add dark mode toggle by @hta218 in #45
- Fix cart total calculation when discount is applied by @dev2 in #48
- Optimize image loading for product pages by @hta218 in #50
- Update dependencies by @hta218 at a1b2c3d

**Full Changelog**: https://github.com/<owner>/<repo>/compare/v<prev-version>...v<version>
EOF
)"
```

Always append a "Full Changelog" link at the bottom comparing the previous version tag to the new version.

### Step 7: Summary

Output a final summary:

```
Ship complete!

Version:  v<version>
PR:       <pr-url>
Release:  <release-url> (draft)

Next steps:
  1. Review the PR:      <pr-url>
  2. Review the release:  <release-url>
  3. Merge the PR
  4. Publish the release
```

## Error Handling

- If `gh` CLI is not installed or not authenticated, inform the user and stop
- If there are uncommitted changes, warn and stop — do not auto-commit
- If already on `main`, warn the user and stop
- If no commits ahead of `main`, inform the user there is nothing to ship
- If `package.json` does not exist, skip version bump logic and ask the user for a version string to use in the PR title and release tag
- If `ni` fails, show the error and ask the user if they want to continue without updating the lock file
- If PR creation fails (e.g., PR already exists), show the error and provide the URL to the existing PR
- If release creation fails, show the error but still report the PR as successful
- If push fails, show the error and let the user resolve it

## Important Notes

- This command does NOT merge the PR or publish the release — the user does that manually
- The release is always created as a **draft**
- The PR targets `main` unless the user specifies otherwise via arguments
- Use `ni` (not `npm install` or `pnpm install`) to re-install — it auto-detects the package manager
- Do NOT create a git tag locally — the tag is created by GitHub when the release is published
- Keep the PR title concise but descriptive — it becomes the merge commit message

## User Arguments

$ARGUMENTS
