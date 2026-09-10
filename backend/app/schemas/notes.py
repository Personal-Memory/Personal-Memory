from datetime import datetime
from typing import Any

from pydantic import BaseModel

class NoteCreate(BaseModel):
    title: str
    content_json: dict[str, Any]

class NoteRead(BaseModel):
    id: int
    user_id: int
    title: str
    content_json: dict[str, Any]
    content_text: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes" : True
    } 

class NoteListRead(BaseModel):
    id: int
    title: str
    content_text: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes" : True
    }