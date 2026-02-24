"""Reranker: cross-encoder reranking for search results."""

import math
from dataclasses import dataclass
from typing import Any

from memotrail.utils import config, get_logger

logger = get_logger("memotrail.core.reranker")

_cross_encoder = None


def _load_cross_encoder():
    """Lazy-load the cross-encoder model."""
    global _cross_encoder
    if _cross_encoder is None:
        from sentence_transformers import CrossEncoder
        model_name = config.reranker_model
        logger.info(f"Loading cross-encoder model: {model_name}")
        _cross_encoder = CrossEncoder(model_name)
        logger.info("Cross-encoder model loaded.")
    return _cross_encoder


class Reranker:
    """Reranks search results using a cross-encoder model."""

    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or config.reranker_model

    def rerank(
        self,
        query: str,
        results: list[Any],
        limit: int,
        text_getter=None,
    ) -> list[Any]:
        """Rerank results using cross-encoder scoring.

        Args:
            query: The search query
            results: List of result objects to rerank
            limit: Number of top results to return
            text_getter: Callable to extract text from a result.
                         Defaults to using .chunk_text for ChatSearchResult
                         or .text for SearchResult.

        Returns:
            Reranked list of results (top `limit`)
        """
        if not results or len(results) <= 1:
            return results[:limit]

        model = _load_cross_encoder()

        # Extract text from results
        if text_getter is None:
            def text_getter(r):
                return getattr(r, 'chunk_text', None) or getattr(r, 'text', '')

        pairs = [[query, text_getter(r)] for r in results]
        scores = model.predict(pairs)

        # Normalize scores with sigmoid
        normalized = [self._sigmoid(float(s)) for s in scores]

        # Pair results with scores and sort
        scored = list(zip(results, normalized))
        scored.sort(key=lambda x: x[1], reverse=True)

        # Update scores on results and return top-k
        reranked = []
        for result, score in scored[:limit]:
            # Update the score attribute
            if hasattr(result, 'score'):
                result.score = score
            reranked.append(result)

        return reranked

    @staticmethod
    def _sigmoid(x: float) -> float:
        """Sigmoid normalization."""
        try:
            return 1.0 / (1.0 + math.exp(-x))
        except OverflowError:
            return 0.0 if x < 0 else 1.0
