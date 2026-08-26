
from sqlalchemy.orm import Mapped,mapped_column
from Personal_Memory.backend.app.models.base import BaseModel

class User(BaseModel):
    __tablename__ = 'users'
    username:  Mapped[str] = mapped_column(unique=True,index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    first_name: Mapped[str] 
    last_name: Mapped[str]
    hashed_password: Mapped[str]
    


