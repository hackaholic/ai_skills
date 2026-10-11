"""
Configuration management and runtime profile resolver.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml


class ConfigError(Exception):
    """Base exception for configuration errors."""
    pass


class SchemaValidationError(ConfigError):
    """Raised when configuration values fail schema validation."""
    pass


@dataclass
class CodeIntelligenceConfig:
    enabled: bool = True
    engine: str = "codebase-index"
    cache_dir: str = ".claude/cache/codebase-index"
    offline_only: bool = True
    auto_update: bool = True
    max_tokens_per_query: int = 1500

    def validate(self) -> None:
        if not isinstance(self.enabled, bool):
            raise SchemaValidationError("code_intelligence.enabled must be a boolean")
        if not isinstance(self.engine, str) or not self.engine:
            raise SchemaValidationError("code_intelligence.engine must be a non-empty string")
        if not isinstance(self.offline_only, bool):
            raise SchemaValidationError("code_intelligence.offline_only must be a boolean")
        if not isinstance(self.auto_update, bool):
            raise SchemaValidationError("code_intelligence.auto_update must be a boolean")
        if not isinstance(self.max_tokens_per_query, int) or self.max_tokens_per_query <= 0:
            raise SchemaValidationError("code_intelligence.max_tokens_per_query must be a positive integer")


@dataclass
class SharedMemoryConfig:
    enabled: bool = True
    db_path: str = ".ai_skills/memory.sqlite"
    fts_enabled: bool = True
    embedding_enabled: bool = False
    freshness_check: bool = True
    stale_threshold_seconds: int = 86400

    def validate(self) -> None:
        if not isinstance(self.enabled, bool):
            raise SchemaValidationError("shared_memory.enabled must be a boolean")
        if not isinstance(self.db_path, str) or not self.db_path:
            raise SchemaValidationError("shared_memory.db_path must be a non-empty string")
        if not isinstance(self.fts_enabled, bool):
            raise SchemaValidationError("shared_memory.fts_enabled must be a boolean")
        if not isinstance(self.embedding_enabled, bool):
            raise SchemaValidationError("shared_memory.embedding_enabled must be a boolean")
        if not isinstance(self.freshness_check, bool):
            raise SchemaValidationError("shared_memory.freshness_check must be a boolean")
        if not isinstance(self.stale_threshold_seconds, int) or self.stale_threshold_seconds < 0:
            raise SchemaValidationError("shared_memory.stale_threshold_seconds must be a non-negative integer")


@dataclass
class AgentBobConfig:
    execution_mode: str = "fallback"

    def validate(self) -> None:
        if self.execution_mode not in ("fallback", "native"):
            raise SchemaValidationError("agent_adapters.bob.execution_mode must be 'fallback' or 'native'")


@dataclass
class AgentAdaptersConfig:
    default_agent: str = "gemini"
    supported: List[str] = field(default_factory=lambda: ["gemini", "codex", "bob"])
    bob: AgentBobConfig = field(default_factory=AgentBobConfig)

    def validate(self) -> None:
        if not isinstance(self.default_agent, str) or not self.default_agent:
            raise SchemaValidationError("agent_adapters.default_agent must be a non-empty string")
        if not isinstance(self.supported, list) or not self.supported:
            raise SchemaValidationError("agent_adapters.supported must be a non-empty list of strings")
        self.bob.validate()


@dataclass
class BenchmarksConfig:
    isolation_mode: str = "worktree"
    results_dir: str = ".ai_skills/benchmark_results"

    def validate(self) -> None:
        if self.isolation_mode not in ("worktree", "tempdir", "in_place"):
            raise SchemaValidationError("benchmarks.isolation_mode must be 'worktree', 'tempdir', or 'in_place'")
        if not isinstance(self.results_dir, str) or not self.results_dir:
            raise SchemaValidationError("benchmarks.results_dir must be a non-empty string")


@dataclass
class OptimizationConfig:
    version: str = "1.0"
    active_profile: str = "standard"
    code_intelligence: CodeIntelligenceConfig = field(default_factory=CodeIntelligenceConfig)
    shared_memory: SharedMemoryConfig = field(default_factory=SharedMemoryConfig)
    agent_adapters: AgentAdaptersConfig = field(default_factory=AgentAdaptersConfig)
    benchmarks: BenchmarksConfig = field(default_factory=BenchmarksConfig)
    profiles: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    def validate(self) -> None:
        if not isinstance(self.version, str) or not self.version:
            raise SchemaValidationError("version must be a non-empty string")
        self.code_intelligence.validate()
        self.shared_memory.validate()
        self.agent_adapters.validate()
        self.benchmarks.validate()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "active_profile": self.active_profile,
            "code_intelligence": {
                "enabled": self.code_intelligence.enabled,
                "engine": self.code_intelligence.engine,
                "cache_dir": self.code_intelligence.cache_dir,
                "offline_only": self.code_intelligence.offline_only,
                "auto_update": self.code_intelligence.auto_update,
                "max_tokens_per_query": self.code_intelligence.max_tokens_per_query,
            },
            "shared_memory": {
                "enabled": self.shared_memory.enabled,
                "db_path": self.shared_memory.db_path,
                "fts_enabled": self.shared_memory.fts_enabled,
                "embedding_enabled": self.shared_memory.embedding_enabled,
                "freshness_check": self.shared_memory.freshness_check,
                "stale_threshold_seconds": self.shared_memory.stale_threshold_seconds,
            },
            "agent_adapters": {
                "default_agent": self.agent_adapters.default_agent,
                "supported": list(self.agent_adapters.supported),
                "bob": {
                    "execution_mode": self.agent_adapters.bob.execution_mode,
                },
            },
            "benchmarks": {
                "isolation_mode": self.benchmarks.isolation_mode,
                "results_dir": self.benchmarks.results_dir,
            },
        }


def _deep_merge(target: Dict[str, Any], source: Dict[str, Any]) -> Dict[str, Any]:
    merged = copy.deepcopy(target)
    for k, v in source.items():
        if isinstance(v, dict) and k in merged and isinstance(merged[k], dict):
            merged[k] = _deep_merge(merged[k], v)
        else:
            merged[k] = copy.deepcopy(v)
    return merged


def load_config(
    path: str | Path | None = None,
    profile: str | None = None,
) -> OptimizationConfig:
    config_path = Path(path) if path else Path("config.yaml")
    if not config_path.exists():
        raise ConfigError(f"Configuration file not found: {config_path}")

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            raw_data = yaml.safe_load(f) or {}
    except Exception as e:
        raise ConfigError(f"Failed to parse YAML from {config_path}: {e}") from e

    if not isinstance(raw_data, dict):
        raise SchemaValidationError("Configuration file root must be a mapping/dict")

    version = raw_data.get("version")
    if not version or not isinstance(version, str):
        raise SchemaValidationError("Configuration must define a valid string 'version'")

    profiles = raw_data.get("profiles", {})
    if not isinstance(profiles, dict):
        raise SchemaValidationError("'profiles' must be a mapping/dict")

    target_profile = profile or "standard"
    if target_profile not in profiles and target_profile != "standard":
        raise ConfigError(f"Requested profile '{target_profile}' not found in profiles: {list(profiles.keys())}")

    # Start with base sections
    base_data = {
        "code_intelligence": raw_data.get("code_intelligence", {}),
        "shared_memory": raw_data.get("shared_memory", {}),
        "agent_adapters": raw_data.get("agent_adapters", {}),
        "benchmarks": raw_data.get("benchmarks", {}),
    }

    # Apply profile overrides if requested profile exists
    if target_profile in profiles:
        override_data = profiles[target_profile]
        if not isinstance(override_data, dict):
            raise SchemaValidationError(f"Profile '{target_profile}' must be a mapping/dict")
        base_data = _deep_merge(base_data, override_data)

    ci_data = base_data.get("code_intelligence", {})
    ci_cfg = CodeIntelligenceConfig(
        enabled=ci_data.get("enabled", True),
        engine=ci_data.get("engine", "codebase-index"),
        cache_dir=ci_data.get("cache_dir", ".claude/cache/codebase-index"),
        offline_only=ci_data.get("offline_only", True),
        auto_update=ci_data.get("auto_update", True),
        max_tokens_per_query=ci_data.get("max_tokens_per_query", 1500),
    )

    sm_data = base_data.get("shared_memory", {})
    sm_cfg = SharedMemoryConfig(
        enabled=sm_data.get("enabled", True),
        db_path=sm_data.get("db_path", ".ai_skills/memory.sqlite"),
        fts_enabled=sm_data.get("fts_enabled", True),
        embedding_enabled=sm_data.get("embedding_enabled", False),
        freshness_check=sm_data.get("freshness_check", True),
        stale_threshold_seconds=sm_data.get("stale_threshold_seconds", 86400),
    )

    adapters_data = base_data.get("agent_adapters", {})
    bob_data = adapters_data.get("bob", {})
    bob_cfg = AgentBobConfig(
        execution_mode=bob_data.get("execution_mode", "fallback")
    )
    adapters_cfg = AgentAdaptersConfig(
        default_agent=adapters_data.get("default_agent", "gemini"),
        supported=adapters_data.get("supported", ["gemini", "codex", "bob"]),
        bob=bob_cfg,
    )

    bench_data = base_data.get("benchmarks", {})
    bench_cfg = BenchmarksConfig(
        isolation_mode=bench_data.get("isolation_mode", "worktree"),
        results_dir=bench_data.get("results_dir", ".ai_skills/benchmark_results"),
    )

    config = OptimizationConfig(
        version=version,
        active_profile=target_profile,
        code_intelligence=ci_cfg,
        shared_memory=sm_cfg,
        agent_adapters=adapters_cfg,
        benchmarks=bench_cfg,
        profiles=profiles,
    )
    config.validate()
    return config
