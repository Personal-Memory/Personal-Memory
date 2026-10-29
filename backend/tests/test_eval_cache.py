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


def test_cache_hits_skip_inner(tmp_path):
    spy = SpyEmbedder()
    c = CachedEmbedder(spy, tmp_path / "c.json", "ns")
    first = c.embed_documents(["aa", "bbb"])
    second = c.embed_documents(["aa", "bbb"])
    assert first == second
    assert len(spy.doc_calls) == 1
    assert c.new_texts == 2


def test_cache_persists_across_instances(tmp_path):
    spy = SpyEmbedder()
    CachedEmbedder(spy, tmp_path / "c.json", "ns").embed_documents(["aa"])
    spy2 = SpyEmbedder()
    c2 = CachedEmbedder(spy2, tmp_path / "c.json", "ns")
    c2.embed_documents(["aa"])
    assert spy2.doc_calls == []
    assert c2.new_texts == 0


def test_doc_and_query_are_separate_keys(tmp_path):
    spy = SpyEmbedder()
    c = CachedEmbedder(spy, tmp_path / "c.json", "ns")
    d = c.embed_documents(["same"])[0]
    q = c.embed_queries(["same"])[0]
    assert d != q  # spy returns different vectors per kind


def test_namespace_isolates(tmp_path):
    spy = SpyEmbedder()
    CachedEmbedder(spy, tmp_path / "c.json", "model-a").embed_documents(["x"])
    c = CachedEmbedder(spy, tmp_path / "c.json", "model-b")
    c.embed_documents(["x"])
    assert c.new_texts == 1


def test_duplicates_embedded_once(tmp_path):
    spy = SpyEmbedder()
    c = CachedEmbedder(spy, tmp_path / "c.json", "ns")
    out = c.embed_documents(["a", "a", "a"])
    assert len(out) == 3
    assert spy.doc_calls == [["a"]]