# Coding Rules

## Critical Rules (Always Check)

- [ ] Use `const` for constants with `ALL_CAPS` naming and `let` for everything else
- [ ] Use `cn()` utility for dynamic classes, never template strings
- [ ] Use function declarations `function foo()` not arrow expressions
- [ ] Named exports only, no default exports (except for must-use cases like Route components)
- [ ] No `useMemo` or `useCallback` (React 19 compiler handles it)

## File Organization

- Co-locate related files (component, styles, types, utils)
- No barrel exports (index.ts re-export files)
- Use kebab-case for filenames: `product-card.tsx`

## Naming

- Components: PascalCase (`ProductCard`)
- Files: kebab-case (`product-card.tsx`)
- Functions: camelCase (`getProduct`)
- Constants: UPPER_SNAKE_CASE (`REVIEWS_PER_PAGE`)
- Types: PascalCase (`Product`, `Cart`)

## Styling

- Use Tailwind CSS
- Use `cn()` from `lib/cn` for conditional classes (No string templates)
- Use `cva` for building component class variants, not objects or arrays
