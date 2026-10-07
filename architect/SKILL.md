---
name: architect
description: Scope full-stack features, design system boundaries, API/data contracts, and decompose tasks with minimal token overhead.
---

# Architect

Plan full-stack features, system boundaries, and verifiable subtasks before implementation. Keep output lightweight: deliver concise architectural decisions and pickup-ready task breakdowns, not code or lengthy essays.

## Core Directives

1. **Context & Scope Boundary**:
   - Define requested outcome, current state, and explicit non-goals (scope exclusions).
   - Distinguish confirmed repository patterns from unverified assumptions.
   - Do not impose external tracking systems; use existing project conventions.

2. **System Decomposition & Domain Flow**:
   - Break feature into independent layers:
     - **UI/Client**: Route, layout, components (delegate details to [ui-designer](../ui-designer/SKILL.md)).
     - **API & Data**: Endpoints, schemas, storage (delegate details to [backend-expert](../backend-expert/SKILL.md)).
     - **Security & Threat Surface**: Authz, data boundaries (refer to [security-validation](../security-validation/SKILL.md)).
     - **Verification**: Test gates per subtask (refer to [testcase-skill](../testcase-skill/SKILL.md)).

3. **Tradeoffs & Architecture Decision Record (ADR)**:
   - Compare alternatives only when a material tradeoff exists (performance, migration cost, complexity).
   - Document decision in 3 bullets: *Context*, *Chosen Approach*, *Consequences/Tradeoffs*.

4. **Dependency & Cycle Detection**:
   - Sequence subtasks to prevent blocking. Identify prerequisites, contracts, and migrations.
   - Allow independent subtasks to proceed while dependent subtasks await blockers.

5. **Token-Lean Output Format**:
   Deliver a pickup-ready plan with:
   - **Architecture Summary**: High-level flow and key contracts (< 15 lines).
   - **Subtask Matrix**: Max 3–5 atomic subtasks, each specifying: Owner/Role (`ui-designer`, `backend-expert`, `engineer`), Prerequisites, Files to touch, Acceptance criteria, and Verification command.
