from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import database
from fastapi import WebSocket, WebSocketDisconnect
from typing import List
from app.websockets import manager


# Création d'un gestionnaire de contexte async
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Démarrage de l'application
    await database.connect()
    print("Connexion à la base de données réussie !")
    
    # Permet à l'application de fonctionner
    yield
    
    # Arrêt de l'application
    await database.disconnect()
    print("Déconnexion de la base de données.")

# Créer l'application FastAPI en utilisant lifespan
app = FastAPI(lifespan=lifespan)

# Endpoint pour tester la connexion
@app.get("/test-connection/")
async def test_connection():
    return {"message": "Base de données connectée"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_message(f"Message reçu: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)