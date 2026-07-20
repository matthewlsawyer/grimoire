# grimoire

```text
╭───────────────╮
│  ◈ grimoire   ║
│  ══✧═════✧══  ║
│               ║
|  / ~≃> cast   ║
│               ║
│  ────┬┼┬────  ║
│     ✧ ◈ ✧     ║
╰≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡╝

A spellbook of small, composable agent skills.

+===+===+===+===+===+===+===+===+===+===+===+===+

[/grim-scry](grim-scry/README.md)  ~≃> Distill a repository into a canonical model
/grim-repo   ~≃> Discover repos and summarize Git state across a workspace
/grim-weave  ~≃> Reveal relationships between repositories and systems
/grim-trace  ~≃> Trace a symbol, concept, or service through its relationships
/grim-adr    ~≃> Capture durable architectural decision records
```

## Axioms

- *At-a-glance* is a feature
- *Dead-simple* beats clever
- Opinionated defaults
- Small, single-responsibility skills
- Knowledge first -> viewport second
- Agentic workflows -> think unix `grim-scry && grim-adr`
- Shared artifacts live in `<agent-workspace>/.grimoire/`

## Examples

One directory per skill: `examples/<skill>/`.

| Skill | Example |
| --- | --- |
| [grim-scry](grim-scry/README.md) | [vercel/next.js](examples/grim-scry/example-run.md) (Composer 2.5) |

## Roadmap

- [x] Canonical YAML schema
- [x] ASCII renderer (chat; `ascii.md` reserved)
- [ ] Additional viewports (Markdown, Mermaid, GraphViz)
- [ ] Ship planned spells in Spellbook above

## Install

From the project that should receive the spells:

```bash
/path/to/grimoire/install.sh
```

Copies each skill into `.agents/skills/<skill-name>/` under the invoking directory.
