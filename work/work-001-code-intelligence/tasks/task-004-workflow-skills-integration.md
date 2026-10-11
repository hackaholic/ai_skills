# Task 1.4 — Workflow Skills Integration

**Owner:** Antigravity Agent
**Status:** Completed
**Work item:** Work 001

## Objective

Integrate code-intelligence into workflow coordination and project scaffolding:
1. `workflow-coordinator/SKILL.md`: Instruct agents to ensure index availability (`codebase-index update` or `python3 scripts/codebase_index_helper.py ensure-index`) without duplicating raw index data into work items, and without rebuilding the index repeatedly for every subtask.
2. `workflow-scaffold/SKILL.md`: When scaffolding or migrating a repository, configure `.gitignore` with `.claude/cache/` and index cache ignore rules, and offer/run initial indexing without forcing users to commit binary databases.
3. `workflow-scaffold/templates/AGENTS.md`: Update universal agent instructions with index-first navigation (Step 1.1: Use code-intelligence for symbol lookup and call-graph navigation before reading full source files).

## Context and contract

Preserve all existing multi-agent coordination, subtask contract rules, and prompt interceptor logic.

## Scope

- In scope:
  - `workflow-coordinator/SKILL.md`.
  - `workflow-scaffold/SKILL.md`.
  - `workflow-scaffold/templates/AGENTS.md`.
- Out of scope:
  - Benchmarks (handled in Task 1.5).

## Dependencies and relevant files

- Depends on: Task 1.3.
- Inspect/edit: `workflow-coordinator/SKILL.md`, `workflow-scaffold/SKILL.md`, `workflow-scaffold/templates/AGENTS.md`.

## Test cases (define before implementation)

| ID | Requirement / Subtask | Category | Setup / Actor & Action | Expected Outcome | Verification Command / File | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-1.4-1 | Coordination Guidance | Happy Path | Check workflow-coordinator instructions | References index freshness, forbids raw index in work | Grep check | Passed |
| TC-1.4-2 | Scaffold Ignore Config | Safety | Check workflow-scaffold instructions | Automatically sets .gitignore for index caches | Grep check | Passed |
| TC-1.4-3 | Universal AGENTS.md | Standards | Check templates/AGENTS.md | Index-first step present, existing rules intact | File check | Passed |

## Security validation

- Ensure index files are never added to Git.
- Disposition: Pass.

## Acceptance checks

- [x] `workflow-coordinator/SKILL.md` updated.
- [x] `workflow-scaffold/SKILL.md` updated.
- [x] `workflow-scaffold/templates/AGENTS.md` updated.
- [x] Test cases TC-1.4-1 to TC-1.4-3 pass.

## Handoff back

- Update `tasks.md`, `notes.md`, and advance to Task 1.5.
