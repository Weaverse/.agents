---
name: debug
description: "Instrument web/web-app code with structured debug logging via a global variable (window.__debug_logs). Produces a clean JSON timeline for reproducing and diagnosing bugs. Use when user wants to debug a feature or track down a bug."
argument-hint: "feature, bug description, or file/component to debug"
metadata:
  tools: [Read, Grep, Glob, Write, Edit, Bash, AskUserQuestion]
---

Debug a web/web-app issue by instrumenting code with structured logging via `window.__debug_logs`. This skill does NOT use `console.log` — all debug data is collected in a single global array for clean export and analysis.

## How It Works

1. A global array `window.__debug_logs` collects structured log entries
2. Debug statements are inserted at key points in the code flow
3. The dev reproduces the bug, then copies `window.__debug_logs` to a JSON file
4. An agent reads that JSON to diagnose and fix the issue

---

## Phase 1: Understand the Bug

Analyze $ARGUMENTS and the relevant code to understand:
- What feature/component is affected?
- What is the expected vs actual behavior?
- What data flows through the affected code path?

Use `AskUserQuestion` if the bug description is unclear or if you need to narrow down the scope.

---

## Phase 2: Identify Key Instrumentation Points

Explore the codebase and identify **every critical point** in the code path where data changes or decisions are made. Typical points include:

- **Initial load / mount**: component mount, initial data fetch
- **Data arrival**: API responses, store hydration, prop changes
- **User interactions**: clicks, form changes, selections
- **State transitions**: state updates, effect triggers, re-renders
- **Derived computations**: filtered lists, computed values, transformations
- **Error boundaries**: catch blocks, error states, fallbacks

Map out these points before writing any code.

---

## Phase 3: Instrument the Code

### 3.1 — Initialize the global logger

Add this initialization at the **app entry point** or at the top of the **root component/page** being debugged (whichever is more appropriate):

```typescript
// --- DEBUG START ---
if (typeof window !== 'undefined') {
  window.__debug_logs = []
}
// --- DEBUG END ---
```

### 3.2 — Add a helper (optional, for convenience)

If there are many log points, add a small helper near the initialization:

```typescript
// --- DEBUG START ---
function __debugLog(key: string, data: Record<string, unknown>) {
  if (typeof window !== 'undefined' && window.__debug_logs) {
    window.__debug_logs.push({
      timestamp: Date.now(),
      key,
      ...data,
    })
  }
}
// --- DEBUG END ---
```

### 3.3 — Insert log points

At each instrumentation point, push a structured entry:

```typescript
// --- DEBUG START ---
__debugLog('initial_data', {
  data: { id: product.id, status: product.status, price: product.price },
})
// --- DEBUG END ---
```

### Log Entry Format

Every entry MUST have these fields:

| Field       | Type     | Description                                                                 |
|-------------|----------|-----------------------------------------------------------------------------|
| `timestamp` | `number` | `Date.now()` — milliseconds since epoch                                    |
| `key`       | `string` | Descriptive snake_case ID for this point (see naming conventions below)     |

Additional fields are added as needed per log point (e.g., `data`, `props`, `state`, `error`, `response`).

### Key Naming Conventions

Use descriptive, snake_case keys that tell a story when read in sequence:

```
first_load
initial_props
fetch_start
fetch_response
state_after_fetch
on_filter_change
filtered_results
on_item_click
selected_item_data
on_submit
submit_response
error_caught
```

### Data Pruning Rules

**CRITICAL**: Only log what's relevant to the bug. For each log point:

- ✅ Log IDs, statuses, counts, flags, selected values
- ✅ Log the specific fields that might be wrong
- ✅ Log array lengths instead of full arrays (unless the array content matters)
- ✅ Log error messages and codes
- ❌ Do NOT log entire API responses — pick the relevant fields
- ❌ Do NOT log full component props — pick what matters
- ❌ Do NOT log DOM elements or React internals
- ❌ Do NOT log large objects (images, blobs, full user profiles)

Example — instead of logging an entire product list:
```typescript
// ❌ Bad: logs everything
__debugLog('products_loaded', { data: products })

// ✅ Good: logs what matters
__debugLog('products_loaded', {
  data: {
    count: products.length,
    firstId: products[0]?.id,
    lastId: products[products.length - 1]?.id,
    statuses: [...new Set(products.map(p => p.status))],
  },
})
```

### Wrapping Convention

ALL debug code MUST be wrapped in clearly marked comments for easy removal:

```typescript
// --- DEBUG START ---
__debugLog('some_key', { data: relevantData })
// --- DEBUG END ---
```

This makes cleanup trivial — search for `DEBUG START` and remove all blocks.

---

## Phase 4: Prepare the Debug Output File

### 4.1 — Find or create the output location

Check if there is a spec folder for the feature being debugged:
- Look for a matching folder in the specs directory (check project config or default `.specs/`)
- If a spec folder exists → create a `.debug/` subfolder inside it
- If no spec folder exists → create `.debug/` in the project root

### 4.2 — Create the empty log file

Determine the next available index:
```
.debug/logs-1.json
.debug/logs-2.json
.debug/logs-3.json
...
```

Create the file with a placeholder:

```json
[]
```

### 4.3 — Tell the dev what to do

After instrumenting, output clear instructions:

```
Debug instrumentation is ready.

To capture logs:
1. Reproduce the bug in your browser
2. Open DevTools console and run: copy(JSON.stringify(window.__debug_logs, null, 2))
3. Paste into: <path-to-debug-file>
4. Then ask me to analyze the logs and fix the bug

To clean up after debugging:
- Search for "DEBUG START" and remove all blocks between DEBUG START/END markers
```

---

## Phase 5: Analyze Logs (when the dev comes back with filled logs)

If the user provides a populated debug JSON file or asks to analyze:

1. Read the JSON file
2. Build a timeline of events from the `timestamp` and `key` fields
3. Identify anomalies:
   - Unexpected data values
   - Missing expected log entries (gaps in the flow)
   - Wrong ordering of events
   - State inconsistencies between steps
4. Correlate findings with the code
5. Propose a fix

---

## Important Rules

- **NO `console.log`** — all logging goes through `window.__debug_logs` only
- **Prune aggressively** — each log entry should be small and focused
- **Mark all debug code** with `// --- DEBUG START ---` and `// --- DEBUG END ---`
- **TypeScript**: If the project uses TypeScript, add the global type declaration:
  ```typescript
  // --- DEBUG START ---
  declare global {
    interface Window {
      __debug_logs: Array<Record<string, unknown>>
    }
  }
  // --- DEBUG END ---
  ```
- **Don't break the app** — debug instrumentation must not change any behavior
- **Framework-aware**: Use appropriate patterns for the framework (e.g., `useEffect` for React, `onMounted` for Vue, etc.)
