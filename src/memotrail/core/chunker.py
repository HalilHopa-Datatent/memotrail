"""Chunker: splits conversations into meaningful chunks for embedding."""

import uuid
from dataclasses import dataclass

from memotrail.utils import config, count_tokens


@dataclass
class Chunk:
    """A text chunk ready for embedding."""
    id: str
    text: str
    token_count: int
    metadata: dict


class Chunker:
    """Split conversation messages into chunks for indexing."""

    def __init__(
        self,
        max_tokens: int | None = None,
        overlap_tokens: int | None = None,
    ):
        self.max_tokens = max_tokens or config.chunk_max_tokens
        self.overlap_tokens = overlap_tokens or config.chunk_overlap_tokens

    def chunk_messages(
        self,
        messages: list[dict],
        session_id: str,
        project: str | None = None,
    ) -> list[Chunk]:
        """Chunk a list of messages into embedding-ready pieces.

        Groups consecutive messages into chunks that fit within the token limit.
        Each chunk contains one or more messages with role prefixes.

        Args:
            messages: List of {"role": str, "content": str, "timestamp": str}
            session_id: Session ID for metadata
            project: Optional project name

        Returns:
            List of Chunk objects
        """
        if not messages:
            return []

        chunks = []
        current_lines: list[str] = []
        current_tokens = 0

        for msg in messages:
            role = msg.get("role", "unknown")
            content = msg.get("content", "").strip()
            if not content:
                continue

            line = f"[{role}]: {content}"
            line_tokens = count_tokens(line)

            # If single message exceeds max, split it
            if line_tokens > self.max_tokens:
                # Flush current buffer first
                if current_lines:
                    chunks.append(self._make_chunk(
                        current_lines, current_tokens, session_id, project, msg.get("timestamp")
                    ))
                    current_lines = []
                    current_tokens = 0

                # Split the long message
                chunks.extend(
                    self._split_long_message(line, session_id, project, msg.get("timestamp"))
                )
                continue

            # Would adding this message exceed the limit?
            if current_tokens + line_tokens > self.max_tokens and current_lines:
                chunks.append(self._make_chunk(
                    current_lines, current_tokens, session_id, project, msg.get("timestamp")
                ))
                # Keep last message as overlap for context continuity
                if self.overlap_tokens > 0 and current_lines:
                    last_line = current_lines[-1]
                    last_tokens = count_tokens(last_line)
                    if last_tokens <= self.overlap_tokens:
                        current_lines = [last_line]
                        current_tokens = last_tokens
                    else:
                        current_lines = []
                        current_tokens = 0
                else:
                    current_lines = []
                    current_tokens = 0

            current_lines.append(line)
            current_tokens += line_tokens

        # Flush remaining
        if current_lines:
            chunks.append(self._make_chunk(
                current_lines, current_tokens, session_id, project,
                messages[-1].get("timestamp") if messages else None,
            ))

        return chunks

    def _make_chunk(
        self,
        lines: list[str],
        token_count: int,
        session_id: str,
        project: str | None,
        timestamp: str | None,
    ) -> Chunk:
        text = "\n".join(lines)
        metadata = {
            "session_id": session_id,
            "type": "conversation",
        }
        if project:
            metadata["project"] = project
        if timestamp:
            metadata["timestamp"] = timestamp

        return Chunk(
            id=f"chunk_{uuid.uuid4().hex[:12]}",
            text=text,
            token_count=token_count,
            metadata=metadata,
        )

    def _split_long_message(
        self,
        text: str,
        session_id: str,
        project: str | None,
        timestamp: str | None,
    ) -> list[Chunk]:
        """Split a single long message into multiple chunks."""
        words = text.split()
        chunks = []
        current_words: list[str] = []
        current_tokens = 0

        for word in words:
            word_tokens = count_tokens(word + " ")
            if current_tokens + word_tokens > self.max_tokens and current_words:
                chunk_text = " ".join(current_words)
                metadata = {"session_id": session_id, "type": "conversation"}
                if project:
                    metadata["project"] = project
                if timestamp:
                    metadata["timestamp"] = timestamp
                chunks.append(Chunk(
                    id=f"chunk_{uuid.uuid4().hex[:12]}",
                    text=chunk_text,
                    token_count=current_tokens,
                    metadata=metadata,
                ))
                current_words = []
                current_tokens = 0

            current_words.append(word)
            current_tokens += word_tokens

        if current_words:
            chunk_text = " ".join(current_words)
            metadata = {"session_id": session_id, "type": "conversation"}
            if project:
                metadata["project"] = project
            if timestamp:
                metadata["timestamp"] = timestamp
            chunks.append(Chunk(
                id=f"chunk_{uuid.uuid4().hex[:12]}",
                text=chunk_text,
                token_count=current_tokens,
                metadata=metadata,
            ))

        return chunks
