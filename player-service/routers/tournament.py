# File: main.py
__author__ = "Kisan Pendharkar" 
__date__ = "06/05/2025"
__description__ = "user service for the Player Auction Service"
__version__ = "1.0.0"
__update__ = "06/05/2025"

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from fastapi.responses import JSONResponse
from routers import response
from fastapi.encoders import jsonable_encoder

router = APIRouter()



@router.post("/", response_model=schemas.TournamentBase)
def create_tournament(tournament: schemas.TournamentBase, db: Session = Depends(get_db)):
    
    try:
        
        if not tournament.name:
           return JSONResponse(status_code=400, content={"error": "Tournament name is required"})
           
        if not tournament.start_date:   
            return JSONResponse(status_code=400, content={"error": "Tournament start_date is required"})
       
        if not tournament.end_date:
            return JSONResponse(status_code=400, content={"error": "end_date is required"})
            
        exit_name = db.query(models.User).filter(models.Tournament.name == tournament.name).first()
        
        # Check if the tournament already exists
        if exit_name and exit_name.name:
            return JSONResponse(status_code=400, content={"error": "Tournament already exists"})
        
        db_tournament = models.Tournament(**tournament.dict())
        db.add(db_tournament)
        db.commit()
        db.refresh(db_tournament)
        return JSONResponse(status_code=200, content={"message": "Tournament created successfully", "name": db_tournament.name})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
  
  
  
        
@router.get("/", response_model=response.PaginatedResponse)
def get_users(
    db: Session = Depends(get_db),
    limit: int = Query(10, description="Number of users to return"),
    offset: int = Query(0, description="Number of users to skip")
):
    try:
        if limit < 0 or offset < 0:
            raise HTTPException(status_code=400, detail="Limit and offset must be non-negative")
    except ValueError:
        raise HTTPException(status_code=400, detail="Limit and offset must be integers")

    if limit > 100: 
        raise HTTPException(status_code=400, detail="Limit must be less than or equal to 100")

    if offset > 1000:
        raise HTTPException(status_code=400, detail="Offset must be less than or equal to 1000")
    
   
    # Prepare response
    response = {
        "success": True,
        "message": "Tournament fetched successfully",
        "data": [],
        "total": 0,
        "limit": limit,
        "offset": offset,
    }
    
    
    
    if limit == 0:
        return JSONResponse(status_code=200, content=response)
        
    if offset == 0:
        tournament = db.query(models.Tournament).limit(limit).all()
        
    if limit == 0 and offset == 0:
        tournament = db.query(models.Tournament).all()
    
    if limit > 0 and offset > 0:
        tournament = db.query(models.Tournament).offset(offset).limit(limit).all()
    
    serialized_tournaments = jsonable_encoder(tournament)
    
    response["data"] = serialized_tournaments
    response["total"] = db.query(models.Tournament).count()
    
    return response
    

