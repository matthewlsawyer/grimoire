# grimoire

```
╭───────────────╮
│  ◈ grimoire   ║
│  ══✧═════✧══  ║
│               ║
|  / ~ > cast   ║
│               ║
│  ────┬┼┬────  ║
│     ✧ ◈ ✧     ║
╰≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡╝

A spellbook of small, composable agent skills.
```

## Axioms

- _At-a-glance_ is a feature
- _Dead-simple_ beats clever
- Small, single-responsibility spells
- Fast over exhaustive
- Knowledge first -> viewport second
- Evidence over inference
- Agent-orchestrated skill workflows -> think unix `grim-scry && grim-adr`
- Shared artifacts live in `<agent-workspace>/.grimoire/`

---

## Spellbook

- [`grim-scry`](grim-scry/README.md) -> Distill a repository into a high-level canonical understanding.
- `grim-repo` -> Discover repositories and summarize their Git state across a workspace.
- `grim-weave` -> Reveal relationships between repositories and systems.
- `grim-trace` -> Trace a symbol, concept, or service through its surrounding relationships.
- `grim-adr` -> Capture durable architectural decision records from completed work.

---

## Core Architecture

```text
Repository
└─▶ Discovery
   └─▶ Distillation
       └─▶ Canonical Model -> `<agent-workspace>/.grimoire/scry/<slug>/model.yaml`
           ├─▶ ASCII (reserved sibling: `ascii.md`)
           ├─▶ Markdown
           ├─▶ Mermaid
           ├─▶ GraphViz
           └─▶ Future renderers...
```

---

## Design Principles

- Build the knowledge, not the view.
- Keep the model simple enough for both humans and agents.
- Prefer composable artifacts over complex integrations.
- Favor opinionated defaults over endless configuration.
- Ship small spells that solve one problem well.

---

## Roadmap

### Foundation
- [x] `grim-scry`
- [x] Canonical YAML schema
- [x] ASCII renderer

### Discovery
- [ ] `grim-repo`
- [ ] `grim-weave`
- [ ] `grim-trace`

### Knowledge
- [ ] `grim-adr`

---

## Install

From the project that should receive the spells:

```bash
/path/to/grimoire/install.sh
```

Copies each skill into `.agents/skills/<skill-name>/` under the invoking directory.
