---
name: workflow-scaffold
description: Scaffold the token-lean work/ workflow tree for a new project or migrate an existing project backlog into work packages.
---

# Workflow Scaffolding & Migration

Initialize the token-lean `work/` directory workflow for a new project, or migrate an existing project's unstructured `TODO.md` / backlog into modular work packages.

## Core Directives

1. **Bootstrap New Project Workflow**:
   - Check if `work/` exists. If not, create:
     - `AGENTS.md`: Universal repository-level rules forcing all agents to use the workflow gate.
     - `work/INDEX.md`: Global active work directory.
     - `work/TASK_TEMPLATE.md`: Reusable contract template for subtasks.
     - `work/work-001-<slug>/`: Initial work package containing:
       - `README.md`: Objective and architecture.
       - `coordination.md`: Owner handoff entry point.
       - `tasks.md`: Task checklist (In Progress, Pending, Completed).
       - `decisions.md`: Architecture Decision Records (ADRs).
       - `notes.md`: Execution evidence and test logs.
       - `tasks/`: Directory for atomic subtask contracts.
   - Use templates from [`templates/`](templates/).

2. **Migrate Existing Project to `work/`**:
   - Scan existing task sources: `README.md`, `TODO.md`, `docs/`, or open issues.
   - Group unstructured items into 2–6 coherent, scoped **Work Packages** (e.g. `work-001-auth`, `work-002-dashboard`, `work-003-api`).
   - Create `work/INDEX.md` linking each package with its initial status (`In Progress`, `Pending`, `Completed`).
   - Populate each package's `tasks.md` with the extracted tasks.
   - Replace or update legacy `TODO.md` with a clean pointer to `work/INDEX.md`.

3. **Add a New Work Package**:
   - Inspect `work/INDEX.md` to find the highest work number (e.g. `003`).
   - Increment to create `work/work-<NNN>-<slug>/` (e.g. `work/work-004-billing/`).
   - Copy the standard package templates (`README.md`, `coordination.md`, `tasks.md`, `decisions.md`, `notes.md`, and `tasks/`).
   - Append the new work entry to `work/INDEX.md`.

4. **Token-Lean Output Format**:
   Deliver a concise summary:
   - **Created Structure**: Tree of generated `work/` folders.
   - **Active Packages**: List of work packages in `work/INDEX.md`.
   - **Next Action**: Recommended first task contract to pick up with [workflow-coordinator](../workflow-coordinator/SKILL.md).
