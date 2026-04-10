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

# 🎓 Confirmation email with logging
def send_confirmation_email(to_email: str, full_name: str, opportunity_title: str, date: str):
    print(f"[Email] Preparing confirmation for {to_email}")
    try:
        message = Mail(
            from_email=os.getenv("FROM_EMAIL"),
            to_emails=to_email,
            subject=f"Booking Confirmed - {opportunity_title}",
            html_content=f"""
                <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2>Thanks for Volunteering, {full_name}!</h2>
                    <p>Your booking for <strong>{opportunity_title}</strong> on <strong>{date}</strong> is confirmed.</p>
                    <p>Every hour you give makes a real difference. See you there!</p>
                    <p style="color: #38bdf8; font-weight: bold;">Volunteer Gigs Team ❤️</p>
                </div>
            """
        )
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        print(f"[Email] Sent! Status code: {response.status_code}")
        if response.status_code >= 400:
            print(f"[Email] Response body: {response.body}")
    except Exception as e:
        print(f"[Email ERROR] {e}")

# 🎓 POST /bookings
@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking: BookingCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Save booking in DB
    new_booking = Booking(**booking.model_dump())
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    print(f"[Booking] Created booking for {new_booking.email}, sending email...")

    # Add email to background tasks
    background_tasks.add_task(
        send_confirmation_email,
        new_booking.email,
        new_booking.full_name,
        new_booking.opportunity_title,
        new_booking.date
    )

    return new_booking