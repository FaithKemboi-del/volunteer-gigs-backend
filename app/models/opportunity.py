from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    organization = Column(String, nullable=False)
    category = Column(String, nullable=False)
    location = Column(String, nullable=False)
    description = Column(String, nullable=False)
    full_description = Column(String, nullable=True)
    activities = Column(String, nullable=False)  # stored as comma separated
    timing = Column(String, nullable=False)
    total_slots = Column(Integer, nullable=False)
    registered_count = Column(Integer, default=0)
    image = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())