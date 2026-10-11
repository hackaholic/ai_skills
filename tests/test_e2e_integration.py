"""
End-to-end integration test validating the entire AI Skills Optimization Framework:
Config -> Indexer -> Shared Memory -> Freshness Validation -> Adapter -> Benchmark Runner.
"""

import tempfile
import unittest
from pathlib import Path

from ai_skills_opt.config import load_config
from ai_skills_opt.indexer import CodebaseIndexer
from ai_skills_opt.memory import SharedMemoryEngine
from ai_skills_opt.freshness import ContextFreshnessValidator
from ai_skills_opt.adapters import get_adapter
from ai_skills_opt.benchmark import BenchmarkRunner


class TestE2EIntegration(unittest.TestCase):
    def test_complete_optimization_lifecycle(self):
        # 1. Load configuration with 'standard' profile
        config = load_config("config.yaml", profile="standard")
        self.assertEqual(config.active_profile, "standard")

        # 2. Check code intelligence index
        indexer = CodebaseIndexer(config)
        status = indexer.status()
        self.assertTrue(status.available)
        self.assertGreater(status.files_indexed, 0)

        # 3. Use isolated shared memory store
        with tempfile.TemporaryDirectory() as tmpdir:
            test_root = Path(tmpdir)
            memory = SharedMemoryEngine(config, root_dir=test_root)

            # Store finding
            test_file = test_root / "sample_module.py"
            test_file.write_text("def sample_func(): return True\n", encoding="utf-8")

            finding = memory.put(
                namespace="architecture",
                key="sample_func_definition",
                content="sample_func returns True and is implemented in sample_module.py",
                status="VERIFIED",
                tags=["sample", "core"],
                evidence_path="sample_module.py",
            )
            self.assertIsNotNone(finding)

            # 4. Context Freshness Verification
            validator = ContextFreshnessValidator(config, memory, root_dir=test_root)
            fresh_findings = validator.get_fresh_findings("architecture")
            self.assertEqual(len(fresh_findings), 1)

            # 5. Agent Adapter Execution with injected context
            agent = get_adapter(config.agent_adapters.default_agent, config)
            context_snippet = f"Finding: {fresh_findings[0].content}"
            result = agent.execute("What does sample_func do?", context=context_snippet)
            self.assertGreater(result.total_tokens, 0)

        # 6. Benchmark Suite Execution
        runner = BenchmarkRunner(config_path="config.yaml")
        bench_report = runner.run_suite(
            profiles=["minimal", "standard"],
            benchmarks_path="benchmarks.yaml",
            agent_name="gemini",
        )
        self.assertEqual(len(bench_report.results), 2)
        md_table = bench_report.to_markdown()
        self.assertIn("# Benchmark Evaluation Report", md_table)


if __name__ == "__main__":
    unittest.main()
