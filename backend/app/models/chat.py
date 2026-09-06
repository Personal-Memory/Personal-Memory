from app.models.base import BaseModel
from app.models.users import User
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import ForeignKey

class ChatSession(BaseModel):
    __tablename__= "chat_sessions"
    title:Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

class ChatMessage(BaseModel):
    __tablename__= "chat_messages"
    session_id: Mapped[int] = mapped_column(ForeignKey("chat_sessions.id"))
    user_role: Mapped[str]
    content : Mapped[str]