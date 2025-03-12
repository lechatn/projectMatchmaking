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

            query = "INSERT INTO queue (playerip, port, pseudo, isingame) VALUES (:playerip, :port, :pseudo, :isingame)"
            values = {
                "playerip": websocket.client.host,
                "port": websocket.client.port,
                "pseudo": pseudo,
                "isingame": False
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

    async def send_message(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def play_move(self, websocket: WebSocket, move: str, playerid: str, playerSymbol: str):
        if websocket in self.queue:
            playerid = int(playerid)
            if not database.is_connected:
                await database.connect()

            query = "SELECT * FROM game WHERE player1id = :playerid OR player2id = :playerid"
            values = {
                "playerid": playerid
            }

            try:
                game = await database.fetch_one(query=query, values=values)
            except Exception as e:
                print(e)

            board = list(game["board"])
            board[int(move)] = playerSymbol
            new_board = "".join(board)

            update_query = "UPDATE game SET board = :board WHERE id = :game_id"
            update_values = {
                "board": new_board,
                "game_id": game["id"]
            }

            try:
                await database.execute(query=update_query, values=update_values)
            except Exception as e:
                print(e)

            query3 = "INSERT INTO round (game_id, move, player_turn) VALUES (:game_id, :move, :player_turn)"
            values3 = {
                "game_id": game["id"],
                "move": move,
                "player_turn": playerid
            }

            try:
                await database.execute(query=query3, values=values3)
            except Exception as e:
                print(e)

            await self.checkWin(board, game["id"])

            player1ip, player2ip = await self.get_ip(game["player1id"], game["player2id"])
            player1port, player2port = await self.get_port(game["player1id"], game["player2id"])


            query4 = "SELECT result FROM game WHERE id = :game_id"
            values4 = {
                "game_id": game["id"]
            }

            try:
                result = await database.fetch_one(query=query4, values=values4)
            except Exception as e:
                print(e)


            for player in self.queue:
                if player.client.host == player1ip and player.client.port == player1port:
                    await player.send_text(f"update_board:{new_board}:{result['result']}")
                elif player.client.host == player2ip and player.client.port == player2port:
                    await player.send_text(f"update_board:{new_board}:{result['result']}")

    async def checkWin(self, board, game_id):
        if not database.is_connected:
            await database.connect()
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical
            [0, 4, 8], [2, 4, 6]              # Diagonal
        ]
        for condition in win_conditions:
            if board[condition[0]] == board[condition[1]] == board[condition[2]] == 'X':
                query = "UPDATE game SET result = :result WHERE id = :game_id"
                values = {
                    "result": "winX",
                    "game_id": game_id
                }
                try:
                    await database.execute(query=query, values=values)
                except Exception as e:
                    print(e)

                query2 = "SELECT player1id, player2id FROM game WHERE id = :game_id"
                values2 = {
                    "game_id": game_id
                }

                try:
                    players = await database.fetch_one(query=query2, values=values2)
                except Exception as e:
                    print(e)

                query3 = "UPDATE queue SET isingame = FALSE WHERE id = :playerid"
                await database.execute(query=query3, values={"playerid": players["player1id"]})
                await database.execute(query=query3, values={"playerid": players["player2id"]})

            elif board[condition[0]] == board[condition[1]] == board[condition[2]] == 'O':
                query = "UPDATE game SET result = :result WHERE id = :game_id"
                values = {
                    "result": "winO",
                    "game_id": game_id
                }
                try:
                    await database.execute(query=query, values=values)
                except Exception as e:
                    print(e)

                query2 = "SELECT player1id, player2id FROM game WHERE id = :game_id"
                values2 = {
                    "game_id": game_id
                }

                try:
                    players = await database.fetch_one(query=query2, values=values2)
                except Exception as e:
                    print(e)

                query3 = "UPDATE queue SET isingame = FALSE WHERE id = :playerid"
                await database.execute(query=query3, values={"playerid": players["player1id"]})
                await database.execute(query=query3, values={"playerid": players["player2id"]})

        if 'N' not in board:
            query = "UPDATE game SET result = :result WHERE id = :game_id"
            values = {
                "result": "draw",
                "game_id": game_id
            }
            try:
                await database.execute(query=query, values=values)
            except Exception as e:
                print(e)

            query2 = "SELECT player1id, player2id FROM game WHERE id = :game_id"
            values2 = {
                "game_id": game_id
            }

            try:
                players = await database.fetch_one(query=query2, values=values2)
            except Exception as e:
                print(e)

            query3 = "UPDATE queue SET isingame = FALSE WHERE id = :playerid"
            values3 = {
                "playerid": players["player1id"]
            }
            values4 = {
                "playerid": players["player2id"]
            }
            await database.execute(query=query3, values=values3)
            await database.execute(query=query3, values=values4)

    async def checkGame(self):
        if not database.is_connected:
            await database.connect()

        query = """
        SELECT queue.id
        FROM queue
        WHERE isingame = FALSE
        """

        try:
            players = await database.fetch_all(query=query)
        except Exception as e:
            print(e)
        print(len(players))
        while len(players) >= 2:
            query = "INSERT INTO game (player1id, player2id, board, result) VALUES (:player1id, :player2id, :board, :result)"
            values = {
                "player1id": players[0]["id"],
                "player2id": players[1]["id"],
                "board": "NNNNNNNNN",
                "result": "null"
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
                        await player.send_text(f"game_started:{player2pseudo}:{player1id}:{player2id}")
                    elif player.client.host == player2ip and player.client.port == player2port:
                        await player.send_text(f"game_started:{player1pseudo}:{player2id}:{player1id}")

                update_query = "UPDATE queue SET isingame = TRUE WHERE id = :playerid"
                await database.execute(query=update_query, values={"playerid": player1id})
                await database.execute(query=update_query, values={"playerid": player2id})

                players = players[2:]
            except Exception as e:
                print(e)
        else:
            print("Pas assez de joueurs.")

    async def end_game(self):
        await self.checkGame()

manager = ConnectionManager()