---
name: grim-repo
description: >-
    Given a workspace or directory, hunt nested git repositories, lock in which
    to track, then run the ledger script for an at-a-glance ASCII status board.
---

# Repo

_Reveal the repos underfoot._

## Workflow

Default hunt depth `N = 4`.
Default repo budget `R = 10`.

1. Resolve target:
   - Default: agent workspace root. Do not ask to confirm.
   - Else: a path the user named.
2. Resolve Artifact path for this target (see Artifact path).
3. Lock-in gate:
   - If asked to **regenerate**, or `ledger.txt` is missing / empty / unreadable: run hunt script (see Scripts), then **stop and prompt** (see Lock-in). Do not write until the user answers. After lock-in, write `ledger.txt`, then continue.
   - Else: skip hunt and questions; reuse `ledger.txt`.
4. Run the ledger script (see Scripts). Emit its stdout in a `text` fence.
5. Return a link to `ledger.txt`.
6. If the script reported stale paths: ask whether to regenerate. Do not auto-prune.

## Scripts

```text
scripts/hunt_repos.py      # discovery only (first run / regenerate)
scripts/ascii_ledger.py    # live status from ledger.txt
```

Run from the skill directory (or with an absolute path to the script).

### Hunt

```bash
python3 scripts/hunt_repos.py --target <spell-target-abs> --depth 4 --budget 10
```

- Always pass an absolute `--target` (the resolved spell target). Never use `--target .`; default is workspace.
- Emits one relative path per line (directories keep trailing `/`; target root is `./`).
- Shallow-first; capped by `--budget`. Does not honor `.gitignore`. Avoids symlinks. Never descends into `.git`.
- Does not prompt, write `ledger.txt`, or run status. Agent numbers the lines and prompts.

### Ledger

```bash
python3 scripts/ascii_ledger.py --workspace <agent-workspace-abs> --target <target-rel>
```

- `--workspace`: absolute agent workspace root (where `.grimoire/` lives).
- `--target`: spell target relative to workspace (default `.`). Ledger paths are relative to this.
- Optional: `--ledger`, `--slug` overrides.
- Read-only against git: tree / branch / sync / diff + stale. Does not hunt, lock in, write, or prune `ledger.txt`.
- Do not re-derive status tokens in-session. The ledger script owns them.

## Artifact path

```text
<agent-workspace>/.grimoire/grim-repo/<slug>/
└─ ledger.txt   # written after lock-in only
```

- Agent workspace root, not the target repo.
- `slug`: target path relative to agent workspace; strip trailing `/`; replace `/` with `-`.
  - `projects/next.js` -> `projects-next.js`
  - `knowledge` -> `knowledge`
  - workspace root (`.`) -> repository `name`
- Same-slug regenerate: replace `ledger.txt` entirely after new lock-in. Do not patch or merge.
- Subsequent runs: reuse `ledger.txt`; do not rewrite unless regenerating.

## Ledger

`ledger.txt` stores only the repo paths the user locked in - one path per line:

```text
./
projects/dotfiles/
projects/grimoire/
```

- Paths are relative to the spell target; directories keep a trailing `/`.
- Order is lock-in order (user selection order, or shallow-first when `all`).
- Do not store status, branch, sync, purpose, or other derived fields.

### Lock-in

After hunt script output, prompt before writing:

1. Emit a numbered candidate list from hunt stdout (relative paths).
2. Closed choices: `all`, indices (e.g. `1 3 4`), or `abort`.
3. On `abort`: stop; write nothing.
4. On lock-in: write `ledger.txt` with the selected paths only, then run the ledger script.

## Output

1. Emit the ledger script stdout as an ASCII ledger in a `text` fence.
2. Return a link to the `ledger.txt` path written or reused.
3. If any path was stale: ask whether to regenerate.

## Constraints

- Discovery is hunt-script only on first run or explicit regenerate. No in-session `find`. No deep code intelligence.
- Hunt `--target` must be absolute (spell target).
- Do not honor `.gitignore`. Never descend into `.git` internals.
- Prefer salience over completeness. Cap hunt at depth `N` and budget `R`.
- Chat renders live status via the ledger script; durable file stores paths only.
- Never auto-edit or prune `ledger.txt` on stale paths.
- Do not invent status tokens in-session.

---

## Status

Closed token set (ledger-script-owned). Four child lines under each **valid** repo root:

| Line | Slot | Values |
| --- | --- | --- |
| 1 | tree | `clean` or `dirty` |
| 2 | branch | current branch name, or `DETACHED@<shortsha>` |
| 3 | sync | `↑N ↓N`, `no-up`, or `no-remote` |
| 4 | diff | `+N -M` |

- `dirty` = any unstaged, staged, or untracked change.
- `↑N ↓N` = ahead/behind configured upstream only.
- `no-up` = remotes exist but no upstream for the current branch.
- `no-remote` = no remotes.
- `+N -M` = working-tree line churn vs `HEAD` (staged + unstaged); untracked text lines count as `+`. Binary files skipped.
- No stash counts, ages, remote URLs, or other fields in v1.

---

## ASCII

North star for ledger script output (not a rigid template):

```text
repo1/ ◀─ repo1
├─▶ dirty
├─▶ main
├─▶ ↑1 ↓0
└─▶ +12 -3

repo2/ ◀─ repo2
├─▶ dirty
├─▶ feat/branch
├─▶ ↑30 ↓6
└─▶ +400 -12

path/to/repo/repo3/ ◀─ repo3
├─▶ clean
├─▶ main
├─▶ ↑0 ↓0
└─▶ +0 -0
```

- Root line: `<repo-path>/ ◀─ <repo-name>`; `<repo-name>` is the final directory name.
- Child markers: `├─▶` then `└─▶` on the final sibling.
- Child order fixed: tree, branch, sync, diff.
- Paths relative to the spell target; directories keep trailing `/`.
- Stale paths listed after valid blocks, not as status children.
