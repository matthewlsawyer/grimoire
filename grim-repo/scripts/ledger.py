#!/usr/bin/env python3
"""
Read-only helper for `/grim-repo`: recompute ASCII ledger blocks from ledger.txt.

- Reads `.grimoire/grim-repo/<slug>/ledger.txt` (locked-in paths only)
- Validates which paths are still git roots under the spell target
- Runs git status probes and prints the ledger in the skill format
  (tree / branch / sync / diff + stale)
- Does not hunt, lock in, write, or prune the ledger
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
    repo_leaf: str
    tree_token: str
    branch_token: str
    sync_token: str
    diff_token: str


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


def is_git_root(repo_path: str) -> bool:
    git_entry = os.path.join(repo_path, ".git")
    return os.path.isdir(git_entry) or os.path.isfile(git_entry)


def slug_for_target(target_rel: str, workspace: str) -> str:
    """
    Artifact slug for a target relative to the agent workspace.
    Workspace root (`.`) -> repository basename.
    Otherwise: strip trailing `/`, replace `/` with `-`.
    """
    rel = target_rel.strip()
    if rel in ("", ".", "./"):
        return os.path.basename(workspace.rstrip("/"))
    return rel.strip("/").replace("/", "-")


def resolve_repo(rel: str, target_root: str) -> Tuple[str, str, str]:
    """Return (absolute_path, display_path, leaf_name) for a ledger entry."""
    if rel == "./":
        leaf = os.path.basename(target_root.rstrip("/"))
        return target_root, "./", leaf
    display = rel.rstrip("/") + "/"
    leaf = os.path.basename(rel.rstrip("/"))
    return os.path.join(target_root, rel), display, leaf


def token_tree(repo_path: str) -> str:
    code, porcelain = run(["git", "status", "--porcelain=v1"], cwd=repo_path)
    if code != 0:
        raise RuntimeError(f"git status failed in {repo_path}")
    return "dirty" if porcelain else "clean"


def token_branch(repo_path: str) -> str:
    # Detached if HEAD is not a symbolic ref.
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

    # @{upstream}...HEAD => left=behind, right=ahead
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
            continue  # binary
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
                    continue  # binary
                fh.seek(0)
                total += sum(1 for _ in fh)
        except OSError:
            continue
    return total


def token_diff(repo_path: str) -> str:
    """Working-tree line churn vs HEAD, plus untracked text lines as additions."""
    code, out = run(["git", "diff", "--numstat", "HEAD"], cwd=repo_path)
    if code != 0:
        # No HEAD yet (empty / unborn): fall back to staged + unstaged.
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


def render_block(block: RepoBlock) -> str:
    return "\n".join(
        [
            f"{block.repo_display} ◀─ {block.repo_leaf}",
            f"├─▶ {block.tree_token}",
            f"├─▶ {block.branch_token}",
            f"├─▶ {block.sync_token}",
            f"└─▶ {block.diff_token}",
        ]
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Recompute grim-repo ASCII ledger from ledger.txt")
    ap.add_argument(
        "--workspace",
        default=".",
        help="Agent workspace root (where .grimoire/ lives). Default: cwd.",
    )
    ap.add_argument(
        "--target",
        default=".",
        help="Spell target relative to workspace (ledger paths are relative to this). Default: .",
    )
    ap.add_argument(
        "--ledger",
        default="",
        help="Direct path to ledger.txt. If omitted, uses .grimoire/grim-repo/<slug>/ledger.txt.",
    )
    ap.add_argument(
        "--slug",
        default="",
        help="Override artifact slug (default derived from --target).",
    )
    args = ap.parse_args()

    workspace = os.path.abspath(args.workspace)
    target_root = os.path.abspath(os.path.join(workspace, args.target))
    if not os.path.isdir(target_root):
        print(f"target not found: {target_root}", file=sys.stderr)
        return 2

    slug = args.slug or slug_for_target(args.target, workspace)
    ledger_path = (
        os.path.abspath(args.ledger)
        if args.ledger
        else os.path.join(workspace, ".grimoire", "grim-repo", slug, "ledger.txt")
    )

    if not os.path.isfile(ledger_path):
        print(f"ledger.txt not found: {ledger_path}", file=sys.stderr)
        return 2

    with open(ledger_path, "r", encoding="utf-8") as f:
        rel_paths = [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]

    if not rel_paths:
        print(f"ledger.txt is empty: {ledger_path}", file=sys.stderr)
        return 3

    blocks: List[RepoBlock] = []
    stale: List[str] = []
    errors: List[str] = []

    for rel in rel_paths:
        repo_path, repo_display, repo_leaf = resolve_repo(rel, target_root)
        if not is_git_root(repo_path):
            stale.append(rel)
            continue
        try:
            blocks.append(
                RepoBlock(
                    repo_display=repo_display,
                    repo_leaf=repo_leaf,
                    tree_token=token_tree(repo_path),
                    branch_token=token_branch(repo_path),
                    sync_token=token_sync(repo_path),
                    diff_token=token_diff(repo_path),
                )
            )
        except RuntimeError as e:
            errors.append(str(e))

    if blocks:
        print("\n\n".join(render_block(b) for b in blocks))

    if stale:
        if blocks:
            print()
        print("\nStale paths (not git roots anymore):")
        for s in stale:
            print(f"- {s}")

    if errors:
        for err in errors:
            print(err, file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
