# Token-Lean Full-Stack AI Skills

A high-density, low-token AI skills suite for full-stack software development. Designed to deliver expert-level architecture, UI/UX, backend, engineering, security, testing, and peer review without burning excessive tokens.

---

## Why Token-Lean? (Solving the `pstack` / `upskill` Problem)

Heavy agent frameworks and prompt stacks (like `pstack` and `upskill`) frequently blow through context windows because they:
1. **Dump monolithic system prompts** with verbose conversational preambles and meta-explanations.
2. **Eagerly load giant reference manuals** regardless of the specific task.
3. **Encourage multi-page ceremonial outputs** instead of actionable code diffs and decisions.

This suite solves that through **Progressive Disclosure & Zero-Fluff Directives**:
- **Tiny Discovery Footprint**: Frontmatter descriptions are kept under 25 words (~200 tokens total for the whole suite).
- **Dense Imperative Instructions**: Each `SKILL.md` is strictly under 400 words, focusing purely on decisions, constraints, and deliverables.
- **Reference Sharding**: Deep domain checklists (e.g., API security specs) live in standalone reference files loaded only when that domain is actively engaged.
- **Strict Output Budgets**: Standardized compact formats (ADRs, component trees, DDL schemas, diffs, test matrices) minimize generation tokens.

---

## Full-Stack Skill Roles

| Skill | Role | Key Deliverables & Responsibilities |
| :--- | :--- | :--- |
| **[`architect`](./architect/SKILL.md)** | System Architect | Scope boundaries, domain decomposition, ADRs, subtask dependencies. |
| **[`ui-designer`](./ui-designer/SKILL.md)** | UI/UX & Frontend | Design tokens, layout hierarchy, states (loading/empty/error), a11y, component tree. |
| **[`backend-expert`](./backend-expert/SKILL.md)** | Backend & Database | Schema DDL, indexing, transactions, API contracts, caching, background jobs. |
| **[`engineer`](./engineer/SKILL.md)** | Full-Stack Implementation | Surgical code diffs, adhering to contracts, local build & regression verification. |
| **[`testcase-skill`](./testcase-skill/SKILL.md)** | Test Engineer | Compact traceable test matrices (happy path, boundary, failure, security). |
| **[`security-validation`](./security-validation/SKILL.md)** | Security Expert | Threat modeling, OWASP triage, authz/IDOR checks, mandatory negative tests. |
| **[`peer`](./peer/SKILL.md)** | Peer Reviewer | Diff-first code review, bug/regression spot checks, classified findings (Blocker/Warning/Nit). |
| **[`skill-feedback`](./skill-feedback/SKILL.md)** | Skill Refinement | Evidence-based skill improvements, applied only with explicit user approval. |

---

## Recommended Full-Stack Lifecycle Flow

```mermaid
flowchart LR
    A[Task / Feature] --> B(architect)
    B --> C(ui-designer)
    B --> D(backend-expert)
    C --> E(engineer)
    D --> E
    E --> F(testcase-skill)
    E --> G(security-validation)
    F --> H(peer review)
    G --> H
    H --> I[Verified & Shipped]
```

1. **Architecture (`architect`)**: Define scope, boundaries, and 3–5 atomic subtasks.
2. **Specialized Design**:
   - For UI/frontend tasks: Invoke **`ui-designer`** for components, tokens, and states.
   - For backend/data tasks: Invoke **`backend-expert`** for schemas, endpoints, and concurrency.
3. **Implementation (`engineer`)**: Apply surgical, minimal diffs meeting the specs.
4. **Verification**:
   - Run **`testcase-skill`** to execute the targeted test matrix.
   - Run **`security-validation`** to verify negative security assertions.
5. **Review (`peer`)**: Perform diff-focused code review before merging.

---

## Installation & Sync

### For Google Antigravity
Copy or symlink skills into your project workspace or global agent directory:
```bash
# Workspace level (project-specific)
mkdir -p .agents/skills
cp -r * .agents/skills/

# Or global level
mkdir -p ~/.gemini/antigravity/skills
cp -r * ~/.gemini/antigravity/skills/
```

### For Codex
```bash
mkdir -p ~/.codex/skills
cp -r * ~/.codex/skills/
```
