from pydantic import BaseModel, EmailStr
from datetime import datetime

# 🎓 This is what we expect when someone submits a booking
class BookingCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    location: str
    date: str
    opportunity_id: int
    opportunity_title: str
    opportunity_organization: str
    connect_with_others: bool = False
    receive_reminder: bool = False

# 🎓 This is what we send back after a booking is created
class BookingResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone: str
    location: str
    date: str
    opportunity_id: int
    opportunity_title: str
    opportunity_organization: str
    connect_with_others: bool
    receive_reminder: bool
    created_at: datetime

    class Config:
        from_attributes = True