import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './Home';
import Loading from './Loading';
import Game from './Game';
import Win from './Win';
import Lose from './Lose';
import Draw from './Draw';
import { WebSocketProvider } from './WebSocket';

function App() {
  return (
    <WebSocketProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/loading" element={<Loading />} />
          <Route path="/game" element={<Game />} />
          <Route path="/win" element={<Win />} />
          <Route path="/lose" element={<Lose />} />
          <Route path="/draw" element={<Draw />} />
        </Routes>
      </Router>
    </WebSocketProvider>
  );
}

export default App;