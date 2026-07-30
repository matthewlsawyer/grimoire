from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from subprocess import run

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from load_script import load_script

status_mod = load_script("grim-forge/scripts/status.py", "grim_forge_status")


def init_git(root: Path) -> None:
    subprocess.run(["git", "init"], cwd=root, capture_output=True, check=True)
    subprocess.run(["git", "config", "user.email", "forge@test"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "Forge"], cwd=root, check=True)


class CollectTests(unittest.TestCase):
    def test_status_reports_paths_and_null_marker(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "README.md").write_text("# Root\n", encoding="utf-8")

            manifest = status_mod.status(str(root))

            self.assertEqual(manifest["changelog"], None)
            self.assertEqual(manifest["history"], None)
            self.assertIsNone(manifest["marker"])
            self.assertEqual(manifest["phase"], "genesis")
            self.assertEqual(manifest["commits"], [])
            self.assertEqual(manifest["touched"], [])
            self.assertEqual(manifest["releases"], [])

    def test_status_returns_semver_releases_newest_first(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            init_git(root)
            (root / "README.md").write_text("# Root\n", encoding="utf-8")
            subprocess.run(["git", "add", "README.md"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-m", "feat: bootstrap"], cwd=root, check=True)
            subprocess.run(["git", "tag", "v0.1.0"], cwd=root, check=True)
            (root / "server.py").write_text("pass\n", encoding="utf-8")
            subprocess.run(["git", "add", "server.py"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-m", "feat(api): add server"], cwd=root, check=True)
            subprocess.run(["git", "tag", "v0.2.0"], cwd=root, check=True)
            subprocess.run(["git", "tag", "not-a-release"], cwd=root, check=True)

            manifest = status_mod.status(str(root))

            self.assertEqual(len(manifest["releases"]), 2)
            self.assertEqual(manifest["releases"][0]["tag"], "v0.2.0")
            self.assertEqual(manifest["releases"][0]["version"], "0.2.0")
            self.assertEqual(manifest["releases"][1]["tag"], "v0.1.0")
            self.assertEqual(manifest["releases"][1]["version"], "0.1.0")

    def test_status_parses_history_marker(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "CHANGELOG.md").write_text("# Changelog\n", encoding="utf-8")
            (root / "HISTORY.md").write_text(
                "# History\n\n<!-- marker: AbC1234 -->\n",
                encoding="utf-8",
            )

            manifest = status_mod.status(str(root))

            self.assertEqual(manifest["changelog"], "./CHANGELOG.md")
            self.assertEqual(manifest["history"], "./HISTORY.md")
            self.assertEqual(manifest["marker"], "abc1234")
            self.assertEqual(manifest["phase"], "delta")

    def test_status_genesis_returns_reverse_commits(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            init_git(root)
            (root / "README.md").write_text("# Root\n", encoding="utf-8")
            subprocess.run(["git", "add", "README.md"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-m", "feat: bootstrap"], cwd=root, check=True)
            (root / "server.py").write_text("pass\n", encoding="utf-8")
            subprocess.run(["git", "add", "server.py"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-m", "feat(api): add server"], cwd=root, check=True)

            manifest = status_mod.status(str(root))

            self.assertEqual(manifest["phase"], "genesis")
            self.assertEqual(len(manifest["commits"]), 2)
            self.assertEqual(manifest["commits"][0]["subject"], "feat: bootstrap")
            self.assertEqual(manifest["commits"][1]["subject"], "feat(api): add server")
            self.assertRegex(manifest["commits"][0]["date"], r"^\d{4}-\d{2}-\d{2}$")
            self.assertRegex(manifest["commits"][1]["date"], r"^\d{4}-\d{2}-\d{2}$")

    def test_status_delta_commits_since_marker(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            init_git(root)
            (root / "README.md").write_text("# Root\n", encoding="utf-8")
            subprocess.run(["git", "add", "README.md"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-m", "feat: bootstrap"], cwd=root, check=True)
            first = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                cwd=root,
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
            (root / "CHANGELOG.md").write_text("# Changelog\n", encoding="utf-8")
            (root / "HISTORY.md").write_text(
                f"# History\n\n<!-- marker: {first} -->\n",
                encoding="utf-8",
            )
            (root / "server.py").write_text("pass\n", encoding="utf-8")
            subprocess.run(["git", "add", "server.py"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-m", "fix(cache): default redis"], cwd=root, check=True)

            manifest = status_mod.status(str(root))

            self.assertEqual(manifest["phase"], "delta")
            self.assertEqual(len(manifest["commits"]), 1)
            self.assertEqual(manifest["commits"][0]["subject"], "fix(cache): default redis")
            self.assertRegex(manifest["commits"][0]["date"], r"^\d{4}-\d{2}-\d{2}$")

    def test_status_reports_working_tree(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            init_git(root)
            (root / "README.md").write_text("# Root\n", encoding="utf-8")
            subprocess.run(["git", "add", "README.md"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-m", "feat: bootstrap"], cwd=root, check=True)
            (root / "draft.py").write_text("pass\n", encoding="utf-8")

            manifest = status_mod.status(str(root))

            self.assertIn("./draft.py", manifest["working_tree"])

    def test_status_touched_lists_edited_paths(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            init_git(root)
            (root / "README.md").write_text("# Root\n", encoding="utf-8")
            subprocess.run(["git", "add", "README.md"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-m", "feat: bootstrap"], cwd=root, check=True)
            (root / "server.py").write_text("pass\n", encoding="utf-8")
            subprocess.run(["git", "add", "server.py"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-m", "feat(api): add server"], cwd=root, check=True)

            manifest = status_mod.status(str(root))

            self.assertIn("./README.md", manifest["touched"])
            self.assertIn("./server.py", manifest["touched"])

    def test_status_touched_delta_only_since_marker(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            init_git(root)
            (root / "README.md").write_text("# Root\n", encoding="utf-8")
            subprocess.run(["git", "add", "README.md"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-m", "feat: bootstrap"], cwd=root, check=True)
            first = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                cwd=root,
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
            (root / "HISTORY.md").write_text(
                f"# History\n\n<!-- marker: {first} -->\n",
                encoding="utf-8",
            )
            (root / "server.py").write_text("pass\n", encoding="utf-8")
            subprocess.run(["git", "add", "server.py"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-m", "fix(cache): default redis"], cwd=root, check=True)

            manifest = status_mod.status(str(root))

            self.assertEqual(manifest["touched"], ["./server.py"])

    def test_status_touched_prunes_vendor_paths(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            init_git(root)
            (root / "README.md").write_text("# Root\n", encoding="utf-8")
            hidden = root / "node_modules" / "pkg"
            hidden.mkdir(parents=True)
            (hidden / "index.js").write_text("export {};\n", encoding="utf-8")
            subprocess.run(["git", "add", "-f", "README.md", "node_modules/pkg/index.js"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-m", "chore: vendor pkg"], cwd=root, check=True)

            manifest = status_mod.status(str(root))

            self.assertFalse(any("node_modules" in path for path in manifest["touched"]))

    def test_status_touched_prunes_nested_git_repos(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            init_git(root)
            (root / "README.md").write_text("# Outer\n", encoding="utf-8")
            inner = root / "inner"
            inner.mkdir()
            (inner / ".git").mkdir()
            (inner / "README.md").write_text("# Inner\n", encoding="utf-8")
            subprocess.run(["git", "add", "README.md", "inner/README.md"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-m", "feat: nested layout"], cwd=root, check=True)

            manifest = status_mod.status(str(root))

            self.assertIn("./README.md", manifest["touched"])
            self.assertFalse(any("inner" in path for path in manifest["touched"]))

    def test_cli_rejects_missing_target(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            missing = Path(td) / "missing"
            result = run(
                [sys.executable, status_mod.__file__, "--target", str(missing)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 2)
            self.assertIn("target not found", result.stderr)


if __name__ == "__main__":
    unittest.main()
