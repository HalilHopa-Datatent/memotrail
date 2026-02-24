"""Indexer: orchestrates chunking, embedding, and storage."""

from memotrail.core.chunker import Chunker, Chunk
from memotrail.core.consolidator import Consolidator, ConsolidationAction
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
        consolidator: Consolidator | None = None,
    ):
        self.sqlite = sqlite_store or SQLiteStore()
        self.chroma = chroma_store or ChromaStore()
        self.chunker = chunker or Chunker()
        self.embedder = embedder or Embedder()
        self.consolidator = consolidator or Consolidator(self.sqlite, self.chroma, self.embedder)

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

        # 7. Extract decisions (with consolidation)
        try:
            decisions = extract_decisions(messages)
            added_count = 0
            for dec in decisions:
                result = self.consolidator.check_decision(dec.decision_text, session.id)
                if result.action == ConsolidationAction.ADD:
                    self.sqlite.add_decision(
                        session_id=session.id,
                        decision_text=dec.decision_text,
                        context=dec.context,
                        category=dec.category,
                    )
                    added_count += 1
                elif result.action == ConsolidationAction.UPDATE and result.existing_id:
                    self.sqlite.update_decision(
                        result.existing_id,
                        decision_text=dec.decision_text,
                        context=dec.context,
                    )
                    added_count += 1
                elif result.action == ConsolidationAction.DELETE and result.existing_id:
                    self.sqlite.delete_decision(result.existing_id)
                    self.sqlite.add_decision(
                        session_id=session.id,
                        decision_text=dec.decision_text,
                        context=dec.context,
                        category=dec.category,
                    )
                    added_count += 1
                else:
                    logger.debug(f"Decision skipped (NOOP): {dec.decision_text[:60]}")
            if added_count:
                logger.info(f"Processed {added_count}/{len(decisions)} decision(s) for session {session.id}")
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

    def index_memory(self, content: str, tags: list[str] | None = None) -> tuple[str, ConsolidationAction]:
        """Index a manual memory note with consolidation.

        Args:
            content: Memory text
            tags: Optional tags

        Returns:
            Tuple of (memory_id, action_taken)
        """
        result = self.consolidator.check_memory(content, tags)
        logger.info(f"Memory consolidation: {result.action.value} — {result.reason}")

        if result.action == ConsolidationAction.NOOP:
            return result.existing_id or "", ConsolidationAction.NOOP

        if result.action == ConsolidationAction.UPDATE and result.existing_id:
            # Update existing memory in SQLite and ChromaDB
            self.sqlite.update_memory(result.existing_id, content, tags)
            embedding = self.embedder.embed_single(content)
            self.chroma.update_chunk(
                chunk_id=result.existing_id,
                text=content,
                embedding=embedding,
                metadata={"type": "memory", "memory_id": result.existing_id, "tags": ",".join(tags or [])},
                collection=ChromaStore.MEMORY_COLLECTION,
            )
            logger.info(f"Updated memory {result.existing_id}")
            return result.existing_id, ConsolidationAction.UPDATE

        if result.action == ConsolidationAction.DELETE and result.existing_id:
            # Delete old, then add new
            self.sqlite.delete_memory(result.existing_id)
            self.chroma.delete_by_ids([result.existing_id], collection=ChromaStore.MEMORY_COLLECTION)
            logger.info(f"Deleted contradicted memory {result.existing_id}")

        # ADD (or ADD after DELETE)
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
        return memory_id, result.action
