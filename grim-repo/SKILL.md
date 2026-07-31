---
name: grim-repo
description: >-
  Produce a report that distills an at-a-glance census of git roots in the workspace.
  Use when the user invokes grim-repo or needs a nested-repo census board.
---

# Grim Repo

_What lives must be named._

Produce a report that distills an at-a-glance census of git roots in the workspace.

## Workflow

1. Resolve `target` to an absolute workspace root. Use cwd or named path. Empty means the current workspace root.
2. **Generate a census**. Run census script. See [Script](#script) section below.
3. **Emit report**. Use the stdout to emit a report using template [report.md](./templates/report.md). Do not write to disk.

## Script

From the skill root directory, run:

```bash
python3 {skill-root}/scripts/census.py --target {target}
```

- Always pass an absolute workspace to `--target`. Never use `--target .`
- Stdout is the git root census as a unicode tree.

## Usage

```text
/grim-repo
/grim-repo /path/to/workspace
```
