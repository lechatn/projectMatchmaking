  import React, { useEffect } from 'react';
  import { useNavigate } from 'react-router-dom';
  import './Result.css';
  import { useWebSocket } from './WebSocket';

  const Win = () => {
    const navigate = useNavigate();
    const WebSocket = useWebSocket();

    const handlePlayAgain = () => {
      WebSocket.send('replay');
      WebSocket.send('check_game');
      navigate('/loading');
    };

    return (
      <div className="result-page win">
        <h1>🎉 You Won!</h1>
        <p>Congratulations!</p>
        <button onClick={handlePlayAgain}>Play Again</button>
      </div>
    );
  };

  export default Win;