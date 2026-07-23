# grim-repo

_Reveal the repos underfoot._

Hunt nested git repositories, lock in which to track, then run the ledger script for an at-a-glance ASCII status board. Persist locked-in paths under `.grimoire/grim-repo/`.

## Shape

1. Resolve target: agent workspace root or a path the user named.
2. Lock-in gate:
   - Missing / empty `ledger.txt`, or asked to regenerate: run `scripts/hunt_repos.py` with an absolute `--target` (default depth `N = 4`, budget `R = 10`), then prompt (`all` / indices / `abort`). Write `ledger.txt` only after lock-in.
   - Else reuse `ledger.txt`; skip hunt and questions.
3. Run `scripts/ascii_ledger.py` (tree / branch / sync / diff + stale). Emit stdout in chat.
4. Return a link to `ledger.txt`. If any path was stale, ask whether to regenerate.

## Artifact path

```text
<agent-workspace>/.grimoire/grim-repo/<slug>/
└─ ledger.txt
```

- `slug`: target path relative to agent workspace; strip trailing `/`; replace `/` with `-`.
  - `projects/next.js` -> `projects-next.js`
  - `knowledge` -> `knowledge`
  - workspace root (`.`) -> repository `name`
- `ledger.txt`: one relative repo path per line (directories keep trailing `/`). Status is always live from the ledger script.
- Stale paths: still emit valid repos; note stale; ask regenerate. Never auto-prune.

## Status

| Slot | Values |
| --- | --- |
| tree | `clean` / `dirty` |
| branch | branch name or `DETACHED@<shortsha>` |
| sync | `↑N ↓N` / `no-up` / `no-remote` |
| diff | `+N -M` |

Rendered:

```text
repo1/ ◀─ repo1
├─▶ dirty
├─▶ main
├─▶ ↑1 ↓0
└─▶ +12 -3
```

## Files

| File | Role |
| --- | --- |
| [SKILL.md](SKILL.md) | Lock-in, artifact path, script orchestration |
| [scripts/hunt_repos.py](scripts/hunt_repos.py) | `.git` hunt (candidates only) |
| [scripts/ascii_ledger.py](scripts/ascii_ledger.py) | Live status ledger from `ledger.txt` |
