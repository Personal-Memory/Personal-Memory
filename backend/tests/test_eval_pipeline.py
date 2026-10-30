import unittest

from app.services.embeddings import HashingEmbedder
from evaluation.run_eval import (
    bm25_rankings, build_corpus, load_dataset, score, vector_rankings, summarize, overlap_for, run_config,
)

NOTES = [
    {"id": 1, "title": "Eggs", "text": "Crack four eggs into the pan."},
    {"id": 2, "title": "Git", "text": "Use rebase to keep history linear."},
]


class BuildCorpusTests(unittest.TestCase):
    def test_title_prefixed_and_ids_aligned(self):
        texts, ids = build_corpus(NOTES)
        self.assertEqual(ids, [1, 2])
        self.assertTrue(texts[0].startswith("Eggs\n"))

    def test_long_note_gives_multiple_chunks_same_id(self):
        long_note = {"id": 9, "title": "T", "text": "Sentence number one is here. " * 40}
        _, ids = build_corpus([long_note], max_chars=200, overlap_chars=50)
        self.assertGreater(len(ids), 1)
        self.assertEqual(set(ids), {9})


class RankingTests(unittest.TestCase):
    def test_bm25_finds_exact_term_and_empty_on_no_match(self):
        texts, ids = build_corpus(NOTES)
        out = bm25_rankings(texts, ids, ["rebase history", "zzzz qqqq"])
        self.assertEqual(out[0], [2])
        self.assertEqual(out[1], [])

    def test_vector_ranks_identical_text_first(self):
        texts, ids = build_corpus(NOTES)
        # the hashing embedder isn't semantic, but identical text must score highest
        out = vector_rankings(HashingEmbedder(), texts, ids, [texts[1]], k=2)
        self.assertEqual(out[0][0], 2)


class SmokeOnRealDataset(unittest.TestCase):
    def test_pipeline_runs_end_to_end_offline(self):
        data = load_dataset()
        texts, ids = build_corpus(data["notes"])
        queries = [q["q"] for q in data["queries"]]
        targets = [q["note"] for q in data["queries"]]
        expected_queries = len(data["queries"])
        for ranked in (
            vector_rankings(HashingEmbedder(), texts, ids, queries),
            bm25_rankings(texts, ids, queries),
        ):
            self.assertEqual(len(ranked), expected_queries)
            self.assertEqual(len(score(ranked, targets)["hits"]), expected_queries)

class SummarizeTests(unittest.TestCase):
    def test_splits_by_query_type(self):
        scores = {"hits": [1.0, 0.0, 1.0, 1.0], "rrs": [1.0, 0.0, 0.5, 1.0]}
        types = ["paraphrase", "paraphrase", "keyword", "keyword"]
        out = summarize(scores, types)
        self.assertEqual(out["all"]["n"], 4)
        self.assertEqual(out["all"]["recall"], 0.75)
        self.assertEqual(out["paraphrase"]["recall"], 0.5)
        self.assertEqual(out["keyword"]["recall"], 1.0)
        self.assertEqual(out["keyword"]["mrr"], 0.75)

    def test_ci_brackets_the_mean(self):
        scores = {"hits": [1.0] * 6 + [0.0] * 4, "rrs": [1.0] * 6 + [0.0] * 4}
        out = summarize(scores, ["keyword"] * 10)["all"]
        low, high = out["recall_ci"]
        self.assertLessEqual(low, out["recall"])
        self.assertGreaterEqual(high, out["recall"])


class RunConfigTests(unittest.TestCase):
    def test_result_is_complete_and_json_serialisable(self):
        import json
        data = load_dataset()
        result = run_config(HashingEmbedder(), data, 350, overlap_for(350))
        self.assertEqual(sum(len(v) for v in result["paired"].values()), len(data["queries"]))
        self.assertEqual(result["config"]["queries"], len(data["queries"]))
        result.pop("ranked")
        json.dumps(result)

    def test_overlap_is_capped_and_scaled(self):
        self.assertEqual(overlap_for(200), 50)
        self.assertEqual(overlap_for(350), 87)
        self.assertEqual(overlap_for(600), 100)

if __name__ == "__main__":
    unittest.main()