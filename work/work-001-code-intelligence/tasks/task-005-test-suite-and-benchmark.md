# Task 1.5 — Test Suite & Benchmark

**Owner:** Antigravity Agent
**Status:** Completed
**Work item:** Work 001

## Objective

Create and execute a reproducible test suite and benchmark in `tests/test_code_intelligence.py` and `scripts/benchmark_retrieval.py`:
1. **Unit & Integration Tests**:
   - Verify `codebase-index` CLI and helper script lifecycle (ensure-index, status, check-offline, search, symbol, refs, impact, diff-impact).
   - Test incremental update when a file is modified.
   - Test fallback behavior when index is absent or corrupted.
2. **Reproducible Benchmark**:
   - Compare Approach A (Non-indexed: full file reads and naive searches) vs Approach B (Index-assisted: symbol lookup, callers graph, bounded search).
   - Measure real metrics: Lines retrieved, estimated tokens, files inspected, search latency, and answer accuracy.

## Context and contract

Measure real metrics. Do not fabricate benchmarks or token counts. Report limitations explicitly.

## Scope

- In scope:
  - `tests/test_code_intelligence.py`.
  - `scripts/benchmark_retrieval.py`.
  - Execution logs recorded in `notes.md`.
- Out of scope:
  - Final documentation (handled in Task 1.6).

## Dependencies and relevant files

- Depends on: Tasks 1.1 - 1.4.
- Inspect/edit: `tests/test_code_intelligence.py`, `scripts/benchmark_retrieval.py`.

## Test cases (define before implementation)

| ID | Requirement / Subtask | Category | Setup / Actor & Action | Expected Outcome | Verification Command / File | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-1.5-1 | Test Suite Execution | Quality | Run unit test suite | All test cases pass | `python3 tests/test_code_intelligence.py` | Passed (8/8) |
| TC-1.5-2 | Benchmark Execution | Performance | Run benchmark script | Real measurements output | `python3 scripts/benchmark_retrieval.py` | Passed |
| TC-1.5-3 | Token Reduction Measured | Verification | Compare lines & tokens | Index retrieval uses >50% fewer lines/tokens | Benchmark results | Passed (94.2% reduction) |

## Security validation

- All tests operate on local fixtures; zero remote calls.
- Disposition: Pass.

## Acceptance checks

- [x] `tests/test_code_intelligence.py` passes.
- [x] `scripts/benchmark_retrieval.py` executes and outputs real measurements.
- [x] Test cases TC-1.5-1 to TC-1.5-3 pass.

## Handoff back

- Record metrics in `notes.md`, mark task Complete, advance to Task 1.6.
