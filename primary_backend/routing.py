import heapq

class NetworkGraph:
    def __init__(self, topology):
        self.nodes = [node['id'] for node in topology['nodes']]
        self.topology = topology
        self.adj = self._build_adj()

    def _build_adj(self):
        adj = {node: {} for node in self.nodes}
        for edge in self.topology['edges']:
            # For simplicity, treat edges as undirected and use latency or traffic as base cost
            cost = edge.get('latency', 10) 
            adj[edge['from']][edge['to']] = {'cost': cost, 'data': edge}
            adj[edge['to']][edge['from']] = {'cost': cost, 'data': edge}
        return adj

class Router:
    @staticmethod
    def dijkstra(graph, start, end, predictor=None, use_dynamic_costs=True):
        queue = [(0, start, [])]
        visited = set()
        min_costs = {node: float('inf') for node in graph.nodes}
        min_costs[start] = 0

        congested_edges = []

        while queue:
            (cost, current_node, path) = heapq.heappop(queue)

            if current_node in visited:
                continue

            visited.add(current_node)
            path = path + [current_node]

            if current_node == end:
                return path, cost, congested_edges

            for neighbor, info in graph.adj[current_node].items():
                if neighbor in visited:
                    continue

                edge_data = info['data']
                # Use real-time latency as base cost if dynamic, otherwise use initial static cost
                if use_dynamic_costs:
                    edge_cost = edge_data.get('latency', 10) 
                else:
                    edge_cost = info['cost']
                
                # AI Congestion Check
                is_congested = 0
                if predictor:
                    is_congested = predictor.predict(
                        edge_data.get('traffic', 0),
                        edge_data.get('latency', 0),
                        edge_data.get('bandwidth', 100),
                        edge_data.get('packet_loss', 0)
                    )
                
                if is_congested:
                    congested_edges.append(f"{current_node}-{neighbor}")
                    # Penalize congested edges heavily (Dynamic Routing)
                    edge_cost += 1000 
                
                new_cost = cost + edge_cost
                if new_cost < min_costs[neighbor]:
                    min_costs[neighbor] = new_cost
                    heapq.heappush(queue, (new_cost, neighbor, path))

        return None, float('inf'), congested_edges
