import React from 'react';
import { useLocation } from 'react-router-dom';

const Game = () => {
  const location = useLocation();
  const playAgainst = location.state?.playAgainst;

  return (
    <div className="Game">
      <h1>Welcome to the Game!</h1>
      <p>You're playing against: {playAgainst}</p>
    </div>
  );
};

export default Game;
