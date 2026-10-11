"""
Tests for ai_skills_opt.memory
"""

import tempfile
import unittest
from pathlib import Path

from ai_skills_opt.config import load_config
from ai_skills_opt.memory import SharedMemoryEngine, Finding, MemoryError


class TestSharedMemory(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.config = load_config("config.yaml", profile="standard")
        self.config.shared_memory.db_path = "test_memory.sqlite"
        self.root_dir = Path(self.tmpdir.name)
        self.engine = SharedMemoryEngine(self.config, root_dir=self.root_dir)

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_put_and_get_finding(self):
        finding = self.engine.put(
            namespace="auth",
            key="jwt_expiry",
            content="JWT tokens expire after 3600 seconds",
            status="VERIFIED",
            tags=["auth", "security"],
            evidence_path="src/auth.py",
            line_range="45-60",
        )
        self.assertIsNotNone(finding)
        self.assertEqual(finding.namespace, "auth")

        retrieved = self.engine.get("auth", "jwt_expiry")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.content, "JWT tokens expire after 3600 seconds")
        self.assertEqual(retrieved.status, "VERIFIED")
        self.assertEqual(retrieved.tags, ["auth", "security"])

    def test_fts5_search(self):
        self.engine.put("repo", "arch", "Database runs on SQLite with FTS5 virtual tables", "VERIFIED", ["db"])
        self.engine.put("repo", "api", "FastAPI endpoints serve REST requests", "VERIFIED", ["web"])

        results = self.engine.search("SQLite")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].key, "arch")

        results_web = self.engine.search("FastAPI")
        self.assertEqual(len(results_web), 1)
        self.assertEqual(results_web[0].key, "api")

    def test_namespace_isolation(self):
        self.engine.put("ns1", "k1", "Namespace 1 secret", "HYPOTHESIS")
        self.engine.put("ns2", "k1", "Namespace 2 info", "HYPOTHESIS")

        f1 = self.engine.get("ns1", "k1")
        f2 = self.engine.get("ns2", "k1")
        self.assertEqual(f1.content, "Namespace 1 secret")
        self.assertEqual(f2.content, "Namespace 2 info")

        list_ns1 = self.engine.list_findings(namespace="ns1")
        self.assertEqual(len(list_ns1), 1)
        self.assertEqual(list_ns1[0].namespace, "ns1")

    def test_invalid_status_raises(self):
        with self.assertRaises(MemoryError):
            self.engine.put("ns", "k", "test", status="BOGUS_STATUS")

    def test_delete_finding(self):
        self.engine.put("temp", "k_del", "To be deleted")
        self.assertTrue(self.engine.delete("temp", "k_del"))
        self.assertIsNone(self.engine.get("temp", "k_del"))


if __name__ == "__main__":
    unittest.main()
