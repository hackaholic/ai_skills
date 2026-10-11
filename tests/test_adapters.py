"""
Tests for ai_skills_opt.adapters
"""

import unittest

from ai_skills_opt.config import load_config
from ai_skills_opt.adapters import get_adapter, GeminiAdapter, CodexAdapter, BobAdapter, AdapterError


class TestAdapters(unittest.TestCase):
    def setUp(self):
        self.config = load_config("config.yaml", profile="standard")

    def test_gemini_adapter(self):
        adapter = get_adapter("gemini", self.config)
        self.assertIsInstance(adapter, GeminiAdapter)
        res = adapter.execute("What is the architecture?", context="Context: SQLite db")
        self.assertEqual(res.agent_name, "gemini")
        self.assertGreater(res.total_tokens, 0)
        self.assertGreater(res.duration_seconds, 0)

    def test_codex_adapter(self):
        adapter = get_adapter("codex", self.config)
        self.assertIsInstance(adapter, CodexAdapter)
        res = adapter.execute("Refactor function foo()")
        self.assertEqual(res.agent_name, "codex")
        self.assertIn("code_edit", res.tool_calls)

    def test_bob_adapter_fallback(self):
        adapter = get_adapter("bob", self.config)
        self.assertIsInstance(adapter, BobAdapter)
        # Since bob binary is not in PATH, should gracefully execute in fallback mode
        res = adapter.execute("Run benchmark task")
        self.assertEqual(res.agent_name, "bob")
        self.assertIn("fallback_simulation", res.metadata.get("mode"))
        self.assertFalse(res.metadata.get("available"))

    def test_unsupported_adapter_raises(self):
        with self.assertRaises(AdapterError):
            get_adapter("non_existent_agent", self.config)


if __name__ == "__main__":
    unittest.main()
