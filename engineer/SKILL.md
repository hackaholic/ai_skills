---
name: engineer
description: Implement scoped features with modular architecture, zero hardcoding, reusable patterns, and surgical diffs.
---

# Software Engineer

Execute implementation tasks adhering to modular design standards. Prohibit monolithic files, hardcoded parameters, and copy-pasted code. Keep token usage low by applying surgical edits rather than regenerating entire files.

## Core Directives

1. **Strict Anti-Monolith Directive (MANDATORY)**:
   - **Never code everything into a single file.** Prohibit mixing routes, business logic, and database queries in one place.
   - Follow the modular blueprint from [architect](../architect/SKILL.md):
     - Put route definitions and request parsing in `routes/` or `controllers/`.
     - Put business rules in `services/`.
     - Put database operations and queries in `repositories/`.
     - Put data types and validation schemas in `models/` or `schemas/`.
     - Put shared helpers in `utils/` or `common/`.
   - Keep individual files cohesive and bounded (< 250 lines typical).

2. **Zero-Hardcoding & 12-Factor Configuration**:
   - **Zero hardcoding**: Never place raw URLs, ports, magic strings, thresholds, or credentials in application code.
   - **Config Strategy**:
     - Centralize configuration in a dedicated `config/` module.
     - **Default format**: Use YAML (`config.yaml` / `config.example.yaml`) for hierarchical configs, or suggest and confirm with the user if their stack favors `.env` (dotenv), TOML, or JSON.
     - Support environment variable overrides for every configuration key (12-factor standard).
     - Enforce type-safe startup validation (e.g. Zod, Pydantic, Viper). Fail fast with clear error messages if required variables are missing.

3. **Reusability, Templating & DRY**:
   - Never copy-paste boilerplate across modules.
   - Extract common operations into reusable utilities or base abstractions (e.g., standardized HTTP client with retries, database connection pool wrapper, uniform error responder).
   - Design functions with clear inputs and outputs so they can be imported and composed cleanly.

4. **Surgical, Targeted Modifications & Index Refresh**:
   - Follow the index-first cycle via [code-intelligence](../code-intelligence/SKILL.md): locate target symbol/callers (`symbol`, `refs`) -> view bounded lines -> edit -> verify.
   - Make the smallest coherent change that satisfies the acceptance criteria.
   - Never regenerate or rewrite entire files when updating functions or components; use targeted replacements/diffs.
   - Preserve existing code comments, docstrings, formatting, and unrelated logic.
   - After completing edits, refresh affected index entries via `codebase-index update`.

5. **Token-Lean Output Format**:
   Deliver:
   - **Summary of Changes**: 1–3 bullet points of what was changed and why.
   - **Modular Files Modified/Created**: Exact file paths and roles.
   - **Verification Results**: Command executed and output summary (e.g. `pnpm test - Passed (12/12)`).
