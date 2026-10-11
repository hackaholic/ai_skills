---
name: workflow-coordinator
description: Mandatory starting workflow for any feature, task, or bugfix. Coordinates task pickup, creates subtask contracts, and tracks handoffs in work/ BEFORE writing code.
---

# Workflow Coordinator

Manage task lifecycles, subtask contracts, and agent/developer handoffs using the structured `work/` tree. Applies universally to any AI agent (Claude, GPT, Gemini, DeepSeek, etc.).

When creating or updating records, follow the shared [workflow format](../workflow-scaffold/references/workflow-format.md); preserve existing project conventions and any documented approval mechanism.

## Core Directives

1. **Mandatory Pre-Coding Gate**:
   - **Do not write code immediately.** When given any new feature, bugfix, or change, verify that an active task contract exists in `work/`.
   - If no task contract exists, create the scoped work package and atomic subtask contract first before modifying project files.

2. **Context-Lean Navigation**:
   - Read `work/INDEX.md` to find the active work package (`work-NNN-<slug>/`).
   - Read ONLY that work folder's `coordination.md`, `tasks.md`, and the specific assigned contract in `tasks/task-*.md`.
   - Never load multiple unrelated work packages into context.

3. **Task Pickup Protocol**:
   - Verify task is unassigned or assigned to you. Do not take over work actively owned by another agent.
   - Update `work-NNN/coordination.md`: set current owner and mark status **Active**.
   - In `work-NNN/tasks.md`: move the task item from `Pending` to `In Progress`.
   - Follow the contract's **Pickup checklist**: reuse completed migrations, assets, and setups; never repeat completed work.

4. **Subtask Contract Creation**:
   - For multi-session, complex, or cross-agent tasks, create a contract under `work-NNN/tasks/task-XXX-<slug>.md` using `work/TASK_TEMPLATE.md`.
   - Specify:
     - **Objective & Scope**: Strict in-scope and out-of-scope boundaries.
     - **Dependencies & Files**: Explicit files to touch and required prerequisites.
     - **Test Cases**: Concrete test matrix defined *before* implementation.
     - **Security Validation**: Trust boundaries, sensitive assets, and negative tests.
   - Register the new task ID in `work-NNN/tasks.md`.

5. **Return & Handoff Protocol**:
   - Update task contract acceptance checkboxes only when verified with actual test evidence.
   - Append execution evidence, changed files, and runtime outputs to `work-NNN/notes.md`.
   - In `work-NNN/tasks.md`: mark task `[x]` and move to `Completed`.
   - In `work-NNN/coordination.md`: update status to **Returned** or **Blocked**, link the contract, and specify the exact next action for the owner.
   - If the overall work package status changes (e.g. In Progress -> Completed), update `work/INDEX.md`. Never copy contract text into global index files.
