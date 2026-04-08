from typing import Dict, Any
from schemas import PredictionResponse, GridAction
from demand_model import predict_demand
from grid_simulator import simulate_load_distribution
from quantum_optimizer import optimize_energy_distribution
import json

class DecisionEngine:
    
    def generate_explanation(self, demand: float, temp: float, hour: int, overloaded: list, underutilized: list) -> str:
        """Dynamic Explanation Generator based on inputs and grid state."""
        hour_context = "peak evening hours" if 17 <= hour <= 22 else "morning hours" if 6 <= hour <= 9 else "nighttime operations" if 0 <= hour <= 5 else "standard daytime hours"
        temp_context = f"elevated temperature ({temp}°C)" if temp > 25 else f"low temperature ({temp}°C)" if temp < 15 else f"moderate temperature ({temp}°C)"
        
        if len(overloaded) > 0:
            zones = ", ".join([n['label'] for n in overloaded[:2]]) + (" and others" if len(overloaded)>2 else "")
            return f"{zones} reached critical capacity limits. High demand ({round(demand, 1)} MW) is driven by {hour_context} and {temp_context}."
        elif len(underutilized) > 0 and demand < 120:
            zones = ", ".join([n['label'] for n in underutilized[:2]]) + (" and others" if len(underutilized)>2 else "")
            return f"Demand is very low ({round(demand, 1)} MW) during {hour_context}. Grid is functioning normally with {zones} operating below 40% capacity."
        else:
            return f"Grid is balanced and operating safely. Moderate demand of {round(demand, 1)} MW during {hour_context} is being handled reliably under {temp_context}."

    def process(self, hour: int, temperature: float) -> PredictionResponse:
        # 1. Provide AI Prediction
        predicted_demand = predict_demand(hour, temperature)
        print(f"[DEBUG] Input -> Hour: {hour}, Temp: {temperature} | Predicted Demand: {round(predicted_demand, 2)} MW")
        
        # 2. Simulate Distribution across Grid zones
        unoptimized_grid = simulate_load_distribution(predicted_demand)
        
        # 3. Detect state (overload > 0.85, underutilized < 0.40)
        nodes = unoptimized_grid['nodes']
        overloaded = [n for n in nodes if n['overloaded'] and n['type'] in ['substation', 'local']]
        underutilized = [n for n in nodes if n['underutilized'] and n['type'] in ['substation', 'local']]
        
        print(f"[DEBUG] Grid Status -> Overloaded nodes: {len(overloaded)} | Underutilized nodes: {len(underutilized)}")

        # 4. Determine Action & Optimize if needed
        status = "MAINTAIN_STATE"
        optimized_grid = unoptimized_grid
        metrics = {"quantum_decision_vector": []}
        
        if len(overloaded) > 0:
            status = "SHIFT_LOAD"
            # Quantum Optimization reroutes power away from overloaded zones
            optimization_result = optimize_energy_distribution(unoptimized_grid)
            optimized_grid = optimization_result["optimized_grid"]
            metrics = optimization_result["metrics"]
            
            # After optimization, check remaining overloads
            final_overloads = [n for n in optimized_grid['nodes'] if n['overloaded']]
            if len(final_overloads) > 0:
                status = "CRITICAL_REDISTRIBUTION"
                
        elif len(underutilized) > 2:
            status = "REDISTRIBUTE_ENERGY"
            
        # 5. Dynamic Explanation and Recommendation
        explanation = self.generate_explanation(predicted_demand, temperature, hour, overloaded, underutilized)
        
        if status == "CRITICAL_REDISTRIBUTION":
            recommendation = "Activate cross-zone tie lines manually to bypass failed substations."
        elif status == "SHIFT_LOAD":
            recommendation = "AI rerouting power dynamically to adjacent non-active nodes via Quantum QAOA vector."
        elif status == "REDISTRIBUTE_ENERGY":
            recommendation = "Entering power-saving mode. Grid lines optimized for low-vibration transit."
        else:
            recommendation = "Grid parameters stable. Maintain current routing logic."
            
        q_vector = metrics.get('quantum_decision_vector', [])
        
        return PredictionResponse(
            predicted_demand=round(predicted_demand, 2),
            grid_status=status,
            recommendation=recommendation,
            optimized_routes=[{"route_id": i, "quantum_state": state} for i, state in enumerate(q_vector)],
            explanation=explanation,
            grid_state=optimized_grid
        )

# Singleton instance
decision_engine = DecisionEngine()

def process_energy_request(hour: int, temperature: float) -> PredictionResponse:
    return decision_engine.process(hour, temperature)
