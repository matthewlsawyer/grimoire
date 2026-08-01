---
name: grim-forge
description: >-
  Produce and maintain a historical ledger that captures the history of your project.
  Use when the user invokes grim-forge or wants to create a historical ledger.
---

# Forge

Produce and maintain a historical ledger that captures the history of your project.

## Workflow

1. Resolve `target` to an absolute workspace root. Use cwd or named path. Empty means the current workspace root.
2. **Distill history**. See [Distill](#distill) section below.
3. **Emit artifacts and report**. See [Output](#output) section below.

## Distill

1. Always read `HISTORY.md`, CHANGELOG, and root README when present.
  - Read other documentation (ADRs, AGENTS.md, design docs) when the commit range shows they changed or when the story needs corroboration.
  - Optionally use `git log --name-status` to find candidates.
  - Optionally use `find` or directory listing when git history is thin and genesis needs a shallow doc pass.
2. Resolve `history_commit` via `git -C {target} log -1 --format=%h -- HISTORY.md`.
3. Hunt git logs for story (`history_commit..HEAD` or full log). Walk git log (`--no-merges`, subjects + bodies, `--name-status`) when needed:
  - Notice themes, turning points, refactors, releases.
  - Treat ADR/doc touches as high salience.
  - Skip noise (`chore(deps)`, etc.).

## Output

1. Write or append to `{target}/HISTORY.md` using template [history.md](./templates/history.md).
2. Emit a report to the session window using template [report.md](./templates/report.md). Do not write to disk.
