"""Tests for MemoTrail core components."""

import tempfile
from pathlib import Path

from memotrail.core.chunker import Chunker
from memotrail.storage.sqlite_store import SQLiteStore
from memotrail.utils.tokens import count_tokens, truncate_to_tokens


class TestTokenUtils:
    def test_count_tokens_empty(self):
        assert count_tokens("") == 0

    def test_count_tokens_simple(self):
        tokens = count_tokens("Hello world")
        assert tokens > 0
        assert tokens < 10

    def test_truncate_preserves_short(self):
        text = "Short text"
        assert truncate_to_tokens(text, 100) == text

    def test_truncate_cuts_long(self):
        text = "word " * 1000
        result = truncate_to_tokens(text, 10)
        assert count_tokens(result) <= 10


class TestChunker:
    def test_empty_messages(self):
        chunker = Chunker()
        chunks = chunker.chunk_messages([], "test_session")
        assert chunks == []

    def test_single_message(self):
        chunker = Chunker()
        messages = [{"role": "user", "content": "Hello", "timestamp": "2025-01-01T00:00:00Z"}]
        chunks = chunker.chunk_messages(messages, "test_session")
        assert len(chunks) >= 1
        assert "Hello" in chunks[0].text

    def test_multiple_messages(self):
        chunker = Chunker(max_tokens=50)
        messages = [
            {"role": "user", "content": f"Message {i}", "timestamp": f"2025-01-01T00:0{i}:00Z"}
            for i in range(10)
        ]
        chunks = chunker.chunk_messages(messages, "test_session")
        assert len(chunks) >= 1

    def test_metadata_includes_session(self):
        chunker = Chunker()
        messages = [{"role": "user", "content": "Test", "timestamp": "2025-01-01T00:00:00Z"}]
        chunks = chunker.chunk_messages(messages, "sess_123", project="myproject")
        assert chunks[0].metadata["session_id"] == "sess_123"
        assert chunks[0].metadata["project"] == "myproject"

    def test_turn_strategy_groups_pairs(self):
        chunker = Chunker(strategy="turn")
        messages = [
            {"role": "user", "content": "What is Python?", "timestamp": "2025-01-01T00:00:00Z"},
            {"role": "assistant", "content": "Python is a programming language.", "timestamp": "2025-01-01T00:00:01Z"},
            {"role": "user", "content": "What about Go?", "timestamp": "2025-01-01T00:00:02Z"},
            {"role": "assistant", "content": "Go is also a programming language.", "timestamp": "2025-01-01T00:00:03Z"},
        ]
        chunks = chunker.chunk_messages(messages, "test_session")
        assert len(chunks) == 2
        assert "Python" in chunks[0].text
        assert "Go" in chunks[1].text

    def test_turn_strategy_empty(self):
        chunker = Chunker(strategy="turn")
        assert chunker.chunk_messages([], "test") == []

    def test_recursive_strategy(self):
        chunker = Chunker(strategy="recursive", max_tokens=50)
        messages = [
            {"role": "user", "content": "Tell me about databases", "timestamp": "t1"},
            {"role": "assistant", "content": "There are many databases. " * 20, "timestamp": "t2"},
        ]
        chunks = chunker.chunk_messages(messages, "test_session")
        assert len(chunks) >= 2  # Should split the long content

    def test_recursive_strategy_short(self):
        chunker = Chunker(strategy="recursive")
        messages = [
            {"role": "user", "content": "Hi", "timestamp": "t1"},
            {"role": "assistant", "content": "Hello!", "timestamp": "t2"},
        ]
        chunks = chunker.chunk_messages(messages, "test_session")
        assert len(chunks) == 1  # Short content should be single chunk

    def test_auto_strategy_short_session_uses_turn(self):
        """Auto should pick 'turn' for short sessions (≤20 messages)."""
        chunker = Chunker(strategy="auto")
        messages = [
            {"role": "user", "content": "What is Redis?", "timestamp": "t1"},
            {"role": "assistant", "content": "Redis is an in-memory store.", "timestamp": "t2"},
            {"role": "user", "content": "Should we use it?", "timestamp": "t3"},
            {"role": "assistant", "content": "Yes, for caching.", "timestamp": "t4"},
        ]
        assert chunker._pick_strategy(messages) == "turn"

    def test_auto_strategy_medium_session_uses_token(self):
        """Auto should pick 'token' for medium sessions (>20 short messages)."""
        chunker = Chunker(strategy="auto")
        messages = [
            {"role": "user" if i % 2 == 0 else "assistant", "content": f"Message {i}"}
            for i in range(30)
        ]
        assert chunker._pick_strategy(messages) == "token"

    def test_auto_strategy_long_messages_uses_recursive(self):
        """Auto should pick 'recursive' for sessions with long messages (avg ≥300 tokens)."""
        chunker = Chunker(strategy="auto")
        long_content = "word " * 400  # ~400 tokens per message
        messages = [
            {"role": "user" if i % 2 == 0 else "assistant", "content": long_content}
            for i in range(30)
        ]
        assert chunker._pick_strategy(messages) == "recursive"

    def test_auto_is_default(self):
        """Chunker should default to auto strategy."""
        chunker = Chunker()
        assert chunker.strategy == "auto"


class TestSQLiteStore:
    def test_create_and_get_session(self):
        with tempfile.NamedTemporaryFile(suffix=".db") as tmp:
            store = SQLiteStore(db_path=Path(tmp.name))
            store.connect()

            session = store.create_session(project="test-project")
            assert session.id.startswith("sess_")
            assert session.project == "test-project"

            retrieved = store.get_session(session.id)
            assert retrieved is not None
            assert retrieved.project == "test-project"

            store.close()

    def test_add_and_get_messages(self):
        with tempfile.NamedTemporaryFile(suffix=".db") as tmp:
            store = SQLiteStore(db_path=Path(tmp.name))
            store.connect()

            session = store.create_session()
            store.add_message(session.id, "user", "Hello")
            store.add_message(session.id, "assistant", "Hi there")

            messages = store.get_session_messages(session.id)
            assert len(messages) == 2
            assert messages[0].role == "user"
            assert messages[1].role == "assistant"

            store.close()

    def test_decisions(self):
        with tempfile.NamedTemporaryFile(suffix=".db") as tmp:
            store = SQLiteStore(db_path=Path(tmp.name))
            store.connect()

            session = store.create_session(project="myapp")
            store.add_decision(session.id, "Use Redis for caching", category="architecture")

            decisions = store.get_decisions()
            assert len(decisions) == 1
            assert "Redis" in decisions[0].decision_text

            store.close()

    def test_stats(self):
        with tempfile.NamedTemporaryFile(suffix=".db") as tmp:
            store = SQLiteStore(db_path=Path(tmp.name))
            store.connect()

            session = store.create_session()
            store.add_message(session.id, "user", "Test")

            stats = store.get_stats()
            assert stats["total_sessions"] == 1
            assert stats["total_messages"] == 1

            store.close()
