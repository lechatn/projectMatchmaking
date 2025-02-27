from typing import List
from fastapi import WebSocket
from .database import database

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.queue: List[WebSocket] = []  # Liste pour la gestion de la queue

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def join_queue(self, websocket: WebSocket, pseudo: str):
        if websocket not in self.queue:
            self.queue.append(websocket)

            if not database.is_connected:
                await database.connect()

            query = "INSERT INTO queue (playerip, port, pseudo) VALUES (:playerip, :port, :pseudo)"
            values = {
                "playerip": websocket.client.host,
                "port": websocket.client.port,
                "pseudo": pseudo
            }

            try:
                await database.execute(query=query, values=values)
            except Exception as e:
                print(e)

            await websocket.send_text("Vous avez rejoint la file d'attente.")

    async def leave_queue(self, websocket: WebSocket):
        if websocket in self.queue:
            self.queue.remove(websocket)

            if not database.is_connected:
                await database.connect()

            query = "DELETE FROM queue WHERE playerip = :playerip AND port = :port"
            values = {
                "playerip": websocket.client.host,
                "port": websocket.client.port
            }

            try:
                await database.execute(query=query, values=values)
                print("Player removed from queue.")
            except Exception as e:
                print(e)

            await websocket.send_text("Vous avez quitté la file d'attente.")

    async def send_message(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def play_move(self, move: str):
        for connection in self.active_connections:
            await connection.send_text(move)

    async def start_game(self, player1id: int, player2id: int):
        print(f"Game started between {player1id} and {player2id}")

        if not database.is_connected:
            await database.connect()

        player1id = int(player1id)
        player2id = int(player2id)

        query = "INSERT INTO game (player1id, player2id, board) VALUES (:player1id, :player2id, :board)"
        values = {
            "player1id": player1id,
            "player2id": player2id,
            "board": "---------"
        }

        try:
            await database.execute(query=query, values=values)
        except Exception as e:
            print(e)

        await self.send_message(f"Game started between {player1id} and {player2id}")



manager = ConnectionManager()
