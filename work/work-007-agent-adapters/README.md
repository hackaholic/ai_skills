# Work 007 — WORK-06: Agent Adapters

**Objective:** Implement unified agent adapter abstractions (`ai_skills_opt.adapters`) for `gemini`, `codex`, and `bob`, standardizing tool invocation, token accounting, and fallback behavior.

**Current state:** Completed.

**Architecture:**
- Base class `AgentAdapter`: standard interface `execute_turn(prompt, context) -> AgentResult`.
- Concrete adapters: `GeminiAdapter`, `CodexAdapter`, `BobAdapter`.
- `BobAdapter` gracefully handles missing `bob` binary via fallback/mock execution mode to ensure CI/test stability without failing ungracefully.

**Done when:**
- `ai_skills_opt.adapters` module implemented.
- Tool invocation protocol and structured execution metrics captured.
- Unit tests pass in `tests/test_adapters.py`.
