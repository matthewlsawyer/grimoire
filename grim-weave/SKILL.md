---
name: grim-weave
description: >-
  Follow a file, symbol, or concept through a workspace and emit a ledger of
  dependencies, references, and related threads. Use when tracing how a token
  connects across a codebase.
---

# Grim Weave

_Follow the thread._

Follow a single token through a workspace: bounded path discovery, then an at-a-glance **Weave Ledger** in chat. The script lists files that contain the token; relationships are agent-composed from reads. Do not write the ledger to disk.

## Inputs

| Input | Required | Holds |
| --- | --- | --- |
| `target` | yes | Absolute workspace root. Ask if unclear. |
| `user token` | yes | File path, symbol, or concept phrase. |

| Token shape | Search behavior |
| --- | --- |
| `path/to/file.go`, `SKILL.md` | `file` - resolve path(s), include in closed set |
| `TodoService` (identifier) | `symbol` - case-insensitive grep/scan |
| `log in`, multi-word phrase | `concept` - case-insensitive line scan (regex retry when substring finds nothing) |

## Workflow

1. Resolve `target` and **user token**. Ask if either is unclear.
2. **Disambiguate** to `search_token` when the user token is unlikely to work as-is for search; otherwise `search_token` = user token. In-session discovery allowed **only** for this choice. Ask if multiple anchors are equally valid; do not run Script until one `search_token` is chosen.
3. **Discovery** - run Script with `search_token`; latest stdout lines are the closed **path set** (see Script, Script policy, and Discovery below).
4. Read **only** paths in the closed path set. No further repo discovery except supplement per Script policy.
5. From those reads, map **Definition**, **Depends On**, **Referenced By**, and **Related** within each trunk's row cap (see Weave Ledger). Omit what reads cannot support; omit uncertain rows.
6. **Emit Output** - in order: Weave Ledger, then `# Summary`, then `Threads:` when applicable (see Output). Closing sections must not introduce paths or symbols outside the ledger and read set.

## Disambiguation

- Skip when the user token is already a path, symbol, or literal grep needle.
- Ledger title uses the **user token** (`# Grim Weave: <user token>`).
- When user token ≠ `search_token`, note both in `# Summary` (one short clause).

## Script

From the skill root directory, run:

```bash
python3 <skill-root>/scripts/weave.py --target <absolute_workspace_root> --token <search_token> [--budget <budget>]
```

- Always pass an absolute workspace to `--target`. Never use `--target .`
- Stdout: flat paths, one `./rel` path per line. No section headers.
- Default `budget`: `40`.

### Script policy

- Script stdout is the path observation floor; the Weave Ledger is agent-composed from reads.
- **Prefer** `scripts/weave.py` for the path list (do not skip the script and freestyle collection).
- **Re-run** with reasoned `--token` / `search_token`, `--budget`, or after disambiguation when stdout is empty, at budget, or mismatched to the ask. Briefly note what changed vs the prior run.
- **Read-only** - do not edit script files in-session; read the script only to understand behavior.
- **Supplement** only after at least one script run (re-run when params might help). Keep supplements bounded; merge into an explicit path set before reads. Note in chat when any path came from outside script stdout (one line is enough).

## Discovery

The script implements this contract:

**Prune** - skip any path with a segment in this closed set:

`.git`, `node_modules`, `vendor`, `.venv`, `venv`, `__pycache__`, `.pnpm-store`, `.yarn`, `dist`, `build`, `_site`, `.next`, `.nuxt`, `target`, `coverage`, `.turbo`

**Collection** - bounded path discovery (stdout is unique paths only; internal line-hit caps bound grep/scan before dedupe):

| Step | Behavior |
| --- | --- |
| Classify | `file` (path or basename), else `symbol` if single identifier, else `concept` |
| Scan | Line-scan text-like extensions and doc paths listed under `target` via `find(1)` |
| Concept retry | If substring scan finds no line hits, retry with escaped-regex line match |
| Case | `file` token content match is case-sensitive; `symbol` / `concept` are case-insensitive |
| File seeds | Resolved file path(s) always included in the path set even with no line match |

**Ranking** - dedupe by path; sort shallow-first `(depth, path)`; cap at `budget` (CLI default `40`).

**Closed read boundary** - after the path set is fixed, no ad-hoc expansion except supplement per Script policy. Reads stay within the closed path set.

Discovery does not honor `.gitignore`.

## Output

North star: one at-a-glance ledger for the token, then a **terse** `# Summary` (salient facts only).

| Part | Required | Holds |
| --- | --- | --- |
| Title + one-line distillation | yes | Outside fence: `# Grim Weave: <user token>` and one sentence hook (scope or role) |
| Weave Ledger | yes | `text` fence: tree only |
| `# Summary` | yes | 1-2 sentences or ≤3 terse bullets; see Summary |
| `Threads:` | when ledger Related non-empty | See Threads |

### Summary

- **Length:** at most **2 sentences**, or **≤3** `-` bullets (one line each).
- **Content:** one or two salient facts not obvious from the ledger hook alone - role, scope, or gotcha. Evidence-backed; token/ask only.
- **Do not:** repeat the title hook, recap Definition/Depends On/Referenced By rows, or narrate repo shape.
- When user token ≠ `search_token`, one short clause naming both is enough.

### Threads

After `# Summary`, when the ledger **Related** trunk is non-empty:

```markdown
Threads:
- `/grim-weave <token>` - short description
- ...
```

- Pick **1-3** high-signal continuations from the ledger Related trunk (not every `≣` row).
- Each bullet: invocable `/grim-weave` command plus one short phrase (why pull that thread).
- Omit the entire `Threads:` block when the ledger Related trunk is empty.

### Weave Ledger

Sections (top-level `≣` trunks; omit empty). Cap rows per trunk - prefer highest-signal evidence; do not pad to the max.

| Trunk | Cap | Content |
| --- | --- | --- |
| Definition | 1-3 | Primary file(s) where the token is defined (declaration, entrypoint, canonical config). Path rows; optional `ⓘ` for non-obvious role. |
| Depends On | 1-5 | Files the definition files pull in or require to exist - imports, build deps, types - not definition sites. Path rows; optional `ⓘ`. |
| Referenced By | 1-5 | Files that import, call, configure, or document the definition files. Path rows; optional `ⓘ`. |
| Related | 1-3 | Follow-on tokens for nested `/grim-weave`; each child `├─≣` / `└─≣`. Closing `Threads:` picks from these (1-3). |

Evidence-backed only - omit uncertain rows and empty trunks.

Rules:

- Root header: `≣ <user token>`.
- One required `ⓘ` annotation under the header, before divider - short role from reads only; not a second Summary.
- Do not duplicate closing Summary in the tree.
- Prefer vertical trees; one `./path` per branch under a trunk.
- Moderate `ⓘ` use - detail reads cannot hang as paths.
- Use `≣` for section trunks and Related follow-on tokens.
- Depends On and Referenced By: other files only. Same-file callees or entrypoints -> Definition `ⓘ` or Related `≣`; never repeat the definition path in those trunks.

Style:

- Hierarchy branch glyphs: `│`, `├─`, `└─`.
- Annotation glyphs: `├─ⓘ`, `└─ⓘ`, `─ⓘ`.
- Concept glyphs: `├─≣`, `└─≣`, `─≣`.
- Divider glyph: `╞══════════════════◆`.
- Indent each level; continue ancestors with `│`.
- `├─` / `├─ⓘ` / `├─≣` non-final sibling;
- `└─` / `└─ⓘ` / `└─≣` final sibling.

Rules above are authoritative; below is drawing guide only.

```text
≣ zig build
├─ⓘ CLI front door to `./build.zig` `pub fn build`; options via `zig build --help` / `Config.zig`
╞══════════════════◆
│
├─≣ Definition
│  └─ ./build.zig
│     └─ⓘ `pub fn build` root; default install to `zig-out`
│
├─≣ Depends On
│  ├─ ./build.zig.zon
│  └─ ./src/build/Config.zig
│
├─≣ Referenced By
│  ├─ ./AGENTS.md
│  ├─ ./HACKING.md
│  └─ ./CMakeLists.txt
│     └─ⓘ triggers `zig build -Demit-lib-vt`
│
└─≣ Related
   ├─≣ Config.zig
   ├─≣ emit-macos-app
   └─≣ distcheck
```

Colocated symbol (omit Depends On; no duplicate definition path):

```text
≣ weave_paths
├─ⓘ Discovery orchestrator in `weave.py`; CLI prints ranked paths
╞══════════════════◆
│
├─≣ Definition
│  └─ ./projects/grimoire/grim-weave/scripts/weave.py
│     └─ⓘ `weave_paths`; `main()` stdout loop; calls `list_files`, `classify_token`, `collect_paths`
│
├─≣ Referenced By
│  └─ ./projects/grimoire/tests/grim-weave/test.py
│     └─ⓘ `WeavePathsTests` via `load_script` module handle
│
└─≣ Related
   ├─≣ collect_paths
   ├─≣ classify_token
   └─≣ list_files
```

## Usage

```text
/grim-weave discover.py
/grim-weave packages/core/SKILL.md
/grim-weave "log in"
/grim-weave TodoService
```

## Boundaries

- Session-only viewport; no disk artifacts.
- No collection or reads beyond closed path set, `budget`, and Script policy supplements.
