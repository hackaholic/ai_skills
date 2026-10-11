"""
Benchmark isolation manager.
Provides clean isolated workspaces and sandboxed storage contexts.
"""

from __future__ import annotations

import contextlib
import shutil
import tempfile
from pathlib import Path
from typing import Generator, List, Optional
import yaml

from ai_skills_opt.config import OptimizationConfig
from ai_skills_opt.evaluation import EvaluationTask


class IsolationError(Exception):
    """Exception raised for workspace isolation failures."""
    pass


def load_benchmark_tasks(path: str | Path = "benchmarks.yaml") -> List[EvaluationTask]:
    file_path = Path(path)
    if not file_path.exists():
        raise IsolationError(f"Benchmarks file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    raw_tasks = data.get("tasks", [])
    tasks: List[EvaluationTask] = []
    for t in raw_tasks:
        tasks.append(EvaluationTask(
            id=t["id"],
            name=t["name"],
            prompt=t["prompt"],
            context=t.get("context"),
            expected_keywords=t.get("expected_keywords", []),
        ))
    return tasks


@contextlib.contextmanager
def isolated_workspace(config: OptimizationConfig, root_dir: Optional[Path] = None) -> Generator[Path, None, None]:
    """
    Creates an isolated workspace for a benchmark run, ensuring zero pollution of host data.
    """
    base_root = (root_dir or Path.cwd()).resolve()
    mode = config.benchmarks.isolation_mode

    with tempfile.TemporaryDirectory(prefix="ai_skills_bench_") as tmpdir:
        isolated_path = Path(tmpdir)
        # Create isolated subdirectories
        (isolated_path / ".ai_skills").mkdir(parents=True, exist_ok=True)
        (isolated_path / ".claude" / "cache" / "codebase-index").mkdir(parents=True, exist_ok=True)
        try:
            yield isolated_path
        finally:
            pass
