---
description: Create a GitHub issue with project board integration
---

# Create Task

Create a GitHub issue with full metadata and optional project board integration.

## Usage

- `create-task` - Interactive guided issue creation
- `create-task Add dark mode support` - Pre-fill the title/description from arguments

## Behavior

Load and follow the `create-task` skill. The skill guides through:

1. **Detect owner** - Auto-detect GitHub owner/org from current repo, or ask
2. **Select project** - Choose a GitHub project board (optional)
3. **Issue details** - Repo, title, assignees, description, and content style preferences
4. **Enhance description** - Rewrite the raw description into a polished issue body
5. **Metadata** - Status, priority, labels, milestone, issue type
6. **Create & configure** - Create the issue, set type, add to project with field values
7. **Confirm** - Output a summary with issue URL and project board deep link

Pass `$ARGUMENTS` to pre-fill the issue title and description.
