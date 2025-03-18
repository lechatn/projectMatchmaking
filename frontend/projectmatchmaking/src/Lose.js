import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Result.css';
import { useWebSocket } from './WebSocket';

const Lose = () => {
  const navigate = useNavigate();
  const WebSocket = useWebSocket();

  const handlePlayAgain = () => {
    WebSocket.send('replay');
    WebSocket.send('check_game');
    navigate('/loading');
  };

  const handleGoHome = () => {
    WebSocket.send('leave_queue');
    navigate('/');
  }

  return (
    <div className="result-page lose">
      <h1>😢 You Lost!</h1>
      <p>Better luck next time!</p>
      <button onClick={handlePlayAgain}>Play Again</button>
      <button onClick={handleGoHome}>Home</button>
    </div>
  );
};

export default Lose;