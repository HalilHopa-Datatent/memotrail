"""Tests for the Consolidator module."""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from memotrail.core.consolidator import (
    Consolidator,
    ConsolidationAction,
    ConsolidationResult,
)
from memotrail.storage.chroma_store import SearchResult


class TestDecideAction:
    """Test the core _decide_action logic without needing real embeddings."""

    def setup_method(self):
        self.consolidator = Consolidator.__new__(Consolidator)

    def test_low_similarity_returns_add(self):
        result = self.consolidator._decide_action(
            "Use PostgreSQL for storage", "mem_123", "Set up CI/CD pipeline", 0.3
        )
        assert result.action == ConsolidationAction.ADD
        assert result.similarity == 0.3

    def test_medium_similarity_returns_update(self):
        result = self.consolidator._decide_action(
            "Use PostgreSQL 16 with pgvector for storage",
            "mem_123",
            "Use PostgreSQL for storage",
            0.85,
        )
        assert result.action == ConsolidationAction.UPDATE
        assert result.existing_id == "mem_123"

    def test_high_similarity_short_text_returns_noop(self):
        result = self.consolidator._decide_action(
            "Use Redis for caching", "mem_123", "Use Redis for caching", 0.95
        )
        assert result.action == ConsolidationAction.NOOP
        assert result.existing_id == "mem_123"

    def test_high_similarity_longer_text_returns_update(self):
        existing = "Use Redis"
        new_text = "Use Redis for caching with a 5-minute TTL and connection pooling"
        result = self.consolidator._decide_action(new_text, "mem_123", existing, 0.93)
        assert result.action == ConsolidationAction.UPDATE

    def test_contradiction_returns_delete(self):
        result = self.consolidator._decide_action(
            "Switched from Redis to Memcached for caching",
            "mem_123",
            "Use Redis for caching",
            0.82,
        )
        assert result.action == ConsolidationAction.DELETE
        assert result.existing_id == "mem_123"

    def test_boundary_at_update_threshold(self):
        result = self.consolidator._decide_action(
            "Updated database config", "mem_123", "Database configuration", 0.78
        )
        assert result.action == ConsolidationAction.UPDATE

    def test_boundary_just_below_update_threshold(self):
        result = self.consolidator._decide_action(
            "New feature added", "mem_123", "Database configuration", 0.77
        )
        assert result.action == ConsolidationAction.ADD


class TestIsContradiction:
    def setup_method(self):
        self.consolidator = Consolidator.__new__(Consolidator)

    def test_replaced_pattern(self):
        assert self.consolidator._is_contradiction(
            "Replaced PostgreSQL with MySQL",
            "Use PostgreSQL for storage",
        )

    def test_switched_from_pattern(self):
        assert self.consolidator._is_contradiction(
            "Switched from Redis to Memcached",
            "Use Redis for caching",
        )

    def test_no_longer_using_pattern(self):
        assert self.consolidator._is_contradiction(
            "No longer using webpack for bundling",
            "Use webpack for bundling",
        )

    def test_no_contradiction_unrelated(self):
        assert not self.consolidator._is_contradiction(
            "Added new logging module",
            "Use PostgreSQL for storage",
        )

    def test_no_contradiction_similar_topic(self):
        assert not self.consolidator._is_contradiction(
            "Updated PostgreSQL to version 16",
            "Use PostgreSQL for storage",
        )

    def test_instead_of_pattern(self):
        assert self.consolidator._is_contradiction(
            "Use bun instead of npm for package management",
            "Use npm for package management",
        )


class TestCheckMemory:
    def test_no_existing_memories_returns_add(self):
        mock_chroma = MagicMock()
        mock_chroma.search.return_value = []
        mock_embedder = MagicMock()
        mock_embedder.embed_single.return_value = [0.1] * 384

        consolidator = Consolidator(
            sqlite_store=MagicMock(),
            chroma_store=mock_chroma,
            embedder=mock_embedder,
        )
        result = consolidator.check_memory("New fact about the project")
        assert result.action == ConsolidationAction.ADD

    def test_similar_existing_memory_returns_noop(self):
        mock_chroma = MagicMock()
        mock_chroma.search.return_value = [
            SearchResult(
                chunk_id="mem_existing",
                text="Use Redis for caching",
                score=0.95,
                metadata={},
            )
        ]
        mock_embedder = MagicMock()
        mock_embedder.embed_single.return_value = [0.1] * 384

        consolidator = Consolidator(
            sqlite_store=MagicMock(),
            chroma_store=mock_chroma,
            embedder=mock_embedder,
        )
        result = consolidator.check_memory("Use Redis for caching")
        assert result.action == ConsolidationAction.NOOP


class TestCheckDecision:
    def test_no_existing_decisions_returns_add(self):
        mock_sqlite = MagicMock()
        mock_sqlite.get_decisions.return_value = []
        mock_embedder = MagicMock()
        mock_embedder.embed_single.return_value = [0.1] * 384

        consolidator = Consolidator(
            sqlite_store=mock_sqlite,
            chroma_store=MagicMock(),
            embedder=mock_embedder,
        )
        result = consolidator.check_decision("Use REST over gRPC", "sess_123")
        assert result.action == ConsolidationAction.ADD


class TestCosineSimliarity:
    def test_identical_vectors(self):
        v = [1.0, 0.0, 0.0]
        assert abs(Consolidator._cosine_similarity(v, v) - 1.0) < 1e-6

    def test_orthogonal_vectors(self):
        a = [1.0, 0.0]
        b = [0.0, 1.0]
        assert abs(Consolidator._cosine_similarity(a, b)) < 1e-6

    def test_zero_vector(self):
        assert Consolidator._cosine_similarity([0, 0], [1, 1]) == 0.0
