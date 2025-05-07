# File: main.py
__author__ = "Kisan Pendharkar" 
__date__ = "06/05/2025"
__description__ = "Main entry point for the Player Auction Service"
__version__ = "1.0.0"
__update__ = "06/05/2025"

from fastapi import FastAPI
from database import Base, engine
from routers import users, teams, players, auction, bids, tournament
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(description="Player Auction Service", title="Player Auction API", version="1.0.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/users",tags=["Users"])
app.include_router(teams.router, prefix="/teams", tags=["Teams"])
app.include_router(players.router, prefix="/players", tags=["Players"])
app.include_router(auction.router, prefix="/auction", tags=["Auction"])
app.include_router(bids.router, prefix="/bids", tags=["Bids"])
app.include_router(tournament.router, prefix="/tournament", tags=["Tournament"])

