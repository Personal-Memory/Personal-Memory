from  pydantic import BaseModel,model_validator
from typing import Optional

class UserCreate(BaseModel):
    username:str
    email:str
    first_name:str
    last_name:str
    password:str

class UserRead(BaseModel):
    id:int
    username:str
    email:str
    first_name:str
    last_name:str

    model_config = {
        "from_attributes": True
    }
class UserLogin(BaseModel):
    username:Optional[str] = None
    email:Optional[str] = None
    password: str

    @model_validator(mode="after")
    def check_username_or_email(self):
        if not self.username and not self.email:
            raise ValueError("Either username or email must be provided") 
        return self

class Token(BaseModel):
    access_token:str
    token_type:str


