import math
import unittest
from app.services.embeddings import EMBEDDING_DIM, HashingEmbedder

class Tests(unittest.TestCase):
    def test_size_unit_length_and_determinism(self):
        e = HashingEmbedder()
        a = e.embed_query("hello world")
        self.assertEqual(a, e.embed_query("hello world"))
        self.assertEqual(len(a), EMBEDDING_DIM)
        self.assertAlmostEqual(math.sqrt(sum(x * x for x in a)), 1.0, places=9)

    def test_provider_failure_becomes_embedding_error(self):
        from types import SimpleNamespace
        from app.services.embeddings import EmbeddingError, GeminiEmbedder
        # Mock the Gemini client to simulate a failure
        # the class FailingClient is a mock class that simulates the behavior of the Gemini client. It has a static method embed_content that raises a RuntimeError to simulate a failure in the embedding service.
        # how does it work? The FailingClient class is defined inside the test_provider_failure_becomes_embedding_error method. It has a static method embed_content that raises a RuntimeError with the message "boom". This simulates a failure in the embedding service.
        
        
        class FailingModels:
            @staticmethod
            def embed_content(**kwargs):
                raise RuntimeError("boom")

        embedder = GeminiEmbedder().__new__(GeminiEmbedder)
        embedder._client = SimpleNamespace(models=FailingModels)
        embedder._model = "x"
        embedder._types = SimpleNamespace(EmbedContentConfig=lambda **kw: kw)
        with self.assertRaises(EmbeddingError):
            embedder.embed_query("hello")
