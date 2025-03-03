import './App.css';

const socket = new WebSocket('ws://127.0.0.1:8000/ws');
socket.addEventListener('open', function (event) {
    socket.send('Connection Established');
});

socket.addEventListener('message', function (event) {
    console.log(event.data);
});
const contactServer = () => {
    socket.send("Initialize");
}

function App() {
  return (
    <button onClick={contactServer}>Contact Server</button>
  );
}

export default App;
