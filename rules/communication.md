# Agent Communication Rules

## Question vs Statement Handling

### Questions (Contain `?`)
When the user asks a question:
- **DON'T** modify code
- Provide recommendations, solutions, or coding proposals
- Ask for confirmation before proceeding
- Example: "Should we add X?" → "Yes, we could do X by... Should I implement this?"

### Statements (Instructions)
When the user gives a statement or command:
- **DO** implement the changes directly
- Follow existing code patterns
- Ask only if clarification is needed
- Example: "Add a toggle button" → [implement directly]

### Examples

| User Input | Action |
|------------|--------|
| "Should we use X?" | Answer with proposal, don't code |
| "Can we add Y?" | Explain approach, ask to proceed |
| "Add X to the component" | Implement directly |
| "Make it blue" | Change the code |
| "How can we deal with this?" | Provide recommendations, wait for go-ahead |
| "Fix the bug" | Fix it directly |

## Why This Matters

- Questions often seek exploration and discussion before commitment
- Statements indicate clear intent to act
- Respecting this distinction prevents unwanted changes
- Ensures you stay in control of when code gets modified

## Reminder

**When in doubt:**
- If it ends with `?` → Answer, don't code
- If it's a command → Code it
- If ambiguous → Ask for clarification
