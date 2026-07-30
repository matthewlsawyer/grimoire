#!/usr/bin/env python3
"""Deterministic `status` evidence for `/grim-forge`."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

PRUNE_DIR_NAMES = frozenset(
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
COMMIT_LIMIT = 250
CHANGELOG_NAME = "CHANGELOG.md"
HISTORY_NAME = "HISTORY.md"
MARKER_PATTERN = re.compile(r"<!--\s*marker:\s*([0-9a-fA-F]+)\s*-->")
RELEASE_TAG = re.compile(r"^v?\d+\.\d+")
COMMIT_FORMAT = "%h%x09%as%x09%s"
RELEASE_FORMAT = "%(refname:strip=2)\t%(objectname:short)\t%(creatordate:short)"


def display(root: Path, path: Path) -> str:
    return "./" + path.relative_to(root).as_posix()


def git_lines(root: Path, *args: str) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.splitlines() if result.returncode == 0 else []


def parse_marker(history_path: Path) -> str | None:
    if not history_path.is_file():
        return None
    match = MARKER_PATTERN.search(history_path.read_text(encoding="utf-8"))
    return match.group(1).lower() if match else None


def parse_commits(lines: list[str]) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for line in lines:
        commit, _, rest = line.partition("\t")
        if not commit:
            continue
        date, _, subject = rest.partition("\t")
        records.append(
            {
                "commit": commit,
                "date": date[:10] if date else "",
                "subject": subject,
            }
        )
    return records


def parse_releases(lines: list[str]) -> list[dict[str, str]]:
    releases: list[dict[str, str]] = []
    for line in lines:
        tag, _, rest = line.partition("\t")
        if not tag:
            continue
        commit, _, date = rest.partition("\t")
        if not RELEASE_TAG.match(tag):
            continue
        version = tag[1:] if tag.startswith("v") else tag
        releases.append(
            {
                "tag": tag,
                "version": version,
                "commit": commit.lower(),
                "date": date[:10] if date else "",
            }
        )
    return releases


def repo_releases(root: Path) -> list[dict[str, str]]:
    return parse_releases(
        git_lines(
            root,
            "for-each-ref",
            "refs/tags",
            "--sort=-version:refname",
            f"--format={RELEASE_FORMAT}",
        )
    )


def repo_commits(root: Path, marker: str | None) -> list[dict[str, str]]:
    if marker:
        return parse_commits(
            git_lines(
                root,
                "log",
                f"{marker}..HEAD",
                f"-n{COMMIT_LIMIT}",
                f"--format={COMMIT_FORMAT}",
            )
        )
    return list(
        reversed(
            parse_commits(
                git_lines(
                    root,
                    "log",
                    f"-n{COMMIT_LIMIT}",
                    f"--format={COMMIT_FORMAT}",
                )
            )
        )
    )


def path_has_pruned_dir(rel: str) -> bool:
    return any(part in PRUNE_DIR_NAMES for part in Path(rel.removeprefix("./")).parts)


def is_under_nested_git(root: Path, rel: str) -> bool:
    full = (root / rel.removeprefix("./")).resolve()
    repo_root = root.resolve()
    for parent in [full, *full.parents]:
        if parent == repo_root:
            break
        if (parent / ".git").is_dir():
            return True
    return False


def should_prune_touched(root: Path, rel: str) -> bool:
    return path_has_pruned_dir(rel) or is_under_nested_git(root, rel)


def repo_touched_paths(root: Path, marker: str | None) -> list[str]:
    if marker:
        args = [
            "log",
            f"{marker}..HEAD",
            f"-n{COMMIT_LIMIT}",
            "--name-only",
            "--pretty=format:",
        ]
    else:
        args = ["log", f"-n{COMMIT_LIMIT}", "--name-only", "--pretty=format:"]
    seen: set[str] = set()
    paths: list[str] = []
    for line in git_lines(root, *args):
        rel = "./" + line.strip().replace(os.sep, "/")
        if not rel or rel == "./":
            continue
        if should_prune_touched(root, rel) or rel in seen:
            continue
        seen.add(rel)
        paths.append(rel)
    return paths


def repo_working_tree(root: Path) -> list[str]:
    paths: set[str] = set()
    for line in git_lines(root, "status", "--porcelain=v1", "--untracked-files=all"):
        path = "./" + line[3:].rsplit(" -> ", 1)[-1].replace(os.sep, "/")
        paths.add(path)
    return sorted(paths)


def artifact_path(root: Path, name: str) -> str | None:
    path = root / name
    return display(root, path) if path.is_file() else None


def status(target: str) -> dict[str, object]:
    root = Path(target).resolve()
    marker = parse_marker(root / HISTORY_NAME)
    phase = "delta" if marker else "genesis"
    return {
        "target": str(root),
        "changelog": artifact_path(root, CHANGELOG_NAME),
        "history": artifact_path(root, HISTORY_NAME),
        "marker": marker,
        "phase": phase,
        "commits": repo_commits(root, marker),
        "touched": repo_touched_paths(root, marker),
        "releases": repo_releases(root),
        "working_tree": repo_working_tree(root),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="JSON evidence for grim-forge")
    parser.add_argument("--target", required=True)
    args = parser.parse_args()

    root = Path(args.target).resolve()
    if not root.is_dir():
        parser.error(f"target not found: {root}")

    print(json.dumps(status(str(root)), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
