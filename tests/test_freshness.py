"""
Tests for ai_skills_opt.freshness
"""

import os
import tempfile
import time
import unittest
from pathlib import Path

from ai_skills_opt.config import load_config
from ai_skills_opt.memory import SharedMemoryEngine
from ai_skills_opt.freshness import ContextFreshnessValidator


class TestFreshness(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root_dir = Path(self.tmpdir.name)
        self.config = load_config("config.yaml", profile="standard")
        self.config.shared_memory.db_path = "test_memory.sqlite"
        self.memory = SharedMemoryEngine(self.config, root_dir=self.root_dir)
        self.validator = ContextFreshnessValidator(self.config, self.memory, root_dir=self.root_dir)

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_unmodified_evidence_remains_fresh(self):
        src_file = self.root_dir / "service.py"
        src_file.write_text("class Service: pass\n", encoding="utf-8")

        f = self.memory.put(
            namespace="backend",
            key="service_def",
            content="Service class defined",
            status="VERIFIED",
            evidence_path="service.py",
        )

        val_f, is_fresh = self.validator.validate_finding(f)
        self.assertTrue(is_fresh)
        self.assertEqual(val_f.status, "VERIFIED")

        fresh_list = self.validator.get_fresh_findings("backend")
        self.assertEqual(len(fresh_list), 1)

    def test_modified_file_becomes_stale(self):
        src_file = self.root_dir / "service.py"
        src_file.write_text("class Service: pass\n", encoding="utf-8")

        f = self.memory.put(
            namespace="backend",
            key="service_def",
            content="Service class defined",
            status="VERIFIED",
            evidence_path="service.py",
        )

        time.sleep(0.05)
        # Modify file
        src_file.write_text("class Service:\n    def run(self): pass\n", encoding="utf-8")

        val_f, is_fresh = self.validator.validate_finding(f)
        self.assertFalse(is_fresh)
        self.assertEqual(val_f.status, "STALE")

        # Context filter should now exclude it
        fresh_list = self.validator.get_fresh_findings("backend")
        self.assertEqual(len(fresh_list), 0)

    def test_deleted_file_becomes_invalidated(self):
        src_file = self.root_dir / "obsolete.py"
        src_file.write_text("obsolete code", encoding="utf-8")

        f = self.memory.put(
            namespace="backend",
            key="obsolete_key",
            content="Obsolete code exists",
            status="VERIFIED",
            evidence_path="obsolete.py",
        )

        src_file.unlink()

        val_f, is_fresh = self.validator.validate_finding(f)
        self.assertFalse(is_fresh)
        self.assertEqual(val_f.status, "INVALIDATED")

        fresh_list = self.validator.get_fresh_findings("backend")
        self.assertEqual(len(fresh_list), 0)


if __name__ == "__main__":
    unittest.main()
