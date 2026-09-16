from pydantic import BaseModel
from typing import Optional

class ChatMessageCreate(BaseModel):
    session_id : Optional[int] = None
    content: str
    user_role: str

class ChatMessageRead(BaseModel):
    id: int
    session_id: int
    user_role: str
    content: str

class GetAllSessionMessagesByRole(BaseModel):
    session_id:int
    user_role: str
    user_id: int

class GetAllSessionMessageByRoleRead(BaseModel):
    id:int
    content: str
    user_role : str


class GetAllSessionRead(BaseModel):
    session_id : int
    title : str




