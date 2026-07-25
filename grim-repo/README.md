# grim-repo

_What lives must be named._

Inject a live nested-repo status board into the session: every git root under the target, with branch and working-tree deltas.

## Shape

1. Resolve the target.
2. Run ledger (find roots + status draw).
3. Emit the board in chat.

## Reason with the board

The board is a fact surface - dirty trees, branches, which nested root is which.

The spell earns its place when you use it for the rest of the session (where to work, what is out of sync), not when you only reprint it.

## Example output

`ledger.py` stdout (agent fences as-is):

```text
throneroom/
╞══════════════════◆
├─ ./
│  ├─▲ +0 -0
│  └─● main
│
├─ projects/dotfiles/
│  ├─▲ +8 -8
│  └─● main
│
└─ projects/site/
   ├─▲ +82 -2
   └─● main
```

`▲` working-tree delta vs HEAD; `●` current branch per repo.

## Scripts

| File | Role |
| --- | --- |
| [scripts/ledger.py](scripts/ledger.py) | Find nested git roots + live status board |
