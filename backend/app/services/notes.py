from app.models.note_chunks import NoteChunk
from app.models.notes import Note
from app.models.users import User
from app.repositories.notes import NoteRepository
from app.schemas.notes import NoteCreate
from app.services.chunking import chunk_index_text, chunk_text, extract_text
from app.services.embeddings import Embedder
from app.services.ranking import Hit, top_notes

# Fetch more chunks than requested: several chunks of one note can crowd the top
# of the list, and grouping per note happens afterwards.

# the above comment is explaining why we are fetching more chunks than the limit specified in the search function. The reason is that if a single note has multiple chunks that are highly relevant to the query, they could dominate the top results. By fetching more chunks than requested, we can ensure that we have a better chance of getting a diverse set of notes in the final results after grouping by note.
CHUNK_OVERFETCH = 4


class NoteService:

    def __init__(self, note_repository: NoteRepository, embedder: Embedder):
        self.note_repository = note_repository
        self.embedder = embedder

    def create_note(self, data: NoteCreate, user: User) -> Note:
        note = Note(
            user_id=user.id,
            title=data.title,
            content_json=data.content_json,
            content_text=extract_text(data.content_json),
        )

        # Embed BEFORE writing to the database, so an embedding failure leaves nothing behind.
        chunks = chunk_text(note.content_text)
        vectors = self.embedder.embed_documents(
            [chunk_index_text(note.title, chunk) for chunk in chunks]
        )

        created_note = self.note_repository.add(note)
        self.note_repository.add_chunks(
            [
                NoteChunk(note_id=created_note.id, chunk_index=index, content=chunk, embedding=vector)
                for index, (chunk, vector) in enumerate(zip(chunks, vectors))
            ]
        )
        self.note_repository.commit()
        return created_note

    # the usage of chunk overfetch comes here.
    # we fetch more chunks than requested to ensure that we have a better chance of getting a diverse set of notes in the final results after grouping by note.
    # after search chunks is called with the overfetch limit, we then call top_notes to group the hits by note and return the top k notes based on their best chunk's score.
    
    def search(self, query: str, user: User, limit: int = 5) -> list[Hit]:
        query = query.strip()
        if not query:
            raise ValueError("Query must not be empty.")

        query_vector = self.embedder.embed_query(query)
        rows = self.note_repository.search_chunks(user.id, query_vector, limit * CHUNK_OVERFETCH)
        hits = [
            Hit(
                note_id=row.note_id,
                chunk_index=row.chunk_index,
                content=row.content,
                score=1.0 - float(row.distance),   # distance -> similarity
                title=row.title,
            )
            for row in rows
        ]
        return top_notes(hits, limit)

    def get_notes(self, user: User) -> list[Note]:
        return self.note_repository.get_notes_by_user(user.id)

    def get_note(self, note_id: int, user: User) -> Note:
        note = self.note_repository.get_note_by_id(note_id)

        if note is None or note.user_id != user.id:
            raise ValueError("Note not found or access denied.")

        return note