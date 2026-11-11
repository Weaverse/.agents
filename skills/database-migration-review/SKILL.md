---
name: database-migration-review
description: "Review Prisma/PlanetScale and Cloudflare D1 schema changes at the live catalog and atomicity boundaries. Use when merging schema-consuming code, approving migration SQL or applying a migration; not for generic SQL style review."
allowed-tools: Read, Grep, Glob, Bash
---

# Database migration review

## Ordering and history

- A green build exercises the repository schema, not the target catalog. If the deployment has no schema step,
  prove schema availability before code cutover. An additive column/index can still reject old writers through
  NOT NULL, unique, CHECK or trigger constraints. Exercise both deployed and candidate write shapes.
- Read the migration ledger before editing history. Applied files are immutable; use a new migration and retain
  historical hashes/snapshots. If parallel branches allocate one number, renumber only the unapplied local file
  and repair every journal, snapshot ancestry and test reference.
- Inspect what the release actually applies. An unapproved migration must not accidentally enter an auto-apply
  lane; use the repository's approved staging mechanism and report schema work as pending until authorized.
- Backfills that preserve `updated_at` can strand rows behind `(updated_at, id)` consumers. Prove downstream
  cursor visibility, not just the repaired values. Choose legacy defaults that reflect real lifecycle state,
  rather than making every old row appear to be live work.

## Prisma and PlanetScale

- Inspect the pinned Prisma CLI help. Prisma 7 removed flags including `--skip-generate` and URL-based migrate
  diff inputs; usage output is not proof of a successful apply. Read the effective config/datasource before any
  mutation. `dotenv/config` does **not** override existing variables by default, but config and wrappers can.
- `db push` reconciles in both directions. Review the complete diff, including mappings and Vitess `_vt_`
  artifacts, rather than treating an artifact DROP as permission to delete it. Keep safe migrations enabled.
- Apply approved schema changes through a task database branch and deploy request where production forbids
  direct DDL. Opening a deploy request is not applying it. Preserve its branch through the provider's revert window.
- Never filter DDL by line regex or split arbitrary SQL on semicolons: literals, comments and triggers can defeat
  both. Use the pinned generator's supported execution path and inspect the exact statement set/count.
- Verify the physical target through approved connection metadata and the provider's branch mapping, not a
  friendly branch name or row count alone. Never print connection strings or credential values as evidence.
- With a serverless driver, `DATABASE()` can be empty. A catalog query using it may falsely report no tables.
  Use `SHOW COLUMNS FROM <table>` / `SHOW INDEX FROM <table>` in the verified session and read defaults back.
- Separate stale schema source, generated ORM client, running process and live catalog. Client-side
  `Unknown argument` validation happens before SQL; it does not justify new DDL.

## Cloudflare D1

- Use the pinned CLI's supported noninteractive migration path, normally
  `CI=true wrangler d1 migrations apply <database> --remote`. Do not add unsupported `-y`; verify the ledger
  after any apparent success. Select `migrations_dir`, config and environment explicitly where applicable.
- A populated database with an empty ledger needs schema/ledger reconciliation before apply. Do not replay
  historical CREATE statements or bulk-mark files applied without proving their exact effective schema.
- Atomicity depends on the API/CLI path. Inspect the pinned Wrangler implementation for `/query` versus
  `/import`, and fault-inject a later failure in the actual execution path. A comment saying "transactional"
  and a local SQLite script do not prove remote rollback or ledger atomicity.
- D1's expression-depth limit is lower than common local SQLite builds (100 versus 1000). Compile the real
  trigger/write path with `.limit expr_depth 100` and `EXPLAIN` against the migrated prior schema. Triggers may
  compile even when their WHEN arm is false; renames can recompile unrelated schema.
- Parent-table rebuilds need immediate foreign-key enforcement considered, not only deferred local tests.
  Copy parents before children, remove child references before parent drops, and verify every surviving trigger,
  index and foreign-key target after rename. Do not disable enforcement to make a test pass.
- Do not blindly retry `D1_RESET_DO`: it can represent deterministic timeout/resource exhaustion. Split a large
  migration only at a safe boundary that preserves fail-closed behavior between phases.
- D1 `batch()` rolls back on statement error; a conditional UPDATE affecting zero rows is **not** an error.
  If a later statement must not execute after a lost CAS, abort inside the same batch using a proven constraint
  failure or supported transactional primitive. Check returned changes and test rollback of earlier writes.
  `RAISE()` belongs in triggers, not arbitrary standalone SQL.

## SQLite and authorization semantics

- `json_extract(...) <> 'X'` becomes NULL for a missing path, so a trigger predicate can silently permit it.
  Prove presence/type and positive shape. With `json_each`, use its `type` column; `json_type(value)` on a text
  element can parse that text as malformed JSON.
- Date functions can normalize out-of-range components. Validate explicit bounds in addition to round-trips.
- TEXT may hold NUL plus hidden trailing bytes. Check BLOB byte length and reject NUL before recursive string
  processing. Bound any integer crossing into JavaScript to its safe integer range or serialize it losslessly.
- SQLite `RAISE(ABORT)` rolls back its statement, not all earlier statements in an arbitrary script. A caller's
  `NEW.timestamp` is not trusted wall time for authority windows. Choose database-owned time where required.
- A trigger recreation can drop an earlier guard arm. Compare effective `sqlite_master` bodies after migrating
  both base and candidate, not only the newest migration file.
- PostgreSQL `SECURITY DEFINER` changes the execution identity; RLS behavior depends on ownership, BYPASSRLS and
  FORCE RLS. Prove the complete caller authorization predicate and compare with the latest effective policies.
- Bulk terminalization must exclude unresolved external operations, including unknown/null states. Prove the
  migration's actual WHERE predicate on adversarial fixtures and authorized read-only target counts before apply.

Report severity, source of evidence (live catalog, ledger, runtime or repository), mixed-version behavior and
any unapplied/unauthorized phase. This review never grants schema mutation permission.
