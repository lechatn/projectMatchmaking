import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './Home';
import Loading from './Loading';
import Game from './Game';
import { WebSocketProvider } from './WebSocket';

function App() {
  return (
    <WebSocketProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/loading" element={<Loading />} />
          <Route path="/game" element={<Game />} />
        </Routes>
      </Router>
    </WebSocketProvider>
  );
}

export default App;