# Task 6.1 — Automated Context Freshness & Evidence Validator

**Owner:** Antigravity Agent
**Status:** Completed
**Work item:** Work 006 (WORK-05)

## Objective

Build `ai_skills_opt.freshness` module to validate finding evidence, detect file mutations, mark stale entries, and provide clean context filtering.

## Context and contract

Never feed stale context to agents. If evidence file has changed since the finding was recorded, mark finding status as `STALE` and exclude from active prompt injection unless explicitly overridden.

## Scope

- In scope:
  - `ContextFreshnessValidator` class in `ai_skills_opt/freshness.py`.
  - Evidence checks: file existence, mtime, git commit diff.
  - Filtering API: `get_fresh_findings()`.
  - Unit tests in `tests/test_freshness.py`.
- Out of scope:
  - Agent adapter prompting (WORK-06).

## Test cases

| ID | Requirement / Subtask | Category | Setup / Actor & Action | Expected Outcome | Verification Command / File | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-6.1-1 | Valid Fresh Finding | Happy Path | Check finding where evidence file unmodified | Status remains VERIFIED | `python3 -m unittest discover tests` | Pass |
| TC-6.1-2 | Modified File Staleness | Negative | Modify evidence file on disk | Finding marked STALE | `python3 -m unittest discover tests` | Pass |
| TC-6.1-3 | Deleted File Invalidation | Negative | Delete evidence file on disk | Finding marked INVALIDATED | `python3 -m unittest discover tests` | Pass |
| TC-6.1-4 | Fresh Filter Pipeline | Happy Path | Query fresh findings for prompt | Excludes STALE/INVALIDATED | `python3 -m unittest discover tests` | Pass |

## Acceptance checks

- [x] `ai_skills_opt/freshness.py` implemented.
- [x] Automated file mutation & deletion detection.
- [x] Unit tests pass cleanly.
