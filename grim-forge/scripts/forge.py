#!/usr/bin/env python3
"""Deterministic `status` and `focus` evidence for `/grim-forge`."""

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
MANIFEST_NAMES = frozenset(
    {
        "package.json",
        "pyproject.toml",
        "cargo.toml",
        "go.mod",
        "pom.xml",
        "build.gradle",
        "build.gradle.kts",
        "composer.json",
        "gemfile",
        "makefile",
    }
)
COMMIT_LIMIT = 50
CHANGELOG_NAME = "CHANGELOG.md"
HISTORY_NAME = "HISTORY.md"
MARKER_PATTERN = re.compile(r"<!--\s*marker:\s*([0-9a-fA-F]+)\s*-->")
COMMIT_FORMAT = "%h%x09%as%x09%s"


def display(root: Path, path: Path) -> str:
    return "./" + path.relative_to(root).as_posix()


def depth(path: str) -> int:
    return len(Path(path).parts)


def is_readme(path: Path) -> bool:
    return path.name.lower().startswith("readme")


def is_git_root(path: Path) -> bool:
    return (path / ".git").exists()


def is_nested_git_root(path: Path, repo_root: Path) -> bool:
    return path.resolve() != repo_root.resolve() and is_git_root(path)


def walk_files(root: Path) -> list[Path]:
    repo_root = root.resolve()
    files: list[Path] = []
    for current, directories, names in os.walk(root):
        current_path = Path(current).resolve()
        if is_nested_git_root(current_path, repo_root):
            directories[:] = []
            continue
        directories[:] = sorted(
            name
            for name in directories
            if name not in PRUNE_DIR_NAMES
            and not is_nested_git_root((current_path / name).resolve(), repo_root)
        )
        files.extend(current_path / name for name in sorted(names))
    return files


def sorted_paths(paths: list[str], limit: int) -> list[str]:
    return sorted(paths, key=lambda path: (depth(path), path))[:limit]


def git_lines(root: Path, *args: str) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.splitlines() if result.returncode == 0 else []


def parse_marker(changelog_path: Path) -> str | None:
    if not changelog_path.is_file():
        return None
    match = MARKER_PATTERN.search(changelog_path.read_text(encoding="utf-8"))
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


def repo_commits(root: Path, marker: str | None, bootstrap: bool) -> list[dict[str, str]]:
    if bootstrap:
        return parse_commits(
            git_lines(
                root,
                "log",
                "--reverse",
                f"-n{COMMIT_LIMIT}",
                f"--format={COMMIT_FORMAT}",
            )
        )
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
    return []


def repo_working_tree(root: Path) -> list[str]:
    paths: set[str] = set()
    for line in git_lines(root, "status", "--porcelain=v1", "--untracked-files=all"):
        path = "./" + line[3:].rsplit(" -> ", 1)[-1].replace(os.sep, "/")
        paths.add(path)
    return sorted(paths)


def artifact_path(root: Path, name: str) -> str | None:
    path = root / name
    return display(root, path) if path.is_file() else None


def status(target: str, bootstrap: bool = False) -> dict[str, object]:
    root = Path(target).resolve()
    changelog_path = root / CHANGELOG_NAME
    marker = parse_marker(changelog_path)
    return {
        "target": str(root),
        "changelog": artifact_path(root, CHANGELOG_NAME),
        "history": artifact_path(root, HISTORY_NAME),
        "marker": marker,
        "commits": repo_commits(root, marker, bootstrap),
        "working_tree": repo_working_tree(root),
    }


def candidate_path(root: Path, candidate: str) -> Path:
    path = (root / candidate).resolve()
    if root not in path.parents and path != root:
        raise ValueError("--candidate must be inside --target")
    if not path.exists():
        raise ValueError(f"candidate not found: {candidate}")
    return path


def candidate_files(files: list[Path], candidate: Path) -> list[Path]:
    if candidate.is_file():
        return [candidate]
    return [path for path in files if candidate in path.parents]


def ancestor_context(files: list[Path], candidate: Path, root: Path) -> list[Path]:
    current = candidate if candidate.is_dir() else candidate.parent
    directories = {current}
    while current != root:
        current = current.parent
        directories.add(current)
    return [
        path
        for path in files
        if path.parent in directories
        and (is_readme(path) or path.name.lower() in MANIFEST_NAMES)
    ]


def focused_paths(root: Path, candidate: Path, budget: int) -> list[str]:
    files = walk_files(root)
    selected = candidate_files(files, candidate) + ancestor_context(files, candidate, root)
    relative = list(dict.fromkeys(display(root, path) for path in selected))
    return sorted_paths(relative, budget)


def focus(target: str, candidate: str, budget: int) -> dict[str, object]:
    root = Path(target).resolve()
    path = candidate_path(root, candidate)
    relative = display(root, path)
    return {
        "target": str(root),
        "candidate": relative,
        "read_set": focused_paths(root, path, budget),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="JSON evidence for grim-forge")
    commands = parser.add_subparsers(dest="command", required=True)
    status_parser = commands.add_parser("status")
    status_parser.add_argument("--target", required=True)
    status_parser.add_argument("--bootstrap", action="store_true")
    focus_parser = commands.add_parser("focus")
    focus_parser.add_argument("--target", required=True)
    focus_parser.add_argument("--candidate", required=True)
    focus_parser.add_argument("--budget", type=int, default=25)
    args = parser.parse_args()

    root = Path(args.target).resolve()
    if not root.is_dir():
        parser.error(f"target not found: {root}")
    if args.command == "status":
        result = status(str(root), bootstrap=args.bootstrap)
    else:
        if args.budget < 1:
            parser.error("--budget must be >= 1")
        try:
            result = focus(str(root), args.candidate, args.budget)
        except ValueError as error:
            parser.error(str(error))

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
