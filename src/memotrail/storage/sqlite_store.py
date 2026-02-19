"""SQLite storage for session metadata, messages, and decisions."""

import sqlite3
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

from memotrail.utils import config, get_logger

logger = get_logger("memotrail.storage.sqlite")

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    project TEXT,
    started_at TEXT NOT NULL,
    ended_at TEXT,
    summary TEXT,
    message_count INTEGER DEFAULT 0,
    tags TEXT DEFAULT '[]',
    source TEXT DEFAULT 'claude_code'
);

CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES sessions(id),
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    token_count INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS decisions (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES sessions(id),
    decision_text TEXT NOT NULL,
    context TEXT,
    category TEXT DEFAULT 'general',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS memories (
    id TEXT PRIMARY KEY,
    content TEXT NOT NULL,
    tags TEXT DEFAULT '[]',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS indexed_files (
    file_path TEXT PRIMARY KEY,
    file_size INTEGER NOT NULL,
    file_mtime REAL NOT NULL,
    session_id TEXT NOT NULL REFERENCES sessions(id),
    indexed_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_messages_session ON messages(session_id);
CREATE INDEX IF NOT EXISTS idx_decisions_session ON decisions(session_id);
CREATE INDEX IF NOT EXISTS idx_sessions_project ON sessions(project);
CREATE INDEX IF NOT EXISTS idx_sessions_started ON sessions(started_at);
"""


@dataclass
class Session:
    id: str
    project: Optional[str]
    started_at: str
    ended_at: Optional[str] = None
    summary: Optional[str] = None
    message_count: int = 0
    tags: list[str] = field(default_factory=list)
    source: str = "claude_code"


@dataclass
class Message:
    id: str
    session_id: str
    role: str
    content: str
    timestamp: str
    token_count: int = 0


@dataclass
class Decision:
    id: str
    session_id: str
    decision_text: str
    context: Optional[str] = None
    category: str = "general"
    created_at: str = ""


class SQLiteStore:
    """SQLite-based metadata storage."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or config.sqlite_path
        self._conn: Optional[sqlite3.Connection] = None

    def connect(self) -> None:
        """Initialize database connection and schema."""
        config.ensure_dirs()
        self._conn = sqlite3.connect(str(self.db_path))
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(SCHEMA_SQL)
        logger.info(f"SQLite connected: {self.db_path}")

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None

    @property
    def conn(self) -> sqlite3.Connection:
        if self._conn is None:
            self.connect()
        return self._conn

    # ── Sessions ──────────────────────────────────────────────

    def create_session(
        self,
        project: Optional[str] = None,
        source: str = "claude_code",
        tags: Optional[list[str]] = None,
    ) -> Session:
        session = Session(
            id=f"sess_{uuid.uuid4().hex[:12]}",
            project=project,
            started_at=datetime.now(timezone.utc).isoformat(),
            source=source,
            tags=tags or [],
        )
        self.conn.execute(
            "INSERT INTO sessions (id, project, started_at, source, tags) VALUES (?, ?, ?, ?, ?)",
            (session.id, session.project, session.started_at, session.source, json.dumps(session.tags)),
        )
        self.conn.commit()
        return session

    def update_session(
        self,
        session_id: str,
        ended_at: Optional[str] = None,
        summary: Optional[str] = None,
        message_count: Optional[int] = None,
    ) -> None:
        updates = []
        params = []
        if ended_at:
            updates.append("ended_at = ?")
            params.append(ended_at)
        if summary:
            updates.append("summary = ?")
            params.append(summary)
        if message_count is not None:
            updates.append("message_count = ?")
            params.append(message_count)
        if updates:
            params.append(session_id)
            self.conn.execute(
                f"UPDATE sessions SET {', '.join(updates)} WHERE id = ?", params
            )
            self.conn.commit()

    def get_session(self, session_id: str) -> Optional[Session]:
        row = self.conn.execute(
            "SELECT * FROM sessions WHERE id = ?", (session_id,)
        ).fetchone()
        if not row:
            return None
        return Session(
            id=row["id"],
            project=row["project"],
            started_at=row["started_at"],
            ended_at=row["ended_at"],
            summary=row["summary"],
            message_count=row["message_count"],
            tags=json.loads(row["tags"]),
            source=row["source"],
        )

    def get_recent_sessions(self, limit: int = 10) -> list[Session]:
        rows = self.conn.execute(
            "SELECT * FROM sessions ORDER BY started_at DESC LIMIT ?", (limit,)
        ).fetchall()
        return [
            Session(
                id=r["id"], project=r["project"], started_at=r["started_at"],
                ended_at=r["ended_at"], summary=r["summary"],
                message_count=r["message_count"], tags=json.loads(r["tags"]),
                source=r["source"],
            )
            for r in rows
        ]

    # ── Messages ──────────────────────────────────────────────

    def add_message(
        self, session_id: str, role: str, content: str, token_count: int = 0
    ) -> Message:
        msg = Message(
            id=f"msg_{uuid.uuid4().hex[:12]}",
            session_id=session_id,
            role=role,
            content=content,
            timestamp=datetime.now(timezone.utc).isoformat(),
            token_count=token_count,
        )
        self.conn.execute(
            "INSERT INTO messages (id, session_id, role, content, timestamp, token_count) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (msg.id, msg.session_id, msg.role, msg.content, msg.timestamp, msg.token_count),
        )
        self.conn.commit()
        return msg

    def get_session_messages(self, session_id: str) -> list[Message]:
        rows = self.conn.execute(
            "SELECT * FROM messages WHERE session_id = ? ORDER BY timestamp", (session_id,)
        ).fetchall()
        return [
            Message(
                id=r["id"], session_id=r["session_id"], role=r["role"],
                content=r["content"], timestamp=r["timestamp"],
                token_count=r["token_count"],
            )
            for r in rows
        ]

    # ── Decisions ─────────────────────────────────────────────

    def add_decision(
        self,
        session_id: str,
        decision_text: str,
        context: Optional[str] = None,
        category: str = "general",
    ) -> Decision:
        dec = Decision(
            id=f"dec_{uuid.uuid4().hex[:12]}",
            session_id=session_id,
            decision_text=decision_text,
            context=context,
            category=category,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self.conn.execute(
            "INSERT INTO decisions (id, session_id, decision_text, context, category, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (dec.id, dec.session_id, dec.decision_text, dec.context, dec.category, dec.created_at),
        )
        self.conn.commit()
        return dec

    def get_decisions(
        self, project: Optional[str] = None, limit: int = 20
    ) -> list[Decision]:
        if project:
            rows = self.conn.execute(
                "SELECT d.* FROM decisions d JOIN sessions s ON d.session_id = s.id "
                "WHERE s.project = ? ORDER BY d.created_at DESC LIMIT ?",
                (project, limit),
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT * FROM decisions ORDER BY created_at DESC LIMIT ?", (limit,)
            ).fetchall()
        return [
            Decision(
                id=r["id"], session_id=r["session_id"],
                decision_text=r["decision_text"], context=r["context"],
                category=r["category"], created_at=r["created_at"],
            )
            for r in rows
        ]

    # ── Memories (manual notes) ───────────────────────────────

    def save_memory(self, content: str, tags: Optional[list[str]] = None) -> str:
        memory_id = f"mem_{uuid.uuid4().hex[:12]}"
        now = datetime.now(timezone.utc).isoformat()
        self.conn.execute(
            "INSERT INTO memories (id, content, tags, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (memory_id, content, json.dumps(tags or []), now, now),
        )
        self.conn.commit()
        return memory_id

    # ── File tracking ────────────────────────────────────────

    def is_file_indexed(self, file_path: str) -> bool:
        """Check if a file has already been indexed (same size and mtime)."""
        path = Path(file_path)
        if not path.exists():
            return False
        row = self.conn.execute(
            "SELECT file_size, file_mtime FROM indexed_files WHERE file_path = ?",
            (file_path,),
        ).fetchone()
        if not row:
            return False
        return row["file_size"] == path.stat().st_size and row["file_mtime"] == path.stat().st_mtime

    def mark_file_indexed(self, file_path: str, session_id: str) -> None:
        """Record that a file has been indexed."""
        path = Path(file_path)
        stat = path.stat()
        self.conn.execute(
            "INSERT OR REPLACE INTO indexed_files (file_path, file_size, file_mtime, session_id, indexed_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (file_path, stat.st_size, stat.st_mtime, session_id,
             datetime.now(timezone.utc).isoformat()),
        )
        self.conn.commit()

    # ── Stats ─────────────────────────────────────────────────

    def get_stats(self) -> dict:
        sessions = self.conn.execute("SELECT COUNT(*) as c FROM sessions").fetchone()["c"]
        messages = self.conn.execute("SELECT COUNT(*) as c FROM messages").fetchone()["c"]
        decisions = self.conn.execute("SELECT COUNT(*) as c FROM decisions").fetchone()["c"]
        return {
            "total_sessions": sessions,
            "total_messages": messages,
            "total_decisions": decisions,
        }
