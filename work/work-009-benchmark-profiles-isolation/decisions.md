# Work <NNN> Architecture & Design Decisions

Record critical technical decisions, tradeoffs, and contracts made during this work.

## Decision Log

- **<Date / ID> — <Decision Title>**:
  - **Context**: <Why the decision was needed>
  - **Decision**: <Chosen approach>
  - **Consequences**: <Tradeoffs, compatibility, migrations>

- **2026-10-11 — D11: Benchmark Workspace Isolation Architecture**:
  - **Context**: Benchmarking multiple profiles (`minimal`, `standard`, `full`) on the same repository could result in shared memory leakage or dirty git states affecting subsequent profile measurements.
  - **Decision**: Provide `isolated_workspace` context manager in `ai_skills_opt.isolation`. Standardize evaluation benchmark tasks in `benchmarks.yaml`. All scratch data, SQLite memory, and temporary indexes during a benchmark run are sandboxed and cleaned up upon exit.
  - **Consequences**: Zero cross-test state leakage, deterministic benchmark reproducibility.
