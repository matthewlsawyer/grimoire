---
name: grim-scry
description: >-
    Given a repository or workspace, produce a simple canonical understanding.
---

# Grim Scry

_You must see before you act._

## Workflow

1. Resolve target (cwd / named repo; ask if unclear).
2. Run Script; stdout lines are the seed paths (closed set).
3. From stdout:
   - Read **only** those seed paths. Leave any other files unread.
   - Skip unreadable seeds; omit rather than invent.
   - Concepts and commands: omit if unnamed by this crawl.
   - No follow-up discovery after the script.
4. Distill for salience in-session (density included); do not write the lantern to disk.

## Script

Default seed budget `K = 50`.

From the skill root directory, run:

```bash
python3 <skill-root>/scripts/discover.py --target <absolute_target_filepath> --budget 50
```

- Always pass an absolute workspace to `--target`. Never use `--target .`
- Stdout (closed set): flat seed paths, one `./rel` per line. No section headers.
- Script lists only. Agent reads seed contents. No inventory on disk. No in-session `find`.
- Do not invent discovery scripts at runtime.

## Output

North star: at-a-glance. Every section stays tight and high-level.

1. Emit one Scry Lantern:
  - `# Grim Scry: <project>` outside the fence
  - One-line distillation outside the fence
  - `text` fence: tree only
2. `# Summary` - one short paragraph; high-level shape only
3. `Observations:` - ≤3 `-` bullets; high-signal only

### Scry Lantern

Ideas first. Implementers hung underneath concepts. Hang named commands under their concept (`▶`). Annotate with `ⓘ` only when seeds named purpose - do not invent.

Rules:
- Prefer vertical trees; largest concepts win.
- One required `ⓘ` annotation under workspace header, before divider.
- Moderate use of annotation in concept trees; ideas not captured in tree.
- Use `≣` for concept group trunks.
- Use `▶` for execution branches - primary named commands only.

Style:
- Hierarchy branch glyphs: `│`, `├─`, `└─`.
- Annotation glyphs: `├─ⓘ`, `└─ⓘ`, `─ⓘ`.
- Concept glyphs: `├─≣`, `└─≣`, `─≣`.
- Command glyphs: `├─▶`, `└─▶`, `─▶`.
- Divider glyph: `╞══════════════════◆`.
- Indent each level; continue ancestors with `│`.
- `├─` / `├─ⓘ` / `├─≣` / `├─▶` non-final sibling;
- `└─` / `└─ⓘ` / `└─≣` / `└─▶` final sibling.

Rules above are authoritative; below is drawing guide only.

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
