# Work <NNN> Architecture & Design Decisions

Record critical technical decisions, tradeoffs, and contracts made during this work.

## Decision Log

- **<Date / ID> — <Decision Title>**:
  - **Context**: <Why the decision was needed>
  - **Decision**: <Chosen approach>
  - **Consequences**: <Tradeoffs, compatibility, migrations>

- **2026-10-11 — D05: Configuration Architecture & Validation**:
  - **Context**: Need lightweight, reproducible runtime profiles without bloated dependencies or external config servers.
  - **Decision**: Define single top-level `config.yaml` using pure Python dataclasses and PyYAML. Support profile inheritance (`minimal`, `standard`, `full`, `benchmark`) via deep dictionary merging. Expose inspection through `ai-skills config show`.
  - **Consequences**: Zero framework lock-in, deterministic schemas, instant validation and profile switching.
