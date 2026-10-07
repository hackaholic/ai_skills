---
name: testcase-skill
description: Plan and execute concise, traceable test cases covering happy path, boundaries, error handling, and security with minimal token overhead.
---

# Test Engineering & Verification

Design and execute traceable, deterministic test cases. Focus on real behavioral verification rather than tautological or brittle mock tests. Keep output compact and structured.

## Core Directives

1. **Test Pyramid & Isolation**:
   - Choose the lowest test level that reliably validates the behavior (Unit > Integration > E2E).
   - Test against real integration boundaries (e.g. real test DB container or transactional rollback) for query safety and authorization. Do not mock away the security or database layer.
   - Use deterministic, isolated fixtures. Never depend on live production data or shared global state.

2. **Core Coverage Categories**:
   Every feature must cover:
   - **Happy Path**: Standard valid input and expected state change.
   - **Boundary / Edge**: Empty inputs, maximum payload limits, pagination boundaries, 0/1/N items.
   - **Failure Modes**: Upstream timeouts, network failure, duplicate keys, invalid schema.
   - **Security / Authorization**: Wrong tenant, unauthenticated caller, tampered IDs.
   - **Regression**: For bug fixes, establish a failing test first, then verify pass after fix.

3. **Observable Assertions**:
   - Assert observable state changes, exact status codes, and response schemas.
   - Verify absence of unintended side effects on denial or failure.

4. **Token-Lean Output Format**:
   Deliver a compact test matrix:
   | ID | Scenario | Category | Input / Trigger | Expected Outcome | Level | Status |
   | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
   | TC-01 | ... | Happy | ... | ... | Unit | Pass |
   | TC-02 | ... | Boundary | ... | ... | Integration | Pass |
   | TC-03 | ... | Security | ... | ... | Integration | Pass |
