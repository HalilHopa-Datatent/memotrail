"""Tests for the Reranker module."""

import math
from dataclasses import dataclass
from unittest.mock import MagicMock, patch

from memotrail.core.reranker import Reranker


@dataclass
class FakeResult:
    chunk_text: str
    score: float


class TestRerankerSigmoid:
    def test_sigmoid_zero(self):
        assert abs(Reranker._sigmoid(0) - 0.5) < 1e-6

    def test_sigmoid_positive(self):
        result = Reranker._sigmoid(5.0)
        assert result > 0.99

    def test_sigmoid_negative(self):
        result = Reranker._sigmoid(-5.0)
        assert result < 0.01

    def test_sigmoid_overflow_positive(self):
        assert Reranker._sigmoid(1000) == 1.0

    def test_sigmoid_overflow_negative(self):
        assert Reranker._sigmoid(-1000) == 0.0


class TestRerankerRerank:
    @patch("memotrail.core.reranker._load_cross_encoder")
    def test_rerank_reorders_results(self, mock_load):
        mock_model = MagicMock()
        # Return scores that invert the original order
        mock_model.predict.return_value = [0.1, 0.9, 0.5]
        mock_load.return_value = mock_model

        results = [
            FakeResult(chunk_text="First", score=0.9),
            FakeResult(chunk_text="Second", score=0.8),
            FakeResult(chunk_text="Third", score=0.7),
        ]

        reranker = Reranker()
        reranked = reranker.rerank("test query", results, limit=3)

        assert len(reranked) == 3
        assert reranked[0].chunk_text == "Second"  # Highest cross-encoder score
        assert reranked[1].chunk_text == "Third"
        assert reranked[2].chunk_text == "First"

    @patch("memotrail.core.reranker._load_cross_encoder")
    def test_rerank_respects_limit(self, mock_load):
        mock_model = MagicMock()
        mock_model.predict.return_value = [0.5, 0.9, 0.1]
        mock_load.return_value = mock_model

        results = [
            FakeResult(chunk_text="A", score=0.9),
            FakeResult(chunk_text="B", score=0.8),
            FakeResult(chunk_text="C", score=0.7),
        ]

        reranker = Reranker()
        reranked = reranker.rerank("test query", results, limit=2)

        assert len(reranked) == 2

    def test_rerank_empty_results(self):
        reranker = Reranker()
        assert reranker.rerank("query", [], limit=5) == []

    def test_rerank_single_result(self):
        reranker = Reranker()
        results = [FakeResult(chunk_text="Only", score=0.5)]
        reranked = reranker.rerank("query", results, limit=5)
        assert len(reranked) == 1
        assert reranked[0].chunk_text == "Only"

    @patch("memotrail.core.reranker._load_cross_encoder")
    def test_rerank_updates_scores(self, mock_load):
        mock_model = MagicMock()
        mock_model.predict.return_value = [2.0, -1.0]  # sigmoid(2.0) ≈ 0.88
        mock_load.return_value = mock_model

        results = [
            FakeResult(chunk_text="Test", score=0.5),
            FakeResult(chunk_text="Other", score=0.3),
        ]
        reranker = Reranker()
        reranked = reranker.rerank("query", results, limit=2)

        expected = 1.0 / (1.0 + math.exp(-2.0))
        assert abs(reranked[0].score - expected) < 0.01
        assert reranked[0].chunk_text == "Test"
