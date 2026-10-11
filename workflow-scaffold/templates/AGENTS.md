# Universal Agent Workflow & Coding Rules

These rules apply universally to any AI agent (Claude, GPT, Gemini, DeepSeek, Codex, etc.) working in this repository. The repository is the source of truth.

## 1. Mandatory Pre-Coding Gate (DO NOT SKIP)

**STOP! Before modifying or writing any application code:**
1. Check `work/INDEX.md` to identify the active work package (`work-NNN-<slug>/`).
2. If this is a new feature, bugfix, or non-trivial change without an active task contract:
   - **DO NOT WRITE CODE IMMEDIATELY.**
   - First invoke the `$workflow-coordinator` or `$architect` skill.
   - Create or assign the work item in `work/INDEX.md` and define the subtask contract in `work/work-NNN/tasks/task-XXX.md` using `work/TASK_TEMPLATE.md`.
   - Lock in Objective, Scope, Test Cases, and Security requirements before touching code.
3. If picking up an existing task, read only that work folder's `coordination.md`, `tasks.md`, and the assigned `task-*.md`. Mark it `In Progress`.

## 2. Engineering Standards

- **Index-First Navigation**: Do not read entire source files to find definitions or call sites. Use `$code-intelligence` (`codebase-index symbol <Name>`, `codebase-index refs <Name>`) to locate targets and view only bounded lines. Refresh affected entries via `codebase-index update` after changes.
- **Strict Anti-Monolith Rule**: Never write all logic in a single file. Separate routes/controllers, services, repositories/data access, models, and utilities into dedicated files (< 250 LOC typical).
- **Zero Hardcoding**: Never hardcode URLs, ports, magic numbers, or credentials. Load all configuration from environment variables and a centralized configuration file (YAML default, with typed schema validation at startup).
- **Code Reusability & DRY**: Extract shared operations into reusable utilities, base classes, and templates rather than copy-pasting code.
- **Environment Parity**: Write production-grade code locally. Maintain identical application code, schemas, and security controls across environments.

## 3. Verification & Return Handoff

1. Execute the defined test cases and negative security checks. Record exact commands and results.
2. Update the task contract checkboxes with verification evidence.
3. Append execution evidence and changed files to `work/work-NNN/notes.md`.
4. In `work-NNN/tasks.md`, mark the task `[x] Completed`.
5. Update `work-NNN/coordination.md` to `Returned` or `Blocked`, with clear next actions for the owner.
