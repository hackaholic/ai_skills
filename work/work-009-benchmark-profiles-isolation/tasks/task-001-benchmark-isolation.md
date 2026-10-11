# Task 9.1 — Benchmark Profiles & Workspace Isolation

**Owner:** Antigravity Agent
**Status:** Completed
**Work item:** Work 009 (WORK-08)

## Objective

Create `benchmarks.yaml` and `ai_skills_opt.isolation` to guarantee isolated execution across `minimal`, `standard`, and `full` profiles.

## Context and contract

Benchmark runs must not modify working repository state or contaminate shared memory caches between runs.

## Scope

- In scope:
  - `benchmarks.yaml` definition.
  - `ai_skills_opt/isolation.py` implementation (`IsolationManager`).
  - Unit tests in `tests/test_isolation.py`.
- Out of scope:
  - Markdown reporting table generation (WORK-09).

## Test cases

| ID | Requirement / Subtask | Category | Setup / Actor & Action | Expected Outcome | Verification Command / File | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-9.1-1 | Load Benchmarks YAML | Happy Path | Parse `benchmarks.yaml` | Valid task definitions returned | `python3 -m unittest discover tests` | Pass |
| TC-9.1-2 | Workspace Isolation Context | Happy Path | Enter isolation context manager | Clean isolated temp directory created | `python3 -m unittest discover tests` | Pass |
| TC-9.1-3 | State Isolation | Negative | Write to memory in isolated run | Host memory database untouched | `python3 -m unittest discover tests` | Pass |

## Acceptance checks

- [x] `benchmarks.yaml` created.
- [x] Isolation context manager implemented.
- [x] Unit tests pass cleanly.
