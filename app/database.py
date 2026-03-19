from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# 🎓 load_dotenv() reads your .env file
# so we can use os.getenv() to get the values
load_dotenv()

# 🎓 This is the connection string to your PostgreSQL database
DATABASE_URL = os.getenv("DATABASE_URL")

# 🎓 create_engine creates the connection to the database
engine = create_engine(DATABASE_URL)

# 🎓 SessionLocal is used to talk to the database
# Each request gets its own session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🎓 Base is the parent class for all our database models
Base = declarative_base()

# 🎓 get_db is a dependency that gives each request a database session
# and closes it when the request is done
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()