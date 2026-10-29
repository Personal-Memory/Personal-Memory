import hashlib
import json
import os
import tempfile
from pathlib import Path


# this class wraps an Embedder and caches the results in a JSON file on disk. It uses a SHA256 hash of the text and the kind of embedding (document or query) to create a unique key for each embedding. It is useful for testing and development, but should not be used in production as it does not handle cache invalidation or concurrency.

class CachedEmbedder:
    # the constructor takes an inner Embedder, a path to a cache file, a namespace for the cache, and an optional batch size for embedding requests. It loads the cache from the file if it exists, and saves it back to the file after each batch of new embeddings.
    # each parameter explained:
    # inner: the Embedder to wrap and cache results from
    # cache_path: the path to the cache file
    # namespace: a string to namespace the cache keys. An example would be "myapp-v1" to avoid collisions with other apps or versions.
    # batch_size: the number of texts to embed in each batch
    def __init__(self, inner, cache_path, namespace, batch_size=50):
        self.inner = inner
        self.path = Path(cache_path)
        self.namespace = namespace
        self.batch_size = batch_size
        self.new_texts = 0
        self._store: dict[str, list[float]] = {}
        if self.path.exists():
            self._store = json.loads(self.path.read_text(encoding="utf-8"))

    # this method generates a unique key for each embedding based on the namespace, kind, and text. It uses SHA256 hashing to create a fixed-length string that can be used as a dictionary key. The kind parameter is either "doc" for document embeddings or "query" for query embeddings. The text parameter is the actual text to be embedded.
    def _key(self, kind: str, text: str) -> str:
        raw = f"{self.namespace}|{kind}|{text}".encode("utf-8")
        return hashlib.sha256(raw).hexdigest()

    # this method saves the cache to the file.
    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=self.path.parent, suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(self._store, f)
        os.replace(tmp, self.path)  # atomic swap

    def _embed(self, kind: str, texts: list[str], embed_fn) -> list[list[float]]:
        keys = [self._key(kind, t) for t in texts]
        missing: dict[str, str] = {}  # dict dedupes repeated texts
        for key, text in zip(keys, texts):
            if key not in self._store and key not in missing:
                missing[key] = text

        items = list(missing.items())
        for i in range(0, len(items), self.batch_size):
            batch = items[i : i + self.batch_size]
            vectors = embed_fn([text for _, text in batch])
            for (key, _), vec in zip(batch, vectors):
                self._store[key] = [float(x) for x in vec]
            self.new_texts += len(batch)
            self._save()

        return [self._store[k] for k in keys]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self._embed("doc", texts, self.inner.embed_documents)

    def embed_queries(self, texts: list[str]) -> list[list[float]]:
        return self._embed("query", texts, self.inner.embed_queries)