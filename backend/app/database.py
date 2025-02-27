from databases import Database
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, Text, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ENUM

DATABASE_URL = "postgresql+asyncpg://postgres:Ynovnoe2025@localhost/matchmaking_db"

# Création d'une instance Database
database = Database(DATABASE_URL)

# SQLAlchemy pour la gestion des modèles
metadata = MetaData()
Base = declarative_base(metadata=metadata)

# Créer le moteur de connexion
engine = create_engine(DATABASE_URL)

# Définition du type ENUM pour les résultats du jeu
game_result_enum = ENUM('draw', 'player1_win', 'player2_win', name='game_result', create_type=False)

# Définition des tables
class Queue(Base):
    __tablename__ = 'queue'
    id = Column(Integer, primary_key=True)
    playerip = Column(String(50), unique=True, nullable=False)
    port = Column(Integer, nullable=False)
    pseudo = Column(String(50), nullable=False)
    entrance_date = Column(TIMESTAMP, default='CURRENT_TIMESTAMP')

class Game(Base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True)
    player1id = Column(Integer, ForeignKey('queue.id', ondelete='CASCADE'), nullable=False)
    player2id = Column(Integer, ForeignKey('queue.id', ondelete='CASCADE'), nullable=False)
    board = Column(Text, nullable=False)
    is_finished = Column(Boolean, default=False)
    result = Column(game_result_enum, default='draw')

class Round(Base):
    __tablename__ = 'round'
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('game.id', ondelete='CASCADE'), nullable=False)
    move = Column(String(50), nullable=False)
    player_turn = Column(Integer, ForeignKey('queue.id', ondelete='CASCADE'), nullable=False)

# Créer toutes les tables
def create_all_tables():
    Base.metadata.create_all(engine)
