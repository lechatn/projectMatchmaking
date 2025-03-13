import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./Home.css";
import { useWebSocket } from './WebSocket';

function Home() {
  const navigate = useNavigate();
  const socket = useWebSocket();
  const [username, setUsername] = useState("");
  const [isConnecting, setIsConnecting] = useState(false);

  useEffect(() => {
    if (!socket) return;

    const handleOpen = () => {
      console.log('🟢 Connection established');
    };

    const handleMessage = (event) => {
      const data = event.data;
      const splitData = data.split(':');
      const message = splitData[0];
      console.log(data);
      
      setIsConnecting(false);
      
      if (message === 'connection_established') {
        navigate('/loading');
      } else if (data === 'connection_failed') {
        alert('Cannot find a game. Please try again later.');
      } else {
        alert('Unknown message received');
      }
    };

    socket.addEventListener('open', handleOpen);
    socket.addEventListener('message', handleMessage);

    return () => {
      socket.removeEventListener('open', handleOpen);
      socket.removeEventListener('message', handleMessage);
    };
  }, [socket, navigate]);

  const joinQueue = () => {
    if (!username.trim()) {
      // Animation pour secouer l'input si vide
      const input = document.getElementById('username');
      input.classList.add('shake');
      setTimeout(() => input.classList.remove('shake'), 500);
      return;
    }
    
    setIsConnecting(true);
    socket.send('join_queue:' + username);
    console.log('📤 Sent:', 'join_queue:' + username);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      joinQueue();
    }
  };

  return (
    <div className="App">
      <div className="animated-bg"></div>
      <header className="App-header">
        <h1>Tic Tac Toe</h1>
        <p className="subtitle">Challenge players online!</p>
        
        <div className="input-container">
          <input 
            type="text" 
            placeholder="Enter your username" 
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            onKeyPress={handleKeyPress}
            autoFocus
          />
        </div>
        
        <button 
          onClick={joinQueue}
          disabled={isConnecting}
          className={isConnecting ? "connecting" : ""}
        >
          {isConnecting ? "Searching..." : "Play Now"}
        </button>
        
        {isConnecting && (
          <div className="loader">
            <div className="spinner"></div>
          </div>
        )}
      </header>
    </div>
  );
}

export default Home;