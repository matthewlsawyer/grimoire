# Note Template

Monthly append-only ledger under `{target}/notes/YYYY-MM.md`.

## Structure

```markdown
## YYYY-MM-DD

### Notes
- {freeform note}

### Todos
- [ ] {todo}

### Resources
- {url or snippet}
```

## Rules

- **One file per month** (`YYYY-MM.md`). Create the file with a `# YYYY-MM` title when missing.
- **Day headings** are `## YYYY-MM-DD`. Append a new day block at end of file when the day is new.
- **Sections** under a day: `### Notes`, `### Todos`, `### Resources`.
  - Skip empty sections on first write for a day (only create sections that receive items this run).
  - When appending into an existing day that lacks a needed section, add that section then append.
- **Notes** are plain bullets (`- ...`).
- **Todos** are checkbox bullets (`- [ ] ...`).
- **Resources** are bullets for links, or fenced code blocks when the item is a snippet.
- **Append-only**. Never edit, reorder, or rewrite prior days or prior bullets.
