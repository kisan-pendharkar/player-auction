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
from typing import Optional
from routers import response
from fastapi.encoders import jsonable_encoder

router = APIRouter()



@router.post("/", response_model=schemas.UserBase)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    try:
        
        if not user.username:
           return JSONResponse(status_code=400, content={"error": "Username is required"})
           
        if not user.password:   
            
            return JSONResponse(status_code=400, content={"error": "Password is required"})
       
        if not user.email:
            return JSONResponse(status_code=400, content={"error": "Email is required"})
            
        exit_user = db.query(models.User).filter(models.User.username == user.username).first()
        
        # Check if the user already exists
        if exit_user.username:
            return JSONResponse(status_code=400, content={"error": "User already exists"})
        
        db_user = models.User(**user.dict())
        db_user.username
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return JSONResponse(status_code=200, content={"message": "User created successfully", "username": db_user.username})
    
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
        "message": "Users fetched successfully",
        "data": [],
        "total": 0,
        "limit": limit,
        "offset": offset,
    }
    
    
    
    if limit == 0:
        return JSONResponse(status_code=200, content=response)
        
    if offset == 0:
        users = db.query(models.User).limit(limit).all()
        
    if limit == 0 and offset == 0:
        users = db.query(models.User).all()
    
    if limit > 0 and offset > 0:
        users = db.query(models.User).offset(offset).limit(limit).all()
    
    serialized_users = jsonable_encoder(users)
    
    response["data"] = serialized_users
    response["total"] = db.query(models.User).count()
    
    return response
    

