# Work 002 Architecture & Design Decisions

## Decision Log

- **2026-10-11 — D01: Framework Extension Strategy**:
  - **Context**: The user requested extending `ai_skills` into an optimization framework without rewriting working functionality, without creating a competing framework, and without introducing unnecessary daemons.
  - **Decision**: Keep existing Markdown skills as the primary agent instruction medium. Introduce a lightweight Python package `ai_skills_opt` (or minimal CLI `ai-skills`) for deterministic operations: config validation, index lifecycle, shared memory SQLite storage, and benchmark running.
  - **Consequences**: Skills remain 100% portable and model-agnostic. Deterministic code enforces configuration, benchmarks, and data persistence.

- **2026-10-11 — D02: Shared Memory Technology Selection**:
  - **Context**: Need lightweight, offline, cross-agent persistent memory without introducing Neo4j, Redis, or heavy vector database daemons.
  - **Decision**: Implement a local SQLite-backed shared memory engine with FTS5 lexical search and optional local embedding support. Store discrete verified findings (`VERIFIED`, `HYPOTHESIS`, `STALE`, `INVALIDATED`), not full conversation transcripts.
  - **Consequences**: Zero external services, zero API costs, instant queries, portable single-file SQLite database.

- **2026-10-11 — D03: Context Freshness and Evidence Validation**:
  - **Context**: LLM agents suffer from stale assumptions when files change or when prior agent runs left unverified notes.
  - **Decision**: Findings stored in shared memory must carry metadata: `evidence_path`, `line_range`, `git_hash` (or mtime), and status (`VERIFIED`, `HYPOTHESIS`, `STALE`, `INVALIDATED`). Prior to retrieval or injection into prompt contexts, an automated staleness check validates whether referenced files/lines have changed. If changed, findings transition to `STALE`.
  - **Consequences**: Zero hallucinated stale contexts passed to agents. Stale findings require re-verification or are purged from active prompts.

- **2026-10-11 — D04: Benchmarking and Isolation Architecture**:
  - **Context**: Evaluating agent skills and retrieval efficiency requires comparing runs across multiple profiles (`minimal`, `standard`, `full`, `benchmark`) without contamination.
  - **Decision**: The benchmark harness isolates runs using distinct temporary execution directories or clean Git worktrees, isolated SQLite caches, and deterministic task definitions in `benchmarks.yaml`. Upskill and agent adapters log structured execution metrics (token counts, wall time, tool calls, accuracy/pass rates).
  - **Consequences**: Deterministic, reproducible evaluation; no state leakage across benchmark iterations.
