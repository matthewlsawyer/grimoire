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
root/ ◀─ short note
├─ foo1/ ◀─ short note
├─ foo2/
│  ├─ bar1/
│  └─ bar2/
└─ foo3/
   └─ bar1/
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

Example:

```text
Foo ◀─ short note
└─ Bar ◀─ short note
  ├─ bar/
  └─ Baz ◀─ short note
     └─ bar/baz/

Qux
└─ Quux ◀─ short note

Scorge
├─ sponge/
└─ Spangle ◀─ short note
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

Example:

```text
CLI
├─▶ foo --cli ◀─ short note
└─▶ bar.sh

Local development
├─▶ foo ◀─ short note
│  ├─▶ foo.sh
│  └─▶ foo pr ◀─ PR triage
└─▶ bar build
   └─▶ bar build-all

Testing ◀─ short note
├─▶ baz test-e2e
└─▶ baz test-unit

Specialized instructions
├─ .github/build.md ◀─ short note
├─ qux/qux.md
└─ AGENTS.md ◀─ primary instruction
```

## Output constraints

- Emit one ASCII block, `text` fenced, per lens unless the user asks for a subset.
