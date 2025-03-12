import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Result.css';

const Draw = () => {
  const navigate = useNavigate();

  return (
    <div className="result-page draw">
      <h1>🤝 It's a Draw!</h1>
      <p>No winners this time!</p>
      <button onClick={() => navigate('/loading')}>Play Again</button>
      <button onClick={() => navigate('/')}>Go Home</button>
    </div>
  );
};

export default Draw;
