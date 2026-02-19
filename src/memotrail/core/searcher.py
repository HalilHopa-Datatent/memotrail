"""Searcher: semantic search across stored conversations and memories."""

from dataclasses import dataclass

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

    def search_memories(self, query: str, limit: int = 10) -> list[SearchResult]:
        """Search manual memory notes."""
        query_embedding = self.embedder.embed_single(query)
        return self.chroma.search(
            query_embedding=query_embedding,
            limit=limit,
            collection=ChromaStore.MEMORY_COLLECTION,
        )
