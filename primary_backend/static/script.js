const socket = io({
    transports: ['websocket'],
    upgrade: false
});

let network = null;
let isSimActive = false;

const simBtn = document.getElementById('sim-btn');
const initialPathEl = document.getElementById('initial-path');
const optimizedPathEl = document.getElementById('optimized-path');
const initialCostEl = document.getElementById('initial-cost');
const optimizedCostEl = document.getElementById('optimized-cost');
const congestedListEl = document.getElementById('congested-list');

// Initialize map on load
window.onload = async () => {
    const response = await fetch('/topology');
    const topology = await response.json();
    console.log("Initial Topology Loaded");
    drawNetwork(topology, ["A", "B", "C"], ["A", "B", "C"], []);
};

function drawNetwork(topology, initialPath, optimizedPath, congestedEdges) {
    const container = document.getElementById('network-map');
    if (!container) return;

    const nodes = topology.nodes.map(node => ({
        ...node,
        color: optimizedPath.includes(node.id) ? '#4ade80' : 
               (initialPath.includes(node.id) ? '#94a3b8' : '#38bdf8'),
        font: { color: '#ffffff' },
        size: optimizedPath.includes(node.id) ? 35 : 25
    }));

    const edges = topology.edges.map(edge => {
        const edgeId = `${edge.from}-${edge.to}`;
        const reverseEdgeId = `${edge.to}-${edge.from}`;
        const isCongested = congestedEdges.includes(edgeId) || congestedEdges.includes(reverseEdgeId);
        
        let inOptimized = false;
        for (let i = 0; i < optimizedPath.length - 1; i++) {
            if ((optimizedPath[i] === edge.from && optimizedPath[i + 1] === edge.to) || 
                (optimizedPath[i] === edge.to && optimizedPath[i + 1] === edge.from)) {
                inOptimized = true;
                break;
            }
        }

        return {
            ...edge,
            label: edge.traffic ? `T:${edge.traffic}%` : '',
            color: isCongested ? '#f87171' : (inOptimized ? '#4ade80' : '#475569'),
            width: inOptimized ? 5 : (isCongested ? 3 : 1),
            dashes: isCongested,
            arrows: inOptimized ? 'to' : ''
        };
    });

    const data = { nodes: new vis.DataSet(nodes), edges: new vis.DataSet(edges) };
    const options = {
        physics: { enabled: true, stabilization: true },
        nodes: { shape: 'dot' },
        edges: { smooth: { type: 'continuous' }, font: { size: 10, color: '#94a3b8', strokeWidth: 0 } }
    };

    if (!network) {
        network = new vis.Network(container, data, options);
    } else {
        network.setData(data);
    }
}

socket.on('traffic_update', (data) => {
    console.log("Update received:", data);
    initialPathEl.innerText = data.initial_path ? data.initial_path.join(' → ') : '...';
    optimizedPathEl.innerText = data.new_path ? data.new_path.join(' → ') : '...';
    initialCostEl.innerText = data.initial_cost || 0;
    
    // Handle high cost display
    const cost = data.new_cost;
    optimizedCostEl.innerText = cost > 1000 ? 'Rerouted' : (cost || 0);
    
    congestedListEl.innerText = data.congested_edges.length > 0 ? 
                                `Avoided: ${data.congested_edges.join(', ')}` : 'No congestion predicted';

    drawNetwork(data.topology, data.initial_path, data.new_path, data.congested_edges);
});

socket.on('simulation_status', (data) => {
    isSimActive = data.active;
    simBtn.innerText = isSimActive ? 'Stop Simulation' : 'Start Simulation';
    simBtn.className = `btn ${isSimActive ? 'btn-danger' : 'btn-primary'}`;
});

simBtn.addEventListener('click', () => {
    socket.emit('toggle_simulation', { active: !isSimActive });
});
