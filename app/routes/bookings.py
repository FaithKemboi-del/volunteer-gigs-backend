from fastapi import APIRouter, Depends, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.booking import Booking
from app.schemas.booking import BookingCreate, BookingResponse
from typing import List
from dotenv import load_dotenv
import resend
import os

load_dotenv()

router = APIRouter(prefix="/bookings", tags=["bookings"])

def send_confirmation_email(to_email: str, full_name: str, opportunity_title: str, date: str):
    try:
        resend.api_key = os.getenv("RESEND_API_KEY")
        resend.Emails.send({
            "from": os.getenv("FROM_EMAIL"),
            "to": to_email,
            "subject": f"Booking Confirmed - {opportunity_title}",
            "html": f"""
                <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2 style="color: #0f2942;">Thanks for Volunteering, {full_name}! 🌟</h2>
                    <p>Your booking for <strong>{opportunity_title}</strong> on <strong>{date}</strong> is confirmed.</p>
                    <p>Every hour you give makes a real difference. See you there!</p>
                    <br/>
                    <p style="color: #38bdf8; font-weight: bold;">Volunteer Gigs Team ❤️</p>
                </div>
            """
        })
    except Exception as e:
        print(f"Email error: {e}")

@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(booking: BookingCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    new_booking = Booking(**booking.model_dump())
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    background_tasks.add_task(
        send_confirmation_email,
        new_booking.email,
        new_booking.full_name,
        new_booking.opportunity_title,
        new_booking.date
    )
    return new_booking

@router.get("/", response_model=List[BookingResponse])
def get_bookings(db: Session = Depends(get_db)):
    return db.query(Booking).all()