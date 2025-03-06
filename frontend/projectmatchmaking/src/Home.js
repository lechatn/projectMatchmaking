import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const socket = new WebSocket("ws://127.0.0.1:8000/ws");

const Home = () => {
  const [username, setUsername] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    socket.addEventListener("open", () => {
      console.log("✅ Connexion WebSocket établie");
    });

    socket.addEventListener("message", (event) => {
      console.log("📩 Message reçu :", event.data);
      if (event.data === "match_found") {
        navigate("/game"); // 🔀 Redirige vers la page du jeu
      } else if (event.data === "connection_failed") {
        alert("❌ Aucun match trouvé, réessayez plus tard.");
      }
    });

    return () => socket.close();
  }, []);

  const joinQueue = () => {
    if (username.trim() === "") {
      alert("Entrez un pseudo !");
      return;
    }
    socket.send("join_queue:" + username);
    console.log("📤 Envoyé :", "join_queue:" + username);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎮 Project Matchmaking</h1>
        <input
          type="text"
          placeholder="Enter your username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <button onClick={joinQueue}>Search for a game</button>
      </header>
    </div>
  );
};

export default Home;
