# grimoire

```text
╭───────────────╮
│  ◈ grimoire   ║
│  ══✧═════✧══  ║
│               ║
|  / ~≃▶ cast   ║
│               ║
│  ────┬┼┬────  ║
│     ✧ ◈ ✧     ║
╰≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡╝

A spellbook of small, composable agent skills.

+===+===+===+===+===+===+===+===+===+===+===+===+

> *At-a-glance* is a feature

+===+===+===+===+===+===+===+===+===+===+===+===+

/grim-scry   ~≃▶ Shape of a system
/grim-repo   ~≃▶ Manage repos
/grim-weave  ~≃▶ Relationships between systems
/grim-trace  ~≃▶ Trace a symbol
/grim-adr    ~≃▶ Capture durable records
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
| [omarchy](examples/grim-scry/omarchy.md) | Composer 2.5 |

## Roadmap

- [x] grim-scry
- [ ] grim-repo, grim-weave, grim-trace, grim-adr

## Install

From the project that should receive the spells:

```bash
/path/to/grimoire/install.sh
```

Copies each skill into `.agents/skills/<skill-name>/` under the invoking directory.
