"""
Tests for ai_skills_opt.benchmark
"""

import unittest

from ai_skills_opt.benchmark import BenchmarkRunner, SuiteBenchmarkReport


class TestBenchmark(unittest.TestCase):
    def setUp(self):
        self.runner = BenchmarkRunner()

    def test_run_suite_and_generate_markdown(self):
        report = self.runner.run_suite(
            profiles=["minimal", "standard"],
            benchmarks_path="benchmarks.yaml",
            agent_name="gemini",
        )
        self.assertIsInstance(report, SuiteBenchmarkReport)
        self.assertEqual(len(report.results), 2)
        self.assertEqual(report.results[0].profile, "minimal")
        self.assertEqual(report.results[1].profile, "standard")

        md = report.to_markdown()
        self.assertIn("# Benchmark Evaluation Report", md)
        self.assertIn("| `minimal` |", md)
        self.assertIn("| `standard` |", md)


if __name__ == "__main__":
    unittest.main()
