---
name: grim-weave
description: >-
  Follow a file, symbol, or concept through a workspace and emit a ledger of
  definitions, relationships, provenance, and threads. Use when tracing
  provenance, dependencies, or documentation for a token in a codebase.
---

# Grim Weave

_Follow the thread._

Follow a single token through a workspace, revealing its provenance, relationships, and supporting evidence. Starting from a symbol, file, or concept, it produces a deterministic thread showing where it is defined, what it depends on, what depends on it, how it evolved, and where it is documented.

## Workflow

1. Resolve target (cwd / named repo) and **user token** (file path, symbol, or concept phrase). Ask if either is unclear.
2. **Disambiguate** to `script_token` when the user token is unlikely to work as-is for Script; otherwise `script_token` = user token. Choose how in-session (no fixed search recipe). Ask if multiple anchors are equally valid; do not run Script until one `script_token` is chosen.
3. Run Script with `script_token`; parse stdout JSON as the closed evidence set.
4. Read **only** paths listed in `paths` plus any file you must open to interpret a `hits` line already in evidence. No further repo discovery.
5. From evidence and those reads, reason about definition sites, depends-on, referenced-by, evolution, docs, and follow-on threads. Omit what evidence cannot support.
6. Emit the Weave Ledger in chat. Do not write the ledger to disk.

## Disambiguation

Outcome only: pick `script_token` for `--token` before Script runs. In-session discovery is allowed **only** for that choice—not for evidence after Script.

- Skip when the user token is already a path, symbol, or literal grep needle.
- Ledger title uses the **user token** (`# Grim Weave: <user token>`).
- When user token ≠ `script_token`, note both in `Evidence:`.

## Script

From the skill root directory, run:

```bash
python3 <skill-root>/scripts/weave.py --target <absolute_target_dir> --token <script_token>
```

- Always pass an absolute workspace to `--target`. Never use `--target .`
- Stdout: one JSON object (`token_kind`, `paths`, `hits`, `documents`, `commits`, `commits_order`, `git_available`).
- Script collects occurrences and history only. Agent owns relationships and threads.
- Do not invent collection scripts at runtime.

## Output

North star: one at-a-glance ledger for the token.

1. Emit one Weave Ledger:
  - `# Grim Weave: <user token>` outside the fence
  - One-line distillation outside the fence (agent judgment; grounded in evidence)
  - `text` fence: tree only
2. `Evidence:` - ≤3 `-` bullets; what was discovered by weave

### Weave Ledger

- Token header is the weave root.
- One required `ⓘ` annotation under the header before the divider - purpose or role from evidence only.

Sections (use `≣` trunks; omit empty sections):

| Trunk | Content |
| --- | --- |
| Definition | Defining paths / symbols from `definition_candidate` hits and file reads |
| Relationships | `Depends On` and `Referenced By` - named symbols the agent infers from read files |
| Provenance | `Commits` (`●` + short sha + subject from evidence, **newest first**); `Documents` from `documents` |
| Threads | `▶` follow-on symbols worth a nested `/grim-weave` (high-signal only) |

Provenance layout:

- Omit `Commits` when evidence has no commits.
- Omit `Documents` when `documents` is empty.

Style (matches Grimoire glyph dictionary):

- Hierarchy: `│`, `├─`, `└─`
- Annotation: `├─ⓘ`, `└─ⓘ`
- Concept: `├─≣`, `└─≣`
- Thread: `├─▶`, `└─▶`
- Commit snapshot: `├─●`, `└─●`
- Divider: `╞══════════════════◆`
- Indent each level; continue ancestors with `│`
- `├─` non-final sibling; `└─` final sibling

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
