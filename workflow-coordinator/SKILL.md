---
name: workflow-coordinator
description: Coordinate tasks, multi-agent handoffs, and status updates using the token-lean work/ directory tree and subtask contracts.
---

# Workflow Coordinator

Manage task lifecycles, subtask contracts, and agent/developer handoffs using the structured `work/` tree. Keep context small: read only the assigned work package and task contract.

## Core Directives

1. **Context-Lean Navigation**:
   - Read `work/INDEX.md` to find the active work package (`work-NNN-<slug>/`).
   - Read ONLY that work folder's `coordination.md`, `tasks.md`, and the specific assigned contract in `tasks/task-*.md`.
   - Never load multiple unrelated work packages into context.

2. **Task Pickup Protocol**:
   - Verify task is unassigned or assigned to you. Do not take over work actively owned by another agent.
   - Update `work-NNN/coordination.md`: set current owner and mark status **Active**.
   - In `work-NNN/tasks.md`: move the task item from `Pending` to `In Progress`.
   - Follow the contract's **Pickup checklist**: reuse completed migrations, assets, and setups; never repeat completed work.

3. **Subtask Contract Creation**:
   - For multi-session, complex, or cross-agent tasks, create a contract under `work-NNN/tasks/task-XXX-<slug>.md` using `work/TASK_TEMPLATE.md`.
   - Specify:
     - **Objective & Scope**: Strict in-scope and out-of-scope boundaries.
     - **Dependencies & Files**: Explicit files to touch and required prerequisites.
     - **Test Cases**: Concrete test matrix defined *before* implementation.
     - **Security Validation**: Trust boundaries, sensitive assets, and negative tests.
   - Register the new task ID in `work-NNN/tasks.md`.

4. **Return & Handoff Protocol**:
   - Update task contract acceptance checkboxes only when verified with actual test evidence.
   - Append execution evidence, changed files, and runtime outputs to `work-NNN/notes.md`.
   - In `work-NNN/tasks.md`: mark task `[x]` and move to `Completed`.
   - In `work-NNN/coordination.md`: update status to **Returned** or **Blocked**, link the contract, and specify the exact next action for the owner.
   - If the overall work package status changes (e.g. In Progress -> Completed), update `work/INDEX.md`. Never copy contract text into global index files.
