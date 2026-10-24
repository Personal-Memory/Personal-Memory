from sqlalchemy.orm import Session
from sqlalchemy import delete, select
from app.models.note_chunks import NoteChunk

from app.models.notes import Note

class NoteRepository:

    def __init__(self, session: Session):
        self.session = session

    def add(self, note: Note) -> Note:
        self.session.add(note)
        self.session.flush()

        return note

    def get_notes_by_user(self, user_id: int) -> list[Note]:
        return self.session.query(Note).filter(Note.user_id == user_id).order_by(Note.updated_at.desc()).all()

    def get_note_by_id(self, note_id: int) -> Note | None:
        return self.session.query(Note).filter(Note.id == note_id).first()

    def add_chunks(self, chunks: list[NoteChunk]) -> None:
        self.session.add_all(chunks)
        self.session.flush()

    def delete_chunks(self, note_id: int) -> None:
        self.session.execute(delete(NoteChunk).where(NoteChunk.note_id == note_id))

    def search_chunks(self, user_id: int, query_embedding: list[float], limit: int):
        distance = NoteChunk.embedding.cosine_distance(query_embedding).label("distance")
        statement = (
            select(
                NoteChunk.note_id,
                NoteChunk.chunk_index,
                NoteChunk.content,
                Note.title,
                distance,
            )
            .join(Note, Note.id == NoteChunk.note_id)
            .where(Note.user_id == user_id)
            .order_by(distance)
            .limit(limit)
        )
        return self.session.execute(statement).all()

    def commit(self) -> None:
        self.session.commit()