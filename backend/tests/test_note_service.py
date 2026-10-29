import unittest
import uuid

from app.services.embeddings import HashingEmbedder


def doc(*paragraphs):
    return {"type": "doc", "content": [
        {"type": "paragraph", "content": [{"type": "text", "text": p}]} for p in paragraphs]}


class NoteServiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            from sqlalchemy import text
            from app.core.database import SessionLocal
            cls.session = SessionLocal()
            cls.session.execute(text("SELECT 1 FROM note_chunks LIMIT 1"))
        except Exception as error:
            raise unittest.SkipTest(f"database not available: {error}")

        from app.models.users import User
        from app.repositories.notes import NoteRepository
        from app.schemas.notes import NoteCreate
        from app.services.notes import NoteService

        cls.NoteCreate = NoteCreate
        cls.service = NoteService(NoteRepository(cls.session), HashingEmbedder())
        suffix = uuid.uuid4().hex[:8]
        cls.users = []
        for name in ("alice", "bob"):
            user = User(username=f"{name}_{suffix}", email=f"{name}_{suffix}@example.invalid",
                        first_name=name, last_name="Test", hashed_password="x")
            cls.session.add(user)
            cls.users.append(user)
        cls.session.commit()
        cls.alice, cls.bob = cls.users

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "session"):
            cls.session.rollback()
            for user in cls.users:
                cls.session.delete(user)
            cls.session.commit()
            cls.session.close()

    def create(self, user, title, *paragraphs):
        return self.service.create_note(self.NoteCreate(title=title, content_json=doc(*paragraphs)), user)

    def test_search_finds_the_right_note_and_scores_it(self):
        iron = self.create(self.alice, "Cast iron", "Wash the skillet and oil it to stop rust.")
        self.create(self.alice, "Flights", "The flight to Lalibela takes one hour.")
        hits = self.service.search("skillet rust oil", self.alice, limit=5)
        self.assertEqual(hits[0].note_id, iron.id)
        self.assertGreater(hits[0].score, hits[-1].score if len(hits) > 1 else -1)

    def test_one_result_per_note(self):
        long_text = " ".join(f"Sentence {i} about cast iron skillets and rust." for i in range(60))
        note = self.create(self.alice, "Long note", long_text)
        hits = self.service.search("cast iron skillets rust", self.alice, limit=5)
        self.assertEqual([h.note_id for h in hits].count(note.id), 1)

    def test_users_are_isolated(self):
        bob_note = self.create(self.bob, "Bob private", "Bob's secret zebra recipe.")
        alice_ids = {h.note_id for h in self.service.search("zebra recipe", self.alice, limit=10)}
        self.assertNotIn(bob_note.id, alice_ids)

    def test_empty_query_is_rejected(self):
        with self.assertRaises(ValueError):
            self.service.search("   ", self.alice)

    def test_note_without_body_creates_no_chunks(self):
        from sqlalchemy import func, select
        from app.models.note_chunks import NoteChunk
        note = self.create(self.alice, "Empty", "")
        count = self.session.execute(
            select(func.count()).select_from(NoteChunk).where(NoteChunk.note_id == note.id)
        ).scalar_one()
        self.assertEqual(count, 0)


if __name__ == "__main__":
    unittest.main()