"""Configuration management for MemoTrail."""

import os
from pathlib import Path
from dataclasses import dataclass, field


def _default_data_dir() -> Path:
    """Return platform-appropriate data directory."""
    xdg = os.environ.get("XDG_DATA_HOME")
    if xdg:
        return Path(xdg) / "memotrail"
    return Path.home() / ".memotrail"


@dataclass
class Config:
    """MemoTrail configuration."""

    # Storage paths
    data_dir: Path = field(default_factory=_default_data_dir)

    # Embedding model
    embedding_model: str = "all-MiniLM-L6-v2"

    # Chunking settings
    chunk_max_tokens: int = 512
    chunk_overlap_tokens: int = 64

    # Search settings
    search_default_limit: int = 10
    search_max_limit: int = 50

    # Context packing budget (tokens)
    context_budget_total: int = 32_000
    context_budget_system: int = 2_000
    context_budget_decisions: int = 2_000
    context_budget_retrieved: int = 8_000
    context_budget_recent: int = 4_000

    # Consolidation settings
    consolidation_noop_threshold: float = 0.92
    consolidation_update_threshold: float = 0.78

    # Reranker settings
    reranker_enabled: bool = False
    reranker_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    reranker_candidate_multiplier: int = 3

    # Claude Code collector
    claude_code_log_dir: Path = field(
        default_factory=lambda: Path.home() / ".claude" / "projects"
    )

    @property
    def chroma_dir(self) -> Path:
        return self.data_dir / "chroma"

    @property
    def sqlite_path(self) -> Path:
        return self.data_dir / "memotrail.db"

    def ensure_dirs(self) -> None:
        """Create necessary directories."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.chroma_dir.mkdir(parents=True, exist_ok=True)


# Global config instance
config = Config()
