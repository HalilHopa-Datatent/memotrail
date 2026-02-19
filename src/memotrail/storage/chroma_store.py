"""ChromaDB vector storage for semantic search."""

from typing import Optional
from dataclasses import dataclass

import chromadb
from chromadb.config import Settings

from memotrail.utils import config, get_logger

logger = get_logger("memotrail.storage.chroma")


@dataclass
class SearchResult:
    """A single search result from ChromaDB."""
    chunk_id: str
    text: str
    score: float
    metadata: dict


class ChromaStore:
    """ChromaDB-based vector storage for embeddings."""

    CHAT_COLLECTION = "chat_chunks"
    MEMORY_COLLECTION = "memories"

    def __init__(self, persist_dir: Optional[str] = None):
        self.persist_dir = persist_dir or str(config.chroma_dir)
        self._client: Optional[chromadb.ClientAPI] = None

    def connect(self) -> None:
        """Initialize ChromaDB client."""
        config.ensure_dirs()
        self._client = chromadb.PersistentClient(
            path=self.persist_dir,
            settings=Settings(anonymized_telemetry=False),
        )
        # Ensure collections exist
        self._client.get_or_create_collection(
            name=self.CHAT_COLLECTION,
            metadata={"hnsw:space": "cosine"},
        )
        self._client.get_or_create_collection(
            name=self.MEMORY_COLLECTION,
            metadata={"hnsw:space": "cosine"},
        )
        logger.info(f"ChromaDB connected: {self.persist_dir}")

    @property
    def client(self) -> chromadb.ClientAPI:
        if self._client is None:
            self.connect()
        return self._client

    def _get_collection(self, collection_name: str):
        return self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add_chunks(
        self,
        chunks: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict],
        ids: list[str],
        collection: str = CHAT_COLLECTION,
    ) -> None:
        """Add text chunks with pre-computed embeddings."""
        col = self._get_collection(collection)
        col.add(
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids,
        )
        logger.info(f"Added {len(chunks)} chunks to '{collection}'")

    def search(
        self,
        query_embedding: list[float],
        limit: int = 10,
        collection: str = CHAT_COLLECTION,
        where: Optional[dict] = None,
    ) -> list[SearchResult]:
        """Search for similar chunks."""
        col = self._get_collection(collection)

        kwargs = {
            "query_embeddings": [query_embedding],
            "n_results": min(limit, col.count()) if col.count() > 0 else limit,
        }
        if where:
            kwargs["where"] = where

        try:
            results = col.query(**kwargs)
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []

        if not results or not results["ids"] or not results["ids"][0]:
            return []

        search_results = []
        for i, chunk_id in enumerate(results["ids"][0]):
            score = 1.0 - (results["distances"][0][i] if results["distances"] else 0)
            search_results.append(
                SearchResult(
                    chunk_id=chunk_id,
                    text=results["documents"][0][i] if results["documents"] else "",
                    score=score,
                    metadata=results["metadatas"][0][i] if results["metadatas"] else {},
                )
            )
        return search_results

    def get_collection_count(self, collection: str = CHAT_COLLECTION) -> int:
        """Get number of items in a collection."""
        col = self._get_collection(collection)
        return col.count()

    def delete_by_session(self, session_id: str, collection: str = CHAT_COLLECTION) -> None:
        """Delete all chunks for a session."""
        col = self._get_collection(collection)
        col.delete(where={"session_id": session_id})
