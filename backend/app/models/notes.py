from typing import Any

from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB

from app.models.base import BaseModel

class Note(BaseModel):
    __tablename__ = 'notes'
    title: Mapped[str] = mapped_column(index=True, nullable=False)
    content_text: Mapped[str] = mapped_column(Text, nullable=False,)
    content_json: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        index=True,
        nullable=False,
    )

