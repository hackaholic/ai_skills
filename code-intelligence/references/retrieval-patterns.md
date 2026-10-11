# Code Retrieval Patterns Reference

Query recipes and token-budgeting guidelines for AI agents using `codebase-index`.

## 1. Symbol-First Navigation vs Full-File Dumps

| Objective | Traditional Token-Heavy Method | Index-First Token-Lean Method |
| :--- | :--- | :--- |
| **Locate a class or function** | `view_file` on entire 1,000-line files | `codebase-index symbol <Name>` -> view only lines `L120-L160` |
| **Find who calls a function** | `grep_search` producing 80 raw lines | `codebase-index refs <Name> --compact` (exact caller list) |
| **Check impact of changing code** | Manually inspecting 15 files | `codebase-index impact <Name> --compact` (blast radius graph) |
| **Review pre-commit diff** | Guessing affected downstream code | `codebase-index diff-impact` |
| **Explore concept or flow** | Paging through entire directories | `codebase-index search "<query>" --compact --token-budget 1200` |

---

## 2. CLI Recipes for Common Scenarios

### A. Finding Where a Symbol Is Defined
```bash
codebase-index symbol UserService.createUser
```
Returns: file path, line span, and function signature.

### B. Finding Call Sites & References (Before Refactoring)
```bash
codebase-index refs processPayment --compact --exclude-tests
```
Returns: exact `path:line` caller locations.

### C. Measuring Blast Radius of a Modification
```bash
# Check what depends on a file or symbol
codebase-index impact src/auth/token.py --depth 2 --compact

# Check what the current uncommitted Git diff impacts
codebase-index diff-impact
```

### D. Token-Bounded Concept Search
```bash
codebase-index search "jwt validation logic" --compact --token-budget 1000 --limit 5
```
Returns: ranked snippets fitting strictly within the token budget.

---

## 3. Fallback Protocol (When Indexing is Unavailable)

If `codebase-index` is missing, damaged, or unsupported for a language:
1. State: `"Notice: codebase-index unavailable; using targeted grep fallback."`
2. Use `grep_search` with specific identifiers (`MatchPerLine: true`).
3. View targeted line ranges via `view_file` with `StartLine` and `EndLine`.
4. Never block task progress due to tool absence.
