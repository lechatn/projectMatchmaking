import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Result.css';

const Lose = () => {
  const navigate = useNavigate();

  return (
    <div className="result-page lose">
      <h1>😢 You Lost!</h1>
      <p>Better luck next time!</p>
      <button onClick={() => navigate('/loading')}>Try Again</button>
      <button onClick={() => navigate('/')}>Go Home</button>
    </div>
  );
};

export default Lose;
