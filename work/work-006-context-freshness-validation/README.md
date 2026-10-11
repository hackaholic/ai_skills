# Work 006 — WORK-05: Context Freshness and Validation

**Objective:** Implement automated context freshness verification (`ai_skills_opt.freshness`) to detect stale findings based on file modification times, git commit changes, and evidence validation.

**Current state:** Completed.

**Architecture:**
- `ContextFreshnessValidator` checks finding evidence (`evidence_path`, `git_hash`, `mtime`).
- Detects stale findings when referenced files are modified or deleted.
- Transitions status to `STALE` or `INVALIDATED` and strips stale findings from active prompt injection contexts.

**Done when:**
- `ai_skills_opt.freshness` module implemented.
- Automatic staleness detection for modified and deleted evidence files.
- Unit tests pass in `tests/test_freshness.py`.
