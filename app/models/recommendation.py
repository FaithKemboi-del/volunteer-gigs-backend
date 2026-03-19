# This file defines what a Recommendation looks like in the database
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    organization_name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    website = Column(String, nullable=True)
    category = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())