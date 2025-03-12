import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './Result.css';

const Win = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const winner = location.state?.winner || "You";

  return (
    <div className="result-page win">
      <h1>🎉 Congratulations! 🎉</h1>
      <p>{winner} won the game!</p>
      <button onClick={() => navigate('/loading')}>Play Again</button>
      <button onClick={() => navigate('/')}>Go Home</button>
    </div>
  );
};

export default Win;
