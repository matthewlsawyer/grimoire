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

```bash
python3 scripts/ledger.py --target <spell-target-abs>
```

- Absolute `--target` only; never `--target .`.
- Owns find + status draw. Fence full stdout as-is. Do not redraw.

## Output

1. `# Grim Repo: <project>` outside the fence
2. `text` fence: full ledger stdout
3. Next steps

## Scripts

| File | Role |
| --- | --- |
| [scripts/ledger.py](scripts/ledger.py) | Find nested git roots + live status board |
