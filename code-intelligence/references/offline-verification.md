# Offline Verification & Safety Guide

This guide details how to verify that `codebase-index` operates strictly locally and offline without external network requests or LLM API tokens.

## 1. Zero Network & Zero Token Guarantees

`codebase-index` uses a dual-engine architecture:
1. **Tree-sitter**: Parses ASTs locally to extract classes, functions, methods, and call sites.
2. **SQLite with FTS5**: Stores symbols, chunks, and full-text inverted indexes in a local file (`index.sqlite`).

### Native Offline Configuration
By default in `codebase-index`:
- `embeddings.backend`: Set to `"noop"`.
- `embeddings.enabled`: Set to `False`.
- `embeddings.allow_external`: Set to `False`.

No external embedding calls (OpenAI, Voyage, Cohere, etc.) are made. All search is pure local hybrid lexical + AST symbol matching.

## 2. Verification Commands

Run the deterministic helper script to audit configuration:
```bash
python3 scripts/codebase_index_helper.py check-offline
```

Expected output:
```
Checking offline guarantees...
  Embeddings backend : noop
  Embeddings enabled : False
  Allow external     : False
  Ignore files       : ['.gitignore', '.cursorignore', '.claudeignore', '.codeindexignore']
✓ PASS: Index operates completely offline with native Tree-sitter & SQLite.
```

### Network Isolation Audit
To verify zero outbound sockets are opened during indexing:
```bash
# Run doctor diagnostic
codebase-index doctor

# Or execute with network isolation / strace
strace -f -e trace=network codebase-index index 2>&1 | grep -E 'connect\(.*AF_INET'
```
No external IP connections should be established.

## 3. Secret & Privacy Exclusions

- Secrets, credentials, and private files listed in `.gitignore`, `.cursorignore`, `.claudeignore`, or `.codeindexignore` are strictly excluded from indexing.
- SQLite cache files are located in `.claude/cache/codebase-index/` and must never be committed to Git.
- Redaction is enabled by default (`redaction.enabled = True`) to sanitize tokens and API keys.
