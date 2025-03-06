// filepath: c:\Users\lecha\OneDrive - Ynov\Bureau\Ynov\B2\projectMatchmaking\frontend\projectmatchmaking\src\WebSocketContext.js
import React, { createContext, useContext, useEffect, useState } from 'react';

const WebSocketContext = createContext(null);

export const WebSocketProvider = ({ children }) => {
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    const newSocket = new WebSocket('ws://127.0.0.1:8000/ws');
    setSocket(newSocket);

    newSocket.addEventListener('open', () => {
      console.log('🟢 Connection established');
    });

    newSocket.addEventListener('close', () => {
      console.log('❌ Connection closed');
    });

    return () => {
      newSocket.close();
    };
  }, []);

  return (
    <WebSocketContext.Provider value={socket}>
      {children}
    </WebSocketContext.Provider>
  );
};

export const useWebSocket = () => {
  return useContext(WebSocketContext);
};