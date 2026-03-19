# This file defines what a Booking looks like in the database
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    location = Column(String, nullable=False)
    date = Column(String, nullable=False)
    opportunity_id = Column(Integer, nullable=False)
    opportunity_title = Column(String, nullable=False)
    opportunity_organization = Column(String, nullable=False)
    # 🎓 Boolean fields for the checkboxes
    connect_with_others = Column(Boolean, default=False)
    receive_reminder = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())