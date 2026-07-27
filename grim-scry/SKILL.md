---
name: grim-scry
description: >-
  Given a repository or workspace, produce a simple canonical understanding.
  Use when the user invokes grim-scry or wants an at-a-glance conceptual map
  of a project.
---

# Grim Scry

_You must see before you act._

Given a repository or workspace, distill meaning and emit one at-a-glance **Scry Lantern** in chat. Viewport is the spell: ideas hang first; implementers and named commands hang underneath. Inventory and lantern stay session-only.

## Inputs

| Input | Required | Holds |
| --- | --- | --- |
| `target` | yes | Absolute path to workspace root, or remote URL (clone to a temp dir, then absolute path). Ask if unclear. |
| `budget` | no | Max seed paths to read; default `50`. |

## Workflow

1. Resolve `target` to an absolute workspace root (cwd, named path, or clone).
2. **Discovery** - run Script; latest stdout lines are the closed **Seed set** (see Script, Script policy, and Discovery below).
3. Read **only** Seed set paths. Skip unreadable seeds; omit rather than invent.
4. Distill for salience in-session (density included). Concepts and commands: omit if unnamed by this crawl.
5. Emit Output. Do not write the lantern to disk.

## Script

From the skill root directory, run:

```bash
python3 <skill-root>/scripts/discover.py --target <absolute_workspace_root> --budget <budget>
```

- Always pass an absolute workspace to `--target`. Never use `--target .`
- Stdout: flat seed paths, one `./rel` path per line. No section headers.

### Script policy

- Script stdout is the seed observation floor; the Scry Lantern is agent-composed from reads. Scripts supply bounded evidence, not conclusions.
- **Prefer** `scripts/discover.py` for the seed list (do not skip the script and freestyle discovery).
- **Re-run** with reasoned `--budget` (or other supported flags) when stdout is empty, at budget, or mismatched to the ask. Briefly note what changed vs the prior run.
- **Read-only** - do not edit script files in-session; read the script only to understand behavior.
- **Supplement** only after at least one script run (re-run when params might help). Keep supplements bounded; merge into an explicit Seed set before reads. Note in chat when any seed path came from outside script stdout (one line is enough).

## Discovery

The script implements this contract:

**Prune** - skip any path with a segment in this closed set:

`.git`, `node_modules`, `vendor`, `.venv`, `venv`, `__pycache__`, `.pnpm-store`, `.yarn`, `dist`, `build`, `_site`, `.next`, `.nuxt`, `target`, `coverage`, `.turbo`

**Seed basenames** (case-insensitive match on file basename):

`readme`, `readme.*`, `agents.md`, `agents*.md`, `claude.md`, `skill.md`, `index`, `index.md`, `index.yaml`, `index.yml`, `index.json`

**Ranking** - dedupe by realpath; sort shallow-first `(depth, path)`; cap at `budget`.

**Closed read boundary** - after the Seed set is fixed, no ad-hoc seed expansion except supplement per Script policy. Reads stay within the closed Seed set.

Discovery does not honor `.gitignore` unless the user asks otherwise.

## Output

North star: at-a-glance. Every section stays tight and high-level.

| Part | Required | Holds |
| --- | --- | --- |
| Title + one-line distillation | yes | Outside fence: `# Grim Scry: <project>` and one line |
| Scry Lantern | yes | `text` fence: tree only |
| `# Summary` | yes | One short paragraph; high-level shape only |
| `Observations:` | yes | ≤3 `-` bullets; high-signal only |

### Scry Lantern

Ideas first. Implementers hung underneath concepts. Hang named commands under their concept (`▶`). Annotate with `ⓘ` only when seeds named purpose - do not invent.

Rules:

- Prefer vertical trees; largest concepts win.
- One required `ⓘ` annotation under workspace header, before divider.
- Moderate use of annotation in concept trees; ideas not captured in tree.
- Use `≣` for concept group trunks.
- Use `▶` for execution branches - primary named commands only.

Style:

- Hierarchy branch glyphs: `│`, `├─`, `└─`.
- Annotation glyphs: `├─ⓘ`, `└─ⓘ`, `─ⓘ`.
- Concept glyphs: `├─≣`, `└─≣`, `─≣`.
- Command glyphs: `├─▶`, `└─▶`, `─▶`.
- Divider glyph: `╞══════════════════◆`.
- Indent each level; continue ancestors with `│`.
- `├─` / `├─ⓘ` / `├─≣` / `├─▶` non-final sibling;
- `└─` / `└─ⓘ` / `└─≣` / `└─▶` final sibling.

Rules above are authoritative; below is drawing guide only.

```text
workspace/
├─ⓘ Example golang api surface
╞══════════════════◆
│
├─≣ Runtime
│  ├─ⓘ Runtime notes
│  ├─ⓘ Other complexities
│  ├─ server/
│  └─ client/
│
├─≣ Packages
│  └─ packages/core/
│     └─ⓘ Main library
│
├─≣ Quality
│  ├─▶ npm audit
│  │  └─ⓘ full repo audit
│  └─▶ npm test
│
├─≣ Docs
│  ├─ docs/README.md
│  └─▶ npm run docs
│
└─≣ Guidance
   └─ AGENTS.md
      └─ⓘ Agent source of truth
```

## Usage

Call `/grim-scry` with a target or infer the current workspace.

```text
/grim-scry packages/api/
/grim-scry .
/grim-scry
/grim-scry https://github.com/example/repo
```

## Boundaries

- Session-only viewport; no disk artifacts.
- Do not read outside the Seed set after Discovery closes.
