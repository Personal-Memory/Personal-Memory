from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector

from app.models.base import BaseModel

class NoteChunk(BaseModel):
    __tablename__ = "note_chunks"

    note_id: Mapped[int] = mapped_column(
        ForeignKey("notes.id", ondelete="CASCADE"), 
        index=True, 
        nullable=False
    )

    chunk_index: Mapped[int] = mapped_column(
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    embedding: Mapped[list[float]] = mapped_column(
        Vector(768),
        nullable=False,
    )
