---
name: grim-scry
description: >-
  Produce a report that distills a simple at-a-glance understanding of the workspace.
  Use when the user invokes grim-scry or wants an at-a-glance conceptual map
  of a project.
---

# Scry

Produce a report that distills a simple at-a-glance understanding of the workspace.

## Workflow

1. Resolve `target` to an absolute workspace root. Use cwd, named path, or remote URL (clone to an OS temp dir, then absolute path). Empty means the current workspace root.
2. **Discovery**. Run discover script. See [Script](#script) section below.
3. **Read seed paths**. Skip unreadable seeds; omit rather than invent.
4. **Distill for salience**. Distill concepts, structure, and commands from the read. Treat ADR and README seeds as high salience.
5. **Emit report**. Use the distillation to emit a report using template [report.md](./templates/report.md). Do not write to disk.

## Script

From the skill root directory, run:

```bash
python3 {skill-root}/scripts/discover.py --target {target}
```

- Always pass an absolute path to `--target`. Never use `--target .`.
- Stdout: flat seed paths, one `./rel` path per line.

## Usage

Call `/grim-scry` with a target or infer the current workspace.

```text
/grim-scry packages/api/
/grim-scry .
/grim-scry
/grim-scry https://github.com/example/repo
```
