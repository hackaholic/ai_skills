# Work 004 — WORK-03: Code-Intelligence Integration

**Objective:** Integrate `codebase-index` programmatically into `ai_skills_opt.indexer` respecting runtime profiles, token budgets, offline enforcement, and incremental updates.

**Current state:** Completed.

**Architecture:**
- Bridge module `ai_skills_opt.indexer`: invokes `codebase-index` CLI and sqlite state with profile-constrained token budgets and strict `--offline` guarantees.
- Provides high-level Python API: `CodebaseIndexer` for queries (symbol, references, impact, bounded search) and lifecycle management (status, update).
- Tests verify bounded token enforcement, offline mode, and error handling.

**Done when:**
- `ai_skills_opt.indexer` implemented.
- Unit tests pass in `tests/test_indexer.py`.
- Integration verified against existing codebase index cache.
