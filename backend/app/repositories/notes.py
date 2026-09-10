from sqlalchemy.orm import Session

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

    def commit(self) -> None:
        self.session.commit()