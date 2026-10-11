"""
Tests for ai_skills_opt.evaluation
"""

import unittest

from ai_skills_opt.config import load_config
from ai_skills_opt.evaluation import SkillEvaluator, EvaluationTask


class TestEvaluation(unittest.TestCase):
    def setUp(self):
        self.config = load_config("config.yaml", profile="standard")
        self.evaluator = SkillEvaluator(self.config)

    def test_upskill_cli_detected(self):
        self.assertTrue(self.evaluator.has_upskill_cli())

    def test_run_evaluation_gemini(self):
        tasks = [
            EvaluationTask(
                id="task-1",
                name="Query Index",
                prompt="Find symbol build_parser",
                expected_keywords=["Gemini"],
            ),
            EvaluationTask(
                id="task-2",
                name="Check memory",
                prompt="Get finding auth",
                expected_keywords=["Gemini"],
            ),
        ]
        report = self.evaluator.run_evaluation(tasks, agent_name="gemini")
        self.assertEqual(report.agent_name, "gemini")
        self.assertEqual(report.tasks_run, 2)
        self.assertEqual(report.tasks_passed, 2)
        self.assertEqual(report.pass_rate, 1.0)
        self.assertGreater(report.total_tokens, 0)

    def test_run_evaluation_bob_fallback(self):
        tasks = [
            EvaluationTask(
                id="task-bob",
                name="Bob benchmark",
                prompt="Run optimization test",
                expected_keywords=["simulated"],
            ),
        ]
        report = self.evaluator.run_evaluation(tasks, agent_name="bob")
        self.assertEqual(report.agent_name, "bob")
        self.assertEqual(report.tasks_passed, 1)


if __name__ == "__main__":
    unittest.main()
