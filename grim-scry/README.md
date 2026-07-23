# grim-scry

_Reveal the shape of a system._

Given a repository or workspace, distill meaning and emit three at-a-glance ASCII lenses in chat.

## Shape

1. Resolve the target.
2. Run `scripts/discover.py` every time (absolute `--target`; depth `N`, seed budget `K`, dir width `W`). Use stdout as the inventory snapshot - do not write it to disk.
3. From stdout: read only the listed seeds; distill to a small salient set. Annotate purpose only when docs named it. Always distill in chat - do not write lenses to disk.
4. Emit:
   - Directory hierarchy
   - Conceptual hierarchy
   - Workflow hierarchy
   - Summary + observations

Viewport is the spell. Agent chooses tree form; glyphs and lens intents constrain the render. Inventory is session-only stdout; lenses are session-only.

## Scripts

| File | Role |
| --- | --- |
| [scripts/discover.py](scripts/discover.py) | Deterministic `## dirs` + `## seeds` discovery |

## Lenses

| Lens | Intent |
| --- | --- |
| Directory | Filesystem structure; purpose only when docs earned it |
| Conceptual | Ideas first; implementers/containers under concepts |
| Workflow | Named flows; commands/entrypoints; invocations |

Keep lenses distinct. Omit rather than invent.
