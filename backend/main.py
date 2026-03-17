from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from schemas import PredictionResponse
from decision_engine import process_energy_request

app = FastAPI(
    title="AI + Quantum Smart Energy Grid Optimizer",
    description="Predicts energy demand using AI and optimizes power distribution using quantum-inspired optimization.",
    version="1.0.0"
)

# CORS configuration to allow frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI + Quantum Smart Energy Grid Optimizer API"}

@app.get("/predict", response_model=PredictionResponse)
def predict(
    hour: int = Query(..., ge=0, le=23, description="Hour of the day (0-23)"),
    temp: float = Query(..., description="Temperature in Celsius")
):
    """
    Predicts energy demand and returns the optimized grid state and action recommendations.
    """
    response = process_energy_request(hour, temp)
    return response

if __name__ == "__main__":
    # Provides setup instructions when run directly
    print("Starting AI + Quantum Smart Energy Grid Optimizer Backend...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
