import unittest

from evaluation.run_eval import paired, ranked_note_ids, score


class RankedNoteIdsTests(unittest.TestCase):
    def test_best_chunk_per_note_wins(self):
        self.assertEqual(ranked_note_ids([0.9, 0.8, 0.5, 0.95], [1, 1, 2, 3], k=3), [3, 1, 2])

    def test_note_appears_once(self):
        self.assertEqual(ranked_note_ids([0.9, 0.8, 0.7], [1, 1, 1], k=5), [1])

    def test_k_limits_results(self):
        self.assertEqual(ranked_note_ids([3, 2, 1], [1, 2, 3], k=2), [1, 2])

    def test_min_score_drops_zero_chunks(self):
        self.assertEqual(ranked_note_ids([0.0, 0.0], [1, 2], k=5, min_score=0.0), [])

    def test_negative_cosine_kept_when_no_min_score(self):
        self.assertEqual(ranked_note_ids([-0.1, -0.5], [1, 2], k=5), [1, 2])

    def test_ties_break_by_note_id(self):
        self.assertEqual(ranked_note_ids([0.5, 0.5], [7, 3], k=5), [3, 7])


class ScoreTests(unittest.TestCase):
    def test_hit_and_rr(self):
        s = score([[1, 2], [8, 9], [5, 4]], [1, 2, 4], k=2)
        self.assertEqual(s["hits"], [1.0, 0.0, 1.0])
        self.assertEqual(s["rrs"], [1.0, 0.0, 0.5])

    def test_empty_ranking_scores_zero(self):
        s = score([[]], [1], k=5)
        self.assertEqual((s["hits"], s["rrs"]), ([0.0], [0.0]))


class PairedTests(unittest.TestCase):
    def test_buckets(self):
        out = paired([1, 1, 0, 0], [1, 0, 1, 0])
        self.assertEqual(
            out, {"both": [0], "vector_only": [1], "bm25_only": [2], "neither": [3]}
        )


if __name__ == "__main__":
    unittest.main()