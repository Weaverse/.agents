---
name: release-verification
description: "Verify what Cloudflare Workers, Shopify Oxygen and Fly.io actually serve, including cron, queue and release-tag state. Use when shipping to those platforms or checking whether a feature is live; not for preparing version bumps."
allowed-tools: Read, Grep, Glob, Bash
---

# Release verification

## Before cutover

- A pipeline without a schema step can deploy code against missing columns while CI stays green. Verify the
  target catalog, not a developer database or generated ORM client. `database-migration-review` owns schema proof.
- Compare the candidate with each target's serving source, not just its branch. Manual promotions can contain
  fixes absent from the branch; a seemingly additive release can roll them back.
- Read the candidate workflow's trigger and conditions for the actual event/ref. A merge is a separate trigger;
  changing path filters can itself deploy. Do not assume the previous workflow or a feature-branch exclusion wins.
- Check environment configuration by presence and approved digests, never by dumping secret values. A green
  health route may not exercise a newly configured provider.
- Keep version and changelog in the implementation change before final review/CI. `ship` prepares a draft;
  neither a draft nor a development-branch merge is production evidence.

## Serving identity

- Bind producer evidence to consumer readback: intended SHA/version, running platform version or image digest,
  and a response from the affected route. Match the runtime's version field, not any old changelog text in HTML.
- Workers can serve multiple versions. Order deployment entries by parsed `created_on`, inspect the active
  traffic allocation and all referenced versions, and compare their provenance with the reviewed candidate.
  An upload ID, message containing a SHA, or row zero from a list is not alone proof of serving identity.
- For Fly.io, inspect every active serving Machine, its image digest and SHA. A stopped Machine is not serving.
  Read environment values only through an approved, non-secret projection. Machine config updates may merge env
  rather than remove absent keys; verify removal explicitly without exposing values.
- A container `COPY . .` after generation can overwrite the generated client with local output. Compare
  `.dockerignore` and generation order, then inspect the running artifact. A host build or `--no-cache` is not proof.
- Peel a remote release tag to its commit and compare with the reviewed/deployed SHA. `target_commitish` may be
  a moving branch; an annotated tag-object ID is not a commit ID. Do not repair a mismatch by silently moving tags.
- WAF or bot-policy refusals can occur before application execution. Report the blocked probe, not an app outage,
  and do not spoof identity or bypass the policy to complete verification.

## Cloudflare schedules and queues

- Version upload/deploy does not configure cron schedules. Read the live schedules and intended environment
  separately. A normal deploy can synchronize configuration too; inspect its effects instead of assuming it is
  code-only.
- Prove scheduled work in stages: trigger, execution, durable effects, report delivery. A completion marker with
  zero affected rows is a successful empty run. Empty logs need a known control request and retention window.
- Analytics can lag; distinguish late data from absent execution. Use a bounded read-only follow-up, not another
  invocation of a side-effecting job. A self-restarting job needs outcome verification from outside its runner.
- Healthy HTTP plus a green deploy does not prove queue delivery. Read the queue API's `delivery_paused` and
  consumer configuration; list-table output and a queue existing are insufficient.
- Idempotent cutover automation must tolerate successful DELETE responses with empty bodies. After any partial
  failure, re-list and reconcile only missing operations. A timed-out write can still apply; read before retrying.

## Hydrogen on Oxygen

- Keep framework build/codegen, Vite plugins, route preset, worker entry and the supported deploy path intact
  during toolchain changes. Use version-matched Hydrogen instructions instead of reconstructing the workflow.
- Oxygen deployments are immutable: environment changes require redeployment. Keep routability verification on;
  a branch named dev is not automatically an isolated preview environment.
- Probe a locale route, product/collection, CMS content, assets, redirects, robots/sitemap and logs alongside the
  homepage. Cart-to-checkout and account initiation need authorized test scope; never place a purchase as a probe.
- A resolved submit or HTTP 200 can still carry `errors` or `userErrors`. Assert the intended cart mutation.
  Correct Storefront query context does not ensure a fresh cart's `buyerIdentity.countryCode`; SDK mutations can
  create carts implicitly. An unprefixed API request from a locale page can select the default market.
- Public locale, translation bundle, CMS locale and provider market are distinct. Verify currency provenance;
  never relabel an external amount with the route currency. Prefer same-response SSR/hydration consistency over
  literals that a content edit can invalidate.
- For deploy-memory problems, inspect the pinned CLI's resolved sourcemap options. A Vite setting that the
  deploy command overrides is a placebo; measure the production command before changing heap limits.

## Readback after a failed wrapper

- A watcher timeout does not fail the remote run. Save its exit before logging and re-read that same run ID in
  the correct repository. A trailing `echo` must not convert failure to success.
- With `pipefail`, `head`/SIGPIPE or a no-match grep can fail a wrapper **after** a successful mutation. Separate
  mutation and readback, and settle remote state before retrying. Quote workflow input arguments.
- An always-run artifact upload can turn a successful cutover red when an expected file is missing. Check live
  state before rollback. Exclude environment snapshots and provider bodies from uploaded evidence.

Report serving SHA/version, tag identity, verified feature probes, schedule/queue state and unproven paths.
"No new failures" on an already-red baseline is not "all gates passed".
