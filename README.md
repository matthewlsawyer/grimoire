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

## grim-forge

Grim Forge maintains a project's provenance - `CHANGELOG.md` (Keep a Changelog factual ledger: what changed) and `HISTORY.md` (temporal ledger: when it landed) per git repository root.

`/grim-forge` resolves `repo_root` with `git rev-parse --show-toplevel`, then traces bounded history within that repo only. On its first run it bootstraps both artifacts; later runs append curated Unreleased bullets and dated Timeline entries since the recorded marker. Name a nested path (for example, `projects/grimoire`) to forge that repo's artifacts separately.

[grim-forge/SKILL.md](grim-forge/SKILL.md)

Forge writes only under `## [Unreleased]` until a human cuts a release. The marker lives in `CHANGELOG.md`. HISTORY `## Timeline` is reverse chronological, keyed to commit dates from git. Timeline may link to changelog bullets and ADRs when git named them; changelog never links to history.

HISTORY Story is a palimpsest: genesis writes the durable narrative once; delta runs add 0-1 dated Timeline entry per run when warranted. An outer workshop history records Throneroom policy only - boundary decisions evidenced in outer commits, rules, or XP. It does not name inner repos or narrate their commits.

Forge writes only `CHANGELOG.md` and `HISTORY.md`. It does not edit source, README, ADR, or other project documentation.

## Scripts

Ship inside each skill directory (`<skill-root>/scripts/`).

| Spell | Script |
| --- | --- |
| `/grim-scry` | [discover.py](grim-scry/scripts/discover.py) |
| `/grim-repo` | [census.py](grim-repo/scripts/census.py) |
| `/grim-forge` | [forge.py](grim-forge/scripts/forge.py) |

Stdout:

- `/grim-scry` - seed paths, one `./rel` per line
- `/grim-repo` - full census board (fence as-is)
- `/grim-forge` - status or focused JSON evidence manifest

Example invocations (absolute paths only):

```bash
python3 grim-scry/scripts/discover.py --target /abs/workspace --budget 50
python3 grim-repo/scripts/census.py --target /abs/workspace
python3 grim-forge/scripts/forge.py status \
  --target /abs/workspace
python3 grim-forge/scripts/forge.py status \
  --target /abs/workspace \
  --bootstrap
python3 grim-forge/scripts/forge.py focus \
  --target /abs/workspace \
  --candidate ./packages/api \
  --budget 25
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
| `/grim-scry` | [_template](examples/_template.md) |
| `/grim-repo` | [_template](examples/_template.md) |
| `/grim-forge` | [genesis and delta](examples/grim-forge/genesis-and-delta.md) |

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