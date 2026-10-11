# Task 1.2 — Reusable `code-intelligence` Skill

**Owner:** Antigravity Agent
**Status:** Completed
**Work item:** Work 001

## Objective

Create the `code-intelligence` skill in `code-intelligence/SKILL.md` along with reference guides in `code-intelligence/references/`:
1. `SKILL.md`: Concise (< 350 words) imperative interface covering the repository footprint lifecycle (Project Open -> Index Check -> Incremental Update -> Retrieval -> Fallback), CLI commands, and token-bounded output flags.
2. `references/offline-verification.md`: Complete verification steps proving zero network calls, no embedding tokens, and local Tree-sitter + SQLite operations.
3. `references/retrieval-patterns.md`: Concrete query recipes for symbol lookups, call graph expansion, blast-radius impact analysis, and token budgeting.

## Context and contract

The skill must be model-agnostic, token-lean, and avoid embedding raw database dumps or long conversational essays into the prompt. Detailed procedures are sharded into `references/`.

## Scope

- In scope:
  - `code-intelligence/SKILL.md` with YAML frontmatter.
  - `code-intelligence/references/offline-verification.md`.
  - `code-intelligence/references/retrieval-patterns.md`.
- Out of scope:
  - Editing other skills (handled in Task 1.3).

## Dependencies and relevant files

- Depends on: Task 1.1 (`codebase-index` verified and helper utility created).
- Inspect/edit: `code-intelligence/SKILL.md`, `code-intelligence/references/*`.

## Test cases (define before implementation)

| ID | Requirement / Subtask | Category | Setup / Actor & Action | Expected Outcome | Verification Command / File | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-1.2-1 | Frontmatter Validity | Happy Path | Parse SKILL.md frontmatter | `name: code-intelligence`, concise description | YAML/frontmatter check | Passed |
| TC-1.2-2 | Token / Word Budget | Token Efficiency | Check word count | `SKILL.md` < 350 words | `wc -w code-intelligence/SKILL.md` | Passed (295w) |
| TC-1.2-3 | Reference Resolution | Links | Check relative references | `references/*.md` exist and resolve | `ls code-intelligence/references` | Passed |
| TC-1.2-4 | Fallback Documented | Safety | Check fallback instructions in SKILL.md | Explicit grep/view_file fallback | Grep check | Passed |

## Security validation (required for every subtask)

- Changed attack surfaces: Index retrieval commands.
- Applicable controls: Bounded `--token-budget`, explicit offline verification reference, fallback behavior.
- Disposition: Pass.

## Acceptance checks

- [x] `code-intelligence/SKILL.md` created with tight, high-signal directives (< 350 words).
- [x] `references/offline-verification.md` created with actionable diagnostic commands.
- [x] `references/retrieval-patterns.md` created with CLI recipes.
- [x] Test cases TC-1.2-1 through TC-1.2-4 pass.

## Handoff back

- Update `tasks.md`, `notes.md`, and mark task Complete.
