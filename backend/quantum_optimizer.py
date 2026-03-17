import random
from typing import Dict, Any, List

# Try to import qiskit, but provide a fallback if it's not installed/available for some reason
try:
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False

class QuantumOptimizer:
    def __init__(self):
        self.simulator = AerSimulator() if QISKIT_AVAILABLE else None

    def _quantum_solve(self, nodes: List[Dict], edges: List[Dict]) -> List[int]:
        """
        A simplified QAOA-style approach to find the optimal paths.
        Since a full QAOA for load balancing requires complex mapping, we simulate
        a quantum circuit that generates probability distributions for routing decisions.
        """
        # We need as many qubits as we have "decisions" or a subset of key decision variables.
        # For simplicity, we create a small circuit that generates random bits to represent
        # quantum superposition of states.
        num_qubits = min(len(nodes), 10)  # limit to 10 qubits for speed
        
        qc = QuantumCircuit(num_qubits, num_qubits)
        # Apply Hadamard gates to create superposition
        for i in range(num_qubits):
            qc.h(i)
            
        # Add some entanglement
        for i in range(num_qubits - 1):
            qc.cx(i, i+1)
            
        # Measure
        qc.measure(range(num_qubits), range(num_qubits))
        
        # Run simulation
        result = self.simulator.run(qc, shots=1).result()
        counts = result.get_counts()
        
        # The result key is a string like '0101...', we use it to influence our classical algorithm
        selected_state = list(counts.keys())[0]
        # Convert to list of ints
        decision_vector = [int(bit) for bit in selected_state]
        
        return decision_vector

    def _classical_fallback(self, nodes: List[Dict], edges: List[Dict]) -> List[int]:
        """Fallback in case Qiskit isn't available."""
        num_decisions = min(len(nodes), 10)
        return [random.choice([0, 1]) for _ in range(num_decisions)]

    def optimize_energy_distribution(self, grid_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Takes the unoptimized grid state and applies a quantum-inspired optimization
        to find better routes and prevent node/edge overloading.
        """
        nodes = grid_state.get('nodes', [])
        edges = grid_state.get('links', [])
        
        # 1. Get a "quantum decision vector" 
        if QISKIT_AVAILABLE and self.simulator:
            try:
                decision_vector = self._quantum_solve(nodes, edges)
                method_used = "Qiskit Quantum Circuit Simulation"
            except Exception as e:
                print(f"Quantum error: {e}")
                decision_vector = self._classical_fallback(nodes, edges)
                method_used = "Classical Fallback (Exception)"
        else:
            decision_vector = self._classical_fallback(nodes, edges)
            method_used = "Classical Fallback (Qiskit Unavailable)"

        optimized_nodes = []
        optimized_links = []
        overloaded_count = 0
        total_load_balanced = 0

        # Simulate the "optimization" by adjusting loads based on the decision vector
        # Heuristic: if a node has high load and the quantum bit is 1, divert load.
        for i, node in enumerate(nodes):
            new_node = node.copy()
            
            # Simple balancing logic
            if new_node.get('current_load', 0) > new_node.get('capacity', 0):
                # We need to shed load
                shed_amount = new_node['current_load'] - new_node['capacity']
                
                # Use quantum bit to decide how aggressively to shed/re-route
                q_bit_idx = i % len(decision_vector)
                q_bit = decision_vector[q_bit_idx]
                
                if q_bit == 1:
                    # aggressive shed
                    new_node['current_load'] -= shed_amount * 0.9
                    total_load_balanced += shed_amount * 0.9
                else:
                    # conservative shed
                    new_node['current_load'] -= shed_amount * 0.5
                    total_load_balanced += shed_amount * 0.5
                    
            # Update overloaded flag
            is_overloaded = new_node.get('current_load', 0) > new_node.get('capacity', 0)
            new_node['overloaded'] = is_overloaded
            if is_overloaded:
                overloaded_count += 1
                
            new_node['current_load'] = round(new_node['current_load'], 2)
            optimized_nodes.append(new_node)
            
        for i, link in enumerate(edges):
            new_link = link.copy()
            if new_link.get('current_flow', 0) > new_link.get('capacity', 0):
                # Shed flow
                shed_amount = new_link['current_flow'] - new_link['capacity']
                q_bit_idx = i % len(decision_vector)
                
                if decision_vector[q_bit_idx] == 1:
                    new_link['current_flow'] -= shed_amount * 0.8
                else:
                    new_link['current_flow'] -= shed_amount * 0.4
                    
            is_overloaded = new_link.get('current_flow', 0) > new_link.get('capacity', 0)
            new_link['overloaded'] = is_overloaded
            new_link['current_flow'] = round(new_link['current_flow'], 2)
            optimized_links.append(new_link)

        return {
            "optimized_grid": {
                "nodes": optimized_nodes,
                "links": optimized_links
            },
            "metrics": {
                "overloaded_substations_after": overloaded_count,
                "total_load_balanced_mw": round(total_load_balanced, 2),
                "optimization_method": method_used,
                "quantum_decision_vector": decision_vector
            }
        }

# Singleton instance
quantum_optimizer = QuantumOptimizer()

def optimize_energy_distribution(grid_state: Dict[str, Any]) -> Dict[str, Any]:
    return quantum_optimizer.optimize_energy_distribution(grid_state)
