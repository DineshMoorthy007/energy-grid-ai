from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from enum import Enum

class ActionEnum(str, Enum):
    NORMAL = "NORMAL"
    OPTIMIZED = "OPTIMIZED"
    CRITICAL = "CRITICAL"
    LOW_DEMAND = "LOW_DEMAND"

class RouteDecision(BaseModel):
    route_id: int
    quantum_state: int

class PredictionResponse(BaseModel):
    demand: float
    action: str
    optimized_routes: List[RouteDecision]
    explanation: str
    grid_state: Dict[str, Any]

class GridAction(BaseModel):
    hour: int
    temperature: float
