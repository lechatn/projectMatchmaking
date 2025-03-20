from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from .database import database, create_all_tables, Base
from .websocket import manager
from sqlalchemy.exc import OperationalError
import asyncio
import os

# Créez un moteur asynchrone
DATABASE_URL = os.getenv('DATABASE_URL')
async_engine = create_async_engine(DATABASE_URL, echo=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    print("Connexion à la base de données réussie !")
    
    yield
    
    await database.disconnect()
    print("Déconnexion de la base de données.")

app = FastAPI(lifespan=lifespan)

# WebSocket Endpoint
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
            elif data.startswith("start_game"):
                move_data = data.split(":")
                player1id = move_data[1]
                player2id = move_data[2]
                await manager.start_game(player1id, player2id)
            elif data.startswith("play_move"):
                move_data = data.split(":")
                move = move_data[1]
                playerid = move_data[2]
                playerSymbol = move_data[3]
                await manager.play_move(websocket, move, playerid, playerSymbol)          
            elif data == "check_game":
                await manager.checkGame() 
            elif data == "replay":
                await manager.replay(websocket)        
            else:
                await manager.send_message(f"Message reçu: {data}")
            
    except WebSocketDisconnect:
        await manager.disconnect(websocket)