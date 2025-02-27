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
            if data.startswith("join_queue"):
                move_data = data.split(":")
                pseudo = move_data[1]
                await manager.join_queue(websocket, pseudo)
            elif data == "leave_queue":
                await manager.leave_queue(websocket)
            elif data == "start_game":
                await manager.send_message(f"Un match commence !")        
            elif data.startswith("play_move"):
                move_data = data.split(":")
                move = move_data[1]
                await manager.send_message(f"Le coup joué est : {move}")                
            elif data == "end_game":
                await manager.send_message(f"Le match est terminé.")                
            else:
                await manager.send_message(f"Message reçu: {data}")
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)