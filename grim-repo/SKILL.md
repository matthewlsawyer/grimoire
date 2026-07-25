---
name: grim-repo
description: >-
    Given a workspace or directory, reveal nested git repositories and their
    current status.
---

# Grim Repo

_What lives must be named._

## Workflow

1. Resolve target (workspace root or named path).
2. Run ledger; emit output.

## Ledger

From the skill root directory, run:

```bash
python3 <skill-root>/scripts/ledger.py --target <absolute_target_filepath>
```

- Always pass an absolute workspace to `--target`. Never use `--target .`
- Owns find + status draw. Fence full stdout as-is. Do not redraw.

## Output

1. `# Grim Repo: <project>` outside the fence
2. `text` fence: full ledger stdout
