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

    async def play_move(self, websocket: WebSocket, move: str, playerid: str):
        print("ok")
        if websocket in self.queue:
            print("ok 2")
            playerid = int(playerid)
            if not database.is_connected:
                await database.connect()

            query = "SELECT * FROM game WHERE player1id = :playerid OR player2id = :playerid"
            values = {
                "playerid": playerid
            }

            try:
                game = await database.execute(query=query, values=values)
            except Exception as e:
                print(e)

            query ="SELECT id FROM game WHERE player1id = :playerid OR player2id = :playerid"
            values = {
                "playerid": playerid
            }

            try:
                game = await database
            except Exception as e:
                print(e)

            query3 = "INSERT INTO round (game_id, move, player_turn) VALUES (:game_id, :move, :player_turn)"
            values3 = {
                "game_id": game,
                "move": move,
                "player_turn": playerid
            }

            try:
                await database.execute(query=query3, values=values3)
            except Exception as e:
                print(e)

            await self.send_message(f"Player {playerid} played move {move}")
            



    async def start_game(self, player1id: int, player2id: int):
        if not database.is_connected:
            await database.connect()

        player1id = int(player1id)
        player2id = int(player2id)

        query = "SELECT FROM game WHERE player1id = :player1id AND player2id = :player2id"
        values = {
            "player1id": player1id,
            "player2id": player2id
        }

        try:
            game = await database.fetch_one(query=query, values=values)
        except Exception as e:
            print(e)

        if game:
            if player1id == game.player1id or player1id == game.player2id:
                await self.send_message(f"Player {player1id} is already in a game.")
                return
            elif player2id == game.player1id or player2id == game.player2id:
                await self.send_message(f"Player {player2id} is already in a game.")
                return
        else:
            query2 = "INSERT INTO game (player1id, player2id, board) VALUES (:player1id, :player2id, :board)"
            values2 = {
                "player1id": player1id,
                "player2id": player2id,
                "board": "---------"
            }

            try:
                await database.execute(query=query2, values=values2)
            except Exception as e:
                print(e)

            await self.send_message(f"Game started between {player1id} and {player2id}")



manager = ConnectionManager()
