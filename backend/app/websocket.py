from typing import List, Dict, Any, Union, Optional
from fastapi import WebSocket
from .database import database
import time
from .handlers import select, update, delete

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.queue: List[WebSocket] = []
        self.websocket_to_playerid: Dict[WebSocket, int] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        if websocket in self.queue:
            self.queue.remove(websocket)
        if websocket in self.websocket_to_playerid:
            del self.websocket_to_playerid[websocket]

    async def get_pseudo(self, player1id: int, player2id: int):
        query = "SELECT pseudo FROM queue WHERE id = :playerid"
        
        player1pseudo = await select(query=query, values={"playerid": player1id})
        player2pseudo = await select(query=query, values={"playerid": player2id})
        
        if player1pseudo and player2pseudo:
            return player1pseudo["pseudo"], player2pseudo["pseudo"]
        return None, None

    async def get_ip(self, player1id: int, player2id: int):
        query = "SELECT playerip FROM queue WHERE id = :playerid"

        player1ip = await select(query=query, values={"playerid": player1id})
        player2ip = await select(query=query, values={"playerid": player2id})
        
        if player1ip and player2ip:
            return player1ip["playerip"], player2ip["playerip"]
        return None, None

    async def get_port(self, player1id: int, player2id: int):
        query = "SELECT port FROM queue WHERE id = :playerid"

        player1port = await select(query=query, values={"playerid": player1id})
        player2port = await select(query=query, values={"playerid": player2id})
        
        if player1port and player2port:
            return player1port["port"], player2port["port"]
        return None, None

    async def join_queue(self, websocket: WebSocket, pseudo: str):
        if websocket not in self.queue:
            self.queue.append(websocket)

            query = "INSERT INTO queue (playerip, port, pseudo, isingame) VALUES (:playerip, :port, :pseudo, :isingame)"
            values = {
                "playerip": websocket.client.host,
                "port": websocket.client.port,
                "pseudo": pseudo,
                "isingame": False
            }
            
            if await update(query=query, values=values):
                queryId = "SELECT id FROM queue WHERE playerip = :playerip AND port = :port"
                valuesId = {
                    "playerip": websocket.client.host,
                    "port": websocket.client.port
                }
                
                player = await select(query=queryId, values=valuesId)
                if player:
                    playerId = player["id"]
                    self.websocket_to_playerid[websocket] = playerId
                    await websocket.send_text(f"connection_established:{playerId}")
                    await self.checkGame()
                else:
                    await websocket.send_text("connection_failed")
            else:
                await websocket.send_text("connection_failed")

    async def leave_queue(self, websocket: WebSocket):
        if websocket in self.queue:
            self.queue.remove(websocket)

            query = "DELETE FROM queue WHERE playerip = :playerip AND port = :port"
            values = {
                "playerip": websocket.client.host,
                "port": websocket.client.port
            }

            if await delete(query=query, values=values):
                print("Player removed from queue.")

    async def send_message(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def play_move(self, websocket: WebSocket, move: str, playerid: str, playerSymbol: str):
        if websocket in self.queue:
            playerid = int(playerid)
            
            query = "SELECT * FROM game WHERE (player1id = :playerid OR player2id = :playerid) AND is_finished = FALSE"
            values = {"playerid": playerid}

            game = await select(query=query, values=values)
            if not game:
                return
                
            board = list(game["board"])
            board[int(move)] = playerSymbol
            new_board = "".join(board)

            update_query = "UPDATE game SET board = :board WHERE id = :game_id"
            update_values = {
                "board": new_board,
                "game_id": game["id"]
            }

            await update(query=update_query, values=update_values)
            
            query3 = "INSERT INTO round (game_id, move, player_turn) VALUES (:game_id, :move, :player_turn)"
            values3 = {
                "game_id": game["id"],
                "move": move,
                "player_turn": playerid
            }

            await update(query=query3, values=values3)
            
            await self.checkWin(board, game["id"])

            player1ip, player2ip = await self.get_ip(game["player1id"], game["player2id"])
            player1port, player2port = await self.get_port(game["player1id"], game["player2id"])

            query4 = "SELECT result FROM game WHERE id = :game_id"
            values4 = {"game_id": game["id"]}

            result = await select(query=query4, values=values4)
            if not result:
                return

            for player in self.queue:
                if player.client.host == player1ip and player.client.port == player1port:
                    await player.send_text(f"update_board:{new_board}:{result['result']}")
                elif player.client.host == player2ip and player.client.port == player2port:
                    await player.send_text(f"update_board:{new_board}:{result['result']}")

    async def checkWin(self, board, game_id):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  
            [0, 4, 8], [2, 4, 6]
        ]
        
        for condition in win_conditions:
            if board[condition[0]] == board[condition[1]] == board[condition[2]] == 'X':
                query = "UPDATE game SET result = :result, is_finished = TRUE WHERE id = :game_id"
                values = {
                    "result": "winX",
                    "game_id": game_id
                }
                await update(query=query, values=values)
                
            elif board[condition[0]] == board[condition[1]] == board[condition[2]] == 'O':
                query = "UPDATE game SET result = :result, is_finished = TRUE WHERE id = :game_id"
                values = {
                    "result": "winO",
                    "game_id": game_id
                }
                await update(query=query, values=values)

        if 'N' not in board:
            query = "UPDATE game SET result = :result, is_finished = TRUE WHERE id = :game_id"
            values = {
                "result": "draw",
                "game_id": game_id
            }
            await update(query=query, values=values)

    async def checkGame(self):
        query = """
        SELECT queue.id
        FROM queue
        WHERE isingame = FALSE
        """

        players = await select(query=query, fetch_all=True)
        if not players:
            return
            
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

            if await update(query=query, values=values):
                player1pseudo, player2pseudo = await self.get_pseudo(player1id, player2id)
                player1ip, player2ip = await self.get_ip(player1id, player2id)
                player1port, player2port = await self.get_port(player1id, player2id)
                
                for player in self.queue:
                    if player.client.host == player1ip and player.client.port == player1port:
                        await player.send_text(f"game_started:{player2pseudo}:{player1id}:{player2id}")
                    elif player.client.host == player2ip and player.client.port == player2port:
                        await player.send_text(f"game_started:{player1pseudo}:{player2id}:{player1id}")

                update_query = "UPDATE queue SET isingame = TRUE WHERE id = :playerid"
                await update(query=update_query, values={"playerid": player1id})
                await update(query=update_query, values={"playerid": player2id})

                players = players[2:]
            else:
                break

    async def replay(self, websocket: WebSocket):
        playerId = self.websocket_to_playerid.get(websocket)
        if playerId is None:
            return

        query = "UPDATE queue SET isingame = FALSE WHERE id = :playerid"
        values = {"playerid": playerId}

        if await update(query=query, values=values):
            await self.checkGame()


manager = ConnectionManager()