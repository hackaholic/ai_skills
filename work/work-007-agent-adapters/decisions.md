# Work <NNN> Architecture & Design Decisions

Record critical technical decisions, tradeoffs, and contracts made during this work.

## Decision Log

- **<Date / ID> — <Decision Title>**:
  - **Context**: <Why the decision was needed>
  - **Decision**: <Chosen approach>
  - **Consequences**: <Tradeoffs, compatibility, migrations>

- **2026-10-11 — D09: Unified Agent Adapters and Degradation Strategy**:
  - **Context**: The framework must support disparate agents (`gemini`, `codex`, `bob`) while maintaining reproducible benchmarks even when proprietary/external binaries are not present.
  - **Decision**: Define base `AgentAdapter` producing standardized `AgentResult` (token counts, latency, tool calls). For `BobAdapter`, dynamically inspect system binary presence; if missing, execute an explicit fallback simulation mode recording `metadata={"mode": "fallback_simulation", "available": False}` rather than aborting test/benchmark workflows.
  - **Consequences**: Continuous testing and benchmark runs succeed deterministically regardless of workstation environment differences.
