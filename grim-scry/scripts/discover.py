#!/usr/bin/env python3
"""
Deterministic discovery for `/grim-scry`.

List-then-filter pipeline:
  list paths -> (git ignore via ls-files, or plain walk)
  -> split:
       dirs:  depth N + fan-out width W -> ## dirs
       seeds: basename filter -> rank -> budget K -> ## seeds

Does not read seed contents, distill, or write artifacts. Emits to stdout only.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple


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


def to_display_dir(rel: str) -> str:
    rel = rel.replace(os.sep, "/").strip("/")
    if not rel:
        return "./"
    return "./" + rel + "/"


def segments(rel_path: str) -> List[str]:
    p = rel_path[2:] if rel_path.startswith("./") else rel_path
    p = p.rstrip("/")
    return [s for s in p.split("/") if s]


def parent_key(dir_display: str) -> str:
    segs = segments(dir_display)
    if len(segs) <= 1:
        return "./"
    return to_display_dir("/".join(segs[:-1]))


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
        # Basename prune .git; skip symlink dirs
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


def dirs_from_files(files: Iterable[str]) -> Set[str]:
    dirs: Set[str] = set()
    for f in files:
        segs = segments(f)
        for i in range(1, len(segs)):
            dirs.add(to_display_dir("/".join(segs[:i])))
    return dirs


def filter_dirs(dirs: Set[str], depth: int, width: int) -> List[str]:
    """Keep dirs with 1..depth segments; collapse children when sibling count > width."""
    if depth < 1:
        return []

    candidates = [d for d in dirs if 1 <= len(segments(d)) <= depth]

    by_parent: Dict[str, List[str]] = {}
    for d in candidates:
        by_parent.setdefault(parent_key(d), []).append(d)

    # Shallow parents first: collapse fat sibling sets; drop those children and descendants.
    collapsed: Set[str] = set()
    for parent in sorted(by_parent.keys(), key=lambda p: len(segments(p))):
        if any(parent == c or parent.startswith(c) for c in collapsed):
            continue
        children = by_parent[parent]
        if len(children) > width:
            for c in children:
                collapsed.add(c)

    kept: List[str] = []
    for d in candidates:
        if any(d == c or d.startswith(c) for c in collapsed):
            continue
        kept.append(d)

    return sorted(set(kept), key=lambda p: (segments(p), p))


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


def discover(
    target_root: str, depth: int, budget: int, dir_width: int
) -> Tuple[List[str], List[str]]:
    files = list_files(target_root)
    dirs = filter_dirs(dirs_from_files(files), depth=depth, width=dir_width)
    seeds = rank_seeds(collect_seeds(files), budget=budget)
    return dirs, seeds


def main() -> int:
    ap = argparse.ArgumentParser(
        description=(
            "Discover dirs (depth + width capped) and ranked seed paths for grim-scry"
        )
    )
    ap.add_argument(
        "--target",
        default=".",
        help="Directory to discover under. Skill should pass an absolute path.",
    )
    ap.add_argument(
        "--depth",
        type=int,
        default=3,
        help="Max directory depth to emit in ## dirs (default 3).",
    )
    ap.add_argument(
        "--budget",
        type=int,
        default=20,
        help="Max ranked seed paths to emit (default 20).",
    )
    ap.add_argument(
        "--dir-width",
        type=int,
        default=25,
        help="Max sibling dirs emitted per parent; collapse when exceeded (default 25).",
    )
    args = ap.parse_args()

    if args.depth < 0:
        print("--depth must be >= 0", file=sys.stderr)
        return 2
    if args.budget < 1:
        print("--budget must be >= 1", file=sys.stderr)
        return 2
    if args.dir_width < 1:
        print("--dir-width must be >= 1", file=sys.stderr)
        return 2

    target_root = os.path.abspath(args.target)
    if not os.path.isdir(target_root):
        print(f"target not found: {target_root}", file=sys.stderr)
        return 2

    dirs, seeds = discover(
        target_root,
        depth=args.depth,
        budget=args.budget,
        dir_width=args.dir_width,
    )

    print("## dirs")
    for p in dirs:
        print(p)
    print()
    print("## seeds")
    for p in seeds:
        print(p)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
