"""
Benchmark Evaluation and Reporting Engine for ai_skills_opt.
Executes benchmark tasks across runtime profiles and generates comparative telemetry.
"""

from __future__ import annotations

import datetime
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from ai_skills_opt.config import OptimizationConfig, load_config
from ai_skills_opt.evaluation import EvaluationReport, EvaluationTask, SkillEvaluator
from ai_skills_opt.isolation import isolated_workspace, load_benchmark_tasks


@dataclass
class ProfileBenchmarkResult:
    profile: str
    report: EvaluationReport
    token_budget: int
    memory_enabled: bool


@dataclass
class SuiteBenchmarkReport:
    timestamp: str
    agent_name: str
    results: List[ProfileBenchmarkResult]

    def to_markdown(self) -> str:
        lines = [
            f"# Benchmark Evaluation Report",
            f"**Timestamp:** {self.timestamp}  ",
            f"**Agent Adapter:** {self.agent_name}  \n",
            "| Profile | Pass Rate | Total Tokens | Query Token Budget | Duration (s) | Tasks Run |",
            "| :--- | :--- | :--- | :--- | :--- | :--- |",
        ]
        for r in self.results:
            rep = r.report
            pass_pct = f"{rep.pass_rate * 100:.1f}%"
            dur = f"{rep.total_duration_seconds:.3f}"
            lines.append(
                f"| `{r.profile}` | {pass_pct} | {rep.total_tokens} | {r.token_budget} | {dur} | {rep.tasks_run} |"
            )
        return "\n".join(lines)


class BenchmarkRunner:
    def __init__(self, config_path: str | Path = "config.yaml", root_dir: Optional[Path] = None):
        self.config_path: Path = Path(config_path)
        self.root_dir: Path = (root_dir or Path.cwd()).resolve()

    def run_suite(
        self,
        profiles: List[str],
        benchmarks_path: str | Path = "benchmarks.yaml",
        agent_name: Optional[str] = None,
    ) -> SuiteBenchmarkReport:
        tasks = load_benchmark_tasks(benchmarks_path)
        results: List[ProfileBenchmarkResult] = []
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        target_agent = agent_name or "gemini"

        for prof in profiles:
            cfg = load_config(self.config_path, profile=prof)
            with isolated_workspace(cfg, root_dir=self.root_dir) as iso_dir:
                evaluator = SkillEvaluator(cfg, root_dir=iso_dir)
                report = evaluator.run_evaluation(tasks, agent_name=target_agent)
                results.append(ProfileBenchmarkResult(
                    profile=prof,
                    report=report,
                    token_budget=cfg.code_intelligence.max_tokens_per_query,
                    memory_enabled=cfg.shared_memory.enabled,
                ))

        return SuiteBenchmarkReport(
            timestamp=now,
            agent_name=target_agent,
            results=results,
        )
