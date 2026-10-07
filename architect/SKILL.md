---
name: architect
description: Mandatory planning step for non-trivial features. Selects system design patterns, justifies them, defines modular directory blueprints, and decomposes subtasks before coding.
---

# Architect

Plan full-stack features, select and justify system design patterns, and define modular directory blueprints before implementation. Keep output lightweight: deliver concise architectural decisions and pickup-ready task breakdowns, not code or lengthy essays.

## Core Directives

1. **System Design Selection & Justification (MANDATORY)**:
   - Evaluate project scale and select the appropriate architectural pattern:
     - **Modular Monolith**: Default for most apps (domain-driven modular folders).
     - **Clean / Hexagonal Architecture**: For complex domain logic needing decoupled infrastructure/storage.
     - **Layered MVC / Three-Tier**: For standard CRUD and REST applications.
     - **Event-Driven**: For asynchronous workflows, high concurrency, or decoupled pipelines.
   - **Explain WHY to the User** in 3 crisp bullets:
     - *Fit*: Why this pattern best solves the current problem.
     - *Tradeoffs*: What operational or structural complexity it introduces.
     - *Maintainability*: How it enables code reuse and future evolution.

2. **Modular Blueprint & Anti-Monolith Defense**:
   - Explicitly define the target folder structure upfront so implementation never collapses into a monolithic single file.
   - Enforce separation of concerns:
     - `config/`: Type-safe configuration and environment variable loading.
     - `models/` or `entities/`: Pure data models, schemas, and types.
     - `repositories/` or `data/`: Database queries and data access logic.
     - `services/`: Business logic, domain rules, and external integrations.
     - `routes/` or `controllers/`: HTTP/API request parsing, routing, and response serialization.
     - `utils/` or `common/`: Reusable helpers, templates, base classes, and middleware.

3. **System Decomposition & Domain Flow**:
   - Break feature into independent layers:
     - **UI/Client**: Route, layout, components (delegate details to [ui-designer](../ui-designer/SKILL.md)).
     - **API & Data**: Endpoints, schemas, storage (delegate details to [backend-expert](../backend-expert/SKILL.md)).
     - **Security & Threat Surface**: Authz, data boundaries (refer to [security-validation](../security-validation/SKILL.md)).
     - **Verification**: Test gates per subtask (refer to [testcase-skill](../testcase-skill/SKILL.md)).

4. **Tradeoffs & Architecture Decision Record (ADR)**:
   - Document decisions in 3 bullets: *Context*, *Chosen Approach*, *Consequences/Tradeoffs*.

5. **Token-Lean Output Format**:
   Deliver a pickup-ready plan with:
   - **System Design & Justification**: Pattern chosen and 3-bullet rationale.
   - **Modular Blueprint**: Tree of folders/files to create/edit.
   - **Subtask Matrix**: Max 3–5 atomic subtasks, each specifying: Owner/Role (`ui-designer`, `backend-expert`, `engineer`), Prerequisites, Files to touch, Acceptance criteria, and Verification command.
