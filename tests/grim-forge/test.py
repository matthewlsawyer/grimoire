from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from subprocess import run

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from load_script import load_script

forge = load_script("grim-forge/scripts/forge.py", "grim_forge")


def init_git(root: Path) -> None:
    subprocess.run(["git", "init"], cwd=root, capture_output=True, check=True)
    subprocess.run(["git", "config", "user.email", "forge@test"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "Forge"], cwd=root, check=True)


class CollectTests(unittest.TestCase):
    def test_status_reports_paths_and_null_marker(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "README.md").write_text("# Root\n", encoding="utf-8")

            manifest = forge.status(str(root))

            self.assertEqual(manifest["changelog"], None)
            self.assertEqual(manifest["history"], None)
            self.assertIsNone(manifest["marker"])
            self.assertEqual(manifest["commits"], [])
            self.assertNotIn("documentation", manifest)
            self.assertNotIn("coverage", manifest)

    def test_status_parses_changelog_marker(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "CHANGELOG.md").write_text(
                "# Changelog\n\n<!-- marker: AbC1234 -->\n",
                encoding="utf-8",
            )
            (root / "HISTORY.md").write_text("# History\n", encoding="utf-8")

            manifest = forge.status(str(root))

            self.assertEqual(manifest["changelog"], "./CHANGELOG.md")
            self.assertEqual(manifest["history"], "./HISTORY.md")
            self.assertEqual(manifest["marker"], "abc1234")

    def test_status_bootstrap_returns_reverse_commits(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            init_git(root)
            (root / "README.md").write_text("# Root\n", encoding="utf-8")
            subprocess.run(["git", "add", "README.md"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-m", "feat: bootstrap"], cwd=root, check=True)
            (root / "server.py").write_text("pass\n", encoding="utf-8")
            subprocess.run(["git", "add", "server.py"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-m", "feat(api): add server"], cwd=root, check=True)

            manifest = forge.status(str(root), bootstrap=True)

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
            (root / "CHANGELOG.md").write_text(
                f"# Changelog\n\n<!-- marker: {first} -->\n",
                encoding="utf-8",
            )
            (root / "server.py").write_text("pass\n", encoding="utf-8")
            subprocess.run(["git", "add", "server.py"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-m", "fix(cache): default redis"], cwd=root, check=True)

            manifest = forge.status(str(root))

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

            manifest = forge.status(str(root))

            self.assertIn("./draft.py", manifest["working_tree"])

    def test_focus_closes_a_stable_context_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            readme = root / "README.md"
            readme.write_text("# Root\n", encoding="utf-8")
            package = root / "packages" / "api"
            package.mkdir(parents=True)
            (package / "package.json").write_text("{}\n", encoding="utf-8")
            (package / "server.py").write_text("pass\n", encoding="utf-8")

            manifest = forge.focus(str(root), "./packages/api", 10)

            self.assertEqual(manifest["candidate"], "./packages/api")
            self.assertEqual(
                manifest["read_set"],
                [
                    "./README.md",
                    "./packages/api/package.json",
                    "./packages/api/server.py",
                ],
            )
            self.assertNotIn("recent_history", manifest)
            self.assertNotIn("working_tree", manifest)
            self.assertEqual(readme.read_text(encoding="utf-8"), "# Root\n")

    def test_status_and_focus_prune_vendor_files(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "README.md").write_text("# Root\n", encoding="utf-8")
            hidden = root / "node_modules" / "pkg"
            hidden.mkdir(parents=True)
            (hidden / "README.md").write_text("# Hidden\n", encoding="utf-8")
            (hidden / "index.js").write_text("export {};\n", encoding="utf-8")

            focused = forge.focus(str(root), ".", 10)

            self.assertFalse(any("node_modules" in path for path in focused["read_set"]))

    def test_status_prunes_nested_git_repos_in_focus(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "README.md").write_text("# Outer\n", encoding="utf-8")
            inner = root / "inner"
            inner.mkdir()
            (inner / ".git").mkdir()
            (inner / "README.md").write_text("# Inner\n", encoding="utf-8")

            outer_focus = forge.focus(str(root), ".", 10)
            inner_focus = forge.focus(str(inner), ".", 10)

            self.assertIn("./README.md", outer_focus["read_set"])
            self.assertFalse(any("inner" in path for path in outer_focus["read_set"]))
            self.assertIn("./README.md", inner_focus["read_set"])

    def test_cli_rejects_invalid_focus_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            invalid_budget = run(
                [
                    sys.executable,
                    forge.__file__,
                    "focus",
                    "--target",
                    str(root),
                    "--candidate",
                    ".",
                    "--budget",
                    "0",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            outside_target = run(
                [
                    sys.executable,
                    forge.__file__,
                    "focus",
                    "--target",
                    str(root),
                    "--candidate",
                    "..",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(invalid_budget.returncode, 2)
            self.assertIn("--budget must be >= 1", invalid_budget.stderr)
            self.assertEqual(outside_target.returncode, 2)
            self.assertIn("--candidate must be inside --target", outside_target.stderr)


if __name__ == "__main__":
    unittest.main()
