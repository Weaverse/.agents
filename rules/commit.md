# Commit Rules

## Commit Message Format

Use simple, descriptive sentences. NO conventional commits (feat:, fix:, etc.)

### Good
```
Add pagination to reviews section
Fix filtering bug for property stats
Update review card styles
```

### Bad
```
feat: add pagination to reviews
fix: resolve filtering issue
chore: update styles
```

## What to Commit

- ✅ Working features
- ✅ Bug fixes
- ✅ Refactoring
- ✅ Documentation updates

## What NOT to Commit

- ❌ Secrets or API keys
- ❌ `.env` files
- ❌ Build artifacts (`.next/`, `dist/`)
- ❌ Debug code or console.logs
- ❌ Large binary files

## Before Committing

Run these commands:
```bash
nr format    # Format with Biome
nr fix       # Fix linting issues
nr typecheck  # Check types with TypeScript
```

## Commit Messages Language

- Use English for technical changes
- Be specific: "Fix null pointer in cart" not "Fix bug"

## Examples

```
Implement pagination for reviews with 10 items per page
Add sub-rating filtering to property stats
Remove unused Dialog imports from review section
Refactor aspect keywords into shared utils
Update hero section background image
```
