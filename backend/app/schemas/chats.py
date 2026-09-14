from pydantic import BaseModel
from typing import Optional

class ChatMessageCreate(BaseModel):
    session_id : Optional[int] =None
    content: str
    user_role: str

class ChatMessageRead(BaseModel):
    id: int
    session_id: int
    user_role: str
    content: str

class GetAllMessagesByRole(BaseModel):
    session_id:int
    user_role: str


