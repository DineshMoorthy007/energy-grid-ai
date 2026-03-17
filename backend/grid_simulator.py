import networkx as nx
import random
from typing import Dict, Any, List

class GridSimulator:
    def __init__(self):
        self.graph = nx.Graph()
        self._initialize_grid()

    def _initialize_grid(self):
        """Creates the initial graph representing substations (nodes) and power lines (edges)."""
        # Create a realistic generic grid topology (e.g., small world or custom)
        # Let's define specific nodes for visual consistency
        
        # Main power source or central hubs
        self.graph.add_node(0, type="source", label="Main Power Plant", capacity=10000, current_load=0)
        
        # Distribution Substations
        self.graph.add_node(1, type="substation", label="North Substation", capacity=200, current_load=0)
        self.graph.add_node(2, type="substation", label="East Substation", capacity=250, current_load=0)
        self.graph.add_node(3, type="substation", label="South Substation", capacity=180, current_load=0)
        self.graph.add_node(4, type="substation", label="West Substation", capacity=200, current_load=0)
        
        # Local distribution nodes
        for i in range(5, 12):
            self.graph.add_node(i, type="local", label=f"Local Grid {i}", capacity=100, current_load=0)

        # Edges (Power lines) defined as (node1, node2, capacity)
        edges = [
            (0, 1, 300), (0, 2, 300), (0, 3, 300), (0, 4, 300),
            (1, 5, 150), (1, 6, 150),
            (2, 6, 150), (2, 7, 150),
            (3, 8, 150), (3, 9, 150),
            (4, 10, 150), (4, 11, 150),
            # Interconnections to create loops (graph instead of tree)
            (1, 2, 100), (2, 3, 100), (3, 4, 100), (4, 1, 100),
            (5, 11, 50), (6, 7, 50), (8, 9, 50)
        ]
        
        for u, v, cap in edges:
            self.graph.add_edge(u, v, capacity=cap, current_flow=0)

    def get_grid_state(self) -> Dict[str, Any]:
        """Returns the current state of the grid as a dictionary for easy frontend rendering."""
        nodes = []
        for node, data in self.graph.nodes(data=True):
            nodes.append({
                "id": node,
                "label": data.get("label", str(node)),
                "type": data.get("type", "unknown"),
                "capacity": data.get("capacity", 0),
                "current_load": data.get("current_load", 0),
                "overloaded": data.get("current_load", 0) > data.get("capacity", 0)
            })
            
        links = []
        for u, v, data in self.graph.edges(data=True):
            links.append({
                "source": u,
                "target": v,
                "capacity": data.get("capacity", 0),
                "current_flow": data.get("current_flow", 0),
                "overloaded": data.get("current_flow", 0) > data.get("capacity", 0)
            })
            
        return {"nodes": nodes, "links": links}

    def simulate_load_distribution(self, total_demand: float) -> Dict[str, Any]:
        """
        Distributes the total predicted demand across local nodes and updates the graph state.
        This provides the unoptimized baseline before quantum optimization.
        """
        local_nodes = [n for n, d in self.graph.nodes(data=True) if d.get('type') == 'local']
        substation_nodes = [n for n, d in self.graph.nodes(data=True) if d.get('type') == 'substation']
        
        # Reset current loads and flows
        for n in self.graph.nodes:
            self.graph.nodes[n]['current_load'] = 0
            
        for u, v in self.graph.edges:
            self.graph.edges[u, v]['current_flow'] = 0

        # Randomly distribute demand to local nodes (adding some noise)
        remaining_demand = total_demand
        for i, n in enumerate(local_nodes):
            if i == len(local_nodes) - 1:
                load = remaining_demand
            else:
                # Assign a chunk of demand
                chunk = (total_demand / len(local_nodes)) * random.uniform(0.5, 1.5)
                load = min(chunk, remaining_demand)
                remaining_demand -= load
            self.graph.nodes[n]['current_load'] = round(load, 2)
            
        # Simulate unoptimized flow (shortest path from source to each local node)
        for n in local_nodes:
            load = self.graph.nodes[n]['current_load']
            if load > 0:
                try:
                    # Shortest path by generic weights (number of hops)
                    path = nx.shortest_path(self.graph, source=0, target=n)
                    for idx in range(len(path) - 1):
                        u, v = path[idx], path[idx+1]
                        # Accumulate load on nodes (except source 0)
                        if v != n:
                            self.graph.nodes[v]['current_load'] += load
                        # Accumulate flow on edges
                        self.graph.edges[u, v]['current_flow'] += load
                except nx.NetworkXNoPath:
                    pass

        return self.get_grid_state()

# Singleton instance for the app to use
grid_simulator = GridSimulator()

def create_grid() -> Dict[str, Any]:
    return grid_simulator.get_grid_state()

def simulate_load_distribution(total_demand: float) -> Dict[str, Any]:
    return grid_simulator.simulate_load_distribution(total_demand)
