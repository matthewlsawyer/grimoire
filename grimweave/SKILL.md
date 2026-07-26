---
name: grimweave
description: >-
  Follow a file, symbol, or concept through a workspace and emit a ledger of
  definitions, relationships, provenance, and threads. Use when tracing
  provenance, dependencies, or documentation for a token in a codebase.
---

# Grim Weave

_Follow the thread._

Follow a single token through a workspace: bounded evidence, then an at-a-glance **Weave Ledger** in chat. Collection stays within caps; relationships and threads are agent-composed from evidence and reads. Do not write the ledger to disk.

## Inputs

| Input | Required | Holds |
| --- | --- | --- |
| `target` | yes | Absolute workspace root. Ask if unclear. |
| `user token` | yes | File path, symbol, or concept phrase. |

| Token shape | `token_kind` |
| --- | --- |
| `path/to/file.go`, `SKILL.md` | `file` |
| `TodoService` (identifier) | `symbol` |
| `log in`, multi-word phrase | `concept` |

## Workflow

1. Resolve `target` and **user token**. Ask if either is unclear.
2. **Disambiguate** to `search_token` when the user token is unlikely to work as-is for search; otherwise `search_token` = user token. In-session discovery allowed **only** for this choice. Ask if multiple anchors are equally valid; do not collect evidence until one `search_token` is chosen.
3. **Evidence** - build a closed evidence packet in-session (see Evidence below).
4. Read **only** paths in `paths` plus any file needed to interpret a `hits` line already in evidence. No further repo discovery.
5. From evidence and those reads, reason about definition sites, depends-on, referenced-by, evolution, docs, and follow-on threads. Omit what evidence cannot support.
6. **Emit Output** - in order: Weave Ledger, then `# Summary` only (see Output). Closing Summary must not introduce paths or symbols outside the ledger and read set.

## Disambiguation

- Skip when the user token is already a path, symbol, or literal grep needle.
- Ledger title uses the **user token** (`# Grim Weave: <user token>`).
- When user token ≠ `search_token`, note both in the closing `# Summary` when needed.

## Evidence

Collect in-session (prefer `git grep`; else bounded ripgrep or line scan).

**Prune** - skip any path with a segment in this closed set:

`.git`, `node_modules`, `vendor`, `.venv`, `venv`, `__pycache__`, `.pnpm-store`, `.yarn`, `dist`, `build`, `_site`, `.next`, `.nuxt`, `target`, `coverage`, `.turbo`

**Caps** (hard stop when reached):

| Cap | Value |
| --- | --- |
| `paths` | 40 |
| `hits` (total) | 120 |
| `hits` per path | 8 |
| `commits` | 5 |
| files scanned (fallback line scan) | 8000 |

**Search**

- `file`: path relative to target; hits on that path.
- `symbol`: `git grep -F` / ripgrep; case-insensitive; flag `definition_candidate` when line matches declaration-shaped patterns for the language.
- `concept`: phrase search; case-insensitive; prefer docs (`*.md`, `*.mdx`, `docs/`, `adr/`).

**Commits** (when git available): pickaxe / `git log` on touched paths; merge newest-first; max 5. When git unavailable, `commits` empty.

**Evidence packet** (session-only, before ledger):

| Field | Shape |
| --- | --- |
| `token_kind` | `file` \| `symbol` \| `concept` |
| `paths` | Closed read set (repo-relative) |
| `hits` | Path, line, kind (`match` \| `definition_candidate`) |
| `documents` | Doc-path subset of hits |
| `commits` | Short sha + subject; newest first |
| `git_available` | boolean |

## Output

North star: one at-a-glance ledger for the token, then a short closing synthesis.

| Part | Required | Holds |
| --- | --- | --- |
| Title + one-line distillation | yes | Outside fence: `# Grim Weave: <user token>` and one sentence hook (scope or role) |
| Weave Ledger | yes | `text` fence: tree only |
| `# Summary` | yes | See Summary |

### Summary

1. What this token is in this repo - evidence-backed, token/ask only, not repo-wide shape.
2. Suggest **1-3** follow-ups from **Threads** as `/grimweave <token>` loop (prose or inline):
  - Omit when Threads is empty.
  - Do not repeat the hook verbatim; do not list every `▶` - pick best continuations

### Weave Ledger

- Token header is the weave root.
- One required `ⓘ` annotation under the header before the divider - short role line from evidence only; not a second Summary.
- Do not duplicate closing Summary in the tree.

Sections (use `≣` trunks; omit empty sections):

| Trunk | Content |
| --- | --- |
| Definition | Defining paths / symbols from `definition_candidate` hits and file reads |
| Relationships | `Depends On` and `Referenced By` - named symbols inferred from read files |
| Provenance | `Commits` (`●` + short sha + subject, **newest first**); `Documents` from `documents` |
| Threads | `▶` follow-on symbols worth a nested `/grimweave` (high-signal only). Closing Summary selects from these for the loop suggestion. |

Provenance layout:

- Omit `Commits` when evidence has no commits.
- Omit `Documents` when `documents` is empty.

Style:

- Hierarchy: `│`, `├─`, `└─`
- Annotation: `├─ⓘ`, `└─ⓘ`
- Concept: `├─≣`, `└─≣`
- Thread: `├─▶`, `└─▶`
- Commit snapshot: `├─●`, `└─●`
- Divider: `╞══════════════════◆`

Rules above are authoritative; below is drawing guide only.

```text
TodoService
├─ⓘ Core task orchestration
╞══════════════════◆
│
├─≣ Definition
│  ├─ packages/core/todo/service.go
│  └─ interface.go
│
├─≣ Relationships
│  ├─ Depends On
│  │  ├─ TodoStore
│  │  ├─ Clock
│  │  └─ EventBus
│  │
│  └─ Referenced By
│     ├─ CreateTodo
│     ├─ UpdateTodo
│     └─ TodoHandler
│
├─≣ Provenance
│  ├─ Commits
│  │  ├─● 0034ac refactor(todo): extract EventBus
│  │  ├─● 0017b2 feat(product): business logic
│  │  └─● 001e13 feat(todo): introduce TodoService
│  │
│  └─ Documents
│     ├─ adr/todo-app-arch.md
│     └─ docs/todo.md
│
└─≣ Threads
   ├─▶ TodoStore
   └─▶ EventBus
```

## Usage

```text
/grimweave discover.py
/grimweave packages/core/SKILL.md
/grimweave "log in"
/grimweave TodoService
```

## Boundaries

- Session-only viewport; no disk artifacts.
- No collection or reads beyond Evidence caps and closed `paths`.
