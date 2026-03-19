from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.recommendation import Recommendation
from app.schemas.recommendation import RecommendationCreate, RecommendationResponse
from typing import List

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

# 🎓 POST /recommendations - saves a recommendation
@router.post("/", response_model=RecommendationResponse, status_code=status.HTTP_201_CREATED)
def create_recommendation(recommendation: RecommendationCreate, db: Session = Depends(get_db)):
    new_recommendation = Recommendation(**recommendation.model_dump())
    db.add(new_recommendation)
    db.commit()
    db.refresh(new_recommendation)
    return new_recommendation

# 🎓 GET /recommendations - returns all recommendations
@router.get("/", response_model=List[RecommendationResponse])
def get_recommendations(db: Session = Depends(get_db)):
    return db.query(Recommendation).all()