"""Indexer: orchestrates chunking, embedding, and storage."""

from memotrail.core.chunker import Chunker, Chunk
from memotrail.core.embedder import Embedder
from memotrail.extractors import summarize_session, extract_decisions
from memotrail.storage import ChromaStore, SQLiteStore
from memotrail.utils import get_logger, count_tokens

logger = get_logger("memotrail.core.indexer")


class Indexer:
    """Indexes conversations into vector and metadata stores."""

    def __init__(
        self,
        sqlite_store: SQLiteStore | None = None,
        chroma_store: ChromaStore | None = None,
        chunker: Chunker | None = None,
        embedder: Embedder | None = None,
    ):
        self.sqlite = sqlite_store or SQLiteStore()
        self.chroma = chroma_store or ChromaStore()
        self.chunker = chunker or Chunker()
        self.embedder = embedder or Embedder()

    def index_session(
        self,
        messages: list[dict],
        project: str | None = None,
        source: str = "claude_code",
        tags: list[str] | None = None,
    ) -> str:
        """Index a complete session (list of messages).

        Args:
            messages: List of {"role": str, "content": str, "timestamp": str}
            project: Optional project name
            source: Source tool (claude_code, cursor, etc.)
            tags: Optional tags

        Returns:
            Session ID
        """
        # 1. Create session in SQLite
        session = self.sqlite.create_session(project=project, source=source, tags=tags)
        logger.info(f"Created session {session.id} ({len(messages)} messages)")

        # 2. Store individual messages
        for msg in messages:
            self.sqlite.add_message(
                session_id=session.id,
                role=msg.get("role", "unknown"),
                content=msg.get("content", ""),
                token_count=count_tokens(msg.get("content", "")),
            )

        # 3. Chunk the conversation
        chunks = self.chunker.chunk_messages(messages, session.id, project)
        if not chunks:
            logger.warning(f"No chunks generated for session {session.id}")
            return session.id

        # 4. Generate embeddings
        texts = [c.text for c in chunks]
        embeddings = self.embedder.embed(texts)

        # 5. Store in ChromaDB
        self.chroma.add_chunks(
            chunks=texts,
            embeddings=embeddings,
            metadatas=[c.metadata for c in chunks],
            ids=[c.id for c in chunks],
        )

        # 6. Generate session summary
        summary = None
        try:
            summary = summarize_session(messages)
        except Exception as e:
            logger.warning(f"Summary generation failed for {session.id}: {e}")

        # 7. Extract decisions
        try:
            decisions = extract_decisions(messages)
            for dec in decisions:
                self.sqlite.add_decision(
                    session_id=session.id,
                    decision_text=dec.decision_text,
                    context=dec.context,
                    category=dec.category,
                )
            if decisions:
                logger.info(f"Extracted {len(decisions)} decision(s) from session {session.id}")
        except Exception as e:
            logger.warning(f"Decision extraction failed for {session.id}: {e}")

        # 8. Update session metadata
        self.sqlite.update_session(
            session.id, message_count=len(messages), summary=summary
        )

        logger.info(
            f"Indexed session {session.id}: {len(messages)} messages → {len(chunks)} chunks"
        )
        return session.id

    def index_memory(self, content: str, tags: list[str] | None = None) -> str:
        """Index a manual memory note.

        Args:
            content: Memory text
            tags: Optional tags

        Returns:
            Memory ID
        """
        memory_id = self.sqlite.save_memory(content, tags)

        embedding = self.embedder.embed_single(content)
        self.chroma.add_chunks(
            chunks=[content],
            embeddings=[embedding],
            metadatas=[{"type": "memory", "memory_id": memory_id, "tags": ",".join(tags or [])}],
            ids=[memory_id],
            collection=ChromaStore.MEMORY_COLLECTION,
        )

        logger.info(f"Indexed memory {memory_id}")
        return memory_id
