from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter()

@router.post("/", response_model=schemas.AuctionBase)
def start_auction(auction: schemas.AuctionBase, db: Session = Depends(get_db)):
    db_auction = models.Auction(**auction.dict())
    db.add(db_auction)
    db.commit()
    db.refresh(db_auction)
    return db_auction

