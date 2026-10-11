"""
Tests for ai_skills_opt.isolation
"""

import unittest
from pathlib import Path

from ai_skills_opt.config import load_config
from ai_skills_opt.isolation import load_benchmark_tasks, isolated_workspace, IsolationError
from ai_skills_opt.memory import SharedMemoryEngine


class TestIsolation(unittest.TestCase):
    def setUp(self):
        self.config = load_config("config.yaml", profile="standard")

    def test_load_benchmark_tasks(self):
        tasks = load_benchmark_tasks("benchmarks.yaml")
        self.assertEqual(len(tasks), 3)
        self.assertEqual(tasks[0].id, "bench-01-symbol-nav")

    def test_missing_benchmark_file(self):
        with self.assertRaises(IsolationError):
            load_benchmark_tasks("missing_benchmarks.yaml")

    def test_isolated_workspace_preserves_host(self):
        # Write to memory inside isolated workspace
        with isolated_workspace(self.config) as iso_dir:
            self.assertTrue(iso_dir.exists())
            iso_memory = SharedMemoryEngine(self.config, root_dir=iso_dir)
            iso_memory.put("iso_ns", "key1", "isolated finding")
            self.assertIsNotNone(iso_memory.get("iso_ns", "key1"))

        # Verify host memory does not have this key
        host_memory = SharedMemoryEngine(self.config)
        self.assertIsNone(host_memory.get("iso_ns", "key1"))


if __name__ == "__main__":
    unittest.main()
