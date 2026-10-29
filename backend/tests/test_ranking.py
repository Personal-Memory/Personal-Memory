import unittest
from app.services.ranking import Hit, top_notes


class Tests(unittest.TestCase):

    def hit(self, note_id, chunk_index, score):
        return Hit(note_id=note_id, chunk_index=chunk_index, content="text", score=score)

    def test_best_chunk_per_note_then_top_k(self):
        hits = [self.hit(1, 0, 0.5), self.hit(1, 1, 0.9), self.hit(2, 0, 0.8), self.hit(3, 0, 0.7)]
        ranked = top_notes(hits, 2)
        self.assertEqual([(h.note_id, h.chunk_index) for h in ranked], [(1, 1), (2, 0)])

    def test_ties_are_deterministic(self):
        hits = [self.hit(2, 0, 0.5), self.hit(1, 0, 0.5)]
        self.assertEqual([h.note_id for h in top_notes(hits, 5)], [1, 2])

    def test_empty(self):
        self.assertEqual(top_notes([], 5), [])