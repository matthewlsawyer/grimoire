---
name: grim-repo
description: >-
    Given a workspace or directory, reveal nested git repositories and their
    current status.
---

_Reveal the repos underfoot._

# Grim Repo Workflow

1. Resolve target (workspace root or named path).
2. If `ledger.txt` is missing, empty, unreadable, or **regenerate** was requested:
   - On **regenerate**: wipe `ledger.txt` first.
   - Discover → Lock-in (fresh selection; do not reuse prior) → write `ledger.txt` only if Lock-in accepts.
3. Run Ledger; emit Output.

## Discover

Default depth `N = 4`. Default budget `R = 10`.

```bash
python3 scripts/discover.py --target <spell-target-abs> --depth 4 --budget 10
```

- Absolute `--target` only; never `--target .`.
- Stdout only: one relative path per line.
- Script does not prompt, write, or run status.

## Ledger

```bash
python3 scripts/ledger.py --workspace <agent-workspace-abs> --target <target-rel>
```

- `--workspace`: agent workspace root. `--target`: relative to workspace.
- Owns draw + status tokens. Stdout may include a stale-path block after the tree; fence all of it as-is. Does not write or prune `ledger.txt`.

## Artifact

```text
<agent-workspace>/.grimoire/grim-repo/<slug>/
└─ ledger.txt
```

- `slug`: target relative to workspace, `/` → `-`. Workspace root → repository name.
- `ledger.txt`: locked-in paths, one per line.

## Lock-in

- One candidate → auto-lock.
- Multiple → numbered list; accept `all`, indices (e.g. `1 3 4`), or `abort`.
- `abort` → write nothing. Otherwise → write selected paths to `ledger.txt`.

## Output

1. `# Grim Repo: <project>` outside the fence
2. `text` fence: full Ledger stdout

### Footer

Plain prose after the fence (blank line between each line).

**Current**:

- `Ledger: [.grimoire/grim-repo/<slug>/ledger.txt](...).`
- Run again for fast repository status against the ledger.
- Say **regenerate** to rewrite the ledger.

**Stale** (stdout lists stale paths):

- `Ledger: [.grimoire/grim-repo/<slug>/ledger.txt](...).`
- `Stale: \`path/a/\`, \`path/b/\`.`
- Run again for fast repository status against the ledger.
- Say **regenerate** to rewrite the ledger.
