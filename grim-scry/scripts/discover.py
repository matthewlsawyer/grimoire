#!/usr/bin/env python3
"""
Deterministic discovery for `/grim-scry` via find(1).

- find for seed basenames under target; does not honor gitignore
- Prunes known vendor/build/cache dir names (see PRUNE_DIR_NAMES); skips symlinks via find default
- Seed basenames from SEED_BASENAME_PATTERNS (find -iname + post-filter)
- Shallow-first sort -> budget K
- Flat seed paths on stdout (one per line)

Does not read seed contents, distill, or write artifacts.
"""

from __future__ import annotations

import argparse
import fnmatch
import os
import subprocess
import sys

# Directory names: any path segment match prunes the subtree (find + post-filter).
PRUNE_DIR_NAMES: frozenset[str] = frozenset(
    {
        ".git",
        "node_modules",
        "vendor",
        ".venv",
        "venv",
        "__pycache__",
        ".pnpm-store",
        ".yarn",
        "dist",
        "build",
        "_site",
        ".next",
        ".nuxt",
        "target",
        "coverage",
        ".turbo",
    }
)

# Basename globs for seed files (-iname in find; case-insensitive fnmatch in Python).
SEED_BASENAME_PATTERNS: tuple[str, ...] = (
    "readme",
    "readme.*",
    "agents.md",
    "agents*.md",
    "claude.md",
    "skill.md",
    "index",
    "index.md",
    "index.yaml",
    "index.yml",
    "index.json",
)


def to_display_file(rel: str) -> str:
    rel = rel.replace(os.sep, "/").lstrip("/")
    return "./" + rel if not rel.startswith("./") else rel


def segments(rel_path: str) -> list[str]:
    p = rel_path[2:] if rel_path.startswith("./") else rel_path
    p = p.rstrip("/")
    return [s for s in p.split("/") if s]


def is_under_pruned_dir(rel_path: str) -> bool:
    parts = segments(rel_path)
    if len(parts) <= 1:
        return False
    return any(part in PRUNE_DIR_NAMES for part in parts[:-1])


def is_seed_file(name: str) -> bool:
    lower = name.lower()
    return any(fnmatch.fnmatch(lower, pattern.lower()) for pattern in SEED_BASENAME_PATTERNS)


def _find_or_name_args(names: frozenset[str] | tuple[str, ...]) -> list[str]:
    ordered = sorted(names) if isinstance(names, frozenset) else list(names)
    args: list[str] = ["("]
    for i, name in enumerate(ordered):
        if i > 0:
            args.append("-o")
        args.extend(["-name", name])
    args.append(")")
    return args


def _find_or_iname_args(patterns: tuple[str, ...]) -> list[str]:
    args: list[str] = ["("]
    for i, pattern in enumerate(patterns):
        if i > 0:
            args.append("-o")
        args.extend(["-iname", pattern])
    args.append(")")
    return args


def _find_prune_args() -> list[str]:
    return [*_find_or_name_args(PRUNE_DIR_NAMES), "-type", "d", "-prune"]


def find_candidates(target_root: str) -> list[str]:
    """Absolute paths from find(1); prune vendor/build dirs; match seed basenames."""
    proc = subprocess.run(
        [
            "find",
            target_root,
            *_find_prune_args(),
            "-o",
            "(",
            "-type",
            "f",
            *_find_or_iname_args(SEED_BASENAME_PATTERNS),
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
        rel = os.path.relpath(abs_path, target_root)
        display = to_display_file(rel)
        if is_under_pruned_dir(display):
            continue
        key = os.path.realpath(abs_path)
        if key in seen:
            continue
        seen.add(key)
        found.append(display)

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
        default=50,
        help="Max ranked seed paths to emit (default 50).",
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
