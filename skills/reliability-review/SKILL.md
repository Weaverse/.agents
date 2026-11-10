---
name: reliability-review
description: "Find Workers, D1, Queues, R2 and MySQL/Prisma failures hidden by ordinary concurrency tests: request-context I/O, stale CAS reads, late provider writes and cache resurrection. Use when reviewing multi-writer, lease, retry or cache changes."
allowed-tools: Read, Grep, Glob, Bash
---

# Reliability at platform boundaries

## Workers and background execution

- Module-level single-flight promises can retain I/O owned by a different request context and fail only under
  overlapping requests. Test in the real runtime; use durable coordination or a cache strategy rather than
  sharing request-owned I/O promises across invocations.
- `ctx.waitUntil(f())` calls `f` immediately; it extends lifetime, not start time or durability. A refresh can
  queue ahead of the response's required read. Prove dispatch order at the contended resource, not just latency.
- Durable Objects are single-threaded but async work can interleave across awaits unless protected by the
  applicable input/storage gates. A shared object can still bottleneck unrelated readers. Inspect every caller
  and test overlap; do not infer either transaction isolation or total request serialization from the object type.
- D1 session bookmarks/read routing do not provide a multi-request transaction. For revisioned writes, prove the
  receipt, CAS and subsequent writes share an atomic authority boundary. A zero-change receipt INSERT does not
  abort a batch; fault-inject a lost claim and a later statement error separately.
- R2 download latency includes every body `read()`, not just `get()`. Bound the full stream. Confirm remote
  scope, bucket name, config and environment; a local default can report a missing object that exists remotely.
- In a Queues batch, fail-fast `Promise.all` can abandon sibling outcome handling. Isolate each message, await
  all settlements and explicitly ack/retry according to durable outcome. Cancellation is not automatic ACK;
  swallowed failures can make a successful handler implicitly acknowledge unfinished work.

## Authority and retries

- A conditional mutation's returned count is part of the fence. Exercise the caller branch where the claim or
  persist loses ownership; ignoring `count === 0` defeats even correct SQL.
- A preflight lock read does not guard a later mutation. Put tenant, liveness and ownership conditions in the
  same current-read locking statement, with deterministic lock order and identity-checked release.
- Under MySQL REPEATABLE READ, a later plain SELECT can use the snapshot established before a lock wait.
  Drive two genuinely overlapping transactions through the production driver; mocks cannot prove current reads.
  Inspect emitted ORM SQL before assuming `updateMany` is one native guarded UPDATE.
- Timeouts must fit inside the lease, but timeout/heartbeat alone cannot fence an external write. A cancelled
  request can commit later. Prefer destination-enforced fencing or provider idempotency plus durable adoption;
  reconcile unknown outcomes before another submission.
- Claims before a provider call prevent overlapping cron ticks only while authority holds. Release with an
  ownership CAS; ensure recovery covers expired claims and calls that outlive the claimant.
- A polling budget shorter than measured provider processing time guarantees repeated failures, possibly with
  repeated charges. Measure acquisition-to-result time, distinguish submit/status endpoints, and fix the budget
  before raising retries. Re-delivery must adopt the same external operation rather than resubmit it.
- Match queue retry lifetime with orphan detection and reconciliation. A task can dead-letter before a sweeper's
  threshold. Terminalization must not hide unresolved paid operations; fail closed on unknown ledger states.
- A connection failure after a write is not a confirmed abort. Read durable state before retrying counters or
  metering. Bound transaction fan-out; `allSettled` waits for outcomes but does not limit concurrency.
- Promise chains such as `queue.then(op)` are not reentrant: a nested acquisition can wait on itself. A cleared
  timer does not cancel an already-running callback; use an epoch/identity check at each mutation boundary.

## Cache identity and invalidation

- Audit every writer by table/field, including jobs, when introducing a cache. Include tenant, locale/market,
  preview/live mode and revision in representation identity. A `forceFresh` read can still join stale pending work.
- Deleting a key does not cancel an in-flight refresh, which can repopulate old data. Fence refresh writes with
  revision/epoch authority and test invalidation during the refresh, not only before it starts.
- Stale-while-revalidate extends the stale window beyond the fresh TTL. Verify maximum stale age and behavior
  when refresh fails, not only the happy HIT path.
- Keep authenticated responses out of shared edge caches unless an explicit, reviewed isolation contract proves
  otherwise. Cloudflare cache eligibility, custom keys, Cache Rules and origin headers all matter; `DYNAMIC`
  is not a hit and missing Cache-Control alone does not prove a CDN invented a TTL.
- Prove cache HIT/age alongside cross-identity isolation and invalidation. An always-miss `caches` stub after
  a Workers-to-Node port can compile and silently multiply origin load.
- MySQL relation-OR-ID queries can full-scan. Inspect real plans before splitting aggregates, preserving duplicate
  semantics. Process-local usage buffers multiply hot-row writes across Machines; batch writes without dropping
  metering, and treat metering kill switches as data-loss decisions.

Report the adversarial interleavings exercised, runtime/driver used, unresolved external outcomes and remaining
cache/tenant boundaries. Live infrastructure and data changes retain their separate authorization gates.
