# grim-scry

_Reveal the shape of a system._

Given a repository or workspace, distill a small canonical model and show it through three at-a-glance ASCII lenses.

## What it does

1. Dir reveal: `find -P . -mindepth 1 -maxdepth 3 -type d` for structure (first pass). Honors `.gitignore`; skips `.git`, plumbing, vendor, and generated paths. Avoids symlinks.
2. Doc seed: hunt README / `AGENTS.md` / index files on the revealed dirs only; read seeds and extract meaning. No SKILL/workflow/source follow-ups.
3. Writes `workspace_data` to `<agent-workspace>/.grimoire/scry/<slug>/model.yaml`.
4. Emits chat-facing output:
   - Directory hierarchy
   - Conceptual hierarchy
   - Workflow hierarchy
   - Summary + observations
   - Link to the written `model.yaml`

Knowledge first -> viewport second. The YAML is the source of truth; the ASCII viewport is the projection.

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

Every entity requires an `id`, `kind`, and `name`. The remaining fields depend on the kind - for example, directories use `path`, concepts use `description`, and scripts use `command`.

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
| Conceptual | `concept` plus linked implementers | `contains`, `implements` | Ideas, their sub-concepts, and concrete realizations |
| Workflow | `entrypoint`, `script`, `instruction` | `invokes`, `uses`, `depends_on` | Actions, guidance surfaces, and execution/dependency flow |

The same entity can appear in more than one lens when its kind and edges qualify. For example, a directory can implement a concept in the conceptual lens, while a script can be invoked by an entrypoint in the workflow lens. `config` entities are available to a lens when linked, but are not required in every viewport.

## Core Architecture

```text
Target workspace
└─▶ Discovery & Distillation
    └─▶ Canonical Model -▶ `<agent-workspace>/.grimoire/scry/<slug>/model.yaml`
        ├─▶ ASCII (default)
        ├─▶ Plaintext
        ├─▶ Markdown
        ├─▶ Mermaid
        ├─▶ GraphViz
        └─▶ Future renderers...
```

## Files

| File | Role |
| --- | --- |
| [SKILL.md](SKILL.md) | Executable skill instructions |
| [viewport-ascii.md](viewport-ascii.md) | ASCII rendering contract |
| [schema.yaml](schema.yaml) | Canonical entity and relationship schema |
