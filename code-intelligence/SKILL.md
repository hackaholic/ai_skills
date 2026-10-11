---
name: code-intelligence
description: Persistent, offline code intelligence via codebase-index. Retrieves symbols, callers, blast-radius impact, and bounded context without burning tokens.
---

# Code Intelligence

Navigate and analyze repositories using persistent, local Tree-sitter + SQLite code intelligence (`codebase-index`). Prioritize targeted symbol and call-graph queries over reading entire files.

## Lifecycle & Freshness

1. **Root & Index Check**:
   - Locate root via nearest `.git` or `.claude`.
   - Check if index exists at `<root>/.claude/cache/codebase-index/index.sqlite` (or run `python3 scripts/codebase_index_helper.py status`).
2. **Freshness Maintenance**:
   - If missing: Run `codebase-index index` to initialize.
   - If existing: Run `codebase-index update` for incremental re-indexing (mtime/git aware).
   - Never rebuild unconditionally. After modifying files, run `codebase-index update` to refresh affected entries.
3. **Graceful Fallback**:
   - If `codebase-index` is not installed or fails: Immediately fall back to `grep_search` and targeted `view_file`. Do not retry in a loop or halt task execution.

## Index-First Query Commands

Use the native CLI (`codebase-index` or `python3 scripts/codebase_index_helper.py query`):

- **Symbol Definition**:
  `codebase-index symbol <Name>` (find exact file, lines, and signature).
- **Callers & References**:
  `codebase-index refs <Name> --compact` (shows callers without full file reads).
- **Change Impact / Blast Radius**:
  `codebase-index impact <Target> --compact` (upstream/downstream dependency walk).
  `codebase-index diff-impact` (predicts blast radius of current Git diff).
- **Hybrid Search (Bounded Tokens)**:
  `codebase-index search "<query>" --compact --token-budget 1200`
- **Architecture Overview**:
  `codebase-index architecture` (module graph and central hubs).

## Retrieval Discipline

- **Never read entire files** when searching for functionality. Query symbols or callers first, then view only the returned `file:lines` range.
- Use `--compact` and `--token-budget` to avoid context window explosion.
- Graph edges do not capture dynamic reflection or runtime DI; treat index output as navigational evidence, not absolute runtime truth.

For offline guarantees and deep query patterns, read:
- [Offline Verification Guide](references/offline-verification.md)
- [Retrieval Patterns Reference](references/retrieval-patterns.md)
