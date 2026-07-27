from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from load_script import load_script

weave = load_script("grim-weave/scripts/weave.py", "grim_weave_weave")


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


class WeavePathsTests(unittest.TestCase):
    def test_prunes_vendor_subtree(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "note.md").write_text("needle here\n", encoding="utf-8")
            vendor = root / "node_modules" / "pkg"
            vendor.mkdir(parents=True)
            (vendor / "note.md").write_text("needle here\n", encoding="utf-8")
            paths = weave.weave_paths(str(root), "needle", budget=50)
            self.assertIn("./note.md", paths)
            self.assertFalse(any("node_modules" in p for p in paths))

    def test_shallow_first_and_budget(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "a.md").write_text("token\n", encoding="utf-8")
            deep = root / "x" / "y"
            deep.mkdir(parents=True)
            (deep / "b.md").write_text("token\n", encoding="utf-8")
            paths = weave.weave_paths(str(root), "token", budget=1)
            self.assertEqual(paths, ["./a.md"])

    def test_file_token_includes_seed_without_match(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            f = root / "empty.py"
            f.write_text("pass\n", encoding="utf-8")
            paths = weave.weave_paths(str(root), "empty.py", budget=50)
            self.assertIn("./empty.py", paths)

    def test_finds_token_via_scan_without_git(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "note.md").write_text("Hand charter\n", encoding="utf-8")
            paths = weave.weave_paths(str(root), "Hand", budget=50)
            self.assertIn("./note.md", paths)


class ConceptRegexRetryTests(unittest.TestCase):
    def test_scan_file_for_regex_finds_escaped_pattern(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "note.md").write_text("match: foo(bar)\n", encoding="utf-8")
            found = weave.scan_file_for_regex(
                str(root), "./note.md", "foo(bar)", case_insensitive=True
            )
            self.assertEqual(len(found), 1)

    def test_concept_regex_retry_when_substring_misses(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "note.md").write_text("id: foo(bar)\n", encoding="utf-8")
            paths = weave.weave_paths(str(root), "foo(bar)", budget=50)
            self.assertIn("./note.md", paths)


class CliTests(unittest.TestCase):
    def test_cli_prints_paths(self) -> None:
        script = Path(__file__).resolve().parents[2] / "grim-weave" / "scripts" / "weave.py"
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "hit.md").write_text("xyzzy\n", encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(script), "--target", str(root), "--token", "xyzzy"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0)
            self.assertEqual(proc.stdout.strip(), "./hit.md")


if __name__ == "__main__":
    unittest.main()
