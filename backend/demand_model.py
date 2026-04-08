import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import sys

# Ensure scripts path is accessible if run as module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from scripts.generate_data import generate_synthetic_data
except ImportError:
    pass

class DemandPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
        self.scaler = StandardScaler()
        self.data_path = os.path.join(os.path.dirname(__file__), 'data', 'synthetic_demand.csv')
        self._initialize_model()

    def _initialize_model(self):
        # Generate data if it doesn't exist
        if not os.path.exists(self.data_path):
            print("Data file not found. Generating realistic synthetic dataset...")
            if 'generate_synthetic_data' in globals():
                generate_synthetic_data(output_file=self.data_path)
            else:
                # If script import failed, duplicate minimal logic just in case
                os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
                df = pd.DataFrame({'hour': [12], 'temperature': [25], 'demand': [150]})
                df.to_csv(self.data_path, index=False)

        # Train the model
        df = pd.read_csv(self.data_path)
        if df.empty or len(df) < 10:
            return # safety catch
            
        X = df[['hour', 'temperature']]
        y = df['demand']
        
        # Scale inputs 
        X_scaled = self.scaler.fit_transform(X)
        
        self.model.fit(X_scaled, y)
        print("AI Model Trained Successfully with Realistic Data.")

    def predict_demand(self, hour: int, temperature: float) -> float:
        """
        Predicts total energy demand dynamically based on hour and temperature.
        """
        # Pass a DataFrame to avoid "X does not have valid feature names" warning
        input_df = pd.DataFrame({'hour': [hour], 'temperature': [temperature]})
        X_input = self.scaler.transform(input_df)
        prediction = self.model.predict(X_input)
        
        # Add small simulated real-world fluctuations
        import random
        noise = random.uniform(-2, 2)
        
        return float(prediction[0]) + noise

# Singleton instance for the app to use
demand_model = DemandPredictor()

def predict_demand(hour: int, temperature: float) -> float:
    return demand_model.predict_demand(hour, temperature)
