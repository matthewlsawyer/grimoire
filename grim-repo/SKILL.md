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
2. **Census** - discover git roots and collect status per root (see Census below).
3. **Draw** the status board in-session per Output (agent composes the tree; no script stdout).
4. Emit Output. Do not write the board to disk.

## Census

Discover every git repository root under `target`:

- Treat `.git` as directory or gitfile (worktree/submodule layouts).
- Sort roots shallow-first; dedupe by realpath of repo root.
- Display path: `./` for the target root repo, else `relpath/` under target.

Per repo, collect:

| Token | Glyph | Meaning |
| --- | --- | --- |
| sync | `▲` | `↑ahead ↓behind` vs `@{upstream}`; or `no-remote` / `no-up` |
| diff | `▲` | `+added -deleted` vs `HEAD`, including untracked non-binary line counts |
| branch | `●` | Current branch, or `DETACHED@<shortsha>` |

Use `git` in the repo root with C locale when parsing output. If a repo fails, note in chat and omit or partial that row; do not invent metrics.

## Output

| Part | Required | Holds |
| --- | --- | --- |
| Title | yes | `# Grim Repo: <project>` outside the fence |
| Board | yes | `text` fence: full census tree |

### Board layout

Header: `<basename(target)>/`, then divider `╞══════════════════◆`, then spacer line `│`.

For each repo (shallow-first), one subtree:

```text
├─ <repo_display>/
│  ├─▲ <sync>
│  ├─▲ <diff>
│  └─● <branch>
```

Use `└─` for the last repo at the forest level; `│` between sibling repos. Indent continuation with `│  ` or three spaces on the last repo per drawing guide below.

Drawing guide:

```text
throneroom/
╞══════════════════◆
│
├─ ./
│  ├─▲ ↑0 ↓0
│  ├─▲ +0 -0
│  └─● main
│
├─ projects/dotfiles/
│  ├─▲ ↑1 ↓0
│  ├─▲ +8 -8
│  └─● main
│
└─ projects/site/
   ├─▲ ↑0 ↓2
   ├─▲ +82 -2
   └─● main
```

Glyphs: see [grimoire Glyph Dictionary](../README.md#glyph-dictionary).

## Usage

```text
/grim-repo
/grim-repo /path/to/workspace
```

## Boundaries

- Read-only git inspection; do not modify repos.
- Session-only viewport.
