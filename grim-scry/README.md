# grim-scry

_Reveal the shape of a system._

Given a repository or workspace, distill a small canonical model and show it through three at-a-glance ASCII lenses.

## What it does

1. Resolve target (cwd or named path).
2. Dir reveal (structure): `find -P . -mindepth 1 -maxdepth "$N"` (default `N = 3`). Honors `.gitignore`; skips `.git`, plumbing, vendor, and generated paths. Avoids symlinks.
3. Doc seed extract (meaning): among the target root and dirs already revealed, hunt README, `AGENTS.md` / `CLAUDE.md`, rules (e.g. `rule-name.mdc`), and index files (`index.md`, `index.yaml`, or similar) only. Read seeds; extract meaning. No follow-up discovery.
4. Distill to a small salient set. Set `directory.purpose` only when docs named it.
5. Write `workspace_data` to `<agent-workspace>/.grimoire/scry/<slug>/model.yaml`.
6. Emit chat-facing output:
   - Directory hierarchy
   - Conceptual hierarchy
   - Workflow hierarchy
   - Summary + observations
   - Link to the written `model.yaml`

Knowledge first -> viewport second. The YAML is the source of truth; the ASCII viewport is the projection.

Same-slug re-run: `rm -rf` the whole `.grimoire/scry/<slug>/` dir, then recreate and write `model.yaml`. Do not patch or merge prior runs.

## Model vocabulary

`workspace_data` has two graph primitives: entities are nodes; relationships are directed edges. The schema is closed, so every node and edge uses one of the kinds or types below.

### Entity kinds

| Kind | Represents | Typical hierarchy use |
| --- | --- | --- |
| `directory` | A filesystem directory in the revealed tree | Directory hierarchy nodes; may implement a concept |
| `concept` | A named system idea or boundary | Conceptual hierarchy parent; may contain other concepts |
| `entrypoint` | A user- or agent-facing entry into a workflow | Workflow hierarchy root or starting node |
| `script` | An executable command or operational action | Workflow hierarchy action node |
| `config` | A named configuration artifact | Conceptual or workflow implementer when linked |
| `instruction` | An instruction or guidance surface | Workflow hierarchy API surface |

Every entity requires an `id`, `kind`, and `name`. The remaining fields depend on the kind - for example, directories use `path` and optional `purpose`, concepts use `description`, and scripts use `command`.

### Relationship types

| Type | Meaning | Direction |
| --- | --- | --- |
| `contains` | The source groups, owns, or structurally includes the target | container -> member |
| `implements` | The source is a concrete realization of the target | implementer -> concept |
| `invokes` | The source starts or calls the target workflow | caller -> callee |
| `uses` | The source relies on or consults the target | user -> dependency |
| `depends_on` | The source cannot complete without the target | dependent -> prerequisite |

Relationships are directional. Do not infer the reverse edge: `A depends_on B` does not mean `B depends_on A`.

### How lenses use the vocabulary

Lenses are filters over the same model, not separate graphs. Each hierarchy chooses the entity kinds and relationship types that best expose its question:

| Lens | Entity filter | Relationship filter | Shows |
| --- | --- | --- | --- |
| Directory | `directory` | `contains` | Filesystem structure and documented directory purpose |
| Conceptual | `concept`, `directory` (via `implements`) | `uses`, `invokes`, `implements` | Ideas, linked implementers, and concept flow |
| Workflow | `script`, `concept`, `entrypoint`, `instruction` | `uses`, `invokes`, `contains`, `implements`, `depends_on` | Actions, guidance surfaces, and execution/dependency flow |

The same entity can appear in more than one lens when its kind and edges qualify. For example, a directory can implement a concept in the conceptual lens, while a script can be invoked by an entrypoint in the workflow lens. `config` entities are available to a lens when linked, but are not required in every viewport.

## Core Architecture

```text
Target workspace
└─▶ Discovery (dir reveal + doc seed)
    └─▶ model.yaml  ◀─ <agent-workspace>/.grimoire/scry/<slug>/
        ├─▶ ASCII (default)
        ├─▶ Plaintext
        ├─▶ Markdown
        ├─▶ Mermaid
        ├─▶ GraphViz
        └─▶ Future renderers...
```

Additional viewports (Markdown, Mermaid, GraphViz, ...) are planned; only ASCII is shipped today.

## Files

| File | Role |
| --- | --- |
| [SKILL.md](SKILL.md) | Executable skill instructions |
| [viewport-ascii.md](viewport-ascii.md) | ASCII rendering contract |
| [schema.yaml](schema.yaml) | Canonical entity and relationship schema |
