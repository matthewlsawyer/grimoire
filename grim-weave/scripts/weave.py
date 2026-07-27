#!/usr/bin/env python3
"""
Deterministic path floor for `/grim-weave`.

Finds files under a target workspace that contain a search token. The agent reads
only paths this script prints; it composes the Weave Ledger from those reads.

Pipeline:
  1. Classify token -> file, symbol, or concept (search behavior only)
  2. Line-scan text-like files under target (find list) with internal caps
  3. Dedupe, shallow-first sort, apply budget

Stdout: flat `./rel` paths, one per line. Does not honor `.gitignore`.
"""

from __future__ import annotations

import argparse
import fnmatch
import os
import re
import subprocess
import sys
from typing import Literal

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

DOC_BASENAME_PATTERNS: tuple[str, ...] = (
    "*.md",
    "*.mdx",
    "*.rst",
    "*.adoc",
)

TEXT_SCAN_SUFFIXES: frozenset[str] = frozenset(
    {
        ".go",
        ".py",
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".rs",
        ".java",
        ".kt",
        ".rb",
        ".php",
        ".cs",
        ".cpp",
        ".c",
        ".h",
        ".hpp",
        ".swift",
        ".md",
        ".mdx",
        ".yaml",
        ".yml",
        ".json",
        ".toml",
        ".sql",
        ".sh",
        ".bash",
        ".zsh",
    }
)

DEFAULT_BUDGET = 40
MAX_HITS = 120
MAX_HITS_PER_PATH = 8
MAX_SCAN_FILES = 8000

TokenKind = Literal["file", "symbol", "concept"]

IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def to_display_file(rel: str) -> str:
    """Normalize a relative path to `./posix/style` for stable stdout lines."""
    rel = rel.replace(os.sep, "/").lstrip("/")
    return "./" + rel if not rel.startswith("./") else rel


def segments(rel_path: str) -> list[str]:
    """Split a display path into non-empty path segments (no leading `./`)."""
    p = rel_path[2:] if rel_path.startswith("./") else rel_path
    p = p.rstrip("/")
    return [s for s in p.split("/") if s]


def is_under_pruned_dir(rel_path: str) -> bool:
    """True when any parent segment is in PRUNE_DIR_NAMES (vendor/build trees)."""
    parts = segments(rel_path)
    if len(parts) <= 1:
        return False
    return any(part in PRUNE_DIR_NAMES for part in parts[:-1])


def _find_or_name_args(names: frozenset[str]) -> list[str]:
    """Build find(1) argument group: `(-name a -o -name b ...)`."""
    ordered = sorted(names)
    args: list[str] = ["("]
    for i, name in enumerate(ordered):
        if i > 0:
            args.append("-o")
        args.extend(["-name", name])
    args.append(")")
    return args


def _find_prune_args() -> list[str]:
    """find prune clause for PRUNE_DIR_NAMES directory segments."""
    return [*_find_or_name_args(PRUNE_DIR_NAMES), "-type", "d", "-prune"]


def list_files(target_root: str) -> list[str]:
    """
    List repo files under target via find(1), skipping pruned subtrees.

    Returns sorted display paths, capped at MAX_SCAN_FILES.
    """
    proc = subprocess.run(
        [
            "find",
            target_root,
            *_find_prune_args(),
            "-o",
            "-type",
            "f",
            "-print",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode not in (0, 1):
        return []
    out: list[str] = []
    for ln in proc.stdout.splitlines():
        ln = ln.strip()
        if not ln:
            continue
        rel = os.path.relpath(ln, target_root)
        display = to_display_file(rel)
        if is_under_pruned_dir(display):
            continue
        out.append(display)
    out.sort()
    return out[:MAX_SCAN_FILES]


def classify_token(token: str, target_root: str, all_files: list[str]) -> TokenKind:
    """
    Classify the weave token.

    - file: path exists, or basename matches a listed file
    - symbol: single identifier (IDENT_RE), e.g. TodoService
    - concept: everything else (phrases, hyphenated names like throne-ask)
    """
    raw = token.strip()
    if not raw:
        return "concept"
    candidate = raw.lstrip("./")
    abs_path = os.path.join(target_root, candidate)
    if os.path.isfile(abs_path):
        return "file"
    base = os.path.basename(candidate)
    if any(p.endswith("/" + base) or p == "./" + base for p in all_files):
        return "file"
    if IDENT_RE.match(raw):
        return "symbol"
    return "concept"


def resolve_file_paths(
    token: str, target_root: str, all_files: list[str], budget: int
) -> list[str]:
    """
    Resolve a file token to display path(s).

    Prefer exact path; else all files with matching basename, shallow paths first.
    """
    raw = token.strip().lstrip("./")
    abs_path = os.path.join(target_root, raw)
    if os.path.isfile(abs_path):
        return [to_display_file(raw)]
    base = os.path.basename(raw)
    matches = [p for p in all_files if p.endswith("/" + base) or p == "./" + base]
    matches.sort(key=lambda p: (len(segments(p)), p))
    return matches[:budget]


def _read_file_lines(target_root: str, display_path: str) -> list[str]:
    """
    Load lines from a file under `target_root` for line scanning.

    `display_path` uses the `./rel` form from `list_files`. Returns [] when the
    path is missing, not a file, or cannot be read (UTF-8, errors replaced).
    """
    rel = display_path[2:] if display_path.startswith("./") else display_path
    abs_path = os.path.join(target_root, rel)
    if not os.path.isfile(abs_path):
        return []
    try:
        with open(abs_path, encoding="utf-8", errors="replace") as f:
            return f.readlines()
    except OSError:
        return []


def scan_file_for_needle(
    target_root: str, display_path: str, needle: str, case_insensitive: bool
) -> list[tuple[int, str]]:
    """Substring search in one file."""
    lines = _read_file_lines(target_root, display_path)
    found: list[tuple[int, str]] = []
    n = needle if not case_insensitive else needle.lower()
    for i, line in enumerate(lines, start=1):
        hay = line if not case_insensitive else line.lower()
        if n in hay:
            found.append((i, line.rstrip("\n")))
    return found


def scan_file_for_regex(
    target_root: str,
    display_path: str,
    pattern: str,
    *,
    case_insensitive: bool,
) -> list[tuple[int, str]]:
    """Regex search in one file (`pattern` is escaped for literal-safe concept retry)."""
    lines = _read_file_lines(target_root, display_path)
    flags = re.IGNORECASE if case_insensitive else 0
    rx = re.compile(re.escape(pattern), flags)
    found: list[tuple[int, str]] = []
    for i, line in enumerate(lines, start=1):
        if rx.search(line):
            found.append((i, line.rstrip("\n")))
    return found


def is_doc_path(display_path: str) -> bool:
    """True for markdown-family basenames or paths under docs/ or adr/."""
    lower = display_path.lower()
    if "/adr/" in lower or "/docs/" in lower or lower.startswith("./docs/"):
        return True
    base = os.path.basename(lower)
    return any(fnmatch.fnmatch(base, pat) for pat in DOC_BASENAME_PATTERNS)


def is_text_scan_path(display_path: str) -> bool:
    """True for extensions we line-scan (includes doc paths)."""
    _, ext = os.path.splitext(display_path.lower())
    return ext in TEXT_SCAN_SUFFIXES or is_doc_path(display_path)


def collect_paths(
    target_root: str,
    token: str,
    kind: TokenKind,
    seed_paths: list[str],
    all_files: list[str],
) -> set[str]:
    """
    Collect paths that contain the token (bounded internal line-hit caps).

    Symbol and concept tokens use case-insensitive search.
    """
    needle = token.strip()
    case_insensitive = kind != "file"
    path_set: set[str] = set(seed_paths)
    hit_count = 0
    per_path: dict[str, int] = {}

    def add_path(path: str) -> bool:
        nonlocal hit_count
        if hit_count >= MAX_HITS:
            return False
        if per_path.get(path, 0) >= MAX_HITS_PER_PATH:
            return False
        per_path[path] = per_path.get(path, 0) + 1
        hit_count += 1
        path_set.add(path)
        return True

    scan_paths = list(
        dict.fromkeys(
            seed_paths + [p for p in all_files if is_text_scan_path(p)]
        )
    )

    def run_scan(
        matcher: Literal["substring", "regex"],
    ) -> None:
        for display_path in scan_paths:
            if hit_count >= MAX_HITS:
                break
            if per_path.get(display_path, 0) >= MAX_HITS_PER_PATH:
                continue
            if matcher == "substring":
                line_hits = scan_file_for_needle(
                    target_root, display_path, needle, case_insensitive
                )
            else:
                line_hits = scan_file_for_regex(
                    target_root,
                    display_path,
                    needle,
                    case_insensitive=case_insensitive,
                )
            for _line_no, _text in line_hits:
                if not add_path(display_path):
                    break
                if per_path.get(display_path, 0) >= MAX_HITS_PER_PATH:
                    break

    run_scan("substring")
    if kind == "concept" and needle and hit_count == 0:
        run_scan("regex")

    return path_set


def weave_paths(target_root: str, token: str, budget: int) -> list[str]:
    """Run collection for one target directory and token; return ranked display paths."""
    if budget < 1:
        return []

    all_files = list_files(target_root)
    kind = classify_token(token, target_root, all_files)
    seed_paths: list[str] = []
    if kind == "file":
        seed_paths = resolve_file_paths(token, target_root, all_files, budget)

    path_set = collect_paths(target_root, token, kind, seed_paths, all_files)
    if kind == "file" and seed_paths:
        path_set |= set(seed_paths)

    ranked = sorted(path_set, key=lambda p: (len(segments(p)), p))
    return ranked[:budget]


def main() -> int:
    """CLI entry: print ranked paths, one per line."""
    ap = argparse.ArgumentParser(
        description="Collect token-matching paths for grim-weave (flat stdout)"
    )
    ap.add_argument(
        "--target",
        required=True,
        help="Repository root (absolute path).",
    )
    ap.add_argument(
        "--token",
        required=True,
        help="File path, symbol, or concept phrase.",
    )
    ap.add_argument(
        "--budget",
        type=int,
        default=DEFAULT_BUDGET,
        help=f"Max ranked paths to emit (default {DEFAULT_BUDGET}).",
    )
    args = ap.parse_args()

    if args.budget < 1:
        print("--budget must be >= 1", file=sys.stderr)
        return 2

    target_root = os.path.abspath(args.target)
    if not os.path.isdir(target_root):
        print(f"target not found: {target_root}", file=sys.stderr)
        return 2
    if not args.token.strip():
        print("--token must be non-empty", file=sys.stderr)
        return 2

    for p in weave_paths(target_root, args.token, budget=args.budget):
        print(p)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
