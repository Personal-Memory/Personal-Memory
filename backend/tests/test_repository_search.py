import unittest
import uuid

from app.services.embeddings import HashingEmbedder

class SearchChunksTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            from sqlalchemy import text
            from app.core.database import SessionLocal
            cls.session = SessionLocal()
            cls.session.execute(text("SELECT 1 FROM note_chunks LIMIT 1"))
        except Exception as error:
            raise unittest.SkipTest(f"database not available: {error}")

        from app.models.note_chunks import NoteChunk
        from app.models.notes import Note
        from app.models.users import User
        from app.repositories.notes import NoteRepository

        cls.embedder = HashingEmbedder()
        cls.repo = NoteRepository(cls.session)
        suffix = uuid.uuid4().hex[:8]

        def make_user(name):
            user = User(
                username=f"{name}_{suffix}", 
                email=f"{name}_suffix@example.invalid", 
                first_name=name,
                last_name="Test",
                hashed_password="notarealpassword",
            )
            cls.session.add(user)
            cls.session.flush()
            return user

        def make_note(user, title, text):
            note = Note(
                user_id=user.id,
                title=title,
                content_text=text,
                content_json={}
            )
            cls.repo.add(note)
            cls.repo.add_chunks([NoteChunk(
                note_id=note.id,
                chunk_index=0,
                content=text,
                embedding=cls.embedder.embed_documents([text])[0])])

            return note

        cls.alice = make_user("alice")
        cls.bob = make_user("bob")
        iron = "wash the cast iron skillet and oil it to stop rust."
        cls.alice_iron = make_note(cls.alice, "Cast iron", iron)
        cls.alice_flight = make_note(cls.alice, "Lalibela", "The flight to Lalibela takes one hour.")
        cls.bob_iron = make_note(cls.bob, "Bob cast iron", iron)  # identical text, other user
        cls.session.commit()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "session"):
            cls.session.rollback()
            for user in (cls.alice, cls.bob):
                cls.session.delete(user)  # cascades to notes and chunks
            cls.session.commit()
            cls.session.close()

    def test_closest_chunk_first_and_distances_ascend(self):
        q = self.embedder.embed_query("cast iron skillet rust")
        rows = self.repo.search_chunks(self.alice.id, q, limit=5)
        self.assertEqual(rows[0].note_id, self.alice_iron.id)
        distances = [r.distance for r in rows]
        self.assertEqual(distances, sorted(distances))

    def test_user_only_sees_own_notes(self):
        q = self.embedder.embed_query("cast iron skillet rust")
        alice_ids = {r.note_id for r in self.repo.search_chunks(self.alice.id, q, limit=10)}
        bob_ids = {r.note_id for r in self.repo.search_chunks(self.bob.id, q, limit=10)}
        self.assertNotIn(self.bob_iron.id, alice_ids)
        self.assertEqual(bob_ids, {self.bob_iron.id})

    def test_limit_is_respected(self):
        q = self.embedder.embed_query("anything")
        self.assertEqual(len(self.repo.search_chunks(self.alice.id, q, limit=1)), 1)


if __name__ == "__main__":
    unittest.main()