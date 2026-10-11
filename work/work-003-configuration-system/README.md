# Work 003 — WORK-02: Configuration System

**Objective:** Implement a lightweight, versioned YAML configuration system with strict schema validation and runtime profile resolution (`minimal`, `standard`, `full`, `benchmark`).

**Current state:** Completed.

**Architecture:**
- Single root configuration: `config.yaml` supporting declarative profiles.
- Pure Python validation module `ai_skills_opt.config` (using standard dataclasses and PyYAML) with zero heavy daemon dependencies.
- Command-line inspection interface: `python3 -m ai_skills_opt config show --profile <name>`.

**Done when:**
- `config.yaml` is authored with versioning and profile specifications.
- `ai_skills_opt.config` validates schemas, catches invalid types/ranges, and resolves profiles deterministically.
- Full unit test suite passes in `tests/test_config.py`.
