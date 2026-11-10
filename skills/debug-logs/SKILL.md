---
name: debug-logs
description: "Collect a bounded browser-only reproduction timeline in window.__debug_logs instead of console output. Use when temporary client-side instrumentation is needed; use production-debugging for server, edge or database failures."
allowed-tools: Read, Grep, Glob, Bash
---

# Browser debug timeline

Use the team's temporary `window.__debug_logs` technique when console output is noisy or a reproduction must
be handed back as JSON. Browser access still follows the current task's permission rules.

## Instrument

1. Choose only the decision points that distinguish the competing explanations. Use code-owned stage names,
   counts, booleans and bounded status categories. No customer data, identifiers, tokens, full URLs, form values,
   raw errors, props or response bodies belong in `window.__debug_logs`.
2. Wrap every added helper, call and type declaration in `DEBUG START` / `DEBUG END` markers.
   Keep initialization out of the render path so a re-render does not erase the capture.
3. Adapt this bounded example to the repository's style; do not spread arbitrary objects into an entry:

   ```typescript
   // DEBUG START
   type DebugStage = 'load' | 'submit' | 'result';
   interface DebugEntry {
     timestamp: number;
     stage: DebugStage;
     count: number;
     ok: boolean;
   }
   declare global {
     interface Window { __debug_logs?: DebugEntry[]; }
   }
   function debugLog(stage: DebugStage, count: number, ok: boolean) {
     if (typeof window === 'undefined') return;
     window.__debug_logs ??= [];
     if (window.__debug_logs.length >= 1000) window.__debug_logs.shift();
     window.__debug_logs.push({timestamp: Date.now(), stage, count, ok});
   }
   // DEBUG END
   ```

## Capture and remove

- Before a fresh reproduction, clear the array explicitly once. Do not clear it on every mount or render.
- Verify `.debug/` at the project root is Git-ignored **before** writing a capture. Do not put logs in a spec.
- In an approved browser session, reproduce and export with
  `copy(JSON.stringify(window.__debug_logs ?? [], null, 2))`; this DevTools helper is browser-specific.
  Save a reviewed capture as `.debug/logs-1.json` (choose the next unused index).
- Read the timeline against the actual code. Missing stages prove absence only if the capture window,
  initialization and capacity limit cover them. Distinguish a bounded buffer eviction from a missing event.
- Remove all marked instrumentation and global declarations after the investigation. Search for both markers
  and `__debug_logs`, then run the relevant tests/build. Do not ship a dormant payload collector.

Report the captured stages, last proven boundary, resulting fix and cleanup status. If the failure is outside
the browser, switch to `production-debugging` rather than extending this array into a retained logging system.
