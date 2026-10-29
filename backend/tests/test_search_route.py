import unittest

from fastapi import HTTPException

from app.api.notes import search_notes
from app.services.embeddings import EmbeddingError
from app.services.ranking import Hit

class FakeService:
    def __init__(self, error=None, result=None):
        self.error, self.result = error, result or []

    def search(self, query, user, limit):
        if self.error:
            raise self.error
        return self.result

    class Tests(unittest.TestCase):
        
        def call(self, service):
            return search_notes(
                q="cast iron", 
                limit=5, 
                current_user=object(), 
                note_service=service,
            )

        def test_blank_query_becomes_422(self):
            with self.assertRaises(HTTPException) as ctx:
                self.call(FakeService(error=ValueError("Query must not be empty.")))
            self.assertEqual(ctx.exception.status_code, 422)

        def test_embedding_failure_becomes_503(self):
            with self.assertRaises(HTTPException) as ctx:
                self.call(FakeService(error=EmbeddingError("down")))
            self.assertEqual(ctx.exception.status_code, 503)

        def test_results_pass_through(self):
            hit = Hit(note_id=1, chunk_index=0, content="x", score=0.9, title="T")
            self.assertEqual(self.call(FakeService(result=[hit])), [hit])

