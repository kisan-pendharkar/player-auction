# module: player-service
__author__ = "Kisan Pendharkar" 
__date__ = "06/05/2025"
__description__ = "Module for defining database models for the Player Auction Service"
__version__ = "1.0.0"
__update__ = "06/05/2025"



from sqlalchemy import Column, Integer, String, ForeignKey, Float, Enum, DateTime
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String)
    status = Column(String)
    team = relationship("Team", back_populates="owner", uselist=False)

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    budget_remaining = Column(Float)
    owner = relationship("User", back_populates="team")
    players = relationship("Player", back_populates="team")
    t_id = Column(Integer, ForeignKey("tournaments.id"))
    tournament = relationship("Tournament", back_populates="teams")


class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    base_price = Column(Float)
    sold_price = Column(Float)
    team_id = Column(Integer, ForeignKey("teams.id"))
    team = relationship("Team", back_populates="players")

class Auction(Base):
    __tablename__ = "auction"
    id = Column(Integer, primary_key=True)
    current_player_id = Column(Integer, ForeignKey("players.id"))
    round = Column(Integer)
    status = Column(String)

class Bid(Base):
    __tablename__ = "bids"
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    team_id = Column(Integer, ForeignKey("teams.id"))
    bid_amount = Column(Float)

class Tournament(Base):
    __tablename__ = "tournaments"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(String)
    
    