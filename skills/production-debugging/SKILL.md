---
name: production-debugging
description: "Discriminate opaque server, edge and database failures on Workers, D1, Prisma, Shopify and React Router without retaining customer data. Use when logs are empty, catches hide causes, instrumentation is needed or a production fix may be unreachable."
allowed-tools: Read, Grep, Glob, Bash
---

# Opaque production failures

## Find the last proven boundary

- Empty logs prove nothing until a known request appears under the same sampling, status filter and retention.
  Workers runtime outcome `ok` can include a caught HTTP 500. An error-only tail can miss it entirely.
- When external state cannot distinguish the failure branches, ship a narrow diagnostic change through the
  normal review/release gates rather than a guessed behavioral fix. Do not make logging a reason to bypass review.
- Compare the reported status with each catch's return value. A branch returning 503 cannot explain an observed
  500. Use durable writes/artifacts as checkpoints only after excluding other writers and partial transactions.
- On Workers, `Date.now()` does not advance during pure CPU execution. Compare runtime limits and I/O boundaries
  rather than trusting an in-process stopwatch as independent wall time.
- A 401 is not permission to switch to a database. Use only an already-authorized read-only datastore path;
  report an access blocker otherwise. Do not invent diagnostic endpoints or guess private routes.

## Datastore and projection evidence

- Run the real query and binds, not a reconstruction. A returned row proves that query can read it, not that the
  request used the same authorization, projection or response path. Count `.bind()` parameters positionally.
- Inspect effective triggers/views when an error is flattened to 404. On SQLite, read `sqlite_master` bodies;
  compare against a locally migrated schema before blaming production drift. Separate trigger aborts from
  constraints using runtime-produced errors, not hand-written strings that a test invented.
- `prisma db execute` is not a row-returning query client. Use the application's actual driver adapter for
  authorized reads. ORM `Unknown field` can mean a stale generated client, not missing production DDL.
- Check D1 database identifiers versus binding aliases and the selected config environment. For a missing UI
  failure reason, compare the projection's source tables with those the failure writer updates.
- Sweep **all** authority layers: application SQL copies, views, triggers and release gates. Fixing one copy of
  a mirrored predicate can merely move the refusal downstream. Add joins one at a time to localize the rejected arm.
- A null provider request ID does not prove no provider call or charge occurred; submission can precede ID
  persistence. Keep the operation unresolved until provider/durable evidence settles it.

## Platform traps

- Re-read opaque references after a mutation that can replace them. First-N-success followed by identical
  failures can mean the loop is using stale references, not a provider outage.
- A scheduler can overwrite manual row edits. Check periodic writers and lease state before recovery; a retry
  counter stuck below its cap can mean delivery stopped rather than retries being exhausted.
- React Router data requests can use `/route.data`; a gateway matching only `/route` can render the page yet
  reject navigation or action requests. Test both forms with the correct methods. If normalizing a `.data`
  suffix, keep authorization/method gates on the canonical route and do not widen a generic allowlist.
- A root network probe does not exercise a workload UID's egress policy. Probe under the actual restricted
  identity in an authorized test environment, including any runtime loopback/HMR dependencies.
- For authenticated webhooks, acknowledge only after durable admission. `waitUntil` alone is not a durable queue
  and cannot guarantee work survives termination. Persist an idempotent receipt before reporting acceptance.

## Diagnostics without leaks

- Retention makes existing reachable `console.*` calls durable, not just the new diagnostic. Audit the production
  bundle and invocation metadata too; a query string can leak without an explicit application log call.
- Emit a closed vocabulary: fixed event/stage/category, bounded status and counts. Do not copy `Error.name`,
  message, cause, stack, schema issue paths, SQL/binds, request URLs, prompts or provider bodies into retained logs.
- Minification can erase source file/line identities. Set fixed checkpoints before significant awaits and emit
  the last checkpoint from a sanitized catch; do not log a fake source frame that only exists in tests.
- A pathname can contain customer identifiers too. Map routes to code-owned route IDs/templates; removing only
  query parameters is not a privacy boundary. Check sibling throw sites and error-tracker grouping keys.
- Test every console argument recursively with nested sentinel values in error names/messages and payloads.
  Assert an exact key/category allowlist; removing a payload dump means deleting its carrier, not partial redaction.
- Remote analytics config can enable console capture without a deploy. Compliance webhooks can be logged before
  dispatch. Audit shared middleware, SDK settings and event metadata as well as handlers.
- Limit a production tail to the authorized probe, filter locally to categories/counts and close it promptly.
  A filter is not redaction: raw captured logs remain sensitive. A fix stops new leaks; it does not undo old ones.

## Prove the path and the regression

- Preserve structural payload shape while sanitizing fixtures. A hand-made version/state combination may enter a
  branch that production cannot reach. Assert the actual output artifact, not just a helper return value.
- Shopify Admin GraphQL can throw an SDK error as well as returning transport/GraphQL errors or mutation
  `userErrors`. Verify the pinned SDK's real shape; HTTP success alone does not prove a mutation succeeded.
- A newly reachable branch inherits the authorization, budget, retry and recovery guarantees previously supplied
  by the path it bypasses. Trace the real caller before relaxing a refusal.
- Revert only the source fix in a disposable copy. Require a named assertion failure, not an import/build error,
  then restore exact bytes and green. A surviving mutation is a coverage hole, invalid mutation or unreachable
  scenario to investigate, not automatic proof that a guard is dead.
- After release, read the retry/fallback's own durable evidence before saying it ran. Inspect sibling catch,
  finally, cancellation, reset and non-2xx branches for the same defect.

Report last proven boundary, discriminating evidence, fix reachability, privacy proof and remaining assumptions.
