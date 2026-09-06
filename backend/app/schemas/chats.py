from pydantic import BaseModel
from typing import Optional

class ChatSessionCreate(BaseModel):
    title: Optional[str] = None

class ChatMessageCreate(BaseModel):
    session_id = Optional[int] =None
    content: str
    user_role: str

class ChatSessionRead(BaseModel):
    id: int
    user_id: int
    title: str


class ChatMessageRead(BaseModel):
    id: int
    session_id: int
    user_role: str
    content: str


