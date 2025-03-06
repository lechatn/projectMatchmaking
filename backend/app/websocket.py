from typing import List
from fastapi import WebSocket
from .database import database
import time

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.queue: List[WebSocket] = [] 

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def get_pseudo(self, player1id: int, player2id: int):
        if not database.is_connected:
            await database.connect()

        query = "SELECT pseudo FROM queue WHERE id = :playerid"
        
        try:
            player1pseudo = await database.fetch_one(query=query, values={"playerid": player1id})
            player2pseudo = await database.fetch_one(query=query, values={"playerid": player2id})
        except Exception as e:
            print(e)
            return None, None

        return player1pseudo["pseudo"], player2pseudo["pseudo"]

    
    async def get_ip(self, player1id: int, player2id: int):
        if not database.is_connected:
            await database.connect()

        query = "SELECT playerip FROM queue WHERE id = :playerid"

        try:
            player1ip = await database.fetch_one(query=query, values={"playerid": player1id})
            player2ip = await database.fetch_one(query=query, values={"playerid": player2id})
        except Exception as e:
            print(e)
            return None, None

        return player1ip["playerip"], player2ip["playerip"]

    async def get_port(self, player1id: int, player2id: int):
        if not database.is_connected:
            await database.connect()

        query = "SELECT port FROM queue WHERE id = :playerid"

        try:
            player1port = await database.fetch_one(query=query, values={"playerid": player1id})
            player2port = await database.fetch_one(query=query, values={"playerid": player2id})
        except Exception as e:
            print(e)
            return None, None

        return player1port["port"], player2port["port"]


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
                queryId = "SELECT id FROM queue WHERE playerip = :playerip AND port = :port"
                valuesId = {
                    "playerip": websocket.client.host,
                    "port": websocket.client.port
                }
                try:
                    id = await database.execute(query=queryId, values=valuesId)
                except Exception as e:
                    print(e)
                await websocket.send_text("connection_established:" + str(id))
                time.sleep(5)
                print("Checking game")
                await self.checkGame()
            except Exception as e:
                await websocket.send_text("connection_failed")
                print(e)
                return
    
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
        if websocket in self.queue:
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
                player1pseudo, player2pseudo = await self.get_pseudo(player1id, player2id)
                player1ip , player2ip = await self.get_ip(player1id, player2id)
                player1port, player2port = await self.get_port(player1id, player2id)
                print(player1pseudo, player2pseudo)
                print(player1ip, player2ip)
                print(player1port, player2port)
                for player in self.queue:
                    if player.client.host == player1ip and player.client.port == player1port:
                        await player.send_text(f"game_started:{player2pseudo}")
                    elif player.client.host == player2ip and player.client.port == player2port:
                        await player.send_text(f"game_started:{player1pseudo}")
            except Exception as e:
                print(e)


    async def checkGame(self):
        if not database.is_connected:
            await database.connect()

        query = """
        SELECT queue.id
        FROM queue
        LEFT JOIN game
        ON queue.id = game.player1id OR queue.id = game.player2id
        WHERE game.player1id IS NULL AND game.player2id IS NULL;
        """

        try:
            players = await database.fetch_all(query=query)
        except Exception as e:
            print(e)
        
        print(players)
        print(len(players))
        if len(players) == 2:
            query = "INSERT INTO game (player1id, player2id, board) VALUES (:player1id, :player2id, :board)"
            values = {
                "player1id": players[0]["id"],
                "player2id": players[1]["id"],
                "board": "---------"
            }

            player1id = players[0]["id"]
            player2id = players[1]["id"]

            try:
                await database.execute(query=query, values=values)
                player1pseudo, player2pseudo = await self.get_pseudo(player1id, player2id)
                player1ip , player2ip = await self.get_ip(player1id, player2id)
                player1port, player2port = await self.get_port(player1id, player2id)
                for player in self.queue:
                    if player.client.host == player1ip and player.client.port == player1port:
                        await player.send_text(f"game_started:{player2pseudo}")
                    elif player.client.host == player2ip and player.client.port == player2port:
                        await player.send_text(f"game_started:{player1pseudo}")
            except Exception as e:
                print(e)
        else:
            print("Pas assez de joueurs.")



manager = ConnectionManager()
