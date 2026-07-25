# grim-scry

_You must see before you act._

Given a repository or workspace, distill meaning and emit one at-a-glance Scry Lantern in chat.

## Shape

1. Resolve the target.
2. Discover a closed seed set (session-only).
3. Read only those seeds; distill for salience. Annotate purpose only when docs named it.
4. Emit:
  - Scry Lantern (one tree: concepts, paths, commands)
  - Summary + observations

Viewport is the spell. Ideas hang first; implementers and named commands hang underneath.

Inventory and lantern stay session-only.

## Usage

Call `/grim-scry` with a target (local or remote) or let it infer the current workspace.

```text
# specific project
/grim-scry projects/site/

# workspace
/grim-scry .

# inferred workspace
/grim-scry

# remote repository
/grim-scry https://github.com/basecamp/omarchy
```

## Scripts

| File | Role |
| --- | --- |
| [scripts/discover.py](scripts/discover.py) | Deterministic seed listing |
