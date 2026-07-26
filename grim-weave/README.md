# grim-weave

_Follow the thread._

Given a file path, symbol, or concept phrase, collect bounded evidence then reason into one at-a-glance **ledger** in chat.

grim-weave follows a single concept through a repository, revealing its provenance, relationships, and supporting evidence. Starting from a symbol, file, or concept, it produces a deterministic thread showing where it is defined, what it depends on, what depends on it, how it evolved, and where it is documented.

## Shape

1. Resolve target and token.
2. Run weave collector (JSON evidence).
3. Read only the closed path set; infer relationships from file contents.
4. Emit Weave Ledger + short evidence notes.

Viewport is the spell. Collection is reproducible; the ledger is agent-composed from that evidence.

## Usage

```text
/grim-weave grim-scry

/grim-weave projects/grimoire grim-scry

/grim-weave discover.py

/grim-weave "log in"
```

| Token shape | Classified as |
| --- | --- |
| `path/to/file.go`, `SKILL.md` | file |
| `TodoService` | symbol |
| `log in`, multi-word phrase | concept |

## Evidence contract

`weave.py` stdout fields:

| Field | Role |
| --- | --- |
| `token_kind` | `file`, `symbol`, or `concept` |
| `paths` | Closed set of repo-relative paths to read |
| `hits` | Line matches (case-insensitive for symbol and concept); `definition_candidate` when declaration-shaped |
| `documents` | Doc-path subset of hits |
| `commits` | Short sha + subject when git is available; newest first, max 5 |
| `commits_order` | Always `newest_first` when commits are present |
| `git_available` | `false` -> Provenance commits stay empty |

## Scripts

| File | Role |
| --- | --- |
| [scripts/weave.py](scripts/weave.py) | Deterministic evidence JSON |
