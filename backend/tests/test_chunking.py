import unittest
from app.services.chunking import chunk_text, extract_text

def para(*texts):
    return {"type": "paragraph", "content": [{"type" : "text", "text": t} for t in texts]}

class Tests(unittest.TestCase):
    def test_marks_do_not_split_words(self):
        self.assertEqual(extract_text({"type": "doc", "content": [para("un", "believable")]}), "unbelievable")

    def test_blocks_become_lines(self):
        doc = {"type": "doc", "content": [para("First."), para("Second.")]}
        self.assertEqual(extract_text(doc), "First.\nSecond.")

    def test_empty(self):
        self.assertEqual(chunk_text(""), [])

    def test_short_text_is_one_chunk(self):
        self.assertEqual(chunk_text("Hello. World."), ["Hello. World."])

    def test_size_limit_and_no_lost_sentences(self):
        sentences = [f"Sentence number {i} is here." for i in range(40)]
        chunks = chunk_text(" ".join(sentences), max_chars=200, overlap_chars=50)
        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(len(c) <= 200 for c in chunks))
        for s in sentences:
            self.assertIn(s, " ".join(chunks))

    def test_overlap_repeats_last_sentence(self):
        sentences = [f"Sentence number {i} is here." for i in range(20)]
        chunks = chunk_text(" ".join(sentences), max_chars=120, overlap_chars=40)
        for a, b in zip(chunks, chunks[1:]):
            self.assertIn(a.split(". ")[-1].rstrip("."), b)
            # the above line checks that the last sentence of chunk a is in chunk b, allowing for the period to be stripped
    