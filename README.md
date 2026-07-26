# grimoire

```text
╭───────────────╮
│  ◆ grimoire   ║
│  ══+═════+══  ║
│               ║
|  / ~─▶ cast   ║
│               ║
│  ────┬┼┬────  ║
│     ◇ ◆ ◇     ║
╰≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡╝

A spellbook of at-a-glance agent skills.
```

## Skills

| Spell | Purpose |
| --- | --- |
| [grim-scry](grim-scry/README.md) | Conceptual graph of target project |
| [grim-repo](grim-repo/README.md) | Nested git repo census |
| [grim-weave](grim-weave/README.md) | Thread a token through the repo into a ledger |

## Glyph Dictionary

| Glyph | Role |
| --- | --- |
| `│` `├` `└` `─` | hierarchy (structure) |
| `╞` `═` | divider |
| `◆` `◇` | terminator |
| `ⓘ` | annotation |
| `≣` | concept / group / thread |
| `▶` | execution |
| `▲` | status / delta / metric |
| `●` | state / snapshot |

## Examples

One directory per spell: `examples/<spell>/`. One file per run.

| Run | Date | Ran with |
| --- | --- | --- |
| [grim-scry/omarchy](examples/grim-scry/omarchy.md) | 2026-07-24 | Composer 2.5 |
| [grim-repo/throneroom](examples/grim-repo/throneroom.md) | 2026-07-24 | Composer 2.5 |
| [grim-weave/grim-scry](examples/grim-weave/grim-scry.md) | 2026-07-26 | Composer 2.5 |

## Roadmap

- [x] grim-scry
- [x] grim-repo
- [x] grim-weave

## Install

From the project that should receive the spells:

```bash
/path/to/grimoire/install.sh
```

Copies each skill into `.agents/skills/<skill-name>/` under the invoking directory.

## Tests

From this directory (`projects/grimoire/`):

```bash
python3 tests/grim-weave/test.py
python3 tests/grim-scry/test.py
python3 tests/grim-repo/test.py
```

Standard-library `unittest` only. Spell scripts are loaded by path via [`tests/load_script.py`](tests/load_script.py).
