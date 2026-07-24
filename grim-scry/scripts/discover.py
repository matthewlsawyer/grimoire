#!/usr/bin/env python3
"""
Deterministic discovery for `/grim-scry`.

List-then-filter pipeline:
  list paths -> (git ignore via ls-files, or plain walk)
  -> basename seed filter -> rank -> budget K
  -> flat seed paths on stdout (one per line)

Does not read seed contents, distill, or write artifacts. Emits to stdout only.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from typing import Iterable, List, Optional, Sequence


def find_git_root(start: str) -> Optional[str]:
    cur = os.path.abspath(start)
    while True:
        if os.path.isdir(os.path.join(cur, ".git")) or os.path.isfile(
            os.path.join(cur, ".git")
        ):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return None
        cur = parent


def to_display_file(rel: str) -> str:
    rel = rel.replace(os.sep, "/").lstrip("/")
    return "./" + rel if not rel.startswith("./") else rel


def segments(rel_path: str) -> List[str]:
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


def list_files_git(target_root: str, git_root: str) -> List[str]:
    """Tracked + untracked non-ignored files under target, as ./rel display paths."""
    proc = subprocess.run(
        [
            "git",
            "-C",
            git_root,
            "ls-files",
            "-z",
            "--cached",
            "--others",
            "--exclude-standard",
        ],
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        return []

    try:
        target_from_git = os.path.relpath(target_root, git_root)
    except ValueError:
        return []
    if target_from_git.startswith(".."):
        return []

    if target_from_git == ".":
        prefix = ""
    else:
        prefix = target_from_git.replace(os.sep, "/") + "/"

    out: List[str] = []
    for raw in proc.stdout.split(b"\0"):
        if not raw:
            continue
        try:
            path = raw.decode("utf-8", errors="surrogateescape")
        except Exception:
            continue
        path = path.replace(os.sep, "/")
        if path == ".git" or path.startswith(".git/") or "/.git/" in path:
            continue
        if any(seg == ".git" for seg in path.split("/")):
            continue
        if prefix and not path.startswith(prefix):
            continue
        local = path[len(prefix) :] if prefix else path
        if not local or local.endswith("/"):
            continue
        out.append(to_display_file(local))
    return out


def list_files_walk(target_root: str) -> List[str]:
    """All files under target via os.walk. No deny list; prune .git basename; skip symlinks."""
    out: List[str] = []
    for dirpath, dirnames, filenames in os.walk(target_root, followlinks=False):
        keep: List[str] = []
        for name in dirnames:
            if name == ".git":
                continue
            child = os.path.join(dirpath, name)
            if os.path.islink(child):
                continue
            keep.append(name)
        dirnames[:] = keep

        for name in filenames:
            child = os.path.join(dirpath, name)
            if os.path.islink(child):
                continue
            rel = os.path.relpath(child, target_root).replace(os.sep, "/")
            out.append(to_display_file(rel))
    return out


def list_files(target_root: str) -> List[str]:
    git_root = find_git_root(target_root)
    if git_root is not None:
        return list_files_git(target_root, git_root)
    return list_files_walk(target_root)


def collect_seeds(files: Iterable[str]) -> List[str]:
    seeds: List[str] = []
    for f in files:
        name = segments(f)[-1] if segments(f) else ""
        if name and is_seed_file(name):
            seeds.append(f)
    return sorted(set(seeds), key=lambda p: (len(segments(p)), p))


def rank_seeds(candidates: Sequence[str], budget: int) -> List[str]:
    if budget < 1:
        return []
    return sorted(candidates, key=lambda p: (len(segments(p)), p))[:budget]


def discover(target_root: str, budget: int) -> List[str]:
    files = list_files(target_root)
    return rank_seeds(collect_seeds(files), budget=budget)


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
        default=20,
        help="Max ranked seed paths to emit (default 20).",
    )
    args = ap.parse_args()

    if args.budget < 1:
        print("--budget must be >= 1", file=sys.stderr)
        return 2

    target_root = os.path.abspath(args.target)
    if not os.path.isdir(target_root):
        print(f"target not found: {target_root}", file=sys.stderr)
        return 2

    seeds = discover(target_root, budget=args.budget)
    for p in seeds:
        print(p)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
