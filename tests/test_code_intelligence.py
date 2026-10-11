#!/usr/bin/env python3
"""
tests/test_code_intelligence.py
Unit and integration test suite for codebase-index integration.
"""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class TestCodebaseIndexIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo_root = Path(__file__).resolve().parent.parent
        cls.helper = cls.repo_root / "scripts" / "codebase_index_helper.py"

    def test_01_cli_installed(self):
        proc = subprocess.run(["codebase-index", "--help"], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)
        self.assertIn("Local-first hybrid codebase index", proc.stdout)

    def test_02_check_offline_guarantee(self):
        proc = subprocess.run([sys.executable, str(self.helper), "check-offline"], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)
        self.assertIn("PASS: Index operates completely offline", proc.stdout)

    def test_03_helper_status(self):
        proc = subprocess.run([sys.executable, str(self.helper), "status"], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)
        self.assertIn("CLI installed: Yes", proc.stdout)
        self.assertIn("Index exists : Yes", proc.stdout)

    def test_04_symbol_search(self):
        proc = subprocess.run(
            ["codebase-index", "--root", str(self.repo_root), "symbol", "find_project_root", "--json"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0)
        self.assertIn("find_project_root", proc.stdout)
        self.assertIn("scripts/codebase_index_helper.py", proc.stdout)

    def test_05_refs_search(self):
        proc = subprocess.run(
            ["codebase-index", "--root", str(self.repo_root), "refs", "find_project_root", "--compact"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0)
        self.assertIn("scripts/codebase_index_helper.py", proc.stdout)

    def test_06_diff_impact(self):
        proc = subprocess.run(
            ["codebase-index", "--root", str(self.repo_root), "diff-impact"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0)

    def test_07_incremental_lifecycle(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            (tmp_path / ".git").mkdir()
            sample_file = tmp_path / "module_a.py"
            sample_file.write_text("def hello_world():\n    return 'hello'\n")

            # 1. Initial build
            proc = subprocess.run(["codebase-index", "--root", str(tmp_path), "index"], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0)
            self.assertTrue((tmp_path / ".claude" / "cache" / "codebase-index" / "index.sqlite").is_file())

            # 2. Modify file
            sample_file.write_text("def hello_world():\n    return 'hello'\ndef new_func():\n    return 42\n")

            # 3. Incremental update
            proc = subprocess.run(["codebase-index", "--root", str(tmp_path), "update"], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0)
            self.assertIn("Updated 1 file(s)", proc.stdout)

            # 4. Search new symbol
            proc = subprocess.run(["codebase-index", "--root", str(tmp_path), "symbol", "new_func"], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0)
            self.assertIn("new_func", proc.stdout)

    def test_08_fallback_handling(self):
        non_existent_root = Path("/tmp/non_existent_project_12345")
        proc = subprocess.run(
            [sys.executable, str(self.helper), "--root", str(non_existent_root), "status"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0)
        self.assertIn("Index exists : No", proc.stdout)


if __name__ == "__main__":
    unittest.main()
