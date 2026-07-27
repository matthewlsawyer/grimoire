# grimoire

```text
╭─────────────╮
│ ◆ grimoire  ║
│ ══+═════+══ ║
│      ☾      ║
| / ~─▶ cast  ║
│ ────┬┼┬──── ║
│    ◇ ◆ ◇    ║
╰≡≡≡≡≡≡≡≡≡≡≡≡≡╝
```

A spellbook of at-a-glance agent skills.

---

You open a workspace cold. You open the README and read a couple lines. You eventually open the agent window.

> "What's going on here?"

The usual response is paragraphs you don't need. What you're looking for is _shape_.

---

Grimoire spells put **shape** into the session: bounded viewports the agent composes from evidence. Orientation, not omniscience; cast from within an agent session.

Reason with the results.

## grimscry

`/grimscry` distills a target into one concept lantern - ideas hang first, named commands underneath.

[grimscry/SKILL.md](grimscry/SKILL.md)

## grimweave

`/grimweave` follows a file, symbol, or phrase into definitions, relationships, provenance, and threads worth pulling next.

[grimweave/SKILL.md](grimweave/SKILL.md)

## grimrepo

`/grimrepo` censuses every nested git root and puts branch, sync, and working-tree deltas on one board so you can see work-in-flight before the next task.

[grimrepo/SKILL.md](grimrepo/SKILL.md)

## Scripts

Ship inside each skill directory (`<skill-root>/scripts/`).

| Spell | Script |
| --- | --- |
| `/grimscry` | [discover.py](grimscry/scripts/discover.py) |
| `/grimweave` | [weave.py](grimweave/scripts/weave.py) |
| `/grimrepo` | [census.py](grimrepo/scripts/census.py) |

Stdout:

- `/grimscry` - seed paths, one `./rel` per line
- `/grimweave` - JSON evidence floor (`kind`: `weave_evidence`)
- `/grimrepo` - full census board (fence as-is)

Example invocations (absolute `--target` only):

```bash
python3 grimscry/scripts/discover.py --target /abs/workspace --budget 50
python3 grimrepo/scripts/census.py --target /abs/workspace
python3 grimweave/scripts/weave.py --target /abs/workspace --token MySymbol
```

## At-a-glance viewports

Example Grim Scry template:

```text
Workspace
├─ⓘ Go todo api surface
╞══════════════════◆
│
├─≣ Runtime
│  ├─ⓘ Runtime complexities
│  ├─ server/
│  └─ client/
│
├─≣ Packages
│  └─ packages/core/
│     └─ⓘ Main library
│
├─≣ Quality
│  ├─▶ npm audit
│  │  └─ⓘ full repo audit
│  └─▶ npm test
│
├─≣ Docs
│  └─▶ npm run docs
│
└─≣ Guidance
   └─ AGENTS.md
      └─ⓘ Agent source of truth
```

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

Sample runs (metadata + viewport): [examples/](examples/).

| Spell | Run |
| --- | --- |
| `/grimscry` | [ghostty](examples/grimscry/ghostty-2026-07-26.md) |
| `/grimweave` | [ghostty-zig](examples/grimweave/ghostty-zig-2026-07-26.md) |
| `/grimrepo` | [throneroom](examples/grimrepo/throneroom-2026-07-26.md) |

## Install

From the project that should receive the spells:

```bash
/path/to/grimoire/install.sh
```

Copies each skill into `.agents/skills/<skill-name>/` under the invoking directory.

## Tests

From this directory (`projects/grimoire/`):

```bash
python3 tests/grimscry/test.py
python3 tests/grimrepo/test.py
python3 tests/grimweave/test.py
```

Standard-library `unittest` only. Spell scripts load by path via `[tests/load_script.py](tests/load_script.py)`.