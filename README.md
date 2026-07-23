# grimoire

```text
╭───────────────╮
│  ◈ grimoire   ║
│  ══✧═════✧══  ║
│               ║
|  / ~≃> cast   ║
│               ║
│  ────┬┼┬────  ║
│     ✧ ◈ ✧     ║
╰≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡╝

A spellbook of small, composable agent skills.

+===+===+===+===+===+===+===+===+===+===+===+===+

> *At-a-glance* is a feature

+===+===+===+===+===+===+===+===+===+===+===+===+

/grim-scry   ~≃> Reveal the shape of a project
/grim-repo   ~≃> Manage repos across workspace
/grim-weave  ~≃> Reveal relationships between systems
/grim-trace  ~≃> Trace a symbol or concept through workspace
/grim-adr    ~≃> Capture durable architectural decision records
```

## Skills

| Spell | Purpose |
| --- | --- |
| [grim-scry](grim-scry/README.md) | Project at-a-glance understanding |

## Examples

One directory per spell: `examples/<spell>/`. One file per run.

### [grim-scry](grim-scry/README.md)

| Run | Ran with |
| --- | --- |
| [tailscale](examples/grim-scry/tailscale-output.md) | Composer 2.5, Cursor |
| [kubernetes](examples/grim-scry/kubernetes-output.md) | Composer 2.5, Cursor |

## Roadmap

- [x] grim-scry (chat-only ASCII lenses)
- [ ] grim-repo, grim-weave, grim-trace, grim-adr

## Install

From the project that should receive the spells:

```bash
/path/to/grimoire/install.sh
```

Copies each skill into `.agents/skills/<skill-name>/` under the invoking directory.
