# Task 1.1 — Verification of `codebase-index` & Helper Script

**Owner:** Antigravity Agent
**Status:** Completed
**Work item:** Work 001

## Objective

Verify that `codebase-index` operates completely offline without external APIs, validate its CLI commands on a real local repository, ensure `.gitignore` excludes cache directories, and create a deterministic helper utility script `scripts/codebase_index_helper.py` for health checks, offline verification, and lifecycle management.

## Context and contract

The integration must run locally without external network requests or embedding keys.
The tool creates its cache under `<root>/.claude/cache/codebase-index/index.sqlite` or configured root.
We must verify:
- CLI operates with zero network traffic.
- Incremental updates work via `codebase-index update`.
- Bounded search works via `--token-budget` and `--compact`.
- Helper script provides clean diagnosis, index status, and safe fallback.

## Scope

- In scope:
  - CLI execution tests.
  - Offline verification check.
  - Helper script for index lifecycle (`status`, `check-offline`, `ensure-index`, `doctor`).
  - Updating `.gitignore` to prevent committing `.claude/cache/`.
- Out of scope:
  - Modifying other skills (handled in Tasks 1.3 - 1.4).

## Dependencies and relevant files

- Depends on: `codebase-index==2.1.2`
- Inspect/edit: `.gitignore`, `scripts/codebase_index_helper.py`, `work/work-001-code-intelligence/tasks/task-001-verification-and-helpers.md`

## Test cases (define before implementation)

| ID | Requirement / Subtask | Category | Setup / Actor & Action | Expected Outcome | Verification Command / File | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-1.1-1 | CLI Availability | Happy Path | Run `codebase-index --help` | Exit code 0, lists commands | `codebase-index --help` | Passed |
| TC-1.1-2 | Offline Guarantees | Security/Offline | Inspect config & run doctor | Embeddings backend `noop`, no network calls | `python3 scripts/codebase_index_helper.py check-offline` | Passed |
| TC-1.1-3 | Index & Search | Happy Path | Build index on test project & search | SQLite created, returns ranked results | `codebase-index stats --json` | Passed |
| TC-1.1-4 | Gitignore Protection | Safety | Check .gitignore | `.claude/cache/` ignored | `git check-ignore -v .claude/cache/` | Passed |

## Security validation (required for every subtask)

- Changed attack surfaces / trust boundaries: Local file reading by Tree-sitter and SQLite.
- Applicable controls: Ensure no external HTTP requests, ignore secrets via `.gitignore` and `ignore_files`.
- Commands / targets / redacted results: Verified via `check-offline`.
- Disposition: Pass
- Findings and remediation: Ensure cache directories are not tracked by Git.

## Acceptance checks

- [x] `codebase-index` verified functional on local python environment.
- [x] `.gitignore` protects index cache directories (`.claude/cache/`).
- [x] Helper script created for reproducible setup, status, and offline verification.
- [x] Offline guarantees validated with concrete evidence.

## Handoff back

- Update `tasks.md` and append evidence to `notes.md`.
- Mark task complete when acceptance checks pass.
