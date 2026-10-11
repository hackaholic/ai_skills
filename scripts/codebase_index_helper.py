#!/usr/bin/env python3
"""
codebase_index_helper.py
Deterministic helper utility for managing the codebase-index lifecycle.

Provides:
- status: Check index availability, size, freshness, and database path.
- check-offline: Verify that embeddings are disabled and operation is strictly local/offline.
- ensure-index: Incrementally update if present, or initialize if missing.
- query: Convenience wrapper for symbol, refs, impact, and bounded search.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def find_project_root(start: Path | None = None) -> Path:
    start = (start or Path.cwd()).resolve()
    for candidate in (start, *start.parents):
        if (candidate / ".git").exists():
            return candidate
        if (candidate / ".claude").exists() and candidate != Path.home():
            return candidate
    return start


def get_index_path(root: Path) -> Path:
    return root / ".claude" / "cache" / "codebase-index" / "index.sqlite"


def check_installed() -> bool:
    return shutil.which("codebase-index") is not None


def run_cbx(cmd: list[str], root: Path, capture_json: bool = False) -> tuple[int, str]:
    if not check_installed():
        return 1, "codebase-index is not installed. Install via: pip install codebase-index==2.1.2"
    full_cmd = ["codebase-index", "--root", str(root)] + cmd
    if capture_json and "--json" not in full_cmd:
        full_cmd.append("--json")
    try:
        proc = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
            check=False,
        )
        output = proc.stdout if proc.returncode == 0 else (proc.stderr or proc.stdout)
        return proc.returncode, output.strip()
    except Exception as e:
        return 1, str(e)


def cmd_status(root: Path) -> int:
    idx_path = get_index_path(root)
    installed = check_installed()
    print(f"Project root : {root}")
    print(f"CLI installed: {'Yes' if installed else 'No (fallback to ripgrep/view_file)'}")
    print(f"Index file   : {idx_path}")
    print(f"Index exists : {'Yes' if idx_path.is_file() else 'No'}")

    if idx_path.is_file():
        size_kb = idx_path.stat().st_size / 1024
        print(f"Index size   : {size_kb:.1f} KB")
        if installed:
            code, out = run_cbx(["stats", "--json"], root)
            if code == 0:
                try:
                    data = json.loads(out)
                    files_cnt = data.get("files", "N/A")
                    syms_cnt = data.get("symbols", "N/A")
                    built_at = data.get("built_at", "N/A")
                    print(f"Files indexed: {files_cnt}")
                    print(f"Symbols count: {syms_cnt}")
                    print(f"Built at     : {built_at}")
                except Exception:
                    pass
    return 0


def cmd_check_offline(root: Path) -> int:
    print("Checking offline guarantees...")
    try:
        from codebase_index import config
        cfg = config.load(root)
        emb = cfg.embeddings
        print(f"  Embeddings backend : {emb.backend}")
        print(f"  Embeddings enabled : {emb.enabled}")
        print(f"  Allow external     : {emb.allow_external}")
        print(f"  Ignore files       : {cfg.ignore_files}")

        is_offline = (emb.backend == "noop" or not emb.enabled) and not emb.allow_external
        if is_offline:
            print("✓ PASS: Index operates completely offline with native Tree-sitter & SQLite.")
            return 0
        else:
            print("✗ WARNING: External embeddings or remote endpoints might be configured!")
            return 1
    except ImportError:
        print("codebase_index python package not importable.")
        return 1


def cmd_ensure_index(root: Path) -> int:
    if not check_installed():
        print("Notice: codebase-index not installed. Operating in grep fallback mode.")
        return 0

    idx_path = get_index_path(root)
    if not idx_path.is_file():
        print(f"Initializing index for {root}...")
        code, out = run_cbx(["index"], root)
        if code == 0:
            print("✓ Initial index build complete.")
            return 0
        else:
            print(f"Warning: Index build failed ({out}). Falling back gracefully.")
            return code
    else:
        # Incremental update
        code, out = run_cbx(["update"], root)
        if code == 0:
            print("✓ Index incrementally updated.")
            return 0
        else:
            print(f"Warning: Incremental update returned {code}: {out}")
            return code


def cmd_query(args: argparse.Namespace, root: Path) -> int:
    if not check_installed():
        print(f"Fallback: codebase-index unavailable. Querying '{args.target}' via grep.")
        return 1

    subcmd = args.type
    cmd_args = [subcmd]
    if subcmd == "search":
        cmd_args.extend(["--compact", "--token-budget", str(args.token_budget), args.target])
    elif subcmd == "symbol":
        cmd_args.append(args.target)
    elif subcmd == "refs":
        cmd_args.extend(["--compact", args.target])
    elif subcmd == "impact":
        cmd_args.extend(["--compact", args.target])
    elif subcmd == "diff-impact":
        pass

    code, out = run_cbx(cmd_args, root)
    print(out)
    return code


def main() -> int:
    parser = argparse.ArgumentParser(description="Helper for codebase-index lifecycle.")
    parser.add_argument("--root", type=str, default=None, help="Project root directory")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status", help="Check index availability and stats")
    subparsers.add_parser("check-offline", help="Verify offline/no-embedding guarantees")
    subparsers.add_parser("ensure-index", help="Initialize or incrementally update index")

    query_parser = subparsers.add_parser("query", help="Query the code intelligence index")
    query_parser.add_argument(
        "type",
        choices=["search", "symbol", "refs", "impact", "diff-impact"],
        help="Query type",
    )
    query_parser.add_argument("target", nargs="?", default="", help="Symbol, file, or search string")
    query_parser.add_argument("--token-budget", type=int, default=1200, help="Max token budget for search")

    args = parser.parse_args()
    root = find_project_root(Path(args.root) if args.root else None)

    if args.command == "status":
        return cmd_status(root)
    elif args.command == "check-offline":
        return cmd_check_offline(root)
    elif args.command == "ensure-index":
        return cmd_ensure_index(root)
    elif args.command == "query":
        return cmd_query(args, root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
