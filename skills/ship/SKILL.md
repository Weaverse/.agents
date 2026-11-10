---
name: ship
description: "Prepare the normal release PR and a draft GitHub release for an already-bumped Weaverse version. Use when explicitly asked to ship; never treat invocation as permission to merge, deploy, tag or publish."
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash
---

# Ship an already-prepared version

1. Read the repository release policy, actual base/default branches, dirty state and workflow triggers.
   Reuse the implementation PR and its evidence. If a normal production release PR is required, that is still
   allowed; a separate version-bump branch or PR is not.
2. Verify that the version, lockfile and visible changelog already landed in the implementation change **before
   final review and CI**. Do not choose a new calendar date or bump at release time. Missing metadata goes back
   into the same implementation change, followed by the required review and gates. If already merged, disclose
   missing copy and fold it into the next substantive update, not a bookkeeping-only PR.
3. Freeze the reviewed commit and tree, and check CI/review on that identity with `pr-merge-gates`.
   A moving branch name or historical approval is not the release candidate.
4. If authorized to push, use one explicit branch refspec with follow-tags disabled. Read triggers before pushing;
   a bare push workflow may deploy every branch. Never add tags as a side effect of preparing the release.
5. Draft the GitHub release for the repository's tag convention and the **already-bumped** version, using the
   full candidate SHA as target rather than a moving branch. Generated notes replace hand-built contributor lists:

   ```bash
   gh release create "$TAG" --repo "$REPO" --target "$REVIEWED_SHA" \
     --title "$TAG" --draft --generate-notes
   ```

   Read an existing draft before editing it. If the tag already exists, resolve it first and stop on a mismatch.
   Read back the draft status, tag name and notes. Report "draft prepared", not "released".
6. Merge, deploy and publish only if separately within the approved scope. Follow `release-verification` and
   prove production before publishing the tag/Release. If merge strategy changes the commit SHA, re-bind review
   and deployment evidence to the resulting commit; tree equivalence alone is not SHA equality.
7. After publishing, fetch the remote tag into a task-owned inspection ref (do not overwrite an existing local
   tag). Peel annotated tags with `git rev-parse "$TAG_REF^{commit}"` and require equality with the **reviewed
   and deployed** commit. `target_commitish`, a release page and `git ls-remote`'s annotated tag-object ID alone
   are not proof of the commit. Stop on a mismatch; do not move a published tag to hide it.

Report version, reviewed SHA/tree, PR, draft/published Release status, serving identity and peeled remote tag
identity. Keep preparation, merge, deployment and publication distinct, with explicit unverified steps.
