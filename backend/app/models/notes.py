from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped,mapped_column
from Personal_Memory.backend.app.models.base import BaseModel

class Note(BaseModel):
    __tablename__ = 'notes'
    title: Mapped[str] 
    content : Mapped[str]
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id') )