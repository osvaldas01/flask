from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    guessed_score = Column(String(7))

    bets = relationship("Bet", back_populates="user")

class Match(Base):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True, autoincrement=True)
    team1 = Column(String, nullable=False)
    team2 = Column(String, nullable=False)
    match_date = Column(String, nullable=False)
    result = Column(String)

    bets = relationship("Bet", back_populates="match")

class Bet(Base):
    __tablename__ = 'bets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    match_id = Column(Integer, ForeignKey('matches.id'), nullable=False)

    user = relationship("User", back_populates="bets")
    match = relationship("Match", back_populates="bets")


