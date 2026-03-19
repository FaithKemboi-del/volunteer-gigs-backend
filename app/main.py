from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import auth, bookings, recommendations
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.booking import Booking
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

# 🎓 Creates all database tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Volunteer Gigs API")

# 🎓 CORS allows our React frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🎓 Register all our routers
app.include_router(auth.router)
app.include_router(bookings.router)
app.include_router(recommendations.router)

# ============================================================
# 🎓 REMINDER SCHEDULER
# This function runs every day at 8am
# It checks the database for bookings scheduled for tomorrow
# and sends reminder emails to those volunteers
# ============================================================
def send_daily_reminders():
    print("⏰ Checking for tomorrow's bookings...")
    db: Session = SessionLocal()

    try:
        # 🎓 Get tomorrow's date in YYYY-MM-DD format
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

        # 🎓 Find all bookings where:
        # 1. The date is tomorrow
        # 2. The volunteer checked receive_reminder
        bookings_tomorrow = db.query(Booking).filter(
            Booking.date == tomorrow,
            Booking.receive_reminder == True
        ).all()

        print(f"📬 Found {len(bookings_tomorrow)} reminders to send")

        for booking in bookings_tomorrow:
            try:
                message = Mail(
                    from_email=os.getenv("FROM_EMAIL"),
                    to_emails=booking.email,
                    subject=f"Reminder - {booking.opportunity_title} is tomorrow!",
                    html_content=f"""
                        <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto;">
                            <h2 style="color: #0f2942;">See you tomorrow, {booking.full_name}! 👋</h2>
                            <p>Just a reminder that you're volunteering at <strong>{booking.opportunity_title}</strong> tomorrow on <strong>{booking.date}</strong>.</p>
                            <p>📍 Location: {booking.opportunity_organization}</p>
                            <p>Thank you for making a difference!</p>
                            <br/>
                            <p style="color: #38bdf8; font-weight: bold;">Volunteer Gigs Team ❤️</p>
                        </div>
                    """
                )
                sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
                sg.send(message)
                print(f"✅ Reminder sent to {booking.email}")
            except Exception as e:
                print(f"❌ Failed to send reminder to {booking.email}: {e}")

    finally:
        db.close()

# 🎓 BackgroundScheduler runs tasks in the background
# without blocking the API
scheduler = BackgroundScheduler()

# 🎓 Add the reminder job to run every day at 8:00 AM
scheduler.add_job(
    send_daily_reminders,
    trigger='cron',
    hour=8,
    minute=0,
    id='daily_reminders'
)

# 🎓 Start the scheduler when the API starts
scheduler.start()

# 🎓 Simple test endpoint
@app.get("/")
def root():
    return {"message": "Volunteer Gigs API is running! 🚀"}

# 🎓 Test endpoint to manually trigger reminders
# Useful for testing without waiting until 8am!
@app.get("/test-reminders")
def test_reminders():
    send_daily_reminders()
    return {"message": "Reminders checked!"}