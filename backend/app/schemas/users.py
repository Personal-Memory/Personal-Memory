from  pydantic import BaseModel,model_validator,Field, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username:str = Field(
        min_length = 3,
        max_length = 30,
        pattern = r"^[a-zA-Z0-9_]+$"
    )
    email:EmailStr
    first_name:str = Field(min_length=1)
    last_name:str = Field(min_length=1)
    password:str = Field(min_length=8)


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


