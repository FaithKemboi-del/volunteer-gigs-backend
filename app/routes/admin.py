from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.booking import Booking
from app.models.recommendation import Recommendation
from app.schemas.booking import BookingResponse
from app.schemas.recommendation import RecommendationResponse
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter(prefix="/admin", tags=["admin"])

class AdminLogin(BaseModel):
    email: str
    password: str

class AdminToken(BaseModel):
    access_token: str
    token_type: str

@router.post("/login", response_model=AdminToken)
def admin_login(credentials: AdminLogin):
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")
    
    if credentials.email != admin_email or credentials.password != admin_password:
        raise HTTPException(status_code=401, detail="Invalid admin credentials")
    
    return {"access_token": "admin-token-volunteer-gigs", "token_type": "bearer"}

@router.get("/bookings", response_model=List[BookingResponse])
def get_all_bookings(token: str, db: Session = Depends(get_db)):
    if token != "admin-token-volunteer-gigs":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return db.query(Booking).order_by(Booking.created_at.desc()).all()

@router.get("/recommendations", response_model=List[RecommendationResponse])
def get_all_recommendations(token: str, db: Session = Depends(get_db)):
    if token != "admin-token-volunteer-gigs":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return db.query(Recommendation).order_by(Recommendation.created_at.desc()).all()

@router.get("/stats")
def get_stats(token: str, db: Session = Depends(get_db)):
    if token != "admin-token-volunteer-gigs":
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    total_bookings = db.query(Booking).count()
    total_recommendations = db.query(Recommendation).count()
    reminders_requested = db.query(Booking).filter(Booking.receive_reminder == True).count()
    connect_requested = db.query(Booking).filter(Booking.connect_with_others == True).count()

    return {
        "total_bookings": total_bookings,
        "total_recommendations": total_recommendations,
        "reminders_requested": reminders_requested,
        "connect_requested": connect_requested,
    }