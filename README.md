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

/grim-scry  ~≃> Distill a repository into a canonical model
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

| Skill | Examples |
| --- | --- |
| [grim-scry](grim-scry/README.md) | [tailscale](examples/grim-scry/tailscale-output.md) (Composer 2.5, Cursor) |

## Roadmap

- [x] Canonical YAML schema
- [x] ASCII viewport
- [x] grim-scry
- [ ] grim-repo, grim-weave, grim-trace, grim-adr

## Install

From the project that should receive the spells:

```bash
/path/to/grimoire/install.sh
```

Copies each skill into `.agents/skills/<skill-name>/` under the invoking directory.
