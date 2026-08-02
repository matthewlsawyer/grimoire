---
name: grim-notes
description: >-
  Capture and organize daily notes into a monthly ledger under notes/.
  Use when the user invokes grim-notes or wants to append classified notes,
  todos, or resources into a workspace notes directory.
---

# Notes

Capture and organize daily notes into a monthly ledger under `notes/`.

## Workflow

1. Resolve `target` to an absolute workspace root. Use cwd or named path. Empty means the current workspace root.
2. Choose mode from the invocation:
  - **Bare** (`/grim-notes` with no context): **Status**. See [Status](#status).
  - **Context** (blurb, links, snippets, or mixed): **Capture**. See [Capture](#capture).
3. **Emit report**. See [Output](#output).

## Capture

1. Classify the context into atomic items. See [Classify](#classify).
2. Resolve today as `YYYY-MM-DD` and the month file as `{target}/notes/YYYY-MM.md`.
3. Create `notes/` and the month file if missing.
4. Append into the month file using template [note.md](./templates/note.md):
  - If `## YYYY-MM-DD` exists, append under the matching sub-section only; create missing sections under that day when needed.
  - If the day is new, append a full day block at end of file (only sections that receive items this run).
  - Never edit, reorder, or rewrite prior days or prior bullets.

## Classify

Split the context into atomic items, then assign:

| Bucket | Heuristic |
| --- | --- |
| Resources | URLs / bare links; fenced or clearly pasted code snippets |
| Todos | Action / obligation language ("I need to", "TODO", "figure out", "remind me to", imperative task lines) |
| Notes | Everything else (freeform prose, observations) |

One context may yield multiple buckets. Do not reclassify or rewrite existing ledger content.

## Status

1. List `{target}/notes/*.md` month files descending (newest `YYYY-MM.md` first).
2. For each file, count Notes bullets, Todos items, and Resources items across all day sections.
3. If `notes/` is missing or empty, emit the trunk with a single annotation that nothing is captured yet. Do not invent month nodes.

## Output

1. Capture: write or append the ledger, then emit the session viewport using template [delta.md](./templates/delta.md). Do not write the viewport to disk.
2. Status: emit the session viewport using template [status.md](./templates/status.md). Do not write to disk.

## Usage

```text
/grim-notes
/grim-notes I need to figure out the install path. Also https://example.com
/grim-notes /path/to/workspace
```
