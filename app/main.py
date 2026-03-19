from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import auth, bookings, recommendations

# 🎓 Creates all database tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Volunteer Gigs API")

# 🎓 CORS allows our React frontend to talk to this API
# Without this the browser would block all requests!
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

# 🎓 Simple test endpoint to check if API is running
@app.get("/")
def root():
    return {"message": "Volunteer Gigs API is running! 🚀"}