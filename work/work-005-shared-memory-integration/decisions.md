# Work <NNN> Architecture & Design Decisions

Record critical technical decisions, tradeoffs, and contracts made during this work.

## Decision Log

- **<Date / ID> — <Decision Title>**:
  - **Context**: <Why the decision was needed>
  - **Decision**: <Chosen approach>
  - **Consequences**: <Tradeoffs, compatibility, migrations>

- **2026-10-11 — D07: SQLite + FTS5 Shared Memory Design**:
  - **Context**: Need cross-agent knowledge persistence without Redis, Postgres, Neo4j, or external vector DB daemons.
  - **Decision**: Embed SQLite database with an FTS5 full-text search table and automatic synchronization triggers. Findings are partitioned by `namespace` with strictly typed statuses (`VERIFIED`, `HYPOTHESIS`, `STALE`, `INVALIDATED`), timestamp tracking, and evidence metadata (`evidence_path`, `line_range`, `git_hash`).
  - **Consequences**: Zero memory leaks, zero daemon maintenance, instant multi-agent read/write access.
