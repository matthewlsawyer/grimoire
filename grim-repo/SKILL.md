---
name: grim-repo
description: >-
  Given a workspace or directory, reveal nested git repositories and their
  current status. Use when the user invokes grim-repo or needs a nested-repo
  census board.
---

# Grim Repo

_What lives must be named._

Inject a live nested-repo status board into the session: every git root under the target, with branch and working-tree deltas. The census is a fact surface -> dirty trees, branches, which nested root is which. Use it in session to choose where to work and what is out of sync.

## Inputs

| Input | Required | Holds |
| --- | --- | --- |
| `target` | yes | Absolute workspace root to search under. Default cwd when invoked without a path. Ask if unclear. |

## Workflow

1. Resolve `target` to an absolute directory.
2. **Census** - run Script (see Script below).
3. Emit Output: fence **full script stdout** as the board. Do not redraw. Re-run Script per Script policy if the census is stale or wrong for the ask.
4. Do not write the board to disk.

## Script

From the skill root directory, run:

```bash
python3 <skill-root>/scripts/census.py --target <absolute_workspace_root>
```

- Always pass an absolute workspace to `--target`. Never use `--target .`
- Stdout is the complete census board (Unicode tree). Fence it as-is.

### Script policy

- Script stdout is the complete census board; fence as-is. Do not redraw or reinterpret metrics into a second viewport.
- **Prefer** `scripts/census.py` for the board (do not skip the script and freestyle git status across the tree).
- **Re-run** when the target changes, the board looks incomplete, or the ask needs a fresh census. Briefly note what changed vs the prior run.
- **Read-only** - do not edit script files in-session; read the script only to understand behavior.
- Supplement is rarely needed; re-run on the correct absolute `target` first.

## Census

The script discovers every git repository root under `target`:

- Treat `.git` as directory or gitfile (worktree/submodule layouts).
- Sort roots shallow-first; dedupe by realpath of repo root.
- Display path: `./` for the target root repo, else `relpath/` under target.

Per repo:

| Token | Glyph | Meaning |
| --- | --- | --- |
| sync | `▲` | `↑ahead ↓behind` vs `@{upstream}`; or `no-remote` / `no-up` |
| diff | `▲` | `+added -deleted` vs `HEAD`, including untracked non-binary line counts |
| branch | `●` | Current branch, or `DETACHED@<shortsha>` |

If a repo fails, note in chat and omit or partial that row; do not invent metrics.

## Output

| Part | Required | Holds |
| --- | --- | --- |
| Title | yes | `# Grim Repo: <project>` outside the fence |
| Board | yes | `text` fence: full census stdout |

### Board layout

The script draws:

- Header: `<basename(target)>/`, then divider `╞══════════════════◆`, then spacer line `│`.
- One subtree per repo (shallow-first):

```text
├─ <repo_display>/
│  ├─▲ <sync>
│  ├─▲ <diff>
│  └─● <branch>
```

Glyphs:

- `│` `├` `└` `─` hierarchy
- `╞` `═` divider
- `◆` terminator
- `▲` status / delta
- `●` branch or snapshot

## Usage

```text
/grim-repo
/grim-repo /path/to/workspace
```

## Boundaries

- Read-only git inspection; do not modify repos.
- Session-only viewport.
