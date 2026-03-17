from typing import Dict, Any
from schemas import PredictionResponse, GridAction
from demand_model import predict_demand
from grid_simulator import simulate_load_distribution, create_grid
from quantum_optimizer import optimize_energy_distribution

class DecisionEngine:
    def process(self, hour: int, temperature: float) -> PredictionResponse:
        # 1. AI Prediction
        predicted_demand = predict_demand(hour, temperature)
        
        # 2. Unoptimized Grid Simulation
        unoptimized_grid = simulate_load_distribution(predicted_demand)
        
        # 3. Quantum Optimization
        optimization_result = optimize_energy_distribution(unoptimized_grid)
        optimized_grid = optimization_result["optimized_grid"]
        metrics = optimization_result["metrics"]
        
        # 4. Determine Action & Explanation
        action = "NORMAL"
        explanation = "The grid is operating within normal parameters. AI predicted moderate demand."
        
        if metrics["total_load_balanced_mw"] > 0:
            if metrics["overloaded_substations_after"] > 0:
                action = "CRITICAL"
                explanation = f"AI predicted high demand ({round(predicted_demand, 2)} MW). Quantum optimization rerouted {metrics['total_load_balanced_mw']} MW of power, but {metrics['overloaded_substations_after']} substations remain overloaded. Manual intervention required."
            else:
                action = "OPTIMIZED"
                explanation = f"AI predicted high demand ({round(predicted_demand, 2)} MW). Quantum optimizer effectively rerouted {metrics['total_load_balanced_mw']} MW of power to prevent grid failure and balance the load."
        elif predicted_demand < 50:
            action = "LOW_DEMAND"
            explanation = f"AI predicted very low demand ({round(predicted_demand, 2)} MW). Excess capacity available for storage or maintenance."
            
        # Extract some routes or decisions for the frontend to show
        q_vector = metrics.get('quantum_decision_vector', [])
        
        return PredictionResponse(
            demand=round(predicted_demand, 2),
            action=action,
            optimized_routes=[{"route_id": i, "quantum_state": state} for i, state in enumerate(q_vector)],
            explanation=explanation,
            grid_state=optimized_grid
        )

# Singleton instance
decision_engine = DecisionEngine()

def process_energy_request(hour: int, temperature: float) -> PredictionResponse:
    return decision_engine.process(hour, temperature)
