"""
Entry point for CLI commands: python3 -m ai_skills_opt ...
Provides config, benchmark, and doctor subcommands.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
import yaml

from ai_skills_opt.config import load_config, ConfigError
from ai_skills_opt.benchmark import BenchmarkRunner
from ai_skills_opt.indexer import CodebaseIndexer
from ai_skills_opt.memory import SharedMemoryEngine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ai-skills",
        description="AI Skills Optimization Framework CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # config command
    config_parser = subparsers.add_parser("config", help="Manage and inspect framework configuration")
    config_sub = config_parser.add_subparsers(dest="subcommand", help="Config operations")
    
    show_parser = config_sub.add_parser("show", help="Display resolved configuration")
    show_parser.add_argument("--config", "-c", default="config.yaml", help="Path to config.yaml")
    show_parser.add_argument("--profile", "-p", default="standard", help="Runtime profile to resolve")
    show_parser.add_argument("--format", choices=["yaml", "json"], default="yaml", help="Output format")

    # benchmark command
    bench_parser = subparsers.add_parser("benchmark", help="Run benchmark evaluation across profiles")
    bench_parser.add_argument("--config", "-c", default="config.yaml", help="Path to config.yaml")
    bench_parser.add_argument("--benchmarks", "-b", default="benchmarks.yaml", help="Path to benchmarks.yaml")
    bench_parser.add_argument("--profiles", "-p", default="minimal,standard,full", help="Comma-separated profiles")
    bench_parser.add_argument("--agent", "-a", default="gemini", help="Target agent adapter")
    bench_parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="Output format")

    # doctor command
    doctor_parser = subparsers.add_parser("doctor", help="Run diagnostic health check")
    doctor_parser.add_argument("--config", "-c", default="config.yaml", help="Path to config.yaml")

    return parser


def handle_config_show(args: argparse.Namespace) -> int:
    try:
        cfg = load_config(args.config, profile=args.profile)
        data = cfg.to_dict()
        if args.format == "json":
            print(json.dumps(data, indent=2))
        else:
            print(yaml.safe_dump(data, sort_keys=False))
        return 0
    except ConfigError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def handle_benchmark(args: argparse.Namespace) -> int:
    profiles = [p.strip() for p in args.profiles.split(",") if p.strip()]
    runner = BenchmarkRunner(config_path=args.config)
    report = runner.run_suite(profiles=profiles, benchmarks_path=args.benchmarks, agent_name=args.agent)
    if args.format == "markdown":
        print(report.to_markdown())
    else:
        # JSON output
        serializable = {
            "timestamp": report.timestamp,
            "agent_name": report.agent_name,
            "results": [
                {
                    "profile": r.profile,
                    "pass_rate": r.report.pass_rate,
                    "total_tokens": r.report.total_tokens,
                    "duration": r.report.total_duration_seconds,
                    "token_budget": r.token_budget,
                }
                for r in report.results
            ],
        }
        print(json.dumps(serializable, indent=2))
    return 0


def handle_doctor(args: argparse.Namespace) -> int:
    print("=== AI Skills Optimization Framework Doctor ===")
    all_ok = True
    
    # 1. Config Check
    try:
        cfg = load_config(args.config, profile="standard")
        print("  [PASS] Configuration: Valid (config.yaml)")
    except Exception as e:
        print(f"  [FAIL] Configuration Error: {e}")
        all_ok = False
        return 1

    # 2. Codebase Indexer Check
    indexer = CodebaseIndexer(cfg)
    idx_status = indexer.status()
    if idx_status.available:
        print(f"  [PASS] Code Intelligence: Available ({idx_status.files_indexed} files indexed)")
    else:
        print(f"  [WARN] Code Intelligence: Not available ({idx_status.error})")

    # 3. Shared Memory Check
    try:
        mem = SharedMemoryEngine(cfg)
        print(f"  [PASS] Shared Memory: Functional (DB at {mem.db_path.name})")
    except Exception as e:
        print(f"  [FAIL] Shared Memory Error: {e}")
        all_ok = False

    # 4. Upskill Check
    import shutil
    upskill_bin = shutil.which("upskill") or "/home/anu/.local/bin/upskill"
    if Path(upskill_bin).exists():
        print(f"  [PASS] Upskill CLI: Available ({upskill_bin})")
    else:
        print("  [WARN] Upskill CLI: Not detected")

    print("\nDiagnostic Status: " + ("HEALTHY" if all_ok else "ISSUES DETECTED"))
    return 0 if all_ok else 1


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "config":
        if args.subcommand == "show":
            return handle_config_show(args)
        else:
            parser.parse_args(["config", "--help"])
            return 1
    elif args.command == "benchmark":
        return handle_benchmark(args)
    elif args.command == "doctor":
        return handle_doctor(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
