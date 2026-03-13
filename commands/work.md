---
description: Start working on a GitHub issue — fetch context, create branch, plan solution, and optionally open a PR
---

# Work

Pick up a GitHub issue and set up everything needed to start working on it: understand the issue, create a feature branch, generate a spec-driven plan, and optionally push and open a PR.

## Usage

- `work` - Interactive mode, lists recent issues to choose from
- `work 42` - Start working on issue #42
- `work https://github.com/org/repo/issues/42` - Start from a full issue URL

## Process

### Step 1: Identify the issue

If `$ARGUMENTS` is provided, parse it:
- **Number only** (e.g., `42`) - treat as issue number in the current repo
- **Full URL** (e.g., `https://github.com/org/repo/issues/42`) - extract owner, repo, and number from the URL
- **Owner/repo#number** (e.g., `Weaverse/pilot#42`) - extract owner, repo, and number

If `$ARGUMENTS` is empty or not provided, list recent open issues and let the user pick:

```bash
gh issue list --state open --limit 20 --json number,title,labels,assignees
```

Present the issues to the user and ask them to select one.

### Step 2: Fetch and display issue details

```bash
gh issue view <number> --json title,body,labels,assignees,milestone,state,url
```

Display a concise summary of the issue so the user understands what they are about to work on:
- Title
- Body (truncated if very long)
- Labels, assignees, milestone
- URL

### Step 3: Create a feature branch

Suggest a branch name derived from the issue using a **type prefix**:

**Format**: `<type>/<kebab-case-description>`

Determine the type from the issue's labels, title, or body:

| Type | When to use | Examples |
|------|-------------|---------|
| `feat/` | New feature, new capability | `feat/dark-mode-toggle`, `feat/user-onboarding-flow` |
| `fix/` | Bug fix, error correction | `fix/cart-total-calculation`, `fix/null-pointer-in-auth` |
| `refactor/` | Code improvement, restructuring | `refactor/extract-payment-utils`, `refactor/simplify-auth-flow` |
| `docs/` | Documentation changes | `docs/api-reference`, `docs/setup-guide` |
| `chore/` | Maintenance, config, tooling | `chore/upgrade-dependencies`, `chore/ci-pipeline` |

**Branch name rules:**
- Lowercase the issue title
- Replace spaces and special characters with hyphens
- Strip non-alphanumeric characters (except hyphens and `/`)
- Collapse consecutive hyphens into one
- Truncate the description part to keep total branch name under ~60 chars
- No issue number in the branch name (the PR links to the issue instead)

If the type cannot be determined confidently, default to `feat/` and let the user confirm.

Ask the user to confirm or customize the branch name.

Then ask which branch to check out from:

```bash
# Show available remote branches for context
git branch -r --list 'origin/*' --sort=-committerdate | head -10
```

Present common options (e.g., `main`, `dev`) plus the list above. Let the user pick or type a custom base branch.

```bash
git fetch origin <base-branch>
git checkout -b <new-branch> origin/<base-branch>
```

### Step 4: Generate the implementation plan

This step follows **Spec-Driven Development (SDD)** conventions. The plan output goes into the `.specs/` folder, NOT the `.plans/` folder.

1. Create the spec folder: `.specs/{YYYY-MM-DD}--{kebab-case-title}/`

2. Create **`.specs/{folder}/README.md`** with the SDD template:

   ```markdown
   # Feature: [Issue Title]

   | Field            | Value                                     |
   | ---------------- | ----------------------------------------- |
   | **Status**       | in-progress                               |
   | **Owner**        | @<current git user or assignee>           |
   | **Created**      | YYYY-MM-DD                                |
   | **Last Updated** | YYYY-MM-DD                                |

   ## Original Prompt

   > [Paste the exact issue body here. Do not edit or paraphrase.]

   ## Summary

   [2-3 sentences. What this feature does and why it exists.]
   ```

3. Ask the user if they want to provide additional guidance or context for the planning phase (free text). This becomes extra input passed to the planning skill.

4. **Invoke the `feature-plan` skill** to generate `.specs/{folder}/plan.md`.
   - Pass the issue title, body, labels, and any user-provided guidance as the skill arguments
   - The skill will explore the codebase, ask clarifying questions, suggest solutions, and produce the plan
   - **Override the skill's output path**: the plan MUST be saved to `.specs/{folder}/plan.md` instead of the skill's default `.plans/` directory
   - The plan MUST be under 500 lines and MUST include a section listing all files/folders the feature touches

### Step 5: Commit and push the spec

After the plan is generated, ask the user:

> "Spec and plan are ready. Should I commit and push them to remote?"

If yes:
```bash
git add .specs/<folder>/
git commit -m "Add spec and plan for #<issue-number>: <short-title>"
git push -u origin <new-branch>
```

If no, skip to Step 6 (the spec stays as uncommitted local files).

### Step 6: Create a pull request (optional)

Ask the user:

> "Should I create a draft PR targeting `<base-branch>`?"

If yes:
```bash
gh pr create \
  --base <base-branch> \
  --head <new-branch> \
  --title "<issue-title>" \
  --body "$(cat <<'EOF'
## Summary

Spec and implementation plan for #<issue-number>.

See `.specs/<folder>/plan.md` for the full plan.

Closes #<issue-number>
EOF
)" \
  --draft
```

- Use `Closes #<number>` in the body to auto-link the PR to the issue.
- Create as **draft** since no implementation code exists yet.

### Step 7: Update issue status and assignee

First, assign the current user to the issue if not already assigned:

```bash
gh issue edit <number> --add-assignee @me
```

Then, if a PR was created, update the issue status on the project board (if the issue belongs to a project):

```bash
# Get project items for this issue
gh api graphql -f query='
{
  repository(owner: "<owner>", name: "<repo>") {
    issue(number: <number>) {
      projectItems(first: 10) {
        nodes {
          id
          project { id number title }
        }
      }
    }
  }
}'
```

For each project the issue belongs to, find the "Status" field and set it to "In Progress" (or the closest matching option):

```bash
gh project item-edit \
  --id <ITEM_ID> \
  --project-id <PROJECT_ID> \
  --field-id <STATUS_FIELD_ID> \
  --single-select-option-id <IN_PROGRESS_OPTION_ID>
```

If the issue is not on any project board, skip this step silently.

### Step 8: Summary

Output a final summary of everything that was done:

```
Issue:    #<number> - <title>
Branch:   <new-branch> (from <base-branch>)
Spec:     .specs/<folder>/
Plan:     .specs/<folder>/plan.md
PR:       <pr-url> (or "Not created")
Assignee: @<username> (assigned)
Status:   Updated to "In Progress" (or "No project board found")
```

## Error Handling

- If `gh` CLI is not installed or not authenticated, inform the user and stop
- If the issue number is invalid or not found, show the error and ask for a valid number
- If the branch name already exists, ask the user to pick a different name
- If `git checkout` fails (e.g., uncommitted changes), warn the user and suggest stashing or committing first
- If the `feature-plan` skill is not available, fall back to creating a minimal `plan.md` with the issue details and a TODO outline
- If push fails, show the error and let the user decide how to proceed

## Important Notes

- Always follow the **Spec-Driven Development** conventions from the global rules for the `.specs/` folder structure
- The `feature-plan` skill output MUST go to `.specs/<folder>/plan.md`, not `.plans/`
- The `README.md` in the spec folder preserves the **exact original issue body** as the "Original Prompt" — do not paraphrase
- The PR should be created as a **draft** since it only contains the spec, not implementation code
- Use `Closes #<number>` in the PR body to link the PR to the issue for automatic closure on merge
