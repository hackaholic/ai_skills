"""
Codebase Indexer bridge module for ai_skills_opt.
Wraps codebase-index with runtime profile constraints and offline enforcement.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from ai_skills_opt.config import OptimizationConfig, CodeIntelligenceConfig


class IndexerError(Exception):
    """Exception raised for indexing and retrieval errors."""
    pass


@dataclass
class IndexStatus:
    available: bool
    installed: bool
    db_path: Optional[Path]
    size_bytes: int
    files_indexed: int
    offline_verified: bool
    error: Optional[str] = None


class CodebaseIndexer:
    def __init__(self, config: OptimizationConfig, root_dir: Optional[Path] = None):
        self.config: OptimizationConfig = config
        self.ci_config: CodeIntelligenceConfig = config.code_intelligence
        self.root_dir: Path = (root_dir or Path.cwd()).resolve()

    def is_installed(self) -> bool:
        return shutil.which("codebase-index") is not None

    def get_db_path(self) -> Path:
        return self.root_dir / self.ci_config.cache_dir / "index.sqlite"

    def status(self) -> IndexStatus:
        installed = self.is_installed()
        db_path = self.get_db_path()

        if not self.ci_config.enabled:
            return IndexStatus(
                available=False,
                installed=installed,
                db_path=None,
                size_bytes=0,
                files_indexed=0,
                offline_verified=True,
                error="Code intelligence disabled by configuration",
            )

        if not installed:
            return IndexStatus(
                available=False,
                installed=False,
                db_path=db_path if db_path.exists() else None,
                size_bytes=0,
                files_indexed=0,
                offline_verified=True,
                error="codebase-index CLI is not installed",
            )

        if not db_path.exists():
            return IndexStatus(
                available=False,
                installed=True,
                db_path=None,
                size_bytes=0,
                files_indexed=0,
                offline_verified=True,
                error="Index database does not exist",
            )

        size = db_path.stat().st_size
        file_count = 0
        try:
            import sqlite3
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("SELECT count(*) FROM files")
            row = cur.fetchone()
            if row:
                file_count = row[0]
            conn.close()
        except Exception:
            file_count = 0

        return IndexStatus(
            available=True,
            installed=True,
            db_path=db_path,
            size_bytes=size,
            files_indexed=file_count,
            offline_verified=self.ci_config.offline_only,
        )

    def _run_cli(self, args: List[str]) -> str:
        if not self.ci_config.enabled:
            raise IndexerError("Code intelligence is disabled in current profile")
        if not self.is_installed():
            raise IndexerError("codebase-index CLI is not installed")

        cmd = ["codebase-index", "--root", str(self.root_dir)] + args
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            err = proc.stderr.strip() or proc.stdout.strip()
            raise IndexerError(f"codebase-index failed: {err}")
        return proc.stdout.strip()

    def update(self) -> str:
        return self._run_cli(["update"])

    def symbol(self, name: str) -> str:
        return self._run_cli(["symbol", name])

    def references(self, name: str, compact: bool = True) -> str:
        args = ["refs", name]
        if compact:
            args.append("--compact")
        return self._run_cli(args)

    def impact(self, target: str, compact: bool = True) -> str:
        args = ["impact", target]
        if compact:
            args.append("--compact")
        return self._run_cli(args)

    def search(self, query: str, token_budget: Optional[int] = None) -> str:
        budget = token_budget or self.ci_config.max_tokens_per_query
        return self._run_cli(["search", query, "--compact", "--token-budget", str(budget)])
