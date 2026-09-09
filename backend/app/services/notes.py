from typing import Any

from app.models.notes import Note
from app.models.users import User
from app.repositories.notes import NoteRepository
from app.schemas.notes import NoteCreate

class NoteService:

    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository

    def create_note(
            self, 
            data: NoteCreate,
            user: User,
    ) -> Note:
        note = Note(
            user_id = user.id,
            title = data.title,
            content_json = data.content_json,
            content_text = self._extract_text(data.content_json),
        )

        created_note = self.note_repository.add(note)
        self.note_repository.commit()

        return created_note

    def _extract_text(self, document: Any) -> str:
        text_parts: list[str] = []

        def walk(node: dict[str, Any]) -> None:
            if node.get("type") == "text":
                text_parts.append(node.get("text", ""))

            for child in node.get("content", []):
                walk(child)

        walk(document)

        return " ".join(text_parts)

    def get_notes(self, user: User) -> list[Note]:
        return self.note_repository.get_notes_by_user(user.id)

    def get_note(self, note_id: int, user: User) -> Note:
        note = self.note_repository.get_note_by_id(note_id)

        if note is None or note.user_id != user.id:
            raise ValueError("Note not found or access denied.")

        return note