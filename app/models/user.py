from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String)
    nomber = Column(String)
    
    hashed_password = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
