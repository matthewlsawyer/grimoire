---
name: grim-scry
description: >-
    Given a repository or workspace, produce a simple canonical understanding.
---

# Scry

_Reveal the shape of a system._

## Workflow

Default depth `N = 3`.
Default seed read budget `K = 20`.
Default dir width `W = 25`.

1. Resolve target (cwd / named repo; ask if unclear)
2. Run discovery script (see Scripts) with absolute `--target`, `--depth N`, `--budget K`, `--dir-width W`. Use stdout as the inventory snapshot. Do not write inventory to disk.
3. From discover stdout:
   - Use `## dirs` for Directory lens structure (mute folders may still appear). Group by parent; preserve script sibling order (do not reorder for salience).
   - Read **only** the paths under `## seeds` (already ranked and capped). Leave any other seeds unread.
   - Skip unreadable seed paths; omit rather than invent. Optional short Observation if several miss.
   - Extract meaning from what was read. Annotate directory purpose only when docs named it - do not invent purposes.
   - Concepts / scripts / instructions / configs: if a candidate cannot be named from this crawl, omit it.
   - No follow-up discovery after the script. Do not re-`find` in-session.
4. Distill -> small salient set only (cap what you keep, not shell commands):
   - Fast: prefer fewer nodes, short purposes/notes; omit rather than verify.
   - Directory tree may be fuller than concepts/workflows; emit at-a-glance depth.
   - Prefer unlabeled nodes. Annotate only when the label alone would mislead. Per-lens budgets: see Lenses.
   - Always distill in-session from the inventory snapshot. Do not write distilled lenses to disk.
5. Emit per Output below.

## Scripts

```text
scripts/discover.py
```

```bash
python3 scripts/discover.py --target <spell-target-abs> --depth 3 --budget 20 --dir-width 25
```

- Always pass an absolute `--target` (the resolved spell target). Never use `--target .` when invoking from the skill directory - `.` means the skill package, not the workspace.
- Stdout sections (closed set): `## dirs` then `## seeds`. Dirs keep trailing `/`; seeds are files.
- Pipeline: list paths once -> split. Dirs: depth `N` + fan-out `W`. Seeds: basename filter -> rank -> budget `K` (not depth-truncated).
- Git target: `git ls-files --cached --others --exclude-standard` (ignore free). No-git: plain `os.walk` (no deny list; prune `.git` basename; skip symlinks).
- Script lists only. Agent reads seed file contents; script does not distill or write inventory to disk.

## Output

1. Emit the three lenses (see Lenses) as ASCII trees (see ASCII), with distillation.
  - `# Lense` (e.g. "Directory hierarchy").
  - Distillation - Short description/distillation from this section.
  - Text fenced ASCII tree.
2. Divider `---`
3. Surface a short Summary and Observations.
  - `# Summary` followed by `[summary]`
  - "Observations:" followed by list `- [observation]`

## Constraints

- Discovery is script-owned (`scripts/discover.py`) every run. No inventory cache. No in-session `find`. No deep code intelligence.
- Seed *listing* may span the whole target (not depth-capped); seed *reads* are the ranked `## seeds` list capped by budget `K`. Cap reads and dir emit (`N`, `W`), not seed hunt.
- Seeds only - no follow-up discovery after the script.
- Git: honor ignore via `ls-files --exclude-standard`. Always prune `.git` by basename. Avoids symlinks.
- Absolute `--target` required when invoking from the skill directory.
- Do not write inventory, distilled lenses, or a model file to disk.
- Do not invent directory purposes for reveal-only dirs.
- Observations are short bullets, not a second essay.
- README files are not instruction, they are evidence-only.
- Keep the three lenses distinct (filesystem vs ideas vs run). No lens bleed.
- Omit rather than invent. Prefer salience over completeness.

---

## Lenses

Three named views. Agent chooses tree shape; lens intent is the constraint.

### Directory hierarchy

Filesystem structure. Group `## dirs` by parent; preserve discovery sibling order. Annotate purpose only when docs named it - do not invent.

Prefer legibility over density; annotate important directories.

### Conceptual hierarchy

Ideas first. Implementers and containers hung underneath concepts.

Prefer legibility over density; annotate roots / forks / non-obvious mappings.

### Workflow hierarchy

Named flows. Commands and entrypoints grouped by purpose.

Prefer legibility over density; annotate commands, complexity / non-obvious purpose.

---

## ASCII

Glyphs:

| Role | Glyphs |
| --- | --- |
| Hierarchy branches | `│`, `├─`, `└─` |
| Workflow / invocation | `├─▶`, `└─▶`, `─▶` |
| Annotation / directionality | `◀─`, `─▶` |

Rules:

- Emit each lens in a `text` fence.
- Prefer vertical, at-a-glance trees over dense graphs.
- Labels are short; optional annotations use `◀─ <terse note>` (≤ ~8 words). Prefer omit.
- In annotations, use `─▶` for infix direction (`a ─▶ b`).
- Indent each level; continue ancestors with `│` (three-column gutters).
- `├─` for a non-final sibling; `└─` for the final sibling.
- If a cycle appears, break it for rendering; do not loop forever.
- If a node has multiple parents, choose one primary parent for the tree.
- Treat below examples as north stars, not rigid templates. North stars may be denser than the annotation budget - follow the budget on emit.

### Directory hierarchy - north star

```text
next.js/
├─ packages/ ◀─ Published npm packages (pnpm workspace)
│  ├─ next/ ◀─ Main framework; published as `next`
│  ├─ create-next-app/
│  ├─ next-swc/
│  ├─ eslint-plugin-next/
│  ├─ font/
│  ├─ third-parties/
│  └─ ...
├─ turbopack/ ◀─ Turbopack bundler (Rust); git subtree
│  ├─ crates/
│  ├─ benchmark-apps/
│  └─ packages/
├─ crates/ ◀─ Rust crates for Next.js SWC bindings
│  ├─ next-core/
│  ├─ next-api/
│  ├─ next-custom-transforms/
│  ├─ next-napi-bindings/
│  └─ ...
├─ rspack/
├─ test/ ◀─ All test suites
│  ├─ unit/
│  ├─ development/
│  ├─ production/
│  ├─ e2e/
│  └─ examples/
├─ examples/ ◀─ Example Next.js applications
├─ docs/
│  ├─ 01-app/
│  ├─ 02-pages/
│  ├─ 03-architecture/
│  └─ 04-community/
├─ scripts/ ◀─ Build and maintenance scripts
├─ bench/
├─ evals/ ◀─ Agent evals for Next.js
├─ apps/
│  └─ bundle-analyzer/ ◀─ Vendored into `next` at build
├─ skills/
├─ .agents/
│  └─ skills/
├─ .github/
├─ .conductor/ ◀─ Conductor parallel-agent worktree config
├─ turbo/
├─ contributing/
├─ errors/
└─ AGENTS.md / CLAUDE.md
```

### Conceptual hierarchy - north star

```text
Next.js framework ◀─ `packages/next`; `src/` ─▶ `dist/`
├─ CLI entrypoints
│  ├─ next dev ─▶ `src/cli/next-dev.ts` ─▶ dev server
│  ├─ next start ─▶ `src/cli/next-start.ts` ─▶ production server
│  └─ next build ─▶ `src/cli/next-build.ts` ─▶ build pipeline
├─ Runtime layers
│  ├─ server/ ◀─ Most runtime changes
│  ├─ client/
│  └─ build/
├─ Bundler stack ◀─ Turbopack default; webpack and rspack selectable
│  ├─ turbopack/ ◀─ General-purpose bundler; Next-agnostic inside subtree
│  ├─ packages/next/ ◀─ Translates Next config ─▶ Turbopack options
│  ├─ rspack/
│  └─ packages/next-rspack/
├─ Native / SWC layer
│  ├─ packages/next-swc/
│  └─ crates/
├─ Scaffolding and lint
│  ├─ create-next-app/
│  ├─ eslint-plugin-next/
│  └─ font/ / third-parties/
├─ Documentation ◀─ `docs/` bundled into package `dist/docs/`
├─ Agent guidance
│  ├─ AGENTS.md ◀─ Always-loaded dev guide
│  └─ .agents/skills/ ◀─ On-demand deep workflows
├─ Quality gates
│  ├─ test/ ◀─ unit, development, production, e2e
│  └─ evals/ ◀─ Sandbox agent evals vs bundled docs
└─ Bundle analysis UI
   └─ apps/bundle-analyzer/ ─▶ vendored into `next` build
```

### Workflow hierarchy - north star

```text
next.js
├─ Bootstrap / build
│  ├─▶ pnpm install
│  ├─▶ pnpm build ◀─ JS via Turborepo
│  ├─▶ pnpm build-all ◀─ JS + Rust; after branch switch
│  └─▶ pnpm --filter=next build ◀─ Core package only
├─ Local iteration
│  ├─▶ pnpm --filter=next dev ◀─ Watch rebuild (~1-2s/change)
│  └─▶ pnpm --filter=next types ◀─ Fast type check (~10s)
├─ CLI (end user)
│  ├─▶ next dev
│  ├─▶ next build
│  ├─▶ next start
│  ├─▶ next dev --webpack
│  └─▶ next build --webpack
├─ Integration tests ◀─ Mode x bundler matrix
│  ├─▶ pnpm test-dev-turbo ◀─ Dev + Turbopack (default)
│  ├─▶ pnpm test-dev-webpack
│  ├─▶ pnpm test-start-turbo ◀─ Prod build+start + Turbopack
│  ├─▶ pnpm test-start-webpack
│  ├─▶ pnpm test-dev-rspack / pnpm test-start-rspack
│  └─▶ pnpm test-unit ◀─ Fast; no browser
├─ Test authoring
│  └─▶ pnpm new-test -- --args <appDir> <name> <type>
├─ Quality
│  ├─▶ pnpm lint
│  ├─▶ pnpm lint-fix
│  └─▶ pnpm types
├─ PR / CI triage
│  └─▶ node scripts/pr-status.js
│      └─▶ .agents/skills/pr-status-triage/SKILL.md
├─ Agent evals
│  └─▶ pnpm eval <agent-NNN-name>
│      └─▶ run-evals.js ─▶ @vercel/agent-eval
├─ Parallel agents (Conductor)
│  ├─▶ .conductor/scripts/setup.sh
│  └─▶ .conductor/scripts/run.sh ─▶ pnpm --filter=next dev
└─ Primary instruction
   └─▶ AGENTS.md
```
