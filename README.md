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

Grimoire spells put evidence into the session: bounded discovery, live state, and durable artifacts. Cast from within an agent session.

Reason with the results.

| Spell | Intent |
| --- | --- |
| Grim Scry | Discover understanding. |
| Grim Repo | Survey the workspace. |
| Grim Forge | Maintain provenance. |

## grim-scry

Grim Scry gives insight into the conceptual _shape of a project_.

`/grim-scry` distills a target into one conceptual tree; ideas hang first, context underneath.

[grim-scry/SKILL.md](grim-scry/SKILL.md)

Example viewport:

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

## grim-repo

Grim Repo gives insight into a _project in motion_.

`/grim-repo` censuses every nested git root and puts branch, sync, and working-tree deltas on one board so you can see work-in-flight before the next task.

[grim-repo/SKILL.md](grim-repo/SKILL.md)

Example viewport:

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

## grim-forge

Grim Forge maintains a project's _provenance over time_.

`/grim-forge` bootstraps or updates `CHANGELOG.md` and `HISTORY.md` per git root from bounded history since the last marker, then shows a summary viewport of the delta.

[grim-forge/SKILL.md](grim-forge/SKILL.md)

Example viewport:

```text
workspace/
╞══════════════════◆
│
├─ CHANGELOG.md
│  └─ ## [Unreleased]
│     ├─ ### Added
│     └─ ### Changed
│
└─ HISTORY.md
   ├─ marker: none -> abc1234
   ├─ ## Story
   └─ ## Timeline
      └─ ### 2026-07-29
```

## Scripts

Ship inside each skill directory (`<skill-root>/scripts/`).

| Spell | Script |
| --- | --- |
| `/grim-scry` | [discover.py](grim-scry/scripts/discover.py) |
| `/grim-repo` | [census.py](grim-repo/scripts/census.py) |
| `/grim-forge` | [status.py](grim-forge/scripts/status.py) |

Stdout:

- `/grim-scry` - seed paths, one `./rel` per line
- `/grim-repo` - full census board (fence as-is)
- `/grim-forge` - status JSON evidence manifest

Example invocations (absolute paths only):

```bash
# scry
python3 grim-scry/scripts/discover.py --target /abs/workspace --budget 50

# repo
python3 grim-repo/scripts/census.py --target /abs/workspace

# forge
python3 grim-forge/scripts/status.py --target /abs/workspace
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
| `/grim-scry` | [ghostty](examples/grim-scry/ghostty-2026-07-26.md) |
| `/grim-repo` | [throneroom](examples/grim-repo/throneroom-2026-07-26.md) |
| `/grim-forge` | [11ty buildawesome](examples/grim-forge/11ty-2026-07-30.md) |

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
python3 tests/grim-forge/test.py
```

Standard-library `unittest` only. Spell scripts load by path via `[tests/load_script.py](tests/load_script.py)`.

## Roadmap

- Grim Scry: accept repositories, directories, files, symbols, and arbitrary tokens as discovery entry points.
- Grim Repo: add agentic insights about in-flight work on top of its deterministic census.
