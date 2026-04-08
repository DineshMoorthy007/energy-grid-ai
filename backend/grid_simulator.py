import networkx as nx
import random
from typing import Dict, Any, List

class GridSimulator:
    def __init__(self):
        self.graph = nx.Graph()
        self._initialize_grid()

    def _initialize_grid(self):
        """Creates the initial graph representing substations (nodes) and power lines (edges)."""
        self.graph.add_node(0, type="source", label="Main Power Plant", capacity=5000, current_load=0)
        
        # Define 3 Main Zones as specified
        self.graph.add_node(1, type="substation", label="Zone A Substation", capacity=100, current_load=0)
        self.graph.add_node(2, type="substation", label="Zone B Substation", capacity=120, current_load=0)
        self.graph.add_node(3, type="substation", label="Zone C Substation", capacity=80, current_load=0)
        
        # Local distribution nodes for each zone
        self.graph.add_node(4, type="local", label="Zone A Residential", capacity=60, current_load=0)
        self.graph.add_node(5, type="local", label="Zone A Commercial", capacity=40, current_load=0)
        
        self.graph.add_node(6, type="local", label="Zone B Residential", capacity=50, current_load=0)
        self.graph.add_node(7, type="local", label="Zone B Industrial", capacity=70, current_load=0)
        
        self.graph.add_node(8, type="local", label="Zone C Residential", capacity=40, current_load=0)
        self.graph.add_node(9, type="local", label="Zone C Rural", capacity=40, current_load=0)

        # Edges (Power lines)
        edges = [
            (0, 1, 300), (0, 2, 300), (0, 3, 300),
            (1, 4, 60), (1, 5, 40),
            (2, 6, 50), (2, 7, 70),
            (3, 8, 40), (3, 9, 40),
            (1, 2, 50), (2, 3, 50) # cross-zone ties
        ]
        
        for u, v, cap in edges:
            self.graph.add_edge(u, v, capacity=cap, current_flow=0)

    def get_grid_state(self) -> Dict[str, Any]:
        """Returns the current state of the grid"""
        nodes = []
        for node, data in self.graph.nodes(data=True):
            load = data.get("current_load", 0)
            cap = data.get("capacity", 0)
            nodes.append({
                "id": node,
                "label": data.get("label", str(node)),
                "type": data.get("type", "unknown"),
                "capacity": cap,
                "current_load": round(load, 2),
                # Dynamic Thresholds
                "overloaded": load > (cap * 0.85),
                "underutilized": load < (cap * 0.4) if cap > 0 and node != 0 else False
            })
            
        links = []
        for u, v, data in self.graph.edges(data=True):
            links.append({
                "source": u,
                "target": v,
                "capacity": data.get("capacity", 0),
                "current_flow": round(data.get("current_flow", 0), 2),
                "overloaded": data.get("current_flow", 0) > (data.get("capacity", 0) * 0.85)
            })
            
        return {"nodes": nodes, "links": links}

    def simulate_load_distribution(self, total_demand: float) -> Dict[str, Any]:
        """
        Distributes the total predicted demand across local nodes and updates the graph state.
        This provides the unoptimized baseline before quantum optimization.
        """
        # Reset current loads and flows
        for n in self.graph.nodes:
            self.graph.nodes[n]['current_load'] = 0
            
        for u, v in self.graph.edges:
            self.graph.edges[u, v]['current_flow'] = 0

        # Distribution logic proportional to capacities
        local_nodes = [n for n, d in self.graph.nodes(data=True) if d.get('type') == 'local']
        total_local_cap = sum(self.graph.nodes[n]['capacity'] for n in local_nodes)
        
        # We assign load based on capacity fraction and a bit of random noise
        for n in local_nodes:
            cap = self.graph.nodes[n]['capacity']
            base_fraction = cap / total_local_cap
            # simulate different zones reacting slightly differently (+/- 20% noise)
            noise_factor = random.uniform(0.8, 1.2)
            load = total_demand * base_fraction * noise_factor
            self.graph.nodes[n]['current_load'] = load
            
        # Simulate unoptimized flow (shortest path from source to each local node)
        for n in local_nodes:
            load = self.graph.nodes[n]['current_load']
            if load > 0:
                try:
                    path = nx.shortest_path(self.graph, source=0, target=n)
                    for idx in range(len(path) - 1):
                        u, v = path[idx], path[idx+1]
                        if v != n:
                            self.graph.nodes[v]['current_load'] += load
                        self.graph.edges[u, v]['current_flow'] += load
                except nx.NetworkXNoPath:
                    pass

        return self.get_grid_state()

# Singleton instance
grid_simulator = GridSimulator()

def create_grid() -> Dict[str, Any]:
    return grid_simulator.get_grid_state()

def simulate_load_distribution(total_demand: float) -> Dict[str, Any]:
    return grid_simulator.simulate_load_distribution(total_demand)
