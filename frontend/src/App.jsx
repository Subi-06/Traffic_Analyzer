import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import NetworkMap from './components/NetworkMap';
import './App.css';

const socket = io('http://localhost:5000');

function App() {
  const [topology, setTopology] = useState(null);
  const [traffic, setTraffic] = useState({ level: 0, status: 'Loading...', path: [] });
  const [isAttack, setIsAttack] = useState(false);

  useEffect(() => {
    fetch('http://localhost:5000/topology')
      .then(res => res.json())
      .then(data => setTopology(data));

    socket.on('traffic_data', (data) => {
      setTraffic(data);
    });

    socket.on('attack_status', (data) => {
      setIsAttack(data.active);
    });

    return () => {
      socket.off('traffic_data');
      socket.off('attack_status');
    };
  }, []);

  const toggleAttack = () => {
    socket.emit('simulate_attack', { active: !isAttack });
  };

  return (
    <div className="App">
      <header>
        <h1>Network Traffic Prediction & Self-healing</h1>
        <div className="status-bar">
          <div className="status-item">
             <span>Congestion:</span> 
             <span className="value" style={{ color: traffic.level > 0.8 ? 'red' : 'green' }}>
               {(traffic.level * 100).toFixed(1)}%
             </span>
          </div>
          <div className="status-item">
             <span>Status:</span> 
             <span className="value">{traffic.status}</span>
          </div>
        </div>
      </header>

      <main>
        <div className="controls">
          <button 
            className={`attack-btn ${isAttack ? 'active' : ''}`}
            onClick={toggleAttack}
          >
            {isAttack ? 'Stop Attack' : 'Simulate Attack'}
          </button>
        </div>

        <NetworkMap 
          topology={topology} 
          path={traffic.path} 
          congestion={traffic.level} 
        />
        
        <div className="path-info">
          <h3>Active Route:</h3>
          <p>{traffic.path.join(' → ')}</p>
        </div>
      </main>
    </div>
  );
}

export default App;
