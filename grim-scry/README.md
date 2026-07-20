# grim-scry

_Reveal the shape of a system._

Given a repository or workspace, distill a small canonical model and show it through three at-a-glance ASCII lenses.

## What it does

1. Discovers layout from top-level dirs + README / `AGENTS.md` / manifests (not deep code archaeology).
2. Writes `workspace_data` to `<agent-workspace>/.grimoire/scry/<slug>/model.yaml`.
3. Emits chat-facing output:
   - Directory hierarchy
   - Conceptual hierarchy
   - Workflow hierarchy
   - `repository.summary` + short `observations`
   - Link to the written `model.yaml`

Knowledge first -> viewport second. The YAML is the source of truth; ASCII is a projection.

## Files

| File | Role |
| --- | --- |
| [SKILL.md](SKILL.md) | Executable skill instructions |
| [ascii-viewport.md](ascii-viewport.md) | ASCII rendering contract for the three lenses |
