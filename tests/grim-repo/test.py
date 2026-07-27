from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from load_script import load_script

census = load_script("grim-repo/scripts/census.py", "grim_repo_census")


class CensusHelperTests(unittest.TestCase):
    def test_rel_display_root_and_nested(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            nested = root / "projects" / "site"
            nested.mkdir(parents=True)
            self.assertEqual(census._rel_display(str(root), str(root)), "./")
            self.assertEqual(
                census._rel_display(str(root), str(nested)),
                "projects/site/",
            )

    def test_resolve_repo(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            abs_path, display = census.resolve_repo("./", str(root))
            self.assertEqual(abs_path, str(root))
            self.assertEqual(display, "./")
            child = root / "pkg"
            child.mkdir()
            abs_path, display = census.resolve_repo("pkg/", str(root))
            self.assertEqual(abs_path, str(child))
            self.assertEqual(display, "pkg/")

    def test_render_census_shape(self) -> None:
        blocks = [
            census.RepoBlock(
                repo_display="./",
                branch_token="main",
                diff_token="+0 -0",
                sync_token="↑0 ↓0",
            ),
            census.RepoBlock(
                repo_display="nested/",
                branch_token="dev",
                diff_token="+1 -0",
                sync_token="no-up",
            ),
        ]
        out = census.render_census("fixture", blocks)
        self.assertIn("fixture/", out)
        self.assertIn("╞══════════════════◆", out)
        self.assertIn("└─● dev", out)
        self.assertIn("├─ ./", out)


if __name__ == "__main__":
    unittest.main()
