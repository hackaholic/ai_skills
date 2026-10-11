# Task 4.1 — Programmatic Code Intelligence Bridge

**Owner:** Antigravity Agent
**Status:** Completed
**Work item:** Work 004 (WORK-03)

## Objective

Build `ai_skills_opt.indexer` module wrapping `codebase-index` with profile-aware token bounding, offline enforcement, symbol lookup, reference graph, impact analysis, and status checks.

## Context and contract

Must operate strictly offline, respect `max_tokens_per_query` from active profile, and gracefully degrade if indexing fails or is disabled.

## Scope

- In scope:
  - `ai_skills_opt/indexer.py` implementation.
  - Profile-driven parameters (`max_tokens_per_query`, `offline_only`).
  - Unit tests in `tests/test_indexer.py`.
- Out of scope:
  - Shared memory findings (WORK-04).

## Test cases

| ID | Requirement / Subtask | Category | Setup / Actor & Action | Expected Outcome | Verification Command / File | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-4.1-1 | Index Status | Happy Path | Query status of current repo | Reports indexed file count & db path | `python3 -m unittest discover tests` | Pass |
| TC-4.1-2 | Symbol Lookup | Happy Path | Query known symbol `build_parser` | Returns file & line bounds | `python3 -m unittest discover tests` | Pass |
| TC-4.1-3 | Bounded Search | Happy Path | Search with token budget constraint | Result output <= budget | `python3 -m unittest discover tests` | Pass |
| TC-4.1-4 | Disabled Config | Happy Path | Initialize indexer with enabled=False | Returns disabled status | `python3 -m unittest discover tests` | Pass |

## Acceptance checks

- [x] `ai_skills_opt/indexer.py` implemented.
- [x] Profile token limits respected.
- [x] Unit tests pass cleanly.
