from app.core.database import Base
from sqlalchemy.orm import Mapped,mapped_column
from datetime import datetime

class BaseModel(Base):
    __abstract__ =True
    id :Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at :Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
   


