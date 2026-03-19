from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# 🎓 This is what we expect when someone submits a recommendation
class RecommendationCreate(BaseModel):
    organization_name: str
    location: str
    website: Optional[str] = None  # Optional means it can be empty
    category: str
    description: str

# 🎓 This is what we send back after a recommendation is created
class RecommendationResponse(BaseModel):
    id: int
    organization_name: str
    location: str
    website: Optional[str]
    category: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True