# Work 009 — WORK-08: Benchmark Profiles and Isolation

**Objective:** Implement workspace isolation (`ai_skills_opt.isolation`) and profile comparison harness (`benchmarks.yaml`) to run benchmarks across profiles without test contamination.

**Current state:** Completed.

**Architecture:**
- `IsolationManager`: creates isolated temporary directories or Git worktrees with clean caches for benchmark runs.
- `benchmarks.yaml`: defines standardized benchmark tasks (code intelligence navigation, memory retrieval, blast radius calculation).
- Guarantees zero cross-profile state leakage.

**Done when:**
- `benchmarks.yaml` authored.
- `ai_skills_opt.isolation` module implemented.
- Unit tests pass in `tests/test_isolation.py`.
