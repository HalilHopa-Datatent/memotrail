"""Searcher: semantic and keyword search across stored conversations and memories."""

from dataclasses import dataclass

from memotrail.core.bm25 import BM25Index
from memotrail.core.embedder import Embedder
from memotrail.storage import ChromaStore, SQLiteStore, SearchResult
from memotrail.utils import get_logger

logger = get_logger("memotrail.core.searcher")


@dataclass
class ChatSearchResult:
    """Enriched search result with session context."""
    chunk_text: str
    score: float
    session_id: str
    project: str | None
    timestamp: str | None
    session_summary: str | None


class Searcher:
    """Search across indexed conversations and memories."""

    def __init__(
        self,
        sqlite_store: SQLiteStore | None = None,
        chroma_store: ChromaStore | None = None,
        embedder: Embedder | None = None,
    ):
        self.sqlite = sqlite_store or SQLiteStore()
        self.chroma = chroma_store or ChromaStore()
        self.embedder = embedder or Embedder()
        self._bm25_index: BM25Index | None = None

    def search_chats(
        self,
        query: str,
        limit: int = 10,
        project: str | None = None,
    ) -> list[ChatSearchResult]:
        """Search past conversations semantically.

        Args:
            query: Natural language search query
            limit: Max results
            project: Optional filter by project

        Returns:
            List of enriched search results
        """
        query_embedding = self.embedder.embed_single(query)

        where = None
        if project:
            where = {"project": project}

        results = self.chroma.search(
            query_embedding=query_embedding,
            limit=limit,
            collection=ChromaStore.CHAT_COLLECTION,
            where=where,
        )

        # Enrich with session metadata
        enriched = []
        session_cache: dict = {}
        for r in results:
            session_id = r.metadata.get("session_id", "")
            if session_id not in session_cache:
                session_cache[session_id] = self.sqlite.get_session(session_id)

            session = session_cache.get(session_id)
            enriched.append(ChatSearchResult(
                chunk_text=r.text,
                score=r.score,
                session_id=session_id,
                project=session.project if session else None,
                timestamp=r.metadata.get("timestamp"),
                session_summary=session.summary if session else None,
            ))

        return enriched

    def search_keyword(
        self,
        query: str,
        limit: int = 10,
        project: str | None = None,
    ) -> list[ChatSearchResult]:
        """Search past conversations using BM25 keyword matching.

        Builds an in-memory BM25 index from stored messages on first call.

        Args:
            query: Keyword search query
            limit: Max results
            project: Optional filter by project

        Returns:
            List of enriched search results
        """
        if self._bm25_index is None:
            self._build_bm25_index()

        where = None
        if project:
            where = {"project": project}

        bm25_results = self._bm25_index.search(query, limit=limit, where=where)

        session_cache: dict = {}
        enriched = []
        for r in bm25_results:
            session_id = r.metadata.get("session_id", "")
            if session_id not in session_cache:
                session_cache[session_id] = self.sqlite.get_session(session_id)

            session = session_cache.get(session_id)
            enriched.append(ChatSearchResult(
                chunk_text=r.text,
                score=r.score,
                session_id=session_id,
                project=session.project if session else None,
                timestamp=r.metadata.get("timestamp"),
                session_summary=session.summary if session else None,
            ))

        return enriched

    def search_hybrid(
        self,
        query: str,
        limit: int = 10,
        project: str | None = None,
        semantic_weight: float = 0.7,
    ) -> list[ChatSearchResult]:
        """Hybrid search combining semantic and keyword results.

        Uses reciprocal rank fusion to merge results from both methods.

        Args:
            query: Search query
            limit: Max results
            project: Optional filter by project
            semantic_weight: Weight for semantic results (0-1), keyword gets 1-weight

        Returns:
            List of merged, deduplicated search results
        """
        # Get results from both methods (fetch more to allow good merging)
        fetch_limit = limit * 2
        semantic_results = self.search_chats(query, limit=fetch_limit, project=project)
        keyword_results = self.search_keyword(query, limit=fetch_limit, project=project)

        # Reciprocal rank fusion
        rrf_scores: dict[str, float] = {}
        result_map: dict[str, ChatSearchResult] = {}
        k = 60  # RRF constant

        for rank, r in enumerate(semantic_results):
            key = f"{r.session_id}:{r.chunk_text[:100]}"
            rrf_scores[key] = rrf_scores.get(key, 0) + semantic_weight / (k + rank + 1)
            result_map[key] = r

        keyword_weight = 1.0 - semantic_weight
        for rank, r in enumerate(keyword_results):
            key = f"{r.session_id}:{r.chunk_text[:100]}"
            rrf_scores[key] = rrf_scores.get(key, 0) + keyword_weight / (k + rank + 1)
            if key not in result_map:
                result_map[key] = r

        # Sort by fused score
        sorted_keys = sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)

        results = []
        for key in sorted_keys[:limit]:
            r = result_map[key]
            results.append(ChatSearchResult(
                chunk_text=r.chunk_text,
                score=rrf_scores[key],
                session_id=r.session_id,
                project=r.project,
                timestamp=r.timestamp,
                session_summary=r.session_summary,
            ))

        return results

    def search_memories(self, query: str, limit: int = 10) -> list[SearchResult]:
        """Search manual memory notes."""
        query_embedding = self.embedder.embed_single(query)
        return self.chroma.search(
            query_embedding=query_embedding,
            limit=limit,
            collection=ChromaStore.MEMORY_COLLECTION,
        )

    def _build_bm25_index(self) -> None:
        """Build BM25 index from all stored messages."""
        logger.info("Building BM25 index from stored messages...")
        self._bm25_index = BM25Index()

        sessions = self.sqlite.get_recent_sessions(limit=1000)

        doc_ids = []
        texts = []
        metadatas = []

        for session in sessions:
            messages = self.sqlite.get_session_messages(session.id)
            if not messages:
                continue

            # Group messages into a single document per session
            content_parts = []
            for msg in messages:
                content_parts.append(f"[{msg.role}]: {msg.content}")

            doc_ids.append(session.id)
            texts.append("\n".join(content_parts))
            metadatas.append({
                "session_id": session.id,
                "project": session.project,
                "timestamp": session.started_at,
            })

        if doc_ids:
            self._bm25_index.add_documents(doc_ids, texts, metadatas)

        logger.info(f"BM25 index built with {len(doc_ids)} document(s)")

    def invalidate_bm25_cache(self) -> None:
        """Force rebuild of BM25 index on next keyword search."""
        self._bm25_index = None
