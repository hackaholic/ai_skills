# Task 3.1 — Configuration Schema & Profile Resolver

**Owner:** Antigravity Agent
**Status:** Completed
**Work item:** Work 003 (WORK-02)

## Objective

Create `config.yaml` and Python module `ai_skills_opt.config` to validate framework configuration and resolve runtime profiles (`minimal`, `standard`, `full`, `benchmark`).

## Context and contract

Configuration must be versioned, reject invalid values early with readable errors, and support profile overrides without mutating disk state.

## Scope

- In scope:
  - `config.yaml` definition.
  - `ai_skills_opt/config.py` parser, schema models, profile inheritance/overrides.
  - Unit tests in `tests/test_config.py`.
- Out of scope:
  - Codebase indexing logic (WORK-03).
  - Shared memory implementation (WORK-04).

## Test cases

| ID | Requirement / Subtask | Category | Setup / Actor & Action | Expected Outcome | Verification Command / File | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-3.1-1 | Load Default Config | Happy Path | Load `config.yaml` without profile | Resolves `standard` profile defaults | `python3 -m unittest discover tests` | Pass |
| TC-3.1-2 | Profile Override Resolution | Happy Path | Resolve `minimal`, `benchmark`, `full` | Profile values override base | `python3 -m unittest discover tests` | Pass |
| TC-3.1-3 | Schema Validation Error | Negative | Provide invalid type / missing version | SchemaValidationError raised | `python3 -m unittest discover tests` | Pass |
| TC-3.1-4 | CLI Config Show | Integration | Run `ai-skills config show --profile minimal` | JSON/YAML dump matches resolved config | CLI execution | Pass |

## Acceptance checks

- [x] `config.yaml` created and valid.
- [x] Schema validation and profile resolution implemented.
- [x] Unit tests pass with 100% coverage on config module.
