#!/usr/bin/env python3
"""
Read-only helper for `/grim-repo`: live nested-repo census.

- find(1) for nested `.git` roots, then branch + diff per repo
- Unicode board format (diff / branch)
- Glyphs: `▲` status (diff metric, ahead/behind), `●` state (branch)

Example stdout::

    throneroom/
    ╞══════════════════◆
    ├─ ./
    │  ├─▲ ↑0 ↓0
    │  ├─▲ +0 -0
    │  └─● main
    │
    └─ projects/site/
    │  ├─▲ ↑1 ↓0
       ├─▲ +3 -9
       └─● main
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class RepoBlock:
    repo_display: str
    branch_token: str
    diff_token: str
    sync_token: str


def run(cmd: List[str], cwd: str) -> Tuple[int, str]:
    env = {**os.environ, "LC_ALL": "C", "LANG": "C"}
    p = subprocess.run(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        check=False,
        env=env,
    )
    return p.returncode, (p.stdout or "").strip()


def _rel_display(target_root: str, repo_abs: str) -> str:
    rel = os.path.relpath(repo_abs, target_root)
    if rel in (".", ""):
        return "./"
    return rel.replace(os.sep, "/") + "/"


def discover_roots(target_root: str) -> List[str]:
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

    found: List[str] = []
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
        found.append(_rel_display(target_root, repo_abs))

    found.sort(key=lambda p: (p.count("/"), p))
    return found


def resolve_repo(rel: str, target_root: str) -> Tuple[str, str]:
    """Return (absolute_path, display_path) for a repo root relative to target."""
    if rel == "./":
        return target_root, "./"
    display = rel.rstrip("/") + "/"
    return os.path.join(target_root, rel.rstrip("/")), display


def token_branch(repo_path: str) -> str:
    code, _ = run(["git", "symbolic-ref", "-q", "HEAD"], cwd=repo_path)
    if code != 0:
        sha_code, shortsha = run(["git", "rev-parse", "--short=7", "HEAD"], cwd=repo_path)
        if sha_code != 0 or not shortsha:
            raise RuntimeError(f"git rev-parse failed in {repo_path}")
        return f"DETACHED@{shortsha}"

    code, branch = run(["git", "branch", "--show-current"], cwd=repo_path)
    if code != 0 or not branch:
        raise RuntimeError(f"git branch --show-current failed in {repo_path}")
    return branch


def token_sync(repo_path: str) -> str:
    code, remotes = run(["git", "remote"], cwd=repo_path)
    if code != 0:
        raise RuntimeError(f"git remote failed in {repo_path}")
    if not remotes:
        return "no-remote"

    up_code, _ = run(["git", "rev-parse", "--abbrev-ref", "@{upstream}"], cwd=repo_path)
    if up_code != 0:
        return "no-up"

    count_code, counts = run(
        ["git", "rev-list", "--left-right", "--count", "@{upstream}...HEAD"],
        cwd=repo_path,
    )
    if count_code != 0 or not counts:
        raise RuntimeError(f"git rev-list failed in {repo_path}")

    parts = counts.split()
    if len(parts) != 2:
        raise RuntimeError(f"unexpected rev-list output in {repo_path}: {counts!r}")
    behind, ahead = parts
    return f"↑{ahead} ↓{behind}"


def _sum_numstat(text: str) -> Tuple[int, int]:
    added = 0
    deleted = 0
    for line in text.splitlines():
        parts = line.split("\t", 2)
        if len(parts) < 2:
            continue
        a, d = parts[0], parts[1]
        if a == "-" or d == "-":
            continue
        added += int(a)
        deleted += int(d)
    return added, deleted


def _count_untracked_lines(repo_path: str) -> int:
    code, files = run(["git", "ls-files", "-o", "--exclude-standard"], cwd=repo_path)
    if code != 0 or not files:
        return 0
    total = 0
    for rel in files.splitlines():
        path = os.path.join(repo_path, rel)
        if not os.path.isfile(path):
            continue
        try:
            with open(path, "rb") as fh:
                sample = fh.read(4096)
                if b"\0" in sample:
                    continue
                fh.seek(0)
                total += sum(1 for _ in fh)
        except OSError:
            continue
    return total


def token_diff(repo_path: str) -> str:
    code, out = run(["git", "diff", "--numstat", "HEAD"], cwd=repo_path)
    if code != 0:
        _, unstaged = run(["git", "diff", "--numstat"], cwd=repo_path)
        _, staged = run(["git", "diff", "--cached", "--numstat"], cwd=repo_path)
        added, deleted = _sum_numstat(unstaged)
        a2, d2 = _sum_numstat(staged)
        added += a2
        deleted += d2
    else:
        added, deleted = _sum_numstat(out)

    added += _count_untracked_lines(repo_path)
    return f"+{added} -{deleted}"


def render_census(target_leaf: str, blocks: List[RepoBlock]) -> str:
    """Forest under target leaf: divider, then repos with ▲ diff, ▲ sync, ● branch."""
    lines: List[str] = [
        f"{target_leaf}/",
        "╞══════════════════◆",
    ]
    n = len(blocks)
    for i, block in enumerate(blocks):
        last = i == n - 1
        branch = "└─" if last else "├─"
        gutter = "   " if last else "│  "
        lines.append(f"{branch} {block.repo_display}")
        lines.append(f"{gutter}├─▲ {block.sync_token}")
        lines.append(f"{gutter}├─▲ {block.diff_token}")
        lines.append(f"{gutter}└─● {block.branch_token}")
        if not last:
            lines.append("│")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Live grim-repo status board under a target")
    ap.add_argument(
        "--target",
        default=".",
        help="Directory to search under. Skill should pass an absolute path.",
    )
    args = ap.parse_args()

    target_root = os.path.abspath(args.target)
    if not os.path.isdir(target_root):
        print(f"target not found: {target_root}", file=sys.stderr)
        return 2

    rel_paths = discover_roots(target_root)
    blocks: List[RepoBlock] = []
    errors: List[str] = []

    for rel in rel_paths:
        repo_path, repo_display = resolve_repo(rel, target_root)
        try:
            blocks.append(
                RepoBlock(
                    repo_display=repo_display,
                    branch_token=token_branch(repo_path),
                    diff_token=token_diff(repo_path),
                    sync_token=token_sync(repo_path),
                )
            )
        except RuntimeError as e:
            errors.append(str(e))

    if blocks:
        target_leaf = os.path.basename(target_root.rstrip("/"))
        print(render_census(target_leaf, blocks))

    if errors:
        for err in errors:
            print(err, file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
