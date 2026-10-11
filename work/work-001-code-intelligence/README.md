# Work 001 — Code Intelligence Integration (`codebase-index`)

**Objective:** Integrate persistent, offline code intelligence into `ai_skills` using `codebase-index` so AI coding agents navigate and understand repositories using symbol search, call graphs, impact analysis, and token-bounded context rather than repeatedly reading full source files.

**Current state:** Completed (Tasks 1.1 through 1.6 verified and closed).

**Architecture:**
- CLI / Library: Native `codebase-index` (Tree-sitter + SQLite FTS5, offline, no embeddings, zero remote LLM calls).
- Reusable Skill: `code-intelligence/SKILL.md` with concise interface and sharded references in `code-intelligence/references/`.
- Lifecycle & Cache: Automatic project root discovery, index existence check, incremental freshness updates (`codebase-index update`), and fallback to grep/view_file when unavailable.
- Integration Layer: Targeted lightweight hooks in `architect`, `backend-expert`, `engineer`, `peer`, `testcase-skill`, `security-validation`, `workflow-coordinator`, and `workflow-scaffold`.

**Done when:**
- `code-intelligence` skill created with concise SKILL.md and modular references.
- All 8 existing skills updated with minimal, high-signal index-first retrieval guidance.
- Deterministic helper script provided for installation, health check, and offline verification.
- Reproducible benchmark and test suite implemented and executed.
- Documentation in `README.md` updated.
- All validation passes and changes committed.
