"""
Context freshness and evidence validation module.
Detects stale findings based on disk modifications and git tracking.
"""

from __future__ import annotations

import datetime
from pathlib import Path
from typing import List, Optional, Tuple

from ai_skills_opt.config import OptimizationConfig
from ai_skills_opt.memory import Finding, SharedMemoryEngine


class ContextFreshnessValidator:
    def __init__(self, config: OptimizationConfig, memory_engine: SharedMemoryEngine, root_dir: Optional[Path] = None):
        self.config: OptimizationConfig = config
        self.memory: SharedMemoryEngine = memory_engine
        self.root_dir: Path = (root_dir or Path.cwd()).resolve()

    def validate_finding(self, finding: Finding) -> Tuple[Finding, bool]:
        """
        Validates if a finding's evidence is still fresh.
        Returns: (updated_finding, is_fresh)
        """
        if not self.config.shared_memory.freshness_check:
            return finding, True

        # If no evidence path is linked, treat as valid unless status was already invalid
        if not finding.evidence_path:
            return finding, (finding.status in ("VERIFIED", "HYPOTHESIS"))

        target_file = self.root_dir / finding.evidence_path
        if not target_file.exists():
            # Evidence file was deleted or moved
            if finding.status != "INVALIDATED":
                finding.status = "INVALIDATED"
                self.memory.put(
                    namespace=finding.namespace,
                    key=finding.key,
                    content=finding.content,
                    status="INVALIDATED",
                    tags=finding.tags,
                    evidence_path=finding.evidence_path,
                    line_range=finding.line_range,
                    git_hash=finding.git_hash,
                )
            return finding, False

        # Check file modification time vs finding updated_at
        if finding.updated_at:
            try:
                mtime = target_file.stat().st_mtime
                file_dt = datetime.datetime.fromtimestamp(mtime, datetime.timezone.utc)
                finding_dt = datetime.datetime.fromisoformat(finding.updated_at)
                if file_dt > finding_dt:
                    # File was changed after finding was recorded
                    if finding.status != "STALE":
                        finding.status = "STALE"
                        self.memory.put(
                            namespace=finding.namespace,
                            key=finding.key,
                            content=finding.content,
                            status="STALE",
                            tags=finding.tags,
                            evidence_path=finding.evidence_path,
                            line_range=finding.line_range,
                            git_hash=finding.git_hash,
                        )
                    return finding, False
            except Exception:
                pass

        return finding, (finding.status == "VERIFIED")

    def get_fresh_findings(self, namespace: Optional[str] = None) -> List[Finding]:
        """
        Returns only fresh verified findings suitable for active context injection.
        """
        all_findings = self.memory.list_findings(namespace=namespace)
        fresh_findings: List[Finding] = []

        for f in all_findings:
            validated_finding, is_fresh = self.validate_finding(f)
            if is_fresh and validated_finding.status == "VERIFIED":
                fresh_findings.append(validated_finding)

        return fresh_findings
