"""Consolidator: deduplicates and updates memories and decisions."""

import re
from enum import Enum
from dataclasses import dataclass
from typing import Optional

from memotrail.core.embedder import Embedder
from memotrail.storage import ChromaStore, SQLiteStore
from memotrail.utils import config, get_logger

logger = get_logger("memotrail.core.consolidator")

# Regex patterns that indicate the new text contradicts/replaces the old
_CONTRADICTION_PATTERNS = [
    re.compile(r"(?:replaced|switched from|migrated from|moved away from|no longer using|stopped using|dropped|removed)\s+", re.IGNORECASE),
    re.compile(r"(?:don'?t|do not|never|avoid)\s+(?:use|use)\s+", re.IGNORECASE),
    re.compile(r"instead of\s+", re.IGNORECASE),
]


class ConsolidationAction(Enum):
    ADD = "add"
    UPDATE = "update"
    DELETE = "delete"
    NOOP = "noop"


@dataclass
class ConsolidationResult:
    action: ConsolidationAction
    existing_id: Optional[str] = None
    similarity: float = 0.0
    reason: str = ""


class Consolidator:
    """Checks existing memories/decisions before inserting, to avoid duplicates."""

    def __init__(
        self,
        sqlite_store: SQLiteStore | None = None,
        chroma_store: ChromaStore | None = None,
        embedder: Embedder | None = None,
    ):
        self.sqlite = sqlite_store or SQLiteStore()
        self.chroma = chroma_store or ChromaStore()
        self.embedder = embedder or Embedder()

    def check_memory(self, content: str, tags: Optional[list[str]] = None) -> ConsolidationResult:
        """Check if a memory should be added, updated, or skipped.

        Args:
            content: New memory text
            tags: Optional tags

        Returns:
            ConsolidationResult with the recommended action
        """
        embedding = self.embedder.embed_single(content)

        # Search existing memories for similar content
        results = self.chroma.search(
            query_embedding=embedding,
            limit=5,
            collection=ChromaStore.MEMORY_COLLECTION,
        )

        if not results:
            return ConsolidationResult(action=ConsolidationAction.ADD, reason="no existing memories")

        # Check the most similar result
        top = results[0]
        return self._decide_action(content, top.chunk_id, top.text, top.score)

    def check_decision(self, decision_text: str, session_id: str) -> ConsolidationResult:
        """Check if a decision should be added, updated, or skipped.

        Embeds the decision text and compares against existing decisions
        stored in ChromaDB's chat_chunks collection (with type=decision metadata).

        Args:
            decision_text: New decision text
            session_id: Session that produced this decision

        Returns:
            ConsolidationResult with the recommended action
        """
        # Get existing decisions from SQLite and compare via embeddings
        existing_decisions = self.sqlite.get_decisions(limit=50)
        if not existing_decisions:
            return ConsolidationResult(action=ConsolidationAction.ADD, reason="no existing decisions")

        new_embedding = self.embedder.embed_single(decision_text)
        existing_texts = [d.decision_text for d in existing_decisions]
        existing_embeddings = self.embedder.embed(existing_texts)

        # Find the most similar existing decision
        best_sim = 0.0
        best_idx = -1
        for i, emb in enumerate(existing_embeddings):
            sim = self._cosine_similarity(new_embedding, emb)
            if sim > best_sim:
                best_sim = sim
                best_idx = i

        if best_idx < 0:
            return ConsolidationResult(action=ConsolidationAction.ADD, reason="no similar decisions")

        existing = existing_decisions[best_idx]
        return self._decide_action(decision_text, existing.id, existing.decision_text, best_sim)

    def _decide_action(
        self,
        new_text: str,
        existing_id: str,
        existing_text: str,
        similarity: float,
    ) -> ConsolidationResult:
        """Core logic: decide ADD, UPDATE, DELETE, or NOOP based on similarity.

        Thresholds (from config):
        - sim < update_threshold (0.78) → ADD (new information)
        - 0.78 ≤ sim < noop_threshold (0.92) → UPDATE (same topic, newer version)
        - sim ≥ 0.92 and new text isn't longer → NOOP (near-duplicate)
        - sim ≥ 0.92 and new text is longer → UPDATE (richer version)
        - contradiction detected → DELETE old + ADD new
        """
        update_threshold = config.consolidation_update_threshold
        noop_threshold = config.consolidation_noop_threshold

        # Check for contradiction first
        if self._is_contradiction(new_text, existing_text):
            return ConsolidationResult(
                action=ConsolidationAction.DELETE,
                existing_id=existing_id,
                similarity=similarity,
                reason="contradiction detected — new text replaces old",
            )

        if similarity < update_threshold:
            return ConsolidationResult(
                action=ConsolidationAction.ADD,
                similarity=similarity,
                reason=f"low similarity ({similarity:.2f}), treating as new information",
            )

        if similarity >= noop_threshold:
            # Near-duplicate: only update if new text is meaningfully longer
            if len(new_text) > len(existing_text) * 1.2:
                return ConsolidationResult(
                    action=ConsolidationAction.UPDATE,
                    existing_id=existing_id,
                    similarity=similarity,
                    reason=f"near-duplicate ({similarity:.2f}) but new text is richer",
                )
            return ConsolidationResult(
                action=ConsolidationAction.NOOP,
                existing_id=existing_id,
                similarity=similarity,
                reason=f"near-duplicate ({similarity:.2f}), skipping",
            )

        # Between update and noop thresholds: update
        return ConsolidationResult(
            action=ConsolidationAction.UPDATE,
            existing_id=existing_id,
            similarity=similarity,
            reason=f"same topic ({similarity:.2f}), updating with newer version",
        )

    def _is_contradiction(self, new_text: str, existing_text: str) -> bool:
        """Check if new_text contradicts existing_text using regex patterns.

        Looks for replacement/negation language in the new text that references
        key terms from the existing text.
        """
        # Extract key terms from existing text (words > 3 chars)
        existing_terms = set(
            word.lower() for word in re.findall(r'\b\w{4,}\b', existing_text)
        )

        for pattern in _CONTRADICTION_PATTERNS:
            match = pattern.search(new_text)
            if match:
                # Check if the contradiction references something from the existing text
                after_match = new_text[match.start():].lower()
                for term in existing_terms:
                    if term in after_match:
                        return True

        return False

    @staticmethod
    def _cosine_similarity(a: list[float], b: list[float]) -> float:
        """Compute cosine similarity between two vectors."""
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)
