# Work <NNN> Architecture & Design Decisions

Record critical technical decisions, tradeoffs, and contracts made during this work.

## Decision Log

- **<Date / ID> — <Decision Title>**:
  - **Context**: <Why the decision was needed>
  - **Decision**: <Chosen approach>
  - **Consequences**: <Tradeoffs, compatibility, migrations>

- **2026-10-11 — D06: Code Intelligence Programmatic Bridge**:
  - **Context**: Need standard programmatic access to `codebase-index` from optimization workflows with bounded token budgets and offline guarantees.
  - **Decision**: Build `ai_skills_opt.indexer.CodebaseIndexer` wrapping native CLI calls, pulling token budgets dynamically from the active runtime profile, verifying SQLite index state, and guaranteeing no external API tokens are consumed.
  - **Consequences**: Deterministic, profile-respecting code retrieval with zero external dependencies.
