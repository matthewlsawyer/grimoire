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

grimoire/
├─ⓘ Spellbook of at-a-glance agent skills
╞══════════════════◆
│
├─▶ /grim-scry
├─▶ /grim-repo
├─▶ /grim-forge
└─▶ /grim-notes
```

---

Grimoire is a spellbook of at-a-glance agent skills. Each spell distills one aspect of your workspace into a compact viewport for you and your agents to reason about.

| Spell | Intent |
| --- | --- |
| Grim Scry | Discover understanding. |
| Grim Repo | Survey the workspace. |
| Grim Forge | Maintain historical provenance. |
| Grim Notes | Capture and organize daily notes. |

## grim-scry

Grim Scry gives insight into the conceptual _shape of a project_.

`/grim-scry` distills a target into one conceptual tree; ideas hang first, context underneath.

[grim-scry/SKILL.md](grim-scry/SKILL.md)

Example viewport:

```text
grimoire/
├─ⓘ Spellbook of at-a-glance agent skills
╞══════════════════◆
│
├─≣ Spells
│  ├─ⓘ Bounded discovery, live state, durable artifacts
│  ├─▶ /grim-scry
│  │  └─ⓘ Conceptual shape of a target
│  ├─▶ /grim-repo
│  │  └─ⓘ Nested git census board
│  ├─▶ /grim-forge
│  │  └─ⓘ HISTORY.md provenance ledger
│  └─▶ /grim-notes
│     └─ⓘ Monthly notes / todos / resources
│
├─≣ Scripts
│  ├─ⓘ Live under each skill's scripts/
│  ├─ grim-scry/scripts/discover.py
│  └─ grim-repo/scripts/census.py
│
├─≣ Ship
│  ├─▶ ./install.sh
│  │  └─ⓘ Copies spells into .agents/skills/
│  ├─ examples/
│  └─ tests/
│
└─≣ Docs
   └─ README.md
      └─ⓘ Spell intents, glyphs, roadmap
```

## grim-repo

Grim Repo gives insight into a _project in motion_.

`/grim-repo` censuses every nested git root and presents branch, sync, and working-tree deltas on a single board.

[grim-repo/SKILL.md](grim-repo/SKILL.md)

Example viewport:

```text
throneroom/
╞══════════════════◆
│
├─ ./
│  ├─▲ ↑0 ↓0
│  ├─▲ +95 -0
│  └─● main
│
├─ projects/dotfiles/
│  ├─▲ ↑0 ↓0
│  ├─▲ +35 -8
│  └─● main
│
├─ projects/grimoire/
│  ├─▲ ↑0 ↓0
│  ├─▲ +66 -69
│  └─● feat/grim-notes
│
└─ projects/site/
   ├─▲ ↑0 ↓0
   ├─▲ +0 -0
   └─● main
```

## grim-forge

Grim Forge maintains a project's _provenance over time_.

`/grim-forge` bootstraps or updates `HISTORY.md` from bounded history since last run, then shows a summary viewport of the delta.

[grim-forge/SKILL.md](grim-forge/SKILL.md)

Example excerpt from history file:

```markdown
### Origins

The repo began July 6, 2026 as a skills collection (`cb12339`), renamed to skillit the next day (`786ce80`) and grimoire on July 8 (`451261f`). Grim Scry arrived July 20 (`a031701`) as the first spell — canonical repo models distilled into session viewports. `install.sh` copied spells into invoking `.agents/skills/` (`0b5c1c5`); README framed spellbook axioms and roadmap (`82c236b`).
```

Example excerpt from viewport:

```text
projects/grimoire/HISTORY.md
╞══════════════════◆
│
├─≣ 2026-08-02
│  └─ grim-notes arrives: daily notes/todos/resources ledger + examples.
├─ ...
└─≣ 2026-07-06 -> 2026-07-08
   └─ Origins: skills -> skillit -> grimoire; first spell July 20.
```

## grim-notes

Grim Notes captures a workspace's _daily notes_ into a monthly ledger.

`/grim-notes` with a given context classifies notes, todos, and resources into `notes/YYYY-MM.md` under today's day heading, then shows a delta viewport. Bare `/grim-notes` shows a status snapshot across all monthly ledgers.

[grim-notes/SKILL.md](grim-notes/SKILL.md)

Capture viewport:

```text
notes/
╞══════════════════◆
│
└─≣ 2026-08.md
   └─≣ 2026-08-02
      ├─▲ +1 note
      └─▲ +1 todo
```

Status viewport:

```text
notes/
╞══════════════════◆
│
└─≣ 2026-08.md
   ├─● 1 note
   └─● 1 todo
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

Sample runs: [examples/](examples/).

| Spell | Run |
| --- | --- |
| `/grim-scry` | [buildawesome](examples/grim-scry/buildawesome-2026-07-31.md), [ghostty](examples/grim-scry/ghostty-2026-07-31.md) |
| `/grim-repo` | [throneroom](examples/grim-repo/throneroom-2026-07-31.md) |
| `/grim-forge` | [buildawesome](examples/grim-forge/buildawesome-2026-08-02.md), [ghostty](examples/grim-forge/ghostty-2026-08-02.md) |
| `/grim-notes` | [throneroom](examples/grim-notes/throneroom-2026-08-02.md) |

## Install

Via [skills.sh](https://skills.sh/) / the skills CLI:

```bash
npx skills add matthewlsawyer/grimoire
```

Options:

```bash
# list spells without installing
npx skills add matthewlsawyer/grimoire --list

# one spell
npx skills add matthewlsawyer/grimoire --skill grim-scry

# global (all agents on this machine)
npx skills add matthewlsawyer/grimoire -g
```

Local copy into the invoking project's `.agents/skills/`:

```bash
/path/to/grimoire/install.sh
```

## Scripts

Ship inside each skill directory (`{skill-root}/scripts/`).

| Spell | Script |
| --- | --- |
| `/grim-scry` | [discover.py](grim-scry/scripts/discover.py) |
| `/grim-repo` | [census.py](grim-repo/scripts/census.py) |

Stdout:

- `/grim-scry` - seed paths, one `./rel` per line
- `/grim-repo` - full census board (fence as-is)

Example invocations (absolute paths only):

```bash
# scry
python3 grim-scry/scripts/discover.py --target /abs/workspace

# repo
python3 grim-repo/scripts/census.py --target /abs/workspace
```

## Tests

From this directory (`projects/grimoire/`):

```bash
python3 tests/grim-scry/test.py
python3 tests/grim-repo/test.py
```

Standard-library `unittest` only. Spell scripts load by path via `[tests/load_script.py](tests/load_script.py)`.

## Roadmap

- Grim Scry: accept repositories, directories, files, symbols, and arbitrary tokens as discovery entry points.
- Grim Repo: add agentic insights about in-flight work on top of its deterministic census.
