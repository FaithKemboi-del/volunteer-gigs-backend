from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.booking import Booking
from app.schemas.booking import BookingCreate, BookingResponse
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
from typing import List
import os

load_dotenv()

router = APIRouter(prefix="/bookings", tags=["bookings"])

# 🎓 This function sends a confirmation email using SendGrid
def send_confirmation_email(to_email: str, full_name: str, opportunity_title: str, date: str):
    try:
        message = Mail(
            from_email=os.getenv("FROM_EMAIL"),
            to_emails=to_email,
            subject=f"Booking Confirmed - {opportunity_title}",
            html_content=f"""
                <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2 style="color: #0f2942;">Thanks for Volunteering, {full_name}! 🌟</h2>
                    <p>Your booking for <strong>{opportunity_title}</strong> on <strong>{date}</strong> is confirmed.</p>
                    <p>Every hour you give makes a real difference. See you there!</p>
                    <br/>
                    <p style="color: #38bdf8; font-weight: bold;">Volunteer Gigs Team ❤️</p>
                </div>
            """
        )
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        sg.send(message)
    except Exception as e:
        print(f"Email error: {e}")

# 🎓 This function sends a reminder email
def send_reminder_email(to_email: str, full_name: str, opportunity_title: str, date: str):
    try:
        message = Mail(
            from_email=os.getenv("FROM_EMAIL"),
            to_emails=to_email,
            subject=f"Reminder - {opportunity_title} is tomorrow!",
            html_content=f"""
                <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2 style="color: #0f2942;">See you tomorrow, {full_name}! 👋</h2>
                    <p>Just a reminder that you're volunteering at <strong>{opportunity_title}</strong> tomorrow on <strong>{date}</strong>.</p>
                    <p>Thank you for making a difference!</p>
                    <br/>
                    <p style="color: #38bdf8; font-weight: bold;">Volunteer Gigs Team ❤️</p>
                </div>
            """
        )
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        sg.send(message)
    except Exception as e:
        print(f"Reminder email error: {e}")

# 🎓 POST /bookings - saves a booking and sends confirmation email
@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(booking: BookingCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    new_booking = Booking(**booking.model_dump())
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    # 🎓 BackgroundTasks sends email WITHOUT making the user wait
    background_tasks.add_task(
        send_confirmation_email,
        new_booking.email,
        new_booking.full_name,
        new_booking.opportunity_title,
        new_booking.date
    )

    return new_booking

# 🎓 GET /bookings - returns all bookings
@router.get("/", response_model=List[BookingResponse])
def get_bookings(db: Session = Depends(get_db)):
    return db.query(Booking).all()