---
description: Explain recent code changes in simple terms a junior dev can understand
argument-hint: "[optional focus area or question about the changes]"
---

# Explain

Explain the code changes that were just applied in this conversation. Break it down so a junior developer can fully understand what happened, why, and how it works.

## Workflow

### Step 1: Gather context

Look back through the conversation history and identify all code changes that were just made. This includes:
- Files created, edited, or deleted
- Functions added or modified
- Dependencies or imports changed
- Config changes

If `$ARGUMENTS` is provided, focus the explanation on that specific area or answer that specific question about the changes.

### Step 2: Explain — What did you do?

List every change that was made, file by file. For each file:
- What was the file before (or that it's new)
- What changed and where
- Use short code snippets to highlight the key parts (not the full file)

Keep it scannable. Use bullet points and headers.

### Step 3: Explain — Why did you do it?

For each change (or group of related changes), explain:
- What problem it solves
- Why this approach was chosen over alternatives
- What would happen if this change was NOT made

Connect the dots between changes. If file A was changed because of file B, say so.

### Step 4: Explain — How does it work?

This is the deep dive. Explain the logic step by step:
- Walk through the code flow as if you are tracing execution
- Use numbered steps: "First this happens, then this, then this..."
- Use simple analogies where helpful (e.g., "Think of this like a to-do list where...")
- If the logic involves data flow, show it visually with ASCII diagrams:

```
  User clicks button
       |
       v
  handleClick() runs
       |
       v
  API call to /api/save
       |
       v
  Response updates state
       |
       v
  Component re-renders with new data
```

- If there are important patterns (hooks, context, middleware, etc.), explain what they are and why they are used here
- Define any technical terms the first time you use them

### Step 5: Key takeaways

Summarize with 3-5 bullet points:
- The most important thing to remember
- Any gotchas or edge cases to watch out for
- Related concepts worth learning more about

## Writing Rules

- Use simple English. Short sentences. No jargon without explanation.
- Write like you are explaining to a teammate on their first week.
- Prefer concrete examples over abstract descriptions.
- Use "you" and "we" to keep it conversational.
- Use code snippets, ASCII diagrams, and step-by-step flows wherever they help.
- Do NOT assume the reader knows framework-specific concepts — explain them briefly.

## Step 6: Ask about saving

After the explanation is complete, ask:

> "Want me to save this explanation to a markdown file for future reference? (default: no)"

- If the user says **no** or does not respond, do nothing. Stop here.
- If the user says **yes**, ask where they want to save it. Suggest a sensible default path based on the project structure (e.g., `docs/explanations/` or `.notes/`).
- Save the explanation as a clean markdown file with a descriptive filename based on the topic (e.g., `auth-flow-explanation.md`).

## User Arguments

$ARGUMENTS
