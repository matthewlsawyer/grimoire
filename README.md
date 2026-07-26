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


| Spell                           | Purpose                            |
| ------------------------------- | ---------------------------------- |
| [grimscry](grimscry/SKILL.md)   | Conceptual graph of target project |
| [grimrepo](grimrepo/SKILL.md)   | Nested git repo census             |
| [grimweave](grimweave/SKILL.md) | Thread a token into a ledger       |




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


| Glyph           | Role                     |
| --------------- | ------------------------ |
| `│` `├` `└` `─` | hierarchy (structure)    |
| `╞` `═`         | divider                  |
| `◆` `◇`         | terminator               |
| `ⓘ`             | annotation               |
| `≣`             | concept / group / thread |
| `▶`             | execution                |
| `▲`             | status / delta / metric  |
| `●`             | state / snapshot         |




## Examples

Sample runs (metadata + viewport): [examples/](examples/).


| Spell     | Runs                                                        |
| --------- | ----------------------------------------------------------- |
| grimscry  | [ghostty](examples/grimscry/ghostty-2026-07-26.md)          |
| grimweave | [ghostty-zig](examples/grimweave/ghostty-zig-2026-07-26.md) |
| grimrepo  | [throneroom](examples/grimrepo/throneroom-2026-07-26.md)    |




## Install

From the project that should receive the spells:

```bash
/path/to/grimoire/install.sh
```

Copies each skill into `.agents/skills/<skill-name>/` under the invoking directory.
