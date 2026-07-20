# ASCII Viewport

Descriptive rendering contract for the three current lenses.

## Purpose

Render the selected lens from `workspace_data` as compact UTF-8 ASCII.
The YAML remains the source of truth. This file defines how ASCII draws what the lens admits.

## Global drawing contract

Charset: `┌ ┐ └ ┘ ─ │ ┬ ┴ ├ ┤ ┼ ▲ ▼ ◀ ▶`

Also use tree markers and flow arrows:

- Hierarchy branches: `├─ └─ │`
- Workflow flow: `▶` and `->`

Rules:

1. Draw only entities and relationships admitted by the active lens.
2. Prefer vertical, at-a-glance trees over dense graphs.
3. Labels are short; optional annotations use `-> <terse note>`.
4. If a node has multiple parents, pick one primary parent for the tree; note other parents in an annotation only when necessary.
5. If a cycle appears, break it for rendering; do not loop forever.
6. Omit disconnected nodes unless they are entrypoints, scripts, or instructions that still belong in the workflow surface.
7. Prefer one primary root when possible (`repository.name`, a concept root, or the main entrypoint/instruction).
8. Do not invent nodes or edges that are not in `workspace_data`.

## Directory lens renderer

Admits:

- entities: `kind: directory`
- relationships: `type: contains`

Mapping:

- Parent/child edges come from `contains`.
- Root label is usually `repository.name/` with optional `->` purpose/summary fragment.
- Directory label is `name` with a trailing `/`.
- Annotation comes from `purpose` as `-> <purpose>`.
- Prefer purpose annotations on rendered dirs when `purpose` is present.
- Omit directories with no `contains` path from the rendered root.
- Prefer filesystem order that matches the distilled model; do not expand ignored/plumbing paths.

## Conceptual lens renderer

Admits:

- entities: `kind: concept` (and directory/config implementers when linked)
- relationships: `type: contains` + `type: implements`

Mapping:

- Concepts are the primary parents.
- `implements` edges place implementers under concepts.
- `contains` edges nest concepts under concepts when present.
- Concept label is `name`.
- Annotation comes from `description` as `-> <description>`.
- Implementer labels may be directory names with `/` when they are directories.
- Prefer concept-first trees over filesystem trees.
- If concepts do not form a single tree, render sibling concept roots under the repository/system name.

## Workflow lens renderer

Admits:

- entities: `kind: entrypoint` + `kind: script` + `kind: instruction`
- relationships: `type: invokes` + `type: uses` + `type: depends_on` + `type: contains`

Mapping:

- Nodes are entrypoints, scripts, and instructions.
- Edges come from `invokes`, `uses`, `depends_on`, and workflow-relevant `contains`.
- Instruction files are API surfaces, not shell commands.
- Script label prefers `command` text when available; otherwise `name`.
- Entrypoint label prefers basename/`name` or `path`.
- Instruction label prefers basename or skill name; may annotate with `path`.
- Use flow form (`├─▶` / `└─▶`) for invocation and dependency direction.
- Standalone scripts may appear as sibling roots when not reached from an entrypoint/instruction.
- Keep related flows grouped; avoid one giant entangled tree when several independent pipelines exist.

## Output constraints

- Emit one ASCII block per lens unless the user asks for a subset.
