---
name: create-task
description: "Create a Weaverse GitHub issue with duplicate detection and complete metadata. Use when explicitly asked to create a task or issue, not for implementation or review support on an existing issue."
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash
---

# Create task

1. Resolve the repository from the request and `gh repo view --json nameWithOwner`; do not assume the default
   checkout is the destination. If authentication or destination is missing, return the blocker, not a login wizard.
2. Search related issues in **all states**, across the organization as well as the target repository:
   `gh search issues '<topic>' --owner Weaverse --limit 100 --json number,title,state,url,repository`.
   Refine the search or paginate if results are truncated, and read likely matches with `gh issue view`.
   Reuse a genuine match even if closed. Reopening or editing it needs authority; a loosely related epic is not a match.
3. Read the issue template, labels, assignees, milestones, organization issue types and project fields.
   Use GET `orgs/Weaverse/issue-types` for types and `gh project field-list` for board field/option IDs.
   Use available assignee, labels, milestone, type, project, status and priority; distinguish absent from inaccessible.
4. Prepare the title, body and metadata together. Include outcome, scope/non-goals, acceptance and context.
   Show the final payload and destination for approval unless that exact scope is already approved.
   Do not invent fields or silently rewrite an approved body. In unattended work, return a specific blocker.
5. Create noninteractively using the supported `--type` flag, not an issue-type GraphQL mutation:

   ```bash
   gh issue create --repo "$REPO" --title "$TITLE" --body-file "$BODY_FILE" \
     --type "$TYPE" --assignee "$ASSIGNEES" --label "$LABELS" --milestone "$MILESTONE"
   ```

   Omit only metadata that is unavailable or intentionally unset in the approved payload.
   If the installed CLI lacks `--type`, report the version gap rather than starting an upgrade or workaround.
6. For an approved project, use `gh project item-add --url "$ISSUE_URL" --format json`, retain the item ID,
   then set single-select fields with `gh project item-edit --id ... --project-id ... --field-id ...
   --single-select-option-id ...`. Adding a project does not set its status or priority. Names are not field IDs.
7. Read the issue and project item back. If a board update fails after creation, report the existing issue URL
   and the incomplete field; do not create a duplicate on retry.

Report the issue URL, verified metadata, reused match (if any), and anything left unset with its reason.
