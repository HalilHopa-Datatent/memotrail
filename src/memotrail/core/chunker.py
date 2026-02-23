"""Chunker: splits conversations into meaningful chunks for embedding."""

import re
import uuid
from dataclasses import dataclass
from typing import Literal

from memotrail.utils import config, count_tokens


@dataclass
class Chunk:
    """A text chunk ready for embedding."""
    id: str
    text: str
    token_count: int
    metadata: dict


ChunkStrategy = Literal["token", "turn", "recursive"]


class Chunker:
    """Split conversation messages into chunks for indexing.

    Strategies:
        - "token": Groups consecutive messages up to token limit (default)
        - "turn": Groups user+assistant pairs as natural conversation turns
        - "recursive": Splits on natural boundaries (paragraphs, sentences, then words)
    """

    def __init__(
        self,
        max_tokens: int | None = None,
        overlap_tokens: int | None = None,
        strategy: ChunkStrategy = "token",
    ):
        self.max_tokens = max_tokens or config.chunk_max_tokens
        self.overlap_tokens = overlap_tokens or config.chunk_overlap_tokens
        self.strategy = strategy

    def chunk_messages(
        self,
        messages: list[dict],
        session_id: str,
        project: str | None = None,
    ) -> list[Chunk]:
        """Chunk a list of messages into embedding-ready pieces.

        Args:
            messages: List of {"role": str, "content": str, "timestamp": str}
            session_id: Session ID for metadata
            project: Optional project name

        Returns:
            List of Chunk objects
        """
        if not messages:
            return []

        if self.strategy == "turn":
            return self._chunk_by_turns(messages, session_id, project)
        elif self.strategy == "recursive":
            return self._chunk_recursive(messages, session_id, project)
        else:
            return self._chunk_by_tokens(messages, session_id, project)

    # ── Token-based chunking (original) ──────────────────────────

    def _chunk_by_tokens(
        self,
        messages: list[dict],
        session_id: str,
        project: str | None,
    ) -> list[Chunk]:
        """Group consecutive messages up to token limit."""
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
                if current_lines:
                    chunks.append(self._make_chunk(
                        current_lines, current_tokens, session_id, project, msg.get("timestamp")
                    ))
                    current_lines = []
                    current_tokens = 0

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

        if current_lines:
            chunks.append(self._make_chunk(
                current_lines, current_tokens, session_id, project,
                messages[-1].get("timestamp") if messages else None,
            ))

        return chunks

    # ── Turn-based chunking ──────────────────────────────────────

    def _chunk_by_turns(
        self,
        messages: list[dict],
        session_id: str,
        project: str | None,
    ) -> list[Chunk]:
        """Group messages by conversation turns (user question + assistant response).

        Each turn becomes one chunk. If a turn exceeds max_tokens,
        falls back to token-based splitting for that turn.
        """
        chunks = []
        current_turn: list[dict] = []
        last_role = None

        for msg in messages:
            role = msg.get("role", "unknown")
            content = msg.get("content", "").strip()
            if not content:
                continue

            # A new user message after an assistant message starts a new turn
            if role in ("user", "human") and last_role == "assistant":
                if current_turn:
                    chunks.extend(
                        self._turn_to_chunks(current_turn, session_id, project)
                    )
                current_turn = []

            current_turn.append(msg)
            last_role = role

        # Flush last turn
        if current_turn:
            chunks.extend(
                self._turn_to_chunks(current_turn, session_id, project)
            )

        return chunks

    def _turn_to_chunks(
        self,
        turn_messages: list[dict],
        session_id: str,
        project: str | None,
    ) -> list[Chunk]:
        """Convert a single conversation turn into one or more chunks."""
        lines = []
        for msg in turn_messages:
            role = msg.get("role", "unknown")
            content = msg.get("content", "").strip()
            if content:
                lines.append(f"[{role}]: {content}")

        text = "\n".join(lines)
        tokens = count_tokens(text)
        timestamp = turn_messages[0].get("timestamp")

        if tokens <= self.max_tokens:
            return [self._make_chunk(lines, tokens, session_id, project, timestamp)]

        # Turn is too long, fall back to token-based splitting
        return self._chunk_by_tokens(turn_messages, session_id, project)

    # ── Recursive chunking ───────────────────────────────────────

    def _chunk_recursive(
        self,
        messages: list[dict],
        session_id: str,
        project: str | None,
    ) -> list[Chunk]:
        """Split messages using recursive text splitting on natural boundaries.

        First tries paragraphs, then sentences, then words.
        """
        # Combine all messages into a single text with role markers
        lines = []
        timestamp = None
        for msg in messages:
            role = msg.get("role", "unknown")
            content = msg.get("content", "").strip()
            if not content:
                continue
            lines.append(f"[{role}]: {content}")
            if not timestamp:
                timestamp = msg.get("timestamp")

        full_text = "\n".join(lines)

        # Recursively split
        text_chunks = self._recursive_split(full_text)

        chunks = []
        for text in text_chunks:
            tokens = count_tokens(text)
            chunks.append(self._make_chunk(
                [text], tokens, session_id, project, timestamp
            ))

        return chunks

    def _recursive_split(self, text: str) -> list[str]:
        """Recursively split text on natural boundaries."""
        tokens = count_tokens(text)
        if tokens <= self.max_tokens:
            return [text] if text.strip() else []

        # Try splitting on these separators in order
        separators = [
            "\n\n",       # Double newline (paragraphs)
            "\n",         # Single newline
            ". ",         # Sentence boundary
            "? ",         # Question boundary
            "! ",         # Exclamation boundary
            "; ",         # Semicolon
            ", ",         # Comma
            " ",          # Word boundary
        ]

        for sep in separators:
            parts = text.split(sep)
            if len(parts) <= 1:
                continue

            # Merge parts into chunks that fit within token limit
            merged = self._merge_parts(parts, sep)
            if len(merged) > 1:
                # Recursively split any chunks that are still too large
                result = []
                for chunk in merged:
                    result.extend(self._recursive_split(chunk))
                return result

        # Fallback: force split by words
        words = text.split()
        chunks = []
        current = []
        current_tokens = 0

        for word in words:
            wt = count_tokens(word + " ")
            if current_tokens + wt > self.max_tokens and current:
                chunks.append(" ".join(current))
                current = []
                current_tokens = 0
            current.append(word)
            current_tokens += wt

        if current:
            chunks.append(" ".join(current))

        return chunks

    def _merge_parts(self, parts: list[str], separator: str) -> list[str]:
        """Merge split parts back together respecting token limit."""
        merged = []
        current = ""
        current_tokens = 0

        for part in parts:
            candidate = current + separator + part if current else part
            candidate_tokens = count_tokens(candidate)

            if candidate_tokens <= self.max_tokens:
                current = candidate
                current_tokens = candidate_tokens
            else:
                if current:
                    merged.append(current)
                current = part
                current_tokens = count_tokens(part)

        if current:
            merged.append(current)

        return merged

    # ── Shared helpers ───────────────────────────────────────────

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
