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
2. **Disambiguate** to `search_token` when the user token is unlikely to work as-is for search; otherwise `search_token` = user token. In-session discovery allowed **only** for this choice. Ask if multiple anchors are equally valid; do not run Script until one `search_token` is chosen.
3. **Evidence** - run Script with `search_token`; parse stdout JSON as the default closed evidence set (see Script, Script policy, and Evidence below).
4. Read **only** paths in the closed evidence set plus any file needed to interpret a `hits` line already in evidence. No further repo discovery except supplement per Script policy.
5. From evidence and those reads, reason about definition sites, depends-on, referenced-by, evolution, docs, and follow-on threads. Omit what evidence cannot support.
6. **Emit Output** - in order: Weave Ledger, then `# Summary` only (see Output). Closing Summary must not introduce paths or symbols outside the ledger and read set.

## Disambiguation

- Skip when the user token is already a path, symbol, or literal grep needle.
- Ledger title uses the **user token** (`# Grim Weave: <user token>`).
- When user token ≠ `search_token`, note both in the closing `# Summary` when needed.
- JSON field `token` is always the **search token** passed to Script.

## Script

From the skill root directory, run:

```bash
python3 <skill-root>/scripts/weave.py --target <absolute_workspace_root> --token <search_token>
```

- Always pass an absolute workspace to `--target`. Never use `--target .`
- Stdout: one JSON object (`kind`: `weave_evidence`). Evidence only - not the Weave Ledger.
- Script collects occurrences and history; agent owns relationships, threads, and the viewport.

### Script policy

- Script stdout is the evidence floor (`weave_evidence`); relationships, threads, and the Weave Ledger are agent synthesis from evidence and reads.
- **Prefer** `scripts/weave.py` for the evidence floor (do not skip the script and freestyle the whole collection phase).
- **Re-run** with reasoned `--token` / `search_token` or after disambiguation when output is empty, at `caps`, or mismatched to the ask. Briefly note what changed vs the prior run.
- **Read-only** - do not edit script files in-session; read the script only to understand behavior.
- **Supplement** only after at least one script run (re-run when params might help). Default closed set = latest weave stdout; supplemental grep only per policy, within the spirit of `caps`. Merge supplements into an explicit closed set before reads. Note in chat when evidence came from outside script stdout (one line is enough).

## Evidence

The script implements collection within `caps` (see JSON). Default closed set = latest script stdout unless supplemented per Script policy.

**Prune** - skip any path with a segment in this closed set:

`.git`, `node_modules`, `vendor`, `.venv`, `venv`, `__pycache__`, `.pnpm-store`, `.yarn`, `dist`, `build`, `_site`, `.next`, `.nuxt`, `target`, `coverage`, `.turbo`

**Stdout fields** (deterministic evidence floor):

| Field | Shape |
| --- | --- |
| `kind` | `weave_evidence` |
| `token` | Search needle used for collection |
| `token_kind` | `file` \| `symbol` \| `concept` |
| `paths` | Closed read set (`./rel` paths) |
| `hits` | Path, line, text, kind (`match` \| `definition_candidate`) |
| `documents` | Doc-path subset of hits |
| `commit_groups` | Per git root: `repo` display path + `commits` (sha, subject); newest first within each group |
| `commits_order` | `newest_first` when any group has commits |
| `git_available` | boolean |
| `caps` | `paths`, `hits`, `hits_per_path`, `commits_per_repo`, `scan_files` limits |

Stdout includes `caps`, `paths`, `hits`, `documents`, and `commit_groups`. Relationships and threads are agent-composed after reads.

**Not in JSON (agent synthesis):** Relationships, Threads, ledger annotations beyond evidence-backed role line, `# Summary`, follow-up `/grimweave` suggestions.

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
| Provenance | `Commits` from `commit_groups` (nest by `repo` then `●` rows, newest first within each repo); `Documents` from `documents` |
| Threads | `▶` follow-on symbols worth a nested `/grimweave` (high-signal only). Closing Summary selects from these for the loop suggestion. |

Provenance layout:

- Omit `Commits` when `commit_groups` is empty.
- Under `Commits`, nest one branch per `repo` in `commit_groups` (shallow-first), then `●` rows for that group's `commits`.
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
│  │  ├─ ./
│  │  │  └─● 0034ac refactor(todo): extract EventBus
│  │  └─ packages/nested/
│  │     ├─● 0017b2 feat(product): business logic
│  │     └─● 001e13 feat(todo): introduce TodoService
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
- No collection or reads beyond closed evidence set, evidence `caps`, and Script policy supplements.
