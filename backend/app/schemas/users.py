from  pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username:str
    email:str
    first_name:Optional[str] = None
    last_name :Optional[str] = None
    password: str

class UserRead(BaseModel):
    id:int
    username:str
    email:str
    first_name:str
    last_name:str
