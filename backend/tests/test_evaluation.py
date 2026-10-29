import json
import unittest
from pathlib import Path

from evaluation.bm25 import BM25, tokenize
from evaluation.metrics import bootstrap_ci, hit_at_k, mean, reciprocal_rank

DATASET = json.loads(
    (Path(__file__).parent.parent / "evaluation" / "dataset.json").read_text(encoding="utf-8")
)
class MetricsTests(unittest.TestCase):
    def test_hit_and_rr(self):
        self.assertEqual(hit_at_k([3, 1, 2], 1, 5), 1)
        self.assertEqual(hit_at_k([3, 1, 2], 1, 1), 0)
        self.assertEqual(reciprocal_rank([3, 1, 2], 1, 5), 0.5)
        self.assertEqual(reciprocal_rank([3, 1, 2], 9, 5), 0.0)

    def test_ci_is_reproducible_and_brackets_the_mean(self):
        values = [1] * 60 + [0] * 40
        low, high = bootstrap_ci(values)
        self.assertLess(low, mean(values))
        self.assertGreater(high, mean(values))
        self.assertEqual(bootstrap_ci(values), bootstrap_ci(values))

class BM25Tests(unittest.TestCase):
    def test_exact_terms_rank_first(self):
        docs = ["cast iron skillet seasoning", "tomato eggs shakshuka", "git rebase and merge"]
        scores = BM25(docs).scores("shakshuka eggs")
        self.assertEqual(max(range(3), key=lambda i: scores[i]), 1)

    def test_no_overlap_scores_zero(self):
        self.assertEqual(BM25(["alpha beta"]).scores("gamma"), [0.0])

    def test_stopwords_removed(self):
        self.assertEqual(tokenize("The cat is on the mat"), ["cat", "mat"])

class DatasetTests(unittest.TestCase):
    def test_enough_queries_and_valid_labels(self):
        note_ids = {n["id"] for n in DATASET["notes"]}
        self.assertGreaterEqual(len(DATASET["queries"]), 100)
        for q in DATASET["queries"]:
            self.assertIn(q["note"], note_ids)
            self.assertIn(q["type"], {"paraphrase", "keyword"})

    def test_every_note_has_both_query_types(self):
        for note in DATASET["notes"]:
            types = {q["type"] for q in DATASET["queries"] if q["note"] == note["id"]}
            self.assertEqual(types, {"paraphrase", "keyword"}, note["title"])