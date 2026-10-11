# Work <NNN> Architecture & Design Decisions

Record critical technical decisions, tradeoffs, and contracts made during this work.

## Decision Log

- **<Date / ID> — <Decision Title>**:
  - **Context**: <Why the decision was needed>
  - **Decision**: <Chosen approach>
  - **Consequences**: <Tradeoffs, compatibility, migrations>

- **2026-10-11 — D10: Skill Evaluation Bridge Architecture**:
  - **Context**: Need to connect the benchmark harness with Hugging Face `upskill` and agent adapters without requiring live network calls or unmetered token spending.
  - **Decision**: Implement `SkillEvaluator` in `ai_skills_opt.evaluation`. Wrap evaluation tasks into structured `EvaluationReport` tracking pass rates, total token footprint, and execution wall-time. Bridge to `upskill` CLI where available and provide deterministic offline keyword scoring.
  - **Consequences**: Standardized evaluation metrics across all supported agent adapters.
