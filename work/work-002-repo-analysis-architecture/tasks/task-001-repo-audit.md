# Task 2.1 — Repository & Dependency Audit

**Owner:** Antigravity Agent
**Status:** Completed
**Work item:** Work 002 (WORK-01)

## Objective

Audit all existing skills, templates, references, helper scripts, dependencies, and test baselines in `ai_skills`. Document reusable mechanisms, missing capabilities, and integration points for the optimization framework.

## Context and contract

Preserve the existing Markdown architecture. Identify how YAML configuration, code intelligence, shared memory, and benchmarks connect into existing workflows.

## Scope

- In scope:
  - Inventory of existing skills, files, and templates.
  - Analysis of runtime tools (`codebase-index`, `upskill`, python environment).
  - Identification of integration points.
- Out of scope:
  - Writing the configuration code (WORK-02).

## Test cases (define before implementation)

| ID | Requirement / Subtask | Category | Setup / Actor & Action | Expected Outcome | Verification Command / File | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-2.1-1 | Skill Inventory Audit | Happy Path | Scan all skills in repo | 11 skills identified with SKILL.md | `find . -maxdepth 2 -name "SKILL.md" \| sort` | Pass |
| TC-2.1-2 | Existing Test Baseline | Quality | Run existing unit tests | 8/8 tests pass | `python3 tests/test_code_intelligence.py` | Pass |
| TC-2.1-3 | Dependency & Tool Check | Environment | Check codebase-index, upskill | Versions verified | CLI checks | Pass |

## Acceptance checks

- [x] Repository inventory documented.
- [x] Existing test baseline confirmed passing.
- [x] Tool availability recorded.

## Handoff back

- Mark task complete, update `tasks.md` and `notes.md`.
