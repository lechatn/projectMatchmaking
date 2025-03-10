// filepath: c:\Users\lecha\OneDrive - Ynov\Bureau\Ynov\B2\projectMatchmaking\frontend\projectmatchmaking\src\Loading.js
import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useWebSocket } from './WebSocket';
import { dotSpinner } from 'ldrs';

const Loading = () => {
  const navigate = useNavigate();
  const socket = useWebSocket();

  dotSpinner.register()

  useEffect(() => {
    if (!socket) return;

    const handleOpen = () => {
      console.log("🟢 Connection established");
    };

    const handleMessage = (event) => {
      const data = event.data;
      const splitData = data.split(":");
      const message = splitData[0];
      const playAgainst = splitData[1];
      const hostId = splitData[2];
      const opponentId = splitData[3];
      console.log(data);
      if (message === "game_started") {
        navigate("/game", { state: { playAgainst, hostId, opponentId } });
      } else if (data === "connection_failed") {
        alert("Cannot find a game. Please try again later.");
      } else {
        alert("Unknown message received");
      }
    };

    socket.addEventListener('open', handleOpen);
    socket.addEventListener('message', handleMessage);

    return () => {
      socket.removeEventListener('open', handleOpen);
      socket.removeEventListener('message', handleMessage);
    };
  }, [socket, navigate]);

  const LeaveGame = () => {
    socket.send('leave_queue');
    navigate('/');
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>🕹️ En recherche de match...</h1>
        <button onClick={ LeaveGame }>Quitter la recherche</button>
      </header>
    </div>
  );
};

export default Loading;