# API design and security contract

Apply to new or changed API surfaces; preserve established public contracts or explicitly plan compatibility. Record applicability and tests in the task. This is a project-independent baseline, not a certification or replacement for repository policy.

## Contract and integrity

Specify method/path, versioning compatibility, request/response schemas, field types and bounds, allowed content types, errors, pagination, sorting, and documented limits. GET must not mutate state. Use consistent HTTP semantics and structured errors without internal details. Maintain OpenAPI or the project's equivalent and test contract changes. Define transactions, constraints, idempotency/replay behavior, and concurrency handling for writes with business consequences. Derive prices, roles, ownership, and state transitions on the server.

## Access and input boundaries

Authenticate protected routes; enforce operation, object/tenant, and property permissions on every request. Explicitly document public endpoints. Validate token signature and configured algorithm, issuer, audience, expiry and relevant claims; use established libraries. Test missing/invalid credentials, wrong role, and a second user's object IDs, including list/bulk routes. Filter writable fields to prevent mass assignment and return only allowed response fields.

Validate types, lengths, ranges, nesting, and allowed enums at entry. Require HTTPS outside authorized local development; use explicit CORS origins and methods. CORS is not authorization. For cookie-authenticated mutations assess CSRF protections and Secure/HttpOnly/SameSite cookie settings; do not assume SameSite alone covers the design.

## Database and injection

Bind query values using parameterized statements or safe ORM expressions. Never concatenate untrusted input into SQL, including raw ORM queries and stored procedures. Map dynamic sort columns/table identifiers to fixed server-side allowlists; value placeholders cannot secure identifiers. Escaping/blacklisting is not the primary SQL defense. Specify intended wildcard semantics for LIKE/search. Use least-privilege application DB accounts and separate migration privileges. Test query behavior against the actual database with isolated data, including quotes and SQL-like strings; assert no extra rows, authorization bypass, or unintended writes.

## Resource and integration controls

Bound request/upload size, page size, expensive searches, execution time, and retries. Apply rate/concurrency controls appropriate to sensitive endpoints and test limits without stressing live services. For URL-fetching features validate destination/scheme, redirects and resolved addresses; block unauthorized private/metadata destinations. For uploads validate size/type/content and safe storage paths; do not execute uploads. Avoid shell interpolation, unsafe deserialization, and untrusted templates. For webhooks validate signatures and replay rules. Apply these controls only where that surface exists.

## Operations and verification

Keep credentials in the project's secrets mechanism. Restrict admin/debug endpoints and database network exposure. Logs/errors must omit tokens, credentials, private payloads and stack traces; preserve useful redacted audit events. Check dependency/config changes and environment parity. Record applicable existing scanner results alongside manual code tracing and security regression tests. Failed or unavailable required checks prevent a passing validation.

References, consulted 2026-10-07; consult current framework guidance for implementation details:
- [OWASP SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [OWASP REST Security](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)
- [OWASP Database Security](https://cheatsheetseries.owasp.org/cheatsheets/Database_Security_Cheat_Sheet.html)
