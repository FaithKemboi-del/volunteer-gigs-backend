from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.opportunity import Opportunity
from app.schemas.opportunity import OpportunityCreate, OpportunityResponse
from typing import List

router = APIRouter(prefix="/opportunities", tags=["opportunities"])

# 🎓 GET all opportunities - used by React frontend
@router.get("/", response_model=List[OpportunityResponse])
def get_opportunities(db: Session = Depends(get_db)):
    return db.query(Opportunity).all()

# 🎓 GET single opportunity by id
@router.get("/{opportunity_id}", response_model=OpportunityResponse)
def get_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return opportunity

# 🎓 POST - admin creates new opportunity
@router.post("/", response_model=OpportunityResponse, status_code=status.HTTP_201_CREATED)
def create_opportunity(opportunity: OpportunityCreate, token: str, db: Session = Depends(get_db)):
    if token != "admin-token-volunteer-gigs":
        raise HTTPException(status_code=401, detail="Unauthorized")
    new_opportunity = Opportunity(**opportunity.model_dump())
    db.add(new_opportunity)
    db.commit()
    db.refresh(new_opportunity)
    return new_opportunity

# 🎓 DELETE - admin deletes opportunity
@router.delete("/{opportunity_id}")
def delete_opportunity(opportunity_id: int, token: str, db: Session = Depends(get_db)):
    if token != "admin-token-volunteer-gigs":
        raise HTTPException(status_code=401, detail="Unauthorized")
    opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    db.delete(opportunity)
    db.commit()
    return {"message": "Opportunity deleted successfully"}