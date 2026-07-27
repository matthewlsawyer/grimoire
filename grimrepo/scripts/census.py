#!/usr/bin/env python3
"""
Read-only helper for `/grim-repo`: live nested-repo census.

Finds every git root under a target directory, collects branch, upstream sync,
and working-tree diff metrics per repo, then renders one Unicode status board.

Pipeline:
  1. find(1) for `.git` files and directories
  2. Per repo: branch (or detached), ahead/behind, numstat diff + untracked lines
  3. render_census() draws the board (agent fences stdout as-is)

Glyphs: `▲` sync and diff metrics; `●` branch name.

Example stdout::

    throneroom/
    ╞══════════════════◆
    │
    ├─ ./
    │  ├─▲ ↑0 ↓0
    │  ├─▲ +0 -0
    │  └─● main
    │
    └─ projects/dotfiles/
       ├─▲ ↑0 ↓0
       ├─▲ +8 -8
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
    """One repo row on the census board: display path and three status tokens."""

    repo_display: str
    branch_token: str
    diff_token: str
    sync_token: str


def run(cmd: List[str], cwd: str) -> Tuple[int, str]:
    """Run a subprocess with C locale; return (exit_code, stdout stripped)."""
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
    """Format a repo absolute path as a display path ending in `/` (or `./`)."""
    rel = os.path.relpath(repo_abs, target_root)
    if rel in (".", ""):
        return "./"
    return rel.replace(os.sep, "/") + "/"


def discover_roots(target_root: str) -> List[str]:
    """
    Find nested git repository roots under target via find(1).

    Handles `.git` as directory or gitfile. Returns sorted display paths
    (shallow paths first). Dedupes by realpath of repo root.
    """
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
    """Map a census display path to (absolute_repo_path, display_path_with_slash)."""
    if rel == "./":
        return target_root, "./"
    display = rel.rstrip("/") + "/"
    return os.path.join(target_root, rel.rstrip("/")), display


def token_branch(repo_path: str) -> str:
    """
    Current branch name, or DETACHED@<shortsha> when HEAD is not a symbolic ref.

    Raises RuntimeError when git cannot resolve HEAD.
    """
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
    """
    Upstream sync summary: `↑ahead ↓behind`, or `no-remote` / `no-up`.

    Uses @{upstream}...HEAD rev-list counts. Raises RuntimeError on git failure.
    """
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
    """Sum added/deleted line counts from git diff --numstat output."""
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
    """
    Count lines in untracked non-binary files (git ls-files -o).

    Binary files are skipped when the first 4KiB contains a null byte.
    """
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
    """
    Working tree delta vs HEAD as `+added -deleted` including untracked line count.

    Falls back to unstaged + staged numstat when diff against HEAD is unavailable.
    """
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
    """
    Draw the grim-repo status board for all RepoBlock rows.

    target_leaf is the basename of the search root (header line). Each repo shows
    sync (▲), diff (▲), then branch (●). Deterministic for a given blocks list.
    """
    lines: List[str] = [
        f"{target_leaf}/",
        "╞══════════════════◆",
        "│",
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
    """CLI entry: discover repos under --target, print board or errors to stderr."""
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
