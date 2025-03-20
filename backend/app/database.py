from databases import Database
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, Text, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ENUM
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

database = Database(DATABASE_URL)

metadata = MetaData()
Base = declarative_base(metadata=metadata)

engine = create_engine(DATABASE_URL)

game_result_enum = ENUM('draw', 'player1_win', 'player2_win', name='game_result', create_type=False)

class Queue(Base):
    __tablename__ = 'queue'
    id = Column(Integer, primary_key=True)
    playerip = Column(String(50), unique=True, nullable=False)
    port = Column(Integer, nullable=False)
    pseudo = Column(String(50), nullable=False)
    entrance_date = Column(TIMESTAMP, default='CURRENT_TIMESTAMP')
    isingame = Column(Boolean, default=False)

class Game(Base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True)
    player1id = Column(Integer, ForeignKey('queue.id', ondelete='CASCADE'), nullable=False)
    player2id = Column(Integer, ForeignKey('queue.id', ondelete='CASCADE'), nullable=False)
    board = Column(Text, nullable=False)
    is_finished = Column(Boolean, default=False)
    result = Column(Text)

class Round(Base):
    __tablename__ = 'round'
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('game.id', ondelete='CASCADE'), nullable=False)
    move = Column(String(50), nullable=False)
    player_turn = Column(Integer, ForeignKey('queue.id', ondelete='CASCADE'), nullable=False)

def create_all_tables():
    Base.metadata.create_all(engine)
