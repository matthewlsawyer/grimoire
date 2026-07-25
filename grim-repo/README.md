# grim-repo

_What lives must be named._

Inject a live nested-repo status board into the session: every git root under the target, with branch and working-tree deltas.

## Shape

1. Resolve the target.
2. Run census (find roots + status draw).
3. Emit the board in chat.

## Usage

Invoke the skill directly to see the census.

```text
/grim-repo
```

### Reason with the census

The census is a fact surface -> dirty trees, branches, which nested root is which.

The spell earns its place when used in session: where to work, what is out of sync; ask questions and let it help guide your next step.

## Example output

`census.py` stdout (agent fences as-is):

```text
throneroom/
╞══════════════════◆
├─ ./
│  ├─▲ ↑0 ↓0
│  ├─▲ +0 -0
│  └─● main
│
├─ projects/dotfiles/
│  ├─▲ ↑1 ↓0
│  ├─▲ +8 -8
│  └─● main
│
└─ projects/site/
   ├─▲ ↑0 ↓2
   ├─▲ +82 -2
   └─● main
```

- `▲` working-tree delta vs HEAD
- `▲` commits ahead/behind configured upstream (`↑N ↓N`, or `no-up` / `no-remote`)
- `●` current branch per repo

## Scripts

| File | Role |
| --- | --- |
| [scripts/census.py](scripts/census.py) | Find nested git roots + live status board |
