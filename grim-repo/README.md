# grim-repo

_Reveal the repos underfoot._

Hunt nested git repositories, lock in which to track, then emit an at-a-glance status board in chat.

## Shape

1. Resolve the target.
2. Reuse ledger lock-in or discover + lock-in.
3. Draw ledger and emit output.

Lock-in under `.grimoire/grim-repo/`; status is live each run.

## Scripts

| File | Role |
| --- | --- |
| [scripts/discover.py](scripts/discover.py) | Nested repo discovery |
| [scripts/ledger.py](scripts/ledger.py) | Live status ledger |
