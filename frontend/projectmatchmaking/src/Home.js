import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./Home.css";
import './App.css';
import { useWebSocket } from './WebSocket';

function Home() {
  const navigate = useNavigate();
  const socket = useWebSocket();

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
    const username = document.getElementById('username').value;
    socket.send('join_queue:' + username);
    console.log('📤 Sent:', 'join_queue:' + username);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Project Matchmaking</h1>
        <input type="text" placeholder="Enter your username" id="username" />
        <button onClick={joinQueue}>Search for a game</button>
      </header>
    </div>
  );
}

export default Home;