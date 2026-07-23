#!/usr/bin/env python3
"""
Read-only helper for `/grim-repo`: hunt nested git roots under a target.

- Walks the filesystem for directories containing `.git/` or a `.git` file
- Does not honor .gitignore; does not follow symlinks; never descends into `.git`
- Emits relative paths (trailing `/`), shallow-first, capped by budget
- Does not prompt, write ledger.txt, or run status
"""

from __future__ import annotations

import argparse
import os
import sys
from collections import deque
from typing import List


def is_git_root(dir_path: str) -> bool:
    git_entry = os.path.join(dir_path, ".git")
    return os.path.isdir(git_entry) or os.path.isfile(git_entry)


def rel_display(target_root: str, abs_path: str) -> str:
    """Path relative to target; `./` for the target itself; trailing `/` otherwise."""
    rel = os.path.relpath(abs_path, target_root)
    if rel in (".", ""):
        return "./"
    return rel.replace(os.sep, "/") + "/"


def hunt(target_root: str, depth: int, budget: int) -> List[str]:
    """
    BFS shallow-first hunt for git roots under target_root.

    depth: max path depth relative to target (target itself is depth 0).
    budget: max candidates to return.
    """
    found: List[str] = []
    seen: set[str] = set()

    # queue items: (abs_dir, depth_from_target)
    q: deque[tuple[str, int]] = deque([(target_root, 0)])

    while q and len(found) < budget:
        current, d = q.popleft()
        try:
            if os.path.islink(current):
                continue
        except OSError:
            continue

        if is_git_root(current):
            key = os.path.realpath(current)
            if key not in seen:
                seen.add(key)
                found.append(rel_display(target_root, current))
            # Still do not descend into .git; may continue into siblings via BFS.
            # Nested repos under this root are still reachable if we walk children
            # (e.g. projects/foo under workspace root). Do not skip children just
            # because current is a git root.

        if d >= depth:
            continue

        try:
            names = os.listdir(current)
        except OSError:
            continue

        for name in sorted(names):
            if name == ".git":
                continue  # never walk into .git internals
            child = os.path.join(current, name)
            try:
                if os.path.islink(child) or not os.path.isdir(child):
                    continue
            except OSError:
                continue
            q.append((child, d + 1))

    return found


def main() -> int:
    ap = argparse.ArgumentParser(description="Hunt nested git roots under a target")
    ap.add_argument(
        "--target",
        default=".",
        help="Directory to hunt under. Default: cwd.",
    )
    ap.add_argument(
        "--depth",
        type=int,
        default=4,
        help="Max walk depth relative to target (default 4).",
    )
    ap.add_argument(
        "--budget",
        type=int,
        default=10,
        help="Max candidate repos to emit, shallow-first (default 10).",
    )
    args = ap.parse_args()

    if args.depth < 0:
        print("--depth must be >= 0", file=sys.stderr)
        return 2
    if args.budget < 1:
        print("--budget must be >= 1", file=sys.stderr)
        return 2

    target_root = os.path.abspath(args.target)
    if not os.path.isdir(target_root):
        print(f"target not found: {target_root}", file=sys.stderr)
        return 2

    for path in hunt(target_root, depth=args.depth, budget=args.budget):
        print(path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
