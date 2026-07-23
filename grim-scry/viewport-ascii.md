# ASCII Viewport

Descriptive rendering contract for the three current lenses.

## Purpose

Render the selected lens from `workspace_data` as compact UTF-8 tree text.
The YAML remains the source of truth. This file defines how ASCII draws what the lens admits.

## Global drawing contract

Glyphs:

| Role | Glyphs |
| --- | --- |
| Hierarchy branches | `│`, `├─`, `└─` |
| Workflow / invocation | `├─▶`, `└─▶`, `─▶` |
| Annotation | `◀─` |

Rules:

- Emit each lens in a `text` fence.
- Draw only entities and relationships admitted by the active lens.
- Prefer vertical, at-a-glance trees over dense graphs.
- Labels are short; optional annotations use `◀─ <terse note>`.
- Indent each level; continue ancestors with `│` (three-column gutters).
- `├─` for a non-final sibling; `└─` for the final sibling.
- If a cycle appears, break it for rendering; do not loop forever.
- If a node has multiple parents, choose one primary parent for the tree.
- Do not invent nodes or edges that are not in `workspace_data`.
- Treat below examples as north stars.

## Directory lens renderer

Admits:

- entities: `kind: directory`
- relationships: `type: contains`

Mapping:

- One primary root: `repository.name`.
- Parent/child edges come from `contains`.
- Root label is usually `repository.name/` with optional `◀─` purpose/summary fragment.
- Directory label is `name` with a trailing `/`.
- Annotation comes from `purpose` as `◀─ <purpose>`.
- Prefer purpose annotations on rendered dirs when `purpose` is present.
- Prefer filesystem order that matches the distilled model; do not expand ignored/plumbing paths.

Example:

```text
next.js/ ◀─ Next.js React framework
├─ packages/ ◀─ Published npm packages (core `next` and siblings)
│  └─ next/
├─ turbopack/ ◀─ Turbopack bundler (Rust) subtree
├─ crates/ ◀─ Rust crates for Next.js SWC bindings
├─ rspack/
├─ test/ ◀─ All test suites
│  ├─ e2e/
│  ├─ development/
│  ├─ production/
│  └─ unit/
├─ examples/ ◀─ Example Next.js applications
├─ docs/ ◀─ Documentation
│  ├─ 01-app/
│  ├─ 02-pages/
│  ├─ 03-architecture/
│  └─ 04-community/
├─ scripts/ ◀─ Build and maintenance scripts
└─ evals/ ◀─ Agent evals for Next.js
```

## Conceptual lens renderer

Admits:

- entities:
  - `kind: concept`
  - `kind: directory` - when linked via `implements`
- relationships:
  - `type: uses`
  - `type: contains`
  - `type: implements`

Mapping:

- Concepts are the primary parents.
- `implements` and `uses` edges are placed under concepts.
- `contains` edges nest concepts under concepts when present.
- Concept label is `name`.
- Annotation comes from `description` as `◀─ <description>`.
- Implementer labels may be `path` when they are directories.
- Prefer concept-first trees over filesystem trees.
- If concepts do not form a single tree, render sibling concept roots under the repository/system name.

Example:

```text
Next.js framework ◀─ Main next npm package; dev, build, and production server
├─ packages/next/
├─ Bundler tooling ◀─ Turbopack default; Webpack and Rspack still selectable
│  ├─ turbopack/
│  └─ rspack/
├─ Native / SWC layer ◀─ Rust crates and NAPI bindings behind transforms
|  ├─ packages/next-swc/
|  └─ crates/
└─ Dev / build / test loop -> Watch build, mode-specific tests, full bootstrap builds
   ├─ scripts/
   └─ test/
```

## Workflow lens renderer

Admits:

- entities:
  - `kind: script`
  - `kind: concept` - via `invokes`, `uses`
  - `kind: entrypoint`
  - `kind: instruction`
- relationships:
  - `type: uses`
  - `type: invokes`
  - `type: contains`
  - `type: implements`
  - `type: depends_on`

Mapping:

- Nodes are entrypoints, scripts, and instructions.
- Edges come from `invokes`, `uses`, `depends_on`, and workflow-relevant `contains`.
- Script label prefers `command` text when available; otherwise `name`.
- Prefer to group related flows by usage/domain/purpose of the invocations therein -> named workflows.
- Use `├─▶` / `└─▶` / `─▶` for invocation and dependency direction.
- Use `◀─` for notes for invocation and dependency direction.
- If nodes do not form a single tree, render sibling workflow roots under `repository.name`.

Example:

```text
next.js
├─ CLI
│  ├─▶ next dev
│  ├─▶ next start
│  └─▶ next build
├─ Local development
│  ├─▶ pnpm --filter=next dev ◀─ watch rebuild while iterating
│  └─▶ pnpm --filter=next build ◀─ core package only
├─ Build
│  ├─▶ pnpm build
│  └─▶ pnpm build-all ◀─ JS and Rust; use after branch switch
├─ Testing ◀─ mode- and bundler-specific
│  ├─▶ pnpm test-dev-turbo ◀─ dev mode, Turbopack (default)
│  │   └─▶ pnpm --filter=next build
│  ├─▶ pnpm test-dev-webpack
│  ├─▶ pnpm test-start-turbo ◀─ prod build+start
│  │   └─▶ pnpm --filter=next build
│  ├─▶ pnpm test-start-webpack
│  ├─▶ pnpm test-unit ◀─ fast, no browser
│  └─▶ pnpm new-test ◀─ generate test fixtures
├─ Quality
│  ├─▶ pnpm lint
│  └─▶ pnpm types
├─ PR triage
│  └─▶ node scripts/pr-status.js
│      └─▶ .agents/skills/pr-status-triage/SKILL.md ◀─ CI failure workflow
└─ Specialized instructions
   └─▶ AGENTS.md ◀─ primary instruction
```

## Output constraints

- Emit one ASCII block, `text` fenced, per lens unless the user asks for a subset.
