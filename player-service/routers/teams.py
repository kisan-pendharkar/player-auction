### routers/teams.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter()

@router.post("/", response_model=schemas.TeamBase)
def create_team(team: schemas.TeamBase, db: Session = Depends(get_db)):
    db_team = models.Team(name=team.name, budget_remaining=team.budget)  
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


@router.get("/")
def get_teams(db: Session = Depends(get_db)):
    return db.query(models.Team).all()