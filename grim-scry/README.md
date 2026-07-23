# grim-scry

_Reveal the shape of a system._

Given a repository or workspace, distill meaning and emit three at-a-glance ASCII lenses in chat.

## Shape

1. Resolve the target.
2. Reveal structure (shallow directory pass).
3. Hunt seeds for meaning (docs / agents / rules / indexes; read budgeted).
4. Distill to a small salient set. Annotate purpose only when docs named it.
5. Emit in chat only - no model file on disk:
   - Directory hierarchy
   - Conceptual hierarchy
   - Workflow hierarchy
   - Summary + observations

Viewport is the spell. Agent holds shape in-session and chooses tree form; glyphs and lens intents constrain the render.

## Lenses

| Lens | Intent |
| --- | --- |
| Directory | Filesystem structure; purpose only when docs earned it |
| Conceptual | Ideas first; implementers/containers under concepts |
| Workflow | Named flows; commands/entrypoints; invocations |

Keep lenses distinct. Omit rather than invent.
