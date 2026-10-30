# tests/test_eval_cache.py
import tempfile
import unittest
from pathlib import Path

from evaluation.cache import CachedEmbedder


class SpyEmbedder:
    def __init__(self):
        self.doc_calls = []
        self.query_calls = []

    def embed_documents(self, texts):
        self.doc_calls.append(list(texts))
        return [[float(len(t)), 1.0] for t in texts]

    def embed_queries(self, texts):
        self.query_calls.append(list(texts))
        return [[float(len(t)), 2.0] for t in texts]


class CachedEmbedderTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.path = Path(tmp.name) / "c.json"

    def test_cache_hits_skip_inner(self):
        spy = SpyEmbedder()
        c = CachedEmbedder(spy, self.path, "ns")
        first = c.embed_documents(["aa", "bbb"])
        second = c.embed_documents(["aa", "bbb"])
        self.assertEqual(first, second)
        self.assertEqual(len(spy.doc_calls), 1)
        self.assertEqual(c.new_texts, 2)

    def test_cache_persists_across_instances(self):
        CachedEmbedder(SpyEmbedder(), self.path, "ns").embed_documents(["aa"])
        spy2 = SpyEmbedder()
        c2 = CachedEmbedder(spy2, self.path, "ns")
        c2.embed_documents(["aa"])
        self.assertEqual(spy2.doc_calls, [])
        self.assertEqual(c2.new_texts, 0)

    def test_doc_and_query_are_separate_keys(self):
        c = CachedEmbedder(SpyEmbedder(), self.path, "ns")
        self.assertNotEqual(c.embed_documents(["same"])[0], c.embed_queries(["same"])[0])

    def test_namespace_isolates(self):
        spy = SpyEmbedder()
        CachedEmbedder(spy, self.path, "model-a").embed_documents(["x"])
        c = CachedEmbedder(spy, self.path, "model-b")
        c.embed_documents(["x"])
        self.assertEqual(c.new_texts, 1)

    def test_duplicates_embedded_once(self):
        spy = SpyEmbedder()
        c = CachedEmbedder(spy, self.path, "ns")
        out = c.embed_documents(["a", "a", "a"])
        self.assertEqual(len(out), 3)
        self.assertEqual(spy.doc_calls, [["a"]])


if __name__ == "__main__":
    unittest.main()