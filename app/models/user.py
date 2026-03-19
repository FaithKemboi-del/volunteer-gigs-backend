# This file defines what a User looks like in the database
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    # 🎓 __tablename__ is the actual table name in PostgreSQL
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    # 🎓 We never store plain passwords - always store hashed version!
    hashed_password = Column(String, nullable=False)
    # 🎓 func.now() automatically sets current time when record is created
    created_at = Column(DateTime(timezone=True), server_default=func.now())