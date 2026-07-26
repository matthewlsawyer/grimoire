from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from load_script import load_script

weave = load_script("grim-weave/scripts/weave.py", "grim_weave_weave")


class CollectDocumentsTests(unittest.TestCase):
    def test_dedupes_one_record_per_path_earliest_line(self) -> None:
        hits = [
            weave.HitRecord(
                path="./docs/a.md",
                line=10,
                text="later mention",
                kind="match",
            ),
            weave.HitRecord(
                path="./docs/a.md",
                line=3,
                text="first mention",
                kind="match",
            ),
            weave.HitRecord(
                path="./README.md",
                line=1,
                text="top",
                kind="match",
            ),
        ]
        docs = weave.collect_documents(hits, [])
        self.assertEqual(len(docs), 2)
        by_path = {d["path"]: d for d in docs}
        self.assertEqual(by_path["./docs/a.md"]["line"], 3)
        self.assertEqual(by_path["./docs/a.md"]["text"], "first mention")

    def test_seed_doc_when_no_hits(self) -> None:
        docs = weave.collect_documents([], ["./docs/only.md"])
        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0]["path"], "./docs/only.md")
        self.assertEqual(docs[0]["line"], 1)
        self.assertEqual(docs[0]["text"], "")


class ClassifyHitKindTests(unittest.TestCase):
    def test_definition_candidate_for_def_line(self) -> None:
        patterns = weave.compile_definition_patterns("TodoService", case_insensitive=False)
        kind = weave.classify_hit_kind(
            "symbol",
            "def TodoService(db):",
            patterns,
        )
        self.assertEqual(kind, "definition_candidate")

    def test_case_insensitive_symbol_patterns(self) -> None:
        patterns = weave.compile_definition_patterns("hand", case_insensitive=True)
        kind = weave.classify_hit_kind(
            "symbol",
            "class Hand:",
            patterns,
        )
        self.assertEqual(kind, "definition_candidate")


class ClassifyTokenTests(unittest.TestCase):
    def test_symbol_concept_file(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "foo.py").write_text("x = 1\n", encoding="utf-8")
            files = weave.list_files(str(root))
            self.assertEqual(weave.classify_token("Todo", str(root), files), "symbol")
            self.assertEqual(weave.classify_token("throne-ask", str(root), files), "concept")
            self.assertEqual(weave.classify_token("foo.py", str(root), files), "file")


class CaseInsensitiveHitsTests(unittest.TestCase):
    def test_scan_finds_hand_in_hand_heading(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            doc = root / "AGENTS.md"
            doc.write_text("# The Hand\n", encoding="utf-8")
            display = "./AGENTS.md"
            found = weave.scan_file_for_needle(str(root), display, "hand", True)
            self.assertTrue(any("Hand" in line for _ln, line in found))


class WeaveNoGitTests(unittest.TestCase):
    def test_weave_without_git(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "note.md").write_text("Hand charter\n", encoding="utf-8")
            evidence = weave.weave(str(root), "Hand")
            self.assertFalse(evidence["git_available"])
            self.assertEqual(evidence["commits"], [])
            self.assertEqual(evidence["commits_order"], "newest_first")


class CommitOrderTests(unittest.TestCase):
    def test_merged_commits_newest_first(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            env = {
                **__import__("os").environ,
                "GIT_AUTHOR_NAME": "t",
                "GIT_AUTHOR_EMAIL": "t@example.com",
                "GIT_COMMITTER_NAME": "t",
                "GIT_COMMITTER_EMAIL": "t@example.com",
            }
            try:
                subprocess.run(
                    ["git", "init"],
                    cwd=root,
                    check=True,
                    capture_output=True,
                    env=env,
                )
            except subprocess.CalledProcessError:
                self.skipTest("git init unavailable in this environment")
            f = root / "alpha.txt"
            f.write_text("marker\n", encoding="utf-8")
            subprocess.run(["git", "add", "alpha.txt"], cwd=root, check=True, env=env)
            subprocess.run(
                ["git", "commit", "-m", "older marker"],
                cwd=root,
                check=True,
                env={**env, "GIT_AUTHOR_DATE": "2020-01-01T00:00:00", "GIT_COMMITTER_DATE": "2020-01-01T00:00:00"},
            )
            f.write_text("marker\nmore\n", encoding="utf-8")
            subprocess.run(["git", "add", "alpha.txt"], cwd=root, check=True, env=env)
            subprocess.run(
                ["git", "commit", "-m", "newer marker"],
                cwd=root,
                check=True,
                env={**env, "GIT_AUTHOR_DATE": "2025-01-01T00:00:00", "GIT_COMMITTER_DATE": "2025-01-01T00:00:00"},
            )
            commits = weave.collect_commits(
                str(root),
                "marker",
                "symbol",
                ["./alpha.txt"],
                git_ok=True,
            )
            self.assertGreaterEqual(len(commits), 2)
            self.assertIn("newer", commits[0]["subject"])
            self.assertIn("older", commits[1]["subject"])


if __name__ == "__main__":
    unittest.main()
