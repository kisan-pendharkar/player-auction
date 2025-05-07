                                                                   
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str
    role: str
    status: str

class UserCreate(UserBase):
    password: str

class TeamBase(BaseModel):
    name: str
    budget : int

class PlayerBase(BaseModel):
    name: str
    category: str
    base_price: float

class AuctionBase(BaseModel):
    current_player_id: Optional[int]
    round: int
    status: str

class BidBase(BaseModel):
    player_id: int
    team_id: int
    bid_amount: float
    
    
class TournamentBase(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime
    status: str
    