# Work <NNN> Architecture & Design Decisions

Record critical technical decisions, tradeoffs, and contracts made during this work.

## Decision Log

- **<Date / ID> — <Decision Title>**:
  - **Context**: <Why the decision was needed>
  - **Decision**: <Chosen approach>
  - **Consequences**: <Tradeoffs, compatibility, migrations>

- **2026-10-11 — D12: Multi-Profile Comparative Reporting Engine**:
  - **Context**: Need automated comparative reporting of token spending, runtimes, and pass rates across profiles without manual log calculation.
  - **Decision**: Build `ai_skills_opt.benchmark.BenchmarkRunner` and CLI subcommand `ai-skills benchmark --profiles minimal,standard,full`. Output clean GitHub Flavored Markdown comparison tables and structured JSON logs.
  - **Consequences**: Direct observability into token savings and performance tradeoffs across different optimization levels.
