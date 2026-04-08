from pydantic import BaseModel
from typing import List, Dict, Any

class RouteDecision(BaseModel):
    route_id: int
    quantum_state: int

class PredictionResponse(BaseModel):
    predicted_demand: float
    grid_status: str
    recommendation: str
    optimized_routes: List[RouteDecision]
    explanation: str
    grid_state: Dict[str, Any]

class GridAction(BaseModel):
    hour: int
    temperature: float
