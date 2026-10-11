# Work <NNN> Architecture & Design Decisions

Record critical technical decisions, tradeoffs, and contracts made during this work.

## Decision Log

- **<Date / ID> — <Decision Title>**:
  - **Context**: <Why the decision was needed>
  - **Decision**: <Chosen approach>
  - **Consequences**: <Tradeoffs, compatibility, migrations>

- **2026-10-11 — D08: Dynamic Evidence Staleness Detection**:
  - **Context**: Code intelligence and shared memory findings can easily become outdated when code is modified or refactored, causing hallucinated prompt context.
  - **Decision**: In `ai_skills_opt.freshness.ContextFreshnessValidator`, compare referenced `evidence_path` mtime and presence against finding `updated_at`. If modified, transition finding to `STALE`; if deleted, transition to `INVALIDATED`. Exclude all non-fresh findings from active prompt injection streams via `get_fresh_findings()`.
  - **Consequences**: Deterministic protection against stale context injection with zero runtime LLM overhead.
