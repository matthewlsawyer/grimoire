# Delta

## Structure

````markdown
# Grim Notes: {Project Name}

```text
notes/
╞══════════════════◆
│
└─≣ 2026-08.md
   └─≣ 2026-08-02
      ├─▲ +1 note
      ├─▲ +2 todos
      └─▲ +1 resource
```
````

## Rules

- **Show the delta**. Capture only what was appended this run.
- Omit zero-count lines.
- Singular/plural labels: `note`/`notes`, `todo`/`todos`, `resource`/`resources`.

## Style Guide

- Hierarchy glyphs: `│`, `├`, `└`, `─`.
- Group glyphs: `├─≣`, `└─≣`.
- Delta glyph: `▲`.
- Divider glyph: `╞══════════════════◆`.
- Indent each level, continue ancestors with `│`.
- `├─` for non-final sibling;
- `└─` for final sibling.
