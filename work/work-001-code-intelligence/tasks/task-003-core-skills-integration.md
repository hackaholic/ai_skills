# Task 1.3 — Core Skills Integration

**Owner:** Antigravity Agent
**Status:** Completed
**Work item:** Work 001

## Objective

Update existing core skills with targeted, lightweight index-first retrieval guidance without bloating their token counts:
- `architect`: Use `code-intelligence` (`architecture`, `symbol`, `impact`) to inspect existing module boundaries and dependency relationships before designing subtasks.
- `backend-expert`: Use `code-intelligence` (`symbol`, `refs`) to discover existing interfaces, service dependencies, and query patterns before writing backend logic.
- `engineer`: Follow the 8-step index-first cycle: query symbol/callers -> inspect bounded range -> modify -> refresh index (`codebase-index update`).
- `peer`: Use `code-intelligence` (`diff-impact`, `refs`) to verify callers and downstream blast radius of changed symbols.
- `testcase-skill`: Use `code-intelligence` (`symbol`, `refs`) to locate the implementation under test and identify dependent call paths.
- `security-validation`: Use `code-intelligence` (`refs`, `impact`) to trace data flow from entry points to sensitive sinks.

## Context and contract

Keep each addition minimal (1-3 sentences per skill). Do not duplicate the indexing engine documentation. Point directly to `[code-intelligence](../../../code-intelligence/SKILL.md)`.

## Scope

- In scope:
  - Updates to `architect/SKILL.md`.
  - Updates to `backend-expert/SKILL.md`.
  - Updates to `engineer/SKILL.md`.
  - Updates to `peer/SKILL.md`.
  - Updates to `testcase-skill/SKILL.md`.
  - Updates to `security-validation/SKILL.md`.
- Out of scope:
  - Workflow skills (handled in Task 1.4).

## Dependencies and relevant files

- Depends on: Task 1.2 (`code-intelligence/SKILL.md`).
- Inspect/edit: `architect/SKILL.md`, `backend-expert/SKILL.md`, `engineer/SKILL.md`, `peer/SKILL.md`, `testcase-skill/SKILL.md`, `security-validation/SKILL.md`.

## Test cases (define before implementation)

| ID | Requirement / Subtask | Category | Setup / Actor & Action | Expected Outcome | Verification Command / File | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-1.3-1 | Word Count Constraint | Token Efficiency | Check word count of modified skills | Each skill remains < 400 words | `wc -w */SKILL.md` | Passed (< 400w) |
| TC-1.3-2 | Relative Link Validity | Links | Check relative links to code-intelligence | Links resolve cleanly | File check | Passed |
| TC-1.3-3 | Post-edit Index Refresh | Lifecycle | Modify files and run `codebase-index update` | Incremental update succeeds | `codebase-index update` | Passed |

## Security validation

- Tracing call sites is evidence, not proof of complete runtime security. Security skills retain negative test requirements.
- Disposition: Pass.

## Acceptance checks

- [x] All 6 core skills updated with index-first navigation.
- [x] Token count per skill strictly preserved (< 400 words).
- [x] Test cases TC-1.3-1 to TC-1.3-3 pass.

## Handoff back

- Update `tasks.md`, `notes.md`, and advance to Task 1.4.
