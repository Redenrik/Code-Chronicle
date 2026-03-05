import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import sys

sys.path.insert(0, os.path.abspath("src"))
import file_explorer_summary as fes


class IgnorePatternTests(unittest.TestCase):
    def test_directory_only_pattern_matches_directory(self):
        self.assertTrue(fes._pattern_matches("build", "build/", is_dir=True))
        self.assertFalse(fes._pattern_matches("build.log", "build/", is_dir=False))

    def test_wildcard_pattern_matches(self):
        self.assertTrue(fes._pattern_matches("logs/error.log", "*.log", is_dir=False))

    def test_basename_pattern_matches_any_depth(self):
        self.assertTrue(fes._pattern_matches("a/b/node_modules/pkg.json", "node_modules", is_dir=False))

    def test_anchored_pattern_matches_from_root_only(self):
        self.assertTrue(fes._pattern_matches("dist/app.js", "/dist", is_dir=False))
        self.assertFalse(fes._pattern_matches("src/dist/app.js", "/dist", is_dir=False))


class FilesystemBehaviorTests(unittest.TestCase):
    def test_get_file_paths_is_sorted_deterministically(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = Path(tmp) / "b.py"
            b = Path(tmp) / "a.py"
            a.write_text("print('b')")
            b.write_text("print('a')")

            files = fes.get_file_paths(tmp, [])
            self.assertEqual(files, sorted(files))

    def test_list_files_skips_unreadable_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            protected = Path(tmp) / "protected"
            protected.mkdir()
            output = Path(tmp) / "index.txt"

            original_listdir = os.listdir

            def fake_listdir(path):
                if os.path.abspath(path) == os.path.abspath(protected):
                    raise PermissionError("denied")
                return original_listdir(path)

            with mock.patch("file_explorer_summary.os.listdir", side_effect=fake_listdir):
                fes.list_files(tmp, [], str(output))

            content = output.read_text(encoding="utf-8")
            self.assertIn("permission denied", content)

    def test_list_files_detects_symlink_loop(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            child = root / "child"
            child.mkdir()
            loop = child / "loop"
            loop.symlink_to(root, target_is_directory=True)

            output = root / "index.txt"
            fes.list_files(str(root), [], str(output))
            content = output.read_text(encoding="utf-8")
            self.assertIn("symlink loop skipped", content)

    def test_get_ignore_patterns_includes_internal_patterns(self):
        with tempfile.TemporaryDirectory() as tmp:
            patterns = fes.get_ignore_patterns(tmp)
            self.assertIn(".git", patterns)
            self.assertIn(".git/", patterns)


if __name__ == "__main__":
    unittest.main()
