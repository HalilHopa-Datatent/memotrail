"""Embedder: generates vector embeddings using sentence-transformers."""

from memotrail.utils import config, get_logger

logger = get_logger("memotrail.core.embedder")

_model = None


def _load_model():
    """Lazy-load the embedding model."""
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        logger.info(f"Loading embedding model: {config.embedding_model}")
        _model = SentenceTransformer(config.embedding_model)
        logger.info("Embedding model loaded.")
    return _model


class Embedder:
    """Generate embeddings for text chunks."""

    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or config.embedding_model

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a list of texts.

        Args:
            texts: List of text strings to embed

        Returns:
            List of embedding vectors
        """
        if not texts:
            return []

        model = _load_model()
        embeddings = model.encode(texts, show_progress_bar=False, normalize_embeddings=True)
        return embeddings.tolist()

    def embed_single(self, text: str) -> list[float]:
        """Generate embedding for a single text."""
        results = self.embed([text])
        return results[0] if results else []
