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

> What's going on here?

The usual response is paragraphs you don't need. What you're looking for is _shape_.

---

Grimoire spells put **shape** into the session: bounded viewports the agent composes from evidence. Orientation, not omniscience; cast from within an agent session.

Reason with the results.

## grim-scry

Grim Scry gives insight into the conceptual _shape of a project_.

`/grim-scry` distills a target into one concept lantern - ideas hang first, named commands underneath.

[grim-scry/SKILL.md](grim-scry/SKILL.md)

Example template:

```text
workspace/
├─ⓘ Example golang api surface
╞══════════════════◆
│
├─≣ Runtime
│  ├─ⓘ Runtime notes
│  ├─ⓘ Other complexities
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
│  ├─ docs/README.md
│  └─▶ npm run docs
│
└─≣ Guidance
   └─ AGENTS.md
      └─ⓘ Agent source of truth
```

## grim-weave

Grim Weave gives insight into the _relationships_ of a concept.

`/grim-weave` follows a file, symbol, or phrase into depends-on, referenced-by, and related threads worth pulling next.

[grim-weave/SKILL.md](grim-weave/SKILL.md)

Example template:

```text
≣ weave_paths
├─ⓘ Runs `list_files` → `classify_token` → optional file seeds → `collect_paths` → shallow sort → `budget` slice; `main()` prints each path
╞══════════════════◆
│
├─≣ Definition
│  └─ ./projects/grimoire/grim-weave/scripts/weave.py
│     └─ⓘ `def weave_paths(target_root, token, budget)`
│
├─≣ Referenced By
│  ├─ ./projects/grimoire/tests/grim-weave/test.py
│  │  └─ⓘ `WeavePathsTests` (prune, budget, file seed, scan) via `load_script`
│  ├─ ./projects/grimoire/grim-weave/SKILL.md
│  └─ ./projects/grimoire/README.md
│     └─ⓘ example ledger trunk for this symbol
│
└─≣ Related
   ├─≣ collect_paths
   ├─≣ classify_token
   ├─≣ list_files
   └─≣ main
```

Follow-ons: `/grim-weave collect_paths`, `/grim-weave classify_token`, etc.

## grim-repo

Grim Repo gives insight into a _project in motion_.

`/grim-repo` censuses every nested git root and puts branch, sync, and working-tree deltas on one board so you can see work-in-flight before the next task.

[grim-repo/SKILL.md](grim-repo/SKILL.md)

Example template:

```text
workspace/
╞══════════════════◆
│
├─ ./
│  ├─▲ ↑2 ↓0
│  ├─▲ +540 -6
│  └─● main
│
├─ projects/dotfiles/
│  ├─▲ ↑0 ↓0
│  ├─▲ +8 -8
│  └─● main
│
└─ projects/site/
   ├─▲ ↑0 ↓0
   ├─▲ +318 -229
   └─● main
```

## Scripts

Ship inside each skill directory (`<skill-root>/scripts/`).

| Spell | Script |
| --- | --- |
| `/grim-scry` | [discover.py](grim-scry/scripts/discover.py) |
| `/grim-weave` | [weave.py](grim-weave/scripts/weave.py) |
| `/grim-repo` | [census.py](grim-repo/scripts/census.py) |

Stdout:

- `/grim-scry` - seed paths, one `./rel` per line
- `/grim-weave` - matching paths, one `./rel` per line
- `/grim-repo` - full census board (fence as-is)

Example invocations (absolute `--target` only):

```bash
python3 grim-scry/scripts/discover.py --target /abs/workspace --budget 50
python3 grim-repo/scripts/census.py --target /abs/workspace
python3 grim-weave/scripts/weave.py --target /abs/workspace --token MySymbol --budget 40
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
| `/grim-scry` | [ghostty](examples/grim-scry/ghostty-2026-07-26.md) |
| `/grim-weave` | [ghostty-zig](examples/grim-weave/ghostty-zig-2026-07-26.md) |
| `/grim-repo` | [throneroom](examples/grim-repo/throneroom-2026-07-26.md) |

## Install

From the project that should receive the spells:

```bash
/path/to/grimoire/install.sh
```

Copies each skill into `.agents/skills/<skill-name>/` under the invoking directory.

## Tests

From this directory (`projects/grimoire/`):

```bash
python3 tests/grim-scry/test.py
python3 tests/grim-repo/test.py
python3 tests/grim-weave/test.py
```

Standard-library `unittest` only. Spell scripts load by path via `[tests/load_script.py](tests/load_script.py)`.