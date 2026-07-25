#!/usr/bin/env python3
"""
Deterministic discovery for `/grim-scry` via find(1).

- find for seed basenames under target; does not honor gitignore
- Prunes `.git` dirs only (speed); skips symlinks via find default
- Basename post-filter -> shallow-first sort -> budget K
- Flat seed paths on stdout (one per line)

Does not read seed contents, distill, or write artifacts.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys


def to_display_file(rel: str) -> str:
    rel = rel.replace(os.sep, "/").lstrip("/")
    return "./" + rel if not rel.startswith("./") else rel


def segments(rel_path: str) -> list[str]:
    p = rel_path[2:] if rel_path.startswith("./") else rel_path
    p = p.rstrip("/")
    return [s for s in p.split("/") if s]


def is_seed_file(name: str) -> bool:
    lower = name.lower()
    if lower == "readme" or lower.startswith("readme."):
        return True
    if name in {"AGENTS.md", "CLAUDE.md"} or lower in {"agents.md", "claude.md"}:
        return True
    if name == "SKILL.md" or lower == "skill.md":
        return True
    if lower in {"index", "index.md", "index.yaml", "index.yml", "index.json"}:
        return True
    if name.endswith(".md") and name.upper().startswith("AGENTS"):
        return True
    return False


def find_candidates(target_root: str) -> list[str]:
    """Absolute paths from find(1); prune .git; match seed basenames."""
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
            ")",
            "-o",
            "(",
            "-type",
            "f",
            "(",
            "-iname",
            "readme",
            "-o",
            "-iname",
            "readme.*",
            "-o",
            "-iname",
            "agents.md",
            "-o",
            "-iname",
            "agents*.md",
            "-o",
            "-iname",
            "claude.md",
            "-o",
            "-iname",
            "skill.md",
            "-o",
            "-iname",
            "index",
            "-o",
            "-iname",
            "index.md",
            "-o",
            "-iname",
            "index.yaml",
            "-o",
            "-iname",
            "index.yml",
            "-o",
            "-iname",
            "index.json",
            ")",
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
    return [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]


def discover(target_root: str, budget: int) -> list[str]:
    if budget < 1:
        return []

    found: list[str] = []
    seen: set[str] = set()
    for abs_path in find_candidates(target_root):
        name = os.path.basename(abs_path)
        if not is_seed_file(name):
            continue
        key = os.path.realpath(abs_path)
        if key in seen:
            continue
        seen.add(key)
        rel = os.path.relpath(abs_path, target_root)
        found.append(to_display_file(rel))

    found.sort(key=lambda p: (len(segments(p)), p))
    return found[:budget]


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Discover ranked seed paths for grim-scry (flat stdout)"
    )
    ap.add_argument(
        "--target",
        default=".",
        help="Directory to discover under. Skill should pass an absolute path.",
    )
    ap.add_argument(
        "--budget",
        type=int,
        default=25,
        help="Max ranked seed paths to emit (default 25).",
    )
    args = ap.parse_args()

    if args.budget < 1:
        print("--budget must be >= 1", file=sys.stderr)
        return 2

    target_root = os.path.abspath(args.target)
    if not os.path.isdir(target_root):
        print(f"target not found: {target_root}", file=sys.stderr)
        return 2

    for p in discover(target_root, budget=args.budget):
        print(p)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
