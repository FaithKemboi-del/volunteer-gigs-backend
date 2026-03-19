# Schemas define the shape of data coming IN and going OUT of the API
from pydantic import BaseModel, EmailStr
from datetime import datetime

# 🎓 This is what we expect when someone SIGNS UP
class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str

# 🎓 This is what we expect when someone SIGNS IN
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# 🎓 This is what we SEND BACK after signup/signin
class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

# 🎓 This is what we send back after successful login
# access_token is the JWT token the frontend will use for protected routes
class Token(BaseModel):
    access_token: str
    token_type: str