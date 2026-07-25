#!/usr/bin/env python3
"""
Read-only helper for `/grim-repo`: nested git roots under a target via find(1).

- find for `.git` dirs (pruned) and `.git` submodule pointer files
- Emits relative paths (trailing `/`), shallow-first
- Does not prompt, write ledger.txt, or run status
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys


def rel_display(target_root: str, repo_abs: str) -> str:
    rel = os.path.relpath(repo_abs, target_root)
    if rel in (".", ""):
        return "./"
    return rel.replace(os.sep, "/") + "/"


def discover(target_root: str) -> list[str]:
    proc = subprocess.run(
        [
            "find",
            target_root,
            "(",
            "-name",
            ".git",
            "-type",
            "d",
            "-prune",
            "-print",
            ")",
            "-o",
            "(",
            "-name",
            ".git",
            "-type",
            "f",
            "-print",
            ")",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode not in (0, 1):
        print(proc.stderr or "find failed", file=sys.stderr)
        return []

    found: list[str] = []
    seen: set[str] = set()
    for line in proc.stdout.splitlines():
        git_path = line.strip()
        if not git_path:
            continue
        repo_abs = os.path.dirname(git_path)
        key = os.path.realpath(repo_abs)
        if key in seen:
            continue
        seen.add(key)
        found.append(rel_display(target_root, repo_abs))

    found.sort(key=lambda p: (p.count("/"), p))
    return found


def main() -> int:
    ap = argparse.ArgumentParser(description="Find nested git roots under a target")
    ap.add_argument(
        "--target",
        default=".",
        help="Directory to search under. Default: cwd.",
    )
    args = ap.parse_args()

    target_root = os.path.abspath(args.target)
    if not os.path.isdir(target_root):
        print(f"target not found: {target_root}", file=sys.stderr)
        return 2

    for path in discover(target_root):
        print(path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
