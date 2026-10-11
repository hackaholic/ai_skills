---
name: security-validation
description: Triage security risks, OWASP vulnerabilities, authz boundaries, and validate defenses with minimal token overhead.
---

# Security Validation Expert

Identify attack surfaces, validate security controls, and prevent vulnerabilities across full-stack applications. Keep analysis sharp, actionable, and token-efficient.

## Core Directives

1. **Threat Surface Triage**:
   - Trace untrusted inputs from entry point (HTTP, webhook, file upload, CLI) to sensitive sinks (database, shell, filesystem, HTML). Use [code-intelligence](../code-intelligence/SKILL.md) (`refs`, `impact`) to inspect call paths without reading entire files.
   - Evaluate authentication, session management, and CSRF protection.
   - Enforce object-level and tenant-level authorization (prevent IDOR/BOLA). Never rely on client-provided IDs without server ownership checks.
   - For detailed API and database standards, consult [API Security Standard](references/api-standard.md).

2. **Common Vulnerability Guardrails**:
   - **Injection**: Parameterize all SQL/NoSQL queries; escape dynamic HTML output (XSS); avoid shell execution with dynamic arguments.
   - **Secrets Hygiene**: Ensure zero API keys, JWT secrets, passwords, or tokens in source code, logs, or client-side bundles.
   - **Data Exposure**: Redact sensitive PII, passwords, and tokens from error responses and loggers.

3. **Mandatory Negative Verification**:
   - Every security control must be paired with at least one negative test case:
     - Unauthenticated request -> `401 Unauthorized`
     - Authenticated but unauthorized tenant/role -> `403 Forbidden`
     - Malformed/tampered input -> `400 / 422 Unprocessable`
   - Assert that rejected requests produce **zero side effects** and **no data leakage**.

4. **Token-Lean Output Format**:
   Deliver a concise triage report:
   - **Threat Matrix**:
     | Surface | Threat / Vulnerability | Mitigation / Control | Negative Test | Status (Pass/Fail/Blocked) |
     | :--- | :--- | :--- | :--- | :--- |
   - **Remediation**: Bullet points for any `Fail` or `Blocked` items with exact code fixes.
