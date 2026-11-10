---
name: agent-work-verification
description: "Verify a coding agent's returned branch against Git, gate and artifact evidence. Use when delegating bounded implementation or accepting agent-built work, especially when reports claim clean state, baseline failures or published artifacts."
allowed-tools: Read, Grep, Glob, Bash
---

# Accepting agent-built work

## Preserve the task contract

- Give one writer ownership of the outcome across source, schema, tests and docs. Include repository, branch,
  exact base, authoritative dirty work, required surviving capabilities, forbidden side effects and expected
  commands/results. Never put a second writer into a live owner's checkout.
- Pass a brief file rather than long Markdown in a double-quoted shell argument: backticks can execute and
  transports can truncate it. A mid-run correction should identify only the changed contract and affected boundary.
- A deletion-only brief can remove the sole creation path across repositories. Name the capability to preserve,
  and check replacement SDK types/actual dispatch before accepting a keyword match as feature parity.

## Authenticate the return

```bash
git branch --show-current
git rev-parse HEAD
git status --short --untracked-files=all
git log --oneline -5
git reflog -10
git diff --stat <base>...HEAD
git diff --check <base> HEAD
```

- A clean checkout's bare `git diff --check` checks no committed change. Include new/untracked files in the
  inventory. Check staged bytes against what will actually commit, not only working-tree text.
- A canonical checkout may be sitting on the candidate too. Authenticate both candidate and exact base before
  comparing test totals. Read the target's current tip and inspect whether landing would discard intervening work.
- If a claimed commit is missing, inspect reflog/object history without resetting or writing lost-found output.
  Preserve the complete recovered chain on a task-owned ref only within authority; do not reset to the first
  orphan found and lose its descendants.
- Inspect push configuration and use an explicit `SHA:refs/heads/branch` with follow-tags disabled when pushing
  is authorized. Do not infer a destination from the local branch name or upstream alone. A mistaken push needs
  immediate disclosure and an approved recovery, not an automatic force-push.
- Missing SSH allowed-signers configuration makes `git verify-commit` inconclusive, not proof of an invalid
  signature. Establish the verifier's trusted identity without weakening signing or verification guards.

## Evidence stronger than a completion report

- Claimed image publication, resource creation and releases need registry/platform readback at the exact
  identity. A build log, local tag or intended URL does not prove the consumer can fetch the artifact.
- For "pre-existing failures", execute the **same failing gate** on the exact base in an isolated checkout
  using its own correctly resolved workspace dependencies. Regenerate ignored prerequisites without applying
  schema or copying the candidate fix. A symlinked dependency graph can secretly execute the candidate.
- Compare failure signatures, not just totals. Rotating failures can be timing/load-sensitive. A failure present
  at base establishes attribution; it does not waive a release gate or justify saying the gate passed.
- Keep logs tied to their command's working directory, exit and SHA. A wrapper's trailing echo or a cached log
  can mask failure. An errored/partial reviewer supplies no clean verdict; historical SHA reviews need rechecking.
- Verify a missing-runtime/tool claim before authorizing a workaround. Never source an agent's environment file
  into the persistent shell; inspect it and use the approved isolated environment for reproduction.
- Check deletion effects before reverting or accepting them. A removed module may be inert, or it may be the
  only remaining lifecycle path; import counts alone cannot prove dynamically dispatched behavior.

## Boundaries to inspect explicitly

- Re-scan the exact migration diff and ledger. A follow-up correction can silently edit applied history.
  `database-migration-review` owns numbering, snapshots, live-catalog and unresolved-operation proof.
- A config/filter change can make the target test pass by excluding unrelated tests. Compare executed file sets,
  not only total counts. For a Dockerfile change, build the real target or report image behavior unproven.
- Copy/clone/move/import operations need `sourceId === targetId` and tenant-boundary cases; a nontransactional
  read-then-write can duplicate children or erase settings even when ordinary inputs pass.
- A source fix and green test are not enough if production cannot reach the branch. Use
  `production-debugging` for payload-shape, path-reachability and negative-control proof.
- Retire a worktree only when its work is retained, it is clean (including untracked files) and no live owner
  uses it. Ignored dependency trees are not protected by a clean status; preserve anything valuable first.
  Use native `git worktree remove` within authorization, never force removal as an inspection shortcut.

Report verified branch/base/SHA/tree, changed paths, actual gate exits, artifact identities and remaining gaps.
Keep unverified claims explicitly separate; this playbook does not authorize recovery writes or publication.
