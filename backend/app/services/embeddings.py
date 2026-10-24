import hashlib
import math
import os
import re
from functools import lru_cache
from typing import Protocol
import logging

logger = logging.getLogger(__name__)

EMBEDDING_DIM = 768
DEFAULT_GEMINI_MODEL = "gemini-embedding-001"
BATCH_SIZE = 50

def _normalize(vector: list[float]) -> list[float]:
    norm = math.sqrt(sum(x * x for x in vector))
    return [x / norm for x in vector] if norm else vector


class Embedder(Protocol):
    dim: int
    def embed_documents(self, texts: list[str]) -> list[list[float]]: ...
    def embed_query(self, text: str) -> list[float]: ...

class EmbeddingError(RuntimeError):
    """The embedding provider failed (network, quota, bad key)."""

class GeminiEmbedder:
    dim = EMBEDDING_DIM
    # the above is a class attribute, not an instance attribute, so it can be accessed without instantiating the class
    # This is useful for the database schema, which needs to know the dimension of the embedding vector without having to create an instance of the embedder.

    def __init__(self, model: str = DEFAULT_GEMINI_MODEL, api_key: str | None = None):
        from google import genai
        from google.genai import types

        self._types = types
        self._client = genai.Client(api_key=api_key)
        self._model = model

    def _embed(self, texts: list[str], task_type: str) -> list[list[float]]:
        vectors: list[list[float]] = []
        for start in range(0, len(texts), BATCH_SIZE):
            try:
                result = self._client.models.embed_content(
                    model=self._model,
                    contents=texts[start:start + BATCH_SIZE],
                    config=self._types.EmbedContentConfig(
                        task_type=task_type,
                        output_dimensionality=EMBEDDING_DIM,
                    ),
                )
            except Exception as error:
                logger.exception("Gemini embedding request failed")
                raise EmbeddingError("The embedding service request failed") from error
            
            vectors.extend(_normalize(list(e.values)) for e in result.embeddings)

        if len(vectors) != len(texts) or any(len(v) != EMBEDDING_DIM for v in vectors):
            raise RuntimeError("Embedding response does not match the requested size")
        return vectors

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self._embed(texts, "RETRIEVAL_DOCUMENT")

    def embed_query(self, text: str) -> list[float]:
        return self._embed([text], "RETRIEVAL_QUERY")[0]


# below is a fake embedder for testing purposes. It is deterministic, but not semantic. It should never be used in production.
# It is useful for testing the chunking and embedding pipeline without relying on an external API or model.
class HashingEmbedder:
    """Deterministic fake for tests. NOT semantic. Never report its numbers."""
    dim = EMBEDDING_DIM

    def _embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dim
        for token in re.findall(r"\w+", text.lower()):
            digest = hashlib.md5(token.encode()).digest()
            vector[int.from_bytes(digest[:4], "big") % self.dim] += 1.0 if digest[4] % 2 == 0 else -1.0
        return _normalize(vector)

    def embed_documents(self, texts): return [self._embed(t) for t in texts]
    def embed_query(self, text): return self._embed(text)


@lru_cache(maxsize=1)
def get_embedder() -> Embedder:
    backend = os.getenv("EMBEDDING_BACKEND", "gemini").lower()
    if backend == "hashing":
        return HashingEmbedder()
    if backend == "gemini":
        return GeminiEmbedder(model=os.getenv("EMBEDDING_MODEL", DEFAULT_GEMINI_MODEL))
    raise ValueError(f"Unknown EMBEDDING_BACKEND: {backend!r}")