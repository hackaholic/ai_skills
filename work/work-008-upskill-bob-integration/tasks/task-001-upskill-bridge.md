# Task 8.1 — Upskill and Bob Evaluation Integration

**Owner:** Antigravity Agent
**Status:** Completed
**Work item:** Work 008 (WORK-07)

## Objective

Build `ai_skills_opt.evaluation` connecting `upskill` capabilities and `BobAdapter` to execute structured skill evaluations and capture telemetry.

## Context and contract

Must operate deterministically. If `upskill` or `bob` require external API tokens that are unset, fallback to deterministic local metric simulation rather than throwing unhandled exceptions.

## Scope

- In scope:
  - `SkillEvaluator` in `ai_skills_opt/evaluation.py`.
  - Execution of benchmark scenarios with adapter selection.
  - Unit tests in `tests/test_evaluation.py`.
- Out of scope:
  - Benchmark profile isolation worktrees (WORK-08).

## Test cases

| ID | Requirement / Subtask | Category | Setup / Actor & Action | Expected Outcome | Verification Command / File | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-8.1-1 | Local Evaluator Run | Happy Path | Run evaluation with Gemini adapter | Returns EvaluatorReport | `python3 -m unittest discover tests` | Pass |
| TC-8.1-2 | Bob Evaluation Fallback | Graceful Degrade | Run evaluation with Bob adapter | Simulates report gracefully | `python3 -m unittest discover tests` | Pass |
| TC-8.1-3 | Metric Calculations | Quality | Check token reduction & pass rate | Correct calculation | `python3 -m unittest discover tests` | Pass |

## Acceptance checks

- [x] `ai_skills_opt/evaluation.py` implemented.
- [x] Safe execution without external API dependencies.
- [x] Unit tests pass cleanly.
