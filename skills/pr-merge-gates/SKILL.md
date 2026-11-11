---
name: pr-merge-gates
description: "Check GitHub signals that can falsely clear a Weaverse PR: skipped CI, remapped review comments, incomplete automated cycles and moving heads. Use when preparing, approving or merging a PR, not as a generic code-review checklist."
allowed-tools: Read, Grep, Glob, Bash
---

# PR merge gates

## Apparent green versus executed checks

- `gh pr checks` can exit 0 when material jobs were skipped. Require completed/success results for each material
  job on the current head, and explain any intentionally absent job. "No checks reported" is absence, not green.
- Marking a draft ready runs CI only if the workflow subscribes to `ready_for_review` or another matching event.
  Read `on`, branch/path filters and job conditions. Do not wait for a run that the workflow cannot create.
- `gh pr checks --required` can report no required checks when branch protection enforces none. Read all checks
  and the actual protection/ruleset separately; policy may require more than GitHub enforces.
- Re-runs and matrices can share names. Bind conclusions to the head, workflow/run ID, attempt and material job,
  not the first matching name or an old green row. Auto-merge waits only for enforced checks.
- A setup/download failure did not run tests. Report it as unexecuted, then rerun the **same** failed run only
  within authority. A test count in the PR body needs execution evidence behind it.
- For exported API changes, run any checked-in API/declaration report gate before review. A typecheck alone may
  trust an ambient `declare module` that only the production bundler will disprove.

## Review identity

- Read inline threads, formal review bodies and PR discussion. An empty body or `COMMENTED` state is not a pass.
  The `fix-pr` helper filters GraphQL threads by `isResolved=false` and `isOutdated=false`; flat comments cannot.
- Wait for the repository's automated-review completion signal on this exact trigger and head. Multiple findings
  can arrive minutes apart. A reaction is sufficient only where the repository explicitly uses it as a verdict;
  require the configured reviewer's identity and creation after the latest trigger. Quiet time is not completion.
- Match the configured reviewer's account on each API surface; app and bot identities can differ. Do not hardcode
  a person's handle or accept any user's reaction as the automated verdict.
- Bind a remapped finding to `original_commit_id` and creation time, not only `commit_id`. Classify it against
  current source before rewriting a working fix. Severity labels inform, but do not replace, impact assessment.
- A clean automated review does not waive required human approval or `reviewDecision: REVIEW_REQUIRED`.
- If a finding disproves the PR description, correct the claim as well as the code. A failed or partial review
  is not a review pass; findings from a previous SHA remain historical until rechecked.

## Placebo changes and ancestry

- Rebuild with and without a suspected configuration fix at the real command boundary. Framework CLIs can
  override Vite config inline; a changed source value may produce an identical deployment artifact.
- Check supersession against the **current** base and serving history. Older PRs can restore older file content
  without conflicts. Inspect a disposable integration result; patch equivalence alone does not establish ancestry.
- Resolve generated-artifact conflicts by regenerating from the combined sources, then run the generator's
  check. Do not hand-merge lockfiles, API reports or spec indices just to remove conflict markers.

## Authorized publication and merge

- Read workflow triggers before pushing: `on: [push]` can deploy feature branches. Inherited push configuration
  can publish extra refs or tags; use an explicit refspec with tag-following disabled:

  ```bash
  git -c push.default=nothing -c push.followTags=false push origin "$SHA:refs/heads/$BRANCH"
  ```

- Pass PR prose with `--body-file` to avoid shell expansion of backticks and dollar signs.
- Use only supported `gh pr view --json` fields; one invalid field aborts the whole read. The REST PR resource
  gives both exact repository identities when abbreviated CLI fields are insufficient.
- Within merge authority, use `gh pr merge --match-head-commit "$SHA"`, then read merged status and the resulting
  base commit back. If the base moved or the merge strategy changes the tree, recheck the integration result.
  Even on an unchanged base, require the merged tree to match the reviewed tree; do not assume it.
- Attribute a newly red base gate by executing the same gate on candidate and base, not by guessing from history.
  Development-branch merge and production delivery are separate outcomes.

Report `READY`, `BLOCKED` or `NOT REVIEWABLE`, with head SHA, executed/absent checks, review-cycle evidence and
live blockers bound to original commits. This playbook never grants publication or merge permission.
