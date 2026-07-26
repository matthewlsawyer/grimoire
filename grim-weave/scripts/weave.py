#!/usr/bin/env python3
"""
Deterministic evidence collection for `/grim-weave`.

Builds a closed evidence JSON object for one token under a target workspace.
The agent reads only what this script returns; it does not draw the ledger or
infer dependency relationships.

Pipeline:
  1. Classify token -> file, symbol, or concept
  2. Collect line hits (git grep, else line scan) with caps
  3. Derive document rows and git commit subjects
  4. Emit sorted paths, hits, documents, commits

Stdout: one JSON document (`WeaveEvidence`). Does not infer relationships.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import subprocess
import sys
from typing import Literal, TypedDict

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

MAX_PATHS = 40
MAX_HITS = 120
MAX_HITS_PER_PATH = 8
MAX_COMMITS = 5
MAX_SCAN_FILES = 8000

TokenKind = Literal["file", "symbol", "concept"]
HitKind = Literal["match", "definition_candidate"]

IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

DEF_PATTERN_STRINGS: tuple[str, ...] = (
    r"\b(type|struct|class|interface|enum|trait|func|fn|def|async\s+def)\s+{name}\b",
    r"\bfunction\s+{name}\b",
    r"\b(const|let|var)\s+{name}\b",
    r"\b{name}\s*:\s*",
    r"\b{name}\s*=\s*",
)


class HitRecord(TypedDict):
    """One line match: repo-relative path, 1-based line, text, and match kind."""

    path: str
    line: int
    text: str
    kind: HitKind


class DocumentRecord(TypedDict):
    """One documentation path for provenance; at most one row per path."""

    path: str
    line: int
    text: str


class CommitRecord(TypedDict):
    """Short git sha and subject line for provenance."""

    sha: str
    subject: str


class WeaveEvidence(TypedDict):
    """Full stdout payload for grim-weave; `paths` is the closed read set."""

    target: str
    token: str
    token_kind: TokenKind
    git_available: bool
    commits_order: str
    paths: list[str]
    hits: list[HitRecord]
    documents: list[DocumentRecord]
    commits: list[CommitRecord]


def to_display_file(rel: str) -> str:
    """Normalize a relative path to `./posix/style` for stable JSON and trees."""
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

    Returns sorted display paths, capped at MAX_SCAN_FILES. Used for file-token
    resolution and fallback line scan when git grep is unavailable or empty.
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


def resolve_file_paths(token: str, target_root: str, all_files: list[str]) -> list[str]:
    """
    Resolve a file token to display path(s).

    Prefer exact path; else all files with matching basename, shallow paths first,
    capped at MAX_PATHS.
    """
    raw = token.strip().lstrip("./")
    abs_path = os.path.join(target_root, raw)
    if os.path.isfile(abs_path):
        return [to_display_file(raw)]
    base = os.path.basename(raw)
    matches = [p for p in all_files if p.endswith("/" + base) or p == "./" + base]
    matches.sort(key=lambda p: (len(segments(p)), p))
    return matches[:MAX_PATHS]


def git_available(target_root: str) -> bool:
    """True when target is inside a git work tree."""
    code, _ = run_git(["rev-parse", "--is-inside-work-tree"], target_root)
    return code == 0


def run_git(args: list[str], cwd: str) -> tuple[int, str]:
    """Run git with C locale; return (exit_code, stdout stripped). stderr discarded."""
    env = {**os.environ, "LC_ALL": "C", "LANG": "C"}
    proc = subprocess.run(
        ["git", *args],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        check=False,
        env=env,
    )
    return proc.returncode, (proc.stdout or "").strip()


def git_grep(
    target_root: str, pattern: str, fixed: bool, *, case_insensitive: bool = False
) -> list[tuple[str, int, str]]:
    """
    Run `git grep` from target_root.

    Returns (display_path, line_no, line_text) tuples. Exit 0 and 1 mean success
    (no matches is exit 1). Uses -F fixed string or -E regex when fixed is False.
    """
    args = ["grep", "-n", "-I", "--no-color"]
    if case_insensitive:
        args.append("-i")
    if fixed:
        args.append("-F")
    else:
        args.append("-E")
    args.extend([pattern, "--"])
    code, out = run_git(args, target_root)
    if code not in (0, 1) or not out:
        return []
    hits: list[tuple[str, int, str]] = []
    for line in out.splitlines():
        if ":" not in line:
            continue
        path_part, rest = line.split(":", 1)
        if ":" not in rest:
            continue
        line_no_s, text = rest.split(":", 1)
        try:
            line_no = int(line_no_s)
        except ValueError:
            continue
        rel = to_display_file(path_part)
        hits.append((rel, line_no, text.rstrip("\n")))
    return hits


def scan_file_for_needle(
    target_root: str, display_path: str, needle: str, case_insensitive: bool
) -> list[tuple[int, str]]:
    """
    Substring search in one file when git grep is missing or insufficient.

    Returns (line_no, line_text) for each matching line (1-based line numbers).
    """
    rel = display_path[2:] if display_path.startswith("./") else display_path
    abs_path = os.path.join(target_root, rel)
    if not os.path.isfile(abs_path):
        return []
    try:
        with open(abs_path, encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except OSError:
        return []
    found: list[tuple[int, str]] = []
    n = needle if not case_insensitive else needle.lower()
    for i, line in enumerate(lines, start=1):
        hay = line if not case_insensitive else line.lower()
        if n in hay:
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
    """True for extensions we line-scan in fallback mode (includes doc paths)."""
    _, ext = os.path.splitext(display_path.lower())
    return ext in TEXT_SCAN_SUFFIXES or is_doc_path(display_path)


def compile_definition_patterns(
    name: str, *, case_insensitive: bool
) -> tuple[re.Pattern[str], ...]:
    """Compile DEF_PATTERN_STRINGS for a symbol name (once per weave, not per line)."""
    flags = re.IGNORECASE if case_insensitive else 0
    escaped = re.escape(name)
    return tuple(
        re.compile(template.replace("{name}", escaped), flags)
        for template in DEF_PATTERN_STRINGS
    )


def classify_hit_kind(
    kind: TokenKind,
    text: str,
    def_patterns: tuple[re.Pattern[str], ...] | None,
) -> HitKind:
    """
    Label a hit line: definition_candidate for symbol + declaration-shaped line,
    otherwise match.
    """
    if kind == "symbol" and def_patterns is not None:
        for rx in def_patterns:
            if rx.search(text):
                return "definition_candidate"
    return "match"


def collect_hits(
    target_root: str,
    token: str,
    kind: TokenKind,
    seed_paths: list[str],
    all_files: list[str],
) -> tuple[list[HitRecord], list[str]]:
    """
    Collect bounded line hits and the path set they imply.

    Symbol and concept tokens use case-insensitive search. Order of work:
    git grep (fixed needle; concepts may retry as regex), then optional file scan.
    Enforces MAX_HITS, MAX_HITS_PER_PATH, and MAX_PATHS.
    """
    needle = token.strip()
    case_insensitive = kind != "file"
    hits: list[HitRecord] = []
    path_set: set[str] = set(seed_paths)
    def_patterns: tuple[re.Pattern[str], ...] | None = None
    if kind == "symbol" and needle:
        def_patterns = compile_definition_patterns(needle, case_insensitive=case_insensitive)

    git_hits = git_grep(target_root, needle, fixed=True, case_insensitive=case_insensitive)
    if not git_hits and kind == "concept" and needle:
        git_hits = git_grep(
            target_root, re.escape(needle), fixed=False, case_insensitive=case_insensitive
        )

    per_path: dict[str, int] = {}

    def add_hit(path: str, line_no: int, text: str, hit_kind: HitKind) -> None:
        if len(hits) >= MAX_HITS:
            return
        if per_path.get(path, 0) >= MAX_HITS_PER_PATH:
            return
        per_path[path] = per_path.get(path, 0) + 1
        path_set.add(path)
        hits.append(
            HitRecord(
                path=path,
                line=line_no,
                text=text,
                kind=hit_kind,
            )
        )

    for path, line_no, text in git_hits:
        add_hit(path, line_no, text, classify_hit_kind(kind, text, def_patterns))

    need_fallback_scan = len(git_hits) == 0 or bool(seed_paths)
    if need_fallback_scan and len(hits) < MAX_HITS:
        scan_paths = list(seed_paths) if seed_paths else []
        if not git_hits:
            scan_paths = list(
                dict.fromkeys(scan_paths + [p for p in all_files if is_text_scan_path(p)])
            )
        for display_path in scan_paths:
            if len(hits) >= MAX_HITS:
                break
            if per_path.get(display_path, 0) >= MAX_HITS_PER_PATH:
                continue
            for line_no, text in scan_file_for_needle(
                target_root, display_path, needle, case_insensitive
            ):
                add_hit(
                    display_path,
                    line_no,
                    text,
                    classify_hit_kind(kind, text, def_patterns),
                )
                if per_path.get(display_path, 0) >= MAX_HITS_PER_PATH:
                    break

    hits.sort(key=lambda h: (h["path"], h["line"]))
    paths = sorted(path_set)[:MAX_PATHS]
    return hits, paths


def collect_documents(hits: list[HitRecord], seed_paths: list[str]) -> list[DocumentRecord]:
    """
    Build the documents list for provenance.

    One row per doc path: earliest hit line wins. File-token seed paths that are
    docs but have no hit get a placeholder row (line 1, empty text).
    """
    docs: list[DocumentRecord] = []
    seen_paths: set[str] = set()
    for h in sorted(hits, key=lambda row: (row["path"], row["line"])):
        if not is_doc_path(h["path"]):
            continue
        if h["path"] in seen_paths:
            continue
        seen_paths.add(h["path"])
        docs.append(DocumentRecord(path=h["path"], line=h["line"], text=h["text"]))
    for p in seed_paths:
        if is_doc_path(p) and p not in seen_paths:
            seen_paths.add(p)
            docs.append(DocumentRecord(path=p, line=1, text=""))
    docs.sort(key=lambda d: d["path"])
    return docs


COMMIT_LOG_FORMAT = "%H\t%h\t%at\t%s"


def collect_commits(
    target_root: str,
    token: str,
    kind: TokenKind,
    paths: list[str],
    *,
    git_ok: bool,
) -> list[CommitRecord]:
    """
    Merge git log results into newest-first commit rows.

    Sources: pickaxe (-S) for symbols, --grep for concepts, and path history for
    up to 10 evidence paths. Dedupes by full sha; caps at MAX_COMMITS.
    """
    if not git_ok:
        return []
    by_full_sha: dict[str, tuple[int, str, str]] = {}

    def add_from_log(args: list[str]) -> None:
        code, out = run_git(args, target_root)
        if code != 0 or not out:
            return
        for line in out.splitlines():
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t", 3)
            if len(parts) != 4:
                continue
            full_sha, short_sha, at_s, subject = parts
            try:
                at = int(at_s)
            except ValueError:
                continue
            prev = by_full_sha.get(full_sha)
            if prev is None or at > prev[0]:
                by_full_sha[full_sha] = (at, short_sha[:6], subject.strip())

    log_tail = ["--pretty=format:" + COMMIT_LOG_FORMAT]

    name = token.strip()
    if kind == "symbol" and name:
        add_from_log(
            [
                "log",
                f"--max-count={MAX_COMMITS}",
                f"-S{name}",
                *log_tail,
            ]
        )
    if kind == "concept" and name:
        add_from_log(
            [
                "log",
                f"--max-count={MAX_COMMITS}",
                f"--grep={name}",
                "-i",
                *log_tail,
            ]
        )
    for p in paths[:10]:
        rel = p[2:] if p.startswith("./") else p
        add_from_log(
            [
                "log",
                f"--max-count={MAX_COMMITS}",
                *log_tail,
                "--",
                rel,
            ]
        )

    ranked = sorted(by_full_sha.values(), key=lambda row: row[0], reverse=True)
    return [
        CommitRecord(sha=short, subject=subject)
        for _at, short, subject in ranked[:MAX_COMMITS]
    ]


def weave(target_root: str, token: str) -> WeaveEvidence:
    """Run the full evidence pipeline for one target directory and token."""
    all_files = list_files(target_root)
    kind = classify_token(token, target_root, all_files)
    seed_paths: list[str] = []
    if kind == "file":
        seed_paths = resolve_file_paths(token, target_root, all_files)

    hits, paths = collect_hits(target_root, token, kind, seed_paths, all_files)
    if kind == "file" and seed_paths:
        paths = sorted(set(paths) | set(seed_paths))[:MAX_PATHS]

    documents = collect_documents(hits, seed_paths)
    git_ok = git_available(target_root)
    commits = collect_commits(target_root, token, kind, paths, git_ok=git_ok)

    return WeaveEvidence(
        target=target_root,
        token=token.strip(),
        token_kind=kind,
        git_available=git_ok,
        commits_order="newest_first",
        paths=paths,
        hits=hits,
        documents=documents,
        commits=commits,
    )


def main() -> int:
    """CLI entry: --target and --token required; prints JSON WeaveEvidence to stdout."""
    ap = argparse.ArgumentParser(description="Collect weave evidence for grim-weave (JSON stdout)")
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
    args = ap.parse_args()

    target_root = os.path.abspath(args.target)
    if not os.path.isdir(target_root):
        print(f"target not found: {target_root}", file=sys.stderr)
        return 2
    if not args.token.strip():
        print("--token must be non-empty", file=sys.stderr)
        return 2

    payload = weave(target_root, args.token)
    json.dump(payload, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
