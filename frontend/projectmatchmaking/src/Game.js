import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import './Game.css';
import { useWebSocket } from './WebSocket';

const Game = () => {
  const WebSocket = useWebSocket();

  const location = useLocation();
  const playAgainst = location.state?.playAgainst;
  const hostId = location.state?.hostId;
  const opponentId = location.state?.opponentId;

  const [board, setBoard] = useState(Array(9).fill(null));
  const [turn] = useState(0);
  const [isMyTurn, setIsMyTurn] = useState(false);

  useEffect(() => {
    if (turn === 0) {
      setBoard(Array(9).fill(null));
      setIsMyTurn(hostId < opponentId);
    }
  }, [turn, hostId, opponentId]);

  const handleClick = (index) => {
    if (!isMyTurn || board[index]) return;
    const playerSymbol = hostId < opponentId ? 'X' : 'O';
    WebSocket.send(`play_move:${index}:${hostId}:${playerSymbol}`);
  };

  useEffect(() => {
    const handleMessage = (event) => {
      const data = event.data;
      const [command, newBoard] = data.split(':');
      if (command === 'update_board') {
        const updatedBoard = newBoard.split('').map(cell => cell === 'N' ? '' : cell);
        setBoard(updatedBoard);
        setIsMyTurn(!isMyTurn);
      }
    };

    WebSocket.addEventListener('message', handleMessage);
    return () => {
      WebSocket.removeEventListener('message', handleMessage);
    };
  }, [WebSocket, isMyTurn]);

  return (
    <div className="Game">
      <h1>Welcome to the Game!</h1>
      <p>You're playing against: {playAgainst}</p>
      <h2>Voici le plateau de jeu :</h2>
      <div className="board">
        {board.map((cell, index) => (
          <div key={index} className="cell" onClick={() => handleClick(index)}>
            {cell}
          </div>
        ))}
      </div>
      <p>{isMyTurn ? "It's your turn!" : "Waiting for opponent's move..."}</p>
    </div>
  );
};

export default Game;