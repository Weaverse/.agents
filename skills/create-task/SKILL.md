---
name: create-task
description: "[Skill] Create a GitHub issue in the Weaverse org, add it to a project, and set all metadata (status, priority, labels, milestone, type). Use when user wants to create a new task/issue."
argument-hint: "[task description or requirements]"
allowed-tools: "Bash, AskUserQuestion"
---

Create a new GitHub issue in the Weaverse organization with full project board integration.

## Org Context

- **GitHub Org:** Weaverse
- **Org Members:** hieuht09, hta218, imsinhp, NamTM-24, paul-phan, viethung26

## Workflow

Follow these steps **in order**. Use `AskUserQuestion` (the `mcp_question` tool) to gather all required info before creating anything.

### Step 1: Ask which project

Fetch the list of projects dynamically:

```bash
gh project list --owner Weaverse --format json --jq '.projects[] | "\(.number) \(.title)"'
```

Then ask the user to select a project. Include a "None (no project)" option.

### Step 2: Ask for repo, title, assignee, and description

Ask these in a single question block if possible:

1. **Repository** - List repos from the org. Run:
   ```bash
   gh repo list Weaverse --json name --jq '.[].name' --limit 50
   ```
   Let user select one.

2. **Title** - Ask for the issue title (free text).

3. **Assignee** - Let user select from org members: `hieuht09, hta218, imsinhp, NamTM-24, paul-phan, viethung26`. Allow multiple selections. Include an "Unassigned" option.

4. **Description/Body** - Ask for the issue body content (free text). If user provides `$ARGUMENTS`, pre-fill from that.

### Step 3: Ask for metadata

If a project was selected in Step 1, fetch the project's fields:

```bash
gh project field-list <PROJECT_NUMBER> --owner Weaverse --format json
```

Then ask the user to set:

1. **Status** - Show the available status options from the project's SingleSelect fields (e.g., Todo, In Progress, In Review, Done, Closed).

2. **Priority** - Show available priority options if the project has a Priority field (e.g., High, Medium, Low). Include a "None" option.

3. **Labels** - Fetch labels from the selected repo:
   ```bash
   gh label list --repo Weaverse/<repo> --json name --jq '.[].name'
   ```
   Let user select multiple. Include a "None" option.

4. **Milestone** - Fetch milestones from the selected repo:
   ```bash
   gh api repos/Weaverse/<repo>/milestones --jq '.[].title'
   ```
   Let user select one. Include a "None" option.

5. **Issue Type** - Fetch issue types from the repo:
   ```bash
   gh api graphql -f query='{ repository(owner: "Weaverse", name: "<repo>") { issueTypes(first: 20) { nodes { id name } } } }'
   ```
   Let user select one (e.g., Task, Bug, Feature). Include a "None" option.

### Step 4: Create the issue

```bash
gh issue create \
  --repo Weaverse/<repo> \
  --title "<title>" \
  --body "<body>" \
  --assignee "<assignee1>,<assignee2>" \
  --label "<label1>,<label2>" \
  --milestone "<milestone>"
```

Use a heredoc for the body to preserve formatting:
```bash
gh issue create --repo Weaverse/<repo> --title "<title>" --assignee "<assignees>" --body "$(cat <<'EOF'
<body content>
EOF
)"
```

Omit `--assignee`, `--label`, `--milestone` flags if the user selected "None" for those.

### Step 5: Set issue type (if selected)

Get the issue node ID:
```bash
gh api repos/Weaverse/<repo>/issues/<number> --jq '.node_id'
```

Then set the type:
```bash
gh api graphql -f query='mutation { updateIssueIssueType(input: { issueId: "<issue_node_id>", issueTypeId: "<type_id>"}) { issue { id } } }'
```

### Step 6: Add to project and set project fields

If a project was selected:

1. Add the issue to the project:
   ```bash
   gh project item-add <PROJECT_NUMBER> --owner Weaverse --url <issue_url> --format json
   ```
   This returns the item ID.

2. Parse the item ID from the JSON output (field: `id`).

3. Set **Status** on the project item:
   ```bash
   gh project item-edit \
     --id <ITEM_ID> \
     --project-id <PROJECT_ID> \
     --field-id <STATUS_FIELD_ID> \
     --single-select-option-id <STATUS_OPTION_ID>
   ```

4. Set **Priority** on the project item (if selected and field exists):
   ```bash
   gh project item-edit \
     --id <ITEM_ID> \
     --project-id <PROJECT_ID> \
     --field-id <PRIORITY_FIELD_ID> \
     --single-select-option-id <PRIORITY_OPTION_ID>
   ```

### Step 7: Confirm

Output a summary of what was created:
- Issue URL
- Repository
- Assignees
- Labels, Milestone, Type
- Project, Status, Priority

## Important Notes

- Always use `--format json` when you need to parse output from `gh` commands.
- Use the project's internal IDs (from `field-list`) for `item-edit` commands, not display names.
- If any `gh` command fails, show the error to the user and ask how to proceed.
- The `--project` flag on `gh issue create` does NOT set project field values -- you must use `gh project item-add` + `gh project item-edit` separately.
- For issue body, always use heredoc syntax to preserve multiline formatting.
