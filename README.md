# AI + Quantum Smart Energy Grid Optimizer

This project is a full-stack application that uses an AI model to predict energy demand and a Quantum Inspired algorithm (using Qiskit) to optimize grid routing and balance loads across substations.

## Project Structure

- `backend/`: FastAPI application containing the AI model, Graph simulator, and Quantum Optimizer.
- `frontend/`: React + Vite application with Tailwind CSS, Recharts, and Force Graph for visualization.

## Prerequisites

- Node.js (v16+)
- Python (v3.10+)
- npm or yarn

---

## 🚀 Setup Instructions

### 1. Backend Setup

1. Open a terminal and navigate to the project root:
   ```bash
   cd "d:\1.2 Hackathons\Quantum_worshop\energy-grid-ai"
   ```
2. Create and activate a Virtual Environment:
   * Windows: 
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   * macOS/Linux: 
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
3. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
4. Run the Backend Server:
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   *The backend will be available at `http://localhost:8000`*
   *You can view the interactive API docs at `http://localhost:8000/docs`*

---

### 2. Frontend Setup

1. Open a new terminal and navigate to the frontend folder:
   ```bash
   cd "d:\1.2 Hackathons\Quantum_worshop\energy-grid-ai\frontend"
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the Frontend Development Server:
   ```bash
   npm run dev
   ```
   *The frontend will usually be accessible at `http://localhost:3000` or `http://localhost:5173`*

---

## 📡 Example API Call

You can test the backend independently using cURL:

```bash
curl -X 'GET' \
  'http://localhost:8000/predict?hour=14&temp=35' \
  -H 'accept: application/json'
```

### Response Format:
```json
{
  "demand": 112.45,
  "action": "CRITICAL",
  "optimized_routes": [
    {"route_id": 0, "quantum_state": 1},
    {"route_id": 1, "quantum_state": 0}
  ],
  "explanation": "AI predicted high demand (112.45 MW). Quantum optimizer effectively rerouted power to prevent grid failure.",
  "grid_state": {
    "nodes": [...],
    "links": [...]
  }
}
```

## 🛠 Features

- **RandomForestRegressor** accurately predicts power load demand based on synthetic temporal and weather data.
- **NetworkX** simulates complex power flows across substations.
- **Qiskit (Quantum Simulator)** generates probabilistic route weights mimicking QAOA to redistribute severe grid loads.
- **React Force Graph** visually animates overloaded nodes (pulsing red) and power flow traffic.
