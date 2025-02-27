from typing import List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.queue: List[WebSocket] = []  # Liste pour la gestion de la queue

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def join_queue(self, websocket: WebSocket):
        if websocket not in self.queue:
            self.queue.append(websocket)
            await websocket.send_text("Vous avez rejoint la file d'attente.")

    async def leave_queue(self, websocket: WebSocket):
        if websocket in self.queue:
            self.queue.remove(websocket)
            await websocket.send_text("Vous avez quitté la file d'attente.")

    async def send_message(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def play_move(self, move: str):
        for connection in self.active_connections:
            await connection.send_text(move)


manager = ConnectionManager()
