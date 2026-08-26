from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NoteCreate(BaseModel):
    title:str
    content:str

class NoteRead(BaseModel):
    id:int
    title:str
    content:str
    owner_id:int
    created_at:datetime
    updated_at:datetime

    model_config = {"from_attributes": True}

class NoteUpdate(BaseModel):
    title:Optional[str] = None
    content:Optional[str] = None