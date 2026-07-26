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

Agent-only spells: each skill is a single `SKILL.md` (Inputs, Workflow, Output shapes). No helper scripts; the session agent gathers evidence and draws viewports per the skill.

## Skills

| Spell | Purpose |
| --- | --- |
| [grim-scry](grim-scry/SKILL.md) | Conceptual graph of target project |
| [grim-repo](grim-repo/SKILL.md) | Nested git repo census |
| [grim-weave](grim-weave/SKILL.md) | Thread a token through the repo into a ledger |

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
