
# File: main.py
__author__ = "Kisan Pendharkar" 
__date__ = "06/05/2025"
__description__ = "player service for the Player Auction Service"
__version__ = "1.0.0"
__update__ = "06/05/2025"


from fastapi import APIRouter, Depends,Query,HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from fastapi.responses import JSONResponse
from routers import response
from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.post("/", response_model=schemas.PlayerBase)
def create_player(player: schemas.PlayerBase, db: Session = Depends(get_db)):
    
    if not player.name:
           return JSONResponse(status_code=400, content={"error": "Username is required"})
           
    if not player.category:   
        
        return JSONResponse(status_code=400, content={"error": "Category is required"})
    
    if not player.base_price:
        return JSONResponse(status_code=400, content={"error": "Base price is required"})
        
    exit_player = db.query(models.Player).filter(models.Player.name == player.name).first()
    
    # Check if the player already exists
    if exit_player and exit_player.name:
        return JSONResponse(status_code=400, content={"error": "Player already exists"})
    
    
    db_player = models.Player(**player.dict())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return JSONResponse(status_code=200, content={"success":True,"message": "Player created successfully", "name": player.name})



@router.get("/",response_model=response.PaginatedResponse)
def get_players(db: Session = Depends(get_db),
    limit: int = Query(10, description="Number of users to return"),
    offset: int = Query(0, description="Number of users to skip")):
    
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
        "message": "Player fetched successfully",
        "data": [],
        "total": 0,
        "limit": limit,
        "offset": offset,
    }
    
    
    
    if limit == 0:
        return JSONResponse(status_code=200, content=response)
        
    if offset == 0:
        users = db.query(models.Player).limit(limit).all()
        
    if limit == 0 and offset == 0:
        users = db.query(models.Player).all()
    
    if limit > 0 and offset > 0:
        users = db.query(models.Player).offset(offset).limit(limit).all()
    
    serialized_users = jsonable_encoder(users)
    
    response["data"] = serialized_users
    response["total"] = db.query(models.Player).count()
    
    return response
    
    
    
    
    return db.query(models.Player).limit(limit).offset(offset).all()
