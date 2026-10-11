"""
Tests for ai_skills_opt.indexer
"""

import unittest
from pathlib import Path

from ai_skills_opt.config import load_config
from ai_skills_opt.indexer import CodebaseIndexer, IndexerError


class TestIndexer(unittest.TestCase):
    def setUp(self):
        self.config = load_config("config.yaml", profile="standard")
        self.indexer = CodebaseIndexer(self.config)

    def test_indexer_status(self):
        status = self.indexer.status()
        self.assertTrue(status.installed)
        self.assertTrue(status.available)
        self.assertIsNotNone(status.db_path)
        self.assertGreater(status.files_indexed, 0)
        self.assertTrue(status.offline_verified)

    def test_symbol_lookup(self):
        res = self.indexer.symbol("build_parser")
        self.assertIn("ai_skills_opt/__main__.py", res)

    def test_search_with_budget(self):
        res = self.indexer.search("OptimizationConfig", token_budget=500)
        self.assertTrue(len(res) > 0)

    def test_disabled_indexer(self):
        cfg = load_config("config.yaml", profile="minimal")
        cfg.code_intelligence.enabled = False
        indexer = CodebaseIndexer(cfg)
        status = indexer.status()
        self.assertFalse(status.available)
        with self.assertRaises(IndexerError):
            indexer.symbol("build_parser")


if __name__ == "__main__":
    unittest.main()
