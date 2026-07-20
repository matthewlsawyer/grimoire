---
name: grim-scry
description: >-
    Given a repository or workspace, produce a simple canonical understanding.
---

# Scry

_Reveal the shape of a system._

## Workflow

1. Resolve target (cwd / named repo; ask if unclear)
2. Discover in **one** shell pass:
   - `ls` top-level (honor `.gitignore`; skip plumbing / vendor / generated)
   - Read README (and `AGENTS.md` / `package.json` / index / equivalent manifest if present)
   - Discover instruction surfaces: `SKILL.md` and automation such as `.github/workflows/*`
   - Do not deep-read files unless a concept cannot be named from those sources
3. Distill -> small salient set only (see Constraints caps)
4. Write workspace_data (see Artifact path)
5. Emit per Output below

## Artifact path

```text
<agent-workspace>/.grimoire/scry/<slug>/
├─ model.yaml   # scry writes this
└─ ascii.md     # reserved sibling viewport; not written by scry yet
```

- Agent workspace root, not the target repo.
- `slug`: target path relative to agent workspace; strip trailing `/`; replace `/` with `-`.
  - `projects/next.js` -> `projects-next.js`
  - `knowledge` -> `knowledge`
  - workspace root (`.`) -> repository `name`
- Same-slug re-run: `rm -rf` the whole `.grimoire/scry/<slug>/` dir, then recreate and write `model.yaml`.
- Do not patch, merge, or leave prior siblings. Stale viewport files are worse than missing ones.

## Output

1. Emit the three lenses (see Lenses) as ASCII viewports (default for now; chat only - do not write `ascii.md` yet).
2. Return a link to the `model.yaml` path written.
3. Surface `repository.summary` and `observations`.

Do not re-embed the whole model in chat unless asked.

## Constraints

- Prefer directory layout + README + AGENTS over deep code intelligence.
- Ignore plumbing, boilerplate, generated, and vendor paths.
- Observations are short bullets, not a second essay.

---

## Schema

workspace_data = `<agent-workspace>/.grimoire/scry/<slug>/model.yaml`

Closed sets and required fields for workspace_data.

```yaml
# required top-level keys
version: 1                    # required; integer
repository:                   # required
  name: string                # required
  root: string                # required; usually "."
  summary: string             # required; one short paragraph
entities: []                  # required; may be empty only if truly barren
relationships: []             # required
evidence: []                  # optional; may be empty
observations: []              # required; short bullets; capped

# entity — required fields by kind
# id: string                  # required; stable, namespaced (dir.*, concept.*, ...)
# kind: enum                  # required; closed set below
# name: string                # required
#
# kind: directory
#   path: string              # required
#   purpose: string           # required; terse
#
# kind: concept
#   description: string       # required; terse
#
# kind: entrypoint
#   path: string              # required
#
# kind: script
#   command: string           # required
#
# kind: config
#   path: string              # required
#
# kind: instruction
#   path: string              # required; AGENTS.md, SKILL.md, workflow, or equivalent

# kind — closed
# directory | concept | entrypoint | script | config | instruction

# relationship — required fields
# type: enum                  # required; closed set below
# from: string                # required; entity id or "repository"
# to: string                  # required; entity id

# type — closed
# contains | implements | invokes | uses | depends_on

# evidence — optional; use when a citation helps, skip when it doesn't
# - entity: <id>
#   sources: [path, ...]
# - relationship:
#     type: <type>
#     from: <id>
#     to: <id>
#   sources: [path, ...]
```

---

## Lenses

Named projections over workspace_data. Each lens selects entities and relationships; viewports (ASCII, later others) only draw what the lens admits.

### Directory hierarchy

Filter the workspace_data for:
- entity `kind: directory` -> short `purpose`
- relationship `type: contains`

Prefer:
- no annotation on root (1) dir
- purpose annotations on next level (2) dirs
- no annotation on nested (3+) dirs

### Conceptual hierarchy

Filter the workspace_data for:
- entity `kind: concept`
- relationship `type: contains` + `type: implements`

### Workflow hierarchy

Filter the workspace_data for:
- entity `kind: entrypoint` + `kind: script` + `kind: instruction`
- relationship `type: invokes` + `type: uses` + `type: depends_on` + `type: contains`

Include as an API surface:
- agent instructions -> include `AGENTS.md`, `SKILL.md`
- repository automations -> workflow files e.g. `.github/workflows/*.yaml`

---

## ASCII Viewport

Read [`ascii-viewport.md`](ascii-viewport.md) before emitting the default ASCII viewports.
Treat that file as the descriptive rendering contract only.
