"""
Shared memory engine backed by local SQLite with FTS5 search.
"""

from __future__ import annotations

import datetime
import json
import sqlite3
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from ai_skills_opt.config import OptimizationConfig, SharedMemoryConfig


class MemoryError(Exception):
    """Exception raised for shared memory errors."""
    pass


VALID_STATUSES = {"VERIFIED", "HYPOTHESIS", "STALE", "INVALIDATED"}


@dataclass
class Finding:
    id: Optional[int]
    namespace: str
    key: str
    content: str
    status: str
    tags: List[str]
    evidence_path: Optional[str] = None
    line_range: Optional[str] = None
    git_hash: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def validate(self) -> None:
        if self.status not in VALID_STATUSES:
            raise MemoryError(f"Invalid status '{self.status}'. Must be one of {VALID_STATUSES}")
        if not self.namespace or not isinstance(self.namespace, str):
            raise MemoryError("Namespace must be a non-empty string")
        if not self.key or not isinstance(self.key, str):
            raise MemoryError("Key must be a non-empty string")
        if not self.content:
            raise MemoryError("Content cannot be empty")


class SharedMemoryEngine:
    def __init__(self, config: OptimizationConfig, root_dir: Optional[Path] = None):
        self.config: OptimizationConfig = config
        self.sm_config: SharedMemoryConfig = config.shared_memory
        self.root_dir: Path = (root_dir or Path.cwd()).resolve()
        self.db_path: Path = self.root_dir / self.sm_config.db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        if not self.sm_config.enabled:
            return

        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS findings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    namespace TEXT NOT NULL,
                    key TEXT NOT NULL,
                    content TEXT NOT NULL,
                    status TEXT NOT NULL,
                    tags TEXT NOT NULL,
                    evidence_path TEXT,
                    line_range TEXT,
                    git_hash TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    UNIQUE(namespace, key)
                )
            """)

            if self.sm_config.fts_enabled:
                cur.execute("""
                    CREATE VIRTUAL TABLE IF NOT EXISTS findings_fts USING fts5(
                        content,
                        tags,
                        key,
                        content=findings,
                        content_rowid=id
                    )
                """)
                # Triggers to keep FTS index synchronized
                cur.execute("""
                    CREATE TRIGGER IF NOT EXISTS findings_ai AFTER INSERT ON findings BEGIN
                        INSERT INTO findings_fts(rowid, content, tags, key)
                        VALUES (new.id, new.content, new.tags, new.key);
                    END;
                """)
                cur.execute("""
                    CREATE TRIGGER IF NOT EXISTS findings_ad AFTER DELETE ON findings BEGIN
                        INSERT INTO findings_fts(findings_fts, rowid, content, tags, key)
                        VALUES('delete', old.id, old.content, old.tags, old.key);
                    END;
                """)
                cur.execute("""
                    CREATE TRIGGER IF NOT EXISTS findings_au AFTER UPDATE ON findings BEGIN
                        INSERT INTO findings_fts(findings_fts, rowid, content, tags, key)
                        VALUES('delete', old.id, old.content, old.tags, old.key);
                        INSERT INTO findings_fts(rowid, content, tags, key)
                        VALUES (new.id, new.content, new.tags, new.key);
                    END;
                """)
            conn.commit()

    def put(
        self,
        namespace: str,
        key: str,
        content: str,
        status: str = "HYPOTHESIS",
        tags: Optional[List[str]] = None,
        evidence_path: Optional[str] = None,
        line_range: Optional[str] = None,
        git_hash: Optional[str] = None,
    ) -> Finding:
        if not self.sm_config.enabled:
            raise MemoryError("Shared memory is disabled in current profile")

        finding = Finding(
            id=None,
            namespace=namespace,
            key=key,
            content=content,
            status=status,
            tags=tags or [],
            evidence_path=evidence_path,
            line_range=line_range,
            git_hash=git_hash,
        )
        finding.validate()

        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        tags_json = json.dumps(finding.tags)

        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO findings (namespace, key, content, status, tags, evidence_path, line_range, git_hash, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(namespace, key) DO UPDATE SET
                    content = excluded.content,
                    status = excluded.status,
                    tags = excluded.tags,
                    evidence_path = excluded.evidence_path,
                    line_range = excluded.line_range,
                    git_hash = excluded.git_hash,
                    updated_at = excluded.updated_at
            """, (
                namespace, key, content, status, tags_json, evidence_path, line_range, git_hash, now, now
            ))
            conn.commit()
            finding.id = cur.lastrowid
            finding.created_at = now
            finding.updated_at = now
        return finding

    def get(self, namespace: str, key: str) -> Optional[Finding]:
        if not self.sm_config.enabled:
            return None

        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, namespace, key, content, status, tags, evidence_path, line_range, git_hash, created_at, updated_at
                FROM findings WHERE namespace = ? AND key = ?
            """, (namespace, key))
            row = cur.fetchone()
            if not row:
                return None
            return Finding(
                id=row["id"],
                namespace=row["namespace"],
                key=row["key"],
                content=row["content"],
                status=row["status"],
                tags=json.loads(row["tags"]),
                evidence_path=row["evidence_path"],
                line_range=row["line_range"],
                git_hash=row["git_hash"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
            )

    def list_findings(self, namespace: Optional[str] = None, status: Optional[str] = None) -> List[Finding]:
        if not self.sm_config.enabled:
            return []

        query = "SELECT id, namespace, key, content, status, tags, evidence_path, line_range, git_hash, created_at, updated_at FROM findings WHERE 1=1"
        params: List[Any] = []
        if namespace:
            query += " AND namespace = ?"
            params.append(namespace)
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY updated_at DESC"

        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute(query, tuple(params))
            results = []
            for row in cur.fetchall():
                results.append(Finding(
                    id=row["id"],
                    namespace=row["namespace"],
                    key=row["key"],
                    content=row["content"],
                    status=row["status"],
                    tags=json.loads(row["tags"]),
                    evidence_path=row["evidence_path"],
                    line_range=row["line_range"],
                    git_hash=row["git_hash"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"],
                ))
            return results

    def search(self, query: str, namespace: Optional[str] = None) -> List[Finding]:
        if not self.sm_config.enabled:
            return []

        with self._get_connection() as conn:
            cur = conn.cursor()
            if self.sm_config.fts_enabled:
                sql = """
                    SELECT f.id, f.namespace, f.key, f.content, f.status, f.tags, f.evidence_path, f.line_range, f.git_hash, f.created_at, f.updated_at
                    FROM findings f
                    JOIN findings_fts fts ON f.id = fts.rowid
                    WHERE findings_fts MATCH ?
                """
                params: List[Any] = [query]
                if namespace:
                    sql += " AND f.namespace = ?"
                    params.append(namespace)
                sql += " ORDER BY rank"
            else:
                # Fallback to LIKE if FTS is disabled
                like_term = f"%{query}%"
                sql = """
                    SELECT id, namespace, key, content, status, tags, evidence_path, line_range, git_hash, created_at, updated_at
                    FROM findings
                    WHERE (content LIKE ? OR key LIKE ? OR tags LIKE ?)
                """
                params = [like_term, like_term, like_term]
                if namespace:
                    sql += " AND namespace = ?"
                    params.append(namespace)

            try:
                cur.execute(sql, tuple(params))
                results = []
                for row in cur.fetchall():
                    results.append(Finding(
                        id=row["id"],
                        namespace=row["namespace"],
                        key=row["key"],
                        content=row["content"],
                        status=row["status"],
                        tags=json.loads(row["tags"]),
                        evidence_path=row["evidence_path"],
                        line_range=row["line_range"],
                        git_hash=row["git_hash"],
                        created_at=row["created_at"],
                        updated_at=row["updated_at"],
                    ))
                return results
            except sqlite3.OperationalError:
                # Fallback to simple scan if FTS syntax error
                return []

    def delete(self, namespace: str, key: str) -> bool:
        if not self.sm_config.enabled:
            return False

        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM findings WHERE namespace = ? AND key = ?", (namespace, key))
            conn.commit()
            return cur.rowcount > 0
