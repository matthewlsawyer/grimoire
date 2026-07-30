---
name: grim-forge
description: >-
  Maintain forge provenance - a Keep a Changelog ledger and a narrative HISTORY
  sidecar per git repository root. Unreleased-only writes; human cuts releases.
---

# Grim Forge

_Forge provenance._

Forge maintains two artifacts per git repository:

- **CHANGELOG.md** - factual ledger per [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/)
- **HISTORY.md** - temporal ledger; dated timeline that may reference the changelog

The first run bootstraps both. Later runs append curated Unreleased bullets and dated Timeline entries since the recorded marker.

## Inputs

| Input | Required | Holds |
| --- | --- | --- |
| `target` | no | Repository or directory named by the prompt. Empty means the current workspace root. |
| `intention` | no | The session ask. |
| `budget` | no | Max files to read per run; default `50`. |

Resolve `target` from the prompt before collection:

- No target -> current workspace root.
- One unambiguous repository or path -> use it.
- Multiple plausible targets -> ask.

## Repo scope

One git repository, one changelog, one history, one run.

Resolve `repo_root` before collection:

```bash
git -C <target> rev-parse --show-toplevel
```

- If `target` lies inside a nested repo, `repo_root` is that nested root.
- If ambiguous (multiple nested targets, no clear intent), ask.
- All Script calls and artifact writes are relative to `repo_root`.
- Do not read, cite, or write provenance for files outside `repo_root`.
- Nested repos under the outer tree are out of scope unless `repo_root` is that nested repo.

**Outer artifacts: policy only.** Do not name, inventory, or narrate inner repos. Do not record inner-project decisions, refactors, or commits. If the only fact is "nested repos exist under `projects/`", omit it unless an outer decision changed the layout.

## Artifacts

Default paths at `repo_root`:

| Artifact | Path | Role |
| --- | --- | --- |
| Changelog | `./CHANGELOG.md` | Factual ledger; Unreleased-only writes |
| History | `./HISTORY.md` | Temporal ledger; dated timeline |

**Versioning:** Delta appends only under `## [Unreleased]`. Genesis cuts `## [version] - YYYY-MM-DD` release sections from git tags in `status.releases` (newest first, below Unreleased).

**Releases:** `status` returns semver-shaped git tags (`tag`, `version`, `commit`, `date`), sorted newest first. Use them to bound Unreleased and to seed versioned changelog sections on genesis.

**Marker:** lives in `HISTORY.md` only.

```markdown
<!-- marker: abc1234 -->
```

**Detect phase:** `HISTORY.md` absent or missing valid marker -> genesis; otherwise delta.

**References:** HISTORY may link to CHANGELOG bullets and ADR files when git named them. CHANGELOG never links to HISTORY.

## CHANGELOG contract (Keep a Changelog 1.1.0)

Forge creates or extends `CHANGELOG.md` at `repo_root`.

Header (genesis if new file):

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- ...

### Changed
- ...

### Removed
- ...

### Fixed
- ...

### Deprecated
- ...

### Security
- ...
```

Rules:

- **Curated, not a git dump** - synthesize notable changes; group under KaC types (`Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`).
- **Omit empty type sections** - per KaC guidance, do not keep blank `### Added` blocks.
- **Map evidence** - use conventional commit type when clear (`feat` -> Added, `fix` -> Fixed, `refactor!` -> Changed, etc.); default to Changed when unsure.
- **Bullet content** - human-readable what changed; optional commit shorthand in parentheses at end.
- **Existing CHANGELOG** - extend in place; match existing format when present; do not add forge metadata.
- **No HISTORY links** - changelog never mentions `HISTORY.md`.
- **Releases on genesis** - when `releases` is non-empty, `## [Unreleased]` holds commits after the newest tag only; cut `## [version] - date` sections from `releases` (strip leading `v` from tag). Curate bullets from commits between each tag and the next newer tag; omit empty sections. When tag count is large, keep recent releases in full and summarize older major lines rather than one heading per patch.
- **Releases on delta** - do not rewrite versioned sections; append to `## [Unreleased]` only.

## HISTORY contract (temporal ledger)

HISTORY records when changes landed and what they mean in sequence. No `## Recent`.

```markdown
# History

<What this project is and why this sidecar exists.>

<!-- marker: def5678 -->

## Story

### Origins
...

### Architecture
...

### Refactors
...

## Timeline

### 2026-07-29

The Projects workshop boundary ([CHANGELOG.md](./CHANGELOG.md#unreleased)) restores cortex-not-landlord after the Court retirement arc.

### 2026-07-20

...
```

Rules:

| Rule | Detail |
| --- | --- |
| **Story** | Palimpsest. Thematic eras; genesis only. Optional era date ranges in prose (`2026-06 -> 2026-07`); not a commit dump. |
| **Timeline** | Append-only ledger. Reverse chronological (`### YYYY-MM-DD` headings). |
| **Genesis** | Write Story; seed Timeline with 0-3 dated era anchors when bootstrap commits warrant them (curated, not one line per commit). |
| **Delta** | Append 0-1 entry per run under `### YYYY-MM-DD` where the date is the **newest commit** in the forged range (`commits[-1].date` from status). |
| **Entry content** | Brief narrative glue + link to CHANGELOG for what + ADR link when git named one. Do not restate bullets or ADR bodies. |
| **Dedupe** | Skip a timeline entry when the changelog bullet alone is sufficient and no narrative adds temporal context. |
| **Outer repo policy** | No inner repo names or commits. |

## ADRs: reference via git, don't hunt

Forge does not hunt for missing ADRs or suggest new ones. When a commit touches `docs/adrs/*.md`, read that file before writing a HISTORY timeline entry that links it.

| Layer | ADR role |
| --- | --- |
| **CHANGELOG** | Facts only. No ADR links. |
| **HISTORY** | Link when ADR already explains the decision; do not restate ADR prose. |
| **Collector** | No ADR finder. |
| **SKILL** | Read ADR when git named the path and a Timeline entry warrants it. |

## Workflow

1. **Interpret** - resolve target, `repo_root`, intention.
2. **Detect** - no `HISTORY.md` or no marker -> genesis; else delta.
3. **Status** - run `status.py` with `repo_root` as `--target` (auto-selects genesis or delta range from marker).
4. **Read** - read from `status.touched` per read policy below; include `working_tree` paths only when they support a bullet.
5. **Genesis**
   - Create/update `CHANGELOG.md` with KaC header, curated `## [Unreleased]` (commits after newest tag), and versioned release sections from `releases`.
   - Create `HISTORY.md` with `## Story` and optional `## Timeline` era anchors (curated; not one line per commit); link changelog and ADRs git named.
   - Set marker to `HEAD` in HISTORY.
6. **Delta**
   - Append notable bullets under correct `###` type(s) in `## [Unreleased]`; dedupe.
   - Optionally append 0-1 dated `### YYYY-MM-DD` entry under `## Timeline` when narrative is warranted (`commits[-1].date`).
   - Advance marker in HISTORY.
7. **Write** - only `CHANGELOG.md` and `HISTORY.md` at `repo_root`.
8. **Emit** - compose the ledger viewport from artifacts just written; emit title, fenced viewport, and slim Provenance footer. Do not return a parallel suggestion list.

## Read policy

| Rule | Detail |
| --- | --- |
| **Source** | `status.touched` first; `working_tree` only when it supports a bullet |
| **Grouping** | 1-3 narrative dirs from touched parent paths |
| **Context** | Ancestor README/manifests on path to root for each touched file |
| **Budget** | Cap reads at `budget` (default 50) |
| **Fallback** | If `touched` empty: `./README.md` + root manifest only |
| **No `.`** | No full-repo tree walks |

## Script

From the skill root directory, run:

```bash
python3 <skill-root>/scripts/status.py --target <absolute_repo_root>
```

### Script policy

- Always pass `repo_root` as `--target`. Never pass a workspace path that is wider than `repo_root`.
- `status.py` auto-selects range from the HISTORY marker: no marker -> genesis; marker present -> delta (`marker..HEAD`). Commits and `touched` paths use the same latest-`250` commit window.
- Returns artifact paths, `phase`, marker, `commits` (latest 250; each with `commit`, `date`, `subject`), `touched` (paths from that window, newest-first), `releases` (git tags), and `working_tree`. Do not run raw git commands during a Forge run.
- `status.py` is read-only. Do not edit it while using Forge.
- File reads are skill-owned per read policy above.

## Output

| Part | Required | Holds |
| --- | --- | --- |
| Title | yes | `# Grim Forge: <target>` outside the fence |
| Ledger | yes | `text` fence: agent-composed glyph viewport |
| Provenance | yes | slim footer: phase, marker, written |

### Rendered output

````markdown
# Grim Forge: <target>

```text
<ledger-viewport>
```

## Provenance

- **Phase:** delta
- **Marker:** abc1234 -> def5678
- **Written:** 2 Unreleased entries; 1 Timeline entry
````

- `CHANGELOG.md` and `HISTORY.md` are the deliverables on disk. The ledger viewport is session-only.
- Do not return a parallel suggestion list.

### Ledger viewport

Compose after writes complete. Read what was written; do not redraw from memory.

Glyphs:

- `│` `├` `└` `─` hierarchy
- `╞` `═` divider
- `◆` terminator
- Leaves are plain text

| Rule | Detail |
| --- | --- |
| **Workspace trunk** | Basename of `repo_root` with trailing `/`; owns the sole `╞═◆` divider and spacer line `│` |
| **CHANGELOG branch** | Under trunk: `CHANGELOG.md` -> `## [Unreleased]` -> versioned `## [version]` sections on genesis when `releases` present -> only non-empty `###` types -> bullet leaves (truncate long bullets) |
| **Branch spacer** | Bare `│` line between CHANGELOG and HISTORY siblings |
| **HISTORY branch** | Under trunk: `HISTORY.md` -> `marker: <before> -> <after>` (genesis uses `none -> <after>`) -> `## Story` (genesis only; omit on delta when unchanged) -> `## Timeline` -> latest `### YYYY-MM-DD` entries (cap 3, newest first) |
| **This run** | Show leaves written this run; omit empty KaC sections; do not dump full file bodies |

Rules above are authoritative; below is drawing guide only.

```text
repository/
╞══════════════════◆
│
├─ CHANGELOG.md
│  └─ ## [Unreleased]
│     ├─ ### Added
│     └─ ### Changed
│
└─ HISTORY.md
   ├─ marker: none -> def5678
   ├─ ## Story
   └─ ## Timeline
      └─ ### 2026-07-29
```

```text
foo-api/
╞══════════════════◆
│
├─ CHANGELOG.md
│  ├─ ## [Unreleased]
│  │  ├─ ### Added
│  │  │  └─ `{ FooExport }` named export on the foo-api package (6d2c04d1)
│  │  └─ ### Fixed
│  │     └─ Bar worker adopts idempotency keys (b71d4f0)
│  └─ ## [3.1.6]
│
└─ HISTORY.md
   ├─ marker: 9fd02ae -> b71d4f0
   └─ ## Timeline
      └─ ### 2026-08-04
         └─ Idempotency guard closes duplicate-charge gap
```

## Boundaries

- One changelog and one history per git repository. Never append nested-repo deltas to outer artifacts.
- Never cite inner repo paths, commits, or implementation detail.
- Forge writes only `CHANGELOG.md` and `HISTORY.md` at `repo_root`.
- Write 0-3 Unreleased bullets per delta run. Skip noise and dedupe against existing Unreleased.
- Preserve Story after genesis. Amend it only to correct a factual error with evidence.
- No facts, commands, APIs, history, or rationale beyond touched evidence and read policy.
