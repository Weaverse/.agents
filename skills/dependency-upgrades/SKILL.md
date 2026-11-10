---
name: dependency-upgrades
description: "Verify npm/pnpm upgrades and JavaScript toolchain replacements beyond install success: peer-policy masking, hook rewrites, linter parity and artifact compatibility. Use when upgrading dependencies, fixing advisories or replacing lint, format, compiler or build tools."
allowed-tools: Read, Grep, Glob, Bash
---

# Dependency and toolchain upgrades

## Resolution is not compatibility

- `npm ci` with `legacy-peer-deps=true` does not establish peer compatibility. Inspect effective npm config and
  `.npmrc` files. If claiming strict compatibility, run an isolated frozen install with
  `--legacy-peer-deps=false --strict-peer-deps=true`; do not silently change the repository's persistent policy.
- Lifecycle scripts can rewrite shared Git hooks in worktrees. Record hook state before an install and compare
  afterwards. Use an authorized script-free install plus explicit generation when appropriate; do not mistake
  missing generated artifacts for an application defect or weaken hooks to get a green result.
- Query registry metadata for the exact release. `latest` can be a prerelease; aliases and calendar versions need
  semantic review. Respect release-age policy and report held versions. Compare lockfile integrity for advisories.
- Prefer a narrow transitive/lockfile change where the parent already admits the patch. A major override needs
  testing at the actual consuming boundary, not just an import. Never dismiss an advisory to clear a count.
- Check the advertised Node range against every resolved dependency's engines. A lower bound also promises
  future majors that dependencies may exclude; update runtime selectors, package metadata and docs together.
- Resolve duplicate framework/SDK copies: registration through one copy may not reach dispatch through another.

## Audit evidence

- Keep GitHub alerts, package-manager advisories and unique packages separate. Zero open alerts does not prove
  the frozen lockfile is clean; equal totals do not prove the same findings. A local fix does not close a
  default-branch alert. Record audit exit separately from any successful collection wrapper.
- "Unreachable" requires tracing the real consumer, including export/SSR paths that accept stored content.
  When no patched version exists, inspect the parent upgrade or removal path rather than forcing incompatibility.

## Toolchain parity

- Review migrator edits to manifests, catalogs, overrides, scripts, hooks and source. Cached task runners can
  strip environment overrides; test the real child with a harmless sentinel rather than trusting the wrapper.
- Print resolved linter configuration for source and test files. Trigger each previously enforced rule as a
  positive control, especially hooks/accessibility and type-aware rules that can silently be disabled.
- Translated suppressions need the new diagnostic span, not just a renamed rule ID. Prove both the intended
  exception and a fresh violation. A warning-level autofix may still rewrite source in a supposedly check-only lane.
- To claim no formatter churn, format the **baseline** in a disposable copy and count changed paths. A green
  check of already-reformatted candidate files proves only a fixed point.
- Import sorting changes module side-effect order; moving a JSX prop across a spread changes precedence.
  Review execution/AST order, not only token equality. Exercise the real fix/staged-file hook path.
- Keep framework route/code generation before typecheck. API/declaration consumers still using the old compiler
  make a compiler migration incomplete even if the main typecheck is green.

## Tests and deliverables

- A suite named unit can launch a browser. Read fixtures before executing it and retain browser permission gates.
  After runner/filter changes, compare executed file sets and full test-name multisets, not just counts.
- For wire changes, test the unchanged deployed client's parser. Upgrading both test SDK and server can make
  them agree on a format old clients reject.
- For package builders, compare ESM/CJS loading, export targets, declarations, sourcemaps, tarball paths and API
  reports. Equal counts are not parity. Recompute after the final bundler edit; overload and union changes need
  semantic review even when nearby quote/order changes are cosmetic.
- Cached Turbo/Nx logs are replayed evidence, not fresh execution. Pass force flags to the task runner itself,
  not through `--` to its child. Container install/prune changes need the real production image target;
  a host build cannot prove that stage.
- Transitive packages can break a pinned parent's imports. Inspect the resolved graph and known-good lockfile
  before proposing an unrelated major upgrade; test scoped overrides in isolation.

Before handing off manual testing, install the frozen graph and regenerate local clients/types/icons/bundles
without schema pushes. State branch, SHA, runtime, executed versus cached gates and unverified image/browser work.
