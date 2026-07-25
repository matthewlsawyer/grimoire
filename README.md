# grimoire

```text
╭───────────────╮
│  ◆ grimoire   ║
│  ══+═════+══  ║
│               ║
|  / ◇─▶ cast   ║
│               ║
│  ────┬┼┬────  ║
│     + ◆ +     ║
╰≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡╝

A spellbook of at-a-glance agent skills.
```

## Skills

| Spell | Purpose |
| --- | --- |
| [grim-scry](grim-scry/README.md) | Reveal project meaning |
| [grim-repo](grim-repo/README.md) | Nested git repo status |

## Glyph Dictionary

| Glyph | Role |
| --- | --- |
| `│` `├` `└` `─` | hierarchy (structure) |
| `╞` `═` | divider |
| `ⓘ` | annotation |
| `▶` | execution |
| `▲` | status / delta / metric |
| `●` | state / snapshot |
| `◆` | terminator |

## Examples

One directory per spell: `examples/<spell>/`. One file per run.

| Run | Date | Ran with |
| --- | --- | --- |
| [grim-scry/omarchy](examples/grim-scry/omarchy.md) | 2026-07-24 | Composer 2.5 |
| [grim-repo/throneroom](examples/grim-repo/throneroom.md) | 2026-07-24 | Composer 2.5 |

## Roadmap

- [x] grim-scry
- [x] grim-repo
- [ ] grim-weave, grim-trace, grim-adr

## Install

From the project that should receive the spells:

```bash
/path/to/grimoire/install.sh
```

Copies each skill into `.agents/skills/<skill-name>/` under the invoking directory.
