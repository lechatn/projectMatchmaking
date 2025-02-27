from databases import Database
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql+asyncpg://postgres:Ynovnoe2025@localhost/matchmaking_db"

# Création d'une instance Database
database = Database(DATABASE_URL)

# SQLAlchemy pour la gestion des modèles
metadata = MetaData()
Base = declarative_base(metadata=metadata)

# Créer le moteur de connexion
engine = create_engine(DATABASE_URL)
