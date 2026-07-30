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
| `budget` | no | Max files in one focused read set; default `25`. |

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

**Outer artifacts: policy only.** Record boundary decisions about Projects when evidenced in outer commits, rules, or XP - for example cortex-not-landlord or local ownership. Do not name, inventory, or narrate inner repos. Do not record inner-project decisions, refactors, or commits. If the only fact is "nested repos exist under `projects/`", omit it unless an outer decision changed the layout.

## Artifacts

Default paths at `repo_root`:

| Artifact | Path | Role |
| --- | --- | --- |
| Changelog | `./CHANGELOG.md` | Factual ledger; Unreleased-only writes |
| History | `./HISTORY.md` | Temporal ledger; dated timeline |

**Versioning:** Forge writes only under `## [Unreleased]`. Humans cut versioned release sections.

**Marker:** lives in `CHANGELOG.md` only.

```markdown
<!-- marker: abc1234 -->
```

**Detect phase:** `CHANGELOG.md` absent or missing valid marker -> genesis; otherwise delta.

**References:** HISTORY may link to CHANGELOG bullets and ADR files when git named them. CHANGELOG never links to HISTORY.

## CHANGELOG contract (Keep a Changelog 1.1.0)

Forge creates or extends `CHANGELOG.md` at `repo_root`.

Header (genesis if new file):

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!-- marker: def5678 -->

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
- **Existing CHANGELOG** - extend in place; match existing format when present; add `marker` on first Forge run without rewriting human entries.
- **No HISTORY links** - changelog never mentions `HISTORY.md`.

## HISTORY contract (temporal ledger)

HISTORY records when changes landed and what they mean in sequence. No `## Recent`. No marker.

```markdown
# History

<What this project is and why this sidecar exists.>

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
| **Outer repo policy** | Projects only as Throneroom policy; no inner repo names or commits. |

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
2. **Detect** - no `CHANGELOG.md` or no marker -> genesis; else delta.
3. **Status** - run `status` with `repo_root` as `--target`.
4. **Genesis**
   - Run `status --bootstrap`.
   - Create/update `CHANGELOG.md` with KaC header and curated `## [Unreleased]` entries from `commits`.
   - Create `HISTORY.md` with `## Story` and optional `## Timeline` era anchors (0-3); link changelog and ADRs git named.
   - Set marker to `HEAD` in CHANGELOG.
5. **Delta**
   - Run `status` (commits since marker in JSON, each with `date`).
   - Pick 1-3 `focus` candidates from commit paths or root; read each `read_set`.
   - Append 0-3 notable bullets under correct `###` type(s) in `## [Unreleased]`; dedupe.
   - Optionally append 0-1 dated `### YYYY-MM-DD` entry under `## Timeline` when narrative is warranted (`commits[-1].date`).
   - Advance marker in CHANGELOG.
6. **Write** - only `CHANGELOG.md` and `HISTORY.md` at `repo_root`.
7. **Emit** - report both artifacts.

## Script

From the skill root directory, run:

```bash
python3 <skill-root>/scripts/forge.py \
  status \
  --target <absolute_repo_root>

python3 <skill-root>/scripts/forge.py \
  status \
  --target <absolute_repo_root> \
  --bootstrap

python3 <skill-root>/scripts/forge.py \
  focus \
  --target <absolute_repo_root> \
  --candidate <relative_candidate_path> \
  --budget <budget>
```

### Script policy

- Always pass `repo_root` as `--target`. Never pass a workspace path that is wider than `repo_root`.
- `status` returns artifact paths, marker, bounded `commits` (each with `commit`, `date`, `subject`), and `working_tree`. Do not run raw git commands during a Forge run.
- Genesis -> `status --bootstrap` (reverse log, cap 50). Delta -> `status` (commits since marker, cap 50).
- `focus` emits a bounded contextual read set: candidate files, README, and manifests on the path to root.
- Re-run focus with a reasoned `--budget` when the read set is full or misses context. Briefly state what changed.
- `forge.py` is read-only. Do not edit it while using Forge.
- Include material `working_tree` paths only when focused evidence supports them.

## Output

```markdown
# Grim Forge: <target>

## Provenance

- **Repo:** `./`
- **Phase:** delta
- **Changelog:** `./CHANGELOG.md`
- **History:** `./HISTORY.md`
- **Marker:** abc1234 -> def5678
- **Written:** 2 Unreleased entries; 1 Timeline entry
- **Status:** `status --bootstrap` | `status`
```

- The changelog and history are the deliverables. Do not return a parallel suggestion list.
- State repo (display path under the workspace), phase, both artifact paths, marker before and after, and what was written.
- State which `status` mode was used.

## Boundaries

- One changelog and one history per git repository. Never append nested-repo deltas to outer artifacts.
- Outer Story may cite Projects only as policy. Never cite inner repo paths, commits, or implementation detail.
- Forge writes only `CHANGELOG.md` and `HISTORY.md` at `repo_root`.
- Write 0-3 Unreleased bullets per delta run. Skip noise and dedupe against existing Unreleased.
- Preserve Story after genesis. Amend it only to correct a factual error with evidence.
- No facts, commands, APIs, history, or rationale beyond focused evidence.
