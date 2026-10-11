"""
Tests for ai_skills_opt.config using standard unittest
"""

import tempfile
import unittest
from pathlib import Path
import yaml

from ai_skills_opt.config import (
    load_config,
    OptimizationConfig,
    ConfigError,
    SchemaValidationError,
)


class TestConfig(unittest.TestCase):
    def test_load_default_config(self):
        cfg = load_config("config.yaml", profile="standard")
        self.assertIsInstance(cfg, OptimizationConfig)
        self.assertEqual(cfg.version, "1.0")
        self.assertEqual(cfg.active_profile, "standard")
        self.assertTrue(cfg.code_intelligence.enabled)
        self.assertEqual(cfg.code_intelligence.max_tokens_per_query, 1500)
        self.assertTrue(cfg.shared_memory.fts_enabled)
        self.assertEqual(cfg.agent_adapters.default_agent, "gemini")
        self.assertEqual(cfg.benchmarks.isolation_mode, "worktree")

    def test_profile_resolution_overrides(self):
        minimal_cfg = load_config("config.yaml", profile="minimal")
        self.assertEqual(minimal_cfg.active_profile, "minimal")
        self.assertEqual(minimal_cfg.code_intelligence.max_tokens_per_query, 500)
        self.assertFalse(minimal_cfg.shared_memory.fts_enabled)

        full_cfg = load_config("config.yaml", profile="full")
        self.assertEqual(full_cfg.active_profile, "full")
        self.assertEqual(full_cfg.code_intelligence.max_tokens_per_query, 4000)
        self.assertTrue(full_cfg.shared_memory.embedding_enabled)

        bench_cfg = load_config("config.yaml", profile="benchmark")
        self.assertEqual(bench_cfg.active_profile, "benchmark")
        self.assertEqual(bench_cfg.code_intelligence.max_tokens_per_query, 1000)

    def test_missing_config_file(self):
        with self.assertRaises(ConfigError):
            load_config("non_existent_config.yaml")

    def test_invalid_profile_name(self):
        with self.assertRaises(ConfigError):
            load_config("config.yaml", profile="unknown")

    def test_schema_validation_failures(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir) / "invalid.yaml"

            # Missing version
            tmp_path.write_text("code_intelligence: {}\n", encoding="utf-8")
            with self.assertRaises(SchemaValidationError):
                load_config(tmp_path)

            # Invalid token budget type
            invalid_tokens = {
                "version": "1.0",
                "code_intelligence": {
                    "max_tokens_per_query": -100
                }
            }
            tmp_path.write_text(yaml.safe_dump(invalid_tokens), encoding="utf-8")
            with self.assertRaises(SchemaValidationError):
                load_config(tmp_path)

            # Invalid isolation mode
            invalid_isolation = {
                "version": "1.0",
                "benchmarks": {
                    "isolation_mode": "invalid_mode"
                }
            }
            tmp_path.write_text(yaml.safe_dump(invalid_isolation), encoding="utf-8")
            with self.assertRaises(SchemaValidationError):
                load_config(tmp_path)

    def test_config_to_dict(self):
        cfg = load_config("config.yaml", profile="standard")
        d = cfg.to_dict()
        self.assertEqual(d["version"], "1.0")
        self.assertEqual(d["active_profile"], "standard")
        self.assertIn("code_intelligence", d)
        self.assertIn("shared_memory", d)
        self.assertIn("agent_adapters", d)
        self.assertIn("benchmarks", d)


if __name__ == "__main__":
    unittest.main()
