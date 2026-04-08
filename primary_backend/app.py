from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
import json
import time
import threading
import random
import os
import sys

# Ensure AI and Backend modules are in path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(BASE_DIR))

from routing import NetworkGraph, Router
from ai_model.predictor import TrafficPredictor

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Load Topology
TOPOLOGY_PATH = os.path.join(BASE_DIR, 'topology.json')
with open(TOPOLOGY_PATH) as f:
    topology = json.load(f)

# Initialize System
predictor = TrafficPredictor()
graph = NetworkGraph(topology)

class TrafficSystem:
    def __init__(self):
        self.is_attack = False

    def get_current_state(self):
        # Initial Shortest Path is static (based on initial network conditions)
        initial_path, initial_cost, _ = Router.dijkstra(graph, "A", "C", use_dynamic_costs=False)
        # Optimized path is dynamic and accounts for AI-predicted congestion
        new_path, new_cost, congested = Router.dijkstra(graph, "A", "C", predictor, use_dynamic_costs=True)
        return {
            'topology': topology,
            'initial_path': initial_path,
            'initial_cost': initial_cost,
            'new_path': new_path,
            'new_cost': new_cost,
            'congested_edges': list(set(congested))
        }

    def update_traffic(self):
        while True:
            # Simulate real-time traffic updates
            for edge in topology['edges']:
                # Targeted attack: only congest the primary path (A-B and B-C)
                is_target = (edge['from'] == 'A' and edge['to'] == 'B') or (edge['from'] == 'B' and edge['to'] == 'C')
                
                if self.is_attack and is_target:
                    edge['traffic'] = random.randint(85, 100)
                    edge['latency'] = random.randint(60, 100)
                    edge['packet_loss'] = random.uniform(5, 10)
                else:
                    # Normal traffic for other nodes or during non-attack
                    edge['traffic'] = random.randint(10, 40)
                    edge['latency'] = random.randint(5, 15)
                    edge['packet_loss'] = random.uniform(0, 1.5)
            
            socketio.emit('traffic_update', self.get_current_state())
            time.sleep(2)

system = TrafficSystem()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    res = predictor.predict(
        data.get('traffic'),
        data.get('latency'),
        data.get('bandwidth'),
        data.get('packet_loss')
    )
    return jsonify({'congestion_prediction': res})

@app.route('/route')
def get_route():
    path, cost, _ = Router.dijkstra(graph, "A", "C", predictor)
    return jsonify({'path': path, 'total_cost': cost})

@app.route('/topology')
def get_topology():
    return jsonify(topology)

@socketio.on('connect')
def handle_connect():
    print("Client connected, sending initial state...")
    emit('traffic_update', system.get_current_state())

@socketio.on('toggle_simulation')
def toggle(data):
    system.is_attack = data.get('active', False)
    emit('simulation_status', {'active': system.is_attack}, broadcast=True)

if __name__ == '__main__':
    threading.Thread(target=system.update_traffic, daemon=True).start()
    socketio.run(app, port=5000, host='0.0.0.0')
