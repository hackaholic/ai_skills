# Work 001 Architecture & Design Decisions

Record critical technical decisions, tradeoffs, and contracts made during this work.

## Decision Log

- **2026-10-11 — D01: Engine Selection & Version**:
  - **Context**: Need local, offline code intelligence without LLM API token consumption or external services.
  - **Decision**: Pinned `codebase-index==2.1.2` (native Tree-sitter + SQLite FTS5). Embeddings backend default is explicitly set to `noop` (disabled), guaranteeing 0 network calls and 0 embedding token costs.
  - **Consequences**: Fast indexing, completely offline, zero API keys required. Operates via CLI (`codebase-index` / `cbx`) and MCP server.

- **2026-10-11 — D02: Token-Lean Skill Design**:
  - **Context**: Avoid bloating context windows with large instructions or raw index graph dumps.
  - **Decision**: Keep `code-intelligence/SKILL.md` under 350 words focusing on CLI commands and return formats. Shard detailed guides into `references/offline-verification.md` and `references/retrieval-patterns.md`. Skills retrieve bounded results (`--limit`, `--token-budget`, `--compact`).
  - **Consequences**: Skills load only minimal instructions; actual code inspection uses targeted line spans.
