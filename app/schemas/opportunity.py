from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class OpportunityCreate(BaseModel):
    title: str
    organization: str
    category: str
    location: str
    description: str
    full_description: Optional[str] = None
    activities: str  # comma separated e.g "Dog walking, Feeding, Grooming"
    timing: str
    total_slots: int
    image: Optional[str] = None

class OpportunityResponse(BaseModel):
    id: int
    title: str
    organization: str
    category: str
    location: str
    description: str
    full_description: Optional[str]
    activities: str
    timing: str
    total_slots: int
    registered_count: int
    image: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True