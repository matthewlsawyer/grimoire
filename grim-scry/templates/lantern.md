# Lantern

## Structure

```text
{workspace}/
├─ⓘ {annotation}
╞══════════════════◆
│
├─≣ {concept}
│  ├─ⓘ {annotation}
│  ├─ {dir}/
│  └─ {dir}/{file}
│
├─≣ {concept}
│  ├─ {file}
│  └─ {path/to/dir}/
│     ├─ⓘ {annotation}
│     └─▶ {command}
│
└─≣ {...}
```

## Rules

- **Prefer vertical trees**. Do not deeply nest sub-trees.
- **Keep annotations tight**. Be succinct and annotate moderately.
- **Concepts first**. Relevant files, commands, sources, annotations, etc. hang underneath each concept trunk. Further context may hang thereunder.

## Style Guide

- One required `ⓘ` annotation under workspace header, before divider.
- Hierarchy branch glyphs: `│`, `├─`, `└─`.
- Annotation glyphs: `├─ⓘ`, `└─ⓘ`, `─ⓘ`.
- Concept glyphs: `├─≣`, `└─≣`, `─≣`.
- Command glyphs: `├─▶`, `└─▶`, `─▶`.
- Divider glyph: `╞══════════════════◆`.
- Indent each level, continue ancestors with `│`.
- `├─` / `├─ⓘ` / `├─≣` / `├─▶` non-final sibling;
- `└─` / `└─ⓘ` / `└─≣` / `└─▶` final sibling.
- Use `≣` for concept group trunks.
- Use `▶` for execution branches. Primary named commands only.
