import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Result.css';
import { useWebSocket } from './WebSocket';

const Draw = () => {
  const navigate = useNavigate();
  const WebSocket = useWebSocket();

  const handlePlayAgain = () => {
    WebSocket.send('replay');
    WebSocket.send('check_game');
    navigate('/loading');
  };

  return (
    <div className="result-page draw">
      <h1>🤝 It's a Draw!</h1>
      <p>No winners this time!</p>
      <button onClick={handlePlayAgain}>Play Again</button>
    </div>
  );
};

export default Draw;