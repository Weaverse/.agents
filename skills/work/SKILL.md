---
name: work
description: "Start issue-governed Weaverse implementation using the repository's branch policy and one flat spec. Use when explicitly asked to pick up an issue; not for review, verification or release support on existing work."
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash
---

# Work from an issue

1. Read repository instructions and the requested issue, including its discussion and existing Development links.
   If no issue is named, search related open **and closed** Weaverse issues and read likely matches before choosing.
   Reuse a genuine match; creating, reopening or changing an issue is a separate authorized external write.
2. Resolve the actual PR base and remote default separately. Preserve the current owner's branch and dirty work.
   Follow the repository's branching policy; do not assume main, change branches under active work, or stash to inspect.
3. For new substantive implementation, verify the matching issue before changing source. Small clear fixes can use
   the issue as the mini-spec. Support on an existing PR reuses its issue/spec without extra tracking documents.
4. Search for the closest canonical spec before creating one. Use **one flat** `YYYY-MM-DD-what-update.md`
   directly in the repository's existing spec root (`.specs/` or `.weaverse/specs/`, per the team rule).
   Keep the original creation-date path when updating. Include the exact issue URL or `Weaverse/repo#number`.
5. The single file contains these sections, without duplicating the issue's owner, status or priority:

   ```markdown
   ## Outcome
   ## Scope and non-goals
   ## Acceptance
   ## Approach
   ## Verification
   ```

   No feature/month folder, per-spec README, parallel plan, work-log or handoff file unless requested.
   Link one shared contract across repositories instead of copying it. Leave unrelated legacy specs alone;
   consolidate a legacy outcome only when substantively editing it, preserving history and backlinks.
6. Implement within the agreed scope and run the repository's gates. Include required version/changelog changes
   in this implementation before final review and CI, never in a later version-only preparation branch.
7. Commit, push, publish a PR or update project metadata only within the requested authority. A spec-only PR
   references the issue without `Closes #n`. Only a default-target PR fully resolving the issue uses a closing
   keyword. A legitimate non-default target needs a supported explicit Development link, verified by readback;
   never retarget or close a broader issue merely to satisfy tracking.

Report issue, branch/base, spec path (or issue-as-spec), actual checks and remaining work. Evidence belongs in the
existing PR; no new handoff document is needed.
