# Task 7.1 — Unified Agent Adapter Layer

**Owner:** Antigravity Agent
**Status:** Completed
**Work item:** Work 007 (WORK-06)

## Objective

Build `ai_skills_opt.adapters` implementing consistent agent interfaces for `gemini`, `codex`, and `bob`.

## Context and contract

Must decouple agent runtime differences. Support fallback simulation when external binary (such as `bob`) is not installed. Return standardized execution results with token counts, latency, and tool calls.

## Scope

- In scope:
  - Base `AgentAdapter`, `AgentResult`.
  - Concrete adapters: `GeminiAdapter`, `CodexAdapter`, `BobAdapter`.
  - Factory: `get_adapter(name, config)`.
  - Unit tests in `tests/test_adapters.py`.
- Out of scope:
  - Upskill dataset orchestration (WORK-07).

## Test cases

| ID | Requirement / Subtask | Category | Setup / Actor & Action | Expected Outcome | Verification Command / File | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-7.1-1 | Gemini Adapter Execution | Happy Path | Execute query with Gemini adapter | Returns formatted AgentResult | `python3 -m unittest discover tests` | Pass |
| TC-7.1-2 | Codex Adapter Execution | Happy Path | Execute query with Codex adapter | Returns formatted AgentResult | `python3 -m unittest discover tests` | Pass |
| TC-7.1-3 | Bob Fallback Execution | Graceful Degrade | Execute Bob adapter without binary | Executes in fallback mode | `python3 -m unittest discover tests` | Pass |
| TC-7.1-4 | Adapter Factory Validation | Negative | Request unsupported agent name | Raises AdapterError | `python3 -m unittest discover tests` | Pass |

## Acceptance checks

- [x] `ai_skills_opt/adapters.py` implemented.
- [x] Bob fallback mode working reliably without crashing.
- [x] Unit tests pass cleanly.
