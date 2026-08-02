# Status

## Structure

````markdown
# Grim Notes: {Project Name}

```text
notes/
╞══════════════════◆
│
├─≣ 2026-08.md
│  ├─● 1 note
│  ├─● 2 todos
│  └─● 1 resource
│
└─≣ 2026-07.md
   ├─● 12 notes
   ├─● 2 todos
   └─● 15 resources
```
````

## Rules

- **Show the snapshot**. Totals per month file across all days in that file.
- List month files descending (newest `YYYY-MM.md` first).
- Omit zero-count lines for a bucket within a month.
- Singular/plural labels: `note`/`notes`, `todo`/`todos`, `resource`/`resources`.
- If `notes/` is missing or empty:

```text
notes/
╞══════════════════◆
│
└─ⓘ nothing captured yet
```

## Style Guide

- Hierarchy glyphs: `│`, `├`, `└`, `─`.
- Group glyphs: `├─≣`, `└─≣`.
- Snapshot glyph: `●`.
- Annotation glyph: `ⓘ`.
- Divider glyph: `╞══════════════════◆`.
- Indent each level, continue ancestors with `│`.
- `├─` for non-final sibling;
- `└─` for final sibling.
