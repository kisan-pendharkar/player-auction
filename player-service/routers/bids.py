from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.BidBase)
def place_bid(bid: schemas.BidBase, db: Session = Depends(get_db)):
    team = db.query(models.Team).filter(models.Team.id == bid.team_id).first()
    if team.budget_remaining < bid.bid_amount:
        raise HTTPException(status_code=400, detail="Insufficient budget")

    db_bid = models.Bid(**bid.dict())
    db.add(db_bid)
    player = db.query(models.Player).filter(models.Player.id == bid.player_id).first()
    
    player.team_id = bid.team_id
    db.commit()
    db.refresh(db_bid)

    return db_bid
