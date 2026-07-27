from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from load_script import load_script

discover = load_script("grimscry/scripts/discover.py", "grimscry_discover")


class DiscoverTests(unittest.TestCase):
    def test_prunes_vendor_subtree(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "README.md").write_text("# root\n", encoding="utf-8")
            vendor = root / "node_modules" / "pkg"
            vendor.mkdir(parents=True)
            (vendor / "README.md").write_text("# hidden\n", encoding="utf-8")
            seeds = discover.discover(str(root), budget=50)
            paths = {p for p in seeds}
            self.assertIn("./README.md", paths)
            self.assertFalse(any("node_modules" in p for p in paths))

    def test_shallow_first_and_budget(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "README.md").write_text("# shallow\n", encoding="utf-8")
            deep = root / "a" / "b" / "c"
            deep.mkdir(parents=True)
            (deep / "README.md").write_text("# deep\n", encoding="utf-8")
            seeds = discover.discover(str(root), budget=1)
            self.assertEqual(seeds, ["./README.md"])

    def test_is_seed_file_agents(self) -> None:
        self.assertTrue(discover.is_seed_file("AGENTS.md"))
        self.assertFalse(discover.is_seed_file("random.txt"))


if __name__ == "__main__":
    unittest.main()
