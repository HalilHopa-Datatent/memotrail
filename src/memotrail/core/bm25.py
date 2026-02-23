"""BM25 keyword search — lightweight pure-Python implementation."""

import math
import re
from dataclasses import dataclass

from memotrail.utils import get_logger

logger = get_logger("memotrail.core.bm25")

# BM25 parameters
_K1 = 1.5
_B = 0.75

# Common English stop words to filter out
_STOP_WORDS = frozenset({
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "shall", "can", "need", "must",
    "it", "its", "this", "that", "these", "those", "i", "you", "he", "she",
    "we", "they", "me", "him", "her", "us", "them", "my", "your", "his",
    "our", "their", "what", "which", "who", "when", "where", "how", "not",
    "no", "so", "if", "then", "than", "too", "very", "just", "about",
})

_TOKEN_RE = re.compile(r"[a-zA-Z0-9_]+")


@dataclass
class BM25Result:
    """A single BM25 search result."""
    doc_id: str
    text: str
    score: float
    metadata: dict


def _tokenize(text: str) -> list[str]:
    """Tokenize text into lowercase words, filtering stop words."""
    tokens = _TOKEN_RE.findall(text.lower())
    return [t for t in tokens if t not in _STOP_WORDS and len(t) > 1]


class BM25Index:
    """In-memory BM25 index for keyword search over documents."""

    def __init__(self):
        self._docs: list[dict] = []  # [{id, text, metadata, tokens}]
        self._doc_count = 0
        self._avg_dl = 0.0
        self._df: dict[str, int] = {}  # document frequency per term

    def add_documents(
        self,
        doc_ids: list[str],
        texts: list[str],
        metadatas: list[dict] | None = None,
    ) -> None:
        """Add documents to the index."""
        metadatas = metadatas or [{} for _ in texts]

        for doc_id, text, meta in zip(doc_ids, texts, metadatas):
            tokens = _tokenize(text)
            self._docs.append({
                "id": doc_id,
                "text": text,
                "metadata": meta,
                "tokens": tokens,
            })

            # Update document frequency
            unique_tokens = set(tokens)
            for token in unique_tokens:
                self._df[token] = self._df.get(token, 0) + 1

        # Recalculate average document length
        self._doc_count = len(self._docs)
        if self._doc_count > 0:
            self._avg_dl = sum(len(d["tokens"]) for d in self._docs) / self._doc_count

    def search(
        self,
        query: str,
        limit: int = 10,
        where: dict | None = None,
    ) -> list[BM25Result]:
        """Search documents using BM25 scoring.

        Args:
            query: Search query string
            limit: Max results to return
            where: Optional metadata filter (e.g., {"project": "myapp"})

        Returns:
            List of BM25Result sorted by score descending
        """
        query_tokens = _tokenize(query)
        if not query_tokens or not self._docs:
            return []

        scores: list[tuple[int, float]] = []

        for idx, doc in enumerate(self._docs):
            # Apply metadata filter
            if where:
                if not all(doc["metadata"].get(k) == v for k, v in where.items()):
                    continue

            score = self._score_document(query_tokens, doc["tokens"])
            if score > 0:
                scores.append((idx, score))

        # Sort by score descending
        scores.sort(key=lambda x: x[1], reverse=True)

        results = []
        for idx, score in scores[:limit]:
            doc = self._docs[idx]
            results.append(BM25Result(
                doc_id=doc["id"],
                text=doc["text"],
                score=score,
                metadata=doc["metadata"],
            ))

        return results

    def _score_document(self, query_tokens: list[str], doc_tokens: list[str]) -> float:
        """Calculate BM25 score for a document against query tokens."""
        dl = len(doc_tokens)
        if dl == 0:
            return 0.0

        # Count term frequencies in document
        tf: dict[str, int] = {}
        for token in doc_tokens:
            tf[token] = tf.get(token, 0) + 1

        score = 0.0
        for qt in query_tokens:
            if qt not in tf:
                continue

            # IDF component
            df = self._df.get(qt, 0)
            idf = math.log((self._doc_count - df + 0.5) / (df + 0.5) + 1.0)

            # TF component with BM25 normalization
            term_freq = tf[qt]
            tf_norm = (term_freq * (_K1 + 1)) / (
                term_freq + _K1 * (1 - _B + _B * dl / self._avg_dl)
            )

            score += idf * tf_norm

        return score

    @property
    def document_count(self) -> int:
        return self._doc_count
